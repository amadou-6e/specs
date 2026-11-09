#!/usr/bin/env python3
"""Build a read-only traceability graph over specifications and report gaps.

The graph is derived deterministically from repository structure: Markdown
frontmatter, relative Markdown links, `related`/`supersedes` references, and
interaction IDs in visible Draw.io labels. It reports findings and never fails
on them; `validate_specs.py` remains the only enforcing check.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from validate_specs import IGNORED_PARTS, MARKDOWN_LINK, parse_frontmatter


ROOT = Path(__file__).resolve().parents[1]
LIFECYCLE_DOC = Path("shared/conventions/spec_lifecycle.md")
# PREFIX-NN or PREFIX-SNN (state IDs such as OV-S01).
ID_PATTERN = re.compile(r"(?<![\w-])([A-Z][A-Z0-9]{0,5})-(S?\d{1,4})(?![\w-])")
# Ranges: ED-06–10, OV-09..17, OV-15-17, and with the prefix repeated, ED-01 to ED-26.
ID_RANGE = re.compile(
    r"(?<![\w-])([A-Z][A-Z0-9]{0,5})-(S?)(\d{1,4})"
    r"(?:(?:–|\.\.|-)(?:\1-\2)?|\s*(?:–|to|through)\s*\1-\2)(\d{1,4})(?![\w-])"
)
MAX_RANGE = 60
# Lists: CA-06/07 names CA-06 and CA-07.
ID_LIST = re.compile(r"(?<![\w-])([A-Z][A-Z0-9]{0,5})-(S?)(\d{1,4})((?:/\d{1,4})+)(?![\w-])")
# Tokens that look like IDs but are standard names (UTF-8, SHA-256, ...).
NON_ID_PREFIXES = {"UTF", "SHA", "ISO", "RFC", "CVE", "TLS", "HTTP", "H264", "MP4"}
# Diagrams under these folders are history, not the current authority.
HISTORICAL_PARTS = {"archive", "deprecated", "legacy"}
HTML_TAG = re.compile(r"<[^>]+>")
FENCED_CODE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")


@dataclass
class Graph:
    nodes: dict[str, dict] = field(default_factory=dict)
    edges: set[tuple[str, str, str]] = field(default_factory=set)
    outgoing: dict[tuple[str, str], set[str]] = field(default_factory=lambda: defaultdict(set))
    incoming: dict[tuple[str, str], set[str]] = field(default_factory=lambda: defaultdict(set))

    def node(self, node_id: str, **attrs: object) -> None:
        self.nodes.setdefault(node_id, {}).update(attrs)

    def edge(self, source: str, kind: str, target: str) -> None:
        self.edges.add((source, kind, target))
        self.outgoing[source, kind].add(target)
        self.incoming[kind, target].add(source)

    def targets(self, source: str, kind: str) -> set[str]:
        return self.outgoing.get((source, kind), set())

    def sources(self, kind: str, target: str) -> set[str]:
        return self.incoming.get((kind, target), set())


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_historical(path: Path) -> bool:
    return any(part in HISTORICAL_PARTS for part in path.parts)


def find_ids(text: str) -> set[str]:
    found: set[str] = set()

    def expand(match: re.Match) -> str:
        prefix, state, start, end = match.groups()
        if prefix in NON_ID_PREFIXES or not 0 < int(end) - int(start) <= MAX_RANGE:
            return match.group(0)
        found.update(f"{prefix}-{state}{n:0{len(start)}d}" for n in range(int(start), int(end) + 1))
        return " "

    def expand_list(match: re.Match) -> str:
        prefix, state, first, rest = match.groups()
        if prefix in NON_ID_PREFIXES:
            return match.group(0)
        found.update(f"{prefix}-{state}{n}" for n in [first, *rest.split("/")[1:]])
        return " "

    remainder = ID_LIST.sub(expand_list, ID_RANGE.sub(expand, text))
    found.update(
        f"{prefix}-{number}"
        for prefix, number in ID_PATTERN.findall(remainder)
        if prefix not in NON_ID_PREFIXES
    )
    return found


def drawio_labels(path: Path) -> list[str]:
    """Return the visible label text of every cell, with HTML markup removed."""
    try:
        tree = ET.parse(path)
    except ET.ParseError:
        return []
    labels = []
    for cell in tree.iter():
        value = cell.get("value") or cell.get("label")
        if value:
            labels.append(html.unescape(HTML_TAG.sub(" ", html.unescape(value))))
    return labels


def project_files(project: Path, suffix: str) -> list[Path]:
    found: list[Path] = []
    for directory, names, filenames in os.walk(project):
        names[:] = sorted(name for name in names if name not in IGNORED_PARTS)
        found.extend(Path(directory) / name for name in sorted(filenames) if name.endswith(suffix))
    return found


def resolve_ref(project: Path, ref: str) -> Path | None:
    for candidate in (project / f"{ref}.md", project / ref / "README.md"):
        if candidate.exists():
            return candidate
    return None


def build_graph(root: Path) -> Graph:
    graph = Graph()
    root_prefix = os.path.normpath(root) + os.sep
    for project in sorted(p for p in (root / "projects").iterdir() if p.is_dir()):
        slug = project.name
        graph.node(f"project:{slug}", type="project")

        for path in project_files(project, ".drawio"):
            diagram = rel(path, root)
            historical = is_historical(path.relative_to(project))
            graph.node(diagram, type="diagram", project=slug, historical=historical)
            for label in drawio_labels(path):
                for found in find_ids(label):
                    graph.node(f"{slug}:{found}", type="id", project=slug)
                    graph.edge(diagram, "historical-defines" if historical else "defines", f"{slug}:{found}")

        for path in project_files(project, ".md"):
            doc = rel(path, root)
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            fields = parse_frontmatter(text) or {}
            graph.node(
                doc,
                type="doc",
                project=slug,
                title=fields.get("title"),
                status=fields.get("status"),
                kind=fields.get("kind"),
                last_reviewed=fields.get("last_reviewed"),
            )
            prose = FENCED_CODE.sub("", text)
            for found in find_ids(prose):
                graph.node(f"{slug}:{found}", type="id", project=slug)
                graph.edge(doc, "mentions", f"{slug}:{found}")
            for match in MARKDOWN_LINK.finditer(INLINE_CODE.sub("", prose)):
                target = match.group(1).split("#", 1)[0].strip().strip("<>")
                if not target or target.startswith("/"):
                    continue
                resolved = os.path.normpath(os.path.join(path.parent, target))
                if resolved.startswith(root_prefix) and os.path.isfile(resolved):
                    graph.edge(doc, "links", resolved[len(root_prefix):].replace(os.sep, "/"))
            for kind in ("related", "supersedes"):
                refs = fields.get(kind) or []
                for ref in [refs] if isinstance(refs, str) else refs:
                    target = resolve_ref(project, ref) if ref and ref != "null" else None
                    if target is not None:
                        graph.edge(doc, kind, rel(target, root))
    return graph


def lifecycle_statuses(root: Path) -> list[str]:
    path = root / LIFECYCLE_DOC
    if not path.exists():
        return []
    section = path.read_text(encoding="utf-8").split("## Statuses", 1)[-1].split("\n## ", 1)[0]
    return re.findall(r"^- `([a-z-]+)`:", section, re.MULTILINE)


def ids_by_prefix(ids: set[str]) -> str:
    return ", ".join(sorted(i.split(":", 1)[1] for i in ids))


def report(graph: Graph, root: Path, *, today: date, stale_days: int) -> str:
    lines = ["# Specification trace report", ""]
    lines.append(
        "Report-only: findings are prompts for review, not validation failures. "
        "IDs are read from visible Draw.io labels and Markdown prose."
    )
    projects = sorted(n.split(":", 1)[1] for n, a in graph.nodes.items() if a["type"] == "project")
    docs = {n: a for n, a in graph.nodes.items() if a["type"] == "doc"}

    lines += ["", "## Diagram interaction IDs", ""]
    for slug in projects:
        ids = {n for n, a in graph.nodes.items() if a["type"] == "id" and a["project"] == slug}
        defined = {i for i in ids if graph.sources("defines", i)}
        historical_only = {i for i in ids if graph.sources("historical-defines", i)} - defined
        if not defined and not historical_only:
            continue
        prefixes = {i.split(":", 1)[1].split("-", 1)[0] for i in defined}
        mentioned = {i for i in ids if graph.sources("mentions", i)}
        unprojected = defined - mentioned
        not_in_authority = {
            i for i in mentioned - defined - historical_only
            if i.split(":", 1)[1].split("-", 1)[0] in prefixes
        }
        lines.append(f"### {slug}")
        lines.append("")
        lines.append(f"- {len(defined)} IDs in current diagrams (prefixes: {', '.join(sorted(prefixes))}).")
        lines.append(f"- In a diagram but no Markdown mentions it: {len(unprojected)}"
                     + (f" ({ids_by_prefix(unprojected)})" if unprojected else ""))
        lines.append(f"- In Markdown with a diagram prefix but in no current diagram: {len(not_in_authority)}"
                     + (f" ({ids_by_prefix(not_in_authority)})" if not_in_authority else ""))
        if historical_only:
            lines.append(f"- Defined only in archived/deprecated/legacy diagrams: {len(historical_only)}")
        lines.append("")

    lines += ["## Interactions not cited by ID in ui-tests.md", ""]
    lines.append("A test may exist without citing its ID; uncited IDs cannot be traced to a test.")
    lines.append("")
    pairs = 0
    for doc in sorted(docs):
        if not doc.endswith("/interactions.md"):
            continue
        tests = doc[: -len("interactions.md")] + "ui-tests.md"
        if tests not in docs:
            continue
        pairs += 1
        missing = graph.targets(doc, "mentions") - graph.targets(tests, "mentions")
        lines.append(f"- `{doc}`: {len(missing)} of {len(graph.targets(doc, 'mentions'))} uncited"
                     + (f" ({ids_by_prefix(missing)})" if missing else ""))
    if not pairs:
        lines.append("- No interactions.md/ui-tests.md pairs found.")

    lines += ["", "## Lifecycle status", ""]
    lifecycle = lifecycle_statuses(root)
    counts = Counter(str(a["status"]) for a in docs.values() if a["status"])
    lines.append("- Counts: " + ", ".join(f"`{s}` {c}" for s, c in counts.most_common()))
    lines.append(f"- No frontmatter status: {sum(1 for a in docs.values() if not a['status'])} Markdown files")
    if lifecycle:
        outside = sorted(set(counts) - set(lifecycle))
        unused = [s for s in lifecycle if s not in counts]
        lines.append(f"- Statuses in use but not defined in `{LIFECYCLE_DOC.as_posix()}`: "
                     + (", ".join(f"`{s}`" for s in outside) or "none"))
        lines.append("- Lifecycle statuses never used: " + (", ".join(f"`{s}`" for s in unused) or "none"))

    stale = []
    for doc, attrs in docs.items():
        try:
            reviewed = date.fromisoformat(str(attrs["last_reviewed"]))
        except ValueError:
            continue
        if attrs["status"] not in {"archived", "superseded", "template"} and (today - reviewed).days > stale_days:
            stale.append(doc)
    lines.append(f"- Live docs with `last_reviewed` older than {stale_days} days: {len(stale)}")
    for doc in sorted(stale)[:20]:
        lines.append(f"  - `{doc}` ({docs[doc]['last_reviewed']})")

    lines += ["", "## Document links", ""]
    superseded_unlinked = sorted(
        d for d, a in docs.items()
        if a["status"] == "superseded" and not graph.targets(d, "links") | graph.targets(d, "supersedes")
    )
    lines.append(f"- `superseded` docs with no outgoing link to a replacement: {len(superseded_unlinked)}")
    for doc in superseded_unlinked[:20]:
        lines.append(f"  - `{doc}`")
    linked = {s for s, k, _ in graph.edges if k in {"links", "related", "supersedes"}}
    linked |= {t for _, k, t in graph.edges if k in {"links", "related", "supersedes"}}
    isolated = sorted(d for d, a in docs.items() if d not in linked and a["status"] != "template")
    lines.append(f"- Docs with no Markdown links in or out: {len(isolated)}")
    for doc in isolated[:20]:
        lines.append(f"  - `{doc}`")
    if len(isolated) > 20:
        lines.append(f"  - ... {len(isolated) - 20} more (see `--json`)")

    lines += ["", "## Other ID namespaces", ""]
    lines.append("Mentioned in Markdown without a Draw.io authority; their owners are not yet modeled.")
    lines.append("")
    for slug in projects:
        defined_prefixes = {
            n.split(":", 1)[1].split("-", 1)[0]
            for n, a in graph.nodes.items()
            if a["type"] == "id" and a["project"] == slug and graph.sources("defines", n)
        }
        other = Counter(
            n.split(":", 1)[1].split("-", 1)[0]
            for n, a in graph.nodes.items()
            if a["type"] == "id" and a["project"] == slug and graph.sources("mentions", n)
            and n.split(":", 1)[1].split("-", 1)[0] not in defined_prefixes
        )
        if other:
            lines.append(f"- {slug}: " + ", ".join(f"`{p}` {c}" for p, c in other.most_common(12)))
    return "\n".join(lines) + "\n"


def to_json(graph: Graph) -> dict:
    by_kind: dict[str, int] = defaultdict(int)
    for _, kind, _ in graph.edges:
        by_kind[kind] += 1
    return {
        "nodes": [{"id": n, **a} for n, a in sorted(graph.nodes.items())],
        "edges": [{"source": s, "kind": k, "target": t} for s, k, t in sorted(graph.edges)],
        "summary": {"nodes": len(graph.nodes), "edges_by_kind": dict(sorted(by_kind.items()))},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", type=Path, help="also write the graph as JSON to this path")
    parser.add_argument("--stale-days", type=int, default=180)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today(),
                        help="reference date for staleness (YYYY-MM-DD)")
    args = parser.parse_args(argv)

    graph = build_graph(ROOT)
    sys.stdout.reconfigure(encoding="utf-8")
    print(report(graph, ROOT, today=args.today, stale_days=args.stale_days), end="")
    if args.json:
        args.json.write_text(json.dumps(to_json(graph), indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

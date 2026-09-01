#!/usr/bin/env python3
"""Regenerate managed transition regions inside authoritative BlogHub Draw.io files.

The Draw.io files remain the sole authority. Review their diffs after running this
helper. Overview is managed by its view-local generator and is intentionally excluded.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Node:
    key: str
    title: str
    detail: str
    x: float
    y: float
    color: str = "#181C27"
    width: float = 270


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    label: str = ""
    dashed: bool = False


@dataclass(frozen=True)
class Band:
    label: str
    detail: str
    y: float
    height: float
    nodes: tuple[Node, ...]
    edges: tuple[Edge, ...]


@dataclass(frozen=True)
class Section:
    path: str
    page_id: str
    section_id: str
    offset_y: float
    width: float
    title: str
    subtitle: str
    bands: tuple[Band, ...]


def text_style(size: int, color: str, *, bold: bool = False) -> str:
    return (
        "text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;spacing=0;"
        "fontFamily=Arial;align=left;verticalAlign=top;letterSpacing=0;locked=1;"
        f"fontSize={size};fontColor={color};fontStyle={1 if bold else 0};"
    )


def vertex(
    root: ET.Element,
    cell_id: str,
    value: str,
    style: str,
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    cell = ET.SubElement(
        root,
        "mxCell",
        {"id": cell_id, "value": value, "style": style, "vertex": "1", "parent": "1"},
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        {"x": str(x), "y": str(y), "width": str(width), "height": str(height), "as": "geometry"},
    )


def state(root: ET.Element, prefix: str, node: Node) -> None:
    value = f"<b>{node.title}</b><br><font color=\"#8991AA\">{node.detail}</font>"
    vertex(
        root,
        prefix + node.key,
        value,
        "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=" + node.color + ";"
        "strokeColor=#2B3141;fontFamily=Arial;fontSize=15;fontColor=#E8EAF2;"
        "align=center;verticalAlign=middle;spacing=8;locked=1;",
        node.x,
        node.y,
        node.width,
        92,
    )


def edge(root: ET.Element, prefix: str, index: int, item: Edge) -> None:
    style = (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
        "endArrow=block;endFill=1;strokeColor=#69708A;fontColor=#4F554D;fontSize=12;"
        "fontFamily=Arial;labelBackgroundColor=#F3F4F1;locked=1;"
    )
    if item.dashed:
        style += "dashed=1;dashPattern=6 4;"
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": f"{prefix}edge-{index}",
            "value": item.label,
            "style": style,
            "edge": "1",
            "parent": "1",
            "source": prefix + item.source,
            "target": prefix + item.target,
        },
    )
    ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})


def section_height(section: Section) -> float:
    return max(band.y + band.height for band in section.bands) + 40


def generate(section: Section) -> None:
    path = ROOT / section.path
    tree = ET.parse(path)
    file_root = tree.getroot()
    diagram = next(
        page for page in file_root.findall("diagram") if page.get("id") == section.page_id
    )
    model = diagram.find("mxGraphModel")
    page_root = model.find("root")
    for cell in list(page_root):
        if cell.get("bloghubSection") == section.section_id:
            page_root.remove(cell)

    generated = ET.Element("root")
    prefix = section.section_id + "-"
    vertex(generated, prefix + "title", section.title, text_style(24, "#171914", bold=True), 60, 25, section.width - 120, 40)
    vertex(generated, prefix + "subtitle", section.subtitle, text_style(14, "#747970"), 60, 68, section.width - 120, 34)
    edge_index = 0
    for band_index, band in enumerate(section.bands):
        band_id = f"{prefix}band-{band_index}"
        vertex(
            generated,
            band_id,
            "",
            "rounded=0;whiteSpace=wrap;html=1;fillColor=#F3F4F1;strokeColor=#D8DBD4;locked=1;",
            40,
            band.y,
            section.width - 80,
            band.height,
        )
        vertex(generated, band_id + "-label", band.label, text_style(12, "#747970", bold=True), 75, band.y + 30, 390, 24)
        vertex(generated, band_id + "-detail", band.detail, text_style(13, "#4F554D"), 75, band.y + 66, 370, band.height - 90)
        for node in band.nodes:
            state(generated, prefix, node)
        for item in band.edges:
            edge_index += 1
            edge(generated, prefix, edge_index, item)

    for cell in generated:
        cell.set("bloghubSection", section.section_id)
        geo = cell.find("mxGeometry")
        if geo is not None and cell.get("parent") == "1" and geo.get("relative") != "1":
            geo.set("y", str(float(geo.get("y", "0")) + section.offset_y))
        page_root.append(cell)

    model.set("pageWidth", str(max(float(model.get("pageWidth", "0")), section.width)))
    model.set(
        "pageHeight",
        str(max(float(model.get("pageHeight", "0")), section.offset_y + section_height(section))),
    )
    file_root.set("pages", str(len(file_root.findall("diagram"))))
    ET.indent(tree, space="  ")
    tree.write(path, encoding="UTF-8", xml_declaration=True)


SECTIONS = (
    Section(
        "projects/blog-hub/views/create-article/create-article.drawio", "create-prompt", "create-prompt-transitions", 1370, 1880,
        "CREATE ARTICLE · PROMPT TRANSITIONS", "Brief and optional context become the input contract for configuration.",
        (Band("PROMPT AND CONTEXT", "Context may be a document, URL, web search, or omitted.", 130, 520,
            (Node("brief", "Write brief", "Required article intent", 450, 270), Node("context", "Add context", "File · URL · web search", 850, 270), Node("ready", "Brief ready", "Validated prompt", 1250, 270, "#173127"), Node("error", "Context error", "Explain and remain here", 850, 450, "#302027")),
                (Edge("brief", "context", "CA-09/10 · add context"), Edge("context", "ready", "CA-12 · Next"), Edge("context", "error", "SYSTEM · invalid file", True), Edge("error", "context", "CA-11 · remove / retry", True))),),
    ),
    Section(
        "projects/blog-hub/views/create-article/create-article.drawio", "create-configure", "create-configure-transitions", 1370, 1880,
        "CREATE ARTICLE · CONFIGURATION TRANSITIONS", "Format, provider, tone, and length must resolve before destinations.",
        (Band("CONFIGURE", "Back preserves the brief. Missing providers route to Settings.", 130, 520,
            (Node("format", "Choose format", "Article structure", 360, 270), Node("provider", "Choose provider", "Claude or Codex", 720, 270), Node("options", "Tone and length", "Generation controls", 1080, 270), Node("next", "Destinations", "Configuration valid", 1440, 270, "#173127"), Node("settings", "AI Settings", "Configure a provider", 720, 450, "#1F2740")),
            (Edge("format", "provider", "CA-13 · format"), Edge("provider", "options", "CA-14/15 · provider"), Edge("provider", "settings", "CA-16 · Settings", True), Edge("settings", "provider", "SYSTEM · return", True), Edge("options", "next", "CA-17/19 · Next"))),),
    ),
    Section(
        "projects/blog-hub/views/create-article/create-article.drawio", "create-destinations", "create-destinations-transitions", 1370, 1880,
        "CREATE ARTICLE · GENERATION TRANSITIONS", "Selected destinations accompany the generated canonical article into the Editor.",
        (Band("GENERATE", "The generation job disables navigation until it completes or fails.", 130, 560,
            (Node("dest", "Pick destinations", "Zero or more platforms", 280, 270), Node("generate", "Generate", "POST /api/agent/generate", 650, 270), Node("poll", "Poll job", "GET /api/jobs/:id", 1020, 270), Node("editor", "Editor", "Open generated article", 1390, 270, "#173127"), Node("error", "Generation failed", "Show error · retry", 1020, 470, "#302027")),
            (Edge("dest", "generate", "CA-20–23/27 · Generate"), Edge("generate", "poll", "SYSTEM · 202"), Edge("poll", "editor", "SYSTEM · done"), Edge("poll", "error", "SYSTEM · error", True), Edge("error", "generate", "CA-28 · Retry", True))),),
    ),
    Section(
        "projects/blog-hub/views/import-article/import-article.drawio", "import-upload", "import-upload-transitions", 1370, 2200,
        "IMPORT ARTICLE · SOURCE TRANSITIONS", "Upload and connected-platform paths converge on the same review state.",
        (Band("CHOOSE SOURCE", "Entry mode is fixed by the route; Cancel returns to the caller.", 130, 650,
            (Node("entry", "Entry mode", "Upload or platform", 430, 300), Node("file", "File drop", "Accept .md only", 800, 220), Node("platform", "Platform picker", "Connected platforms", 800, 420), Node("draft", "Draft list", "Select remote draft", 1170, 420), Node("review", "Review", "Editable title and preview", 1540, 300, "#173127"), Node("error", "Source error", "Stay and explain", 1170, 600, "#302027")),
            (Edge("entry", "file", "IM-14/15 · upload"), Edge("entry", "platform", "IM-05 · platform"), Edge("file", "review", "SYSTEM · valid markdown"), Edge("platform", "draft", "SYSTEM · fetched"), Edge("draft", "review", "IM-11/24 · Next"), Edge("file", "error", "SYSTEM · invalid", True), Edge("draft", "error", "SYSTEM · fetch failed", True), Edge("error", "entry", "IM-17/21 · Retry", True))),),
    ),
    Section(
        "projects/blog-hub/views/import-article/import-article.drawio", "import-review", "import-review-transitions", 1370, 1880,
        "IMPORT ARTICLE · REVIEW TRANSITIONS", "Review commits the imported markdown as a BlogHub article before opening Editor.",
        (Band("REVIEW AND IMPORT", "All actions are disabled while the import request is in flight.", 130, 720,
            (Node("review", "Review", "Edit title · inspect markdown", 280, 270), Node("import", "Importing", "POST /api/articles/import", 650, 270, "#1F2740"), Node("editor", "Editor", "201 created", 1020, 270, "#173127"), Node("error", "Import failed", "Banner · Try again", 650, 470, "#302027"), Node("cancel", "Return", "Overview or Create", 280, 630)),
            (Edge("review", "import", "IM-25 · Import"), Edge("import", "editor", "SYSTEM · 201"), Edge("import", "error", "SYSTEM · 4xx / 5xx", True), Edge("error", "review", "IM-21 · Try again", True), Edge("review", "cancel", "IM-22/23 · return", True))),),
    ),
    Section(
        "projects/blog-hub/views/editor/editor.drawio", "article-editor-assembly", "editor-transitions", 17220, 3350,
        "ARTICLE EDITOR · INTERACTION LIFECYCLE", "Autosave, review, comments, patches, preview, and cross-view exits.",
        (
            Band("LOAD AND AUTOSAVE", "Typing marks the document unsaved; two seconds of inactivity starts optimistic autosave.", 130, 500,
                (Node("load", "Load article", "GET /api/articles/:id", 400, 280), Node("idle", "Write · saved", "Editor ready", 800, 280, "#173127"), Node("dirty", "Unsaved", "Amber status", 1200, 280, "#302A18"), Node("save", "Autosave", "PATCH with revision", 1600, 280, "#1F2740"), Node("saved", "Saved revision", "New revision active", 2000, 280, "#173127"), Node("conflict", "Conflict / failure", "Keep local changes", 1600, 440, "#302027")),
                (Edge("load", "idle", "SYSTEM · loaded"), Edge("idle", "dirty", "ED-02/24 · edit"), Edge("dirty", "save", "SYSTEM · 2s idle"), Edge("save", "saved", "SYSTEM · saved"), Edge("save", "conflict", "SYSTEM · 409 / error", True), Edge("conflict", "dirty", "ED-02/24 · edit / retry", True))),
            Band("REVIEW, COMMENTS, AND PATCHES", "Agent patches are reviewed explicitly; acceptance applies the diff and creates a new revision.", 660, 620,
                (Node("write", "Write mode", "Canonical markdown", 500, 850), Node("review", "Review mode", "Comment anchors active", 920, 780), Node("comment", "Comment", "Resolve or Fix with AI", 1340, 780), Node("patch", "Patch pending", "Diff in Patches panel", 1760, 780, "#1F2740"), Node("accept", "Accept", "Apply diff", 2180, 730, "#173127"), Node("reject", "Reject", "Keep comment open", 2180, 930, "#302027"), Node("preview", "Preview", "Rendered markdown", 920, 1030)),
                (Edge("write", "review", "ED-03/06 · Review"), Edge("review", "write", "ED-26/27 · Done", True), Edge("review", "comment", "ED-19/23/25 · comment"), Edge("comment", "patch", "ED-34 · Fix with AI"), Edge("patch", "accept", "ED-36 · Accept"), Edge("patch", "reject", "ED-37 · Reject"), Edge("accept", "write", "SYSTEM · applied"), Edge("reject", "write", "SYSTEM · returned", True), Edge("write", "preview", "ED-43 · toggle"), Edge("preview", "write", "ED-43 · toggle", True))),
            Band("EXIT ROUTES", "Inspection and Articles navigation preserve the latest accepted or autosaved revision.", 1310, 380,
                (Node("ready", "Editor", "Current revision", 700, 1450), Node("inspect", "Inspection", "Run article checks", 1200, 1370, "#1F2740"), Node("overview", "Articles", "Return to overview", 1200, 1530)),
                (Edge("ready", "inspect", "ED-04/40 · Inspect"), Edge("ready", "overview", "ED-01 · back"))),
        ),
    ),
)


def main() -> None:
    for section in SECTIONS:
        generate(section)


if __name__ == "__main__":
    main()

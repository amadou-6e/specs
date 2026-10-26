"""Tests for trace_graph.py. Run: python -m unittest discover -s tools -p "test_*.py"."""

from __future__ import annotations

import tempfile
import textwrap
import unittest
from datetime import date
from pathlib import Path

import trace_graph


FRONTMATTER = "---\ntitle: {title}\nstatus: {status}\nkind: specification\nowners: [x]\nlast_reviewed: {reviewed}\napplies_to: [demo]\nsupersedes: null\nrelated: []\n---\n\n"
DRAWIO = """<?xml version='1.0' encoding='utf-8'?>
<mxfile><diagram id="d" name="d"><mxGraphModel><root>
<mxCell id="0"/>
<mxCell id="GI01" value="{labels}" vertex="1" parent="0"/>
</root></mxGraphModel></diagram></mxfile>
"""


class TraceGraphTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.write("shared/conventions/spec_lifecycle.md",
                   "# Lifecycle\n\n## Statuses\n\n- `draft`: x\n- `accepted`: y\n\n## Other\n\n- `ignored`: z\n")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def doc(self, relative: str, body: str, *, status: str = "draft", reviewed: str = "2026-10-01") -> None:
        self.write(relative, FRONTMATTER.format(title=relative, status=status, reviewed=reviewed) + textwrap.dedent(body))

    def build_report(self) -> tuple[trace_graph.Graph, str]:
        graph = trace_graph.build_graph(self.root)
        return graph, trace_graph.report(graph, self.root, today=date(2026, 10, 25), stale_days=180)

    def test_diagram_ids_come_from_labels_not_cell_ids(self) -> None:
        self.write("projects/demo/views/home/home.drawio",
                   DRAWIO.format(labels="&lt;b&gt;HM-01&lt;/b&gt; Save&#10;HM-S01 loading"))
        self.doc("projects/demo/views/home/interactions.md", "- `HM-01` saves.\n- `HM-02` is not drawn.\n")
        graph, text = self.build_report()
        defined = {t for s, k, t in graph.edges if k == "defines"}
        self.assertEqual(defined, {"demo:HM-01", "demo:HM-S01"})
        self.assertNotIn("demo:GI01", graph.nodes)
        self.assertIn("In a diagram but no Markdown mentions it: 1 (HM-S01)", text)
        self.assertIn("in no current diagram: 1 (HM-02)", text)

    def test_historical_diagrams_are_not_authority(self) -> None:
        self.write("projects/demo/ui/archive/old.drawio", DRAWIO.format(labels="HM-09"))
        self.write("projects/demo/views/home/home.drawio", DRAWIO.format(labels="HM-01"))
        self.doc("projects/demo/views/home/interactions.md", "HM-01 and HM-09\n")
        _, text = self.build_report()
        self.assertIn("in no current diagram: 0", text)
        self.assertIn("Defined only in archived/deprecated/legacy diagrams: 1", text)

    def test_interactions_without_ui_tests(self) -> None:
        self.write("projects/demo/views/home/home.drawio", DRAWIO.format(labels="HM-01 HM-02"))
        self.doc("projects/demo/views/home/interactions.md", "HM-01, HM-02\n")
        self.doc("projects/demo/views/home/ui-tests.md", "- [ ] `HM-01` works\n")
        _, text = self.build_report()
        self.assertIn("1 of 2 uncited (HM-02)", text)

    def test_id_ranges_expand(self) -> None:
        self.assertEqual(trace_graph.find_ids("ED-06–08"), {"ED-06", "ED-07", "ED-08"})
        self.assertEqual(trace_graph.find_ids("OV-09..10 and OV-S01-02"), {"OV-09", "OV-10", "OV-S01", "OV-S02"})
        self.assertEqual(trace_graph.find_ids("ED-01 to ED-03"), {"ED-01", "ED-02", "ED-03"})
        self.assertEqual(trace_graph.find_ids("OV-18 - 300 px"), {"OV-18"})
        self.assertEqual(trace_graph.find_ids("CA-06/07 · add"), {"CA-06", "CA-07"})

    def test_standard_names_and_code_blocks_are_not_ids(self) -> None:
        self.doc("projects/demo/a.md", "UTF-8 and SHA-256 text.\n\n```\nXX-01\n```\n")
        graph, _ = self.build_report()
        self.assertFalse([n for n, a in graph.nodes.items() if a["type"] == "id"])

    def test_links_statuses_and_staleness(self) -> None:
        self.doc("projects/demo/a.md", "See [b](b.md) and [missing](nope.md).\n")
        self.doc("projects/demo/b.md", "Back.\n", status="superseded")
        self.doc("projects/demo/c.md", "Alone.\n", status="complete", reviewed="2025-01-01")
        graph, text = self.build_report()
        self.assertIn(("projects/demo/a.md", "links", "projects/demo/b.md"), graph.edges)
        self.assertIn("Statuses in use but not defined in `shared/conventions/spec_lifecycle.md`: `complete`, `superseded`", text)
        self.assertIn("Lifecycle statuses never used: `accepted`", text)
        self.assertIn("older than 180 days: 1", text)
        self.assertIn("`superseded` docs with no outgoing link to a replacement: 1", text)
        self.assertIn("Docs with no Markdown links in or out: 1\n  - `projects/demo/c.md`", text)


if __name__ == "__main__":
    unittest.main()

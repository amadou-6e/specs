#!/usr/bin/env python3
"""Regenerate managed interaction markers in authoritative BlogHub Draw.io files.

The Draw.io files remain the sole authority. Review their diffs after running this
helper; Markdown interaction tables are projections of the IDs represented there.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SECTION_PREFIX = "bloghub-interaction-markers-"


@dataclass(frozen=True)
class Marker:
    label: str
    x: float
    y: float
    width: float = 78


@dataclass(frozen=True)
class Legend:
    x: float
    y: float
    width: float
    height: float
    rows: tuple[tuple[str, str], ...]
    columns: int = 2


@dataclass(frozen=True)
class Page:
    path: str
    page_id: str
    markers: tuple[Marker, ...]
    legend: Legend


def geometry(cell: ET.Element, x: float, y: float, width: float, height: float) -> None:
    ET.SubElement(cell, "mxGeometry", {
        "x": str(x), "y": str(y), "width": str(width), "height": str(height), "as": "geometry"
    })


def vertex(
    root: ET.Element,
    section: str,
    cell_id: str,
    value: str,
    style: str,
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    cell = ET.SubElement(root, "mxCell", {
        "id": cell_id,
        "value": value,
        "style": style,
        "vertex": "1",
        "parent": "1",
        "bloghubSection": section,
    })
    geometry(cell, x, y, width, height)


def text_style(size: int, color: str, *, bold: bool = False) -> str:
    return (
        "text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;spacing=0;"
        "fontFamily=Arial;align=left;verticalAlign=middle;letterSpacing=0;locked=1;"
        f"fontSize={size};fontColor={color};fontStyle={1 if bold else 0};"
    )


def badge(root: ET.Element, section: str, index: int, marker: Marker) -> None:
    vertex(
        root,
        section,
        f"{section}-badge-{index}",
        marker.label,
        "rounded=1;arcSize=18;whiteSpace=wrap;html=1;fillColor=#FBBF24;strokeColor=#171914;"
        "strokeWidth=2;fontFamily=Arial;fontSize=11;fontStyle=1;fontColor=#171914;"
        "align=center;verticalAlign=middle;spacing=0;locked=1;",
        marker.x,
        marker.y,
        marker.width,
        24,
    )


def add_legend(root: ET.Element, section: str, legend: Legend) -> None:
    vertex(
        root,
        section,
        section + "-legend-background",
        "",
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#F3F4F1;strokeColor=#D8DBD4;locked=1;",
        legend.x,
        legend.y,
        legend.width,
        legend.height,
    )
    vertex(
        root,
        section,
        section + "-legend-title",
        "INTERACTION INDEX",
        text_style(18, "#171914", bold=True),
        legend.x + 28,
        legend.y + 20,
        legend.width - 56,
        32,
    )
    vertex(
        root,
        section,
        section + "-legend-help",
        "Amber IDs mark interactive geometry. Matching edge IDs show the user action; SYSTEM marks automatic work.",
        text_style(11, "#747970"),
        legend.x + 28,
        legend.y + 54,
        legend.width - 56,
        42,
    )
    row_count = (len(legend.rows) + legend.columns - 1) // legend.columns
    column_width = (legend.width - 56) / legend.columns
    row_height = max(44, (legend.height - 118) / max(row_count, 1))
    for index, (label, description) in enumerate(legend.rows):
        column = index // row_count
        row = index % row_count
        x = legend.x + 28 + column * column_width
        y = legend.y + 105 + row * row_height
        badge(root, section, 1000 + index, Marker(label, x, y, 88))
        vertex(
            root,
            section,
            f"{section}-legend-text-{index}",
            description,
            text_style(11, "#4F554D"),
            x + 100,
            y - 2,
            column_width - 108,
            30,
        )


PAGES = (
    Page(
        "projects/blog-hub/views/create-article/create-article.drawio",
        "create-prompt",
        (
            Marker("CA-01", 700, 18), Marker("CA-02", 875, 18), Marker("CA-03", 1040, 18),
            Marker("CA-04", 1405, 18), Marker("CA-05", 1080, 430), Marker("CA-06/07", 690, 655, 92),
            Marker("CA-08", 1045, 655), Marker("CA-09/10", 1050, 765, 92), Marker("CA-12", 1710, 1185),
        ),
        Legend(1220, 585, 570, 500, (
            ("CA-01–04", "Navigation and reset"), ("CA-05", "Edit article brief"),
            ("CA-06/07", "Load a brief template"), ("CA-08", "Save current template"),
            ("CA-09/10", "Browse for or drop context"), ("CA-11", "Remove uploaded context"),
            ("CA-12", "Continue to Configure"),
        ), 1),
    ),
    Page(
        "projects/blog-hub/views/create-article/create-article.drawio",
        "create-configure",
        (
            Marker("CA-01", 700, 18), Marker("CA-02", 875, 18), Marker("CA-03", 1040, 18),
            Marker("CA-04", 1405, 18), Marker("CA-13", 1080, 420), Marker("CA-14/15", 1050, 785, 92),
            Marker("CA-17", 1070, 980), Marker("CA-18", 75, 1185), Marker("CA-19", 1710, 1185),
        ),
        Legend(1220, 585, 570, 500, (
            ("CA-01–04", "Navigation and reset"), ("CA-13", "Choose article format"),
            ("CA-14/15", "Choose AI provider"), ("CA-16", "Open AI Settings"),
            ("CA-17", "Set target word count"), ("CA-18", "Return to Prompt"),
            ("CA-19", "Continue to Destinations"),
        ), 1),
    ),
    Page(
        "projects/blog-hub/views/create-article/create-article.drawio",
        "create-destinations",
        (
            Marker("CA-01", 700, 18), Marker("CA-02", 875, 18), Marker("CA-03", 1040, 18),
            Marker("CA-04", 1405, 18), Marker("CA-20/21", 1000, 420, 92), Marker("CA-22", 1000, 510),
            Marker("CA-23", 1000, 600), Marker("CA-25", 680, 455), Marker("CA-26", 75, 1185),
            Marker("CA-27", 935, 1185),
        ),
        Legend(1140, 330, 650, 650, (
            ("CA-01–04", "Navigation and reset"), ("CA-20/21", "Toggle Medium"),
            ("CA-22", "Toggle Hashnode"), ("CA-23", "Toggle Dev.to"),
            ("CA-24/25", "Reconnect or configure platform"), ("CA-26", "Return to Configure"),
            ("CA-27", "Generate article"), ("CA-28", "Retry failed generation"),
        ), 1),
    ),
    Page(
        "projects/blog-hub/views/import-article/import-article.drawio",
        "import-upload",
        (
            Marker("IM-01", 700, 18), Marker("IM-02", 875, 18), Marker("IM-03", 1040, 18),
            Marker("IM-14–16", 1030, 390, 92), Marker("IM-24", 1710, 1185),
        ),
        Legend(1350, 300, 700, 560, (
            ("IM-01–03", "Navigation"), ("IM-04", "Open platform Settings"),
            ("IM-05/06", "Choose connected platform"), ("IM-07–13", "Search and select remote draft"),
            ("IM-14–16", "Browse, drop, or drag file"), ("IM-17", "Retry invalid upload"),
            ("IM-22", "Back or return"), ("IM-24", "Continue to Review"),
        ), 1),
    ),
    Page(
        "projects/blog-hub/views/import-article/import-article.drawio",
        "import-review",
        (
            Marker("IM-01", 700, 18), Marker("IM-02", 875, 18), Marker("IM-03", 1040, 18),
            Marker("IM-18", 950, 390), Marker("IM-22", 95, 1185), Marker("IM-23", 300, 1185),
            Marker("IM-25", 760, 1185),
        ),
        Legend(1030, 410, 720, 620, (
            ("IM-01–03", "Navigation"), ("IM-18", "Edit imported title"),
            ("IM-19", "Open preview link"), ("IM-20", "Select article in multi-import"),
            ("IM-21", "Retry failed import"), ("IM-22", "Back or return"),
            ("IM-23", "Start over"), ("IM-25", "Import and open Editor"),
        ), 1),
    ),
    Page(
        "projects/blog-hub/views/editor/editor.drawio",
        "article-editor-assembly",
        (
            Marker("ED-01", 88, 105), Marker("ED-02", 850, 105), Marker("ED-03", 1600, 105),
            Marker("ED-04", 1710, 105), Marker("ED-05", 1800, 105), Marker("ED-06–10", 720, 164, 92),
            Marker("ED-11–19", 690, 207, 92), Marker("ED-24/25", 1015, 330, 92),
            Marker("ED-28", 75, 285), Marker("ED-29–33", 365, 500, 92),
            Marker("ED-43", 1870, 285), Marker("ED-44/46", 1700, 265, 92),
            Marker("ED-34", 2770, 7645), Marker("ED-35", 2770, 7680),
            Marker("ED-36", 2245, 8250), Marker("ED-37", 2400, 8250),
            Marker("ED-39", 2770, 8935), Marker("ED-40", 2645, 9035),
            Marker("ED-41/42", 2640, 9735, 92),
        ),
        Legend(2020, 40, 1250, 730, (
            ("ED-01–05", "Top navigation, title, review, inspect, publish"),
            ("ED-06–10", "AI action strip"), ("ED-11–19", "Formatting and comment tools"),
            ("ED-20–25", "Selection popover and article editing"),
            ("ED-26/27", "Generation overlay actions"), ("ED-28–33", "Panel and accordion controls"),
            ("ED-34/35", "Fix or resolve comment"), ("ED-36/37", "Accept or reject patch"),
            ("ED-38–40", "Destination link, retry, inspect"), ("ED-41/42", "Chat input and send"),
            ("ED-43–46", "Preview controls"), ("ED-47", "Autosave failure and retry state"),
        )),
    ),
    Page(
        "projects/blog-hub/views/settings/settings.drawio",
        "settings-platforms",
        (
            Marker("ST-01", 700, 18), Marker("ST-02", 875, 18), Marker("ST-03", 1040, 18),
            Marker("ST-04", 220, 160), Marker("ST-05", 220, 205), Marker("ST-06", 220, 330),
            Marker("ST-07", 1280, 260), Marker("ST-14", 1110, 360), Marker("ST-15", 1200, 445),
            Marker("ST-16", 1290, 445), Marker("ST-07", 2370, 1585), Marker("ST-08", 2480, 2245),
            Marker("ST-12/18", 2370, 2525, 92), Marker("ST-16/17", 2430, 3250, 92),
            Marker("ST-19", 2370, 3545),
        ),
        Legend(1900, 40, 1660, 810, (
            ("ST-01–06", "Navigation and Settings sections"), ("ST-07", "Open connection method"),
            ("ST-08", "Start browser login"), ("ST-09–13", "Enter, save, cancel, or learn about token"),
            ("ST-14/15", "Test or update connection"), ("ST-16–18", "Disconnect confirmation"),
            ("ST-19", "Reconnect expired connection"),
        )),
    ),
    Page(
        "projects/blog-hub/views/settings/settings.drawio",
        "settings-ai-providers",
        (
            Marker("ST-01", 700, 18), Marker("ST-02", 875, 18), Marker("ST-03", 1040, 18),
            Marker("ST-04", 220, 160), Marker("ST-05", 220, 205), Marker("ST-06", 220, 330),
            Marker("ST-20", 840, 325), Marker("ST-21", 1040, 325),
            Marker("ST-20", 840, 500), Marker("ST-21", 1040, 500),
        ),
        Legend(1900, 40, 1660, 810, (
            ("ST-20", "Start provider browser login"), ("ST-21–24", "Add, save, cancel, or learn about API key"),
            ("ST-25–28", "Anthropic callback and polling"), ("ST-29–31", "OpenAI device code and polling"),
            ("ST-32/33", "Test or update provider"), ("ST-34–36", "Remove confirmation"),
        )),
    ),
    Page(
        "projects/blog-hub/views/settings/settings.drawio",
        "settings-account",
        (
            Marker("ST-01", 700, 18), Marker("ST-02", 875, 18), Marker("ST-03", 1040, 18),
            Marker("ST-04", 220, 160), Marker("ST-05", 220, 205), Marker("ST-06", 220, 330),
        ),
        Legend(700, 500, 900, 360, (
            ("ST-01–03", "Primary navigation"), ("ST-04", "Open Platforms"),
            ("ST-05", "Open AI Providers"), ("ST-06", "Open Account"),
        )),
    ),
)


EDGE_LABELS = {
    "settings-platforms": {
        "edge-h-1": "ST-07 · Connect",
        "edge-h-2": "ST-08 · Browser",
        "edge-h-3": "SYSTEM · tab closed",
        "edge-h-4": "SYSTEM · verified",
        "edge-h-retry": "ST-19 · Retry",
        "edge-h-sync": "SYSTEM · durable job",
        "edge-m-1": "ST-08 · Connect",
        "edge-m-2": "SYSTEM · tab closed",
        "edge-m-3": "SYSTEM · verified",
        "edge-m-retry": "ST-19 · Retry",
        "edge-m-sync": "SYSTEM · durable job",
    },
    "settings-ai-providers": {
        "ai-key-1": "ST-21 · Add API key",
        "ai-key-2": "ST-22 · Save",
        "ai-key-3": "SYSTEM · valid",
        "ai-key-fail": "SYSTEM · rejected",
        "ai-key-retry": "ST-22 · edit / retry",
        "ai-key-cancel": "ST-23 · Cancel",
        "ai-anthropic-1": "SYSTEM · authorized",
        "ai-anthropic-2": "ST-26 · Submit",
        "ai-anthropic-3": "SYSTEM · accepted",
        "ai-openai-1": "ST-20 · Open URL",
        "ai-openai-2": "SYSTEM · approved",
        "ai-browser-anthropic-ok": "SYSTEM · connected",
        "ai-browser-openai-ok": "SYSTEM · connected",
        "ai-browser-anthropic-fail": "SYSTEM · error / timeout",
        "ai-browser-openai-fail": "SYSTEM · error / timeout",
        "ai-browser-retry": "ST-20 · Try again",
        "ai-maint-1": "ST-32 · Test",
        "ai-maint-2": "SYSTEM · response",
        "ai-maint-3": "SYSTEM · remain connected",
        "ai-maint-4": "ST-33 · Update key",
        "ai-maint-5": "ST-22 · valid key",
        "ai-maint-6": "ST-34 · Remove",
        "ai-maint-7": "ST-36 · Cancel",
        "ai-maint-8": "ST-35 · Confirm remove",
    },
}


def generate(page: Page) -> None:
    path = ROOT / page.path
    tree = ET.parse(path)
    file_root = tree.getroot()
    diagram = next(item for item in file_root.findall("diagram") if item.get("id") == page.page_id)
    root = diagram.find("mxGraphModel/root")
    section = SECTION_PREFIX + page.page_id
    for cell in list(root):
        if cell.get("bloghubSection") == section:
            root.remove(cell)
    for index, marker in enumerate(page.markers):
        badge(root, section, index, marker)
    add_legend(root, section, page.legend)
    labels = EDGE_LABELS.get(page.page_id, {})
    for cell in root.findall("mxCell"):
        if cell.get("id") in labels:
            cell.set("value", labels[cell.get("id")])
    ET.indent(tree, space="  ")
    tree.write(path, encoding="UTF-8", xml_declaration=True)


def main() -> None:
    for page in PAGES:
        generate(page)


if __name__ == "__main__":
    main()

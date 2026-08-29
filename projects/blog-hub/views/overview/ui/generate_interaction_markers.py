"""Regenerate the managed contract regions in the authoritative Overview Draw.io.

The Draw.io remains the sole authority; this helper is only a deterministic editor for
tagged geometry and must be reviewed through the resulting Draw.io diff.
"""

from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET


HERE = Path(__file__).resolve().parent
DRAWIO = HERE.parent / "overview.drawio"
PAGE_ID = "overview-main"
SECTION = "overview-interaction-markers"
TRANSITION_SECTION = "overview-transitions"
CONTROL_SECTION = "overview-contract-controls"


def geometry(cell: ET.Element, x: float, y: float, width: float, height: float) -> None:
    ET.SubElement(
        cell,
        "mxGeometry",
        {"x": str(x), "y": str(y), "width": str(width), "height": str(height), "as": "geometry"},
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
    *,
    section: str = SECTION,
) -> None:
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": cell_id,
            "value": value,
            "style": style,
            "vertex": "1",
            "parent": "1",
            "bloghubSection": section,
        },
    )
    geometry(cell, x, y, width, height)


def text_style(size: int, color: str, *, bold: bool = False) -> str:
    return (
        "text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;spacing=0;"
        "fontFamily=Arial;align=left;verticalAlign=middle;letterSpacing=0;locked=1;"
        f"fontSize={size};fontColor={color};fontStyle={1 if bold else 0};"
    )


def badge(root: ET.Element, cell_id: str, label: str, x: float, y: float, width: float = 82) -> None:
    vertex(
        root,
        cell_id,
        label,
        "rounded=1;arcSize=18;whiteSpace=wrap;html=1;fillColor=#FBBF24;strokeColor=#171914;"
        "strokeWidth=2;fontFamily=Arial;fontSize=11;fontStyle=1;fontColor=#171914;"
        "align=center;verticalAlign=middle;spacing=0;locked=1;",
        x,
        y,
        width,
        24,
    )


def legend_row(root: ET.Element, index: int, label: str, description: str, x: float, y: float) -> None:
    badge(root, f"overview-marker-legend-{index}", label, x, y, 96)
    vertex(
        root,
        f"overview-marker-legend-text-{index}",
        description,
        text_style(14, "#4F554D"),
        x + 116,
        y - 2,
        390,
        30,
    )


def state(root: ET.Element, cell_id: str, title: str, detail: str, x: float, y: float, *, color: str = "#181C27") -> None:
    vertex(
        root,
        cell_id,
        f"<b>{title}</b><br><font color=\"#8991AA\">{detail}</font>",
        "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=" + color + ";"
        "strokeColor=#2B3141;fontFamily=Arial;fontSize=14;fontColor=#E8EAF2;"
        "align=center;verticalAlign=middle;spacing=8;locked=1;",
        x,
        y,
        260,
        76,
        section=TRANSITION_SECTION,
    )


def edge(root: ET.Element, index: int, source: str, target: str, label: str, *, dashed: bool = False) -> None:
    style = (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
        "endArrow=block;endFill=1;strokeColor=#69708A;fontColor=#4F554D;fontSize=11;"
        "fontFamily=Arial;labelBackgroundColor=#F3F4F1;locked=1;"
    )
    if dashed:
        style += "dashed=1;dashPattern=6 4;"
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": f"overview-transitions-edge-{index}",
            "value": label,
            "style": style,
            "edge": "1",
            "parent": "1",
            "source": f"overview-transitions-{source}",
            "target": f"overview-transitions-{target}",
            "bloghubSection": TRANSITION_SECTION,
        },
    )
    ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})


def band(root: ET.Element, index: int, label: str, detail: str, y: float, height: float) -> None:
    vertex(
        root,
        f"overview-transitions-band-{index}",
        "",
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#F3F4F1;strokeColor=#D8DBD4;locked=1;",
        40,
        y,
        3520,
        height,
        section=TRANSITION_SECTION,
    )
    vertex(root, f"overview-transitions-band-{index}-label", label, text_style(12, "#747970", bold=True), 75, y + 24, 330, 24, section=TRANSITION_SECTION)
    vertex(root, f"overview-transitions-band-{index}-detail", detail, text_style(13, "#4F554D"), 75, y + 55, 330, height - 75, section=TRANSITION_SECTION)


def add_contract_controls(root: ET.Element) -> None:
    # The full-page reconstruction pre-dates the Platforms tab and split action.
    for cell_id in ("18", "19", "20"):
        cell = root.find(f"mxCell[@id='{cell_id}']")
        if cell is None:
            continue
        geo = cell.find("mxGeometry")
        if cell_id == "18":
            geo.set("x", "1205")
        elif cell_id == "19":
            geo.set("x", "1405")
        else:
            geo.set("x", "1420")

    settings = root.find("mxCell[@id='18']")
    nav_style = settings.get("style")
    vertex(root, "overview-nav-platforms", "Platforms", nav_style, 1040, 50, 145, 40, section=CONTROL_SECTION)
    vertex(
        root,
        "overview-new-article-primary",
        "New article",
        "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#6366F1;strokeColor=#4F52D9;"
        "fontFamily=Arial;fontSize=12.6;fontStyle=1;fontColor=#FFFFFF;align=center;verticalAlign=middle;locked=1;",
        1640,
        52,
        130,
        36,
        section=CONTROL_SECTION,
    )
    vertex(
        root,
        "overview-new-article-menu",
        "v",
        "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#6366F1;strokeColor=#4F52D9;"
        "fontFamily=Arial;fontSize=12.6;fontStyle=1;fontColor=#FFFFFF;align=center;verticalAlign=middle;locked=1;",
        1770,
        52,
        34,
        36,
        section=CONTROL_SECTION,
    )


def add_transition_contract(root: ET.Element) -> None:
    vertex(root, "overview-transitions-title", "OVERVIEW - AUTHORITATIVE INTERACTION LIFECYCLE", text_style(24, "#171914", bold=True), 60, 6525, 3400, 40, section=TRANSITION_SECTION)
    vertex(root, "overview-transitions-subtitle", "Desktop states, uniquely identified user actions, and automatic collection/job transitions. Mobile sidebar behavior is out of scope.", text_style(14, "#747970"), 60, 6570, 3400, 34, section=TRANSITION_SECTION)

    band(root, 0, "LOAD AND COLLECTION", "Initial responses distinguish loaded, empty, and failed states.", 6630, 340)
    state(root, "overview-transitions-loading", "Loading", "OV-S01 - five skeletons", 470, 6740, color="#1F2740")
    state(root, "overview-transitions-browse", "Browse", "OV-S02 - articles", 900, 6740, color="#173127")
    state(root, "overview-transitions-first-empty", "First-run empty", "OV-S03 - New article", 1330, 6665)
    state(root, "overview-transitions-load-error", "Load error", "OV-S04 - retry load", 1330, 6815, color="#302027")
    edge(root, 1, "loading", "browse", "OV-S02 - articles")
    edge(root, 2, "loading", "first-empty", "OV-S03 - empty")
    edge(root, 3, "loading", "load-error", "OV-S04 - failed", dashed=True)
    edge(root, 4, "load-error", "loading", "OV-34 / OV-S01", dashed=True)

    band(root, 1, "FILTER AND SELECTION", "Preview tabs stay local; Visit is the only external card action.", 6990, 410)
    state(root, "overview-transitions-filter-browse", "Filtered browse", "OV-09..17 / OV-S05", 470, 7100)
    state(root, "overview-transitions-filter-empty", "Filtered empty", "OV-S06 - Clear filters", 850, 7100)
    state(root, "overview-transitions-selected-open", "Selected - open", "OV-18 - 300 px details", 1230, 7100, color="#1F2740")
    state(root, "overview-transitions-selected-collapsed", "Selected - collapsed", "OV-28 - 12 px strip", 1610, 7100, color="#1F2740")
    state(root, "overview-transitions-selection-cleared", "Selection cleared", "OV-S14 - absent/removed", 1990, 7100)
    edge(root, 5, "filter-browse", "filter-empty", "OV-S06 - no matches")
    edge(root, 6, "filter-empty", "browse", "OV-24 / OV-S05")
    edge(root, 7, "browse", "filter-browse", "OV-09..17 / OV-S05")
    edge(root, 8, "selected-open", "selected-collapsed", "OV-28 - collapse")
    edge(root, 9, "selected-collapsed", "selected-open", "OV-28 - expand", dashed=True)
    edge(root, 10, "selected-open", "selected-open", "OV-19..21 - preview")
    edge(root, 11, "selected-open", "selection-cleared", "OV-S14 - removed", dashed=True)
    edge(root, 23, "filter-browse", "selected-open", "OV-18 - select")

    band(root, 2, "PAGINATION", "Existing cards remain visible while another page loads or fails.", 7420, 300)
    state(root, "overview-transitions-page-browse", "Browse", "Next page available", 470, 7520)
    state(root, "overview-transitions-page-loading", "Page loading", "OV-26 - three skeletons", 900, 7520, color="#1F2740")
    state(root, "overview-transitions-page-failed", "Page failed", "OV-S08 - inline retry", 1330, 7520, color="#302027")
    state(root, "overview-transitions-page-appended", "Page appended", "OV-S07 - unique articles", 1760, 7520, color="#173127")
    edge(root, 12, "page-browse", "page-loading", "OV-26 - Load more")
    edge(root, 13, "page-loading", "page-appended", "OV-S07 - success")
    edge(root, 14, "page-loading", "page-failed", "OV-S08 - failed", dashed=True)
    edge(root, 15, "page-failed", "page-loading", "OV-27 - Retry", dashed=True)

    band(root, 3, "DURABLE ARTICLE JOB", "Queued, running, completed, failed, retained, and removed outcomes remain explicit.", 7740, 420)
    state(root, "overview-transitions-job-selected", "Selected - open", "OV-29 primary / OV-31 inspect", 470, 7880)
    state(root, "overview-transitions-job-queued", "Job queued", "OV-S09 - accepted", 850, 7880, color="#1F2740")
    state(root, "overview-transitions-job-running", "Job running", "OV-S10 - polling", 1230, 7880, color="#1F2740")
    state(root, "overview-transitions-job-failed", "Job failed", "OV-S12 - retryable", 1610, 7800, color="#302027")
    state(root, "overview-transitions-job-done", "Job completed", "OV-S11 - refresh", 1610, 7960, color="#173127")
    state(root, "overview-transitions-job-retained", "Selection retained", "OV-S13 - repopulate", 1990, 7960, color="#173127")
    state(root, "overview-transitions-job-removed", "Selection cleared", "OV-S14 - article absent", 2370, 7960)
    edge(root, 16, "job-selected", "job-queued", "OV-S09 - 202")
    edge(root, 17, "job-queued", "job-running", "OV-S10 - running")
    edge(root, 18, "job-running", "job-failed", "OV-S12 - error", dashed=True)
    edge(root, 19, "job-failed", "job-queued", "OV-33 - Retry", dashed=True)
    edge(root, 20, "job-running", "job-done", "OV-S11 - done")
    edge(root, 21, "job-done", "job-retained", "OV-S13 - still present")
    edge(root, 22, "job-done", "job-removed", "OV-S14 - absent", dashed=True)

    band(root, 4, "VIEW EXITS", "Only Visit leaves BlogHub; preview tabs remain in Overview.", 8180, 400)
    state(root, "overview-transitions-overview", "Overview", "Current desktop state", 470, 8310)
    state(root, "overview-transitions-queue", "Publish Queue", "OV-02 / OV-32", 850, 8240, color="#1F2740")
    state(root, "overview-transitions-platforms", "Platforms", "OV-03", 1230, 8240, color="#1F2740")
    state(root, "overview-transitions-settings", "Settings", "OV-04", 1610, 8240, color="#1F2740")
    state(root, "overview-transitions-create", "Create Article", "OV-05 / OV-25", 1990, 8240, color="#1F2740")
    state(root, "overview-transitions-import", "Import Article", "OV-07 / OV-08", 850, 8400, color="#1F2740")
    state(root, "overview-transitions-editor", "Editor", "OV-23 / OV-30", 1230, 8400, color="#1F2740")
    state(root, "overview-transitions-remote", "Remote article", "OV-22 - new tab", 1610, 8400, color="#173127")
    edge(root, 24, "overview", "queue", "OV-02 / OV-32")
    edge(root, 25, "overview", "platforms", "OV-03")
    edge(root, 26, "overview", "settings", "OV-04")
    edge(root, 27, "overview", "create", "OV-05 / OV-25")
    edge(root, 28, "overview", "import", "OV-07 / OV-08")
    edge(root, 29, "overview", "editor", "OV-23 / OV-30")
    edge(root, 30, "overview", "remote", "OV-22 - external")


def main() -> None:
    tree = ET.parse(DRAWIO)
    file_root = tree.getroot()
    diagram = next(page for page in file_root.findall("diagram") if page.get("id") == PAGE_ID)
    root = diagram.find("mxGraphModel/root")
    for cell in list(root):
        if cell.get("bloghubSection") in {SECTION, TRANSITION_SECTION, CONTROL_SECTION}:
            root.remove(cell)

    add_contract_controls(root)

    # Markers on the reconstructed screen.
    markers = (
        ("overview-marker-ov01", "OV-01", 748, 18, 68),
        ("overview-marker-ov02", "OV-02", 913, 18, 68),
        ("overview-marker-ov03", "OV-03", 1078, 18, 68),
        ("overview-marker-ov04", "OV-04", 1243, 18, 68),
        ("overview-marker-ov05-06", "OV-05/06", 1690, 18, 88),
        ("overview-marker-ov09", "OV-09", 305, 168, 68),
        ("overview-marker-ov10-14", "OV-10-14", 900, 168, 88),
        ("overview-marker-ov15-17", "OV-15-17", 1370, 168, 88),
        ("overview-marker-ov18", "OV-18", 180, 330, 68),
        ("overview-marker-ov19", "OV-19", 345, 185, 68),
        ("overview-marker-ov20", "OV-20", 540, 185, 68),
        ("overview-marker-ov21", "OV-21", 735, 185, 68),
        ("overview-marker-ov22", "OV-22", 1398, 497, 68),
        ("overview-marker-ov23", "OV-23", 1507, 497, 68),
        ("overview-marker-ov28", "OV-28", 903, 5409, 68),
        ("overview-marker-ov29", "OV-29", 1450, 6106, 68),
        ("overview-marker-ov30", "OV-30", 1062, 6275, 68),
        ("overview-marker-ov31", "OV-31", 1236, 6275, 68),
        ("overview-marker-ov32", "OV-32", 1412, 6275, 68),
    )
    for marker in markers:
        badge(root, *marker)

    # Interaction index in the otherwise unused right side of the page canvas.
    vertex(
        root,
        "overview-marker-legend-background",
        "",
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#F3F4F1;strokeColor=#D8DBD4;locked=1;",
        1900,
        40,
        1660,
        820,
    )
    vertex(root, "overview-marker-legend-title", "OVERVIEW · INTERACTION INDEX", text_style(24, "#171914", bold=True), 1940, 72, 1500, 40)
    vertex(
        root,
        "overview-marker-legend-help",
        "Amber OV IDs identify user controls. OV-S IDs identify automatic transitions. The lifecycle below is authoritative; this index is its control legend.",
        text_style(14, "#747970"),
        1940,
        118,
        1450,
        56,
    )
    rows = (
        ("OV-01", "Keep Articles active"),
        ("OV-02", "Open Publish Queue"),
        ("OV-03", "Open Platforms"),
        ("OV-04", "Open Settings"),
        ("OV-05", "Create a new article"),
        ("OV-06", "Toggle import menu"),
        ("OV-07", "Import from platform"),
        ("OV-08", "Upload a Markdown file"),
        ("OV-09", "Search articles"),
        ("OV-10", "Clear status filter"),
        ("OV-11", "Filter Drafting"),
        ("OV-12", "Filter Ready"),
        ("OV-13", "Filter Error"),
        ("OV-14", "Filter Published"),
        ("OV-15", "Toggle Medium filter"),
        ("OV-16", "Toggle Hashnode filter"),
        ("OV-17", "Toggle Dev.to filter"),
        ("OV-18", "Select or change article"),
        ("OV-19", "Show Medium preview"),
        ("OV-20", "Show Hashnode preview"),
        ("OV-21", "Show Dev.to preview"),
        ("OV-22", "Visit active remote article"),
        ("OV-23", "Edit card article"),
        ("OV-24", "Clear empty-result filters"),
        ("OV-25", "Create from first-run empty"),
        ("OV-26", "Load next article page"),
        ("OV-27", "Retry next-page load"),
        ("OV-28", "Collapse or expand details panel"),
        ("OV-29", "Run visible primary action"),
        ("OV-30", "Edit selected article"),
        ("OV-31", "Inspect selected article"),
        ("OV-32", "Schedule selected article"),
        ("OV-33", "Retry failed article job"),
        ("OV-34", "Retry initial collection load"),
    )
    for index, (label, description) in enumerate(rows):
        column = index // 12
        row = index % 12
        legend_row(root, index, label, description, 1940 + column * 535, 190 + row * 54)

    add_transition_contract(root)

    model = diagram.find("mxGraphModel")
    model.set("pageHeight", "8660")

    ET.indent(tree, space="  ")
    tree.write(DRAWIO, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    main()

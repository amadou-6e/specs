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
ACTION_SECTION = "overview-card-actions"
JOB_STUDY_SECTION = "overview-job-state-study"


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


def gate_badge(
    root: ET.Element,
    cell_id: str,
    label: str,
    x: float,
    y: float,
    *,
    fill: str,
    stroke: str,
    text: str,
    width: float = 104,
) -> None:
    vertex(
        root,
        cell_id,
        label,
        "rounded=1;arcSize=18;whiteSpace=wrap;html=1;fillColor=" + fill + ";"
        "strokeColor=" + stroke + ";strokeWidth=2;fontFamily=Arial;fontSize=11;"
        "fontStyle=1;fontColor=" + text + ";align=center;verticalAlign=middle;"
        "spacing=0;locked=1;",
        x,
        y,
        width,
        28,
        section=ACTION_SECTION,
    )


def study_panel(
    root: ET.Element,
    cell_id: str,
    title: str,
    detail: str,
    x: float,
    y: float,
    *,
    color: str = "#1F2740",
    status: str = "",
) -> None:
    vertex(
        root,
        cell_id,
        "",
        "rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#10131C;"
        "strokeColor=#2B3141;strokeWidth=2;locked=1;",
        x,
        y,
        500,
        250,
        section=JOB_STUDY_SECTION,
    )
    vertex(root, cell_id + "-title", title, text_style(16, "#E8EAF2", bold=True), x + 24, y + 22, 450, 32, section=JOB_STUDY_SECTION)
    vertex(root, cell_id + "-detail", detail, text_style(13, "#8991AA"), x + 24, y + 62, 450, 70, section=JOB_STUDY_SECTION)
    vertex(
        root,
        cell_id + "-status",
        status,
        "rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=" + color + ";"
        "strokeColor=#2B3141;fontFamily=Arial;fontSize=12;fontStyle=1;"
        "fontColor=#E8EAF2;align=left;verticalAlign=middle;spacingLeft=14;locked=1;",
        x + 24,
        y + 148,
        452,
        54,
        section=JOB_STUDY_SECTION,
    )


def add_gate_and_context_study(root: ET.Element) -> None:
    # Live card controls on the reconstructed first article.
    gate_badge(root, "overview-main-gate-pass", "PASS - INSPECT", 1248, 277, fill="#173127", stroke="#22C55E", text="#86EFAC", width=126)
    vertex(
        root,
        "overview-main-context-trigger",
        "...",
        "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#181C27;"
        "strokeColor=#2B3141;fontFamily=Arial;fontSize=16;fontStyle=1;"
        "fontColor=#C9CFE0;align=center;verticalAlign=middle;locked=1;",
        1510,
        277,
        42,
        32,
        section=ACTION_SECTION,
    )

    # Isolated component states sit in unused canvas space, beside the approved card studies.
    vertex(root, "overview-actions-background", "", "rounded=0;whiteSpace=wrap;html=1;fillColor=#F3F4F1;strokeColor=#D8DBD4;locked=1;", 2500, 920, 1060, 1000, section=ACTION_SECTION)
    vertex(root, "overview-actions-title", "GATE BADGES AND CARD CONTEXT ACTIONS", text_style(22, "#171914", bold=True), 2540, 950, 960, 38, section=ACTION_SECTION)
    vertex(root, "overview-actions-help", "Faithful card states for issue #98. Gate status is visible without opening the menu; only completed Pass, Warn, and Fail gates navigate to Inspection.", text_style(14, "#747970"), 2540, 995, 940, 56, section=ACTION_SECTION)

    gate_badge(root, "overview-gate-pass", "PASS", 2540, 1080, fill="#173127", stroke="#22C55E", text="#86EFAC")
    gate_badge(root, "overview-gate-warn", "WARN", 2670, 1080, fill="#302A17", stroke="#FBBF24", text="#FDE68A")
    gate_badge(root, "overview-gate-fail", "FAIL", 2800, 1080, fill="#302027", stroke="#EF4444", text="#FCA5A5")
    gate_badge(root, "overview-gate-pending", "PENDING", 2930, 1080, fill="#181C27", stroke="#5A6080", text="#8991AA", width=118)
    vertex(root, "overview-gate-note", "OV-S15 renders gate data. OV-35 opens Inspection for Pass / Warn / Fail. Pending is passive.", text_style(13, "#4F554D"), 3080, 1072, 420, 46, section=ACTION_SECTION)

    vertex(root, "overview-context-card", "<b>RAG Pipeline with Neo4j and LangChain</b><br><font color=\"#8991AA\">Apr 5 - 2,100 words</font>", "rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#10131C;strokeColor=#2B3141;fontFamily=Arial;fontSize=14;fontColor=#E8EAF2;align=left;verticalAlign=top;spacing=18;locked=1;", 2540, 1160, 620, 150, section=ACTION_SECTION)
    gate_badge(root, "overview-context-card-gate", "WARN", 2560, 1258, fill="#302A17", stroke="#FBBF24", text="#FDE68A")
    vertex(root, "overview-context-trigger", "...", "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#181C27;strokeColor=#2B3141;fontFamily=Arial;fontSize=16;fontStyle=1;fontColor=#C9CFE0;align=center;verticalAlign=middle;locked=1;", 3092, 1178, 42, 32, section=ACTION_SECTION)
    vertex(root, "overview-context-menu", "<b>Edit</b><br><br>Duplicate<br><br>Archive<br><br><font color=\"#FCA5A5\">Delete</font>", "rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#181C27;strokeColor=#3A4155;fontFamily=Arial;fontSize=14;fontColor=#C9CFE0;align=left;verticalAlign=top;spacing=16;locked=1;", 3180, 1160, 320, 240, section=ACTION_SECTION)
    for cell_id, label, x, y in (
        ("overview-marker-ov37", "OV-37", 3400, 1180),
        ("overview-marker-ov38", "OV-38", 3400, 1232),
        ("overview-marker-ov39", "OV-39", 3400, 1284),
        ("overview-marker-ov40", "OV-40", 3400, 1336),
    ):
        badge(root, cell_id, label, x, y, 72)

    vertex(root, "overview-delete-confirm", "<b>Delete this article?</b><br><font color=\"#8991AA\">Published copies are not removed.</font>", "rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#181C27;strokeColor=#EF4444;fontFamily=Arial;fontSize=14;fontColor=#E8EAF2;align=left;verticalAlign=top;spacing=16;locked=1;", 2540, 1440, 460, 160, section=ACTION_SECTION)
    vertex(root, "overview-delete-cancel", "Cancel", "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#181C27;strokeColor=#3A4155;fontFamily=Arial;fontSize=13;fontColor=#C9CFE0;align=center;verticalAlign=middle;locked=1;", 2710, 1545, 110, 36, section=ACTION_SECTION)
    vertex(root, "overview-delete-confirm-button", "Delete", "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#EF4444;strokeColor=#DC2626;fontFamily=Arial;fontSize=13;fontStyle=1;fontColor=#FFFFFF;align=center;verticalAlign=middle;locked=1;", 2830, 1545, 140, 36, section=ACTION_SECTION)
    badge(root, "overview-marker-ov42", "OV-42", 2700, 1588, 72)
    badge(root, "overview-marker-ov41", "OV-41", 2864, 1588, 72)

    vertex(root, "overview-context-conflict", "<b>Cannot delete published article</b><br><font color=\"#FCA5A5\">Remove its live destinations first. The article and history remain unchanged.</font>", "rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#302027;strokeColor=#EF4444;fontFamily=Arial;fontSize=14;fontColor=#E8EAF2;align=left;verticalAlign=middle;spacing=16;locked=1;", 3040, 1440, 460, 160, section=ACTION_SECTION)
    vertex(root, "overview-context-error-note", "404, 409, and other mutation failures replace the action row with an inline card message. No alert or modal is used.", text_style(13, "#4F554D"), 2540, 1660, 960, 58, section=ACTION_SECTION)


def add_job_state_study(root: ET.Element) -> None:
    vertex(root, "overview-job-study-background", "", "rounded=0;whiteSpace=wrap;html=1;fillColor=#F3F4F1;strokeColor=#D8DBD4;locked=1;", 1650, 4520, 1910, 1880, section=JOB_STUDY_SECTION)
    vertex(root, "overview-job-study-title", "DURABLE ARTICLE ACTION - PANEL STATES", text_style(22, "#171914", bold=True), 1690, 4550, 1800, 38, section=JOB_STUDY_SECTION)
    vertex(root, "overview-job-study-help", "The selected panel remains open. The same visible operation, job ID, and idempotency key survive polling and reload recovery.", text_style(14, "#747970"), 1690, 4595, 1760, 54, section=JOB_STUDY_SECTION)

    panels = (
        ("submitting", "Submitting action", "Push drafts is being accepted. Action buttons are disabled before the first response.", "#1F2740", "Submitting - duplicate actions disabled"),
        ("queued", "Queued", "Job 7F2A is durable. Polling continues at the documented interval.", "#1F2740", "Queued - waiting for a worker"),
        ("running", "Running", "Job 7F2A is publishing to Medium and Hashnode.", "#1F2740", "Running - 2 of 3 destinations"),
        ("recovering", "Recovering after reload", "Overview is discovering the selected article's active durable job.", "#302A17", "Checking durable jobs..."),
        ("retrying", "Retrying", "The failed job is being retried through its durable retry endpoint.", "#302A17", "Retrying - action buttons disabled"),
        ("failed", "Failed", "Hashnode authentication expired. Failure remains visible until retry or another action.", "#302027", "Failed - authentication required"),
        ("canceled", "Canceled", "The backend reports a terminal cancellation. Retry remains available when supported.", "#302027", "Canceled - no work is running"),
        ("completed", "Completed", "Fresh article and destination data replace the stale panel copy.", "#173127", "Completed - collection refreshed"),
        ("recovery-warning", "Recovery unavailable", "Active-job discovery failed. Keep the article selected and allow an explicit retry.", "#302A17", "Could not restore job status"),
    )
    for index, (slug, title, detail, color, status) in enumerate(panels):
        column = index % 3
        row = index // 3
        study_panel(root, "overview-job-study-" + slug, title, detail, 1690 + column * 610, 4670 + row * 330, color=color, status=status)

    for cell_id, label, x, y, marker_id, marker_label, marker_x in (
        ("overview-job-study-failed-retry", "Retry", 3270, 5210, "overview-job-study-retry-failed", "OV-33", 3185),
        ("overview-job-study-canceled-retry", "Retry", 2050, 5540, "overview-job-study-retry-canceled", "OV-33", 1965),
        ("overview-job-study-recovery-retry", "Retry recovery", 3230, 5540, "overview-marker-ov43", "OV-43", 3145),
    ):
        vertex(root, cell_id, label, "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#181C27;strokeColor=#3A4155;fontFamily=Arial;fontSize=12;fontStyle=1;fontColor=#C9CFE0;align=center;verticalAlign=middle;locked=1;", x, y, 116 if label == "Retry" else 156, 34, section=JOB_STUDY_SECTION)
        badge(root, marker_id, marker_label, marker_x, y + 5, 72)
    vertex(root, "overview-job-study-rule", "Duplicate prevention: OV-29 and OV-31 are disabled in Submitting, Queued, Running, Recovering, and Retrying. A repeated idempotency key reattaches to the existing job through OV-S22 and never creates another job.", text_style(13, "#4F554D"), 1690, 5690, 1760, 88, section=JOB_STUDY_SECTION)


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

    band(root, 3, "GATE AND CONTEXT ACTIONS", "Gate navigation is separate from card selection. Context mutations keep confirmation and failures inline.", 7740, 500)
    state(root, "overview-transitions-card", "Article card", "Gate + context available", 470, 7900)
    state(root, "overview-transitions-inspection", "Inspection", "OV-35 - completed gate", 850, 7820, color="#1F2740")
    state(root, "overview-transitions-context-open", "Context open", "OV-36 - menu", 850, 7980, color="#1F2740")
    state(root, "overview-transitions-mutation", "Mutation pending", "OV-38 / OV-39 / OV-41", 1230, 7980, color="#1F2740")
    state(root, "overview-transitions-delete-confirm", "Delete confirmation", "OV-40 - inline", 1230, 7820, color="#302A17")
    state(root, "overview-transitions-mutation-done", "Collection refreshed", "OV-S16 / OV-S17 / OV-S18", 1610, 7980, color="#173127")
    state(root, "overview-transitions-mutation-missing", "Article not found", "OV-S19 - inline 404", 1990, 7820, color="#302027")
    state(root, "overview-transitions-mutation-conflict", "Delete conflict", "OV-S20 - inline 409", 1990, 7980, color="#302027")
    state(root, "overview-transitions-mutation-error", "Action failed", "OV-S21 - inline error", 1990, 8140, color="#302027")
    edge(root, 31, "card", "inspection", "OV-35")
    edge(root, 32, "card", "context-open", "OV-36")
    edge(root, 33, "context-open", "delete-confirm", "OV-40")
    edge(root, 34, "delete-confirm", "context-open", "OV-42", dashed=True)
    edge(root, 35, "context-open", "mutation", "OV-38 / OV-39")
    edge(root, 36, "delete-confirm", "mutation", "OV-41")
    edge(root, 37, "mutation", "mutation-done", "OV-S16 / S17 / S18")
    edge(root, 38, "mutation", "mutation-missing", "OV-S19", dashed=True)
    edge(root, 39, "mutation", "mutation-conflict", "OV-S20", dashed=True)
    edge(root, 40, "mutation", "mutation-error", "OV-S21", dashed=True)
    edge(root, 51, "context-open", "card", "OV-36 / Esc / outside", dashed=True)

    band(root, 4, "DURABLE ARTICLE JOB", "Submission, idempotency, polling, cancellation, retry, and reload recovery remain visible in the selected panel.", 8260, 940)
    state(root, "overview-transitions-job-selected", "Selected - open", "OV-29 primary / OV-31 inspect", 470, 8400)
    state(root, "overview-transitions-job-submitting", "Submitting", "Actions disabled", 850, 8400, color="#1F2740")
    state(root, "overview-transitions-job-queued", "Job queued", "OV-S09 / OV-S22", 1230, 8400, color="#1F2740")
    state(root, "overview-transitions-job-running", "Job running", "OV-S10 - durable polling", 1610, 8400, color="#1F2740")
    state(root, "overview-transitions-job-failed", "Job failed", "OV-S12 / OV-S30", 1990, 8320, color="#302027")
    state(root, "overview-transitions-job-done", "Job completed", "OV-S11 - refresh", 1990, 8480, color="#173127")
    state(root, "overview-transitions-job-canceled", "Job canceled", "OV-S23 - terminal", 1990, 8640, color="#302027")
    state(root, "overview-transitions-job-retrying", "Retrying", "OV-33 - actions disabled", 2370, 8320, color="#302A17")
    state(root, "overview-transitions-job-retained", "Selection retained", "OV-S13 - fresh detail", 2370, 8480, color="#173127")
    state(root, "overview-transitions-job-removed", "Selection cleared", "OV-S14 - article absent", 2750, 8480)
    state(root, "overview-transitions-job-recovering", "Recovering after reload", "OV-S26 - discover active jobs", 470, 8820, color="#302A17")
    state(root, "overview-transitions-job-recovery-warning", "Recovery unavailable", "OV-S29 - inline retry", 850, 8820, color="#302A17")
    state(root, "overview-transitions-job-no-active", "No active job", "OV-S28 - fresh selected state", 1230, 8820, color="#173127")
    edge(root, 16, "job-selected", "job-submitting", "OV-29 / OV-31")
    edge(root, 17, "job-submitting", "job-queued", "OV-S09")
    edge(root, 18, "job-submitting", "job-queued", "OV-S22", dashed=True)
    edge(root, 19, "job-queued", "job-running", "OV-S10")
    edge(root, 20, "job-running", "job-failed", "OV-S12 / OV-S30", dashed=True)
    edge(root, 21, "job-running", "job-done", "OV-S11")
    edge(root, 22, "job-running", "job-canceled", "OV-S23", dashed=True)
    edge(root, 41, "job-failed", "job-retrying", "OV-33", dashed=True)
    edge(root, 42, "job-canceled", "job-retrying", "OV-33", dashed=True)
    edge(root, 43, "job-retrying", "job-queued", "OV-S24")
    edge(root, 44, "job-retrying", "job-failed", "OV-S25", dashed=True)
    edge(root, 45, "job-done", "job-retained", "OV-S13")
    edge(root, 46, "job-done", "job-removed", "OV-S14", dashed=True)
    edge(root, 47, "job-recovering", "job-queued", "OV-S27 queued", dashed=True)
    edge(root, 48, "job-recovering", "job-running", "OV-S27 running", dashed=True)
    edge(root, 49, "job-recovering", "job-no-active", "OV-S28")
    edge(root, 50, "job-recovering", "job-recovery-warning", "OV-S29", dashed=True)
    edge(root, 52, "job-recovery-warning", "job-recovering", "OV-43", dashed=True)

    band(root, 5, "VIEW EXITS", "Only Visit leaves BlogHub externally; preview tabs remain in Overview.", 9220, 400)
    state(root, "overview-transitions-overview", "Overview", "Current desktop state", 470, 9350)
    state(root, "overview-transitions-queue", "Publish Queue", "OV-02 / OV-32", 850, 9280, color="#1F2740")
    state(root, "overview-transitions-platforms", "Platforms", "OV-03", 1230, 9280, color="#1F2740")
    state(root, "overview-transitions-settings", "Settings", "OV-04", 1610, 9280, color="#1F2740")
    state(root, "overview-transitions-create", "Create Article", "OV-05 / OV-25", 1990, 9280, color="#1F2740")
    state(root, "overview-transitions-import", "Import Article", "OV-07 / OV-08", 850, 9440, color="#1F2740")
    state(root, "overview-transitions-editor", "Editor", "OV-23 / OV-30 / OV-37", 1230, 9440, color="#1F2740")
    state(root, "overview-transitions-remote", "Remote article", "OV-22 - new tab", 1610, 9440, color="#173127")
    edge(root, 24, "overview", "queue", "OV-02 / OV-32")
    edge(root, 25, "overview", "platforms", "OV-03")
    edge(root, 26, "overview", "settings", "OV-04")
    edge(root, 27, "overview", "create", "OV-05 / OV-25")
    edge(root, 28, "overview", "import", "OV-07 / OV-08")
    edge(root, 29, "overview", "editor", "OV-23 / OV-30 / OV-37")
    edge(root, 30, "overview", "remote", "OV-22 - external")


def main() -> None:
    tree = ET.parse(DRAWIO)
    file_root = tree.getroot()
    diagram = next(page for page in file_root.findall("diagram") if page.get("id") == PAGE_ID)
    root = diagram.find("mxGraphModel/root")
    for cell in list(root):
        if cell.get("bloghubSection") in {
            SECTION,
            TRANSITION_SECTION,
            CONTROL_SECTION,
            ACTION_SECTION,
            JOB_STUDY_SECTION,
        }:
            root.remove(cell)

    add_contract_controls(root)
    add_gate_and_context_study(root)
    add_job_state_study(root)

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
        ("overview-marker-ov35", "OV-35", 1268, 242, 68),
        ("overview-marker-ov36", "OV-36", 1498, 242, 68),
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
        860,
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
        ("OV-35", "Open completed gate inspection"),
        ("OV-36", "Toggle card context menu"),
        ("OV-37", "Edit from card context"),
        ("OV-38", "Duplicate article once"),
        ("OV-39", "Archive article"),
        ("OV-40", "Open inline delete confirmation"),
        ("OV-41", "Confirm article deletion"),
        ("OV-42", "Cancel article deletion"),
        ("OV-43", "Retry active-job recovery"),
    )
    for index, (label, description) in enumerate(rows):
        column = index // 15
        row = index % 15
        legend_row(root, index, label, description, 1940 + column * 535, 190 + row * 48)

    add_transition_contract(root)

    model = diagram.find("mxGraphModel")
    model.set("pageHeight", "9700")

    ET.indent(tree, space="  ")
    tree.write(DRAWIO, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    main()

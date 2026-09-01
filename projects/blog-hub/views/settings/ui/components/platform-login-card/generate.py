from __future__ import annotations

import base64
import copy
from pathlib import Path
import struct
import xml.etree.ElementTree as ET


HERE = Path(__file__).resolve().parent
DRAWIO = HERE.parents[2] / "settings.drawio"
CAPTURES = HERE / "references" / "states"
WORKSHOP_OFFSET_Y = 1370
WORKSHOP_SECTION = "platform-login-workshop"


def geometry(cell: ET.Element, x: float, y: float, width: float, height: float) -> None:
    geo = cell.find("mxGeometry")
    if geo is None:
        geo = ET.SubElement(cell, "mxGeometry", {"as": "geometry"})
    geo.attrib.update(
        x=str(x), y=str(y), width=str(width), height=str(height), **{"as": "geometry"}
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
    parent: str = "1",
) -> ET.Element:
    cell = ET.SubElement(
        root,
        "mxCell",
        {"id": cell_id, "value": value, "style": style, "vertex": "1", "parent": parent},
    )
    geometry(cell, x, y, width, height)
    return cell


def text_style(size: int, color: str, *, bold: bool = False, locked: bool = True) -> str:
    return (
        "text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;spacing=0;"
        "fontFamily=Arial;align=left;verticalAlign=top;letterSpacing=0;"
        f"fontSize={size};fontColor={color};fontStyle={1 if bold else 0};"
        f"locked={1 if locked else 0};"
    )


def image_style(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return (
        "shape=image;verticalLabelPosition=bottom;verticalAlign=top;imageAspect=0;"
        f"aspect=fixed;image=data:image/png%3Bbase64,{encoded};locked=1;"
    )


def set_style_property(cell: ET.Element, key: str, value: str | int) -> None:
    prefix = f"{key}="
    properties = [
        item for item in cell.get("style", "").split(";") if item and not item.startswith(prefix)
    ]
    properties.append(f"{key}={value}")
    cell.set("style", ";".join(properties) + ";")


def descendants(source_root: ET.Element, group_id: str) -> list[ET.Element]:
    ids = {group_id}
    changed = True
    while changed:
        changed = False
        for cell in source_root.findall("mxCell"):
            if cell.get("parent") in ids and cell.get("id") not in ids:
                ids.add(cell.get("id"))
                changed = True
    return [cell for cell in source_root.findall("mxCell") if cell.get("id") in ids]


def clone_group(
    source_root: ET.Element,
    target_root: ET.Element,
    template_id: str,
    new_id: str,
    x: float,
    y: float,
    *,
    values: dict[str, str] | None = None,
    styles: dict[str, str] | None = None,
    remove: set[str] | None = None,
) -> dict[str, ET.Element]:
    values = values or {}
    styles = styles or {}
    remove = remove or set()
    cells = descendants(source_root, template_id)
    mapping = {
        cell.get("id"): new_id + cell.get("id")[len(template_id):]
        for cell in cells
    }
    result: dict[str, ET.Element] = {}
    for original in cells:
        old_id = original.get("id")
        suffix = old_id[len(template_id):]
        if old_id in remove or suffix in remove:
            continue
        cell = copy.deepcopy(original)
        cell.set("id", mapping[old_id])
        parent = cell.get("parent")
        if parent in mapping:
            cell.set("parent", mapping[parent])
        if old_id in values or suffix in values:
            cell.set("value", values.get(old_id, values.get(suffix)))
        if old_id in styles or suffix in styles:
            cell.set("style", styles.get(old_id, styles.get(suffix)))
        target_root.append(cell)
        result[suffix] = cell
        result[old_id] = cell
    group = result[""]
    geo = group.find("mxGeometry")
    geo.set("x", str(x))
    geo.set("y", str(y))
    return result


def add_row(
    root: ET.Element,
    row_id: str,
    y: float,
    height: float,
    index: str,
    title: str,
    description: str,
    capture: str,
    note_title: str,
    note: str,
) -> None:
    vertex(
        root,
        f"{row_id}-background",
        "",
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#F3F4F1;strokeColor=#D8DBD4;locked=1;",
        40,
        y,
        3520,
        height,
    )
    vertex(root, f"{row_id}-index", index, text_style(12, "#747970", bold=True), 75, y + 34, 420, 24)
    vertex(root, f"{row_id}-title", title, text_style(22, "#171914", bold=True), 75, y + 70, 420, 42)
    vertex(root, f"{row_id}-description", description, text_style(14, "#747970"), 75, y + 122, 400, height - 150)

    path = CAPTURES / capture
    png = path.read_bytes()
    width, height = struct.unpack(">II", png[16:24])
    image_height = 1000 * height / width
    vertex(root, f"{row_id}-reference", "", image_style(path), 520, y + 66, 1000, image_height)
    vertex(root, f"{row_id}-note-title", note_title, text_style(12, "#747970", bold=True), 2730, y + 70, 720, 24)
    vertex(root, f"{row_id}-note", note, text_style(15, "#4F554D"), 2730, y + 105, 720, height - 135)


def add_edge(root: ET.Element, edge_id: str, source: str, target: str, value: str = "", *, dashed: bool = False) -> None:
    style = (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
        "endArrow=block;endFill=1;strokeColor=#69708A;fontColor=#4F554D;fontSize=13;"
        "labelBackgroundColor=#F3F4F1;"
    )
    if dashed:
        style += "dashed=1;dashPattern=6 4;"
    edge = ET.SubElement(
        root,
        "mxCell",
        {"id": edge_id, "value": value, "style": style, "edge": "1", "parent": "1", "source": source, "target": target},
    )
    ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})


def add_flow_box(root: ET.Element, box_id: str, label: str, x: float, y: float, *, color: str = "#181C27") -> None:
    vertex(
        root,
        box_id,
        label,
        "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=" + color + ";strokeColor=#2B3141;"
        "fontFamily=Arial;fontSize=16;fontStyle=1;fontColor=#E8EAF2;align=center;verticalAlign=middle;locked=1;",
        x,
        y,
        260,
        82,
    )


def main() -> None:
    tree = ET.parse(DRAWIO)
    file_root = tree.getroot()
    diagram = next(
        page
        for page in file_root.findall("diagram")
        if page.get("id") == "settings-platforms"
    )
    model = diagram.find("mxGraphModel")
    page_root = model.find("root")
    managed_cells = [
        cell
        for cell in page_root
        if cell.get("bloghubSection") == WORKSHOP_SECTION
    ]
    if not managed_cells:
        raise RuntimeError("The Settings page has no managed platform-login workshop")

    source_copy = ET.Element("root")
    for cell in managed_cells:
        source_copy.append(copy.deepcopy(cell))

    source_root = ET.Element("root")
    ET.SubElement(source_root, "mxCell", {"id": "0"})
    ET.SubElement(source_root, "mxCell", {"id": "1", "parent": "0"})

    vertex(source_root, "title", "BLOG PLATFORM LOGIN CARDS · VERIFIED STATES", text_style(26, "#171914", bold=True), 60, 25, 2400, 42)
    vertex(
        source_root,
        "subtitle",
        "Live references on the left, editable Draw.io geometry in the center, and the durable state contract on the right.",
        text_style(14, "#747970"),
        60,
        68,
        2600,
        34,
    )

    rows = [
        ("disconnected", 130, 300, "STATE 01", "Disconnected", "Hashnode offers one calm entry point before a login method is selected.", "hashnode-01-disconnected.png", "TRANSITION", "Connect opens the Hashnode method chooser. Medium skips the chooser and starts browser login directly."),
        ("method", 460, 580, "STATE 02 · HASHNODE ONLY", "Choose login method", "Hashnode Plus can use a token; free accounts use the persistent browser path.", "hashnode-02-method-choice.png", "METHOD CONTRACT", "API token opens credential entry and then connects. Browser login opens one Skyvern tab and enters the pending state."),
        ("waiting", 1070, 300, "STATE 03", "Waiting for browser sign-in", "The provider tab is open. BlogHub waits for the user to finish and close it.", "hashnode-03-waiting.png", "USER CONTROL", "Close the tab after the provider confirms login. Cancel closes the session and returns to Disconnected. There is no Open login action."),
        ("verifying", 1400, 300, "STATE 04", "Saving and verifying", "BlogHub closes no tabs here; it saves and verifies the browser profile after the user closes it.", "hashnode-04-verifying.png", "ATOMIC HANDOFF", "No card action is available while verification runs. Success enters Connected; an invalid or unavailable profile enters Failed."),
        ("connected", 1730, 330, "STATE 05", "Connected", "The verified method is explicit and synchronization is automatic.", "hashnode-05-connected.png", "BACKGROUND SYNC", "Connection queues an immediate durable import and a recurring 1-minute schedule. Disconnect is the only maintenance action."),
        ("failed", 2090, 300, "STATE 06", "Login failed", "Failure explains what did not complete and returns to the normal provider entry action.", "hashnode-06-failed.png", "RECOVERY", "Hashnode Connect returns to method choice. Medium Connect starts a fresh browser login. Neither provider reopens a stale session."),
    ]
    for row in rows:
        add_row(source_root, *row)

    disconnected = clone_group(source_copy, source_root, "disconnected-card", "disconnected-card", 1600, 196)
    geometry(disconnected[""], 1600, 196, 1000, 160)

    method = clone_group(
        source_copy,
        source_root,
        "disconnected-card",
        "method-card",
        1600,
        526,
        styles={
            "ect-chevron": "shape=triangle;direction=south;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=none;"
        },
    )
    geometry(method[""], 1600, 526, 1000, 160)
    menu = clone_group(
        source_copy,
        source_root,
        "method-menu-live",
        "method-menu-live",
        2160,
        700,
        values={"help": "Deterministic publishing for Hashnode Plus", "ser-help": "Isolated persistent browser for free accounts"},
    )
    geometry(menu[""], 2160, 700, 550, 320)
    menu_geometry = {
        "row": (10, 10, 530, 136),
        "icon": (30, 42, 65, 65),
        "title": (118, 24, 225, 40),
        "help": (118, 64, 320, 64),
        "badge": (438, 48, 73, 32),
        "der": (10, 154, 530, 2),
        "ser-row": (10, 164, 530, 144),
        "ser-icon": (30, 202, 65, 65),
        "ser-title": (118, 184, 240, 40),
        "ser-help": (118, 224, 320, 64),
        "ser-badge": (438, 208, 73, 32),
    }
    for cell_id, bounds in menu_geometry.items():
        geometry(menu[cell_id], *bounds)
    menu_font_sizes = {
        "icon": 18,
        "title": 26,
        "help": 19,
        "badge": 14,
        "ser-icon": 16,
        "ser-title": 26,
        "ser-help": 19,
        "ser-badge": 14,
    }
    for cell_id, size in menu_font_sizes.items():
        set_style_property(menu[cell_id], "fontSize", size)

    waiting = clone_group(
        source_copy,
        source_root,
        "disconnected-card",
        "waiting-card",
        1600,
        1136,
        values={"-status": "Finish signing in", "er": "Complete sign-in in the opened tab, then close it.", "ect": "Cancel"},
        styles={
            "-status-dot": "ellipse;whiteSpace=wrap;html=1;fillColor=#FBBF24;strokeColor=none;",
            "-status": text_style(22, "#FBBF24", locked=False).replace("verticalAlign=top", "verticalAlign=middle"),
            "ect": text_style(18, "#F87171", locked=False).replace("align=left", "align=center").replace("verticalAlign=top", "verticalAlign=middle"),
        },
        remove={"ect-chevron"},
    )
    geometry(waiting[""], 1600, 1136, 1000, 160)

    verifying = clone_group(
        source_copy,
        source_root,
        "disconnected-card",
        "verifying-card",
        1600,
        1466,
        values={"-status": "Verifying login", "er": "Saving and verifying the browser profile."},
        styles={
            "-status-dot": "ellipse;whiteSpace=wrap;html=1;fillColor=#FBBF24;strokeColor=none;",
            "-status": text_style(22, "#FBBF24", locked=False).replace("verticalAlign=top", "verticalAlign=middle"),
        },
        remove={"ect", "ect-chevron"},
    )
    geometry(verifying[""], 1600, 1466, 1000, 160)

    connected = clone_group(
        source_copy,
        source_root,
        "connected-card",
        "connected-card",
        1600,
        1796,
        values={"fied": "Articles sync automatically in the background."},
        styles={"fied": text_style(16, "#53658F", locked=False).replace("verticalAlign=top", "verticalAlign=middle")},
    )
    geometry(connected[""], 1600, 1796, 1000, 190)
    geometry(connected["fied"], 118, 109, 620, 30)

    failed = clone_group(
        source_copy,
        source_root,
        "disconnected-card",
        "failed-card",
        1600,
        2156,
        values={"-status": "Login failed", "er": "Hashnode sign-in was not completed in the browser"},
        styles={
            "-status-dot": "ellipse;whiteSpace=wrap;html=1;fillColor=#F87171;strokeColor=none;",
            "-status": text_style(22, "#F87171", locked=False).replace("verticalAlign=top", "verticalAlign=middle"),
        },
    )
    geometry(failed[""], 1600, 2156, 1000, 160)

    flow_y = 2420
    vertex(source_root, "flow-background", "", "rounded=0;whiteSpace=wrap;html=1;fillColor=#F3F4F1;strokeColor=#D8DBD4;locked=1;", 40, flow_y, 3520, 820)
    vertex(source_root, "flow-title", "CORE STATE TRANSITIONS", text_style(22, "#171914", bold=True), 75, flow_y + 34, 900, 38)
    vertex(source_root, "flow-subtitle", "Connection state controls the card. Synchronization runs beside it as durable work and does not add a manual card action.", text_style(14, "#747970"), 75, flow_y + 76, 1900, 34)

    vertex(source_root, "flow-hash-label", "HASHNODE", text_style(12, "#747970", bold=True), 75, flow_y + 154, 260, 24)
    hash_boxes = [("flow-h-disconnected", "Disconnected", 420), ("flow-h-method", "Method choice", 810), ("flow-h-waiting", "Waiting", 1200), ("flow-h-verifying", "Verifying", 1590), ("flow-h-connected", "Connected", 1980)]
    for box_id, label, x in hash_boxes:
        add_flow_box(source_root, box_id, label, x, flow_y + 130)
    add_flow_box(source_root, "flow-h-failed", "Failed", 1590, flow_y + 280, color="#302027")
    add_flow_box(source_root, "flow-h-sync", "Immediate import +\n1-minute schedule", 2370, flow_y + 130, color="#173127")
    add_edge(source_root, "edge-h-1", "flow-h-disconnected", "flow-h-method", "Connect")
    add_edge(source_root, "edge-h-2", "flow-h-method", "flow-h-waiting", "Browser")
    add_edge(source_root, "edge-h-3", "flow-h-waiting", "flow-h-verifying", "Tab closed")
    add_edge(source_root, "edge-h-4", "flow-h-verifying", "flow-h-connected", "Verified")
    add_edge(source_root, "edge-h-fail", "flow-h-verifying", "flow-h-failed", "", dashed=True)
    add_edge(source_root, "edge-h-retry", "flow-h-failed", "flow-h-method", "Retry", dashed=True)
    add_edge(source_root, "edge-h-sync", "flow-h-connected", "flow-h-sync", "Durable job", dashed=True)

    vertex(source_root, "flow-medium-label", "MEDIUM", text_style(12, "#747970", bold=True), 75, flow_y + 505, 260, 24)
    medium_boxes = [("flow-m-disconnected", "Disconnected", 420), ("flow-m-waiting", "Waiting", 920), ("flow-m-verifying", "Verifying", 1420), ("flow-m-connected", "Connected", 1920)]
    for box_id, label, x in medium_boxes:
        add_flow_box(source_root, box_id, label, x, flow_y + 480)
    add_flow_box(source_root, "flow-m-failed", "Failed", 1420, flow_y + 630, color="#302027")
    add_flow_box(source_root, "flow-m-sync", "Immediate import +\n1-minute schedule", 2370, flow_y + 480, color="#173127")
    add_edge(source_root, "edge-m-1", "flow-m-disconnected", "flow-m-waiting", "Connect")
    add_edge(source_root, "edge-m-2", "flow-m-waiting", "flow-m-verifying", "Tab closed")
    add_edge(source_root, "edge-m-3", "flow-m-verifying", "flow-m-connected", "Verified")
    add_edge(source_root, "edge-m-fail", "flow-m-verifying", "flow-m-failed", "", dashed=True)
    add_edge(source_root, "edge-m-retry", "flow-m-failed", "flow-m-waiting", "Retry", dashed=True)
    add_edge(source_root, "edge-m-sync", "flow-m-connected", "flow-m-sync", "Durable job", dashed=True)

    vertex(source_root, "return-title", "RETURN TRANSITIONS", text_style(12, "#747970", bold=True), 2850, flow_y + 154, 620, 24)
    vertex(
        source_root,
        "return-contract",
        "Hashnode API token saved: Method choice → Connected<br><br>Cancel: Waiting → Disconnected<br><br>Disconnect: Connected → Disconnected<br><br>Sync job failure: remain Connected; retry durably",
        text_style(15, "#4F554D"),
        2850,
        flow_y + 190,
        620,
        250,
    )

    for cell in managed_cells:
        page_root.remove(cell)
    for cell in source_root:
        if cell.get("id") in {"0", "1"}:
            continue
        cell.set("bloghubSection", WORKSHOP_SECTION)
        geo = cell.find("mxGeometry")
        if (
            geo is not None
            and cell.get("parent") == "1"
            and geo.get("relative") != "1"
            and geo.get("y") is not None
        ):
            geo.set("y", str(float(geo.get("y", "0")) + WORKSHOP_OFFSET_Y))
        page_root.append(cell)

    model.attrib.update(pageWidth="3600", pageHeight="4670", pageScale="1", page="1")

    ET.indent(tree, space="  ")
    tree.write(DRAWIO, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    main()

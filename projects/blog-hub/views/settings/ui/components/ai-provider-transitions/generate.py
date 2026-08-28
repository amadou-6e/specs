from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET


HERE = Path(__file__).resolve().parent
DRAWIO = HERE.parents[2] / "settings.drawio"
PAGE_ID = "settings-ai-providers"
SECTION = "ai-provider-transitions"
OFFSET_Y = 1370
SECTION_HEIGHT = 2260


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
) -> None:
    cell = ET.SubElement(
        root,
        "mxCell",
        {"id": cell_id, "value": value, "style": style, "vertex": "1", "parent": "1"},
    )
    geometry(cell, x, y, width, height)


def text_style(size: int, color: str, *, bold: bool = False) -> str:
    return (
        "text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;spacing=0;"
        "fontFamily=Arial;align=left;verticalAlign=top;letterSpacing=0;locked=1;"
        f"fontSize={size};fontColor={color};fontStyle={1 if bold else 0};"
    )


def add_state(
    root: ET.Element,
    cell_id: str,
    title: str,
    detail: str,
    x: float,
    y: float,
    *,
    color: str = "#181C27",
    width: float = 300,
) -> None:
    value = f"<b>{title}</b><br><font color=\"#8991AA\">{detail}</font>"
    vertex(
        root,
        cell_id,
        value,
        "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=" + color + ";"
        "strokeColor=#2B3141;fontFamily=Arial;fontSize=16;fontColor=#E8EAF2;"
        "align=center;verticalAlign=middle;spacing=8;locked=1;",
        x,
        y,
        width,
        100,
    )


def add_edge(
    root: ET.Element,
    cell_id: str,
    source: str,
    target: str,
    label: str = "",
    *,
    dashed: bool = False,
) -> None:
    style = (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
        "endArrow=block;endFill=1;strokeColor=#69708A;fontColor=#4F554D;fontSize=13;"
        "fontFamily=Arial;labelBackgroundColor=#F3F4F1;locked=1;"
    )
    if dashed:
        style += "dashed=1;dashPattern=6 4;"
    edge = ET.SubElement(
        root,
        "mxCell",
        {
            "id": cell_id,
            "value": label,
            "style": style,
            "edge": "1",
            "parent": "1",
            "source": source,
            "target": target,
        },
    )
    ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})


def add_band(root: ET.Element, cell_id: str, y: float, height: float, label: str, detail: str) -> None:
    vertex(
        root,
        cell_id,
        "",
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#F3F4F1;strokeColor=#D8DBD4;locked=1;",
        40,
        y,
        3520,
        height,
    )
    vertex(root, f"{cell_id}-label", label, text_style(12, "#747970", bold=True), 75, y + 34, 430, 24)
    vertex(root, f"{cell_id}-detail", detail, text_style(14, "#4F554D"), 75, y + 72, 400, height - 100)


def build_section() -> ET.Element:
    root = ET.Element("root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    vertex(root, "ai-flow-title", "AI PROVIDER CONNECTIONS · STATE TRANSITIONS", text_style(26, "#171914", bold=True), 60, 25, 2600, 42)
    vertex(
        root,
        "ai-flow-subtitle",
        "API keys and provider-specific browser authentication converge on one durable connected state.",
        text_style(14, "#747970"),
        60,
        68,
        2600,
        34,
    )

    add_band(root, "ai-key-band", 130, 500, "API KEY PATH", "Shared by Anthropic and OpenAI. Validation must succeed before credentials become active.")
    add_state(root, "ai-key-disconnected", "Not configured", "Choose browser login or API key", 560, 250)
    add_state(root, "ai-key-form", "Key form", "Enter key · Save · Cancel", 1050, 250)
    add_state(root, "ai-key-validating", "Validating", "Provider probe in progress", 1540, 250, color="#302A18")
    add_state(root, "ai-key-connected", "Connected", "Credential encrypted and available", 2030, 250, color="#173127")
    add_state(root, "ai-key-failed", "Validation failed", "Show reason · keep key form", 1540, 430, color="#302027")
    add_edge(root, "ai-key-1", "ai-key-disconnected", "ai-key-form", "Add API key")
    add_edge(root, "ai-key-2", "ai-key-form", "ai-key-validating", "Save")
    add_edge(root, "ai-key-3", "ai-key-validating", "ai-key-connected", "Valid")
    add_edge(root, "ai-key-fail", "ai-key-validating", "ai-key-failed", "Rejected", dashed=True)
    add_edge(root, "ai-key-retry", "ai-key-failed", "ai-key-form", "Edit + retry", dashed=True)
    add_edge(root, "ai-key-cancel", "ai-key-form", "ai-key-disconnected", "Cancel", dashed=True)

    add_band(root, "ai-browser-band", 660, 860, "BROWSER LOGIN PATHS", "Login starts in BlogHub, continues in the provider browser, and completes through CLI-runner status polling.")
    vertex(root, "ai-anthropic-label", "ANTHROPIC · LOOPBACK CALLBACK", text_style(12, "#747970", bold=True), 540, 725, 500, 24)
    add_state(root, "ai-anthropic-start", "Start CLI login", "Open provider authorization", 540, 790)
    add_state(root, "ai-anthropic-callback", "Callback URL", "Paste full loopback URL", 1020, 790)
    add_state(root, "ai-anthropic-submit", "Submit callback", "Backend forwards authorization code", 1500, 790)
    add_state(root, "ai-anthropic-poll", "Polling", "Check CLI login every 2 seconds", 1980, 790, color="#1F2740")
    add_edge(root, "ai-anthropic-1", "ai-anthropic-start", "ai-anthropic-callback", "Browser authorized")
    add_edge(root, "ai-anthropic-2", "ai-anthropic-callback", "ai-anthropic-submit", "Submit")
    add_edge(root, "ai-anthropic-3", "ai-anthropic-submit", "ai-anthropic-poll", "Accepted")

    vertex(root, "ai-openai-label", "OPENAI · DEVICE CODE", text_style(12, "#747970", bold=True), 540, 1045, 500, 24)
    add_state(root, "ai-openai-start", "Request device code", "Receive URL and one-time code", 540, 1110)
    add_state(root, "ai-openai-browser", "Provider browser", "Enter code and approve access", 1020, 1110)
    add_state(root, "ai-openai-poll", "Polling", "Check CLI login every 2 seconds", 1500, 1110, color="#1F2740")
    add_edge(root, "ai-openai-1", "ai-openai-start", "ai-openai-browser", "Open URL")
    add_edge(root, "ai-openai-2", "ai-openai-browser", "ai-openai-poll", "User approved")

    add_state(root, "ai-browser-connected", "Connected", "Reload provider card", 2580, 920, color="#173127")
    add_state(root, "ai-browser-failed", "Login failed", "Error or timeout · try again", 2580, 1240, color="#302027")
    add_edge(root, "ai-browser-anthropic-ok", "ai-anthropic-poll", "ai-browser-connected", "Connected")
    add_edge(root, "ai-browser-openai-ok", "ai-openai-poll", "ai-browser-connected", "Connected")
    add_edge(root, "ai-browser-anthropic-fail", "ai-anthropic-poll", "ai-browser-failed", "Error / timeout", dashed=True)
    add_edge(root, "ai-browser-openai-fail", "ai-openai-poll", "ai-browser-failed", "Error / timeout", dashed=True)
    add_edge(root, "ai-browser-retry", "ai-browser-failed", "ai-key-disconnected", "Try again", dashed=True)

    add_band(root, "ai-connected-band", 1550, 670, "CONNECTED MAINTENANCE", "Testing does not disconnect automatically. Updating or removing credentials requires an explicit user action.")
    add_state(root, "ai-maint-connected", "Connected", "Browser profile or API key", 560, 1740, color="#173127")
    add_state(root, "ai-maint-testing", "Testing", "Probe current credential", 1050, 1660, color="#1F2740")
    add_state(root, "ai-maint-result", "Test result", "OK or inline failure", 1540, 1660)
    add_state(root, "ai-maint-key", "Key form", "Replace API key", 1050, 1900)
    add_state(root, "ai-maint-confirm", "Remove confirmation", "Cancel or remove credential", 2030, 1740, color="#302A18")
    add_state(root, "ai-maint-disconnected", "Not configured", "Provider unavailable to agents", 2520, 1740, color="#302027")
    add_edge(root, "ai-maint-1", "ai-maint-connected", "ai-maint-testing", "Test")
    add_edge(root, "ai-maint-2", "ai-maint-testing", "ai-maint-result", "Response")
    add_edge(root, "ai-maint-3", "ai-maint-result", "ai-maint-connected", "Remain connected", dashed=True)
    add_edge(root, "ai-maint-4", "ai-maint-connected", "ai-maint-key", "Update key")
    add_edge(root, "ai-maint-5", "ai-maint-key", "ai-maint-connected", "Valid key")
    add_edge(root, "ai-maint-6", "ai-maint-connected", "ai-maint-confirm", "Remove")
    add_edge(root, "ai-maint-7", "ai-maint-confirm", "ai-maint-connected", "Cancel", dashed=True)
    add_edge(root, "ai-maint-8", "ai-maint-confirm", "ai-maint-disconnected", "Confirm remove")
    return root


def main() -> None:
    tree = ET.parse(DRAWIO)
    file_root = tree.getroot()
    diagram = next(page for page in file_root.findall("diagram") if page.get("id") == PAGE_ID)
    model = diagram.find("mxGraphModel")
    page_root = model.find("root")

    for cell in list(page_root):
        if cell.get("bloghubSection") == SECTION:
            page_root.remove(cell)

    generated = build_section()
    for cell in generated:
        if cell.get("id") in {"0", "1"}:
            continue
        cell.set("bloghubSection", SECTION)
        geo = cell.find("mxGeometry")
        if (
            geo is not None
            and cell.get("parent") == "1"
            and geo.get("relative") != "1"
            and geo.get("y") is not None
        ):
            geo.set("y", str(float(geo.get("y", "0")) + OFFSET_Y))
        page_root.append(cell)

    model.attrib.update(
        pageWidth="3600",
        pageHeight=str(OFFSET_Y + SECTION_HEIGHT),
        pageScale="1",
        page="1",
    )
    ET.indent(tree, space="  ")
    tree.write(DRAWIO, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    main()

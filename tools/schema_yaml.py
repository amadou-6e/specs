"""Read the deliberately small YAML subset used by financial object schemas.

Values are JSON-compatible YAML scalars; nested maps and lists use two-space
indentation. This avoids a runtime YAML dependency for the specs validator.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")


def load_schema(path: Path) -> dict:
    lines: list[tuple[int, str, int]] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        spaces = len(raw) - len(raw.lstrip(" "))
        if "\t" in raw[:spaces] or spaces % 2:
            raise ValueError(f"line {number}: expected two-space indentation")
        lines.append((spaces, raw.strip(), number))

    def block(position: int, indent: int):
        if position >= len(lines) or lines[position][0] != indent:
            raise ValueError(f"expected a block at indentation {indent}")
        sequence = lines[position][1].startswith("- ")
        result = [] if sequence else {}
        while position < len(lines) and lines[position][0] == indent:
            _, text, number = lines[position]
            if sequence:
                if not text.startswith("- "):
                    raise ValueError(f"line {number}: mixed mapping and sequence")
                result.append(json.loads(text[2:]))
                position += 1
                continue
            key, marker, value = text.partition(":")
            if not marker or not _KEY.fullmatch(key):
                raise ValueError(f"line {number}: invalid key")
            if key in result:
                raise ValueError(f"line {number}: duplicate key {key}")
            if value.strip():
                result[key] = json.loads(value.strip())
                position += 1
            elif position + 1 < len(lines) and lines[position + 1][0] > indent:
                if lines[position + 1][0] != indent + 2:
                    raise ValueError(f"line {number}: indentation jumped")
                result[key], position = block(position + 1, indent + 2)
            else:
                result[key] = {}
                position += 1
        return result, position

    if not lines:
        raise ValueError("empty schema")
    value, end = block(0, 0)
    if end != len(lines) or not isinstance(value, dict):
        raise ValueError("unexpected trailing content or non-mapping root")
    return value

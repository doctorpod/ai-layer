"""YAML for note frontmatter and the layer's config, with a fallback when PyYAML isn't installed.

The fallback reads what these files use: nested mappings by indentation, block
lists ("- item"), inline lists ("[a, b]"), quoted or plain scalars and comments.
Scalars stay strings, so a date reads as "2026-11-10" either way once passed
through str().
"""
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

KEY = re.compile(r"^([^\s:#-][^:]*?|-[^\s:][^:]*?):(?:\s+(.*))?$")


def parse_yaml(raw):
    """A mapping from YAML text; {} if it doesn't parse to one."""
    if yaml:
        try:
            v = yaml.safe_load(raw)
        except yaml.YAMLError:
            return {}
    else:
        v = parse_fallback(raw)
    return v if isinstance(v, dict) else {}


def split_frontmatter(text):
    """(frontmatter text or None, body) for a note's full text."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end], text[end + 4:]
    return None, text


def read_note(path):
    """(frontmatter dict, body) for a note on disk."""
    raw, body = split_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
    return (parse_yaml(raw) if raw is not None else {}), body


def load_config(path):
    """The config file as a mapping, or None if there's no file."""
    path = Path(path)
    if not path.is_file():
        return None
    return parse_yaml(path.read_text(encoding="utf-8"))


# ---- fallback ------------------------------------------------------------------
def parse_fallback(raw):
    lines = []
    for line in raw.splitlines():
        text = line.strip()
        if text and not text.startswith("#"):
            lines.append((len(line) - len(line.lstrip()), text))
    if not lines:
        return {}
    return _block(lines, 0, lines[0][0])[0]


def _is_item(text):
    return text == "-" or text.startswith("- ")


def _block(lines, i, indent):
    """The value made by lines[i:] at this indent, and the index after it."""
    if _is_item(lines[i][1]):
        out = []
        while i < len(lines) and lines[i][0] == indent and _is_item(lines[i][1]):
            out.append(_scalar(lines[i][1][1:]))
            i += 1
        return out, i
    out = {}
    while i < len(lines) and lines[i][0] >= indent:
        ind, text = lines[i]
        m = KEY.match(text) if ind == indent else None
        i += 1
        if not m:
            continue  # a stray deeper line, or one this parser doesn't read
        key, val = _scalar(m.group(1)), (m.group(2) or "").strip()
        if val:
            out[key] = _scalar(val)
        elif i < len(lines) and (lines[i][0] > indent or (lines[i][0] == indent and _is_item(lines[i][1]))):
            out[key], i = _block(lines, i, lines[i][0])
        else:
            out[key] = None
    return out, i


def _scalar(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    s = re.split(r"\s+#", s, maxsplit=1)[0].strip()
    if s.startswith("[") and s.endswith("]"):
        return [_scalar(x) for x in s[1:-1].split(",") if x.strip()]
    return s

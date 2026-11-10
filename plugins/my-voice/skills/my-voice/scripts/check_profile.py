#!/usr/bin/env python3
"""Check a My Voice profile against the published format.

Reads one `profile.md` and prints one JSON verdict: pass, fail (naming the
part), rebuild (the profile is in an older `my_voice_format`) or update (it is
in a newer one, written by a newer skill than the one running).

The frontmatter is a restricted YAML subset -- `key: value` lines and flow
lists `[a, b]`, no nesting -- so it is parsed here with the standard library
and the check runs wherever Python 3.9 runs, with nothing to install.

A new channel id is a change to CHANNEL_IDS, never a format version: a profile
carrying only registered ids keeps passing under the same `my_voice_format`.

`--contract` prints the fields, sections, channel ids, size limit, verdicts and
exit codes as JSON.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

FORMAT_VERSION = 1
SIZE_LIMIT_BYTES = 32 * 1024

CHANNEL_IDS = (
    "email-internal",
    "email-external",
    "linkedin-post",
    "linkedin-comment",
    "social-post",
    "chat-message",
    "blog-post",
    "bio",
)

# (name, kind, required). Kinds: int, str, list, date.
FIELDS = (
    ("my_voice_format", "int", True),
    ("owner_name", "str", True),
    ("owner_email", "str", True),
    ("aliases", "list", True),
    ("languages", "list", True),
    ("channels", "list", True),
    ("created", "date", True),
    ("updated", "date", True),
)

# Level-2 headings, in order. "Language: <code>" repeats once per entry of
# `languages`, in that order, between the general voice and the channel rules.
SECTIONS_BEFORE_LANGUAGES = ("General voice",)
LANGUAGE_SECTION_PREFIX = "Language: "
SECTIONS_AFTER_LANGUAGES = (
    "Channel rules",
    "Approved samples",
    "Facts about the user",
    "Explicit rules",
    "Provenance record",
    "Change log",
)

# Level-3 headings under these sections name a channel id; under "Approved
# samples" the form is "<channel id> (<language>)".
CHANNEL_HEADED_SECTIONS = ("Channel rules", "Approved samples")

LANGUAGE_RE = re.compile(r"^[a-z]{2,3}(-[A-Z]{2})?$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
KEY_RE = re.compile(r"^([a-z_][a-z0-9_]*):(.*)$")
SAMPLE_HEADING_RE = re.compile(r"^(\S+) \(([^)]+)\)$")

EXIT_CODES = {
    "0": "pass -- the profile matches the current format",
    "1": "fail -- the profile breaks the format; `part` names where",
    "2": "could not run -- the file is missing or unreadable",
    "3": "rebuild -- the profile is in an older my_voice_format",
    "4": "update -- the profile is in a newer my_voice_format than this check",
}
VERDICT_EXIT = {"pass": 0, "fail": 1, "error": 2, "rebuild": 3, "update": 4}

CONTRACT = {
    "purpose": "Check one My Voice profile file against the published format.",
    "format_version": FORMAT_VERSION,
    "size_limit_bytes": SIZE_LIMIT_BYTES,
    "frontmatter": {
        "delimiters": "a line '---' opens the file and a second '---' closes the block",
        "syntax": "one 'key: value' per line; a value is a scalar or a flow "
                  "list [a, b]; no nesting, no block lists; blank lines and "
                  "'#' comment lines allowed; a scalar may be single- or "
                  "double-quoted",
        "fields": [
            {"name": n, "kind": k, "required": r} for n, k, r in FIELDS
        ],
        "kinds": {
            "int": "a whole number",
            "str": "a non-empty scalar",
            "list": "a flow list; 'languages' is non-empty and holds codes "
                    "such as en or pt-BR; 'channels' holds registered channel ids",
            "date": "YYYY-MM-DD",
        },
    },
    "sections": {
        "level": 2,
        "order": list(SECTIONS_BEFORE_LANGUAGES)
        + ["Language: <code> -- one per entry of 'languages', in that order"]
        + list(SECTIONS_AFTER_LANGUAGES),
        "channel_subsections": {
            "Channel rules": "### <channel id>",
            "Approved samples": "### <channel id> (<language code>)",
        },
        "unknown_level_2_heading": "fail",
    },
    "channel_ids": list(CHANNEL_IDS),
    "channel_id_rule": "a new channel id is added to this registry, never a "
                       "new format version",
    "verdicts": {
        "pass": "matches the current format",
        "fail": "breaks the format; 'part' names the field, section or limit",
        "rebuild": "older my_voice_format; rebuild into a new profile",
        "update": "newer my_voice_format; leave the profile unchanged and "
                  "update the skill",
    },
    "exit_codes": EXIT_CODES,
    "output": "one JSON object on stdout: verdict, part, detail, format",
}

Scalar = Union[str, List[str]]


class FormatError(Exception):
    def __init__(self, part: str, detail: str) -> None:
        super().__init__(detail)
        self.part = part
        self.detail = detail


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _parse_value(raw: str) -> Scalar:
    value = raw.strip()
    if value.startswith("["):
        if not value.endswith("]"):
            raise ValueError("an unclosed flow list")
        inner = value[1:-1].strip()
        if not inner:
            return []
        items = [_unquote(item.strip()) for item in inner.split(",")]
        if any(not item or item[0] in "[{" for item in items):
            raise ValueError("an empty or nested list item")
        return items
    if value.startswith("{") or value in ("|", ">"):
        raise ValueError("nesting or a block scalar")
    return _unquote(value)


def split_frontmatter(text: str) -> Tuple[List[str], str]:
    """Return the frontmatter lines and the body after the closing '---'."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FormatError("frontmatter", "the file does not open with a '---' line")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], "\n".join(lines[index + 1:])
    raise FormatError("frontmatter", "no closing '---' line")


def parse_frontmatter(lines: List[str]) -> Dict[str, Scalar]:
    data: Dict[str, Scalar] = {}
    for number, line in enumerate(lines, start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = KEY_RE.match(line)
        if not match:
            raise FormatError(
                "frontmatter",
                "line %d is not 'key: value' at the left margin" % number,
            )
        key, raw = match.group(1), match.group(2)
        if key in data:
            raise FormatError("frontmatter: %s" % key, "the field appears twice")
        try:
            data[key] = _parse_value(raw)
        except ValueError as exc:
            raise FormatError("frontmatter: %s" % key, "the value has %s" % exc)
    return data


def read_format_version(data: Dict[str, Scalar]) -> int:
    raw = data.get("my_voice_format")
    if raw is None:
        raise FormatError("frontmatter: my_voice_format", "the field is missing")
    if not isinstance(raw, str) or not raw.isdigit():
        raise FormatError("frontmatter: my_voice_format", "not a whole number")
    return int(raw)


def check_fields(data: Dict[str, Scalar]) -> None:
    known = {name for name, _, _ in FIELDS}
    for key in data:
        if key not in known:
            raise FormatError("frontmatter: %s" % key, "not a field of this format")
    for name, kind, required in FIELDS:
        part = "frontmatter: %s" % name
        if name not in data:
            if required:
                raise FormatError(part, "the field is missing")
            continue
        value = data[name]
        if kind == "list":
            if not isinstance(value, list):
                raise FormatError(part, "not a flow list [a, b]")
        elif isinstance(value, list) or not value:
            raise FormatError(part, "not a non-empty scalar")
        elif kind == "date" and not DATE_RE.match(value):
            raise FormatError(part, "not a YYYY-MM-DD date")
    languages = data["languages"]
    if not languages:
        raise FormatError("frontmatter: languages", "names no language")
    for code in languages:
        if not LANGUAGE_RE.match(code):
            raise FormatError("frontmatter: languages", "%r is not a language code" % code)
    if len(set(languages)) != len(languages):
        raise FormatError("frontmatter: languages", "a language appears twice")
    for channel in data["channels"]:
        if channel not in CHANNEL_IDS:
            raise FormatError(
                "frontmatter: channels", "%r is not a registered channel id" % channel
            )


def _headings(body: str, level: int) -> List[Tuple[int, str]]:
    marker = "#" * level + " "
    found = []
    in_fence = False
    for number, line in enumerate(body.splitlines()):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and line.startswith(marker):
            found.append((number, line[len(marker):].strip()))
    return found


def check_sections(body: str, languages: List[str], channels: List[str]) -> None:
    expected = (
        list(SECTIONS_BEFORE_LANGUAGES)
        + [LANGUAGE_SECTION_PREFIX + code for code in languages]
        + list(SECTIONS_AFTER_LANGUAGES)
    )
    found = _headings(body, 2)
    titles = [title for _, title in found]
    for title in titles:
        if title not in expected:
            raise FormatError("section: %s" % title, "not a section of this format")
    for title in expected:
        if title not in titles:
            raise FormatError("section: %s" % title, "the section is missing")
        if titles.count(title) > 1:
            raise FormatError("section: %s" % title, "the section appears twice")
    if titles != expected:
        raise FormatError(
            "sections", "out of order; expected: %s" % ", ".join(expected)
        )

    lines = body.splitlines()
    starts = [number for number, _ in found] + [len(lines)]
    for position, title in enumerate(titles):
        if title not in CHANNEL_HEADED_SECTIONS:
            continue
        chunk = "\n".join(lines[starts[position] + 1:starts[position + 1]])
        for _, sub in _headings(chunk, 3):
            channel, language = sub, None
            if title == "Approved samples":
                match = SAMPLE_HEADING_RE.match(sub)
                if not match:
                    raise FormatError(
                        "section: %s" % title,
                        "%r is not '<channel id> (<language code>)'" % sub,
                    )
                channel, language = match.group(1), match.group(2)
            if channel not in CHANNEL_IDS:
                raise FormatError(
                    "section: %s" % title, "%r is not a registered channel id" % channel
                )
            if channel not in channels:
                raise FormatError(
                    "section: %s" % title,
                    "%r is not listed in the 'channels' field" % channel,
                )
            if language is not None and language not in languages:
                raise FormatError(
                    "section: %s" % title,
                    "%r is not listed in the 'languages' field" % language,
                )


def check_text(raw: bytes) -> Dict[str, object]:
    """Return the verdict for one profile's bytes."""
    if len(raw) > SIZE_LIMIT_BYTES:
        return _verdict(
            "fail", "size",
            "%d bytes, over the %d-byte limit" % (len(raw), SIZE_LIMIT_BYTES),
        )
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return _verdict("fail", "encoding", "the file is not UTF-8 text")
    try:
        lines, body = split_frontmatter(text)
        data = parse_frontmatter(lines)
        version = read_format_version(data)
        if version < FORMAT_VERSION:
            return _verdict(
                "rebuild", "frontmatter: my_voice_format",
                "format %d is older than %d" % (version, FORMAT_VERSION), version,
            )
        if version > FORMAT_VERSION:
            return _verdict(
                "update", "frontmatter: my_voice_format",
                "format %d is newer than %d" % (version, FORMAT_VERSION), version,
            )
        check_fields(data)
        check_sections(body, list(data["languages"]), list(data["channels"]))
    except FormatError as exc:
        return _verdict("fail", exc.part, exc.detail)
    return _verdict("pass", None, None, FORMAT_VERSION)


def _verdict(
    verdict: str, part: Optional[str], detail: Optional[str],
    version: Optional[int] = None,
) -> Dict[str, object]:
    return {"verdict": verdict, "part": part, "detail": detail, "format": version}


def check_file(path: Path) -> Dict[str, object]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return _verdict("error", "file", "could not read %s: %s" % (path, exc.strerror))
    return check_text(raw)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check a My Voice profile against the published format "
                    "(see --contract).",
    )
    parser.add_argument("profile", nargs="?", help="path to profile.md")
    parser.add_argument(
        "--contract", action="store_true",
        help="print the format contract and exit codes as JSON",
    )
    args = parser.parse_args(argv)
    if args.contract:
        print(json.dumps(CONTRACT, indent=2))
        return 0
    if not args.profile:
        parser.error("a profile path is required unless --contract is given")
    result = check_file(Path(args.profile).expanduser())
    print(json.dumps(result))
    return VERDICT_EXIT[str(result["verdict"])]


if __name__ == "__main__":
    sys.exit(main())

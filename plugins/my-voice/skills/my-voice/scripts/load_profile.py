#!/usr/bin/env python3
"""Load the My Voice profile in one call.

Resolves the folder as `profile_path.py` does, checks `profile.md` as
`check_profile.py` does, and prints one JSON object carrying the verdict, the
profile text and, when the overlay names its register with
`--register-file <name>`, that file's text when it exists.
One call replaces the separate resolve, check and read steps, so drafting can
start without a round trip per step.

`--stamp-file <path>` adds that file's SHA-256, so a caller can tell whether
the file changed since it last recorded the fingerprint.

`--contract` prints the output fields, the verdicts and the exit codes as JSON.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

# The two sibling scripts own the folder rules and the format check; importing
# them keeps one definition of each.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_profile  # noqa: E402
import profile_path  # noqa: E402

VERDICT_EXIT = {
    "pass": 0,
    "fail": 1,
    "error": 2,
    "rebuild": 3,
    "update": 4,
    "refused": 5,
    "missing": 6,
}

EXIT_CODES = {
    "0": "pass -- the profile matches the current format",
    "1": "fail -- the profile breaks the format; `part` names where",
    "2": "could not run -- the home folder could not be determined, the "
         "profile is unreadable, or --register-file is not a plain file name",
    "3": "rebuild -- the profile is in an older my_voice_format",
    "4": "update -- the profile is in a newer my_voice_format than this check",
    "5": "refused -- the home or the folder sits inside a refused location",
    "6": "missing -- the folder resolved but holds no profile.md",
}

CONTRACT = {
    "purpose": "Resolve the My Voice folder, check the profile and return the "
               "verdict, the profile text and the overlay register text "
               "in one call.",
    "arguments": {
        "--register-file <name>": "the overlay's register file name in the "
                                  "folder; without it no register is read",
        "--stamp-file <path>": "add the SHA-256 of that file to the output",
        "--contract": "print this contract and exit 0",
    },
    "output": {
        "verdict": "pass, fail, rebuild or update (the check_profile.py "
                   "verdicts); error when the profile or home cannot be read; "
                   "refused when the location is refused; missing when there "
                   "is no profile.md",
        "part": "where the profile breaks the format, or null",
        "detail": "why, in one line, or null",
        "format": "the profile's my_voice_format when known, or null",
        "folder": "the resolved my-voice folder, or null when refused or "
                  "unresolved",
        "profile_path": "the profile.md path, or null",
        "register_path": "the register path from --register-file, or null "
                         "without it",
        "folder_exists": "true when the folder exists",
        "profile_exists": "true when profile.md exists",
        "profile": "the profile text when the file was read as UTF-8, on any "
                   "check verdict; null otherwise",
        "register": "the register text when the file exists and reads as "
                    "UTF-8; null when absent, unreadable or not named",
        "stamp": "only with --stamp-file: {path, sha256}; sha256 is null and "
                 "error names the cause when the file cannot be read",
    },
    "verdicts": {
        "pass": "draft from the profile",
        "fail": "the profile breaks the format; part and detail say where",
        "rebuild": "older my_voice_format; rebuild into a new profile",
        "update": "newer my_voice_format; leave the profile unchanged and "
                  "update the skill",
        "error": "could not read the home folder or the profile",
        "refused": "the location is a documents or synced folder; detail "
                   "names it",
        "missing": "no profile yet",
    },
    "stamp_rule": "a stamp file that cannot be read never changes the verdict "
                  "or the exit code",
    "exit_codes": EXIT_CODES,
}


def _read_text(path: str) -> Optional[str]:
    try:
        return Path(path).read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def stamp(path: str) -> Dict[str, object]:
    """The SHA-256 of one file, or a null hash with the cause."""
    target = Path(path).expanduser()
    try:
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
    except OSError as exc:
        return {
            "path": str(target),
            "sha256": None,
            "error": "could not read %s: %s" % (target, exc.strerror),
        }
    return {"path": str(target), "sha256": digest}


def load(
    home: Optional[str] = None,
    platform: Optional[str] = None,
    stamp_file: Optional[str] = None,
    register_name: Optional[str] = None,
) -> Dict[str, object]:
    result: Dict[str, object] = {
        "verdict": None,
        "part": None,
        "detail": None,
        "format": None,
        "folder": None,
        "profile_path": None,
        "register_path": None,
        "folder_exists": False,
        "profile_exists": False,
        "profile": None,
        "register": None,
    }
    if stamp_file is not None:
        result["stamp"] = stamp(stamp_file)

    if register_name is not None:
        problem = profile_path.register_name_error(register_name)
        if problem:
            result.update(verdict="error", part="register", detail=problem)
            return result
    paths = profile_path.resolve(
        home=home, platform=platform, register_name=register_name,
    )
    if "error" in paths:
        result.update(verdict="error", part="home", detail=paths["error"])
        return result
    if "refused" in paths:
        result.update(verdict="refused", part="folder", detail=paths["refused"])
        return result

    result.update(
        folder=paths["folder"],
        profile_path=paths["profile"],
        register_path=paths.get("register"),
        folder_exists=paths["folder_exists"],
        profile_exists=paths["profile_exists"],
    )
    if "register" in paths:
        register_file = Path(str(paths["register"]))
        if register_file.is_file():
            result["register"] = _read_text(str(register_file))

    if not paths["profile_exists"]:
        result.update(
            verdict="missing", part="file",
            detail="no profile at %s" % paths["profile"],
        )
        return result

    verdict = check_profile.check_file(Path(str(paths["profile"])))
    result.update(verdict)
    if verdict["verdict"] != "error":
        result["profile"] = _read_text(str(paths["profile"]))
    return result


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Resolve, check and read the My Voice profile in one call "
                    "(see --contract).",
    )
    parser.add_argument(
        "--register-file", metavar="NAME",
        help="read the overlay's register file NAME from the folder",
    )
    parser.add_argument(
        "--stamp-file", metavar="PATH",
        help="add the SHA-256 of this file to the output",
    )
    parser.add_argument(
        "--contract", action="store_true",
        help="print the output fields, verdicts and exit codes as JSON",
    )
    args = parser.parse_args(argv)
    if args.contract:
        print(json.dumps(CONTRACT, indent=2))
        return 0
    result = load(stamp_file=args.stamp_file, register_name=args.register_file)
    print(json.dumps(result))
    return VERDICT_EXIT[str(result["verdict"])]


if __name__ == "__main__":
    sys.exit(main())

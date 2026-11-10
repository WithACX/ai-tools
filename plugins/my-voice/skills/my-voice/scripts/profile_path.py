#!/usr/bin/env python3
"""Resolve the My Voice folder and its files for the current user.

The folder is always `my-voice` directly under the home folder; the user never
chooses a location. A home that itself sits inside Documents, Desktop or a
folder a cloud service syncs is refused, and so is a `my-voice` folder that is
a link into one: the profile file stays on the owner's computer and is never
synced out by a side door.

An organization overlay may keep a register file in the same folder. Its name
comes from the overlay and is passed as `--register-file <name>`; this script
knows no register name of its own.

Prints one JSON object. `--contract` prints the layout, the refusal rules and
the exit codes.
"""

from __future__ import annotations

import argparse
import json
import ntpath
import os
import posixpath
import sys
from typing import Dict, List, Optional

FOLDER_NAME = "my-voice"
FILES = {
    "profile": "profile.md",
    "rebuild": "profile-rebuild.md",
    "archive": "archive",
}

# Folder names that place a path inside a synced or user-document area.
# Compared case-insensitively against each path component below the user's
# own home root; a name with a trailing "*" matches by prefix.
REFUSED_COMPONENTS = (
    "Documents",
    "Desktop",
    "OneDrive*",
    "iCloud Drive",
    "iCloudDrive",
    "Mobile Documents",
    "CloudStorage",
    "Dropbox*",
    "Google Drive",
    "GoogleDrive*",
    "My Drive",
    "Box",
    "Box Sync",
    "pCloud Drive",
    "Nextcloud",
    "ownCloud",
)

EXIT_CODES = {
    "0": "resolved -- the paths are printed",
    "1": "refused -- the home or the folder sits inside a refused location",
    "2": "could not run -- the home folder could not be determined, or "
         "--register-file is not a plain file name",
}

CONTRACT = {
    "purpose": "Resolve the My Voice folder and its files for the current user.",
    "folder": "<home>/" + FOLDER_NAME,
    "layouts": {
        "macOS": "/Users/<user>/my-voice/",
        "Windows": "C:\\Users\\<user>\\my-voice\\",
        "other": "<home>/my-voice/",
    },
    "files": FILES,
    "arguments": {
        "--register-file <name>": "add `register`, the path of the overlay's "
                                  "register file <name> in the folder; a plain "
                                  "file name, never a path or a reserved name",
        "--contract": "print this contract and exit 0",
    },
    "refused": {
        "rule": "the home, or the real target of the my-voice folder when it "
                "is a link, has a path component below the user's home root "
                "matching one of these names (case-insensitive; '*' matches "
                "by prefix)",
        "components": list(REFUSED_COMPONENTS),
    },
    "exit_codes": EXIT_CODES,
    "output": "one JSON object: folder, the file paths, register when "
              "--register-file is given, folder_exists and profile_exists; "
              "on refusal, refused names the reason; on error, error names "
              "the cause",
}


def _pathmod(platform: str):
    return ntpath if platform == "win32" else posixpath


def _components_below_home_root(path: str, platform: str) -> List[str]:
    """Path components, dropping the `Users/<user>` or `home/<user>` root."""
    mod = _pathmod(platform)
    _, rest = mod.splitdrive(mod.normpath(path))
    parts = [part for part in rest.replace("\\", "/").split("/") if part]
    if len(parts) >= 2 and parts[0].lower() in ("users", "home"):
        return parts[2:]
    return parts


def refused_component(path: str, platform: str) -> Optional[str]:
    """The first refused component of `path`, or None when it is allowed."""
    for part in _components_below_home_root(path, platform):
        lowered = part.lower()
        for name in REFUSED_COMPONENTS:
            pattern = name.lower()
            if pattern.endswith("*"):
                if lowered.startswith(pattern[:-1]):
                    return part
            elif lowered == pattern:
                return part
    return None


def register_name_error(name: str) -> Optional[str]:
    """Why `name` cannot be a register file name, or None when it can."""
    if not name or name in (".", "..") or "/" in name or "\\" in name or ":" in name:
        return "--register-file %r is not a plain file name" % name
    if name in FILES.values():
        return "--register-file %r names a file this skill owns" % name
    return None


def resolve(
    home: Optional[str] = None,
    platform: Optional[str] = None,
    check_disk: bool = True,
    register_name: Optional[str] = None,
) -> Dict[str, object]:
    platform = platform or sys.platform
    mod = _pathmod(platform)
    if register_name is not None:
        problem = register_name_error(register_name)
        if problem:
            return {"error": problem}
    if home is None:
        home = os.path.expanduser("~")
        if home == "~":
            return {"error": "the home folder could not be determined"}
    hit = refused_component(home, platform)
    if hit:
        return {
            "refused": "the home folder %s is inside %r, a documents or synced "
                       "folder" % (home, hit),
        }
    folder = mod.join(home, FOLDER_NAME)
    result: Dict[str, object] = {"folder": folder}
    for key, name in FILES.items():
        result[key] = mod.join(folder, name)
    if register_name is not None:
        result["register"] = mod.join(folder, register_name)
    result["folder_exists"] = False
    result["profile_exists"] = False
    if check_disk and os.path.lexists(folder):
        real = os.path.realpath(folder)
        if os.path.normcase(real) != os.path.normcase(os.path.abspath(folder)):
            hit = refused_component(real, platform)
            if hit:
                return {
                    "refused": "%s links to %s, inside %r, a documents or "
                               "synced folder" % (folder, real, hit),
                }
        result["folder_exists"] = os.path.isdir(folder)
        result["profile_exists"] = os.path.isfile(str(result["profile"]))
    return result


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Resolve the My Voice folder and its files (see --contract).",
    )
    parser.add_argument(
        "--register-file", metavar="NAME",
        help="also resolve the overlay's register file NAME in the folder",
    )
    parser.add_argument(
        "--contract", action="store_true",
        help="print the layout, refusal rules and exit codes as JSON",
    )
    args = parser.parse_args(argv)
    if args.contract:
        print(json.dumps(CONTRACT, indent=2))
        return 0
    result = resolve(register_name=args.register_file)
    print(json.dumps(result))
    if "error" in result:
        return 2
    if "refused" in result:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

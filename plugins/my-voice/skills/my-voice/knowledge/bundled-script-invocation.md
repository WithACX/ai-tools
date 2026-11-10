# Running the Bundled Scripts

How My Voice runs the scripts in its own `scripts` folder in each app. Every
script runs from the installed copy of this skill; nothing is downloaded.

`<skill dir>` is the folder that holds this skill's `SKILL.md`, as the app
announced it when the skill loaded. Where the skill's references write
`${CLAUDE_PLUGIN_ROOT}/skills/my-voice` and the app has not replaced it with a
path, use `<skill dir>` in its place.

## Resolve the interpreter first

```bash
PY="$(command -v python3 || command -v python)"
```

The scripts need Python 3.9 or later. `command -v` only looks the name up, so
the `||` here picks `python` only when `python3` is absent.

## Load the My Voice profile

`<args>` are the options an organization overlay in this skill folder names,
and none when the folder carries no overlay. Take the first route that applies:

- **Claude Code and the Codex CLI.** The shell runs on the user's computer:
  `"$PY" "<skill dir>/scripts/load_profile.py" <args>`.
- **Claude desktop app chat with Desktop Commander.** Desktop Commander's
  shell runs on the user's computer and sees `~/my-voice/`. When it also sees
  `<skill dir>`, run `"$PY" "<skill dir>/scripts/load_profile.py" <args>`
  there. Otherwise copy `~/my-voice/profile.md` through Desktop Commander into
  a folder named `my-voice` that the chat's own shell sees, and run the script
  there once with `HOME` set to the folder that holds it. The chat never writes
  `~/my-voice/`.
- **Cowork, one shell sees both.** When one shell sees both this skill folder
  and the connected `my-voice` folder, run the script there with `HOME` set to
  the folder that holds `my-voice` as that shell sees it:
  `HOME=<that folder> "$PY" "<skill dir>/scripts/load_profile.py" <args>`.
- **Cowork, no shell sees both.** Stage `~/my-voice/profile.md` into the
  session with the device file-staging tool, keeping it in a folder named
  `my-voice`, then run the script once with `HOME` set to the folder that holds
  it: `HOME=<that folder> "$PY" "<skill dir>/scripts/load_profile.py" <args>`.
  A file written this way goes back to `~/my-voice/` with the device commit
  tool.

`scripts/check_profile.py` and `scripts/profile_path.py` run the same way, on
the same route.

## An unrunnable script never becomes a silent skip

When no route above runs the script, the step has not passed. The profile
check protects every draft: say before drafting that it could not run, name
the cause, and ask how to go on. A path that does not resolve is not reachable
from the shell that ran it; never report the skill as not installed.

## Never retry a failed script with another interpreter

`"$PY" <script> || python <script>` is not a fallback. The scripts report their
verdicts with non-zero exit codes, so the retry runs every side effect twice and
replaces the real verdict with the retry's.

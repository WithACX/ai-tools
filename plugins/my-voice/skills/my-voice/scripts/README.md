# my-voice scripts

The parts of My Voice that must give the same answer on every surface and every
run: where the profile folder is and which locations are refused, whether a
profile matches the published format, and the one load call that does both and
returns the profile and the overlay's register with the verdict. They are
scripts so that no model decides these from memory.

## How they are invoked

Through the resolve-first contract in `knowledge/bundled-script-invocation.md`:
resolve the interpreter, then the plugin root, then the script path. Each script
is a plain Python 3.9-compatible CLI with no third-party imports, prints one
JSON object, and documents its fields and exit codes under `--contract`.

## Conventions

- **One owner per rule.** The folder rules and the format check each live in
  one script; a script that needs them imports that script rather than copying
  it.
- **Read only.** No script here writes, moves or deletes a profile file; the
  skill does that, with the user's approval.
- **No organization content.** An organization's rules arrive through the
  overlay, never through a script here.

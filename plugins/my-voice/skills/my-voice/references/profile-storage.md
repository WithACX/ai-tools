# Profile Storage

Where the profile lives and how each surface reaches it. The format is
`references/profile-schema.md`; this file covers location and access only.

## Support by surface

The one statement of what works where. Every other surface claim in this skill
follows it.

| Surface | Reaches the profile | Create, tune, manage |
|---|---|---|
| Cowork (desktop, web, mobile through the linked computer) | Yes, the connected `my-voice` folder | Yes |
| Claude Code | Yes, reads the folder | No: points to Cowork |
| Codex CLI | Yes, reads the folder | No: points to Cowork |
| Claude desktop app chat with Desktop Commander | Yes, reads the folder | No: points to Cowork |
| Claude.ai web chat, ChatGPT | No | No: says so before drafting |

## The folder

One fixed folder, `my-voice`, directly under the user's home folder:
`/Users/<user>/my-voice/` on macOS, `C:\Users\<user>\my-voice\` on Windows.
The user never chooses a location. Resolve it with the bundled script rather
than building the path yourself, locating the script and `$PY` per
`knowledge/bundled-script-invocation.md`:

```bash
"$PY" "${CLAUDE_PLUGIN_ROOT}/skills/my-voice/scripts/profile_path.py"
```

It prints the folder and file paths and whether they exist, or `refused` with a
reason when the home folder, or the real target of a linked `my-voice` folder,
sits inside Documents, Desktop or a folder a cloud service syncs. A refusal
stops the save: tell the user why and that the folder must be a plain folder
under their home. `--contract` lists the files and refusal rules.

| File | Holds |
|---|---|
| `profile.md` | The profile in use |
| `profile-rebuild.md` | A rebuilt profile awaiting approval (format upgrade) |
| `archive/` | Earlier profiles, kept until the user deletes them |
| The overlay's register | Named and written only by an organization overlay the bundle carries; this skill never creates it |

Nothing else is stored anywhere: no copy in a project, a repository, a chat
memory, a connector or any service. Never pass profile text to another skill,
an issue, a learning or a log.

## Cowork

Cowork reaches the folder as a connected folder.

- **First save.** Name the fixed folder, `~/my-voice/`, and ask the user only
  to create it and connect it to the session. Never ask them to pick a
  location, and never save into a different connected folder instead.
- **Later sessions without the connection.** Ask for access to `~/my-voice/`
  only, never to the home folder or any broader folder.
- **Writes.** Cowork is the only surface that writes the folder: the first
  save, tuning, edits, rebuilds, archive moves and deletion.

## Claude Code, the Codex CLI and the desktop app chat

Claude Code, the Codex CLI and the Claude desktop app chat with Desktop
Commander read `~/my-voice/profile.md` from the user's computer and never write
the folder. When the user asks for a change there, say that profile changes are
made in Cowork and leave the file unchanged.

None of them has an edit path: offer none, including changing file permissions,
widening a sandbox, or editing the file by hand on the user's behalf.

## Surfaces with no profile

Claude.ai web chat and ChatGPT cannot read the user's computer, so they have no
profile. Say so before drafting, name the surfaces in "Support by surface" that
reach it, and ask whether to draft without it.

## Missing profile

When `profile.md` is missing but `archive/` or `profile-rebuild.md` holds a
profile, or the user says one was saved, offer two choices: restore the newest archived profile,
or create a new one. Never recreate it silently.

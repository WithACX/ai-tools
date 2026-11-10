# Profile Schema

The published format of `profile.md`. The exact field list, section order,
registered channel ids, size limit, verdicts and exit codes are owned by the
check script and printed by its `--contract`; this file says what each part
means and how versions move. Where the two disagree, the contract wins.

## Run the check

Resolve `$PY` and the plugin root per `knowledge/bundled-script-invocation.md`,
then:

```bash
"$PY" "${CLAUDE_PLUGIN_ROOT}/skills/my-voice/scripts/check_profile.py" --contract
"$PY" "${CLAUDE_PLUGIN_ROOT}/skills/my-voice/scripts/check_profile.py" <path to profile.md>
```

The check prints one JSON object (`verdict`, `part`, `detail`, `format`). Run it
on every load and before every save; never save a file that does not pass.

## Shape

A frontmatter block between two `---` lines, then the sections as level-2
headings in the contract's order. The frontmatter is a restricted YAML subset:
one `key: value` per line, lists written inline as `[a, b]`, no nesting and no
block lists. Write it exactly in that form; a tool that reformats it into
block lists breaks the check.

```markdown
---
my_voice_format: 1
owner_name: <full name>
owner_email: <address>
aliases: [<short name>, <initials>]
languages: [en]
channels: [email-internal, linkedin-post]
created: 2026-01-31
updated: 2026-01-31
---

# Voice profile: <full name>

## General voice
## Language: en
## Channel rules
### email-internal
## Approved samples
### email-internal (en)
## Facts about the user
## Explicit rules
## Provenance record
## Change log
```

## Fields

- `my_voice_format` -- the format version this file was written in.
- `owner_name`, `owner_email`, `aliases` -- who the profile belongs to and the
  names they sign or are addressed by. Used to recognize the owner's own
  content, never to look anyone else up.
- `languages` -- the languages the profile has a section for, in section order.
- `channels` -- the channel ids the profile has rules or samples for.
- `created`, `updated` -- dates of the first save and the latest change.

## Sections

- **General voice** -- rules that hold in every language and channel: sentence
  length, structure, word choice, tone, what the owner never does.
- **Language: `<code>`** -- one per language: what changes in that language.
- **Channel rules** -- one `###` subsection per channel id: length, structure,
  greeting and sign-off, formality for that channel.
- **Approved samples** -- one `### <channel id> (<language>)` subsection per
  channel and language, holding one short excerpt the owner approved. Excerpts
  carry no other person's name or detail and no client name or content.
- **Facts about the user** -- only facts that support a rule or an approved
  sample, each saying which.
- **Explicit rules** -- rules the owner stated in words. They outrank inferred
  rules.
- **Provenance record** -- every source read: what it was, its date range and
  the read date. Never the source text.
- **Change log** -- one dated entry per change, naming its cause.

## Channel ids

| Id | Channel |
|---|---|
| `email-internal` | Email to colleagues in the owner's organization |
| `email-external` | Email to anyone outside it |
| `linkedin-post` | A LinkedIn post under the owner's name |
| `linkedin-comment` | A comment or reply on LinkedIn |
| `social-post` | A post on another social network |
| `chat-message` | A message in a team chat tool |
| `blog-post` | A blog article |
| `bio` | A short biography or profile text |

A new channel is a new id registered in the check script. It never changes
`my_voice_format`, so every existing profile keeps passing.

## Size

The contract states the limit. A save that would cross it is refused: say so,
and offer to shorten samples or merge rules before trying again.

## Version rules

- **Pass** -- use the profile.
- **Fail** -- name the `part` to the owner and offer to fix it; do not draft
  from a profile that failed until it is fixed or the owner says to proceed
  with general rules only.
- **Rebuild** -- the profile is in an older format. Build the current format
  from it into `profile-rebuild.md` in the same folder and keep using
  `profile.md` until the owner approves the rebuild. On approval, move the old
  file into `archive/` with its date in the name and save the rebuild as
  `profile.md`.
- **Update** -- the profile was written by a newer version of the skill. Leave
  it unchanged and tell the owner to update the plugin.

Installing a new version of the skill never changes a profile by itself. A
format change raises `my_voice_format`; a new channel id does not.

# Tuning

Improving the profile from what the user does and says, without rewriting it.
Tuning writes the profile, so it runs only in Cowork
(`references/profile-storage.md`, "Support by surface"). In Claude Code, the
Codex CLI or the desktop app chat, note the proposed change and point the user
to Cowork.

## Inputs

- **An edited draft.** The user changes a draft this skill produced. Compare
  the draft with the edited text and name each difference that reflects a
  habit, not a one-off correction of fact.
- **A final published text.** The user shares what they actually sent or
  posted. Compare it with the draft the same way.
- **A stated rule.** The user says how they write ("I never open with a
  question"). It becomes an explicit rule, worded as they said it.
- **New content.** The user offers more of their writing. It goes through the
  screen in `references/voice-creation.md`, "3. Screen each item", before it
  can shape a rule or a sample.

## Propose, never apply

For each change, show:

- the section it touches (and the language or channel),
- the rule before the change (or "none"),
- the rule after the change,
- the cause: which edit, text, statement or content it came from.

Group the proposals and let the user approve, edit or reject each one.
Nothing is written until the user approves it.

## Write approved changes

1. Apply only the approved changes to `profile.md`.
2. Add one change-log entry per change: the date, the section, and the cause.
3. Set `updated` to today.
4. Run the check. Save only a file that passes; a save that would cross the
   size limit is refused per `references/profile-schema.md`, "Size".

An explicit rule the user stated outranks an inferred rule it contradicts:
replace the inferred rule rather than keeping both.

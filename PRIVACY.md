# Privacy

AI Tools is a set of skills that run inside an AI product, such as Claude or
Codex. This page covers what happens to data when one of these skills runs.

- **The skills send nothing to A-CX.** No skill reports usage, content or any
  other data to A-CX.
- **A profile stays with the person who made it.** When a skill saves a profile,
  it keeps it on the computer it runs on or in the AI account it runs in.
- **An AI provider that stores a profile does so under its own terms.** When the
  AI product keeps a profile in its account storage, that provider's terms and
  privacy policy apply to it.
- **GitHub covers visits to this repository.** Viewing or downloading from this
  repository is subject to the
  [GitHub General Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).

## My Voice

My Voice sends nothing to A-CX. It keeps your voice profile in one place: a
folder named `my-voice` directly in your home folder, on your own computer.

| App | Where the profile lives | What the app does with it |
|---|---|---|
| Cowork | The `my-voice` folder on the computer you connect to Cowork: `/Users/<you>/my-voice/` on macOS, `C:\Users\<you>\my-voice\` on Windows | Creates, reads, changes and deletes it |
| Claude Code | The same `my-voice` folder, on the computer where Claude Code runs | Reads it; never changes it |
| Codex CLI | The same `my-voice` folder, on the computer where Codex CLI runs | Reads it; never changes it |

- **No other copy.** My Voice keeps no copy of the profile in a project, a
  repository, a chat memory, an AI account or any online service.
- **The AI in your session reads it.** To create the profile and to draft, My
  Voice gives the profile and the writing you choose to the AI in that session.
  The AI provider, Anthropic or OpenAI, processes that text under its own terms
  and privacy policy.
- **You stay in control.** In Cowork you can view, export or delete the
  profile at any time. Deleting the `my-voice` folder removes the profile and
  its earlier versions from your computer.

This page is the privacy statement for AI Tools. The privacy policy of the A-CX
website does not apply to the skills.

# AI Tools from A-CX

AI Tools is a small, hand-picked set of skills from [A-CX](https://www.a-cx.com)
for Claude and Codex. Each skill is free to use under the
[PolyForm Shield 1.0.0](LICENSE) license, which does not allow using it in a
product that competes with it or with a product A-CX provides using it.

## Skills

| Skill | What it does | Works in | Version |
|---|---|---|---|
| [My Voice](#my-voice) | Learns how you write from your own texts, then drafts emails, posts and messages that sound like you. | Cowork, Claude Code, Codex CLI | 1.0.0 |

A skill lists an app under "Works in" only after it passes verification in that
app for the release. [CHANGELOG.md](CHANGELOG.md) lists every release.

### My Voice

My Voice builds a voice profile from writing you choose, such as emails and
posts you wrote yourself. It then drafts new text under your name that follows
that profile. It drafts only: it never posts or sends anything.

The profile is one file in a folder named `my-voice` in your home folder, on
macOS or Windows. You create and change it in Cowork. Claude Code and Codex CLI
on the same computer read it to draft, and send you to Cowork for any change.

| App | What it does with My Voice | Guide |
|---|---|---|
| Cowork | Creates, tunes and deletes the profile, and drafts with it | [Install in Cowork](guides/cowork.md) |
| Claude Code | Drafts with the profile; changes happen in Cowork | [Install in Claude Code](guides/claude-code.md) |
| Codex CLI | Drafts with the profile; changes happen in Cowork | [Install in Codex](guides/codex.md) |

Claude.ai chat on the web and ChatGPT cannot reach a folder on your computer,
so My Voice cannot use a profile there.

## Install

Pick the guide for the app in use. Each guide covers turning on what the app
needs, installing, updating and removing a skill, and what to do when a step
fails.

| App | Guide |
|---|---|
| Claude Code | [Claude Code](guides/claude-code.md) |
| Cowork in the Claude desktop app | [Cowork](guides/cowork.md) |
| Codex CLI and Codex in the ChatGPT desktop app | [Codex](guides/codex.md) |

[guides/README.md](guides/README.md) explains which guide fits which app and how
an app gets listed.

Claude Code and Codex add this repository as a marketplace with one command:

```text
claude plugin marketplace add withACX/ai-tools
codex plugin marketplace add withACX/ai-tools
```

## Privacy

The skills send nothing to A-CX. A profile a skill creates stays on the
computer it runs on or in the AI account it runs in. My Voice keeps its profile
only on your computer. [PRIVACY.md](PRIVACY.md) has the details for each app.

## License and terms

The skills are free to use under PolyForm Shield 1.0.0, in [LICENSE](LICENSE),
which does not allow competing use, and under the terms of use in
[TERMS.md](TERMS.md). Review what the AI produces and does before you rely on
it; the terms explain why. The license grants no right to the A-CX name or logo.

Claude is a trademark of Anthropic. Codex and ChatGPT are trademarks of OpenAI.
A-CX is not affiliated with, sponsored by or endorsed by Anthropic or OpenAI.

## Help and reporting

- [SUPPORT.md](SUPPORT.md): how to get help and report a bug.
- [SECURITY.md](SECURITY.md): how to report a vulnerability privately.
- [CHANGELOG.md](CHANGELOG.md): what changed in each release.

A-CX is a software design and engineering consultancy. More at
[www.a-cx.com](https://www.a-cx.com).

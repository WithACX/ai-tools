# Install a skill in Cowork

This guide is for Cowork in the Claude desktop app. There are two ways to
install a skill from AI Tools: add the AI Tools marketplace, or upload a skill
ZIP. Both save the skill to the Claude account, so it also works in Claude.ai
chat with the same account.

<!-- surface verification: confirm both paths below in Cowork for each release, and add screenshots. -->

## First: what Cowork needs

1. Install the Claude desktop app and sign in.
2. Turn on code execution, as described in the
   [Claude.ai guide](claude-ai.md#first-turn-on-code-execution).

On a Team or Enterprise plan, an organization owner controls which plugin
sources and skills members can add. When an option below is missing, ask the
organization owner.

## Install

### From the marketplace

1. In the Claude desktop app, open **Customize**.
2. Open **Plugins**.
3. Select **Add**.
4. Select **Add marketplace**.
5. Enter `withACX/ai-tools`.
6. Confirm.
7. Find the plugin named in the skills table of the [main README](../README.md).
8. Select **Add**.
9. Start a new Cowork task to use the skill.

### From a ZIP file

1. Follow the [Claude.ai install steps](claude-ai.md#install) to upload the
   skill ZIP.
2. Start a new Cowork task to use the skill.

## Update

- **From the marketplace:** open **Customize**, then **Plugins**, open the
  AI Tools marketplace and select **Check for updates**. To get updates
  without this step, turn on **Sync automatically** for the marketplace.
- **From a ZIP file:** follow the [Claude.ai update steps](claude-ai.md#update).

Start a new Cowork task after an update.

## Remove

- **From the marketplace:** open **Customize**, then **Plugins**, open the
  plugin, open its menu and select **Remove**. To pause it instead, turn off its
  **Disable plugin** switch.
- **From a ZIP file:** follow the [Claude.ai remove steps](claude-ai.md#remove).

## Troubleshooting

### Adding the marketplace fails

- **Spelling.** The source is exactly `withACX/ai-tools`.
- **Network.** Check that [github.com](https://github.com) opens in a browser on
  the same computer. Then try again.
- **The option is missing.** On a Team or Enterprise plan, an organization owner
  may have turned off adding marketplaces. Ask the owner, or use the ZIP path.

### The upload is refused

See [The upload is refused](claude-ai.md#the-upload-is-refused) in the
Claude.ai guide.

### The skill does not appear in a task

Start a new Cowork task. A task loads plugins and skills only when it starts.

Anthropic describes plugins in Cowork in
[Plugins](https://claude.com/docs/plugins/overview). If none of these help,
report it with the
[bug report form](https://github.com/withACX/ai-tools/issues/new/choose).

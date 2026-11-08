# Install a skill in Codex

This guide is for Codex CLI and for Codex in the ChatGPT desktop app. AI Tools
is a plugin marketplace named `a-cx-ai-tools`. Add it once, then install each
skill's plugin from it.

The Codex IDE extension does not support plugins. To use a skill from AI Tools
with Codex in an editor, install it with Codex CLI or the ChatGPT desktop app.

## First: what Codex needs

1. Install Codex CLI, as OpenAI describes in
   [Codex CLI](https://learn.chatgpt.com/docs/codex/cli).
2. Sign in to Codex when it asks.

<!-- minimum version: the verified minimum Codex CLI version is added here at the first release. -->

## Install

### Codex CLI

1. In a terminal, add the marketplace:

   ```text
   codex plugin marketplace add withACX/ai-tools
   ```

2. Start Codex by typing `codex` and pressing Enter.
3. Type `/plugins` to open the plugin browser.
4. Open the `a-cx-ai-tools` tab.
5. Find the plugin named in the skills table of the [main README](../README.md).
6. Install it.
7. Start a new Codex session to use the skill.

<!-- screenshot: the Codex CLI plugin browser on the a-cx-ai-tools tab. Added at surface verification. -->

### Codex in the ChatGPT desktop app

1. Add the marketplace with Codex CLI, as in step 1 above.
2. Open the ChatGPT desktop app.
3. Open the **Plugins** tab.
4. Find the plugin named in the skills table of the [main README](../README.md).
5. Select the **+** button to install it.
6. Start a new chat to use the skill.

<!-- surface verification: confirm that a marketplace added with Codex CLI appears in the ChatGPT desktop app, and add a screenshot. -->

## Update

1. Refresh the marketplace:

   ```text
   codex plugin marketplace upgrade a-cx-ai-tools
   ```

2. Start a new Codex session or chat to load the new version.

## Remove

1. In Codex CLI, type `/plugins`.
2. Open the plugin.
3. Select uninstall.
4. To remove the whole marketplace as well, run:

   ```text
   codex plugin marketplace remove a-cx-ai-tools
   ```

In the ChatGPT desktop app, open the plugin from the **Plugins** tab and select
**Uninstall plugin**.

## Troubleshooting

### Adding the marketplace fails

- **Spelling.** The source is exactly `withACX/ai-tools`. Retype it rather than
  copying it from a formatted document.
- **Network.** Codex downloads the marketplace from GitHub. Check that
  [github.com](https://github.com) opens in a browser on the same computer, and
  that no company proxy or firewall blocks it. Then try again.
- **An old Codex CLI.** An older Codex CLI may not know the
  `codex plugin marketplace` command. Update Codex CLI, as described in
  [Codex CLI](https://learn.chatgpt.com/docs/codex/cli), then try again.

### The skill does not appear after install

Start a new Codex session or chat. Installed skills load only in sessions that
start after the install.

OpenAI describes plugins in Codex in
[Plugins](https://learn.chatgpt.com/docs/plugins). If none of these help, report
it with the [bug report form](https://github.com/withACX/ai-tools/issues/new/choose).

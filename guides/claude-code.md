# Install a skill in Claude Code

This guide is for Claude Code in the terminal. AI Tools is a plugin marketplace
named `a-cx-ai-tools`. Add it once, then install each skill's plugin from it.

## First: what Claude Code needs

1. Install Claude Code, as Anthropic describes in
   [Set up Claude Code](https://code.claude.com/docs/en/setup).
2. Start Claude Code in a terminal by typing `claude` and pressing Enter.

Use the latest version of Claude Code. To update an installed Claude Code, type
`claude update` in a terminal.

## Install

1. In a Claude Code session, add the marketplace:

   ```text
   /plugin marketplace add withACX/ai-tools
   ```

2. Wait for `Successfully added marketplace: a-cx-ai-tools`.
3. Find the plugin name of the skill in the skills table of the
   [main README](../README.md).
4. Install it, replacing `<plugin>` with that name:

   ```text
   /plugin install <plugin>@a-cx-ai-tools
   ```

5. Choose the installation scope Claude Code offers, then confirm.
6. Type `/` and check that the skill appears under the plugin name.

The same steps work from a shell, without starting a session:

```text
claude plugin marketplace add withACX/ai-tools
claude plugin install <plugin>@a-cx-ai-tools
```

## Update

Claude Code does not update plugins from this marketplace automatically unless
auto-update is on.

1. Refresh the marketplace:

   ```text
   /plugin marketplace update a-cx-ai-tools
   ```

2. Run `/plugin`.
3. Open the **Installed** tab.
4. Select the plugin.
5. Select **Update now**.
6. Run `/reload-plugins`, or start a new session, to load the new version.

To turn on automatic updates instead, run `/plugin`, open the **Marketplaces**
tab, select `a-cx-ai-tools` and select **Enable auto-update**.

## Remove

1. Remove one plugin:

   ```text
   /plugin uninstall <plugin>@a-cx-ai-tools
   ```

2. To remove the whole marketplace and every plugin installed from it:

   ```text
   /plugin marketplace remove a-cx-ai-tools
   ```

## Troubleshooting

### Adding the marketplace fails

- **Spelling.** The source is exactly `withACX/ai-tools`. Retype it rather than
  copying it from a formatted document.
- **Network.** Claude Code downloads the marketplace from GitHub. Check that
  [github.com](https://github.com) opens in a browser on the same computer, and
  that no company proxy or firewall blocks it. Then try again.
- **An old Claude Code.** An older Claude Code may not know the
  `/plugin marketplace` command. Update Claude Code, as described in
  [Set up Claude Code](https://code.claude.com/docs/en/setup), then try again.

### The skill does not appear after install

Run `/reload-plugins`, or close Claude Code and start it again. Then type `/` and
look for the plugin name.

Anthropic lists other error messages and their fixes in
[Discover and install plugins](https://code.claude.com/docs/en/discover-plugins).
If none of these help, report it with the
[bug report form](https://github.com/withACX/ai-tools/issues/new/choose).

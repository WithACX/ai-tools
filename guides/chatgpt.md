# Install a skill in ChatGPT

This guide is for ChatGPT on the web and in the ChatGPT desktop app. OpenAI
offers several ways to add a skill, and which ones are available depends on the
ChatGPT plan, the app and the workspace settings. Pick the first channel below
that the plan and app offer.

OpenAI describes these channels in
[Plugins in ChatGPT and Codex](https://help.openai.com/en/articles/20001256) and
[Plugins](https://learn.chatgpt.com/docs/plugins).

<!-- surface verification: confirm each channel per plan and app for each release, and add screenshots. -->

## First: check what the plan offers

| Channel | Where it works | Who can use it |
|---|---|---|
| Upload a skill ZIP | ChatGPT, where the plan offers skill upload | Each person, on a plan that offers it |
| The AI Tools marketplace | Codex in the ChatGPT desktop app | Each person with the desktop app |
| GitHub import by a workspace admin | Every member of the workspace | A workspace admin sets it up once |

Codex in an editor, through the IDE extension, does not support plugins.

## Install

### Upload a skill ZIP

1. Open the [latest release](https://github.com/withACX/ai-tools/releases/latest).
2. Under **Assets**, select the ZIP file named for the skill. Do not use
   **Source code (zip)**.
3. Save the file. Keep it zipped.
4. Upload it in ChatGPT where the plan offers skill upload, as OpenAI describes
   in [Plugins in ChatGPT and Codex](https://help.openai.com/en/articles/20001256).

### The AI Tools marketplace in the ChatGPT desktop app

Follow [Codex in the ChatGPT desktop app](codex.md#codex-in-the-chatgpt-desktop-app)
in the Codex guide.

### GitHub import by a workspace admin

A workspace admin does these steps once for the whole workspace.

1. Open **Admin**.
2. Open **Plugins**.
3. Select **Add**.
4. Select **Import marketplace**.
5. In **Source**, enter `https://github.com/withACX/ai-tools`.
6. Leave **Path** empty.
7. Leave **Branch, tag, or commit** empty, so the workspace gets later releases.
8. Select **Import marketplace**.
9. Authorize GitHub access when asked.
10. Open each imported plugin and set its installation policy.

Members then find the plugin on the **Plugins** tab under the workspace name.
OpenAI describes the import in
[Import and sync plugins from GitHub](https://learn.chatgpt.com/docs/enterprise/plugin-management).

### When no channel is available

When the plan or app offers none of these channels, a skill from AI Tools cannot
be installed there today. Use another app from the [install guides](README.md),
or ask the workspace admin about the GitHub import.

## Update

- **Uploaded ZIP:** remove the old version and upload the new one from the
  [latest release](https://github.com/withACX/ai-tools/releases/latest).
- **Desktop app marketplace:** follow the [Codex update steps](codex.md#update).
- **Workspace import:** the workspace syncs from GitHub each day. Nothing to do.

Start a new chat after an update.

## Remove

For a plugin from the marketplace or the workspace import:

1. Open the **Plugins** tab.
2. Open the plugin.
3. Select **Uninstall plugin**.

For an uploaded skill ZIP, remove the skill where it was uploaded, as OpenAI
describes in [Plugins in ChatGPT and Codex](https://help.openai.com/en/articles/20001256).

A plugin the workspace installed for everyone may not offer this option. The
workspace admin controls it.

## Troubleshooting

### The upload or install option is missing

The plan or the workspace settings may not offer that channel. Check the table
in [First: check what the plan offers](#first-check-what-the-plan-offers), or
ask the workspace admin.

### The skill does not appear in a chat

Start a new chat. Installed skills load only in chats that start after the
install.

### Adding or importing the marketplace fails

Check that the source is exactly `withACX/ai-tools`, and that
[github.com](https://github.com) opens in a browser. For a workspace import,
check that the admin authorized GitHub access.

If none of these help, report it with the
[bug report form](https://github.com/withACX/ai-tools/issues/new/choose).

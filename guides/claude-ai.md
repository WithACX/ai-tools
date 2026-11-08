# Install a skill in Claude.ai

This guide is for Claude.ai on the web and chat in the Claude desktop app. A
skill arrives as a ZIP file from the latest release and is uploaded to the
Claude account. Once uploaded, the skill also works in Cowork with the same
account.

## First: turn on code execution

Skills need code execution. Turn it on first, or the upload fails.

1. Open [claude.ai](https://claude.ai) and sign in.
2. Open **Settings**.
3. Open **Capabilities**.
4. Turn on **Code execution and file creation**. In the newer settings layout
   this switch is called **Create and edit files**.

<!-- screenshot: Settings, Capabilities, with the code execution switch on. Added at surface verification. -->

On a Team or Enterprise plan, an organization owner controls this switch and
the use of skills. If the switch is missing or gray, see
[An admin turned skills off](#an-admin-turned-skills-off).

## Install

1. Open the [latest release](https://github.com/withACX/ai-tools/releases/latest).
2. Under **Assets**, select the ZIP file named for the skill. Do not use
   **Source code (zip)**.
3. Save the file. Keep it zipped.
4. In Claude.ai, open **Customize**.
5. Open **Skills**.
6. Select the **+** button.
7. Select **Create skill**.
8. Select **Upload a skill**.
9. Choose the ZIP file saved in step 3.
10. Check that the skill appears in the skills list with its switch on.

<!-- screenshot: Customize, Skills, the upload dialog. Added at surface verification. -->

To use the skill, describe the task in a chat. Claude loads the skill when the
task matches it.

## Update

Claude.ai does not update an uploaded skill by itself. To move to a newer
version:

1. Open the [latest release](https://github.com/withACX/ai-tools/releases/latest)
   and check the skill's version in [CHANGELOG.md](../CHANGELOG.md).
2. Remove the old version, as described in [Remove](#remove).
3. Install the new version, as described in [Install](#install).

## Remove

1. Open **Customize**.
2. Open **Skills**.
3. Select the skill.
4. To pause it, turn off the switch in the upper right corner.
5. To delete it, select the **...** button next to the switch.
6. Select **Delete**.
7. Select **Delete** again to confirm.

## Troubleshooting

### Code execution is off

The upload or the skill fails when code execution is off. Follow
[First: turn on code execution](#first-turn-on-code-execution), then try again.

### An admin turned skills off

On Team and Enterprise plans, an organization owner decides whether members can
use and upload skills. When **Skills** is missing from **Customize**, or the
upload option is not offered, ask the organization owner to turn skills on. The
owner steps are in [For Team and Enterprise admins](#for-team-and-enterprise-admins).

### The upload is refused

Check each of these, then upload again:

- **The wrong file.** Upload the ZIP named for the skill from the release
  **Assets**, never **Source code (zip)**.
- **The file was unzipped.** Some browsers and computers unzip a download on
  their own. Download the file again and upload the ZIP itself.
- **An older copy is still installed.** Delete the old version first, as
  described in [Remove](#remove).
- **Code execution or skills are off.** See the two sections above.

If the upload is still refused, report it with the
[bug report form](https://github.com/withACX/ai-tools/issues/new/choose) and
include the exact message Claude.ai shows.

## For Team and Enterprise admins

An organization owner can turn skills on for members and provision a skill for
everyone.

1. Open **Organization settings**.
2. Open **Plugins & skills**.
3. Open the **Policy** tab.
4. Turn on **Code execution and file creation**.
5. Turn on **Skills**.

With skills on, each member can upload a skill as described in
[Install](#install). To provision a skill for the whole organization, the owner
uploads its ZIP in organization settings, and it appears in every member's
skills list. Anthropic describes both in
[Use Skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

<!-- screenshot: Organization settings, Plugins & skills, Policy tab. Added at surface verification. -->

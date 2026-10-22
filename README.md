# AIKIZI skills

[Agent Skills](https://agentskills.io) for [AIKIZI](https://aikizi.com), a public gallery of image style decodes.
Each decode names the styles, style DNA, subjects, moods, key tokens, colour palette and a ready generation prompt.

| Skill | What it does | Needs |
|---|---|---|
| [`aikizi-styles`](skills/aikizi-styles/SKILL.md) | Find a visual style, break it down, hand over the prompt and palette | Network. No sign-in, no API key |

Works in any agent that reads `SKILL.md` skills: Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot and others.
If the AIKIZI MCP server is connected, the skill uses its tools. If not, it runs a small Python script
(standard library only) that calls the same two public tools.

## Install

```bash
npx skills add Bashocodes/aikizi-skills
```

Or copy `skills/aikizi-styles/` into your agent's skills folder (for example `~/.claude/skills/`).

## Try it

- `Find decoded styles with warm film grain and soft window light.`
- `Break down https://aikizi.com/decode/93f32917-54d2-49e4-8214-a541a77bcaa5 and give me the prompt.`
- `I want an ink wash landscape. Show me three references and their palettes.`

## Your own images

Decoding your own image, reading your library and checking credits need an AIKIZI account and the MCP server at
`https://aikizi.com/mcp`. Setup for each agent is in
[`skills/aikizi-styles/references/connect.md`](skills/aikizi-styles/references/connect.md). Claude users can
install the [AIKIZI plugin](https://github.com/Bashocodes/aikizi-claude-plugin) instead.

## What runs and what is sent

- `scripts/aikizi.py` sends only your search words or a decode id to `https://aikizi.com/mcp`. It reads no files,
  keys or environment, and writes nothing.
- Results contain only decodes their owners chose to publish.

Privacy: https://aikizi.com/legal/privacy · Terms: https://aikizi.com/legal/terms · Support: hello@aikizi.com

## License

MIT, see [LICENSE](LICENSE).

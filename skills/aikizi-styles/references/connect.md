# Connect the AIKIZI MCP server

The server is `https://aikizi.com/mcp` (streamable HTTP). Public tools work without sign-in. Account tools ask the
person to sign in on aikizi.com through OAuth the first time; nothing is shared until they allow it.

| Agent | How to add it |
|---|---|
| Claude Code | `claude mcp add --transport http aikizi https://aikizi.com/mcp` |
| Claude (web, desktop) | Directory → Connectors → AIKIZI |
| Cursor | `mcp.json`: `{"mcpServers": {"aikizi": {"url": "https://aikizi.com/mcp"}}}` |
| Gemini CLI | `settings.json`: `{"mcpServers": {"aikizi": {"httpUrl": "https://aikizi.com/mcp"}}}` |
| Other MCP clients | Add a remote HTTP server with the URL above |

## Tools

| Tool | Sign-in | Spends credits | What it does |
|---|---|---|---|
| `search_styles` | no | no | Search published decodes by style, subject, mood or colour |
| `get_style_decode` | no | no | Full breakdown of one published decode |
| `check_balance` | yes | no | The account's credit balance |
| `decode_image` | yes | yes | Decode an image from a public https link |
| `check_job_status` | yes | no | Follow a decode that is still running |
| `get_my_decode` | yes | no | Read one of the account's own decodes |
| `list_my_creations` | yes | no | List the account's library |
| `get_creation` | yes | no | Open one image generated on aikizi.com |

## Before a paid call

- Run `check_balance` first and tell the person the balance in one line. At zero, stop and point them to aikizi.com.
- Say in one sentence what you will decode before calling `decode_image`. Never call a paid tool to test the
  connection; `check_balance` is the test.
- `decode_image` needs a public, direct `https://` link to a JPEG, PNG or WebP up to 10 MB. If it says "still
  running", poll `check_job_status` about every 10 seconds for up to two minutes, then read `get_my_decode`.
- New decodes stay private in the person's library. Never claim one is published.

Privacy: https://aikizi.com/legal/privacy · Terms: https://aikizi.com/legal/terms · Support: hello@aikizi.com

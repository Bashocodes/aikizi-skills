#!/usr/bin/env python3
"""Read public AIKIZI style decodes without an MCP client.

Calls the two public tools on https://aikizi.com/mcp over plain JSON-RPC.
No sign-in, no API key, no dependencies beyond Python 3.8+.

  python3 scripts/aikizi.py search "neon noir portrait" --limit 8
  python3 scripts/aikizi.py decode 93f32917-54d2-49e4-8214-a541a77bcaa5
  python3 scripts/aikizi.py decode https://aikizi.com/decode/<id> --json

Default output is the readable text AIKIZI returns. --json prints the
structured result (ids, styles, style_dna, key_tokens, palette, prompt, url).
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

ENDPOINT = "https://aikizi.com/mcp"
TIMEOUT = 30

# Exit codes: 0 ok · 2 bad arguments · 3 network or HTTP failure · 4 AIKIZI refused the request
EPILOG = """examples:
  scripts/aikizi.py search "neon noir portrait" --limit 8
  scripts/aikizi.py decode https://aikizi.com/decode/<id> --json

exit codes: 0 ok, 2 bad arguments, 3 network/HTTP failure, 4 AIKIZI refused (e.g. unknown id)"""


def fail(code, message):
    print(f"aikizi: {message}", file=sys.stderr)
    sys.exit(code)


def call(tool, arguments):
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool, "arguments": arguments},
    }).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": "aikizi-agent-skill/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        fail(3, f"server answered HTTP {e.code}. Try again in a minute.")
    except urllib.error.URLError as e:
        fail(3, f"could not reach {ENDPOINT} ({e.reason}). Check network access.")

    # The server answers plain JSON; tolerate an SSE frame just in case.
    if raw.lstrip().startswith("event:") or raw.lstrip().startswith("data:"):
        raw = next((l[5:] for l in raw.splitlines() if l.startswith("data:")), "{}")
    try:
        msg = json.loads(raw)
    except ValueError:
        fail(3, "the server answered something that is not JSON. Try again in a minute.")
    if "error" in msg:
        fail(4, msg["error"].get("message", "request failed"))
    result = msg.get("result", {})
    if result.get("isError"):
        text = " ".join(c.get("text", "") for c in result.get("content", []))
        fail(4, text or "tool error")
    return result


def main():
    p = argparse.ArgumentParser(description="Search and read public AIKIZI style decodes.",
                                epilog=EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="find published decodes by words")
    s.add_argument("query", help="2-6 style, subject, mood or colour words")
    s.add_argument("--limit", type=int, default=8, help="1-20 results (default 8)")
    s.add_argument("--json", action="store_true", help="print the structured result")
    d = sub.add_parser("decode", help="full breakdown of one published decode")
    d.add_argument("id", help="decode id or https://aikizi.com/decode/<id> link")
    d.add_argument("--json", action="store_true", help="print the structured result")
    a = p.parse_args()

    if a.cmd == "search":
        query = a.query.strip()
        if not 2 <= len(query) <= 200:
            fail(2, f"the query must be 2-200 characters; got {len(query)}.")
        result = call("search_styles", {"query": query, "limit": max(1, min(20, a.limit))})
    else:
        result = call("get_style_decode", {"id": a.id.strip()})

    if a.json and "structuredContent" in result:
        print(json.dumps(result["structuredContent"], indent=2, ensure_ascii=False))
    else:
        print("\n".join(c.get("text", "") for c in result.get("content", []) if c.get("type") == "text"))


if __name__ == "__main__":
    main()

# MCP Server

The [Companion](Companion.md) can expose your display as a set of
**[MCP](https://modelcontextprotocol.io) tools** — so an LLM (Claude, an agent, an IDE
assistant) can *drive the wall in plain language*, and, just as importantly, **read it back**.

> This is a **companion feature**. It's a standalone HTTP server and has nothing to do with
> Home Assistant — you don't need HA to use it.

The difference from a webhook or a REST call is that the model isn't following a script you
wrote. It can look at the board, decide the message won't fit, shorten it, pick a transition,
show it for 30 seconds, and put back what was playing — because each of those is a tool it
can choose to call.

## Turn it on

| Where you run the companion | How |
|---|---|
| Home Assistant App | Configuration tab → `mcp: true` (optionally pin `mcp_token`) |
| Docker / anywhere | `-e COMPANION_MCP=1` (optionally `-e COMPANION_MCP_TOKEN=…`) |

The companion mints a **bearer token** on first enable and persists it. The **⚙ menu** shows
both the token and the server's address — typically:

```text
http://<companion-host>:8000/mcp
```

The transport is **streamable HTTP** (not stdio), so any MCP client that speaks HTTP can
connect over your LAN. The token guards `/mcp` only; with MCP off, the path 404s.

## Connect a client

**Claude Code:**

```bash
claude mcp add --transport http splitflap http://companion-host:8000/mcp \
  --header "Authorization: Bearer <token>"
```

**Claude Desktop** — add a remote MCP server (Settings → Connectors) with the same URL and
`Authorization: Bearer <token>` header. Any other MCP-capable client works the same way.

## What it exposes

Twelve tools — enough to see the board, change it, and run the content engine:

| Tool | What it does |
|---|---|
| `get_display` | What the display is showing right now — the text, the grid, and which app or playlist is running. **This is the one that makes the rest work**: the model can *look before it acts.* |
| `show_message` | Show text, centred and word-wrapped. Optional `style` (transition) and `seconds` — with `seconds`, the board **reverts to whatever was playing** afterwards. |
| `clear_display` | Blank every module, stopping anything running. |
| `stop` | Stop the app/playlist. Nothing is running, so the wall blanks. |
| `list_apps` | The installed apps (weather, clock, stocks, …). |
| `run_app` | Run one of them. |
| `get_app_settings` | An app's settings and their current values. |
| `configure_app` | Change them. |
| `list_playlists` / `run_playlist` | The saved playlists, and run one by name. |
| `list_styles` | The flap transition styles `show_message` accepts. |
| `list_displays` | Every wall this companion drives, and which one is the default. |

Notice what that combination buys you: **read → decide → act → revert**. The model can check
what's on the board before overwriting it, and it can borrow the display for a moment without
destroying your playlist.

## More than one wall

Every tool takes an optional **`display`** argument. Omit it and the tool drives the
**default** display, which is what a single-wall setup has always done — so nothing an agent
already knows how to do changes.

`list_displays` is how an agent discovers the others. Ask for "what's on the office wall" and
it can look the id up and pass it:

```
list_displays()                        -> [{id: "default", name: "Living room", default: true},
                                            {id: "office-wall", name: "Office wall"}]
get_display(display="office-wall")     -> what that wall is showing
run_app("weather", display="office-wall")
```

See **[Multiple Displays](Multiple-Displays.md)**.

## What you can actually do with it

Things that work today, phrased the way you'd say them to Claude:

- **"What's on the split-flap right now?"** — `get_display` answers with the literal text,
  so the model can read your wall back to you from anywhere.
- **"Put 'STANDUP IN 5' on the board for two minutes, then put back whatever was playing."**
  — one `show_message` with `seconds=120`; the revert is automatic.
- **"Show the weather, but for Lisbon instead of here."** — `get_app_settings` to see the
  location field, `configure_app` to change it, `run_app` to show it. The model discovers the
  setting names itself; you don't have to know them.
- **"Something's wrong with the board — what's it doing?"** — `get_display` plus `list_apps`
  is usually enough for it to tell you the playlist is running but the weather app is erroring.
- **"Make a message that fits."** The grid is 15 × 3 — 45 characters. Ask for a haiku, a
  countdown, a birthday greeting, and the model can *see* the dimensions from `get_display`
  and write to fit them, which is exactly the part humans find annoying.
- **"Run the morning playlist and set it to Celsius first."**

Where it gets more interesting is when the display is one tool among several. Because the
model also has your other tools, the split-flap stops being a thing you *configure* and
becomes a thing you *mention*:

> *"Check if the build is green; if it broke, put the failing job on the split-flap in red."*
>
> *"When my next meeting is within 10 minutes, flash its title on the board for 30 seconds."*
>
> *"Summarise today's PRs into 45 characters and show it."*

None of that needed a new app, a template, or a line of YAML — the LLM composed it out of the
tools it already had.

## Notes and limits

- **The board is shared state.** `show_message` without `seconds` takes the display over until
  something else changes it — that's usually what you want for a one-off, and rarely what you
  want inside an automation. Prefer `seconds` when interrupting.
- **`show_message` waits for the flaps.** It returns after the modules have been sent the new
  text, so an agent that immediately calls `get_display` sees the new board, not the old one.
- The token is a **bearer token in a header** — treat it like a password, and keep the
  companion off the public internet. It guards `/mcp` and nothing else.
- What can be *shown* still depends on what's printed on your reels →
  [Flaps & character sets](Flaps-and-Character-Sets.md).

---
**See also:** [Vestaboard-compatible API](Vestaboard-API.md) · [Home Assistant](Home-Assistant.md) · [Companion](Companion.md)

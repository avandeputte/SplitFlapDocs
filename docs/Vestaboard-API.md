# Vestaboard-compatible API

A **[Vestaboard](https://www.vestaboard.com/)** is a commercial split-flap display with a
widely-used **Local API**. Turn this on and the [Companion](Companion.md) *answers that same
API* — so anything already written for a Vestaboard drives **your** wall instead, unchanged.

That's a large pool of software you get for free: Home Assistant integrations, Node-RED
flows, shell scripts, dashboards, whatever someone published for their Vestaboard.

> This is a **companion feature**, and it has nothing to do with Home Assistant — it's plain
> HTTP. HA is just one of the many things that can talk to it.

## Turn it on

| Where you run the companion | How |
|---|---|
| Home Assistant App | Configuration tab → `vestaboard: true` (optionally pin `vestaboard_key`) |
| Docker / anywhere | `-e COMPANION_VESTABOARD=1` (optionally `-e COMPANION_VESTABOARD_KEY=…`) |

The companion **mints an API key** the first time you enable it and persists it. Find it in
the companion's **⚙ menu**, which also shows the full endpoint URL. Pin your own key with
`vestaboard_key` / `COMPANION_VESTABOARD_KEY` if you'd rather choose it (handy when you're
migrating configs off a real Vestaboard).

> **What the key protects:** only `/local-api/*`. It is *not* a login for the companion —
> the rest of the UI and API stay as open (or as firewalled) as they were.

## The endpoints

Base path **`/local-api/message`**, authenticated with the header
**`X-Vestaboard-Local-Api-Key`** — exactly as the real thing.

### Read the board

```bash
curl http://companion-host:8000/local-api/message \
  -H "X-Vestaboard-Local-Api-Key: $KEY"
```

```json
{ "message": [[0,0,8,5,12,12,15,0,0], [0,0,0,0,0,0,0,0,0]] }
```

A row-per-line matrix of **Vestaboard character codes** (`0` = blank, `1–26` = `A–Z`,
`27–36` = digits, then punctuation, then the colour chips). Your wall's real grid size is
used, whatever it is.

### Post a message

Returns **`201 Created`**. It takes every shape a Vestaboard client sends:

```jsonc
[[0,8,5,12,12,15], …]                       // a bare character-code matrix
{"characters": [[…]], "strategy": "…"}      // …with an animation strategy
{"text": "HELLO"}                           // our extension — plain text, centred + wrapped
```

The `{"text": …}` form is ours, because most people just want to send words:

```bash
curl -X POST http://companion-host:8000/local-api/message \
  -H "X-Vestaboard-Local-Api-Key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "DINNERS READY"}'
```

Posting **takes the display over** — any running app or playlist is cancelled, which is what
posting to a Vestaboard implies.

A missing or wrong key returns **`401`** with the plain-text body `Invalid API key`, and
`POST /local-api/enablement` returns the key — both quirks of the real Local API that clients
test for verbatim.

### More than one wall

A Vestaboard client has no way to say *which* board it means — the real product is one board —
so `/local-api/message` always drives the **default** display.

To reach another wall, put its id in the path:

```
GET  /local-api/office-wall/message
POST /local-api/office-wall/message
```

Everything else is identical, key included. See **[Multiple Displays](Multiple-Displays.md)**.

## Using it from Home Assistant

Two ways, and neither needs the [HACS integration](Home-Assistant.md#2-the-hacs-integration):

**The `ha-vestaboard` integration** — [natekspencer/ha-vestaboard](https://github.com/natekspencer/ha-vestaboard)
works against the companion as-is. Point it at `http://companion-host:8000` and give it the
key from the ⚙ menu.

**Or no integration at all** — a plain `rest_command`:

```yaml
rest_command:
  splitflap_message:
    url: "http://companion-host:8000/local-api/message"
    method: POST
    headers:
      X-Vestaboard-Local-Api-Key: !secret splitflap_api_key
    content_type: "application/json"
    payload: '{"text": "{{ message }}"}'
```

> **Which should I use?** If you're starting fresh in Home Assistant, the
> [HACS integration](Home-Assistant.md#2-the-hacs-integration) is richer — it exposes apps and
> playlists as entities, which the Vestaboard API has no concept of. Use the Vestaboard API
> when you want to **reuse software that already exists**.

## Limits

- Vestaboard's **character set** is what the API speaks, so anything outside it can't be
  expressed as codes (send `{"text": …}` and let the companion map it instead).
- What actually lights up still depends on **what's printed on your reels** — see
  [Flaps & character sets](Flaps-and-Character-Sets.md).
- It's the **Local** API only: no Vestaboard cloud, subscriptions or accounts are involved,
  and nothing leaves your network.

---
**See also:** [MCP Server](MCP-Server.md) · [Home Assistant](Home-Assistant.md) · [Companion](Companion.md)

# Companion without Home Assistant

The [Companion](Companion.md) doesn't need Home Assistant — it's a plain web app in a
Docker container, happy on a NAS, a Raspberry Pi or any home server. This page is the
standalone route: the Docker image, the install script, the full environment-variable
reference, and how settings survive a dead SD card.

Running Home Assistant? The add-on is the easier path — see
**[Home Assistant](Home-Assistant.md)**. Everything below applies to the container either
way; the add-on just replaces environment variables with a Configuration tab.

## Quick start

The only thing you **must** configure is `GATEWAY_URL` — the companion refuses to start
without it. Use the gateway's **IP address**, not its `.local` name: containers
frequently can't resolve mDNS names (→ [Finding the gateway's IP](SplitFlap-Gateway.md#finding-it-on-your-network)).

```bash
docker run -d --name splitflap-companion -p 8000:8000 \
  -e GATEWAY_URL=http://192.168.1.50 \
  -e COMPANION_PUBLIC_URL=http://192.168.1.42:8000 \
  -v companion-data:/data \
  ghcr.io/avandeputte/splitflap-gateway-companion:latest
# open http://<host>:8000
```

`COMPANION_PUBLIC_URL` is **this machine's LAN address** (not the gateway's) — it's what
the companion registers with the gateway so the gateway's *Companion* tab can link back.
Set it whenever you run in Docker: on a bridge network the companion can only see its own
`172.17.x.x` address, which your gateway — a device out on the LAN — cannot reach. It
logs a warning if it has to guess, and nothing else depends on it: driving the display
works either way.

**The image.** `ghcr.io/avandeputte/splitflap-gateway-companion` is **multi-arch** —
the same tag runs on x86 (Windows/Linux) and arm64 (Raspberry Pi 64-bit, Apple Silicon);
Docker pulls the right architecture. Use `:latest` unless you have a reason to pin a
specific release tag.

**Docker Compose.** The repo ships a
[docker-compose.yml](https://github.com/avandeputte/SplitFlapGatewayCompanion/blob/main/docker-compose.yml)
with the same setup (port 8000, a `companion-data` volume on `/data`,
`restart: unless-stopped`, every env var as a commented example):

```bash
docker compose pull && docker compose up -d
```

Two compose-only variables go in `.env`: `GHCR_OWNER` (defaults to `avandeputte`) and
`COMPANION_TAG` (defaults to `latest`; set it to pin a release). `build: .` is kept as
a fallback, so `docker compose build` works without the registry.

## The install script

One command sets everything up on a Raspberry Pi or any x86-64 Linux box:

```bash
curl -fsSL https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/install.sh | bash
```

It:

- installs **Docker** if it's absent,
- asks for the **gateway URL** and an optional MQTT password,
- optionally deploys a **Mosquitto broker** — only needed for the
  [Home Assistant MQTT device](Home-Assistant.md#3-the-mqtt-device); skip it if your
  gateway already has a broker (or you don't use HA at all),
- writes a **docker-compose project** and starts the companion, auto-detecting this
  host's IP so the gateway can link back,
- can add a **Watchtower** container that auto-updates the companion every 6 h.

Every prompt has an env-var override, so it runs **unattended**:

```bash
GATEWAY_URL=http://192.168.1.50 DEPLOY_MQTT=no AUTO_UPDATE=yes \
  bash -c "$(curl -fsSL https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/install.sh)"
```

To update by hand instead of Watchtower:
`cd <project-dir> && docker compose pull && docker compose up -d`.

## Configuration reference

**There is no config file.** Configuration is derived at runtime from
`defaults ← gateway ← environment` and never written to disk — nothing to seed, migrate
or back up. The gateway is the **source of truth** for grid size and the MQTT broker
(read from its `/api/config` on startup and on Sync); the environment is for the few
things the gateway can't know. Env always wins. Normally `GATEWAY_URL` is the only
thing you set.

### Core

| Variable | Default | Does |
|---|---|---|
| `GATEWAY_URL` | *(none — **required**)* | Gateway base URL: REST transport, config sync, status. Takes a **comma-separated list** to drive [several displays](Multiple-Displays.md). |
| `COMPANION_PUBLIC_URL` | *(auto-detected)* | This companion's own URL, registered with the gateway for its *Companion* tab. Set it in Docker — the auto-detected bridge address isn't reachable from the LAN. |
| `COMPANION_DATA_DIR` | `/data` in Docker (`<repo>/data` otherwise) | Where app settings, playlists, triggers and uploaded apps live — the volume to keep. |

### Features

Both are **off by default** and 404 as a whole when off; both are also toggleable at
runtime from the **⚙ tools menu**, which shows the generated key/token.

| Variable | Default | Does |
|---|---|---|
| `COMPANION_VESTABOARD` | off | Answer the **[Vestaboard Local API](Vestaboard-API.md)**, so anything written for a Vestaboard drives this wall. Clients that hard-code a real board's port 7000 are satisfied by also publishing the container as `-p 7000:8000` — there's no second server. |
| `COMPANION_VESTABOARD_KEY` | *(generated)* | The key clients send as `X-Vestaboard-Local-Api-Key`. Blank → generated on first use and kept with your settings. Guards **only** `/local-api/*`. |
| `COMPANION_VESTABOARD_ENABLEMENT_TOKEN` | *(unset)* | Enables Vestaboard's enablement handshake: `POST /local-api/enablement` with this value as `X-Vestaboard-Local-Api-Enablement-Token` returns the API key above. Unset simply refuses that exchange — take the key from the ⚙ menu instead. |
| `COMPANION_MCP` | off | Expose the display as **[MCP tools](MCP-Server.md)** at `/mcp`, so an LLM client can show a message, run an app, or read the board. |
| `COMPANION_MCP_TOKEN` | *(generated)* | The bearer token for `Authorization: Bearer …`. Blank → generated on first use and kept with your settings. Guards **only** `/mcp`. |

### Transport & MQTT

The companion **always** drives the display over the gateway's REST API — there is no
transport setting. MQTT exists only for the Home Assistant MQTT device.

| Variable | Default | Does |
|---|---|---|
| `COMPANION_SYNC_FROM_GATEWAY` | `true` | Pull grid size + MQTT settings from the gateway on startup. |
| `COMPANION_HA` | `auto` | Home Assistant MQTT device: `auto` (follow the gateway's HA setting, same broker) \| `true` \| `false`. |
| `COMPANION_MQTT_PASSWORD` | *(blank)* | Broker password, for Home Assistant only — the gateway never exposes it. Blank for an anonymous broker. |
| `COMPANION_GRID_ROWS` / `_COLS` | *(from gateway)* | Manual panel-size override — only if not reading from the gateway. |
| `COMPANION_MQTT_BROKER` / `_PORT` / `_PREFIX` / `_USER` | *(from gateway)* | Manual MQTT overrides — same caveat. |

### Behaviour

| Variable | Default | Does |
|---|---|---|
| `COMPANION_SETTINGS_STORE` | `mirror` | Where settings live: `mirror` \| `local` \| `gateway` — see [below](#settings-storage-disaster-recovery). |
| `COMPANION_MODULE_ID_BASE` | `0` | Module id of grid index 0 (companion-owned; not read from the gateway). |
| `COMPANION_UI_LANGUAGE` | *(unset)* | Deployment default for the web UI's **chrome** language. Unset falls through to the viewer's browser language. Never affects the flap *content* language — that's the global Language setting. |
| `COMPANION_DEV_MODE` | off | Adds **simulation mode** to the ⚙ tools menu: run apps without driving the wall, with a grid override while simulating. |
| `COMPANION_LOG_LEVEL` | `INFO` | `DEBUG` \| `INFO` \| `WARNING` \| `ERROR` \| `CRITICAL`. `DEBUG` adds the companion's own detail (gateway sync, settings mirror, app fetches) without noisy third-party wire logs. |
| `COMPANION_RELOAD` | off | Auto-reload on code changes — [local development](#local-development) only. |

## Settings storage & disaster recovery

The companion keeps its settings, playlists and triggers in
`<data_dir>/app_settings.json`, and can also mirror them onto the gateway — the wall
itself becomes the backup. `COMPANION_SETTINGS_STORE` picks the mode:

| Mode | Where settings live | Use it when |
|---|---|---|
| `mirror` *(default)* | Local file is primary; every change is mirrored to the gateway (gzipped, debounced) | You want a fresh container to recover itself |
| `local` | Local file only; the gateway is never touched | Pre-3.1 behaviour, or you'd rather the gateway held nothing |
| `gateway` | Only on the gateway; nothing written locally | A diskless companion |

**Restore on boot.** In `mirror` mode, a fresh host with **no local file restores from
the gateway**; an empty gateway is seeded from the local copy. So if the NAS dies or the
SD card corrupts: start a new container anywhere, point `GATEWAY_URL` at the same
gateway, and your playlists, triggers and app settings come back from the wall itself.
With [several displays](Multiple-Displays.md), the display registry and each display's
settings ride along in **every** gateway's blob — one gateway URL brings the other walls
back too, with their names and your chosen default.

The fine print:

- `mirror` and `gateway` need **Gateway 3.1+**; on an older gateway they automatically
  degrade to `local` (fully 3.0-compatible).
- The blob is tiny (~1–2 KB gzipped), writes are debounced, and display frames pause
  during a transfer — it never floods the gateway.
- **Uploaded custom apps don't mirror** — they live in `<data_dir>/apps/`, and only the
  settings blob moves. Keep the `/data` volume (or re-upload the `.zip`s) if you run
  your own apps.

## Local development

```bash
cd backend
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
GATEWAY_URL=http://192.168.1.50 python -m app   # required; binds 0.0.0.0:8000
GATEWAY_URL=http://192.168.1.50 COMPANION_RELOAD=1 python -m app   # auto-reload
pytest                                          # run the tests
```

Run it with `python -m app`, **not** a bare `uvicorn app.main:app`: the bare command
binds `127.0.0.1` (localhost only), so the companion isn't reachable on your LAN and the
URL it registers with the gateway won't work. `python -m app` binds `0.0.0.0` and
honours `COMPANION_HOST` / `COMPANION_PORT`.

## Canonical sources

The repo is the source of truth; this page summarises it.

| | |
|---|---|
| [README](https://github.com/avandeputte/SplitFlapGatewayCompanion/blob/main/README.md) | Quick start, configuration, settings storage, everything else |
| [.env.example](https://github.com/avandeputte/SplitFlapGatewayCompanion/blob/main/.env.example) | The annotated environment-variable reference |
| [docker-compose.yml](https://github.com/avandeputte/SplitFlapGatewayCompanion/blob/main/docker-compose.yml) | The compose setup the install script writes for you |

---
**Next:** [Companion →](Companion.md) · [Multiple Displays →](Multiple-Displays.md) · [Vestaboard API →](Vestaboard-API.md) · [MCP Server →](MCP-Server.md)

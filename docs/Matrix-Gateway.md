# Matrix Gateway

*A split-flap display with no split flaps.*

This is the **[SplitFlap Gateway](SplitFlap-Gateway.md) firmware ported to the Waveshare
ESP32-S3-RGB-Matrix driver board** driving a **HUB75 RGB LED matrix**. The RS-485 transceiver
is gone; in its place is a software bus and a wall of **virtual** split-flap modules, each one
emulating a real module's wire protocol byte-for-byte and rendering itself as a flapping
character cell on the panel.

> **Repo:** [github.com/avandeputte/MatrixPortalGateway](https://github.com/avandeputte/MatrixPortalGateway). The firmware runs on the Waveshare ESP32-S3-RGB-Matrix driver board and speaks the gateway REST API natively (ESP-IDF `esp_http_server`), plus `GET /api/events` — a **Server-Sent Events stream** that pushes display state and status the instant the wall changes (the `events` capability token; the dashboard's live preview and status pane ride it, no pollers). OTA and file uploads take the **raw file as the request body** (no multipart): `curl --data-binary @file`. Panel efficiency comes standard: **delta frames** (`PUT /api/canvas/rects`), a **named sprite-atlas library** (`PUT /api/canvas/atlas/<name>`, optionally persisted), and a **persistent draw channel** (`PUT /api/canvas/stream` — TLV records over one connection, no per-frame round trip). The board plays sound (`POST /api/sound` — tones, chimes, and WAV files from the microSD card; Quiet Time silences it), reads the room (SHTC3 temperature/humidity on `GET /api/environment` and in the status JSON), listens (dual microphones drive the `spectrum`/`soundwall`/`ripple`/`scope`/`spectro` effects and the `"audio":true` option on fire/matrix/plasma — all on-device, nothing recorded), and mounts a **microSD card** (`/api/sd/*`, the dashboard Files tab, photo slideshows and movie streaming). Ops throughput over HTTP sustains ~40 fps; ops/ticker text is full UTF-8 → CP1252; gradients have radial/angled modes with ordered dithering. This gateway has **no MQTT and no Home Assistant surface**: the companion is pure REST and the dashboard is SSE-pushed. (The physical SplitFlap Gateway keeps its full MQTT/HA surface.)
Everything above the bus is the unmodified gateway: the same web UI, REST API and OTA
(this gateway has no MQTT/Home Assistant surface — see the note above). The [Companion](Companion.md) drives the split-flap wall **without
any changes** — and, because it asks the gateway what it is, also unlocks the extras a drawn
wall adds: mixed-case text, pictographs, named colours, and the [canvas](Canvas.md) it can draw on.

## Why use it

- **Try the whole stack with no mechanical build** — web UI, companion, the lot, on one
  driver board plus a panel. No modules, no RS-485, no steppers, no calibration.
- **An LED-matrix display in its own right** — full colour, real accented characters,
  lowercase, the colour flaps, and an animated flip effect with a physical-looking seam.
- **A faithful test target** — because it emulates at the protocol level, it exercises the
  same code paths a real gateway does.

## What you need

| Part | Notes |
|---|---|
| **Waveshare ESP32-S3-RGB-Matrix driver board** | The controller — an ESP32-S3 with **32 MB octal flash** and **16 MB octal PSRAM**, USB-C, and a battery-backed **PCF85063 RTC** (SH1.0 cell socket). It plugs straight onto the panel's HUB75 header. |
| A **HUB75 LED panel** | Default layout is a **15 × 3** wall on a **128 × 32** chain (two 64×32 panels in series, or one native 128×32). Bigger panels give roomier cells. |
| A **5 V power supply** | Sized for your panel — check the panel specs. |

64-row panels (128×64) use the HUB75 **E** address line, which this board wires directly on
its HUB75 header — so a 64-row panel just works, with no jumpers or board changes. See the
repo's README for the panel/size table.

Panel wiring varies one other way: some panels are **BGR** rather than RGB. Nothing can
detect that — it shows up as every colour being wrong in a telltale pattern (red draws
blue, yellow draws cyan, while green and white look fine). That's a **setting, not a
hardware fix**: Settings → LED Panel → **BGR**.

On a **large** panel (say 256×64) the framebuffer can outgrow the ESP32-S3's internal SRAM at a
high bit depth. Rather than refuse and run headless, the driver **auto-reduces the bit depth** to
the deepest that fits — 256×64 lands on 3 bitplanes — and reports the real value as `panel.depth`
in `GET /api/status`. See [Canvas API → Panel bit depth](Canvas.md#panel-bit-depth-and-the-panel-object).

### Framebuffer in PSRAM — depth 4 on 256×64 *(experimental)*

Settings → LED Panel → **Framebuffer in PSRAM** (off by default) moves the framebuffer out of
internal SRAM into the board's octal PSRAM (80 MHz). That lifts the internal-RAM cap, so 256×64
runs **depth 4 (16 levels per channel)** instead of 3 — noticeably smoother gradients. The panel
also raises its pixel clock to 10 MHz so depth 4 refreshes at ~80 Hz (at 5 MHz it would be ~40 Hz
and flicker). **Reboot to apply**; turning it off and rebooting returns to the rock-solid depth-3
internal path. It reports `panel.fbPsram` and `panel.refreshHz` in `GET /api/status`, and as a
side effect frees ~90 KB of internal RAM. Worth trying on this Waveshare board specifically — its
octal PSRAM has ~16× the bandwidth the pixel clock needs, and its radio tolerates 10 MHz.

## Flash & set up

```bash
pio run -t upload        # build + flash over USB-C
pio device monitor       # 115200 baud, native USB CDC
```

Later updates can also go over the air, from the web updater at **`/ota`**. There is no UF2
bootloader on this board — no drag-and-drop flashing, no double-tap reset. If the board ever
won't program, hold **BOOT** while plugging in (or while tapping RESET) and flash with
esptool / `pio run -t upload`.

WiFi works like the real [SplitFlap Gateway](SplitFlap-Gateway.md#2-join-it-to-wifi) — with one difference: its
**hostname is configurable**, and the fallback AP is *named after it*.

1. On first boot it raises an access point called **`splitflap-gw-<6 hex digits>`** (derived
   from the board's MAC — e.g. `splitflap-gw-a3f19c`), password **`12345678`**.
2. Join it, open **http://192.168.4.1**, and save your SSID + password in **Settings → WiFi**.
3. It joins your LAN and the AP shuts off. Reach it at **http://<that-hostname>.local** —
   and you can change the hostname to something friendlier in Settings.

The same **mDNS caveats apply**: if `.local` doesn't resolve on your network, find the board's
IP in your router's DHCP client list (look for the hostname above) and use that instead —
see [Finding it on your network](SplitFlap-Gateway.md#finding-it-on-your-network). From there it's the
same web UI as the gateway — same tabs, same settings.

One nicety a physical gateway doesn't have: the board's **battery-backed RTC** (fit a cell in
its SH1.0 socket) means the clock is valid seconds after power-on, before any network is up —
NTP then disciplines it on every sync. Without a cell, the gateway simply waits for NTP as
before.

## What's emulated (and what isn't)

- **Emulated:** the display commands the gateway sends — show a **character** (`-`), show a
  **flap by index** (`+`) and **home** (`h`), addressed by module id or broadcast. That is the
  whole contract now: frames flow **one way**, the modules act on them, and **nothing replies.**
  (Earlier firmware also modelled the bus's `v`/`A` identity and batch *queries* and fabricated a
  stable serial number per module. With no physical bus to interrogate — every answer was a
  compile-time constant — that machinery was removed: a drawn module is just an id and its current
  flap, and `GET /api/flap/modules` rows are simply `{id, flapIndex, flapChar}`.)
- **The reel is bigger:** nothing is drawn from a physical reel, so nothing is rationed. A
  virtual module carries **237 flaps** where a real one carries 64:

  | flaps | what they are |
  |---|---|
  | 0–155 | every Windows-1252 glyph — letters, digits, punctuation, accents |
  | 156–162 | the seven colour flaps — red, orange, yellow, green, blue, violet, white |
  | 163–222 | the 60 **lowercase** letters, accents included |
  | 223–236 | 14 **pictographs** — ♥ ♦ ♣ ♠ ☀ ☺ ♪ ● ■ ⌂ and the four arrows |

- **Not emulated:** the mechanism. There's no stepper, Hall sensor or EEPROM, so calibration,
  diagnostics and provisioning are no-ops (the modules are "born" provisioned). You won't use
  the Calibration or Provision tabs here.
- **The flip is a rendering effect**, not a physics simulation — you can cap or disable it.

## Reaching the extra flaps

The last two rows of that table are the interesting ones, and they need a word of explanation,
because for a long time they were **on the reel but unreachable**.

The gateway's original display protocol carries **one byte per character**, and it has a
collision it can never fix: *the byte for lowercase `r` already means RED*. That is why
`m38-r` sets the red flap, and it is why, on that path, lowercase has to fold to uppercase and
a heart — which has no Windows-1252 byte at all — cannot be addressed by character in **any**
way. This is not a bug to be tidied up; it is the price of a protocol that spends seven of its
letters on colours.

The firmware answers it with a second, **index-addressed** endpoint:

```
POST /api/display/cells
{ "start": 0, "step_ms": 15,
  "cells": [ {"ch": "H"}, {"ch": "i"}, {"color": "red"}, {"skip": true} ] }
```

A cell names a **character**, a **colour by name**, a **blank**, or `skip` (leave that module
alone). Because a colour is now a *name* rather than a borrowed letter, `i` can simply be the
letter `i` — and flap 223 can be a heart.

The plain character protocol works byte for byte, and a physical wall is unaffected.

**You do not have to do any of this yourself.** The [Companion](Companion.md) asks the gateway
what it is (`GET /api/config`), and if it finds a Matrix Gateway it
uses the index API automatically — so apps render in mixed case, colours stay colours, and
pictographs appear. Point it at a physical wall and it falls back to the character protocol
and folds everything to capitals. Same app, same companion, whichever wall you own.

## The panel as a raw canvas

Everything above treats the panel as a **wall of flaps**. But it is also, physically, a grid
of RGB LEDs — and the Matrix Gateway can hand that grid over as a plain **framebuffer**,
bypassing the split-flap emulation entirely, so you can draw *anything* on it. A real
split-flap gateway has no framebuffer at all, so this is the one place a Matrix wall does
something the hardware it emulates simply cannot.

There is a lot here — full frames (`rgb888`, `rgb565` or compressed **QOI**), **partial-rectangle**
updates, an on-device **animation** loop that plays from PSRAM after the client disconnects, a
scrolling **ticker**, JSON **draw ops**, twelve on-device **effects** (`plasma`, `fire`, `matrix`, `fliporama`, `clock`, `life`, `spectrum`, `soundwall`, `maze`, `ripple`, `scope`, `spectro`), each declaring its own parameters (`effectDefs`), and a framebuffer **readback** you
can poll for a live preview. A client discovers the whole surface from `GET /api/capabilities` — the
`canvas`, `effects` and `effectDefs` keys, which a physical gateway never carries.

On-device effects and animations run on the panel **itself** with nothing on the network — pushing
frames over HTTP sustains ~40 fps, while a panel effect is
limited only by the display. While a
canvas is active the reel renderer **stands down**; a split-flap command or Quiet Time reclaims the
panel, and nothing canvas is persisted, so a reboot returns to the flaps.

**→ Full reference: the [Canvas API](Canvas.md) page.** You rarely drive any of this by hand — the
[Companion](Companion.md) exposes it through **canvas apps**: Effects, Image, Animation, Ticker, Lumina
Clock, Photo Frame, Stock Graph, Scoreboard and
Aquarium — plus **dual-surface** views of nearly every app: each draws a rich view on the panel
*and* runs on flaps, with channel/quiz apps rendering as text + a themed icon — and any you
[write yourself](Writing-Matrix-Apps.md).

## Timer, alarms & gestures *(3.14–3.15)*

The board doubles as a kitchen appliance. `POST /api/timer {"minutes":5}` puts a
full-screen anti-aliased countdown on the panel that outranks everything — canvas,
effects, the companion — until it's answered; four persisted alarm slots
(`/api/alarms`) do the same on a schedule, and an alarm's chime deliberately
overrides Quiet Time. Both are advertised (`timer`, `alarms`) and the dashboard has
a card for them.

To answer one without walking to a browser: **double-clap at the panel, or
double-tap the board** (knuckle-tap the frame). Clap detection runs in the
microphone DSP — a transient over the room's noise floor plus a *not-bass* spectral
gate, calibrated against real hands (on these mics a clap is mid-spread, not
bright; a music thump is bass-heavy, which is exactly what the gate rejects). Tap
detection uses the IMU's on-die tap engine. Both are off by default
(`clapEnabled` / `tapEnabled`), advertised as `claps` / `taps`, and every detection
streams to the companion as an SSE `clap`/`tap` event — singles are yours to bind
to anything; doubles dismiss a live timer or alarm on-device and are logged to the
card's event log. A single stray clap does nothing by design. Every registered gesture that isn't consumed by a dismissal flashes a small acknowledgment square in the panel's top-right corner (~220 ms, cyan = clap, amber = tap) — the board's way of saying *heard you*.

## How it fits the rest of the wiki

The Matrix Gateway is a **drop-in replacement** for the modules **and** the gateway.
Wherever the rest of this guide says "the gateway," it applies here too — including
registering the [Companion](Companion.md). (Exception: the [Home Assistant](Home-Assistant.md)
page is physical-gateway-only the Matrix Gateway has no MQTT/HA support.)
Skip the [Hardware](Hardware.md) and [Module Firmware](Module-Firmware.md) pages entirely.

---
**Next:** [Companion →](Companion.md)

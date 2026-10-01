# LCD Gateway

*A split-flap display with no split flaps.*

This is the **[SplitFlap Gateway](SplitFlap-Gateway.md) firmware ported to the Waveshare
ESP32-P4-WIFI6-POE-ETH board**, driving a **10.1" MIPI-DSI touch LCD** (JD9365, 1280×800).
It is the newest member of the family and shares the [Matrix Gateway](Matrix-Gateway.md)'s trick:
the RS-485 wire is gone, and in its place is a wall of **virtual** split-flap modules, each one
receiving the same protocol frames a real module would and rendering itself as a flapping
character **card** on the LCD.

> **Repo:** [github.com/avandeputte/SplitFlapGatewayLCD](https://github.com/avandeputte/SplitFlapGatewayLCD). The firmware runs on the Waveshare ESP32-P4-WIFI6-POE-ETH board and speaks the gateway REST API natively (ESP-IDF `esp_http_server`), plus `GET /api/events` — a **Server-Sent Events stream** that pushes display state and status the instant the wall changes. OTA and file uploads take the **raw file as the request body**: `curl --data-binary @firmware.bin http://<board>/api/ota/upload`. Panel efficiency comes standard: **delta frames** (`PUT /api/canvas/rects`), a **named sprite-atlas library** (`PUT /api/canvas/atlas/<name>`, optionally persisted), and a **persistent draw channel** (`PUT /api/canvas/stream` — records over one connection, no per-frame round trip). The board plays sound and listens (the **ES8311** codec's microphone drives the `spectrum`/`scope`/`spectro`/`soundwall` effects and the `"audio":true` option on fire/matrix/plasma — all on-device, nothing recorded), mounts a **microSD card** (`/api/sd/*`, the dashboard Files tab), and reads a **capacitive touchscreen**. Ops text is full UTF-8 → CP1252, and the canvas adds **scalable anti-aliased text**. Like the Matrix Gateway it has **no MQTT and no Home Assistant surface** — the companion is pure REST and the dashboard is SSE-pushed. The REST contract is `openapi.yaml`, served live at `GET /openapi.yaml`.

Where the Matrix Gateway lights up an external LED panel, the LCD Gateway drives a single
**integrated 10.1" IPS touchscreen** — and the board it runs on brings three things the S3
boards don't: a **capacitive touchscreen**, **Ethernet with PoE** (one cable powers *and*
networks it), and **WiFi 6** (remoted through an onboard ESP32-C6). Two things it drops:
there is **no battery-backed RTC** (the clock comes from NTP) and **no IMU** — the touchscreen
replaces tap gestures.

Everything above the protocol seam is the unmodified gateway — the same web UI, REST API, OTA
and command log — so the [Companion](Companion.md) drives it **without any changes** and cannot
tell the difference, while still unlocking the extras a drawn wall adds: mixed-case text,
pictographs, named colours, and the [canvas](Canvas.md) it can draw on.

## Why use it

- **A big, bright display with no mechanical build** — 1280×800 of IPS panel, and the whole
  stack (web UI, companion, canvas, effects) on one board. No modules, no RS-485, no steppers,
  no calibration.
- **One cable does everything** — Power-over-Ethernet carries power *and* network to a
  wall-mounted panel over a single run: no barrel jack, no WiFi setup.
- **A pixel surface in its own right** — full colour, real accented characters, lowercase, the
  colour flaps, and an animated flip with a physical-looking seam, plus on-device effects,
  animations and a scalable-text ticker on a proper HD panel.
- **A faithful test target** — like the Matrix Gateway it emulates at the protocol level, so it
  exercises the same code paths a real gateway does.

## What you need

| Part | Notes |
|---|---|
| **Waveshare ESP32-P4-WIFI6-POE-ETH board** | The controller — an **ESP32-P4** (dual RISC-V) with PSRAM for the framebuffer, **WiFi 6** via an onboard **ESP32-C6**, **Ethernet with PoE**, USB-C, a microSD (TF) slot, and an **ES8311** audio codec. |
| **A 10.1" MIPI-DSI touch LCD** | The Waveshare **JD9365** panel — **1280×800** IPS with **GT911** capacitive touch — on the board's MIPI-DSI FPC connector. |
| **Power** | **PoE** (an 802.3af switch or injector) *or* **USB-C**. |

No external LED panel, no HUB75 chain, no separate 5 V panel supply — the display *is* the panel.

## Flash & set up

```bash
pio run -t upload        # build + flash over USB-C
pio device monitor       # 115200 baud, native USB CDC
```

Later updates go over the air from the web updater at **`/ota`** (or
`curl --data-binary @firmware.bin http://<board>/api/ota/upload`). There is no UF2 bootloader —
if the board ever won't program, hold **BOOT** while plugging in USB and flash again.

**Networking is Ethernet-first.** Plug it into your LAN or a PoE switch and it comes up on DHCP
with **zero configuration** — no setup page, no access point. Reach it at
**http://\<hostname\>.local**, or by the IP in your router's DHCP client list. While Ethernet is
connected the WiFi radio stays **off** by design.

For a **WiFi-only** install it behaves like the other gateways: on first boot with no network it
raises a setup access point; join it, save your SSID and password, and it joins your LAN. See
[the SplitFlap Gateway's WiFi steps](SplitFlap-Gateway.md#2-join-it-to-wifi). The same **mDNS
caveats** apply — if `.local` doesn't resolve, use the board's IP.

Unlike the Matrix board there is **no RTC chip**, so the clock is invalid from power-on until the
first NTP sync. Every caller already handles that state, and frame timestamps show uptime until
time is real.

## What's emulated — and the reel

This is the same emulation model as the
[Matrix Gateway](Matrix-Gateway.md#whats-emulated-and-what-isnt), byte for byte:

- **Emulated:** the display commands the gateway sends — show a **character** (`-`), a **flap by
  index** (`+`) and **home** (`h`), addressed to one module or broadcast. Frames flow one way and
  **nothing replies**; the command log (`GET /api/log`) records the outbound traffic.
- **Not emulated:** the mechanism. There is no stepper, Hall sensor or EEPROM, so calibration,
  diagnostics and provisioning are no-ops — the modules are "born" provisioned. You won't use the
  Calibration or Provision tabs.
- **The reel is the full 237 flaps** — every Windows-1252 glyph, the seven colour flaps, the 60
  lowercase letters and 14 pictographs. Mixed case, named colours and pictographs are reachable
  through the index-addressed `POST /api/display/cells`, while the legacy one-byte protocol
  (`m5-r` sets **red**, `hello` renders `HELLO`) is **untouched**. The Matrix Gateway page
  explains [the two ways in](Matrix-Gateway.md#reaching-the-extra-flaps) in full; it applies here
  unchanged.

The default wall is **15 × 5** (75 modules); any grid from **10 × 1 up to 32 × 10**
(`VM_MAX_MODULES` = 320) works, chosen in **Settings → Module Wall** and applied on reboot. A
flap **card keeps its proportion** whatever the grid, and a wall that does not fill the panel is
**centred** on both axes — short walls letterbox or pillarbox.

### If every colour is wrong

Same story as the LED panel: if red and blue are swapped, the panel is wired **BGR** rather than
RGB. Tick **Settings → LCD Panel → "Panel is wired BGR"** — it takes effect on the next frame, no
reboot.

## The panel as a raw canvas

Because the wall is really a **1280×800 framebuffer**, the gateway can hand it over directly —
bypassing the split-flap emulation so you can draw *anything*. A real split-flap gateway has no
framebuffer at all, so this is the one place a drawn wall does something the hardware it emulates
simply cannot.

- Full frames (`rgb888`, `rgb565` or compressed **QOI**), **partial-rectangle** deltas
  (`PUT /api/canvas/rects`), and a **persistent stream channel** (`PUT /api/canvas/stream`) for
  animation-rate updates with no per-frame HTTP round trip.
- An on-device **animation** library (with GIF import) that plays from PSRAM after the client
  disconnects, a scrolling **ticker** — exclusive, or overlaid as a lower-third band, with an
  optional auto-dismiss timer — **scalable anti-aliased text**, and a named **sprite-atlas
  library** (up to 16 sheets, optionally persisted to flash).
- On-device **effects** — plasma, fire, matrix rain, flip-o-rama, a clock, Game of Life, an
  oscilloscope and a spectrogram — each declaring its own typed parameters through `effectDefs`.
- **Audio-reactive** modes driven by the board's onboard microphone (the ES8311 codec): a
  `spectrum` analyzer, `scope`, `spectro`, a `soundwall` where the flap wall itself flips on the
  beat, and an `"audio":true` option on fire/matrix/plasma. Sound is reduced to a handful of
  numbers on-device; nothing is recorded.

Rendering runs at **60 Hz**: the logical landscape frame is a linear RGB565 framebuffer in PSRAM,
and `panelShow()` rotates it 90° into the DSI scanout in hardware with the P4's **PPA** (Pixel
Processing Accelerator). Pixel effects render at a reduced 256×160 surface the PPA upscales; the
clock and the wall render native. A client discovers the whole surface from
`GET /api/capabilities` — the `canvas`, `effects` and `effectDefs` keys a physical gateway never
carries. While a canvas is active the reel renderer **stands down**; a split-flap command or Quiet
Time reclaims the panel, and nothing canvas is persisted, so a reboot returns to the flaps.

**→ Full reference: the [Canvas API](Canvas.md) page.** You rarely drive any of this by hand — the
[Companion](Companion.md) exposes it through **canvas apps** (Effects, Image, Animation, Ticker,
Lumina Clock, Photo Frame, Stock Graph, Scoreboard, Aquarium…), and any you
[write yourself](Writing-Matrix-Apps.md).

## Timer, alarms & touch

Like the Matrix Gateway, the board doubles as a kitchen appliance. `POST /api/timer
{"minutes":5}` puts a full-screen anti-aliased countdown on the panel that outranks everything —
canvas, effects, the companion — until it is answered; four persisted alarm slots (`/api/alarms`)
do the same on a schedule, and an alarm's chime deliberately overrides Quiet Time. Both are
advertised (`timer`, `alarms`) and the dashboard has a card for them.

To answer one without reaching for a browser, **double-tap the touchscreen**. The LCD board has no
IMU, so where the Matrix Gateway offers clap and knuckle-tap gestures, this one uses its
**capacitive touch panel** (GT911): a double-tap dismisses a live timer or alarm on-device.

## How it fits the rest of the wiki

The LCD Gateway is a **drop-in replacement** for the modules **and** the gateway, exactly like the
Matrix Gateway. Wherever the rest of this guide says "the gateway," it applies here too — including
registering the [Companion](Companion.md). (Exception: the [Home Assistant](Home-Assistant.md) page is
physical-gateway-only — this gateway has no MQTT/HA surface.) Skip the [Hardware](Hardware.md) and
[Module Firmware](Module-Firmware.md) pages entirely.

---
**Next:** [Companion →](Companion.md)

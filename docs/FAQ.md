# FAQ & Glossary

## Glossary

| Term | What it means |
|---|---|
| **Module** | One split-flap character cell — an ATtiny1616 board with a reel, stepper and Hall sensor. |
| **Reel / flaps** | The printed flaps on a module. A default reel has 64 flaps, including 7 colour flaps. The count and characters are [configurable](Flaps-and-Character-Sets.md). |
| **Bus / RS-485** | The shared serial pair all modules sit on, carried by the DIN conductor rail (with 12 V and ground) that modules contact via pogo pins. 9600 baud. |
| **Gateway** | The ESP32 that bridges your network to the bus and serves the web UI. |
| **Provisioning** | Assigning a bus ID to a freshly-flashed module (which starts with none). |
| **Calibration** | Teaching a module where home is and how far a full reel turn is. |
| **Companion** | The content app — apps, playlists, schedules, triggers, compose. |
| **App / plugin** | One content source (weather, clock, …), in the splitflap-os plugin format. |
| **Channel vs functional app** | Channel = static content (`data.json`); functional = live data (`app.py` with `fetch()`). A **quiz** is a channel whose entries are `[question, answer]` pairs shown as a two-screen reveal. |
| **Matrix Gateway** | The gateway on an LED matrix with virtual flaps — no mechanical build. |

## Frequently asked

**Do I have to build the mechanical display?**
No. The **[Matrix Gateway](Matrix-Gateway.md)** renders virtual flaps on an LED
matrix and behaves exactly like a real gateway. It's the fastest way to try everything.

**Do I need the Companion?**
No — the [SplitFlap Gateway](SplitFlap-Gateway.md) can show text on its own from its web UI. The companion is what
adds apps, playlists, schedules and the Home Assistant surfaces.

**Do I need Home Assistant?**
No. It's one of several optional ways to drive the companion. See
[Home Assistant](Home-Assistant.md).

**How do I get the gateway onto my WiFi in the first place?**
It raises its own access point when it has no network: join **`Split-Flap-GW`** (password
**`12345678`**), open **http://192.168.4.1**, and save your SSID/password in Settings → WiFi.
It then joins your LAN and the AP disappears. →
[Gateway → Join it to WiFi](SplitFlap-Gateway.md#2-join-it-to-wifi)

**The gateway's `.local` address doesn't load.**
mDNS is best-effort — it commonly fails across VLANs or guest/IoT SSIDs, on routers that block
multicast, on Windows, and from VMs and containers. **Use the IP instead:** find it in your
router's DHCP/attached-devices list (the host is named `splitflap-gw-xxxxxx`), or read it off the
gateway's Status tab / USB serial console. Give it a DHCP reservation and use
`http://<that-ip>` everywhere — including `GATEWAY_URL`. →
[Finding it on your network](SplitFlap-Gateway.md#finding-it-on-your-network)

**How do I install the companion in Home Assistant?**
Two separate things, either or both: the **App** (the full UI in your sidebar) — add
`https://github.com/avandeputte/SplitFlapGatewayCompanion` under Settings → Apps → App Store →
⋮ → Repositories; and the **HACS integration** (entities for automations) — add the same URL
as a *custom repository of type Integration* in HACS, then restart and add the integration,
pointing it at the **companion's** URL. Full steps:
[Home Assistant](Home-Assistant.md#1-the-app-add-on).

**Can I print my own flaps — with accents, or fewer of them?**
Yes, with the Universal Firmware (v31+): both the flap count and the character set are
configurable per module. → [Flaps & character sets](Flaps-and-Character-Sets.md)

**Where do I set the grid size?**
On the **gateway**, in Settings → Display Layout. The companion reads it from there — set it
once.

**Why won't my new module respond to commands?**
A freshly-flashed module has **no ID** until you [provision](Module-Firmware.md#2-provisioning)
it — it advertises its serial number instead. Assign it an ID from the gateway's Provision
tab.

**My module's calibration/ID disappeared after I re-flashed it.**
You skipped the fuse step. Run `pio run -t fuses` **once per chip** — it sets the `EESAVE`
fuse so EEPROM survives reflashes. Without it, every upload wipes the module.

**The companion won't start.**
It needs **`GATEWAY_URL`** set to your gateway's address — it refuses to start without one. As
a Home Assistant app, that's the `gateway_url` option.

**Can I use my existing Vestaboard automations?**
Yes — turn on the companion's [Vestaboard-compatible API](Vestaboard-API.md) and point them at
the companion. It speaks the real Vestaboard Local API, so `ha-vestaboard` and friends work
unchanged.

**Can Claude / an LLM drive the display?**
Yes — turn on the companion's [MCP server](MCP-Server.md). It exposes twelve tools (read the
board, show a message with a timed revert, run apps and playlists, change app settings), so a
model can look at the wall before it writes to it.

**Where do settings and uploaded apps live?**
In the companion's data volume (`/data`). It can also mirror settings to the gateway so a
fresh container inherits them.

## The repositories

| Repo | What |
|---|---|
| [adamgmakes/SplitFlapDisplay](https://github.com/adamgmakes/SplitFlapDisplay) | The hardware (Adam G Makes) |
| [SplitFlapUniversalFirmware](https://github.com/avandeputte/SplitFlapUniversalFirmware) | Module firmware |
| [SplitFlapGateway](https://github.com/avandeputte/SplitFlapGateway) | The ESP32 gateway |
| [MatrixPortalGateway](https://github.com/avandeputte/MatrixPortalGateway) | The LED-matrix gateway |
| [SplitFlapGatewayCompanion](https://github.com/avandeputte/SplitFlapGatewayCompanion) | The content app (+ HA add-on & HACS integration) |
| [csader/splitflap-os](https://github.com/csader/splitflap-os) | An alternative content engine; apps written for it run on the companion |

---
[← Home](index.md)

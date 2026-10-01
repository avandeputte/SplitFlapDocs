# SplitFlap — the complete guide

Build a mechanical **split-flap display** — the kind you hear clacking in old train
stations and airports — and drive it with rich, live content: clocks, weather, stocks,
transit, sports, quotes, animations, or a message you type. This guide is the single place
that ties the whole project together, from a bare circuit board to a message on the wall,
and into Home Assistant.

![The SplitFlap ecosystem](ecosystem.png)

## The pieces, and how they fit

The project is a small stack. Each layer does one job and hands off to the next; you only
build the layers you need.

| Layer | What it is | Required? |
|---|---|---|
| **[Hardware](Hardware.md)** | The physical split-flap modules — Adam G Makes' design (ATtiny1616, stepper, Hall sensor, RS-485). | Required (unless you use the Matrix Gateway below) |
| **[Module firmware](Module-Firmware.md)** | The Universal Firmware each module runs. Flash once; identity is assigned later. | Required for real modules |
| **[Flaps & character sets](Flaps-and-Character-Sets.md)** | What's printed on your reels — the flap count and character set are configurable per module. | Optional (defaults work) |
| **[SplitFlap Gateway](SplitFlap-Gateway.md)** | An ESP32 that bridges your network to the module bus, with a web UI to provision, calibrate and drive the wall. | Required |
| **[Companion](Companion.md)** | The content app: apps, playlists, schedules, triggers, compose, a live view. | Optional but recommended |
| **[Home Assistant](Home-Assistant.md)** | The sidebar app, the HACS integration, the MQTT device. | Optional |
| **[Vestaboard API](Vestaboard-API.md)** · **[MCP Server](MCP-Server.md)** | Companion features, no HA required: answer the Vestaboard Local API, and expose the board as MCP tools an LLM can drive. | Optional |

Two branches keep the whole thing flexible:

- **No mechanical build?** Two boards run the same gateway with *virtual* flaps — the
  **[Matrix Gateway](Matrix-Gateway.md)** on an LED matrix, and the **[LCD Gateway](LCD-Gateway.md)**
  on an integrated 10.1" touchscreen (Ethernet/PoE). Either one replaces the modules **and** the
  gateway; the companion can't tell the difference. Great for trying the full stack, or as a
  display in its own right.
- **Don't want the companion?** You can drive the gateway with
  **[csader's splitflap-os](Using-splitflap-os.md)** instead — a separate content engine
  whose apps also run on the companion. Every viable mix is compared in
  **[Choosing a Configuration](Choosing-a-Configuration.md)**.

## Start here

**[→ Quick Start: from parts to a message on the wall](Quick-Start.md)** — the recommended
end-to-end path, with every optional step clearly marked.

## All pages

1. **[Quick Start](Quick-Start.md)** — the whole flow, start to finish
2. **[Choosing a Configuration](Choosing-a-Configuration.md)** — every viable mix of firmware × driver, with a feature grid
3. **[Hardware](Hardware.md)** — Adam G Makes' split-flap modules; what to build or buy
4. **[Module Firmware](Module-Firmware.md)** — flash, provision, calibrate a module
5. **[Building a UPDI Flasher](UPDI-Flasher.md)** — a CH340 adapter and one diode is the whole programmer
6. **[Flashing Modules](Flashing-Modules.md)** — fuses once, firmware once: with a prebuilt release, or from source
7. **[Provisioning](Provisioning.md)** — assigning module identities, in the gateway or bare-metal
8. **[Calibration](Calibration.md)** — total steps, home offset and the per-flap map, step by step
9. **[Module Diagnostics](Module-Diagnostics.md)** — the built-in self-tests: power, Hall sensor, motor — and how to read them
10. **[Flaps & Character Sets](Flaps-and-Character-Sets.md)** — flap count, custom reels, localization
11. **[SplitFlap Gateway](SplitFlap-Gateway.md)** — flash the ESP32, join WiFi, tour the web UI
12. **[Gateway Case](Gateway-Case.md)** — a printed case that clips the gateway onto the rail and takes power and the bus from pogo pins
13. **[Matrix Gateway](Matrix-Gateway.md)** — the no-hardware alternative (LED matrix)
14. **[LCD Gateway](LCD-Gateway.md)** — the no-hardware alternative (10.1" touchscreen, Ethernet/PoE)
15. **[Companion](Companion.md)** — the content app: install and use it
16. **[Built-in Apps](Built-in-Apps.md)** — every shipped app at a glance
17. **[Companion without Home Assistant](Companion-Standalone.md)** — Docker, the install script, the configuration reference
18. **[Multiple Displays](Multiple-Displays.md)** — drive several walls from one companion
19. **[Home Assistant](Home-Assistant.md)** — the app, the HACS integration, the MQTT device
20. **[Vestaboard-compatible API](Vestaboard-API.md)** — reuse anything written for a Vestaboard
21. **[MCP Server](MCP-Server.md)** — let Claude read and drive the board
22. **[Using splitflap-os](Using-splitflap-os.md)** — csader's engine as an alternative
23. **[Writing Apps](Writing-Apps.md)** — build an app of your own
24. **[Compatibility](Compatibility.md)** — the plugin ABI contract with splitflap-os
25. **[Bus Protocol](Bus-Protocol.md)** — the RS-485 wire-level reference
26. **[Gateway API](Gateway-API.md)** — the REST & MQTT reference, both gateways
27. **[Languages & Localization](Localization.md)** — every language surface, and how to add one
28. **[FAQ & Glossary](FAQ.md)** — terms, gotchas, where things live

**Release notes** live with the code: the
[companion changelog](https://github.com/avandeputte/SplitFlapGatewayCompanion/blob/main/addon/CHANGELOG.md),
the [gateway](https://github.com/avandeputte/SplitFlapGateway/blob/main/RELEASE_NOTES.md),
the [Matrix Gateway](https://github.com/avandeputte/MatrixPortalGateway/blob/main/RELEASE_NOTES.md),
the [LCD Gateway](https://github.com/avandeputte/SplitFlapGatewayLCD/blob/main/RELEASE_NOTES.md),
and the [module firmware](https://github.com/avandeputte/SplitFlapUniversalFirmware/blob/main/RELEASE_NOTES.md).

---

**Credits.** The split-flap module hardware and the original bus protocol are by
**[Adam G Makes](https://www.youtube.com/@AdamGMakes)**
([hardware repo](https://github.com/adamgmakes/SplitFlapDisplay)). The companion's app
library grew from **[csader/splitflap-os](https://github.com/csader/splitflap-os)**'s
plugin format, and apps written for that project still drop in. Everything
here is **CC BY-NC-SA 4.0** (non-commercial, share-alike, attribution).

# Using splitflap-os

The apps that make the display *interesting* — weather, clocks, stocks, transit, quotes,
animations — come from **[csader/splitflap-os](https://github.com/csader/splitflap-os)**, an
open-source split-flap "OS" and app library. This page explains the relationship and your
options.

## How the projects relate

- **splitflap-os** (by csader) is the original project: a controller plus a plugin library of
  apps, designed for its own setup.
- **The [Companion](Companion.md)** has **its own app library** — some apps originated in
  splitflap-os and have been enhanced since, many more were created here — running on a
  **behavior-identical plugin runtime**, so any splitflap-os app also runs unchanged
  against *this* project's [SplitFlap Gateway](SplitFlap-Gateway.md). A conformance test
  asserts the runtime honours the plugin contract.

In other words: the companion is a bridge that lets csader's apps drive Adam G Makes'
hardware through the ESP32 gateway. You get the splitflap-os app ecosystem without splitflap-os
needing to know anything about this gateway.

> The compatibility contract is documented in [Compatibility](Compatibility.md),
> and there's a full app-authoring guide in [Writing Apps](Writing-Apps.md).

## Your options

*(A side-by-side feature grid of every combination — firmwares × drivers — is in
[Choosing a Configuration](Choosing-a-Configuration.md).)*

**Use the companion (recommended).** Its own app library is larger than splitflap-os's
(and you can upload your own apps), plus playlists, schedules, triggers, compose, a live
view, localization and the Home Assistant surfaces. Nothing extra to set up — see [Companion](Companion.md).

**Run splitflap-os itself.** If you'd rather use csader's original project — for its own
tooling, or to develop apps against it — head to
[github.com/csader/splitflap-os](https://github.com/csader/splitflap-os). It runs on a
Raspberry Pi and drives the modules directly over USB-RS485, or **through the Gateway over
MQTT** — splitflap-os speaks MQTT natively, so pointing it at the gateway's broker is a
settings change, nothing more; it works with the original firmware and the Universal
Firmware alike. This guide
documents the gateway + companion path in depth; splitflap-os has its own docs.

**Write your own apps.** The runtimes share a plugin format — asymmetrically: an app
written for splitflap-os runs on the companion (that direction is the contract), while an
app written for the companion *may* run on splitflap-os, without the companion's injected
helpers and unoptimized — no guarantees. A plugin is a `manifest.json` plus:

- an **`app.py`** with a `fetch()` function (a *functional* app — live data), or
- a **`data.json`** (a *channel* app — static pages).

Upload a `.zip` from the companion's **App Library**, and it loads immediately. The full ABI —
`fetch()` arguments, settings fields, the injected `i18n` / `get_weather` / `get_location`
helpers, triggers and animations — is in [Writing Apps](Writing-Apps.md).

## Credit

The app library and plugin format are **csader's** work; see
[csader/splitflap-os](https://github.com/csader/splitflap-os) and this project's
[`ATTRIBUTION.md`](https://github.com/avandeputte/SplitFlapGatewayCompanion/blob/main/ATTRIBUTION.md).
Everything here is CC BY-NC-SA 4.0, a derivative of splitflap-os.

---
**Next:** [Quick Start →](Quick-Start.md)

# Module Firmware

Every split-flap module runs the **SplitFlap Universal Firmware** — one binary, flashed
once to each module. Identity, calibration and the flap set are stored in the chip's EEPROM
and assigned *after* flashing, so there is nothing to change per module before you upload.

> **Repo:** [github.com/avandeputte/SplitFlapUniversalFirmware](https://github.com/avandeputte/SplitFlapUniversalFirmware)
> · target: **ATtiny1616** · toolchain: **PlatformIO** · programmer: **SerialUPDI**

Three stages take a bare module to a working cell: **flash → provision → calibrate**.
Everything below rides the RS-485 wire protocol — every command, reply and result code is
specified in [Bus Protocol](Bus-Protocol.md).

---

## 1. Flash

Two things to get right, and the rest is two commands per module:

- **A flasher.** No dedicated programmer: a cheap **CH340 USB-to-serial adapter with one
  Schottky diode** soldered between its `TXD` and `RXD` pins is a complete SerialUPDI
  programmer, and it **powers the module over its `3V3` wire** while flashing, so a module
  can be flashed on the bench with nothing else connected. Build it in ten minutes:
  **[Building a UPDI Flasher](UPDI-Flasher.md)** — parts, photos, and why the diode's band
  must face `TXD`.
- **The fuses, once per chip, before the firmware.** They set the `EESAVE` fuse that keeps
  the module's ID, calibration and flap set through every later reflash, and (since v32)
  the brown-out detector that stops a sagging supply from corrupting EEPROM. Skip this and
  every upload wipes the module's identity.

Then either **flash the prebuilt `firmware.hex`** from the
[latest release](https://github.com/avandeputte/SplitFlapUniversalFirmware/releases/latest)
with the free `avrdude` tool — no VS Code, no compiler — or **build from source** with VS
Code + PlatformIO (`pio run -t fuses`, then `pio run -t upload`). Both routes, step by
step, with the fuse values and a troubleshooting table:
**[Flashing Modules](Flashing-Modules.md)**.

Every module gets the identical binary. Verify over the bus: `m<ID>v` returns the firmware
version, ID and serial.

> **Upgrading to v32?** Run the fuses step once more on every module — it enables the
> brown-out detector and does not erase EEPROM. See [Flashing Modules](Flashing-Modules.md#the-fuses-and-why-they-come-first).

---

## 2. Provisioning

*(The short version — the full process, gateway and bare-metal alike, is
[Module provisioning](Provisioning.md).)*

A freshly flashed module has **no ID** (it reports `255`) and doesn't answer numeric
commands. Instead it **advertises its serial number** on the bus every 10–15 seconds. You
assign it a bus ID from the **[Gateway's](SplitFlap-Gateway.md#the-web-ui-tab-by-tab) Provision tab**,
from **splitflap-os's own UI** (provisioning is built into the product) if that is what
drives your wall, or with the included `provision.py` terminal tool on any serial host —
all three do the same thing.

The flow, either way:

1. **Discover** — the tool/UI lists modules advertising their serials.
2. **Identify (optional)** — home one module by serial so its reel spins; you can see which
   physical tile it is.
3. **Assign** — give it a bus ID (0, 1, 2, …). The module writes the ID to EEPROM,
   acknowledges, and stops advertising.

Repeat for each cell, left to right, top to bottom, to match how you want the wall
addressed. To start over, **de-provision** a module (or all) and it returns to advertising.

> Because identity is assigned here — not compiled in — you flash the same binary to every
> module and never touch the IDE again after the first flash.

---

## 3. Calibration

*(The short version — the full walkthrough is [Module calibration](Calibration.md).)*

Calibration teaches each module where "home" is and how far a full reel turn is, so the
right flap lands dead center. Again this is easiest from the **[Gateway's Calibration
tab](SplitFlap-Gateway.md#the-web-ui-tab-by-tab)** (it has a guided wizard), but the underlying steps are:

- **Count steps per revolution** — the module measures a full turn automatically.
- **Set the home offset** — nudge so the blank flap sits centered at home.
- **(Optional) per-flap fine-tuning** — for any flap that lands slightly off, drive to it
  and lock a corrected position into the map.
- **(Optional) custom flap set** — if your reel isn't the default 64-flap set, tell the
  module its character string so text maps to the right flaps.

Once calibrated, the values live in EEPROM and survive reboots (and reflashes, thanks to
the `EESAVE` fuse).

---

## Diagnostics

The firmware has built-in self-tests, surfaced on the gateway's Modules tab (or over the
bus). Run them in order — each depends on the one before:

1. **Snapshot** — reset cause, boot count, supply voltage, EEPROM OK, current flap. No
   movement.
2. **Hall sensor test** — one revolution; reports OK / stuck / dead / noisy / inverted.
3. **Mechanical test** — several revolutions; reports OK / inconsistent / no motion.

→ **[Module diagnostics](Module-Diagnostics.md)** — running them from the gateway, reading
every result, and a symptom-to-cause guide.

## The flap set

The default 64-flap reel is:

```
 (blank) A–Z  0–9  ! @ # $ & ( ) - + = ; : % ' . , / ? *  r o y g b p w
```

The seven lowercase letters at the end are the **colour flaps** (red, orange, yellow,
green, blue, purple, white).

Both the **flap count** and the **character set** are configurable per module and stored in
EEPROM (v31+) — so you can print a reel with `É`, `Ö` or `Ñ` on it, or a shorter reel with
no punctuation, and text still lands on the right flap. This is one of the Universal
Firmware's biggest departures from the original, and it's what makes the companion's
translated apps show up as words rather than blanks.

→ **[Flaps & character sets](Flaps-and-Character-Sets.md)** — how to set it, the 64-flap
budget, and starter sets per locale.

---
**Next:** [Gateway →](SplitFlap-Gateway.md)

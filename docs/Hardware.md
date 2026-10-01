# Hardware

The physical display is a wall of **split-flap modules**, one per character cell. The
module design — the mechanics, the circuit board, and the original bus protocol — is by
**[Adam G Makes](https://www.youtube.com/@AdamGMakes)**, and the build is documented in
his repository:

> ### 👉 [github.com/adamgmakes/SplitFlapDisplay](https://github.com/adamgmakes/SplitFlapDisplay)
>
> The circuit board, the 3D-printed parts, the bill of materials and the assembly steps
> live there. Start with Adam's repo and his [YouTube channel](https://www.youtube.com/@AdamGMakes)
> to build or source the modules; this guide picks up once you have them.

This page is a quick orientation so the rest of the guide makes sense — it is **not** a
substitute for Adam's build docs.

## What one module is

Each character cell is a small, self-contained board carrying:

- an **ATtiny1616** microcontroller (3.3 V logic) that runs the [module firmware](Module-Firmware.md);
- a **28BYJ-48 stepper motor** turning the flap reel, through a **ULN2003 driver**, from a
  **separate 12 V motor supply** (the motor is *not* powered from the logic rail);
- a **Hall-effect sensor** that finds a magnet on the reel to establish the home position;
- a half-duplex **RS-485 transceiver**, with the driver-enable line on a GPIO;
- a **DIN-rail clip** and four **pogo pins** on the underside — the module's only
  electrical connection (see below).

The reel carries the printed flaps — letters, digits, punctuation and a set of solid
**colour flaps** (red, orange, yellow, green, blue, purple, white). A default reel has
**64 flaps**; index 0 is the blank/home flap.

## How modules connect

There is **no wiring between modules**. Each module **clips onto a DIN rail**, and four
**pogo pins** on its underside press against a conductor rail carrying the four shared
lines: **power (12 V), ground, and the two RS-485 bus signals (A/B)**. Mounting a module
*is* connecting it — snap it onto the rail and it's on the bus.

A single controller is the bus master. In this project that controller is the
**[SplitFlap Gateway](SplitFlap-Gateway.md)** (an ESP32); the bus runs at **9600 baud, 8N1**.

```
    [M0]    [M1]    [M2]    [M3]    [M4]   … up to 255 modules,
   ══╪╪══════╪╪══════╪╪══════╪╪══════╪╪══   each clipped onto the DIN rail;
   ────────────────────────────────────    4 pogo pins per module contact the
   conductor rail:  12V · GND · RS-485 A · RS-485 B  ──── to the Gateway (ESP32)
```

Every module runs the **same firmware binary** — there is nothing to change per module
before flashing. A module's identity (its **bus ID**, e.g. "module 0") is assigned later,
at runtime, by [provisioning](Module-Firmware.md#2-provisioning). That's the key difference from
Adam's original firmware, where each module's ID was compiled in; see the
[Module Firmware](Module-Firmware.md) page.

## What you need to drive them

| Part | Notes |
|---|---|
| Split-flap modules | However many cells you want — a 3 × 15 wall is 45. Built/sourced per [Adam's repo](https://github.com/adamgmakes/SplitFlapDisplay). |
| **DIN rail + conductor rail** | One per row. The modules clip on; the conductor rail distributes 12 V, GND and the two bus signals to their pogo pins. Per Adam's design. |
| A **12 V supply** | Sized for your module count (the steppers are the load). See Adam's BOM. |
| The **[SplitFlap Gateway](SplitFlap-Gateway.md)** board | A Waveshare **ESP32-S3-RS485-CAN** — it has the RS-485 transceiver on board. |
| A **SerialUPDI programmer** | A cheap CH340 USB-serial adapter with one Schottky diode soldered on — [build it yourself](UPDI-Flasher.md) in ten minutes. It powers the module while flashing, so modules can be flashed on the bench before they go on the rail. See [Flashing Modules](Flashing-Modules.md). |

## The no-hardware option

Don't want to build anything mechanical? The **[Matrix Gateway](Matrix-Gateway.md)**
renders *virtual* split-flap modules on an LED matrix — no modules, no RS-485, no steppers —
and behaves exactly like a real gateway to everything downstream. It's the fastest way to try
the whole stack.

---
**Next:** [Module Firmware →](Module-Firmware.md)

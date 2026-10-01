# Flashing modules

Every split-flap module runs the same [Universal Firmware](Module-Firmware.md) binary, flashed
once over **UPDI** with a [flasher you build from a USB-serial adapter](UPDI-Flasher.md). There
are two ways to get the firmware onto a chip, and they end in the same place:

| Route | You need | Best for |
|---|---|---|
| **[A. Flash a release](#route-a-flash-a-release-no-compiler)** | The flasher, `firmware.hex` from the latest release, and the free `avrdude` tool | Everyone who just wants the current firmware on their modules |
| **[B. Build from source](#route-b-build-from-source-platformio)** | The flasher, VS Code and the PlatformIO extension | Changing the firmware, or following the project's own toolchain |

Either way it is **two commands per module**: one writes the **fuses** (once per chip), one
writes the **firmware**. Both routes are the firmware project's own instructions —
[FLASHING.md](https://github.com/avandeputte/SplitFlapUniversalFirmware/blob/main/FLASHING.md)
and [SETUP.md](https://github.com/avandeputte/SplitFlapUniversalFirmware/blob/main/SETUP.md)
— condensed here and kept in step with them.

> **Nothing to change before flashing.** Identity (the bus ID), calibration and the flap
> set are stored in the chip's EEPROM and assigned *after* flashing, over the bus. See
> [Provisioning](Provisioning.md) and [Calibration](Calibration.md).

---

## Connect the module

Three wires from the flasher to the module's `UPDI Interface` header, which is labelled
`+3V3`, `G` and `UPDI`:

| Flasher pin | Module pin |
|---|---|
| `3V3` | `+3V3` |
| `GND` | `G` |
| `RXD` | `UPDI` |

**The flasher powers the module's controller** through the `3V3` wire while flashing, so
nothing else needs to be connected — no 12 V, no rail. Plug the flasher into a USB port and
find its serial port name:

| System | Command | Looks like |
|---|---|---|
| macOS | `ls /dev/cu.usbserial*` | `/dev/cu.usbserial-11430` |
| Linux | `ls /dev/ttyUSB*` | `/dev/ttyUSB0` (add yourself to the `dialout` group: `sudo usermod -aG dialout $USER`, then log out and in) |
| Windows | Device Manager → *Ports (COM & LPT)* | `USB-SERIAL CH340 (COM5)` → use `COM5` |

Use that name wherever the commands below say `PORT`.

---

## The fuses, and why they come first

Fuses are the chip's configuration: the clock, the brown-out detector, and — the one that
matters most — **`EESAVE`**, which keeps the EEPROM (the module's ID, calibration and flap
set) intact when the flash is erased. Writing the firmware erases the chip, and only this
fuse stops the erase from taking the EEPROM with it. So the fuses are written **once per
chip, before the firmware**. Running the step again on a chip that already has the right
fuses is harmless; skipping it means every reflash turns the module back into an
unprovisioned blank.

> **Firmware v32 changed a fuse.** The fuses now enable the **brown-out detector at 2.6 V**.
> Without it the ATtiny at 10 MHz keeps executing during the part of every power-up and
> power-down where it is below its rated voltage, and EEPROM can be misread or corrupted
> there — the cause of modules "forgetting" their settings after a power cycle. **If a
> module's fuses were written before v32, write them once more** (either route below).
> Writing fuses does not erase EEPROM; the module keeps its ID and calibration.

---

## Route A: flash a release (no compiler)

You need the flasher, **`firmware.hex`** from the *Assets* of the
[latest release](https://github.com/avandeputte/SplitFlapUniversalFirmware/releases/latest),
and **avrdude 7.0 or newer** (the `serialupdi` programmer was added in 7.0):

| System | Install |
|---|---|
| macOS | `brew install avrdude` ([Homebrew](https://brew.sh)) |
| Windows | Download the Windows zip from the [avrdude releases page](https://github.com/avrdudes/avrdude/releases), unzip it, and run `avrdude.exe` from that folder in a Command Prompt. Windows 10 and 11 normally install the CH340 driver by themselves; if no COM port appears, install the WCH `CH341SER` driver. |
| Linux | `sudo apt install avrdude` on Debian or Ubuntu 24.04 and newer. Older distributions ship avrdude 6.x, which lacks `serialupdi`; use the release build from the page above instead. |

Check the install: `avrdude -c '?'` lists the supported programmers, and `serialupdi`
should be among them.

### Step 1 — write the fuses (once per module)

macOS and Linux:

```
avrdude -c serialupdi -p attiny1616 -P PORT -b 57600 \
  -U fuse0:w:0x00:m \
  -U fuse1:w:0x54:m \
  -U fuse2:w:0x02:m \
  -U fuse4:w:0x00:m \
  -U fuse5:w:0xC5:m \
  -U fuse6:w:0x06:m \
  -U fuse7:w:0x00:m \
  -U fuse8:w:0x00:m \
  -U lock:w:0xC5:m
```

Windows, one line:

```
avrdude -c serialupdi -p attiny1616 -P COM5 -b 57600 -U fuse0:w:0x00:m -U fuse1:w:0x54:m -U fuse2:w:0x02:m -U fuse4:w:0x00:m -U fuse5:w:0xC5:m -U fuse6:w:0x06:m -U fuse7:w:0x00:m -U fuse8:w:0x00:m -U lock:w:0xC5:m
```

Each fuse ends with `1 byte written, 1 verified`. What they set:

| Fuse | Value | Meaning |
|---|---|---|
| `fuse0` WDTCFG | `0x00` | Watchdog off at reset; the firmware turns it on itself. |
| `fuse1` BODCFG | `0x54` | Brown-out detector on at 2.6 V. Protects EEPROM during power-up and power-down. |
| `fuse2` OSCCFG | `0x02` | 20 MHz internal oscillator, which the firmware runs at 10 MHz. |
| `fuse4` TCD0CFG | `0x00` | Default. |
| `fuse5` SYSCFG0 | `0xC5` | **EEPROM retained across flashes** (`EESAVE`), UPDI pin left as UPDI. |
| `fuse6` SYSCFG1 | `0x06` | Start-up delay. |
| `fuse7` APPEND | `0x00` | No application data section. |
| `fuse8` BOOTEND | `0x00` | No bootloader section. |
| `lock` | `0xC5` | Unlocked. |

These are the same values `platformio.ini` writes with `pio run -t fuses`. If a future
release changes a fuse, its release notes will say so.

### Step 2 — write the firmware

```
avrdude -c serialupdi -p attiny1616 -P PORT -b 57600 -U flash:w:firmware.hex:i
```

Run it from the folder where you saved `firmware.hex`, or give the full path to the file.
It takes about 25 seconds and ends with a line like `16244 bytes of flash verified` (the
exact number depends on the release). The module restarts on the new firmware immediately.

### Step 3, optional — confirm the settings survived

```
avrdude -c serialupdi -p attiny1616 -P PORT -b 57600 -U eeprom:r:-:h
```

This prints the module's EEPROM as hex. The first value should be `0x5d` (settings
present) and the sixth value is the module's bus ID (`0xff` means unprovisioned). If the
first value is `0xff` on a module that had settings, the fuses were not written before the
flash.

---

## Route B: build from source (PlatformIO)

The firmware is a **VS Code + PlatformIO** project — there is no Arduino sketch any more.
The full from-nothing walkthrough (installing VS Code, the PlatformIO extension, getting
the code, finding the port) is the project's
[SETUP.md](https://github.com/avandeputte/SplitFlapUniversalFirmware/blob/main/SETUP.md);
the shape of it:

1. Install **VS Code**, then the **PlatformIO IDE** extension (it downloads the ATtiny
   toolchain on first build).
2. Get the code and open the folder that **directly contains `platformio.ini`** — the
   highest-numbered version folder. Opening a parent folder is the classic mistake:
   PlatformIO looks for `platformio.ini` at the root of what you opened.
3. Connect the module as above and set `upload_port` in `platformio.ini` to your
   flasher's port (macOS `/dev/cu.usbserial-…`, Windows `COM5`, Linux `/dev/ttyUSB0`).
   Everything else in the file is already right: `upload_protocol = serialupdi`, 57600
   baud, the 10 MHz clock, `EESAVE` and the 2.6 V brown-out detector.
4. **Build** (the ✓ button, or `pio run`). No hardware needed — a good first check that
   the toolchain works. The firmware fills about 99 % of the chip's 16 KB by design.
5. **Write the fuses, once per chip:** `pio run -t fuses` (or the *Set Fuses* task in the
   PlatformIO sidebar). This is the PlatformIO equivalent of the Arduino IDE's *Burn
   Bootloader*.
6. **Upload** (the → button, or `pio run -t upload`). Success ends with avrdude's
   "bytes of flash verified" and `[SUCCESS]`.

After the one-time setup the everyday loop is two clicks, or:

| Action | VS Code | CLI |
|---|---|---|
| Compile | Build ✓ | `pio run` |
| Flash | Upload → | `pio run -t upload` |
| Write fuses (once per new chip) | *Set Fuses* task | `pio run -t fuses` |
| List serial ports | — | `pio device list` |

Prefer no VS Code at all? The PlatformIO Core CLI (`pio`) alone does everything above —
see [its install guide](https://docs.platformio.org/en/latest/core/installation/index.html).

---

## Verify it's running

On the bus, a module answers a version query with its firmware version, ID and serial:

```
m<ID>v        →  m<ID>v:32:<ID>:<serialNumber>
```

A freshly flashed, never-provisioned module has ID **255**, does not answer numeric
commands, and **advertises its serial number** every 10–15 seconds — which is exactly what
the [gateway's Provision tab](Provisioning.md) is listening for. From the gateway, **Identify
All** on the Modules tab reads every module's version in one go, so you can see that a
whole wall took an update.

## Doing a whole wall

Repeat per module: connect the three wires, fuses, firmware, disconnect, next. Once a
module has the right fuses, later updates need only the firmware step. Because identity
lives in EEPROM and the fuses keep it, **updating firmware on a provisioned, calibrated
wall changes nothing** about which module is which or how it is calibrated. Keep a
[calibration backup](SplitFlap-Gateway.md) from the gateway anyway; it is the recovery path
if a chip is ever wiped or replaced.

---

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| **`UPDI link initialization failed`** | The module is not answering. Check all three wires at both ends (without `3V3` it has no power), wait a few seconds and retry, confirm the **diode band is at `TXD`** ([UPDI Flasher](UPDI-Flasher.md)), and as a last resort use `28800` baud. |
| **`unknown programmer` / `invalid programmer`** | Your avrdude is older than 7.0. Install a current one from the releases page. |
| **`can't open device`** on Linux | You are not in the `dialout` group yet. Add yourself and log in again. |
| **`can't open device`** on Windows | Wrong COM number, or the CH340 driver is missing. |
| **Verification error partway through** | The link dropped. Run the firmware step again. |
| **Module forgets its ID or calibration after a reflash** | The `EESAVE` fuse was not set before that flash. Write the fuses, reflash, then re-provision and re-calibrate — or restore from a gateway backup. |
| **Module forgets its settings after a power cycle** | Fuses written before v32, without the brown-out detector. Write the fuses once more. |
| **PlatformIO doesn't recognise the project** | You opened a parent folder. Open the one that directly contains `platformio.ini`. |
| **Build fails pointing at a comment (`'T' does not name a type`)** | You are building a `.ino`. The project is a `.cpp` on purpose; build `src/SplitFlapUniversalFirmware.cpp`. |

---
**Next:** [Provisioning →](Provisioning.md) · [Calibration →](Calibration.md)

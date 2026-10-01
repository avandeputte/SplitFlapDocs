# The RS-485 bus protocol

Every module on the wall is an independent ATtiny1616 on a shared **half-duplex RS-485
bus**, running the [Universal Firmware](Module-Firmware.md). One controller — normally the
[SplitFlap Gateway](SplitFlap-Gateway.md), or splitflap-os, or a Raspberry Pi with a USB-RS-485 adapter — is the
bus master; modules speak only when addressed (the single exception is the unprovisioned
advertisement, below).

This page is the **wire-level reference**: everything a controller can say to a module and
exactly what comes back. You don't need it to *use* a wall — the [SplitFlap Gateway](SplitFlap-Gateway.md) gives
you point-and-click over all of these commands (its **Bus Monitor** tab even has a Send
Frame box for typing them by hand). Read on if you're writing your own controller software
or debugging with a serial console. For the flash/provision/calibrate *procedure*, see
[Module-Firmware](Module-Firmware.md).

> **Bus settings: 9600 baud, 8N1.** Commands are plain ASCII — you can drive a module from
> any serial terminal.

---

## The frame

```
m  <ADDR>  <CMD>  [data]  \n
│     │      │      │
│     │      │      └── Command payload (digits, one character, or hex string)
│     │      └───────── Command letter (see the command reference below)
│     └──────────────── Module address (see Addressing)
└────────────────────── Literal 'm' — start-of-message marker
```

Every message begins with a lowercase `m` and ends with a newline (`\n`). A message that
stops arriving without a terminator is **flushed after a 50 ms idle timeout** — the parser
recovers on its own, so a garbled frame on a noisy bus never wedges a module.

Address parsing is a simple accumulator: digits accumulate into an ID, `*` sets the
broadcast flag, `X` sets the provisioning flag, and the **first character that is none of
those is the command letter**. That one mechanism accepts every address form below with no
special cases.

## Addressing

| Form | Example | Meaning |
|---|---|---|
| Two-digit zero-padded decimal | `m38`, `m05` | Single module — v6 style |
| Variable-length decimal | `m5`, `m138` | Single module — v7+ style |
| One or two stars | `m*`, `m**` | Broadcast to all provisioned modules |
| Star with ID range | `m*v0-49` | Broadcast query to a sub-range of IDs (`v` and `A` only) |
| Literal `X` | `mXH…` | Provisioning address — every module processes it, matching by serial number |

### Staggered broadcast replies

The bus is half-duplex, so if every module answered a broadcast query (`m*v`, `m*A`) at
once the replies would collide. Instead each module computes its own reply slot:

```
replyTime = now + 30 ms lead-in + (moduleId − rangeLo) × slotWidth
```

- **`v` replies** use a **100 ms** slot (a version frame is ~40 ms on the wire).
- **`A` replies** use a **700 ms** slot (a combined dump frame is ~570 ms).
- The 30 ms lead-in gives the controller time to switch its transceiver to receive before
  the lowest ID answers. Direct-addressed replies use the same ~30 ms settling delay.
- A module whose ID falls outside the requested `<lo>-<hi>` range stays silent — that is
  what makes **ranged polling** work. A plain `m*v` is equivalent to `m*v0-254`.
  Unprovisioned modules (ID 255) never match a range and never answer broadcast queries.

On a large bus, poll in batches (`m*v0-49`, then `m*v50-99`, …) and re-issue only the
ranges that come back incomplete — far more reliable at 200+ modules than one
all-or-nothing sweep. Waiting is non-blocking on the module side: it records *when* to
answer and keeps parsing, so it stays responsive while queued.

### Direct-addressed only

Long, motor-driven commands and multi-line replies cannot be staggered across a broadcast:
**`c`, `d`, `T`, `Q`, `M` and `P` ignore the `*` wildcard** and must be sent to one ID (or
one serial number via their `mX…` forms). `A` is the exception — its broadcast form *is*
supported, staggered on wide 700 ms slots.

---

## Command reference

In all syntax below `<ID>` is a numeric module ID (0–254), `*` broadcasts to all
provisioned modules, and `<sn>` is a module's 20-character uppercase-hex serial number.
"—" in the Reply column means the command sends no reply.

### Display commands

| Cmd | Syntax | Action | Broadcast | Reply |
|---|---|---|---|---|
| `-` | `m<ID>-<char>` | Show a character. `<char>` is exactly one byte from the module's flap set. A character **not** in the set homes the reel instead (v31) — a predictable, visible response. | ✓ | — |
| `+` | `m<ID>+<index>` | Show the flap at a zero-based index, `0` to flap count − 1 (0–63 by default). An index ≥ the flap count is ignored. | ✓ | — |

```
m38-B\n       → module 38 shows 'B'
m*- \n        → all modules show blank (space = flap 0, home)
m38+7\n       → module 38 shows flap 7
```

The default 64-flap set is ` ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$&()-+=;q:%'.,/?*roygbpw`
(position 0 is always blank); both the count and the set are configurable per module with
`N` below — see [Flaps-and-Character-Sets](Flaps-and-Character-Sets.md).

### Calibration commands

| Cmd | Syntax | Action | Broadcast | Reply |
|---|---|---|---|---|
| `h` | `m<ID>h` | Home: spin to the Hall sensor, advance the stored offset to flap 0, reset the step counter. | ✓ | — |
| `c` | `m<ID>c` | Measure the exact half-steps in one revolution (two Hall passes), save to EEPROM, then home. | — | `m<ID>:<measuredSteps>` |
| `o` | `m<ID>o<steps>` | Set the home offset (half-steps past the Hall trigger to flap 0). Saved to EEPROM immediately. | ✓ | — |
| `s` | `m<ID>s<steps>` | Nudge forward `<steps>` half-steps and add the distance to the stored home offset. May be **negative** (`m38s-16`): the one-way reel spins forward nearly a full revolution to the equivalent position and the offset wraps accordingly. | ✓ | — |
| `t` | `m<ID>t<steps>` | Override total half-steps per revolution (normally measured by `c`). Saved immediately. | ✓ | — |
| `g` | `m<ID>g<position>` | Go to an absolute raw step position (0 to total − 1). Marks the current flap index unknown. | ✓ | — |
| `w` | `m<ID>w<index>:<step>` | Write a fine-calibrated step position for one flap index into the EEPROM map; `moveToIndex` then uses it instead of the evenly-spaced estimate. | ✓ | — |
| `e` | `m<ID>e` | Erase the whole flap-position map (all entries back to `0xFFFF`); the module falls back to evenly-spaced estimates. | ✓ | — |

### Configuration commands

| Cmd | Syntax | Action | Broadcast | Reply |
|---|---|---|---|---|
| `i` | `m<ID>i<newId>` | Assign a new bus ID, saved to EEPROM, effective immediately. (First-time assignment on an unprovisioned module uses `mXI` instead.) | ✓ | — |
| `a` | `m<ID>a<0\|1>` | Auto-home mode: `1` = home on every boot (default); `0` = save position on every move and restore it on boot instead. | ✓ | — |
| `N` | `m<ID>N<count>:<chars>` | Configure the flap set — see below. | ✓ | — |

**`N` in detail.** Both parts are **optional and independent**:

```
m38N48\n              → set the flap count only (1–64; chars unchanged)
m38N: ABCDEFGHIJ\n    → set the character set only (count unchanged)
m38N10: 0123456789\n  → set both: 10 flaps showing the digits 0–9
```

`<count>` drives the valid index range and the position math (`index × totalSteps / count`),
so it must match the real reel; out-of-range values are ignored. `<chars>` is the ordered
character at each flap index, up to 64 bytes, taken **verbatim to end-of-line** — it may
itself contain `:`, so only the *first* colon separates the two parts. Count and set length
are stored separately and a mismatch is tolerated. Works direct, as a broadcast (`m*N…`
configures a whole panel in one frame), and by serial number (`mXN<sn>:<count>:<chars>`).
Read the current values back with the `A` dump; a factory reset (`F`) restores both
defaults (64 / the built-in set).

### Diagnostic commands

| Cmd | Syntax | Action | Broadcast | Reply |
|---|---|---|---|---|
| `v` | `m<ID>v` / `m*v<lo>-<hi>` | Report firmware version, ID and serial number. | ✓ staggered, optional range | `m<ID>v:<version>:<moduleId>:<serialNumber>` |
| `d` | `m<ID>d` | Dump calibration: home offset, total steps, and only the *calibrated* map entries (≠ `0xFFFF`). A full dump can be ~600 bytes / ~0.6 s. | — | `m<ID>d:<homeOffset>:<totalSteps>:<idx>=<pos>,…` |
| `A` | `m<ID>A` / `m*A<lo>-<hi>` | Everything from `v` **and** `d` in one message, plus the flap set (tail appended in v31). | ✓ staggered (700 ms slots — prefer ranged batches), optional range | `m<ID>A:<version>:<moduleId>:<serialNumber>:<homeOffset>:<totalSteps>:<autoHome>:<curIndex>:<idx>=<pos>,…:<flapCount>:<flapChars>` |
| `F` | `m<ID>F` | Factory-reset EEPROM to firmware defaults (home offset 2832, total steps 4096, auto-home on, map cleared, default flap set) while **preserving the module ID and magic byte** — the module stays addressable, but needs recalibrating. | ✓ | — |
| `T` | `m<ID>T` | Hall sensor self-test: one revolution, classifies the sensor (codes below). | — | `m<ID>T:<code>:<edges>:<activeSamples>:<fallingEdges>` |
| `P` | `m<ID>P` | Re-detect Hall polarity: drives one revolution, picks the minority level as active, stores it, then re-homes. Polarity is also auto-detected on first boot and at every `c` calibrate, so `P` is only needed after re-mounting a magnet without a full recalibration. | — | `m<ID>P:<code>:<level>` — code `0` detected / `1` no magnet seen (previous kept); level `0` active-low / `1` active-high (the level now in use) |
| `Q` | `m<ID>Q` | Diagnostics snapshot — **no motor movement**, fast and safe to poll. | — | `m<ID>Q:<resetCause>:<bootCount>:<vcc_mV>:<eepromOk>:<curIndex>` |
| `M` | `m<ID>M` / `m<ID>M<n>` | Mechanical self-test: drives several revolutions and compares steps-per-rev. `<n>` requests more rotations (clamped 5–20, ~4 s each; default run ~20 s). | — | `m<ID>M:<code>:<min>:<max>:<spreadTenthsPct>:<gateActive>:<gateSpan>:<avgMagnetWidth>:<r1>,<r2>,…,<rN>` |

**`Q` fields:**

| Field | Meaning |
|---|---|
| `resetCause` | Raw reset-flag bits from the last reset: `0x01` power-on, `0x02` brown-out, `0x04` external, `0x08` watchdog, `0x10` software |
| `bootCount` | Boots since the counter last wrapped/cleared (wraps at 255) — a climbing value means the module is silently resetting |
| `vcc_mV` | Measured supply voltage in millivolts |
| `eepromOk` | `1` if the EEPROM write-read-verify check passed |
| `curIndex` | Current flap index (`-1` = position unknown, needs homing) |

**`T` result codes (Hall self-test):**

| Code | Meaning | Likely cause |
|---|---|---|
| 0 | OK | One clean home pulse per revolution |
| 1 | Stuck active | Shorted sensor, magnet jammed at the sensor, mis-wiring |
| 2 | Dead / disconnected | No magnet detection at all |
| 3 | Multiple regions | Stray magnet, electrical noise, chattering sensor |
| 4 | Inverted polarity | Active everywhere with one brief dip — wired backwards |

`<edges>` counts home pulses per revolution (healthy = 1); `<activeSamples>` is how many
sampled steps read active; `<fallingEdges>` (appended in v28) counts active→inactive
transitions — a clean sensor shows `edges == fallingEdges == 1`.

**`M` result codes (mechanical self-test):**

| Code | Meaning | Likely cause |
|---|---|---|
| 0 | OK | All revolutions consistent |
| 1 | Inconsistent | Spread > 5% — intermittent missed steps (drag, weak supply, failing driver) |
| 2 | No motion | Motor not turning (open coil, dead driver, jam) **or** a dead Hall sensor — run `T` first |

Every `M` field means the same thing regardless of code, so a parser never branches:
`min`/`max` are the smallest/largest steps-per-rev measured (both `0` on no motion);
`spreadTenthsPct` is `(max − min) / average` in tenths of a percent (`23` = 2.3%);
`gateActive`/`gateSpan` report the ~1.1-revolution motion-detect gate (on a code 2:
`gateActive` ≈ one magnet width → the reel under-rotated; ≈ 0 → the sensor never fired;
≈ `gateSpan` → parked on the magnet); `avgMagnetWidth` is the magnet's average active
width in steps; the trailing comma list is the raw steps-per-rev of every rotation —
the trend distinguishes a one-off snag from a progressive fault. Because `M` observes
motion *through* the Hall sensor, always run `T` first and interpret accordingly.

### Provisioning commands (`mX…`)

These use the `X` address and are processed by **every module on the bus** regardless of
provisioning state; each module matches the serial number internally, and non-matching
modules silently discard the frame. A module's serial is the factory-programmed
ATtiny1616 SIGROW value, formatted as a 20-character uppercase hex string.

**The advertisement** — an unprovisioned module (ID 255) does not answer numeric commands.
Instead it transmits, every **~10–15 s** (randomised per module, after listening for 20 ms
of bus silence):

```
mXadv:<serialNumber>
```

Advertisements pause during broadcast (`m*`) sweeps so they never collide with staggered
replies.

| Cmd | Syntax | Action | Reply |
|---|---|---|---|
| `mXH` | `mXH<sn>` | Home the matching module — spin its reel so you can see which physical tile it is. | — |
| `mXI` | `mXI<sn>:<newId>` | Assign a bus ID (0–254). The module writes it to EEPROM, stops advertising, and acknowledges. | `mXack:<sn>:<assignedId>` |
| `mXD` | `mXD<sn>` | Dump EEPROM config by serial number. | Same as `d` |
| `mXA` | `mXA<sn>` | Combined all-fields dump by serial number. | Same as `A` |
| `mXF` | `mXF<sn>` | Factory-reset EEPROM by serial number (preserves the module ID). | — |
| `mXN` | `mXN<sn>:<count>:<chars>` | Configure the flap set by serial number — same semantics as `N`, both parts optional. | — |
| `mXW` | `mXW<sn>:<homeOffset>:<totalSteps>:<idx>=<pos>,…[:<flapCount>:<flapChars>]` | Restore a previously dumped EEPROM image — see below. | — |
| `mXT` | `mXT<sn>` | Hall sensor self-test by serial number. | Same as `T` |
| `mXQ` | `mXQ<sn>` | Diagnostics snapshot by serial number. | Same as `Q` |
| `mXM` | `mXM<sn>` | Mechanical self-test by serial number (always the default rotation count — no `<n>`). | Same as `M` |

**`mXW` — backup and restore.** The payload mirrors the calibration portion of the `d`/`A`
dumps. The module ID is always preserved; map entries absent from the payload are cleared
to `0xFFFF`; the optional `:<flapCount>:<flapChars>` tail (exactly as `A` emits it)
restores the flap set, and if omitted the flap set is left unchanged — so a `d`/`mXD` dump
(which has no tail) still restores correctly. An `A` dump therefore **round-trips**:

```
mXAA3F24C0018E7D29B3F01\n
→  m38A:31:38:A3F24C0018E7D29B3F01:2832:4096:1:0:0=0,7=342:64: ABC…w\n

mXWA3F24C0018E7D29B3F01:2832:4096:0=0,7=342:64: ABC…w\n
```

Keeping periodic `mXA` dumps of each module means calibration *and* the flap set can be
restored onto a replacement board.

### De-provisioning

| Cmd | Syntax | Action | Broadcast | Reply |
|---|---|---|---|---|
| `R` | `m<ID>R` | Erase the stored bus ID and return to the unprovisioned state. **All calibration is preserved.** The module resumes advertising within ~10–15 s. | ✓ (`m*R` de-provisions the whole bus) | — |

---

## EEPROM layout

Identity, calibration and the flap set persist in the ATtiny's EEPROM (and survive
reflashing when the `EESAVE` fuse is set — see [Module-Firmware](Module-Firmware.md#1-flash)).
The field layout has been **stable since v6**: `0x0A`/`0x0B` were reserved padding put to
use in v26, and the v30/v31 fields sit in the previously-unused tail past the flap map, so
no v6-era field has ever moved. Any field a module has never written reads back as
`0xFF`/`0xFFFF` and falls back to its default.

| Address | Size | Contents |
|---|---|---|
| 0x00 | 1 byte | Magic byte (`0x5D`) — confirms EEPROM has been initialised |
| 0x01 | 2 bytes | Home offset — steps from the Hall trigger edge to flap 0 |
| 0x03 | 2 bytes | Total steps per revolution |
| 0x05 | 1 byte | Module bus ID (255 = unprovisioned) |
| 0x06 | 1 byte | Auto-home flag (1 = home on boot, 0 = restore saved position) |
| 0x07 | 2 bytes | Saved step position (used when auto-home is off) |
| 0x09 | 1 byte | Saved flap index (used when auto-home is off) |
| 0x0A | 1 byte | Boot counter (diagnostics; wraps at 255) |
| 0x0B | 1 byte | EEPROM health-check scratch byte (diagnostics) |
| 0x0C | 128 bytes | Calibrated step positions: 64 × `uint16_t`, `0xFFFF` = uncalibrated |
| 0x8C | 1 byte | Hall sensor active level (v30): `0` = active-low, `1` = active-high, `0xFF` = not yet auto-detected |
| 0x8D | 1 byte | Flap count (v31): `1`–`64`; `0xFF`/out-of-range → default 64 |
| 0x8E | 64 bytes | Flap character set (v31): one byte per flap; `0xFF` in the first byte → built-in default set |

**Magic byte history** — all known values are recognised and migrated to `0x5D` on first
boot after an upgrade:

| Value | Written by | Action on load |
|---|---|---|
| `0x5D` | v6 and later (current) | Load all fields — already current |
| `0x5E` | v8, v9 (erroneous bump) | Load all fields, rewrite magic to `0x5D` |
| Other | Blank chip | Write all defaults, leave ID as 255 |

Writes are read-compare-write to spare EEPROM endurance; the scratch byte at `0x0B` backs
the `eepromOk` field in the `Q` snapshot.

---

## Boot sequence

```
Power on
  │
  ├─ Capture reset cause (RSTFR) and increment the boot counter
  ├─ Read the ATtiny serial number from SIGROW; seed the RNG from it
  ├─ Load config from EEPROM (magic-byte check / migration, see above)
  ├─ Staggered startup delay — prevents inrush when a whole wall powers on:
  │     Provisioned   → (moduleId mod 32) × 120 ms   (≤ ~3.7 s)
  │     Unprovisioned → random 0–4 s (spread from the serial number)
  ├─ Enable the 2 s watchdog
  └─ Home or restore position
        autoHome = 1 → spin to the Hall sensor, advance to flap 0
        autoHome = 0 → restore the last saved step position from EEPROM
```

The **2-second hardware watchdog** runs continuously after boot: if anything hangs (say, a
stuck Hall sensor mid-move) the module resets and re-homes itself instead of staying dead
until a power cycle. On a genuinely fresh chip (polarity byte still `0xFF`), v30+ firmware
also auto-detects the Hall polarity and auto-measures steps-per-revolution once — a normal
reflash with preserved EEPROM never triggers this, so a good calibration is never silently
overwritten.

---

## The compatibility contract

The message format, command vocabulary and EEPROM layout have been **stable since v6**.
New capability arrives only two ways:

1. **A new command letter** (`A` in v24, `T`/`Q`/`M` in v26, `P` in v30, `N` in v31), or
2. **New fields appended to the end of an existing reply** — never by moving or
   repurposing an existing field's position.

Examples of the append-only rule in action: `T` gained `<fallingEdges>` in v28; `M` gained
`<gateActive>`/`<gateSpan>` in v27 and `<avgMagnetWidth>` plus the raw rotation list in
v28; the `A` dump gained `:<flapCount>:<flapChars>` in v31, appended *after* the
variable-length map so every earlier field stays byte-for-byte identical. An older
controller keeps working unchanged — it just ignores the tail.

Practical parsing rules for controller authors:

- Split replies on `:` **by field position**; never assume a reply ends where your version
  of the format ends — tolerate (ignore) trailing fields you don't know.
- When the documented *final* field is variable-length (`<flapChars>` in `A`, the payload
  of `N`/`mXN`/`mXW`), read it **verbatim to end-of-line** — it may itself contain `:`,
  `,` or `=`.
- Split rotation lists (`M`) on commas without assuming a fixed count.

---

## Canonical sources

This page summarises the firmware repo's own documentation — when in doubt, the repo wins:

- [31/README.md](https://github.com/avandeputte/SplitFlapUniversalFirmware/blob/main/README.md) — the master command and protocol reference
- [31/ARCHITECTURE.md](https://github.com/avandeputte/SplitFlapUniversalFirmware/blob/main/ARCHITECTURE.md) — how the firmware is structured, bus timing, motion model
- [31/RELEASE_NOTES.md](https://github.com/avandeputte/SplitFlapUniversalFirmware/blob/main/RELEASE_NOTES.md) — per-version change history

---
**See also:** [Module-Firmware](Module-Firmware.md) — flash, provision & calibrate ·
[SplitFlap Gateway](SplitFlap-Gateway.md) — the point-and-click UI over these commands ·
[Flaps-and-Character-Sets](Flaps-and-Character-Sets.md) — the character set and custom reels

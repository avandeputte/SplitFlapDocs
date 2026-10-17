# Module diagnostics

Every module running the Universal Firmware (v26 or newer) carries three **built-in
self-tests**, and the [SplitFlap Gateway](SplitFlap-Gateway.md) runs them for you and reads
the results back in plain language. Together they answer the question you actually have
when a cell misbehaves — *is it the power, the sensor, or the motor?* — without opening the
module, and in the right order to tell those apart.

You'd come here when a module **skips or lands on the wrong flap**, **stalls**, **resets by
itself**, **never finds home**, or has just been **built or repaired** and you want to
know it is healthy before calibrating it. If the *position* is merely off-center, that's
[Calibration](Calibration.md), not a fault; diagnostics are for things calibration can't fix.

> The [Matrix Gateway](Matrix-Gateway.md) and [LCD Gateway](LCD-Gateway.md) have no motors and no
> sensors, so this page does not apply to them.

---

## The three tests, in one minute

| Test | Bus command | What it does | Moves the reel? | Takes |
|---|---|---|---|---|
| **Stats snapshot** | `Q` | Reports the last reset cause, boot count, supply voltage, an EEPROM write-verify, and the current flap | No | Instant |
| **Hall sensor self-test** | `T` | Turns the reel one revolution and watches the home sensor | Yes, ~1 turn | 10–20 s |
| **Mechanical self-test** | `M` | Turns the reel several times and counts the steps of each revolution | Yes, 5–20 turns | ~4 s per turn |

**The order matters.** The snapshot first, because a sagging supply voltage explains
"motor" faults and resets alike, and you should fix that before chasing anything else. The
Hall test second, because the mechanical test *measures motion through the Hall sensor* — a
dead sensor makes a perfectly good motor report "no motion". The gateway runs them in this
order automatically.

---

## Running them from the gateway

1. Open the gateway's web UI and go to the **Modules** tab.
2. Turn on **Maintenance mode** (Calibration tab) if a companion or home automation is
   driving the wall — a display update arriving mid-test would fight the spinning reel. The
   tests themselves don't require it.
3. Click the **🩺 stethoscope** icon on the module's card. The icon is only shown for
   modules that report firmware **v26 or newer**; on older modules the card has no
   diagnostics.
4. A results dialog opens and fills in as the tests complete: the **snapshot** at once,
   then the **Hall test** (the reel turns once), then the **mechanical test** (the reel
   turns five times by default).
5. On firmware **v29 or newer** a **rotation count** control (5–20) appears under the
   mechanical result. More rotations catch rarer, intermittent faults; each adds about four
   seconds. Pick a count and click **Run again** to repeat only the mechanical test.

Run one module at a time. The motor-driven tests are direct-addressed (there is no
"test every module" broadcast, on purpose), and the gateway allows only one motor test in
flight — starting one on a *different* module while one is running answers
`409 Conflict` (re-running the same module is allowed). The dialog can be closed at any
time; a running test simply finishes on the module.

> **Legacy (v7) modules** have no self-tests. Everything on this page needs the
> [Universal Firmware](Module-Firmware.md).

---

## Reading the results

The dialog interprets every result for you; this is what the words mean and what to do
about them.

### Stats snapshot (`Q`)

| Row | Healthy | Worth attention |
|---|---|---|
| **Last reset cause** | *power-on* (you just powered it) or *none recorded* | **brown-out** — the supply dipped low enough to reset the chip. **watchdog** — the firmware hung and recovered. Both mean the module is resetting when it shouldn't; a climbing boot count confirms it. |
| **Boot count** | Small, and not changing between runs | Climbing between polls → the module is silently resetting in the field (supply, wiring, a loose connector). Wraps at 255. |
| **Supply voltage** | At your design rail: about **5 V** on a 5 V build, **3.3 V** on a 3.3 V build | Flagged **LOW** when a 5 V rail reads under 4.5 V, or a 3.3 V rail under 3.0 V. A sagging rail under-powers the stepper: missed steps, stalls, brown-out resets. Check the supply's current rating and the wiring gauge before anything else. |
| **EEPROM verify** | *passed* | **FAILED** — the chip could not write and read back a scratch cell. Calibration and identity live in that EEPROM; treat the module as unreliable. (The check runs on the first snapshot after boot and then at most hourly; later snapshots repeat the cached result.) |
| **Current flap index** | A flap number | *unknown (needs homing)* is normal after power-up until the module has homed; *released* means the motor is idle and unpositioned. |

### Hall sensor self-test (`T`)

The reel turns one revolution and the module counts how many times, and for how long,
the home sensor saw the magnet. A healthy reel shows **one** rising edge and **one**
falling edge — one clean home region per turn.

| Verdict | Meaning | Likely cause / fix |
|---|---|---|
| **OK** | One clean home region per revolution | — |
| **Stuck active** | Reads active all the way round | Shorted sensor, the magnet jammed against the sensor, or a wiring fault. **Homing cannot work until this is fixed.** |
| **Stuck inactive** | Never reads active | Dead or disconnected sensor, or the home magnet is missing. |
| **Multiple regions** | Active more than once per revolution | Electrical noise, a stray magnet, or a chattering sensor. Homing may land on the wrong position. |
| **Inverted polarity** | Active almost all the way round with one brief dip — the mirror image of healthy | The sensor is wired with reversed polarity. Firmware v30+ auto-detects Hall polarity on first home; the `P` command re-detects it (see [Bus Protocol](Bus-Protocol.md#diagnostic-commands)). |

The **Edges** row shows rising / falling counts; the dialog flags an OK result whose edges
are not 1 / 1, which means the active region straddles the revolution boundary or the
sensor releases raggedly. **Active samples** is how many steps the sensor read active — the
width of the magnet's region, useful later (see the mechanical test).

### Mechanical self-test (`M`)

The reel turns several times and the module counts the steps of each revolution, using the
home sensor as the reference. Consistent counts mean the motor, its driver, and the supply
are all keeping up.

| Verdict | Meaning | Likely cause / fix |
|---|---|---|
| **OK** | Every revolution consistent (spread within 5 %) | Motor, driver and supply are healthy. |
| **Inconsistent** | Revolutions varied by more than 5 % — intermittent missed steps | Mechanical drag or binding (flaps rubbing, a tight bearing), a weak or sagging supply under load, or a failing driver channel. Check the supply-voltage row of the snapshot first. |
| **No motion** | The reel did not complete a sensed revolution | Either the motor is not turning (open coil, a dead driver channel, a physical jam) **or the Hall sensor is dead** — the test cannot tell the two apart by itself, which is why the Hall test runs first. |

For a **No motion** result the dialog reads the *motion gate* — how many steps the sensor
was active during a ~1.1-revolution sweep — and tells you which it was:

- active about **one magnet width** (roughly 150–200 steps): the sensor works but the reel
  **under-rotated** — motor slip;
- active **0**: the sensor **never fired** — dead sensor, or the magnet never reached it;
- active for the **whole sweep**: the reel is **parked on the magnet**, or the sensor is
  stuck active (the Hall test above will say the same).

Two more rows repay a look when the verdict is *Inconsistent*:

- **Per-rev counts** — the raw steps of each revolution. `4096, 4095, 4097, 4096, 3700`
  is one snag among healthy turns: an *intermittent* glitch. `4096, 4030, 3960, 3890, 3820`
  is a steady decline: a fault *in progress* — a motor losing torque as it heats, or a
  coupler loosening. The spread alone cannot tell these apart; the trend can.
- **Magnet width (avg)** — the average width of the sensor's active region across the
  turns. If it wanders while the step counts stay steady, or drifts away from the Hall
  test's *active samples*, the **sensor-to-magnet gap is changing** as the reel turns:
  shaft wobble, or a loosening magnet.

> A **wild** mechanical result — an enormous spread, or a "revolution" counted as far fewer
> steps than a real one — usually means the **Hall sensor is producing false detections**,
> not that the motor failed. Believe the Hall test before replacing a motor or driver.

---

## Symptom → what to run → what it usually is

| Symptom | Look at | Typical finding |
|---|---|---|
| A module **resets on its own**, or "forgets" where it was | Snapshot: reset cause, boot count, supply voltage | Brown-out resets and a low rail → supply or wiring. Watchdog resets → the firmware hung; note the firmware version and report it. |
| Flaps land **one or two positions off, sometimes** | Mechanical test (after a clean Hall test) | *Inconsistent* — missed steps from drag or a weak supply. If the count is stable, it's calibration instead: [Calibration](Calibration.md). |
| The reel **never finds home** / spins forever on power-up | Hall test | *Stuck inactive* (dead sensor or missing magnet) or *Inverted polarity*. |
| Homes to the **wrong place** every time | Hall test | *Multiple regions* (noise, stray magnet). If the Hall test is clean, it's the home offset: [Calibration](Calibration.md#step-2-fix-the-home-position). |
| The reel **doesn't move at all** | Hall test, then mechanical test | Hall OK + *No motion* with a one-magnet-width gate → motor slip / jam. Hall *Stuck inactive* → the sensor, not the motor. |
| Calibration values **won't stick** | Snapshot: EEPROM verify | *FAILED* → the chip's EEPROM is unreliable; replace the module. |
| A **new or repaired** module, before calibrating | All three | Expect *OK*, *OK*, near-zero spread, and a supply at your design rail. |

---

## Without the gateway

The tests are plain bus commands, so any RS-485 host can run them — a serial terminal, a
script, or the [Gateway API](Gateway-API.md) from automation:

```
m38Q          → m38Q:<resetCause>:<bootCount>:<vcc_mV>:<eepromOk>:<curIndex>
m38T          → m38T:<code>:<risingEdges>:<activeSamples>:<fallingEdges>
m38M          → m38M:<code>:<min>:<max>:<spreadTenthsPct>:<gateActive>:<gateSpan>:<avgMagnetWidth>:<r1>,<r2>,...
m38M20        → mechanical test over 20 rotations (v29+)
```

By serial number, for a module that has no ID yet: `mXQ<sn>`, `mXT<sn>`, `mXM<sn>`. Every
field and result code is specified in [Bus Protocol ▸ Diagnostic commands](Bus-Protocol.md#diagnostic-commands).

Over REST, the gateway sequences the motor-driven tests as a job you poll:

| Call | What happens |
|---|---|
| `POST /api/flap/diag` `{"id":38}` | Returns the snapshot inline as `q`, and starts the Hall test |
| `GET /api/flap/diag/status` | `state` is `pending`, then `done` with the result **once** (the next read says `idle`), or `timeout` |
| `POST /api/flap/diag/mech` `{"id":38,"revs":10}` | Starts the mechanical test; `revs` 5–20 is honoured on v29+ |

Both motor tests are refused with a **503** while a [restore on boot](SplitFlap-Gateway.md)
is running, since that owns the bus; while they run they hold the bus themselves, so
display content from outside the dashboard is paused *(v3.15)*.

---

## When a module answers short questions but not long ones

The three tests tell you about a module's hardware. A different kind of fault looks like
a dead module and is not one: the module answers `v` (its version, 30-odd bytes) every
time, answers the stats snapshot, and then fails its **calibration backup** — the `A`
reply, the longest frame a module ever sends, several hundred bytes. Erasing the EEPROM
"fixes" it, because an empty calibration makes the reply short again. That pattern is a
**bus** problem — a long frame breaking up over a marginal line — or a module whose
transmitter runs out of breath, not a module whose hardware is failing, and the
self-tests will all pass. Two tools in the gateway are built for exactly this, and
neither moves a flap.

### The reply-size probe

In the module's Diagnostics dialog, below the three tests *(gateway v3.14)*. It asks the
module for four replies of increasing size — `v`, `Q`, the EEPROM dump `d` and the
combined dump `A` — three times each, and shows which came back and how big they were.
Read it as a staircase:

| What you see | What it usually is |
|---|---|
| Every size answers, every time | The module and the line are fine; look elsewhere (a stale registry entry, a wrong ID). |
| Short replies answer, `d` and `A` fail or come back short | The **line** loses long frames: termination, cable length, a marginal transceiver, or a baud rate the wiring cannot carry cleanly. Also check Bus Health for *discarded* frames. |
| Only `A` fails, and only sometimes | Borderline. The gateway already falls back to `v`+`d` for a backup when `A` fails, so the backup still succeeds; fix the line when you can. |
| Nothing answers at all | The module is silent — now the three tests, or the [Without the gateway](#without-the-gateway) commands, are the next step. |

The probe runs on its own and holds the bus while it does; it will not start while a
self-test, a calibration or the soak test owns the bus, and the button stays disabled
until the motor tests on the dialog have finished. Over REST: `POST /api/flap/probe`
`{"id":38,"rounds":3}`, then poll `GET /api/flap/probe/status` until `state` is `done`;
each step carries `tries`, `ok` and the longest `bytes` seen.

### The soak test

The probe asks one module a dozen questions. The soak asks **the whole wall** for minutes on
end, and in seven different ways, which is what catches the module that only drops out now and
then. On the Status tab, under **Bus Health** *(gateway v3.15)*, pick **5, 10, 20 or 30
minutes** and start it. Pass after pass it works the bus a different way:

| Pass | What it sends | What that catches |
|---|---|---|
| **Roll call** | `m*v<lo>-<hi>` — every module answers in its own timed slot | a reply that is missing, that arrives damaged, or that arrives **twice** for one ID |
| **Version, snapshot** | `v`, `Q` — the short replies, one module at a time | power and contact faults, which hit every size equally |
| **Dump, combined dump** | `d`, `A` — the long replies | a line that loses long frames |
| **Broadcast dump** | `m*A<lo>-<hi>` — the longest replies, back to back | slot timing under the heaviest load the bus ever sees |
| **Write round trip** | the home offset and one map entry, each nudged one half-step, read back, **put back**, read back again | a write that does not land, or an EEPROM that no longer holds one |

Nothing it sends moves a flap, so it is safe on a wall in service, with one caveat: it holds the
bus for the whole run, so display content from outside the dashboard is paused until it
finishes. You can cancel it at any time; a write round trip always runs to its restore step
first. The two values it writes are read back and written back to what they were. If one cannot
be confirmed restored, the report says so **first**, names the module, and prints the original
value so you can write it back by hand or restore that module from your backup.

**The report is a list of findings, not a scoreboard.** Each one names the modules, the evidence
and what to do:

| The finding | What it means | Where to start |
|---|---|---|
| **The bus loses long frames** — short replies fine, long ones lost, worst modules first | the line, not the modules | the 120 Ω termination at **both** ends, then total cable length and any stub, then the baud rate |
| **Dropping out at every size** — the shortest reply fails as often as the longest | power or contact at those modules | re-seat them, check the pogo pins and the rail voltage in the snapshot; neighbours point at a shared backplane segment |
| **Cannot send their dump** — every short reply arrives, not one dump ever does | the module's calibration map has grown too large for its firmware to assemble that reply | erase the map and restore from your backup, which writes the entries one at a time (see below) |
| **Replies collide in broadcasts** — fine asked alone, missing or damaged in roll calls | two modules talking at once | Identify, then compare serial numbers and firmware versions |
| **Two modules share an ID** — one ID answered twice in a broadcast | exactly that | Identify lists both serials; give one a new ID |
| **Writes do not stick** | the value is not stored, or not read back as written | the snapshot's EEPROM verify: *FAILED* means a worn chip |
| **Never answered** | not on the bus, or not on this ID | power, the pogo pins, a broken trace; Identify to see what is really out there |

Over REST: `POST /api/flap/soak` `{"minutes":10}` (1–60), `GET /api/flap/soak/status` for the
live tally (one row per module, `[ok, tries]` per kind of traffic plus the longest reply, the
current and the worst miss streak), `POST /api/flap/soak/cancel` to stop early. The soak, the
probe and the self-tests refuse to run over one another (`409`).

### A full calibration map can silence a module's dump

Worth knowing before you fine-tune all 64 flaps on a module. On module firmware **v32**, a
module whose map is completely full can no longer send its EEPROM dump at all: it answers `v`
and `Q` normally, and `d`/`A` never arrive, until the map is erased. Its backups fail from then
on and its calibration cannot be read, while the display keeps working — which is the puzzle
reported as *"the module stopped answering `mXA`; erasing the EEPROM fixed it."* The module
assembles the whole reply before it sends anything, and a full map does not fit.

Until the module firmware streams its dump:

- **Back up before you fully calibrate**, not after.
- **Fine-tune only the flaps that need it.** Total Steps and Home Offset get a reel most of the
  way; a map with a handful of entries dumps without trouble.
- **To recover a module that has stopped dumping**, erase its map (`m<id>e`, or Factory Reset in
  its Info dialog) and restore it from your backup. The restore writes the entries one at a
  time, which the module takes without complaint — it is only the *reply* that cannot be
  assembled, not the storage.

---

## Good habits

- **Run the snapshot on every module once in a while** — it moves nothing, takes no time,
  and a climbing boot count or a low rail is the earliest warning you will get of a supply
  problem, long before flaps start landing wrong.
- **Diagnose before you calibrate.** Calibrating a module that is missing steps just bakes
  the fault into the map. Get a clean Hall test and a near-zero spread first.
- **After any mechanical work** — a new flap set, a re-seated magnet, a replaced motor — run
  all three, then re-home and re-check the calibration.
- **Soak a new wall once, and after any rewiring.** Ten minutes with a clean sheet is a
  baseline you will be glad to have the day a module starts missing backups.
- **Keep the firmware current.** v26 introduced the tests; v28 added the per-revolution
  counts and magnet width; v29 the rotation count; v30 automatic Hall-polarity detection.
  The gateway shows what a module reports and hides what it can't.

---
**Related:** [Calibration](Calibration.md) · [Module Firmware](Module-Firmware.md) ·
[Bus Protocol](Bus-Protocol.md#diagnostic-commands) · [Hardware](Hardware.md)

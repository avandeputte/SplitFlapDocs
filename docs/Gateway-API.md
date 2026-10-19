# The Gateway API (REST & MQTT)

> **MQTT is SplitFlap Gateway (physical) only.** The Matrix Gateway removed its entire MQTT/Home
> Assistant surface in firmware **3.0** — its push channel is the SSE stream (`GET /api/events`)
> and its only control surface is REST. Rows below marked "both" for MQTT-adjacent endpoints
> predate that and are annotated.

This is the integrator's reference for driving a gateway programmatically — both the
[SplitFlap Gateway](SplitFlap-Gateway.md) (driving a real RS-485 wall) and the
[Matrix Gateway](Matrix-Gateway.md) (the same firmware family drawing virtual
modules on an LED panel). They speak **the same API by design**; where they differ, this page
says so. (Both products run on ESP32-class boards — the Matrix Gateway is an ESP32-S3 —
so this page never says "ESP32" to tell them apart: the distinction is the wall each
drives, and the labels are **SplitFlap Gateway** and **Matrix Gateway**.) Every display
endpoint here ultimately wraps the raw bus frames documented in
[Bus Protocol](Bus-Protocol.md) — `POST /api/flap/char` with `{"id":5,"char":"A"}` becomes
`m5-A\n` on the wire.

*(The [Companion](Companion.md) exposes a separate, Vestaboard-compatible surface of its own —
that's [Vestaboard API](Vestaboard-API.md), not this page.)*

## Orientation

- **Base URL:** `http://<gateway-ip>` — or `http://192.168.4.1` while on the setup AP. The
  Both gateways advertise mDNS names of the form **`splitflap-gw-<6 hex digits>.local`** —
  the board's own id (SplitFlap Gateway since firmware 3.11; before that, plain
  `splitflap-gw`). The Matrix Gateway's hostname is also configurable. mDNS is
  best-effort — see [finding it on your network](SplitFlap-Gateway.md#finding-it-on-your-network).
- **JSON in, JSON out.** All `POST` endpoints accept and return `application/json` (the two
  binary exceptions — OTA upload and the companion settings blob — are called out below).
- **CORS is open.** Every endpoint sends `Access-Control-Allow-Origin: *`, so a page served
  from anywhere on your LAN can call the API straight from the browser.
- **No authentication.** Anything that can reach the gateway's IP can drive the wall — the
  API treats your LAN as the trust boundary. The only credential anywhere is the optional
  OTA password.
- **Which wall am I talking to?** `GET /api/config` reports `product` and `version` (the firmware version). Key behaviour on
  `product` and on `/api/capabilities` tokens, not on version heuristics.

## REST endpoints

### Bus

| Method | Path | Body | Reply | Gateway |
|---|---|---|---|---|
| `GET` | `/api/rs485/messages` | — | Frames buffered since the last call (up to 64); each call drains the buffer | SplitFlap Gateway only |
| `GET` | `/api/log` | — | Commands acted on since the last call, up to 64  — same drain-cursor idea, but there is no wire to trace on a drawn wall | Matrix Gateway only |
| `POST` | `/api/rs485/send` | `{"data":"m5-A\n"}` — optional `"raw":true` | `{ok,bytes}` | SplitFlap Gateway |
| `POST` | `/api/frames/send` | `{"data":"m5-A\n"}` — optional `"raw":true` | `{ok,bytes}` | **Matrix Gateway** |
| `POST` | `/api/rs485/batch` | `{"frames":["m00-A\n","m01-B\n",…],"step_ms":15}` | `{ok,sent}` | SplitFlap Gateway |
| `POST` | `/api/frames/batch` | `{"frames":[…],"step_ms":15}` | `{ok,sent}` | **Matrix Gateway** |

> **Matrix Gateway naming.** Its raw-frame endpoints are `/api/frames/send` and `/api/frames/batch`
> — bodies and behaviour identical to the SplitFlap Gateway's `rs485` paths. Frames on a drawn wall are **one-way**:
> the modules act on them and nothing replies.

**Framing is normalized for you.** Unless `"raw":true`, the gateway strips/re-adds the
trailing newline and trims junk past a complete known command — `m5-A` and `m5-A\n` behave
identically. `raw` is the debugging escape hatch that sends bytes verbatim. Frame syntax
lives on [Bus Protocol](Bus-Protocol.md).

**Batch is how pages get drawn.** One batch call — `POST /api/rs485/batch`, or `/api/frames/batch`
on the Matrix Gateway — carries a whole wall of up to 512 frames in a single HTTP call, with no
broker in the display path. On a physical wall it is what the [Companion](Companion.md) uses for every
page; on a Matrix wall the Companion prefers the higher-level [`/api/display/cells`](#display),
which skips unchanged cells and reaches lowercase, accents and pictographs. `step_ms` (0–30) paces
the cascade device-side so the wall animates instead of snapping over at once. Since gateway 3.4
paced frames are *queued* and the call returns immediately: **`200` means accepted, not yet on the
wire**, and the pacing queue holds 127 frames in flight (a longer cascade loses its stagger past
that point; the frames still all arrive).

### Modules

| Method | Path | Body | Reply | Gateway |
|---|---|---|---|---|
| `GET` | `/api/flap/modules` | — | Array of module objects. **SplitFlap Gateway:** `id, serial, firmware, current character, last-seen`. **Matrix Gateway:** just `{id, flapIndex, flapChar}` — a drawn module has no serial or firmware | both |
| `POST` | `/api/flap/char` | `{"id":5,"char":"A"}` — `id:-1` broadcasts | `{ok}` | both |
| `POST` | `/api/flap/index` | `{"id":5,"index":1}` | `{ok}` | both — 0–63 on a real 64-flap reel, 0–236 on the Matrix Gateway's 237-flap reel |
| `POST` | `/api/flap/text` | `{"text":"HELLO","start":0}` | `{ok,chars}` | both |
| `POST` | `/api/flap/home` | `{"id":5}` — `id:-1` homes all | `{ok}` | both |

`char` and `text` take UTF-8 and transcode to the single Windows-1252 byte the bus uses, so
`€` and accented letters work. ASCII letters are uppercased — **except** the seven lowercase
colour codes `r o y g b p w`, which address the colour flaps and go through as-is. Characters
with no Windows-1252 representation are rejected.

The SplitFlap Gateway also carries a whole **hardware-maintenance tier** under `/api/flap/*` —
version/EEPROM queries, calibration, provisioning, self-diagnostics, per-module flap-set
config, restore-by-serial, and the bus tests — `POST /api/flap/probe` with
`GET /api/flap/probe/status` *(v3.14)*, and `POST /api/flap/soak` with `…/soak/status` and
`…/soak/cancel`, `…/soak/log` for the raw trace of the last run *(v3.17)*, with
`…/soak/snapshot` and `…/soak/rollback` to keep or replay the calibration
it read before it began *(v3.15)*, both described in
[Module Diagnostics](Module-Diagnostics.md#when-a-module-answers-short-questions-but-not-long-ones).
The Matrix Gateway omits all of it by design: its modules are drawn, so there is nothing to
calibrate or provision. That tier is documented in the SplitFlapGateway README and
`openapi.yaml` (see [the footer](#canonical-sources)).

### Display

| Method | Path | Body | Reply | Gateway |
|---|---|---|---|---|
| `GET` | `/api/display/state` | — | `{rows,cols,cells:[…]}` — cell index = row·cols + col = module id; `null` = no module there. The Matrix Gateway adds `flaps:[index…]` (the raw flap index per cell — the only way to tell a **colour flap**, index 156–162, from a lowercase `r o y g b p w`, whose `cells` letter is identical) and `mode:"wall"\|"pixels"` (`pixels` = canvas/effect/animation/ticker owns the panel; render `GET /api/canvas/frame` instead of cells) | both |
| `GET` | `/api/events` | — | **Server-Sent Events stream** (`events` capability token): a `display` event with the display-state JSON within ~150 ms of the wall changing (max ~7/s, snapshot on connect, 15 s keepalives, up to 3 streams — a 4th gets `503`), plus a `status` event with the `/api/status` JSON every 5 s. With gestures enabled it also carries `clap` / `tap` events (`{count,seq}` — count 2 = a double) the instant one is detected. The dashboard's Live Display and status pane ride it, with polling as fallback | Matrix Gateway only |
| `GET`/`POST` | `/api/sound` | — / `{freq,ms,vol}` or `{notes:[[f,ms],…],vol}` or `{stop}` | *(`sound` token)* Tones and chimes on the board's speaker — on-device synthesis. **Quiet Time silences it** (mid-play too); the settings **master enable** (`403` off) and **master volume** apply  | Matrix Gateway only |
| `POST` | `/api/sound` (wav) | `{"wav":"/sounds/x.wav","vol":80}` | Stream a WAV from the microSD card — strict 16-bit 16 kHz mono/stereo PCM. Quiet Time + master enable/volume apply | Matrix Gateway only |
| `GET` | `/api/environment` | — | *(`environment` token)* Onboard SHTC3 temperature + humidity — `{available, tempC, tempF, rh, ageMs}`; also in `/api/status` under `env` | Matrix Gateway only |
| `GET` | `/api/status` (resets) | — | `resets`: the last 8 reboots as `[cause, minutesAlive]` pairs from RTC memory — a crashed board names its own killer (1 poweron, 3 sw, 4 panic, 5-7 watchdogs, 9 brownout, 11 usb) | Matrix Gateway only |
| `GET`/`POST` | `/api/timer` | `{"min":5}` or `{"sec":90}` (1 s – 24 h) / `{"stop":true}` | *(`timer` token)* One kitchen timer, full-screen anti-aliased countdown that **outranks every mode** (canvas included) while it alerts; `TIME!` + chime at zero (the chime overrides Quiet Time — you asked for it). `GET` → `{active,remaining,alarmFiring}` | Matrix Gateway only |
| `GET`/`POST` | `/api/alarms` | a JSON **array** of slots: `[{"time":"07:30","days":127,"enabled":true},…]` (up to 4; omitted slots disable; slot 0 may carry `tzOffsetMin`) | *(`alarms` token)* 4 daily alarm slots (`days` is a Mon-Sun bitmask), persisted; ring is a red-flash screen + chime for 90 s. Dismiss via `POST /api/timer {"stop":true}` — or a double gesture | Matrix Gateway only |
| `GET` | `/api/gestures` | — | *(`claps`/`taps` tokens)* Clap detection (mic DSP: transient over the room floor + a not-bass spectral gate) and tap detection (the IMU's on-die tap engine). Off by default — `clapEnabled`/`tapEnabled` in settings. Detections stream as SSE `clap`/`tap` events for the companion to act on; **a double gesture dismisses a running timer or ringing alarm on-device** (audit-logged to the card, not forwarded). Reply carries availability, lifetime counters, and reset-on-read tuning telemetry | Matrix Gateway only |
| `GET` | `/api/sd` | — | *(`sd` token)* microSD card presence + capacity — `{present, type, sizeMB, usedMB, freeMB}`; also in `/api/status` under `sd`. Answers 200 even with no card (`present:false`). The firmware keeps its own event log on the card at `/logs/gateway.log`: boot post-mortems, watchdog reasons, OTA events, 10-min heap heartbeat | Matrix Gateway only |
| `GET` | `/api/sd/list` | `?path=/` | One directory level: `[{name,dir,size},…]`. Paths are card-absolute (must start with `/`, no `..`). `503` when no card is mounted | Matrix Gateway only |
| `GET` | `/api/sd/get` | `?path=/dir/file` | Download a file as raw bytes (`application/octet-stream`, `Content-Disposition` carries its name). `&tail=N` returns only the last N bytes — how the dashboard's log viewer reads `/logs/gateway.log` without pulling the whole file | Matrix Gateway only |
| `PUT` | `/api/sd/mkdir` | `?path=/dir` | Create a directory (parent must exist) → `{ok}`; `409` if it already exists | Matrix Gateway only |
| `PUT` | `/api/sd/put` | `?path=/dir/file` + raw body | Upload/overwrite a file → `{ok,bytes}` | Matrix Gateway only |
| `DELETE` | `/api/sd/delete` | `?path=/dir/file` `[&recursive=1]` | Remove a file, an empty directory, or (with `recursive=1`) a directory and everything under it → `{ok}`. A non-empty dir without the flag returns `409`; the card root is protected | Matrix Gateway only |
| `GET`/`POST` | `/api/backup` | — | *(v3.16)* The card guards the flash: internal FATFS (animations, fonts, atlases, the companion blob) is mirrored incrementally to `/backup/fatfs` — nightly at 03:30 (`backupEnabled` setting), after boot when no mirror exists, or `POST` to run now. Deletions prune the mirror. **A reformatted FATFS (crash recovery) is restored from the mirror automatically on the next boot.** `GET` → pass status/counters | Matrix Gateway only |
| `POST` | `/api/display/cells` | `{"start":0,"step_ms":15,"cells":[{"ch":"H"},{"color":"red"},{"blank":true},{"skip":true}]}` | RS-485: `{ok,cells,sent,skipped}` · Matrix Gateway: `{ok,cells,sent}` | both (SplitFlap Gateway 3.8+) |

`/api/display/state` drives the Live Display. On the SplitFlap Gateway a cell is the *tracked*
character (`"?"` when unknown, e.g. after a home or an index set); on the Matrix Gateway it is
read straight from the module and reported as a **code point**, so lowercase, accents and a
`♥` read back as themselves (a colour flap reports as its protocol letter).

`/api/display/cells` is the **index-addressed display API** — the same JSON contract on both
gateways, so one client can drive either wall through one endpoint. Each cell is exactly one
of `ch` (a character), `color` (a **named** flag: `red orange yellow green blue purple
white`), `blank` (home the module) or `skip` (leave it alone); `step_ms` (0–30) paces the
cascade without ever blocking the web server. It exists because the one-byte character
protocol cannot say everything: the byte for lowercase `r` already means *red*, and a heart
has no byte at all — see [Reaching the extra
flaps](Matrix-Gateway.md#reaching-the-extra-flaps).

One deliberate difference:

| | SplitFlap Gateway | Matrix Gateway |
|---|---|---|
| A cell the wall can't show | **Lenient** — skipped, reported in `skipped` (real reels differ per module; only structural errors 400) | **Strict** — the whole request is a `400` ("no flap for U+1F600"), resolved before anything is sent |
| Sent on the (emulated) bus as | `m<id>-<char>` — each module maps the byte against its own reel | `m<id>+<n>` — one shared reel, so an index always names the same flap |

A client that needs certainty consults `/api/capabilities` first.

### Status & configuration

| Method | Path | Body | Reply | Gateway |
|---|---|---|---|---|
| `GET` | `/api/status` | — | Uptime, IP, NTP, heap, PSRAM and OTA-slot figures and why the board last rebooted *(v3.16: `psram`, `flash`, `reset`)*, and the quiet flag (SplitFlap Gateway also `maintenance` and `mqtt`). The Matrix Gateway adds a `panel` object — size, grid, font, and the **running bit `depth`** — and per-task stack watermarks (`stk`) | both |
| `GET` | `/api/config` | — | Current configuration, passwords excluded; includes `product` + `version` | both |
| `POST` | `/api/config/wifi` | `{"ssid":"…","pass":"…"}` | `{ok}` — reconnects | both |
| `POST` | `/api/config/mqtt` | `{"host":"…","port":1883,"user":"…","pass":"…","prefix":"splitflap"}` | `{ok}` — reconnects | SplitFlap Gateway only (the Matrix Gateway has no MQTT) |
| `POST` | `/api/config/settings` | Send only what you're changing: `posixTZ`, `ntpServer`, `serialDebug`, `haEnabled`, `otaPassword` — the Matrix Gateway adds panel fields (`panelW`/`panelH`/`panelBitDepth`/`panelBGR`/`panelBright`), the module-grid layout (`gridRows`/`gridCols`) and flip timing (`flapMs`/`flapMax`), the brightness schedule (`dimEnabled`/`dimStart`/`dimEnd`/`dimLevel` — nightly dim that yields to Quiet Time), and gesture enables (`clapEnabled`/`tapEnabled`), and the nightly SD backup (`backupEnabled`, v3.16) | `{ok}` | both |
| `POST` | `/api/config/rs485` | Bus parameters (baud, data bits, parity, stop bits) | `{ok}` | SplitFlap Gateway only — the Matrix Gateway removed it (there is no RS-485 bus) |
| `GET` | `/api/config/export` | — | *(v3.16)* Every setting as one downloadable JSON file (named `<hostname>-config.json`) — WiFi password deliberately excluded, so the file is safe to store anywhere. The nightly SD backup writes the same export to `/backup/config.json`: card + firmware binary rebuild a board completely | Matrix Gateway only |
| `POST` | `/api/config/import` | an exported settings file | *(v3.16)* Applies whichever known keys the body carries (same clamps as NVS load), saves, and reports `rebootNeeded` when a boot-read field (panel geometry, grid, hostname, fbPsram) changed | Matrix Gateway only |
| `GET` | `/api/capabilities` | — | What the wall can show — [see below](#apicapabilities-one-contract-across-walls) | both, identical shape |
| `GET` / `POST` | `/api/maintenance` | `{"on":true}` | `{ok,on}` | **SplitFlap Gateway only** — the Matrix Gateway removed maintenance mode (a drawn wall needs no calibration to protect) |
| `GET` | `/api/bus` | — | *(v3.15)* Who holds the bus: `level` (0 free, 1 busy, 2 exclusive), `reason`, `remaining` seconds (−1 = no expiry) and the list of `holds` | SplitFlap Gateway only |
| `POST` | `/api/bus/hold` | `{"reason":"backup","seconds":60}` | *(v3.15)* Take or renew a busy lease (5–300 s; the same reason renews in place). Reasons the firmware owns are refused | SplitFlap Gateway only |
| `GET` / `DELETE` | `/api/bus/incidents` | `?max=50` | *(v3.16)* What the bus got wrong, newest first: the module it belongs to, the command in flight, the size and the time. Kinds are `D` discarded, `R` would not parse, `L` answered only on the second ask, `M` never answered, `X` two modules on one ID. `DELETE` clears it | SplitFlap Gateway only |
| `POST` | `/api/bus/release` | `{"reason":"backup"}`, or `{"reason":"soak","force":true}` | *(v3.15)* Drop a lease taken with `/api/bus/hold`. *(v3.15.1)* `force` releases a hold the firmware owns — the way out of a stuck banner; forcing the soak's hold cancels the soak, and a restore can only be cancelled | SplitFlap Gateway only |
| `GET` / `POST` | `/api/quiet` | `{"on":true}` | `{ok,on}` | both |
| `GET` / `POST` | `/api/quiet/schedule` | `{"enabled":true,"start":"22:00","end":"07:00","days":127}` | `{enabled,start,end,days}` | both |
| `POST` | `/api/mqtt/test` | `{"host","port","user","pass"}` — all optional, defaults to saved config | Broker reachability + credentials, without touching the live connection | SplitFlap Gateway only (the Matrix Gateway has no MQTT) |

**The bus hold** *(SplitFlap Gateway, v3.15)*. Every maintenance operation — provisioning,
calibration, the self-tests, the probe and the soak, a backup sweep, a restore — takes a hold on
the bus automatically for its own duration, and each hold is a lease that expires on its own.
While a *busy* hold is in force the display endpoints (`/api/flap/char|index|text|home`,
`/api/rs485/send|batch`, `/api/display/cells`, quiet ON) answer
`503 {"error":"maintenance in progress -- display content is paused","reason":"…","remaining":N}`
to any caller that does not send the header `X-SF-Client: dashboard`, and MQTT display commands
are dropped; **retry after `remaining` seconds.** A caller also counts as the operator when it
is the address that took the hold *(v3.15.1)*, so a proxy that strips unknown headers cannot
lock a client out of its own hold. `/api/flap/home` is **not** gated as content: homing is
maintenance and stays available *(v3.15.1)*, except while a probe, soak or self-test is
measuring the bus, when content and homing are both refused to every caller. An *exclusive* hold (a restore) answers
`503 {"error":"bus is reserved"}` to every bus route, dashboard or not. Read-only endpoints,
settings and status are never gated; `/api/status` carries the current hold as `bus.lock`.
**Maintenance mode** is the same hold without an expiry, flipped by hand; before v3.15 it gated
MQTT only, so a companion driving the wall over REST could paint over a calibration in progress.
**Quiet time** blanks the wall — every reel homes to its blank flap — and restores it
when turned off; the schedule's `days` is a bitmask, bit 0 = Sunday. Both reset to off on reboot.

### Files, display & system (Matrix Gateway)

| Method | Path | Body | Reply | Gateway |
|---|---|---|---|---|
| `GET` | `/api/fs` | — | FATFS totals + recursive file list — the storage behind `/anim`, `/fonts` and the companion blob | Matrix Gateway only |
| `GET` | `/api/fs/file?path=…` | — | Download one file (`Content-Disposition` carries its name) | Matrix Gateway only |
| `POST` | `/api/fs/delete` | `{"path":"/anim/x.mpg"}` | `{ok}` — deliberately unrestricted; it is your flash | Matrix Gateway only |
| `POST` | `/api/fs/upload?name=<file>` | The file's bytes, raw (**raw body**, `curl --data-binary`) | `{ok,path,bytes}` — routed by extension: `.mpg`→`/anim/`, `.fnt`→`/fonts/`, else `/` | Matrix Gateway only |
| `GET`/`POST` | `/api/display/brightness` | `{"brightness":1-255}` | Panel brightness, applied to the next frame and persisted; the `brightness` capability token advertises it | Matrix Gateway only |
| `POST` | `/api/system/reboot` | — | `{ok,rebooting:true}` — replies first, then restarts | Matrix Gateway only |

### OTA & UI

| Method | Path | Body | Reply | Gateway |
|---|---|---|---|---|
| `GET` | `/ota` | — | Browser firmware-upload page | both |
| `POST` | `/api/ota/upload` | `firmware.bin` — the plain **app image**, never the factory image. Multipart on the physical gateway; on the Matrix Gateway the **raw binary body** (`curl --data-binary @firmware.bin`) | Flashes and reboots | both |
| `GET` | `/lang/{code}` | — | The dashboard's translation dictionary for one language (keys are the English strings); `404` for a code the firmware doesn't ship | both |

`/lang/{code}` is served with `Content-Encoding: gzip` — a *transfer* encoding the client
inflates transparently. Note the contrast with the companion settings blob below, where the
gzip bytes **are** the payload.

### Canvas (Matrix Gateway only)

The Matrix Gateway can hand its HUB75 panel over as a plain **framebuffer**, so a client can draw
anything on it — raw frames (`rgb888`/`rgb565`/**QOI**), partial rectangles, an on-device animation
loop, a scrolling ticker, JSON **and binary** draw ops, twelve on-device effects (each self-describing its parameters), a persistent draw stream, named sprite atlases, and a framebuffer readback, and a
framebuffer readback. A physical wall has no framebuffer, so none of these endpoints exist there.

The full surface — `GET`/`POST /api/canvas`, `PUT`/`GET /api/canvas/frame`, `PUT /api/canvas/rect`,
`PUT /api/canvas/qoi`, `PUT /api/canvas/anim`, `POST /api/canvas/ticker`, `POST /api/canvas/ops`,
`POST /api/canvas/effect` — is documented on its own page: **→ [Canvas API](Canvas.md).**

## /api/capabilities — one contract across walls

`GET /api/capabilities` answers *"what characters can this display show?"* in one call, made
once when a client connects. Both gateways answer the same URL with the same shape **by
design** — a client never has to know which kind of wall it is talking to. (It is the "what
can you show" companion to `/api/display/cells`' "show this".)

The subtlety it exists for: on a real wall the answer is **not one set**. Every module owns
its reel, and since module firmware v31 each can be told a different one — so the response
reports set arithmetic, not a single alphabet:

| Field | The question it answers |
|---|---|
| `charset.union` | Can this wall show a `Z` **anywhere**? — every character *some* module can show |
| `charset.common` | Can I lay this text across **arbitrary** cells? — every character *every* module can show |
| `charset.uniform` | Does every module carry the same reel? (always `true` on the Matrix Gateway — one drawn reel) |
| `charset.assumed` | Module ids too old (pre-v31) to report a reel — theirs is *assumed* to be the firmware default, and the guess is visible rather than folded in silently |
| `charset.unknown` | Module ids whose reel is genuinely not known yet — excluded from both sets |
| `sets` | Each **distinct** reel once: `flaps`, `source` (`reported`/`assumed`/`builtin`), the reel `chars` **verbatim in flap-index order**, and the ids that carry it as a compressed list (`"0-44,50"`) |
| `colors` | The colour flaps the wall actually has, **by name** (`["red","orange",…]`) |
| `maxFlaps` | Flaps a module can carry — 64 real, 237 drawn |
| `features` | Named capability flags to check instead of sniffing endpoints. The walls differ: a SplitFlap Gateway advertises e.g. `["colors","index","batch","quiet","maintenance","ha","ota","flapconfig"]`; a **Matrix Gateway** advertises `["cells","colors","index","lowercase","pictographs","quiet","ota","canvas","effects","ticker","brightness","events","effectDefs"]` `timer`/`alarms` (3.14), plus `audio`/`sound`/`environment`/`sd`/`claps`/`taps` when the mic, speaker, sensor, card or IMU is present — and no `maintenance`/`flapconfig`/`ha`. `` — note `canvas`/`effects`/`ticker`, and no `maintenance`/`flapconfig` |
| `surface` | **What the wall is drawn on** (v3.17, drawn gateways only): `{"kind": "led-matrix" \| "lcd", "w", "h", "colorBits", "refreshHz"}` — a chunky LED matrix and a 10.1″ LCD invite different client rendering (art density, fonts, what "pixels" even look like), so the surface is stated directly, never inferred from the product name. `colorBits` is total bits per pixel (a depth-4 matrix = 12, the LCD\'s RGB565 = 16). The physical SplitFlap Gateway omits the key — no pixels to describe |
| `motion` | **How the wall moves** (SplitFlap Gateway 3.10+; every Matrix Gateway): `{"kind": "drawn" \| "mechanical", "settleMs": …}`. `drawn` — a cell is a repaint, interruptible, nothing queues, so sub-second updates are honest; `mechanical` — motion must physically complete, and `settleMs` (~4000: a full revolution) is a real constraint. On the drawn wall `settleMs` is the worst-case flip *animation* (`flapMs × flapMax`, live-configurable) — cosmetic pacing, advisory. Stated directly so a client never infers the wall's nature from which endpoints exist. |

Plus `product`, `fw`, `openapi` (the path of the device's own live spec), `grid` (rows × cols), `modules` and `maxFlaps`. A **Matrix Gateway** additionally
advertises a `canvas` object (pixel `formats` including `qoi`, panel `width`/`height`, and the
`rect`/`anim`/`ticker`/`readback` flags), an `effects` list, and `effectDefs` (per-effect parameter declarations)
— the entry points to the [Canvas API](Canvas.md).

`union` and `common` genuinely differ: if module 1 carries `A-Z` and module 2 carries `0-9`,
the union is `A-Z0-9` but the common set is **empty** — the wall cannot show `HI42` wherever
it likes, and only `common` says so. Reporting each distinct reel once (rather than one entry
per module) is what keeps the response small: a uniform wall is a few hundred bytes however
large it is.

**Two translations** are applied to the character sets, matching exactly what the gateway
does when it resolves a frame: the seven colour flaps `r o y g b p w` are kept *out* of the
sets and reported by name under `colors`, and `q` — which the classic reel borrows for the
double-quote flap — is reported as `"`. A client that read those as letters would believe a
classic reel can show a lowercase `w`.

## The companion contract

Two endpoint pairs make the [Companion](Companion.md) and the gateway feel like one product —
and let a containerized companion run **diskless**.

### Registration: `/api/companion`

| Method | Body / reply | Behavior |
|---|---|---|
| `POST` | `{"url":"http://192.168.1.60:8000","status":"Running: Weather","tabs":[{"id":"apps","label":"Apps"},…]}` | Register and heartbeat. The URL is persisted (debounced, so heartbeats don't wear the flash); `status` and `tabs` are runtime-only and clear on reboot. An **empty `url` deregisters**. Either field may be sent alone |
| `GET` | `{url,status,tabs,gwTabs}` | The registered companion's URL, its last reported status, and both sides' tab lists |

**The tabs advertisement** (gateway 3.4) is how the two navs stay in sync without matched
releases: the companion sends `tabs` — the deep links its UI actually has — and the reply
always carries `gwTabs`, the gateway's own. Each side then links exactly what the other
really offers. Both halves are optional and independent, so any old/new pairing works: a peer
that says nothing simply gets the built-in list.

### Settings blob: `/api/companion/settings` (gateway 3.1)

The gateway is deliberately a **dumb blob store** for the companion's settings, playlists and
triggers. The payload is `gzip(minified JSON)` whose schema belongs entirely to the
companion — the firmware stores the bytes verbatim, hands them back byte-for-byte, and never
parses them. A companion container becomes effectively **stateless**: destroy it, start
another on a different host, and it restores its configuration from the gateway on boot.

| Method | Behavior |
|---|---|
| `GET` | Returns the stored blob as `application/gzip`, or `404` when nothing is stored yet |
| `PUT` | Stores the gzipped request body **atomically**; replies `200 {"ok":true,"bytes":N}` |

- **Atomic writes.** The body streams to a temp file, renamed over the live one only once the
  last byte lands — a crash or dropped connection mid-upload can never corrupt settings that
  were already good.
- **No `Content-Encoding: gzip`.** The gzip bytes *are* the payload, not a transfer encoding
  of it — declaring the encoding would make HTTP clients silently decompress the body. The
  companion decompresses it itself.
- **Bounded.** Blobs over 64 KB are rejected with `413`; real ones are 1–2 KB, and the
  companion debounces its writes so a burst of edits becomes one write.
- **Durable.** The blob lives on the FATFS partition (`/compset.gz`), which a firmware update
  doesn't touch — it survives OTA.
- **Errors:** `400` empty or truncated body · `413` too large · `503` filesystem not
  mounted · `507` write failed.

On the companion side this is `COMPANION_SETTINGS_STORE`: `mirror` (default — local file
primary, mirrored here), `local`, or `gateway` (diskless). The companion gates the feature on
`GET /api/config` reporting `version >= 3.1` and quietly falls back to local storage against
an older gateway.

## MQTT

Optional. Default topic prefix **`splitflap`** (configurable in Settings → MQTT), default
port **1883**. MQTT never carries display frames for the companion — that path is always
REST — but it is the transport for Home Assistant and for external automations.

### Published

| Topic | Payload | When |
|---|---|---|
| `splitflap/rx` | `{"ts":…,"wt":"…","command":"m5-A"}` | Frame received from the bus |
| `splitflap/tx` | `{"ts":…,"wt":"…","command":"m5-A"}` | Frame transmitted to the bus |
| `splitflap/status` | Heartbeat with the full diagnostic set — uptime, frame count(s), heap, RSSI, module count, IP, version, quiet flag (SplitFlap Gateway also `maintenance`) | Once per minute |
| `splitflap/flap/adv` | `"AABBCCDD…"` | Unprovisioned module advertisement |
| `splitflap/flap/ack` | `{"id":5,"sn":"…"}` | Provisioning acknowledgement |
| `splitflap/flap/version` | `{"id":5,"ver":"12","reportedId":5,"sn":"…"}` | Version response |
| `splitflap/flap/calibrated` | `{"id":5,"stepsPerRev":4096}` | Calibration result |
| `splitflap/flap/dump` | `{"id":5,"dump":"…"}` | EEPROM dump response |
| `splitflap/availability` | `online` / `offline` | Retained; `offline` via MQTT Last Will |
| `splitflap/display/state` | `HELLO   WORLD` | Best-known display contents (`?` = unknown), on change |
| `splitflap/maintenance/state` | `ON` / `OFF` | Maintenance mode |
| `splitflap/quiet/state` | `ON` / `OFF` | Quiet time |

The `rx`/`tx`/`status`/`flap/*` topics publish whenever MQTT is connected; `availability`,
`display/state`, `maintenance/state` and `quiet/state` (plus the discovery configs) publish
only when **Home Assistant integration** is enabled on the Settings tab. *(Topic names here are the
SplitFlap Gateway's; the Matrix Gateway renames and trims them — see the note after the Subscribed
table.)*

### Subscribed

| Topic | Payload | Action |
|---|---|---|
| `splitflap/send` | `m9h\n` or `{"data":"m9h\n"}` (optional `"raw":true`) | Send a raw frame — normalized like `/api/rs485/send` |
| `splitflap/flap/set` | `{"id":5,"char":"A"}` | Show character |
| `splitflap/flap/home` | `{"id":5}` | Home module |
| `splitflap/flap/provision` | `{"sn":"AABBCC…","id":5}` | Provision module |
| `splitflap/flap/flapconfig` | `{"id":5,"flapCount":40,"charSet":" ABC…€é"}` | Configure a module's flap set (fw v31+) — SplitFlap Gateway only; the Matrix Gateway dropped this topic (its reel isn't configurable) |
| `splitflap/display/set` | `HELLO` | Show a string from module 0 (the Home Assistant text entity) |
| `splitflap/maintenance/set` | `ON`/`OFF`/`true`/`1` | Set maintenance mode (reachable even while it's on) |
| `splitflap/quiet/set` | `ON`/`OFF`/`true`/`1` | Set quiet time |

****The Matrix Gateway has no MQTT at all.** Everything in this section is SplitFlap Gateway (physical) only.

With MQTT configured, the SplitFlap Gateway can also announce itself to **Home Assistant** via
retained MQTT discovery (opt-in on the Settings tab) — a device with a Display text entity,
Maintenance and Quiet switches, and diagnostic sensors. That, and what the companion adds on
top, is covered on [Home Assistant](Home-Assistant.md).

## Canonical sources

The two repos are the source of truth; each ships a machine-readable OpenAPI 3.1 spec you can
import straight into **Postman** (Import → drop the file, then set a `baseUrl` collection
variable to your gateway's IP), **Swagger Editor** ([editor.swagger.io](https://editor.swagger.io)
for interactive try-it-out docs), or **Insomnia**:

| Gateway | README (API sections) | OpenAPI spec |
|---|---|---|
| Split-Flap Gateway (RS-485) | [README.md](https://github.com/avandeputte/SplitFlapGateway/blob/main/README.md) | [openapi.yaml](https://github.com/avandeputte/SplitFlapGateway/blob/main/openapi.yaml) |
| Matrix Gateway | [README.md](https://github.com/avandeputte/MatrixPortalGateway/blob/main/README.md) | [openapi.yaml](https://github.com/avandeputte/MatrixPortalGateway/blob/main/openapi.yaml) |

Both specs are generated alongside the firmware and track it closely — the Matrix Gateway's
documents the full `/api/canvas/*` surface under its **Canvas** tag, for instance. Where a spec and
its README ever disagree, **the README is current**.

---

Both gateways also serve their spec **live** at `GET /openapi.yaml`, discoverable via RFC 9727's `GET /.well-known/api-catalog` — always the contract of the firmware you're actually talking to. The Companion serves its own API the same way: `/openapi.json`, `/openapi.yaml` and `/.well-known/api-catalog` on its port.

**See also:** [SplitFlap Gateway](SplitFlap-Gateway.md) · [Matrix Gateway](Matrix-Gateway.md) ·
[Bus-Protocol](Bus-Protocol.md) · [Vestaboard-API](Vestaboard-API.md) ·
[Home-Assistant](Home-Assistant.md) · [Compatibility](Compatibility.md)

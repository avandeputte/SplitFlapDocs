# The Canvas API (Matrix Gateway)

Everything else in this guide treats the [Matrix Gateway](Matrix-Gateway.md) as a **wall of flaps**.
But under the split-flap costume it is, physically, a grid of RGB LEDs — and the Matrix Gateway
can hand that grid over as a plain **framebuffer**, bypassing the split-flap emulation entirely,
so you can draw *anything* on it. A real [SplitFlap Gateway](SplitFlap-Gateway.md) has no framebuffer
at all, so **this is the one place a Matrix wall does something the hardware it emulates simply
cannot** — and every endpoint on this page is Matrix-only.

You rarely drive this by hand: the [Companion](Companion.md) exposes all of it through **canvas apps**
(see [Built-in Apps](Built-in-Apps.md#matrix-panel-only-apps) and
[Writing Matrix Apps](Writing-Matrix-Apps.md)). This page is the integrator's reference; the
per-op detail lives in the [Canvas Ops Reference](Canvas-Ops-Reference.md); and the
machine-readable contract is the **Canvas** tag of the gateway's own spec — **every wall
serves it at `GET /openapi.yaml`** (also discoverable via RFC 9727's
`/.well-known/api-catalog`), so you always read the contract of the firmware you're
actually talking to.

## How it behaves

- **Takeover.** Pushing a frame, ops, an image, an animation, a ticker, an effect or an open
  stream channel **stands the reel renderer down** — the same way it does during an OTA — and
  the canvas owns every pixel. (One deliberate exception: the `soundwall` effect drives the
  flap wall itself and leaves the reel renderer running.)
- **Release.** `POST /api/canvas {"active":false}` (or `POST /api/canvas/effect {"type":"none"}`)
  repaints the wall from the modules' current state.
- **Auto-reclaim.** Any split-flap command that changes the wall — a character, an index, a
  home, over `/api/frames/*` or `/api/display/cells` — **takes the panel back automatically**,
  so sending content to the wall always shows it. **Quiet Time** reclaims it too.
- **Nothing on screen is persisted.** A reboot always returns to the flaps — with two
  exceptions: animations and fonts **saved to the on-device library** survive as files, and a
  configured **boot animation** autoplays at power-on until the first display command supersedes
  it (see [the animation library](#the-animation-library-and-the-boot-animation)).

## Discovery

A client learns the whole surface from `GET /api/capabilities` (see
[Gateway API](Gateway-API.md#apicapabilities-one-contract-across-walls)) — a physical gateway carries
none of these keys, so their presence *is* the signal that this is a Matrix wall:

```json
"openapi": "/openapi.yaml",
"canvas":  { "formats": ["rgb888","rgb565","qoi"], "width": 256, "height": 64,
             "rect": true, "rects": true, "stream": true,
             "anim": true, "ticker": true, "readback": true,
             "atlas": { "named": true, "persist": true,
                        "maxSheets": 16, "maxBytes": 4194304, "maxSheetBytes": 2097152 },
             "ops": ["clear","pixel","hline","vline","line","rect","circle","ellipse",
                     "triangle","roundrect","gradient","polyline","poly","arc","clip",
                     "origin","text","textbox","image","sprite","scroll","show"] },
"effects": ["plasma","fire","matrix","fliporama","clock","life",
            "spectrum","soundwall","maze","ripple"],
"effectDefs": [ { "id": "fire", "name": "Fire",
                  "params": [ { "key": "audio", "type": "bool",
                                "default": false, "label": "Audio reactive" } ] }, … ],
"features": [ …, "canvas", "effects", "ticker", "brightness", "events",
              "audio", "effectDefs" ]
```

Feature-detect from the **tokens and keys, not version numbers**: `canvas.rects`,
`canvas.stream`, `canvas.atlas`, the `audio` token (present only when the microphone ADC
actually answered at boot), `effectDefs` (one entry per effect declaring exactly
the typed, ranged, labelled params it consumes, so an effects UI builds itself), and the
`canvas.ops` list for individual ops.

`GET /api/canvas` reports the live state: `{active, width, height, formats, effect, anim,
ticker, atlas, effects}` — take the panel dimensions from here before you size a frame.
`atlas` is `{bound, loaded:[…]}` — the sticky-bound sheet name and every resident
sheet.

## Pixel formats

| Format | Bytes/px | Notes |
|---|---|---|
| `rgb888` | 3 | `R G B` per pixel. |
| `rgb565` | 2 | **Big-endian** (high byte first). Halves the upload; the panel's colour depth loses nothing to it. |
| `qoi` | — | [QOI](https://qoiformat.org): lossless, ~2–4× smaller than raw, one-pass decode. |

For a raw frame or rectangle upload the format is **inferred from the body length** — a
full frame is unambiguously `W×H×3` or `W×H×2`, so nothing has to be signalled and any
`?fmt=` hint is ignored: the length is authoritative. (The readback `GET`, which has no
body, *does* take `?fmt=rgb888|rgb565`.)

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` / `POST` | `/api/canvas` | Canvas state / take over (`{"active":true}` blanks) or release (`false`). |
| `PUT` | `/api/canvas/frame` | Blit a full raw frame — `W×H`, row-major, top-left, rgb888 or rgb565. |
| `GET` | `/api/canvas/frame` | **Read the panel back** as raw pixels (a screenshot). |
| `PUT` | `/api/canvas/rect` | Update **one rectangle** without resending the whole panel. |
| `PUT` | `/api/canvas/qoi` | A full-panel **QOI** image. |
| `PUT` | `/api/canvas/anim` | Upload an animation that **loops on-device** from PSRAM. |
| `POST` | `/api/canvas/anim/save` | **Persist** the loaded animation to the on-device library. |
| `POST` | `/api/canvas/anim/play` | Load a **library animation** and play it. |
| `POST` | `/api/canvas/anim/delete` | Delete a library animation. |
| `GET` | `/api/canvas/anims` | List the animation library. |
| `PUT` | `/api/canvas/gif` | Import an ordinary **animated GIF** into the animation store. |
| `POST` | `/api/canvas/transition` | Configure a **crossfade / wipe / slide** for full-frame presents. |
| `PUT` | `/api/canvas/rects` | **Multi-rect delta**: one binary body of N changed regions, drawn over the frame, presented once — 10–50× less traffic than full-frame re-sends (`canvas.rects` capability). |
| `PUT` | `/api/canvas/stream` | **Persistent draw channel**: one long-lived connection carrying TLV draw records back-to-back — no per-frame round trip (`canvas.stream` capability). `GET` reports channel state. |
| `GET` | `/api/canvas/audio` | Microphone features behind the audio effects: level / beat / 16-band spectrum, plus whether the ES7210 is present and capturing. Derived numbers only — no samples. |
| `PUT` | `/api/canvas/atlas/<name>` | Upload a **named sprite tile sheet** for the ops `sprite` op. |
| `GET` | `/api/canvas/atlas` | List the atlas library — resident + persisted sheets. |
| `POST` | `/api/canvas/atlas/<name>/save` | Persist a sheet to flash (`/atlas/<name>.mpta`). |
| `DELETE` | `/api/canvas/atlas/<name>` | Delete a sheet, resident and persisted. |
| `PUT` | `/api/canvas/font` | Upload a **custom font** (the `custom` face). |
| `POST` | `/api/canvas/font/save` / `font/delete` | Persist / delete a **library font**. |
| `GET` | `/api/canvas/fonts` | List the font library. |
| `POST` | `/api/canvas/ticker` | One line of **scrolling text**, rendered on-device — exclusive or an **overlay**. |
| `POST` | `/api/canvas/ops` | A JSON batch of **draw commands** (shapes + labels + sprites). |
| `POST` | `/api/canvas/opsb` | The same draw batch in the **fixed-layout binary encoding** (`canvas.opsBin`) — ~6× smaller, no JSON parse on the panel. See [Canvas Ops Reference → Binary encoding](Canvas-Ops-Reference.md#binary-encoding). |
| `POST` | `/api/canvas/effect` | Start an **on-device effect** (or `none` to release). |

### `PUT /api/canvas/frame` — a full raw frame

Body is `W×H` pixels, row-major, top-left origin, streamed straight to the back buffer (no
multi-KB frame is buffered whole). Length must equal `W×H×3` (rgb888) or `W×H×2` (rgb565) exactly,
or it is a `400`. Reply `{ok, width, height, pixels}`.

With a transition configured (below), the frame is staged in PSRAM and **tweened on-device**
instead of hard-cutting.

### `POST /api/canvas/transition` — how full frames present

`{"type": "none|crossfade|wipe|slide", "ms": 100-2000}` — **sticky and persisted (saved to NVS, restored at boot; `GET /api/config` reports `transitionType`/`transitionMs`)** (saved to NVS, restored at boot; `GET /api/config` reports it as `transitionType`/`transitionMs`). Applies to full-frame presents — `PUT /api/canvas/frame`
and `PUT /api/canvas/qoi` (the format the companion actually sends): the incoming frame is
staged in PSRAM, the outgoing frame is captured from the framebuffer, and the tween renders
on the gateway — `crossfade` blends, `wipe` sweeps left to right, `slide` pushes the old
frame off to the left. `ms` is the duration (default 400). rect and anim are untouched, and
if the staging buffers can't be allocated the frame falls back to a hard cut rather than
failing.

### `GET /api/canvas/frame` — framebuffer readback

A screenshot of whatever is on screen — wall, effect, canvas, animation or ticker — reconstructed
from the framebuffer. **Read-only: it never takes the panel over**, so a UI can poll it for a live
preview. The body is raw pixels (`?fmt=rgb888` default, or `?fmt=rgb565`); the dimensions and
format are echoed in `X-Canvas-Width`, `X-Canvas-Height` and `X-Canvas-Format` so a client needn't
have called `GET /api/canvas` first.

Two caveats: the colours are **quantised to the panel's real bit depth** (it is what is physically
lit, not the intended image), and **brightness — an OE duty cycle — is not in the framebuffer**, so
a dim wall still reads back at full value.

### `PUT /api/canvas/rect` — partial update

Update one rectangle without resending the whole panel — the changed area costs only its own bytes.
The body is an **8-byte big-endian header** — `x`, `y`, `w`, `h`, one unsigned 16-bit each — then
`w×h` pixels, rgb888 or rgb565 by the remaining length. It is drawn **on top of what is on screen**
(the back buffer is synced to the live frame first), so everything outside the rectangle is
untouched. Off-panel pixels are dropped.

### `PUT /api/canvas/qoi` — a compressed image

A full-panel QOI image whose dimensions must match the panel. Buffered in PSRAM and decoded in one
pass. Reply `{ok, width, height}`; `400` if it isn't a QOI image for this panel, `507` if memory is
low (see [below](#a-note-on-memory-the-507-guard)).

### `PUT /api/canvas/anim` — an on-device animation loop

Upload a short loop **once** and it plays on-device from PSRAM, so the client can disconnect. The
body is a **14-byte header** followed by the frames back-to-back:

| Bytes | Field | |
|---|---|---|
| 0–3 | magic | `"MPGA"` |
| 4 | version | `1` |
| 5 | format | `2` = rgb565, `3` = rgb888 |
| 6 | fps | 1–60 |
| 7 | flags | bit 0 = loop |
| 8–9 | width | u16 (must match panel) |
| 10–11 | height | u16 (must match panel) |
| 12–13 | frames | u16 |

Then `frames × W × H × (2 or 3)` bytes of frame data. The store is capped at 8 MB of PSRAM
(≈ 256 frames at 256×64 rgb565). Reply `{ok, frames}`; errors `400` (bad header / short upload),
`413` (over budget), `503`/`507` (memory).

### The animation library, and the boot animation

The animation store is volatile; the **library on the gateway's own
flash** (the 23.9 MB FATFS partition), so a loop is uploaded once and kept:

| Call | Does |
|---|---|
| `POST /api/canvas/anim/save` `{"name":"x"}` | Write whatever is loaded — an `MPGA` upload, a GIF import, a previous play — to `/anim/<name>.mpg`, byte-identical to the wire format. `409` when nothing is loaded. |
| `POST /api/canvas/anim/play` `{"name":"x"}` | Load a library entry into the store and play it. `404` unknown name, `409` during Quiet Time. |
| `POST /api/canvas/anim/delete` `{"name":"x"}` | Remove it. |
| `GET /api/canvas/anims` | The library: `[{name, bytes, frames, w, h, fps, loop}, …]`, metadata re-read from each file's header. |

Names are **1–24 characters of `a-z 0-9 - _`** (a bad name is a `400`); saving over an existing
name replaces it, atomically enough that an interrupted save never corrupts the old entry.
Storage errors surface as `503` (filesystem unavailable) and `507` (full / write failed).

**The boot animation.** Set `bootAnim` to a library name (`POST /api/config/settings`, reported
by `GET /api/config`; empty string disables) and the gateway plays it **at boot, before WiFi is
even up** — a splash screen from flash. The first display command supersedes it, exactly like
any other animation.

### `PUT /api/canvas/gif` — GIF import

The `MPGA` format needs a packer; a GIF doesn't. Upload an ordinary **animated GIF** (whole file,
4 MB cap) and the gateway decodes it **on-device** into the same animation store the `anim`
upload fills — GIF deltas, transparency and frame disposal composited properly, a GIF smaller
than the panel **centred on black**, one larger than the panel rejected with `400`. Playback fps
comes from the GIF's own frame delays, clamped 1–30. It plays immediately, and because it lands
in the same store, `anim/save` persists it and `bootAnim` can name it. Reply `{ok, frames, fps}`;
errors `400` (undecodable / oversized-for-panel / truncated), `413` (over 4 MB, or more frames
than the store holds), `503`/`507` (memory).

### `POST /api/canvas/ticker` — scrolling text, exclusive or overlay

`{"text": "…", "color": [r,g,b], "speed": 1-20}` scrolls one line across the panel on-device, no
streaming. The font is auto-picked for the panel height. An **empty `text` hands the panel back** to
the wall — and stops an overlay ticker too. Starting one is refused with `409` during Quiet Time.

Two options:

- **`"overlay": true`** composites the ticker as a **lower-third band over whatever else is
  presenting** — the flap wall, an effect, an animation, a pushed frame — instead of taking the
  panel over. It rides a hook on every presented frame, so it **survives page and mode changes**;
  only an explicit `{"text":""}`, Quiet Time, or replacing it with a non-overlay ticker removes
  it. `"band": false` drops the black band and scrolls the glyphs straight over the content.
- **`"font": "…"`** names a face: `custom` is the uploaded slot (see
  [fonts](#put-apicanvasfont-uploadable-fonts)), any other name loads a library face.
  Unknown names fall back to the built-in face — a missing font scrolls text, it never errors.

Reply `{ok, active, overlay}`.

### `POST /api/canvas/ops` — draw commands The ops surface grew up: **`arc`** (arcs/pies, 0° = 12 o'clock CW — the gauge
primitive), **`poly`** (filled or outlined closed polygons), **`clip`** and **`origin`**
(batch-scoped clip window and coordinate translation — build placeable components),
**`textbox`** (word-wrap + two-axis alignment, clipped), thickness **`t`** on `line`/
`polyline`/`rect`/`circle`/`ellipse` outlines, **anti-aliased text** (`"aa":true`, smooth
Orbitron at 34/24/13 px, A–Z 0–9 `:.-+%/`), `outline`/`shadow` text styles, and **sprite
transforms** (`flip`, `rot` 90/180/270, `scale` 1–4). `canvas.ops` in capabilities is the
authoritative list; per-op parameter tables with defaults and examples live in the
**[Canvas Ops Reference](Canvas-Ops-Reference.md)**, and the device's own `/openapi.yaml`
carries the machine-readable spec.

A JSON **array** of ops, applied in order and presented — shapes and labels without composing a
whole frame client-side. Colours are `[r,g,b]` (0–255); off-panel pixels are dropped; unknown ops
are skipped. The set a wall offers is advertised as `capabilities.canvas.ops`.

| Op | Shape |
|---|---|
| `clear` | fill the panel (`color`, black by default) |
| `pixel` | `x, y` |
| `hline` / `vline` | `x, y, w` / `x, y, h` |
| `line` | `x, y` → `x1, y1` (Bresenham) |
| `rect` | `x, y, w, h`, outline or `fill: true` |
| `circle` | `x, y` centre, `r` radius, outline or `fill: true` |
| `ellipse` | `x, y` centre, semi-axes `rx, ry`, outline or `fill: true` |
| `triangle` | vertices `x,y` · `x1,y1` · `x2,y2`, outline or `fill: true` |
| `roundrect` | `x, y, w, h`, corner `r`, outline or `fill: true` |
| `gradient` | fill `x, y, w, h` with a linear gradient `from` → `to`, `dir` `"v"` (default) or `"h"` |
| `polyline` | connect `points: [[x,y],…]` with lines |
| `text` | `x, y, s`, `size` (bundled CP1252 faces, 8–20), `align` `"left"` (default) / `"center"` / `"right"`, `font` — `"custom"` or a library face; unknown names keep the built-in face |
| `image` | blit a base64 sprite: `x, y, w, h`, `fmt` (`rgb888`/`rgb565`), `data` — ≤ 8 KB decoded (use `PUT /api/canvas/frame` for a full panel) |
| `atlas` | `{"op":"atlas","name":"…"}` — bind a named sheet for subsequent `sprite` ops (lazy-loads a persisted sheet). Sticky across batches; an unknown name binds nothing — later sprites no-op, the batch never fails |
| `sprite` | blit tile `i` of the **bound** [atlas](#put-apicanvasatlasname-a-named-sprite-tile-sheet) at `x, y` — magenta pixels transparent; skipped (not counted) with nothing bound or `i` out of range |
| `scroll` | shift the current frame by `dx, dy`, filling vacated pixels with `color`. Make it the **first** op, then draw the newly-revealed edge — a **marquee** without resending the panel |
| `show` | present mid-batch (otherwise presented once at the end) |

### `PUT /api/canvas/stream` — a persistent draw channel

Every REST draw costs a full HTTP round trip, and with Nagle's algorithm on the gateway
each response adds a ~40 ms delayed-ACK floor — fine for a clock, limiting for animation.
The stream channel removes both: one long-lived `PUT` carries **TLV records**
back-to-back, executed as they arrive, with **no per-record response**. A rect-delta
animation measures ~28 fps client-paced over one connection.

Record framing (big-endian): `u8 type, u24 payloadLength, payload`.

| type | payload | effect |
|------|---------|--------|
| `0x01` | `u8 fmt (2 = rgb565 BE, 3 = rgb888)` + W×H×bpp pixels | full frame — draw, no present |
| `0x02` | the `PUT /api/canvas/rects` body verbatim | rect deltas — draw, no present |
| `0x03` | a JSON array as `POST /api/canvas/ops` | ops (present only via its `show` op) |
| `0x04` | sheet name | bind a named atlas sheet |
| `0x05` | *(empty)* | present the back buffer |
| `0x06` | a binary ops batch, as `POST /api/canvas/opsb` | binary ops (present via its SHOW op) |
| `0x00` | *(empty)* | end — the gateway answers `200 {"ok":true,"records":N}` and closes |

Draw and present are separate so records compose: frame + rects + ops, one `show`.

Rules of the road:

* Declare a large placeholder `Content-Length` (the embedded server has no inbound
  chunked support) and just stop at the end record.
* **Send the first record in the same write as the request head.** A bare
  body-carrying head parse-blocks stock esp_http_server's single worker for the 8 s
  socket timeout — any body byte alongside the head avoids it. (Generic server
  behaviour, not specific to this route.)
* One stream at a time; the drawing REST endpoints answer `409` while it is open.
* A malformed record or 30 s of silence aborts the stream; the panel keeps its last
  frame either way.
* `GET /api/canvas/stream` returns `{open, records, ticks, lastClose, …}` — handy for
  discovering whether a stream is live and why the previous one ended.

### `PUT /api/canvas/atlas/<name>` — a named sprite tile sheet

Up to **16 resident named sheets** share a **4 MB** PSRAM budget (**2 MB** per-sheet cap),
LRU-evicted when it fills. An upload builds in a fresh allocation and **publishes atomically
at commit**, so a bound sheet is never blitted half-written — there is no "blits no-op during
upload" window any more. Name grammar `[a-z0-9._-]{1,32}` (it becomes a filename when
persisted). The body is the unchanged 12-byte MPTA header (`MPTA`, ver `1`, fmt `2`=rgb565 BE /
`3`=rgb888, tileW, tileH, tiles — all big-endian) followed by the tile pixels, row-major,
magenta transparent (`0xF81F` / `255,0,255`).

`POST /api/canvas/atlas/<name>/save` persists the sheet as `/atlas/<name>.mpta`; a persisted
sheet that gets evicted (or a reboot — nothing preloads) **lazy-loads on its next bind**.
`GET /api/canvas/atlas` lists everything — `[{name,tiles,w,h,fmt,bytes,resident,persisted}]` —
and `GET /api/capabilities` advertises `canvas.atlas = {named, persist, maxSheets, maxBytes,
maxSheetBytes}` for feature detection. Tip: put a **content fingerprint in the name**
(`dash-a1b2c3`) and "name is in the list" means "exactly these tiles are already loaded" — no
re-upload needed. Files-tab uploads route `.mpta` to `/atlas/` automatically.

### `PUT /api/canvas/font` — uploadable fonts

The wall's bundled faces are fixed at build time; you can bring your own. The gateway's
`tools/fontpack.py` packs any **BDF face up to 16 px wide** into an `MPFT` blob — header
`"MPFT" ver=1 width height ascent`, then the **216 printable CP1252 glyphs** as big-endian
uint16 rows — and `PUT /api/canvas/font` installs it (≤ 64 KB) as the face named **`custom`**.
Reply `{ok, font: "custom", w, h, ascent}`.

The custom slot gets the same library treatment as animations, on the same naming rule
(1–24 chars of `a-z 0-9 - _`):

| Call | Does |
|---|---|
| `POST /api/canvas/font/save` `{"name":"x"}` | Persist the loaded face to `/fonts/<name>.fnt`. `409` when none is loaded. |
| `POST /api/canvas/font/delete` `{"name":"x"}` | Remove it (`404` unknown). |
| `GET /api/canvas/fonts` | The library: `[{name, bytes, w, h, ascent}, …]`. |

A face is then used **by name** — in the ticker's `font` field or the ops `text` op — where
`custom` means the slot as-is and a library name loads its file first. Unknown names always
fall back to the built-in face rather than erroring.

### `POST /api/canvas/effect` — on-device effects

`{"type": "<name>", "speed": 1-10, "hue"?: 0-255, "density"?: 1-100, "audio"?: bool}`. The effect
is animated by the panel **itself** at its native rate with nothing on the network — pushing frames
over HTTP sustains ~40 fps;
an on-device effect is limited only by the panel. `"type":"none"` releases. Refused
with `409` during Quiet Time. Reply `{ok, effect, speed, hue, density, audio}`. `"audio": true` makes `fire`/`matrix`/`plasma` follow the board's **dual
microphones** — loudness drives intensity/tempo, beats add sparks/bursts/lurches. Only offered
when capabilities carry the `audio` feature token (the ES7210 mic ADC answered at boot). Sound
is reduced to a few numbers on-device (`GET /api/canvas/audio` shows them); nothing is recorded.

| Effect | What it is | `hue` | `density` |
|---|---|---|---|
| `plasma` | Classic rolling plasma field | tints the palette | — |
| `fire` | Doom-style fire from the bottom row | — | — |
| `matrix` | Falling "digital rain" | recolours the rain (default green) | — |
| `fliporama` | The whole board flips through random glyphs | — | churn rate |
| `clock` | Big Orbitron `HH:MM` + date + a seconds bar | — | — |
| `life` | Conway's Game of Life, cells coloured by age | tints the cells | seed % |
| `spectrum` *(3.5)* | 16-band microphone spectrum analyzer, falling peak caps | rotates the bass→treble gradient | — |
| `soundwall` *(3.5)* | The **flap wall itself** reacts: beats flip loudness-scaled splashes of cells to colour flaps picked by the dominant frequency; quiet settles it home. Genuine wall mode — the dashboard preview follows. | — | — |
| `scope` | Oscilloscope — the live microphone waveform traced across the panel | `speed`, `hue` |
| `spectro` | Spectrogram — a scrolling frequency-vs-time waterfall, newest column on the right, 16 log bands through the fire palette | `speed`, `hue` |
| `ripple` *(3.5)* | Beat-launched expanding rings, coloured by the dominant frequency band, loudness-scaled, fading with radius; a centre glow breathes with the room | rotates the band palette | — |
| `maze` *(3.5)* | Hunt-and-Kill maze generation watched live: 2 px corridors in a rainbow tracing carve order, animated dead-end-filling solve, golden solution path, repeat. Speed spans one-carve-per-4-frames to ~49/frame | rotates the rainbow | — |

`hue` is `0–255` around the colour wheel; `density` is `1–100`. **Omit a parameter and the effect
keeps its own default.** A wall advertises
which effects it honours in `effects`, and each effect's parameters in `effectDefs`.

## Streaming animations from the microSD card

`POST /api/canvas/anim/play {"path":"/movies/x.mpg"}` plays an MPGA file straight from the
card: one frame is resident at a time, so there is **no size cap** — minutes-long clips are
fine. Same 14-byte MPGA header as uploads; geometry must match the panel; loop honoured from
the header. `{"name":…}` still plays from the FATFS library.

## Panel bit depth and the `panel` object

By default the framebuffer lives in the ESP32-S3's internal SRAM, and a large panel at a high bit
depth can run that internal RAM out. Rather than refuse and go dark, the
driver **auto-clamps the bit depth down** to the deepest that fits — a **256×64** panel lands on
**depth 3** — and `GET /api/status` reports the **actual running depth** in its `panel` object:

```json
"panel": { "ok": true, "w": 256, "h": 64, "depth": 3, "fbPsram": false, "refreshHz": 86, "cols": 32, "rows": 5, "font": "8x10", "vmods": 160 }
```

**Framebuffer in PSRAM (experimental).** Settings → LED Panel → **Framebuffer in PSRAM**
moves the framebuffer into the board's octal PSRAM, lifting that internal-RAM cap so a 256×64 panel
runs **depth 4** (16 levels/channel — smoother gradients). The pixel clock rises to 10 MHz to keep
depth 4 at ~80 Hz. `panel.fbPsram` becomes `true` and `panel.depth` reads `4`. Reboot to apply; off
by default (older worries that the PSRAM/DMA bus would starve WiFi didn't materialise on this octal
board — a per-frame cache flush keeps it coherent and WiFi is unaffected).

## A note on memory: the 507 guard

A big panel (256×64) runs canvas uploads close to the firmware's reboot floor. The **large** ops —
`PUT /api/canvas/anim`, `PUT /api/canvas/qoi`, `GET /api/canvas/frame` (readback),
`PUT /api/canvas/atlas` and `PUT /api/canvas/gif`, and `PUT /api/canvas/rects` +
opening `PUT /api/canvas/stream` — therefore check free memory first and
answer **`507`** ("try again in a moment") when it is already low, rather than risk a reboot. A
client should treat `507` as *retry shortly*, not a hard failure. The companion-critical
raw-frame path (`PUT /api/canvas/frame`) is left ungated so a continuous stream is never
interrupted. (The stores themselves — animation frames, staged transition frames, the atlas, the
font table — all live in the board's 16 MB PSRAM, not the internal RAM this guard protects.)

## Text encoding

The ops `text` op and the ticker accept **UTF-8** and transcode it to the panel font's CP1252
repertoire on the gateway — `°`, accents, umlauts, `ß`, the CP1252 punctuation (em-dash, curly
quotes) all render; anything outside the repertoire draws as `?` rather than failing. Centre/
right alignment counts characters, not bytes. ---
**See also:** [Matrix Gateway](Matrix-Gateway.md) · [Gateway API](Gateway-API.md) · [Built-in Apps](Built-in-Apps.md) · [Writing Apps](Writing-Apps.md)

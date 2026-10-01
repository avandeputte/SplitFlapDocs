# Canvas Ops Reference

Every drawing op the Matrix Gateway's `POST /api/canvas/ops` accepts, in detail. This is
the companion page to **[Canvas API](Canvas.md)** (the endpoint-level view) and
**[Writing Matrix Apps](Writing-Matrix-Apps.md)** (the app author's view — the `canvas.*`
helpers there emit exactly these ops).

An ops request is a JSON **array** of op objects, applied **in order**, then presented:

```json
[ {"op":"clear","color":[0,0,40]},
  {"op":"arc","x":64,"y":16,"r":14,"t":3,"start":0,"end":270,"color":[0,200,120]},
  {"op":"text","x":64,"y":11,"s":"75%","align":"center"} ]
```

The same array, byte for byte, rides the **stream channel**'s ops record
(`PUT /api/canvas/stream`, type `0x03`) — everything below applies there too.

## Conventions (read once)

- **Coordinates**: pixels, origin top-left, `x` right / `y` down. Everything is clipped
  to the panel (and to the [`clip`](#clip-clip-window) window when one is set) —
  off-panel drawing is dropped, never an error.
- **Colours**: `"color": [r, g, b]` (0–255 each). Omitted, it defaults to **white** for
  drawing ops and **black** for `clear`/`scroll` vacancy. The panel quantises to its
  running bit depth.
- **Batching**: ops draw into the back buffer; nothing appears until a present. The
  batch **auto-presents when it ends** unless it contained an explicit `show` — include
  `{"op":"show"}` mid-batch only when you want an intermediate present. (On the stream
  channel there is **no** auto-present: send `show` ops or a `0x05` record.)
- **Batch-scoped state**: [`origin`](#origin-translate),
  [`clip`](#clip-clip-window), the [transform stack](#transform-stack),
  [macro](#ops-macros) definitions, and any open [layer](#offscreen-layers)
  affect only the *same* batch and reset between batches.
  [`atlas`](#atlas-bind-a-sprite-sheet) binding is **sticky** across batches by design.
- **Unknown ops and params are ignored** (the op is skipped / the param unread, never a
  400) — old and new clients interoperate with old and new firmware in any combination.
  `GET /api/capabilities` → `canvas.ops` is the authoritative list of what the wall
  you're talking to understands.
- **The reply** is `{"ok":true,"applied":N}` — `applied` counts ops that did something
  (unknown ops and out-of-range sprites don't count). It answers **before** the present,
  so the ~14 ms present overlaps your next frame's build.

---

## Fills & pixels

### `clear` — fill the panel

```json
{"op":"clear","color":[0,0,0]}
```

| param | type | default | |
|---|---|---|---|
| `color` | `[r,g,b]` | black | fill colour |

Fills the whole panel (a fast whole-buffer fill, ~5 ms on 256×64). Almost every frame
starts here. Ignores `origin`; respects `clip`.

### `pixel` — one pixel

```json
{"op":"pixel","x":10,"y":4,"color":[255,0,0]}
```

| param | type | default |
|---|---|---|
| `x`, `y` | int | 0 |
| `color` | `[r,g,b]` | white |

### `hline` / `vline` — axis-aligned runs

```json
{"op":"hline","x":0,"y":31,"w":128,"color":[80,80,80]}
{"op":"vline","x":64,"y":0,"h":32}
```

| param | type | default | |
|---|---|---|---|
| `x`, `y` | int | 0 | start |
| `w` (hline) / `h` (vline) | int | 0 | run length |
| `color` | `[r,g,b]` | white | |

For a thick rule use `rect` with `fill:true` — it's one fast fill.

---

## Lines & outlines

### `line` — any-angle line **

```json
{"op":"line","x":0,"y":0,"x1":127,"y1":31,"t":3,"color":[255,200,0]}
```

| param | type | default | |
|---|---|---|---|
| `x`, `y` | int | 0 | one end |
| `x1`, `y1` | int | 0 | other end |
| `t` | int | 1 | stroke thickness |
| `color` | `[r,g,b]` | white | |

Bresenham at `t:1`; thicker strokes sweep a `t`×`t` square brush along the line, which
reads as a solid stroke at panel resolutions.

### `polyline` — connected open line **

```json
{"op":"polyline","points":[[0,30],[20,10],[40,25],[60,5]],"t":2,"color":[0,255,255]}
```

| param | type | default | |
|---|---|---|---|
| `points` | `[[x,y],…]` | — | vertices, drawn in order, **not** closed |
| `t` | int | 1 | stroke thickness |
| `color` | `[r,g,b]` | white | |

The graphing primitive. For a closed shape use [`poly`](#poly-closed-polygon).

---

## Shapes

All shape ops share: `color` (default white), `fill` (default `false` — outline).
Outlines take `t` thickness where noted.

### `rect` — rectangle

```json
{"op":"rect","x":4,"y":4,"w":40,"h":24,"t":2,"color":[255,255,255]}
{"op":"rect","x":4,"y":4,"w":40,"h":24,"fill":true}
```

| param | type | default |
|---|---|---|
| `x`, `y`, `w`, `h` | int | 0 |
| `fill` | bool | false |
| `t` | int | 1 (outline only) |

A `t`-thick outline is four filled bars, drawn *inside* the `w`×`h` box.

### `roundrect` — rounded rectangle

```json
{"op":"roundrect","x":2,"y":2,"w":60,"h":28,"r":6,"fill":true,"color":[30,30,60]}
```

| param | type | default | |
|---|---|---|---|
| `x`, `y`, `w`, `h` | int | 0 | box |
| `r` | int | 0 | corner radius |
| `fill` | bool | false | |

The card/badge primitive. (Outline is 1 px; for a thick rounded frame draw two filled
roundrects, inner in the background colour.)

### `circle` — circle

```json
{"op":"circle","x":16,"y":16,"r":10,"t":3,"color":[255,0,128]}
```

| param | type | default | |
|---|---|---|---|
| `x`, `y` | int | 0 | centre |
| `r` | int | 0 | radius |
| `fill` | bool | false | disc |
| `t` | int | 1 | ring thickness (outline; renders a true annulus) |

### `ellipse` — ellipse

```json
{"op":"ellipse","x":64,"y":16,"rx":30,"ry":12,"fill":true,"color":[0,60,120]}
```

| param | type | default | |
|---|---|---|---|
| `x`, `y` | int | 0 | centre |
| `rx`, `ry` | int | 0 | semi-axes |
| `fill` | bool | false | |
| `t` | int | 1 | outline thickness (nested rings) |

### `triangle` — triangle

```json
{"op":"triangle","x":10,"y":28,"x1":30,"y1":4,"x2":50,"y2":28,"fill":true}
```

| param | type | default |
|---|---|---|
| `x`,`y`, `x1`,`y1`, `x2`,`y2` | int | 0 |
| `fill` | bool | false |
| `color` | `[r,g,b]` | white |

### `poly` — closed polygon

```json
{"op":"poly","points":[[10,2],[20,12],[16,26],[4,26],[0,12]],"color":[255,180,0]}
{"op":"poly","points":[[10,2],[20,12],[4,26]],"fill":false,"t":2}
```

| param | type | default | |
|---|---|---|---|
| `points` | `[[x,y],…]` | — | up to **16** vertices, closed automatically |
| `fill` | bool | **true** | even-odd scanline fill |
| `t` | int | 1 | outline thickness when `fill:false` |
| `color` | `[r,g,b]` | white | |

Even-odd fill means self-intersecting outlines (stars) render with holes, HTML-canvas
style. Beyond 16 vertices the extras are ignored.

### `arc` — arc, ring segment, pie slice

```json
{"op":"arc","x":64,"y":32,"r":20,"t":4,"start":0,"end":270,"color":[0,220,100]}
{"op":"arc","x":64,"y":32,"r":20,"start":120,"end":200,"fill":true}
```

| param | type | default | |
|---|---|---|---|
| `x`, `y` | int | 0 | centre |
| `r` | int | 0 | outer radius |
| `t` | int | 2 | ring thickness (ignored when `fill`) |
| `start`, `end` | int deg | 0, 360 | sweep, **0° = 12 o'clock, clockwise** |
| `fill` | bool | false | pie slice instead of ring segment |
| `color` | `[r,g,b]` | white | |

**The gauge primitive.** `start:0, end: value*360/max` is a progress ring;
`t:r` makes the ring a full disc segment. Sweeps may cross 0° (`start:300, end:420` or
equivalently `end:60`, which the firmware unwraps). A full `0→360` with `t` is exactly a
thick circle outline.

---

## Compositing

Every draw can composite over what's already in the back buffer instead of overwriting.
Two independent controls: **per-colour alpha** and a **batch blend mode**.

- **Alpha** — a colour may carry a 4th element: `"color":[r,g,b,a]`, `a` = 0 (transparent)
  … 255 (opaque). Applies to any op that takes a `color` (shapes, text, gradient, clear).
- **`blend`** — `{"op":"blend","mode":"over"|"add"|"multiply"|"screen"|"max"}` sets the
  mode for **subsequent** ops (batch-scoped, resets between batches). `over` is normal
  alpha; **`add`** is additive (the LED-glow mode — overlapping lights sum); `multiply`
  darkens; `screen` lightens; `max` keeps the brighter of source/destination.

```json
[ {"op":"clear","color":[0,0,40]},
  {"op":"rect","x":0,"y":0,"w":64,"h":32,"fill":true,"color":[0,0,200,128]},
  {"op":"blend","mode":"add"},
  {"op":"circle","x":40,"y":16,"r":14,"fill":true,"color":[80,0,0]},
  {"op":"circle","x":56,"y":16,"r":14,"fill":true,"color":[80,0,0]} ]
```

Compositing reads the current **back buffer**, so it layers over what the batch has
already drawn (start with a `clear` or a background). Advertised in capabilities as
`canvas.compositing` (`{alpha, blendModes[], aa, transform, layers, macros}`).

## Anti-aliased strokes

`"aa":true` on **`line`**, **`polyline`**, **`poly`** (outline) and **`circle`** (outline)
draws smooth edges (Xiaolin-Wu lines; coverage-blended circle ring) instead of hard
jaggies — coverage becomes alpha through the same compositing path, so it honours the
colour alpha and blend mode. AA is 1 px; thick strokes stay hard-edged. Especially worth
it on diagonals and curves.

## Stroke styling

`line`, `polyline` and `poly` (outline) take stroke-style params:

| param | type | | |
|---|---|---|---|
| `cap` | string | `butt` (default) / `round` / `square` | end shape of a thick line |
| `join` | string | `miter` (default) / `round` | corner fill at thick-polyline/poly vertices |
| `dash` | `[on, off]` | e.g. `[8,4]` | dashed stroke; the pattern flows continuously along a polyline/poly |

```json
{"op":"line","x":4,"y":16,"x1":124,"y1":16,"t":4,"cap":"round","color":[0,255,0]}
{"op":"line","x":4,"y":24,"x1":124,"y1":24,"t":2,"dash":[8,4],"color":[255,255,0]}
{"op":"polyline","points":[[4,8],[40,28],[80,8],[120,28]],"t":3,"join":"round","color":[0,200,255]}
```

Caps/joins apply to thick strokes (`t`>1). Dash and AA don't combine (AA wins).

## `bezier` — smooth curves

```json
{"op":"bezier","points":[[4,28],[64,2],[124,28]],"aa":true,"color":[255,200,0]}
{"op":"bezier","points":[[0,30],[20,0],[80,60],[120,10]],"t":2,"color":[0,200,255]}
```

| param | type | default | |
|---|---|---|---|
| `points` | `[[x,y],…]` | — | **3** points = quadratic, **4** = cubic |
| `aa` | bool | false | anti-aliased |
| `t` | int | 1 | stroke thickness (non-AA) |
| `color` | `[r,g,b(,a)]` | white | |

Flattened to line segments on-device (segment count scales with the curve's size). The
charting/gauge-needle primitive.

## Batch state

### `clip` — clip window

```json
{"op":"clip","x":10,"y":0,"w":50,"h":32}
{"op":"clip"}
```

| param | type | default | |
|---|---|---|---|
| `x`, `y`, `w`, `h` | int | 0 | window; `w`/`h` ≤ 0 (or the bare form) **clears** |

Every later op in the batch — including full `clear` fills, images, sprites and text —
draws only inside the window. Enforced in the firmware's pixel/fill/blit fast paths, so
there's no op that escapes it. Reset automatically when the batch ends.

### `origin` — translate

```json
{"op":"origin","x":40,"y":8}
{"op":"origin"}
```

| param | type | default | |
|---|---|---|---|
| `x`, `y` | int | 0 | added to every later coordinate; bare form resets |

Applies to all coordinate params, including `x1/y1/x2/y2` and `points` arrays. Absolute
(not cumulative): a second `origin` replaces the first. **The component pattern**: draw a
widget's ops with coordinates relative to (0,0), prefix them with `origin` (and usually
`clip`) to place as many copies as you like:

```json
[ {"op":"origin","x":0,"y":0},   {"op":"clip","x":0,"y":0,"w":64,"h":32},  …widget ops…,
  {"op":"origin","x":64,"y":0},  {"op":"clip","x":64,"y":0,"w":64,"h":32}, …same ops… ]
```

(Note `clip` coordinates are themselves origin-translated — set `origin` first with the
window in mind, or set `clip` before `origin` as above.)

---

## Transform stack

`origin` is a pure translate. The transform stack generalises it to full **affine**
transforms — translate, scale, and rotate, composable and stackable — advertised as
`canvas.compositing.transform`.

| op | params | effect |
|---|---|---|
| `translate` | `x`, `y` | shift the coordinate frame |
| `scale` | `x`, `y` (`y` defaults to `x`) | scale about the current origin |
| `rotate` | `deg` | rotate the frame clockwise, in degrees |
| `save` | — | push the current transform (stack depth 8) |
| `restore` | — | pop back to the last `save` |

```json
[ {"op":"clear"},
  {"op":"translate","x":64,"y":16},
  {"op":"rotate","deg":30},
  {"op":"line","x":0,"y":0,"x1":40,"y1":0,"color":[0,220,255]},
  {"op":"save"},
    {"op":"scale","x":2},
    {"op":"text","x":0,"y":4,"s":"2x","color":[255,220,0]},
  {"op":"restore"} ]
```

**What rotates and what doesn't.** Point/line ops transform *every vertex*, so they rotate
fully: `line`, `polyline`, `poly`, `triangle`, `bezier`, `pixel`. Box-anchored fills —
`rect`, `circle`, `ellipse`, `roundrect`, `arc` — transform their **anchor** and **scale**
their size, but stay axis-aligned under rotation (a rotated `rect` moves but does not tilt).
To draw a rotated bitmap, use a `sprite` with its own `rot:90|180|270`.

`origin` remains, and now means "reset the transform to this pure translation" — fully
backward-compatible with older batches. The whole stack is **batch-scoped**: it resets to
identity when the batch ends.

## Offscreen layers

Draw a group of ops into an isolated buffer, then blend the *whole group* back with one
opacity or blend mode — **group opacity**, which per-op alpha can't express (you can fade
a fully-composed scene as a single unit). Advertised as `canvas.compositing.layers`.

| op | params | effect |
|---|---|---|
| `layer` | — | begin: subsequent draws go to an offscreen shadow, not the canvas |
| `composite` | `x`, `y`, `mode`, `alpha` | blend the layer back at `(x,y)` and close it |

`mode` is the same set as [`blend`](#compositing) (`over`/`add`/`multiply`/`screen`/`max`,
default `over`); `alpha` is 0–255 (default 255).

```json
[ {"op":"clear"},
  {"op":"rect","x":0,"y":0,"w":40,"h":40,"fill":true,"color":[200,40,0]},
  {"op":"layer"},
    {"op":"circle","x":30,"y":20,"r":16,"fill":true,"color":[0,80,255]},
    {"op":"circle","x":45,"y":24,"r":16,"fill":true,"color":[0,80,255]},
  {"op":"composite","alpha":128} ]
```

The two circles blend as a unit at 50 % over the red — overlaps inside the group don't
double up. One layer open at a time; the shadow buffer lives in PSRAM only between `layer`
and `composite`, and an unclosed layer is discarded when the batch ends.

## Ops macros

Register a reusable op sequence once, then stamp it anywhere — without re-sending its ops.
Advertised as `canvas.compositing.macros`.

| op | params | effect |
|---|---|---|
| `define` | `name`, `ops` | register the op array under a name (≤12 macros/batch) |
| `call` | `name`, `x`, `y` | replay the macro under a transform translated by `(x,y)` |

```json
[ {"op":"clear"},
  {"op":"define","name":"pip","ops":[
    {"op":"circle","x":0,"y":0,"r":3,"fill":true,"color":[0,255,120]},
    {"op":"text","x":-3,"y":6,"s":"·","color":[0,120,60]} ]},
  {"op":"call","name":"pip","x":20,"y":16},
  {"op":"call","name":"pip","x":64,"y":16},
  {"op":"call","name":"pip","x":108,"y":16} ]
```

Each `call` pushes the transform, translates by `(x,y)`, replays the macro, then pops — so
a macro drawn around `(0,0)` lands wherever you call it, and it inherits any transform in
effect at the call site (scale/rotate a macro by wrapping the `call`). Macros may call other
macros, nested to depth 4. Definitions are **batch-scoped**.

---

## Text

### `text` — one line

```json
{"op":"text","x":64,"y":2,"s":"21° café","align":"center","size":13,"color":[255,220,0]}
{"op":"text","x":64,"y":2,"s":"BIG","aa":true,"size":34,"align":"center"}
{"op":"text","x":2,"y":2,"s":"Score","outline":[0,0,0]}
```

| param | type | default | |
|---|---|---|---|
| `x`, `y` | int | 0 | anchor; `y` is the glyph **top** |
| `s` | string | "" | UTF-8; transcoded to CP1252 on device (`°`, `é`, `ß` … all fine) |
| `size` | int | 10 | bitmap faces: 8, 9, 10, 13, 18, 20 px (nearest wins) |
| `font` | string | — | an uploaded font by name (`PUT /api/canvas/font`); unknown names keep the built-in face |
| `align` | string | left | `left` \| `center` \| `right`, about `x` |
| `aa` | bool | false | anti-aliased Orbitron instead of the bitmap face — `size` ≥ 30 → 34 px, ≥ 18 → 24 px, else 13 px; charset A–Z 0–9 `:.-+%/` (input folded to uppercase, other glyphs skipped) |
| `outline` | `[r,g,b]` | — | 1 px ring under the text (bitmap path) |
| `shadow` | `[r,g,b]` | — | +1,+1 drop shadow (bitmap path; `outline` wins if both) |
| `color` | `[r,g,b]` | white | |

Bitmap glyphs draw **transparent** (background shows between strokes) — text over
gradients/images works directly. The AA path is the one for big numerals: clocks,
temperatures, scores.

### `textbox` — wrapped, aligned text in a box

```json
{"op":"textbox","x":4,"y":4,"w":120,"h":24,"s":"Multi-line text wraps by word and stays inside the box","size":8,"align":"center","valign":"middle"}
```

| param | type | default | |
|---|---|---|---|
| `x`, `y`, `w`, `h` | int | 0 | the box |
| `s` | string | "" | UTF-8; explicit `\n` forces a line break |
| `size` / `font` | | 10 / — | as `text` (bitmap faces only) |
| `align` | string | left | per-line: `left` \| `center` \| `right` |
| `valign` | string | top | block: `top` \| `middle` \| `bottom` |
| `color` | `[r,g,b]` | white | |

Greedy word-wrap; a word longer than the box hard-breaks; everything is clipped to the
box (up to 10 lines). The message-card primitive.

---

## Images & sprites

### `image` — inline bitmap

```json
{"op":"image","x":8,"y":8,"w":16,"h":16,"fmt":"rgb565","data":"<base64>"}
```

| param | type | default | |
|---|---|---|---|
| `x`, `y` | int | 0 | top-left |
| `w`, `h` | int | 0 | pixel dimensions of the data |
| `fmt` | string | rgb888 | `rgb888` \| `rgb565` (big-endian) |
| `data` | string | — | base64 of `w*h*bpp` bytes |

One-off small graphics. For anything reused, upload a sprite sheet once
([Atlas](Canvas.md#put-apicanvasatlasname-a-named-sprite-tile-sheet)) and `sprite`
it — base64-in-JSON is ~33 % bigger and re-sent every time.

### `atlas` — bind a sprite sheet

```json
{"op":"atlas","name":"weather"}
```

Binds the named sheet for subsequent `sprite` ops. **Sticky across batches** (rebind
per batch if you use content-fingerprint names). Lazy-loads a persisted sheet from
flash on first bind; an unknown name binds nothing and later sprites no-op.

### `sprite` — blit an atlas tile

```json
{"op":"sprite","i":4,"x":10,"y":6}
{"op":"sprite","i":4,"x":10,"y":6,"flip":"h","rot":90,"scale":2}
```

| param | type | default | |
|---|---|---|---|
| `i` | int | — | tile index in the bound sheet |
| `x`, `y` | int | 0 | destination top-left |
| `flip` | string | — | `h` \| `v` \| `hv` — applied **first**, in tile space |
| `rot` | int | 0 | `90` \| `180` \| `270`, clockwise, after the flip |
| `scale` | int | 1 | 1–4, integer pixel scaling |

Magenta (`255,0,255` / `0xF81F`) is transparent. With transforms, one sheet serves
every orientation — a game ships one spaceship, not eight. Rotation pivots the tile
about its own top-left destination box (a 90°-rotated `w`×`h` tile occupies `h`×`w`).

---

## Motion & present

### `gradient` — linear gradient fill

```json
{"op":"gradient","x":0,"y":0,"w":128,"h":32,"from":[10,16,44],"to":[3,5,16],"dir":"v"}
```

| param | type | default | |
|---|---|---|---|
| `x`, `y`, `w`, `h` | int | 0 | box |
| `from`, `to` | `[r,g,b]` | — | end colours |
| `dir` | string | v | `v` \| `h` \| `r` radial, centre→corners |
| `angle` | int deg | — | any-angle linear gradient (0 = left→right, 90 = top→down); implies `dir:"a"` |
| `dither` | bool | **true** | ordered (Bayer 4×4) dithering — banding at panel bit depths breaks into a fine blend; `false` restores hard bands |

The backdrop primitive (skies, cards). Binary encoding: the `dir` byte accepts `2` =
radial (always dithered).

### `scroll` — shift the frame

```json
{"op":"scroll","dx":-1,"dy":0,"color":[0,0,0]}
```

| param | type | default | |
|---|---|---|---|
| `dx`, `dy` | int | 0 | shift, pixels (negative = left/up) |
| `color` | `[r,g,b]` | black | fill for the vacated strip |

Shift the whole back buffer and repaint only the fresh edge — the cheap way to pan or
tick a chart along.

### `show` — present

```json
{"op":"show"}
```

Presents the back buffer (double-buffered; the firmware's tear-guard paces the swap).
A batch **without** any `show` auto-presents at the end — reach for explicit `show`
only for multi-present batches or on the stream channel (which never auto-presents).

---

## Where ops fit among the other canvas paths

| you want | use |
|---|---|
| shapes, gauges, text, sprites | **ops** (this page) |
| photographic / Pillow-rendered frames | `PUT /api/canvas/frame` (or QOI) |
| small changed regions of a frame | `PUT /api/canvas/rects` deltas |
| animation-rate updates, no per-frame HTTP | the **stream channel** (ops record `0x03` carries this page's ops) |
| panel-side animation with zero network | **effects** (`POST /api/canvas/effect`) |
| scrolling text | the **ticker** |

## Binary encoding

For game-rate clients the ops surface also exists in a **fixed-layout binary encoding**
(`canvas.opsBin` capability): ~6× smaller and 1.5–1.9× the frame rate on
op-heavy scenes, because the wall skips JSON parsing entirely. Carried by
`POST /api/canvas/opsb` or — the intended path — **stream record `0x06`**. All
integers big-endian, coordinates **signed** int16 (draw off-panel freely). One op =
`u8 opcode` + fixed fields:

| opcode | op | fields after the opcode |
|---|---|---|
| `0x01` | clear | `rgb(3)` |
| `0x02` | pixel | `x y rgb` |
| `0x03`/`0x04` | hline / vline | `x y len(2) rgb` |
| `0x05` | line | `x y x1 y1 t(1) rgb` |
| `0x06` | rect | `x y w h flags(1: bit0 fill) t(1) rgb` |
| `0x07` | circle | `x y r(2) flags t rgb` |
| `0x08` | ellipse | `x y rx ry flags t rgb` |
| `0x09` | triangle | `x y x1 y1 x2 y2 flags rgb` |
| `0x0A` | roundrect | `x y w h r(2) flags rgb` |
| `0x0B` | gradient | `x y w h from(3) to(3) dir(1: 0 v, 1 h)` |
| `0x0C` | arc | `x y r(2) t(1) start(2) end(2) flags(bit0 pie) rgb` |
| `0x0D` | poly | `n(1) flags(bit0 fill, bit1 closed) t(1) rgb` then `n × (x y)` |
| `0x0E` | clip | `x y w h` (`w ≤ 0` clears) |
| `0x0F` | origin | `x y` |
| `0x10` | text | `x y size(1) flags(1) rgb [outline rgb] [shadow rgb] len(1) utf8` — flags: bits 0-1 align (0 L / 1 C / 2 R), bit 2 aa, bit 3 has-outline, bit 4 has-shadow |
| `0x11` | sprite | `i(2) x y flags(1)` — bit 0 flipH, bit 1 flipV, bits 2-3 rot/90°, bits 4-5 scale−1 |
| `0x12` | scroll | `dx dy rgb` |
| `0x13` | show | — |
| `0x14` | blend | `mode(1)`: 0 over, 1 add, 2 multiply, 3 screen, 4 max (batch-scoped) |
| `0x15` | alpha | `alpha(1)`: 0–255, applied to following ops (batch-scoped) |

### Transform, layers, macros, bezier, AA

Every coordinate runs through the **same affine transform** as JSON ops (`origin` is a
matrix reset + pure translate):

| opcode | op | fields after the opcode |
|---|---|---|
| `0x16` | save | — (push the transform, depth 8) |
| `0x17` | restore | — (pop) |
| `0x18` | translate | `x y` (s16 pixels) |
| `0x19` | scale | `sx sy` (u16 **8.8 fixed-point**: 256 = 1.0, 512 = 2.0; `sy` 0 = uniform) |
| `0x1A` | rotate | `deg` (s16 degrees, clockwise) |
| `0x1B` | layer | — (begin an offscreen group) |
| `0x1C` | composite | `x y mode(1) alpha(1)` (blend the group back; group opacity) |
| `0x1D` | define | `id(1: 0–7) len(2)` then `len` bytes of **embedded binary ops** |
| `0x1E` | call | `id(1) x y` — scoped replay under a pushed translate, nestable to depth 4 |
| `0x1F` | bezier | `n(1: 3\|4) t(1) flags(1: bit0 aa) rgb` then `n × (x y)` |
| `0x20` | aaline | `x y x1 y1 rgb` (1 px anti-aliased) |

Additive flag bits: **circle** `flags` bit 1 = aa outline; **poly** `flags` bit 2 = aa
outline/polyline. The same point-vs-box transform rule as JSON applies: vertex ops
(line, poly, triangle, bezier, pixel) rotate fully; box-anchored fills transform the
anchor and scale their size but stay axis-aligned.

The JSON-only remainder is deliberate: `textbox`, `image`, dash/cap stroke styling and
gradient angle mode are layout ops, not game-rate ops — use the JSON path for those.

**Strict decode**: an unknown opcode or truncated op fails the whole batch (binary
cannot skip what it cannot size) — Semantics are identical to the JSON ops
above, verified pixel-for-pixel on device.

Full endpoint semantics: **[Canvas API](Canvas.md)**. Machine-readable: the device's own
`GET /openapi.yaml`.

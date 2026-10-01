# Writing Matrix Apps

Drawing on a **Matrix Gateway**'s LED panel from a companion app: surfaces,
`fetch_matrix`, the `canvas` drawing object, whole-panel shortcuts, Pillow rendering,
redraw pacing, dual-surface apps, and channels on the panel. Split out of
**[Writing Apps](Writing-Apps.md)** (whose §1–6 cover the flap-side model this page builds
on); the underlying wire ops are documented one by one in the
**[Canvas Ops Reference](Canvas-Ops-Reference.md)**.

Everything so far returns **pages** — strings laid across a grid of flaps. A **Matrix
Gateway** (whose modules are drawn, not mechanical — see [Matrix Gateway](Matrix-Gateway.md)) can
do something a flap wall physically cannot: hand you its LED panel as a plain framebuffer and
let you draw **anything** on it, pixel by pixel, free of the module grid.

An app declares which displays it renders on with the manifest's **`surfaces`** array, and
provides a matching **entry point** for each:

| `surfaces` | renders with | example |
|---|---|---|
| `["flap"]` *(default)* | `fetch()` → pages | every app in §1–6 |
| `["matrix"]` | `fetch_matrix()` → draws | Lumina Clock, Photo Frame, Image |
| `["flap", "matrix"]` | **both** | Countdown, World Clock, Public Holidays (§ Dual-surface) |

A **matrix app** (surface `"matrix"`) draws instead of returning pages:

```json
{ "name": "Lumina Clock", "icon": "🕰️", "type": "functional",
  "surfaces": ["matrix"], "refresh_interval": 1, "loop_delay": 1,
  "category": "time" }
```

For a matrix surface the engine runs the app differently: instead of fetching pages and rotating
them, it **takes the panel over** from the reel wall, runs your `fetch_matrix()` on a timer to draw a
frame, and **hands the panel back** the moment you switch to another app — so the wall returns
to its flaps with nothing left stranded on the LEDs.

## `fetch_matrix` and the `canvas` surface

`fetch_matrix(settings, canvas, **helpers)` gets the drawing **`canvas`** as its second argument
(always a real surface — it's only called on a Matrix panel), then the same injected helpers as
`fetch` by name (`i18n`, `caps`, `get_weather`, …):

```python
def fetch_matrix(settings, canvas):
    canvas.clear()                          # start from black
    canvas.rect(0, 0, canvas.width, canvas.height, color=(0, 40, 80), fill=True)
    canvas.text(4, 2, "HELLO", color="yellow", size=13)
    canvas.show()                           # nothing is sent until this line
    return 5                                # hold this frame 5s, then redraw
```

**Interactive games** opt into two more injected helpers and one manifest flag:

- **`controls`** — live player input from the web UI. Read it once per frame: `controls.dir`
  is the held direction (`"up"`/`"down"`/`"left"`/`"right"`, or `None`), `controls.events`
  the presses since the last frame (`"start"`/`"pause"`/`"coin"`, drained), and
  `controls.active()` whether a human is engaged — run an attract-mode demo when it's False
  and hand over when it's True. Inputs arrive via `POST /api/game/input`; the app never waits
  on them.
- **`play_sound(notes=[[freq,ms],…])`** (or `freq=`, `ms=`) — a tone on the gateway speaker
  , fire-and-forget so it never stalls a frame; a no-op where the wall has no
  speaker.
- Set **`"interactive": true`** in the manifest so the web UI shows its control pad while the
  app runs.
- Interactive games ship an **Auto-play after (s)** setting (`takeover`): the seconds of pad
  silence before the game drifts back to attract-mode self-play. Sound follows a house rule:
  `play_sound` only while a human is engaged (`controls.active()`), **never in attract mode** —
  a playlist wall stays silent.
- Besides `dir` and `events`, `controls.taps` is the discrete direction presses since the last
  frame (drained, in order — per-press moves like a rotate read these), and `controls.presses`
  a press-edge counter for "press any key to resume" gates (a held key never advances it).

For the lowest input-to-pixel latency, draw with the ops surface (`canvas.show()` streams
binary ops) and return a short hold. See the **Chomper** app for a worked
example.

You draw in **pixels**, on the real panel — `canvas.width` × `canvas.height` LEDs, not the
`rows × cols` flap grid. The drawing calls are:

| call | draws |
|---|---|
| `canvas.clear(color=(0,0,0))` | fill the whole panel (black by default) |
| `canvas.pixel(x, y, color)` | one pixel |
| `canvas.hline(x, y, w, color)` / `canvas.vline(x, y, h, color)` | a horizontal / vertical run |
| `canvas.rect(x, y, w, h, color, fill=False)` | an outlined or filled rectangle |
| `canvas.text(x, y, s, color, size=10)` | a string in the panel's built-in font (sizes `8, 9, 10, 13, 18, 20`) |
| `canvas.show()` | **send the batch and present it** |

Those are the staples; the wall's op set is considerably larger — lines/polylines,
circles/ellipses/triangles, rounded rects, **arcs and pie slices** (gauges), **filled
polygons**, gradients, a **clip window** and **coordinate origin** (build placeable
components), **word-wrapped textboxes**, **anti-aliased Orbitron type**, outline/shadow
text styles, **sprite blits with flip/rotate/scale**, and frame scrolling (thickness on
every outline). The helper exposes what it wraps and passes unknown params
straight through, so newer wall features work by name the day the wall advertises them —
`GET /api/capabilities` → `canvas.ops` is the wall's authoritative list — in an app,
gate with `canvas.has_op("arc")`. (`canvas.shadow_text(…)` collapses to a single styled
text op automatically — ops apps get that for free.) **Every op,
with every parameter and defaults, is documented in the
[Canvas Ops Reference](Canvas-Ops-Reference.md).**

**Colors** are written three ways, whichever reads best: a **name** (`"red"`, `"cyan"`,
`"orange"` — the same palette as the wall's color flaps), an **`(r, g, b)`** triple (0–255),
or a **`"#RRGGBB"`** string. Anything unrecognised falls back to white.

**Compositing** (gate on `canvas.can_composite` — every Matrix wall has it; the gate
exists for bare hosts): pass a **four-component
color** `[r, g, b, a]` to any drawing op for per-pixel alpha; `canvas.blend("add")` sets an
additive blend for the ops that follow (the LED-glow mode where overlapping lights sum —
reset with `canvas.blend("over")`); and `aa=True` on `line`/`polyline`/`poly`/`circle`
draws anti-aliased. Older walls ignore all of it and draw plainly, so gate the *look* on
`canvas.can_composite` but never worry about breakage. Batch blend AND per-color
alpha both ride the binary stream (alpha becomes the batch-alpha opcode under the
hood); `aa=True` rides the binary
stream natively — gate on `canvas.aa_ok` (compositing presence) and never worry about
the frame rate. Atlas binds travel over the draw stream too — a
sprite + compositing app like the **Aquarium** (godrays, glowing bubbles) streams
whole frames at game rate.

**Capability flags at a glance.** `canvas.can_qoi/can_rect/can_rects/can_stream/can_anim/can_ticker/can_ops_bin/can_composite/can_sd/can_sd_anim/can_readback/can_sprite/can_text_styles` and `canvas.aa_ok` — each mirrors what this wall advertises; gate a flourish on the flag and the app degrades cleanly on a bare host.

**Reading settings.** Settings reach `fetch_matrix` as raw strings (`""` when unset).
Use `canvas.num(settings, key, default, lo, hi)` — blank/junk degrade to the default,
bounds clamp, and the result is an int when the default is an int (a float otherwise):
`speed = canvas.num(settings, 'speed', 5, 1, 10)`. (The flap-side `fetch()` keeps the
hand-rolled `try/int(float(...))` clamp — it has no canvas and its signature is the
portable upstream ABI.)

**The microSD card** (gate on `canvas.can_sd`): `canvas.sd_list(path)`
returns one directory level as `[{name, dir, size}, ...]` and `canvas.sd_get(path)` a
file's raw bytes — both read-only, both answering empty/None without a card. The
**Photo Frame** app is the worked example: it slideshows the card's images with
`sd_list` + `sd_get` + `canvas.frame()`. Streaming FROM the card:
`canvas.play_anim_path("/movies/x.mpg")` (gate on `canvas.can_sd_anim`) plays an MPGA
with no length cap — the wall reads it one frame at a time — and
`play_sound(wav="/sounds/chime.wav")` streams a 16-bit 16 kHz PCM WAV through the
speaker instead of synth tones.

**Transforms, layers and macros** (binary + JSON alike):
`canvas.save()/restore()/translate()/scale()/rotate()` run the ops that follow under an
affine transform; `canvas.layer()` + `canvas.composite(x, y, mode, alpha)` group draws
offscreen and flatten them with one blend; `with canvas.define("star"): …` captures a
reusable op sequence `canvas.call("star", x, y)` replays; `canvas.bezier(points, color,
t, aa)` strokes a quadratic/cubic curve. Gate on `has_op("save")` on a bare host; on a real wall they simply work, binary included.

**Binary ops are automatic.** On a wall that advertises `canvas.opsBin`, the
helper encodes each batch into the fixed-layout binary form (`POST /api/canvas/opsb`) —
~6–7× fewer bytes and no JSON parse on the panel — falling back to JSON whenever a batch
carries something only JSON can (a textbox, an atlas bind, a custom font). A fast
binary-ops app (short holds) is also adopted onto the **draw stream** automatically —
its batches ride record `0x06` with no per-frame HTTP round trip, the same way
frame-push apps stream. Apps change nothing; output is pixel-identical either way.

**Draws are batched until `show()`.** `clear`, `pixel`, `rect`, `text` and the rest don't
touch the panel one at a time — they accumulate, and nothing appears until `show()`, which
posts the whole frame in a single request and presents it. So build the entire frame, *then*
call `show()` once. (Under the hood that one call is `POST /api/canvas/ops`; you never write
the HTTP yourself.)

## Two whole-panel shortcuts

Some content isn't worth plotting pixel by pixel. Two helpers stand apart — each is its own
operation and sends **immediately**, without waiting for `show()`:

- **`canvas.effect(name, speed=5, hue=None, density=None, params=None)`** — start an
  **on-device effect**. The panel renders it *itself*, at its native frame rate, with nothing
  more on the network — the companion names it once and stops. The names live in
  `canvas.effects`, whichever the wall advertises. The wall *describes*
  each effect (`canvas.effect_defs`: per effect, exactly the params it consumes with types and
  ranges) — pass those as `params={...}` and exactly they go on the wire. Without `params`,
  optional `hue` (0–255) and `density` (1–100) tune the effects that support them
  (`canvas.effect_params` lists the knob union). `canvas.effect("none")` hands the panel back to
  the wall. This is the smooth way to
  animate: pushing frames over HTTP sustains ~40 fps, while an on-device effect is limited only
  by the panel.
- **`canvas.frame(image)`** — push a **full raw frame**. Pass a PIL image (it's resized and
  converted to the panel) or raw bytes already sized for it. This is how the **Image** app
  mirrors a picture. A frame is the heaviest thing you can send a wall, so send it once and
  hold it. The helper picks **QOI** compression automatically when the wall advertises it.

The helper also wraps the newer canvas features for apps that want them:
**`canvas.ticker(...)`** — a line of text **scrolling on-device** (the **Ticker** app);
**`canvas.anim(...)`** — upload a short **animation loop once** and it plays from the panel's PSRAM
even after the companion disconnects (the **Animation** app); and **`canvas.paste(...)`** — update
**one rectangle** without resending the whole panel. See the `apps/canvas-*` sources for exact usage.

`canvas.width` / `canvas.height` are the panel size in pixels; `canvas.effects` is the effect names
this panel offers, `canvas.effect_defs` each effect's self-described params (empty
before), `canvas.effect_params` the flat knob-name union (`hue`, `density`, `audio`), and `canvas.formats`
its raw-frame pixel formats (`rgb888`, `rgb565`, and **`qoi`** — lossless compression the helper
uses transparently).

## Rich rendering — smooth type and gradients

The op set draws with the panel's blocky built-in font. For **anti-aliased type, gradients and
glow** — using the panel's full pixel definition — render a whole frame with **Pillow** and push
it with `frame()`. Three helpers on `canvas` cover the common needs so each app doesn't reinvent
them:

- **`canvas.font(size)`** — a cached PIL `ImageFont` at `size` px, from a real bundled face.
- **`canvas.blank(color=(0,0,0))`** — a fresh RGB `Image` the exact size of the panel.
- **`canvas.vgrad(top, bottom)`** — a panel-sized vertical-gradient image (a sky, a backdrop).

And a **text toolkit**, so every app lays type out the same way (all fitters floor at
**8 px** — smaller renders wrong-reading glyphs on the panel):

- **`canvas.fit_font(text, max_w, max_h)`** — the largest font whose `text` fits the box.
- **`canvas.wrap(font, text, max_w, max_lines=None)`** — greedy word-wrap; an overlong word
  hard-splits with a visible hyphen; `max_lines` ellipsizes the surplus.
- **`canvas.wrap_fit(text, max_w, max_h, max_lines=None)`** — `(font, lines)` at the largest
  size that wraps inside the box.
- **`canvas.ink(font, text)`** / **`canvas.text_top(draw, x, y, text, font, fill)`** — ink
  height, and drawing with the ink's TOP at `y` (bbox-corrected).
- **`canvas.message(line1, line2="")`** — the quiet two-line offline/no-data card.
- **`canvas.text_card(label, body, page, accent=…, motif=…, sub=None)`** — the fact/quote
  card: accent label + rule (dropped on panels ≤ 32 px tall), the body page at the largest
  fitting font, page dots, an optional attribution owning the floor. `motif(draw, x, y, s)`
  draws your accent mark and returns its width. Returns `(img, page_count)`.
- **`canvas.mix(a, b, t)`** / **`canvas.dim(c, k)`** — color blend and scale.

```python
def fetch_matrix(settings, canvas):
    from PIL import ImageDraw
    img = canvas.vgrad((10, 16, 44), (3, 5, 16))     # a night-sky backdrop
    d = ImageDraw.Draw(img)
    d.text((4, 2), "22:47", font=canvas.font(24), fill=(255, 255, 255))
    canvas.frame(img)                                # push the whole frame
    return 0.2
```

The built-in **Lumina Clock**, **Photo Frame**, **Stock Graph**, and the panel views
of **Dashboard**, **Date**, **Countdown** and **World Clock** are all built this way — worth reading for layout,
animation-by-frame, and fitting type to the panel size. (The op-drawing apps — **Scoreboard**,
**Aquarium** and the **Home Assistant** panel view — use the `canvas.text`/`rect`/`sprite` ops above instead.)
`import PIL` **inside** `fetch`, never at module top: the module still has to load where Pillow
isn't installed.

## When to redraw — the return value

A matrix app's `fetch_matrix()` has nothing to return as content: the drawing *is* the output. Its
return value is instead a hint about **when to run it again** — a **number** is the seconds to
hold the current frame before the engine redraws; `None` (or anything non-numeric) falls back
to the manifest's `loop_delay`. A clock returns a fraction of a second and redraws so the time
sweeps; an on-device effect draws once and holds for a long time, because the panel is animating
itself and there is nothing more to send.

**Return the time to your next real change, not a fixed tick.** If your app only changes now and
then — a date card, a world clock showing `HH:MM` — return the seconds until it *next* changes (the
next minute, the next local midnight) rather than a small constant. The engine sleeps until then, so
the panel stays quiet and identical frames aren't re-sent over WiFi. The bundled **Date** panel view
holds until midnight; the **World Clock** panel view holds until the next minute.

## Matrix-only apps are gated off a flap wall

A physical split-flap wall has no framebuffer, so a **matrix-only** app (`surfaces: ["matrix"]`) has
nothing to draw on. The engine **gates** it: it refuses to start on a wall with no panel and isn't
offered there — so `fetch_matrix` is only ever called with a real `canvas`. No `canvas is None` guard
is needed; a matrix app has no `fetch` at all.

The built-in matrix apps — **Effects**, **Image**, **Animation**, **Ticker**, **Photo Frame**, **Lumina Clock**, **Stock Graph**, **Scoreboard**, **Aquarium**, and the playable **Chomper** and **Tetris** — are worth reading as templates (e.g. `apps/effects`, `apps/canvas-image`, `apps/canvas-art-clock`, `apps/sd-photos`, `apps/canvas-stock-graph`, `apps/canvas-scoreboard`, `apps/canvas-aquarium`, `apps/canvas-chomper`; for Pillow frame-push inside a dual-surface app, the matrix section of `apps/date` or `apps/weather`; for ops + a sprite atlas, the matrix section of `apps/entity-board`).g. `apps/effects`, `apps/canvas-image`, `apps/canvas-art-clock`, `apps/canvas-weather`,
`apps/canvas-stock-graph`, `apps/canvas-scoreboard`, `apps/canvas-aquarium`; for Pillow
frame-push inside a dual-surface app, the matrix section of `apps/date` is the template; for
drawing with ops + a sprite atlas, the
matrix section of the dual-surface `apps/entity-board` is the template). The raw panel API they sit
on is the firmware's **Canvas** endpoints — see the **[Canvas API](Canvas.md)** page for the full
reference (and the firmware's `openapi.yaml`, the **Canvas** tag, for the machine-readable spec).

## Dual-surface apps — one app, flaps *and* a panel

An app can ship **both** a split-flap view **and** a rich panel view, and let the display decide which
to show. That's a **dual-surface** app (`surfaces: ["flap", "matrix"]`) — the same app spells the
words on the flap wall in your hallway and draws them in pixels on the Matrix panel in your office.

There's no branching and no `canvas`-is-None dance: you write **two functions**, one per surface.

```python
def fetch(settings, format_lines, get_rows, get_cols, i18n=None):
    # the flap view — return pages, exactly like any §1–6 app
    return [format_lines("…", "…")]

def fetch_matrix(settings, canvas, i18n=None):
    # the panel view — draw with the canvas surface, return a hold
    canvas.frame(img)
    return 5.0
```

A **"Show on Matrix panel"** toggle is added to the app's settings automatically, at the **top** of
the form. It appears **only on a Matrix-panel display** — a flap-only wall never sees it — and is
**on by default**. On a panel with the toggle on the engine
calls `fetch_matrix`; otherwise (a flap wall, or the toggle off) it calls `fetch` and shows the pages.
In the app library and pickers a dual-surface app carries a **split-flap-plus-panel badge**.

**Nearly every bundled functional app is dual-surface** — Weather, Stocks, Word Clock, Tides, ISS
Tracker, the lot — so almost any `apps/*/app.py` in the tree is a working template with a `fetch`
and a `fetch_matrix` side by side. The canonical reads remain **Public Holidays**, **Countdown**
and **World Clock**: Holidays draws a
desk-calendar card (month band + big day number) with the holiday beside it; Countdown draws
full-width draining color bars; World Clock draws one lit day/night row per city — each falling back
to its flap text on a reel wall. Read `apps/holidays`, `apps/countdown` and `apps/world_clock` first
(each keeps its `fetch` and `fetch_matrix` side by side, sharing helpers below them).

> Keep the two views agreeing on **what** they show — e.g. rotate over the same items in the same
> order. The bundled dual-surface apps share one data path (`_upcoming`, the same slot enumeration) so
> a wall and a panel showing the same app never disagree.

## Channels and quizzes on the panel

A **channel** or **quiz** app isn't a canvas app — it has no code and no framebuffer drawing — but on
a Matrix panel the engine can still render it there instead of on the flaps: its line **laid out big
beside a themed icon**, on black. Two things opt an app in:

- **`canvas_art`** in the manifest names the icon (§2): `sun`, `moon`, `cookie`, `quote`, `mug`,
  `saber`, `clapperboard`, `grin`, `bubble`, `eightball`, `column`, `bolt`, `shower`.
- A **"Show on Matrix panel (art + text)"** toggle is added to the app's settings automatically, at
  the top of the form. It appears **only on a Matrix-panel display** and is **on by default**. Turn
  it off to keep the app on plain firmware text.

A **quiz** renders its two screens in turn — the question, then the answer — the same reveal it shows
on the flaps. No code is involved; the engine wraps the text and draws the icon. This is how **Movie
Quotes**, **Dad Jokes** and the **Fortune Cookie** apps appear on a panel.

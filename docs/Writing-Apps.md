# Writing a SplitFlap Companion app

This guide explains how to build a new **app** for the SplitFlap Gateway
Companion — the plugins that produce the content shown on the display (clocks,
weather, quotes, animations, …). It covers every file an app needs, the exact
contents of each, the functions your code must expose, and enough background on
the runtime to write non-trivial apps.

Apps here use the **splitflap-os plugin format**
([csader/splitflap-os](https://github.com/csader/splitflap-os)), and one direction of that
is a hard contract: an app written for splitflap-os drops in here and runs
(see [Compatibility](Compatibility.md)). The reverse is best-effort only — an app you write
here loads on stock splitflap-os (the injected helpers are opt-in by signature), but it
runs without them, unoptimized, and **we make no guarantees of it**.

---

## 1. How it works (the runtime in one page)

An app is just a **folder** under `apps/<id>/`. The companion scans that folder
(plus a user-upload folder), reads each app's `manifest.json`, and — for
*installed* apps — loads it. There are two kinds of app:

- **Functional** — has an `app.py` exposing a `fetch()` function that returns the
  content. Use this for anything dynamic (an API call, the current time, a
  computed animation).
- **Channel** — has a `data.json` holding static content as raw text (a rotating
  set of quotes) with no code. A **quiz** is a channel whose entries are
  `[question, answer]` pairs, shown as a two-screen reveal.

The **display** is a grid of `rows × cols` modules. A single screen is called a
**page**: a string of exactly `rows × cols` characters, laid out row-major
(`module index = row × cols + col`). An app returns a **list of pages**.

The **play loop** then:

1. Calls your app to get its pages (functional: runs `fetch()`; channel: reads
   `data.json`).
2. Shows the pages one at a time, each for **`loop_delay`** seconds, cycling.
3. Re-fetches when the cached result is older than **`refresh_interval`** seconds
   (functional apps only — the result is cached in between, so a 5-minute weather
   refresh isn't hit on every page flip).

Your `fetch()` may block on network I/O; the runtime runs it in a thread, so
`requests.get(...)` is fine.

```
apps/
└── my-app/
    ├── manifest.json     ← always required
    ├── app.py            ← functional apps (has fetch())
    └── data.json         ← channel apps (static pages)
```

The folder name is the app **id** (`my-app` above). Ids may contain letters,
digits, `-` and `_`. Folders beginning with `.` or `_` are ignored.

---

## 2. `manifest.json` — the app descriptor

Required for every app. It's JSON describing the app and its settings. Minimal
functional example:

```json
{
  "name": "My App",
  "icon": "✨",
  "description": "One-line summary shown on the app tile",
  "type": "functional",
  "category": "data",
  "refresh_interval": 60,
  "loop_delay": 5
}
```

### Top-level fields

| Field | Type | Required | Meaning |
|---|---|---|---|
| `name` | string | **yes** | Display name (app tile, HA select, menus). |
| `type` | `"functional"` \| `"channel"` \| `"quiz"` | **yes** | `functional` has `app.py`; `channel` and `quiz` have `data.json`. A **quiz** is a channel whose every entry is a `[question, answer]` pair, shown as a two-screen reveal (see §5). |
| `icon` | string (emoji) | no | Tile icon. Default `🧩`. |
| `icon_svg` | string | no | A `data:image/svg+xml,…` URI the catalog card and library row prefer over the emoji — for icons an emoji can't draw (Chomper's Pac-Man, Tetris's tetrominoes). Anything that isn't a `data:image/` URI is dropped. |
| `interactive` | bool | no | Matrix game: while the app runs, the web UI shows a control pad (D-pad + start/pause) under the Live Display; the app reads input via the injected `controls` helper (see [Writing Matrix Apps](Writing-Matrix-Apps.md)). |
| `description` | string | no | One-line blurb on the tile / library. |
| `category` | string | no | Grouping in the App Library — shown as a badge, and one of the library's filter chips. Common: `time`, `data`, `finance`, `sports`, `news`, `entertainment`, `education`, `lifestyle`, `animation`. Default `other`. |
| `id` | string | no | Fallback id, used **only** when the app isn't inside a named folder (e.g. a flat zip). An app in `apps/<id>/` always takes its id from the folder — leave this out. |
| `version` | string | no | Informational (e.g. `"1.0"`); shown next to the type in the App Library. |
| `refresh_interval` | number (s) | no | How long `fetch()` output is cached before re-running. Default `300`. Use `0`/`1` for always-fresh (clocks, animations). Ignored for channel apps. |
| `loop_delay` | number (s) | no | How long each page is shown before advancing. Default = the global loop delay (`8`). |
| `min_rows` / `min_cols` | number | no | Hide/disable the app unless the grid is at least this size. |
| `min_modules` | number | no | Require this many modules **total**, any shape (e.g. `45` works on 1×45 or 3×15). |
| `animation` | bool | no | Marks the app as an animation (see §6). Also inferred when the id starts with `anim_`. |
| `surfaces` | array | no | Which displays the app renders on: `["flap"]` (default), `["matrix"]`, or `["flap","matrix"]`. It renders each with a matching entry point — `fetch()` for flaps, `fetch_matrix()` for a Matrix panel (see §7). A channel/quiz's matrix surface is drawn generically. |
| `canvas_art` | string | no | For a **channel / quiz** app: the icon motif drawn beside its text when it renders on a Matrix panel (see §7). One of `sun`, `moon`, `cookie`, `quote`, `mug`, `saber`, `clapperboard`, `grin`, `bubble`, `eightball`, `column`, `bolt`, `shower`. Default `quote`. |
| `skip_rotation_wait` | bool | no | Advance pages without waiting for the flaps' mechanical settle (snappier multi-page apps). |
| `i18n` | bool | no | Marks the app as localized (a 🌐 badge on its tile). See §4 — set it once your app adapts to the global **Language**. |
| `vertical_align` | string | no | `center` (default) / `top` / `bottom` — where your block sits on a tall wall. See §4. |
| `settings` | array | no | The app's settings form — see §8. |
| `trigger_interval`, `trigger_display_seconds`, `trigger_cooldown`, `trigger_conditions` | — | no | Only for trigger apps — see §9. |

---

## 3. The display model (what a page is)

A **page** is a string of exactly `rows × cols` characters. Row 0 is the first
`cols` characters, row 1 the next `cols`, and so on. You almost never build that
string by hand — use the `format_lines` helper (below), which centres each line
and pads/truncates to the grid.

**Characters. Do not uppercase your own text.** Write it the way the words are
actually written. The companion folds the case *for the wall that needs it*, and it
is the only thing that knows which wall that is: a real split-flap has no lowercase
flaps, while a Matrix Gateway (whose modules are drawn, not mechanical) has them and
shows your text as you wrote it. The fold is Windows-1252-aware, so `É`, `Ü`, `ç`
and `ß` survive it: `ß` is *not* uppercased to `SS`, because a reel that carries `ß` carries
only the lowercase flap (there is no `ẞ`), so `STRAßE` is the correct all-caps German page.
Only a reel with **no** `ß` at all falls back to `SS`, and that is handled for you.

**Write normal text — punctuation, accents and `€` are fine.** You do not have to know what
is printed on the user's reels. The gateway tells the companion (`GET /api/capabilities`), and
anything the wall cannot show is degraded on the way out: an accent to its base letter
(`Åre` → `ARE`), a curly quote to `'`, an em dash to `-`, `ß` to `SS` on a reel with no `ß`.
What the reel *does* carry, it keeps — on a French wall, `Prévu` shows as `PRÉVU`.

Without that substitution, a module asked for a flap it does not have simply **homes** — a
blank hole in the middle of a word, telling nobody. It is what lets you write in full text
instead of stripped-down ASCII.

The one exception is an **animation** (`"animation": true`): in an animation page the
lowercase letters `r o y g b p w` are read as COLOUR FLAPS, not letters (below), so the case
of an animation's text is left exactly as your code produced it. On a split-flap that means an
animation drawing *words* must uppercase them itself — the wall would otherwise read a
lowercase `r` as a red flap:

```python
title = article["title"].upper()   # in an ANIMATION only — elsewhere, never uppercase
```

**Colour tiles.** In an **animation** page, the lowercase letters `r o y g b p w` are the
firmware colour codes (red, orange, yellow, green, blue, purple, white) — a page made of them
shows solid colour flaps. This is why an animation is the one place you write lowercase on
purpose. (In a *normal* app those same letters are just letters, folded to `R O Y G B P W` on a
split-flap.) The **emoji colour squares** work in *any* page — normal or animation — and are
the clearest way to place a colour:

| Emoji | Code | Colour |
|---|---|---|
| 🟥 | `r` | red |
| 🟧 | `o` | orange |
| 🟨 | `y` | yellow |
| 🟩 | `g` | green |
| 🟦 | `b` | blue |
| 🟪 | `p` | purple |
| ⬜ | `w` | white |
| ⬛ | (space) | blank |

> Case matters **in an animation page**: there `y` = a yellow tile and `Y` = the letter Y.
> In a normal app both are letters — reach for the 🟨 emoji square instead, which is a colour
> in any page.

---

## 4. Functional apps — `app.py`

A functional app's `app.py` must define **`fetch`**:

```python
def fetch(settings, format_lines, get_rows, get_cols):
    ...
    return ["<page string>", "<page string>", ...]
```

### The four arguments

- **`settings`** — a flat `dict` of the app's resolved settings plus shared
  global settings (see §8). Read values with `settings.get("key", default)`.
- **`format_lines(*lines, cols=None)`** — build a page from up to `rows` text
  lines. Each line is centred in `cols` (default = grid width) and truncated;
  missing lines are blank. Returns one `rows × cols` page string. This is the
  normal way to build a page.
- **`get_rows()`** / **`get_cols()`** — the current grid dimensions as ints. Call
  these and adapt your layout — a good app renders sensibly at 1×N and 3×N.

### Optional: shared current weather

If your app shows the weather, don't hardcode a provider — opt into the shared
helper by adding a fifth parameter, `get_weather=None`:

```python
def fetch(settings, format_lines, get_rows, get_cols, get_weather=None):
    if get_weather is None:            # running on a host without the helper
        return [format_lines("NO WEATHER")]
    w = get_weather()                  # uses the *global* provider + key + location
    if not w["ok"]:
        return [format_lines("WEATHER", "UNAVAILABLE")]
    return [format_lines(w["city"], f'{w["temp_f"]}F {w["desc"]}')]
```

`get_weather()` returns a dict with at least: `ok`, `city`, `temp_f`, `temp_c`,
`feels_like_f`, `hi_f`, `lo_f`, `desc`, `humidity`, `wind_mph`, `cloud_cover`, `provider`,
`lat`, `lon`, the raw provider `code` — and `sky`, the **canonical condition token**
(`clear`, `pcloudy`, `cloudy`, `fog`, `rainl/rain/rainh`, `shwr`, `snowl/snow/snowh`,
`sleet`, `hail`, `storm`), the same whatever the provider, so you never read provider
codes. Temperatures are in °F; `ok` is `False` with an `error` key on failure.

It also takes optional arguments:

- `get_weather(days=3)` adds `forecast` — `[{date, hi_f, lo_f, sky}]`, today excluded —
  and `hourly` (`{time, temp_f, temp_c, utc_offset_s}`, always keyless Open-Meteo, so a
  temperature graph works with any provider or none);
- `get_weather(air=True)` adds `air` — AQI, UV and pollen with display `*_label`s **and**
  canonical `*_band`s (`good/moderate/poor/bad`, plus `none`/`unknown`), so one colour map
  covers every provider's scale.

Because the default provider is keyless Open-Meteo, weather works with **no API key**. The
four-argument signature keeps working unchanged, so `get_weather` is purely opt-in.

### Optional: location → country / currency (`get_location`)

Anything tied to *geography* — which currency, which country's holidays — should key
off the configured **Location**, not the language (French is France, Canada,
Belgium, Switzerland — different currencies and holidays). Declare a `get_location`
parameter to get the shared resolver:

```python
def fetch(settings, format_lines, get_rows, get_cols, get_location=None):
    loc = get_location() if get_location else {}
    country     = loc.get("country")      # ISO 3166-1 alpha-2, e.g. "CA"
    subdivision = loc.get("subdivision")  # ISO 3166-2, e.g. "CA-QC" (Quebec); may be None
    currency    = loc.get("currency")     # ISO 4217, e.g. "CAD" (None if unknown/unset)
    lat, lon    = loc.get("lat"), loc.get("lon")   # the configured coordinates
    city        = loc.get("city")         # geocoded display name, e.g. "BOSTON"
    # loc["ok"] is False when no location is set or the reverse lookup failed.
    # lat/lon can still be present then (precise coordinates need no lookup), so
    # coordinate apps should test `loc.get("lat") is not None`, not `ok`.
```

**Never geocode yourself.** `lat`/`lon`/`city` are the platform's one cached
Nominatim resolution of the configured Location — the same one the weather helper
uses. An app that runs its own geocode ladder duplicates that query on every
refresh and answers a question the platform has already answered.

It reverse-geocodes the global Location once (cached) and is keyless. Prefer an
explicit setting first, then `get_location()`, then fall back to `i18n` — e.g. a
currency's base: `settings.get("base") or (get_location() or {}).get("currency") or
i18n.base_currency()`. The `subdivision` lets you narrow region-specific data (the
Public Holidays app filters to your province/state with it). Declaring `get_location`
also gives the app an automatic per-app **Location** override in its settings.

If you show public-holiday names from an English-only source, `i18n.holiday(name)`
returns a localized name for the common holidays (or `None` — then keep the source's
native name).

### Optional: localization (`i18n`)

If your app shows words (day/month names, status labels), opt into localization by
adding an `i18n=None` parameter. The runtime binds it to the global **Language**
setting; on a host without it, `i18n` is `None` and you fall back to English.

```python
def fetch(settings, format_lines, get_rows, get_cols, i18n=None):
    from datetime import datetime
    now = datetime.now()
    weekday = i18n.weekday(now) if i18n else now.strftime("%A")
    label = i18n.t("SUNRISE") if i18n else "SUNRISE"
    return [format_lines(weekday, label)]
```

- `i18n.weekday(dt, short=False)` / `i18n.month(dt, short=False)` — CLDR-correct day
  and month names for *every* language (via babel), in that language's **own case**:
  `Monday`, `lundi` (French does not capitalise them), `Montag` (German does). The
  wall folds it if it must.
- `i18n.date(dt, short=False, year=False)` — day + month (and optional year) in the
  locale's **own order and wording**: `July 9` in English but `9 juillet` (fr),
  `9. Juli` (de), `9 de julio` (es). Don't hand-assemble `month + " " + day` — the
  order is language-specific, so let this decide it.
- `i18n.time(dt, seconds=False, ampm_space=True)` — wall-clock time: `3:48 PM` in
  English, `15:48` everywhere else (AM/PM is an English convention). `i18n.is_24h`
  exposes the same decision if you need to branch yourself.
- `i18n.unit("D")` — a localized compact duration suffix for `D`/`H`/`M`/`S`, so
  `175D` becomes `175J` in French (jour), `175T` in German (Tag), `175G` in Italian.
- `i18n.number(value, decimals=2, grouping=True)` — a number with the locale's own
  separators: `1,234.50` (en) vs `1.234,50` (de) vs `1 234,50` (fr). Use it for any
  price/rate/percent — never hardcode `f"{v:,.2f}"`.
- `i18n.base_currency()` — the currency a language/region implies (`USD`/`GBP`/`AUD`
  for US/UK/Australian English, `EUR` for Western Europe), a sensible default base for
  a currency/FX app. English is split by region (`en-US`/`en-GB`/`en-AU`), which also
  drives date order — `i18n.date()` gives `JULY 9` for US but `9 JULY` for UK/AU.
- `i18n.t("ENGLISH LABEL")` — a translated UI word; if there's no translation for
  the current language it returns the English key, so nothing ever breaks. The data
  lives in `app/i18n_data.json` (the language list, translations, and per-language
  default currency/country). Add keys or languages there rather than in your app,
  give each key a generic `context` note for translators, and keep translations short
  — the modules are narrow, and a long word will be trimmed. A regional variant like
  `pt-BR` automatically inherits every `pt` translation.

Localization is grammar, not word-swapping: name the hour before the minutes in
Romance languages, honor date order, spell numbers the way the language does. When
a language's structure genuinely differs (a word clock, a plural rule), keep that
logic **inside the app** keyed off `i18n.lang` — see `apps/word-clock/app.py`, which
carries its own per-language phrase builders. All helpers compose with
`get_weather`: `def fetch(..., get_weather=None, i18n=None)`.

Once your app adapts to the language, add `"i18n": true` to its `manifest.json` — the
Apps grid and library show a 🌐 badge on those cards so users know they follow the
global **Language**.

### Optional: what the wall can show (`caps`)

Some walls are drawn rather than mechanical (a **Matrix Gateway**), and those carry
fourteen pictographs a real reel has no flap for. A **physical** reel can also carry six of
them as real flaps — `♥ ↑ ↓ ☺ ← →` — when they're printed on it. Declare `caps` and the
runtime tells you what you are driving:

```python
def fetch(settings, format_lines, get_rows, get_cols, i18n=None, caps=None):
    high = "↑" if (caps and caps.can_show("↑")) else "HIGH"
    return [format_lines(f"{high} 9:28AM")]
```

`caps` is not a guess. The gateway is asked (`GET /api/capabilities`) what its wall can do,
on boot and on every resync, and this is its answer:

| field | what it tells you |
|---|---|
| `lowercase` | it has lowercase flaps |
| `pictographs` | it has **all fourteen** extra flaps (a drawn wall). A physical reel may carry only some symbols — ask `can_show("♥")`, not this |
| `named_colors` | colors are named, not spelled with `r/o/y/g/b/p/w` |
| `instant` | **are sub-second updates honest here?** `True` on a drawn wall (a cell is a repaint); `False` where mechanical flaps must physically finish a move. Gate any ticking display — a seconds field, a fast bar — on this. Use `getattr(caps, 'instant', False)` so the app still runs on stock splitflap-os. |
| `can_show(ch)` | **can every module on this wall show this exact character?** |
| `charset` | every character it can show (the intersection across its modules) |
| `uniform` | whether all its modules carry the same reel |

`can_show` is the useful one, and it works on a physical wall too — the gateway knows which
flaps are printed on its reels:

```python
def fetch(settings, format_lines, get_rows, get_cols, caps=None):
    degree = "°" if (caps is None or caps.can_show("°")) else " "
    return [format_lines(f"22{degree}C")]
```

**You do not have to do this.** Anything the wall cannot show is degraded on the way out —
an accent to its base letter (`é` → `E`), a curly quote to `'`, a pictograph to its stand-in,
a `ß` to `SS` on a reel that has no `ß`, and only as a last resort to a space. Reach for `caps`
when you want to make a *different* choice, not to avoid a broken one.

(`ß` → `SS` costs a second module, so it happens to your *lines*, inside `format_lines`, before
they are centred — which is why `format_lines` is the thing that lays your page out and you
should not build the grid yourself.)

`caps` is optional and defaults to `None`, which is also what a stock splitflap-os host
passes, and which correctly means *"assume nothing, send it and let the wall cope"*. So an
app that uses it stays drop-in in both directions.

The pictographs: `♥ ♦ ♣ ♠ ☺ ♪ ● ■ ⌂ ← ↑ → ↓ ☀`

**Check before you use one.** A wall without them substitutes the nearest character it
has, and only some of those still mean anything:

| pictograph | on a plain reel | verdict |
|---|---|---|
| `← ↑ → ↓` | `< ^ > V` | **safe with no check** — still reads |
| `■` `⌂` `☺` | `#` `^` `:` | usable |
| `♥ ♦ ♣ ♠ ♪ ● ☀` | `*` | **meaning is lost** — ask `caps.can_show("♥")` |

A physical reel that actually carries `♥ ↑ ↓ ☺ ← →` shows them for real (the gateway sends the
right flap); `can_show` is how you find out, per wall.

The seven **colour flaps** are different: every wall has had them from the start, so a
colour tile (🟥🟩🟦🟨🟧🟪⬜) is always safe. But a colour is invisible when the user turns
colours off — so if you are showing a **direction**, show an arrow as well as the colour.

### Optional: where your lines sit (`vertical_align`)

Return only the lines you actually **have**. Given fewer than the wall is tall,
`format_lines` **centres** the block, so a 3-line app looks right on a 3-row wall and on
a 5-row one. Do **not** pad to `get_rows()` yourself — that fills the page, and your
content ends up pinned to the top of a tall wall.

If your app builds its own layout and wants its rows left exactly where it put them, say
so in the manifest:

```json
{ "vertical_align": "top" }     // "center" (default) | "top" | "bottom"
```

`"top"` is byte-for-byte the original splitflap-os padding. The key is additive: absent
means `"center"`, so an app that omits it is centred. Without it, an app that
centres its own block gets centred a **second** time and drifts below the middle.

### The return value

Return a **list of page strings**. Each should be `rows × cols` characters — i.e.
each should come from `format_lines(...)` (or be built to match). One page = one
screen; multiple pages rotate at `loop_delay`. Always return **at least one**
page. (A non-list return value is coerced to a single page.)

### Caching & errors

- Your `fetch()` result is cached for `refresh_interval` seconds; the play loop
  reuses it for every page flip in between. Don't do your own caching for that.
- If `fetch()` raises, the runtime falls back to the **last good cached pages**;
  if there are none, it shows a generic error page. Exceptions whose text
  mentions `timeout`/`connection`/`network` render an "OFFLINE" page. So it's
  fine to let a network error propagate — but catching it yourself and returning
  a friendly page (as the examples do) is nicer.

### Example — the built-in `date` app

```python
def fetch(settings, format_lines, get_rows, get_cols, i18n=None):
    from datetime import datetime
    import pytz
    try:
        tz = pytz.timezone(settings.get('timezone', 'US/Eastern'))
    except pytz.UnknownTimeZoneError:
        tz = pytz.timezone('US/Eastern')
    now = datetime.now(tz)
    # When the companion injects i18n, honour the global Language: a localized weekday, a
    # locale-ordered date (9 juillet, not juillet 9), and 24h time outside English.
    if i18n is not None:
        time_str, weekday, month_day = i18n.time(now), i18n.weekday(now), i18n.date(now)
    else:
        time_str = now.strftime('%I:%M %p').lstrip('0')
        weekday, month_day = now.strftime('%A'), f"{now.strftime('%B')} {now.day}"
    rows = get_rows()
    if rows == 2:
        return [format_lines(month_day, weekday)]
    if rows >= 4:
        return [format_lines(time_str, weekday, month_day, str(now.year))]
    return [format_lines(time_str, month_day, weekday)]
```

This is the real `apps/date/app.py`. Note how it reads a **global** setting (`timezone`),
**adapts to the grid** (`rows == 2`, `rows >= 4`), and **localizes** through the optional
`i18n` helper while still working without it.

### Dependencies

`app.py` runs in the companion's Python process, so it may `import` anything the
companion already ships: the standard library plus `requests`, `pytz`,
`httpx2`, `yfinance` (pandas/numpy), `Pillow`, `babel`, `python-dateutil`,
`paho-mqtt`, `pyyaml`, and FastAPI's stack. A
**built-in** app that needs a new package requires adding it to
`backend/requirements.txt` and rebuilding the image. An **uploaded** app can only
use packages already present (there's no per-app dependency install).

---

### Optional: shared pagination (`paginate`) and HA states (`get_ha_states`)

Declare `paginate=None` and call `paginate(text, title="")` to get finished pages: the
block word-wrapped and balanced to this wall, title on its own line. It is how the
advice/quote/fact apps paginate, so every text app breaks lines the same way. Declare
`get_ha_states=None` for all Home Assistant entity states (cached; the Supervisor proxy
in the add-on, or `COMPANION_HA_URL`/`_TOKEN` standalone).

## 5. Channel apps — `data.json`

A channel app has no code. Its `data.json` lists the content as **groups** — you
write the words, and the engine wraps them to whatever wall it's on:

```json
{
  "groups": [
    "May the Force be with you\n- Obi Wan",
    "Do or do not, there is no try\n- Yoda",
    ["Why did the scarecrow win?", "He was outstanding in his field"]
  ]
}
```

Each entry in `groups` is one **item**, and an item is either:

- a **string** — a single-page item (a quote, a fortune, one 8-ball answer). The
  engine word-wraps it to the wall. A `\n` forces a line break, which is how you
  keep an attribution (`- Yoda`) or a header on its own line; everything else
  flows.
- a **list of strings** — a multi-page item, one string per page (a joke's setup
  then punchline, a quote that needs two pages). The pages stay **together and in
  order**, always — a shuffle can never tear a punchline off its setup, because
  the grouping is in the data, not guessed.

You write the *text*, not the line breaks. `"May the Force be with you"` reads
the same on a 12-column wall (three lines) and a 22-column one (one line) — you
don't split it yourself.

The manifest `type` must be `"channel"`, and channel apps ignore
`refresh_interval` (the pages are static). Pages rotate at `loop_delay`.

### Page order — sequential or random

By default a channel plays in **file order** (`"order": "sequential"`). A channel
whose items are independent — one quote, one fortune, one answer each — reads
better **shuffled** so it doesn't march the same way every day:

```json
{ "type": "channel", "order": "random" }
```

Because items are grouped in the data, `random` is always safe: a two-page joke
shuffles as a unit, its setup still followed by its punchline. Set `random` for
quote/answer channels; leave setup-then-punchline **jokes** `sequential` if you
want them told in a fixed order.

> **Legacy format.** The older `{"pages": [{"lines": [...]}]}` shape (hand-split
> lines, one page per entry) still loads — a splitflap-os channel drops in
> unchanged. Under it, multi-page grouping comes from the manifest's
> `"group_size": N` (every item is N pages) or a per-page `"group"` id. Prefer
> `groups` for anything new: you write text, not wall-width line breaks.

### Quiz apps — `[question, answer]` pairs

A **quiz** is a channel with one extra rule: every item is a two-element
`[question, answer]` list. The engine shows the two screens in turn — the
question, then (after `loop_delay`) the answer — a small reveal. Set
`"type": "quiz"`, and in every `data.json` (and each `data_<lang>.json`) make
every group a pair of non-empty strings:

```json
{
  "type": "quiz",
  "order": "random",
  "groups": [
    ["Why did the scarecrow win an award?", "He was outstanding in his field"],
    ["What do you call a fake noodle?", "An impasta"]
  ]
}
```

`random` keeps each question with its own answer as it shuffles. Everything else
about a channel — `data_<lang>.json` translations, `loop_delay`, and rendering on
a Matrix panel (§7) — applies unchanged. The bundled **Dad Jokes** app is a quiz.

### Localizing a channel app

Channel apps have no code, so they can't call the [`i18n`](#optional-localization-i18n)
helper a functional app gets. Instead they ship **one data file per language**,
alongside `data.json`:

```
apps/good-morning/
  manifest.json
  data.json          ← the default pages, and the fallback
  data_fr.json       ← French
  data_de.json       ← German
  data_pt-BR.json    ← Brazilian Portuguese specifically
```

The filename is `data_<lang>.json`, where `<lang>` is a language code from the
Language setting (`fr`, `de`, `pt-BR`, `fr-CA` …). Each file has exactly the same
shape as `data.json` — a `groups` list (or the legacy `pages`) — with the same
items in the same order, so item *N* is the same quote or joke in every language.

At render time the companion picks the file from the **effective Language** (the
per-app override if set, otherwise the global one), with this precedence:

1. **exact locale** — `fr-BE` → `data_fr-BE.json`
2. **base language** — `fr-BE` → `data_fr.json`
3. **`data.json`** — any language you haven't translated

So you only translate as far as you care to: ship `data_fr.json` and every French
locale is covered; add `data_fr-CA.json` later and Québec gets its own text while
the rest of the French-speaking world keeps the shared file. A language with no
file renders `data.json` rather than blanking.

Keeping `data.json` as the fallback also means a localized app still runs
unchanged anywhere that ignores the sidecars, including splitflap-os.

You do **not** need `"i18n": true` in the manifest — an app that ships translations
is detected as localizable automatically, which is what puts the 🌐 badge on it and
gives it a per-app **Language** override. (Setting the flag by hand does no harm.)

### Localizing your app's name, description and settings labels

The store metadata translates through a sidecar too — **never through
`manifest.json`**, which must stay a plain splitflap-os manifest:

```
apps/my-app/
  manifest.json        ← name/description stay English here
  i18n/fr.json         ← {"name": "Mon appli", "description": "…",
                          "settings": {"api_key": "Clé API"}}
  i18n/pt-BR.json
```

Recognised keys: `name`, `description`, `flap_name`, and `settings` (a map of
your manifest setting keys to translated labels). The App Library and the
settings form pick the file matching the **viewer's UI language** (exact locale,
then base, then the manifest's English). `flap_name` exists for the fallback
pages rendered *onto the flaps* ("NO DATA"…), which follow the content Language
and the reel's character set — set it when the pretty translated name can't
survive the reel. Files are validated at upload; a broken one is rejected with
the reason. The built-in library is covered centrally in
`backend/app/app_i18n/<lang>.json` — a sidecar in your app wins over it.

Mind the width: translations are centred and truncated to the grid like any other
page, and a word that fits in English often doesn't in German.

---

## 6. Animations

An animation is just a functional app that returns many pages (frames) built from
colour codes, marked with `"animation": true` (or an `anim_` id). The play loop
plays the frames back-to-back — each held for this app's own `anim_speed` (seconds per frame,
default `4` — sized for a physical wall: a frame can send any flap anywhere, and a module's
full revolution takes up to ~4 s) and revealed in its own `anim_style` order, rather than the
normal `loop_delay` and transition timing. Both are per-app settings: each animation keeps
its own.

```json
{ "name": "Rainbow", "icon": "🌈", "type": "functional",
  "animation": true, "refresh_interval": 0, "loop_delay": 0.4,
  "category": "animation" }
```

```python
def fetch(settings, format_lines, get_rows, get_cols):
    colors = 'roygbpw'
    rows, cols = get_rows(), get_cols()
    return [''.join(colors[(c + off) % 7] for r in range(rows) for c in range(cols))
            for off in range(7)]
```

Each string here is a full `rows × cols` frame of colour codes; the seven frames
form a scrolling rainbow. `refresh_interval: 0` keeps frames regenerating.

---

## 7. Matrix apps — drawing on a Matrix panel

A **Matrix Gateway** hands an app its LED panel as a plain framebuffer: apps declare a
`"matrix"` surface and draw — pixels, shapes, gauges, sprites, smooth Pillow-rendered
frames, on-device effects — instead of returning flap pages, and **dual-surface** apps
ship both views side by side. That whole world now has its own page:

- **[Writing Matrix Apps](Writing-Matrix-Apps.md)** — surfaces and `fetch_matrix`, the
  `canvas` drawing object and its helpers, whole-panel shortcuts (effects, frames,
  ticker, animations), Pillow rendering and the text toolkit, redraw pacing,
  matrix-only gating, dual-surface apps, channels/quizzes on the panel.
- **[Canvas Ops Reference](Canvas-Ops-Reference.md)** — every drawing op in detail:
  parameters, defaults, semantics, examples.

## 8. Settings (the app's config form)

`settings` in the manifest is an array of field descriptors. The companion
renders them into the app's settings dialog and passes the saved values into
`fetch()` (and `trigger()`) via the `settings` dict.

```json
"settings": [
  {
    "key": "city",
    "label": "City",
    "type": "text",
    "ph": "Boston",
    "default": ""
  },
  {
    "key": "units",
    "label": "Units",
    "type": "select",
    "options": ["metric", "imperial"],
    "default": "metric"
  }
]
```

### How keys reach your code

- A normal setting `"key": "city"` is stored per-app and appears in the
  `settings` dict under **`"city"`**. (Internally it's namespaced as
  `plugin_<id>_city`, but your code just reads `settings.get("city")`.)
- The companion has a **fixed built-in catalog of global settings** — the API
  keys, location, timezone, language, weather provider and default page dwell,
  including `weather_api_key`, `weather_provider`, `zip_code`, `location_lat/lon/name`,
  `timezone`, `language`, `yt_api_key`, `global_loop_delay`, `disable_colors` and
  `force_uppercase`. Reading one of those keys (`settings.get("weather_api_key")`) returns the
  shared global value.
- **Everything else is per-app** — each app keeps its own value even if two apps
  use the same key name. On the companion a manifest's `"global_key": true` is
  *ignored* (only the catalog is global); it works on stock splitflap-os,
  so it's harmless to leave in, but it won't make a non-catalog key shared here.

The `settings` dict your code receives always includes the catalog globals plus
this app's own keys, so you can read shared config (`settings['zip_code']`) even
without declaring it.

### Setting object fields

| Field | Meaning |
|---|---|
| `key` | **Required.** The setting name (see key resolution above). |
| `label` | Field label in the form. |
| `type` | Field type (table below). Default `text`. |
| `default` | Initial value before the user saves anything. |
| `note` | A caption shown under the field. |
| `global_key` | Legacy splitflap-os flag — **ignored here.** Only catalog keys are global (see above); the flag will not make a non-catalog key shared. Harmless to leave in. |
| `options` | For `select`/`toggle`: array of strings, or `{"value","label"}` objects. |
| `ph` | Placeholder text. |
| `min` / `max` / `step` | For `number` inputs. |
| `stepper` | `true` → show −/+ stepper buttons around a number field. |
| `searchUrl` / `resultKey` / `maxItems` | For `search_chips` (see below). |
| `visible_when` | `{ "otherKey": "value" }` — only show this field when another field equals a value. |
| `inline_toggle` | Attach a small secondary toggle to the field (its own `key`/`default`/`global_key`). |
| `compute` / `watches` | For `computed` read-only fields derived from other fields. |
| `title` / `text` / `items` / `icon` / `linkText` / `linkHref` / `variant` / `size` | Passed through to the frontend for presentational field types. |

### Field types

| `type` | Renders as |
|---|---|
| `text` | Single-line text input. |
| `number` | Numeric input (with optional `stepper`, `min`/`max`/`step`). |
| `password` | Masked text input (API keys). |
| `datetime-local` / `date` / `time` | The browser's native calendar/time picker. `datetime-local` yields the exact ISO string `datetime.fromisoformat` parses — use it for any target-date setting (the Countdown app does). |
| `textarea` | Multi-line text. |
| `select` | Dropdown from `options`. |
| `toggle` | Segmented buttons from `options` (`{value,label}`). |
| `search_chips` | Live-search field that adds chips — see below. |
| `computed` | Read-only value derived from other fields (`compute`/`watches`). |
| `notice` | Static informational text (`label`/`text`) — not an input. |

### `search_chips` and the built-in search endpoints

A `search_chips` field queries an endpoint as the user types and lets them pick
results as chips. Point `searchUrl` at one of the companion's built-in search
endpoints (same paths and response shapes as splitflap-os):

| `searchUrl` | For | `resultKey` |
|---|---|---|
| `/location_search` | Cities / locations | `results` |
| `/timezones` | Timezone names | `zones` |
| `/stocks_search` | Stock tickers | `results` |
| `/crypto_search` | Cryptocurrencies | `results` |
| `/sports_search` | Leagues **and** their teams, in one call | `results` |

`resultKey` names the array in the JSON response to read, and `maxItems` caps how
many chips can be selected. Example (the `date` app's timezone override):

```json
{ "key": "timezone", "label": "Timezone (override global)",
  "type": "search_chips", "searchUrl": "/timezones", "resultKey": "zones",
  "maxItems": 1 }
```

(`timezone` is a **catalog global**, so this field is edited under *Global settings*, not in
the app's own dialog — the snippet shows the shape, not where it appears.)

---

## 9. Triggers (optional, functional apps)

A trigger lets an app **interrupt** the display when something happens (the ISS
passes overhead, a game starts). Add a `trigger` function to `app.py`:

```python
def trigger(settings, conditions) -> bool:
    # return True to fire the interrupt now, False otherwise
    ...
```

- `settings` — same dict as `fetch()`.
- `conditions` — the values the user configured from `trigger_conditions` (below).
- **Helpers**: a trigger opts into the same injected helpers as `fetch()`, by
  parameter name — `trigger(settings, conditions, caps=None, i18n=None,
  get_weather=None, get_location=None)`. Default them to `None`: a stock
  splitflap-os host injects nothing, and the two-argument form stays the hard
  contract. Use them instead of hand-rolling geocoding or timezone parsing inside
  a trigger.
- Return **`True`** to interrupt and show this app's **first page** — held static —
  for `trigger_display_seconds`, then respect `trigger_cooldown` before it can fire
  again. (A trigger is a glance, not a running app: only page 1 is shown.)

Declare the schedule and the config UI in the manifest:

```json
"trigger_interval": 60,
"trigger_display_seconds": 30,
"trigger_cooldown": 3600,
"trigger_conditions": [
  { "key": "condition_type", "label": "Fire when", "type": "toggle",
    "default": "overhead",
    "options": [
      {"value": "overhead", "label": "ISS overhead"},
      {"value": "crew_change", "label": "Crew change"}
    ] }
]
```

| Manifest field | Meaning |
|---|---|
| `trigger_interval` | How often (seconds) the runtime calls `trigger()`. |
| `trigger_display_seconds` | How long to show the app when it fires. |
| `trigger_cooldown` | Minimum seconds between firings. |
| `trigger_conditions` | Setting fields (same schema as §8) whose values arrive in `conditions`. |

### Keeping state across calls

`trigger()` (and `fetch()`) are plain functions, but you can stash state on the
function object itself — the runtime keeps the module loaded, so it persists
between calls:

```python
def trigger(settings, conditions):
    state = getattr(trigger, '_state', None)
    if state is None:
        state = {'last_crew': None}
        setattr(trigger, '_state', state)
    ...
```

This is how the built-in `iss` app remembers the previous crew roster to detect a
change.

---

## 10. Installing your app

Two ways:

1. **Drop-in (built-in style).** Put the folder in `apps/<id>/` and (re)start the
   companion. It appears in the **App Library**; enable it there to load it. This
   is how the built-in apps ship.

2. **Upload a `.zip` (no restart).** In the UI: **App Library → Upload**. Zip the
   **app folder** so the archive contains exactly one `manifest.json` (its parent
   folder becomes the id):

   ```
   my-app/
     manifest.json
     app.py          (or data.json)
   ```
   ```bash
   cd my-app && zip -r ../my-app.zip .        # or zip the folder itself
   ```

   The upload is vetted before it installs — if anything fails, the upload is
   rejected with a clear reason and nothing is written:

   - **Manifest** must have a `name`, a valid `type`, and (if present) a
     `settings` list whose entries each have a `key`.
   - **Functional** apps must include `app.py`; it must define
     `fetch(settings, format_lines, get_rows, get_cols)` (checked statically),
     pass the **safety audit** below, and then import cleanly (so a missing
     dependency is caught).
   - **Channel** apps must include a `data.json` with a non-empty `groups` (or legacy `pages`) list; a **quiz** app's groups must each be a `[question, answer]` pair.

   **Safety audit.** `app.py` is statically scanned *before it is ever executed*
   and rejected if it uses operations an app has no business doing — running
   programs (`subprocess`, `os.system`), executing code (`eval`/`exec`/`compile`,
   `pickle`, dynamic import), spawning threads or processes
   (`threading`, `multiprocessing`, `asyncio`), raw sockets, writing/deleting files,
   reading `os.environ`, or interpreter-escape introspection (`__subclasses__`,
   `__globals__`, `sys._getframe`, …). Apps fetch data with `requests`/`urllib`
   and render pages — that's allowed; the rest isn't. (This is best-effort
   defense-in-depth, not a sandbox — a vetted app still runs in-process, so only
   install apps you trust.)

   **Settings are scoped for you.** Any setting your code *reads* that isn't a
   global (catalog) key is auto-declared as an **app-level** setting in the
   manifest on upload (and a misleading `global_key` flag on a non-catalog setting
   is dropped), so every non-global setting is stored under `plugin_<id>_<key>`
   and never collides with another app. (Catalog globals like `timezone` are the
   deliberate exception — they are shared, that's the point.)

   Uploaded apps are written to the persistent data volume (so they survive
   restarts and image upgrades), enabled, and loaded immediately. They show a
   **· uploaded** tag and a 🗑 to remove; built-ins can't be deleted. An uploaded
   app with the same id as a built-in **overrides** it.

> ⚠️ **Security:** the audit blocks obvious abuse, but installing a functional app
> ultimately *runs its `app.py`* on the companion host. Only install apps you
> trust. Same trust model as splitflap-os plugins.

---

## 11. House rules

The 2026 catalog audit distilled these from the ways apps actually went wrong.
Each is a convention, and several are enforced by tests — a new built-in that
breaks one fails `pytest`.

**One truthy parser.** A toggle setting arrives as a string. Parse it with the
whitelist, nothing else:

```python
on = str(settings.get('some_toggle', '')).strip().lower() in {'1', 'true', 'yes', 'on'}
```

**One timezone snippet.** A bad zone string coming out of settings must never
take a fetch down, and the fallback is **UTC** — the only zone that means the
same thing on every wall (the host injects the real timezone into `settings`
anyway, so the fallback almost never shows):

```python
try:
    tz = pytz.timezone(settings.get('timezone') or 'UTC')
except Exception:
    tz = pytz.utc
```

Apps with `i18n` can use `i18n.tz(settings.get('timezone'))`, which is the same
thing as a one-liner.

**Errors: raise, or fall back to real content.** Prefer letting a network error
*raise* — the engine shows the cached pages if it has them, OFFLINE if not.
If you build an error page by hand, its words go through `t()` like any other
chrome. And for apps with bundled data, canned content beats an error page:
a wall that says "Offline" all night is a broken clock; one that shows a bundled
fact is still a display.

**`min_rows`/`min_cols` are a contract.** Declare the smallest wall your layout
*actually fits* — the widest line you produce, the rows your layout needs. An
under-declared minimum doesn't make the app more available; it guarantees
truncation on the walls in between (twelve channels once declared `min_cols: 10`
over 15-wide data — every page was cut on a 10-column wall).
`backend/tests/test_app_conformance.py` enforces this for channel data.

**The i18n badge is a promise.** Set `"i18n": true` only when the app accepts
the `i18n` helper (or ships `data_<lang>.json`) and localizes its visible
chrome. The badge surfaces a per-app Language override — if changing the
language changes nothing, don't fly it. Also enforced by
`test_app_conformance.py`.

**Don't filter characters "for safety."** The renderer degrades wall-aware at
the last moment: accents survive on reels that carry them, `é` folds to `E`
only where they don't, arrows `↑↓` degrade to `^v`, and colour squares
🟥🟧🟨🟩🟦🟪⬜ become colour flaps on a physical wall. An ASCII allow-set in the
app deletes characters the wall could have shown. If you must know what the
wall carries, ask `caps.can_show(ch)` — never reach into the host's internals.

---

## 12. Checklist & tips

- [ ] Folder `apps/<id>/` with a valid `manifest.json` (`name` + `type`).
- [ ] Functional: `app.py` defines `fetch(settings, format_lines, get_rows, get_cols)` returning a **list of pages**; each page from `format_lines(...)`.
- [ ] `surfaces` in the manifest matches the code: `["flap"]` → `fetch`; `["matrix"]` → `fetch_matrix(settings, canvas)`; both → both functions (see §7). Omit `surfaces` for a flap-only app.
- [ ] Channel: `data.json` with a `groups` list of **raw text** (the engine wraps and paginates it — don't pre-split lines). The legacy `pages` shape still loads.
- [ ] Quiz (`type: "quiz"`): `data.json` `groups` where every entry is a `[question, answer]` pair.
- [ ] Read grid size with `get_rows()/get_cols()` and lay out for at least a couple of shapes; set `min_rows`/`min_cols`/`min_modules` if it needs a minimum.
- [ ] Pick sensible `refresh_interval` (cache) and `loop_delay` (page dwell).
- [ ] Only `import` packages the companion ships (or add to `requirements.txt` for a built-in).
- [ ] Let network errors raise (you get OFFLINE/cached fallback) or catch and return a friendly page.
- [ ] Follow the [house rules](#11-house-rules) — the truthy/timezone snippets, honest minimums, no character filtering.
- [ ] The conformance tests (`backend/tests/test_plugins.py::test_every_app_loads`, `backend/tests/test_app_conformance.py`) load every app and check the contract — run `pytest` after adding a built-in.

For the formal compatibility contract (and the two places the companion
intentionally differs from splitflap-os — character normalization and vertical
centering), see [Compatibility](Compatibility.md).

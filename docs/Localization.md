# Languages & localization

The ecosystem is localized in **three places**, and they answer two different
questions: *what language is on the wall?* and *what language is the web page in
front of you?* The first is a setting on the display; the second follows whoever
is looking.

| Surface | What gets translated | Languages | Chosen by |
|---|---|---|---|
| [Companion](Companion.md) — app **content** | What the flaps show: weekday and month names, date order, 12h/24h time, number formats, holiday names, translated app words | 34 locales in the Language picker | The per-display **Language** setting (overridable per app and per playlist entry) |
| [Companion](Companion.md) — UI **chrome** | The web app itself: menus, buttons, settings forms, app names and descriptions in the store | English + French, German, Spanish today; more languages are data-only additions | Per viewer — a five-level chain, browser by default |
| [SplitFlap Gateway](SplitFlap-Gateway.md) web UI | The whole dashboard (Modules, Calibration, Settings…) | 14 — English plus 13 others | Per browser: `?lang=`, a Settings override, or Auto |
| [Matrix-Portal-Gateway](Matrix-Gateway.md) web UI | The whole dashboard | 13 | Same rules, resolved entirely in the browser |

---

## The companion: content

The per-display **Language** setting (Global settings) drives what apps put on
the flaps. Any app with a 🌐 badge adapts through the companion's `i18n`
helper: weekday and month names in the language's own words and case
(`lundi`, `Montag`), dates in the locale's own order (`July 9` vs `9 juillet`
vs `9. Juli`), 12h time in English and 24h everywhere else, numbers with the
right separators (`1,234.50` vs `1.234,50`), and translated labels. Channel
apps (no code) ship one page file per language instead.

Two things deliberately do **not** follow the Language:

- **Currency and public holidays follow your Location** — French is spoken in
  four currencies' worth of countries, so geography decides, down to
  province/state.
- **Case follows the wall** — apps write `Partly cloudy`; the companion folds
  it to capitals only for a wall with no lowercase flaps.

The picker offers **34 locales** — regional English (US/UK/Australia/Canada),
the Western-European languages with their regional variants (`fr-CA`, `de-AT`,
`pt-BR`…), the Nordics, and a handful more whose alphabets the flaps can carry.
Both Language and Location are overridable **per app** and **per playlist
entry**, so one playlist can show Paris in French and Berlin in German back to
back.

App authors: the `i18n` helper's API — `i18n.weekday()`, `i18n.date()`,
`i18n.number()`, `i18n.t()` and friends — is documented in
[Writing-Apps](Writing-Apps.md) §4.

## The companion: chrome

The web UI itself — menus, forms, the App Library — is translated separately,
because chrome has no reason to be a single server-side setting: two browsers
can each read it in their own language. The choice is made per viewer, first
match wins:

| Wins | Source | Set by | Scope |
|---|---|---|---|
| 1 | `?lang=fr` in the URL | whoever crafts the link | that tab |
| 2 | the global **Language** setting, *when explicitly saved* | the user, in Settings | the install |
| 3 | `COMPANION_UI_LANGUAGE` env var / `ui_language` add-on option | the operator | the deployment |
| 4 | Home Assistant's own language (the signed-in user's HA profile) | the HA user | that viewer, inside HA |
| 5 | `Accept-Language` — the browser | the browser | that viewer |

**"Explicitly saved"** matters because a fresh install is seeded with
`en-US` — untouched and chosen-en-US would otherwise look identical. The
setting only participates once the Language control has actually been saved
(a `language_explicit` flag records that); on older installs, a stored
language that differs from the default also counts, since someone picked it.
Until then, the chrome follows the viewer's browser.

Whichever level wins, the resolved code degrades **exact locale → base
language → English** (`fr-BE` → `fr` → `en`), and any individual string with
no translation falls back to English on its own — a partial catalog is a
supported state, never a broken page.

Chrome catalogs exist today for **French, German and Spanish**; adding another
language is a data-only contribution (below).

## Content vs chrome

The distinction runs through everything:

- **Content is per-display and reaches the flaps.** The weekday name on the
  wall is in the display's Language, for everyone in the room — the wall is
  shared hardware.
- **Chrome is per-browser.** The menus around the live view are in *your*
  language.

So a French wall viewed from a German phone shows German chrome over French
content — which is correct: the setting describes the display, the browser
describes the reader.

Content has one constraint chrome doesn't: **the reels**. Showing `É` needs a
flap with `É` printed on it. The gateway reports what its reels carry, and
anything the wall cannot show is degraded on the way out (`É` → `E`); what it
does carry, it keeps. See [Flaps-and-Character-Sets](Flaps-and-Character-Sets.md)
— and note the language lists across the ecosystem are scoped to the
Windows-1252 (Western-European) repertoire for exactly this reason.

---

## The gateway and Matrix Gateway dashboards

Both hardware dashboards translate themselves the same way they already pick
light or dark: **they follow your browser**, and there is nothing to
configure. The gateway speaks **English plus 13 other languages**:

| | |
|---|---|
| English | US *(built in)*, UK, Australia |
| Romance | French, Spanish, Italian, Portuguese (Portugal), Portuguese (Brazil) |
| Germanic | German, Dutch |
| Nordic | Danish, Swedish, Norwegian, Finnish |

The [Matrix Gateway](Matrix-Gateway.md) dashboard speaks 13 languages,
drawn from the same set.

The choice is resolved in the browser, first match wins:

1. **`?lang=<code>` in the URL** — wins over everything and is deliberately
   **not saved**, so the [Companion](Companion.md) can request a language for the
   gateway tabs it embeds without changing what *you* see. This is how the
   embedded gateway pages come up in the same language as the companion.
2. **Settings ▸ Language** — an explicit override, stored in your browser
   (`localStorage`), so it is per-device. The gateway itself keeps **no
   language state at all** — no config field, no API.
3. **Your browser** (`Auto`, the default). A region falls back to its base
   (`fr-CA` → `fr`); `en-GB` and `en-AU` browsers get British and Australian
   spelling automatically.
4. **English**, if nothing matches.

All languages ship in the **one firmware image** — switching never means
reflashing. Each language is a gzipped JSON dictionary fetched from
**`GET /lang/<code>`** only when it is the one in use; English downloads
nothing, because it *is* the text in the page. Untranslated strings fall back
to English individually, so partial dictionaries are safe. The **bus monitor
is never translated** — it shows protocol, not prose.

---

## Contributing a translation

Every catalog in the ecosystem is keyed by the **English string itself**, so
there are no key names to learn: copy the English file, translate the values,
open a PR. Missing entries fall back to English, so partial files are welcome.

### Companion — UI chrome

Add `backend/app/static/i18n/<lang>.json`: a flat
`{"English string": "translation"}` map. Copy `en.json` as the template. A CI
test asserts every language file's keys are a subset of `en.json`, so catalogs
can't silently drift from the code.

### Companion — app names, descriptions, settings labels

Store metadata never goes in `manifest.json` (that must stay a plain
splitflap-os manifest). Two layers, same shape:

| File | Covers | Wins |
|---|---|---|
| `backend/app/app_i18n/<lang>.json` | the whole built-in app library, one file per language, keyed by app id | |
| `apps/<id>/i18n/<lang>.json` | one app — travels inside an uploaded `.zip`, validated at upload | over the central file |

Recognised keys per app: `name`, `description`, `flap_name`, and `settings`
(a map of setting keys to translated labels). These follow the **viewer's
chrome language**; the one exception is `flap_name`, used when an app's name
is rendered *onto the flaps* — that follows the content Language and the
reel's character set.

### Companion — app content

Functional apps translate through `i18n.t()`; the words live in
`backend/app/i18n_data.json` (translations, holiday names, per-language
defaults). Channel apps ship `data_<lang>.json` sidecars next to `data.json`.
Both are covered in [Writing-Apps](Writing-Apps.md) §4–5.

### Gateway and Matrix Gateway

Edit (or add) `ui/strings/<code>.json` — keys are the English strings. Then
consult **`ui/strings/CONTEXT.md`**, generated by `tools/i18n_context.py`: it
lists, for every string, *where it appears* (which tab, whether it's a button,
a form label, a tooltip, a heading) and its grammatical role — in this UI
**Home** is a verb, **Flap** is the physical leaf on the reel, and buttons
take the imperative. The same English word is often a different part of speech
in different places, and CONTEXT.md is what keeps a translation from guessing.

Validate with `tools/i18n_check.py` (unknown keys, dropped product name,
non-Windows-1252 characters); `node tools/i18n_test.js` covers the
language-matching rules. On the gateway, `python3 tools/build_ui.py` then
regenerates `src/web_ui.h` — never edit that file by hand.

---

## Canonical sources

| What | Where |
|---|---|
| Companion chrome i18n design & record | [docs/UI_I18N_PLAN.md](https://github.com/avandeputte/SplitFlapGatewayCompanion/blob/main/docs/UI_I18N_PLAN.md) |
| Companion chrome catalogs | [backend/app/static/i18n/](https://github.com/avandeputte/SplitFlapGatewayCompanion/tree/main/backend/app/static/i18n) |
| Companion app-metadata catalogs | [backend/app/app_i18n/](https://github.com/avandeputte/SplitFlapGatewayCompanion/tree/main/backend/app/app_i18n) |
| Companion content translations & language list | [backend/app/i18n_data.json](https://github.com/avandeputte/SplitFlapGatewayCompanion/blob/main/backend/app/i18n_data.json) |
| Gateway dictionaries & translator context | [ui/strings/](https://github.com/avandeputte/SplitFlapGateway/tree/main/ui/strings) · [README § Language](https://github.com/avandeputte/SplitFlapGateway/blob/main/README.md#language) |
| Matrix Gateway dictionaries & translator context | [ui/strings/](https://github.com/avandeputte/MatrixPortalGateway/tree/main/ui/strings) · [README § Language](https://github.com/avandeputte/MatrixPortalGateway/blob/main/README.md#language) |

---
**Next:** [Writing-Apps](Writing-Apps.md) · [Flaps-and-Character-Sets](Flaps-and-Character-Sets.md) · [SplitFlap Gateway](SplitFlap-Gateway.md) · [Matrix-Portal-Gateway](Matrix-Gateway.md)

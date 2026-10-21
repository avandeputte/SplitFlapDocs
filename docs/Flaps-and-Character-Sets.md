# Flaps & character sets

**What's printed on your reels is your choice — and the firmware adapts to it.**

On Adam's original firmware the character set is fixed: the reel is what the firmware
expects, and that's that. The **[Universal Firmware](Module-Firmware.md)** (v31+) makes both
the **flap count** and the **character set** *configurable per module* and stores them in
the module's EEPROM. That's what lets you print a reel with `É`, `Ö` or `Ñ` on it — or a
reel with no punctuation at all — and have text land on the right flap.

This is one of the bigger differentiators of the Universal Firmware, and it's what makes
the companion's **[localization](Companion.md#localization)** actually show up on the wall
rather than as blanks.

## How it works

Each module stores two things you can change:

| | |
|---|---|
| **Flap count** | `1`–`64`. It drives the step maths (`index × totalSteps ÷ count`), so it must match the real reel. |
| **Character set** | The ordered character at each flap index. Index `0` is always the **blank / home** flap. |

Send a character (`m<ID>-É`) and the module looks it up in *its* set and turns to that
flap. If the character isn't on the reel, the module **homes** — a visible, predictable
"I can't show that" rather than silence.

**Setting it** — easiest from the **[Gateway's](SplitFlap-Gateway.md) Modules tab** (**ℹ Info** → *Flap
Set*, on v31+ modules). Over the bus it's the `N` command, which works direct, **by
broadcast** (configure a whole wall in one shot) or by serial number:

```text
m<ID>N<count>:<chars>      one module
m*N<count>:<chars>         every module on the bus
```

Both parts are independent — set the count, the characters, or both. They persist in
EEPROM and survive a reflash (as long as you wrote the `EESAVE` fuse; see
[Module Firmware](Module-Firmware.md#1-flash)).

## Symbol flaps *(gateway v4.1)*

Some reels are printed with symbols — a heart, arrows, a smiley. The bus carries exactly one
byte per flap and addresses a module **by** that byte, and those symbols have no Windows-1252
code, so each one travels as a **reserved lowercase letter** — the same arrangement the seven
colour flaps (`r o y g b p w`) and the classic reel's double-quote flap (`q`) already use.

| Symbol | Letter on the wire | Name | Stand-in | Also accepted |
|---|---|---|---|---|
| ♥ | `h` | heart | `*` | ❤ |
| ↑ | `u` | up | `^` | ⬆ |
| ↓ | `d` | down | `V` | ⬇ |
| ☺ | `s` | smiley | `:` | 🙂 😊 😀 |
| ← | `l` | left | `<` | ⬅ |
| → | `t` | right | `>` | ➡ |

**You never type the letters.** Paste the symbol into the Flap Set editor, or use the palette
of symbols and colours beside the field, and the gateway stores the letter for you. Send `♥` to
a module through the API, MQTT or the dashboard and it reaches the heart flap; ask the gateway
what a module is showing and it answers `♥`.

**A typed letter is still a letter.** `h` goes out as `H`, exactly as before — every client
that sends lowercase text depends on that. Only `♥` (or one of the shapes in the last column)
means the heart.

**A symbol exists only where it is printed.** Each character is resolved against the reel of the
module it lands on, so on a wall where one module carries the heart and the rest do not, `A♥B`
puts the heart on that module and the stand-in (`*`) on any other — one glyph per module either
way, so nothing shifts. A reel with neither the symbol nor its stand-in shows a blank.

**Which modules carry what:** `GET /api/capabilities` reports the symbols in `charset.union`
(some reel has it) and `charset.common` (every reel has it), names them in `pictographs`, and
gives the wire byte for each in `spelling`. The raw frame paths still take the letter:
`m5-h` shows the heart on module 5.

Needs **gateway 4.1 or later** — an older gateway stores the letters but reports them as
lowercase letters. Module firmware needs no change at all: a v31+ module stores and reports
whatever bytes its flap set holds.

## The 64-flap budget

A reel holds at most **64** flaps, so a character set is a zero-sum choice. The fixed
costs:

| Slot | Count |
|---|---|
| Blank / home flap (index 0) | 1 |
| `A`–`Z` | 26 |
| `0`–`9` | 10 |
| Colour flaps `r o y g b p w` | 7 |
| **Subtotal** | **44** |
| **Left for punctuation + accents + currency** | **20** |

So every accented letter you print costs you a punctuation mark or a colour flap — and so does
every [symbol flap](#symbol-flaps-gateway-v41): a heart and two arrows are three of those
twenty slots, which is why the gateway falls back to a stand-in on the reels that spent them
elsewhere.
Thirteen French accents (`ÀÂÇÈÉÊËÎÏÔÙÛÜ`) eat most of the budget on their own.

## The default (English) set

This is what a module ships with — no accents, a full punctuation run, all seven colours:

```text
 ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$&()-+=;q:%'.,/?*roygbpw
```

*(In printed listings a `q` in the punctuation run stands in for the double-quote flap.)*

**If you don't want accents, stop here — use the default set.** Nothing else in the stack
requires them. The companion will simply blank (or home) anything your reel can't show.

## Starter sets by locale

A starting point, **not a prescription** — what you print is 100% up to you. Each row below
is exactly 64 unique flaps, all printable on a Windows-1252 wall, built as:

> blank + `A–Z` + the locale's accents + `0–9` + its currency symbol + as much punctuation
> as still fits + the seven colour flaps

| Locale | Language | Accents | 64-flap set (`␣` = the blank / home flap, index 0) |
|---|---|:-:|---|
| `en-US` | English (US) | 0 | `␣ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$!?.,'-:%&()@#+=/;*"roygbpw` |
| `en-GB` | English (UK) | 0 | `␣ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789£!?.,'-:%&()@#+=/;*"roygbpw` |
| `fr-FR` | French | 13 | `␣ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÇÈÉÊËÎÏÔÙÛÜ0123456789€!?.,'-roygbpw` |
| `de-DE` | German | 4 | `␣ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß0123456789€!?.,'-:%&()@#+=roygbpw` |
| `es-ES` | Spanish | 7 | `␣ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÑÓÚÜ0123456789€!?.,'-:%&()@roygbpw` |
| `it-IT` | Italian | 6 | `␣ABCDEFGHIJKLMNOPQRSTUVWXYZÀÈÉÌÒÙ0123456789€!?.,'-:%&()@#roygbpw` |
| `pt-PT` | Portuguese | 12 | `␣ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÇÉÊÍÓÔÕÚ0123456789€!?.,'-:roygbpw` |
| `nl-NL` | Dutch | 7 | `␣ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉËÍÓÚÜ0123456789€!?.,'-:%&()@roygbpw` |
| `sv-SE` | Swedish | 3 | `␣ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ0123456789€!?.,'-:%&()@#+=/roygbpw` |
| `da-DK` | Danish | 3 | `␣ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ0123456789€!?.,'-:%&()@#+=/roygbpw` |
| `nb-NO` | Norwegian | 3 | `␣ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ0123456789€!?.,'-:%&()@#+=/roygbpw` |
| `fi-FI` | Finnish | 3 | `␣ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÅ0123456789€!?.,'-:%&()@#+=/roygbpw` |

Trim or reorder freely: drop the colour flaps to buy four more accents, drop `@ # % &` if
you never show them, or print a 40-flap reel and set `count` to 40. The firmware only
needs the count and the set to *match what you actually printed*.

## How this relates to the rest of the stack

- **[Companion](Companion.md) localization** picks the *words* (French app text, `9 juillet`,
  `1 234,50`). Whether those words can be *shown* depends on your reels. Language and
  flaps are independent settings — set both.
- Text is handled as **Windows-1252**, which is why the character sets above stay inside
  that code page.

## What happens to a character your reel doesn't have

A split-flap fails quietly. Send a module a character that is not printed on its reel and it
does not complain and does not substitute — it **homes**. You get a blank cell in the middle
of a word, and nothing anywhere reports it.

The gateway now tells the companion what it can show (`GET /api/capabilities`, asked on boot
and on every resync — it knows, because it is the thing that configures the modules). On a
**mixed wall** it reports the *intersection*: a character only half your modules carry is a
character that will punch holes in the other half.

So the companion doesn't send a character and hope. What your reel cannot show becomes the
nearest thing it can:

| the app sends | your reel has no… | you get |
|---|---|---|
| `Åre` | `Å` | `ARE` — the accent goes, the word survives |
| `Dinner — 7pm` | em dash | `DINNER - 7PM` |
| `15:30` | colon (the `fr-FR` reel has none) | `15.30` |
| `♥` | the heart flap | `*` — the gateway's stand-in; a blank if the reel has no `*` either. A reel printed **with** ♥ shows it ([symbol flaps](#symbol-flaps-gateway-v41)) |
| `Straße` | `ß` | `STRASSE` — **two** flaps, the documented German fallback |

**ß is the interesting one.** A reel that carries it carries only the *lowercase* form — there
is no uppercase `ẞ` flap — so an all-caps German page correctly shows `STRAßE`, and that is not
a bug. Only a reel with no `ß` at all falls back to `SS`, which costs a second module: the
substitution therefore happens while the text is still text, before it is centred, so the line
is wrapped knowing it got longer. (A single `S` is not a shorter spelling of `SS`; it is a
misspelling.)

And what your reel *does* have, it keeps: on the French reel above, `Prévu` goes out as
**`PRÉVU`**, accent and all. That is what those thirteen accent flaps are for.

If a gateway is too old to answer, the companion sends the character and
the module does what it does.

## Case: the wall decides, not the app

An app writes its words the way a person writes them — `Partly cloudy`, not `PARTLY CLOUDY`.
The **companion folds them to capitals on the way out**, and only for a wall that has no
lowercase flaps. So the same app feeds both kinds of display:

| the app produces | a split-flap shows | a Matrix Gateway shows |
|---|---|---|
| `It's five past three` | `IT'S FIVE PAST THREE` | `It's five past three` |

If you own a physical wall, nothing about this is visible to you — a split-flap shows plain uppercase, byte for byte. If you'd rather a Matrix Gateway shouted anyway (it is, after all, what a
split-flap *looks* like), turn on **Always uppercase** in the companion's global settings, per
display.

## The extra flaps on a Matrix Gateway

A **[Matrix Gateway](Matrix-Gateway.md)** has no printed flaps at all — its virtual
reels carry **237** of them, so on top of the full Windows-1252 set it has the 60 lowercase
letters and **14 pictographs**:

| | | |
|---|---|---|
| `♥` heart | `♦` diamond | `♣` club |
| `♠` spade | `☀` sun | `☺` smiley |
| `♪` note | `●` dot | `■` block |
| `⌂` house | `←` `↑` `→` `↓` | the four arrows |

Apps use them only when the wall has them. Ask the display what it can do (see
[Writing Apps](Writing-Apps.md))
and fall back when it can't: the arrows degrade to `< ^ > v`, which still read; a heart has no
honest substitute, so an app that wants one has to check first.

The seven **colours** work on both, but differently. On a physical wall a colour is spelled
with a letter — `r` is the red flap, which is exactly why lowercase `r` cannot also be the
letter. A Matrix Gateway names its colours instead, so it keeps both.

---
**Next:** [Module Firmware](Module-Firmware.md) · [Companion](Companion.md)

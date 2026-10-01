# Built-in Apps

The companion ships **its own library** of ready-to-run apps. One tap on a tile runs an
app; the [App Library](Companion.md) adds or removes them; and you can
[write your own](Writing-Apps.md).

> ⚠️ **This page is a tour, not an inventory.** The app ecosystem is always
> changing — apps are added, gain settings, and improve all the time, and this
> list is a snapshot. **Always check the App Library inside the companion**
> (Apps tab → App Library) for what your install actually offers: it is the
> source of truth, and it's where new apps appear first.

**Badges:** 🌐 adapts to the global **Language** (translated text, local date &
number formats) · ⚡ has a **trigger** mode — it can watch for a condition and
briefly interrupt the display when it fires · 🎞 **animation** (color frames)
· 🎨 **Matrix-panel-only** — draws graphics straight onto a
[Matrix Gateway](Matrix-Gateway.md)'s LED panel and won't appear on a physical flap
display · 🔑 needs an **API key**. *Min wall* is the smallest flap wall the app
accepts, rows × columns.

### Every app runs on both displays

Nearly every functional app is **dual-surface**: the same app, off one shared configuration,
spells its text on a physical flap wall *and* draws a **rich panel view** on a Matrix
Gateway — adapting to whatever surface it is given, from a big 256×64 panel down to
64×32, and from a tall five-row flap wall down to a slim two-row one. On a Matrix-panel
display, each app's settings open with a **Show on Matrix panel** toggle at the top — on
by default; flip it off to keep that app on flap-style text. (The toggle only appears on
Matrix-panel displays, and a playlist entry can override it per entry.)

The screenshots below are rendered straight from the app code with sample data — the
Matrix view at four panel resolutions and the flap view at three wall heights. They live
in the repo's [screenshots gallery](https://github.com/avandeputte/SplitFlapGatewayCompanion/tree/main/screenshots).

### Matrix-panel-only apps

A few apps (🎨) drive the panel as a raw LED **canvas** — arbitrary graphics, free of the
flap grid. They need a Matrix wall and won't appear on a physical flap display. See
[Writing Apps → Canvas apps](Writing-Matrix-Apps.md) to
build your own.

### Channels and quizzes on the panel

A **channel** or **quiz** app (jokes, quotes, fortunes …) shows as text on the flaps; on
a Matrix panel it renders as **large text beside a themed icon** (the manifest's
`canvas_art` names the icon — a clapperboard for Movie Quotes, a moon for Good Night, the
🥠 for the fortune cookies). A line too long to stay readable on a short panel splits
across screens rather than shrinking the type. A **quiz** shows its two screens in turn:
the question, then — after the page delay — the answer.

---

## Advice

A random piece of advice.  
*min wall 2×15*

| | |
|---|---|
| ![Advice — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/advice.png)<br>Matrix 256 × 64 | ![Advice — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/advice.png)<br>Matrix 128 × 64 |
| ![Advice — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/advice.png)<br>Matrix 128 × 32 | ![Advice — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/advice.png)<br>Matrix 64 × 32 |
| ![Advice — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/advice.png)<br>Flap wall 3 × 15 | ![Advice — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/advice.png)<br>Flap wall 5 × 15 |
| ![Advice — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/advice.png)<br>Flap wall 2 × 15 |  |

## Animation

Plays a looping animation (e.g. a GIF), uploaded to the panel **once** and then run on-device from PSRAM — the companion can disconnect and it keeps looping.  
*🎨🎞*

*Matrix panel only — no screenshot yet.*

## Photo Frame

A slideshow of the photos — and **MPGA movies**, streamed by the
wall straight off the card — on the gateway's microSD card: drop files onto the card
from the gateway's **Files** tab and the panel rotates through them. Photos fill or
letterbox (on a dim blurred echo of the photo), optional shuffle, EXIF rotation honored;
movies loop on-device for their turn. Matrix-only.
*🎨*

## Aquarium

An animated reef — fish drift and dart across the panel. It draws on the compositing surface: additive **godrays** shimmering down from the surface,
anti-aliased weeds, and a soft **glow** around the bubbles. Purely decorative.  
*🎨*

*Matrix panel only — no screenshot yet.*

## Art Clock

The time drawn in color art.  
*🎞 · min wall 3×15*

*An animation — best seen in motion; no static screenshot.*

## Aurora Watch

Geomagnetic activity (Kp index) with a severity color — will you see the aurora tonight?  
*🌐 · min wall 1×12*

| | |
|---|---|
| ![Aurora Watch — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/aurora.png)<br>Matrix 256 × 64 | ![Aurora Watch — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/aurora.png)<br>Matrix 128 × 64 |
| ![Aurora Watch — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/aurora.png)<br>Matrix 128 × 32 | ![Aurora Watch — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/aurora.png)<br>Matrix 64 × 32 |
| ![Aurora Watch — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/aurora.png)<br>Flap wall 3 × 15 | ![Aurora Watch — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/aurora.png)<br>Flap wall 5 × 15 |
| ![Aurora Watch — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/aurora.png)<br>Flap wall 2 × 15 |  |

## Binary Clock

The time as a classic BCD binary clock — color flaps as bits, colors for 1 and 0 yours to pick. Seconds on a Matrix Gateway.  
*min wall 4×8*

| | |
|---|---|
| ![Binary Clock — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/binary-clock.png)<br>Matrix 256 × 64 | ![Binary Clock — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/binary-clock.png)<br>Matrix 128 × 64 |
| ![Binary Clock — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/binary-clock.png)<br>Matrix 128 × 32 | ![Binary Clock — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/binary-clock.png)<br>Matrix 64 × 32 |
| ![Binary Clock — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/binary-clock.png)<br>Flap wall 3 × 15 | ![Binary Clock — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/binary-clock.png)<br>Flap wall 5 × 15 |
| ![Binary Clock — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/binary-clock.png)<br>Flap wall 2 × 15 |  |

## BirdNET

Live bird detections from a BirdNET-Pi on your network.  
*⚡ · min wall 1×10*

| | |
|---|---|
| ![BirdNET — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/birdnet.png)<br>Matrix 256 × 64 | ![BirdNET — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/birdnet.png)<br>Matrix 128 × 64 |
| ![BirdNET — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/birdnet.png)<br>Matrix 128 × 32 | ![BirdNET — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/birdnet.png)<br>Matrix 64 × 32 |
| ![BirdNET — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/birdnet.png)<br>Flap wall 3 × 15 | ![BirdNET — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/birdnet.png)<br>Flap wall 5 × 15 |
| ![BirdNET — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/birdnet.png)<br>Flap wall 2 × 15 |  |

## BTC Fear & Greed

The Bitcoin Fear & Greed index, with a sentiment color.  
*🌐⚡ · min wall 1×14*

| | |
|---|---|
| ![BTC Fear & Greed — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/bitcoin-fear-greed.png)<br>Matrix 256 × 64 | ![BTC Fear & Greed — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/bitcoin-fear-greed.png)<br>Matrix 128 × 64 |
| ![BTC Fear & Greed — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/bitcoin-fear-greed.png)<br>Matrix 128 × 32 | ![BTC Fear & Greed — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/bitcoin-fear-greed.png)<br>Matrix 64 × 32 |
| ![BTC Fear & Greed — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/bitcoin-fear-greed.png)<br>Flap wall 3 × 15 | ![BTC Fear & Greed — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/bitcoin-fear-greed.png)<br>Flap wall 5 × 15 |
| ![BTC Fear & Greed — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/bitcoin-fear-greed.png)<br>Flap wall 2 × 15 |  |

## Calendar

Your next events from iCal feeds (Google, Apple, …), recurring events included.  
*🌐 · min wall 2×12*

| | |
|---|---|
| ![Calendar — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/calendar.png)<br>Matrix 256 × 64 | ![Calendar — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/calendar.png)<br>Matrix 128 × 64 |
| ![Calendar — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/calendar.png)<br>Matrix 128 × 32 | ![Calendar — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/calendar.png)<br>Matrix 64 × 32 |
| ![Calendar — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/calendar.png)<br>Flap wall 3 × 15 | ![Calendar — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/calendar.png)<br>Flap wall 5 × 15 |
| ![Calendar — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/calendar.png)<br>Flap wall 2 × 15 |  |

## Cat Facts

A concise cat fact.  
*min wall 3×15*

| | |
|---|---|
| ![Cat Facts — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/cat-facts.png)<br>Matrix 256 × 64 | ![Cat Facts — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/cat-facts.png)<br>Matrix 128 × 64 |
| ![Cat Facts — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/cat-facts.png)<br>Matrix 128 × 32 | ![Cat Facts — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/cat-facts.png)<br>Matrix 64 × 32 |
| ![Cat Facts — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/cat-facts.png)<br>Flap wall 3 × 15 | ![Cat Facts — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/cat-facts.png)<br>Flap wall 5 × 15 |
| ![Cat Facts — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/cat-facts.png)<br>Flap wall 2 × 15 |  |

## Checker

A checkerboard.  
*🎞 · min wall 1×1*

*An animation — best seen in motion; no static screenshot.*

## Breakout

Paddle, ball and rainbow bricks: bricks score by row, the paddle repaints the ball's
angle by where it lands, and clearing the wall deals the next level a step faster.
Three lives with a READY? hold between them; on a compositing wall the ball wears a
soft additive glow. Plays itself (with a fallible demo paddle) until you take over —
left/right steer, up launches.
*👾 · interactive*

## Chomper

A Pac-Man-style maze chase the panel plays by itself — classic one-cell corridors and
thin walls randomized fresh every level, all loops (nowhere to get cornered), wrap-around
side tunnels plus a vertical one, pellets, blinking power-ups, ghosts that turn blue and
flee when one is eaten, with lives, levels and a score that carry on forever. Drawn entirely with **on-device draw ops** — the chomper is a
filled `arc` whose mouth opens and shuts as it runs, the ghosts wear `poly` skirts
 — and streamed as **binary ops** for
game-rate latency. **Playable:** while it runs, an on-screen D-pad appears under the Live
Display (arrow keys / WASD too); grab it and you steer the chomper live, with tones on the
gateway speaker. Let go and it drifts back to playing itself.  
*🎨 · playable*

| | |
|---|---|
| ![Chomper — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/canvas-chomper.png)<br>Matrix 256 × 64 | ![Chomper — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/canvas-chomper.png)<br>Matrix 128 × 64 |
| ![Chomper — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/canvas-chomper.png)<br>Matrix 128 × 32 | ![Chomper — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/canvas-chomper.png)<br>Matrix 64 × 32 |

## Chuck Norris

Chuck Norris facts.  
*min wall 3×10*

| | |
|---|---|
| ![Chuck Norris — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/chuck-norris.png)<br>Matrix 256 × 64 | ![Chuck Norris — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/chuck-norris.png)<br>Matrix 128 × 64 |
| ![Chuck Norris — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/chuck-norris.png)<br>Matrix 128 × 32 | ![Chuck Norris — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/chuck-norris.png)<br>Matrix 64 × 32 |
| ![Chuck Norris — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/chuck-norris.png)<br>Flap wall 3 × 15 | ![Chuck Norris — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/chuck-norris.png)<br>Flap wall 5 × 15 |
| ![Chuck Norris — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/chuck-norris.png)<br>Flap wall 2 × 15 |  |

## Comments

Latest comments on your videos.  
*⚡🔑 · min wall 2×10*

| | |
|---|---|
| ![Comments — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/yt_comments.png)<br>Matrix 256 × 64 | ![Comments — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/yt_comments.png)<br>Matrix 128 × 64 |
| ![Comments — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/yt_comments.png)<br>Matrix 128 × 32 | ![Comments — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/yt_comments.png)<br>Matrix 64 × 32 |
| ![Comments — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/yt_comments.png)<br>Flap wall 3 × 15 | ![Comments — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/yt_comments.png)<br>Flap wall 5 × 15 |
| ![Comments — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/yt_comments.png)<br>Flap wall 2 × 15 |  |

## Countdown

A timer to a moment you pick (up to five at once). On walls five rows or taller, each unit gets its own row with a color bar of how much of its cycle remains. On a Matrix panel: full-width draining color bars. Optional seconds on a Matrix Gateway.  
*🌐⚡ · min wall 1×6*

| | |
|---|---|
| ![Countdown — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/countdown.png)<br>Matrix 256 × 64 | ![Countdown — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/countdown.png)<br>Matrix 128 × 64 |
| ![Countdown — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/countdown.png)<br>Matrix 128 × 32 | ![Countdown — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/countdown.png)<br>Matrix 64 × 32 |
| ![Countdown — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/countdown.png)<br>Flap wall 3 × 15 | ![Countdown — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/countdown.png)<br>Flap wall 5 × 15 |
| ![Countdown — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/countdown.png)<br>Flap wall 2 × 15 |  |

## Crypto

Coin prices, shown by ticker (BTC, ETH, …).  
*🌐⚡ · min wall 1×13*

| | |
|---|---|
| ![Crypto — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/crypto.png)<br>Matrix 256 × 64 | ![Crypto — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/crypto.png)<br>Matrix 128 × 64 |
| ![Crypto — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/crypto.png)<br>Matrix 128 × 32 | ![Crypto — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/crypto.png)<br>Matrix 64 × 32 |
| ![Crypto — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/crypto.png)<br>Flap wall 3 × 15 | ![Crypto — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/crypto.png)<br>Flap wall 5 × 15 |
| ![Crypto — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/crypto.png)<br>Flap wall 2 × 15 |  |

## Dad Jokes (quiz)

A question, then the punchline — a two-screen *quiz* reveal.  
*🌐 · min wall 3×15*

| | |
|---|---|
| ![Dad Jokes — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/dad-jokes.png)<br>Matrix 256 × 64 | ![Dad Jokes — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/dad-jokes.png)<br>Matrix 128 × 64 |
| ![Dad Jokes — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/dad-jokes.png)<br>Matrix 128 × 32 | ![Dad Jokes — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/dad-jokes.png)<br>Matrix 64 × 32 |
| ![Dad Jokes — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/dad-jokes.png)<br>Flap wall 3 × 15 | ![Dad Jokes — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/dad-jokes.png)<br>Flap wall 5 × 15 |
| ![Dad Jokes — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/dad-jokes.png)<br>Flap wall 2 × 15 |  |

## Dashboard

Time + weather on one screen. On a tall wall (5+ rows) it drops both onto one dense page that spreads to the edges, instead of two sparse pages. On a Matrix panel: the full overview card — big clock, date, weather column, seconds sweep.  
*🌐 · min wall 3×12*

| | |
|---|---|
| ![Dashboard — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/dashboard.png)<br>Matrix 256 × 64 | ![Dashboard — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/dashboard.png)<br>Matrix 128 × 64 |
| ![Dashboard — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/dashboard.png)<br>Matrix 128 × 32 | ![Dashboard — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/dashboard.png)<br>Matrix 64 × 32 |
| ![Dashboard — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/dashboard.png)<br>Flap wall 3 × 15 | ![Dashboard — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/dashboard.png)<br>Flap wall 5 × 15 |
| ![Dashboard — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/dashboard.png)<br>Flap wall 2 × 15 |  |

## Date

The full date, laid out for your wall. On a Matrix panel: the full Date Card — big day numeral, weekday accent, facts column, year-progress bar.  
*🌐 · min wall 2×10*

| | |
|---|---|
| ![Date — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/date.png)<br>Matrix 256 × 64 | ![Date — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/date.png)<br>Matrix 128 × 64 |
| ![Date — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/date.png)<br>Matrix 128 × 32 | ![Date — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/date.png)<br>Matrix 64 × 32 |
| ![Date — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/date.png)<br>Flap wall 3 × 15 | ![Date — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/date.png)<br>Flap wall 5 × 15 |
| ![Date — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/date.png)<br>Flap wall 2 × 15 |  |

## Dog Facts

A concise dog fact.  
*min wall 3×15*

| | |
|---|---|
| ![Dog Facts — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/dog-facts.png)<br>Matrix 256 × 64 | ![Dog Facts — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/dog-facts.png)<br>Matrix 128 × 64 |
| ![Dog Facts — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/dog-facts.png)<br>Matrix 128 × 32 | ![Dog Facts — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/dog-facts.png)<br>Matrix 64 × 32 |
| ![Dog Facts — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/dog-facts.png)<br>Flap wall 3 × 15 | ![Dog Facts — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/dog-facts.png)<br>Flap wall 5 × 15 |
| ![Dog Facts — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/dog-facts.png)<br>Flap wall 2 × 15 |  |

## Earthquakes

Recent significant earthquakes (USGS), color-coded by magnitude.  
*🌐 · min wall 1×12*

| | |
|---|---|
| ![Earthquakes — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/earthquakes.png)<br>Matrix 256 × 64 | ![Earthquakes — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/earthquakes.png)<br>Matrix 128 × 64 |
| ![Earthquakes — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/earthquakes.png)<br>Matrix 128 × 32 | ![Earthquakes — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/earthquakes.png)<br>Matrix 64 × 32 |
| ![Earthquakes — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/earthquakes.png)<br>Flap wall 3 × 15 | ![Earthquakes — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/earthquakes.png)<br>Flap wall 5 × 15 |
| ![Earthquakes — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/earthquakes.png)<br>Flap wall 2 × 15 |  |

## Effects

On-device panel effects — **plasma**, **fire**, **matrix** rain, **flip-o-rama**, **clock**,
Conway's **Life**, the audio-reactive **spectrum** analyzer, **soundwall**, **beat ripples**,
an **oscilloscope** tracing the live mic waveform, a scrolling **spectrogram** waterfall, and
a self-carving **maze** — rendered by the panel itself at its native frame rate, with nothing
on the network. One app per effect the wall advertises, and each app's knobs come from the
wall's **own description** of that effect (`effectDefs`): speed, hue, density, or an
**Audio reactive** toggle, exactly where the effect supports them — a future firmware effect
or option appears with no companion update.
*🎨*

## Exchange Rates

Live currency rates (ECB).  
*🌐 · min wall 1×12*

| | |
|---|---|
| ![Exchange Rates — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/exchange-rates.png)<br>Matrix 256 × 64 | ![Exchange Rates — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/exchange-rates.png)<br>Matrix 128 × 64 |
| ![Exchange Rates — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/exchange-rates.png)<br>Matrix 128 × 32 | ![Exchange Rates — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/exchange-rates.png)<br>Matrix 64 × 32 |
| ![Exchange Rates — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/exchange-rates.png)<br>Flap wall 3 × 15 | ![Exchange Rates — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/exchange-rates.png)<br>Flap wall 5 × 15 |
| ![Exchange Rates — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/exchange-rates.png)<br>Flap wall 2 × 15 |  |

## Falling Sand

Not a game, a toy: grains pour from a wandering spout, tumble down the slopes and
settle into layered dunes whose colors drift around the hue wheel — slow sediment
bands, one grain per LED. Take the pad and left/right steer the pour; any key dumps
a burst. When the pile swallows the panel it fades out and pours again.
*⏳ · interactive*

## Flappy

The one-button side-scroller: gravity pulls the bird down, **any key flaps**, pipes
scroll in and passing a pair scores. It plays itself (flapping toward the next gap)
until you press; hit anything and it's a fade-to-black GAME OVER — the next press
deals again.
*🐤 · interactive*

## Forecast Ribbon

The day's temperature curve as a color bar chart.  
*🎞 · min wall 3×8*

*An animation — best seen in motion; no static screenshot.*

## Formula 1

The next Grand Prix & championship leader.  
*🌐 · min wall 2×12*

| | |
|---|---|
| ![Formula 1 — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/formula1.png)<br>Matrix 256 × 64 | ![Formula 1 — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/formula1.png)<br>Matrix 128 × 64 |
| ![Formula 1 — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/formula1.png)<br>Matrix 128 × 32 | ![Formula 1 — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/formula1.png)<br>Matrix 64 × 32 |
| ![Formula 1 — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/formula1.png)<br>Flap wall 3 × 15 | ![Formula 1 — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/formula1.png)<br>Flap wall 5 × 15 |
| ![Formula 1 — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/formula1.png)<br>Flap wall 2 × 15 |  |

## Fortune Cookie (channel)

A fortune without the cookie.  
*🌐 · min wall 3×15*

| | |
|---|---|
| ![Fortune Cookie — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/fortune-cookie.png)<br>Matrix 256 × 64 | ![Fortune Cookie — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/fortune-cookie.png)<br>Matrix 128 × 64 |
| ![Fortune Cookie — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/fortune-cookie.png)<br>Matrix 128 × 32 | ![Fortune Cookie — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/fortune-cookie.png)<br>Matrix 64 × 32 |
| ![Fortune Cookie — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/fortune-cookie.png)<br>Flap wall 3 × 15 | ![Fortune Cookie — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/fortune-cookie.png)<br>Flap wall 5 × 15 |
| ![Fortune Cookie — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/fortune-cookie.png)<br>Flap wall 2 × 15 |  |

## Good Morning (channel)

A morning pick-me-up.  
*🌐 · min wall 3×15*

| | |
|---|---|
| ![Good Morning — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/good-morning.png)<br>Matrix 256 × 64 | ![Good Morning — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/good-morning.png)<br>Matrix 128 × 64 |
| ![Good Morning — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/good-morning.png)<br>Matrix 128 × 32 | ![Good Morning — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/good-morning.png)<br>Matrix 64 × 32 |
| ![Good Morning — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/good-morning.png)<br>Flap wall 3 × 15 | ![Good Morning — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/good-morning.png)<br>Flap wall 5 × 15 |
| ![Good Morning — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/good-morning.png)<br>Flap wall 2 × 15 |  |

## Good Night (channel)

An evening wind-down.  
*🌐 · min wall 3×15*

| | |
|---|---|
| ![Good Night — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/good-night.png)<br>Matrix 256 × 64 | ![Good Night — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/good-night.png)<br>Matrix 128 × 64 |
| ![Good Night — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/good-night.png)<br>Matrix 128 × 32 | ![Good Night — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/good-night.png)<br>Matrix 64 × 32 |
| ![Good Night — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/good-night.png)<br>Flap wall 3 × 15 | ![Good Night — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/good-night.png)<br>Flap wall 5 × 15 |
| ![Good Night — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/good-night.png)<br>Flap wall 2 × 15 |  |

## Harry Potter (channel)

Wizarding wisdom.  
*min wall 3×15*

| | |
|---|---|
| ![Harry Potter — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/harry-potter-quotes.png)<br>Matrix 256 × 64 | ![Harry Potter — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/harry-potter-quotes.png)<br>Matrix 128 × 64 |
| ![Harry Potter — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/harry-potter-quotes.png)<br>Matrix 128 × 32 | ![Harry Potter — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/harry-potter-quotes.png)<br>Matrix 64 × 32 |
| ![Harry Potter — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/harry-potter-quotes.png)<br>Flap wall 3 × 15 | ![Harry Potter — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/harry-potter-quotes.png)<br>Flap wall 5 × 15 |
| ![Harry Potter — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/harry-potter-quotes.png)<br>Flap wall 2 × 15 |  |

## Home Assistant

Your Home Assistant entity states, one row per entity — renamed, reordered and thresholded as you choose, with a green / amber / red color flap for on-states and numeric bands. Automatic in the add-on; standalone Docker sets `COMPANION_HA_URL` + `COMPANION_HA_TOKEN`. On a Matrix panel: a grid of entity cards with device icons — and a thresholded numeric entity's icon becomes a live **arc-gauge dial** in its band color.  
*min wall 1×12*

| | |
|---|---|
| ![Home Assistant — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/entity-board.png)<br>Matrix 256 × 64 | ![Home Assistant — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/entity-board.png)<br>Matrix 128 × 64 |
| ![Home Assistant — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/entity-board.png)<br>Matrix 128 × 32 | ![Home Assistant — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/entity-board.png)<br>Matrix 64 × 32 |
| ![Home Assistant — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/entity-board.png)<br>Flap wall 3 × 15 | ![Home Assistant — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/entity-board.png)<br>Flap wall 5 × 15 |
| ![Home Assistant — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/entity-board.png)<br>Flap wall 2 × 15 |  |

Thresholds carry a **polarity** (both HA apps read the same grammar): `lo,hi` is a
comfort **band** (green inside, red outside — temperature), `<limit` or `<warn,bad`
means **lower is better** (green below, amber between, red above — CO₂, power), and
`>floor` or `>warn,good` means **higher is better** (battery, signal). The settings
table's ◦/</> button picks it per row.

## Image

Mirrors a picture onto the panel as a full-color frame — fit or fill. Leave the URL blank for a color demo.  
*🎨*

![Image on a 128×64 panel](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/canvas-image.png)

## Invaders

The marching fleet, complete with the two-note heartbeat that speeds up as it
thins: steer the cannon, TAP up to fire (one shot airborne at a time), dodge the
bombs, and shoot the magenta saucer for 100. Deeper rows score less; a cleared
wave restarts lower and faster, and if the fleet reaches the cannon row the
invasion ends the game outright. Three lives, READY? holds between them.
*👾 · interactive*

## ISS Tracker

Where the Space Station is — and an interruption when it passes overhead.  
*🌐⚡ · min wall 1×14*

| | |
|---|---|
| ![ISS Tracker — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/iss.png)<br>Matrix 256 × 64 | ![ISS Tracker — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/iss.png)<br>Matrix 128 × 64 |
| ![ISS Tracker — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/iss.png)<br>Matrix 128 × 32 | ![ISS Tracker — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/iss.png)<br>Matrix 64 × 32 |
| ![ISS Tracker — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/iss.png)<br>Flap wall 3 × 15 | ![ISS Tracker — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/iss.png)<br>Flap wall 5 × 15 |
| ![ISS Tracker — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/iss.png)<br>Flap wall 2 × 15 |  |

## Livestream

Launch-day rotation for a stream.  
*🌐🔑 · min wall 3×12*

| | |
|---|---|
| ![Livestream — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/livestream.png)<br>Matrix 256 × 64 | ![Livestream — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/livestream.png)<br>Matrix 128 × 64 |
| ![Livestream — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/livestream.png)<br>Matrix 128 × 32 | ![Livestream — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/livestream.png)<br>Matrix 64 × 32 |
| ![Livestream — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/livestream.png)<br>Flap wall 3 × 15 | ![Livestream — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/livestream.png)<br>Flap wall 5 × 15 |
| ![Livestream — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/livestream.png)<br>Flap wall 2 × 15 |  |

## Lumina Clock

The time as luminous color — big **anti-aliased** digits filling the panel, in four treatments: **Glow** (a light-to-color gradient with a soft halo), **Aurora** (color flowing through the numerals), **Neon** (a bright tube-glow) and **Minimal**. Curated palettes (Amber / Ice / Mint / Duotone / Daylight, never pink), 12h/24h, a smooth seconds bar. The canvas evolution of the flap **Art Clock**.  
*🎨*

![Lumina Clock on a 128×64 panel](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/canvas-art-clock.png)

## Magic 8 Ball (channel)

Ask, and the wall answers.  
*🌐 · min wall 3×15*

| | |
|---|---|
| ![Magic 8 Ball — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/magic-8-ball.png)<br>Matrix 256 × 64 | ![Magic 8 Ball — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/magic-8-ball.png)<br>Matrix 128 × 64 |
| ![Magic 8 Ball — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/magic-8-ball.png)<br>Matrix 128 × 32 | ![Magic 8 Ball — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/magic-8-ball.png)<br>Matrix 64 × 32 |
| ![Magic 8 Ball — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/magic-8-ball.png)<br>Flap wall 3 × 15 | ![Magic 8 Ball — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/magic-8-ball.png)<br>Flap wall 5 × 15 |
| ![Magic 8 Ball — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/magic-8-ball.png)<br>Flap wall 2 × 15 |  |

## Matrix

A cascade reveal.  
*🎞 · min wall 1×1*

*An animation — best seen in motion; no static screenshot.*

## Metro

MBTA arrivals for your stop.  
*🌐⚡ · min wall 1×10*

| | |
|---|---|
| ![Metro — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/metro.png)<br>Matrix 256 × 64 | ![Metro — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/metro.png)<br>Matrix 128 × 64 |
| ![Metro — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/metro.png)<br>Matrix 128 × 32 | ![Metro — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/metro.png)<br>Matrix 64 × 32 |
| ![Metro — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/metro.png)<br>Flap wall 3 × 15 | ![Metro — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/metro.png)<br>Flap wall 5 × 15 |
| ![Metro — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/metro.png)<br>Flap wall 2 × 15 |  |

## Moon Phase

The current moon phase, with an illumination bar in color flaps.  
*🌐⚡ · min wall 3×10*

| | |
|---|---|
| ![Moon Phase — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/moon-phase.png)<br>Matrix 256 × 64 | ![Moon Phase — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/moon-phase.png)<br>Matrix 128 × 64 |
| ![Moon Phase — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/moon-phase.png)<br>Matrix 128 × 32 | ![Moon Phase — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/moon-phase.png)<br>Matrix 64 × 32 |
| ![Moon Phase — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/moon-phase.png)<br>Flap wall 3 × 15 | ![Moon Phase — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/moon-phase.png)<br>Flap wall 5 × 15 |
| ![Moon Phase — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/moon-phase.png)<br>Flap wall 2 × 15 |  |

## Motivational Quotes (channel)

Daily motivation.  
*🌐 · min wall 3×15*

| | |
|---|---|
| ![Motivational Quotes — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/motivational-quotes.png)<br>Matrix 256 × 64 | ![Motivational Quotes — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/motivational-quotes.png)<br>Matrix 128 × 64 |
| ![Motivational Quotes — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/motivational-quotes.png)<br>Matrix 128 × 32 | ![Motivational Quotes — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/motivational-quotes.png)<br>Matrix 64 × 32 |
| ![Motivational Quotes — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/motivational-quotes.png)<br>Flap wall 3 × 15 | ![Motivational Quotes — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/motivational-quotes.png)<br>Flap wall 5 × 15 |
| ![Motivational Quotes — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/motivational-quotes.png)<br>Flap wall 2 × 15 |  |

## Movie Quotes (channel)

Iconic film lines, each with the movie it's from.  
*min wall 3×15*

| | |
|---|---|
| ![Movie Quotes — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/movie-quotes.png)<br>Matrix 256 × 64 | ![Movie Quotes — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/movie-quotes.png)<br>Matrix 128 × 64 |
| ![Movie Quotes — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/movie-quotes.png)<br>Matrix 128 × 32 | ![Movie Quotes — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/movie-quotes.png)<br>Matrix 64 × 32 |
| ![Movie Quotes — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/movie-quotes.png)<br>Flap wall 3 × 15 | ![Movie Quotes — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/movie-quotes.png)<br>Flap wall 5 × 15 |
| ![Movie Quotes — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/movie-quotes.png)<br>Flap wall 2 × 15 |  |

## News Headlines

Latest news from RSS feeds you choose.  
*⚡ · min wall 3×10*

| | |
|---|---|
| ![News Headlines — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/news-headlines.png)<br>Matrix 256 × 64 | ![News Headlines — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/news-headlines.png)<br>Matrix 128 × 64 |
| ![News Headlines — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/news-headlines.png)<br>Matrix 128 × 32 | ![News Headlines — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/news-headlines.png)<br>Matrix 64 × 32 |
| ![News Headlines — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/news-headlines.png)<br>Flap wall 3 × 15 | ![News Headlines — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/news-headlines.png)<br>Flap wall 5 × 15 |
| ![News Headlines — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/news-headlines.png)<br>Flap wall 2 × 15 |  |

## On This Day

Historical events that happened today — up to three per day.  
*min wall 3×10*

| | |
|---|---|
| ![On This Day — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/on-this-day.png)<br>Matrix 256 × 64 | ![On This Day — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/on-this-day.png)<br>Matrix 128 × 64 |
| ![On This Day — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/on-this-day.png)<br>Matrix 128 × 32 | ![On This Day — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/on-this-day.png)<br>Matrix 64 × 32 |
| ![On This Day — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/on-this-day.png)<br>Flap wall 3 × 15 | ![On This Day — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/on-this-day.png)<br>Flap wall 5 × 15 |
| ![On This Day — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/on-this-day.png)<br>Flap wall 2 × 15 |  |

## One Liners (channel)

Quick witty laughs.  
*min wall 3×15*

| | |
|---|---|
| ![One Liners — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/funny-one-liners.png)<br>Matrix 256 × 64 | ![One Liners — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/funny-one-liners.png)<br>Matrix 128 × 64 |
| ![One Liners — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/funny-one-liners.png)<br>Matrix 128 × 32 | ![One Liners — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/funny-one-liners.png)<br>Matrix 64 × 32 |
| ![One Liners — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/funny-one-liners.png)<br>Flap wall 3 × 15 | ![One Liners — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/funny-one-liners.png)<br>Flap wall 5 × 15 |
| ![One Liners — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/funny-one-liners.png)<br>Flap wall 2 × 15 |  |

## Planes Overhead

Nearby aircraft. Keyless via OpenSky; FlightAware / Flightradar24 / AirLabs / aviationstack with a key.  
*⚡ · min wall 3×12*

| | |
|---|---|
| ![Planes Overhead — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/planes_overhead.png)<br>Matrix 256 × 64 | ![Planes Overhead — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/planes_overhead.png)<br>Matrix 128 × 64 |
| ![Planes Overhead — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/planes_overhead.png)<br>Matrix 128 × 32 | ![Planes Overhead — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/planes_overhead.png)<br>Matrix 64 × 32 |
| ![Planes Overhead — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/planes_overhead.png)<br>Flap wall 3 × 15 | ![Planes Overhead — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/planes_overhead.png)<br>Flap wall 5 × 15 |
| ![Planes Overhead — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/planes_overhead.png)<br>Flap wall 2 × 15 |  |

## Pong

The first arcade game, on the aspect ratio it was born for: you take the left
paddle, the machine takes the right. It follows the ball a shade slower than a
well-angled shot travels — returns off the paddle's edge are how points are won —
and every return in a rally adds pace. First to 7; in attract mode both sides play
themselves with wandering aim.
*🏓 · interactive*

## Precious Metals

Gold & silver spot prices.  
*🌐 · min wall 1×13*

| | |
|---|---|
| ![Precious Metals — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/metals.png)<br>Matrix 256 × 64 | ![Precious Metals — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/metals.png)<br>Matrix 128 × 64 |
| ![Precious Metals — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/metals.png)<br>Matrix 128 × 32 | ![Precious Metals — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/metals.png)<br>Matrix 64 × 32 |
| ![Precious Metals — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/metals.png)<br>Flap wall 3 × 15 | ![Precious Metals — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/metals.png)<br>Flap wall 5 × 15 |
| ![Precious Metals — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/metals.png)<br>Flap wall 2 × 15 |  |

## Public Holidays

Upcoming holidays for your country and province/state — ten years bundled, works offline. Four layers, each switchable: public holidays, religious observances by tradition, curated cultural traditions per language-region, and a fun-day-every-day novelty calendar. On a Matrix panel: a desk-calendar card per holiday.  
*🌐 · min wall 2×12*

| | |
|---|---|
| ![Public Holidays — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/holidays.png)<br>Matrix 256 × 64 | ![Public Holidays — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/holidays.png)<br>Matrix 128 × 64 |
| ![Public Holidays — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/holidays.png)<br>Matrix 128 × 32 | ![Public Holidays — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/holidays.png)<br>Matrix 64 × 32 |
| ![Public Holidays — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/holidays.png)<br>Flap wall 3 × 15 | ![Public Holidays — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/holidays.png)<br>Flap wall 5 × 15 |
| ![Public Holidays — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/holidays.png)<br>Flap wall 2 × 15 |  |

## Quote

An inspirational quote.  
*min wall 3×15*

| | |
|---|---|
| ![Quote — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/quote.png)<br>Matrix 256 × 64 | ![Quote — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/quote.png)<br>Matrix 128 × 64 |
| ![Quote — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/quote.png)<br>Matrix 128 × 32 | ![Quote — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/quote.png)<br>Matrix 64 × 32 |
| ![Quote — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/quote.png)<br>Flap wall 3 × 15 | ![Quote — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/quote.png)<br>Flap wall 5 × 15 |
| ![Quote — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/quote.png)<br>Flap wall 2 × 15 |  |

## Rainbow

A color wave.  
*🎞 · min wall 1×1*

*An animation — best seen in motion; no static screenshot.*

## Random Fact

A concise random fact — in English or German, following your Language.  
*🌐 · min wall 3×15*

| | |
|---|---|
| ![Random Fact — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/useless-fact.png)<br>Matrix 256 × 64 | ![Random Fact — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/useless-fact.png)<br>Matrix 128 × 64 |
| ![Random Fact — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/useless-fact.png)<br>Matrix 128 × 32 | ![Random Fact — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/useless-fact.png)<br>Matrix 64 × 32 |
| ![Random Fact — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/useless-fact.png)<br>Flap wall 3 × 15 | ![Random Fact — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/useless-fact.png)<br>Flap wall 5 × 15 |
| ![Random Fact — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/useless-fact.png)<br>Flap wall 2 × 15 |  |

## Random Spin

Continuous random flaps.  
*🎞 · min wall 1×1*

*An animation — best seen in motion; no static screenshot.*

## Rocket Launch

The next orbital rocket launch.  
*🌐 · min wall 1×12*

| | |
|---|---|
| ![Rocket Launch — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/rocket-launch.png)<br>Matrix 256 × 64 | ![Rocket Launch — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/rocket-launch.png)<br>Matrix 128 × 64 |
| ![Rocket Launch — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/rocket-launch.png)<br>Matrix 128 × 32 | ![Rocket Launch — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/rocket-launch.png)<br>Matrix 64 × 32 |
| ![Rocket Launch — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/rocket-launch.png)<br>Flap wall 3 × 15 | ![Rocket Launch — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/rocket-launch.png)<br>Flap wall 5 × 15 |
| ![Rocket Launch — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/rocket-launch.png)<br>Flap wall 2 × 15 |  |

## Sarcastic Fortune Cookies (channel)

Cynical fortune-cookie wisdom.  
*🌐 · min wall 3×15*

| | |
|---|---|
| ![Sarcastic Fortune Cookies — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/sarcastic-fortune-cookies.png)<br>Matrix 256 × 64 | ![Sarcastic Fortune Cookies — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/sarcastic-fortune-cookies.png)<br>Matrix 128 × 64 |
| ![Sarcastic Fortune Cookies — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/sarcastic-fortune-cookies.png)<br>Matrix 128 × 32 | ![Sarcastic Fortune Cookies — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/sarcastic-fortune-cookies.png)<br>Matrix 64 × 32 |
| ![Sarcastic Fortune Cookies — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/sarcastic-fortune-cookies.png)<br>Flap wall 3 × 15 | ![Sarcastic Fortune Cookies — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/sarcastic-fortune-cookies.png)<br>Flap wall 5 × 15 |
| ![Sarcastic Fortune Cookies — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/sarcastic-fortune-cookies.png)<br>Flap wall 2 × 15 |  |

## Scoreboard

Live and upcoming games with team logos and scores, cycling one matchup at a time. Uses the same team / league picker as the flap **Sports**.  
*🎨*

*Matrix panel only — no screenshot yet.*

## Sensor Graph

What the Stock Graph does for a ticker, for any Home Assistant sensor: the recent
history as a dim area chart under the live value in big type. The window seeds from
HA's history API the moment the card first draws — so it's a full, meaningful line
immediately, even as a brief playlist slot — and live samples append from there
(pure sampling with a quiet once-a-minute retry if the recorder has nothing to
give). Config lines are `entity_id | Label | lo,hi`; the optional band pins the
scale and colors the value (green in range, red out), several entities rotate like
a board.

## Shower Thoughts (channel)

Mind-bending thoughts.  
*🌐 · min wall 3×15*

| | |
|---|---|
| ![Shower Thoughts — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/shower-thoughts.png)<br>Matrix 256 × 64 | ![Shower Thoughts — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/shower-thoughts.png)<br>Matrix 128 × 64 |
| ![Shower Thoughts — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/shower-thoughts.png)<br>Matrix 128 × 32 | ![Shower Thoughts — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/shower-thoughts.png)<br>Matrix 64 × 32 |
| ![Shower Thoughts — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/shower-thoughts.png)<br>Flap wall 3 × 15 | ![Shower Thoughts — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/shower-thoughts.png)<br>Flap wall 5 × 15 |
| ![Shower Thoughts — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/shower-thoughts.png)<br>Flap wall 2 × 15 |  |

## Simon

The memory game where the sound IS the game: the machine plays a growing sequence of
lit strips, each with its own note, and you echo it back on the pad — the four
full-height colors map left-to-right to ◄ ▲ ▼ ►, with the arrows drawn on the strips.
One wrong press ends it; go idle mid-echo and the melody replays as a hint. The demo
plays itself silently until you press.
*🧠 · interactive*

## Snake

The classic: steer with the pad, eat to grow and score, don't hit the wall or
yourself. A greedy self-playing demo holds the panel until you take over, and the
body draws as merged runs of rects so even a long snake is a tiny ops batch.
*🐍 · interactive*

## Sports

Scores & schedules for the teams you follow.  
*🌐⚡ · min wall 1×8*

| | |
|---|---|
| ![Sports — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/sports.png)<br>Matrix 256 × 64 | ![Sports — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/sports.png)<br>Matrix 128 × 64 |
| ![Sports — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/sports.png)<br>Matrix 128 × 32 | ![Sports — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/sports.png)<br>Matrix 64 × 32 |
| ![Sports — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/sports.png)<br>Flap wall 3 × 15 | ![Sports — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/sports.png)<br>Flap wall 5 × 15 |
| ![Sports — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/sports.png)<br>Flap wall 2 × 15 |  |

## Star Wars (channel)

May the force be with you.  
*min wall 3×15*

| | |
|---|---|
| ![Star Wars — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/star-wars-quotes.png)<br>Matrix 256 × 64 | ![Star Wars — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/star-wars-quotes.png)<br>Matrix 128 × 64 |
| ![Star Wars — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/star-wars-quotes.png)<br>Matrix 128 × 32 | ![Star Wars — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/star-wars-quotes.png)<br>Matrix 64 × 32 |
| ![Star Wars — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/star-wars-quotes.png)<br>Flap wall 3 × 15 | ![Star Wars — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/star-wars-quotes.png)<br>Flap wall 5 × 15 |
| ![Star Wars — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/star-wars-quotes.png)<br>Flap wall 2 × 15 |  |

## Stock Graph

A live quote — an index or ticker — in big bold type over its own price chart, green when up and red when down, with the day's percentage and a faint previous-close baseline. One symbol, or a rotating watchlist (a market board). Range 1D…1Y. Prices from the same source as the flap **Stocks**.  
*🎨*

![Stock Graph on a 128×64 panel](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/canvas-stock-graph.png)

## Stocks

Live prices for the tickers you follow.  
*🌐⚡ · min wall 1×13*

| | |
|---|---|
| ![Stocks — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/stocks.png)<br>Matrix 256 × 64 | ![Stocks — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/stocks.png)<br>Matrix 128 × 64 |
| ![Stocks — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/stocks.png)<br>Matrix 128 × 32 | ![Stocks — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/stocks.png)<br>Matrix 64 × 32 |
| ![Stocks — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/stocks.png)<br>Flap wall 3 × 15 | ![Stocks — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/stocks.png)<br>Flap wall 5 × 15 |
| ![Stocks — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/stocks.png)<br>Flap wall 2 × 15 |  |

## Stoic Quotes (channel)

Ancient wisdom.  
*🌐 · min wall 3×15*

| | |
|---|---|
| ![Stoic Quotes — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/stoic-quotes.png)<br>Matrix 256 × 64 | ![Stoic Quotes — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/stoic-quotes.png)<br>Matrix 128 × 64 |
| ![Stoic Quotes — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/stoic-quotes.png)<br>Matrix 128 × 32 | ![Stoic Quotes — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/stoic-quotes.png)<br>Matrix 64 × 32 |
| ![Stoic Quotes — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/stoic-quotes.png)<br>Flap wall 3 × 15 | ![Stoic Quotes — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/stoic-quotes.png)<br>Flap wall 5 × 15 |
| ![Stoic Quotes — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/stoic-quotes.png)<br>Flap wall 2 × 15 |  |

## Sun Times

Sunrise, sunset & day length.  
*🌐 · min wall 1×12*

| | |
|---|---|
| ![Sun Times — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/sun-times.png)<br>Matrix 256 × 64 | ![Sun Times — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/sun-times.png)<br>Matrix 128 × 64 |
| ![Sun Times — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/sun-times.png)<br>Matrix 128 × 32 | ![Sun Times — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/sun-times.png)<br>Matrix 64 × 32 |
| ![Sun Times — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/sun-times.png)<br>Flap wall 3 × 15 | ![Sun Times — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/sun-times.png)<br>Flap wall 5 × 15 |
| ![Sun Times — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/sun-times.png)<br>Flap wall 2 × 15 |  |

## Sweep

A color sweep.  
*🎞 · min wall 1×1*

*An animation — best seen in motion; no static screenshot.*

## Tetris

Tetris turned on its side for a wide panel: gravity pulls **left**, pieces drift in from
the right and pile against the left wall, and filling a whole **column** clears it. It
plays itself until you grab the controls — **up/down** move the piece, **right** rotates,
**left** is a soft drop — then plays live with sound; game over fades the well to black
behind your score. Drawn entirely with on-device draw ops, streamed as binary ops.  
*🎨 · playable*

| | |
|---|---|
| ![Tetris — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/canvas-tetris.png)<br>Matrix 256 × 64 | ![Tetris — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/canvas-tetris.png)<br>Matrix 128 × 64 |
| ![Tetris — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/canvas-tetris.png)<br>Matrix 128 × 32 | ![Tetris — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/canvas-tetris.png)<br>Matrix 64 × 32 |

## The Office (channel)

That's what she said.  
*min wall 3×15*

| | |
|---|---|
| ![The Office — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/office-quotes.png)<br>Matrix 256 × 64 | ![The Office — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/office-quotes.png)<br>Matrix 128 × 64 |
| ![The Office — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/office-quotes.png)<br>Matrix 128 × 32 | ![The Office — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/office-quotes.png)<br>Matrix 64 × 32 |
| ![The Office — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/office-quotes.png)<br>Flap wall 3 × 15 | ![The Office — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/office-quotes.png)<br>Flap wall 5 × 15 |
| ![The Office — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/office-quotes.png)<br>Flap wall 2 × 15 |  |

## Ticker

A line of text scrolling across the panel, rendered on-device — a message you type, or a live news / RSS feed.  
*🎨*

*Matrix panel only — no screenshot yet.*

## Tides

Today's high & low tides (NOAA).  
*🌐 · min wall 1×12*

| | |
|---|---|
| ![Tides — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/tides.png)<br>Matrix 256 × 64 | ![Tides — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/tides.png)<br>Matrix 128 × 64 |
| ![Tides — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/tides.png)<br>Matrix 128 × 32 | ![Tides — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/tides.png)<br>Matrix 64 × 32 |
| ![Tides — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/tides.png)<br>Flap wall 3 × 15 | ![Tides — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/tides.png)<br>Flap wall 5 × 15 |
| ![Tides — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/tides.png)<br>Flap wall 2 × 15 |  |

## Time

A live clock. Optional seconds on a Matrix Gateway.  
*🌐 · min wall 1×8*

| | |
|---|---|
| ![Time — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/time.png)<br>Matrix 256 × 64 | ![Time — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/time.png)<br>Matrix 128 × 64 |
| ![Time — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/time.png)<br>Matrix 128 × 32 | ![Time — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/time.png)<br>Matrix 64 × 32 |
| ![Time — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/time.png)<br>Flap wall 3 × 15 | ![Time — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/time.png)<br>Flap wall 5 × 15 |
| ![Time — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/time.png)<br>Flap wall 2 × 15 |  |

## Time Since

Elapsed time since a moment — days without incident, days since launch. Live seconds on a Matrix Gateway.  
*🌐⚡ · min wall 3×10*

| | |
|---|---|
| ![Time Since — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/time-since.png)<br>Matrix 256 × 64 | ![Time Since — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/time-since.png)<br>Matrix 128 × 64 |
| ![Time Since — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/time-since.png)<br>Matrix 128 × 32 | ![Time Since — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/time-since.png)<br>Matrix 64 × 32 |
| ![Time Since — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/time-since.png)<br>Flap wall 3 × 15 | ![Time Since — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/time-since.png)<br>Flap wall 5 × 15 |
| ![Time Since — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/time-since.png)<br>Flap wall 2 × 15 |  |

## Trivia

Random trivia questions.  
*min wall 3×10*

| | |
|---|---|
| ![Trivia — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/trivia.png)<br>Matrix 256 × 64 | ![Trivia — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/trivia.png)<br>Matrix 128 × 64 |
| ![Trivia — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/trivia.png)<br>Matrix 128 × 32 | ![Trivia — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/trivia.png)<br>Matrix 64 × 32 |
| ![Trivia — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/trivia.png)<br>Flap wall 3 × 15 | ![Trivia — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/trivia.png)<br>Flap wall 5 × 15 |
| ![Trivia — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/trivia.png)<br>Flap wall 2 × 15 |  |

## Twinkle

A sparkle effect.  
*🎞 · min wall 1×1*

*An animation — best seen in motion; no static screenshot.*

## Weather

Current conditions, a multi-day forecast with per-day sky words and color flaps, and AQI / UV / pollen. Keyless out of the box (Open-Meteo); WeatherAPI, QWeather or OpenWeather with a key. On a Matrix panel: the weather as a **living sky scene** (the merged Weather Sky) — a glowing sun by day or a moon and colored stars by night, drifting cloud, falling rain or snow — and on a big panel a full info column with feels-like, humidity, wind and a three-day forecast strip.  
*🌐⚡ · min wall 1×8*

| | |
|---|---|
| ![Weather — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/weather.png)<br>Matrix 256 × 64 | ![Weather — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/weather.png)<br>Matrix 128 × 64 |
| ![Weather — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/weather.png)<br>Matrix 128 × 32 | ![Weather — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/weather.png)<br>Matrix 64 × 32 |
| ![Weather — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/weather.png)<br>Flap wall 3 × 15 | ![Weather — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/weather.png)<br>Flap wall 5 × 15 |
| ![Weather — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/weather.png)<br>Flap wall 2 × 15 |  |

## Wikipedia Today

Wikipedia's featured article & most-read pages.  
*🌐 · min wall 2×15*

| | |
|---|---|
| ![Wikipedia Today — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/wiki-today.png)<br>Matrix 256 × 64 | ![Wikipedia Today — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/wiki-today.png)<br>Matrix 128 × 64 |
| ![Wikipedia Today — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/wiki-today.png)<br>Matrix 128 × 32 | ![Wikipedia Today — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/wiki-today.png)<br>Matrix 64 × 32 |
| ![Wikipedia Today — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/wiki-today.png)<br>Flap wall 3 × 15 | ![Wikipedia Today — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/wiki-today.png)<br>Flap wall 5 × 15 |
| ![Wikipedia Today — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/wiki-today.png)<br>Flap wall 2 × 15 |  |

## Word Clock

The time as a written phrase — "QUARTER PAST NINE".  
*🌐 · min wall 3×12*

| | |
|---|---|
| ![Word Clock — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/word-clock.png)<br>Matrix 256 × 64 | ![Word Clock — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/word-clock.png)<br>Matrix 128 × 64 |
| ![Word Clock — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/word-clock.png)<br>Matrix 128 × 32 | ![Word Clock — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/word-clock.png)<br>Matrix 64 × 32 |
| ![Word Clock — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/word-clock.png)<br>Flap wall 3 × 15 | ![Word Clock — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/word-clock.png)<br>Flap wall 5 × 15 |
| ![Word Clock — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/word-clock.png)<br>Flap wall 2 × 15 |  |

## Word of the Day

A new word every day.  
*🌐 · min wall 2×15*

| | |
|---|---|
| ![Word of the Day — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/word-of-the-day.png)<br>Matrix 256 × 64 | ![Word of the Day — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/word-of-the-day.png)<br>Matrix 128 × 64 |
| ![Word of the Day — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/word-of-the-day.png)<br>Matrix 128 × 32 | ![Word of the Day — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/word-of-the-day.png)<br>Matrix 64 × 32 |
| ![Word of the Day — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/word-of-the-day.png)<br>Flap wall 3 × 15 | ![Word of the Day — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/word-of-the-day.png)<br>Flap wall 5 × 15 |
| ![Word of the Day — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/word-of-the-day.png)<br>Flap wall 2 × 15 |  |

## World Clock

Time zones side by side. On a Matrix panel: one lit day/night row per city.  
*🌐⚡ · min wall 1×10*

| | |
|---|---|
| ![World Clock — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/world_clock.png)<br>Matrix 256 × 64 | ![World Clock — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/world_clock.png)<br>Matrix 128 × 64 |
| ![World Clock — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/world_clock.png)<br>Matrix 128 × 32 | ![World Clock — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/world_clock.png)<br>Matrix 64 × 32 |
| ![World Clock — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/world_clock.png)<br>Flap wall 3 × 15 | ![World Clock — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/world_clock.png)<br>Flap wall 5 × 15 |
| ![World Clock — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/world_clock.png)<br>Flap wall 2 × 15 |  |

## YouTube

Channel stats — real subscribers with an API key, latest uploads without.  
*🌐⚡🔑 · min wall 3×10*

| | |
|---|---|
| ![YouTube — Matrix 256 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r256x64/youtube.png)<br>Matrix 256 × 64 | ![YouTube — Matrix 128 × 64](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x64/youtube.png)<br>Matrix 128 × 64 |
| ![YouTube — Matrix 128 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r128x32/youtube.png)<br>Matrix 128 × 32 | ![YouTube — Matrix 64 × 32](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/r64x32/youtube.png)<br>Matrix 64 × 32 |
| ![YouTube — Flap wall 3 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-3x15/youtube.png)<br>Flap wall 3 × 15 | ![YouTube — Flap wall 5 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-5x15/youtube.png)<br>Flap wall 5 × 15 |
| ![YouTube — Flap wall 2 × 15](https://raw.githubusercontent.com/avandeputte/SplitFlapGatewayCompanion/main/screenshots/flap-2x15/youtube.png)<br>Flap wall 2 × 15 |  |

---

Missing something? Upload your own app as a `.zip` from the App Library — the
guide is [Writing Apps](Writing-Apps.md).

# news-image-20261121 — The World in One Image

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/kiw33/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/kiw33/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Entry for make.fun competition `news-image-20261121`: sum up the world
news of Saturday 21 November 2026 in a single 1024x1024 image.

## Files

- `main.py` — entrypoint (Python 3.13, standard library only). Copies
  `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`, or a local `out/`
  when neither exists), so both grader runs write byte-identical output.
- `draw_news21.py` — the drawing program (Pillow + DejaVu fonts). Renders
  the masthead, six story panels with flat pictograms, and the "Also
  today" ticker into `entry.png`. Deterministic: two runs give the same
  sha256.
- `entry.png` — the finished image (1024x1024, ~134 KiB).
- `SOURCES.md` — every fact in the image, with sources dated 21 Nov 2026.

## Stories

1. Poland — Russian Kh-101 cruise missile lands in Poland; Tusk calls it an "intentional provocation"
2. Ukraine — Russia's overnight barrage: 400+ drones, 110 missiles; 8 killed
3. Antalya — COP31 climate talks spill into overtime; draft drops fossil fuels
4. Odisha — Cyclone Akvan weakens after landfall near Gopalpur; 3.7 lakh evacuated, no deaths
5. Paris — Europeans ready to travel to Moscow if given a full role in Ukraine talks
6. New York — JPMorgan, Visa and Mastercard confirm vendor data breaches; 16,000+ emails leak

## Build

```sh
python3 draw_news21.py          # regenerates entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Verified 21 Nov 2026: two runs of `draw_news21.py` produce the same
sha256, and `main.py` writes the same bytes to the output directory.

## Kit check

```sh
node <kit>/cli/makefun.mjs check --kit <kit> --repo . --commit HEAD
```

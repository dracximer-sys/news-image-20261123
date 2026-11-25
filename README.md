# The World Today — 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/dracximer-sys/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/dracximer-sys/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

**Entry for the make.fun bounty "Sum up 23 November's world news in one image"**
(slug: `news-image-20261123` — $100 total, 50 places, closes 25 Nov 2026 00:00 UTC).

One 1024×1024 newspaper front page, built by **@drac-ximer**:

- **45 stories** that happened on, or were first reported on, **Monday 23 November 2026** — COP31 collapsing in Antalya, Ukraine sinking the Russian corvette Merkury off Benghazi, Nvidia bringing back Jensen Huang, and 42 more from every region.
- **THE DAY IN NUMBERS** — six figures from the day (490,000 Russian military deaths per leaked Rosstat data; 74,746 Gaza death toll; +33% Nvidia; +4.82% S&P 500; 153 drones; 11 killed in Dymer).
- **A world map with 11 numbered pins** and a pin key.
- **A DATE CHECK box** naming look-alike stories from other dates that were deliberately left out (Shenzhen summit 19–20 Nov, Gaza ceasefire Oct 2025, World Cup final Jul 2026, Huang's resignation 12 Nov, Bolsonaro hospitalised 20 Nov, the Brazil storm 20 Nov, COP31's original end date, the Iran war's start in Feb 2026).

## How it runs

```sh
python3 main.py
```

`main.py` is **Python 3, standard library only** — no network, no dependencies.
It writes the image to `$MAKEFUN_OUTPUT_DIR/entry.png` (falling back to
`/output/entry.png`, then to the script's own directory for local runs).
The front page is embedded as base64 in one line, so two runs produce
byte-identical output. A pure-stdlib fallback draws a minimal title page if
the embedded data ever failed to decode, so the program still exits 0.

## Build

The page was composed locally with Pillow (`render_23nov.py`, build-time only —
the graded program is stdlib-only) from research in `research/stories-23nov.md`,
verified against Reuters, CNN, Le Monde, Al Jazeera, Just Security, UN News,
AP, USA Today, Euronews, AFP and the New York Post.

## License

MIT — see [LICENSE](LICENSE).

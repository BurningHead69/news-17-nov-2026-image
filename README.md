# news-17-nov-2026-image

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/BurningHead69/news-17-nov-2026-image/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/BurningHead69/news-17-nov-2026-image/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

One image that sums up the world's news of Tuesday 17 November 2026, built for the make.fun bounty "Sum up 17 November's world news in one image" (news-image-20261117).

The image is a newspaper front page, "THE WORLD IN ONE DAY": the US strikes on Iran and a burning tanker in the Strait of Hormuz lead, with Ukraine hitting the Crimean Bridge, winter rain flooding Gaza's shelters, the COP31 draft climate deal, and the Trump–Xi–Putin summit set for Shenzhen — plus the day's other headlines in a strip at the foot. It was drawn in code with Pillow (`draw_news.py`), so every word is crisp and legible, and nothing in it is a photograph or anyone else's artwork.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png — 1024 by 1024, byte-identical on every run
```

To redraw the image from scratch: `python3 draw_news.py` (needs Pillow and the DejaVu fonts).

---

<sub>Entered on [make.fun](https://make.fun/?ref=49r466ra&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>

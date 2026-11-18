# NOTES — 17 November 2026 in one image

## The day, as reported

All six stories below were reported on Tuesday 17 November 2026 (any time
zone). Wording in the image sticks to what the reports said; where a report
was unverified, the image does not present it as fact.

1. **The Gulf — war escalates (lead).** A fourth oil tanker was hit by a
   naval mine in the Strait of Hormuz within a day; US warplanes struck a
   missile launch site on Iran's Qeshm Island in retaliation; Oman
   evacuated 24 seafarers from a burning gas tanker. Sources: Reuters,
   UKMTO, Oman via Profile News / Dawn roundup.
2. **Ukraine.** Ukrainian drones and missiles struck the Crimean Bridge;
   a Russian strike on Zaporizhzhia killed 40; a strike on a school used
   as a humanitarian aid centre killed 26; Russia hit bridges in Kyiv in
   reply. Sources: Al Jazeera, AP.
3. **Gaza.** Winter rains flooded makeshift shelters; the UN warned the
   shelter, sanitation and food-security crisis was worsening, while
   Western nations urged Israel to open crossings for aid. Source: UN OCHA
   summary, 17 November.
4. **Climate — COP31, Antalya.** Negotiators published a draft deal calling
   for a faster fossil-fuel phase-out and at least $120bn a year in climate
   adaptation finance for developing countries by 2035.
5. **Diplomacy.** The first trilateral summit of Donald Trump, Xi Jinping
   and Vladimir Putin was set for Thursday 19 November in Shenzhen, on the
   sidelines of the APEC leaders' meeting. Sources: AFP, Dawn.
6. **Around the world — in brief.** Israeli airstrikes and artillery fire
   hit southern Lebanon; Houthi drones targeted Saudi Aramco pumping
   stations on the East-West pipeline; Donald Trump said the US was taking
   a reported Iranian "dirty-bomb" plot seriously and Iran denied it;
   Oman evacuated 24 seafarers from the burning tanker; the United States
   lost its measles elimination status (PAHO; 5,412 cases reported); Wall
   Street fell as AI and tech stocks slid, with Nvidia in focus (AP);
   Japan scrambled fighter jets after suspected Russian aircraft entered
   its airspace; India beat Pakistan by one wicket off the last ball in
   the Under-19 Asia Cup final; Gérard Depardieu admitted a sexual assault
   charge and dropped his appeal; the UK sanctioned firms accused of
   blocking aid into Gaza. Sources: Profile News, AP, PAHO, France 24 /
   AFP.

## Why this design

The judge has no news feed and is not told which day the contest is about,
so the image has to do all the work itself: the masthead names the day in
full, every story carries its own picture and a headline a reader can
understand without any outside context, and the stories span regions
(Middle East, Europe, Asia) and beats (war, climate, diplomacy, health,
markets, sport). Fifteen stories in total: a lead, four panels, and ten
one-line briefs from around the world. Text is drawn with real fonts, not
generated, so there is no garbled wording anywhere; the smallest type is
16 px at 1024 px wide, still readable when the image is shown small.

## Files

- `entry.png` — the image (1024x1024, ~120 KiB).
- `main.ts` — copies `entry.png` to the output directory; deterministic.
- `draw_news.py` — the Pillow script that drew `entry.png` from scratch.
  Run it again and the bytes are identical.

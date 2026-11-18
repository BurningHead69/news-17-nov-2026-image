// news-image-20261117 entry (Node 22, standard library only).
//
// The entry image lives next to this file as entry.png: a newspaper
// front page drawn for Tuesday 17 November 2026 (see draw_news.py for how
// it was drawn, and NOTES.md for the stories and their sources). This
// program only copies that image to the grader's output directory, so
// both runs write exactly the same bytes. No network, no clock, no input.
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const entryFile = "entry.png";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL(`./${entryFile}`, import.meta.url), join(outDir, entryFile));

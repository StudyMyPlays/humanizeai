# Humanize

Rewrites AI-sounding text so it reads like a person wrote it, without changing what it says.

## Install

Save `humanize.skill` (the packaged version of this folder) via the **Save skill** button on the file card. Once installed it triggers on its own when you say "humanize this", "make this sound less like AI", "fix this writing", or drop a file and ask for a rewrite.

To use it as a plain folder instead, keep this directory in your Cowork workspace and point Claude at `SKILL.md`.

## The governing rule

**Never invent.** Every concrete detail in the output exists in the input. The skill cuts, sharpens, reorders, and rephrases. It does not add an anecdote, number, name, date, testimonial, or result that the source didn't contain.

When a passage is flat and there's nothing concrete to work with, it cuts it, sharpens from elsewhere in the same document, or flags it with a specific question. Every job ends with a "Needs your input" list when one applies.

## Files

| File | What it does |
| --- | --- |
| `SKILL.md` | Core rules, the 8-pass workflow, format routing, scoring |
| `references/tells.md` | Pattern library — phrases, structures, false agency, passive voice, narrator distance, quotables |
| `references/formats.md` | Per-platform norms: article, LinkedIn, X, Reddit, email, docs, landing page, slides, script, academic, legal |
| `references/voice.md` | Building and reusing a voice profile from your own writing samples |
| `references/persuasion.md` | Integrity checks for sales and marketing copy |
| `references/examples.md` | Before/after calibration, including the cases where the right move is a small edit plus a question |
| `scripts/detect.py` | Scanner — line-numbered pattern flags and rhythm metrics |

## Scanner

```bash
python scripts/detect.py draft.md --report
python scripts/detect.py draft.md --min-severity high --report
cat draft.md | python scripts/detect.py - --json
```

Standard library only. Skips code fences, tables, inline code, URLs, and front matter, so nothing untouchable gets flagged.

Flags are candidates, not verdicts. Every pattern in the library has a legitimate use somewhere — `tells.md` says where.

## What it deliberately doesn't do

Optimize for AI detectors. They're unreliable in both directions and flag non-native English speakers and technical writing at elevated rates. The skill targets writing quality; detector scores are not a goal.

## Voice profile

For anything published under your name, "sounds human" is the floor and "sounds like you" is the target. Give Claude three to five things you wrote and liked, and it will write a `voice-profile.md` into your working folder for reuse. See `references/voice.md`.

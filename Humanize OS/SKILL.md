---
name: humanize
description: "Rewrite AI-sounding text so it reads like a person wrote it — removing filler, formulaic structures, false agency, narrator distance, and manufactured quotables — while preserving every fact, number, and technical detail exactly. Use this skill whenever the user asks to humanize, de-slop, de-AI, depersonalize-the-robot-voice, 'make this sound less like ChatGPT', fix stiff or corporate copy, edit a draft for voice, or clean up any text they paste or attach — including .md, .txt, .docx, .pptx, .xlsx, .pdf, email drafts, landing pages, LinkedIn or X posts, scripts, and documentation. Trigger it even when the user just says 'fix this writing', 'this reads like AI', or drops a file and asks for a rewrite."
---

# Humanize

Take text that sounds machine-generated and make it sound like a specific person wrote it, without changing what it says.

## The one rule that overrides everything

**Never invent.** Every concrete detail in the output must exist in the input.

This skill is subtractive on facts. It can cut, sharpen, reorder, and rephrase. It cannot add an anecdote, a number, a name, a date, a customer quote, a result, or a personal memory that the source did not contain.

The temptation is real: flat text usually lacks personality *because* it lacks specifics, and the fastest way to add personality is to make up a war story. Don't. A fabricated "we shipped this in six weeks and it nearly killed us" is worse than the bland sentence it replaced, because the user may publish it under their own name.

When a passage is flat and there is nothing concrete to work with, do one of these instead:

- Cut it. Most filler paragraphs say nothing and lose nothing.
- Sharpen what is already there — the vague noun probably has a specific referent elsewhere in the document.
- Flag it. Put the passage in the "Needs your input" section of your output and say what detail would fix it: *"Paragraph 3 claims the process is 'significantly faster' — what's the actual number?"*

Asking beats guessing. A short list of good questions is a better deliverable than confident fiction.

## What counts as untouchable

Leave these byte-identical, always:

- Code blocks, commands, config, file paths, variable names
- Numbers, dates, prices, measurements, statistics, units
- Proper nouns, product names, job titles, citations, URLs
- Formulas, specs, legal or compliance language, disclaimers, quotes from real people
- Anything inside a quotation attributed to someone

You humanize the prose *around* technical content, never the technical content itself. Formal and technical writing gets flagged as AI-sounding partly because precision reads as stiffness — that's a false positive, and stripping the precision to fix it makes the document worse.

## Workflow

### 0. Load the input and preserve

Read the file. Identify and write down (for yourself, not the user):

- What the piece is trying to do and who reads it
- Facts, terminology, and claims that must survive
- Any voice that's already present — a real writer's tics are the thing you're protecting, not the thing you're cleaning

If the user has a voice profile on file, load `references/voice.md` and apply it.

### 1. Detect before rewriting

Run the scanner:

```bash
python scripts/detect.py <file> --report
```

It reports line numbers and pattern names for phrase-level tells, false agency, passive constructions, narrator distance, manufactured quotables, and rhythm problems (sentence-length uniformity, repeated sentence openings, paragraph symmetry, three-item lists).

Run this before you rewrite anything. It gives you a concrete target list, which keeps you editing passages instead of regenerating the whole document — and regeneration is how voice gets flattened and facts get dropped.

The scanner is a detection aid, not a verdict. A flagged line may be fine. Read `references/tells.md` to understand what each pattern is and when it's legitimate.

### 2. Repair the smallest unit that fixes the problem

Work sentence by sentence and paragraph by paragraph. Rewrite a full section only when the section's structure is itself the problem.

### 3. Ground

Replace abstractions with what they actually refer to — but only using material already in the document. "The situation" becomes the specific event named two paragraphs up. "Significant improvement" becomes the number in the table. If the referent genuinely isn't there, flag it rather than filling it.

Put the actor back in the sentence when the document tells you who the actor is. Don't invent one: if the source says "the decision was made" and never says by whom, leave it or flag it. Manufacturing "the team decided" asserts something you don't know.

### 4. Rhythm

Vary sentence length and paragraph shape. Check that you haven't produced a new metronome — short-punchy-short-punchy is as recognizable as uniform-medium-length.

Don't mechanically delete em dashes, adverbs, passive voice, or Wh- openings. Each has legitimate uses. Judge function, not form.

### 5. Restore voice

Cleanup flattens. Read the original again and put back the deliberate choices you sanded off — the odd word, the long digressive sentence, the joke, the unfashionable semicolon. If the author writes a certain way on purpose, that's the signal, not the noise.

### 6. Density

Cut words and sentences that do no work. Stop before you cut nuance — compression that turns a hedged claim into an absolute one has changed the meaning, which violates the preservation rule.

### 7. Score and revise

Rate 1–10 on each:

| Dimension | Question |
| --- | --- |
| Directness | Does it state things rather than announce them? |
| Rhythm | Does sentence and paragraph structure vary naturally? |
| Trust | Does it respect the reader's intelligence? |
| Authenticity | Does it sound like a person rather than a model? |
| Density | Is every sentence doing work? |

Plus two hard gates that are pass/fail, not scored:

- **Fidelity** — every fact, number, and name traces back to the input. Any failure here means revise, regardless of the other scores.
- **Non-manipulation** — no invented urgency, fake social proof, or pressure that wasn't in the original. Applies to marketing and sales copy especially; see `references/persuasion.md`.

Below 35/50, or either gate failing, means another pass. Re-score after revising, because rewrites introduce their own tells.

The score measures whether the prose avoided known patterns. It does not prove a human wrote it, and this skill does not optimize for AI-detector scores — detectors are unreliable in both directions and flag non-native English speakers and technical writing at elevated rates. Write well; ignore the detectors.

## Handling different input formats

Humanize the prose, return the original format.

| Input | Approach |
| --- | --- |
| `.md`, `.txt`, pasted text | Edit directly. Preserve heading structure and any front matter. |
| `.docx` | Use the `docx` skill so styles, tracked changes, and formatting survive. Edit text runs in place. |
| `.pptx` | Use the `pptx` skill. Humanize slide text and speaker notes. Respect the character budget — a slide is not a paragraph. |
| `.xlsx` / `.csv` | Use the `xlsx` skill. Only touch free-text cells (descriptions, notes, comments). Never touch data, headers, or formulas. |
| `.pdf` | Extract with `pdf-reading`, humanize, then ask the user whether they want the result as text, `.md`, or a rebuilt `.docx`. Don't silently change their format. |
| Code files | Humanize comments, docstrings, and README prose only. Code is untouchable. |

Then apply the format adapter in `references/formats.md` — a LinkedIn post, a support email, and API documentation each have different norms for length, contractions, and directness, and applying the same "human voice" to all three is its own tell.

## Output

Deliver in this order:

1. **The humanized text.** Clean. No inline commentary, no tracked-change markup, no "[revised]" labels.
2. **What changed** — three to six lines naming the main patterns removed. Not a diff.
3. **Needs your input** — only if it exists. The flagged passages where the source was too vague to sharpen honestly, each with the specific question that would resolve it.

Never narrate the methodology inside the humanized text itself.

## Scope control

Default to editing what the user gave you. If a document needs restructuring rather than line-editing, say so and ask before doing it — "this reads like AI" and "reorganize my argument" are different requests, and doing the second when asked for the first destroys work the user may have wanted.

## Reference files

Read these as needed rather than upfront:

- `references/tells.md` — the pattern library: phrases, structures, false agency, passive voice, narrator distance, manufactured quotables. Read during detection.
- `references/formats.md` — per-platform norms. Read once you know the target format.
- `references/voice.md` — how to capture a voice profile from samples and reuse it. Read when the user wants their own voice, not just neutral human.
- `references/persuasion.md` — ethical influence checks for sales and marketing copy. Read when the text is trying to get someone to do something.
- `references/examples.md` — before/after transformations. Read when you want calibration on how hard to edit.

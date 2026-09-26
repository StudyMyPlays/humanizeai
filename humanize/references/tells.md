# Pattern library

Detection heuristics, not a blacklist. Every pattern here has a legitimate use somewhere. The scanner flags candidates; you decide.

Contents:
1. Filler and throat-clearing
2. Vocabulary tells
3. Structural formulas
4. False agency
5. Passive voice
6. Narrator distance
7. Manufactured quotables
8. Rhythm and cadence
9. Reader-trust violations
10. When a flagged pattern is actually fine

---

## 1. Filler and throat-clearing

Openers that delay the sentence: *Here's the thing. It turns out that. The truth is. What's interesting is. Let's be honest. Make no mistake. At the end of the day. When it comes to. In today's landscape. It's worth noting that. It should be noted. It is important to.*

Fix: delete the opener and start at the content. "It turns out that most teams struggle with alignment" → "Most teams struggle with alignment."

Emphasis crutches that add no information: *truly, really, very, incredibly, remarkably, fundamentally, essentially, in essence, absolutely, literally* (when not literal).

Meta-commentary about the text itself: *In this section we'll explore. Before we dive in. Let's unpack this. Now that we've covered X, let's turn to Y.* Headings already do this work.

---

## 2. Vocabulary tells

| Tell | Replace with |
| --- | --- |
| enhance, optimize, leverage, facilitate, maximize, utilize | boost, make easier, use, push |
| robust, seamless, comprehensive, holistic, multifaceted | the specific property you mean |
| dynamic, synergistic, paradigm shift, game-changing | cut entirely |
| delve, navigate, embark, unlock, harness, foster, underscore | plain verbs |
| landscape, ecosystem, journey, space (as in "the X space") | the actual thing |
| stakeholders, various stakeholders | who specifically — buyers, managers, the ops team |
| significant, substantial, considerable | the number or the consequence |
| challenging, complex, nuanced | the actual constraint |

The substitution table is the weakest tool here. Swapping "leverage" for "use" makes the sentence less annoying but no more human. The real fix for most of these is specificity: the word is vague because the thought is.

---

## 3. Structural formulas

**Binary contrast.** *Not because X. Because Y.* / *It's not about X, it's about Y.* / *X isn't Y. It's Z.*
Occasionally earns its place. Twice in a document is a tic; three times is a template.

**Negative listing.** *This isn't a story about failure. It isn't a story about luck either.* Defining by elimination before stating the thing.

**Rhetorical setup.** *What if I told you… Here's what I mean… Think about it… Ask yourself…* Just say the point.

**Dramatic fragmentation.** *Speed. Quality. Cost. Pick two. That's it. That's the tradeoff.* One fragment is emphasis. A stack of them is a performance.

**The triad reflex.** Three parallel items, three examples, three-part sentences, everywhere. Real writing has ones, twos, and fives in it.

**The closing pivot.** Every paragraph ending on a short punchy reversal. Vary where paragraphs land — some should just stop.

**Symmetrical hedging.** *While X is true, it's also true that Y.* Repeated, it signals a model balancing rather than a person thinking.

---

## 4. False agency

Abstract or inanimate subjects performing human actions. This is the highest-value tell because it's rarely deliberate and always hides the actor.

| Construction | Repair — only if the source names the actor |
| --- | --- |
| A complaint becomes a fix. | The team fixed it that week. |
| The decision emerges. | The team decided. |
| The culture shifts. | People changed how they worked. |
| The conversation moves toward… | Someone steered it toward… |
| The data tells us… | The analysts found… |
| The market rewards… | Buyers pay for… |
| The architecture demands… | The architecture requires — or: we had to, because… |

Test: *who actually did this?*

**Critical constraint:** if the document never says who, you cannot supply one. "The team decided" when the source says "the decision was made" is a fabricated attribution. Either leave the construction, rephrase without inventing ("the decision went the other way"), or flag it for the user.

---

## 5. Passive voice

Not a grammatical sin. The question is whether the passive is hiding someone.

*X was created. It is believed that. Mistakes were made. The decision was reached. Concerns were raised.*

Keep the passive when: the actor is genuinely unknown, the actor is irrelevant, the object is the real topic of the sentence, or scientific and legal convention calls for it. "The samples were incubated for 48 hours" is correct writing, not a tell.

Same constraint as above — naming the actor requires knowing the actor.

---

## 6. Narrator distance

Prose that hovers above the subject and reports on it.

| Detached | Grounded |
| --- | --- |
| Nobody designed this. | You don't sit down and decide to… |
| This happens because… | The constraint is… |
| People tend to… | Teams often… / You… |
| This is why… | The reason is… |
| One might consider… | Consider… / You can… |

Second person and concrete participants close the distance. Don't force it into genres where it doesn't belong — a research paper should not address the reader as "you."

---

## 7. Manufactured quotables

Grammatically clean sentences engineered to be screenshotted. Symmetrical wording, dramatic reversal, slogan endings, compressed wisdom.

*The best teams don't optimize for output. They optimize for learning.*
*Culture isn't what you say. It's what you tolerate.*
*The problem was never the technology. It was always the people.*

Inspect any sentence that sounds quotable. Some are genuinely the author's best line and should stay. The test: does it say something the surrounding text doesn't already say? If it's a restatement dressed as an epiphany, cut it.

---

## 8. Rhythm and cadence

Flags worth checking:

- Four or more consecutive sentences within a few words of the same length
- Several sentences in a row opening with the same word or construction
- Paragraphs all landing at the same length
- Fragments stacked for emphasis
- Every paragraph ending on a punch line

Fix by varying, not by inverting. Replacing uniform-long with uniform-short is a different monotony.

Em dashes are not evidence of anything. Neither are contractions, or the absence of them. Judge by function.

---

## 9. Reader-trust violations

- Announcing what you're about to say before saying it
- Justifying why a point matters instead of making it matter
- *Let that sink in. Think about that. Notice how. Remember:*
- Reassurance the reader didn't ask for: *And that's okay. Don't worry. You're not alone.*
- Explaining the structure of the piece inside the piece
- Manufactured intimacy — simulated confidences, fake vulnerability, "between you and me"

---

## 10. When a flagged pattern is actually fine

Do not edit a pattern out when:

- It's a direct quotation from a real person
- It's genre convention (legal disclaimers, scientific passive, API reference terseness)
- It's the author's established voice, visible across their other work
- Removing it would change the meaning or weaken a necessary hedge
- It's a term of art — "optimize" in a performance-engineering doc means something specific
- The alternative is a worse cliché

A skill that mechanically strips every flagged construction produces its own recognizable output. Variation in *how much* you edit is part of the job.

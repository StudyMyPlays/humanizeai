# Before / after

Calibration, not templates. Copying these phrasings produces a new recognizable style.

---

**Throat-clearing + binary contrast + reader-trust violation**

Before: "Here's the thing: building products is hard. Not because the technology is complex. Because people are complex. Let that sink in."

After: "Building products is hard. Technology is manageable; people aren't."

---

**Filler + unrequested reassurance**

Before: "It turns out that most teams struggle with alignment. The uncomfortable truth is that nobody wants to admit they're confused. And that's okay."

After: "Most teams struggle with alignment. Nobody admits to being confused."

---

**Jargon stack**

Before: "In today's fast-paced landscape, we need to lean into discomfort and navigate uncertainty with clarity. This matters because your competition isn't waiting."

After: "Move faster. Your competition is."

---

**Dramatic fragmentation**

Before: "Speed. Quality. Cost. You can only pick two. That's it. That's the tradeoff."

After: "Speed, quality, cost — pick two."

---

**Rhetorical setup**

Before: "What if I told you that the best teams don't optimize for productivity? Here's what I mean: they optimize for learning. Think about it."

After: "The best teams optimize for learning, not productivity."

---

**False agency, actor available in the source**

Source context: an earlier paragraph says the platform team owns deploy tooling.

Before: "The deployment process was overhauled and the decision was reached to consolidate on a single pipeline."

After: "The platform team overhauled deployment and consolidated on a single pipeline."

---

**False agency, actor NOT available — the flag case**

Before: "The decision emerged that the feature would ship without the analytics layer."

After: "The feature shipped without the analytics layer."

Note to user: "Paragraph 4 never says who made the call to drop analytics. I rewrote it as a plain statement of what happened rather than inventing an owner — if you want the decision attributed, tell me who."

Do not write "leadership decided" or "the team chose." Neither appears in the source.

---

**Vague quantifier — sharpened from elsewhere in the document**

Before: "The migration delivered significant performance improvements across the board."

Source contains a table showing p95 latency going from 840ms to 210ms.

After: "The migration cut p95 latency from 840ms to 210ms."

This is legal because the number was already in the document. Writing "cut latency by 75%" when no table exists is not.

---

**Vague quantifier — nothing to sharpen with**

Before: "The migration delivered significant performance improvements across the board."

After: "The migration improved performance."

Note to user: "'Significant... across the board' doesn't say anything a skeptical reader would accept. What's the actual before/after number? One figure here would carry the whole paragraph."

The edit is small on purpose. Cutting the inflation is honest; replacing it with invented precision is not.

---

**Manufactured quotable that's a restatement**

Before: "Teams that measure the wrong thing optimize the wrong thing. Measurement is destiny."

After: "Teams that measure the wrong thing optimize the wrong thing."

The second sentence adds nothing but cadence.

---

**Manufactured quotable that earns its place — leave it**

Before: "We spent eight months building a feature three customers asked for and none of them used. Expensive listening."

Leave it. It's compressed and a little sharp, but it follows a concrete fact and says something the setup didn't.

---

**Rhythm — a new monotony introduced by over-editing**

Over-edited: "Ship fast. Learn faster. Cut what fails. Keep what works. Repeat."

Better: "Ship fast and cut what fails. The teams that do this well aren't smarter, they just find out sooner."

---

**Technical content — what not to touch**

Before: "It's worth noting that the `retry_backoff` parameter accepts values between 100 and 30000 milliseconds, with a default of 1000."

After: "The `retry_backoff` parameter accepts values from 100 to 30000 milliseconds. Default: 1000."

The filler opener goes. Every number, the parameter name, and the units stay exactly as they were.

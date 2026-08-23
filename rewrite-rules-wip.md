# Readable technical English: rules, tooling, and the traps

Derived 2026-08-22 while working on
`draft-dogru-scitt-disclosure-evidence-04`. Everything here was tested on real
text the same afternoon. Where a rule failed, the failure is recorded, because
the failures are the most transferable part.

Written so a later reader needs no other source.

---

## 0. What problem this solves

Technical prose that is fluent, grammatical, confident, and hard to read. It
excludes people: readers in a second language, readers with limited time,
readers outside the working group. The text looks like English and does not
function as it.

The defect is **not** vocabulary difficulty. It is low information density
combined with high fluency, plus specialist senses of common words. You cannot
skim it (no redundancy to skip) and you cannot argue with it (no specific claim
to attack).

---

## 1. The rules that survived testing

Adopted from **ASD-STE100** (Simplified Technical English), the aerospace
maintenance standard, Issue 9. Origin matters: it was built because
fluent-but-dense English excluded competent technicians reading a second
language from safety-critical work. Same problem, forty years earlier, in an
industry that had to fix it.

### 1.1 Mechanical rules — check these automatically

| rule | limit |
|---|---|
| sentence length, descriptive text | ≤ 25 words |
| sentence length, procedures | ≤ 20 words |
| sentences per paragraph, procedures | ≤ 6 |
| voice | active |
| tense | present where possible |
| `-ing` forms as nouns (gerunds) | none |
| noun clusters | ≤ 3 words |

**Use the maximum, not the median.** A text with median 12 can hold a 31-word
sentence. Median hides tails; that is the whole reason STE sets a cap.

### 1.2 Vocabulary

ASD-STE100 Part 2 is a controlled dictionary: ~851 approved words, each with
**one** permitted meaning and one part of speech, plus ~1,301 explicitly
unapproved words with suggested alternatives.

Machine-readable extraction of Issue 9 (January 2025):
`github.com/sourdough-bread/asd-ste100-checker`, file
`ste100/dictionary/data/dictionary.json`. ASD provide the spec free for
individual use. The extraction is third-party and unaudited.

**Technical Names and Technical Verbs are permitted** outside the dictionary.
Defined domain terms are not violations.

⚠ **Do not apply the dictionary wholesale to a specification.** See §4.3.

---

## 2. The claudisms list — cut these in every register

From a working list we keep, plus an external register review.

- **Negation-first reveal** — "It is not X. It is Y." staged against a reading
  nobody proposed. Earned *only* if the previous paragraph actually proposed X.
  Highest-frequency tic; also appears as the bare contrast pair "X, not Y".
- **Significance designation** — "the actual question", "the part that matters",
  "what is interesting here": ranking the reader's attention instead of saying
  the thing.
- **Abstraction agency** — tables show, medians hide, machinery is proportionate,
  failure modes live. Put a real subject in the subject slot.
- **Deferred noun** — "One thing is not flat" when the noun is available.
- **Coy or thesis headers** — a header is a label; it can *be* the definition.
- **Colon-staged intro** — "So:", "The defensible statement:" as a drum roll.
- **Aphoristic closer** that withholds its referent.
- **Staccato fragments** as gravitas.
- **Self-grading / move-narration** — "that distinction changes what you would
  predict" instead of making the move.
- **Performed humility** — "their phrasing is better than mine".
- **Structural-metaphor locator** — "the seam where", "the hinge", "the fault
  line". Name the mechanism.
- **Suspense construction** — "here's where it gets interesting".
- **Rhetorical question + fragment answer.**
- **Straw-man knockdown** — quoting a wrong reading attributed to the reader.
- **Em-dash density** — more than ~1 per 150 words reads machine-written.
- **Inflation** — "collapse" for a 30-point drop; "exactly" as intensifier.

Signposts are the cheapest cut: "Now the problem, which comes from the code."
"Here is my difficulty." Three of those pointed at things the reader was about
to read anyway; removing them cost nothing.

---

## 3. Method: how to validate a writing metric

**Never adopt a metric you have not calibrated.** Two of three metrics tried
today scored *backwards*.

### 3.1 Calibration pairs
Two texts, **identical content**, known-different readability (ideally one that
a human has called hard to read). Any candidate metric must rank them correctly.

### 3.2 The gaming test
Deliberately try to **pass the metric while making the text worse**. Ten minutes.
If you succeed, the metric cannot be a gate.

### 3.3 Self-normalisation
Compare a section against **its own document's body text**. Author, subject and
expertise are held constant, and no cross-genre threshold is needed — which is
what kills absolute gates (§4.1).

Worked example: the draft's abstract vs its own body —
median sentence 28 vs 21, longest 61 vs 56, anchors 5.4 vs 38.5 per 1,000 words.
The abstract is an outlier inside its own document.

---

## 4. Traps — every one of these was hit for real

### 4.1 Absolute density thresholds are genre-dependent and invertible
Proposed gate: "concrete anchors 55–60 per 1,000 words". Result:

| version | words | median sent | longest | anchors | verdict |
|---|---|---|---|---|---|
| A published abstract | 186 | 28 | 61 | 5.4 | — |
| B rewritten for readability | 142 | 12 | 24 | **14.1** | **fails the gate** |
| C published + cross-references, nothing improved | 230 | 32 | 77 | **78.3** | **passes the gate** |

Writing it well failed; padding it with section references passed. Inverted, and
inverted toward a behaviour specification authors already have an incentive to
adopt. The STE 25-word rule ranked all three correctly.

### 4.2 Nominalisation density scores backwards on a rewrite
`-tion/-ment/-ance` counting is the standard measure and the countable form of
"characters as subjects". On a content-preserving rewrite it went **up** when the
text improved (53.2 → 60.1), because compression strips verb-heavy connective
prose and leaves content nouns.

🔑 **A rule applied at composition time is not the same object as a metric
applied at review time.** STE bans nominalisations while writing, which works.
Counting them afterwards does not.

### 4.3 A general dictionary collides with defined domain terms
STE wanted `origin` → `source`. In this document "source" already means *the
data source*. Following the dictionary would have created exactly the
one-word-two-meanings ambiguity STE exists to prevent, and no checker can see it.

**Rule: domain terminology outranks the dictionary. Unapproved beats ambiguous.**

### 4.4 Short sentences of common words in specialist senses pass every check
These passed sentence length, voice, gerund and cluster rules, and were
unreadable:

> It reports no bare pass. It reports no result stronger than the declaration it
> used.

"Bare pass" and "stronger" are the draft's specialist senses of ordinary words.
Only the one-word-one-meaning dictionary rule catches this class.

⚠ **Worse than a long sentence.** A long sentence looks hard, so the reader
slows down. This looks easy, so they read on and lose the thread.

### 4.5 Compression removes courtesy, and the metric calls that an improvement
Pushing density stripped two clauses doing diplomatic work: the reason the
author's design choice was reasonable, and the concession that a gap is hard to
see from inside. Both carry no facts, so a density metric scores them as padding.

**An information-density metric will always score generosity as waste.**

### 4.6 Density and simplicity trade against each other
STE vocabulary made every text **longer**: review 171 → 252 words, abstract
162 → 211. Plain words need more of them. "Snapshotted at both ends of a time
window" becomes "read at the start of the window and again at the end".

Fixing vocabulary also pushed one sentence from 24 to 27 words and forced a
re-split. Expect to iterate between the two rules.

**"Shorter" was never the goal.** Of nine abstract revisions, the last four each
got longer and each was better.

### 4.7 Compression into inaccuracy
Three times in one afternoon, a shorter sentence became a *false* one. Example:
the draft requires each bound to be labelled `protocol-defined | measured |
operator-declared | undeclared`. This was compressed to "nobody measures what the
operator states" — which reads as *nothing is measured* and is wrong.

**Every compression is an edit to meaning until proven otherwise. Re-read the
source, not your previous draft.**

### 4.8 Self-assessment does not work
One of us measured information density across 1,600 mailing-list messages that
morning, then could not see the same problem in our own paragraph written an hour
later. (Our own prose throughout — not the draft's.) One line of external feedback
("hard to read") produced a 56% cut with no content lost.

Later, a "restructure" that was reported as an improvement scored *worse* on
sentence length (median 14 → 18) because two added paragraphs were written long.
The tool caught it; we had not.

**Corollary: the reviewer must be someone who has not read the source document.**
When rewriting someone else's text, the missing referent is already in your head,
so you simplify the sentences around the jargon and leave the jargon in place.
This happened twice and was caught by a reader both times.

---

## 5. Deployment: mirror, not gate

- **Advisory, never a gate.** §4.1 shows how fast a gate is gamed.
- **Private to the author, before anyone else sees it.** What works is being
  told, not being caught. A public score becomes a pillory, then a target.
- **Authorship-neutral.** It never asks who or what wrote the text. This is the
  decisive property: AI detectors false-positive on non-native English writers,
  because careful, slightly formal, low-idiom prose is what a good
  second-language writer produces. A readability mirror helps that writer; a
  detector accuses them.
- **Self-normalised** (§3.3) so no cross-genre threshold is needed.
- **Report the maximum, not the average** (§1.1).

Target the artefact, not the author. "The abstract must be readable by a
competent engineer outside the working group" is checkable by a human in ten
seconds and applies identically to a human who writes 40 messages a week.

---

## 6. Tooling used

Both were ~40 lines of Python with no dependencies. **Neither ships with this
repo**, so no measurement here is reproducible from it; the figures below are
ours, and the method is described rather than executable.

**Rule checker** — sentence length (max, not median), sentences per paragraph,
passive voice, `-ing` gerunds, noun clusters. Known limits: no POS tagger, so
copulas read as passives ("is one"), adjectives read as gerunds ("missing"), and
verbs read as nouns in cluster detection. **Read every flag; do not trust the
count.**

**Vocabulary checker** — loads `dictionary.json`, reports words whose status is
`unapproved`, with the suggested alternatives. Same POS caveat: it flags a noun
against a verb entry. On the final abstract it produced 7 flags and 0 real
violations.

---

## 7. Worked result

> ⚠ **These figures come from the hand-written abstract revisions produced
> while deriving the rules, not from `draft-rewritten.md`.** They will not
> match `rewrite-report.md`, which measures the actual rewrite with a
> different sentence splitter. Both are stated rather than reconciled,
> because sentence counting over hard-wrapped definition lists is
> method-dependent and neither number is authoritative. Where they differ,
> `rewrite-report.md` is the one about the file in this repo.


Draft abstract, before and after, same content:

| | words | sentences | median | longest | over 25 |
|---|---|---|---|---|---|
| as published | 186 | 6 | 28 | 61 | 3 (50%) |
| final | ~230 | 22 | 10 | 21 | 0 |

Longer, and easier to read on the measures in this document. That is the trade,
and it is the right one for a
specification whose readers are doing careful work in a second language.

---

## 8. Order of operations

1. Rewrite for **meaning** first: is every claim still true against the source?
2. Apply the **mechanical rules** (§1.1). Split on the maximum.
3. Apply **vocabulary** (§1.2), respecting §4.3.
4. Re-run §1.1 — vocabulary changes lengthen sentences (§4.6).
5. Cut **claudisms** (§2).
6. Check for **specialist senses of common words** (§4.4). This needs a human.
7. Give it to **someone who has not read the source** (§4.8).
8. Restore any **courtesy** the density pass removed (§4.5).

## 9. Forward dependencies (added 2026-08-23, from a real reader's two trips)

**The rule: avoid forward *dependencies*. Where the content cannot be moved
earlier, name the dependency at the point where the reader forms the objection.**

⚠ **This is NOT "avoid forward references" — that would delete the fix.** A
forward *reference* ("the counter-reset case is treated in §6") is the cheap
cure. A forward *dependency* is the disease: text whose meaning needs material
the reader has not reached yet, left unsignposted, so the reader carries a
false objection for pages.

**Where this came from.** A reader read draft-dogru-scitt-disclosure-evidence-04
cold and was tripped twice by the same shape:
- §4.3 invalidates a window on counter regression while §1 asks the reader to
  trust the counters. It reads as a contradiction. §6 resolves it — fifteen
  pages later, with nothing at §4.3 saying so.
- §4.3's clock-skew machinery reads like a workaround for something NTP would
  fix. §4.4 gives the actual argument (a synchronised clock is an operator
  *declaration*, not a measurement). Again, no pointer at the point of doubt.

Both objections were answered by the document. Neither was answered *where the
reader had them*. One tripped reader is an anecdote; the same shape twice is a
structural property of the document.

### 9.1 It must stay advisory prose, never a metric

⛔ **Do not turn this into a count of cross-references.** §4.1 already measured
that failure on this exact document: version C, *"published + cross-references,
nothing improved"*, scored **78.3 anchors and passed the gate** while the
genuinely better rewrite failed it. A rule that rewards pointers gets "see §4.4,
see §6, see §5.2" sludge, which is worse than the silence it replaces.

### 9.2 Signpost; do not reorder

⛔ **A rewriter does not move another author's sections.** Reordering is editing
someone's document, not rewriting their prose, and it changes what the section
numbers mean for everyone already citing them. The rewriter's move is to **add
the pointer**; hoisting material is a recommendation to make to the author, in
the notes, not a change to make silently.

### 9.3 How to find them

A whole-document pass, not a per-section one — a section read in isolation
cannot show this. For each place the text raises a tension, a risk, or an
apparent contradiction, ask: **is it resolved here, or later?** If later, and
nothing at this point says so, that is a forward dependency. Record it in the
rewrite notes as *"tension raised in §X, resolved in §Y, no pointer at §X"*.

## 10. Ad-hoc terminology (added 2026-08-23, after we broke this in the commit that added §9)

**The rule: coin a term only when repetition makes the plain description
unworkable. If you coin one, define it at first use, say it is yours, and use
exactly one name for it.**

Coining is not itself the fault. The concept §9 describes appears about thirty
times in `forward-dependencies.md`, and repeating *"a place where the draft
answers an objection later than the reader forms it"* thirty times would be
unreadable. The fault is shipping a private label as though it were public
vocabulary.

### 10.1 Earn it

If the concept appears two or three times, spell it out. **The test is whether
the label saves the *reader* work or saves the *writer* work.** A term that
exists so the writer can stop explaining is a cost transferred to the reader.

### 10.2 Disclose it

A coined term reads as established vocabulary, so a reader who does not
recognise it assumes the gap is theirs and goes looking for a source that does
not exist. Say plainly that it is your name for the thing.

⚠ **In a specification this matters more than in prose.** A new term implies a
defined concept with boundaries — an implementer may reasonably expect it to be
testable. Introducing one without a definition invites exactly the guessing that
a definitions section exists to prevent.

### 10.3 Use exactly one name

Two names for one idea is worse than a clumsy plain phrase, because the reader
spends effort deciding whether they are two ideas.

**What we did, recorded because it is the whole reason this section exists:** the
commit that added §9 shipped **two** coined names for one concept. This file
called it a *forward dependency*; the analysis file called it a *forward
tension*, four times, and was named `forward-tensions.md`. Neither file said the
term was ours. A reader would have met a filename naming a term they had never
seen, then found a different term for it in the rules, with nothing marking
either as ten minutes old. Unified on *forward dependency* the same day.

### 10.4 Why this recurs

**Naming a pattern feels like discovering it.** That is the incentive, and it is
worth naming because it does not go away once you know about it. It is the same
instinct as the *structural-metaphor locator* in the claudisms list (§2) — "the
hinge", "the seam where" — wearing a lab coat. The question that defuses it: if
the label were removed and the plain description put back everywhere, would the
reader lose anything?

## 11. Rewrite the non-normative prose, and leave the normative sentences alone

**The rule: a sentence containing a BCP 14 keyword is reproduced verbatim. Only
sentences without one are rewritten.**

This began as an objection from a draft's author, and it is the strongest single
result the experiment has produced.

### 11.1 The objection

> *"I will not take the rewritten prose wholesale — the normative text has to
> stay something I can defend line by line."*

That is correct and it is not negotiable. An author who cannot defend a
normative sentence has lost the thing the document is for. It looks like a
ceiling on the whole method.

### 11.2 It is not a ceiling. It is a limit on about a sixth of the problem

Measured on `draft-dogru-scitt-disclosure-evidence-06`:

```
331 sentences
135 over the 25-word line
 23 of those contain a BCP 14 keyword
112 of those contain none          <- 83%
 normative sentences are 13% of the whole document
```

**The density that makes a draft hard to read is almost entirely in prose that
carries no normative weight.** Rewriting only the keyword-free sentences takes
that draft from **42.9% over the line to 8.3%**, without touching one normative
statement.

It is not one lucky document. Across **162 prose-dominated drafts**: a median
**84%** of over-long sentences are non-normative, and the median draft would go
from **27.2%** over the line to **4.2%**.

### 11.3 Why this is worth more than the four points it costs

Leaving every BCP 14 sentence byte-identical gives up a little readability and
removes the entire reason to refuse the rewrite. **It converts a promise into a
checkable property**: a checker can confirm that no normative sentence moved.
Nobody has to trust the tool, or us, on the point that matters most.

⚠ **Do not verify this with a plain `diff` — it cannot do it.** The source is
hard-wrapped at 72 columns and the rewrite is not, so *every* normative sentence
differs in whitespace, and a word split across a line break (`non-\nauthoritative`)
differs in hyphenation as well. A diff therefore reports that all of them changed.
The check that does work compares the BCP 14 sentences with line wrapping and
hyphenation normalised away, and normalises nothing else; it fails if any of them
really moved. We run one (`check-normative.py`) after every rewrite and ship its
output alongside the result, so the author does not have to build it.

A rewrite report should therefore state the BCP 14 sentence count as *unchanged
and verifiable*, not as *carefully preserved*.

### 11.4 ⚠ Two limits on the numbers, stated because they are easy to overclaim

- **4.2% is a ceiling, not a prediction.** It assumes every non-normative long
  sentence lands under the cap. The real run on the SCITT draft reached 0.2% in
  the sections it processed, so it is achievable — but do not quote the ceiling
  as a result.
- **"Contains no BCP 14 keyword" is a proxy for "not load-bearing", and it is
  not exact.** A definitions section and a section defining outcome semantics
  carry precise meaning with no MUST anywhere in sight, and deserve the same
  protection. Protect those by **naming the sections**, not by scanning for
  keywords.

# Rewrite report: draft-dogru-scitt-disclosure-evidence-07, register-only rewrite

Arm: REWRITE (register only). Inputs: source.txt (-07), rules-snapshot.md
(sections 0-24 plus claudisms list). Output: rewritten.md.

## Verification

- §11: 46 sentences in the source contain an uppercase BCP 14 keyword. All
  46 are reproduced byte-for-byte, verified with a checker that normalises
  line wrapping and hyphenation only (scratchpad check-normative.py,
  written for this run because the rules' check-normative.py does not ship
  with the snapshot). Result: 46 = 46, zero divergent. The count is stated
  as unchanged and verifiable, per §11.3, not as "carefully preserved".
- §1.1 cap: every non-frozen prose sentence I wrote is at or under 25
  words, checked mechanically. Residual over-25 flags are all frozen text
  (Section 2, Section 4.7, outcome and field definitions), IETF legal
  boilerplate, tables, or splitter artifacts at headings.
- §20: non-ASCII scan over the deliverable. Every remaining hit is either
  a letter in a proper name (Doğru, TEKNOLOJİ, Türkiye) or an em dash
  inside frozen text, where §11 outranks §20 (recorded below).

## Per-rule account of the changes

- §11 (freeze normative sentences). All 46 keyword sentences kept
  verbatim, including their internal em dashes and their §21-defective
  trigger conditions. Interstitial prose around them rewritten.
- §11.4 (protect named sections, not just keyword hits). Section 2
  (Conventions and Definitions) and Section 4.7 (Semantics of the
  outcomes) are reproduced verbatim in full, as a definitions section and
  an outcome-semantics section. The outcome definitions inside 4.3
  (matched .. indeterminate) and the result-statement field definitions in
  4.6 are likewise kept verbatim or near-verbatim. Cost: 4.7's staccato
  register survives; protection outranks register there.
- §12 (a split must conserve the relation). The dominant move of this
  rewrite, applied in reverse: -07 is the revision whose sentence-length
  pass halved stated inter-sentence relations (rules §12.1), so the
  rewrite restores causal/concessive/contrastive links while keeping every
  sentence under the cap. Examples: intro gap paragraphs ("but not what
  happened to the data", "so an allowed request can answer questions"),
  4.3 clock paragraph ("The procedure sets no floor, because a smaller
  offset is harder for a reader to suspect" - the relation the
  Acknowledgments state was the author's reason), 4.4 ("because the
  operator knows it and the Gateway cannot measure it"), 9 (the temporal-
  history passage uses the rules' own §12 compliant split verbatim: "That
  review was commissioned because the fix had loosened a default. It was
  also commissioned because the fix's author was not the party who should
  clear it."). Per §12.4 the adverse n=1 evidence is noted: the one human
  test of restored relations preferred the disconnected version.
- §2 claudisms. Cut throughout: staccato fragment runs (1.3, 3.4, 4.4,
  4.5, 6, 6.1, 9, Acknowledgments) merged with their relations restated;
  aphoristic closers rewritten to plain statements ("Neither layer rescues
  the other. One artefact answers half..." -> "Each artefact answers half
  of a two-part question."; "That is the strongest claim in this area. It
  is the one least often actually made." -> one sentence); drum-roll
  fragment "Two limits, stated rather than left to be found." -> "The
  check has two limits."; negation-first "The multiplicity is not a
  property of the Gateway. It is a property of the deployment." -> one
  positive sentence with mechanism attached.
- §14 (vocabulary follows reader state). Abstract rewritten as one
  compact paragraph, no locally-defined capitalized terms, no citations,
  outcome vocabulary paraphrased ("names every item that did not match,
  instead of reporting a bare pass or fail"). The five outcome names are
  no longer enumerated in the abstract; they are body vocabulary.
- §15 (references live at the claim). "several receipt formats exist" in
  Introduction paragraph 1 now carries the four draft citations at the
  claim - the rules' own worked example. The related-work paragraph stays
  and keeps the discussion.
- §16 + §18 (criterion at the label, claim must exclude an alternative).
  "They share a limit." now states its criterion, and the criterion chosen
  is the non-tautological one §18 derives: "The formats share one limit:
  the party under audit selects the evidence." ("cannot attest what its
  producer did not record" was rejected as the §18 tautology.)
- §17 (definition scope is shown, not narrated). Deleted: "This document
  does not reinvent that. This document defines no new receipt format, no
  policy evaluation semantics, and no transparency mechanism." (intro;
  replaced by the §17 worked fold: "Both structures are payloads for
  registration as Signed Statements on a SCITT Transparency Service
  [RFC9943], whose append-only log a third party can audit."); "This
  document defines no countersignature, no anchoring, and no log format of
  its own." (Section 5 - the rules' own named cut); the abstract's final
  defines-no sentence; "This layering is deliberate." (Section 5); "This
  subsection states the bound so a reader meets it before the procedure."
  (1.1, structure narration, deletion test passed).
- §19 (a problem is three sentences). Intro gap paragraphs tightened to
  name/mechanism/consequence with one example each; restatements deleted
  ("That silence is the failure this document names", "The size is not an
  assertion").
- §20 (ASCII punctuation). All em dashes in prose I wrote replaced by
  role (colon, comma pair, or sentence break), including the two in my own
  masthead caught by the grep. Em dashes inside frozen text remain: §11
  byte-for-byte outranks §20 there. Names keep their non-ASCII letters.
- §22 composition note applied where possible without touching frozen
  text: no rewrite performed on the "policy's vocabulary as much as about
  the data, and MUST be read that way" sentence (frozen); recorded as an
  author finding below.
- §23 (a rule earns one reason, attached). After the frozen clocks-member
  MUST sentence, one why-sentence kept ("A silently ignored fourth field
  declares less than its author believes."); the derived second
  consequence ("The gap shows up as an outcome the operator cannot account
  for.") deleted - the rules' own worked example, adapted because the rule
  sentence is frozen and cannot take an attached colon.
- §24 (the document does not grade its own machinery). 4.5: "It therefore
  needs the tightest reporting rules of the five." replaced with the
  rules' accepted fix: "The rules below therefore make each exclusion
  visible in the result." Also removed grading framings: "The essential
  property is that..." (4.1), "the asymmetry is deliberate" (4.6 counts).
- §4.4 trap (specialist senses of common words). "bare pass" in 1.2
  replaced with "reduces its result to a single pass"; kept in 4.7 (frozen
  section) and in the frozen counts sentence.
- §9 (forward dependencies). Whole-document pass done; -07 already
  carries the pointers the rules' examples demanded (1.1 -> Section 4.3 /
  Section 6; 4.3 -> Section 4.4 skew bound). No new unsignposted forward
  dependency found that a pointer sentence could fix without reordering.
- §8 (order of operations) followed: meaning first, mechanical caps,
  claudisms, specialist senses; courtesy clauses (e.g. "an honest
  statement some deployments need to make", "Session or catalog
  housekeeping is a legitimate exclusion") kept per §4.5.

## Structural / furniture decisions

- Page headers, footers, and page numbers dropped; table of contents kept
  without page numbers, per the task instruction.
- Status of This Memo, Copyright Notice, IANA templates, and References
  kept verbatim: fixed legal/registry furniture, not prose to rewrite.
- ASCII tables converted to Markdown tables with the wording of every
  cell unchanged.
- Section order, numbering, and all technical content unchanged.

## Recorded as author work (out of scope for this arm)

1. §21 - unenforceable MUST: "An implementation encountering a value in a
   field defined here MUST reject the structure." (3.2). The receiver
   cannot decide "this string is a data value". Kept frozen per §11/§21;
   the finding goes to the author (repair options: supply the checkable
   procedure, re-address to the producer, or demote to the definition).
2. §22 - blur-shaped ambiguity inside a frozen sentence (3.4): "The
   absence of a class from the array is therefore a statement about the
   policy's vocabulary as much as about the data, and MUST be read that
   way." The repair (enumerate the two worlds; recast the unverifiable
   MUST as a Consumer presentation rule, MUST -> MUST NOT) changes a
   normative sentence and is the author's.
3. §17 hard form at section scale: headings and sections 1.2 ("What these
   structures do not claim") and 3.4 ("What Transformation Evidence does
   not prove") are built around descriptive negatives. Honing the
   positives until the sections dissolve is re-authoring; only
   sentence-level cuts were made here.
4. §11.4 cost inside protected sections: Section 4.7 and Section 2 retain
   staccato register and em dashes because they are frozen by name; any
   register work there is author work.
5. §13 (build it twice): not run - it is a validation procedure with
   subagent implementers, not a register change. Noted per §13.7 that
   Section 9 (to be removed before publication) carries load-bearing facts
   (skew direction, bounds key names, "the outcome it would have had"),
   already recorded in the rules; promotion into normative text is the
   author's decision.
6. §14 corollary: the abstract no longer enumerates the five outcome
   names. If the author wants them at position zero, that is a content
   decision, not register.
7. §9.2: no sections were moved; no hoisting recommendations arose beyond
   the pointers -07 already contains.

## Rules I could not apply, and why

- §3 (metric calibration), §5 (deployment), §6 (tooling), §7, §13:
  scoped to metric-building, deployment, or validation, not to a rewrite.
- §4.8 (reviewer who has not read the source): requires a second reader;
  cannot be satisfied from inside this run. The rewrite has not had its
  external-reader pass.
- §10 (ad-hoc terminology): no term was coined in this rewrite, so only
  the "don't" half applied.

## Known limits of this run

- Sentence counting over definition lists is method-dependent (rules §7
  warning); the cap check used one splitter and I read every flag rather
  than trusting the count (§6).
- The §11 checker here is my ~40-line reconstruction of the described
  check, not the project's check-normative.py.

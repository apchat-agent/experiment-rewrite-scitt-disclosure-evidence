# Rewrite report — draft-dogru-scitt-disclosure-evidence-07, rules-transfer iteration 3 (REWRITE arm)

Inputs: `source.txt` (-07) and `rules-snapshot.md` (§1–§27 + claudisms). Register-only rewrite; no
structural work performed. Output: `rewritten.md`.

## 1. §11 compliance — checked, not promised

- BCP 14 sentence check (line-wrap and whitespace normalized, nothing else): **45 keyword-bearing
  sentences in the source, 45 in the rewrite, 0 differ**. Unchanged and verifiable, not "carefully
  preserved". (Checker run in-session; the boilerplate BCP 14 key-words paragraph is additionally
  kept verbatim inside frozen Section 2.)
- §11.4 named sections frozen whole and verified identical after normalization:
  **Section 2 (Conventions and Definitions)** and **Section 4.7 (Semantics of the outcomes)**.
- Section order and numbering: unchanged, 1–10 plus subsections, ToC reproduced without page numbers.
- Page furniture dropped: running headers/footers, page breaks, dot leaders.
- Also kept verbatim: Status of This Memo, Copyright Notice (fixed IETF boilerplate), References,
  both IANA registration templates and registry tables (reformatted as markdown lists/tables, text
  unchanged), Author's Address.

## 2. Self-measured texture (counted by script, same method on both files)

| | source.txt | rewritten.md |
|---|---|---|
| prose sentences (body before References; headings/tables/ToC excluded) | 643 | **559** |
| median sentence | 10 | **12** |
| mean | 12.7 | 14.0 |
| longest | 159 (splitter artifact over a field list; real longest is a frozen 4.6 sentence) | 52 (same artifact class) |
| over 25 words | 51 (7.9%) | **33 (5.9%)** |
| ... of which BCP14-bearing (frozen) | 20 | 20 |
| connective-bearing, §12.1 broad word list | 96 (14.9%) | 92 (16.5%) |
| connective-bearing, narrow discourse list (because/therefore/but/however/although/instead/rather than/also/...) | 28 (4.4%) | **26 (4.7%)** |
| narrow share, non-normative sentences only | 3.5% | **3.7%** |

Reading of the numbers, per §3.3 self-normalisation: the §26 target ("connective share in single
digit percent") is met on the discourse-connective list (4.7%, and 3.7% in the prose I could touch),
and the rewrite sits within 0.3 points of the source's own register — the register the reviewer
accepted. The broad §12.1 list lands at 16.5% because it counts if/where/when/unless, which are the
condition words of the normative sentences themselves; 20 of the 33 over-25 sentences are frozen
BCP 14 text, and the remaining 13 are IETF boilerplate (3), frozen Section 2 definitions (2), one
frozen 4.7 sentence, and field-label/enumeration splitter artifacts (value-format lists, outcome
enumerations). Zero over-25 sentences remain in prose that was mine to edit and is not an
enumeration.

Counting method recorded per §7's warning: sentence split on `[.?!]` + space, over hard-wrap
normalization; field-list labels merge into their following sentence, which inflates a handful of
lengths in both files equally. The numbers are comparable to each other and to nothing else.

## 3. §25 — glossary and exemption ledger

### 3.1 Glossary (concept -> chosen word <- words it replaced)

- show <- reveal ("receipt chain does not reveal this"), surface, "differ in a way a digest does not reveal"
- does not show <- "are silent about" (hash chains), "silent about what is missing"
- bind / bound (verb) <- pin / pinned ("digest that pins", "visible and pinned") — except inside frozen text, see ledger
- state <- testify ("the set then testifies to its own extent")
- count(ers) of activity <- "account of activity" / "second account" (coined noun in source §1)
- remove <- "make ... disappear" (4.1)
- population <- account ("either account", intro bullet)
- rewrite after the fact <- "quietly rewrite" (Section 5)
- avoid <- "route around" (Section 6)
- detectable <- "becomes detectable, rather than invisible" (4.1, complement dropped)

### 3.2 Exemption ledger (kept words neither plain nor on the exemption list; one line each)

The exemption list per §25: the document's Terminology section (Section 2 terms), registry values
(five actions; six outcomes; no-exceptions/exceptions), standard names (SCITT, JSON, JCS, CBOR,
COSE, SHA-256, Ed25519, ISO 8601, RFC/I-D anchors, PostgreSQL, npm, TypeScript, IANA), and BCP 14
keywords.

1. **standing** — the source's one word for a bound's provenance (protocol-defined/measured/
   operator-declared/undeclared); locked in by frozen 4.4/4.6 text; kept as the single word.
2. **bound (noun)** — multiplicity/skew bound; defined inside the frozen Mapping Profile entry.
3. **accusation** — kept for one-word-per-concept consistency with the frozen 4.4 sentence
   ("the false accusation this document now guards against").
4. **overclaim** — locked in by the frozen 4.6 counts sentence; used once in my prose (4.4).
5. **bare pass** — source's term for an unqualified verdict; locked in by frozen 4.7; at its one
   use in my prose (1.2) it is defined by the colon that follows it.
6. **bypass / bypassed** — outcome semantics term (frozen 4.7 "Gateway bypass").
7. **skew / multiplicity** — clocks.skew field name; Mapping Profile definition vocabulary.
8. **snapshot** — structure name (activity-snapshot/1) and Window definition vocabulary.
9. **sealed** (6.1, "sealed total", "sealed quantity") — specialist sense (signed over a completed
   set); no one-word plain substitute; meaning carried by the surrounding sentences.
10. **trust statement** (3.4) — source's phrase for the dependency set of the claim; one use.
11. **self-attested** (3.4) — technical compound, standard usage.
12. **housekeeping** (4.5) — deployment jargon for session/catalog maintenance activity; the source
    defines it by example in the same sentence.
13. **pooler / object-relational mapper** (4.4) — component names.
14. **green dashboard** (Acknowledgments) — dedication metaphor, kept as courtesy per rules §4.5.
15. **"For digesting and signing"** (3.3, 8.1, 8.2) — gerund phrase kept: fixed formula shared with
    the IANA templates; rewriting it in one place would fork the wording.

Ledger size: **15 entries.**

## 4. Per-rule log

- **§1.1 mechanical**: all remaining over-25 sentences are frozen, boilerplate, or enumeration
  artifacts (see §2 above). Active voice restored where the agent exists ("Window validity is
  checked first" -> "The reconciler checks Window validity first"; "A Mapping Profile is therefore
  declared by the operator" -> "The operator therefore declares the Mapping Profile"). Gerund-noun
  removals: "detecting the cut needs" (1.1), "Accepting an unknown prefix ... would let" (6),
  "renumbering them ... would break" (9), "neither was found by reading this document" (9),
  "He proposed applying" (Acks), "What the implementation is forbidden to do is state" (4.3).
- **§2 claudisms**: cut or repaired — "The essential property is that" (significance designation,
  4.1); "This layering is deliberate." (self-grading, 5); "the asymmetry is deliberate" (4.6);
  "The failure is more instructive than the current state." (self-grading, 9); "Two limits, stated
  rather than left to be found." (colon-staged intro, 9); "Neither layer rescues the other. One
  artefact answers half of a two-part question." (aphoristic closer restating the paragraph, 1.3);
  "This subsection states the bound so a reader meets it before the procedure." (structure
  narration, 1.1 — deleted whole per the delete-never-trim rule; the Section 6 pointer stays);
  merged several negation-first pairs where unearned ("The multiplicity is not a property of the
  Gateway. It is a property of the deployment." -> one sentence). Kept "X, not Y" contrasts that
  exclude a real alternative (§18 test): payload-not-envelope (5), declared-not-measured, error-not-
  default (4.4).
- **§9 forward dependencies**: the source already carries the -04 fixes (1.1 exists for this; 4.3
  points at 4.4/4.7/6). No pointer removed; none needed adding. One new finding recorded in §5 below
  (Section 9 dependency).
- **§10**: no terms coined.
- **§12 + §26**: relations conserved by order, colon, and noun echo; see §6 below for the three
  sites where §26 changed the output. No connective word added anywhere in the rewrite; splits at
  colons/semicolons only. The commissioned-because relation lost in the published -07 (rules §12's
  own worked pair) restored via "That review was commissioned for two reasons: ..." — noun echo +
  colon, zero discourse connectives, both sentences under the cap.
- **§14**: abstract rewritten to position-zero vocabulary: outcome names replaced by "one of five
  outcomes", "not a bare pass" replaced by "an undecided item stays undecided in the result";
  citation-free; the two payload names kept (they are the document's deliverables, not Terminology
  entries).
- **§15**: the four receipt-format citations attached at the claim "Several receipt formats exist"
  (Section 1, paragraph 1) — the rules' own worked example; the related-work paragraph keeps its
  discussion and its citations.
- **§16 + §18**: "They share a limit" now carries its criterion and a non-tautological claim:
  "They share one limit: the party under audit selects the evidence." (the §18-approved real claim;
  the property sentence follows as support).
- **§17** (hard form): deleted — "This document defines no new receipt format, transparency
  mechanism, or signature format." (Abstract); "This document does not reinvent that. This document
  defines no new receipt format, no policy evaluation semantics, and no transparency mechanism."
  (1) — replaced by the rules' accepted positive form ("payloads for registration ... whose
  append-only log a third party can audit"); "This document defines no countersignature, no
  anchoring, and no log format of its own." (5); "No evidence structure substitutes for that."
  (3.4, counterfactual restatement, §20 sub-case); "rather than invisible" (4.1, complement
  restatement); "The size is not an assertion." (4.6, restatement). Kept: security-consideration
  negatives that bound what the EVIDENCE means ("does not defend against that operator", "It does
  not establish that...", frozen), and Section 1.2/3.4 does-not-claim sentences that name their
  criterion (per §16) — these limit evidence meaning and several are frozen.
- **§19**: the two problem statements in Section 1 kept to name/mechanism/consequence; duplicate
  restatements removed (see §17 list).
- **§20 ASCII**: every em dash in rewritable prose replaced by role (colon, comma pair, or period).
  `grep -nP '[^\x00-\x7F]'` residue: author-name letters (Doğru, TEKNOLOJİ, ŞİRKETİ, Türkiye) and
  em dashes inside frozen text only (Section 2 definitions x2, the frozen 4.4 MUST NOT sentence) —
  §11 outranks §20 there; flagged as author work.
- **§21**: found and left frozen: "An implementation encountering a value in a field defined here
  MUST reject the structure." (3.2) — the receiver holds nothing that decides "this string is a
  value"; the rules' own example. Recorded for the author (repair options a/b/c per §21).
- **§22**: found and left frozen: "The absence of a class ... MUST be read that way." (3.4) — the
  enumerated form (two worlds: no values occurred, or the policy does not define the class) plus a
  decidable presentation rule is recorded for the author; the freeze keeps the defect visible.
- **§23**: "A silently ignored fourth field ... The gap shows up as an outcome the operator cannot
  account for." — W2 deleted, W1 kept attached after the frozen MUST sentence (the colon-attach
  form was unavailable because the rule sentence is frozen). The declared-zero/assumed-zero
  sentence kept as the source already has it in the one-sentence form §23 endorses.
- **§24**: "It therefore needs the tightest reporting rules of the five." (4.5) -> "The rules below
  therefore make each exclusion visible in the result." (the rules' accepted fix). "This layering
  is deliberate" and "the asymmetry is deliberate" deleted; the properties they graded are stated
  by the sentences that follow. "first-class" dropped from 3.1.
- **§25/§26**: see §3 above and §6 below.
- **§27**: NOT applied — pyramid re-authoring is author work and this run is register-only per the
  task brief; the source outline is kept 1:1.

## 5. Recorded as author work (not done)

1. **§21 unenforceable MUST** (3.2): trigger condition undecidable by the receiver. Options:
   (a) supply the checks that exist (member not in defined set, wrong type, class not in policy
   list); (b) re-address to the producer; (c) demote to the definition sentence that already
   carries it.
2. **§22 enumeration** (3.4): replace "MUST be read that way" with the two named worlds plus a
   presentation rule ("A Consumer MUST NOT present the absence of a class as evidence that no
   values of that class were disclosed"); strength ledger MUST -> MUST NOT if adopted.
3. **§13.7 dependency on Section 9**: Section 4.3 cites "The measured case was three seconds
   (Section 9)" and 4.4 cites "The twenty-three hour case ... is in Section 9" — load-bearing
   motivation living in a section the draft says will be removed. Promote the two cases (or their
   numbers) into 4.3/4.4, or lose them knowingly.
4. **Spelling fork artifact/artefact**: both appear, each at least once in frozen text ("signed
   artifact" 3.1/6; "boundary artefact" in the frozen 4.4 MAY sentence). Normalization requires
   touching normative text; author's call.
5. **Ambiguous referent** (Section 9): "What made the second sentence sayable was the tool's own
   output." — "the second sentence" has no clear antecedent; kept as "made the second sentence
   sayable" pending the author naming it.
6. **Em dashes inside frozen text** (§20 conflict, see §4): three sites, author-side fix.
7. **Structural suggestions not taken** (register-only run): worked JSON examples for both payloads;
   §27 pyramid re-derivation of chapter order.

## 6. The three places §26 changed the outcome (vs. what §12 alone would have produced)

1. **Section 9, the commissioned-review pair.** §12 alone restores two "because" sentences (the
   rules' §12 compliant example does exactly that). Written instead as noun echo + colon: "The
   second came from an adversarial review of the implementation. That review was commissioned for
   two reasons: the fix had loosened a default, and its author was not the party who should clear
   it." Relation conserved, zero discourse connectives added.
2. **Section 4.4, the ceiling paragraph.** The draft's "The consequence is a ceiling." staging (and
   the tempting "Therefore, ...") both dropped: the sentence "A coverage outcome against a declared
   correspondence cannot be stronger than the declaration." now sits directly after the MUST-state
   rule — order alone carries the inference, and the metaphor "ceiling" fell out of the vocabulary
   with it.
3. **Section 4.3, no-floor and membership.** "Window membership is itself a bound: it is decided
   across two clocks." and "The procedure sets no floor: a smaller offset is harder for a reader to
   suspect." — both would naturally have taken "because"; the colon form carries the reason. Same
   move deleted "In particular," before the undeclared-multiplicity sentence: adjacency to the
   frozen MUST NOT sentence already scopes it.

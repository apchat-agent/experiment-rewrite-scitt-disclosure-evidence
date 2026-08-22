# Rewrite report — draft-dogru-scitt-disclosure-evidence-04

Source: `draft-dogru-scitt-disclosure-evidence-04.txt` (plain-text I-D, page furniture stripped).
Output: `draft-rewritten.md`.
Rules: `rewrite-rules-wip.md`.
Scope: Abstract and Sections 1-9. RFC boilerplate, TOC and Section 10 skipped.

## 0. Headline numbers

| | original | rewritten |
|---|---|---|
| words (Abstract + §1-9) | 5,765 | 6,465 (+12.1%) |
| sentences over 25 words | 42 | **1** (BCP 14 boilerplate, kept verbatim — see §2) |
| paragraphs over 6 sentences | — | 0 |
| RFC 2119 keyword instances | bare MUST 16, MUST NOT 23, SHOULD 2, SHOULD NOT 1, MAY 4, SHALL 1, SHALL NOT 1, REQUIRED 1, RECOMMENDED 3, OPTIONAL 1 | identical in both texts, all ten classes (counts are of the *bare* keyword, i.e. MUST excludes MUST NOT) |

Keyword parity was checked mechanically over §1-9 of both texts.

## 1. Per-section table

Word counts include the heading line. "Longest" is the longest sentence in words.

Measurement caveat: the original is plain text with hanging-indent definition
lists and bullets, and the sentence splitter sometimes joins a heading or a list
label to the sentence that follows it. Original "longest" figures marked † are
inflated by a few words for that reason; the ranking is still sound.

| § | orig words | new words | orig longest | new longest |
|---|---|---|---|---|
| Abstract | 185 | 274 | 51 | 22 |
| 1 Introduction | 413 | 491 | 48† | 24 |
| 1.1 What these structures do not claim | 130 | 159 | 35 | 23 |
| 2 Conventions and Definitions | 263 | 275 | 49 | 48 (boilerplate) |
| 3 Transformation Evidence (heading) | 3 | 3 | 2 | 2 |
| 3.1 Purpose | 44 | 50 | 23† | 23 |
| 3.2 Structure | 218 | 248 | 28 | 22 |
| 3.3 Serialization and digests | 87 | 93 | 29 | 20 |
| 3.4 What Transformation Evidence does not prove | 281 | 318 | 39 | 25 |
| 4 Coverage Reconciliation (heading) | 3 | 3 | 2 | 2 |
| 4.1 Purpose | 82 | 95 | 27 | 22 |
| 4.2 Activity snapshots | 145 | 165 | 21† | 23 |
| 4.3 Reconciliation procedure | 903 | 995 | 45 | 25 |
| 4.4 Mapping profiles | 588 | 640 | 41 | 24 |
| 4.5 Exclusions | 317 | 353 | 38 | 25 |
| 4.6 Result statement | 431 | 461 | 53 | 24 |
| 4.7 Semantics of the outcomes | 361 | 417 | 45 | 25 |
| 5 Registration on a Transparency Service | 153 | 172 | 56 | 22† |
| 6 Security Considerations | 388 | 419 | 39 | 25 |
| 7 Privacy Considerations | 102 | 112 | 50 | 22† |
| 8 IANA Considerations | 37 | 37 | 29† | 17† |
| 9 Implementation Status | 631 | 681 | 87 | 25 |
| **total** | **5,765** | **6,465** | 87 | 48 (25 excl. boilerplate) |

§4.2 is the one section whose longest sentence grew (21 → 23). The original 21
was an artefact of the splitter (heading + label). The genuine new maximum there
is the `source` member gloss, at 23 words, and it is under the cap.

## 2. Original wording kept deliberately

| kept text | reason |
|---|---|
| The whole BCP 14 paragraph in §2 ("The key words "MUST", "MUST NOT", … as shown here.") — 45 words, one sentence | Required boilerplate. RFC 8174 fixes this wording; editing it changes the normative binding of every keyword in the document. This is the only remaining sentence over 25 words. |
| The five outcome names `matched`, `observed-without-receipt`, `receipted-without-observation`, `excluded`, `indeterminate` | Defined terms. Constraint. The Abstract of the reference rewrite glosses them in plain words; I kept the real names and added a plain-word gloss around them instead. |
| `invalid-window`, `no-exceptions`, `exceptions`, `covered`, `mask`, `redact`, `tokenize`, `truncate`, `none`, `protocol-defined`, `measured`, `operator-declared`, `undeclared` | Wire values and outcome names. |
| All member names (`v`, `disclosure`, `request`, `policy`, `classes`, `class`, `action`, `count`, `ts`, `source`, `entries`, `pattern`, `window`, `snapshots`, `receipts`, `profile`, `bounds`, `outcome`, `items`, `counts`) | Wire names. In particular the snapshot member `source` and the result member `source` keep their names even though "source" is otherwise avoided as a synonym for origin (rules §4.3). |
| Version strings `transformation-evidence/1`, `activity-snapshot/1`, `coverage-reconciliation/1`, `coverage-reconciliation/2` | Wire values. |
| "A coverage outcome computed against a declared correspondence cannot be stronger than the declaration." (§4.4) | This is the document's own italicised statement of its central limit. "Stronger" is a specialist sense (see §3 below) and I glossed it in the surrounding sentences and in the Abstract, but the sentence itself is a load-bearing formulation the working group is likely to quote. Kept verbatim, with plain-language support around it. |
| "the absence of a decision is not a decision" → rendered as "A missing decision is not a decision." | Near-verbatim. Any longer paraphrase weakened the MUST NOT it justifies. |
| "It MUST NOT be presented as either" (§1.1) and "It MUST be read that way" (§3.4) — kept passive | The originals are agentless passives ("MUST NOT be presented as", "MUST be read that way"). Naming a subject (consumers? readers? verifiers?) would invent a normative addressee the source does not name, which is a bigger error than a passive. Same for "a result MUST NOT be stated in terms that assert that" (§4.3) and "It MUST NOT be resolved by assumption" (§4.7). Four passives retained on this ground. |
| "Snapshot frequency bounds the exposure" (§6) | "Bounds" here is the document's own technical verb, used consistently. Replacing it with "limits" would split one concept across two words. |
| "indeterminate here is not a weaker pass" (§4.3) and "An indeterminate outcome is a result, and not a degraded pass" (§4.7) — both contrast pairs retained | Rules §2 flags "X, not Y" as a tic. These two are earned: the preceding text does propose the reading being denied, and both sentences are the stated rationale for a MUST NOT. Cutting the contrast would remove the reason for the requirement. |
| "not merely that its values are hidden" (§3.4) and "and not per call count" (§4.3) — contrast pairs retained | Same ground: each denies a reading the surrounding normative rule exists to prevent. |
| `[RFC9943]`, `[RFC2119]`, `[RFC8174]`, `[RFC8785]`, `[RFC9052]`, `[RFC7942]` | References unchanged. |
| Version numbers 0.2.21 / 0.2.22 / 0.2.23 / 0.2.27 / 0.2.28, "three seconds", "two-hour Window", "twenty-three hour", "July 2026", "@conarium-ai/core", "-03" | Facts. Unchanged. |

## 3. Specialist-sense phrases unpacked

Rules §4.4: short sentences of common words in specialist senses pass every
mechanical check and are still unreadable. These are the ones I found and opened
up.

| before (source) | after (rewrite) |
|---|---|
| "it does not report a bare pass" (Abstract); "Neither structure reports a bare pass" (§1.1); "distinguishes this vocabulary from a bare pass" (§4.7) | "The result does not report a plain "pass" and nothing else. It always reports the five counts." / "Neither structure reports a plain "pass" and nothing else." / "separates this set of outcome names from a plain "pass"" |
| "cannot yield an outcome stronger than that declaration" (§1.1) | "Its outcome carries no more weight than that declaration." (In §4.4 the formulation itself is kept — see §2 — but is introduced by "The consequence is an upper limit.") |
| "an outcome of that standing, no stronger" (§4.6) | "states an outcome of that standing, and no stronger" — with "standing" itself unpacked at first use in §4.4: "the outcome takes that standing, and the result statement is required to show it." |
| "the disclosure surface" (§1.1, §3.4) | "what one Disclosure exposes" / "what one result exposes" |
| "it does not claim a value is unlearnable"; "a class be unlearnable rather than hidden" (§1.1, §3.4) | "It does not claim that a client cannot learn a value." / "a class stays beyond the client's reach, and not merely that its values are hidden" |
| "left the gateway transformed or in the clear" (§1) | "left the gateway transformed or unchanged" |
| "predicates over protected columns" (§3.4) | "tests on protected columns" |
| "the pinned Issuer asserted" (§3.4) | "the named Issuer asserted" |
| "that assertion is self-attested" (§3.4) | "the assertion is about the asserting party's own work" |
| "pinned identically and verify identically"; "a pinned exclusion as a justified one"; "the digest that is supposed to pin what was compared" (§4.5) | "The digest covers both in the same way, and both verify in the same way." / "MUST NOT read an exclusion as justified because the digest covers it" / "The digest is supposed to fix what the comparison covered." Also "the requirement is … that they be visible and pinned" → "that each exclusion is visible and that the digest covers it". |
| "all produce the same shape as a receipt describing activity that did not occur" (§4.7) | "produce the same shape in the result as a receipt that describes activity that never occurred" — with the follow-up "because the shape of the result does not distinguish the cases", so "shape" is anchored to the result object rather than left floating. |
| "a boundary artefact cannot exceed the interval it bounds" (§4.4) | "an artefact of the boundary cannot exceed the interval the boundary marks" |
| "a Gateway clock trailing the Data Source" (§4.3, twice) | "the Gateway clock runs behind the Data Source clock" / "a Gateway clock that runs behind the Data Source" |
| "the outcome whose semantics name gateway bypass" (§4.3) | "the outcome whose meaning names gateway bypass" |
| "the source's accounting" / "the Data Source's own accounting" (throughout) | "the Data Source's account" / "the Data Source's own account", to avoid "accounting" as a gerund-noun and to keep "source" from drifting toward "origin" |
| "this vocabulary" used for the set of five outcome names (§4.6, §4.7) | "this set of outcome names" |
| "the mirror condition" (§4.7) | "the condition on the other side" |
| "one layer up" (§4.4) | kept, but re-anchored: "Section 4.7 applies the same discipline to missing evidence. The rule here is that same discipline, one layer up." |
| "the essential property" (§4.1) | kept — it is not significance designation in the rules §2 sense; it names the property the section's whole argument rests on and the next two sentences state it. |
| "Establishing completeness requires…" (§1) — gerund subject | "Completeness therefore needs a second account of the activity" |
| "Matching is per pattern and per data object" (§4.3) — gerund subject | "The reconciler matches per pattern and per data object." |
| "Admitting Receipts on an exact comparison…" (§4.3) — gerund subject | "A reconciler could admit Receipts on an exact comparison between the two timestamps." |
| "Attributing cause is investigation, not reconciliation" (§4.7) — gerund subject | "To attribute a cause is investigation work, and reconciliation does not do it." |
| "This layering is deliberate" (§5) — gerund subject | "This document layers the two parts deliberately." |
| "the gaps are stated here rather than left for a reader to discover" (§9) | "The gaps appear here, rather than waiting for a reader to discover them." |

Claudisms cut (rules §2): the em-dash count drops from 18 in the source body to 0 in
the rewritten body (one remains in the file's own subtitle line); each em-dash aside became its own sentence. Two "precisely"
intensifiers ("precisely the part", "precisely that it surfaces") were removed or
replaced with plain statements; one "exactly" was kept in §4.6 ("restores exactly
the overclaim") because it modifies an identity claim, not an intensity.

## 4. Ambiguities in the source

1. **§4.3, "the item takes the outcome it would have had".** Would have had
   *under what counterfactual* — without the skew bound, or without the Receipt
   in question? I rendered it "the outcome it would otherwise have had", which
   preserves the ambiguity rather than resolving it. An editor should pin this
   down; it decides an implementation's behaviour.

2. **§4.3, "no pattern's counter may be lower at the end than at the start".**
   Lowercase "may", inside a paragraph of uppercase MUSTs. I preserved the
   lowercase, so it is not an RFC 2119 keyword. If the author meant MUST NOT be
   lower, the rewrite does not say so — deliberately, since I may not change
   normative force.

3. **§4.4, "the expected bounded set of source-level patterns".** "Bounded"
   could qualify the set (finite, enumerated in the profile) or the multiplicity
   that follows. I read it as the set and wrote "the expected set of source-level
   patterns, and that set is bounded". If the author meant the multiplicity, the
   sentence is now slightly wrong in emphasis, though the next sentence states
   the multiplicity bound separately either way.

4. **§9, "What made the second sentence sayable was the tool's own output".**
   "The second sentence" has no clear antecedent in the source. Most likely it
   means the sentence in this section describing the second defect. I wrote "The
   tool's own output is what made the second of those sentences sayable", which
   keeps the same referent problem rather than inventing a resolution.

5. **§9, "The temporal rule in this revision has the same history, compressed."**
   "Compressed" could mean the history happened over a shorter period, or that
   the account of it here is shorter. I chose "over a shorter period". This is a
   guess; see §5 item 4.

6. **§4.6, `outcome` / `bounds` ordering.** The source says a result whose bounds
   are operator-declared "states an outcome of that standing, no stronger", but
   `outcome` is a closed vocabulary of three values with no standing marker. The
   standing evidently lives in `bounds`, not in `outcome`. The source does not
   say this and neither does the rewrite; I flag it as an editorial gap, not a
   rewrite decision.

7. **§4.7, "an accounting scope mismatch".** Named as a cause of
   `observed-without-receipt`, but §4.2 says a `source` mismatch between the two
   snapshots invalidates the Window. Whether these are the same condition is not
   stated. I kept both statements as they are and did not harmonise them.

## 5. Places where I may have changed meaning — be paranoid here

Listed worst-first. Nothing here is a change I intend; these are the spots where
I am less than certain.

1. **§1.1 / Abstract, "a bare pass" → "a plain "pass" and nothing else".**
   The unpack asserts that the objection is to *reporting only a pass*. An
   alternative reading of "bare pass" is a pass *unqualified by its standing*
   (i.e. one that hides that its bounds are operator-declared). §4.7's "destroys
   the only property that distinguishes this vocabulary from a bare pass"
   supports my reading; §4.4's ceiling argument supports the other. The rewrite
   carries the first reading in three places. **Highest-risk item in the
   document.**

2. **§4.3, counter regression.** Source: "the reconciler MUST report failure for
   the Window as a whole rather than reconciling the surviving patterns." I
   wrote "MUST report failure for the Window as a whole, instead of reconciling
   the patterns that survived." I deliberately did *not* split this into a
   separate "It MUST NOT reconcile the surviving patterns", because that would
   mint a normative requirement the source does not state as one. But "instead
   of" is weaker-sounding than the original's "rather than", and a reader may
   now take the second clause as advisory. Consider whether the author intended
   a MUST NOT there.

3. **§3.3, "instead of guessing which form the digest has".** Source: "MUST
   reject … rather than guessing". Same shape as item 2 — the "rather than"
   clause is arguably part of the requirement. I kept it inside the same
   sentence so it stays attached to the MUST.

4. **§9, "over a shorter period"** for "compressed" (see §4 item 5). If the
   author meant "told here in compressed form", my version asserts a fact about
   the timeline that the source does not.

5. **§4.4, "This document layers the two parts deliberately"** (§5) and
   **"The consequence is an upper limit"** (§4.4). Both replace a nominal
   subject with a real one, per rules §2 (abstraction agency). In §4.4 the
   source says "The consequence is a ceiling"; "upper limit" and "ceiling" are
   the same idea, but "ceiling" may be terminology the working group has already
   adopted. Consider restoring "ceiling" if so.

6. **§4.1, "A Gateway does not produce the Data Source's account, so it cannot
   make activity that went around it disappear from that account."** The source
   is "A Gateway cannot make bypassed activity disappear from an account it does
   not produce." I made the causal link explicit ("so"). The source states it as
   a single fact and leaves the causality implicit. I believe this is the
   intended reading, but it is an addition of logical structure.

7. **§1, "Completeness therefore needs a second account of the activity, and a
   party other than the gateway must produce that account: the Data Source
   itself."** Lowercase "must" here is mine; the source has "requires … produced
   by a party other than the gateway". Lowercase "must" is not an RFC 2119
   keyword and §2's boilerplate says so explicitly, so this should be safe. Flag
   it anyway: an author may prefer "has to" to keep even the lowercase form out
   of a requirements-shaped sentence.

8. **§4.5, "A party decides excluded before the comparison."** The source has
   "excluded is a decision taken before it". I supplied "A party" as the actor
   because the passive had no subject. "A party" is vague on purpose — the
   deciding actor is really whoever wrote the Mapping Profile, i.e. the
   operator, but the source does not say so at this point in the text and §4.4
   does. If the author is willing, "the operator" would be clearer and is
   probably what is meant.

9. **§4.3, "In the case where someone found this problem, the measured
   difference was three seconds."** Source: "The difference measured where this
   was found was three seconds." "Someone" is a placeholder for an unnamed
   finder. §9 identifies the finder as review of -03 on the SCITT mailing list,
   so the fact is available, but §4.3 does not state it and neither does my
   rewrite.

10. **§9, "The codes stay unchanged on purpose."** Source: "They were left
    unchanged deliberately." I avoided naming an actor. Elsewhere in the same
    bullet I did write "The implementation added one code" for "One code was
    added" — that names the implementation rather than its authors. Both are
    small agency additions to agentless passives.

11. **§4.6, `profile` member: "The member is null when nobody declared a
    profile."** Source: "or null when none was declared". "Nobody declared" is a
    small strengthening — the source allows "none was declared *to this
    reconciler*". Low risk, but noted.

12. **§7, "The cost is that a third-party audit then needs permission and is no
    longer a public act."** Source: "at the cost of making third-party audit a
    permissioned rather than public act." I split the contrast into two clauses.
    The source's "permissioned rather than public" is a single term of art in
    some access-control writing; if it is one here, the split loses it.

13. **§3.4, "A result count of one rather than zero gives the client one bit of
    the value."** Source: "(a result-count of one versus zero is one bit of the
    value)". The source states an identity ("is one bit"); mine states a
    transfer ("gives the client one bit"). In context — a paragraph about what
    the client can learn — I believe these are the same claim. But it is an
    interpretation, not a transcription.

14. **Paragraph splitting.** To meet the ≤6-sentences-per-paragraph rule I broke
    26 paragraphs into two or three. Every break falls on a sentence boundary
    and none reorders text, but a paragraph break is itself a rhetorical signal.
    A few breaks — notably inside §4.3's two-clock argument, §4.5's discussion
    of what the digest achieves, and §4.7's list of causes — separate a claim
    from its immediate justification. An editor should re-read those three
    passages and rejoin any break that reads as a topic change when it is not.

15. **The Abstract deviates from the hand-written reference abstract used as a
    style model, in one respect.** That reference glosses the five outcomes in plain words ("observed with
    no receipt", "receipted with no observation", "excluded before the
    comparison"). The task constraints forbid changing outcome names, so my
    Abstract uses the real hyphenated names. This makes the Abstract slightly
    harder than the reference. If the reference register is to win here, the
    names would have to appear as a gloss alongside the plain wording. Flagging
    it because it is a deliberate divergence from the model text.

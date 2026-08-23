# Re-authoring report: draft-dogru-scitt-disclosure-evidence-07

Inputs: `source.txt` (draft -07), `rules-snapshot.md` (sections 1-24 plus
claudisms). Output: `reauthored.md`. This report carries the structure
decisions, the requirement map, the GAP list, the additions list, and the
author-actionable findings. Per rules section 13.4, the additions list here
duplicates the in-document [ADDITION] marks so they survive copy-out.

## 1. Structure decisions

Chapter order, source -> re-authoring:

| source | re-authoring | change |
|---|---|---|
| Abstract | Abstract | rewritten to position zero (rule 14): one topic per sentence, no locally defined terms, no citations |
| 1 Introduction | 1 Introduction | problem statements recast as name/mechanism/consequence blocks (rule 19); receipt-format citations moved to the claim (rule 15); "share a limit" now carries its criterion (rule 16) |
| 1.1 Threat model | 1.3 Threat model in brief | kept early; it is the source's own forward-dependency fix and rule 9 endorses it |
| 1.2 What these structures do not claim | 1.4 What the evidence means | negative framing honed into positive statements (rule 17 hard form); the two MUST NOT sentences kept |
| 1.3 Relationship to coverage attestation | 1.5 | compressed, relations restated |
| (new) | 1.2 What this document defines | the two structure definitions and related-work paragraph, pulled together so terms are introduced before 1.3 uses them |
| 2 Conventions and Definitions | 2 | same position; definitions grouped so paired roles sit together (operators, Item/Data Object, Issuer/Verifier) |
| 3 Transformation Evidence | 3 | same position; 3.4 retitled "The limit of the evidence" (a label, not a contents narration) |
| 4.2 snapshots, 4.3 procedure, 4.4 profiles, 4.5 exclusions | 4.2 snapshots, 4.3 Mapping Profiles, 4.4 Exclusions, 4.5 procedure | REORDERED: profiles and exclusions now precede the procedure that consumes them (definition-before-use, rule 14 at chapter scale; permitted here because this is a re-authoring, not a rewrite, so rule 9.2's ban on moving sections does not bind) |
| 4.6 result, 4.7 semantics | 4.6, 4.7 | unchanged relative position |
| 5-10, Acks | 5-10, Acks | unchanged order |

Consequences of the reorder: every "the rule below" and "Section 4.4"
forward pointer in the source's procedure text became a backward pointer;
the clock-skew rationale (declaration, not measurement) now precedes the
procedure that depends on it, which removes the forward dependency rule 9
records for the -04 ancestor.

Register: sentence cap applied at the maximum (rule 1.1), relations
restated on every split (rule 12), rationale attached as one clause
(rule 23), ASCII punctuation throughout with the author's name kept in its
own letters (rule 20).

Mechanical result on the final file (same splitter as used during
authoring; deflist-aware, code fences excluded): 690 sentences; 25
sentences over 25 words, of which 13 contain a BCP 14 keyword (exempt per
rule 11.2's logic), 2 are fixed IETF boilerplate, and the rest are
enumeration lists, GAP notes, and deflist artifacts of the splitter. Zero
em dashes; zero non-ASCII outside names.

## 2. Requirement map

Every BCP 14 sentence of the source, its strength, and where it landed.
"Kept" means the re-authored sentence carries the same keyword at the same
strength; wording may differ, meaning may not. Source quotes abbreviated.

| # | source | requirement (abbreviated) | strength | mine | kept |
|---|---|---|---|---|---|
| 1 | 1.2 | result reporting activity w/o receipt MUST NOT be presented as proof of intent or breach | MUST NOT | 1.4 | yes |
| 2 | 3.2 | structure MUST NOT carry data values | MUST NOT | 3.2 | yes (also 8.1, as in source) |
| 3 | 3.2 | implementation encountering a value MUST reject the structure | MUST | 3.2 | yes; reworded "that detects a value"; defect F1 below |
| 4 | 3.3 | MUST reject unrecognized digest prefix | MUST | 3.3 | yes (restated in 6, as in source) |
| 5 | 3.4 | Consumers MUST NOT present as proof of non-exposure | MUST NOT | 3.4 | yes |
| 6 | 3.4 | absence of a class "MUST be read that way" | MUST | 3.4 | absolute strength kept; recast as "Consumer MUST NOT present the absence of a class as evidence that no values of that class were disclosed" after enumerating the two absence cases (rules 21+22); form change MUST -> MUST NOT recorded here as the divergence; defect F2 |
| 7 | 4.2 | both snapshots MUST carry same `source` | MUST | 4.2 | yes |
| 8 | 4.2 | deployments MAY retain pattern text privately | MAY | 4.2 | yes |
| 9 | 4.3 | snapshots MUST carry same `v` and `source` | MUST | 4.5 | yes |
| 10 | 4.3 | end ts MUST be later than start ts | MUST | 4.5 | yes |
| 11 | 4.3 | on counter regression, reconciler MUST report failure for whole Window | MUST | 4.5 | yes |
| 12 | 4.3 | reconciler MUST report which bound it applied | MUST | 4.5 | yes |
| 13 | 4.3 | call counts and receipt counts MUST NOT be compared one-to-one | MUST NOT | 4.5 | yes |
| 14 | 4.3 | unattributable pattern MUST NOT be silently ignored | MUST NOT | 4.5 | yes |
| 15 | 4.3 | MUST NOT report matched when indeterminate | MUST NOT | 4.5 | yes |
| 16 | 4.3 | (temporal mirror) MUST NOT report as observed-without-receipt | MUST NOT | 4.5 | yes |
| 17 | 4.3 | result MUST carry the outcome and the offset | MUST | 4.5 | yes |
| 18 | 4.3 | result MUST NOT be stated in terms asserting per-statement receipting | MUST NOT | 4.5 | yes |
| 19 | 4.4 | MUST reject clocks member with a fourth key; SHOULD name the key | MUST + SHOULD | 4.3 | yes |
| 20 | 4.4 | MUST NOT select between two skew declarations | MUST NOT | 4.3 | yes |
| 21 | 4.4 | two mismatched declarations MUST fail | MUST | 4.3 | yes |
| 22 | 4.4 | result MUST bind the profile digest | MUST | 4.3 | yes |
| 23 | 4.4 | result MUST state each bound's standing | MUST | 4.3 | yes |
| 24 | 4.4 | MUST NOT present operator-declared bound as measured | MUST NOT | 4.3 | yes |
| 25 | 4.4 | MUST NOT substitute default multiplicity of one | MUST NOT | 4.3 | yes |
| 26 | 4.4 | MUST NOT substitute default skew of zero | MUST NOT | 4.3 | yes |
| 27 | 4.4 | MUST NOT substitute a bound of its own choosing | MUST NOT | 4.3 | yes |
| 28 | 4.4 | MAY decline boundary explanation for offset larger than the Window | MAY | 4.3 | yes |
| 29 | 4.5 | exclusion rules MUST be stated in the profile | MUST | 4.4 | yes |
| 30 | 4.5 | result MUST report excluded count and per-item rule | MUST | 4.4 | yes |
| 31 | 4.5 | MUST NOT exclude by a rule not in the profile | MUST NOT | 4.4 | yes |
| 32 | 4.5 | Consumers MUST NOT read a pinned exclusion as justified | MUST NOT | 4.4 | yes |
| 33 | 4.5 | result MUST NOT present the digest as evidence exclusions were appropriate | MUST NOT | 4.4 | yes |
| 34 | 4.6 | Consumer MUST NOT read a /1 result as /2 | MUST NOT | 4.6 | yes (restated in 8.2, as in source) |
| 35 | 4.6 | chain head digest + sequence range RECOMMENDED as identifying material | RECOMMENDED | 4.6 | yes |
| 36 | 4.6 | result SHOULD state provenance of identifying material | SHOULD | 4.6 | yes |
| 37 | 4.6 | MUST NOT carry an outcome name asserting coverage | MUST NOT | 4.6 | yes |
| 38 | 4.6 | MUST NOT aggregate indeterminate into a proportion | MUST NOT | 4.6 | yes |
| 39 | 4.6 | Reconciler SHOULD be operationally independent of the Gateway | SHOULD | 4.6 | yes |
| 40 | 4.7 | result MUST NOT label as intrusion/breach; consumers MUST NOT present it as such | MUST NOT x2 | 4.7 | yes |
| 41 | 4.7 | MAY treat receipted-without-observation as failure under own policy | MAY | 4.7 | yes |
| 42 | 4.7 | indeterminate MUST NOT be resolved by assumption | MUST NOT | 4.7 | yes |
| 43 | 4.7 | folding indeterminate into a proportion MUST NOT be performed | MUST NOT | 4.7 | yes |
| 44 | 6 | MUST reject unknown prefixes (restatement of #4) | MUST | 6 | yes |
| 45 | 8.1 | payload MUST NOT carry data values (restatement of #2) | MUST NOT | 8.1 | yes |
| 46 | 8.1 | MUST reject object if `v` not recognized | MUST | 8.1 | yes |
| 47 | 8.2 | MUST NOT read /1 as /2 (restatement of #34) | MUST NOT | 8.2 | yes |

Summary: 47 normative sentences found (42 distinct requirements, 5
restatements); 47 mapped; 47 at original strength. One form change at
unchanged strength (#6, MUST -> MUST NOT within the absolute level),
recorded above. No requirement added, dropped, promoted, or demoted.

Lowercase near-requirements kept lowercase, as in the source: "no
pattern's counter may be lower" (4.3), "must gain an error" (1.1/4.3
rationale), "must not come from the truncated file" (6.1), "must enforce
that in policy" (3.4). See finding F6.

## 3. GAP list (15)

1. 3.2 `disclosure`: byte serialization of "the receipt" digested when the
   receipt format has no canonical record hash.
2. 3.2 `request`: byte form of "the request" that is digested.
3. 3.2: which members of Transformation Evidence are mandatory vs optional.
4. 4.2 `ts`: required precision and time zone form of the ISO 8601 stamp.
5. 4.2 `source`: identifier format and comparison rule.
6. 4.2 `pattern`: normalization procedure (deployment-specific, undefined).
7. 4.3: profile encoding beyond `clocks` (patterns, multiplicity bound,
   version identifier, exclusion rules have no field names or shapes).
8. 4.5: how the receipt set "for the Window" is selected from a store.
9. 4.5: "the outcome it would have had" is defined nowhere in the body;
   its only concrete statement is in Section 9, scheduled for removal.
10. 4.5: direction of the skew comparison likewise lives only in Section 9.
11. 4.5: encoding of "the offset" in the result (field name, unit).
12. 4.6 `snapshots`: whether snapshots are JCS-canonicalized before
    digesting (Section 3.3 is invoked only for evidence, profiles, results).
13. 4.6 `receipts`: field/encoding for the SHOULD-stated provenance of the
    identifying material.
14. 4.6 `bounds`: key names (only Section 9 shows `bounds.skew`,
    `bounds.exclusion`).
15. 4.6 `items`: member names and full shape of an item entry.

## 4. Additions (2, both marked [ADDITION] in the text)

1. Section 3.2: a worked Transformation Evidence JSON example
   (illustrative values only; consistent with the defined members).
2. Section 4.5: a worked walkthrough of the three-second-offset fixture
   through no-profile / larger-bound / smaller-bound cases. Values are
   taken from the source's own Section 9 fixture, but presenting them as a
   body-level walkthrough is new, so it is marked.

Not counted as an addition: the two-case enumeration of class absence in
3.4, which restates the source's "about the policy's vocabulary as much as
about the data" concretely (rule 22); and the criterion attached to the
receipts-share-one-limit claim in 1 ("the party under audit selects the
evidence"), which the source's own 4.1 and 6 state and the introduction
merely inherits.

## 5. Author-actionable findings (source defects kept at strength or
   rewritten in my prose, per the task's split)

F1 (rule 21, unenforceable MUST, kept at strength): 3.2 "An implementation
encountering a value in a field defined here MUST reject the structure."
The receiver holds nothing that decides whether a string is a data value:
a masked value, a token, and an identifier are all strings. Honest repairs:
supply the checks that exist (member not in set, wrong type, class not in
policy list), re-address to the producer, or demote to the design goal the
preceding MUST NOT already carries.

F2 (rules 21+22, vague MUST, strength kept, form changed): 3.4 "The
absence of a class ... MUST be read that way." Reading is not a checkable
act, and the ambiguity was described abstractly instead of enumerated. Re-
authored as an enumeration of the two absence cases plus a presentation
rule at absolute strength (MUST NOT). The author should decide whether the
presentation-rule form is the intended requirement.

F3 (rule 24, self-grading): 4.5 "It therefore needs the tightest reporting
rules of the five." A ranking whose subject is the document's own rules,
and it compares against outcomes the reader has not reached. Replaced with
"the rules below make each exclusion visible in the result."

F4 (rules 16+18): 1 "They share a limit. A receipt is evidence from the
party that performed the access. It is about an event that party chose to
record." The verdict "limit" never states its criterion, and the property
alone borders on tautology. Re-authored with the criterion attached: the
party under audit selects the evidence, so the set cannot show what that
party left out.

F5 (rule 17, scope narration): abstract and 1 "This document defines no
new receipt format, no policy evaluation semantics, and no transparency
mechanism"; 1 "This document does not reinvent that"; 5 "This document
defines no countersignature, no anchoring, and no log format of its own."
Contents-description negatives; deleted, with the constructive sentences
("SCITT supplies...", "SCITT already defines that place") carrying the fact.

F6 (strength hygiene): lowercase requirement-shaped sentences sit beside
uppercase ones: "no pattern's counter may be lower" (4.3, inside a MUST
validity list), "That quantity must not come from the truncated file" and
"It requires that a result ... be readable as to which one it used" (6.1)
against the SHOULD of 4.6. The 6.1 "requires" overstates the 4.6 SHOULD.
Kept lowercase; the author should reconcile.

F7 (rule 13.7, removable text is load-bearing): the `bounds` key names,
the direction of the skew comparison, and the only concrete statement of
"the outcome it would have had" live solely in Section 9, which the draft
says will be removed. The published RFC would be more ambiguous than the
draft. Promote these facts into the body or lose them knowingly (GAPs 9,
10, 14).

F8 (rule 15, inherited): "several receipt formats exist" was uncited at
the claim in the source's introduction, with the four drafts cited only in
the related-work paragraph. Re-authored with references at the claim; the
related-work discussion stays.

F9 (rule 12, relation loss in -07): several -07 passages state facts in
sequence with the connecting relation deleted; the clearest is the
Implementation Status history ("The fix had loosened a default. Its author
was not the party who should clear it.") where the causal "commissioned
because" of -04 is gone. Relations restored in the re-authoring; the
author may want the same repair in the source line.

F10 (rule 9, forward dependency): the source's procedure text (4.3) leans
on "the rule below" and on Section 4.4's profile semantics pages after the
reader needs them; 1 asks the reader to trust counters that 4.3 then
invalidates, resolved only in 6. The reorder (profiles before procedure)
and the attached one-clause rationales remove both in the re-authoring;
in the source, pointers at the point of doubt would do it without moving
sections.

F11 (claudisms in spec register): negation-first pairs ("The result is
not a bare pass", "It is a result, not a degraded pass"), deferred nouns,
and aphoristic closers ("Nothing replaces that Issuer") recur through the
source's non-normative prose. Rewritten where non-normative; the flavor
sentences inside normative paragraphs were kept only where they carry the
requirement's rationale.

F12 (rule 14, abstract): the source abstract uses document-local senses
("bare pass", "excluded", "indeterminate", "Signed Statements") at
position zero. Re-authored into pre-document vocabulary.

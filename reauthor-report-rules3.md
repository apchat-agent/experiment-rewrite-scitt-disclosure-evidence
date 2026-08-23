# Re-authoring report: draft-dogru-scitt-disclosure-evidence-07, rules iteration 3

Files: pyramid.md (section 27 step 1), outline.md (step 2), reauthored.md
(steps 3-4). This report: requirement map, GAP list, additions, findings,
section 25 glossary and exemption ledger, counted texture numbers.

## 1. Requirement map (bidirectional, equal strength)

Method: every sentence carrying a BCP 14 keyword was extracted from the
source body and from reauthored.md by script (page furniture removed,
hard wrap normalized, the Conventions boilerplate and media-type
template labels excluded). Source: 45. Reauthored: 45. Each source
sentence was matched to a reauthored sentence by content-word overlap
with keyword-sequence comparison; the reverse direction holds by count
equality plus the same matching run. 44 of 45 map at identical keyword
and strength; 1 maps at a recorded divergence (N6, below).

| N | source | strength | new | note |
|---|---|---|---|---|
| N1 | 1.2 | MUST NOT | 5.6 | relocated to the outcome-presentation chapter |
| N2 | 3.2 | MUST NOT | 4.2 | verbatim |
| N3 | 3.2 | MUST | 4.2 | verbatim; finding F1 |
| N4 | 3.3 | MUST | 3 | verbatim; serialization hoisted |
| N5 | 3.4 | MUST NOT | 4.3 | verbatim |
| N6 | 3.4 | MUST | 4.3 | MUST -> MUST NOT; section 22 accepted repair; finding F2 |
| N7 | 4.2 | MUST | 5.2 | verbatim |
| N8 | 4.2 | MAY | 5.2 | verbatim |
| N9 | 4.3 | MUST, MUST | 5.5 | verbatim |
| N10 | 4.3 | MUST | 5.5 | verbatim |
| N11 | 4.3 | MUST | 5.5 | host sentence split; keyword clause intact |
| N12 | 4.3 | MUST NOT | 5.5 | verbatim |
| N13 | 4.3 | MUST NOT | 5.5 | verbatim |
| N14 | 4.3 | MUST NOT | 5.5 | verbatim |
| N15 | 4.3 | MUST NOT | 5.5 | verbatim |
| N16 | 4.3 | MUST | 5.5 | verbatim; finding F4 |
| N17 | 4.3 | MUST NOT | 5.5 | verbatim |
| N18 | 4.4 | MUST + SHOULD | 5.3 | verbatim, rationale attached per section 23 |
| N19 | 4.4 | MUST NOT | 5.3 | em-dash aside lifted to its own sentence (section 20); keyword clause intact |
| N20 | 4.4 | MUST | 5.3 | verbatim |
| N21 | 4.4 | MUST, MUST | 5.3 | verbatim |
| N22 | 4.4 | MUST NOT | 5.3 | verbatim |
| N23 | 4.4 | MUST NOT | 5.3 | verbatim |
| N24 | 4.4 | MUST NOT | 5.3 | verbatim |
| N25 | 4.4 | MUST NOT | 5.3 | verbatim |
| N26 | 4.4 | MAY | 5.3 | verbatim |
| N27 | 4.5 | MUST | 5.4 | verbatim |
| N28 | 4.5 | MUST | 5.4 | verbatim |
| N29 | 4.5 | MUST NOT | 5.4 | verbatim |
| N30 | 4.5 | MUST NOT, MUST NOT | 5.4 | verbatim |
| N31 | 4.6 | MUST NOT | 5.7 | verbatim |
| N32 | 4.6 | RECOMMENDED | 5.7 | verbatim |
| N33 | 4.6 | SHOULD | 5.7 | verbatim; finding F4 |
| N34 | 4.6 | MUST NOT | 5.7 | verbatim; finding F3 |
| N35 | 4.6 | MUST NOT | 5.7 | verbatim; finding F5 |
| N36 | 4.6 | SHOULD | 5.7 | verbatim |
| N37 | 4.7 | MUST NOT, MUST NOT | 5.6 | verbatim |
| N38 | 4.7 | MAY | 5.6 | verbatim |
| N39 | 4.7 | MUST NOT | 5.6 | verbatim |
| N40 | 4.7 | MUST NOT | 5.6 | verbatim; finding F5 |
| N41 | 6 | MUST(-fail, restates N10) | 7 | verbatim |
| N42 | 6 | MUST | 7 | verbatim |
| N43 | 8.1 | MUST NOT | 9.1 | verbatim (restates N2) |
| N44 | 8.1 | MUST | 9.1 | verbatim |
| N45 | 8.2 | MUST NOT | 9.2 | verbatim (restates N31) |

No new normative sentence exists without a source counterpart: the two
counts are equal and every reauthored keyword sentence was consumed by a
match.

## 2. [GAP:] list — what the source never determines

19 marks in reauthored.md, over 13 distinct gaps (several are marked
both at the definition and inside the worked example):

1. The bytes under the `request` digest; no request canonicalization
   (4.2).
2. Value spaces of `policy.id` and `policy.decision` (4.2).
3. Format of the snapshot `source` identifier (5.2).
4. Pattern normalization: exemplified, never specified; two accounting
   layers can normalize one statement differently (5.2).
5. Mapping Profile encoding outside the `clocks` member: patterns,
   multiplicity bound, and exclusion rules have no named fields (5.3).
6. Identifier format of `clocks.observation` / `clocks.receipt` (5.3).
7. Window bounds inclusive or exclusive (5.5).
8. Attribution of a pattern to the Data Objects it touches: no
   procedure (5.5).
9. How a Receipt "names" a Data Object: left to an unconstrained
   receipt format (5.5).
10. No result member carries the offset that N16 requires the result
    to carry, nor the applied bound of N11 (5.5, 5.7).
11. No result member carries the receipts-independence statement that
    N33 requires (5.7).
12. The key names under `bounds` are never enumerated in the body;
    they appear only in the removable Implementation Status section
    (5.7). This is the section 13.7 class: load-bearing facts living
    in text scheduled for deletion.
13. The member names of an `items` entry are never enumerated; the
    Data Objects an Item records have no field (5.7).

## 3. Additions (marked)

- Four worked examples, every member present, invented values flagged
  with [GAP:] where the source constrains nothing: Transformation
  Evidence (4.2), activity snapshot (5.2), `clocks` member (5.3),
  result statement (5.7). The example key names `bounds.multiplicity`,
  `pattern`, `rule` are explicitly marked as inventions.
- The two-world enumeration in 4.3 ("A class can be absent for two
  reasons...") replacing the source's blur-shaped relativization:
  section 22's accepted repair.
- The Consumer presentation rule in 4.3 (part of the same repair;
  recorded as the N6 divergence, not silent).

Nothing else is new technical content. The Serialization chapter (3)
is relocation, not addition.

## 4. Findings (source defects, kept at source strength)

- **F1 (N3, 4.2).** "An implementation encountering a value in a field
  defined here MUST reject the structure" is unenforceable: the
  receiver holds nothing that decides whether a string is a data
  value. Section 21's own worked case. Kept verbatim; repair options
  (supply the checks, re-address to the producer, demote) are the
  author's call.
- **F2 (N6, 3.4).** "MUST be read that way" makes reading the
  addressee's act, which no party can test. Repaired per the section
  22 pattern the rules record as accepted: worlds enumerated, MUST
  replaced by a testable presentation MUST NOT. The strength ledger
  carries MUST -> MUST NOT as a divergence.
- **F3 (N34, 4.6).** "A result MUST NOT carry an outcome name that
  asserts coverage" gives the addressee no procedure for deciding what
  a name "asserts". Blur-shaped trigger; kept at strength.
- **F4 (N16, N11, N33).** Three requirements oblige a result to carry
  information (the offset, the applied bound, the independence
  statement) for which the result structure defines no member. Each is
  checkable only against fields that do not exist. Kept at strength;
  GAPs 10-11 locate them.
- **F5 (N35 vs N40).** The no-proportion prohibition is stated
  normatively twice, in 4.6 counts and again in 4.7. One rule, two
  homes. Both kept (freeze); flagged for the author. N2/N43 and
  N31/N45 duplicate into the IANA templates, which is media-type
  convention and not flagged.
- **F6 (source 4.5, non-normative).** "It therefore needs the tightest
  reporting rules of the five" self-grades the document's machinery
  (section 24). Replaced by the property: "The rules here make each
  exclusion visible in the result."
- **F7 (structural).** The source procedure (4.3) forward-references
  the Mapping Profile five times and the exclusion rules once before
  either is defined. Resolved here by reordering (outline.md); for the
  author's own outline it is a forward-dependency finding per section
  9.

## 5. Section 25 glossary and exemption ledger

Exemption list: the 19 Terminology terms, BCP 14 keywords, registry
values (mask, redact, tokenize, truncate, none; the six outcome
names), member names in code font, standard names (SCITT, JCS, COSE,
CBOR, JSON, SHA-256, Ed25519, ISO 8601, PostgreSQL, RFC numbers,
IANA, npm, TypeScript, MIT).

Glossary (concept -> chosen word -> displaced words):

| concept | chosen | displaced |
|---|---|---|
| make visible | show | reveal, surface |
| fasten by digest | bind | pin (except quoted uses, see ledger), anchor |
| happen before | ahead of | prior to |
| record does not contain | does not show | is silent about |
| trust level of a bound | standing | strength, quality |
| produce (of outcomes) | produce | generate, yield (except N10 "yield", frozen) |

Exemption ledger (kept words neither plain nor on the exemption list;
one line each). 9 entries:

1. "disclosure surface" (4.3) — the source's own compound for what one
   result shows; renaming it would fork the source's vocabulary.
2. "standing" (throughout) — half-defined by the source's
   Protocol-defined/Measured entries; kept as the source's ladder word.
3. "pinned" (4.3, 5.4, Acks) — the source's verb for digest-bound;
   kept where the source's "pinned exclusion" concept is discussed.
4. "ceiling" (5.3) — source metaphor for an upper limit on outcome
   strength; kept, one use, at the source's own site.
5. "attack surface" (7) — standard security term.
6. "leaves no mark in the chain" (1) — one mild figure for the
   hash-chain blindspot; literal alternative ("is not detected by")
   loses the chain as the detector.
7. "testifies to its own extent" (7.1) — source's phrase for the
   self-describing receipt set; the distinction is Sirkkavaara's and
   keeps his wording.
8. "sealed" (7.1) — source's word for signed-and-closed quantity.
9. "green dashboard" (Acks) — the source's acknowledgment image,
   quoted concept.

A stable ledger of 9 across the document is the crispness measurement
section 25 asks for.

## 6. Texture numbers (counted, not estimated)

Method: prose paragraphs only, per the section 12.1 methodology
(headings, tables, code fences, bullet field-lists, [GAP:] marks
removed); sentences split on terminal punctuation; connective list is
the section 12.1 list verbatim. Counted by script over the shipped
reauthored.md.

| measure | value |
|---|---|
| prose sentences, all | 451 |
| non-normative sentences | 418 |
| non-normative median length | 10 words |
| non-normative max | 45 words (the frozen BCP 14 boilerplate; next-longest 25) |
| non-normative over 25 words | 1 of 418 (0.2%; the boilerplate) |
| connective share, raw section 12.1 list | 52/418 = 12.4% |
| connective share, hand-classified discourse connectives | 23/418 = 5.5% |
| normative sentences (mapped, exempt from restyling) | 33 in running prose + 12 in field lists = 45 |
| normative median / max | 24 / 41 words |
| em dashes | 0 |
| non-ASCII | author's name only |

The raw connective count includes ordinal nouns ("the first gap"),
"since July 2026", copular "that is", and relative "where"; the
hand-classified figure counts only sentences whose match is a
discourse-relation marker. Both are reported; the classification list
is in the measurement transcript.

## 7. Largest structural decisions

1. **Serialization hoisted to its own chapter (3).** The source keeps
   JCS and digest form inside Transformation Evidence (3.3); Coverage
   Reconciliation reaches back into that subsection three times. Both
   payloads plus the profile and the result depend on it, so it
   precedes both structures and every later mention points backward.
2. **Declarations before the procedure (5.2 -> 5.3 -> 5.4 -> 5.5).**
   The source's procedure consumes the Mapping Profile's bounds and
   exclusion rules pages before they are defined. The derived order
   gives the procedure only defined inputs; semantics (5.6) then
   interprets the outcomes; the result statement (5.7) comes last as
   the chapter that references every other.
3. **Abstract rebuilt at position zero.** One paragraph, L3 translated:
   every defined term paraphrased (Disclosure -> delivery, Window ->
   time interval, Item -> entry), no citations, no forward references.
   The source abstract used four defined terms and a scope-negation
   sentence; the negation was honed into positives per section 17.

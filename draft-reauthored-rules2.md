# Transformation Evidence and Coverage Reconciliation for Auditable Data Disclosure

draft-dogru-scitt-disclosure-evidence-07, re-authored.
Author of record: E. C. Doğru, VERAX TEKNOLOJİ LİMİTED ŞİRKETİ.
Intended status: Informational.

This re-authoring preserves every requirement of the source draft at its
original BCP 14 strength. Text marked [ADDITION] goes beyond the source and
is a proposal to the author, not source content. Text marked [GAP: ...]
names a question the source does not determine.

## Abstract

Audit receipts record what a policy gateway wrote about each access to a
data source. They do not record how the gateway changed the data before
delivery. They also cannot show an access that produced no receipt. This
document defines two signed evidence formats for those two gaps. The first
names which categories of protected values were changed in one delivery, by
which method, and in what count. It never carries the values. The second
compares the data source's own activity counters against the receipts for a
time interval. It reports each item as matched, observed without a receipt,
receipted without observed activity, excluded, or undecided. An undecided
item is therefore never folded into a pass. Both formats are meant for
registration on an append-only transparency log, where the producing party
cannot quietly rewrite them.

## Status of This Memo

This Internet-Draft is submitted in full conformance with the provisions of
BCP 78 and BCP 79. Internet-Drafts are working documents of the Internet
Engineering Task Force (IETF). Internet-Drafts are draft documents valid
for a maximum of six months and may be updated, replaced, or obsoleted by
other documents at any time. It is inappropriate to use Internet-Drafts as
reference material or to cite them other than as "work in progress." This
Internet-Draft will expire on 24 February 2027.

## Copyright Notice

Copyright (c) 2026 IETF Trust and the persons identified as the document
authors. All rights reserved. This document is subject to BCP 78 and the
IETF Trust's Legal Provisions Relating to IETF Documents in effect on the
date of publication of this document.

## Table of Contents

1. Introduction
   1.1. Two problems
   1.2. What this document defines
   1.3. Threat model in brief
   1.4. What the evidence means
   1.5. Relationship to coverage attestation
2. Conventions and Definitions
3. Transformation Evidence
   3.1. Purpose
   3.2. Structure
   3.3. Serialization and digests
   3.4. The limit of the evidence
4. Coverage Reconciliation
   4.1. Purpose
   4.2. Activity snapshots
   4.3. Mapping Profiles
   4.4. Exclusions
   4.5. Reconciliation procedure
   4.6. Result statement
   4.7. Semantics of the outcomes
5. Registration on a Transparency Service
6. Security Considerations
   6.1. Receipt set completeness
7. Privacy Considerations
8. IANA Considerations
9. Implementation Status
10. References
Acknowledgments
Author's Address

## 1. Introduction

Many systems place a policy gateway between an automated client and a data
source. These systems increasingly emit signed, hash-chained access
receipts, and several receipt formats exist
[I-D.farley-acta-signed-receipts] [I-D.marques-asqav-compliance-receipts]
[I-D.chueayen-attestation-receipts] [I-D.aylward-aiga-2]. All of them share
one limit: the party under audit selects the evidence. A receipt comes from
the party that performed the access. It records an event that the same
party chose to record. As a result, the receipt set cannot show what that
party left out, or what it did to the data.

### 1.1. Two problems

Two problems follow from that limit.

The first problem is an unrecorded transformation. A receipt states that an
access happened and names the policy decision. But a gateway may also mask,
redact, or tokenize values before disclosure, and that transformation is
the privacy claim. No conventional receipt describes it. An auditor
therefore learns that a table was read. The auditor does not learn whether
protected columns left the gateway transformed or in the clear.

The second problem is unrecorded access. A receipt set covers only accesses
that produced receipts. A client that reaches the data source without the
gateway therefore leaves no trace in it. Hash chains detect removal and
reordering of records that exist. They cannot detect a record that was
never created. Completeness therefore needs a second account of activity,
from a party other than the gateway: the data source itself.

### 1.2. What this document defines

This document defines two evidence structures, one per problem. Both are
payloads for registration as Signed Statements on a SCITT Transparency
Service [RFC9943]. A third party can audit that service's append-only log:

* Transformation Evidence (Section 3): a signed statement bound to one
  disclosure. It names which classes of values were transformed, by which
  action, and in what count. It never carries the values.

* Coverage Reconciliation (Section 4): a procedure and a signed result. It
  compares data-source activity snapshots taken at the two ends of a time
  window against the receipt set for that window. Neither account is
  assumed complete. The operator declares the expected correspondence
  between the two accounts (Section 4.3). The result classifies each item
  of either account as matched, observed-without-receipt,
  receipted-without-observation, excluded, or indeterminate.

Related drafts record signed decisions about automated access. Farley
[I-D.farley-acta-signed-receipts], Marques
[I-D.marques-asqav-compliance-receipts], and Chueayen
[I-D.chueayen-attestation-receipts] use Ed25519 [RFC8032] and JSON
Canonicalization [RFC8785]. Aylward [I-D.aylward-aiga-2] uses Ed25519 in a
hybrid signature suite without JCS. None of them defines evidence of either
kind described here.

### 1.3. Threat model in brief

The full account is in Section 6. This subsection states the bound early,
because the procedure of Section 4 is designed against it.

The Gateway and the Data Source are often run by one party, and that party
can suppress the source counters. For that reason a counter reset fails the
Window (Section 4.5) instead of yielding a clean report. The Mapping
Profile is written by the Gateway operator. It can absorb unreceipted
activity or exclude it. The defence is visibility: a digest-bound profile,
reported exclusions, and a stated standing for each bound. Digest prefixes
that an implementation does not recognize are rejected (Section 3.3).
Issuer key compromise is a SCITT-layer problem. A truncated receipt set
still verifies internally, so detecting the cut needs a quantity from
outside that file (Section 6.1).

### 1.4. What the evidence means

Each structure is exactly as strong as the party that produced it.

Transformation Evidence is the Issuer's signed assertion that a
transformation was applied to the disclosure surface. A Verifier can check
the disclosed bytes against that assertion. Until one does, the assertion
stands on the Issuer's signature alone (Section 3.4).

A Coverage Reconciliation result that reports activity without a receipt is
a statement that evidence is absent. It is not, and MUST NOT be presented
as, proof of intent or of a breach (Section 4.7).

A reconciliation against an operator-declared correspondence carries the
standing of that declaration (Section 4.3). An undecided outcome is
reported as undecided. It is never folded into a proportion (Section 4.6).

### 1.5. Relationship to coverage attestation

A record can be intact yet silent about what is missing. A report can be
complete yet silent about what it examined. These are two different
failures, and they close in different places.

This document closes the first failure. A chain that verifies says nothing
about entries that were never written. The vocabulary here lets a
mediator's record say what it covers and what it leaves open, in its own
terms.

The second failure belongs to coverage attestation. There, an examination
declares the population it drew from and the basis for that population. It
also accounts for every unit it did not examine. Work on that layer is
under way on the SCITT list.

The two layers compose in one direction and substitute in neither. An
attestation over a mediated examination inherits whatever the mediator's
record leaves open. It inherits that silently, unless the record says so.
In the other direction, a complete access record over a population chosen
after the results were known records an already decided question exactly.
Each artefact answers half of a two-part question.

## 2. Conventions and Definitions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
"OPTIONAL" in this document are to be interpreted as described in BCP 14
[RFC2119] [RFC8174] when, and only when, they appear in all capitals, as
shown here.

One term keeps one meaning through the full document.

Data Source:
: The system holding the data, with its own accounting of query or access
  activity (for example, a database's statement statistics).

Gateway:
: The component that mediates access between an automated client and a
  Data Source, applies policy, transforms results, and emits receipts.

Gateway operator:
: The party that operates the Gateway.

Data Source operator:
: The party that operates the Data Source. This document always says which
  operator it means. Where both are the same party, Section 6 states the
  limit.

Disclosure:
: A single delivery of data, possibly transformed, from the Gateway to a
  client.

Receipt:
: A signed record of a Disclosure produced by the Gateway. This document
  is agnostic to the receipt format in use.

Protected Class:
: A named category of values that policy subjects to transformation (for
  example, "email", "national-id", "phone").

Client-level operation:
: One Disclosure, or one client request as seen by the Gateway.

Source-level statement:
: One increment of a Data Source activity counter, that is, one snapshot
  entry for one pattern. It is not interchangeable with a Client-level
  operation.

Window:
: A time interval over which reconciliation is performed, bounded by two
  snapshots of the Data Source's activity counters. Both bounds are
  stamped by the Data Source. Whether a Receipt falls inside them is a
  question about a second clock, the Gateway's (Section 4.5).

Mapping Profile:
: A versioned statement, declared by the operator, of the correspondence
  expected between one Client-level operation and the source-level
  activity it produces. It states three things: the bound on that
  multiplicity, the clock source on each side with the skew bound between
  them, and the exclusion rules. A Mapping Profile is a declaration about
  a deployment, not a measurement performed by the Gateway (Section 4.3).

Data Object:
: A named target of source activity or of a Receipt. In the shipped
  reconciler this is a table (or equivalent schema object), not a column.
  The result records these as objects on an Item.

Item:
: One unit the reconciliation procedure classifies. On the source side,
  one snapshot entry whose pattern counter increased in the Window: one
  pattern, not one (pattern, Data Object) pair. On the receipt side, one
  Receipt that names a Data Object the snapshots do not account for.
  Counting each (pattern, Data Object) pair as an Item changes the
  observed-without-receipt population.

Reconciler:
: The party that performs Coverage Reconciliation and produces the result
  statement.

Consumer:
: A party that reads Transformation Evidence or a Coverage Reconciliation
  result and presents it to a human or to another system.

Issuer:
: In the sense of [RFC9943], the party that signs a Signed Statement. For
  Transformation Evidence that is the Gateway operator. For a Coverage
  Reconciliation result it is the Reconciler.

Verifier:
: A party that checks a signature, a digest, or a Transparency Service
  receipt. This document uses the term once, for independent checking of a
  disclosed result against the Issuer's Transformation Evidence assertion
  (Section 3.4).

Protocol-defined:
: A standing this document itself assigns to a bound (for example, the
  invalid-window rule). It is not a measurement.

Measured:
: A standing a bound has when it was obtained by observation of the
  deployment. It is not operator-declared and not assigned by this
  document.

## 3. Transformation Evidence

### 3.1. Purpose

Transformation Evidence answers, for one Disclosure: which Protected
Classes were transformed in the disclosed result, by which action, and in
what count. It makes the transformation claim a first-class, signed,
registrable artifact.

### 3.2. Structure

Transformation Evidence is a JSON object with the following members:

v:
: Structure version string. For this document: `transformation-evidence/1`.

disclosure:
: A digest binding this evidence to exactly one Disclosure. It is computed
  over the receipt for that Disclosure or, where the receipt format
  defines a canonical record hash, over that hash. Digest form is defined
  in Section 3.3. [GAP: for receipt formats without a canonical record
  hash, the digested byte serialization of "the receipt" is not defined.]

request:
: A digest of the request that produced the Disclosure: the digest, never
  the request text, because query text can itself contain protected
  values. [GAP: the byte form of "the request" that is digested is not
  defined.]

policy:
: An object with `id`, an identifier of the policy version applied, and
  `decision`, the policy outcome under which disclosure proceeded.

classes:
: An array of objects, one per Protected Class that the applied policy
  recognizes and that occurred in the disclosed result, each with:

  class:
  : The Protected Class name, as named by the policy.

  action:
  : One of `mask`, `redact`, `tokenize`, `truncate`, or `none`. The value
    `none` states that the class occurred and was disclosed untransformed,
    an honest statement some deployments need to make.

  count:
  : The number of values of this class in the disclosed result to which
    the action was applied.

[GAP: the source does not state which members of this object are mandatory
and which are optional.]

The structure MUST NOT carry data values, transformed or otherwise. Only
class names, action names, counts, digests, and identifiers appear. An
implementation that detects a value in a field defined here MUST reject
the structure.

[ADDITION: worked example, values illustrative only.]

```json
{
  "v": "transformation-evidence/1",
  "disclosure": "sha256:6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
  "request": "sha256:d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35",
  "policy": { "id": "pii-policy-14", "decision": "allow-with-masking" },
  "classes": [
    { "class": "email", "action": "mask", "count": 12 },
    { "class": "phone", "action": "none", "count": 3 }
  ]
}
```

### 3.3. Serialization and digests

For digesting and signing, a structure is serialized with the JSON
Canonicalization Scheme [RFC8785]. Digests in this document are SHA-256.
They are written as strings prefixed with `sha256:` followed by lowercase
hexadecimal. Future documents may register alternative digest prefixes; an
implementation MUST reject a digest whose prefix it does not recognize
rather than guessing.

A CBOR/COSE serialization [RFC9052] of the same data model is expected
once the JSON model has received review. Nothing in the model depends on
JSON specifically.

### 3.4. The limit of the evidence

Transformation Evidence describes the disclosure surface of one result. A
protected value can still be learnable by the client even when every
instance of it was transformed. The reason: request languages can permit
predicates over protected columns. An allowed request can then answer
questions about a masked value. A result count of one versus zero is one
bit. The evidence for such a Disclosure is still accurate, since the value
was transformed in the result. The client may still have learned
something. Consumers MUST NOT present Transformation Evidence as proof of
non-exposure. A deployment that needs a class to be unlearnable must
enforce that in policy, for example by refusing the objects that carry the
class.

The payload is the Issuer's signed assertion that the transformation was
applied. A Verifier may check the disclosed bytes against that assertion.
Until then, the evidence is what the pinned Issuer asserted. Where the
Issuer is the Gateway that performed the transformation, the assertion is
self-attested. A Consumer who treats it as verified has dropped the Issuer
from the trust statement.

The `classes` array is bounded by what the applied policy recognizes. A
value belonging to a class the policy does not name is therefore not
counted. A class can be absent from the array for two reasons. Either no values
of that class occurred in the disclosed result, or the policy does not
define the class. The array does not distinguish the two. A Consumer
MUST NOT present the absence of a class as evidence that no values of that
class were disclosed.

## 4. Coverage Reconciliation

### 4.1. Purpose

Coverage Reconciliation answers, for one Window: did the Data Source's own
accounting record activity for which no Receipt exists? It is the
mechanism by which "the gateway was bypassed" or "the receipt sink failed"
becomes detectable.

The mechanism rests on one property: the two compared accounts originate
from different components. The receipt set comes from the Gateway. The
activity counters come from the Data Source. A Gateway cannot make
bypassed activity disappear from an account it does not produce. Where
those components share one operator, that separation is only
administrative. The same-operator limit is in Section 6.

### 4.2. Activity snapshots

A snapshot is a JSON object capturing the Data Source's cumulative
activity counters at a point in time:

v:
: Snapshot version string. For this document: `activity-snapshot/1`.

ts:
: The time the snapshot was taken (ISO 8601). [GAP: required precision and
  time zone form are not stated.]

source:
: An identifier of the Data Source and the accounting scope within it (for
  example, the database role whose activity is counted). Both snapshots of
  a Window MUST carry the same `source`; a mismatch invalidates the
  Window. [GAP: the identifier's format and its comparison rule are not
  stated.]

entries:
: An array of objects, one per activity pattern the source's accounting
  distinguishes, each with:

  pattern:
  : A digest of the normalized activity pattern (for example, a normalized
    statement with constants removed): the digest, not necessarily the
    text, because pattern text can embed protected values and schema
    detail. Deployments MAY retain pattern text privately for diagnosis;
    only the digest is required here. [GAP: the normalization procedure is
    deployment-specific and not defined.]

  count:
  : The cumulative counter value for this pattern at `ts`.

### 4.3. Mapping Profiles

One Client-level operation may produce several Source-level statements.
The multiplicity is a property of the deployment, not of the Gateway. A
pooler or an object-relational mapper can produce it. A Gateway cannot
measure a correspondence it does not produce.

A Mapping Profile is therefore declared by the operator. For each
Client-level operation it covers, it states the expected source-level
patterns, the multiplicity bound, and the exclusion rules (Section 4.4).
It carries a version identifier. It is serialized and digested as in
Section 3.3. [GAP: apart from the `clocks` member below, no field names or
encoding are defined for the profile's patterns, multiplicity bound,
version identifier, or exclusion rules.]

The profile also declares the temporal correspondence, because the
operator knows it and the Gateway cannot measure it. The Data Source
stamps snapshots. The Gateway stamps Receipts. The profile therefore names
the clock on each side and the skew bound between them. Both are operator
statements. A claim that both sides read one clock, so the bound is zero,
is still a declaration. One clock read twice is not read at the same
instant. Whether that residue matters is a judgement about the deployment.
The rules below forbid presenting a declared zero as measured. They
equally refuse a zero that nobody declared being read as agreement.

The temporal correspondence is declared in three fields under a `clocks`
member. The encoding is given so another specification can adopt the same
shape:

clocks.observation:
: String. An identifier for the clock that stamps the activity snapshots:
  the Data Source side.

clocks.receipt:
: String. An identifier for the clock that stamps Receipts: the Gateway
  side.

clocks.skew:
: Duration. The bound on how far those two clocks may differ. A duration
  is a decimal integer with a unit suffix of `ms`, `s`, `m`, or `h`, or a
  bare decimal integer read as milliseconds: `500ms`, `5s`, `2m`, `1h`,
  `5000`. A duration that does not parse is an error, not a default.

An implementation MUST reject a `clocks` member that carries any key other
than these three, and SHOULD name the key it rejected: a field that is
silently ignored makes the declaration state less than its author
believes.

A declaration that both sides read one clock still writes all three
fields. The two identifiers may be the same string, and `skew` may be
`0ms`. A declared zero is a statement someone is accountable for. An
assumed zero is the condition the no-default rule below forbids.

A skew bound can end up declared twice: in the profile and through an
interface of the reconciler's own. An implementation MUST NOT select
between them. Two declarations that parse to the same number of
milliseconds are one declaration and proceed. Two that do not MUST fail as
an operator error, because which declaration prevailed would not be
visible on the result.

A reconciliation result computed against a Mapping Profile MUST bind that
profile's digest. It MUST state, for each bound it relies on, whether the
bound is protocol-defined, measured, operator-declared, or undeclared. A
result MUST NOT present an operator-declared bound as a measured one.

The consequence is a ceiling: a coverage outcome against a declared
correspondence cannot be stronger than the declaration. Where the
declaration is an operator statement, the outcome inherits that standing,
and the result statement shows it. The same discipline applies to absent
evidence in Section 4.7. A declaration presented as a measurement is an
overclaim, even when the declaration is true.

Where a required multiplicity bound is undeclared, the affected items are
indeterminate (Section 4.5). An implementation MUST NOT substitute a
default bound of one: a one-to-one rule reports false
observed-without-receipt items on any deployment with a pooler, and a
silent default would make that error look like a finding.

An undeclared skew bound is treated the same way, for the same reason. An
implementation MUST NOT substitute a default of zero: zero asserts that
the two clocks agree, which is the assumption behind the false accusation
this document guards against. It MUST NOT substitute a bound of its own
choosing either, because that would decide the operator's question with a
number the operator never saw. Absent the declaration, items whose only
naming Receipt sits outside the Window are indeterminate, and the result
reports the offset. The reader compares that offset with clocks the reader
knows. The Reconciler cannot.

An implementation MAY, absent a declared bound, decline to offer the
Window boundary as the explanation for an offset larger than the Window
itself, on the ground that a boundary artefact cannot exceed the interval
it bounds. This is a reporting choice about what an implementation is
willing to suggest, not a change of outcome: the item is indeterminate
either way. The twenty-three hour case that motivated this choice is in
Section 9.

### 4.4. Exclusions

Exclusion differs from the other outcomes in kind. The outcomes of
Section 4.5 are produced by the comparison. `excluded` is a decision taken
before it, and it decides what is compared at all. Because exclusion can
make a reconciliation come out clean, the rules below make each exclusion
visible in the result.

Exclusion rules MUST be stated in the Mapping Profile and are therefore
covered by its digest. A result statement MUST report the count of
excluded items and the rule that excluded each of them. An implementation
MUST NOT exclude items by a rule that is not in the profile. Without these
constraints, a clean result and a result cleaned by exclusion look the
same. The digest that pins what was compared then misses the step that
decided what was compared. Session or catalog housekeeping is a legitimate
exclusion. Exclusions need not be rare, but they must be visible and
pinned.

Pinning reproduces the decision and does not judge it. The rule identifier
makes the exclusion reproducible. A reader sees which rule removed each
Item, and can check that the rule was in the digest-covered profile. That
does not establish that the exclusion was correct. A housekeeping rule and
a rule that hides the auditor's target pin the same way, and verify the
same way. Consumers MUST NOT read a pinned exclusion as a justified one,
and a result statement MUST NOT present the digest as evidence that the
exclusions were appropriate. The same distinction holds between a declared
bound and a measured one (Section 4.3). Here it applies to what is
compared at all.

### 4.5. Reconciliation procedure

Given a start snapshot, an end snapshot, and the receipt set for the
Window, a reconciler proceeds as follows. [GAP: how the receipt set "for
the Window" is selected from a larger receipt store is not defined.]

Window validity is checked first. The two snapshots MUST carry the same
`v` and `source`, and the end `ts` MUST be later than the start `ts`. No
pattern's counter may be lower at the end than at the start. A counter
regression means the source's accounting was reset or altered inside the
Window. The Window is then unreliable. The reconciler MUST report failure
for the Window as a whole, rather than reconciling the surviving patterns:
an attacker who can reset counters must gain an error, not a clean report.
Why a reset fails the whole Window, rather than dropping only the reset
patterns, is a same-operator concern (Section 6).

Window membership is itself a bound, decided across two clocks. The Data
Source stamps the snapshots. The Gateway stamps each Receipt. An exact
comparison between them fails in one direction. A Gateway clock that
trails the Data Source moves a Receipt out of the Window. The object that
Receipt names then looks like activity with no Receipt. That is the
outcome whose semantics suggest gateway bypass (Section 4.7). A clock
difference of seconds can produce that accusation with no real gap; the
measured case was three seconds (Section 9). The procedure sets no floor,
because a smaller offset is harder for a reader to suspect.

The Mapping Profile states the skew bound (Section 4.3), and the profile
digest covers it like every other part of the profile. Two rules follow.
Where the bound is undeclared, the no-default rule of Section 4.3 applies:
the affected items are indeterminate, not absent evidence. Where it is
declared and a Receipt falls further outside the Window than the bound
allows, the boundary does not explain the offset. The item takes the
outcome it would otherwise have had, and the reconciler MUST report which
bound it applied to reach that. [GAP: "the outcome it would have had" is
not defined procedurally in the body; its only concrete statement, and the
direction of the skew comparison, appear in Section 9, which is scheduled
for removal.]

For each pattern whose counter increased during the Window, the reconciler
attributes the pattern to the Data Objects it touches. It then checks
whether any Receipt in the Window names those objects. [GAP: the
attribution method from pattern to Data Objects is not defined.] Matching
is per pattern and per Data Object, not per call count: one Client-level
request may legitimately produce more than one Source-level statement, so
call counts and receipt counts MUST NOT be compared one-to-one. A pattern
whose target objects cannot be determined MUST NOT be silently ignored; it
receives the indeterminate outcome.

The comparison is between two populations, source-level activity and
Receipts. Neither population is assumed complete. Each Item in either
population receives exactly one of the following outcomes, which the
result statement names as fields (Section 4.6):

matched:
: The Item corresponds to an Item in the other population within the
  bounds of the applicable Mapping Profile (Section 4.3) and within the
  Window. The profile's two kinds of bound do not act alike here: a
  multiplicity bound admits items to this outcome, and the skew bound does
  not. A Receipt outside the Window is never matched, however small the
  declared skew. The bound qualifies how far the boundary can be trusted,
  not where the boundary is.

observed-without-receipt:
: The Data Source recorded activity against an object that no Receipt in
  the Window names.

receipted-without-observation:
: A Receipt in the Window names an object for which the Data Source's
  counters record no activity.

excluded:
: The Item was removed from comparison before matching by a rule stated in
  the Mapping Profile (Section 4.4).

indeterminate:
: The evidence or the Mapping Profile does not determine an outcome: the
  pattern's objects could not be attributed, a required multiplicity or
  skew bound is undeclared, the Item's only naming Receipt falls outside
  the Window, or the Window's evidence is insufficient to decide.

An implementation MUST NOT report an Item as matched when the outcome is
indeterminate: the absence of a decision is not a decision. In particular,
where a Mapping Profile does not declare the multiplicity bound that the
comparison requires, the affected items are indeterminate and not clean
coverage.

The same rule binds the temporal bound in the opposite direction. Where
every object an Item leaves unaccounted for is named by a Receipt that
falls outside the Window, the Item is indeterminate, and an implementation
MUST NOT report it as observed-without-receipt. A reconciler cannot
distinguish a trailing Gateway clock from a Receipt written late.
Reporting absent evidence would assert a distinction the reconciler did
not make. An Item that leaves even one object named by no Receipt at all
is outside this rule. That is a genuine absence. A neighbouring object's
clock does not make it undecidable.

An indeterminate reached this way is not a weaker pass: the comparison did
not come out clean. A result statement MUST carry the outcome and the
offset that produced it. What the implementation is forbidden to state is
the cause. [GAP: the encoding of "the offset" in the result (field name,
unit) is not defined.]

A reconciliation with no observed-without-receipt items establishes one
thing. Each observed source-level Item is attributable to a Receipt naming
the same object, under the declared correspondence. It does not establish
that every Source-level statement was itself receipted, and a result MUST
NOT be stated in terms that assert it. One Receipt naming an object can
clear an unbounded number of further statements against that object inside
the Window. In that case the procedure has established object attribution
and nothing stronger.

[ADDITION: worked walkthrough, illustrative only. A two-hour Window holds
one Receipt naming table `orders`, stamped by the Gateway three seconds
before the Window's start. The snapshot counters show an increase for one
pattern attributed to `orders`. With no profile, the skew bound is
undeclared. The Item is indeterminate, and the result reports the
three-second offset. With `clocks.skew: 5s` declared, the bound exceeds
the offset, yet the Receipt is still outside the Window and is never
matched. The Item remains indeterminate under the declared bound. With
`clocks.skew: 1s` declared, the boundary no longer explains a three-second
offset. The Item takes the outcome it would otherwise have had,
observed-without-receipt, with the applied bound reported.]

### 4.6. Result statement

The reconciliation result is a JSON object:

v:
: `coverage-reconciliation/2`. The outcome vocabulary of
  `coverage-reconciliation/1` is not a subset of this one: a /1 result
  reporting `covered` asserts more than the procedure establishes and is
  not re-expressible here. A Consumer MUST NOT read a /1 result as a /2
  result.

window:
: Object with `start` and `end`, the two snapshot `ts` values.

source:
: The common source identifier of the two snapshots.

snapshots:
: Object with `start` and `end` digests of the two snapshot structures.
  [GAP: the source invokes JCS canonicalization only for evidence,
  profiles, and results; it does not state that snapshots are canonicalized
  the same way before digesting.]

receipts:
: A digest identifying the receipt set that was compared. For chained
  receipt formats, the chain head digest and the sequence range are
  RECOMMENDED as the identifying material. A result SHOULD state whether
  that identifying material was obtained independently of the Issuer or
  read from the receipt set itself. The two are not equivalent evidence,
  and a Consumer cannot tell them apart from the digest (Section 6.1).
  [GAP: the field or encoding for stating that provenance is not defined.]

profile:
: The digest and version identifier of the Mapping Profile the comparison
  was computed against (Section 4.3), or null when none was declared. When
  null, every item whose outcome depends on a multiplicity bound is
  indeterminate. So is every item whose only naming Receipt falls outside
  the Window: with no profile there is no declared skew bound either.

bounds:
: For each bound the comparison relied on, its source: protocol-defined,
  measured, operator-declared, or undeclared. A result whose bounds are
  operator-declared states an outcome of that standing, no stronger.
  [GAP: the key names under `bounds` are not defined in the body; the
  names `bounds.skew` and `bounds.exclusion` appear only in Section 9,
  which is scheduled for removal.]

outcome:
: `invalid-window` when the Window is unreliable (Section 4.5); otherwise
  `no-exceptions` when every item is matched or excluded, and `exceptions`
  when any item is observed-without-receipt,
  receipted-without-observation, or indeterminate. The name states what
  the comparison left open, not what it proved. A result MUST NOT carry an
  outcome name that asserts coverage of the source activity.
  `no-exceptions` is not such an assertion. It says only that the
  comparison produced no open item under the declared correspondence. That
  statement is bounded by the correspondence (Section 4.3) and by the fact
  that neither population is assumed complete.

items:
: The list of items whose outcome is not matched, each with its outcome
  and, for excluded items, the profile rule that excluded it. Pattern
  digests appear here, not pattern text, for the reasons in Section 4.2.
  [GAP: the member names and full shape of an item entry are not defined.]

counts:
: The number of items in each outcome, including matched and excluded. An
  implementation MUST NOT aggregate indeterminate items into a proportion
  of coverage. An outcome that does not decide cannot be averaged into one
  that does. A percentage would restore precisely the overclaim this
  vocabulary exists to prevent.

  A result carries matched as a bare count while carrying every other
  outcome as an itemized accounting, and the asymmetry is deliberate. A
  count a reader cannot reconstruct is an assertion about a population
  only the producer can see. This one is not that. The result digests both
  activity snapshots and the receipt set it compared (Section 4.2,
  Section 3.3). A reader holding those inputs recomputes the matched set,
  so the count is a convenience over material the reader already has.

  That property fails in one named case. The identifying material for the
  receipt set may have been read from the receipt set itself
  (Section 6.1). The reader then recomputes the Issuer's answer. The
  digest checks transcription, not completeness, and the matched count
  inherits that standing.

The result statement is serialized and digested as in Section 3.3. It is
intended to be signed by the Reconciler and registered (Section 5). The
Reconciler SHOULD be operationally independent of the Gateway; where it is
not, registration on a Transparency Service at least makes the result's
existence and timing third-party-visible.

### 4.7. Semantics of the outcomes

An observed-without-receipt outcome states that evidence is absent. It
does not state why. Gateway bypass produces it. Receipt sink failure
produces it. An accounting scope mismatch produces it. A Receipt that
names the object but falls outside the Window on the two clocks also
produced it in an earlier revision. Section 4.5 therefore removes that
case from this outcome. An earlier revision listed the mirror condition
only under receipted-without-observation; this text names both directions
so the omission is visible. A result statement MUST NOT label such
activity as an intrusion, a breach, or an intentional act, and Consumers
MUST NOT present it as such. The mechanism surfaces the condition. Cause
is investigation, not reconciliation.

A receipted-without-observation outcome is likewise a statement about
evidence, and is not by itself a fault. A counter reset at the Window
boundary produces the same shape. So does an intermediary that collapses
statements, an increment outside the snapshot pair, or a receipt
describing activity that did not occur. An implementation MAY treat it as
a failure condition under a policy of its own; this document does not
define it as one, because the shape does not distinguish the cases.

An indeterminate outcome is a result, not a degraded pass. It MUST NOT be
resolved by assumption in either direction: neither counted as matched
because nothing contradicts it, nor reported as missing activity because
nothing confirms it. An implementation under pressure to produce a single
number will be tempted to fold indeterminate into a coverage proportion.
That operation MUST NOT be performed: it destroys the only property that
distinguishes this vocabulary from a bare pass.

Verification of receipt signatures and chain integrity happens before
reconciliation, under the rules of the receipt format in use, and is out
of scope here. Reconciliation compares an already-verified receipt set
against source accounting. It does not re-verify.

## 5. Registration on a Transparency Service

Both structures defined here are payloads for Signed Statements in the
sense of [RFC9943]. The Issuer signs the serialized structure: the Gateway
operator for Transformation Evidence, the Reconciler for a Coverage
Reconciliation result. The Issuer registers the Signed Statement on a
Transparency Service. The SCITT Receipt is proof of inclusion, at a
position, in an append-only log. A party other than the Issuer operates
that log.

The structures gain their audit value from registration that the Issuer
cannot quietly rewrite. SCITT already defines that place, its trust model,
and its verification. Digests in this document bind evidence to receipts
over the payload, not over the envelope, so the binding survives
registration.

## 6. Security Considerations

Same-operator collusion:
: In many deployments the Gateway and the Data Source are operated by the
  same party, and the mechanism's value against that party is reduced. An
  operator with administrative access to the source accounting can
  suppress the counters. The invalid-window rule (Section 4.5) turns a
  reset into a visible failure. Registration (Section 5) makes suppression
  of already-issued results detectable. An operator who controls both
  accounts and never registers is outside this mechanism. Assurance
  against that operator needs an accounting path the operator cannot write
  to. That is a deployment property, not a payload property.

Counter manipulation:
: An attacker who can reset or rewind source counters could otherwise hide
  activity between snapshots. The MUST-fail rule exists for this case: a
  Window containing a regression is reported unreliable in its entirety.
  Snapshot frequency bounds the exposure, because shorter Windows mean a
  reset costs the attacker a visible failure sooner.

Declared correspondence as an attack surface:
: The Mapping Profile (Section 4.3) is written by the operator. It decides
  what counts as a match, and what is excluded before matching. A wider
  multiplicity bound can absorb unreceipted activity. An added exclusion
  rule can remove it from comparison. This mechanism does not defend
  against that operator, because nothing computed against a declaration
  can. Instead it makes the declaration part of the evidence. The profile
  is versioned, and its digest is bound into the result. Exclusions are
  reported with count and rule. The result states that its bounds are
  operator-declared. A reader who trusts the result therefore sees that
  dependency. Registration (Section 5) makes the sequence of declared
  profiles third-party-visible, which a silently edited profile would
  lose.

Digest agility:
: Digests are prefixed (Section 3.3), and an implementation MUST reject
  unknown prefixes: accepting an unknown prefix as an opaque match would
  let an attacker route around comparison.

Signature and key compromise:
: Signing and registration are inherited from the SCITT layer. Key
  management, revocation, and the consequences of Issuer key compromise
  are governed there, not here. A compromised Issuer key voids the
  evidentiary value of statements under that key, as it does for any
  signed artifact.

### 6.1. Receipt set completeness

A receipt set whose most recent entries have been removed is internally
consistent. Every remaining link verifies. Every signature checks. The
file does not state how many entries it should have contained.
Reconciliation does not close this gap, because an operator who can
truncate the receipt set can generally suppress the source accounting too.
Detecting the removal needs a count, a head digest, or an equivalent
quantity, and that quantity must not come from the truncated file.

What matters to a Consumer is where that material arrives from. The two
constructions below differ in a way a digest does not reveal.

An implementation may accept the expected quantity as a verifier input.
The check is then only as trustworthy as that input. An auditor who holds
only the receipt file has no source for it except the Issuer. That is the
party under examination. The verification is real, but its independence is
supplied by whoever ran it, not by the artifacts.

An implementation may instead carry the quantity inside the signed
material, so the set testifies to its own extent. That closes the first
gap, at a cost that should be stated. The Issuer is signing an assertion
about a population it has not finished producing. A per-entry counter
constrains only the entries that were kept, so a sealed total over the
held set is also required. A running count derived from the sequence
number it accompanies adds no information. It restates the position of a
present record and says nothing about an absent one.

This document requires neither construction. It requires that a result
identifying a receipt set be readable as to which one it used (the SHOULD
of Section 4.6). A Consumer who cannot tell them apart will read an
external pin as if the receipt set had proved its own completeness. That
is the strongest claim in this area, and the one least often actually
made.

## 7. Privacy Considerations

Every structure in this document follows one rule: evidence about
protected data must not itself become a disclosure channel. Transformation
Evidence carries class names, action names, and counts. It never carries
values. Request and pattern references are digests, because query and
pattern text can embed values and schema detail. Class names and counts do
reveal that a class was present, and in what quantity. Deployments that
treat even that as sensitive can keep the payloads private and register
only the digests. Third-party audit then becomes a permissioned act.

## 8. IANA Considerations

This document requests registration of two media types and the creation of
two registries. Registrations follow [RFC6838]. Registry policy is
Specification Required as defined in [RFC8126].

### 8.1. Media type: application/transformation-evidence+json

Type name:
: application

Subtype name:
: transformation-evidence+json

Required parameters:
: None.

Optional parameters:
: None.

Encoding considerations:
: 8bit; binary UTF-8 JSON. For digesting and signing, the payload is
  serialized with [RFC8785].

Security considerations:
: See Section 6 and Section 3.4. The payload MUST NOT carry data values.

Interoperability considerations:
: Implementations that do not recognize the `v` member MUST reject the
  object.

Published specification:
: This document, Section 3.2.

Applications that use this media type:
: Policy gateways and auditors that record or verify a disclosure
  transformation.

Fragment identifier considerations:
: None.

Additional information:
: Deprecated alias names for this type: none. Magic number(s): none. File
  extension(s): none. Macintosh file type code(s): none.

Person and email address to contact for further information:
: See the Author's Address section of this document.

Intended usage:
: COMMON

Restrictions on usage:
: None.

Author:
: See the Author's Address section of this document.

Change controller:
: IETF

### 8.2. Media type: application/coverage-reconciliation+json

Type name:
: application

Subtype name:
: coverage-reconciliation+json

Required parameters:
: None.

Optional parameters:
: None.

Encoding considerations:
: 8bit; binary UTF-8 JSON. For digesting and signing, the payload is
  serialized with [RFC8785].

Security considerations:
: See Section 6 and Section 4.7.

Interoperability considerations:
: A Consumer MUST NOT read a coverage-reconciliation/1 result as a /2
  result (Section 4.6).

Published specification:
: This document, Section 4.6.

Applications that use this media type:
: Reconcilers and auditors that compare source activity with a receipt
  set.

Fragment identifier considerations:
: None.

Additional information:
: Deprecated alias names for this type: none. Magic number(s): none. File
  extension(s): none. Macintosh file type code(s): none.

Person and email address to contact for further information:
: See the Author's Address section of this document.

Intended usage:
: COMMON

Restrictions on usage:
: None.

Author:
: See the Author's Address section of this document.

Change controller:
: IETF

### 8.3. Transformation Actions registry

IANA is asked to create a new registry titled "Transformation Actions" in
a new "Disclosure Evidence" group.

Registration policy:
: Specification Required ([RFC8126]).

Registration template:
: Action name (unique ASCII token); description; reference.

Initial contents:

| Action name | Description | Reference |
|---|---|---|
| mask | Replace a value with a class-level placeholder | This document, Section 3.2 |
| redact | Remove a value | This document, Section 3.2 |
| tokenize | Replace a value with a stable token | This document, Section 3.2 |
| truncate | Shorten a value | This document, Section 3.2 |
| none | The class occurred and was disclosed untransformed | This document, Section 3.2 |

### 8.4. Coverage Reconciliation Outcomes registry

IANA is asked to create a new registry titled "Coverage Reconciliation
Outcomes" in the same "Disclosure Evidence" group.

Registration policy:
: Specification Required ([RFC8126]).

Registration template:
: Outcome name (unique ASCII token); description; reference.

Initial contents:

| Outcome name | Description | Reference |
|---|---|---|
| matched | The Item corresponds to an Item in the other population within the declared bounds | This document, Section 4.5 |
| observed-without-receipt | The Data Source recorded activity against a Data Object that no Receipt in the Window names | This document, Section 4.5 |
| receipted-without-observation | A Receipt in the Window names a Data Object for which the Data Source recorded no activity | This document, Section 4.5 |
| excluded | The Item was removed from comparison by a Mapping Profile rule | This document, Section 4.4 |
| indeterminate | The evidence or the Mapping Profile does not determine an outcome | This document, Section 4.5 |
| invalid-window | The Window is unreliable (counter regression or snapshot mismatch) | This document, Section 4.6 |

## 9. Implementation Status

_This section is to be removed before publication as an RFC, per
[RFC7942]._

One implementation of both mechanisms exists: the Conarium gateway
(TypeScript, MIT license, @conarium-ai/core on npm). It has run at one
site since July 2026. Its receipts carry per-class masking counts as in
Section 3. Its conarium-reconcile tool implements Section 4.5 against
PostgreSQL statement statistics. The tool is a single file with no
dependency on the package, so a third party can run it without trusting
the implementation under audit. Conformance test vectors ship with the
package.

The state below was measured against the published 0.2.38 package, not
read from the package documentation. It is now continuously checked, not
measured once. Every revision of this section up to -04 described a tool
that had moved past it. Each time, the section claimed less than the code
did. The correction is at the end of this section, because the failure is
more instructive than the current state.

As of 0.2.38 the tool emits the result statement of Section 4.6 as
coverage-reconciliation/2, on a flag of its own. The /1 body is unchanged
and still carries conarium-reconcile/0.1. The /2 result carries `profile`,
`bounds`, `outcome`, `items`, and `counts` under the names used here. The
tool reads Mapping Profiles (Section 4.3), including the three `clocks`
fields.

The behaviour below was observed on one fixture: a Receipt naming the
object, timestamped three seconds before a two-hour Window, together with
one infrastructure statement.

* With no profile, `profile` is null and all three entries in `bounds` are
  undeclared. Both items are indeterminate: the data statement for want of
  a declared skew bound, the infrastructure statement for want of a
  declared exclusion rule. In the /2 result the tool applies no exclusion
  rule that is not in a profile, which Section 4.4 requires. Its /1 output
  still reports such statements under a category of its own, decided by
  rules built into the tool. That output is not a result statement in the
  sense of Section 4.6, and does not claim to be.

* With a profile declaring exclusions but no `clocks` member, the excluded
  item carries the profile rule that removed it. `bounds.exclusion` is
  operator-declared, and `bounds.skew` remains undeclared.

* With `clocks.skew` declared larger than the offset, `bounds.skew` is
  operator-declared and the item remains indeterminate. A declaration does
  not manufacture a match.

* With `clocks.skew` declared smaller than the offset, the same item
  becomes observed-without-receipt. The declared bound reaches the
  comparison, not only the report.

* A skew bound declared both in a profile and through the command line
  fails, unless the two parse to the same number of milliseconds. A
  `clocks` member carrying a fourth key fails and names the key it
  rejected.

One gap remains. The tool's exit codes predate this vocabulary and are not
a mapping of it. They were left unchanged on purpose, because an exit code
is a compatibility contract. Renumbering them to match this document would
break installations while making a specification look implemented. One
code was added rather than renumbered, for the temporal outcome. Existing
callers do not notice it.

The gap that produced this section's own history is closed. The -04
revision carried four statements that were accurate when written and false
within days, because each claimed less than the code did. No mechanism
here found them; a reader holding the document beside the tool's output
did. The -05 revision recorded that the test suite had no check against
this section. It said that, until such a check existed, the section should
be read as a claim about the date it was measured.

A check now runs this section instead of reading it. Every behavioural
statement above is bound to a run of the shipped tool, and the fixture is
named in this document. Two directions are enforced. Every value a run
produced must appear in the sentence that states it. The number of
statements must equal the number of bound runs. A statement with no run is
therefore unmeasured, and a run with no statement is a dropped
measurement. The revision under test is derived from the repository, not named in
the check. A hard-coded revision would be the same class of stale
declaration the check exists to catch.

The first thing the check caught was the sentence in the paragraph above.
From the commit that added the check, -05's account of its own absence was
false. Because a posted draft cannot be edited, this revision is where the
correction has to live. A check whose first finding is the sentence
claiming it does not exist has shown the failure mode it was written for.

Two limits, stated rather than left to be found. The check pins the
behaviour statements but not the prose around them, so a paragraph can
still go stale in a way nothing runs. A failure has two honest
resolutions: change the code back, or write the revision that says what
the code now does. Editing a posted draft is not one of them. The cost of
drift is therefore a document, not a diff.

A second check covers the conformance class rather than this document.
Every outcome the result statement can carry has a case that produces it.
Each independent ground for indeterminate has a case of its own. The list
of outcomes is read from the tool's own result, not restated in the check.
An outcome added to the vocabulary therefore arrives there without a
reminder, failing until some case produces it. A conformance class can
still lose coverage in silence, because nothing in a test set records what
was removed from it. A class that has lost coverage still passes.

Earlier revisions of this document, and releases of that implementation up
to 0.2.21, described a clean reconciliation as "covered". That word
asserted more than the procedure establishes. It was corrected in the
implementation in 0.2.22 and in this document in -03.

The temporal rule added in -04 has the same history, compressed. The
implementation admitted Receipts on an exact comparison across the two
clocks. A Receipt three seconds outside a two-hour Window therefore
produced observed-without-receipt and a bypass message. That was raised in
review of -03 on the SCITT mailing list, reproduced, and corrected in
0.2.27. The correction was then attacked. A Receipt from the previous day
named the same object, moving a real in-Window absence into the new
outcome. The implementation offered the boundary as its explanation, which
a twenty-three hour offset cannot support. Release 0.2.28 bounds what the
implementation is willing to suggest; that is the reporting choice in
Section 4.3. Both defects were in the implementation first, and neither
was found by reading this document. The first came from review of -03 on
the list. The second came from an adversarial review of the
implementation. That review was commissioned because the fix had loosened
a default, and because the fix's author was not the party who should clear
it. What made the second defect sayable was the tool's own output, since
this text did not yet exist. The document's part was smaller and later. It
is where the correction has to be written down, so the next implementation
does not have to be attacked to learn it.

## 10. References

### 10.1. Normative References

[RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement
Levels", BCP 14, RFC 2119, March 1997.

[RFC6838] Freed, N., Klensin, J., and T. Hansen, "Media Type
Specifications and Registration Procedures", BCP 13, RFC 6838, January
2013.

[RFC8126] Cotton, M., Leiba, B., and T. Narten, "Guidelines for Writing an
IANA Considerations Section in RFCs", BCP 26, RFC 8126, June 2017.

[RFC8174] Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key
Words", BCP 14, RFC 8174, May 2017.

[RFC8785] Rundgren, A., Jordan, B., and S. Erdtman, "JSON Canonicalization
Scheme (JCS)", RFC 8785, June 2020.

[RFC9943] Birkholz, H., Delignat-Lavaud, A., Fournet, C., Deshpande, Y.,
and S. Lasker, "An Architecture for Trustworthy and Transparent Digital
Supply Chains", RFC 9943, June 2026.

### 10.2. Informative References

[I-D.aylward-aiga-2] Aylward, E. R., "AI Governance and Accountability
Protocol (AIGA)", Work in Progress, draft-aylward-aiga-2-00, 26 January
2026.

[I-D.chueayen-attestation-receipts] Chueayen, A., "Enforcement Attestation
Receipts for AI Inference Decisions", Work in Progress,
draft-chueayen-attestation-receipts-02, 8 August 2026.

[I-D.farley-acta-signed-receipts] Farley, T., "Signed Decision Receipts
for Machine-to-Machine Access Control", Work in Progress,
draft-farley-acta-signed-receipts-02, 28 June 2026.

[I-D.marques-asqav-compliance-receipts] Marques, J. A. G., "Compliance
Profile of Signed Action Receipts for AI Agents", Work in Progress,
draft-marques-asqav-compliance-receipts-07, 20 July 2026.

[RFC7942] Sheffer, Y. and A. Farrel, "Improving Awareness of Running Code:
The Implementation Status Section", BCP 205, RFC 7942, July 2016.

[RFC8032] Josefsson, S. and I. Liusvaara, "Edwards-Curve Digital Signature
Algorithm (EdDSA)", RFC 8032, January 2017.

[RFC9052] Schaad, J., "CBOR Object Signing and Encryption (COSE):
Structures and Process", STD 96, RFC 9052, August 2022.

## Acknowledgments

The discipline of stating what each structure does not prove is owed
to every auditor who was handed a green dashboard and asked to trust
it.

Iman Schrock reviewed revision -02 on the SCITT mailing list. He
identified two overclaims. One was that a clean reconciliation established
coverage of the source activity. The other was that Transformation
Evidence proved the transformation, rather than the Issuer's assertion of
it. Both were corrected in -03. The outcome vocabulary of Section 4.5
follows from that exchange, as does the rule that a declared bound cannot
yield a stronger outcome. Reviewing -03, the same reviewer established a
further point: an Item whose classification rule does not resolve under
the pinned profile is indeterminate, not excluded. Revision -04 applies
that rule one layer up, to bounds.

Walter Hawkins read the reconciliation implementation. He found the temporal defect that -04 exists to correct. Window
membership is decided across two clocks, so an exact comparison
manufactures an accusation where no gap exists. The failure is asymmetric, because it produces false
findings rather than missed ones. He also observed that the sub-second
case is the dangerous one, because it is the one a reader will believe.
That is why Section 4.5 sets no floor. The requirement that a source
population declare its own completeness on the same standing ladder is
also his.

Joel Hillier, reviewing -04 on the SCITT mailing list, asked for named
fields: a stated encoding for the temporal correspondence, not prose.
Another specification could then adopt the same shape. The three `clocks`
fields in Section 4.3 are written to be copied and answer that request. He
also observed that a gaps section going stale in the understating
direction is the same failure as one that overstates. That is why the
Implementation Status section of this revision was rewritten from
measurement.

Henri Sirkkavaara established the distinction in Section 6.1. One
construction supplies an expected quantity to a verifier from outside. The
other carries it inside the signed material. He built the second, and he
named what the first leaves an auditor unable to do. The consequence is
stated against this document's own implementation, which does the first.
One narrower observation is this author's, arrived at while measuring
his construction: a running count derived from the sequence number it
accompanies adds no information. It is recorded here because it bears on
that construction.

Andrew Yourtchenko reviewed -04 as a reader new to the work. He identified
the length and density of the non-normative prose as the document's
primary obstacle, ahead of any technical point. He proposed applying the principles of ASD-STE100 (Simplified
Technical English) to the non-normative text. He published a rule set
and a rewritten draft to show the effect. The sentence-length pass in -07 follows that suggestion.

## Author's Address

Emek Can Doğru
VERAX TEKNOLOJİ LİMİTED ŞİRKETİ
Türkiye
Email: e.dogru@conarium.dev

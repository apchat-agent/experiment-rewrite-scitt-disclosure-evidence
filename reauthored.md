# Transformation Evidence and Coverage Reconciliation for Auditable Data Disclosure

draft-dogru-scitt-disclosure-evidence-07, re-authored per the rules
snapshot. Normative sentences are mapped at equal strength; the map is
in reauthor-report.md. [GAP:] marks name facts the source never
determines.

## Abstract

Systems that put a policy gateway in front of a data store can sign a
record of each access. Two questions stay open: how values were
changed before delivery, and whether every access left a record. This
document defines two signed evidence payloads for those questions.
The first states, for one delivery, which categories of values were
changed, by which method, and how many times. It carries no values.
The second compares the data store's own activity counters, read at
both ends of a time interval, with the access records for that
interval. Each entry comes out matched, observed with no record,
recorded with no observed activity, excluded, or undecided. Neither
payload reports a plain pass. Both are meant for registration on an
append-only log that a third party can audit.

## 1. Introduction

Systems place a policy gateway between an automated client and a data
source. Many of these systems emit signed, hash-chained access
receipts, and several receipt formats exist
[I-D.farley-acta-signed-receipts]
[I-D.marques-asqav-compliance-receipts]
[I-D.chueayen-attestation-receipts] [I-D.aylward-aiga-2]. All of them
share one property. A receipt is evidence from the party that
performed the access, about an event that party chose to record. Two
gaps follow.

The first gap is the transformation. A receipt states that access
happened and names the policy decision. A gateway may mask, redact,
or tokenize values before disclosure. That transformation is the
privacy claim, and the receipt does not describe it. An auditor
learns that a table was read. The auditor cannot learn whether
protected columns left the gateway transformed or in the clear.

The second gap is coverage. A receipt set covers only the accesses
that produced receipts. A client that reaches the data source without
the gateway produces none. Hash chains detect removal and reordering
of records that exist. A record never created leaves no mark in the
chain. Completeness needs a second account of activity, from a party
other than the gateway: the data source itself.

This document defines two evidence structures, one per gap:

- **Transformation Evidence** (Section 4): a statement bound to one
  Disclosure. It names which classes of values were transformed, by
  which action, in what count. It carries no values.
- **Coverage Reconciliation** (Section 5): a procedure and a signed
  result. It compares source activity snapshots at the two ends of a
  Window with the receipt set for that Window. It classifies each
  Item of either account. Neither population is assumed complete. The
  operator declares the correspondence (Section 5.3).

Both structures are payloads for registration as Signed Statements on
a SCITT Transparency Service [RFC9943], whose append-only log a third
party can audit. Farley, Marques, and Chueayen use Ed25519 [RFC8032]
with JSON Canonicalization [RFC8785]. Aylward uses Ed25519 in a
hybrid suite without JCS. None of the four defines a transformation
statement or a reconciliation.

### 1.1. Threat model and applicability

The full account is in Section 7. This bound comes ahead of the
procedure that depends on it.

The Gateway and the Data Source are often run by one party. That
party can suppress the source counters. That party writes the Mapping
Profile. A counter reset must fail the Window (Section 5.5), never
yield a clean report. A profile can absorb unreceipted activity or
exclude it. The defence is visibility: a digest-bound profile,
reported exclusions, a stated standing for each bound. Unknown digest
prefixes are rejected. Issuer key compromise is a SCITT-layer
problem. A truncated receipt set still verifies internally. Detecting
the cut needs a quantity from outside that file (Section 7.1).

### 1.2. What the evidence is

Each structure is exactly as strong as its inputs, and says so.
Transformation Evidence is the Issuer's signed assertion that a
transformation was applied (Section 4.3). A reconciliation outcome
that reports activity with no receipt is a statement about absent
evidence (Section 5.6). A reconciliation computed against an
operator-declared correspondence has the standing of that declaration
(Section 5.3). An undecided outcome is reported as undecided, outside
any proportion.

### 1.3. Relationship to coverage attestation

A record can be intact and silent about what is missing. A report can
be complete and silent about what it examined. These are two
failures. They close in different places.

This document closes the first: it lets a mediator's record state
what that record leaves open. The second belongs to coverage
attestation. There, an examination declares its population, names the
basis for it, and accounts for every unit it skipped. Work on that
layer is under way on this list.

The two compose in one direction. They substitute in neither. An
attestation over a mediated examination inherits whatever the
mediator's record leaves open. It inherits that silently, absent a
record that says so. That silence is the failure this document names.
The reverse direction is no rescue. A complete access record over a
population chosen once the results were known is an exact record of a
decided question. One artefact answers half of a two-part question.

## 2. Conventions and Definitions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
"OPTIONAL" in this document are to be interpreted as described in
BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all
capitals, as shown here.

One term keeps one meaning through the full document:

- **Data Source**: The system holding the data, with its own
  accounting of query or access activity (for example, a database's
  statement statistics).
- **Gateway**: The component that mediates access between an
  automated client and a Data Source, applies policy, transforms
  results, and emits receipts.
- **Disclosure**: A single delivery of data (possibly transformed)
  from the Gateway to a client.
- **Receipt**: A signed record of a Disclosure produced by the
  Gateway. This document is agnostic to the receipt format in use.
- **Protected Class**: A named category of values that policy
  subjects to transformation (for example, "email", "national-id",
  "phone").
- **Window**: A time interval over which reconciliation is performed,
  bounded by two snapshots of the Data Source's activity counters.
  The Data Source stamps both bounds. Whether a Receipt falls inside
  them is a question about a second clock, the Gateway's
  (Section 5.5).
- **Mapping Profile**: A versioned statement, declared by the
  operator, of the correspondence expected between one Client-level
  operation and the source-level activity it produces: the bound on
  that multiplicity, the clock source on each side with the skew
  bound between them, and the rules by which activity is excluded
  from comparison. A Mapping Profile is a declaration about a
  deployment, not a measurement performed by the Gateway
  (Section 5.3).
- **Item**: One unit the reconciliation procedure classifies. On the
  source side: one snapshot entry whose pattern counter increased in
  the Window. That is one pattern, not one (pattern, Data Object)
  pair. On the receipt side: one Receipt that names a Data Object the
  snapshots do not account for. Counting each (pattern, Data Object)
  pair as an Item changes observed-without-receipt.
- **Data Object**: A named target of source activity or of a Receipt.
  In the shipped reconciler this is a table (or equivalent schema
  object), not a column. The result records these as objects on an
  Item.
- **Consumer**: A party that reads Transformation Evidence or a
  reconciliation result and presents it to a human or to another
  system.
- **Reconciler**: The party that performs Coverage Reconciliation and
  produces the result statement.
- **Protocol-defined**: A standing this document itself assigns to a
  bound. Example: the invalid-window rule. It is not a measurement.
- **Measured**: A standing a bound has when observation of the
  deployment produced it. It is not operator-declared and not
  assigned by this document.
- **Client-level operation**: One Disclosure, or one client request
  as seen by the Gateway.
- **Source-level statement**: One increment of a Data Source activity
  counter: one snapshot entry for one pattern. It is not
  interchangeable with a Client-level operation.
- **Gateway operator**: The party that operates the Gateway.
- **Data Source operator**: The party that operates the Data Source.
  This document names which operator it means each time. Section 7
  states the limit for deployments with one party in both roles.
- **Issuer**: In the sense of [RFC9943], the party that signs a
  Signed Statement: for Transformation Evidence the Gateway operator,
  for a reconciliation result the Reconciler.
- **Verifier**: A party that checks a signature, a digest, or a
  Transparency Service receipt. The term appears once, for
  independent checking of a disclosed result against the Issuer's
  assertion (Section 4.3).

## 3. Serialization and Digests

Both structures, the Mapping Profile, and the result statement share
one mechanics. A structure is serialized for digesting and signing
with the JSON Canonicalization Scheme [RFC8785]. Digests in this
document are SHA-256. Each is written as a string: the prefix
`sha256:` followed by lowercase hexadecimal. Future documents may
register alternative digest prefixes; an implementation MUST reject a
digest whose prefix it does not recognize rather than guessing.

A CBOR/COSE serialization [RFC9052] of the same data model is
expected once the JSON model has received review. Nothing in the
model depends on JSON specifically.

## 4. Transformation Evidence

### 4.1. Purpose

Transformation Evidence answers, for one Disclosure: which Protected
Classes were transformed in the disclosed result, by which action, in
what count. It makes the transformation claim a first-class, signed,
registrable artifact rather than prose in an operator's
documentation.

### 4.2. Structure

Transformation Evidence is a JSON object with these members:

- **v**: Structure version string. For this document:
  `transformation-evidence/1`.
- **disclosure**: A digest binding this evidence to exactly one
  Disclosure. It is computed over the receipt for that Disclosure
  (or, given a receipt format with a canonical record hash, over that
  hash). Digest form is in Section 3.
- **request**: A digest of the request that produced the Disclosure.
  The digest, never the request text: query text can itself contain
  protected values. [GAP: the source does not define which bytes of
  the request the digest covers, or any request canonicalization.]
- **policy**: An object with `id` (an identifier of the policy
  version applied) and `decision` (the policy outcome under which
  disclosure proceeded). [GAP: the source defines no value space for
  either member.]
- **classes**: An array of objects, one per Protected Class that the
  applied policy recognizes and that occurred in the disclosed
  result, each with:
  - **class**: The Protected Class name, as the policy names it.
  - **action**: One of `mask`, `redact`, `tokenize`, `truncate`, or
    `none`. The value `none` states that the class occurred and was
    disclosed untransformed: a statement some deployments need to
    make.
  - **count**: The number of values of this class in the disclosed
    result to which the action was applied.

The structure MUST NOT carry data values, transformed or otherwise.
Only class names, action names, counts, digests, and identifiers
appear. An implementation encountering a value in a field defined
here MUST reject the structure.

A worked example, every member present:

```json
{
  "v": "transformation-evidence/1",
  "disclosure": "sha256:6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
  "request": "sha256:d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35",
  "policy": {
    "id": "pol-2026-07-01",
    "decision": "allow-with-transformation"
  },
  "classes": [
    { "class": "email",       "action": "mask",   "count": 14 },
    { "class": "national-id", "action": "redact", "count": 2 },
    { "class": "phone",       "action": "none",   "count": 3 }
  ]
}
```

[GAP: `policy.id` and `policy.decision` above are inventions for the
example; the source constrains neither value.] [GAP: the bytes under
the `request` digest are likewise undetermined.]

### 4.3. What Transformation Evidence does not prove

Transformation Evidence describes the disclosure surface of one
result. It does not state that a protected value is unlearnable by
the client. Request languages can permit predicates over protected
columns. An allowed request can then answer questions about a masked
value. The value itself is never disclosed. A result-count of one
versus zero is one bit. The evidence for such a Disclosure is still
accurate. The value was transformed in the result. The client may
still have learned something.

Consumers MUST NOT present Transformation Evidence as proof of
non-exposure. Nor is it proof that the transformation was applied:
the payload is a signed assertion by the Issuer that it was. A
Verifier may check the disclosed bytes against that assertion. Until
that check, the evidence is what the pinned Issuer asserted. An
Issuer that is itself the transforming Gateway is self-attesting. A
Consumer who treats that assertion as verified has dropped the Issuer
from the trust statement. Nothing replaces that Issuer. A deployment
that needs a class to be unlearnable must enforce that in policy, by
refusing the objects that carry the class.

The classes array is bounded by what the applied policy recognizes. A
value belonging to a class the policy does not name is not counted. A class can be absent from the array for two reasons. Either no values
of that class occurred in the result, or the policy does not name the
class.
The array does not distinguish the two. A Consumer MUST NOT present
the absence of a class as evidence that no values of that class were
disclosed.

## 5. Coverage Reconciliation

### 5.1. Purpose

Coverage Reconciliation answers, for one Window: did the Data
Source's own accounting record activity for which no Receipt exists?
It is the mechanism by which "the gateway was bypassed" or "the
receipt sink failed" becomes detectable rather than invisible.

The two accounts under comparison originate from different
components: the receipt set from the Gateway, the activity counters
from the Data Source. A Gateway cannot make bypassed activity
disappear from an account it does not produce. Components under one
operator make that separation administrative. The same-operator limit
is in Section 7.

### 5.2. Activity snapshots

A snapshot is a JSON object capturing the Data Source's cumulative
activity counters at a point in time:

- **v**: Snapshot version string. For this document:
  `activity-snapshot/1`.
- **ts**: The time the snapshot was taken (ISO 8601).
- **source**: An identifier of the Data Source and the accounting
  scope within it (for example, the database role whose activity is
  counted). Both snapshots of a Window MUST carry the same source; a
  mismatch invalidates the Window. [GAP: the source defines no format
  for this identifier.]
- **entries**: An array of objects, one per activity pattern the
  source's accounting distinguishes, each with:
  - **pattern**: A digest of the normalized activity pattern (for
    example, a normalized statement with constants removed). The
    digest, not necessarily the text: pattern text can embed
    protected values and schema detail. Deployments MAY retain
    pattern text privately for diagnosis; only the digest is required
    here. [GAP: the normalization itself is exemplified, never
    specified. Two accounting layers can normalize one statement
    differently.]
  - **count**: The cumulative counter value for this pattern at `ts`.

A worked example, every member present:

```json
{
  "v": "activity-snapshot/1",
  "ts": "2026-08-20T06:00:00Z",
  "source": "pg-prod-1/role:app_reader",
  "entries": [
    { "pattern": "sha256:4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fca", "count": 41290 },
    { "pattern": "sha256:ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d", "count": 355 }
  ]
}
```

[GAP: the `source` string above follows the shipped reconciler's
habit; the source document constrains only "an identifier".]

### 5.3. Mapping profiles

One Client-level operation may produce several Source-level
statements. The multiplicity is a property of the deployment, not of
the Gateway. A pooler or an object-relational mapper can produce it.
A Gateway cannot measure a correspondence it does not produce.

The operator declares a Mapping Profile. For each Client-level
operation it covers, the profile states the expected source-level
patterns. It states the multiplicity bound. It states the exclusion
rules (Section 5.4). It carries a version identifier. It is
serialized and digested as in Section 3. [GAP: outside the `clocks`
member below, the source gives the profile no encoding. Patterns,
multiplicity bound, and exclusion rules have no named fields.]

The profile declares the temporal correspondence on the same ground:
the operator knows it, the Gateway cannot measure it. The Data Source
stamps snapshots. The Gateway stamps Receipts. Both clock identities
and the skew bound between them are operator statements. A claim that both sides read one clock, so the bound is zero, is still
a declaration. One clock read twice is not read at the same instant.
Judging that residue is the operator's call about the deployment. The
rule below forbids presenting that call as measured. This document
refuses a third case: zero absent any look, declared by nobody, read
as agreement.

The temporal correspondence is three fields under a `clocks` member,
encoded so another specification can adopt the same shape:

- **clocks.observation**: String. An identifier for the clock that
  stamps the activity snapshots: the Data Source side.
- **clocks.receipt**: String. An identifier for the clock that stamps
  Receipts: the Gateway side.
- **clocks.skew**: Duration. The bound on how far those two clocks
  may differ. A duration is a decimal integer with a unit suffix of
  `ms`, `s`, `m`, or `h`, or a bare decimal integer read as
  milliseconds: `500ms`, `5s`, `2m`, `1h`, `5000`. A duration that
  does not parse is an error, not a default.

An implementation MUST reject a clocks member carrying any key other
than these three, and SHOULD name the key it rejected: a field
ignored without a report declares less than its author believes.

A declaration that both sides read one clock writes all three fields.
The two identifiers may be the same string. The skew may be `0ms`. A
declared zero is a statement someone is accountable for. An assumed
zero is the condition the rules below forbid.

```json
"clocks": {
  "observation": "pg-prod-1/system-clock",
  "receipt": "gw-prod-1/system-clock",
  "skew": "5s"
}
```

[GAP: the identifier format of `clocks.observation` and
`clocks.receipt` is undetermined; the source constrains them to
strings and nothing further.]

A skew bound can arrive twice: in the profile, and through an
interface of the reconciler's own. An implementation MUST NOT select
between them. Two declarations that parse to the same number of
milliseconds are one declaration and proceed. Two that do not are an
operator error and MUST fail, because which declaration prevailed
would not be visible on the result, and a bound whose origin cannot
be read from the result is not usefully declared at all.

A reconciliation result computed against a Mapping Profile MUST bind
that profile's digest, and MUST state, for each bound it relies on,
whether the bound is protocol-defined, measured, operator-declared,
or undeclared. A result MUST NOT present an operator-declared bound
as a measured one. The consequence is a ceiling: a coverage outcome
against a declared correspondence cannot be stronger than the
declaration. An outcome over an operator statement inherits that
standing. A declaration presented as a measurement is an overclaim.
Truth of the declaration does not change that.

An undeclared multiplicity bound makes the affected items
indeterminate (Section 5.5). An implementation MUST NOT substitute a
default bound of one; a one-to-one rule reports false
observed-without-receipt items on any deployment with a pooler in
front of the Data Source, and a silent default would make that error
look like a finding.

An undeclared skew bound is treated the same way. An implementation
MUST NOT substitute a default of zero: zero asserts that the two
clocks agree, which is the assumption that produces the false
accusation this document guards against. It MUST NOT substitute a
bound of its own choosing either, which would decide the operator's
question with a number the operator never saw. Absent the
declaration, items whose only naming Receipt sits outside the Window
are indeterminate, and the result reports the offset. The reader
compares that offset with clocks the reader knows. The Reconciler
cannot.

An implementation MAY, absent a declared bound, decline to offer the
boundary as the explanation for an offset larger than the Window
itself, on the ground that a boundary artefact cannot exceed the
interval it bounds. This is a reporting choice about what an
implementation is willing to suggest, not a change of outcome: the
item is indeterminate either way. The twenty-three hour case that
motivated the choice is in Section 10.

### 5.4. Exclusions

The outcomes of Section 5.5 are produced by the comparison. One
outcome is different in kind. `excluded` is a decision taken ahead of
the comparison: it decides what will be compared at all. A
reconciliation can be made to come out clean through this outcome.
The rules here make each exclusion visible in the result.

Exclusion rules MUST be stated in the Mapping Profile and are
therefore covered by its digest. A result statement MUST report the
count of excluded items and the rule that excluded each of them. An
implementation MUST NOT exclude items by a rule that is not in the
profile. Without these constraints a clean result and a result
cleaned by exclusion look the same. The digest that pins what was
compared misses the step that decided what was compared. Session or
catalog housekeeping is a legitimate exclusion. Exclusions need not
be rare. They must be visible and pinned.

Pinning reproduces the decision. It does not judge it. The rule
identifier shows a reader which rule removed each Item. The reader
can check that the rule was in the digest-covered profile. A
housekeeping rule and a rule that hides the auditor's target pin the
same way. They verify the same way. Consumers MUST NOT read a pinned
exclusion as a justified one, and a result statement MUST NOT present
the digest as evidence that the exclusions were appropriate. The same
distinction separates a declared bound from a measured one
(Section 5.3). Here it applies to what is compared at all.

### 5.5. Reconciliation procedure

Given a start snapshot, an end snapshot, and the receipt set for the
Window, a Reconciler proceeds as follows.

Window validity is checked first. The two snapshots MUST carry the
same v and source, the end ts MUST be later than the start ts, and no
pattern's counter may be lower at the end than at the start. A
counter regression means the source's accounting was reset or altered
inside the Window; the Window is then unreliable, and the reconciler
MUST report failure for the Window as a whole rather than reconciling
the surviving patterns. An attacker who can reset counters must gain
an error, not a clean report. Section 7 gives the same-operator
ground for failing the whole Window rather than dropping the reset
patterns.

Window membership is itself a bound. It is decided across two clocks.
The Data Source stamps the snapshot timestamps. The Gateway stamps a
Receipt's timestamp. An exact comparison between them fails in one
direction. A Gateway clock that trails the Data Source moves a
Receipt out of the Window. The object that Receipt names then looks
like activity with no Receipt: the outcome whose semantics name
gateway bypass (Section 5.6). A clock difference of seconds can
produce the accusation. No real gap is required. The measured case
was three seconds (Section 10). The procedure sets no floor: a
smaller offset is harder for a reader to suspect. The Mapping Profile
states the skew bound (Section 5.3). [GAP: the source never states
whether the Window's own bounds are inclusive or exclusive.]

The profile's clock declaration governs here. An undeclared skew
bound puts the affected items under the indeterminate rule below, not
under absent evidence. A declared bound can be exceeded: a Receipt
falling further outside the Window than the bound allows is not
explained by the boundary. The item takes the outcome it would have
had, and a reconciler MUST report which bound it applied to reach
that.

For each pattern whose counter increased during the Window, the
reconciler attributes the pattern to the data objects it touches. It
checks whether any Receipt in the Window names those objects. [GAP:
the attribution of a pattern to Data Objects has no specified
procedure.] [GAP: how a Receipt names a Data Object is left to the
receipt format, which this document does not constrain.] Matching is
per pattern and per data object, not per call count: one client-level
request may legitimately produce more than one source-level
statement, so call counts and receipt counts MUST NOT be compared
one-to-one. A pattern whose target objects cannot be determined MUST
NOT be silently ignored; it receives the indeterminate outcome below.

The comparison is between two populations: source-level activity and
Receipts. Neither population is assumed complete. Each Item in either
population receives exactly one of these outcomes, named as fields by
the result statement (Section 5.7):

- **matched**: The item corresponds to an item in the other
  population within the bounds of the applicable Mapping Profile
  (Section 5.3), and within the Window. The profile's two kinds of
  bound act differently here: a multiplicity bound admits items to
  this outcome, and the skew bound does not. A Receipt outside the
  Window is never matched, however small the declared skew. The bound
  qualifies how far the boundary can be trusted, not where the
  boundary is.
- **observed-without-receipt**: The Data Source recorded activity
  against an object that no Receipt in the Window names.
- **receipted-without-observation**: A Receipt in the Window names an
  object for which the Data Source's counters record no activity.
- **excluded**: The item was removed from comparison, ahead of
  matching, by a rule stated in the Mapping Profile (Section 5.4).
- **indeterminate**: The evidence or the Mapping Profile does not
  determine an outcome. Four grounds: the pattern's objects could not
  be attributed, a required multiplicity or skew bound is undeclared,
  the item's only naming Receipt falls outside the Window, or the
  Window's evidence cannot decide.

An implementation MUST NOT report an item as matched when the outcome
is indeterminate; the absence of a decision is not a decision. In
particular, where a Mapping Profile does not declare the multiplicity
bound that the comparison requires, the affected items are
indeterminate and not clean coverage.

The same rule binds the temporal bound, in the opposite direction.
Where every object an item leaves unaccounted for is named by a
Receipt that falls outside the Window, the item is indeterminate, and
an implementation MUST NOT report it as observed-without-receipt. A
reconciler cannot distinguish a Gateway clock that trails the Data
Source from a Receipt written late. Reporting absent evidence would
assert a distinction the reconciler did not make. An item that leaves
even one object named by no Receipt at all sits outside this rule:
that is a genuine absence. A neighbouring object's clock does not
make it undecidable.

indeterminate here is not a weaker pass. The comparison did not come
out clean, and a result statement MUST carry the outcome and the
offset that produced it. The implementation is forbidden one thing:
stating the cause. [GAP: the result statement of Section 5.7 defines
no member to carry this offset, or the applied bound of the reporting
rule above.]

A reconciliation with no observed-without-receipt items establishes one
thing. Each observed source-level item is attributable to a Receipt
naming the same object, under the declared correspondence. It
does not establish that every source-level statement was itself
receipted, and a result MUST NOT be stated in terms that assert it.
One Receipt naming an object can clear an unbounded number of further
statements against that object inside the Window. The procedure has
then established object attribution and nothing stronger.

### 5.6. Semantics of the outcomes

An observed-without-receipt outcome states that evidence is absent.
It does not state why. Gateway bypass produces it. Receipt sink
failure produces it. Accounting scope mismatch produces it. A Receipt that names the object, outside the Window on the two clocks,
once produced it too. Section 5.5 removes that case from this outcome. An earlier revision listed the mirror condition under
receipted-without-observation only. This text names both directions,
keeping the omission visible. A result statement MUST NOT label such
activity as an intrusion, a breach, or an intentional act, and
consumers MUST NOT present it as such. It is not, and MUST NOT be
presented as, proof of intent or of a breach. The mechanism surfaces
the condition. Cause is investigation, not reconciliation.

A receipted-without-observation outcome is likewise a statement about
evidence, not by itself a fault. A counter reset at the Window
boundary produces the same shape. So does an intermediary that
collapses statements. So does an increment outside the snapshot pair.
So does a receipt describing activity that never occurred. An
implementation MAY treat it as a failure condition under a policy of
its own; this document does not define it as one, because the shape
does not distinguish the cases.

An indeterminate outcome is a result, not a degraded pass. It MUST
NOT be resolved by assumption in either direction: neither counted as
matched because nothing contradicts it, nor reported as missing
activity because nothing confirms it. An implementation under
pressure to produce a single number will be tempted to fold
indeterminate into a coverage proportion; that operation destroys the
only property that distinguishes this vocabulary from a bare pass,
and MUST NOT be performed.

Verification of receipt signatures and chain integrity happens ahead
of reconciliation, under the rules of the receipt format in use.
Reconciliation compares an already-verified receipt set against
source accounting. It does not re-verify.

### 5.7. Result statement

The reconciliation result is a JSON object:

- **v**: `coverage-reconciliation/2`. The outcome vocabulary of
  coverage-reconciliation/1 is not a subset of this one: a /1 result
  reporting `covered` asserts more than the procedure establishes,
  and is not re-expressible here. A consumer MUST NOT read a /1
  result as a /2 result.
- **window**: Object with `start` and `end` (the two snapshot ts
  values).
- **source**: The common source identifier of the two snapshots.
- **snapshots**: Object with `start` and `end` digests of the two
  snapshot structures.
- **receipts**: A digest identifying the receipt set that was
  compared (for chained receipt formats, the chain head digest and
  the sequence range are RECOMMENDED as the identifying material). A
  result SHOULD state whether that identifying material was obtained
  independently of the Issuer or read from the receipt set itself:
  the two are not equivalent evidence, and a Consumer cannot tell
  them apart from the digest (Section 7.1). [GAP: no member is
  defined to carry that statement.]
- **profile**: The digest and version identifier of the Mapping
  Profile the comparison was computed against (Section 5.3), or null
  absent a declared profile. Under null, every item whose outcome
  depends on a multiplicity bound is indeterminate. So is every item
  whose only naming Receipt falls outside the Window: no profile, no
  declared skew bound.
- **bounds**: For each bound the comparison relied on, its source:
  protocol-defined, measured, operator-declared, or undeclared. A
  result whose bounds are operator-declared states an outcome of that
  standing, no stronger. [GAP: the body never enumerates the key
  names under bounds. The draft's removable Implementation Status
  section is the only text showing `bounds.skew` and
  `bounds.exclusion`.]
- **outcome**: `invalid-window` for an unreliable Window
  (Section 5.5); no-exceptions for every item matched or
  excluded; exceptions for any item observed-without-receipt,
  receipted-without-observation, or indeterminate. The name states
  what the comparison left open, not what it proved. A result MUST
  NOT carry an outcome name that asserts coverage of the source
  activity, and no-exceptions is not such an assertion: it says the
  comparison produced no open item under the declared correspondence,
  which is bounded by that correspondence (Section 5.3) and by the
  fact that neither population is assumed complete.
- **items**: The list of items whose outcome is not matched, each
  with its outcome and, for excluded, the profile rule that excluded
  it. Pattern digests, not pattern text, for the reasons in
  Section 5.2. [GAP: the member names of an item object are never
  enumerated. The Data Objects an Item records, the offset of
  Section 5.5, and the applied bound have no named fields.]
- **counts**: The number of items in each outcome, including matched
  and excluded. An implementation MUST NOT aggregate indeterminate
  items into a proportion of coverage: an outcome that does not
  decide cannot be averaged into one that does, and reporting it as a
  percentage restores precisely the overclaim this vocabulary exists
  to prevent.

A result carries matched as a count and every other outcome as an
accounting. The asymmetry is deliberate. A count a reader cannot
reconstruct is an assertion about a population the producer alone can
see. This count is not that. The result digests both activity
snapshots and the receipt set it compared (Sections 5.2 and 3). A
reader holding those inputs recomputes the matched set. The size is
not an assertion. The count is a convenience over material the reader
already has. That property fails in one named case: identifying
material read from the receipt set itself (Section 7.1). A reader
then recomputes the Issuer's answer. The digest checks transcription,
not completeness. The matched count inherits that standing.

The result statement is serialized and digested as in Section 3. It
is intended to be signed by the reconciling party and registered
(Section 6). The reconciler SHOULD be operationally independent of
the Gateway; where it is not, registration on a Transparency Service
at least makes the result's existence and timing third-party-visible.

A worked example, every member present:

```json
{
  "v": "coverage-reconciliation/2",
  "window": { "start": "2026-08-20T06:00:00Z", "end": "2026-08-20T08:00:00Z" },
  "source": "pg-prod-1/role:app_reader",
  "snapshots": {
    "start": "sha256:2c624232cdd221771294dfbb310aca000a0df6ac8b66b696d90ef06fdefb64a3",
    "end":   "sha256:19581e27de7ced00ff1ce50b2047e7a567c76b1cbaebabe5ef03f7c3017bb5b7"
  },
  "receipts": "sha256:4a44dc15364204a80fe80e9039455cc1608281820fe2b24f1e5233ade6af1dd5",
  "profile": {
    "digest": "sha256:4fc82b26aecb47d2868c4efbe3581732a3e7cbcc6c2efb32062c08170a05eeb8",
    "version": "profile-2026-08-01"
  },
  "bounds": {
    "multiplicity": "operator-declared",
    "skew": "operator-declared",
    "exclusion": "operator-declared"
  },
  "outcome": "exceptions",
  "items": [
    {
      "outcome": "indeterminate",
      "pattern": "sha256:ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d"
    },
    {
      "outcome": "excluded",
      "pattern": "sha256:e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683",
      "rule": "exclude-catalog-housekeeping"
    }
  ],
  "counts": {
    "matched": 12,
    "observed-without-receipt": 0,
    "receipted-without-observation": 0,
    "excluded": 1,
    "indeterminate": 1
  }
}
```

[GAP: `bounds.multiplicity` and the item members `pattern` and `rule`
are inventions for the example; the body defines none of these key
names.] [GAP: the indeterminate item above owes an offset under
Section 5.5, and no field exists to carry it.]

## 6. Registration on a Transparency Service

Both structures are payloads for Signed Statements in the sense of
[RFC9943]. The Issuer signs the serialized structure: the Gateway
operator for Transformation Evidence, the Reconciler for a
reconciliation result. The Issuer registers the Signed Statement on a
Transparency Service. The SCITT Receipt is proof of inclusion, at a
position, in an append-only log. A party other than the Issuer
operates that log.

This layering is deliberate: the structures gain their audit value
from registration the Issuer cannot quietly rewrite. SCITT already
defines that place, its trust model, and its verification. Digests in
this document bind evidence to receipts over the payload. The binding
survives registration. It is not over the envelope.

## 7. Security Considerations

- **Same-operator collusion.** In many deployments one party operates
  both the Gateway and the Data Source. Value against that party is
  reduced. An operator with administrative access to the source
  accounting can suppress the counters. The invalid-window rule
  (Section 5.5) turns a reset into a visible failure. Registration
  (Section 6) makes suppression of already-issued results detectable.
  An operator who controls both accounts and never registers is
  outside this mechanism. Assurance against that operator needs an
  accounting path the operator cannot write to: a deployment
  property, not a payload property.
- **Counter manipulation.** An attacker who can reset or rewind
  source counters could otherwise hide activity between snapshots.
  The MUST-fail rule exists for this case: a Window containing a
  regression is reported unreliable in its entirety. Snapshot
  frequency bounds the exposure. Shorter Windows cost the attacker a
  visible failure sooner.
- **Declared correspondence as an attack surface.** The operator
  writes the Mapping Profile (Section 5.3). It decides what counts as
  a match. It decides what is excluded ahead of matching. A wider
  multiplicity bound can absorb unreceipted activity. An added
  exclusion rule can remove it from comparison. This mechanism does
  not defend against that operator. Nothing computed against a
  declaration can. It makes the declaration part of the evidence: the
  profile is versioned, its digest is bound into the result,
  exclusions are reported with count and rule, and the result states
  that its bounds are operator-declared. A reader who trusts the
  result sees that dependency. Registration (Section 6) makes the
  sequence of declared profiles third-party-visible. A silently
  edited profile would lose that.
- **Digest agility.** Digests are prefixed (Section 3); an
  implementation MUST reject unknown prefixes. Accepting an unknown
  prefix as an opaque match would let an attacker route around
  comparison.
- **Signature and key compromise.** Signing and registration are
  inherited from the SCITT layer. Key management, revocation, and the
  consequences of Issuer key compromise are governed there, not here.
  A compromised Issuer key voids the evidentiary value of statements
  under that key, as it does for any signed artifact.

### 7.1. Receipt set completeness and where the expected count comes from

A receipt set whose most recent entries have been removed is
internally consistent. Every remaining link verifies. Every signature
checks. The file does not state how many entries it should have
contained. Reconciliation does not close this: it compares the
receipt set against source accounting, and an operator who can
truncate one can generally suppress the other. Detecting the removal
needs a count, a head digest, or an equivalent quantity. That
quantity must not come from the truncated file.

What matters to a Consumer is where that material arrives from. The
two constructions differ in a way a digest does not show.

An implementation may accept the expected quantity as a verifier
input. The check is then only as trustworthy as that input. An
auditor who holds only the receipt file has one source for it: the
Issuer, the party under examination. The verification is real. Its
independence is supplied by whoever ran it, not by the artifacts.

An implementation may instead carry the quantity inside the signed
material. The set then testifies to its own extent. That closes the
first gap, at a cost worth stating: the Issuer signs an assertion
about a population it has not finished producing. A per-entry counter
constrains only the entries that were kept. A sealed total is
required as well. A running count derived from the sequence number it accompanies adds no
information. It restates the position of a present record. It says
nothing about an absent one. The useful
property is a sealed quantity over a held set, not a per-record
decoration.

This document requires neither construction. It requires that a
result identifying a receipt set be readable as to which one it used.
A Consumer who cannot tell them apart will read an external pin as
proof of the set's own completeness. That is the strongest claim in
this area, and the one least often actually made.

## 8. Privacy Considerations

Every structure in this document follows one rule: evidence about
protected data must not itself become a disclosure channel.
Transformation Evidence carries class names, action names, and
counts, never values. Request and pattern references are digests:
query and pattern text can embed values and schema detail. Class
names and counts do show that a class was present, and in what
quantity. Deployments that treat even that as sensitive can keep the
payloads private and register only the digests. Third-party audit is
then a permissioned act.

## 9. IANA Considerations

This document requests registration of two media types and the
creation of two registries. Registrations follow [RFC6838]. Registry
policy is Specification Required as defined in [RFC8126].

### 9.1. Media type: application/transformation-evidence+json

- Type name: application
- Subtype name: transformation-evidence+json
- Required parameters: None.
- Optional parameters: None.
- Encoding considerations: 8bit; binary UTF-8 JSON. For digesting and
  signing, the payload is serialized with [RFC8785].
- Security considerations: See Section 7 and Section 4.3. The payload
  MUST NOT carry data values.
- Interoperability considerations: Implementations that do not
  recognize the v member MUST reject the object.
- Published specification: This document, Section 4.2.
- Applications that use this media type: Policy gateways and auditors
  that record or verify a disclosure transformation.
- Fragment identifier considerations: None.
- Additional information: Deprecated alias names: none. Magic
  number(s): none. File extension(s): none. Macintosh file type
  code(s): none.
- Person and email address for further information: See the Author's
  Address section.
- Intended usage: COMMON
- Restrictions on usage: None.
- Author: See the Author's Address section.
- Change controller: IETF

### 9.2. Media type: application/coverage-reconciliation+json

- Type name: application
- Subtype name: coverage-reconciliation+json
- Required parameters: None.
- Optional parameters: None.
- Encoding considerations: 8bit; binary UTF-8 JSON. For digesting and
  signing, the payload is serialized with [RFC8785].
- Security considerations: See Section 7 and Section 5.6.
- Interoperability considerations: A consumer MUST NOT read a
  coverage-reconciliation/1 result as a /2 result (Section 5.7).
- Published specification: This document, Section 5.7.
- Applications that use this media type: Reconcilers and auditors
  that compare source activity with a receipt set.
- Fragment identifier considerations: None.
- Additional information: Deprecated alias names: none. Magic
  number(s): none. File extension(s): none. Macintosh file type
  code(s): none.
- Person and email address for further information: See the Author's
  Address section.
- Intended usage: COMMON
- Restrictions on usage: None.
- Author: See the Author's Address section.
- Change controller: IETF

### 9.3. Transformation Actions registry

IANA is asked to create a registry titled "Transformation Actions" in
a new "Disclosure Evidence" group. Registration policy: Specification
Required ([RFC8126]). Template: action name (unique ASCII token),
description, reference.

| Action name | Description | Reference |
|---|---|---|
| mask | Replace a value with a class-level placeholder | This document, Section 4.2 |
| redact | Remove a value | This document, Section 4.2 |
| tokenize | Replace a value with a stable token | This document, Section 4.2 |
| truncate | Shorten a value | This document, Section 4.2 |
| none | The class occurred and was disclosed untransformed | This document, Section 4.2 |

### 9.4. Coverage Reconciliation Outcomes registry

IANA is asked to create a registry titled "Coverage Reconciliation
Outcomes" in the same "Disclosure Evidence" group. Registration
policy: Specification Required ([RFC8126]). Template: outcome name
(unique ASCII token), description, reference.

| Outcome name | Description | Reference |
|---|---|---|
| matched | The Item corresponds to an Item in the other population within the declared bounds | This document, Section 5.5 |
| observed-without-receipt | The Data Source recorded activity against a Data Object that no Receipt in the Window names | This document, Section 5.5 |
| receipted-without-observation | A Receipt in the Window names a Data Object for which the Data Source recorded no activity | This document, Section 5.5 |
| excluded | The Item was removed from comparison by a Mapping Profile rule | This document, Section 5.4 |
| indeterminate | The evidence or the Mapping Profile does not determine an outcome | This document, Section 5.5 |
| invalid-window | The Window is unreliable (counter regression or snapshot mismatch) | This document, Section 5.7 |

## 10. Implementation Status

_This section is to be removed before publication as an RFC, per
[RFC7942]._

One implementation of both mechanisms exists: the Conarium gateway
(TypeScript, MIT license, @conarium-ai/core on npm). It has run at
one site since July 2026. Its receipts carry per-class masking counts
as in Section 4. Its conarium-reconcile tool implements Section 5.5
against PostgreSQL statement statistics. The tool is a single file
with no dependency on the package. A third party can run it without
trusting the implementation under audit. Conformance test vectors
ship with the package.

The state below was measured against the published 0.2.38 package,
not read from its documentation. It is now checked, not measured
once. Every revision of this section up to -04 described a tool that
had moved past it. Each time it claimed less than the code did. The
correction is at the end of this section. The failure is more
instructive than the current state.

As of 0.2.38 the tool emits the result statement of Section 5.7 as
coverage-reconciliation/2, on a flag of its own. The /1 body is
unchanged and still carries conarium-reconcile/0.1. The /2 result
carries profile, bounds, outcome, items, and counts under the names
used here. It reads Mapping Profiles (Section 5.3), including the
three clocks fields.

The behaviour below was observed on one fixture: a Receipt naming the
object, timestamped three seconds before a two-hour Window, together
with one infrastructure statement.

- With no profile: profile is null, all three entries in bounds are
  undeclared, and both items are indeterminate. The data statement
  lacks a declared skew bound; the infrastructure statement lacks a
  declared exclusion rule. In the /2 result the tool applies no
  exclusion rule that is not in a profile: the requirement of
  Section 5.4. Its /1 output still reports such statements under a
  category of its own, decided by built-in rules. That output is not
  a result statement in the sense of Section 5.7 and does not claim
  to be.
- With a profile declaring exclusions but no clocks member: the
  excluded item carries the profile rule that removed it,
  bounds.exclusion is operator-declared, and bounds.skew remains
  undeclared.
- With clocks.skew declared larger than the offset: bounds.skew is
  operator-declared and the item remains indeterminate. A declaration
  does not manufacture a match.
- With clocks.skew declared smaller than the offset: the same item
  becomes observed-without-receipt. The declared bound reaches the
  comparison, not only the report.
- A skew bound declared both in a profile and through the command
  line fails unless the two parse to the same number of milliseconds.
  A clocks member carrying a fourth key fails and names the key it
  rejected.

One gap remains. The tool's exit codes predate this vocabulary. They
are not a mapping of it. They were left unchanged on purpose: an exit
code is a compatibility contract. Renumbering them to match this
document would break installations and make a specification look
implemented. One code was added rather than renumbered, for the
temporal outcome. Existing callers do not notice it.

The gap that produced this section's own history is closed. The -04
revision carried four statements, accurate at writing and false
within days. Each claimed less than the code did. No mechanism here
found them. A reader holding the document beside the tool's output
did. The -05 revision recorded that the test suite had no check
against this section. Until such a check existed, it said, read the
section as a claim about the date it was measured.

A check now runs this section rather than reading it. Every
behavioural statement above is bound to a run of the shipped tool.
The fixture is named in this document. Two directions are enforced.
Every value a run produced must appear in the sentence that states
it. The number of statements must equal the number of bound runs. A
statement with no run is unmeasured. A run with no statement is a
dropped measurement. The revision under test is derived from the repository, not named in
the check. A hard-coded revision is the same class of stale declaration
the check exists to catch.

The first thing it caught was the sentence in the paragraph above.
From the commit that added the check, -05's account of its own
absence was false. A posted draft cannot be edited. This revision is
where the correction has to live. A check whose first finding is the
sentence claiming it does not exist has shown the failure mode it was
written for.

Two limits, stated rather than left to be found. The check pins the
behaviour statements, not the prose around them. A paragraph can
still go stale in a way nothing runs. A failure has two honest
resolutions: change the code back, or write the revision that says
what the code now does. Editing a posted draft is not one of them.
The cost of drift is then a document, not a diff.

A second check covers the conformance class rather than this
document. Every outcome the result statement can carry has a case
that produces it. Each independent ground for indeterminate has a
case of its own. The list of outcomes is read from the tool's own
result, not restated in the check. An outcome added to the vocabulary
arrives there without a reminder. It arrives failing until some case
produces it. A conformance class can lose coverage in silence.
Nothing in a test set records what was removed from it. A class that
has lost coverage still passes.

Earlier revisions of this document, and releases of that
implementation up to 0.2.21, described a clean reconciliation as
"covered". That word asserted more than the procedure establishes. It
was corrected in the implementation in 0.2.22 and in this document in
-03.

The temporal rule added in -04 has the same history, compressed. The
implementation admitted Receipts on an exact comparison across the
two clocks. A Receipt three seconds outside a two-hour Window
produced observed-without-receipt and a bypass message. That was
raised in review of -03 on the SCITT mailing list. It was reproduced.
It was corrected in 0.2.27. The correction was then attacked. A
Receipt from the previous day named the same object. It moved a real
in-Window absence into the new outcome. The implementation offered
the boundary as its explanation. A twenty-three hour offset cannot
support that. 0.2.28 bounds what the implementation is willing to
suggest: the reporting choice in Section 5.3. Both defects were in
the implementation first. Neither was found by reading this document.
The first came from review of -03 on the list. The second came from
an adversarial review of the implementation. That review was
commissioned because the fix had loosened a default. It was
commissioned again because the fix's author was not the party who
should clear it. The tool's own output is what made the second
sentence sayable. This text did not yet exist. The document's part
was smaller and later. It is where the correction has to be written
down. The next implementation should not have to be attacked to learn
it.

## 11. References

### 11.1. Normative References

- [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate
  Requirement Levels", BCP 14, RFC 2119, March 1997.
- [RFC6838] Freed, N., Klensin, J., and T. Hansen, "Media Type
  Specifications and Registration Procedures", BCP 13, RFC 6838,
  January 2013.
- [RFC8126] Cotton, M., Leiba, B., and T. Narten, "Guidelines for
  Writing an IANA Considerations Section in RFCs", BCP 26, RFC 8126,
  June 2017.
- [RFC8174] Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC
  2119 Key Words", BCP 14, RFC 8174, May 2017.
- [RFC8785] Rundgren, A., Jordan, B., and S. Erdtman, "JSON
  Canonicalization Scheme (JCS)", RFC 8785, June 2020.
- [RFC9943] Birkholz, H., Delignat-Lavaud, A., Fournet, C.,
  Deshpande, Y., and S. Lasker, "An Architecture for Trustworthy and
  Transparent Digital Supply Chains", RFC 9943, June 2026.

### 11.2. Informative References

- [I-D.aylward-aiga-2] Aylward, E. R., "AI Governance and
  Accountability Protocol (AIGA)", Work in Progress, January 2026.
- [I-D.chueayen-attestation-receipts] Chueayen, A., "Enforcement
  Attestation Receipts for AI Inference Decisions", Work in Progress,
  August 2026.
- [I-D.farley-acta-signed-receipts] Farley, T., "Signed Decision
  Receipts for Machine-to-Machine Access Control", Work in Progress,
  June 2026.
- [I-D.marques-asqav-compliance-receipts] Marques, J. A. G.,
  "Compliance Profile of Signed Action Receipts for AI Agents", Work
  in Progress, July 2026.
- [RFC7942] Sheffer, Y. and A. Farrel, "Improving Awareness of
  Running Code: The Implementation Status Section", BCP 205,
  RFC 7942, July 2016.
- [RFC8032] Josefsson, S. and I. Liusvaara, "Edwards-Curve Digital
  Signature Algorithm (EdDSA)", RFC 8032, January 2017.
- [RFC9052] Schaad, J., "CBOR Object Signing and Encryption (COSE):
  Structures and Process", STD 96, RFC 9052, August 2022.

## Acknowledgments

The discipline of stating what each structure does not prove is owed to
every auditor handed a green dashboard and asked to trust it.

Iman Schrock reviewed revision -02 on the SCITT mailing list. He
identified two overclaims. One: a clean reconciliation established
coverage of the source activity. Two: Transformation Evidence proved
the transformation rather than the Issuer's assertion of it. Both
were corrected in -03. The outcome vocabulary of Section 5.5 follows
from that exchange. So does the rule that a declared bound cannot
yield a stronger outcome. Reviewing -03, he established a further
point: an Item whose classification rule does not resolve under the
pinned profile is indeterminate, not excluded. Revision -04 applies
that rule one layer up, to bounds.

Walter Hawkins read the reconciliation implementation. He found the
temporal defect -04 exists to correct. Window membership is decided
across two clocks. An exact comparison manufactures an accusation
with no gap behind it. The failure is asymmetric: false findings, not
missed ones. He observed that the sub-second case is the dangerous
one, the one a reader will believe. That is why Section 5.5 sets no
floor. The requirement that a source population declare its own
completeness on the same standing ladder is his as well.

Joel Hillier, reviewing -04 on the SCITT mailing list, asked for named
fields. He wanted a stated encoding for the temporal correspondence,
not prose, adoptable by another specification. The three clocks fields in
Section 5.3 answer that request. He observed one thing more: a gaps
section going stale in the understating direction is the same failure
as one that overstates. That is why the Implementation Status section
of this revision was rewritten from measurement.

Henri Sirkkavaara established the distinction in Section 7.1. One
construction supplies an expected quantity to a verifier from
outside. The other carries it inside the signed material. He built
the second. He named what the first leaves an auditor unable to do.
The consequence is stated against this document's own implementation,
which does the first. One narrower observation is this author's,
arrived at while measuring his: a running count derived from the
sequence number it accompanies adds no information. The distinction
stands.

Andrew Yourtchenko reviewed -04 as a reader new to the work. He
identified the length and density of the non-normative prose as the
document's primary obstacle, ahead of any technical point. He
proposed applying the principles of ASD-STE100 (Simplified Technical
English) to the non-normative text. He published a rule set and a
rewritten draft to show the effect. The sentence-length pass in -07
follows that suggestion.

## Author's Address

Emek Can Doğru, VERAX TEKNOLOJİ LİMİTED ŞİRKETİ, Türkiye.
Email: e.dogru@conarium.dev

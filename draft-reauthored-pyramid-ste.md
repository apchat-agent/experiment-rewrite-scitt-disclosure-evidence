# Transformation Evidence and Coverage Reconciliation for Auditable Data Disclosure

Re-authored from draft-dogru-scitt-disclosure-evidence-07 (pyramid arm, stage 2). Normative language restored in this stage (stage 3); BCP 14 keyword strengths follow the source draft.

## Abstract

A policy gateway that controls access to a data source can produce a signed receipt for each disclosure. Such receipts do not show how the data was changed before disclosure, and they cannot show accesses that left no receipt. This document defines two evidence payloads that record this information. The first states which protected data classes were changed in one disclosure, and how, without carrying data values. The second compares the data source's activity counters with the receipt set over a time window and gives each item one of five defined outcomes, none stronger than the declared inputs support. Both payloads are registered on a transparency service for independent verification.

## 1. Introduction and Problem Statement

Many systems put a policy Gateway between an automated client and a Data Source. More and more of these systems produce signed, hash-chained access receipts, and several receipt formats exist [I-D.farley-acta-signed-receipts] [I-D.marques-asqav-compliance-receipts] [I-D.chueayen-attestation-receipts] [I-D.aylward-aiga-2]. All of the formats share one limit: the party under audit selects the evidence. A receipt is produced by the Gateway that performed the access.

This limit causes two problems.

First, a receipt states that access happened and names the policy decision. A Gateway may mask, redact, or tokenize values before Disclosure. That transformation is the privacy claim, and the receipt leaves it unrecorded. An auditor learns that a table was read, and only that.

Second, a receipt set covers only the accesses that produced receipts. A client that reaches the Data Source without the Gateway produces no receipt, and hash chains detect only removal and reordering of records that exist. To check completeness, a second record of activity is necessary. That record must come from a party other than the Gateway: the Data Source itself.

This document defines two evidence structures for these two problems. Both are payloads for registration as Signed Statements on a SCITT Transparency Service [RFC9943], whose append-only log a third party can audit:

- **Transformation Evidence** (Chapter 4): a statement bound to one Disclosure. It names the classes of values that were transformed, the action for each class, and a count for each class. Class names, action names, counts, and digests are its full content.
- **Coverage Reconciliation** (Chapter 5): a procedure and a signed result. The procedure compares Data Source activity snapshots at the bounds of a Window with the receipt set for that Window. It gives an outcome to each Item of each record. The procedure treats each record as possibly incomplete. The operator declares the relation between the two records in a Mapping Profile. The result names what was matched, observed-without-receipt, receipted-without-observation, excluded, or indeterminate.


The mechanisms operate under a stated trust limit: one party often operates both the Gateway and the Data Source. Chapter 8 gives the full threat model. The procedure in Chapter 5 is made to meet that model.

Other individual drafts record signed decisions about automated access. Farley [I-D.farley-acta-signed-receipts], Marques [I-D.marques-asqav-compliance-receipts], and Chueayen [I-D.chueayen-attestation-receipts] use Ed25519 [RFC8032] and JSON Canonicalization [RFC8785]. Aylward [I-D.aylward-aiga-2] uses Ed25519 in a hybrid signature suite and does not specify JCS. None of those drafts defines Transformation Evidence or Coverage Reconciliation.

### 1.1. Evidentiary value

Each structure states the exact value of its own evidence.

Transformation Evidence describes the disclosed result of one Disclosure. It is the Issuer's signed claim that a transformation was applied (Chapter 4).

A Coverage Reconciliation result that reports activity without a Receipt is a statement about absent evidence. It is not, and MUST NOT be presented as, proof of intent or of a breach (Chapter 5).

Each reconciliation Item receives one of five defined outcomes (Chapter 5). A reconciliation against an operator-declared relation carries the status of that declaration. An indeterminate outcome is reported as indeterminate, in a count of its own.

## 2. Terminology

One term keeps one meaning through the full document.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.

**Data Source.** The system that holds the data. It keeps its own record of query or access activity, for example, a database's statement statistics.

**Gateway.** The component that controls access between an automated client and a Data Source. It applies policy, transforms results, and produces receipts.

**Disclosure.** One delivery of data from the Gateway to a client. The data can be transformed.

**Receipt.** A signed record of a Disclosure, produced by the Gateway. This document works with every receipt format.

**Protected Class.** A named category of values that policy makes subject to transformation: for example, "email", "national-id", "phone".

**Window.** A time interval over which reconciliation is performed. Two snapshots of the Data Source's activity counters bound the interval. The Data Source stamps both bounds with its own clock. A different clock, the Gateway's, decides whether a Receipt falls inside the bounds (Chapter 5).

**Mapping Profile.** A versioned statement, declared by the operator, of the correspondence expected between one client-level operation and the source-level activity that the operation produces. It contains the bound on that count. It contains the clock source on each side and the skew bound between the clocks. It contains the rules that exclude activity from comparison. A Mapping Profile is a declaration about a deployment.

**Item.** One unit that the reconciliation procedure classifies. On the source side, an Item is one snapshot entry whose pattern counter increased in the Window. That unit is one pattern. On the receipt side, an Item is one Receipt that names a Data Object that the snapshots do not account for. To count each (pattern, Data Object) pair as an Item would change the observed-without-receipt outcome.

**Data Object.** A named target of source activity or of a Receipt. In the shipped reconciler a Data Object is a table (or equal schema object). The result records these as objects on an Item.

**Consumer.** A party that reads Transformation Evidence or a Coverage Reconciliation result and presents it to a person or to another system.

**Reconciler.** The party that performs Coverage Reconciliation and produces the result statement.

**Client-level operation.** One Disclosure, or one client request as the Gateway sees it.

**Source-level statement.** One increase of a Data Source activity counter: one snapshot entry for one pattern.

**Gateway operator.** The party that operates the Gateway.

**Data Source operator.** The party that operates the Data Source. Each use of "operator" in this document names which operator. Where both operators are the same party, Chapter 8 states the limit.

**Issuer.** In the sense of [RFC9943]: the party that signs a Signed Statement. For Transformation Evidence the Issuer is the Gateway operator. For a Coverage Reconciliation result the Issuer is the Reconciler.

**Verifier.** A party that checks a signature, a digest, or a Transparency Service receipt. This document uses the term once: for independent checking of a disclosed result against the Issuer's Transformation Evidence claim (Chapter 4).

Two status values occur again and again when the document speaks about bounds:

**Protocol-defined.** A status that this document itself assigns to a bound. Example: the invalid-window rule.

**Measured.** A status that a bound has when observation of the deployment produced the bound.

Together with *operator-declared* and *undeclared*, these four values form the status set. A result must give one of these status values to each bound (Chapter 5).

## 3. Common Serialization and Digests

Both payloads, Mapping Profiles, and result statements share one serialization rule and one digest rule.

For digests and signatures, a structure is serialized with the JSON Canonicalization Scheme (JCS) [RFC8785].

Digests in this document are SHA-256. They are written as strings with the prefix `sha256:` followed by lowercase hexadecimal. Future documents may register other digest prefixes. An implementation MUST reject a digest whose prefix the implementation does not recognize.

A CBOR/COSE serialization [RFC9052] of the same data model is expected after the JSON model has received review.

## 4. Transformation Evidence

### 4.1. Purpose

Transformation Evidence answers one question for one Disclosure: which Protected Classes were transformed in the disclosed result, with which action, and in what count. The structure exists to make the transformation claim a signed object that can be registered.

Transformation Evidence describes the disclosed result of one Disclosure. Request languages can permit conditions on protected columns. An allowed request can then answer questions about a masked value. The value itself stays out of the result. But a result count of one against a result count of zero is one bit of information. The evidence for such a Disclosure is still correct: the value was transformed in the result. The client can still have learned something. A Consumer therefore MUST NOT present Transformation Evidence as proof that a value was not exposed.

The payload is the Issuer's signed claim that the transformation was applied. A Verifier may check the disclosed bytes against that claim. Before that check, the evidence is only what the named Issuer claimed. Where the Issuer is the Gateway that performed the transformation, the Issuer makes the claim about itself. A Consumer who treats the claim as checked has removed the Issuer from the trust statement, and nothing replaces that Issuer. A deployment that requires that a client cannot learn a class meets that requirement in policy alone. For example, the policy can refuse the objects that carry the class.

### 4.2. Structure

Transformation Evidence is a JSON object with these members:

- `v`: Structure version string. For this document: `transformation-evidence/1`.
- `disclosure`: A digest that binds the evidence to exactly one Disclosure. It is computed over the receipt for that Disclosure. Where the receipt format defines a canonical record hash, it is computed over that hash instead. The digest form is defined in Chapter 3.
- `request`: A digest of the request that produced the Disclosure. The field carries the digest only: query text can itself contain protected values.
- `policy`: An object with `id` (an identifier of the policy version applied) and `decision` (the policy outcome under which disclosure went ahead).
- `classes`: An array of objects. There is one entry for each Protected Class that the applied policy recognizes and that occurred in the disclosed result. Each entry has:
  - `class`: The Protected Class name, as the policy names it.
  - `action`: One of `mask`, `redact`, `tokenize`, `truncate`, or `none`. The value `none` states that the class occurred and was disclosed untransformed. The value `none` is legitimate evidence: a deployment that discloses a class untransformed needs a way to state that.
  - `count`: The number of values of this class in the disclosed result to which the action was applied.

The structure MUST NOT contain data values, transformed or not transformed. Only class names, action names, counts, digests, and identifiers appear. An implementation MUST reject a structure that carries a member not defined here, an `action` outside the five defined values, or a `count` that is not a non-negative integer.

A complete instance. A Disclosure returned twelve rows; the policy `pol-2026-08-1` recognizes the classes `email` and `national-id`; the email values were masked and the national-id values were disclosed untransformed:

```json
{
  "v": "transformation-evidence/1",
  "disclosure": "sha256:5e5813c6bf3df5896c8643a539e76df2902e535a9ebc1c7f77a843cf6f7854f8",
  "request": "sha256:5987f072912bc460f0ea1379c5c9a2f981892ab01ce1bf043c45f4cfeac3c0ee",
  "policy": {
    "id": "pol-2026-08-1",
    "decision": "permit"
  },
  "classes": [
    { "class": "email", "action": "mask", "count": 12 },
    { "class": "national-id", "action": "none", "count": 12 }
  ]
}
```

[GAP: the permitted values of `policy.decision` are not defined — the source says only "the policy outcome under which disclosure went ahead". The value `permit` above is illustrative, not registry-backed.]

The same result under a policy that does not define `national-id` produces a `classes` array with one entry only:

```json
  "classes": [
    { "class": "email", "action": "mask", "count": 12 }
  ]
```

The two arrays differ, and the disclosed data is the same. This is the absence ambiguity of the paragraph above, shown once.

The `classes` array names only the Protected Classes that the applied policy version defines. A class can be absent for two reasons: no values of that class occurred in the result, or the policy does not define the class. The array does not distinguish the two. A Consumer MUST NOT present the absence of a class as evidence that no values of that class were disclosed.

## 5. Coverage Reconciliation

### 5.1. Purpose

Coverage Reconciliation answers one question for one Window: did the Data Source's own counters record activity for which no Receipt exists? This mechanism makes two conditions detectable that no receipt shows: a client that goes around the Gateway, and a receipt sink that fails.

The necessary property is that the two compared records come from different components. The receipt set comes from the Gateway. The activity counters come from the Data Source. A Gateway cannot remove activity from a record that the Gateway does not produce. Where one operator runs both components, that separation is only administrative. Chapter 8 states the same-operator limit.

### 5.2. Activity snapshots

A snapshot is a JSON object that records the Data Source's total activity counters at one point in time:

- `v`: Snapshot version string. For this document: `activity-snapshot/1`.
- `ts`: The time the snapshot was taken, in ISO 8601.
- `source`: An identifier of the Data Source and the counter scope inside it, for example, the database role whose activity is counted. Both snapshots of a Window MUST carry the same `source`; a difference makes the Window invalid.
- `entries`: An array of objects, one for each activity pattern that the source's counters keep apart. Each entry has:
  - `pattern`: A digest of the normalized activity pattern, for example, a normalized statement with constants removed. The field carries the digest only: pattern text can contain protected values and schema detail. Deployments MAY keep pattern text in private storage for diagnosis; only the digest is required here.
  - `count`: The total counter value for this pattern at `ts`.

Reconciliation also takes the receipt set for the Window as input. [GAP: how the receipt set for a Window is assembled or selected before reconciliation — which Receipts are candidates — is not specified; only the question of where the set's identifying material comes from is addressed (Chapter 8).]

### 5.3. Mapping Profiles

One Client-level operation may produce several Source-level statements. That count is a property of the deployment: a connection pooler or an object-relational mapper can produce it. A Gateway cannot measure a relation that the Gateway does not produce.

For this reason, the operator declares a Mapping Profile. For each Client-level operation that the profile covers, the profile states the expected source-level patterns. It states the count bound: the highest count of Source-level statements for one Client-level operation. It states the exclusion rules (Section 5.4). It carries a version identifier. It is serialized and digested as in Chapter 3. [GAP: the full serialized shape of a Mapping Profile is not defined — only the `clocks` member below is given an encoding "so another specification can adopt the same shape"; the expected patterns, multiplicity bound, exclusion rules, and version are described in prose without field names.]

The profile also declares the clock relation, because the operator knows it and the Gateway cannot measure it. The Data Source stamps snapshots. The Gateway stamps Receipts. The profile names the clock on each side and states the skew bound between the two clocks. Both are operator statements. A claim that both sides read one clock, so the bound is zero, is still a declaration. A shared clock source does not make the effective skew zero. Whether the remaining difference matters is the operator's decision about the deployment. The rules below forbid a result that reports that decision as a measurement. The document also refuses a third case: a zero that nobody measured, that nobody declared, and that a reader takes as agreement.

The clock relation is declared in three fields under a `clocks` member. The encoding is given so another specification can adopt the same shape:

- `clocks.observation`: String. An identifier for the clock that stamps the activity snapshots: the Data Source side.
- `clocks.receipt`: String. An identifier for the clock that stamps Receipts: the Gateway side.
- `clocks.skew`: Duration. The bound on how far the two clocks may differ. A duration is a decimal integer with a unit suffix of `ms`, `s`, `m`, or `h`. A decimal integer without a suffix is read as milliseconds. Examples: `500ms`, `5s`, `2m`, `1h`, `5000`. A duration that does not parse is an error.

An implementation MUST reject a `clocks` member that carries any key other than these three, and SHOULD name the key that it rejected: a field that is ignored without a report makes the declaration state less than its author believes.

A declaration that both sides read one clock still writes all three fields: the identifiers may be the same string, and `skew` may be `0ms`. A declared zero is the operator's own statement; an assumed zero stays forbidden by the rules below.

The skew bound may arrive two times: in the profile and through an interface of the reconciler's own. An implementation MUST NOT select between the two. Two declarations that parse to the same number of milliseconds are one declaration, and the procedure continues. Two declarations that do not parse to the same number are an operator error and MUST fail. The reason: the result would not show which declaration won. A useful declaration shows its origin on the result.

A reconciliation result computed against a Mapping Profile MUST bind that profile's digest. For each bound that the result depends on, the result MUST state the bound's status: protocol-defined, measured, operator-declared, or undeclared. A result MUST NOT present an operator-declared bound as a measured bound.

The consequence is an upper limit. Where the declaration is an operator statement, the outcome gets that same status, and the result statement shows it. The same rule applies to absent evidence (Section 5.7).

Where a required count bound is undeclared, the affected Items are indeterminate (Section 5.5). An implementation MUST NOT apply a default bound of one. A one-to-one rule reports false observed-without-receipt Items on any deployment with a pooler in front of the Data Source.

An undeclared skew bound is treated the same way, for the same reason. An implementation MUST NOT apply a default of zero. Zero states that the two clocks agree, and that assumption is exactly what produces the false accusation that this document guards against. The implementation MUST NOT apply a bound of its own choice either. That would decide the operator's question with a number that the operator never saw. Without the declaration, Items whose only naming Receipt sits outside the Window are indeterminate, and the result reports the offset. The reader compares that offset with clocks that the reader alone knows.

Without a declared bound, an implementation MAY decline to offer the Window boundary as the explanation for an offset larger than the Window itself. An effect of the boundary cannot be larger than the interval that the boundary bounds. This choice changes only what an implementation reports as a possible explanation. The Item is indeterminate in both cases. The twenty-three-hour case that led to this choice is in Chapter 11.

### 5.4. Exclusions

An exclusion is a decision taken before the comparison: it decides what enters the comparison at all. An excluded Item receives no other outcome, and a set of exclusions can make a reconciliation show no exceptions. The rules below therefore make each exclusion visible in the result.

Exclusion rules MUST be stated in the Mapping Profile, so that the profile digest covers them. A result statement MUST report the count of excluded Items and the rule that excluded each Item. An implementation MUST NOT exclude an Item by a rule that is not in the profile.

Without these rules, two results look the same: a result with no exceptions, and a result with no exceptions because exclusions removed them. And the digest that binds what was compared would miss the step that decided what was compared. Session or catalog maintenance is a correct reason for exclusion. Exclusions can be frequent. They must be visible and covered by the digest.

A reader can take the digest to mean more than it means. The rule identifier makes the exclusion reproducible. A reader sees which rule removed each Item, and can check that the rule was in the digest-covered profile. A maintenance rule and a rule that removes the auditor's target are recorded the same way and check the same way. The mechanism lets a reader repeat the decision. A Consumer MUST NOT read a recorded exclusion as a correct exclusion. A result statement MUST NOT present the digest as evidence that the exclusions were correct. The same difference holds between a declared bound and a measured bound (Section 5.3); here it applies to what is compared at all.

### 5.5. Reconciliation procedure

Given a start snapshot, an end snapshot, and the receipt set for the Window, a Reconciler proceeds as follows.

**Window validity comes first.** The two snapshots MUST carry the same `v` and `source`. The end `ts` MUST be later than the start `ts`. Each pattern counter at the end is equal to or higher than at the start. A counter that went down means that the source's counters were reset or changed inside the Window. The Window is then invalid. The Reconciler MUST report failure for the Window as a whole, not a reconciliation of the patterns that were not reset. An attacker who can reset counters gets an error. Chapter 8 explains why a reset fails the whole Window: the reason is the same-operator case.

**Window membership is itself a bound.** Two clocks decide it: the Data Source stamps the snapshots, the Gateway stamps the Receipts. An exact comparison between the two clocks fails in one direction. A Gateway clock that runs behind the Data Source moves a Receipt out of the Window. The object that this Receipt names then looks like activity with no Receipt: the outcome whose meaning names Gateway bypass (Section 5.7). A clock difference of seconds can produce that accusation with no real absence at all; the measured case was three seconds (Chapter 11). The procedure applies the skew rule at every offset magnitude, because a smaller offset is harder for a reader to suspect. The Mapping Profile states the skew bound (Section 5.3), and the profile digest covers the bound as it covers every other part. Where the bound is undeclared, the affected Items are indeterminate. Where the bound is declared, and a Receipt falls further outside the Window than the bound permits, the declared bound excludes the boundary as the explanation. The Item then takes the outcome it would have had, and the Reconciler MUST report which bound it applied to get there.

**Matching.** For each pattern whose counter increased during the Window, the Reconciler finds the Data Objects that the pattern uses. It then checks whether any Receipt in the Window names those objects. [GAP: the exact procedure by which a Reconciler attributes a pattern to the Data Objects it touches is not specified — the document says a pattern whose objects cannot be determined is indeterminate, but gives no attribution method; presumably deployment- or profile-specific, left open.] Matching is per pattern and per Data Object. One client-level request may correctly produce more than one source-level statement, so call counts and receipt counts MUST NOT be compared one-to-one. A pattern whose target objects cannot be found MUST NOT be dropped without a report; it gets the indeterminate outcome.

**Outcomes.** The comparison runs between two sets: source-level activity and Receipts. The comparison treats each set as possibly incomplete. Each Item in either set gets exactly one of these outcomes, which the result statement names as fields (Section 5.6):

- **matched**: The Item corresponds to an Item in the other set, inside the bounds of the applied Mapping Profile and inside the Window. A count bound can admit Items to this outcome. Only a Receipt inside the Window can enter this outcome, however small the declared skew. The skew bound states how far the boundary can be trusted.
- **observed-without-receipt**: The Data Source recorded activity against an object that no Receipt in the Window names.
- **receipted-without-observation**: A Receipt in the Window names an object for which the Data Source's counters record no activity.
- **excluded**: The Item was removed from comparison before matching, by a rule stated in the Mapping Profile (Section 5.4).
- **indeterminate**: The evidence or the Mapping Profile does not decide an outcome. That covers four cases. The pattern's objects could not be found. A required count or skew bound is undeclared. The Item's only naming Receipt falls outside the Window. Or the Window's evidence is not sufficient to decide.

An implementation MUST NOT report an Item as matched when the outcome is indeterminate. In particular, where a Mapping Profile does not declare the count bound that the comparison requires, the affected Items are indeterminate.

The same rule applies to the clock bound, in the other direction. An Item can leave objects with no accounting where every such object is named by a Receipt outside the Window. That Item is indeterminate, and an implementation MUST NOT report it as observed-without-receipt. A Reconciler cannot tell a Gateway clock that runs behind from a Receipt written late. To report absent evidence would state a difference that the Reconciler did not find. This rule covers only Items whose every unaccounted object is named by a Receipt outside the Window. An Item that leaves one object with no naming Receipt at all keeps the observed-without-receipt outcome: that absence is real.

An indeterminate Item is an open Item. The comparison did not come out with zero open Items, and the result statement MUST carry the outcome and the offset that produced it. The result states the condition; the cause belongs to investigation (Section 5.7).

A reconciliation with no observed-without-receipt Items shows one thing. Each observed source-level Item can be attributed to a Receipt that names the same object, under the declared relation. It does not show that every source-level statement had its own Receipt, and a result MUST NOT be stated in words that claim that. One Receipt that names an object can clear an unbounded number of further statements against that object inside the Window. In that case the procedure has shown object attribution.

### 5.6. Result statement

The reconciliation result is a JSON object:

- `v`: `coverage-reconciliation/2`. The /2 outcome names are the outcomes of Section 5.5. A /1 result that reports `covered` claims more than the procedure shows. A Consumer MUST NOT read a /1 result as a /2 result.
- `window`: Object with `start` and `end`: the two snapshot `ts` values.
- `source`: The common source identifier of the two snapshots.
- `snapshots`: Object with `start` and `end` digests of the two snapshot structures.
- `receipts`: A digest that identifies the receipt set that was compared. For chained receipt formats, the chain head digest and the sequence range are RECOMMENDED as the identifying material. A result SHOULD also state whether that identifying material was obtained independently of the Issuer or read from the receipt set itself. The two carry different evidentiary value, and the digest alone looks the same in both cases (Chapter 8).
- `profile`: The digest and version identifier of the Mapping Profile that the comparison was computed against, or `null` when none was declared. When `profile` is `null`, every Item whose outcome depends on a count bound is indeterminate. So is every Item whose only naming Receipt falls outside the Window: a `null` profile makes the skew bound undeclared as well.
- `bounds`: For each bound that the comparison depended on, its status: protocol-defined, measured, operator-declared, or undeclared. A result whose bounds are operator-declared states an outcome of that same status.
- `outcome`: `invalid-window` when the Window is invalid (Section 5.5). Otherwise `no-exceptions` when every Item is matched or excluded, and `exceptions` when any Item is observed-without-receipt, receipted-without-observation, or indeterminate. The name states what the comparison left open. A result MUST NOT carry an outcome name that claims coverage of the source activity. `no-exceptions` states that the comparison produced zero open Items under the declared relation. That statement is limited by the relation and by the possible incompleteness of each set.
- `items`: The list of Items whose outcome is not matched. Each Item carries its outcome. Each excluded Item also carries the profile rule that excluded it. Patterns appear as digests, for the reasons in Section 5.2.
- `counts`: The number of Items in each outcome, including matched and excluded. An implementation MUST NOT count indeterminate Items into a proportion of coverage. A percentage over indeterminate Items makes exactly the too-strong claim that these outcome names exist to prevent.

The result carries matched as a count only, while it carries every other outcome as a list of Items. This difference is intended. The result digests both activity snapshots and the receipt set it compared. A reader who holds those inputs can compute the matched set again. The count is then a shortcut over material that the reader already has. That property fails in one named case. When the identifying material for the receipt set was read from the receipt set itself (Chapter 8), the reader computes the Issuer's own answer again. The digest then checks copying, and the matched count gets that same status.

The result statement is serialized and digested as in Chapter 3, signed by the Reconciler, and registered (Chapter 6). The Reconciler SHOULD be operationally independent of the Gateway. Where it is not, registration on a Transparency Service at least lets a third party see that the result exists and when it was made.

### 5.7. Semantics of the outcomes

An observed-without-receipt outcome states one thing: evidence is absent. Gateway bypass produces it. A failed receipt sink produces it. A wrong counter scope produces it. A Receipt that names the object but falls outside the Window on the two clocks also produced it. Section 5.5 moves that case into indeterminate. An earlier revision listed the mirror condition only under receipted-without-observation. This text names both directions so that the earlier omission stays visible. A result statement MUST NOT call such activity an intrusion, a breach, or an intended act, and a Consumer MUST NOT present it as such. The mechanism shows the condition. Finding the cause is investigation.

A receipted-without-observation outcome is also a statement about evidence. A counter reset at the Window boundary produces the same shape. So does an intermediate component that merges statements. So does a counter increase that falls outside the snapshot pair. A receipt that describes activity that did not happen produces it too. An implementation MAY treat this outcome as a failure condition under a policy of its own. The shape is the same in each of these cases, so the classification belongs to that policy.

An indeterminate outcome is a result. It MUST NOT be resolved by assumption in either direction. An implementation under pressure to produce a single number will want to count indeterminate into a coverage proportion. That operation destroys the one property that makes these outcome names different from a simple pass, and MUST NOT be performed.

Checking of receipt signatures and chain integrity happens before reconciliation, under the rules of the receipt format in use. Reconciliation compares an already-checked receipt set against source counters.

## 6. Registration on a Transparency Service

Both structures are payloads for Signed Statements in the sense of [RFC9943]. The Issuer signs the serialized structure. For Transformation Evidence the Issuer is the Gateway operator. For a Coverage Reconciliation result the Issuer is the Reconciler. The Issuer registers the Signed Statement on a Transparency Service. The SCITT Receipt is proof of inclusion, at a position, in an append-only log. A party other than the Issuer operates that log.

The layering is intended. The structures get their audit value from registration that the Issuer cannot change without detection. SCITT already defines that place, its trust model, and its verification. Digests in this document bind evidence to receipts over the payload, so the binding stays valid through registration.

## 7. Relationship to Coverage Attestation

Coverage attestation is a related layer. Each layer answers its own half of a two-part question.

Two different failures exist. A record can be intact and show nothing about what is missing. A report can be complete and show nothing about what it examined. The two failures are fixed in different places.

This document is about the first failure. It states what a Gateway recorded and what that record leaves open. Chain verification proves integrity of the retained entries only. The outcome names here let a record say so in its own terms.

The second failure belongs to coverage attestation. There, an examination declares the set of units it drew from. It names the basis for that set. It accounts for every unit it did not examine. Work on that layer is in progress on the SCITT list.

The two layers combine in one direction. A coverage attestation states what was examined. The structures here state what the Gateway recorded of it. An attestation over a Gateway-mediated examination carries over whatever the Gateway's record leaves open. It carries that over without a report, unless the record itself says so. That missing report is the failure that this document names. In the other direction, a complete access record over a set chosen after the results were known is an exact record of a question that was already decided.

One object answers half of a two-part question.

## 8. Security Considerations

**Same-operator collusion.** In many deployments one party operates both the Gateway and the Data Source. The mechanism's value against that party is reduced. An operator with administrative access to the source counters can turn the counters off or clear them. The invalid-window rule (Section 5.5) turns a reset into a visible failure. Registration (Chapter 6) makes removal of already-issued results detectable. But an operator who controls both records and never registers is outside this mechanism completely. Assurance against that operator requires a counter path that the operator cannot write to. That is a deployment property.

**Counter manipulation.** An attacker who can reset or lower source counters could otherwise hide activity between snapshots. The MUST-fail rule exists for this case: a Window that contains a counter that went down is reported as not reliable, as a whole. Snapshot frequency limits the exposure: with shorter Windows, a reset costs the attacker a visible failure sooner.

**The declared relation as an attack point.** The Gateway operator writes the Mapping Profile. The profile decides what counts as a match and what is excluded before matching. A wider count bound can absorb activity that has no Receipt. An added exclusion rule can remove that activity from comparison. Against that operator the mechanism has exactly one effect: it makes the declaration part of the evidence. The profile is versioned. Its digest is bound into the result. Exclusions are reported with count and rule. The result states that its bounds are operator-declared. A reader who trusts the result sees that dependency. Registration lets a third party see the sequence of declared profiles; a profile changed without registration would lose that visibility.

**Digest agility.** Digests are prefixed (Chapter 3), and an implementation MUST reject unknown prefixes. To accept an unknown prefix as an opaque match would let an attacker route around comparison.

**Signature and key compromise.** Signing and registration come from the SCITT layer. Key management, revocation, and the results of Issuer key compromise are governed at the SCITT layer. A compromised Issuer key removes the evidence value of statements under that key, as it does for any signed object.

### 8.1. Receipt set completeness and where the expected count comes from

A receipt set whose newest entries have been removed is internally consistent. Every remaining link checks. Every signature checks. The file does not state how many entries it should have contained. Reconciliation compares the receipt set against source counters, and an operator who can cut one can in general also stop the other. To detect the removal, a count, a head digest, or an equal quantity is necessary. That quantity must come from outside the cut file.

What matters to a Consumer is where that material comes from. Two constructions exist, and they differ in a way that a digest does not show.

An implementation may accept the expected quantity as a verifier input. The check is then only as reliable as that input. An auditor who holds only the receipt file has one source for that input: the Issuer, the party under examination. The verification is real, but its independence comes from whoever ran it.

An implementation may instead carry the quantity inside the signed material. The set then states its own size, which fixes the first problem. The cost should be stated: the Issuer signs a claim about a set that it has not finished producing. A per-entry counter limits only the entries that were kept, so a signed total over the whole set is also required. A running count derived from the sequence number next to it repeats the position of a present record. The useful property is a signed total over a held set.

This document permits both constructions. It requires that a reader of a result that identifies a receipt set can see which construction was used. A Consumer who cannot tell them apart will read an external count as if the receipt set had proved its own completeness. That is the strongest claim in this area, and the claim least often actually made.

## 9. Privacy Considerations

Every structure in this document follows one rule: evidence about protected data is built from class names, action names, counts, digests, and identifiers only.

Transformation Evidence carries class names, action names, and counts. Request and pattern references are digests, because query and pattern text can contain values and schema detail.

Class names and counts still show that a class was present, and in what quantity. Deployments that treat even that as sensitive can keep the payloads private and register only the digests. Third-party audit then requires permission.

## 10. IANA Considerations

This document requests registration of two media types and the creation of two registries. Registrations follow [RFC6838]. Registry policy is Specification Required as defined in [RFC8126].

### 10.1. Media type: application/transformation-evidence+json

Type name:  application

Subtype name:  transformation-evidence+json

Required parameters:  None.

Optional parameters:  None.

Encoding considerations:  8bit; binary UTF-8 JSON.  For digesting and signing, the payload is serialized with [RFC8785].

Security considerations:  See Chapter 8 and Section 4.3.  The payload MUST NOT carry data values.

Interoperability considerations:  Implementations that do not recognize the v member MUST reject the object.

Published specification:  This document, Section 4.2.

Applications that use this media type:  Policy gateways and auditors that record or verify a disclosure transformation.

Fragment identifier considerations:  None.

Additional information:  Deprecated alias names for this type: none.  Magic number(s): none.  File extension(s): none.  Macintosh file type code(s): none.

Person and email address to contact for further information:  See the Authors' Addresses section of this document.

Intended usage:  COMMON

Restrictions on usage:  None.

Author:  See the Authors' Addresses section of this document.

Change controller:  IETF

### 10.2. Media type: application/coverage-reconciliation+json

Type name:  application

Subtype name:  coverage-reconciliation+json

Required parameters:  None.

Optional parameters:  None.

Encoding considerations:  8bit; binary UTF-8 JSON.  For digesting and signing, the payload is serialized with [RFC8785].

Security considerations:  See Chapter 8 and Section 5.7.

Interoperability considerations:  A consumer MUST NOT read a coverage-reconciliation/1 result as a /2 result (Section 5.6).

Published specification:  This document, Section 5.6.

Applications that use this media type:  Reconcilers and auditors that compare source activity with a receipt set.

Fragment identifier considerations:  None.

Additional information:  Deprecated alias names for this type: none.  Magic number(s): none.  File extension(s): none.  Macintosh file type code(s): none.

Person and email address to contact for further information:  See the Authors' Addresses section of this document.

Intended usage:  COMMON

Restrictions on usage:  None.

Author:  See the Authors' Addresses section of this document.

Change controller:  IETF

### 10.3. Transformation Actions registry

IANA is asked to create a new registry titled "Transformation Actions" in a new "Disclosure Evidence" group.

Registration policy: Specification Required ([RFC8126]).

Registration template: Action name (unique ASCII token); description; reference.

Initial contents:

       +=============+============================+================+
       | Action name | Description                | Reference      |
       +=============+============================+================+
       | mask        | Replace a value with a     | This document, |
       |             | class-level placeholder    | Section 3.2    |
       +-------------+----------------------------+----------------+
       | redact      | Remove a value             | This document, |
       |             |                            | Section 3.2    |
       +-------------+----------------------------+----------------+
       | tokenize    | Replace a value with a     | This document, |
       |             | stable token               | Section 3.2    |
       +-------------+----------------------------+----------------+
       | truncate    | Shorten a value            | This document, |
       |             |                            | Section 3.2    |
       +-------------+----------------------------+----------------+
       | none        | The class occurred and was | This document, |
       |             | disclosed untransformed    | Section 3.2    |
       +-------------+----------------------------+----------------+

                                  Table 1

### 10.4. Coverage Reconciliation Outcomes registry

IANA is asked to create a new registry titled "Coverage Reconciliation Outcomes" in the same "Disclosure Evidence" group.

Registration policy: Specification Required ([RFC8126]).

Registration template: Outcome name (unique ASCII token); description; reference.

Initial contents:

   +===============================+=======================+===========+
   | Outcome name                  | Description           | Reference |
   +===============================+=======================+===========+
   | matched                       | The Item              | This      |
   |                               | corresponds to an     | document, |
   |                               | Item in the other     | Section   |
   |                               | population within     | 4.3       |
   |                               | the declared bounds   |           |
   +-------------------------------+-----------------------+-----------+
   | observed-without-receipt      | The Data Source       | This      |
   |                               | recorded activity     | document, |
   |                               | against a Data        | Section   |
   |                               | Object that no        | 4.3       |
   |                               | Receipt in the        |           |
   |                               | Window names          |           |
   +-------------------------------+-----------------------+-----------+
   | receipted-without-observation | A Receipt in the      | This      |
   |                               | Window names a Data   | document, |
   |                               | Object for which      | Section   |
   |                               | the Data Source       | 4.3       |
   |                               | recorded no           |           |
   |                               | activity              |           |
   +-------------------------------+-----------------------+-----------+
   | excluded                      | The Item was          | This      |
   |                               | removed from          | document, |
   |                               | comparison by a       | Section   |
   |                               | Mapping Profile       | 4.5       |
   |                               | rule                  |           |
   +-------------------------------+-----------------------+-----------+
   | indeterminate                 | The evidence or the   | This      |
   |                               | Mapping Profile       | document, |
   |                               | does not determine    | Section   |
   |                               | an outcome            | 4.3       |
   +-------------------------------+-----------------------+-----------+
   | invalid-window                | The Window is         | This      |
   |                               | unreliable (counter   | document, |
   |                               | regression or         | Section   |
   |                               | snapshot mismatch)    | 4.6       |
   +-------------------------------+-----------------------+-----------+

                                  Table 2

(Note: the Reference column above reproduces the source's section numbers; in this re-authored ordering they correspond to Sections 5.5, 5.4, and 5.6.)

## 11. Implementation Status

*This section is to be removed before publication as an RFC, per [RFC7942].*

One implementation of both mechanisms exists: the Conarium gateway (TypeScript, MIT license, `@conarium-ai/core` on npm). It has run at one site since July 2026. Its receipts carry masking counts for each class, as in Chapter 4. Its `conarium-reconcile` tool implements the procedure of Section 5.5 against PostgreSQL statement statistics. The tool is a single file with no dependency on the package. A third party can therefore run the tool without trust in the implementation under audit. Conformance test vectors ship with the package.

The state below was measured against the published 0.2.38 package, not read from its documentation. It is now checked on each run, not measured one time. Every revision of this section up to -04 described a tool that had moved past the description. Each time, the section claimed less than the code did. The correction is at the end of this section. The failure gives more information than the current state does.

As of 0.2.38 the tool produces the result statement of Section 5.6 as `coverage-reconciliation/2`, behind a flag of its own. The /1 body is unchanged and still carries `conarium-reconcile/0.1`. The /2 result carries `profile`, `bounds`, `outcome`, `items`, and `counts` under the names used here. The tool reads Mapping Profiles, including the three `clocks` fields.

The behaviour below was observed on one test input. The input is a Receipt that names the object, together with one infrastructure statement. The Receipt is stamped three seconds before a two-hour Window.

- With no profile, `profile` is null and all three entries in `bounds` are undeclared. Both Items are indeterminate. The data statement is indeterminate because no skew bound is declared. The infrastructure statement is indeterminate because no exclusion rule is declared. In the /2 result the tool applies no exclusion rule that is not in a profile, which is the requirement of Section 5.4. Its /1 output still reports such statements under a category of its own, decided by rules built into the tool. That output is not a result statement in the sense of Section 5.6 and does not claim to be one.
- With a profile that declares exclusions but no `clocks` member, the excluded Item carries the profile rule that removed it. `bounds.exclusion` is operator-declared, and `bounds.skew` stays undeclared.
- With `clocks.skew` declared larger than the offset, `bounds.skew` is operator-declared and the Item stays indeterminate. A declaration does not make a match.
- With `clocks.skew` declared smaller than the offset, the same Item becomes observed-without-receipt. The declared bound changes the comparison, not only the report.
- A skew bound declared both in a profile and on the command line fails unless the two parse to the same number of milliseconds. A `clocks` member with a fourth key fails, and the tool names the key it rejected.

One difference stays open. The tool's exit codes are older than these outcome names and are not a mapping of them. They were left unchanged on purpose. An exit code is a compatibility contract. To renumber the codes to match this document would break installations, and would only make a specification look implemented. One code was added, not renumbered, for the clock outcome. Existing callers do not notice it.

The problem that produced this section's own history is fixed. The -04 revision carried four statements. They were correct when written and false within days; each claimed less than the code did. No mechanism here found them: a reader who held the document next to the tool's output did. The -05 revision recorded that the test suite had no check against this section. It said to read the section as a claim about the date it was measured, until such a check existed.

A check now runs this section instead of reading it. Every behaviour statement above is bound to a run of the shipped tool. The test input is named in this document. The check enforces two directions. Every value that a run produced must appear in the sentence that states it. And the number of statements must equal the number of bound runs. A statement with no run is not measured. A run with no statement is a dropped measurement. The revision under test is derived from the repository, not written into the check. A revision written into the check would go stale in the same way that the check exists to catch.

The first thing the check caught was the sentence in the paragraph above. From the commit that added the check, -05's statement that no check existed was false. A posted draft cannot be edited, so this revision is where the correction has to live. The check's first finding was the sentence that claimed the check did not exist. That finding shows the failure the check was written for.

Two limits, stated here so that a reader does not have to find them. The check binds the behaviour statements, not the text around them; a paragraph can still go stale in a way that nothing runs. And a check failure has two correct resolutions: change the code back, or write the revision that says what the code now does. To edit a posted draft is not one of them. The cost of drift is then a document, not a code change.

A second check covers the conformance class, not this document. Every outcome that the result statement can carry has a test case that produces it. Each separate reason for indeterminate has a test case of its own. The check reads the list of outcomes from the tool's own result; the list is not written into the check. An outcome added to the set therefore arrives in the check without a reminder, and arrives failing, until some test case produces it. A conformance class can still lose coverage without a report. Nothing in a test set records what was removed from it. A class that has lost coverage still passes.

Two corrected claims are on record; both claimed too much. Earlier revisions of this document, and releases of the implementation up to 0.2.21, described a reconciliation with no open Items as "covered". That word claimed more than the procedure shows. It was corrected in the implementation in 0.2.22 and in this document in -03.

The clock rule added in -04 has the same history, in shorter form. The implementation admitted Receipts on an exact comparison across the two clocks. A Receipt three seconds outside a two-hour Window produced observed-without-receipt and a bypass message. That was raised in review of -03 on the SCITT mailing list, reproduced, and corrected in 0.2.27. The correction was then attacked. A Receipt from the day before named the same object. That moved a real in-Window absence into the new outcome, and the implementation offered the boundary as the explanation. A twenty-three-hour offset cannot support that explanation. Release 0.2.28 limits what the implementation is willing to offer as an explanation: the reporting choice in Section 5.3. Both defects were in the implementation first. Neither was found by reading this document. The first came from list review of -03. The second came from a review that attacked the implementation. The fix under review had widened a default. The author of that fix was not the party who should approve it. The tool's own output made the second finding possible to state; this text did not yet exist. The document's part was smaller and later. The document is where the correction has to be written down. Then the next implementation does not have to be attacked to learn the correction.

## 12. References

### 12.1. Normative References

- [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.
- [RFC6838]  Freed, N., Klensin, J., and T. Hansen, "Media Type Specifications and Registration Procedures", BCP 13, RFC 6838, January 2013.
- [RFC8126]  Cotton, M., Leiba, B., and T. Narten, "Guidelines for Writing an IANA Considerations Section in RFCs", BCP 26, RFC 8126, June 2017.
- [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, May 2017.
- [RFC8785]  Rundgren, A., Jordan, B., and S. Erdtman, "JSON Canonicalization Scheme (JCS)", RFC 8785, June 2020.
- [RFC9943]  Birkholz, H., Delignat-Lavaud, A., Fournet, C., Deshpande, Y., and S. Lasker, "An Architecture for Trustworthy and Transparent Digital Supply Chains", RFC 9943, June 2026.

### 12.2. Informative References

- [I-D.aylward-aiga-2]  Aylward, E. R., "AI Governance and Accountability Protocol (AIGA)", Work in Progress, draft-aylward-aiga-2-00, 26 January 2026.
- [I-D.chueayen-attestation-receipts]  Chueayen, A., "Enforcement Attestation Receipts for AI Inference Decisions", Work in Progress, draft-chueayen-attestation-receipts-02, 8 August 2026.
- [I-D.farley-acta-signed-receipts]  Farley, T., "Signed Decision Receipts for Machine-to-Machine Access Control", Work in Progress, draft-farley-acta-signed-receipts-02, 28 June 2026.
- [I-D.marques-asqav-compliance-receipts]  Marques, J. A. G., "Compliance Profile of Signed Action Receipts for AI Agents", Work in Progress, draft-marques-asqav-compliance-receipts-07, 20 July 2026.
- [RFC7942]  Sheffer, Y. and A. Farrel, "Improving Awareness of Running Code: The Implementation Status Section", BCP 205, RFC 7942, July 2016.
- [RFC8032]  Josefsson, S. and I. Liusvaara, "Edwards-Curve Digital Signature Algorithm (EdDSA)", RFC 8032, January 2017.
- [RFC9052]  Schaad, J., "CBOR Object Signing and Encryption (COSE): Structures and Process", STD 96, RFC 9052, August 2022.

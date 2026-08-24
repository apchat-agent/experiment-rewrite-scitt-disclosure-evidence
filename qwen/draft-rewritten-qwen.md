SCITT                                                        E. C. Doğru
Internet-Draft                           VERAX TEKNOLOJİ LİMİTED ŞİRKETİ
Intended status: Informational                            23 August 2026
Expires: 24 February 2027


 Transformation Evidence and Coverage Reconciliation for Auditable Data
                               Disclosure
                draft-dogru-scitt-disclosure-evidence-07

Audit receipts record what a gateway wrote about an access. They omit how data changed and whether every access left a receipt. This document defines two evidence payloads for those gaps. Transformation Evidence states which value classes were transformed, and how, without carrying values. Coverage Reconciliation compares source activity counters with a receipt set over a window. Each item is matched, observed without a receipt, receipted without an observation, excluded, or indeterminate. The result is not a bare pass. Both payloads register as Signed Statements on a SCITT Transparency Service.

Status of This Memo

   This Internet-Draft is submitted in full conformance with the
   provisions of BCP 78 and BCP 79.

   Internet-Drafts are working documents of the Internet Engineering
   Task Force (IETF).  Note that other groups may also distribute
   working documents as Internet-Drafts.  The list of current Internet-
   Drafts is at https://datatracker.ietf.org/drafts/current/.

   Internet-Drafts are draft documents valid for a maximum of six months
   and may be updated, replaced, or obsoleted by other documents at any
   time.  It is inappropriate to use Internet-Drafts as reference
   material or to cite them other than as "work in progress."

   This Internet-Draft will expire on 24 February 2027.

Copyright Notice

   Copyright (c) 2026 IETF Trust and the persons identified as the
   document authors.  All rights reserved.










   This document is subject to BCP 78 and the IETF Trust's Legal
   Provisions Relating to IETF Documents (https://trustee.ietf.org/
   license-info) in effect on the date of publication of this document.
   Please review these documents carefully, as they describe your rights
   and restrictions with respect to this document.  Code Components
   extracted from this document must include Revised BSD License text as
   described in Section 4.e of the Trust Legal Provisions and are
   provided without warranty as described in the Revised BSD License.

Table of Contents

   1.  Introduction  . . . . . . . . . . . . . . . . . . . . . . . .   3
     1.1.  Threat model and applicability  . . . . . . . . . . . . .   4
     1.2.  What these structures do not claim  . . . . . . . . . . .   4
     1.3.  Relationship to coverage attestation  . . . . . . . . . .   4
   2.  Conventions and Definitions . . . . . . . . . . . . . . . . .   5
   3.  Transformation Evidence . . . . . . . . . . . . . . . . . . .   7
     3.1.  Purpose . . . . . . . . . . . . . . . . . . . . . . . . .   7
     3.2.  Structure . . . . . . . . . . . . . . . . . . . . . . . .   7
     3.3.  Serialization and digests . . . . . . . . . . . . . . . .   8
     3.4.  What Transformation Evidence does not prove . . . . . . .   8
   4.  Coverage Reconciliation . . . . . . . . . . . . . . . . . . .   9
     4.1.  Purpose . . . . . . . . . . . . . . . . . . . . . . . . .   9
     4.2.  Activity snapshots  . . . . . . . . . . . . . . . . . . .   9
     4.3.  Reconciliation procedure  . . . . . . . . . . . . . . . .  10
     4.4.  Mapping profiles  . . . . . . . . . . . . . . . . . . . .  12
     4.5.  Exclusions  . . . . . . . . . . . . . . . . . . . . . . .  14
     4.6.  Result statement  . . . . . . . . . . . . . . . . . . . .  15
     4.7.  Semantics of the outcomes . . . . . . . . . . . . . . . .  17
   5.  Registration on a Transparency Service  . . . . . . . . . . .  18
   6.  Security Considerations . . . . . . . . . . . . . . . . . . .  18
     6.1.  Receipt set completeness and where the expected count comes
           from  . . . . . . . . . . . . . . . . . . . . . . . . . .  19
   7.  Privacy Considerations  . . . . . . . . . . . . . . . . . . .  20
   8.  IANA Considerations . . . . . . . . . . . . . . . . . . . . .  20
     8.1.  Media type: application/transformation-evidence+json  . .  20
     8.2.  Media type: application/coverage-reconciliation+json  . .  21
     8.3.  Transformation Actions registry . . . . . . . . . . . . .  22
     8.4.  Coverage Reconciliation Outcomes registry . . . . . . . .  22
   9.  Implementation Status . . . . . . . . . . . . . . . . . . . .  24
   10. References  . . . . . . . . . . . . . . . . . . . . . . . . .  26
     10.1.  Normative References . . . . . . . . . . . . . . . . . .  26
     10.2.  Informative References . . . . . . . . . . . . . . . . .  27
   Acknowledgments . . . . . . . . . . . . . . . . . . . . . . . . .  28
   Author's Address  . . . . . . . . . . . . . . . . . . . . . . . .  29

1.  Introduction

   Systems place a policy gateway between an automated client and a data source.
   Those systems emit signed, hash-chained access receipts.
   Several receipt formats exist [I-D.farley-acta-signed-receipts] [I-D.marques-asqav-compliance-receipts] [I-D.chueayen-attestation-receipts] [I-D.aylward-aiga-2].
   All of the formats share one limit: the party under audit selects the evidence.
   A receipt is produced by the gateway that performed the access.

   Two gaps follow from that property.

   First, receipts typically state that access happened.
   They name the policy decision.
   They do not say what happened to the data between the data source and the client.
   A gateway may mask, redact, or tokenize values before disclosure.
   That transformation is the privacy claim.
   A conventional receipt does not describe it.
   An auditor learns that a table was read.
   The auditor does not learn whether protected columns left the gateway transformed or in the clear.

   Second, a receipt set only covers accesses that produced receipts.
   A client that reaches the data source without the gateway produces no receipt.
   The receipt chain does not reveal this.
   Hash chains detect removal and reordering of records that exist.
   They do not show records that were never created.
   Completeness needs a second account of activity.
   That account comes from a party other than the gateway: the data source.

   This document defines two evidence structures for these gaps.

   *  Transformation Evidence (Section 3): a statement bound to one disclosure.
      It names which classes of values were transformed, by which action, and in what count.
      It never carries the values.

   *  Coverage Reconciliation (Section 4): a procedure and a signed result.
      It compares source activity snapshots at the window bounds with the receipt set for that window.
      It classifies each Item of either account.
      Neither population is assumed complete.
      The operator declares the correspondence (Section 4.4).
      The result names what was matched, observed without a receipt, receipted without an observation, excluded, or left undecided.

   Both structures are payloads.
   They are meant to be Signed Statements on a Transparency Service as in [RFC9943].
   SCITT supplies append-only, third-party-auditable registration.


   Other individual drafts record signed decisions about automated access.
   Farley [I-D.farley-acta-signed-receipts], Marques [I-D.marques-asqav-compliance-receipts], and Chueayen [I-D.chueayen-attestation-receipts] use Ed25519 [RFC8032] and JSON Canonicalization [RFC8785].
   Aylward [I-D.aylward-aiga-2] uses Ed25519 in a hybrid signature suite and does not specify JCS.
   None of those drafts defines Transformation Evidence or Coverage Reconciliation.

Section 6 states the full account.
This subsection states the bound before the procedure.
One party often runs the Gateway and the Data Source.
That party can suppress the source counters.
A counter reset MUST fail the Window (Section 4.3).
It MUST NOT yield a clean report.
The Gateway operator writes the Mapping Profile.
The profile can absorb unreceipted activity or exclude it.
Visibility is the defence: a digest-bound profile, reported exclusions, and a stated standing for each bound.
Digests reject unknown prefixes.
Issuer key compromise is a SCITT-layer problem.
A truncated receipt set still verifies internally.
Detecting the cut needs a quantity from outside that file (Section 6.1).

Transformation Evidence describes the disclosure surface. It does not claim a value is unlearnable. It is the Issuer's signed assertion that a transformation was applied, not proof that it was (Section 3.4). A Coverage Reconciliation result that reports activity without a receipt is a statement about absent evidence. It is not, and MUST NOT be presented as, proof of intent or of a breach (Section 4.7).

Neither structure reports a bare pass. A reconciliation against an operator-declared correspondence cannot be stronger than that declaration (Section 4.4). An undecided outcome is reported as undecided. It is not folded into a proportion.

A record can be intact and not show what is missing. A report can be complete and not show what it examined. These are two failures. They close in different places.

This document addresses the first failure. It states what a gateway recorded. It states what that record leaves open.  The vocabulary here lets a record state this in its own terms.

The second failure belongs to coverage attestation. An examination declares the population it drew from. It names the basis for that population. It accounts for every unit it did not examine. Work on that layer is under way on this list.

The two layers compose in one direction. They do not substitute for each other. A coverage attestation states what was examined. The structures here state what the mediator recorded of it. An attestation over a mediated examination inherits whatever the mediator's record leaves open. It inherits that gap silently unless the record states it. That silence is the failure this document names. The reverse direction offers no rescue. A complete access record over a population chosen after the results were known is an exact record of a decided question.

Neither layer rescues the other. One artefact answers half of a two-part question.

2.  Conventions and Definitions

   The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
   "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
   "OPTIONAL" in this document are to be interpreted as described in
   BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all
   capitals, as shown here.

   The terms below define the roles and objects in this document.

   Data Source:  The system that holds the data. It keeps its own count of query or access activity. A database statement statistic is one example.

   Gateway:  The component that mediates access between an automated client and a Data Source. It applies policy, transforms results, and emits receipts.

   Disclosure:  A single delivery of data from the Gateway to a client. The data may be transformed.

   Receipt:  A signed record of a Disclosure. The Gateway produces the Receipt.

   Protected Class:  A named category of values. Policy subjects these values to transformation. "email", "national-id", and "phone" are examples.

   Window:  A time interval for reconciliation. Two snapshots of the Data Source's activity counters bound the interval. The Data Source stamps both bounds. A Receipt falls inside the Window based on the Gateway's clock. Section 4.3 defines this check.

   Mapping Profile:  A versioned statement declared by the operator. It states the expected correspondence between one client-level operation and the data-source-level activity it produces. It includes the bound on that multiplicity. It names the clock source on each side and the skew bound between them. It lists the rules that exclude activity from comparison. A Mapping Profile declares a deployment state. The Gateway does not measure it. Section 4.4 details this.

   Item:  One unit the reconciliation procedure classifies. On the source side, an Item is one snapshot entry whose pattern counter increased in the Window. It is one pattern, not one (pattern, Data Object) pair. On the receipt side, an Item is one Receipt that names a Data Object the snapshots do not account for. Counting each (pattern, Data Object) pair as an Item changes the observed-without-receipt count.

   Data Object:  A named target of source activity or a Receipt. In the shipped reconciler, a Data Object is a table or equivalent schema object. It is not a column. The result records these as objects on an Item.

   Consumer:  A party that reads Transformation Evidence or a Coverage Reconciliation result. It presents the result to a human or another system. This document uses Consumer for that role.

   Reconciler:  The party that performs Coverage Reconciliation. It produces the result statement. This document uses Reconciler for that role.

   Protocol-defined:  A standing this document assigns to a bound. The invalid-window rule is one example. It is not a measurement.

   Measured:  A standing a bound has when observation of the deployment obtained it. It is not operator-declared.

   Client-level operation:  One Disclosure. It is one client request as seen by the Gateway.

   Source-level statement:  One increment of a Data Source activity counter. It is one snapshot entry for one pattern. It is not interchangeable with a Client-level operation.

   Gateway operator:  The party that operates the Gateway.

   Data Source operator:  The party that operates the Data Source. This document names the operator explicitly. Section 6 states the limit where both operators are the same party.

   Issuer:  The party that signs a Signed Statement, per [RFC9943]. For Transformation Evidence, the Gateway operator is the Issuer. For a Coverage Reconciliation result, the Reconciler is the Issuer.

   Verifier:  A party that checks a signature, a digest, or a Transparency Service receipt. This document uses the term once. It refers to independent checking of a disclosed result against the Issuer's Transformation Evidence assertion. Section 3.4 defines this check.

3.  Transformation Evidence

Transformation Evidence records, for one Disclosure, the Protected Classes transformed in the result, the action applied, and the count. The claim is a signed, registrable artifact.

3.2.  Structure

   Transformation Evidence is a JSON object with the following members:

   v:  Structure version string.  For this document: transformation-
      evidence/1.

   disclosure:  A digest binding this evidence to exactly one
      Disclosure, computed over the receipt for that Disclosure (or,
      where the receipt format defines a canonical record hash, that
      hash).  Digest form is defined in Section 3.3.

   request:  A digest of the request that produced the Disclosure.  The
      digest of the request, never the request text: query text can
      itself contain protected values.

   policy:  An object with id (an identifier of the policy version
      applied) and decision (the policy outcome under which disclosure
      proceeded).

   classes:  An array of objects, one per Protected Class that the
      applied policy recognizes and that occurred in the disclosed
      result, each with:

      class:  The Protected Class name, as named by the policy.

      action:  One of mask, redact, tokenize, truncate, or none.  The
         value none states that the class occurred and was disclosed
         untransformed — an honest statement some deployments need to
         make.

      count:  The number of values of this class in the disclosed result
         to which the action was applied.

   The structure MUST NOT carry data values, transformed or otherwise.
   Only class names, action names, counts, digests, and identifiers
   appear.  An implementation encountering a value in a field defined
   here MUST reject the structure.

The structure is serialized with the JSON Canonicalization Scheme [RFC8785] for digesting and signing. Digests in this document are SHA-256. They are written as strings prefixed with sha256: followed by lowercase hexadecimal. Future documents may register alternative digest prefixes; an implementation MUST reject a digest whose prefix it does not recognize rather than guessing. A CBOR/COSE serialization [RFC9052] of the same data model is expected after the JSON model receives review. The model does not depend on JSON.

Transformation Evidence describes the disclosure surface of one result. It does not state that a protected value is unlearnable by the client. Request languages can permit predicates over protected columns. An allowed request can then answer questions about a masked value. The value itself is never disclosed. A result-count of one versus zero is one bit. The evidence for such a Disclosure is still accurate. The value was transformed in the result. The client may still have learned something.

Consumers MUST NOT present Transformation Evidence as proof of non- exposure. The payload is a signed assertion by the Issuer that the transformation was applied. A Verifier may check the disclosed bytes against that assertion. Until then, the evidence is what the pinned Issuer asserted. Where the Issuer is the Gateway that performed the transformation, the assertion is self- attested. A Consumer who treats it as verified has dropped the Issuer from the trust statement. Nothing replaces that Issuer. A deployment that needs a class to be unlearnable must enforce that in policy. It can refuse the objects that carry the class. No evidence structure substitutes for that.

The classes array is bounded by what the applied policy recognizes. A value belonging to a class the policy does not name is not counted. The absence of a class from the array is therefore a statement about the policy's vocabulary as much as about the data, and MUST be read that way.

4.  Coverage Reconciliation

Coverage Reconciliation answers one question for a Window: did the Data Source's accounting record activity for which no Receipt exists?
The mechanism makes bypassed gateways and failed receipt sinks detectable.
The two accounts originate from different components.
The receipt set comes from the Gateway.
The activity counters come from the Data Source.
A Gateway cannot remove bypassed activity from an account it does not produce.
If one operator runs both components, the separation is administrative.
Section 6 states the same-operator limit.

4.2.  Activity snapshots

   A snapshot is a JSON object. It records the Data Source's cumulative activity counters at a point in time:

   v:  Snapshot version string.  For this document: activity-snapshot/1.

   ts:  The time the snapshot was taken (ISO 8601).

   source:  An identifier of the Data Source and the accounting scope within it (for example, the database role whose activity is counted).  Both snapshots of a Window MUST carry the same source; a mismatch invalidates the Window.

   entries:  An array of objects, one per activity pattern the source's accounting distinguishes, each with:

      pattern:  A digest of the normalized activity pattern (for example, a normalized statement with constants removed).  The digest, not necessarily the text: pattern text can embed protected values and schema detail.  Deployments MAY retain pattern text privately for diagnosis; only the digest is required here.

      count:  The cumulative counter value for this pattern at ts.

4.3.  Reconciliation procedure

   A reconciler uses a start snapshot, an end snapshot, and the receipt set for the Window.

   Window validity is checked first.  The two snapshots MUST carry the same v and source, the end ts MUST be later than the start ts, and no pattern's counter may be lower at the end than at the start.  A counter regression means the source's accounting was reset or altered inside the Window; the Window is then unreliable, and the reconciler MUST report failure for the Window as a whole rather than reconciling the surviving patterns.  A counter reset produces an error, not a clean report.  Section 6 explains why a reset fails the Window.

   Window membership is a bound.  Two clocks decide it.  The Data Source takes the snapshot timestamps.  The Gateway writes the Receipt timestamp.  An exact comparison fails in one direction.  A Gateway clock that trails the Data Source moves a Receipt out of the Window.  The object that Receipt names then looks like activity with no Receipt.  That outcome names gateway bypass (Section 4.7).  A clock difference of seconds can produce the accusation.  No real gap is required.  The measured case was three seconds (Section 9).  The procedure sets no floor.  A smaller offset is harder for a reader to suspect.  The Mapping Profile states the skew bound (Section 4.4).

   A Mapping Profile declares the clock source on each side and the skew bound between them.  It also declares multiplicity (Section 4.4).  The profile digest covers both.  Where the bound is undeclared, the rule below applies.  The affected items are indeterminate rather than absent evidence.  Where it is declared and a Receipt falls further outside the Window than the bound allows, the boundary does not explain it: the item takes the outcome it would have had, and a reconciler MUST report which bound it applied to reach that.

   For each pattern whose counter increased during the Window, the reconciler attributes the pattern to the data objects it touches.  It checks whether any Receipt in the Window names those objects.  Matching is per pattern and per data object, not per call count: one client-level request may legitimately produce more than one source- level statement, so call counts and receipt counts MUST NOT be compared one-to-one.  A pattern whose target objects cannot be determined MUST NOT be silently ignored; it receives the indeterminate outcome below.

   The comparison is between two populations: source-level activity and Receipts.  Neither population is assumed complete.  Each Item in either population receives exactly one of the following outcomes.  The result statement names these outcomes as fields (Section 4.6):

   matched:  The item corresponds to an item in the other population within the bounds of the applicable Mapping Profile (Section 4.4), and within the Window.  The profile's two kinds of bound do not act alike here: a multiplicity bound admits items to this outcome, and the skew bound does not.  A Receipt outside the Window is never matched, however small the declared skew — the bound qualifies how far the boundary can be trusted, not where the boundary is.

   observed-without-receipt:  The Data Source recorded activity against an object that no Receipt in the Window names.

   receipted-without-observation:  A Receipt in the Window names an object for which the data source's counters record no activity.

   excluded:  The item was removed from comparison before matching by a rule stated in the Mapping Profile (Section 4.5).

   indeterminate:  The evidence or the Mapping Profile does not determine an outcome — the pattern's objects could not be attributed, a required multiplicity or skew bound is undeclared, the item's only naming Receipt falls outside the Window, or the Window's evidence is insufficient to decide.

   An implementation MUST NOT report an item as matched when the outcome is indeterminate; the absence of a decision is not a decision.  Where a Mapping Profile does not declare the multiplicity bound that the comparison requires, the affected items are indeterminate and not clean coverage.

   The same rule binds the temporal bound, in the opposite direction.  Where every object an item leaves unaccounted for is named by a Receipt that falls outside the Window, the item is indeterminate, and an implementation MUST NOT report it as observed-without-receipt.  A reconciler cannot distinguish a Gateway clock that trails the Data Source from a Receipt written late.  Reporting absent evidence asserts a distinction it did not make.  An item that leaves even one object named by no Receipt at all is not affected by this rule.  That is a genuine absence.  A neighbouring object's clock does not make it undecidable.

   indeterminate here is not a weaker pass.  The comparison did not come out clean, and a result statement MUST carry the outcome and the offset that produced it.  The implementation may not state the cause.

   A reconciliation with no observed-without-receipt items establishes that each observed source-level item is attributable to a Receipt naming the same object, under the declared correspondence.  It does not establish that every source-level statement was itself receipted, and a result MUST NOT be stated in terms that assert it.  Where one Receipt naming an object clears an unbounded number of further statements against that object inside the Window, the procedure has established object attribution and nothing stronger.

4.4.  Mapping profiles

   One Client-level operation may produce several Source-level statements.
   The deployment produces this multiplicity. A pooler or an object-relational
   mapper can produce it. A Gateway cannot measure a correspondence it does
   not produce.

   The operator declares a Mapping Profile. For each Client-level operation,
   the profile states the expected source-level patterns. It states the
   multiplicity bound. It states the exclusion rules (Section 4.5). It
   carries a version identifier. It is serialized and digested as in
   Section 3.3.

   The profile declares the temporal correspondence. The operator knows this
   correspondence. The Gateway cannot measure it. The profile names the clock
   on each side. The Data Source stamps snapshots. The Gateway stamps
   Receipts. The profile states the skew bound between them. Both are
   operator statements. A claim that both sides read one clock, so the bound
   is zero, is still a declaration. One clock read twice is not read at the
   same instant. Whether the residue matters is a judgement about the
   deployment. The rule below forbids presenting that as measured. This
   document also refuses a third case: zero because nobody looked, declared
   by nobody, and read as agreement.

   The temporal correspondence is declared in three fields under a clocks
   member. The encoding is given so another specification can adopt the same
   shape:

   clocks.observation:  String.  An identifier for the clock that stamps
      the activity snapshots — the Data Source side.

   clocks.receipt:  String.  An identifier for the clock that stamps
      Receipts — the Gateway side.

   clocks.skew:  Duration.  The bound on how far those two clocks may
      differ.  A duration is a decimal integer with a unit suffix of ms,
      s, m, or h, or a bare decimal integer read as milliseconds: 500ms,
      5s, 2m, 1h, 5000.  A duration that does not parse is an error, not
      a default.

   An implementation MUST reject a clocks member carrying any key other than these three, and SHOULD name the key it rejected.
   A silently ignored fourth field declares less than its author believes.
   The gap shows up as an outcome the operator cannot account for.

   A declaration that both sides read one clock writes all three fields:
   the two identifiers may be the same string, and skew may be 0ms. A
   declared zero is a statement someone is accountable for; an assumed
   zero is the condition the rule below forbids.

   Where the skew bound is declared twice — in the profile and through an interface of the reconciler's own — an implementation MUST NOT select between them.
   Two declarations that parse to the same number of milliseconds are one
   declaration and proceed.
   Two that do not are an operator error and MUST fail, because which declaration prevailed would not be visible on the result, and a bound whose origin cannot be read from the result is not usefully declared at all.

   A reconciliation result computed against a Mapping Profile MUST bind that profile's digest, and MUST state, for each bound it relies on, whether the bound is protocol-defined, measured, operator-declared, or undeclared.
   A result MUST NOT present an operator-declared bound as a measured one.

   The consequence is a ceiling. A coverage outcome against a declared
   correspondence cannot be stronger than the declaration. Where the
   declaration is an operator statement, the outcome inherits that
   standing. The result statement must show it. The same discipline
   applies to absent evidence in Section 4.7. A declaration presented
   as a measurement is an overclaim. Truth of the declaration does not
   change that.

   Where a required multiplicity bound is undeclared, the affected items
   are indeterminate (Section 4.3).
   An implementation MUST NOT substitute a default bound of one; a one-to-one rule reports false observed-without-receipt items on any deployment with a pooler in front of the Data Source, and a silent default would make that error look like a finding.

   An undeclared skew bound is treated the same way, and for the same
   reason.
   An implementation MUST NOT substitute a default of zero: zero asserts that the two clocks agree, which is the assumption that produces the false accusation this document now guards against.
   It MUST NOT substitute a bound of its own choosing either, which would decide the operator's question with a number the operator never saw.
   Absent the declaration, items whose only naming Receipt sits outside
   the Window are indeterminate and the result reports the offset.  The
   reader compares that offset with clocks the reader knows.  The
   Reconciler does not.

   An implementation MAY, absent a declared bound, decline to offer the boundary as the explanation for an offset larger than the Window itself, on the ground that a boundary artefact cannot exceed the interval it bounds.
   This is a reporting choice about what an implementation is willing to
   suggest, not a change of outcome: the item is indeterminate either
   way. The twenty-three hour case that motivated this choice is in
   Section 9.

Exclusion differs from the other outcomes in kind. matched, observed-without-receipt, receipted-without-observation, and indeterminate are produced by the comparison. excluded is a decision taken before it. It decides what will be compared at all. A reconciliation can be made to come out clean through this outcome. The rules below make each exclusion visible in the result.

Exclusion rules MUST be stated in the Mapping Profile and are therefore covered by its digest. A result statement MUST report the count of excluded items and the rule that excluded each of them. An implementation MUST NOT exclude items by a rule that is not in the profile.

Without these constraints a clean result and a result cleaned by exclusion look the same. The digest that pins what was compared then misses the step that decided what was compared. Session or catalog housekeeping is a legitimate exclusion. Exclusions need not be rare. They must be visible and pinned.

Pinning is easy to read as more than it is. The rule identifier makes the exclusion reproducible. A reader sees which rule removed each Item. The reader can check that the rule was in the profile the digest covers. That does not establish that the exclusion was correct. A housekeeping rule and a rule that hides the auditor's target pin the same way. They verify the same way. The mechanism reproduces the decision. It does not judge it. Consumers MUST NOT read a pinned exclusion as a justified one, and a result statement MUST NOT present the digest as evidence that the exclusions were appropriate. The same distinction holds between a declared bound and a measured one (Section 4.4). Here it applies to what is compared at all.

4.6.  Result statement

   The reconciliation result is a JSON object:

   v:  coverage-reconciliation/2.  The outcome vocabulary of coverage-
      reconciliation/1 is not a subset of this one: a /1 result
      reporting covered asserts more than the procedure establishes, and
      is not re-expressible here.  A consumer MUST NOT read a /1 result
      as a /2 result.

   window:  Object with start and end (the two snapshot ts values).

   source:  The common source identifier of the two snapshots.

   snapshots:  Object with start and end digests of the two snapshot
      structures.

   receipts:  A digest identifying the receipt set that was compared
      (for chained receipt formats, the chain head digest and the
      sequence range are RECOMMENDED as the identifying material).

      A result SHOULD state whether that identifying material was
      obtained independently of the Issuer or read from the receipt set
      itself.  The two are not equivalent evidence, and a Consumer
      cannot tell them apart from the digest (Section 6.1).

   profile:  The digest and version identifier of the Mapping Profile
      the comparison was computed against (Section 4.4), or null when
      none was declared.  When null, every item whose outcome depends on
      a multiplicity bound is indeterminate, and so is every item whose
      only naming Receipt falls outside the Window: with no profile
      there is no declared skew bound either.

   bounds:  For each bound the comparison relied on, its source:
      protocol-defined, measured, operator-declared, or undeclared.  A
      result whose bounds are operator-declared states an outcome of
      that standing, no stronger.

   outcome:  invalid-window when the Window is unreliable (Section 4.3);
      otherwise no-exceptions when every item is matched or excluded,
      and exceptions when any item is observed-without-receipt,
      receipted-without-observation, or indeterminate.

      The name states what the comparison left open, not what it proved.
      A result MUST NOT carry an outcome name that asserts coverage of
      the source activity, and no-exceptions is not such an assertion:
      it says the comparison produced no open item under the declared
      correspondence, which is bounded by that correspondence
      (Section 4.4) and by the fact that neither population is assumed
      complete.

   items:  The list of items whose outcome is not matched, each with its
      outcome and, for excluded, the profile rule that excluded it.
      Pattern digests, not pattern text, for the reasons in Section 4.2.

   counts:  The number of items in each outcome, including matched and
      excluded.  An implementation MUST NOT aggregate indeterminate
      items into a proportion of coverage: an outcome that does not
      decide cannot be averaged into one that does, and reporting it as a
      percentage restores precisely the overclaim this vocabulary
      exists to prevent.

      A result carries matched as a count while carrying every other
      outcome as an accounting.  A count a reader cannot reconstruct is
      an assertion about a population the producer alone can see.  This
      count is not that: the result digests both activity snapshots and
      the receipt set it compared (Section 4.2, Section 3.3).  A reader
      holding those inputs recomputes the matched set.  The size is not
      an assertion.  The count is a convenience over material the reader
      already has.

      That property fails in one named case.  The identifying material
      for the receipt set may be read from the receipt set itself
      (Section 6.1).  A reader then recomputes the Issuer's answer.  The
      digest checks transcription, not completeness.  The matched count
      inherits that standing.

   The result statement is serialized and digested as in Section 3.3 and
   is intended to be signed by the reconciling party and registered
   (Section 5).  The reconciler SHOULD be operationally independent of
   the Gateway; where it is not, registration on a Transparency Service
   at least makes the result's existence and timing third-party-visible.

4.7.  Semantics of the outcomes

   An observed-without-receipt outcome states that evidence is absent.
   It does not state why. Gateway bypass produces it. Receipt sink
   failure produces it. Accounting scope mismatch produces it. A
   Receipt that names the object but falls outside the Window on the two
   clocks also produced it. Section 4.3 therefore removes that case
   from this outcome. An earlier revision listed the mirror condition
   under receipted-without-observation only. This text names both
   directions so the omission is visible. A result statement MUST NOT
   label such activity as an intrusion, a breach, or an intentional act,
   and consumers MUST NOT present it as such. The mechanism surfaces
   the condition. Cause is investigation, not reconciliation.

   A receipted-without-observation outcome is likewise a statement about
   evidence. It is not by itself a fault. A counter reset at the
   Window boundary produces the same shape. So does a gateway that collapses statements. So does an increment outside the snapshot
   pair. A receipt that describes activity that did not occur produces
   it too. An implementation MAY treat it as a failure condition under
   a policy of its own; this document does not define it as one, because
   the shape does not distinguish the cases.

   An indeterminate outcome is a result, not a degraded pass. It MUST
   NOT be resolved by assumption in either direction: neither counted as
   matched because nothing contradicts it, nor reported as missing
   activity because nothing confirms it. An implementation under
   pressure to produce a single number will be tempted to fold
   indeterminate into a coverage proportion; that operation destroys the
   only property that distinguishes this vocabulary from a bare pass,
   and MUST NOT be performed.

    Reconciliation compares an
   already-verified receipt set against source accounting; it does not
   re-verify.

Both structures defined here are payloads for Signed Statements in the sense of [RFC9943]. The Issuer signs the serialized structure. For Transformation Evidence, that Issuer is the Gateway operator. For a Coverage Reconciliation result, that Issuer is the Reconciler. The Issuer registers the Signed Statement on a Transparency Service. The SCITT Receipt is proof of inclusion, at a position, in an append-only log. That log is operated by a party other than the Issuer.

The structures gain their audit value from registration the Issuer cannot quietly rewrite. SCITT already defines that place, its trust model, and its verification. Digests in this document bind evidence to receipts over the payload. The binding survives registration. It is not over the envelope.

6.  Security Considerations

   Same-operator collusion.  The Gateway and the Data Source often share one operator.  That operator can suppress source counters.  The invalid-window rule (Section 4.3) reports a reset as a failure.  Registration (Section 5) detects suppression of issued results.  An operator who controls both accounts and never registers is outside this mechanism.  Assurance against that operator requires an accounting path the operator cannot write to.  That is a deployment property, not a payload property.

   Counter manipulation.  An attacker who resets or rewinds source counters can hide activity between snapshots.  The MUST-fail rule exists for this case: a Window containing a regression is reported unreliable in its entirety.  Snapshot frequency bounds the exposure.  Shorter Windows make a reset visible sooner.

   Declared correspondence as an attack surface.  The operator writes the Mapping Profile (Section 4.4).  It defines what counts as a match.  It defines what is excluded before matching.  A wider multiplicity bound absorbs unreceipted activity.  An added exclusion rule removes activity from comparison.  No computation against a declaration defends against that operator.  The mechanism makes the declaration part of the evidence.  The profile is versioned.  Its digest is bound into the result.  Exclusions are reported with count and rule.  The result states that its bounds are operator-declared.  A reader who trusts the result sees that dependency.  Registration (Section 5) makes the sequence of declared profiles third-party-visible.  A silently edited profile loses that visibility.

   Digest agility.  Digests are prefixed (Section 3.3); an implementation MUST reject unknown prefixes.  Accepting an unknown prefix as an opaque match lets an attacker route around comparison.

   Signature and key compromise.  Signing and registration are inherited from the SCITT layer.    A compromised Issuer key voids the evidentiary value of statements under that key.

6.1.  Receipt set completeness and where the expected count comes from

   A receipt set with removed recent entries remains internally consistent.
   Every remaining link verifies.
   Every signature checks.
   The file does not state the expected entry count.
   Reconciliation does not close this gap.
   It compares the receipt set against source accounting.
   An operator who can truncate one can generally suppress the other.
   Detecting the removal needs a count, a head digest, or an equivalent quantity.
   That quantity must not come from the truncated file.

   What matters to a Consumer is where that material arrives from.
   The two constructions differ in a way a digest does not reveal.

   An implementation may accept the expected quantity as a verifier input.
   The check is then only as trustworthy as that input.
   An auditor who holds only the receipt file has no source for it except the Issuer.
   That is the party under examination.
   The verification is real.
   Its independence is supplied by whoever ran it.
   It is not a property of the artifacts.

   An implementation may instead carry the quantity inside the signed material.
   The set then testifies to its own extent.
   That closes the first gap.
   The Issuer is signing an assertion about a population it has not finished producing.
   A per-entry counter constrains only the entries that were kept.
   A sealed total is also required.
   A running count derived from the sequence number it accompanies adds no information.
   It restates the position of a present record.
   It says nothing about an absent one.
   The useful property is a sealed quantity over a held set.
   It is not a per-record decoration.

   This document requires neither construction.
   It requires that a result identifying a receipt set be readable as to which one it used.
   A Consumer who cannot tell them apart will read an external pin as if the receipt set had proved its own completeness.
   That is the strongest claim in this area.
   It is the one least often actually made.

7.  Privacy Considerations

   Every structure in this document follows one rule.  Evidence about protected data must not itself become a disclosure channel.
   Transformation Evidence contains class names, action names, and counts.
   It does not contain values.
   Request and pattern references are digests.
   Query and pattern text can contain values and schema detail.
   Class names and counts show that a class was present and its quantity.
   Deployments that treat that information as sensitive can keep the payloads private.
   They can register only the digests.
   Third-party audit then becomes a permissioned act.

This document requests registration of two media types and the creation of two registries.
Registrations follow [RFC6838].
Registry policy is Specification Required as defined in [RFC8126].

8.1.  Media type: application/transformation-evidence+json

   Type name:  application

   Subtype name:  transformation-evidence+json

   Required parameters:  None.

   Optional parameters:  None.

   Encoding considerations:  8bit; binary UTF-8 JSON.  The payload uses
      [RFC8785] serialization for digesting and signing.

   Security considerations:  See Section 6 and Section 3.4.  The payload
      MUST NOT carry data values.

   Interoperability considerations:  Implementations that do not recognize the v member MUST reject the object.

   Published specification:  This document, Section 3.2.

   Applications that use this media type:  Policy gateways and auditors
      that record or verify a disclosure transformation.

   Fragment identifier considerations:  None.

   Additional information:  Deprecated alias names for this type: none.
      Magic number(s): none.  File extension(s): none.  Macintosh file
      type code(s): none.

   Person and email address to contact for further information:  See the
      Authors' Addresses section of this document.

   Intended usage:  COMMON

   Restrictions on usage:  None.

   Author:  See the Authors' Addresses section of this document.

   Change controller:  IETF

8.2.  Media type: application/coverage-reconciliation+json

   Type name:  application

   Subtype name:  coverage-reconciliation+json

   Required parameters:  None.

   Optional parameters:  None.

   Encoding considerations:  8bit; binary UTF-8 JSON.  The payload uses
      [RFC8785] serialization for digesting and signing.

   Security considerations:  See Section 6 and Section 4.7.

   Interoperability considerations: A consumer MUST NOT read a coverage-reconciliation/1 result as a /2 result (Section 4.6).

   Published specification:  This document, Section 4.6.

   Applications that use this media type:  Reconcilers and auditors that
      compare source activity with a receipt set.

   Fragment identifier considerations:  None.

   Additional information:  Deprecated alias names for this type: none.
      Magic number(s): none.  File extension(s): none.  Macintosh file
      type code(s): none.

   Person and email address to contact for further information:  See the
      Authors' Addresses section of this document.

   Intended usage:  COMMON

   Restrictions on usage:  None.

   Author:  See the Authors' Addresses section of this document.

   Change controller:  IETF

IANA creates a new registry titled "Transformation Actions" in a new "Disclosure Evidence" group.

Registration policy:  Specification Required ([RFC8126]).

Registration template:  Action name (unique ASCII token); description; reference.

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

IANA is asked to create a new registry titled "Coverage Reconciliation Outcomes" in the same "Disclosure Evidence" group.

Registration policy:  Specification Required ([RFC8126]).

Registration template:  Outcome name (unique ASCII token); description; reference.

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

9.  Implementation Status

   _This section is to be removed before publication as an RFC, per
   [RFC7942]._

   One implementation of both mechanisms exists: the Conarium gateway
   (TypeScript, MIT license, @conarium-ai/core on npm).  It has run at
   one site since July 2026.  Its receipts carry per-class masking
   counts as in Section 3.  Its conarium-reconcile tool implements
   Section 4.3 against PostgreSQL statement statistics.  The tool is a
   single file.  It has no dependency on the package.  A third party can
   run it without trusting the implementation under audit.  Conformance
   test vectors ship with the package.

   The state below was measured against the published 0.2.38 package.
   It was not read from the package documentation.  It is now checked,
   not measured once.  Every revision of this section up to -04
   described a tool that had moved past it.  Each time it claimed less
   than the code did.  The correction is at the end of this section.
   The failure is more instructive than the current state.

   As of 0.2.38 the tool emits the result statement of Section 4.6 as
   coverage-reconciliation/2, on a flag of its own.  The /1 body is
   unchanged and still carries conarium-reconcile/0.1.  The /2 result
   carries profile, bounds, outcome, items, and counts under the names
   used here.  It reads Mapping Profiles (Section 4.4), including the
   three clocks fields.

   The behaviour below was observed on one fixture: a Receipt naming the
   object, timestamped three seconds before a two-hour Window, together
   with one infrastructure statement.

   *  With no profile, profile is null, all three entries in bounds are
      undeclared, and both items are indeterminate — the data statement
      for want of a declared skew bound, the infrastructure statement
      for want of a declared exclusion rule.  In the /2 result the tool
      applies no exclusion rule that is not in a profile, which is the
      requirement of Section 4.5.  Its /1 output still reports such
      statements under a category of its own, decided by rules built
      into the tool; that output is not a result statement in the sense
      of Section 4.6 and does not claim to be.

   *  With a profile declaring exclusions but no clocks member, the
      excluded item carries the profile rule that removed it,
      bounds.exclusion is operator-declared, and bounds.skew remains
      undeclared.

   *  With clocks.skew declared larger than the offset, bounds.skew is
      operator-declared and the item remains indeterminate.  A
      declaration does not manufacture a match.

   *  With clocks.skew declared smaller than the offset, the same item
      becomes observed-without-receipt.  The declared bound reaches the
      comparison and not only the report.

   *  A skew bound declared both in a profile and through the command
      line fails unless the two parse to the same number of
      milliseconds; a clocks member carrying a fourth key fails and
      names the key it rejected.

   One gap remains.  The tool's exit codes predate this vocabulary.
   They are not a mapping of it.  They were left unchanged on purpose.
   An exit code is a compatibility contract.  Renumbering them to match
   this document would break installations.  That would make a
   specification look implemented.  One code was added rather than
   renumbered.  It is for the temporal outcome.  Existing callers do not
   notice it.

   The gap that produced this section's own history is closed.  The -04
   revision carried four statements.  They were accurate when written.
   They were false within days.  Each claimed less than the code did.
   No mechanism here found them.  A reader holding the document beside
   the tool's output did.  The -05 revision recorded that the test suite
   had no check against this section.  Until such a check existed, it
   said, read the section as a claim about the date it was measured.

   A check now runs this section instead of reading it.  Every
   behavioural statement above is bound to a run of the shipped tool.
   The fixture is named in this document.  Two directions are enforced.
   Every value a run produced must appear in the sentence that states
   it.  The number of statements must equal the number of bound runs.  A
   statement with no run is unmeasured.  A run with no statement is a
   dropped measurement.  The revision under test is derived from the
   repository.  It is not named in the check.  A hard-coded revision is
   the same class of stale declaration the check exists to catch.

   The first thing it caught was the sentence in the paragraph above.
   From the commit that added the check, -05's account of its own
   absence was false.  A posted draft cannot be edited.  This revision
   is where the correction has to live.  A check whose first finding is
   the sentence claiming it does not exist has shown the failure mode it
   was written for.

   Two limits, stated rather than left to be found.  The check pins the
   behaviour statements.  It does not pin the prose around them.  A
   paragraph can still go stale in a way nothing runs.  A failure has
   two honest resolutions.  Change the code back.  Or write the revision
   that says what the code now does.  Editing a posted draft is not one
   of them.  The cost of drift is then a document, not a diff.

   A second check covers the conformance class rather than this
   document.  Every outcome the result statement can carry has a case
   that produces it.  Each independent ground for indeterminate has a
   case of its own.  The list of outcomes is read from the tool's own
   result.  It is not restated in the check.  An outcome added to the
   vocabulary arrives there without a reminder.  It arrives failing
   until some case produces it.  A conformance class can lose coverage
   in silence.  Nothing in a test set records what was removed from it.
   A class that has lost coverage still passes.

   Earlier revisions of this document, and releases of that
   implementation up to 0.2.21, described a clean reconciliation as
   "covered".  That word asserted more than the procedure establishes.
   It was corrected in the implementation in 0.2.22 and in this document
   in -03.

   The temporal rule added in -04 has the same history, compressed.  The
   implementation admitted Receipts on an exact comparison across the
   two clocks.  A Receipt three seconds outside a two-hour Window
   produced observed-without-receipt and a bypass message.  That was
   raised in review of -03 on the SCITT mailing list.  It was
   reproduced.  It was corrected in 0.2.27.  The correction was then
   attacked.  A Receipt from the previous day named the same object.  It
   moved a real in-Window absence into the new outcome.  The
   implementation offered the boundary as its explanation.  A twenty-
   three hour offset cannot support that. 0.2.28 bounds what the
   implementation is willing to suggest.  That is the reporting choice
   in Section 4.4.  Both defects were in the implementation first.
   Neither was found by reading this document.  The first came from
   review of -03 on the list.  The second came from an adversarial
   review of the implementation.  The fix had loosened a default.  Its
   author was not the party who should clear it.  What made the second
   sentence sayable was the tool's own output.  This text did not yet
   exist.  The document's part was smaller and later.  It is where the
   correction has to be written down.  The next implementation should
   not have to be attacked to learn it.

10.  References

10.1.  Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119,
              DOI 10.17487/RFC2119, March 1997,
              <https://www.rfc-editor.org/rfc/rfc2119>.

   [RFC6838]  Freed, N., Klensin, J., and T. Hansen, "Media Type
              Specifications and Registration Procedures", BCP 13,
              RFC 6838, DOI 10.17487/RFC6838, January 2013,
              <https://www.rfc-editor.org/rfc/rfc6838>.

   [RFC8126]  Cotton, M., Leiba, B., and T. Narten, "Guidelines for
              Writing an IANA Considerations Section in RFCs", BCP 26,
              RFC 8126, DOI 10.17487/RFC8126, June 2017,
              <https://www.rfc-editor.org/rfc/rfc8126>.

   [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC
              2119 Key Words", BCP 14, RFC 8174, DOI 10.17487/RFC8174,
              May 2017, <https://www.rfc-editor.org/rfc/rfc8174>.

   [RFC8785]  Rundgren, A., Jordan, B., and S. Erdtman, "JSON
              Canonicalization Scheme (JCS)", RFC 8785,
              DOI 10.17487/RFC8785, June 2020,
              <https://www.rfc-editor.org/rfc/rfc8785>.

   [RFC9943]  Birkholz, H., Delignat-Lavaud, A., Fournet, C., Deshpande,
              Y., and S. Lasker, "An Architecture for Trustworthy and
              Transparent Digital Supply Chains", RFC 9943,
              DOI 10.17487/RFC9943, June 2026,
              <https://www.rfc-editor.org/rfc/rfc9943>.

10.2.  Informative References

   [I-D.aylward-aiga-2]
              Aylward, E. R., "AI Governance and Accountability Protocol
              (AIGA)", Work in Progress, Internet-Draft, draft-aylward-
              aiga-2-00, 26 January 2026,
              <https://datatracker.ietf.org/doc/html/draft-aylward-aiga-
              2-00>.

   [I-D.chueayen-attestation-receipts]
              Chueayen, A., "Enforcement Attestation Receipts for AI
              Inference Decisions", Work in Progress, Internet-Draft,
              draft-chueayen-attestation-receipts-02, 8 August 2026,
              <https://datatracker.ietf.org/doc/html/draft-chueayen-
              attestation-receipts-02>.

   [I-D.farley-acta-signed-receipts]
              Farley, T., "Signed Decision Receipts for Machine-to-
              Machine Access Control", Work in Progress, Internet-Draft,
              draft-farley-acta-signed-receipts-02, 28 June 2026,
              <https://datatracker.ietf.org/doc/html/draft-farley-acta-
              signed-receipts-02>.

   [I-D.marques-asqav-compliance-receipts]
              Marques, J. A. G., "Compliance Profile of Signed Action
              Receipts for AI Agents", Work in Progress, Internet-Draft,
              draft-marques-asqav-compliance-receipts-07, 20 July 2026,
              <https://datatracker.ietf.org/doc/html/draft-marques-
              asqav-compliance-receipts-07>.

   [RFC7942]  Sheffer, Y. and A. Farrel, "Improving Awareness of Running
              Code: The Implementation Status Section", BCP 205,
              RFC 7942, DOI 10.17487/RFC7942, July 2016,
              <https://www.rfc-editor.org/rfc/rfc7942>.

   [RFC8032]  Josefsson, S. and I. Liusvaara, "Edwards-Curve Digital
              Signature Algorithm (EdDSA)", RFC 8032,
              DOI 10.17487/RFC8032, January 2017,
              <https://www.rfc-editor.org/rfc/rfc8032>.

   [RFC9052]  Schaad, J., "CBOR Object Signing and Encryption (COSE):
              Structures and Process", STD 96, RFC 9052,
              DOI 10.17487/RFC9052, August 2022,
              <https://www.rfc-editor.org/rfc/rfc9052>.

Acknowledgments

   The rule that states what each structure does not prove responds to
   auditors who receive green dashboards and are asked to trust them.

   Iman Schrock reviewed revision -02 on the SCITT mailing list. He
   identified two overclaims. One claimed that a clean reconciliation
   established coverage of the source activity. The other claimed that
   Transformation Evidence proved the transformation rather than the
   Issuer's assertion of it. Revision -03 corrected both. The outcome
   vocabulary of Section 4.3 follows from that exchange. The rule that
   a declared bound cannot yield a stronger outcome also follows from
   that exchange. Reviewing -03, Schrock established a further point. An
   Item whose classification rule does not resolve under the pinned
   profile is indeterminate, not excluded. Revision -04 applies that
   rule to bounds.

   Walter Hawkins read the reconciliation implementation. He found the
   temporal defect that -04 corrects. Window membership is decided
   across two clocks. An exact comparison creates a false finding where
   no gap exists. The failure is asymmetric. It produces false findings
   rather than missed ones. Hawkins observed that the sub-second case is
   the dangerous one. It is the case a reader will believe. Section 4.3
   sets no floor for this reason. The requirement that a source
   population declare its own completeness on the same standing ladder
   is also his.

   Joel Hillier reviewed -04 on the SCITT mailing list. He asked for
   named fields. He wanted a stated encoding for the temporal
   correspondence, not prose. Another specification could then adopt the
   same shape. The three clocks fields in Section 4.4 are written to be
   copied. They answer that request. Hillier also observed that a gaps
   section going stale in the understating direction is the same failure
   as one that overstates. The Implementation Status section of this
   revision was rewritten from measurement for this reason.

   Henri Sirkkavaara established the distinction in Section 6.1. One
   construction supplies an expected quantity to a verifier from outside.
   The other carries it inside the signed material. Sirkkavaara built
   the second. He named what the first leaves an auditor unable to do.
   The consequence is stated against this document's own implementation,
   which does the first. A running count derived from the sequence number
   it accompanies adds no information. That observation is this
   author's, arrived at while measuring his. It is recorded here because
   it bears on the construction. The distinction stands.

   Andrew Yourtchenko reviewed -04 as a reader new to the work. He
   identified the length and density of the non-normative prose as the
   document's primary obstacle, ahead of any technical point. He proposed
   applying the principles of ASD-STE100 (Simplified Technical English)
   to the non-normative text. He published a rule set and a rewritten
   draft to show the effect. The sentence-length pass in -07 follows
   that suggestion.

Author's Address

   Emek Can Doğru
   VERAX TEKNOLOJİ LİMİTED ŞİRKETİ
   Türkiye
   Email: e.dogru@conarium.dev

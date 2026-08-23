# Undeclared vocabulary in draft-dogru-scitt-disclosure-evidence-04

This is a check for terms that the draft uses as if they named a specific, bounded
concept, but never defines. Section 2 ("Conventions and Definitions") exists and
defines seven terms: Data Source, Gateway, Disclosure, Receipt, Protected Class,
Window, and Mapping Profile. It also adopts the BCP 14 key words with [RFC2119]
and [RFC8174] cited.

The list below was produced by inventorying Section 2 first, then sweeping the
whole file for capitalised terms and for lower-case terms that carry weight inside
normative statements. Each candidate was grepped for its first occurrence and for
any definition anywhere in the document. Terms that turned out to be defined in
Section 2, defined inline at first use, or covered by a citation at the point of
use are listed in "Checked and not reported" at the end.

Seven findings follow. Two further terms are inherited from the cited SCITT
architecture and are kept in a separate section, because they are a citation
question rather than a definition question.

---

## 1. "item"

Load-bearing use, Section 4.3:

> The comparison is between two populations — source-level activity and
> Receipts — and neither population is assumed complete.  Each item in
> either population receives exactly one of the following outcomes:

And Section 4.6:

> counts:  The number of items in each outcome, including matched and
> excluded.

Check: not in Section 2; no inline definition at first use (the first occurrence
is in the Introduction, "a signed result statement classifying each item of either
account"); no reference cited.

Why it matters: "item" is the unit that every outcome attaches to and that the
`items` and `counts` fields of the result statement enumerate, so two
implementations that read it differently will produce different counts from the
same evidence. Two plausible readings: (a) an item is one entry in a snapshot,
that is one activity pattern whose counter increased, paired on the other side
with one Receipt; (b) an item is one (pattern, data object) pair, which is what
"Matching is per pattern and per data object" in Section 4.3 suggests, and which
would multiply the count for any pattern touching several objects. Section 4.3 also
says an item can "leave" objects unaccounted for, which fits reading (b) poorly if
an item is itself per-object.

## 2. "object" / "data object", and what it means for a Receipt to "name" one

Load-bearing uses, Section 4.3:

> For each pattern whose counter increased during the Window, the
> reconciler attributes the pattern to the data objects it touches and
> checks whether any Receipt in the Window names those objects.

> observed-without-receipt:  The Data Source recorded activity against
> an object that no Receipt in the Window names.

Check: not in Section 2; no inline definition; no reference cited. The word
"object" is also used in the document in its JSON sense ("Transformation Evidence
is a JSON object"), which the reader must separate by context.

Why it matters: the whole comparison turns on object identity, and the granularity
is not stated. Two plausible readings: a table-level name, or a column-level name.
These give different answers whenever a pattern reads one protected column of a
table that a Receipt names as a whole. The related verb is undefined too: the draft
is deliberately agnostic to the receipt format ("This document is agnostic to the
receipt format in use", Section 2), so how a reconciler decides that a Receipt
"names" an object is left to the implementation, as is the attribution step that
maps a pattern digest to the objects it touches.

## 3. "Consumer" / "consumer"

Load-bearing uses, Section 3.4:

> Consumers MUST NOT present Transformation Evidence as proof of non-
> exposure.

Section 4.5:

> Consumers MUST NOT read a pinned exclusion as a justified one

Section 4.6:

> A consumer MUST NOT read a /1 result as a /2 result.

Check: not in Section 2; no inline definition; no reference cited. It appears
capitalised in Sections 3.4 and 4.5 and lower-case in Sections 4.6 and 4.7, which
makes it read as a defined role in some places and as ordinary English in others.

Why it matters: three MUST NOT requirements are placed on this party, so a reader
implementing conformance needs to know who is bound. Two plausible readings: any
party that reads the payload, including a human auditor reading a dashboard; or the
software component that parses and displays the structure. The obligations differ
in kind, since "MUST NOT present" is an obligation on a producer of a report while
"MUST NOT read as" is an obligation on an interpreter.

## 4. "reconciler" and "reconciling party"

Load-bearing uses, Section 4.3:

> Given a start snapshot, an end snapshot, and the receipt set for the
> Window, a reconciler proceeds as follows.

> the item takes the outcome it would have had, and a reconciler MUST
> report which bound it applied to reach that.

Section 4.6:

> The result statement is serialized and digested as in Section 3.3 and
> is intended to be signed by the reconciling party and registered
> (Section 5).  The reconciler SHOULD be operationally independent of
> the Gateway

Check: neither term is in Section 2; neither has an inline definition; no reference
cited. Section 5 says an Issuer is "the reconciling party for a Coverage
Reconciliation result", which tells the reader that the reconciling party signs,
but does not say that it is the same entity as the reconciler.

Why it matters: this is the actor that carries most of the normative load in
Section 4, and it appears under two names in adjacent sentences of the same
section. If they are one role, one name would settle it; if the party that runs the
comparison may differ from the party that signs the result, that is a distinction a
reader would want stated, because the "operationally independent of the Gateway"
SHOULD then has to say which of the two it constrains.

## 5. The bound-standing values "protocol-defined" and "measured"

Load-bearing use, Section 4.4:

> A reconciliation result computed against a Mapping Profile MUST bind
> that profile's digest, and MUST state, for each bound it relies on,
> whether the bound is protocol-defined, measured, operator-declared,
> or undeclared.  A result MUST NOT present an operator-declared bound
> as a measured one.

Repeated as the `bounds` field in Section 4.6.

Check: none of the four values is in Section 2. "operator-declared" and
"undeclared" are explained by the surrounding text of Sections 4.3 and 4.4.
"protocol-defined" and "measured" are not defined anywhere in the document, and no
reference is cited for them.

Why it matters: this is an enumerated field in a signed result, and a MUST NOT
turns on the distinction between two of its values. The draft names only two bounds
(multiplicity and skew), and it argues in Section 4.4 that the Gateway cannot
measure either of them, so a reader cannot tell what would ever qualify as
"measured", nor which protocol would supply a "protocol-defined" bound. Two
plausible readings of "protocol-defined": a bound fixed by this document, of which
there are currently none; or a bound fixed by some other protocol in the
deployment, such as a time-synchronisation protocol's stated accuracy.

## 6. "client-level operation" / "client-level request", and "source-level statement"

Load-bearing use, Section 4.4:

> A Mapping Profile is therefore declared by the operator.  It states,
> for each client-level operation it covers, the expected bounded set
> of source-level patterns, the bound on their multiplicity, and the
> exclusion rules applied before comparison (Section 4.5).

Section 4.3 uses a different noun for what appears to be the same thing:

> Matching is per pattern and per data object, not per call count: one
> client-level request may legitimately produce more than one source-
> level statement, so call counts and receipt counts MUST NOT be
> compared one-to-one.

Check: not in Section 2; no inline definition; no reference cited. Section 2 defines
Disclosure ("A single delivery of data ... from the Gateway to a client") and
Section 3.2 has a `request` member, but neither is equated with "client-level
operation".

Why it matters: the Mapping Profile is keyed on this unit, so an operator writing a
profile has to decide what counts as one operation. The draft offers at least three
candidate nouns for the client side (request, Disclosure, client-level operation)
and two for the source side (source-level statement, activity pattern), and does not
say which are synonyms. A profile written against one reading and consumed under
another would produce multiplicity bounds that do not mean what the reconciler
thinks they mean.

## 7. "the operator"

Load-bearing use, Section 2, inside the definition of Mapping Profile:

> Mapping Profile:  A versioned statement, declared by the operator, of
> the correspondence expected between one client-level operation and
> the source-level activity it produces

Section 6:

> Declared correspondence as an attack surface.  The Mapping Profile
> (Section 4.4) is written by the operator, and it decides both what
> counts as a match and what is excluded before matching.

Check: not itself defined in Section 2, although Section 2 uses it inside another
definition; no inline definition; no reference cited. Section 5 mentions "the
Gateway operator" for Transformation Evidence, which is the closest the document
comes to fixing the referent.

Why it matters: Section 6 states that the Gateway and the Data Source are sometimes
operated by the same party, which implies that elsewhere they are not. The
definite article "the operator" then does not identify which one declares the
Mapping Profile. Since the profile declares the clock source on both sides and the
skew between them, a reader assessing the security argument needs to know whether
the declaring party is the one that operates the Gateway, the one that operates the
Data Source, or a deployment owner above both.

---

## Terms inherited from a cited reference, noted separately

These are not counted as findings. They appear to come from the SCITT architecture
[RFC9943], which the draft cites normatively. The note is only that the citation
does not appear at the point of first use.

- **Issuer.** First used in Section 1.1 ("it is the Issuer's signed assertion that a
  transformation was applied"), then eight more times in Section 3.4, with no
  citation. Section 5 supplies a working gloss for this document ("An Issuer (the
  Gateway operator for Transformation Evidence; the reconciling party for a Coverage
  Reconciliation result)") alongside the [RFC9943] citation. A reader who stops at
  Section 3.4 has met the term four pages before that gloss. A pointer at first use
  would close the gap.

- **Verifier.** Used exactly once, in Section 3.4: "Unless a Verifier independently
  establishes that the disclosed bytes carry the transformation the Issuer describes,
  the evidence available is evidence of what the pinned Issuer asserted." Capitalised,
  no citation, no gloss. I could not confirm from the draft alone whether this is the
  SCITT role of the same name, and the activity described is a check on disclosed data
  bytes rather than on a signature or an inclusion proof, so the two readings are: the
  SCITT verifying party, acting here in an additional capacity; or a separate
  data-plane checking party that this document assumes but does not introduce.

---

## Checked and not reported

- **Data Source, Gateway, Disclosure, Receipt, Protected Class, Window, Mapping
  Profile** — defined in Section 2.
- **MUST, SHOULD, MAY and the other key words** — Section 2 cites BCP 14 [RFC2119]
  [RFC8174] with the standard "when, and only when, they appear in all capitals"
  qualifier.
- **snapshot** — defined inline at first use, Section 4.2: "A snapshot is a JSON
  object capturing the Data Source's cumulative activity counters at a point in
  time", with its members enumerated.
- **pattern** — defined inline where the field is introduced, Section 4.2: "A digest
  of the normalized activity pattern (for example, a normalized statement with
  constants removed)."
- **matched, observed-without-receipt, receipted-without-observation, excluded,
  indeterminate** — each is given a definition in the outcome list of Section 4.3,
  and their semantics are expanded in Section 4.7.
- **invalid-window, no-exceptions, exceptions** — defined where the `outcome` field is
  introduced, Section 4.6.
- **multiplicity bound** — explained inline in Section 4.4 ("One client-level
  operation may produce several source-level statements. The multiplicity is not a
  property of the Gateway; it is a property of the deployment"), and named in the
  Section 2 definition of Mapping Profile.
- **skew bound** — explained inline in Sections 4.3 and 4.4 as the bound between the
  Data Source's clock and the Gateway's clock, and named in the Section 2 definition
  of Mapping Profile.
- **Signed Statement, Transparency Service** — SCITT architecture terms, and
  [RFC9943] is cited at the point of use in both Section 1 and Section 5.
- **Receipt in the SCITT sense** — the draft has its own Section 2 definition of
  Receipt and flags the collision itself in Section 5: "obtaining a Receipt in the
  SCITT sense: proof of the statement's inclusion, at a position, in an append-only
  log operated by a party other than the Issuer."
- **population** — identified inline where introduced, Section 4.3: "The comparison
  is between two populations — source-level activity and Receipts".
- **pinned / pinning** — a working sense is given in Section 4.5, which explains that
  carrying the rule identifier makes an exclusion reproducible because the rule is
  covered by the profile digest.
- **receipt set** — used from the Abstract onward without a formal definition, but
  Sections 4.3 and 4.6 tell the reader what determines its membership (the Window,
  decided across two clocks) and how it is identified in a result (a digest, with the
  chain head digest and sequence range RECOMMENDED for chained formats). Reported as
  cleared, though a one-line Section 2 entry would remove the remaining work the
  reader does.
- **auditor** — used three times in ordinary English, never inside a normative
  statement, and never as the name of a bounded role.
- **policy, policy decision** — the Section 2 definition of Gateway states that it
  "applies policy", and Section 3.2 glosses the `policy` member's `id` and `decision`.
  The set of permitted `decision` values is not enumerated, which is a
  specification-completeness question rather than an undefined term.
- **digest prefix values** — Section 3.3 defines the `sha256:` form and the rule for
  unrecognised prefixes.
- **mask, redact, tokenize, truncate, none** — enumerated in Section 3.2, with the
  meaning of `none` stated explicitly.

---

*Advisory only. Produced by an LLM pass on 2026-08-23 over
`draft-dogru-scitt-disclosure-evidence-04.txt`. All quotations and section numbers
were checked against the draft text.*

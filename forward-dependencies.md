# Forward dependencies in draft-dogru-scitt-disclosure-evidence-04

A *forward dependency* — our name for it, not a term of art, coined while
writing this — is a place where the text raises a doubt, a risk, or an apparent
contradiction, and the material that settles it appears later in the document,
with nothing at the point of doubt saying so. The reader forms an objection and
carries it for pages before the answer arrives.

Every item below is answered by this draft. None of these is a technical
defect, and none is a missing argument. The issue is order alone: the answer is
not where the reader needs it. The suggested fix in each case is a pointer at
the place the doubt is formed, not a change to the argument and not a change to
section order.

The list was produced by a whole-document read, then by locating a verbatim
resolution for each candidate. Candidates without a verbatim resolution were
dropped; those are listed at the end.

---

## 1. Counter regression invalidates a Window, while the counters are what the reader is asked to rely on

**Raised in §4.3 (Reconciliation procedure), page 8:**

> A counter regression means the source's accounting was reset or altered
> inside the Window; the Window is then unreliable, and the reconciler MUST
> report failure for the Window as a whole rather than reconciling the
> surviving patterns.  An attacker who can reset counters must gain an error,
> not a clean report.

At this point the reader has been told in §1 that completeness is established
by "a second account of activity, produced by a party other than the gateway:
the data source itself". §4.3 now introduces an attacker who can rewrite that
account, and says nothing about what remains of the mechanism's value once such
an attacker is admitted. The passage reads as conceding the premise.

**Resolved in §6 (Security Considerations), page 15:**

> Counter manipulation.  An attacker who can reset or rewind source counters
> could otherwise hide activity between snapshots.  The MUST-fail rule exists
> for this case: a Window containing a regression is reported unreliable in its
> entirety.  Snapshot frequency bounds the exposure — shorter Windows mean a
> reset costs the attacker a visible failure sooner.

**Distance:** ~7 pages, two major sections apart (§4.3 → §6).

**Suggested fix:** at the "An attacker who can reset counters" sentence, add a
pointer such as "(the exposure this leaves is analysed in Section 6)".

---

## 2. The clock-skew machinery reads like a workaround for something a synchronised clock would remove

**Raised in §4.3 (Reconciliation procedure), page 8:**

> A Mapping Profile therefore declares the clock source on each side and the
> skew bound between them, as it declares multiplicity (Section 4.4), and both
> are covered by the profile digest as every other part of it is.

The reader arriving here has just been shown a three-second clock difference
producing a false bypass finding, and the natural objection is that this is a
deployment problem a synchronised clock would remove, not something a protocol
should carry. §4.3 does cite Section 4.4, but only as the place multiplicity is
declared; nothing at this point tells the reader that the standing of a
synchronised clock — declaration versus measurement — is itself treated there.

**Resolved in §4.4 (Mapping profiles), pages 11 and 11–12:**

> Both are operator statements and carry that standing under the rule below,
> including a declaration that the two sides read one clock and the bound is
> therefore zero.  That declaration is still a declaration: one clock read twice
> is not read at the same instant, and whether the residue matters is a
> judgement about the deployment.

and

> An implementation MUST NOT substitute a default of zero: zero asserts that the
> two clocks agree, which is the assumption that produces the false accusation
> this document now guards against.

**Distance:** ~3 pages, one subsection apart (§4.3 → §4.4).

**Suggested fix:** extend the existing parenthetical so it names what §4.4
supplies, e.g. "(Section 4.4, including the case where the two sides read one
clock)".

---

## 3. The independence of the two accounts is asserted before the same-operator case is admitted

**Raised in §4.1 (Purpose), page 7:**

> The essential property is that the two accounts being compared originate from
> different components: the receipt set from the Gateway, the activity counters
> from the Data Source.  A Gateway cannot make bypassed activity disappear from
> an account it does not produce.

This is the strongest claim in the document and it carries no qualification at
the point it is made. A reader who knows that gateway and database are commonly
run by one party will read "different components" as sleight of hand — different
components, same operator — and will hold that objection through all of §4.

**Resolved in §6 (Security Considerations), page 15:**

> Same-operator collusion.  In many deployments the Gateway and the Data Source
> are operated by the same party.  Coverage Reconciliation's value against that
> party is reduced: an operator with administrative access to the source's
> accounting can suppress the counters themselves. [...] Deployments needing
> assurance against the operator itself require an accounting path the operator
> cannot write to; that is a deployment property, not a payload property.

**Distance:** ~8 pages, two major sections apart (§4.1 → §6).

**Suggested fix:** after "an account it does not produce", add "(the case where
both accounts are under one operator is treated in Section 6)".

---

## 4. §4.3 imposes reporting obligations whose reportable form is defined in §4.6

**Raised in §4.3 (Reconciliation procedure), page 8, twice:**

> the reconciler MUST report failure for the Window as a whole rather than
> reconciling the surviving patterns.

and

> the item takes the outcome it would have had, and a reconciler MUST report
> which bound it applied to reach that.

Neither obligation is expressible in the vocabulary §4.3 itself goes on to
define. The five outcomes listed later in §4.3 — `matched`,
`observed-without-receipt`, `receipted-without-observation`, `excluded`,
`indeterminate` — contain no way to report a failed Window and no way to report
which bound was applied. A reader who takes the list as complete will read the
two MUSTs as unimplementable.

**Resolved in §4.6 (Result statement), page 13:**

> bounds:  For each bound the comparison relied on, its source: protocol-defined,
> measured, operator-declared, or undeclared.

and

> outcome:  invalid-window when the Window is unreliable (Section 4.3);
> otherwise no-exceptions when every item is matched or excluded, and exceptions
> when any item is observed-without-receipt, receipted-without-observation, or
> indeterminate.

The cross-reference exists in one direction only: §4.6 points back to §4.3, and
§4.3 does not point forward to §4.6.

**Distance:** ~5 pages, three subsections apart (§4.3 → §4.6).

**Suggested fix:** name the field at each MUST, e.g. "MUST report failure for
the Window as a whole (reported as invalid-window, Section 4.6)" and "MUST
report which bound it applied (the bounds field, Section 4.6)".

---

## 5. The three-second figure appears without its provenance

**Raised in §4.3 (Reconciliation procedure), page 8:**

> The difference measured where this was found was three seconds; nothing in the
> procedure sets a floor below which it stops happening, and a smaller one is
> correspondingly harder for a reader to suspect.

"Where this was found" is not identified anywhere in §4, so the number reads as
either an unsourced anecdote or a reference to something the reader has missed.
The whole temporal apparatus of §4.3 and §4.4 rests on it.

**Resolved in §9 (Implementation Status), page 18:**

> The implementation admitted Receipts on an exact comparison across the two
> clocks, so a Receipt three seconds outside a two-hour Window produced
> observed-without-receipt and a message about a possible bypass.  That was
> raised in review of -03 on the SCITT mailing list, reproduced, and corrected
> in 0.2.27.

**Distance:** ~10 pages, five major sections apart (§4.3 → §9).

**Suggested fix:** attach the source to the figure at first use, e.g. "three
seconds, in the deployment described in Section 9".

---

## 6. The optional refusal to explain an offset larger than the Window arrives without its motivating case

**Raised in §4.4 (Mapping profiles), page 12:**

> An implementation MAY, absent a declared bound, decline to offer the boundary
> as the explanation for an offset larger than the Window itself, on the ground
> that a boundary artefact cannot exceed the interval it bounds.  This is a
> reporting choice about what an implementation is willing to suggest, not a
> change of outcome: the item is indeterminate either way.

An optional rule, stated abstractly, guarding a case the reader has not been
shown. Without the case, the paragraph reads as a hypothetical whose cost —
another MAY in an implementation profile — is not obviously earned.

**Resolved in §9 (Implementation Status), page 18:**

> The correction was then attacked: a Receipt from the previous day, naming the
> same object, moved a real in-Window absence into the new outcome and the
> implementation offered the boundary as its explanation — an exculpation a
> twenty-three hour offset cannot support. 0.2.28 bounds what the implementation
> is willing to suggest, which is the reporting choice described in Section 4.4.

Again the cross-reference runs backward only: §9 cites §4.4; §4.4 does not cite
§9.

**Distance:** ~6 pages, five major sections apart (§4.4 → §9).

**Suggested fix:** add "(the case that motivates this is in Section 9)" to the
MAY.

---

## Candidates considered and not reported

- **§4.6 `coverage-reconciliation/1` and the word `covered`.** §4.6 states that
  "a /1 result reporting covered asserts more than the procedure establishes"
  without defining `covered`, and §9 supplies the history ("Earlier revisions of
  this document, and releases of that implementation up to 0.2.21, described a
  clean reconciliation as 'covered'"). Both halves are verbatim, but the doubt
  raised is an undefined term rather than an objection the reader forms and
  carries, so it is recorded here rather than as a finding.
- **§4.5 exclusions as the path to a clean result.** §4.5 raises the risk and
  bounds it in place ("the mechanism reproduces the decision, it does not judge
  it") and already cites §4.4. The additional adversarial framing in §6
  ("Declared correspondence as an attack surface") extends it but does not
  resolve a doubt §4.5 leaves open.
- **§3.2 `action: none`.** The reader may ask what stops a deployment from
  declaring every class `none`. No verbatim resolution appears anywhere in the
  document. This is therefore not a forward dependency; if it is worth answering,
  it is a gap rather than an ordering problem.
- **§3.2 "An implementation encountering a value in a field defined here MUST
  reject the structure."** No text states how an implementation distinguishes a
  value from a class name, an action name, or an identifier. Again no verbatim
  resolution exists, so this is noted as a possible gap, not a forward dependency.

---

*This document is advisory. It was produced by an LLM pass over the full text of
draft-dogru-scitt-disclosure-evidence-04 on 2026-08-23. Section numbers and
quotations were checked against the draft; the judgement about where a reader
forms an objection was not, and is the author's to accept or reject.*

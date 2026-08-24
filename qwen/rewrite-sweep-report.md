# sweep v3 report
paras checked: 104
patches proposed: 11
applied: 11
skipped: 0

APPLIED R: They do not say what happened to the data between the source and the client. ==> They do not say what happened to the data between the data source and the client.
APPLIED D: This document defines no new receipt format, no policy evaluation semantics, and no transparency mechanism.
APPLIED D: A chain that verifies does not show entries that were never written.
APPLIED R: It states what a mediator recorded. ==> It states what a gateway recorded.
APPLIED D: This document does not fix the receipt format.
APPLIED R: It states the expected correspondence between one client-level operation and the source-level activity it produces. ==> It states the expected correspondence between one client-level operation and the data-source-level activity it produces.
APPLIED D: This document does not assign it.
APPLIED R: A Receipt in the Window names an object for which the Data Source's counters record no activity. ==> A Receipt in the Window names an object for which the data source's counters record no activity.
APPLIED R: So does an intermediary that collapses statements. ==> So does a gateway that collapses statements.
APPLIED D: Verification of receipt signatures and chain integrity is out of scope for reconciliation and is assumed to have happened first, under the rules of the receipt format in use.
APPLIED D: Key management, revocation, and the consequences of Issuer key compromise are governed there, not here.

metrics: {'sents': 272, 'median': 11, 'over25': 10.7, 'connpct': 6.6}

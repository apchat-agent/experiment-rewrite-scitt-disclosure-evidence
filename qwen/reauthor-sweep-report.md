# sweep v3 report
paras checked: 105
patches proposed: 16
applied: 16
skipped: 0

APPLIED R: The second compares source activity counters against receipt sets to classify items into specific outcomes. ==> The second compares data source activity counters against receipt sets to classify items into specific outcomes.
APPLIED D: They rely on existing mechanisms and do not define new receipt formats.
APPLIED R: They do not say what happened to the data between the source and the client. ==> They do not say what happened to the data between the data source and the client.
APPLIED R: It compares source activity snapshots at the window bounds with the receipt set for that window. ==> It compares data source activity snapshots at the window bounds with the receipt set for that window.
APPLIED D: This document does not reinvent that.
APPLIED D: A chain that verifies says nothing about entries that were never written.
APPLIED R: It states what a mediator recorded. ==> It states what a gateway recorded.
APPLIED D: This document does not fix the receipt format.
APPLIED D: This document does not assign it.
APPLIED R: The digest of the request, never the request text: query text can itself contain protected values. ==> The digest of the request, never the request text: request text can itself contain protected values.
APPLIED R: A silently ignored fourth field declares less than its author believes. The gap shows up as an outcome the operator cannot account for. ==> A silently ignored fourth field declares less than its author believes: the gap shows up as an outcome the operator cannot account for.
APPLIED R: The digest checks transcription, not completeness. ==> The digest checks transcription, not completeness: the matched count inherits that standing.
APPLIED R: So does an intermediary that collapses statements. ==> So does a gateway that collapses statements.
APPLIED D: Verification of receipt signatures and chain integrity is out of scope for reconciliation and is assumed to have happened first, under the rules of the receipt format in use.
APPLIED D: Key management, revocation, and the consequences of Issuer key compromise are governed there, not here.
APPLIED R: What matters to a Consumer is where that material arrives from. The two constructions differ in a way a digest does not reveal. ==> What matters to a Consumer is where that material arrives from: the two constructions differ in a way a digest does not reveal.

metrics: {'sents': 664, 'median': 10, 'over25': 7.5, 'connpct': 4.5}

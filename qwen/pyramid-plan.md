(A)
**Chapter 1: Introduction and Scope**
This chapter introduces the draft's objective to define two specific evidence structures—Transformation Evidence and Coverage Reconciliation—to address audit gaps in data disclosure, while explicitly stating that these structures do not prove the occurrence of transformations or the intent behind missing receipts. It outlines the threat model, noting that Gateway and Data Source operators may be the same entity, and clarifies the relationship between these new evidence types and existing coverage attestation mechanisms, emphasizing that neither substitutes for the other.

**Chapter 2: Conventions and Definitions**
This chapter establishes the terminology and operational roles for the protocol, defining key entities such as the Gateway, Data Source, and Reconciler, and distinguishing between protocol-defined and measured bounds. It specifies that an "Item" in reconciliation refers to a single pattern counter increment or Receipt, and clarifies that the document is agnostic to specific receipt formats, requiring explicit identification of operator roles to avoid ambiguity.

**Chapter 3: Transformation Evidence**
This chapter defines the Transformation Evidence structure as a JSON object that documents which protected data classes were transformed and the actions taken, without revealing the actual data values. It specifies the serialization requirements using JSON Canonicalization Scheme (JCS) and SHA-256 digests, and explicitly limits the scope of this evidence to describing the disclosure surface, prohibiting its use as proof that values are unlearnable or that transformations were successfully applied.

**Chapter 4: Coverage Reconciliation**
This chapter details the Coverage Reconciliation procedure, which compares Data Source activity snapshots against Gateway receipt sets to classify items into five specific outcomes: matched, observed-without-receipt, receipted-without-observation, excluded, or indeterminate. It defines the structure of activity snapshots, the requirements for Mapping Profiles to declare multiplicity and clock skew bounds, and the strict reporting rules for exclusions and results, ensuring that operator-declared bounds are never presented as measured facts.

**Chapter 5: Registration on a Transparency Service**
This chapter explains how both evidence structures are registered as Signed Statements on a SCITT Transparency Service, leveraging existing mechanisms from RFC 9943. It clarifies that the binding between evidence and receipts is established over the payload digest to ensure integrity, and notes that the document does not define new countersignature, anchoring, or log formats, relying instead on the append-only nature of the transparency log for audit value.

**Chapter 6: Security Considerations**
This chapter addresses security risks such as same-operator collusion, counter manipulation, and the detection of truncated receipt sets. It mandates that implementations reject unknown digest prefixes and clarifies that signature compromise is a SCITT-layer issue. It specifically discusses the challenge of detecting receipt set truncation, requiring either an external verifier input or a sealed total within the signed material, and mandates that verification results explicitly identify which construction was used.

**Chapter 7: Privacy Considerations**
This chapter mandates that evidence structures must not act as disclosure channels by strictly prohibiting the inclusion of raw data values in Transformation Evidence. It acknowledges that class names and counts inherently reveal some information but suggests that deployments can mitigate sensitivity by registering only digests and keeping payloads private, thereby restricting third-party audits to a permissioned act.

**Chapter 8: IANA Considerations**
This chapter requests the registration of two new media types (`application/transformation-evidence+json` and `application/coverage-reconciliation+json`) and the creation of two registries for Transformation Actions and Coverage Reconciliation Outcomes. It specifies that the registration policy for these registries is "Specification Required" and defines the templates and initial values for the registries, ensuring that future extensions follow a controlled process.

**Chapter 9: Implementation Status**
This chapter documents the implementation status of the Conarium gateway, noting that its `conarium-reconcile` tool emits `coverage-reconciliation/2` result statements while retaining legacy compatibility. It defines specific behavioral requirements for handling temporal skew and exclusion rules, such as marking items as `indeterminate` when bounds are undeclared, and mandates that implementation claims be verified by automated checks binding behavioral statements to specific tool runs.

**Chapter 10: References**
This chapter lists the normative and informative references required for the document, including RFCs for requirement level keywords, media type specifications, IANA considerations, JSON Canonicalization Scheme, and the SCITT architecture. It also credits specific reviewers for identifying critical technical defects and notes that the document's prose was revised to apply Simplified Technical English principles.

(B)
This Internet-Draft defines two new evidence structures, Transformation Evidence and Coverage Reconciliation, designed to enhance the auditability of data disclosure by recording which data classes were transformed and reconciling source activity counters against receipt sets. Both structures are registered as Signed Statements on a SCITT Transparency Service, relying on existing mechanisms rather than defining new receipt formats, and are intended to address gaps in standard access receipts by providing signed, registrable artifacts that document disclosure surfaces and detect bypassed activity or failed receipt sinks. The document explicitly limits the scope of these structures, stating that they do not prove the occurrence of transformations or the intent behind missing receipts, and it provides detailed specifications for serialization, security considerations, privacy protections, and IANA registrations to ensure interoperability and audit integrity.

(C)
1. **Introduction and Scope** (Source: 1, 1.1, 1.2, 1.3)
2. **Conventions and Definitions** (Source: 2)
3. **Transformation Evidence** (Source: 3, 3.1, 3.2, 3.3, 3.4)
4. **Coverage Reconciliation** (Source: 4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7)
5. **Registration on a Transparency Service** (Source: 5)
6. **Security Considerations** (Source: 6, 6.1)
7. **Privacy Considerations** (Source: 7)
8. **IANA Considerations** (Source: 8, 8.1, 8.2, 8.3, 8.4)
9. **Implementation Status** (Source: 9)
10. **References** (Source: 10, 10.1, 10.2)
#!/usr/bin/env python3
"""Script-driven rules-based rewrite/reauthor of an IETF draft via a llama.cpp
OpenAI-compatible endpoint (qwen38-27b on the beta rig).

Modes:
  rewrite  - register-only rewrite, section by section, BCP14 sentences frozen
  reauthor - pyramid procedure (L1 -> L2/L3+outline -> top-down chapters)

Every run writes a run-config.json (endpoint, model, params, prompt digest
hash) into the output dir before the first call, per the household
record-config-with-measurements rule.
"""
import argparse, hashlib, json, os, re, sys, time, urllib.request

ENDPOINT = os.environ.get("QWEN_URL", "http://100.91.40.51:8080/v1/chat/completions")

BCP14 = r"\b(MUST NOT|MUST|SHALL NOT|SHALL|SHOULD NOT|SHOULD|MAY|REQUIRED|RECOMMENDED|NOT RECOMMENDED|OPTIONAL)\b"

RULES_DIGEST = """You rewrite IETF specification prose. Rules, in force together:
1. FREEZE: every sentence containing an uppercase BCP 14 keyword (MUST, MUST
   NOT, SHALL, SHOULD, SHOULD NOT, MAY, REQUIRED, RECOMMENDED, OPTIONAL, NOT
   RECOMMENDED) is reproduced EXACTLY, byte for byte. Never reword, split, or
   merge such a sentence. Everything else you may rewrite.
2. VOCABULARY: plain, literal, single-meaning words. Exemptions: the
   document's defined terms (Gateway, Data Source, Disclosure, Receipt,
   Protected Class, Window, Mapping Profile, Item, Data Object, Consumer,
   Reconciler, Issuer, Verifier and the other Terminology entries), registry
   values, standard names, BCP 14 keywords. One word per concept everywhere.
   Literal verbs only (be, have, make, get, show, give, use, apply, compare,
   record, sign, reject, contain, define). No metaphor, no personification:
   a chain is never "silent", it "does not show"; nothing "rests on" or
   "anchors" anything.
3. SENTENCES: target median 10-12 words, hard cap 25 (frozen sentences
   exempt). One fact per sentence. Active voice. No dangling "this": repeat
   the noun.
4. RELATIONS: when splitting a long sentence, keep its causal/conditional
   relation, carried by (in order of preference): sentence order (cause
   before effect), a colon, repeating the noun. A connective word (therefore,
   because, but) is the LAST resort. Target: fewer than 1 sentence in 10
   contains a connective word.
5. NO PROSE ABOUT PROSE: no "this section describes"; no sentences listing
   what the document does NOT define (state what it does, precisely); no
   self-grading ("strictest", "deliberate", "important"); no restating as a
   counterfactual ("Without X ...") what the previous sentence already says.
6. CLAIMS: a stated limit or property must exclude a possible alternative
   (never "a receipt cannot attest what was not recorded" - that is empty);
   a claim of existence carries its citations at the claim; an ambiguity is
   stated by enumerating its cases.
7. A rule's rationale: at most ONE clause, attached after a colon. Never a
   chain of consequence sentences.
8. Do not add content, do not reorder sections, do not drop technical facts,
   tables, JSON, or citations like [RFC9943]. Keep headings exactly.

REWRITE, do not copy. Non-frozen sentences that violate a rule MUST change.
Worked example pairs from the rules (BAD -> GOOD):

BAD:  Several receipt formats exist.
GOOD: Several receipt formats exist [I-D.farley-acta-signed-receipts]
      [I-D.marques-asqav-compliance-receipts]
      [I-D.chueayen-attestation-receipts] [I-D.aylward-aiga-2].
      (a claim of existence carries its citations at the claim)

BAD:  They share a limit. A receipt is evidence from the party that
      performed the access. It is about an event that party chose to record.
GOOD: All of the formats share one limit: the party under audit selects the
      evidence. A receipt is produced by the gateway that performed the
      access.
      (the limit states its criterion and excludes an alternative; the
      "chose to record" clause was an empty tautology and died)

BAD:  This document does not define that again. It defines no new receipt
      format, no rules for policy decisions, and no transparency mechanism.
GOOD: (deleted - fold any real fact into the sentence that introduces the
      thing; never enumerate what the document does not define)

BAD:  A fourth field that is ignored without a report makes the declaration
      state less than its author believes. The difference appears later as
      an outcome that the operator cannot explain.
GOOD: : a field that is ignored without a report makes the declaration state
      less than its author believes.
      (one reason, attached after a colon; the second consequence sentence
      died)

BAD:  For this reason it carries the strictest reporting rules of the five.
GOOD: The rules below make each exclusion visible in the result.
      (never grade your own rules; state what they do)

Output ONLY the rewritten text of the given section, no preamble, no fences."""

def call(messages, max_tokens=4096, temperature=0.15, retries=3, thinking=False):
    body = json.dumps({
        "messages": messages, "max_tokens": max_tokens,
        "temperature": temperature,
        "chat_template_kwargs": {"enable_thinking": thinking},
    }).encode()
    for i in range(retries):
        try:
            req = urllib.request.Request(ENDPOINT, data=body,
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=900) as r:
                out = json.load(r)
            return out["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"  call failed ({e}); retry {i+1}", file=sys.stderr)
            time.sleep(10)
    raise RuntimeError("endpoint failed after retries")

def strip_furniture(text):
    out = []
    for ln in text.splitlines():
        if re.match(r"^(Do.ru|Dogru).*\[?Page \d+\]?\s*$", ln): continue
        if re.match(r"^Internet-Draft\s+.*\d{4}\s*$", ln): continue
        if ln.strip() == "\f" or ln == "\x0c": continue
        out.append(ln.replace("\f", ""))
    return "\n".join(out)

def split_sections(text):
    """Split at top/second-level numbered headings at column 0."""
    lines = text.splitlines()
    idx = [i for i, ln in enumerate(lines)
           if re.match(r"^(\d+(\.\d+)*\.)  \S", ln) or re.match(r"^(Abstract|Status of This Memo|Copyright Notice|Table of Contents|Acknowledg|Author's Address|Normative References|Informative References|References)\b", ln)]
    if not idx or idx[0] != 0:
        idx = [0] + idx
    secs = []
    for a, b in zip(idx, idx[1:] + [len(lines)]):
        chunk = "\n".join(lines[a:b]).strip("\n")
        if chunk.strip():
            secs.append(chunk)
    return secs

def norm_ws(s):
    return re.sub(r"\s+", " ", s).strip()

def frozen_sentences(text):
    flat = re.sub(r"\s+", " ", text)
    sents = re.split(r"(?<=[.!?]) (?=[A-Z\[`(])", flat)
    return [s.strip() for s in sents if re.search(BCP14, s) and len(s.split()) > 2]

def verify_frozen(orig_sec, new_sec):
    missing = []
    new_flat = norm_ws(new_sec)
    for s in frozen_sentences(orig_sec):
        if norm_ws(s) not in new_flat:
            missing.append(s)
    return missing

def metrics(text):
    lines = [l for l in text.splitlines() if l.strip() and not l.strip().startswith(("|", "```", "{", "}", '"'))]
    flat = " ".join(lines)
    sents = [s for s in re.split(r"(?<=[.!?]) (?=[A-Z\[`(])", flat) if len(s.split()) >= 3]
    lens = sorted(len(s.split()) for s in sents)
    conn = re.compile(r"\b(because|but|so that|therefore|however|thus|hence|although|though|since|whereas|while|consequently|instead|nevertheless|otherwise|moreover|furthermore|rather than)\b", re.I)
    n = len(sents) or 1
    return dict(sents=len(sents), median=lens[len(lens)//2] if lens else 0,
                over25=round(100*sum(1 for x in lens if x > 25)/n, 1),
                connpct=round(100*sum(1 for s in sents if conn.search(s))/n, 1))

def write_config(outdir, mode, extra=None):
    cfg = dict(endpoint=ENDPOINT, mode=mode, time=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
               digest_sha=hashlib.sha256(RULES_DIGEST.encode()).hexdigest()[:16],
               temperature=0.15, thinking=False, **(extra or {}))
    with open(os.path.join(outdir, "run-config.json"), "w") as f:
        json.dump(cfg, f, indent=1)

def mode_rewrite(src, outdir):
    secs = split_sections(strip_furniture(src))
    write_config(outdir, "rewrite", {"sections": len(secs)})
    out, report = [], []
    for i, sec in enumerate(secs):
        frozen = frozen_sentences(sec)
        head = sec.splitlines()[0][:60]
        print(f"[{i+1}/{len(secs)}] {head} (frozen: {len(frozen)})")
        boiler = re.match(r"^(Status of This Memo|Copyright Notice|Table of Contents|Author's Address|Normative References|Informative References|References)\b", sec)
        if boiler:
            out.append(sec); report.append(f"S{i+1} {head!r}: kept verbatim (boilerplate)")
            continue
        msgs = [{"role": "system", "content": RULES_DIGEST},
                {"role": "user", "content":
                 ("Frozen sentences for this section (reproduce each EXACTLY):\n"
                  + "\n".join(f"- {s}" for s in frozen) + "\n\n" if frozen else "")
                 + "Section to rewrite:\n\n" + sec}]
        new = call(msgs)
        miss = verify_frozen(sec, new)
        if miss:
            msgs.append({"role": "assistant", "content": new})
            msgs.append({"role": "user", "content":
                "These frozen sentences are missing or altered. Output the whole "
                "section again with each reproduced EXACTLY:\n" + "\n".join(f"- {s}" for s in miss)})
            new = call(msgs)
            miss = verify_frozen(sec, new)
        report.append(f"S{i+1} {head!r}: frozen {len(frozen)}, missing-after-retry {len(miss)}"
                      + (" FROZEN-VIOLATION " + " || ".join(m[:80] for m in miss) if miss else ""))
        out.append(new.strip())
    doc = "\n\n".join(out) + "\n"
    open(os.path.join(outdir, "rewritten.md"), "w").write(doc)
    m = metrics(doc)
    open(os.path.join(outdir, "rewrite-report.md"), "w").write(
        "# qwen rewrite report\n\n" + "\n".join(report) + f"\n\nmetrics: {m}\n")
    print("metrics:", m)

def mode_reauthor(src, outdir):
    clean = strip_furniture(src)
    secs = split_sections(clean)
    write_config(outdir, "reauthor", {"sections": len(secs)})
    # Stage 1: L1 summaries
    l1 = []
    for i, sec in enumerate(secs):
        head = sec.splitlines()[0][:60]
        if re.match(r"^(Status|Copyright|Table of Contents|Author|Normative Ref|Informative Ref|References)", head):
            continue
        print(f"[L1 {i+1}/{len(secs)}] {head}")
        l1.append(head + " :: " + call([
            {"role": "system", "content": "Summarize the given IETF draft section in 1-3 faithful sentences. Note requirements and definitions. If the section leaves a needed fact undefined, add [GAP: ...]. Output only the summary."},
            {"role": "user", "content": sec}], max_tokens=400))
    open(os.path.join(outdir, "pyramid-l1.md"), "w").write("\n\n".join(l1))
    # Stage 2: L2/L3 + outline
    plan = call([
        {"role": "system", "content": "You plan the re-authoring of an IETF draft from its per-section summaries."},
        {"role": "user", "content":
         "Per-section summaries:\n\n" + "\n\n".join(l1) + "\n\n"
         "Produce, in this order: (A) one paragraph per top-level chapter "
         "summarizing it (L2); (B) ONE paragraph describing the whole document "
         "(L3); (C) a proposed chapter order where no chapter needs a term or "
         "mechanism a later chapter introduces - list each proposed chapter "
         "with the source section numbers it will carry. Mark sections A/B/C."}],
        max_tokens=3000)
    open(os.path.join(outdir, "pyramid-plan.md"), "w").write(plan)
    # Stage 3: chapters, top-down
    order = call([
        {"role": "system", "content": "Extract the proposed chapter list (part C) as plain lines: one chapter title per line, followed by ':' and the source section numbers. Output nothing else."},
        {"role": "user", "content": plan}], max_tokens=800)
    chapters = [l.strip() for l in order.splitlines() if ":" in l and l.strip()]
    doc_parts = []
    # Abstract first, position zero
    abstract = call([
        {"role": "system", "content": RULES_DIGEST},
        {"role": "user", "content":
         "This is the one-paragraph whole-document summary (L3):\n\n" + plan +
         "\n\nWrite the document Abstract from the L3: ONE compact paragraph, "
         "~100 words, position zero - NO document-defined capitalized terms, "
         "no citations, no forward references; plain-language paraphrases "
         "only. Output only the paragraph."}], max_tokens=500)
    doc_parts.append("## Abstract\n\n" + abstract.strip())
    src_by_num = {}
    for sec in secs:
        mnum = re.match(r"^(\d+(\.\d+)*)\.", sec)
        if mnum: src_by_num[mnum.group(1)] = sec
    for ci, ch in enumerate(chapters):
        title, _, nums = ch.partition(":")
        wanted = re.findall(r"\d+(?:\.\d+)*", nums)
        material = "\n\n".join(src_by_num.get(n, "") for n in wanted if n in src_by_num) or clean[:4000]
        frozen = frozen_sentences(material)
        print(f"[CH {ci+1}/{len(chapters)}] {title.strip()[:50]} (frozen {len(frozen)})")
        body = call([
            {"role": "system", "content": RULES_DIGEST},
            {"role": "user", "content":
             (("Frozen sentences (reproduce each EXACTLY):\n" + "\n".join(f"- {s}" for s in frozen) + "\n\n") if frozen else "")
             + f"Write chapter '{title.strip()}' of the re-authored document, "
             "from this source material. Fresh prose, top-down: the reader has "
             "read only the previous chapters. Mark anything the source never "
             "determines as [GAP: ...]. Do not invent facts.\n\nSource "
             "material:\n\n" + material}], max_tokens=6000)
        miss = verify_frozen(material, body)
        doc_parts.append(f"## {ci+1}. {title.strip()}\n\n" + body.strip()
                         + (f"\n\n[FROZEN-VIOLATION: {len(miss)} normative sentences not byte-identical]" if miss else ""))
    doc = "\n\n".join(doc_parts) + "\n"
    open(os.path.join(outdir, "reauthored.md"), "w").write(doc)
    # Stage 4: mechanical normative coverage
    all_frozen = frozen_sentences(clean)
    flat = norm_ws(doc)
    missing = [s for s in all_frozen if norm_ws(s) not in flat]
    m = metrics(doc)
    open(os.path.join(outdir, "reauthor-report.md"), "w").write(
        "# qwen reauthor report\n\nchapters: " + str(len(chapters)) +
        f"\nnormative: {len(all_frozen)} total, {len(all_frozen)-len(missing)} byte-present, {len(missing)} missing\n"
        + "".join("\nMISSING: " + s for s in missing) + f"\n\nmetrics: {m}\n")
    print("normative missing:", len(missing), "metrics:", m)

SWEEP_PROMPT = """You review ONE paragraph of an IETF draft rewrite. Frozen: any
sentence containing an uppercase BCP 14 keyword (MUST/SHOULD/MAY/etc.) is
untouchable - never propose changes to those.

Defect classes:
(a) SCOPE NARRATION: a sentence enumerating what this document does NOT
    define ("This document defines no X, no Y"). Propose DELETE.
(b) TAUTOLOGY: a negative claim no possible design could violate. Test each
    negative sentence: could any design do otherwise? Example that IS one:
    "They do not show records that were never created." (nothing can show
    what was never created - DELETE; a neighbor about what hash chains DO
    detect already carries the content). Example that is NOT one: "A client
    that reaches the data source without the gateway produces no receipt."
    (names the concrete bypass case - keep).
(c) LOOSE RATIONALE: two consecutive rationale sentences after a rule;
    propose REPLACE merging to one, attached with a colon.
(d) TERM DRIFT: a synonym for an established term (the component is
    "gateway", never "mediator"; the store is "data source"). Propose
    REPLACE of that sentence with the term fixed.

Think it through, then output ONLY these lines (or the single line NO DEFECTS):
DELETE: <the exact sentence>
REPLACE: <the exact sentence> ==> <the replacement sentence>"""

def mode_sweep(src, outdir, indoc):
    text = open(indoc).read()
    paras = text.split("\n\n")
    cand = re.compile(r"\b(not|no|never|nothing|without|neither|cannot|silent)\b", re.I)
    write_config(outdir, "sweep-v3", {"input": indoc, "paras": len(paras)})
    patches, checked = [], 0
    for i, para in enumerate(paras):
        if len(para.split()) < 12 or not cand.search(para):
            continue
        if re.search(BCP14, para) and len(para.split()) < 30:
            continue
        checked += 1
        print(f"[sweep {checked} @para {i}] {para.strip().splitlines()[0][:50]}")
        r = call([{"role": "system", "content": SWEEP_PROMPT},
                  {"role": "user", "content": para}], max_tokens=6000, thinking=True)
        for ln in (r or "").splitlines():
            ln = ln.strip()
            if ln.startswith("DELETE: "):
                patches.append(("D", ln[8:].strip(), None, i))
            elif ln.startswith("REPLACE: ") and "==>" in ln:
                a, _, b = ln[9:].partition("==>")
                patches.append(("R", a.strip(), b.strip(), i))
    applied, skipped = [], []
    for op, a, b, pi in patches:
        if re.search(BCP14, a) or "[GAP" in a:
            skipped.append((op, a, "frozen/GAP")); continue
        flat_para = paras[pi]
        norm_target = norm_ws(a)
        hit = None
        # try to find the sentence with flexible whitespace
        pat = re.escape(a)
        pat = re.sub(r"\\\s+", r"\\s+", pat.replace(re.escape(" "), r"\s+"))
        m = re.search(pat, flat_para)
        if not m:
            skipped.append((op, a, "not found")); continue
        rep = "" if op == "D" else b
        paras[pi] = flat_para[:m.start()] + rep + flat_para[m.end():]
        applied.append((op, a, b))
    doc = "\n\n".join(paras)
    doc = re.sub(r"[ \t]+\n", "\n", doc)
    open(os.path.join(outdir, "swept.md"), "w").write(doc)
    m2 = metrics(doc)
    rep = [f"# sweep v3 report", f"paras checked: {checked}", f"patches proposed: {len(patches)}",
           f"applied: {len(applied)}", f"skipped: {len(skipped)}", ""]
    rep += [f"APPLIED {op}: {a}" + (f" ==> {b}" if b else "") for op, a, b in applied]
    rep += [f"SKIPPED {op} ({why}): {a[:100]}" for op, a, why in skipped]
    rep.append(f"\nmetrics: {m2}")
    open(os.path.join(outdir, "sweep-report.md"), "w").write("\n".join(rep) + "\n")
    print(f"checked {checked}, applied {len(applied)}, skipped {len(skipped)}; metrics: {m2}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["rewrite", "reauthor", "sweep"])
    ap.add_argument("source")
    ap.add_argument("outdir")
    ap.add_argument("--in", dest="indoc", help="input doc for sweep mode")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    src = open(a.source, encoding="utf-8", errors="replace").read()
    if a.mode == "sweep":
        mode_sweep(src, a.outdir, a.indoc)
    else:
        (mode_rewrite if a.mode == "rewrite" else mode_reauthor)(src, a.outdir)

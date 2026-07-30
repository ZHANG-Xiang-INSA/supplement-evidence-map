import json, io, sys

# SRC pointed at a local scratch directory; set it before rerunning
SRC = os.environ.get('SUPPL_SRC', '')
# OUT pointed at a local scratch directory; set it before rerunning
OUT = os.environ.get('SUPPL_OUT', '')

raw = open(SRC, encoding="utf-8").read()
data = json.loads(raw)
if isinstance(data, dict):
    data = data.get("result")
    if isinstance(data, str):
        data = json.loads(data)

def t(s, n):
    if not s:
        return ""
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[:n] + " ..."

buf = io.StringIO()
w = buf.write

w("# DIGEST\n")
w("Domains: %d\n\n" % len(data))

for block in data:
    dom = block.get("domain")
    f = block.get("findings") or {}
    v = block.get("verdict") or {}
    sups = f.get("supplements") or []
    w("\n" + "=" * 90 + "\n")
    w("## DOMAIN: %s  (%d supplements)\n" % (dom, len(sups)))
    w("DOMAIN NOTES: %s\n" % t(f.get("domain_notes"), 900))

    for s in sups:
        w("\n---\n### %s\n" % s.get("name"))
        w("- aliases: %s\n" % t(s.get("aliases"), 110))
        w("- GRADE: %s\n" % t(s.get("evidence_grade"), 150))
        w("- DOSE: %s\n" % t(s.get("typical_effective_daily_dose"), 380))
        w("- UL: %s\n" % t(s.get("upper_limit"), 260))
        w("- does: %s\n" % t(s.get("what_it_does"), 200))
        uses = s.get("evidence_backed_uses") or []
        w("- uses: %s\n" % t("; ".join(uses), 260))
        w("- benefits: %s\n" % t(s.get("who_benefits_most"), 240))
        w("- avoid: %s\n" % t(s.get("who_should_avoid"), 280))
        w("- HYPE: %s\n" % t(s.get("hype_vs_reality"), 340))
        for p in (s.get("key_papers") or [])[:3]:
            w("  * [%s] %s | %s | %s\n" % (
                t(p.get("study_type"), 60),
                t(p.get("citation"), 130),
                t(p.get("identifier"), 60),
                t(p.get("key_finding"), 210)))

    # verifier output: only the problems
    w("\n>>> VERIFIER (%s)\n" % dom)
    bad = [c for c in (v.get("citation_checks") or [])
           if (c.get("exists") is False) or (c.get("finding_correctly_characterized") is False)
           or (c.get("identifier_correct") is False)]
    if bad:
        w("BAD CITATIONS (%d of %d checked):\n" % (len(bad), len(v.get("citation_checks") or [])))
        for c in bad[:14]:
            w("  - %s | exists=%s idOK=%s findingOK=%s | FIX: %s\n" % (
                t(c.get("paper"), 110), c.get("exists"), c.get("identifier_correct"),
                c.get("finding_correctly_characterized"), t(c.get("correction"), 190)))
    else:
        w("BAD CITATIONS: none of %d\n" % len(v.get("citation_checks") or []))
    dbad = [d for d in (v.get("dose_checks") or []) if str(d.get("verdict", "")).upper() != "OK"]
    if dbad:
        w("DOSE PROBLEMS (%d of %d):\n" % (len(dbad), len(v.get("dose_checks") or [])))
        for d in dbad[:14]:
            w("  - %s | %s -> auth: %s | %s (%s)\n" % (
                t(d.get("supplement"), 45), t(d.get("reported"), 150),
                t(d.get("authoritative_value"), 200), d.get("verdict"), t(d.get("source"), 70)))
    else:
        w("DOSE PROBLEMS: none of %d\n" % len(v.get("dose_checks") or []))
    og = v.get("overstated_grades") or []
    if og:
        w("OVERSTATED GRADES:\n")
        for o in og[:10]:
            w("  - %s\n" % t(o, 190))
    mi = v.get("missing_items") or []
    if mi:
        w("MISSING: %s\n" % t("; ".join(mi), 400))
    w("NET: %s\n" % t(v.get("net_assessment"), 650))

open(OUT, "w", encoding="utf-8").write(buf.getvalue())
print("chars:", len(buf.getvalue()))
print("supplements:", sum(len((b.get("findings") or {}).get("supplements") or []) for b in data))
print("papers:", sum(len(s.get("key_papers") or []) for b in data for s in ((b.get("findings") or {}).get("supplements") or [])))
print("citation checks:", sum(len((b.get("verdict") or {}).get("citation_checks") or []) for b in data))

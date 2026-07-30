# -*- coding: utf-8 -*-
import os
import json, io

# SRC pointed at a local scratch directory; set it before rerunning
SRC = os.environ.get('SUPPL_SRC', '')
# OUT pointed at a local scratch directory; set it before rerunning
OUT = os.environ.get('SUPPL_OUT', '')
# RAW pointed at a local scratch directory; set it before rerunning
RAW = os.environ.get('SUPPL_RAW', '')

data = json.loads(open(SRC, encoding="utf-8").read())
if isinstance(data, dict):
    data = data.get("result")
    if isinstance(data, str):
        data = json.loads(data)

# keep a clean machine-readable copy for the merge step
json.dump(data, open(RAW, "w", encoding="utf-8"), ensure_ascii=False)

def t(s, n):
    if not s:
        return ""
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[:n] + " ..."

buf = io.StringIO()
w = buf.write
w("# FOOD SOURCE DIGEST\n")

tot_items = 0
tot_foods = 0
for block in data:
    g = block.get("group")
    f = block.get("found") or {}
    v = block.get("verdict") or {}
    items = f.get("items") or []
    tot_items += len(items)
    w("\n" + "=" * 92 + "\n## GROUP: %s  (%d items)\n" % (g, len(items)))
    for it in items:
        foods = it.get("foods") or []
        tot_foods += len(foods)
        w("\n---\n### %s   [%s]\n" % (it.get("supplement"), it.get("availability")))
        w("- NOTE: %s\n" % t(it.get("availability_note"), 480))
        for fd in foods[:9]:
            w("  * %s | 100g: %s | %s -> %s | %s | %s\n" % (
                t(fd.get("food"), 68), t(fd.get("per_100g"), 44),
                t(fd.get("portion"), 34), t(fd.get("per_portion"), 34),
                t(fd.get("pct_rda_or_dose"), 60), t(fd.get("source"), 66)))
        if len(foods) > 9:
            w("  * (+%d more foods)\n" % (len(foods) - 9))
        w("- DOSE GAP: %s\n" % t(it.get("dose_gap"), 620))
        w("- FORM: %s\n" % t(it.get("form_caveat"), 520))
        w("- BIOAVAIL: %s\n" % t(it.get("bioavailability"), 380))

    w("\n>>> VERIFIER (%s)\n" % g)
    nc = v.get("number_checks") or []
    bad = [c for c in nc if str(c.get("verdict", "")).upper() != "OK"]
    w("NUMBER CHECKS: %d total, %d not OK\n" % (len(nc), len(bad)))
    for c in bad[:16]:
        w("  - [%s] %s | auth: %s | FIX: %s\n" % (
            c.get("verdict"), t(c.get("claim"), 92), t(c.get("authoritative_value"), 130),
            t(c.get("correction"), 210)))
    for key, lab, lim in (("misclassifications", "MISCLASSIFIED", 260),
                          ("dose_gap_errors", "DOSE GAP ERRORS", 260),
                          ("missing_foods", "MISSING FOODS", 190)):
        arr = v.get(key) or []
        if arr:
            w("%s (%d):\n" % (lab, len(arr)))
            for a in arr[:9]:
                w("  - %s\n" % t(a, lim))
    w("NET: %s\n" % t(v.get("net_assessment"), 700))

open(OUT, "w", encoding="utf-8").write(buf.getvalue())
print("digest chars:", len(buf.getvalue()))
print("groups:", len(data), " items:", tot_items, " foods:", tot_foods)
print("number checks:", sum(len((b.get("verdict") or {}).get("number_checks") or []) for b in data))
names = [i.get("supplement") for b in data for i in ((b.get("found") or {}).get("items") or [])]
print("\nsupplements covered (%d):" % len(names))
for n in names:
    print("  -", n)

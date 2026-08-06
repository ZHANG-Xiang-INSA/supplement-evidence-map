# -*- coding: utf-8 -*-
import os
from collections import Counter
from site_base import ALL, FOOD, SYN, FUNC, IX, ORDER, OUTDIR, TAKE, CONSIDER, SKIP, AVOID
import build as B

_DEFC = Counter(v['deficiency_state'] for v in FUNC.values())
_REVC = Counter(v['reversibility'] for v in FUNC.values())

R = '''# Supplement Register

An evidence-graded reference on %d dietary supplements. Each one carries a verdict, an evidence grade, the dose that
was actually tested, its pros and cons listed separately, the foods that supply it with quantities, and whether your
body already makes it.

**[Open the register](https://ZHANG-Xiang-INSA.github.io/supplement-evidence-map/)** &nbsp;|&nbsp; EN / 中文 toggle at
the top right, or press `L`. Press `/` to search.

Compiled by ZHANG Xiang. Not medical advice.

---

## The six axes

The landing page is an interactive register: search it, filter it, sort any column, click a row to open it. Every item
carries a six-cell spec strip encoding the same five answers, in the same order, everywhere it appears.

| Cell | Axis | Question it answers |
|---|---|---|
| 1 | Verdict | Should you take it? Always per group, never universal. |
| 2 | Evidence grade | How sure is the literature? **This cell is deliberately uncoloured**, because a confident answer can be no. |
| 3 | In food | Does the substance occur in ordinary food at all? |
| 4 | Dose from food | Could eating reach the dose used in trials? |
| 5 | Body makes it | Can you synthesise it yourself? |
| 6 | If you lack it | Is there a deficiency state at all, and does the damage reverse? |

Axis 6 is the one most likely to be misread, so it is worth stating plainly: **you cannot be deficient in something
that is not an essential nutrient.** There is no curcumin deficiency, no resveratrol deficiency, no ashwagandha
deficiency. %d of the %d items have no deficiency state at all, and only %d cause damage that does not fully reverse.

Axes 3, 4 and 5 answer different questions and frequently disagree. Vitamin E is **rich** in food, its 400 IU trial
dose is **out of reach** by eating, and the body **cannot** make it. All three are true at once, and only reading them
together tells you anything useful.

## What the data says

| | |
|---|---|
| Products with an explicit verdict | %d |
| Worth taking, for named groups | %d |
| Published evidence of harm | %d |
| Papers cited | 456 |
| Citations independently re-verified | 428 |
| Fabricated references found | **0** |
| Sourced food composition rows | %d |
| Food figures corrected in verification | 486 |
| Drug interaction pairs | %d across %d drug classes |
| Substances the body **cannot** make | %d |
| Substances the body makes **fully** | %d |
| Items with a named deficiency disease | %d |
| Items with **no deficiency state at all** | %d |
| Deficiencies causing **permanent** damage | %d |

Of %d products, 44 have rich food sources but only %d let you reach the supplement dose by eating. The nine substances
the body makes in full are coenzyme Q10, melatonin, collagen, glucosamine and chondroitin, NMN, nicotinamide riboside,
spermidine, alpha-lipoic acid and 5-HTP. Eight of those nine had already been placed in **Skip** on trial evidence
alone, before the synthesis data existed, so the two independent lines of evidence agree.

## Files

| File | What it is |
|---|---|
| [`index.html`](index.html) | The register. Bilingual, interactive, self-contained, works offline. |
| [`supplement-evidence-map.md`](supplement-evidence-map.md) | English markdown, same content. |
| [`supplement-evidence-map.zh.md`](supplement-evidence-map.zh.md) | 中文 markdown，内容相同。 |

## How it was built

Three research passes, each fanned out across ten or more domains, each followed by an independent adversarial checker
instructed to assume a source does not exist until it is found.

1. **Evidence.** Cochrane reviews, meta-analyses and large named trials behind every verdict. 428 citations
   re-searched; every dose re-checked against NIH ODS, EFSA and IOM/NASEM. Zero fabricated references. The checkers
   did catch evidence grades about half a grade too generous, five materially wrong doses, and several cases of a
   flattering subgroup quoted while the null overall result was omitted.
2. **Food.** %d composition rows from USDA FoodData Central, McCance and Widdowson and peer-reviewed analyses, with
   per-portion figures and the quantity of food needed to match each dose. 486 figures corrected, including matcha
   EGCG understated roughly 65-fold, krill astaxanthin quoted dry-weight against a fresh portion, chicken liver CoQ10
   labelled as chicken heart, and lion's mane composition measured on the wrong *Hericium* species.
3. **Synthesis.** Whether the body makes each substance, with pathway, enzymes and daily amount. The first attempt
   drifted because the category field was described rather than constrained, so it was re-run with a hard enumeration
   and audited to %d of %d.
4. **Function and deficiency.** What each substance does in the body, and what happens when it is lacking, with
   reversibility. Research and adversarial checking on Opus, translation on Sonnet. The checkers caught 46 errors and
   17 misclassifications, including two cases where a genetic disorder had been filed as a dietary deficiency
   (creatine transporter defects, primary CoQ10 deficiency), the hepcidin physiology written backwards, a zinc claim
   citing a paper about diabetes-related emotional distress, and a fabricated newborn-screening prevalence figure.
   150 corrections were applied.

Rows the checkers could not trace to a source are tagged **unconfirmed** rather than dropped or presented as sourced.

## Limitations

- NIH ODS fact sheets return HTTP 403 to automated retrieval, so reference intakes come from the underlying IOM/NASEM
  reports and EFSA opinions, which are the primary sources ODS itself cites.
- 86 food rows are tagged unconfirmed and eight items carry a Low data-confidence badge, because USDA FoodData Central
  returned 404s and rate limits during part of the work and the UK CoFID dataset was not retrievable.
- Several entries rest on a single unreplicated trial and say so in their Cons column.
- Food composition varies by more than an order of magnitude between samples for Brazil nut selenium and UV-treated
  mushroom vitamin D. Treat any single figure as a midpoint, not a specification.

## Licence

Text and data: [CC BY 4.0](LICENSE). Cited papers remain under their own terms.

---

This is a research synthesis, not medical advice, and it cannot replace a clinician who knows your history, medication
list and blood results. Several entries carry contraindications that matter: warfarin, SSRIs, levothyroxine,
immunosuppressants, chemotherapy, kidney disease, pregnancy.
''' % (len(ALL), len(ALL), B.COUNTS[TAKE], B.COUNTS[AVOID], B.N_ROWS,
       len(IX), len({r.get('drug_class') for r in IX}),
       B.SYN_C.get('NONE', 0), B.SYN_C.get('FULL', 0),
       _DEFC.get('CLINICAL', 0), _DEFC.get('NONE', 0), _REVC.get('IRREVERSIBLE', 0),
       _DEFC.get('NONE', 0), len(ALL), _REVC.get('IRREVERSIBLE', 0),
       len(ALL), B.N_YES, B.N_ROWS, len(SYN), len(ALL))

if __name__ == '__main__':
    p = os.path.join(OUTDIR, 'README.md')
    open(p, 'w', encoding='utf-8').write(R)
    print('README.md %d bytes' % len(R.encode('utf-8')))

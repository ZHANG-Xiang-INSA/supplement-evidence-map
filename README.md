# Dietary Supplements: an Evidence Map

An evidence-graded reference on 66 supplement products: what each one does, the dose that was actually tested,
its pros and cons listed separately, and the natural food sources with quantities.

**[Read it here](https://ZHANG-Xiang-INSA.github.io/supplement-evidence-map/)** &nbsp;|&nbsp; EN / 中文 toggle at the
top right, or press `L`.

Compiled by ZHANG Xiang. Not medical advice.

---

## What is in it

| | |
|---|---|
| Products with an explicit verdict | 66 |
| Papers cited | 456 |
| Citations independently re-verified | 428 |
| Fabricated references found | **0** |
| Sourced food composition rows | 517 |
| Food figures corrected during verification | 486 |

## The four verdicts

| Verdict | Count | Meaning |
|---|---|---|
| **TAKE** | 10 | Worth taking if you are in the group named. Evidence is strong for that group and that purpose only. |
| **CONSIDER** | 12 | Defensible in one narrow situation. Outside it there is no case. |
| **SKIP** | 30 | No good evidence for the marketed claim. A money problem rather than a safety one, except where noted. |
| **AVOID** | 14 | Published evidence of harm from randomised trials, registries or national surveillance. |

## Two things this document is built to stop you misreading

**A high evidence grade does not mean it works.** It means the literature is confident about the answer, and the
answer can be no. Selenium is Grade A here because Cochrane established with high certainty that it does *not*
prevent cancer. Read the grade together with the verdict, never on its own.

**Being rich in food does not mean the dose is reachable from food.** These are separate questions and they
frequently disagree. Of 66 products, 43 have rich food sources, yet only 20 let you reach the supplement dose by
eating and 28 do not. Vitamin E is abundant in food while a 400 IU dose is roughly 18 times the reference intake.
Coenzyme Q10 is abundant in offal while the richest food supplies under 4% of the trial dose.

## Files

| File | What it is |
|---|---|
| [`index.html`](index.html) | The report. Bilingual, self-contained, works offline. Six inline SVG figures. |
| [`supplement-evidence-map.md`](supplement-evidence-map.md) | English markdown, same content. |
| [`supplement-evidence-map.zh.md`](supplement-evidence-map.zh.md) | 中文 markdown，内容相同。 |

## How it was built

Two research passes, each fanned out across ten domains and each followed by an independent adversarial
fact-checker instructed to default to *does not exist* when a source could not be confirmed.

1. **Evidence pass.** Cochrane reviews, meta-analyses and large named RCTs for every product. 428 citations
   re-searched and re-checked; every dose re-checked against NIH ODS, EFSA and IOM/NASEM. Zero fabricated
   references were found. The checkers did catch evidence grades set about half a grade too generously, five
   materially wrong doses, and several cases of a flattering subgroup being quoted while the null overall result
   was omitted. Those are corrected.
2. **Food pass.** Composition data from USDA FoodData Central, McCance and Widdowson (UK Composition of Foods)
   and peer-reviewed composition analyses, with per-100 g and per-portion figures, plus the quantity of food
   needed to match the supplement dose. 486 figures were corrected during verification, including matcha EGCG
   understated roughly 65-fold, krill astaxanthin quoted on a dry-weight basis against a fresh portion, chicken
   liver CoQ10 labelled as chicken heart, and lion's mane composition measured on the wrong *Hericium* species.

Rows the checkers could not trace back to a cited source are tagged **unconfirmed** in the report rather than
quietly dropped or presented as sourced. Eight items carry a **Low** data-confidence badge for the same reason.

## Limitations

- NIH ODS fact sheets return HTTP 403 to automated retrieval, so reference intakes come from the underlying
  IOM/NASEM reports and EFSA opinions, which are the primary sources ODS itself cites.
- Several entries rest on a single unreplicated trial and say so in their Cons column.
- Market-size figures are unaudited commercial estimates and should be read as orders of magnitude.
- Food composition varies with cultivar, soil, season and preparation. Brazil nut selenium and UV-mushroom
  vitamin D vary by more than an order of magnitude between samples.

## Licence

Text and data: [CC BY 4.0](LICENSE). Cited papers remain under their own terms.

---

This is a research synthesis, not medical advice, and it cannot replace a clinician who knows your history,
medication list and blood results. Several entries carry contraindications that matter: warfarin, SSRIs,
levothyroxine, immunosuppressants, chemotherapy, kidney disease, pregnancy.

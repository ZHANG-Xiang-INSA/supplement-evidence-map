# Build pipeline

Regenerates `index.html`, the two markdown companions and the root `README.md`
from the research data. No dependencies beyond the Python standard library, no
build step, no network access.

```bash
cd src
py -3 assemble.py    # index.html
py -3 md.py          # supplement-evidence-map.md and .zh.md
py -3 readme.py      # ../README.md
```

Output goes to the repo root. `OUTDIR` in `site_base.py` resolves relative to
this folder, so the whole directory can be moved without breaking anything.

## Layout

| File | Role |
|---|---|
| `supp_data.py` | Evidence data: the Take and Consider tiers, with pros, cons, doses and references |
| `supp_data2.py` | Evidence data: the Skip and Avoid tiers |
| `food_manual.py` | Food entries hand-written for the five product categories that are not single substances, plus the name alias map |
| `food_load.py` | Loads `recon_out.json`, joins the Chinese translations, exposes the food axis |
| `syn_load.py` | Loads `syn_out.json`, exposes the synthesis axis and the interaction matrix |
| `design.py` | Design tokens, CSS and client-side behaviour for the register |
| `figures.py` | SVG figures. Colour comes from CSS custom properties so light and dark both work |
| `site_base.py` | Shared helpers, the five-axis vocabulary, the spec strip, the register |
| `cards.py` | Item cards: pros, cons, food table, synthesis block |
| `build.py` | Sections 09 to 12 and their data |
| `assemble.py` | Remaining sections and final page assembly |
| `md.py` | Markdown companions, generated from the same data as the HTML |
| `readme.py` | The root README |

## Data

| File | What it is |
|---|---|
| `recon_out.json` | Food composition after reconciliation: 517 rows with corrections applied |
| `syn_out.json` | Endogenous synthesis for 66 items, plus 121 interaction pairs |
| `food_raw.json` | The food pass before reconciliation, kept so the corrections stay auditable |
| `recon/`, `norm/` | Staged inputs for the reconciliation and normalisation passes |

`tools/` holds the one-off scripts used to stage and recover those datasets.
They are not part of a normal rebuild.

## Two conventions worth knowing before editing

**No raw double-quote inside a Python string literal.** Every module follows
this. The HTML is assembled with `'...'` strings that contain `"` for
attributes, so a stray `"` inside a double-quoted literal breaks the file in
ways that are tedious to find. Where a quotation mark is needed in prose, use
`&ldquo;` / `&rdquo;` in English and the standard Chinese marks in Chinese.

**Categorical fields are enumerated, not described.** The synthesis axis was
first generated with a schema that described the allowed values in prose. Agents
wrote sentences into the field and invented sixty supplements outside the brief.
Anything that feeds a filter or a badge must be constrained to a fixed set.

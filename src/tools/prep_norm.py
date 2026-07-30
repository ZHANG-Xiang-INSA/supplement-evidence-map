# -*- coding: utf-8 -*-
"""Stage per-group normalisation inputs: recovered prose plus the exact target names."""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'syn_out.json')
OUTD = os.path.join(BASE, 'norm')
os.makedirs(OUTD, exist_ok=True)

blocks = json.load(open(SRC, encoding='utf-8'))
entries = []
for b in blocks:
    if b.get('kind') == 'syn':
        entries.extend(b['final']['items'])


def trim(s, n):
    s = ' '.join(str(s or '').split())
    return s if len(s) <= n else s[:n] + ' ...'


slim = [{
    'supplement': e.get('supplement'),
    'endogenous': trim(e.get('endogenous'), 200),
    'endogenous_note': trim(e.get('endogenous_note'), 620),
    'endogenous_note_zh': trim(e.get('endogenous_note_zh'), 400),
    'pathway': trim(e.get('pathway'), 340),
    'pathway_zh': trim(e.get('pathway_zh'), 240),
    'daily_amount': trim(e.get('daily_amount'), 220),
    'daily_amount_zh': trim(e.get('daily_amount_zh'), 160),
    'still_matters_when': trim(e.get('still_matters_when'), 400),
    'still_matters_when_zh': trim(e.get('still_matters_when_zh'), 280),
    'source': trim(e.get('source'), 160),
} for e in entries]

GROUPS = {
 'vitamins': ['Vitamin D3 (cholecalciferol)', 'Vitamin E at or above 400 IU/d',
              'Preformed vitamin A at or above 10,000 IU', 'Beta-carotene supplements',
              'Vitamin K2 (MK-7 and MK-4)', 'Folic acid', 'Vitamin B12 (cobalamin)',
              'High-dose vitamin B6', 'Vitamin C', 'Multivitamin / multimineral',
              'High-dose folic acid plus B12 for cardiovascular prevention'],
 'minerals-omega': ['Iron', 'Iodine', 'Zinc lozenges', 'Selenium at 200 µg/d', 'Magnesium',
                    'Calcium supplements on top of an adequate diet', 'Omega-3 (EPA and DHA)',
                    'Krill oil', 'Cod liver oil', 'ALA from flaxseed, chia or walnut oil',
                    'Algal oil (vegan DHA and EPA)'],
 'performance': ['Creatine monohydrate', 'Protein powder', 'Beta-alanine', 'Caffeine',
                 'Dietary nitrate / beetroot', 'HMB', 'Quercetin and taurine', 'Collagen peptides',
                 'Glucosamine and chondroitin', 'L-glutamine for gut repair',
                 'Bodybuilding and test-booster products'],
 'longevity': ['NMN (nicotinamide mononucleotide)', 'Nicotinamide riboside (NR)', 'Resveratrol',
               'Spermidine', 'Coenzyme Q10 / ubiquinol', 'Alpha-lipoic acid',
               'MSM (methylsulfonylmethane)', 'Astaxanthin', 'Curcumin / turmeric extract',
               'Green tea extract (EGCG)', 'Antioxidants during chemotherapy'],
 'neuro-gut': ['Melatonin', 'Berberine', 'Ashwagandha (Withania somnifera)', 'Rhodiola rosea',
               'Valerian', 'Ginkgo biloba', 'Bacopa monnieri', "Lion's mane (Hericium erinaceus)",
               "St John's wort", '5-HTP', 'Saffron, SAMe and other mood botanicals',
               'Psyllium husk (ispaghula)', 'Wheat bran and insoluble fibre supplements for IBS',
               'Prebiotics: inulin, FOS, GOS', 'Probiotics, named strain only',
               'Generic multi-strain probiotic blends', 'B. infantis 35624 (single strain)',
               'Lactase and pancreatic enzymes', 'Over-the-counter digestive enzyme blends',
               'Probiotics in critical illness', 'Sexual-enhancement products',
               'Weight-loss, fat-burner and energy blends'],
}


def toks(s):
    return set(re.findall(r'[a-z0-9]+', str(s).lower())) - {'the', 'and', 'of', 'a', 'or', 'for', 'at', 'in'}


total = 0
for key, names in GROUPS.items():
    want = [toks(n) for n in names]
    rel = []
    for e in slim:
        et = toks(e['supplement'])
        if any(len(et & w) >= 1 and (len(et & w) / max(1, min(len(et), len(w)))) >= 0.34 for w in want):
            rel.append(e)
    # always include the definition/rules rows, they carry the classification logic
    rel += [e for e in slim if 'definition' in str(e['supplement']).lower() and e not in rel]
    payload = {'target_names': names, 'recovered_entries': rel}
    p = os.path.join(OUTD, 'in_%s.json' % key)
    json.dump(payload, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    total += len(names)
    print('%-16s targets=%-3d matched_entries=%-4d %d KB'
          % (key, len(names), len(rel), os.path.getsize(p) // 1024))

# a shared pool for anything a group could not match locally
json.dump(slim, open(os.path.join(OUTD, 'all_entries.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('\ntarget names total:', total)
print('shared pool:', len(slim), 'entries,',
      os.path.getsize(os.path.join(OUTD, 'all_entries.json')) // 1024, 'KB')

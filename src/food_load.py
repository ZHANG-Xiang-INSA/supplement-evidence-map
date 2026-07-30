# -*- coding: utf-8 -*-
"""Loads the reconciled + translated food data and joins it to the document items."""
import json, os, glob
from food_manual import ALIASES, MANUAL

BASE = os.path.dirname(os.path.abspath(__file__))

FOOD_STATUS_META = {
    'RICH':      ('Rich food sources', '食物来源丰富', 'good'),
    'TRACE':     ('Trace amounts only', '仅有痕量', 'warn'),
    'SYNTHETIC': ('No food source, manufactured', '无食物来源，人工合成', 'bad'),
    'NOT_FOOD':  ('From a plant not eaten as food', '来自不作食物食用的植物', 'mute'),
}

DOSE_META = {
    'YES':     ('Dose reachable by eating', '靠吃可以达到剂量', 'good'),
    'PARTIAL': ('Dose partly reachable', '靠吃只能部分达到', 'warn'),
    'NO':      ('Dose NOT reachable by eating', '靠吃达不到剂量', 'bad'),
    'NA':      ('No dose to compare', '没有可比的剂量', 'mute'),
}


def _find_output():
    """Locate the reconcile workflow output file."""
    cand = sorted(glob.glob(os.path.join(BASE, 'recon_out*.json')))
    if cand:
        return cand[-1]
    tasks = os.path.join(os.path.dirname(os.path.dirname(BASE)), 'tasks')
    return None


def load(path=None):
    """Returns {document_supplement_name: merged_food_dict}."""
    path = path or os.path.join(BASE, 'recon_out.json')
    if not os.path.exists(path):
        raise SystemExit('reconciled food data not found at %s' % path)
    data = json.load(open(path, encoding='utf-8'))
    if isinstance(data, dict):
        data = data.get('result')
        if isinstance(data, str):
            data = json.loads(data)

    out = {}
    warnings = []
    for block in data:
        en_items = ((block.get('en') or {}).get('items')) or []
        zh_items = ((block.get('zh') or {}).get('items')) or []
        zmap = {z.get('supplement'): z for z in zh_items}
        for it in en_items:
            name = it.get('supplement')
            z = zmap.get(name) or {}
            merged = dict(it)
            merged['supplement_zh'] = z.get('supplement_zh', '')
            for f in ('food_status_note', 'dose_from_food_note', 'form_caveat',
                      'bioavailability', 'data_confidence'):
                merged[f + '_zh'] = z.get(f + '_zh', '')
            # align translated food rows by index, defensively
            fz = {int(r.get('i', -1)): r for r in (z.get('foods_zh') or []) if r.get('i') is not None}
            rows = []
            for i, fd in enumerate(merged.get('foods') or []):
                tr = fz.get(i, {})
                rows.append({
                    'food': fd.get('food', ''), 'food_zh': tr.get('food_zh', ''),
                    'per_100g': fd.get('per_100g', ''),
                    'portion': fd.get('portion', ''), 'portion_zh': tr.get('portion_zh', ''),
                    'per_portion': fd.get('per_portion', ''),
                    'pct': fd.get('pct_rda_or_dose', ''), 'pct_zh': tr.get('pct_zh', ''),
                    'source': fd.get('source', ''),
                })
            if len(fz) and len(fz) != len(rows):
                warnings.append('%s: %d english foods but %d translated rows' % (name, len(rows), len(fz)))
            merged['food_rows'] = rows
            key = ALIASES.get(name, name)
            out[key] = merged

    for m in MANUAL:
        m2 = dict(m)
        m2['food_rows'] = []
        out[m2['supplement']] = m2

    return out, warnings


if __name__ == '__main__':
    food, warns = load()
    print('food entries loaded:', len(food))
    from collections import Counter
    print('food_status   :', dict(Counter(v['food_status'] for v in food.values())))
    print('dose_from_food:', dict(Counter(v['dose_from_food'] for v in food.values())))
    print('total food rows:', sum(len(v['food_rows']) for v in food.values()))
    print('corrections applied:', sum(len(v.get('corrections_applied') or []) for v in food.values()))
    print('LOW confidence items:', [k for k, v in food.items()
                                    if str(v.get('data_confidence', '')).upper().startswith('LOW')])
    if warns:
        print('\nWARNINGS:')
        for w in warns:
            print('  !', w)

    # coverage against the document
    from supp_data import ITEMS
    from supp_data2 import ITEMS2
    names = {i['en'] for i in (ITEMS + ITEMS2)}
    missing = sorted(names - set(food))
    extra = sorted(set(food) - names)
    print('\ndocument items:', len(names), ' with food data:', len(names & set(food)))
    if missing:
        print('MISSING food data:')
        for m in missing:
            print('  -', m)
    if extra:
        print('food data with no matching item:')
        for e in extra:
            print('  -', e)

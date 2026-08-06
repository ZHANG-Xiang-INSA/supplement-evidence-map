# -*- coding: utf-8 -*-
"""Loads the function and deficiency axis.

Two independent facts per item: what it does in the body, and what happens when
it is lacking. The second only exists for essential nutrients; for a plant
compound the honest answer is that no deficiency state exists at all.
"""
import json, os, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# Does a deficiency state exist at all?
DEF_META = {
    'CLINICAL':   ('Named deficiency disease', '有明确的缺乏症', 'f',
                   'A recognised deficiency disease exists and is described in the clinical literature',
                   '存在公认的缺乏性疾病，临床文献中有明确描述'),
    'FUNCTIONAL': ('Low status causes dysfunction', '偏低会引起功能异常', 'c',
                   'No named disease, but low status causes measurable dysfunction',
                   '没有命名的疾病，但状态偏低会引起可测量的功能异常'),
    'NONE':       ('No deficiency state exists', '不存在缺乏状态', 'n',
                   'Not an essential nutrient. You cannot be deficient in this',
                   '不是必需营养素。不存在“缺乏”这回事'),
    'NA':         ('Mixed product', '复合产品', 'n',
                   'A compound product whose constituents each have their own entry',
                   '复合产品，其各成分在别处各有条目'),
}

# If you do become deficient, does repletion undo the damage?
REV_META = {
    'FULL':         ('Fully reversible', '完全可逆', 'p',
                     'Repletion corrects the damage completely', '补足后损害可完全纠正'),
    'PARTIAL':      ('Partly reversible', '部分可逆', 'c',
                     'Repletion halts progression; some deficit persists', '补足可阻止进展，但部分损害残留'),
    'IRREVERSIBLE': ('Permanent damage', '损害不可逆', 'f',
                     'Damage is permanent once established. The window closes',
                     '一旦形成即为永久损害，窗口会关闭'),
    'NA':           ('n/a', '不适用', 'n',
                     'No deficiency state, so nothing to reverse', '不存在缺乏状态，无所谓可逆'),
}

_DEF_RANK = {'CLINICAL': 0, 'FUNCTIONAL': 1, 'NONE': 2, 'NA': 3}
_REV_RANK = {'IRREVERSIBLE': 0, 'PARTIAL': 1, 'FULL': 2, 'NA': 3}


def _raw(path=None):
    path = path or os.path.join(BASE, 'func_out.json')
    if not os.path.exists(path):
        return []
    d = json.load(open(path, encoding='utf-8'))
    if isinstance(d, dict):
        d = d.get('result')
        if isinstance(d, str):
            d = json.loads(d)
    return d or []


def load(path=None):
    """{supplement_name: merged entry with _zh fields}"""
    out, warn = {}, []
    for b in _raw(path):
        en_items = ((b.get('en') or {}).get('items')) or []
        zh_items = ((b.get('zh') or {}).get('items')) or []
        zmap = {z.get('supplement'): z for z in zh_items}
        for it in en_items:
            name = it.get('supplement')
            z = zmap.get(name) or {}
            m = dict(it)
            m['supplement_zh'] = z.get('supplement_zh', '')
            for f in ('function_short', 'function_full', 'deficiency_name', 'deficiency_early',
                      'deficiency_severe', 'reversibility_note', 'at_risk', 'prevalence'):
                m[f + '_zh'] = z.get(f + '_zh', '')
            if not z:
                warn.append('%s: no Chinese translation' % name)
            out[name] = m
    return out, warn


def irreversible(func):
    """The entries a reader most needs to see, worst first."""
    rows = [v for v in func.values() if str(v.get('reversibility', '')).upper() in ('IRREVERSIBLE', 'PARTIAL')]
    rows.sort(key=lambda v: (_REV_RANK.get(str(v.get('reversibility', '')).upper(), 9),
                             _DEF_RANK.get(str(v.get('deficiency_state', '')).upper(), 9),
                             str(v.get('supplement', ''))))
    return rows


if __name__ == '__main__':
    from collections import Counter
    f, warn = load()
    print('entries          :', len(f))
    print('deficiency_state :', dict(Counter(v['deficiency_state'] for v in f.values())))
    print('reversibility    :', dict(Counter(v['reversibility'] for v in f.values())))
    print('corrections      :', sum(len(v.get('corrections_applied') or []) for v in f.values()))
    bad = [k for k, v in f.values.__self__.items()
           if v['deficiency_state'] == 'NONE' and str(v.get('reversibility')).upper() != 'NA']
    if bad:
        print('INCONSISTENT (NONE but reversibility not NA):', bad)
    print()
    print('=== irreversible, the ones that matter ===')
    for v in irreversible(f):
        if v['reversibility'] != 'IRREVERSIBLE':
            continue
        print('  %-34s %s' % (v['supplement'][:34], str(v.get('reversibility_note'))[:110]))
    print()
    from supp_data import ITEMS
    from supp_data2 import ITEMS2
    names = {i['en'] for i in (ITEMS + ITEMS2)}
    missing = sorted(names - set(f))
    extra = sorted(set(f) - names)
    print('document items:', len(names), ' with function data:', len(names & set(f)))
    for m in missing:
        print('  MISSING:', m)
    for e in extra:
        print('  EXTRA  :', e)
    for w in warn:
        print('  !', w)

# -*- coding: utf-8 -*-
"""Loads the endogenous-synthesis axis and the disambiguated interaction matrix."""
import json, os, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# Every label names who does what to whom. That is the whole point: the previous
# version bundled opposite directions into one cell and left the reader guessing.
DIRECTION_META = {
    'RAISES_DRUG_EFFECT':            ('Supplement strengthens the drug', '补充剂增强药效', 'f'),
    'LOWERS_DRUG_EFFECT':            ('Supplement weakens the drug', '补充剂减弱药效', 'f'),
    'RAISES_HARM_RISK':              ('Combination raises risk of harm', '合用增加伤害风险', 'f'),
    'REDUCES_DRUG_ABSORPTION':       ('Supplement blocks the drug', '补充剂阻碍药物吸收', 'c'),
    'REDUCES_SUPPLEMENT_ABSORPTION': ('Drug blocks the supplement', '药物阻碍补充剂吸收', 'c'),
    'RAISES_SUPPLEMENT_EFFECT':      ('Drug strengthens the supplement', '药物增强补充剂作用', 'c'),
    'INCREASES_SUPPLEMENT_LOSS':     ('Drug depletes the supplement', '药物使补充剂流失', 'c'),
}

SEVERITY_META = {
    'AVOID':           ('Do not combine', '不要合用', 'f'),
    'MONITOR':         ('Only with monitoring', '需在监测下使用', 'c'),
    'SEPARATE_TIMING': ('Fine if taken hours apart', '间隔几小时即可', 'p'),
    'INFORM_ONLY':     ('Worth knowing, no restriction', '知道即可，无需限制', 'n'),
}

_SEV_RANK = {'AVOID': 0, 'MONITOR': 1, 'SEPARATE_TIMING': 2, 'INFORM_ONLY': 3}


def _find():
    c = sorted(glob.glob(os.path.join(BASE, 'syn_out*.json')))
    return c[-1] if c else None


def _raw():
    p = _find()
    if not p:
        return []
    data = json.load(open(p, encoding='utf-8'))
    if isinstance(data, dict):
        data = data.get('result')
        if isinstance(data, str):
            data = json.loads(data)
    return data or []


def synthesis():
    """{supplement_name: {endogenous, notes, pathway, ...}}"""
    out = {}
    for b in _raw():
        if b.get('kind') != 'syn':
            continue
        for it in ((b.get('final') or {}).get('items') or []):
            out[it.get('supplement')] = it
    return out


def interactions():
    """Sorted list of interaction rows, most severe first."""
    rows = []
    for b in _raw():
        if b.get('kind') != 'ix':
            continue
        rows.extend(((b.get('final') or {}).get('pairs') or []))
    rows.sort(key=lambda r: (_SEV_RANK.get(str(r.get('severity', '')).upper(), 9),
                             str(r.get('drug_class', '')),
                             str(r.get('supplement', ''))))
    return rows


if __name__ == '__main__':
    from collections import Counter
    s = synthesis()
    ix = interactions()
    print('synthesis entries :', len(s))
    print('endogenous classes:', dict(Counter(v.get('endogenous') for v in s.values())))
    print('interaction rows  :', len(ix))
    print('by severity       :', dict(Counter(r.get('severity') for r in ix)))
    print('by direction      :', dict(Counter(r.get('direction') for r in ix)))
    print('drug classes      :', len({r.get('drug_class') for r in ix}))

    from supp_data import ITEMS
    from supp_data2 import ITEMS2
    names = {i['en'] for i in (ITEMS + ITEMS2)}
    missing = sorted(names - set(s))
    extra = sorted(set(s) - names)
    print()
    print('document items:', len(names), ' with synthesis data:', len(names & set(s)))
    if missing:
        print('MISSING synthesis:')
        for m in missing:
            print('  -', m)
    if extra:
        print('synthesis with no matching item:')
        for e in extra:
            print('  -', e)
    bad = [k for k, v in s.items() if str(v.get('endogenous', '')).upper() not in
           ('NONE', 'PARTIAL', 'FULL', 'CONDITIONAL', 'NA')]
    if bad:
        print('unexpected endogenous values:', bad)
    badsev = [r.get('supplement') for r in ix if str(r.get('severity', '')).upper() not in _SEV_RANK]
    if badsev:
        print('unexpected severities:', badsev[:8])
    baddir = [r.get('supplement') for r in ix if str(r.get('direction', '')).upper() not in DIRECTION_META]
    if baddir:
        print('unexpected directions:', baddir[:8])

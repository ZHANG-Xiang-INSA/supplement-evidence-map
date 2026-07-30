# -*- coding: utf-8 -*-
"""Recover the finalise-stage results from the workflow journal.

The finalise stage is identifiable by the presence of the _zh fields; the
earlier research stage has the same shape without them.
"""
import json, os

# J pointed at a local scratch directory; set it before rerunning
J = os.environ.get('SUPPL_JOURNAL', '')   # path to the workflow journal.jsonl
# OUT pointed at a local scratch directory; set it before rerunning
OUT = os.environ.get('SUPPL_OUT', os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'syn_out.json'))

recs = []
for line in open(J, encoding='utf-8'):
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
    except Exception:
        continue
    if d.get('type') == 'result':
        v = d.get('value')
        if v is None:
            v = d.get('result')
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except Exception:
                continue
        if isinstance(v, dict):
            recs.append(v)

syn_final, ix_final = [], []
for v in recs:
    if 'items' in v and isinstance(v['items'], list) and v['items']:
        if any('endogenous_note_zh' in (it or {}) for it in v['items']):
            syn_final.append(v)
    elif 'pairs' in v and isinstance(v['pairs'], list) and v['pairs']:
        if any('what_happens_zh' in (p or {}) for p in v['pairs']):
            ix_final.append(v)

print('finalised synthesis blocks :', len(syn_final))
print('finalised interaction blocks:', len(ix_final))

# dedupe: keep the largest block per supplement set / keep all unique pairs
seen_sup, syn_items = set(), []
for blk in syn_final:
    for it in blk['items']:
        n = it.get('supplement')
        if n and n not in seen_sup:
            seen_sup.add(n)
            syn_items.append(it)

seen_pair, ix_pairs = set(), []
for blk in ix_final:
    for p in blk['pairs']:
        k = (p.get('drug_class'), p.get('supplement'), p.get('direction'))
        if k not in seen_pair:
            seen_pair.add(k)
            ix_pairs.append(p)

print('unique synthesis entries :', len(syn_items))
print('unique interaction rows  :', len(ix_pairs))

blocks = [{'group': 'recovered-syn', 'kind': 'syn', 'final': {'items': syn_items}, 'check': {}},
          {'group': 'recovered-ix', 'kind': 'ix', 'final': {'pairs': ix_pairs}, 'check': {}}]
json.dump(blocks, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print('written:', OUT)

# -*- coding: utf-8 -*-
"""Split the food workflow output into per-group reconciliation inputs."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(BASE, 'food_raw.json'), encoding='utf-8'))

os.makedirs(os.path.join(BASE, 'recon'), exist_ok=True)
manifest = []
for b in data:
    g = b['group']
    payload = {'group': g, 'items_assigned': b.get('items', []),
               'submission': b.get('found', {}), 'verification_report': b.get('verdict', {})}
    p = os.path.join(BASE, 'recon', 'in_%s.json' % g)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    n_items = len(payload['submission'].get('items', []))
    n_bad = len([c for c in payload['verification_report'].get('number_checks', [])
                 if str(c.get('verdict', '')).upper() != 'OK'])
    manifest.append({'group': g, 'path': p, 'items': n_items, 'corrections_pending': n_bad})
    print('%-22s items=%-3d pending-corrections=%-3d  %d KB' % (g, n_items, n_bad, os.path.getsize(p) // 1024))

with open(os.path.join(BASE, 'recon', 'manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)
print('\ntotal pending corrections:', sum(m['corrections_pending'] for m in manifest))

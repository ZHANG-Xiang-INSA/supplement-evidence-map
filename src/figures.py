# -*- coding: utf-8 -*-
"""SVG figures. Colour comes from CSS custom properties so light and dark both work.

Convention: no raw double-quote inside any Python string literal.
"""
import math, html as HH

SVG_CSS = r'''
svg.fig text{font-family:var(--data);fill:var(--muted)}
svg.fig .lab{font-family:var(--body);font-size:11.5px;fill:var(--ink)}
svg.fig .tick,svg.fig .sub{font-size:10.5px;fill:var(--faint)}
svg.fig .axlab{font-size:10.5px;fill:var(--muted);letter-spacing:.08em;text-transform:uppercase}
svg.fig .val{font-size:11px;font-weight:700}
svg.fig .hint{font-size:10px;letter-spacing:.06em;text-transform:uppercase}
svg.fig .big{font-family:var(--display);font-size:25px;font-weight:600;fill:var(--ink)}
svg.fig .band{fill:var(--rule-2)}
svg.fig .grid{stroke:var(--rule-2);stroke-width:1}
svg.fig .zero{stroke:var(--ink);stroke-width:1;stroke-dasharray:2 3;opacity:.55}
svg.fig .p{stroke:var(--pass)} svg.fig .n{stroke:var(--faint)} svg.fig .f{stroke:var(--fail)}
svg.fig circle.p{fill:var(--pass);stroke:none} svg.fig circle.n{fill:var(--faint);stroke:none}
svg.fig circle.f{fill:var(--fail);stroke:none}
svg.fig text.p{fill:var(--pass)} svg.fig text.n{fill:var(--faint)} svg.fig text.f{fill:var(--fail)}
svg.fig rect.bg{fill:var(--rule-2)}
svg.fig rect.p{fill:var(--pass)} svg.fig rect.c{fill:var(--caution)}
svg.fig rect.f{fill:var(--fail)} svg.fig rect.n{fill:var(--faint)}
svg.fig .inbar{font-size:11px;font-weight:700;fill:var(--panel)}
'''

FOREST = [
    ('Folic acid, neural tube defects', '叶酸，神经管缺陷', 0.31, 0.17, 0.58, 'p'),
    ('Probiotics, paediatric antibiotic diarrhoea', '益生菌，儿童抗生素相关腹泻', 0.45, 0.36, 0.56, 'p'),
    ('CoQ10 in heart failure (Q-SYMBIO)', '辅酶Q10 治心衰（Q-SYMBIO）', 0.50, 0.32, 0.80, 'p'),
    ('Probiotics, C. difficile diarrhoea', '益生菌，艰难梭菌相关腹泻', 0.50, 0.38, 0.64, 'p'),
    ('Omega-3 in pregnancy, birth before 34 wk', '孕期omega-3，34周前早产', 0.58, 0.44, 0.77, 'p'),
    ('Icosapent ethyl 4 g (REDUCE-IT)', '高纯EPA 4克（REDUCE-IT）', 0.75, 0.68, 0.83, 'p'),
    ('Vitamin D + calcium, hip fracture', '维生素D+钙，髋部骨折', 0.84, 0.74, 0.96, 'p'),
    ('Calcium + D, hip fracture (WHI)', '钙+维D，髋部骨折（WHI）', 0.88, 0.72, 1.08, 'n'),
    ('Omega-3 1 g, CV events (VITAL)', 'omega-3 1克，心血管事件（VITAL）', 0.92, 0.80, 1.06, 'n'),
    ('Vitamin D 2000 IU, cancer (VITAL)', '维生素D 2000IU，癌症（VITAL）', 0.96, 0.88, 1.06, 'n'),
    ('Omega-3, all-cause mortality (Cochrane)', 'omega-3，全因死亡（Cochrane）', 0.97, 0.93, 1.01, 'n'),
    ('Omega-3 in diabetes (ASCEND)', '糖尿病人群omega-3（ASCEND）', 0.97, 0.87, 1.08, 'n'),
    ('Vitamin D, major CVD (VITAL)', '维生素D，主要心血管病（VITAL）', 0.97, 0.85, 1.12, 'n'),
    ('Omega-3 4 g (STRENGTH)', 'omega-3 4克（STRENGTH）', 0.99, 0.90, 1.09, 'n'),
    ('Selenium, any cancer (Cochrane)', '硒，任何癌症（Cochrane）', 1.01, 0.93, 1.10, 'n'),
    ('Vitamin D monthly bolus (D-Health)', '维生素D 每月冲击（D-Health）', 1.04, 0.93, 1.18, 'n'),
    ('Selenium, prostate cancer (SELECT)', '硒，前列腺癌（SELECT）', 1.09, 0.93, 1.27, 'n'),
    ('Ginkgo 240 mg, dementia (GEM)', '银杏240毫克，痴呆（GEM）', 1.12, 0.94, 1.33, 'n'),
    ('Daily multivitamin, all-cause mortality', '每日复合维生素，全因死亡', 1.04, 1.02, 1.07, 'f'),
    ('Vitamin A + beta-carotene, death (CARET)', '维生素A+β胡萝卜素，死亡（CARET）', 1.17, 1.03, 1.33, 'f'),
    ('Vitamin E 400 IU, prostate cancer (SELECT)', '维生素E 400IU，前列腺癌（SELECT）', 1.17, 1.004, 1.36, 'f'),
    ('Beta-carotene 20 mg, lung cancer (ATBC)', 'β胡萝卜素20毫克，肺癌（ATBC）', 1.18, 1.03, 1.36, 'f'),
    ('Vitamin E, haemorrhagic stroke', '维生素E，出血性卒中', 1.22, 1.00, 1.48, 'f'),
    ('Marine omega-3, atrial fibrillation', '海洋omega-3，房颤', 1.25, 1.07, 1.46, 'f'),
    ('Beta-carotene + vit A, lung cancer (CARET)', 'β胡萝卜素+维A，肺癌（CARET）', 1.28, 1.04, 1.57, 'f'),
    ('Calcium supplements, myocardial infarction', '钙补充剂，心肌梗死', 1.31, 1.02, 1.67, 'f'),
    ('Folic acid + B12, cancer mortality', '叶酸+B12，癌症死亡', 1.38, 1.07, 1.79, 'f'),
    ('Selenium, incident type 2 diabetes', '硒，新发2型糖尿病', 1.55, 1.03, 2.33, 'f'),
    ('Synbiotic in severe pancreatitis, mortality', '重症胰腺炎用合生元，死亡', 2.53, 1.22, 5.25, 'f'),
]


def forest():
    W, ROW = 960, 24.0
    PL, PR, PT, PB = 352, 74, 54, 46
    LO, HI = 0.15, 6.0
    n = len(FOREST)
    H = PT + n * ROW + PB
    lg = math.log

    def x(v):
        v = min(max(v, LO), HI)
        return PL + (lg(v) - lg(LO)) / (lg(HI) - lg(LO)) * (W - PL - PR)

    s = ['<svg viewBox="0 0 %d %.0f" class="fig" role="img">' % (W, H),
         '<title>Landmark supplement trials</title>']
    for i in range(n):
        if i % 2 == 0:
            s.append('<rect class="band" x="0" y="%.1f" width="%d" height="%.1f"/>' % (PT + i * ROW - 2, W, ROW))
    for t in (0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0):
        xx = x(t)
        s.append('<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                 % ('zero' if t == 1.0 else 'grid', xx, PT - 12, xx, PT + n * ROW - 4))
        s.append('<text class="tick" x="%.1f" y="%.1f" text-anchor="middle">%g</text>' % (xx, PT - 18, t))
    s.append('<text class="axlab" x="%.1f" y="%.1f" text-anchor="middle">RR / HR &#183; log</text>' % (x(1.0), PT - 34))
    s.append('<text class="hint p" x="%.1f" y="%.1f" text-anchor="end">&#9664; fewer events</text>' % (x(1.0) - 12, PT + n * ROW + 20))
    s.append('<text class="hint f" x="%.1f" y="%.1f" text-anchor="start">more events &#9654;</text>' % (x(1.0) + 12, PT + n * ROW + 20))
    for i, (le, lz, est, lo, hi, k) in enumerate(FOREST):
        y = PT + i * ROW + ROW / 2 - 3
        s.append('<text class="lab en" x="%d" y="%.1f" text-anchor="end">%s</text>' % (PL - 12, y + 4, HH.escape(le)))
        s.append('<text class="lab zh" x="%d" y="%.1f" text-anchor="end">%s</text>' % (PL - 12, y + 4, HH.escape(lz)))
        s.append('<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke-width="1.8"/>' % (k, x(lo), y, x(hi), y))
        for e in (lo, hi):
            s.append('<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke-width="1.8"/>' % (k, x(e), y - 3.5, x(e), y + 3.5))
        s.append('<circle class="%s" cx="%.1f" cy="%.1f" r="3.6"/>' % (k, x(est), y))
        s.append('<text class="val %s" x="%d" y="%.1f">%.2f</text>' % (k, W - PR + 9, y + 4, est))
    s.append('</svg>')
    return '\n'.join(s)


def stacked(title_en, title_zh, rowlabels, doses, grid, note_en, note_zh, W=940):
    """Generic stacked-bar cross-tab."""
    ROW = 40
    PL, PR, PT, PB = 168, 26, 88, 54
    n = len(rowlabels)
    H = PT + n * ROW + PB
    barw = W - PL - PR
    total = sum(grid.values()) or 1
    s = ['<svg viewBox="0 0 %d %d" class="fig" role="img">' % (W, H),
         '<title>%s</title>' % HH.escape(title_en)]
    s.append('<text class="axlab" x="%d" y="22">%s</text>' % (PL, HH.escape(title_en)))
    for j, (key, lab_en, lab_zh, cls) in enumerate(doses):
        xx = PL + j * 152
        s.append('<rect class="%s" x="%d" y="40" width="10" height="10" rx="2"/>' % (cls, xx))
        s.append('<text class="sub en" x="%d" y="49">%s</text>' % (xx + 15, HH.escape(lab_en)))
        s.append('<text class="sub zh" x="%d" y="49">%s</text>' % (xx + 15, HH.escape(lab_zh)))
    for i, (rkey, ren, rzh) in enumerate(rowlabels):
        y = PT + i * ROW
        s.append('<text class="lab en" x="%d" y="%d" text-anchor="end">%s</text>' % (PL - 12, y + 19, HH.escape(ren)))
        s.append('<text class="lab zh" x="%d" y="%d" text-anchor="end">%s</text>' % (PL - 12, y + 19, HH.escape(rzh)))
        xx = PL
        for key, _, _, cls in doses:
            c = grid.get((rkey, key), 0)
            if not c:
                continue
            w = barw * c / float(total)
            s.append('<rect class="%s" x="%.1f" y="%d" width="%.1f" height="24" rx="2"/>' % (cls, xx, y + 3, max(w - 2, 2)))
            if w > 20:
                s.append('<text class="inbar" x="%.1f" y="%d" text-anchor="middle">%d</text>' % (xx + (w - 2) / 2, y + 20, c))
            xx += w
    s.append('<text class="sub en" x="%d" y="%d">%s</text>' % (PL, PT + n * ROW + 24, HH.escape(note_en)))
    s.append('<text class="sub zh" x="%d" y="%d">%s</text>' % (PL, PT + n * ROW + 24, HH.escape(note_zh)))
    s.append('</svg>')
    return '\n'.join(s)


def hbars(title_en, title_zh, rows, W=940, labelw=300, note=None):
    """rows: list of (label_en, label_zh, pct, sub_en, sub_zh, cls)"""
    ROW = 46
    PL, PR, PT, PB = labelw, 54, 40, 22
    n = len(rows)
    H = PT + n * ROW + PB
    barw = W - PL - PR
    s = ['<svg viewBox="0 0 %d %d" class="fig" role="img">' % (W, H),
         '<title>%s</title>' % HH.escape(title_en)]
    s.append('<text class="axlab" x="%d" y="18">%s</text>' % (PL, HH.escape(title_en)))
    for i, (le, lz, pct, se, sz, cls) in enumerate(rows):
        y = PT + i * ROW
        s.append('<text class="lab en" x="%d" y="%d" text-anchor="end">%s</text>' % (PL - 12, y + 16, HH.escape(le)))
        s.append('<text class="lab zh" x="%d" y="%d" text-anchor="end">%s</text>' % (PL - 12, y + 16, HH.escape(lz)))
        if se:
            s.append('<text class="sub en" x="%d" y="%d" text-anchor="end">%s</text>' % (PL - 12, y + 30, HH.escape(se)))
            s.append('<text class="sub zh" x="%d" y="%d" text-anchor="end">%s</text>' % (PL - 12, y + 30, HH.escape(sz)))
        s.append('<rect class="bg" x="%d" y="%d" width="%d" height="18" rx="2"/>' % (PL, y + 5, barw))
        s.append('<rect class="%s" x="%d" y="%d" width="%.1f" height="18" rx="2"/>' % (cls, PL, y + 5, barw * pct / 100.0))
        s.append('<text class="tick" x="%.1f" y="%d">%d%%</text>' % (PL + barw * pct / 100.0 + 8, y + 19, pct))
    s.append('</svg>')
    return '\n'.join(s)


UL = [
    ('Vitamin B6', '维生素B6', '100 mg', '12 mg', 100, 12),
    ('Vitamin E', '维生素E', '1000 mg', '300 mg', 1000, 300),
    ('Selenium', '硒', '400 µg', '255 µg', 400, 255),
    ('Iodine', '碘', '1100 µg', '600 µg', 1100, 600),
    ('Zinc', '锌', '40 mg', '25 mg', 40, 25),
    ('Magnesium', '镁', '350 mg', '250 mg', 350, 250),
    ('Vitamin D', '维生素D', '100 µg', '100 µg', 100, 100),
]


def ulgap():
    W, ROW = 940, 40
    PL, PR, PT, PB = 168, 140, 40, 22
    n = len(UL)
    H = PT + n * ROW + PB
    barw = W - PL - PR
    s = ['<svg viewBox="0 0 %d %d" class="fig" role="img">' % (W, H),
         '<title>US versus EU upper limits</title>']
    s.append('<text class="axlab" x="%d" y="18">EU limit as a share of the US limit</text>' % PL)
    for i, (ne, nz, us_s, eu_s, us, eu) in enumerate(UL):
        y = PT + i * ROW
        frac = eu / float(us)
        cls = 'f' if frac <= 0.25 else ('c' if frac < 0.8 else 'p')
        s.append('<text class="lab en" x="%d" y="%d" text-anchor="end">%s</text>' % (PL - 12, y + 19, HH.escape(ne)))
        s.append('<text class="lab zh" x="%d" y="%d" text-anchor="end">%s</text>' % (PL - 12, y + 19, HH.escape(nz)))
        s.append('<rect class="bg" x="%d" y="%d" width="%d" height="20" rx="2"/>' % (PL, y + 4, barw))
        s.append('<rect class="%s" x="%d" y="%d" width="%.1f" height="20" rx="2"/>' % (cls, PL, y + 4, barw * frac))
        s.append('<text class="tick" x="%d" y="%d">US %s &#183; EU %s</text>' % (W - PR + 8, y + 18, us_s, eu_s))
        pct = '%d%%' % round(frac * 100)
        if barw * frac < 44:
            s.append('<text class="tick" x="%.1f" y="%d">%s</text>' % (PL + barw * frac + 8, y + 18, pct))
        else:
            s.append('<text class="inbar" x="%.1f" y="%d" text-anchor="end">%s</text>' % (PL + barw * frac - 8, y + 18, pct))
    s.append('</svg>')
    return '\n'.join(s)

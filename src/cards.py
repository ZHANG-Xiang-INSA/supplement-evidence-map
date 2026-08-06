# -*- coding: utf-8 -*-
"""Item cards: pros, cons, food sources and the endogenous-synthesis block."""
from site_base import (T, esc, slug, axes_for, spec_strip, norm_food,
                       FOOD, SYN, FUNC, FOOD_AXIS, DOSE_AXIS, SYN_AXIS, VERDICT_META)
from func_load import DEF_META, REV_META

_UNC = ('INDICATIVE AND UNCONFIRMED', 'indicative and unconfirmed',
        'Indicative and unconfirmed', 'unconfirmed:', 'UNCONFIRMED:')


def split_source(src):
    s = str(src or '').strip()
    for m in _UNC:
        i = s.find(m)
        if i >= 0:
            return (s[:i].rstrip(' .;,:') or s, s[i:].lstrip(' .;,:'))
    return (s, '')


def conf_bits(raw):
    u = str(raw or '').upper()
    if u.startswith('HIGH'):
        return 'p', 'High', '高'
    if u.startswith('LOW'):
        return 'f', 'Low', '低'
    return 'c', 'Medium', '中'


def conf_reason(raw):
    s = str(raw or '').strip()
    for tok in ('HIGH.', 'MEDIUM.', 'LOW.', 'HIGH,', 'MEDIUM,', 'LOW,', 'HIGH', 'MEDIUM', 'LOW'):
        if s.upper().startswith(tok):
            return s[len(tok):].strip(' .,:;')
    return s


def food_block(name):
    f = FOOD.get(name)
    s = SYN.get(name)
    if not f and not s:
        return ''
    o = ['<div class="food"><h5>%s</h5>' % T('Food and the body', '食物与身体')]

    o.append('<div class="fbadges">')
    if f:
        fa = FOOD_AXIS.get(norm_food(f.get('food_status')), FOOD_AXIS['SPLIT'])
        da = DOSE_AXIS.get(str(f.get('dose_from_food') or 'NA').upper(), DOSE_AXIS['NA'])
        o.append('<span class="tag %s">%s</span>'
                 % (fa[2], T('In food: ' + esc(fa[0]), '食物中：' + esc(fa[1]))))
        o.append('<span class="tag %s">%s</span>'
                 % (da[2], T('Dose from food: ' + esc(da[0]), '靠吃达到剂量：' + esc(da[1]))))
    if s:
        sa = SYN_AXIS.get(str(s.get('endogenous') or 'NA').upper(), SYN_AXIS['NA'])
        o.append('<span class="tag %s">%s</span>'
                 % (sa[2], T('Body makes it: ' + esc(sa[0]), '身体自产：' + esc(sa[1]))))
    if f:
        cc, cen, czh = conf_bits(f.get('data_confidence'))
        o.append('<span class="tag %s">%s</span>'
                 % (cc, T('Food data: ' + cen, '食物数据：' + czh)))
    o.append('</div>')

    if f and f.get('food_status_note'):
        o.append('<p class="fline">%s</p>'
                 % T(esc(f['food_status_note']),
                     esc(f.get('food_status_note_zh') or f['food_status_note'])))

    rows = (f or {}).get('food_rows') or []
    if rows:
        anyunc = any(split_source(r['source'])[1] for r in rows)
        o.append('<div class="ftw"><table><colgroup><col class="cf"><col class="ca"><col class="cp">'
                 '<col class="cv"><col class="cs"><col class="cr"></colgroup><thead><tr>')
        for h in [('Food', '食物'), ('Per 100 g', '每 100 克'), ('Portion', '一份'),
                  ('Per portion', '每份'), ('Share', '占比'), ('Source', '来源')]:
            o.append('<th>%s</th>' % T(*h))
        o.append('</tr></thead><tbody>')
        for r in rows:
            cite, unc = split_source(r['source'])
            tag = ''
            if unc:
                tag = ('<span class="unc" title="%s">%s</span>'
                       % (esc(unc), T('unconfirmed', '未核实')))
            o.append('<tr><td class="fd">%s%s</td>'
                     % (T(esc(r['food']), esc(r['food_zh'] or r['food'])), tag))
            o.append('<td class="num">%s</td>' % esc(r['per_100g']))
            o.append('<td class="num">%s</td>'
                     % T(esc(r['portion']), esc(r['portion_zh'] or r['portion'])))
            o.append('<td class="num">%s</td>' % esc(r['per_portion']))
            o.append('<td>%s</td>' % T(esc(r['pct']), esc(r['pct_zh'] or r['pct'])))
            o.append('<td class="src">%s</td></tr>' % esc(cite))
        o.append('</tbody></table></div>')
        if anyunc:
            o.append('<p class="fline">%s</p>' % T(
                'Rows tagged <span class="unc">unconfirmed</span> carry a figure the checking pass could not '
                'trace back to its cited source. Hover the tag for the reason.',
                '标记<span class="unc">未核实</span>的行，其数值在核查中无法追溯到所引来源。把鼠标移到标记上可看原因。'))
    elif f:
        o.append('<p class="fnone">%s</p>' % T(
            'No ordinary food supplies this in a meaningful amount.',
            '没有普通食物能提供有意义的量。'))

    if f:
        for a, b, k in [('To match the dose', '要达到该剂量', 'dose_from_food_note'),
                        ('Food vs supplement', '食物与补充剂', 'form_caveat'),
                        ('Absorption', '吸收', 'bioavailability')]:
            v = f.get(k)
            if not v or (k == 'form_caveat' and str(v).strip().upper().startswith('NONE')):
                continue
            o.append('<p class="fline"><b>%s</b>%s</p>'
                     % (T(a, b), T(esc(v), esc(f.get(k + '_zh') or v))))
        rsn = conf_reason(f.get('data_confidence'))
        if rsn:
            o.append('<p class="fline"><b>%s</b>%s</p>'
                     % (T('Food data note', '食物数据说明'),
                        T(esc(rsn), esc(conf_reason(f.get('data_confidence_zh')) or rsn))))

    if s:
        note = s.get('endogenous_note', '')
        o.append('<p class="fline"><b>%s</b>%s</p>'
                 % (T('Does the body make it', '身体是否自产'),
                    T(esc(note), esc(s.get('endogenous_note_zh') or note))))
        for a, b, k in [('Pathway', '合成通路', 'pathway'),
                        ('Amount made', '自产量', 'daily_amount'),
                        ('Still matters when', '仍有意义的情形', 'still_matters_when')]:
            v = s.get(k)
            if not v or str(v).strip().upper() in ('NOT APPLICABLE', 'NA', 'NEVER ON THIS AXIS'):
                continue
            o.append('<p class="fline"><b>%s</b>%s</p>'
                     % (T(a, b), T(esc(v), esc(s.get(k + '_zh') or v))))
        if s.get('source'):
            o.append('<p class="fline"><b>%s</b>%s</p>'
                     % (T('Synthesis source', '合成来源'), esc(s['source'])))
    o.append('</div>')
    return '\n'.join(o)


def func_block(name):
    fn = FUNC.get(name)
    if not fn:
        return ''
    de = DEF_META.get(str(fn.get('deficiency_state') or 'NA').upper(), DEF_META['NA'])
    rv = REV_META.get(str(fn.get('reversibility') or 'NA').upper(), REV_META['NA'])
    o = ['<div class="food fnb"><h5>%s</h5>' % T('What it does, and what happens without it',
                                                 '它有什么作用，缺了会怎样')]
    o.append('<p class="fline lead">%s</p>'
             % T(esc(fn.get('function_short', '')),
                 esc(fn.get('function_short_zh') or fn.get('function_short', ''))))
    o.append('<div class="fbadges">')
    o.append('<span class="tag %s">%s</span>' % (de[2], T(esc(de[0]), esc(de[1]))))
    if str(fn.get('reversibility', '')).upper() != 'NA':
        o.append('<span class="tag %s">%s</span>' % (rv[2], T(esc(rv[0]), esc(rv[1]))))
    o.append('</div>')
    o.append('<p class="fline"><b>%s</b>%s</p>'
             % (T('In detail', '详细'),
                T(esc(fn.get('function_full', '')),
                  esc(fn.get('function_full_zh') or fn.get('function_full', '')))))
    if str(fn.get('deficiency_state', '')).upper() in ('CLINICAL', 'FUNCTIONAL'):
        for a, b, k in [('Deficiency disease', '缺乏症', 'deficiency_name'),
                        ('First signs', '早期表现', 'deficiency_early'),
                        ('Untreated', '不治疗会怎样', 'deficiency_severe'),
                        ('Does it reverse', '补回来能修复吗', 'reversibility_note'),
                        ('Who becomes deficient', '谁会缺乏', 'at_risk'),
                        ('How common', '有多常见', 'prevalence')]:
            v = fn.get(k)
            if not v or str(v).strip().upper() in ('NONE', 'NOT APPLICABLE', 'NA'):
                continue
            o.append('<p class="fline"><b>%s</b>%s</p>'
                     % (T(a, b), T(esc(v), esc(fn.get(k + '_zh') or v))))
    else:
        o.append('<p class="fline nodef">%s</p>' % T(
            'There is no deficiency state for this. It is not an essential nutrient, so being short of it is not a '
            'thing that can happen.',
            '它不存在缺乏状态。它不是必需营养素，所以“缺了它”这件事本身并不成立。'))
    if fn.get('source'):
        o.append('<p class="fline"><b>%s</b>%s</p>' % (T('Source', '来源'), esc(fn['source'])))
    o.append('</div>')
    return chr(10).join(o)


def item_card(it):
    v = it['verdict']
    name = it['en']
    ax = axes_for(name, v, it['grade'])
    o = ['<article class="item" id="%s">' % slug(name)]
    o.append('<header>%s<span class="nm">%s</span></header>'
             % (spec_strip(ax, big=True), T(esc(name), esc(it['zh']))))
    o.append('<div class="kv">')
    for lab_en, lab_zh, ven, vzh in [
        ('Verdict', '结论', VERDICT_META[v][0], VERDICT_META[v][1]),
        ('Evidence', '证据', 'Grade ' + it['grade'], it['grade'] + ' 级'),
        ('Dose tested', '已验证剂量', it['dose_en'], it['dose_zh']),
        ('Who', '适用人群', it['who_en'], it['who_zh']),
    ]:
        o.append('<div><b>%s</b><span>%s</span></div>'
                 % (T(lab_en, lab_zh), T(esc(ven), esc(vzh))))
    o.append('</div>')
    o.append('<div class="pc"><div class="p"><h5>%s</h5><ul>' % T('Pros', '优点'))
    for a, b in it['pros']:
        o.append('<li>%s</li>' % T(a, b))
    o.append('</ul></div><div class="c"><h5>%s</h5><ul>' % T('Cons', '缺点'))
    for a, b in it['cons']:
        o.append('<li>%s</li>' % T(a, b))
    o.append('</ul></div></div>')
    o.append(func_block(name))
    o.append(food_block(name))
    o.append('<div class="refs">%s %s</div>' % (T('Refs.', '文献'), esc(it['refs'])))
    o.append('</article>')
    return '\n'.join(o)

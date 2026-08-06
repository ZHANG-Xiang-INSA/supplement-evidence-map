# -*- coding: utf-8 -*-
"""Assembles the supplement register site.

Landing view is the interactive register. Prose sections follow.
Convention: no raw double-quote inside any Python string literal.
"""
import io, os, re, html as HH, json
from supp_data import (VERDICT_META, GRADE_META, MISREADINGS, ITEMS,
                       TAKE, CONSIDER, SKIP, AVOID)
from supp_data2 import ITEMS2
from food_load import load as load_food
from design import CSS, JS
import figures as FG
import syn_load
import func_load
from func_load import DEF_META as _DEF, REV_META as _REV

ALL = ITEMS + ITEMS2
FOOD, _ = load_food()
SYN = syn_load.synthesis()
FUNC, _FUNC_WARN = func_load.load()
IX = syn_load.interactions()
ORDER = [TAKE, CONSIDER, SKIP, AVOID]
# repo root, resolved from this file so the folder can be moved freely
OUTDIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))


def T(en, zh):
    return '<span class="en">%s</span><span class="zh">%s</span>' % (en, zh)


def esc(s):
    return HH.escape(str(s or ''))


def slug(name):
    s = re.sub(r'[^a-z0-9]+', '-', str(name).lower()).strip('-')
    return 'i-' + s[:52]


# ---------------------------------------------------------------- axis vocabulary
VERDICT_CELL = {TAKE: ('T', 'p'), CONSIDER: ('C', 'c'), SKIP: ('S', 'n'), AVOID: ('A', 'f')}

FOOD_AXIS = {
    'RICH':      ('Rich', '丰富', 'p', 'Several ordinary foods supply a meaningful amount', '若干普通食物能提供有意义的量'),
    'TRACE':     ('Trace', '痕量', 'c', 'Present in food, but orders of magnitude below a useful dose', '食物中存在，但比有用剂量低几个数量级'),
    'SYNTHETIC': ('None', '无', 'f', 'No meaningful dietary presence; the supplement is manufactured', '膳食中无有意义的存在；补充剂为人工制造'),
    'NOT_FOOD':  ('Not food', '非食物', 'n', 'Comes from a plant or tissue not eaten in normal diets', '来自正常饮食中不食用的植物或组织'),
    'SPLIT':     ('Mixed', '视形式', 'c', 'The answer differs by chemical form; see the entry', '答案随化学形式而异，见条目'),
}

DOSE_AXIS = {
    'YES':     ('Reachable', '可达到', 'p', 'A realistic diet can reach the dose used in trials', '现实饮食可以达到试验所用剂量'),
    'PARTIAL': ('Partly', '部分', 'c', 'Diet gets part of the way, not all', '饮食能达到一部分，但不是全部'),
    'NO':      ('Out of reach', '达不到', 'f', 'No realistic diet reaches the dose', '没有现实的饮食能达到该剂量'),
    'NA':      ('No dose', '无剂量', 'n', 'A product category with no single dose to compare', '产品类别，没有单一剂量可比'),
}

SYN_AXIS = {
    'FULL':        ('Body makes it', '身体自产', 'p', 'Under normal conditions the body makes all it needs', '正常情况下身体自产足够'),
    'PARTIAL':     ('Partly', '部分自产', 'c', 'The body makes some, but not enough on its own', '身体能合成一部分，但不够'),
    'CONDITIONAL': ('Usually', '通常够', 'c', 'Normally enough, but not in a named condition', '通常足够，但在特定情况下不够'),
    'NONE':        ('Cannot', '不能', 'n', 'The body cannot make this at all; it must come from outside', '身体完全无法合成，必须外部获取'),
    'NA':          ('n/a', '不适用', 'n', 'The axis does not apply', '该维度不适用'),
}


def norm_food(v):
    u = str(v or '').upper()
    if '/' in u:
        return 'SPLIT'
    for k in ('RICH', 'TRACE', 'SYNTHETIC', 'NOT_FOOD'):
        if u.startswith(k):
            return k
    return 'SPLIT'


def axes_for(name, verdict, grade):
    f = FOOD.get(name) or {}
    s = SYN.get(name) or {}
    fn = FUNC.get(name) or {}
    return {
        'verdict': verdict,
        'grade': (grade or '?')[0],
        'food': norm_food(f.get('food_status')),
        'dose': str(f.get('dose_from_food') or 'NA').upper(),
        'syn': str(s.get('endogenous') or 'NA').upper(),
        'defi': str(fn.get('deficiency_state') or 'NA').upper(),
        'rev': str(fn.get('reversibility') or 'NA').upper(),
    }


def spec_strip(ax, big=False):
    """The signature: five cells, always the same order."""
    vl, vc = VERDICT_CELL.get(ax['verdict'], ('?', 'n'))
    fa = FOOD_AXIS.get(ax['food'], FOOD_AXIS['SPLIT'])
    da = DOSE_AXIS.get(ax['dose'], DOSE_AXIS['NA'])
    sa = SYN_AXIS.get(ax['syn'], SYN_AXIS['NA'])
    from func_load import DEF_META, REV_META
    de = DEF_META.get(ax.get('defi', 'NA'), DEF_META['NA'])
    rv = REV_META.get(ax.get('rev', 'NA'), REV_META['NA'])
    cells = [
        (vl, vc, 'Verdict: %s' % ax['verdict'], '结论：%s' % ax['verdict']),
        (ax['grade'], 'o', 'Evidence grade %s (confidence, not quality)' % ax['grade'],
         '证据分级 %s（表示确定性，不表示好坏）' % ax['grade']),
        ('F', fa[2], 'In food: %s. %s' % (fa[0], fa[3]), '食物中：%s。%s' % (fa[1], fa[4])),
        ('D', da[2], 'Dose from food: %s. %s' % (da[0], da[3]), '靠吃达到剂量：%s。%s' % (da[1], da[4])),
        ('B', sa[2], 'Body makes it: %s. %s' % (sa[0], sa[3]), '身体自产：%s。%s' % (sa[1], sa[4])),
        ('X', de[2], 'If you lack it: %s. %s' % (de[0], de[3]), '缺乏后果：%s。%s' % (de[1], de[4])),
    ]
    o = ['<span class="spec%s">' % (' lg' if big else '')]
    for letter, cls, ten, tzh in cells:
        o.append('<b class="%s"><span class="en" title="%s">%s</span>'
                 '<span class="zh" title="%s">%s</span></b>' % (cls, esc(ten), esc(letter), esc(tzh), esc(letter)))
    o.append('</span>')
    return ''.join(o)


# ---------------------------------------------------------------- register
def register():
    o = []
    o.append('<section class="reg" id="register" aria-labelledby="reg-h">')
    o.append('<h2 id="reg-h"><span class="no">01</span>%s</h2>'
             % T('The register', '总表'))
    o.append('<p class="lede">%s</p>' % T(
        'Every product, five axes, one row. Search it, filter it, sort any column, click a row to open it. '
        'The filtered view is in the address bar, so you can share exactly what you are looking at.',
        '每个产品一行，五个维度。可以搜索、筛选、按任意列排序，点一行即可展开。'
        '筛选后的视图会写进地址栏，你看到的画面可以直接分享。'))

    # controls
    o.append('<div class="reg-bar">')
    o.append('<div class="search"><svg viewBox="0 0 24 24" aria-hidden="true">'
             '<circle cx="11" cy="11" r="7"/><path d="M16.5 16.5 21 21"/></svg>'
             '<input id="reg-search" type="search" autocomplete="off" spellcheck="false" '
             'aria-label="Search the register" placeholder="'
             + 'Search 66 products, foods, nutrients" >'
             '<kbd>/</kbd></div>')
    o.append('</div>')

    facets = [
        ('verdict', T('Verdict', '结论'),
         [(v, VERDICT_META[v][0], VERDICT_META[v][1], VERDICT_CELL[v][1]) for v in ORDER]),
        ('dose', T('Dose from food', '靠吃达到剂量'),
         [(k, DOSE_AXIS[k][0], DOSE_AXIS[k][1], DOSE_AXIS[k][2]) for k in ('YES', 'PARTIAL', 'NO', 'NA')]),
        ('syn', T('Body makes it', '身体自产'),
         [(k, SYN_AXIS[k][0], SYN_AXIS[k][1], SYN_AXIS[k][2]) for k in ('FULL', 'PARTIAL', 'CONDITIONAL', 'NONE')]),
        ('defi', T('If you lack it', '缺乏后果'),
         [(k, _DEF[k][0], _DEF[k][1], _DEF[k][2]) for k in ('CLINICAL', 'FUNCTIONAL', 'NONE')]),
        ('rev', T('Reversible', '是否可逆'),
         [(k, _REV[k][0], _REV[k][1], _REV[k][2]) for k in ('IRREVERSIBLE', 'PARTIAL', 'FULL')]),
        ('food', T('In food', '食物中'),
         [(k, FOOD_AXIS[k][0], FOOD_AXIS[k][1], FOOD_AXIS[k][2]) for k in ('RICH', 'TRACE', 'SYNTHETIC', 'NOT_FOOD')]),
    ]
    for fkey, flabel, opts in facets:
        o.append('<div class="reg-bar"><span class="reg-note" style="min-width:118px">%s</span><div class="chips">' % flabel)
        for val, len_, lzh, cls in opts:
            o.append('<button class="chip %s" type="button" aria-pressed="false" data-facet="%s" data-val="%s">%s<span class="n"></span></button>'
                     % (cls, fkey, esc(val), T(esc(len_), esc(lzh))))
        o.append('</div></div>')

    o.append('<div class="reg-bar"><span class="reg-note">'
             '<span class="count" id="reg-count">%d</span> %s'
             '</span><button class="linkbtn" id="reg-clear" type="button" style="display:none">%s</button></div>'
             % (len(ALL), T('of %d shown' % len(ALL), '/ %d 项显示中' % len(ALL)),
                T('Clear all filters', '清除所有筛选')))

    # table
    o.append('<div class="tablewrap"><table class="reg-t">'
             '<colgroup><col class="c-nm"><col class="c-sp"><col class="c-vd">'
             '<col class="c-fd"><col class="c-ds"><col class="c-sy"><col class="c-df"><col class="c-wh"></colgroup>'
             '<thead><tr>')
    heads = [
        ('', T('Item', '项目'), 'name'),
        ('', T('Spec', '规格条'), None),
        ('verdict', T('Verdict', '结论'), 'verdict'),
        ('food', T('In food', '食物中'), 'food'),
        ('dose', T('Dose from food', '靠吃达到剂量'), 'dose'),
        ('syn', T('Body makes it', '身体自产'), 'syn'),
        ('defi', T('If you lack it', '缺乏后果'), 'defi'),
        ('', T('Who it is for', '适用人群'), None),
    ]
    for key, lab, sortk in heads:
        if sortk:
            o.append('<th class="sortable" data-key="%s" role="columnheader" tabindex="0">%s<span class="ind">&#9650;&#9660;</span></th>'
                     % (sortk, lab))
        else:
            o.append('<th>%s</th>' % lab)
    o.append('</tr></thead><tbody id="reg-body" class="stagger">')

    for v in ORDER:
        for it in [x for x in ALL if x['verdict'] == v]:
            name = it['en']
            ax = axes_for(name, v, it['grade'])
            f = FOOD.get(name) or {}
            s = SYN.get(name) or {}
            fa = FOOD_AXIS.get(ax['food'], FOOD_AXIS['SPLIT'])
            da = DOSE_AXIS.get(ax['dose'], DOSE_AXIS['NA'])
            sa = SYN_AXIS.get(ax['syn'], SYN_AXIS['NA'])
            searchtext = ' '.join([
                name, it['zh'], it.get('who_en', ''), it.get('who_zh', ''),
                v, ax['grade'],
                ' '.join((r.get('food', '') + ' ' + r.get('food_zh', '')) for r in (f.get('food_rows') or [])),
            ]).lower()
            o.append('<tr class="row" tabindex="0" role="button" aria-expanded="false" '
                     'data-name="%s" data-verdict="%s" data-grade="%s" data-food="%s" data-dose="%s" data-syn="%s" '
                     'data-defi="%s" data-rev="%s" data-search="%s">'
                     % (esc(name), v, ax['grade'], ax['food'], ax['dose'], ax['syn'],
                        ax['defi'], ax['rev'], esc(searchtext)))
            fn = FUNC.get(name) or {}
            o.append('<td class="nm">%s<span class="sub fnc">%s</span></td>'
                     % (T(esc(name), esc(it['zh'])),
                        T(esc(fn.get('function_short', '')), esc(fn.get('function_short_zh') or fn.get('function_short', '')))))
            o.append('<td>%s</td>' % spec_strip(ax))
            o.append('<td><span class="tag %s">%s</span></td>'
                     % (VERDICT_CELL[v][1].replace('n', 'n'),
                        T(esc(VERDICT_META[v][0]), esc(VERDICT_META[v][1]))))
            o.append('<td><span class="tag %s">%s</span></td>' % (fa[2], T(esc(fa[0]), esc(fa[1]))))
            o.append('<td><span class="tag %s">%s</span></td>' % (da[2], T(esc(da[0]), esc(da[1]))))
            o.append('<td><span class="tag %s">%s</span></td>' % (sa[2], T(esc(sa[0]), esc(sa[1]))))
            de = _DEF.get(ax['defi'], _DEF['NA'])
            rv = _REV.get(ax['rev'], _REV['NA'])
            cell = '<span class="tag %s">%s</span>' % (de[2], T(esc(de[0]), esc(de[1])))
            if ax['rev'] in ('IRREVERSIBLE', 'PARTIAL'):
                cell += '<br><span class="tag %s" style="margin-top:3px">%s</span>' % (rv[2], T(esc(rv[0]), esc(rv[1])))
            o.append('<td>%s</td>' % cell)
            o.append('<td class="who">%s</td>' % T(esc(it.get('who_en', '')), esc(it.get('who_zh', ''))))
            o.append('</tr>')

            # detail row
            o.append('<tr class="detail"><td colspan="8"><div class="detail-in">')
            o.append('<section><h5>%s</h5><p>%s</p></section>'
                     % (T('Who it is for', '适用人群'), T(esc(it.get('who_en', '')), esc(it.get('who_zh', '')))))
            o.append('<section><h5>%s</h5><p>%s</p></section>'
                     % (T('Dose tested', '已验证剂量'), T(esc(it['dose_en']), esc(it['dose_zh']))))
            if f.get('dose_from_food_note'):
                o.append('<section><h5>%s</h5><p>%s</p></section>'
                         % (T('To match that from food', '用食物达到该剂量'),
                            T(esc(f['dose_from_food_note']), esc(f.get('dose_from_food_note_zh') or f['dose_from_food_note']))))
            if s.get('endogenous_note'):
                o.append('<section><h5>%s</h5><p>%s</p></section>'
                         % (T('Does the body make it', '身体是否自产'),
                            T(esc(s['endogenous_note']), esc(s.get('endogenous_note_zh') or s['endogenous_note']))))
            if fn.get('function_full'):
                o.append('<section><h5>%s</h5><p>%s</p></section>'
                         % (T('What it does', '它有什么作用'),
                            T(esc(fn['function_full']), esc(fn.get('function_full_zh') or fn['function_full']))))
            if str(fn.get('deficiency_state', '')).upper() in ('CLINICAL', 'FUNCTIONAL'):
                o.append('<section><h5>%s</h5><p>%s</p></section>'
                         % (T('If you lack it', '缺乏会怎样'),
                            T(esc(fn.get('deficiency_severe', '')),
                              esc(fn.get('deficiency_severe_zh') or fn.get('deficiency_severe', '')))))
                if fn.get('reversibility_note'):
                    o.append('<section><h5>%s</h5><p>%s</p></section>'
                             % (T('Does it reverse', '补回来能修复吗'),
                                T(esc(fn['reversibility_note']),
                                  esc(fn.get('reversibility_note_zh') or fn['reversibility_note']))))
            o.append('<div class="go"><a href="#%s">%s</a></div>' % (slug(name), T('Full entry &#8594;', '完整条目 &#8594;')))
            o.append('</div></td></tr>')

    o.append('</tbody></table>')
    o.append('<div class="empty" id="reg-empty">%s</div>'
             % T('Nothing matches those filters. Try clearing one.', '没有符合这些筛选条件的项目。试着去掉一个。'))
    o.append('</div>')

    # legend
    o.append('<h3>%s</h3>' % T('How to read a spec strip', '规格条怎么读'))
    o.append('<p class="lede">%s</p>' % T(
        'Five cells, always in the same order. The second cell has no colour on purpose: an evidence grade measures '
        'how sure the literature is, and a confident answer can be a no.',
        '五个格子，顺序固定。第二格刻意不上色：证据分级衡量的是文献有多确定，而一个确定的答案完全可以是“无效”。'))
    o.append('<div class="legend">')
    o.append('<section><h4>%s</h4><ul>' % T('1 &nbsp;Verdict', '1 &nbsp;结论'))
    for v in ORDER:
        o.append('<li><span class="spec"><b class="%s">%s</b></span><span>%s</span></li>'
                 % (VERDICT_CELL[v][1], VERDICT_CELL[v][0],
                    T('<b>%s</b> %s' % (esc(VERDICT_META[v][0]), esc(VERDICT_META[v][3])),
                      '<b>%s</b> %s' % (esc(VERDICT_META[v][1]), esc(VERDICT_META[v][4])))))
    o.append('</ul></section>')
    o.append('<section><h4>%s</h4><ul>' % T('2 &nbsp;Evidence grade', '2 &nbsp;证据分级'))
    for g, en, zh in GRADE_META:
        o.append('<li><span class="spec"><b class="o">%s</b></span><span>%s</span></li>' % (g, T(esc(en), esc(zh))))
    o.append('</ul></section>')
    for num, ten, tzh, axis, keys, letter in [
        ('3', 'In food', '食物中', FOOD_AXIS, ('RICH', 'TRACE', 'SYNTHETIC', 'NOT_FOOD'), 'F'),
        ('4', 'Dose from food', '靠吃达到剂量', DOSE_AXIS, ('YES', 'PARTIAL', 'NO', 'NA'), 'D'),
        ('5', 'Body makes it', '身体自产', SYN_AXIS, ('FULL', 'PARTIAL', 'CONDITIONAL', 'NONE'), 'B'),
        ('6', 'If you lack it', '缺乏后果', _DEF, ('CLINICAL', 'FUNCTIONAL', 'NONE'), 'X'),
    ]:
        o.append('<section><h4>%s</h4><ul>' % T('%s &nbsp;%s' % (num, ten), '%s &nbsp;%s' % (num, tzh)))
        for k in keys:
            a = axis[k]
            o.append('<li><span class="spec"><b class="%s">%s</b></span><span>%s</span></li>'
                     % (a[2], letter, T('<b>%s</b> %s' % (esc(a[0]), esc(a[3])), '<b>%s</b> %s' % (esc(a[1]), esc(a[4])))))
        o.append('</ul></section>')
    o.append('</div>')
    o.append('</section>')
    return '\n'.join(o)

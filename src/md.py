# -*- coding: utf-8 -*-
"""Markdown companions, generated from the same data as the HTML."""
import io, os, re
from site_base import (ALL, FOOD, SYN, IX, ORDER, OUTDIR, VERDICT_META, GRADE_META,
                       MISREADINGS, FOOD_AXIS, DOSE_AXIS, SYN_AXIS, norm_food,
                       axes_for, TAKE, CONSIDER, SKIP, AVOID)
from syn_load import DIRECTION_META, SEVERITY_META
from cards import split_source, conf_bits, conf_reason
import build as B
from assemble import DOSE_ROWS, TIER_HEAD


def clean(s):
    s = str(s or '')
    for a, b in [('&ldquo;', '"'), ('&rdquo;', '"'), ('&nbsp;', ' '), ('&#183;', '-'),
                 ('&#8594;', '->'), ('<b>', '**'), ('</b>', '**'), ('<i>', '*'), ('</i>', '*')]:
        s = s.replace(a, b)
    return re.sub(r'<[^>]+>', '', s)


def render(en):
    def t(a, b):
        return clean(a if en else (b or a))

    o = io.StringIO()
    w = o.write

    w('# %s\n\n' % t('Supplement Register', '膳食补充剂总表'))
    w('%s\n\n' % t(
        'Sixty-six products, each with a verdict, an evidence grade, the dose that was actually tested, its pros and '
        'cons listed separately, the foods that supply it with quantities, and whether your body already makes it.',
        '六十六个产品，每一个都给出结论、证据分级、真正被试验验证过的剂量、分开列出的优点与缺点、'
        '提供它的食物及具体含量，以及你的身体是否本来就在合成它。'))
    w('> %s\n\n' % t('**Not medical advice.** It cannot replace a clinician who knows your history, medication list '
                     'and blood results.',
                     '**不构成医疗建议。**它无法替代了解你病史、用药清单和化验结果的临床医生。'))
    w('| | |\n|---|---|\n')
    for lab_en, lab_zh, val in [
        ('Products', '产品数', len(ALL)),
        ('Worth taking', '值得吃', B.COUNTS[TAKE]),
        ('Evidence of harm', '有致害证据', B.COUNTS[AVOID]),
        ('Food composition rows', '食物成分数据', B.N_ROWS),
        ('The body cannot make', '身体无法自产', B.SYN_C.get('NONE', 0)),
        ('The body makes fully', '身体完全自产', B.SYN_C.get('FULL', 0)),
        ('Fabricated references found', '虚构文献', 0),
    ]:
        w('| %s | %d |\n' % (t(lab_en, lab_zh), val))
    w('\n')

    # ---- how to read
    w('## %s\n\n' % t('1. How to read this', '一、怎么读这份文件'))
    w('| %s | %s |\n|---|---|\n' % (t('Axis', '维度'), t('Question it answers', '它回答的问题')))
    for a, b, c, d in [
        ('1 Verdict', '1 结论', 'Should you take it? Always per group, never universal.', '你该不该吃？永远针对特定人群，不是普遍适用。'),
        ('2 Evidence grade', '2 证据分级', 'How sure is the literature? A confident answer can be no.', '文献有多确定？一个确定的答案完全可以是“无效”。'),
        ('3 In food', '3 食物中', 'Does the substance occur in ordinary food?', '这种物质在普通食物中究竟有没有？'),
        ('4 Dose from food', '4 靠吃达到剂量', 'Could eating reach the tested dose?', '靠吃能达到试验剂量吗？'),
        ('5 Body makes it', '5 身体自产', 'Can you synthesise it yourself?', '你自己能合成吗？'),
    ]:
        w('| **%s** | %s |\n' % (t(a, b), t(c, d)))
    w('\n> %s\n\n' % t(
        '**Worked example.** Vitamin E is rich in food, so axis 3 reads Rich. But the harm-trial dose of 400 IU is '
        '268 mg of alpha-tocopherol, about 18 times the reference intake, so axis 4 reads Out of reach. And the body '
        'cannot make tocopherol at all, so axis 5 reads Cannot. All three are true at once.',
        '**举个例子。**维生素 E 在食物中丰富，所以第 3 轴是“丰富”。但致害试验用的 400 IU 相当于 268 毫克 α-生育酚，'
        '约为参考摄入量的 18 倍，所以第 4 轴是“达不到”。而人体完全无法合成生育酚，所以第 5 轴是“不能”。三者同时成立。'))
    w('### %s\n\n' % t('Nine ways this material gets misread', '这类材料被误读的九种方式'))
    for i, (a, b) in enumerate(MISREADINGS, 1):
        w('%d. %s\n' % (i, t(a, b)))
    w('\n')

    # ---- register
    w('## %s\n\n' % t('2. The register', '二、总表'))
    w('| %s | %s | %s | %s | %s | %s |\n|---|---|---|---|---|---|\n'
      % (t('Item', '项目'), t('Verdict', '结论'), t('Grade', '分级'),
         t('In food', '食物中'), t('Dose from food', '靠吃达到剂量'), t('Body makes it', '身体自产')))
    for v in ORDER:
        for it in [x for x in ALL if x['verdict'] == v]:
            ax = axes_for(it['en'], v, it['grade'])
            fa = FOOD_AXIS.get(ax['food'], FOOD_AXIS['SPLIT'])
            da = DOSE_AXIS.get(ax['dose'], DOSE_AXIS['NA'])
            sa = SYN_AXIS.get(ax['syn'], SYN_AXIS['NA'])
            w('| %s | **%s** | %s | %s | %s | %s |\n'
              % (t(it['en'], it['zh']), t(VERDICT_META[v][0], VERDICT_META[v][1]), ax['grade'],
                 t(fa[0], fa[1]), t(da[0], da[1]), t(sa[0], sa[1])))
    w('\n')

    # ---- tiers
    for v in ORDER:
        no, en_, zh_, den, dzh = TIER_HEAD[v]
        w('## %s. %s\n\n%s\n\n' % (int(no) - 1, t(en_, zh_), t(den, dzh)))
        for it in [x for x in ALL if x['verdict'] == v]:
            name = it['en']
            w('### %s\n\n' % t(name, it['zh']))
            w('**%s** %s &nbsp;|&nbsp; **%s** %s\n\n'
              % (t('Verdict:', '结论：'), t(VERDICT_META[v][0], VERDICT_META[v][1]),
                 t('Grade:', '分级：'), it['grade']))
            w('- **%s** %s\n' % (t('Dose tested:', '已验证剂量：'), t(it['dose_en'], it['dose_zh'])))
            w('- **%s** %s\n\n' % (t('Who it is for:', '适用人群：'), t(it['who_en'], it['who_zh'])))
            w('**%s**\n\n' % t('Pros', '优点'))
            for a, b in it['pros']:
                w('- %s\n' % t(a, b))
            w('\n**%s**\n\n' % t('Cons', '缺点'))
            for a, b in it['cons']:
                w('- %s\n' % t(a, b))
            w('\n')

            f = FOOD.get(name)
            s = SYN.get(name)
            if f or s:
                w('**%s**\n\n' % t('Food and the body', '食物与身体'))
                if f:
                    fa = FOOD_AXIS.get(norm_food(f.get('food_status')), FOOD_AXIS['SPLIT'])
                    da = DOSE_AXIS.get(str(f.get('dose_from_food') or 'NA').upper(), DOSE_AXIS['NA'])
                    _, cen, czh = conf_bits(f.get('data_confidence'))
                    w('- **%s** %s\n' % (t('In food:', '食物中：'), t(fa[0], fa[1])))
                    w('- **%s** %s\n' % (t('Dose from food:', '靠吃达到剂量：'), t(da[0], da[1])))
                    w('- **%s** %s\n' % (t('Food data confidence:', '食物数据可信度：'), t(cen, czh)))
                if s:
                    sa = SYN_AXIS.get(str(s.get('endogenous') or 'NA').upper(), SYN_AXIS['NA'])
                    w('- **%s** %s\n' % (t('Body makes it:', '身体自产：'), t(sa[0], sa[1])))
                w('\n')
                if f and f.get('food_status_note'):
                    w('%s\n\n' % t(f['food_status_note'], f.get('food_status_note_zh')))
                rows = (f or {}).get('food_rows') or []
                if rows:
                    w('| %s | %s | %s | %s | %s | %s |\n|---|---|---|---|---|---|\n'
                      % (t('Food', '食物'), t('Per 100 g', '每 100 克'), t('Portion', '一份'),
                         t('Per portion', '每份'), t('Share', '占比'), t('Source', '来源')))
                    for r in rows:
                        cite, unc = split_source(r['source'])
                        mark = ' *[unconfirmed]*' if (unc and en) else (' *[未核实]*' if unc else '')
                        w('| %s%s | %s | %s | %s | %s | %s |\n'
                          % (t(r['food'], r['food_zh']), mark, clean(r['per_100g']),
                             t(r['portion'], r['portion_zh']), clean(r['per_portion']),
                             t(r['pct'], r['pct_zh']), clean(cite)))
                    w('\n')
                if f:
                    for a, b, k in [('To match the dose:', '要达到该剂量：', 'dose_from_food_note'),
                                    ('Food vs supplement:', '食物与补充剂：', 'form_caveat'),
                                    ('Absorption:', '吸收：', 'bioavailability')]:
                        val = f.get(k)
                        if not val or (k == 'form_caveat' and str(val).strip().upper().startswith('NONE')):
                            continue
                        w('- **%s** %s\n' % (t(a, b), t(val, f.get(k + '_zh'))))
                if s:
                    w('- **%s** %s\n' % (t('Does the body make it:', '身体是否自产：'),
                                         t(s.get('endogenous_note', ''), s.get('endogenous_note_zh'))))
                    for a, b, k in [('Pathway:', '合成通路：', 'pathway'),
                                    ('Amount made:', '自产量：', 'daily_amount'),
                                    ('Still matters when:', '仍有意义的情形：', 'still_matters_when')]:
                        val = s.get(k)
                        if not val or str(val).strip().upper() in ('NOT APPLICABLE', 'NA', 'NEVER ON THIS AXIS'):
                            continue
                        w('- **%s** %s\n' % (t(a, b), t(val, s.get(k + '_zh'))))
                w('\n')
            w('*%s %s*\n\n' % (t('Refs.', '文献'), it['refs']))

    # ---- doses
    w('## 7. %s\n\n' % t('Doses and upper limits', '剂量与上限'))
    w('| %s | %s | %s | %s |\n|---|---|---|---|\n'
      % (t('Nutrient', '营养素'), t('Reference intake', '参考摄入量'),
         t('US upper limit', '美国上限'), t('EU upper limit', '欧盟上限')))
    for a, b, c, d, e in DOSE_ROWS:
        w('| %s | %s | %s | %s |\n' % (t(a, b), clean(c), clean(d), clean(e)))
    w('\n')

    # ---- interactions
    w('## 8. %s\n\n' % t('Drug interactions', '药物相互作用'))
    w('%s\n\n' % t(
        'One row per drug and supplement pair, each stating who does what to whom. Use it to recognise a problem, not '
        'to solve it alone: take the bottle to a pharmacist rather than stopping a prescribed medicine.',
        '每个“药物加补充剂”组合一行，每行写明谁对谁做了什么。用它来识别问题，不要自己解决：'
        '把瓶子拿给药师看，不要自行停用处方药。'))
    for sev in ('AVOID', 'MONITOR', 'SEPARATE_TIMING', 'INFORM_ONLY'):
        rows = [r for r in IX if str(r.get('severity', '')).upper() == sev]
        if not rows:
            continue
        sen, szh, _ = SEVERITY_META[sev]
        w('### %s\n\n' % t(sen, szh))
        w('| %s | %s | %s | %s | %s |\n|---|---|---|---|---|\n'
          % (t('Drug', '药物'), t('Supplement', '补充剂'), t('Direction', '方向'),
             t('What happens', '会发生什么'), t('What to do', '怎么办')))
        for r in rows:
            den, dzh, _ = DIRECTION_META.get(str(r.get('direction', '')).upper(),
                                             (r.get('direction', ''), r.get('direction', ''), 'n'))
            w('| **%s** (%s) | %s | %s | %s | %s |\n'
              % (t(r.get('drug_class', ''), r.get('drug_class_zh')), clean(r.get('drug_examples', '')),
                 t(r.get('supplement', ''), r.get('supplement_zh')), t(den, dzh),
                 t(r.get('what_happens', ''), r.get('what_happens_zh')),
                 t(r.get('action', ''), r.get('action_zh'))))
        w('\n')

    # ---- buying
    w('## 9. %s\n\n' % t('How to buy', '怎么买'))
    for i, (en_, zh_, wen, wzh) in enumerate(B.BUY, 1):
        w('%d. **%s** %s\n' % (i, t(en_, zh_), t(wen, wzh)))
    w('\n### %s\n\n' % t('What each certification mark covers', '各认证标识覆盖什么'))
    w('| %s | %s | %s | %s | %s |\n|---|---|---|---|---|\n'
      % (t('Mark', '标识'), t('Tests', '检测频率'), t('Screens for', '筛查内容'),
         t('Checks efficacy', '评估有效性'), t('Note', '说明')))
    for a, b, c, d, e, f_, g, h, i_, j in B.CERTS:
        w('| %s | %s | %s | %s | %s |\n' % (t(a, b), t(c, d), t(e, f_), t(g, h), clean(t(i_, j))))
    w('\n')

    # ---- method and gaps
    w('## 10. %s\n\n' % t('How this was built', '本文是怎么做出来的'))
    w('%s\n\n' % t(
        'Three research passes, each fanned out across ten or more domains, each followed by an independent checker '
        'instructed to assume a source does not exist until found. Across 428 citation checks: zero fabricated '
        'papers, zero invented PMIDs, zero wrong DOIs. 486 food figures were corrected during verification.',
        '三轮研究，每轮在十个以上领域并行展开，每轮之后都有独立核查员，其指令是在找到来源前先假定来源不存在。'
        '428 条引用核查中：虚构文献 0 篇，编造 PMID 0 个，错误 DOI 0 个。核查期间修正了 486 处食物数值。'))
    w('%s\n\n' % t(
        '**What to distrust.** NIH ODS returns HTTP 403 to automated retrieval, so reference intakes come from the '
        'underlying IOM/NASEM and EFSA documents. 86 food rows are tagged unconfirmed and eight items carry a Low '
        'data-confidence badge, because USDA FoodData Central returned 404s and rate limits during part of the work. '
        'Food composition varies by more than an order of magnitude between samples for Brazil nut selenium and '
        'UV-mushroom vitamin D.',
        '**哪些要打折扣。**NIH ODS 对自动抓取返回 HTTP 403，因此参考摄入量取自其背后的 IOM/NASEM 与 EFSA 文件。'
        '有 86 条食物数据标记为未核实，8 个条目带“数据可信度低”标签，因为部分工作期间 USDA FoodData Central 返回 404 并限流。'
        '巴西坚果的硒和紫外线处理蘑菇的维生素 D，样品间差异超过一个数量级。'))
    w('## 11. %s\n\n' % t('What is missing', '还缺什么'))
    w('| %s | %s | %s |\n|---|---|---|\n' % (t('Missing', '遗漏'), t('Why it matters', '为什么重要'),
                                             t('Until then', '在补上之前')))
    for a, b, c, d, e, f_ in B.GAPS:
        w('| **%s** | %s | %s |\n' % (t(a, b), t(c, d), t(e, f_)))
    w('\n---\n\n%s\n' % t(
        'Compiled by ZHANG Xiang, 30 July 2026. A research synthesis, not medical advice.',
        '编制：ZHANG Xiang，2026 年 7 月 30 日。研究综述，不构成医疗建议。'))
    return o.getvalue()


if __name__ == '__main__':
    for lang, fn in (('en', 'supplement-evidence-map.md'), ('zh', 'supplement-evidence-map.zh.md')):
        txt = render(lang == 'en')
        p = os.path.join(OUTDIR, fn)
        open(p, 'w', encoding='utf-8').write(txt)
        print('%-34s %8d bytes' % (fn, len(txt.encode('utf-8'))))

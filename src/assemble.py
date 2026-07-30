# -*- coding: utf-8 -*-
"""Remaining sections and final page assembly."""
import io, os, html as HH
from collections import Counter
from site_base import (T, esc, slug, ALL, FOOD, SYN, IX, ORDER, OUTDIR,
                       VERDICT_META, GRADE_META, MISREADINGS, register,
                       FOOD_AXIS, DOSE_AXIS, SYN_AXIS, norm_food,
                       TAKE, CONSIDER, SKIP, AVOID)
from cards import item_card
from design import CSS, JS
from figures import SVG_CSS
import figures as FG
import build as B

DOSE_ROWS = [
    ('Vitamin D', '维生素 D', 'RDA 600 IU (800 IU age 71+); supplement 800-2,000 IU/d', '4,000 IU (100 µg)', '4,000 IU (100 µg)'),
    ('Vitamin A (preformed)', '维生素 A（预成型）', '900 µg RAE men / 700 µg women', '3,000 µg (10,000 IU)', 'see 2024 opinion'),
    ('Vitamin E', '维生素 E', 'RDA 15 mg', '1,000 mg supplemental', '<b>300 mg, all sources</b>'),
    ('Vitamin C', '维生素 C', '90 mg men / 75 mg women (+35 smokers)', '2,000 mg', 'none set (SCF 2004)'),
    ('Vitamin K', '维生素 K', 'AI 120 µg men / 90 µg women (IOM); 70 µg (EFSA)', 'none set', 'none set'),
    ('Folate', '叶酸', '400 µg DFE (600 µg pregnancy)', '1,000 µg <b>synthetic</b>', '1,000 µg'),
    ('Vitamin B12', '维生素 B12', '2.4 µg', 'none (not determinable)', 'none'),
    ('Vitamin B6', '维生素 B6', '1.3 mg (1.7 men / 1.5 women over 50)', '<b>100 mg</b>', '<b>12 mg</b>'),
    ('Niacin', '烟酸', '16 mg NE', '35 mg synthetic', '900 mg nicotinamide'),
    ('Calcium', '钙', '1,000-1,200 mg total', '2,500 mg (2,000 mg over 51)', '2,500 mg'),
    ('Magnesium', '镁', '310-420 mg total', '<b>350 mg supplemental only</b>', '<b>250 mg supplemental</b>'),
    ('Iron', '铁', '8 mg men / 18 mg women 19-50 / 27 mg pregnancy', '45 mg', 'no UL; safe level 40 mg'),
    ('Zinc', '锌', '11 mg men / 8 mg women', '40 mg elemental', '25 mg'),
    ('Selenium', '硒', '55 µg', '<b>400 µg</b>', '<b>255 µg</b>'),
    ('Iodine', '碘', '150 µg (220 pregnancy, 290 lactation)', '1,100 µg', '600 µg'),
    ('Potassium', '钾', 'AI 3,400 mg men / 2,600 mg women', 'none set', 'none set'),
    ('Omega-3 EPA+DHA', 'Omega-3 EPA+DHA', '2-4 g/d for triglycerides', 'none', '5 g/d combined; DHA alone 1 g/d'),
    ('Caffeine', '咖啡因', '3-6 mg/kg pre-exercise', 'not applicable', '400 mg/d; <b>200 mg/d pregnancy</b>'),
    ('Creatine', '肌酸', '3-5 g/d', 'none set', 'none set'),
    ('Protein', '蛋白质', '1.6 g/kg/d plateau; RDA 0.8 g/kg', 'none set', 'none set'),
    ('Fibre', '膳食纤维', 'AI 25-38 g/d', 'none set', 'none set'),
]


def sec_howto():
    o = [B.h2('02', 'How to read this', '怎么读这份文件', 'howto')]
    o.append('<p class="lede">%s</p>' % T(
        'Five axes, and they answer five different questions. The commonest way to misread this material is to let '
        'one of them stand in for another.',
        '五个维度，回答五个不同的问题。误读这类材料最常见的方式，就是拿其中一个去顶替另一个。'))
    o.append(B.dtable([('Axis', '维度'), ('Question', '问题'), ('Trap', '陷阱')], [
        [T('<b>1 Verdict</b>', '<b>1 结论</b>'), T('Should you take it?', '你该不该吃？'),
         T('It is per group, never universal. Take means take if you are the named person.',
           '它针对特定人群，从来不是普遍适用。“值得吃”的意思是：如果你是那类人，才值得吃。')],
        [T('<b>2 Evidence grade</b>', '<b>2 证据分级</b>'), T('How sure is the literature?', '文献有多确定？'),
         T('A high grade does not mean it works. Selenium is grade A because Cochrane established with high certainty '
           'that it does <b>not</b> prevent cancer. This cell is deliberately colourless.',
           '高分级不等于有效。硒是 A 级，因为 Cochrane 高确定性地证明它<b>不能</b>预防癌症。这一格刻意不上色。')],
        [T('<b>3 In food</b>', '<b>3 食物中</b>'), T('Does the substance occur in ordinary food?', '这种物质在普通食物中有吗？'),
         T('Rich in food says nothing about whether the dose is reachable. Those are axes 3 and 4.',
           '“食物中丰富”完全不说明剂量能否达到。那是第 3 和第 4 两个不同的维度。')],
        [T('<b>4 Dose from food</b>', '<b>4 靠吃达到剂量</b>'), T('Could eating reach the tested dose?', '靠吃能达到试验剂量吗？'),
         T('This is the axis that decides whether food can stand in for the pill. Of 66 items, 44 are rich in food but '
           'only %d let you reach the dose.' % B.N_YES,
           '这是决定“食物能否顶替药片”的那个维度。66 个条目中有 44 个食物来源丰富，但只有 %d 个能靠吃达到剂量。' % B.N_YES)],
        [T('<b>5 Body makes it</b>', '<b>5 身体自产</b>'), T('Can you synthesise it yourself?', '你自己能合成吗？'),
         T('%d substances here your body cannot make at all, and %d it makes in full. A molecule you already produce '
           'in quantity is a weak thing to buy.' % (B.SYN_C.get('NONE', 0), B.SYN_C.get('FULL', 0)),
           '这里有 %d 种物质你的身体完全无法合成，另有 %d 种可以完全自产。一个你本来就大量制造的分子，买它的理由很弱。'
           % (B.SYN_C.get('NONE', 0), B.SYN_C.get('FULL', 0)))],
    ]))
    o.append('<div class="note"><span class="lbl">%s</span><p>%s</p></div>' % (
        T('Worked example', '举个例子'),
        T('Vitamin E is genuinely rich in food, so axis 3 reads Rich. One tablespoon of wheatgerm oil covers the daily '
          'reference intake. But the dose in the harm trials was 400 IU, which is 268 mg of alpha-tocopherol, roughly '
          '18 times the reference intake, so axis 4 reads Out of reach. And the body cannot make tocopherol at all, so '
          'axis 5 reads Cannot. All three are true at once, and only reading them together tells you anything useful.',
          '维生素 E 在食物中确实丰富，所以第 3 轴显示“丰富”：一勺小麦胚芽油就够一天的参考摄入量。'
          '但致害试验用的剂量是 400 IU，相当于 268 毫克 α-生育酚，约为参考摄入量的 18 倍，所以第 4 轴显示“达不到”。'
          '而人体完全无法合成生育酚，所以第 5 轴显示“不能”。三者同时成立，只有合起来读才有意义。')))

    o.append('<h3>%s</h3>' % T('Nine ways this material gets misread', '这类材料被误读的九种方式'))
    o.append('<ol class="rules">')
    for en, zh in MISREADINGS:
        o.append('<li>%s</li>' % T(en, zh))
    o.append('</ol>')

    grid = {}
    for v in FOOD.values():
        pass
    for name, f in FOOD.items():
        s = SYN.get(name) or {}
        grid[(norm_food(f.get('food_status')), str(f.get('dose_from_food') or 'NA').upper())] = \
            grid.get((norm_food(f.get('food_status')), str(f.get('dose_from_food') or 'NA').upper()), 0) + 1
    o.append('<figure>%s<figcaption>%s</figcaption></figure>' % (
        FG.stacked('Food presence against dose reachability', '食物中是否存在，对照剂量能否达到',
                   [('RICH', 'Rich in food', '食物中丰富'), ('TRACE', 'Trace only', '仅痕量'),
                    ('SYNTHETIC', 'Manufactured', '人工合成'), ('NOT_FOOD', 'Not a food', '非食物'),
                    ('SPLIT', 'Depends on form', '视形式而定')],
                   [('YES', 'Reachable', '可达到', 'p'), ('PARTIAL', 'Partly', '部分', 'c'),
                    ('NO', 'Out of reach', '达不到', 'f'), ('NA', 'No dose', '无剂量', 'n')],
                   grid,
                   '44 of 66 are rich in food, yet only %d let you reach the supplement dose by eating.' % B.N_YES,
                   '66 个中有 44 个食物来源丰富，但只有 %d 个能靠吃达到补充剂剂量。' % B.N_YES),
        T('<b>Figure 1.</b> Axis 3 against axis 4. Nine products are rich in food while their supplement dose is out '
          'of dietary reach, and that gap is what the industry sells into. Two of the reachable cases are warnings '
          'rather than recommendations: liver exceeds a 10,000 IU vitamin A dose, and a few Brazil nuts exceed 200 µg '
          'of selenium.',
          '<b>图 1。</b>第 3 轴对照第 4 轴。有 9 个产品在食物中很丰富，而其补充剂剂量却在饮食可及范围之外，'
          '行业做的正是这个落差的生意。那些“能达到”的案例里有两个是警示而非推荐：'
          '动物肝脏超过 10000 IU 的维生素 A 剂量，几颗巴西坚果就超过 200 微克的硒。')))

    sgrid = {}
    for name, s in SYN.items():
        v = next((i['verdict'] for i in ALL if i['en'] == name), None)
        if v:
            k = (str(s.get('endogenous') or 'NA').upper(), v)
            sgrid[k] = sgrid.get(k, 0) + 1
    o.append('<figure>%s<figcaption>%s</figcaption></figure>' % (
        FG.stacked('Can the body make it, against the verdict', '身体能否自产，对照结论',
                   [('NONE', 'Cannot make it', '完全不能自产'), ('PARTIAL', 'Makes some', '部分自产'),
                    ('CONDITIONAL', 'Usually enough', '通常够'), ('FULL', 'Makes it fully', '完全自产'),
                    ('NA', 'Not applicable', '不适用')],
                   [(TAKE, 'Take', '值得吃', 'p'), (CONSIDER, 'Consider', '可以考虑', 'c'),
                    (SKIP, 'Skip', '不必买', 'n'), (AVOID, 'Avoid', '不要吃', 'f')],
                   sgrid,
                   'Of the 9 substances the body makes in full, 8 are already in Skip on trial evidence alone.',
                   '身体能完全自产的 9 种物质中，有 8 种仅凭试验证据就已被列入“不必买”。'),
        T('<b>Figure 2.</b> The synthesis axis was researched independently of the trial evidence, so it works as a '
          'cross-check. It agrees: CoQ10, melatonin, collagen, glucosamine, NMN, NR, spermidine, alpha-lipoic acid and '
          '5-HTP are all molecules the body already makes in quantity, and eight of those nine had already landed in '
          'Skip on their trial record.',
          '<b>图 2。</b>合成这一维度是独立于试验证据研究的，因此可以当作交叉验证。结果是一致的：'
          '辅酶 Q10、褪黑素、胶原、氨基葡萄糖、NMN、NR、亚精胺、硫辛酸和 5-HTP，都是身体本来就大量制造的分子，'
          '而这九个里有八个仅凭试验记录就已被归入“不必买”。')))
    return '\n'.join(o)


def sec_market():
    o = [B.h2('03', 'Why the market looks like this', '这个市场为什么是这个样子', 'market')]
    o.append('<p class="lede">%s</p>' % T(
        'One regulatory fact explains most of what follows. Under the US Dietary Supplement Health and Education Act '
        'of 1994, supplements are legally food. No pre-market approval for safety or efficacy, and no statutory cap on '
        'the dose of an ingredient.',
        '一条监管事实解释了后面的大部分内容。按照美国 1994 年《膳食补充剂健康与教育法》，补充剂在法律上属于食品。'
        '上市前不需要安全性或有效性审批，法规也不对成分剂量设上限。'))
    o.append(B.dtable([('Indicator', '指标'), ('Figure', '数字'), ('Source', '来源')], [
        [T('Global market', '全球市场'), T('~USD 209.5bn (2025)', '约 2095 亿美元（2025）'),
         T('Grand View Research, unaudited', 'Grand View Research，未经审计')],
        [T('Growth since 1994', '1994 年以来'),
         T('USD 4bn and ~4,000 products, to ~USD 200bn and 50,000-80,000 products',
           '从 40 亿美元、约 4000 个产品，到约 2000 亿美元、5 万至 8 万个产品'), 'USP / FDA'],
        [T('FDA inspections', 'FDA 检查'), T('~5% of manufacturing facilities per year', '每年约 5% 的生产场所'), 'USP 2024'],
        [T('EU health claims authorised', '欧盟获批健康声称'),
         T('~250 of ~4,600 assessed, from ~44,000 submitted', '提交约 44000 条，评估约 4600 条，获批约 250 条'),
         'Regulation (EC) 1924/2006'],
        [T('Supplement-related ED visits (US)', '美国补充剂相关急诊'),
         T('~23,005 per year', '每年约 23005 次'), 'Geller, NEJM 2015, PMID 26465986'],
    ]))
    o.append('<figure>%s<figcaption>%s</figcaption></figure>' % (
        FG.hbars('Share of tested products that failed', '检测不合格产品占比', [
            ('Melatonin gummies mislabelled', '褪黑素软糖标签不准确', 88, '22 of 25; 74-347% of label', '25 个中 22 个；标示量的 74-347%', 'f'),
            ('Recalled products still spiked', '召回后仍含违禁药', 67, '18 of 27, ~34 months later', '27 个中 18 个，约 34 个月后', 'f'),
            ('Immune-support products mislabelled', '免疫类产品标签不符', 57, '17 of 30, JAMA Netw Open 2022', '30 个中 17 个', 'f'),
            ('Sold as SARMs, contained none', '标称 SARM 却不含', 48, '21 of 44, JAMA 2017', '44 个中 21 个', 'f'),
            ('Botanicals failing DNA check', '植物类 DNA 鉴定不合格', 27, '5,957 products, 37 countries', '5957 个产品，37 国', 'c'),
            ('Ayurvedic with lead, mercury or arsenic', '阿育吠陀检出铅汞砷', 21, '193 products', '193 个产品', 'c'),
        ], labelw=310),
        T('<b>Figure 3.</b> Independent analytical surveys of products bought off the shelf. The retracted 2013 '
          'barcoding paper claiming 59% substitution is deliberately excluded; the 27% figure is Ichim 2019 across '
          '5,957 products in 37 countries.',
          '<b>图 3。</b>对货架上买来的产品所做的独立分析调查。2013 年那篇声称 59% 掺假的条形码论文已撤稿，此处刻意排除；'
          '27% 取自 Ichim 2019，覆盖 37 个国家的 5957 个产品。')))
    return '\n'.join(o)


TIER_HEAD = {
    TAKE: ('04', 'Take it', '值得吃',
           'Strong evidence, but only for the group named under Who. None of these is for everyone.',
           '证据充分，但只对“适用人群”一栏所写的群体成立。没有一样适合所有人。'),
    CONSIDER: ('05', 'Consider it', '可以考虑',
               'Defensible in one specific situation. Outside it there is no case.',
               '只在一种特定情形下站得住。离开那个情形就没有理由。'),
    SKIP: ('06', 'Skip it', '不必买',
           'No good evidence for the marketed claim. Where a genuine narrow signal exists it is listed under Pros, so '
           'you can see how thin it is.',
           '对其宣传的功效没有像样的证据。若确实存在一点狭窄的信号，会列在“优点”里，让你看清它有多薄。'),
    AVOID: ('07', 'Avoid it', '不要吃',
            'Published evidence of harm from randomised trials, registries or national surveillance. Where a '
            'legitimate narrow medical indication exists it is stated, because the harm attaches to consumer '
            'self-dosing rather than supervised use.',
            '来自随机试验、登记或全国性监测的公开致害证据。若存在正当而狭窄的医疗适应证，文中会写明，'
            '因为危害针对的是消费者自行服用，而不是医疗监督下的使用。'),
}


def sec_tier(v):
    no, en, zh, den, dzh = TIER_HEAD[v]
    o = [B.h2(no, en, zh, {TAKE: 'take', CONSIDER: 'consider', SKIP: 'skip', AVOID: 'avoid'}[v])]
    o.append('<p class="lede">%s</p>' % T(den, dzh))
    if v == TAKE:
        o.append('<figure>%s<figcaption>%s</figcaption></figure>' % (FG.forest(), T(
            '<b>Figure 4.</b> Landmark trials, log scale, dashed line is no effect. Green sits entirely below 1, grey '
            'crosses 1, red sits entirely above. Read the middle block: the largest and most heavily marketed '
            'hypotheses in this field all land on the null line.',
            '<b>图 4。</b>标志性试验，对数刻度，虚线代表无效应。绿色完全在 1 以下，灰色跨过 1，红色完全在 1 以上。'
            '看中间那一段：这个领域里规模最大、营销最猛的几个假说，全都停在无效线上。')))
    for it in [x for x in ALL if x['verdict'] == v]:
        o.append(item_card(it))
    if v == SKIP:
        o.append('<div class="note"><span class="lbl">%s</span><p>%s</p></div>' % (
            T('Skip does not mean dangerous', '“不必买”不等于“危险”'),
            T('Everything in this section is a money problem rather than a safety one, with three exceptions flagged '
              'in their Cons: curcumin and green tea extract appear on liver-injury registries, and L-glutamine '
              'carries a mortality signal in the critically ill.',
              '本节内容基本是花钱的问题，不是安全的问题，但有三个例外已在其“缺点”中标出：'
              '姜黄素和绿茶提取物出现在肝损伤登记中，L-谷氨酰胺在危重患者中带有死亡信号。')))
    return '\n'.join(o)


def sec_doses():
    o = [B.h2('08', 'Doses and upper limits', '剂量与上限', 'doses')]
    o.append('<p class="lede">%s</p>' % T(
        'Where the US and EU disagree, both are given. These are not rounding differences; they change what counts '
        'as safe.',
        '美欧不一致的地方，两个数字都给。这不是四舍五入的差别，它改变了“安全”的定义。'))
    o.append('<figure>%s<figcaption>%s</figcaption></figure>' % (FG.ulgap(), T(
        '<b>Figure 5.</b> EU upper limits as a share of the US limit. Vitamin B6 is the extreme case: EFSA set '
        '12 mg/d in 2023 on peripheral neuropathy, against the US figure of 100 mg. Nerve-support and B-complex '
        'products routinely sit between the two.',
        '<b>图 5。</b>欧盟上限相对美国上限的比例。维生素 B6 是极端案例：EFSA 于 2023 年以周围神经病为依据定为 12 毫克/天，'
        '而美国是 100 毫克。“神经营养”和复合 B 族产品的剂量常常正好落在两者之间。')))
    o.append(B.dtable([('Nutrient', '营养素'), ('Reference intake', '参考摄入量'),
                       ('US upper limit', '美国上限'), ('EU upper limit', '欧盟上限')],
                      [[T(esc(a), esc(b)), '<span class="num">%s</span>' % c,
                        '<span class="num">%s</span>' % d, '<span class="num">%s</span>' % e]
                       for a, b, c, d, e in DOSE_ROWS]))
    o.append('<div class="note caution"><span class="lbl">%s</span><p>%s</p></div>' % (
        T('Elemental mass', '元素质量'),
        T('The commonest labelling deception in the mineral aisle. Magnesium oxide is about 60% magnesium and citrate '
          'about 16%, so a capsule labelled 500 mg magnesium citrate delivers roughly 80 mg of magnesium. Ferrous '
          'sulfate 325 mg delivers 65 mg of iron.',
          '矿物质货架上最常见的标签误导。氧化镁约含 60% 的镁，柠檬酸镁约 16%，'
          '所以标着“柠檬酸镁 500 毫克”的胶囊实际提供约 80 毫克镁。硫酸亚铁 325 毫克提供 65 毫克铁。')))
    return '\n'.join(o)


def page():
    w = io.StringIO().write
    b = io.StringIO()
    w = b.write
    w('<!doctype html>\n<html lang="en" data-lang="en">\n<head>\n<meta charset="utf-8">\n')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">\n')
    w('<meta name="color-scheme" content="light dark">\n')
    w('<meta name="description" content="Evidence-graded reference on 66 dietary supplements: verdicts, doses, '
      'pros and cons, food sources with quantities, and whether the body makes it. Bilingual EN and Chinese.">\n')
    w('<title>Supplement Register &#183; 膳食补充剂总表</title>\n')
    w('<style>%s\n%s</style>\n</head>\n<body>\n' % (CSS, SVG_CSS))

    # masthead
    w('<header class="mast"><div class="mast-in">')
    w('<div class="id"><b>%s</b><span>%s</span></div>'
      % (T('Supplement Register', '膳食补充剂总表'),
         T('66 products &#183; rev. 2026-07-30', '66 个产品 &#183; 版本 2026-07-30')))
    w('<nav>')
    for a, en, zh in [('register', 'Register', '总表'), ('howto', 'How to read', '怎么读'),
                      ('market', 'Market', '市场'), ('take', 'Take', '值得吃'),
                      ('consider', 'Consider', '可以考虑'), ('skip', 'Skip', '不必买'),
                      ('avoid', 'Avoid', '不要吃'), ('doses', 'Doses', '剂量'),
                      ('interactions', 'Interactions', '相互作用'), ('buying', 'Buying', '怎么买'),
                      ('method', 'Method', '方法'), ('gaps', 'Gaps', '缺什么')]:
        w('<a href="#%s">%s</a>' % (a, T(en, zh)))
    w('</nav><div class="ctl">')
    w('<div class="seg" role="group" aria-label="Language">'
      '<button id="lang-en" type="button" aria-pressed="true" onclick="setLang(\'en\')">EN</button>'
      '<button id="lang-zh" type="button" aria-pressed="false" onclick="setLang(\'zh\')">&#20013;&#25991;</button></div>')
    w('<button class="iconbtn" id="theme-btn" type="button" onclick="cycleTheme()" title="Theme">&#9681;</button>')
    w('</div></div></header>\n')

    # hero
    w('<div class="hero"><div class="wrap">')
    w('<div class="eyebrow"><span>%s</span><s>/</s><span>%s</span><s>/</s><span>%s</span></div>'
      % (T('Evidence register', '证据总表'), T('456 papers', '456 篇文献'),
         T('428 citations verified', '428 条引用经核查')))
    w('<h1>%s</h1>' % T('Which supplements are worth taking, and which your <em>dinner</em> already covers',
                        '哪些补充剂值得吃，哪些你的<em>一日三餐</em>本来就够了'))
    w('<p class="dek">%s</p>' % T(
        'Sixty-six products, each with a verdict, an evidence grade, the dose that was actually tested, its pros and '
        'cons side by side, the foods that supply it with quantities, and whether your body already makes it.',
        '六十六个产品，每一个都给出结论、证据分级、真正被试验验证过的剂量、并排列出的优点与缺点、'
        '提供它的食物及具体含量，以及你的身体是否本来就在合成它。'))
    w('<div class="meta-grid">')
    for big, en, zh, cls in [
        (str(len(ALL)), 'products', '个产品', ''),
        (str(B.COUNTS[TAKE]), 'worth taking', '个值得吃', 'good'),
        (str(B.COUNTS[AVOID]), 'evidence of harm', '个有致害证据', 'warn'),
        (str(B.N_ROWS), 'food data rows', '条食物数据', ''),
        (str(B.SYN_C.get('NONE', 0)), 'the body cannot make', '种身体无法自产', ''),
        (str(B.SYN_C.get('FULL', 0)), 'the body makes fully', '种身体完全自产', ''),
    ]:
        w('<div class="%s"><b class="d">%s</b><span>%s</span></div>' % (cls, big, T(en, zh)))
    w('</div></div></div>\n')

    w('<main class="wrap">')
    w('<section class="blk">%s</section>' % register())
    for fn in (sec_howto, sec_market):
        w('<section class="blk">%s</section>' % fn())
    for v in ORDER:
        w('<section class="blk">%s</section>' % sec_tier(v))
    w('<section class="blk">%s</section>' % sec_doses())
    w('<section class="blk">%s</section>' % B.sec_interactions())
    w('<section class="blk">%s</section>' % B.sec_buying())
    w('<section class="blk">%s</section>' % B.sec_method())
    w('<section class="blk">%s</section>' % B.sec_gaps())
    w('</main>\n')

    w('<footer><div class="in"><p>%s</p><p>%s</p></div></footer>' % (
        T('Compiled by ZHANG Xiang, 30 July 2026. Three research passes across ten domains each, every one followed by '
          'an independent adversarial checker. %d papers, 428 citations re-verified, %d food composition rows, '
          '486 food figures corrected. Press <kbd>L</kbd> to switch language, <kbd>/</kbd> to search.'
          % (456, B.N_ROWS),
          '编制：ZHANG Xiang，2026 年 7 月 30 日。三轮研究，每轮覆盖十个领域，每轮之后均有独立的对抗式核查。'
          '456 篇文献，428 条引用经复核，%d 条食物成分数据，486 处食物数值被修正。'
          '按 <kbd>L</kbd> 切换语言，按 <kbd>/</kbd> 搜索。' % B.N_ROWS),
        T('This is a research synthesis and not medical advice. It cannot replace a clinician who knows your history, '
          'medication list and blood results.',
          '本文是研究综述，不构成医疗建议。它无法替代了解你病史、用药清单和化验结果的临床医生。')))
    w('\n<script>%s</script>\n</body></html>' % JS)
    return b.getvalue()


if __name__ == '__main__':
    os.makedirs(OUTDIR, exist_ok=True)
    html = page()
    p = os.path.join(OUTDIR, 'index.html')
    open(p, 'w', encoding='utf-8').write(html)
    print('%-38s %8d bytes' % ('index.html', len(html.encode('utf-8'))))
    print('items %d | food rows %d | interactions %d | syn %d'
          % (len(ALL), B.N_ROWS, len(IX), len(SYN)))
    print('en spans %d | zh spans %d' % (html.count('class="en"'), html.count('class="zh"')))

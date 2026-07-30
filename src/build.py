# -*- coding: utf-8 -*-
"""Builds the site. Convention: no raw double-quote inside any Python string literal."""
import io, os, html as HH
from collections import Counter
from site_base import (T, esc, slug, ALL, FOOD, SYN, IX, ORDER, OUTDIR,
                       VERDICT_META, GRADE_META, MISREADINGS, register,
                       FOOD_AXIS, DOSE_AXIS, SYN_AXIS, norm_food,
                       TAKE, CONSIDER, SKIP, AVOID)
from cards import item_card
from syn_load import DIRECTION_META, SEVERITY_META
from design import CSS, JS
import figures as FG

COUNTS = {v: len([i for i in ALL if i['verdict'] == v]) for v in ORDER}
N_ROWS = sum(len(v.get('food_rows') or []) for v in FOOD.values())
N_YES = len([v for v in FOOD.values() if v['dose_from_food'] == 'YES'])
N_NO = len([v for v in FOOD.values() if v['dose_from_food'] == 'NO'])
N_RICH = len([v for v in FOOD.values() if str(v['food_status']).upper().startswith('RICH')])
SYN_C = Counter(v['endogenous'] for v in SYN.values())


def dtable(headers, rows):
    o = ['<div class="tw"><table class="dt"><thead><tr>']
    for h in headers:
        o.append('<th>%s</th>' % (T(*h) if isinstance(h, tuple) else h))
    o.append('</tr></thead><tbody>')
    for r in rows:
        o.append('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r))
    o.append('</tbody></table></div>')
    return '\n'.join(o)


def h2(no, en, zh, anchor):
    return '<h2 id="%s"><span class="no">%s</span>%s</h2>' % (anchor, no, T(en, zh))


# ---------------------------------------------------------------- 09 interactions
def sec_interactions():
    o = [h2('09', 'Drug interactions', '药物相互作用', 'interactions')]
    o.append('<p class="lede">%s</p>' % T(
        'One row per drug and supplement pair. Every row states who does what to whom, because the previous version '
        'of this table put opposite effects in the same cell. Under warfarin it listed vitamin K next to fish oil, '
        'when vitamin K weakens the drug and fish oil raises bleeding. Those need opposite responses.',
        '每个“药物加补充剂”组合一行。每行都写明谁对谁做了什么，因为这张表的上一版把方向相反的作用塞进了同一格。'
        '在华法林那一行里，维生素 K 和鱼油被列在一起，而维生素 K 削弱药效，鱼油增加出血。两者需要相反的应对。'))
    o.append('<div class="note caution"><span class="lbl">%s</span><p>%s</p></div>' % (
        T('Read this first', '先读这一条'),
        T('This table is for recognising a problem, not for solving it alone. Do not stop a prescribed medicine '
          'because of a row here. Take the supplement bottle to a pharmacist, who can check it against your full '
          'medication list in a couple of minutes and for free.',
          '这张表用来识别问题，不是用来自己解决问题。不要因为这里的某一行就停用处方药。'
          '把补充剂的瓶子拿给药师看，他们几分钟就能对照你的完整用药清单核对一遍，而且免费。')))

    for sev in ('AVOID', 'MONITOR', 'SEPARATE_TIMING', 'INFORM_ONLY'):
        rows = [r for r in IX if str(r.get('severity', '')).upper() == sev]
        if not rows:
            continue
        sen, szh, scls = SEVERITY_META[sev]
        o.append('<h3><span class="tag %s">%s</span></h3>' % (scls, T(esc(sen), esc(szh))))
        body = []
        for r in rows:
            den, dzh, dcls = DIRECTION_META.get(str(r.get('direction', '')).upper(),
                                                (r.get('direction', ''), r.get('direction', ''), 'n'))
            body.append([
                '<b>%s</b><br><span class="num" style="font-size:11.5px;color:var(--muted)">%s</span>'
                % (T(esc(r.get('drug_class', '')), esc(r.get('drug_class_zh') or r.get('drug_class', ''))),
                   esc(r.get('drug_examples', ''))),
                T(esc(r.get('supplement', '')), esc(r.get('supplement_zh') or r.get('supplement', ''))),
                '<span class="tag %s">%s</span>' % (dcls, T(esc(den), esc(dzh))),
                T(esc(r.get('what_happens', '')), esc(r.get('what_happens_zh') or r.get('what_happens', ''))),
                T(esc(r.get('action', '')), esc(r.get('action_zh') or r.get('action', ''))),
            ])
        o.append(dtable([('Drug', '药物'), ('Supplement', '补充剂'), ('Direction', '方向'),
                         ('What happens', '会发生什么'), ('What to do', '怎么办')], body))
    o.append('<p style="font-size:13px;color:var(--muted)">%s</p>' % T(
        '%d pairs across %d drug classes. Mechanism and evidence for each pair are in the source data; where a row '
        'rests only on case reports or on mechanism, the evidence field says so.'
        % (len(IX), len({r.get('drug_class') for r in IX})),
        '共 %d 个组合，涉及 %d 类药物。每个组合的机制与证据见源数据；若某行只有个案报告或只有机制推断，证据栏会写明。'
        % (len(IX), len({r.get('drug_class') for r in IX}))))
    return '\n'.join(o)


# ---------------------------------------------------------------- 10 buying
BUY = [
    ('Name the deficiency or the endpoint first', '先说出你要解决的缺乏或指标',
     'If you cannot name what you are correcting, no product is the right answer. Every entry in this document that '
     'earns a Take verdict earns it for a named group with a named problem.',
     '如果你说不出自己要纠正什么，那就没有哪个产品是对的。本文中每一个拿到“值得吃”的条目，都是针对特定人群的特定问题。'),
    ('Buy single ingredients at doses that were tested', '买单一成分，且剂量是被验证过的',
     'A proprietary blend hides the dose of every component behind two words. That is also where adulteration lives: '
     'in the FDA database, 776 adulterated products came from 146 companies, concentrated in blends.',
     '“专有配方”四个字把每种成分的剂量都藏了起来。掺假也正藏在那里：在 FDA 数据库中，776 个掺假产品来自 146 家公司，集中在复方产品。'),
    ('Check the elemental amount, not the compound', '看元素含量，不是化合物重量',
     'Magnesium oxide is about 60% magnesium and magnesium citrate about 16%, so a capsule labelled 500 mg magnesium '
     'citrate delivers roughly 80 mg of magnesium. Ferrous sulfate 325 mg delivers 65 mg of iron.',
     '氧化镁约含 60% 的镁，柠檬酸镁约 16%，所以标着“柠檬酸镁 500 毫克”的胶囊实际提供约 80 毫克镁。硫酸亚铁 325 毫克提供 65 毫克铁。'),
    ('Know what a certification mark does not cover', '搞清楚认证标识不覆盖什么',
     'All three major marks certify content and purity. None of them assesses whether the product works, and only two '
     'screen for substances banned in sport. See the table below.',
     '三大认证标识都只认证成分与纯度。没有一个评估产品是否有效，其中只有两个筛查运动违禁物质。见下表。'),
    ('Treat a seller-supplied certificate as a claim, not a proof', '把卖家提供的检测报告当作说法，不是证据',
     'Ask which production lot it covers, which laboratory produced it, whether that laboratory is ISO 17025 '
     'accredited, and who chose the laboratory. A certificate for a different lot proves nothing about the bottle in '
     'your hand.',
     '要问：它对应哪一个生产批次、哪家实验室出具、该实验室是否通过 ISO 17025 认可、以及实验室是谁挑的。'
     '另一个批次的报告，对你手上这瓶什么也证明不了。'),
    ('Avoid three categories outright', '有三类产品直接不要碰',
     'Anything sold for erections, rapid fat loss, or muscle building and testosterone. These three account for 45.5%, '
     '40.9% and 11.9% of all adulterated supplements in the FDA database, and enforcement does not fix them: 18 of 27 '
     'recalled products still contained banned drugs when re-bought a mean 34 months later.',
     '主打勃起功能、快速减脂、增肌与睾酮的产品。在 FDA 掺假数据库中，这三类分别占 45.5%、40.9% 和 11.9%，'
     '而且执法并不管用：27 个被召回的产品在平均 34 个月后重新购买，仍有 18 个含违禁药。'),
    ('Read the disclaimer literally', '照字面读免责声明',
     'The sentence saying the claim has not been evaluated by the FDA and the product is not intended to diagnose, '
     'treat, cure or prevent any disease is the regulator speaking. It is the most informative sentence on the bottle.',
     '那句“本声明未经 FDA 评估，本产品不用于诊断、治疗、治愈或预防任何疾病”，是监管者在说话。'
     '它是瓶子上信息量最大的一句。'),
    ('Tell your pharmacist what you take', '把你在吃什么告诉药师',
     'Especially before surgery, before starting an anticoagulant, and during cancer treatment. Post-market '
     'surveillance is the entire safety system for supplements, and it only works if people report.',
     '手术前、开始抗凝治疗前、以及肿瘤治疗期间尤其要说。上市后监测就是补充剂安全体系的全部，而它只有在有人上报时才起作用。'),
]

CERTS = [
    ('Informed Sport', 'Informed Sport', 'Every manufactured batch', '每一个生产批次',
     'WADA prohibited list', 'WADA 违禁清单', 'No', '否',
     'The only appropriate standard under anti-doping strict liability.', '在反兴奋剂严格责任下唯一合适的标准。'),
    ('NSF Certified for Sport', 'NSF Certified for Sport', 'Variable batch model', '按批次抽检',
     '280+ banned substances', '280 种以上违禁物质', 'No', '否',
     'Recognised by USADA, MLB and the NHL.', '获 USADA、MLB 和 NHL 认可。'),
    ('USP Verified', 'USP Verified', 'Off-the-shelf surveillance', '市售抽检',
     'Identity, potency, dissolution, contaminants', '成分鉴定、含量、崩解度、污染物', 'No', '否',
     'Does <b>not</b> screen for substances banned in sport, so a verified product can legally contain a prohibited stimulant.',
     '<b>不</b>筛查运动违禁物质，所以通过认证的产品完全可能合法地含有违禁兴奋剂。'),
]


def sec_buying():
    o = [h2('10', 'How to buy', '怎么买', 'buying')]
    o.append('<p class="lede">%s</p>' % T(
        'Eight rules, each with the reason it exists. The reason matters more than the rule, because it tells you '
        'when the rule stops applying.',
        '八条规则，每条都附上它存在的理由。理由比规则更重要，因为它告诉你这条规则在什么时候不再适用。'))
    o.append('<ol class="rules">')
    for en, zh, wen, wzh in BUY:
        o.append('<li><b>%s</b>%s</li>' % (T(esc(en), esc(zh)), T(wen, wzh)))
    o.append('</ol>')
    o.append('<h3>%s</h3>' % T('What each certification mark actually covers', '各认证标识究竟覆盖什么'))
    o.append(dtable([('Mark', '标识'), ('Tests', '检测频率'), ('Screens for', '筛查内容'),
                     ('Checks efficacy', '是否评估有效性'), ('Note', '说明')],
                    [[T(esc(a), esc(b)), T(esc(c), esc(d)), T(esc(e), esc(f)),
                      '<span class="tag n">%s</span>' % T(esc(g), esc(h)), T(i, j)]
                     for a, b, c, d, e, f, g, h, i, j in CERTS]))
    o.append('<div class="note"><span class="lbl">%s</span><p>%s</p></div>' % (
        T('The honest limitation', '一个诚实的局限'),
        T('No published head-to-head study shows that certified products fail less often than uncertified ones. The '
          'case for certification is inferential: it rests on how badly uncertified products perform in the analytical '
          'surveys, not on a trial of certification itself.',
          '没有任何已发表的头对头研究表明认证产品的不合格率低于未认证产品。支持认证的理由是推断性的：'
          '它依据的是未认证产品在分析性调查中有多糟，而不是针对认证本身做过的试验。')))
    return '\n'.join(o)


# ---------------------------------------------------------------- 11 method
def sec_method():
    o = [h2('11', 'How this was built', '本文是怎么做出来的', 'method')]
    o.append('<p class="lede">%s</p>' % T(
        'Three research passes, each fanned out across ten or more domains, and each followed by an independent '
        'checker whose instruction was to assume a source does not exist until it is found.',
        '三轮研究，每轮都在十个以上领域并行展开，每轮之后都有一名独立核查员，其指令是：'
        '在找到来源之前，先假定该来源不存在。'))
    o.append(dtable([('Pass', '轮次'), ('What it produced', '产出'), ('What the checker found', '核查结果')], [
        [T('<b>1 &nbsp;Evidence</b>', '<b>1 &nbsp;证据</b>'),
         T('456 papers behind 66 verdicts and evidence grades: Cochrane reviews, meta-analyses and large named trials.',
           '支撑 66 个结论与证据分级的 456 篇文献：Cochrane 综述、meta 分析和大型具名试验。'),
         T('428 citations re-searched. <b>Zero fabricated references.</b> Caught evidence grades about half a grade too '
           'generous, five materially wrong doses, and several cases of a flattering subgroup quoted while the null '
           'overall result was omitted.',
           '428 条引用被重新检索。<b>零篇虚构文献。</b>发现证据分级普遍偏高约半级、五处实质性剂量错误，'
           '以及若干只引用好看亚组、略去总体阴性结果的情况。')],
        [T('<b>2 &nbsp;Food</b>', '<b>2 &nbsp;食物</b>'),
         T('%d composition rows from USDA FoodData Central, McCance and Widdowson, and peer-reviewed analyses, with '
           'per-portion figures and the quantity of food needed to match each supplement dose.' % N_ROWS,
           '来自 USDA FoodData Central、McCance and Widdowson 及同行评议分析的 %d 条成分数据，'
           '含每份含量和达到各补充剂剂量所需的食物量。' % N_ROWS),
         T('486 figures corrected, including matcha EGCG understated roughly 65-fold, krill astaxanthin quoted on a '
           'dry-weight basis against a fresh portion, chicken liver CoQ10 labelled as chicken heart, and lion mane '
           'composition measured on the wrong <i>Hericium</i> species.',
           '修正 486 处数值，包括抹茶 EGCG 被低估约 65 倍、磷虾虾青素以干重数据对应鲜重份量、'
           '鸡肝的辅酶 Q10 被标成鸡心，以及猴头菇成分数据取自错误的<i>猴头菌属</i>物种。')],
        [T('<b>3 &nbsp;Synthesis</b>', '<b>3 &nbsp;体内合成</b>'),
         T('Whether the body can make each substance itself, with the pathway, the enzymes and the daily amount where '
           'a figure exists.',
           '身体能否自行合成每种物质，附合成通路、关键酶，以及在有数据时的每日自产量。'),
         T('The first attempt drifted badly: the category field was described rather than constrained, so agents wrote '
           'sentences into it and invented sixty supplements outside the brief. Re-run with a hard enumeration and an '
           'explicit coverage rule, then audited to 66 of 66 with one bundling error caught.',
           '第一次尝试严重跑偏：分类字段只是被描述而没有被强制约束，于是智能体往里写整句，还凭空造出六十个不在范围内的补充剂。'
           '改用硬性枚举并写明覆盖规则后重跑，经审计达到 66/66，并发现一处混装错误。')],
    ]))
    o.append('<div class="note pass"><span class="lbl">%s</span><p>%s</p></div>' % (
        T('The fabrication hunt', '查找虚构文献的结果'),
        T('Across 428 citation checks the verifiers found zero fabricated papers, zero invented PMIDs and zero wrong '
          'DOIs. Effect sizes reproduced to the decimal in the large majority of cases. The papers most likely to be '
          'hallucinations, recent 2026 publications with implausible-looking identifiers, all turned out to be real.',
          '在 428 条引用核查中，核查员发现虚构文献 0 篇、编造的 PMID 0 个、错误的 DOI 0 个。'
          '绝大多数效应量精确复现到小数位。最像幻觉的那几篇，也就是标识符看起来不太可信的 2026 年新文献，全部确认真实存在。')))
    o.append('<h3>%s</h3>' % T('What to distrust here', '本文中哪些内容要打折扣'))
    o.append('<ol class="plain">')
    for en, zh in [
        ('NIH ODS fact sheets return HTTP 403 to automated retrieval, so reference intakes come from the underlying '
         'IOM/NASEM reports and EFSA opinions instead. Those are the primary sources ODS itself cites, but it is one '
         'step further from the number you would read on a government page.',
         'NIH ODS 的资料页对自动抓取返回 HTTP 403，因此参考摄入量取自其背后的 IOM/NASEM 报告和 EFSA 意见书。'
         '那是 ODS 自己引用的原始来源，但比你在政府网页上直接读到的数字多隔了一层。'),
        ('86 food rows are tagged unconfirmed and eight items carry a Low data-confidence badge, because USDA '
         'FoodData Central returned 404s and rate limits during part of the work and the UK CoFID dataset was not '
         'retrievable. Those figures are shown with the reason rather than dropped or passed off as sourced.',
         '有 86 条食物数据被标记为未核实，8 个条目带有“数据可信度低”的标签，'
         '因为部分工作期间 USDA FoodData Central 返回 404 并限流，英国 CoFID 数据集也无法取得。'
         '这些数字连同原因一起列出，没有删掉，也没有假装有来源。'),
        ('Several entries rest on a single unreplicated trial. Where that is true it is stated in the Cons column of '
         'that entry, not buried here.',
         '若干条目依赖单项未经重复验证的试验。凡是这种情况，都写在该条目的“缺点”栏里，而不是埋在这一节。'),
        ('Food composition varies enormously with cultivar, soil, season and preparation. Brazil nut selenium and '
         'UV-mushroom vitamin D each vary by more than an order of magnitude between samples, so treat any single '
         'figure as a midpoint rather than a specification.',
         '食物成分随品种、土壤、季节和烹调方式变化极大。巴西坚果的硒和紫外线处理蘑菇的维生素 D，'
         '样品之间的差异都超过一个数量级，所以任何单一数值都应看作中位估计，而不是规格值。'),
        ('Market-size figures are unaudited commercial estimates produced by firms whose customers are the companies '
         'being measured. Read them as orders of magnitude.',
         '市场规模数字是未经审计的商业估算，出具方的客户正是被统计的那些公司。只当数量级看。'),
    ]:
        o.append('<li>%s</li>' % T(en, zh))
    o.append('</ol>')
    return '\n'.join(o)


# ---------------------------------------------------------------- 12 gaps
GAPS = [
    ('Red yeast rice', '红曲',
     'Contains monacolin K, which is chemically identical to lovastatin. It is an unlabelled statin sold without a '
     'prescription, carrying rhabdomyolysis, hepatotoxicity and statin drug-interaction risk.',
     '含莫纳可林 K，化学结构与洛伐他汀完全相同。它是一款不标注、免处方出售的他汀，带有横纹肌溶解、肝毒性和他汀类相互作用风险。',
     'Treat it as a statin: same cautions, same interactions, same monitoring.',
     '把它当他汀对待：同样的注意事项、同样的相互作用、同样的监测。'),
    ('Enteric-coated peppermint oil', '肠溶薄荷油',
     'Sold in the same aisle, with multiple meta-analyses in irritable bowel syndrome and a stronger effect estimate '
     'than almost any probiotic reviewed here.',
     '摆在同一排货架上，在肠易激综合征领域有多项 meta 分析，效应估计强于本文评述的几乎任何一种益生菌。',
     'If you are buying a probiotic for IBS, this has better data.', '如果你为肠易激买益生菌，这个的数据更好。'),
    ('Biotin', '生物素',
     'One of the largest single-B-vitamin retail categories, sold at 5,000 to 10,000 µg against a 30 µg adequate '
     'intake, on essentially no efficacy evidence. It carries an active FDA safety communication because it interferes '
     'with streptavidin-biotin immunoassays, including troponin.',
     '单一 B 族维生素中最大的零售品类之一，常规剂量 5000 至 10000 微克，而适宜摄入量是 30 微克，几乎没有有效性证据。'
     'FDA 就其干扰链霉亲和素-生物素免疫检测（包括肌钙蛋白）发布过至今有效的安全通告。',
     'Stop it before any blood test and tell the person taking the sample.', '任何抽血检查前停用，并告知采血人员。'),
    ('Sodium bicarbonate', '碳酸氢钠',
     'On the IOC short list of supplements with robust performance evidence, alongside caffeine, creatine, '
     'beta-alanine and nitrate, and it has its own ISSN position stand.',
     '与咖啡因、肌酸、β-丙氨酸和硝酸盐一同被列入国际奥委会“具备可靠成绩证据”的短名单，并有自己的 ISSN 立场声明。',
     'The one item on the IOC list this document does not cover.', '国际奥委会短名单上本文唯一没有覆盖的一项。'),
    ('Urolithin A', '尿石素 A',
     'The flagship commercial mitophagy product, with company-run randomised trials that were not assessed here.',
     '商业线粒体自噬赛道的旗舰产品，其公司自办的随机试验本文未作评估。',
     'Expect the NAD-precursor pattern until shown otherwise: biomarker moves, endpoint does not.',
     '在有相反证据之前，可以预期它走 NAD 前体的老路：生物标志物在动，终点不动。'),
    ('Lavender oil / Silexan', '薰衣草油 / Silexan',
     'A licensed anxiolytic medicine in Germany with placebo-controlled and active-comparator trials in generalised '
     'anxiety disorder, and a stronger evidence base than rhodiola, bacopa or lion mane.',
     '在德国是获批的抗焦虑药，在广泛性焦虑障碍上有安慰剂对照和阳性药对照试验，证据基础强于红景天、假马齿苋或猴头菇。',
     'Better evidenced than three botanicals this document does cover.', '证据强于本文已覆盖的三种植物制剂。'),
    ('Calcifediol', '骨化二醇',
     'Over-the-counter across Europe, prescription in the US. Two to three times more potent per microgram than D3 and '
     'raises serum 25(OH)D far faster.',
     '在欧洲非处方销售，在美国为处方药。按微克计效力是 D3 的 2 至 3 倍，升高血清 25(OH)D 的速度也快得多。',
     'Relevant if you are correcting a documented deficiency rather than maintaining.',
     '如果你要纠正已证实的缺乏而不是维持，它是相关的。'),
    ('CBD and hemp cannabinoids', 'CBD 与大麻素',
     'The largest single regulatory gap: excluded from the US supplement definition by the drug-exclusion rule, and '
     'treated by the UK FSA as a novel food requiring authorisation.',
     '最大的单项监管空白：因药品排除规则被排除在美国膳食补充剂定义之外，英国 FSA 则视其为需要授权的新型食品。',
     'Regulatory status differs by country more than for anything else here.',
     '它的监管状态因国家而异的程度超过本文任何其他条目。'),
]


def sec_gaps():
    o = [h2('12', 'What is missing', '还缺什么', 'gaps')]
    o.append('<p class="lede">%s</p>' % T(
        'The checkers named these as the most conspicuous omissions. Each row says why it matters and what to do '
        'until it is covered, so the gap is usable rather than just acknowledged.',
        '核查员点出这些是最明显的遗漏。每一行都说明它为什么重要，以及在补上之前该怎么办，'
        '这样这些缺口是可用的，而不只是被承认。'))
    o.append(dtable([('Missing', '遗漏'), ('Why it matters', '为什么重要'), ('Until then', '在补上之前')],
                    [['<b>%s</b>' % T(esc(a), esc(b)), T(c, d), T(e, f)] for a, b, c, d, e, f in GAPS]))
    return '\n'.join(o)

# -*- coding: utf-8 -*-
"""Food entries for the five items that are product categories rather than single
substances, plus the alias map joining researched names to document names.

Convention: no raw double-quote inside any string literal.
"""

# researched name -> document name
ALIASES = {
    'Ashwagandha': 'Ashwagandha (Withania somnifera)',
    'MSM': 'MSM (methylsulfonylmethane)',
    'NMN': 'NMN (nicotinamide mononucleotide)',
    'Selenium at 200 ug/d': 'Selenium at 200 µg/d',
}


def M(name, status, dose, note_en, note_zh, gap_en, gap_zh, caveat_en, caveat_zh):
    return {
        'supplement': name,
        'food_status': status,
        'dose_from_food': dose,
        'food_status_note': note_en,
        'food_status_note_zh': note_zh,
        'dose_from_food_note': gap_en,
        'dose_from_food_note_zh': gap_zh,
        'foods': [],
        'foods_zh': [],
        'form_caveat': caveat_en,
        'form_caveat_zh': caveat_zh,
        'bioavailability': 'NONE. This entry is a product category rather than a single substance, so there is no single absorption comparison to make.',
        'bioavailability_zh': '不适用。本条目是一个产品类别，不是单一物质，因此没有单一的吸收对比可做。',
        'data_confidence': 'HIGH. The classification follows from what the product is, not from composition data.',
        'data_confidence_zh': '高。这个判断来自产品本身是什么，不依赖成分数据。',
        'corrections_applied': [],
        'manual': True,
    }


MANUAL = [

M('High-dose folic acid plus B12 for cardiovascular prevention',
  'RICH', 'NA',
  'Both nutrients are abundant in ordinary food, so see the folic acid and vitamin B12 entries for the food tables. The distinction that matters here is the dose and the purpose. Food folate and food B12 at dietary levels carry none of the cancer signal seen in the Norwegian trials, which used 0.8 mg/d of synthetic folic acid plus 0.4 mg/d of B12 for a cardiovascular indication.',
  '这两种营养素在普通食物中都很丰富，食物表见叶酸和维生素 B12 两个条目。这里真正要区分的是剂量和用途。'
  '膳食水平的食物叶酸和食物 B12 完全不带挪威试验中出现的癌症信号，那些试验用的是每天 0.8 毫克合成叶酸加 0.4 毫克 B12，目的是心血管预防。',
  'Not applicable as a target. There is no food quantity to aim for, because the trials that produced the cancer signal were testing a supplemental dose for a purpose that does not work. The dietary answer is to meet the reference intake from food and stop there.',
  '作为目标而言不适用。没有需要去凑的食物量，因为产生癌症信号的那些试验测的是一个用途根本不成立的补充剂剂量。膳食层面的答案是靠食物达到参考摄入量，到此为止。',
  'This is the clearest case in the document where the food and the supplement diverge on outcome rather than on amount. Periconceptional folic acid at 400 µg remains the strongest supplement result in existence; the same molecule at twice the dose given to cardiac patients raised cancer incidence. Same compound, different dose, different population, opposite conclusion.',
  '这是全文中食物与补充剂在结局上而非在剂量上分道扬镳最清楚的一例。围孕期 400 微克叶酸仍是现存最强的补充剂结果；'
  '同一个分子加倍剂量给心脏病患者，却升高了癌症发病。同一种化合物，不同剂量，不同人群，相反的结论。'),

M('Antioxidants during chemotherapy',
  'RICH', 'NA',
  'Vitamins A, C and E, carotenoids and CoQ10 are all present in ordinary food, and each has its own food table elsewhere in this document. Food is not the concern here. The concern is supplemental doses taken alongside cytotoxic treatment.',
  '维生素 A、C、E、类胡萝卜素和辅酶 Q10 在普通食物中都存在，本文别处各有其食物表。这里担心的不是食物，'
  '而是在细胞毒治疗期间同时服用的补充剂剂量。',
  'Not applicable, and deliberately so. Eating fruit and vegetables during chemotherapy is not the exposure that SWOG S0221 measured. That study looked at supplement use before and during treatment, at doses far above what food supplies.',
  '不适用，而且是刻意如此。化疗期间吃水果和蔬菜，不是 SWOG S0221 所测量的那种暴露。'
  '那项研究看的是治疗前及治疗期间服用补充剂，剂量远高于食物所能提供的水平。',
  'The gap between food and supplement is the whole point. A portion of berries and a 1,000 mg vitamin C capsule are not the same intervention. Nobody has suggested that dietary antioxidant intake during treatment is harmful, and no oncology body recommends restricting fruit and vegetables. Any change to supplements during cancer treatment belongs with the treating oncologist.',
  '食物与补充剂之间的差距正是关键所在。一份浆果和一粒 1000 毫克维生素 C 胶囊不是同一种干预。'
  '没有人提出治疗期间的膳食抗氧化摄入有害，也没有任何肿瘤学机构建议限制水果和蔬菜。'
  '肿瘤治疗期间对补充剂的任何调整，都应由主治肿瘤医生决定。'),

M('Probiotics in critical illness',
  'RICH', 'NA',
  'Live microorganisms are abundant in fermented foods, and the counts are given in the probiotics entry. That is not the relevant question for this item, because the population is patients in intensive care.',
  '发酵食品中活微生物含量丰富，具体计数见益生菌条目。但对本条目而言这不是相关的问题，因为这里的人群是重症监护中的患者。',
  'Not applicable, and the direction is reversed. There is no food target to reach. The same caution that applies to probiotic capsules applies to fermented foods in these patients, and enteral feeding decisions in intensive care are made by the clinical team.',
  '不适用，而且方向是相反的。这里没有需要达到的食物目标。对益生菌胶囊适用的那些警示，'
  '同样适用于这些患者食用的发酵食品，而重症监护中的肠内营养决策由临床团队做出。',
  'Fermented foods are a reasonable habit for healthy people and are not a substitute for a named strain at a defined dose. In critical illness, compromised gut perfusion and mucosal barrier injury are what make live organisms hazardous, and that hazard does not care whether the organism arrived in a capsule or in a spoonful of yoghurt.',
  '发酵食品对健康人是合理的饮食习惯，但不能替代特定菌株在特定剂量下的作用。'
  '在危重症中，内脏灌注受损和黏膜屏障损伤才是活微生物变得危险的原因，'
  '而这种危险并不在意微生物是来自一粒胶囊还是一勺酸奶。'),

M('Bodybuilding and test-booster products',
  'SYNTHETIC', 'NA',
  'There is no food source, because the active ingredients are undeclared anabolic androgenic steroids: manufactured pharmaceuticals and controlled substances. The label ingredients are largely decorative. Chemical analysis of the products implicated in liver injury repeatedly finds steroids the label does not mention.',
  '没有食物来源，因为其活性成分是未标示的合成代谢雄激素类固醇，也就是人工合成的药物和受管制物质。'
  '标签上列的成分基本是装饰。对那些造成肝损伤的产品所做的化学分析，反复检出标签上根本没写的类固醇。',
  'Not applicable. You cannot eat your way to an undeclared steroid dose, and you should not want to.',
  '不适用。你无法靠吃东西达到一个未标示的类固醇剂量，也不该想去达到。',
  'The legitimate food-adjacent route to the advertised outcome is dull and well evidenced: enough total protein to reach about 1.6 g/kg/day, and creatine monohydrate. Both have their own entries with food tables. Neither requires buying a proprietary blend.',
  '要达到广告宣称的效果，正当且贴近食物的路径既枯燥又有充分证据：把总蛋白摄入提到约 1.6 克/公斤/天，'
  '再加一水肌酸。两者本文都有各自的条目和食物表。都不需要买什么专有配方。'),

M('Sexual-enhancement products',
  'SYNTHETIC', 'NA',
  'There is no food source. The active ingredients are undeclared PDE5 inhibitors, chiefly sildenafil and structural analogues designed to evade laboratory detection. These are prescription pharmaceuticals, not nutrients, and they are present because the product would otherwise do nothing.',
  '没有食物来源。其活性成分是未标示的 PDE5 抑制剂，主要是西地那非以及为规避实验室检测而设计的结构类似物。'
  '这些是处方药，不是营养素，它们之所以在里面，是因为不放的话产品什么作用也没有。',
  'Not applicable. No quantity of any food contains a pharmaceutical PDE5 inhibitor.',
  '不适用。任何食物、任何数量都不含药用的 PDE5 抑制剂。',
  'The danger runs the other way from a normal form caveat. Here the product contains more than the label admits rather than less. Someone taking nitrates for angina who swallows an undeclared PDE5 inhibitor can reach catastrophic hypotension without knowing what they took.',
  '这里的危险与通常的“剂型差异”正好相反。这个产品含有的东西比标签承认的更多，而不是更少。'
  '一个正在服用硝酸酯类抗心绞痛药的人，吞下未标示的 PDE5 抑制剂，可能在不知道自己吃了什么的情况下走向灾难性低血压。'),

]

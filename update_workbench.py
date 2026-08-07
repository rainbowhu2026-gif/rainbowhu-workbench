#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os

wb_path = r"D:\workbuddy\2026-07-26-17-33-36\rainbowhu-workbench.html"
with open(wb_path, "r", encoding="utf-8") as f:
    content = f.read()

# ===== 1. Update dates =====
content = content.replace('id="todayDate">2026-08-03</span>', 'id="todayDate">2026-08-04</span>')
content = content.replace('id="pageDate">2026年8月3日 星期一 · Week 32</div>', 'id="pageDate">2026年8月4日 星期二 · Week 32</div>')
content = content.replace('id="inspDate">2026-07-26</div>', 'id="inspDate">2026-08-04</div>')
content = content.replace('id="titleLabDate">2026-07-26</div>', 'id="titleLabDate">2026-08-04</div>')
content = content.replace('id="weiboDate">2026-07-26</div>', 'id="weiboDate">2026-08-04</div>')
content = content.replace('id="svDate">2026-07-26</div>', 'id="svDate">2026-08-04</div>')
content = content.replace('href="彩虹心理每日心理热点报告_2026-08-03.html"', 'href="彩虹心理每日心理热点报告_2026-08-04.html"')

# ===== 2. Replace RADAR_TOP5 =====
RADAR_TOP5 = '''const RADAR_TOP5 = [
  {rank:1,title:'一个家庭最可怕的不是贫穷，而是「情绪污染」',score:96,tags:['原生家庭','情绪心理'],hook:'踢猫效应 + 情绪感染链 + 家庭情绪环境评估 → 家庭咨询/情绪管理咨询'},
  {rank:2,title:'我们都试图在伴侣身上解决自己的童年烂账',score:95,tags:['亲密关系','原生家庭'],hook:'投射性认同 + 强迫性重复 + 内在小孩识别练习 → 亲密关系咨询'},
  {rank:3,title:'朋友圈和微博的差别belike：你在害怕被谁看见真实的自己',score:93,tags:['社交焦虑','自我成长'],hook:'角色期待 + 自我损耗 + 聚光灯效应 → 自我认同咨询'},
  {rank:4,title:'花钱请自己吃顿好的，你心跳加速了——「不配得感」正在隐秘毁掉你',score:92,tags:['原生家庭','自我价值'],hook:'愧疚式教育 + 不配得感神经通路 + 前额叶重塑 → 原生家庭咨询'},
  {rank:5,title:'什么样的关系最养人？2026年爆火心理学共识',score:90,tags:['亲密关系','自我成长'],hook:'关系营养学 + 情绪价值供给 + 依恋安全基地 → 亲密关系咨询'},
];'''

content = re.sub(r'const RADAR_TOP5 = \[.*?\];', RADAR_TOP5, content, flags=re.DOTALL)

# ===== 3. Replace ARTICLE_PLANS =====
ARTICLE_PLANS = '''const ARTICLE_PLANS = [
  {
    rank:1, score:96, topic:'情绪污染：家庭中最隐蔽的情绪病毒与净化策略', cat:'原生家庭 · 情绪心理',
    angle:'从家庭系统理论和情绪感染链角度解读情绪污染的传播机制，提供可操作的家庭情绪环境评估与净化方法',
    audience:'25-40岁在原生家庭或婚姻中长期承受负面情绪传递、感到家庭氛围压抑窒息、想要改变但不知从何入手的成年人',
    wordCount:'2500字',
    titles:{pro:'家庭情绪污染的认知机制与干预策略——从踢猫效应到情绪感染链',emo:'推开门心就沉下去——你家是不是也有「情绪污染」',viral:'一个家庭最可怕的不是穷，是这种看不见的「情绪病毒」 [推测/示例]'},
    structure:{
      opening:'陈慧每天最怕下班推开门——门里传来的是妈妈的抱怨和爸爸的冷战，明明没做错任何事，却感觉自己像个罪人。',
      pain:'展开情绪污染的三重危害：耗光夫妻情分、刻进孩子性格、代际传递形成恶性循环。',
      mechanism:'踢猫效应+情绪感染理论+家庭系统理论。美国心理学家哈特菲尔德发现人类会自动模仿周围人的情绪，在家庭高密度低边界环境中，情绪感染效率被放大数倍。情绪感染链：工作受挫→带着压抑回家→对伴侣语气生硬→伴侣反击或冷战→孩子感知紧张→全家进入低气压。',
      method:'提供4个练习：1）情绪污染源定位（连续3天记录）；2）家庭情绪温度计（1-10分每日打分）；3）15分钟情绪隔离带（进门前深呼吸+自我对话）；4）家庭情绪会议（每周固定时间正向沟通）。',
      hook:'引出彩虹心理家庭咨询，提供家庭情绪环境评估、个体情绪管理咨询、家庭系统治疗等专业服务。'
    },
    sources:[
      '参考腾讯新闻/微信公众号情绪污染热文（2026-08-01），用自己的案例和语言完全重写',
      '整合哈特菲尔德情绪感染理论和鲍比依恋理论',
      '加入至少1个原创案例（基于真实咨询经验改编，保护隐私）',
      '严禁大段照搬原文，每处引用不超过30字且须改写表达方式'
    ],
    books:[
      '《被管理的心》（阿莉·霍赫希尔德）：情绪劳动理论奠基',
      '《依恋》（约翰·鲍比）：依恋理论与安全基地',
      '《为何家会伤人》（武志红）：中国家庭动力学',
      '《家庭治疗》（维吉尼亚·萨提亚）：家庭系统治疗',
      '《情绪感染》（伊莱恩·哈特菲尔德）：情绪传播机制研究'
    ]
  },
  {
    rank:2, score:95, topic:'童年烂账：投射性认同、强迫性重复与亲密关系中的童年创伤再现', cat:'亲密关系 · 原生家庭',
    angle:'从投射性认同和强迫性重复角度解读亲密关系中的错位争吵，提供内在小孩识别与疗愈工具',
    audience:'25-40岁在亲密关系中反复因小事爆发激烈情绪、意识到可能与童年经历有关但不知如何改变的成年人',
    wordCount:'2500字',
    titles:{pro:'投射性认同与强迫性重复：亲密关系中的童年创伤再现机制',emo:'你气的不是眼前这个人，是当年那个无力的自己',viral:'为什么你总在亲密关系里「借题发挥」？心理咨询师揭开了真相 [推测/示例]'},
    structure:{
      opening:'男生因为女友和异性朋友多说了几句话突然冷战。他真正介意的不是那几句话，而是童年时被背叛、抛弃的感受再一次席卷了他。',
      pain:'展开投射性认同的恶性循环：恐惧→寻找证据→行为验证→恐惧被证实。以及强迫性重复的代际传递：童年被忽视→选择冷漠伴侣→试图改写结局。',
      mechanism:'投射性认同（克莱因）：将自己无法承受的感受投射到伴侣身上，诱导对方按照投射内容回应。强迫性重复（弗洛伊德）：无意识重复创伤性关系模式，试图在重复中获得掌控感。武志红：亲密关系是一面镜子，照见的是我们自己的内心。',
      method:'提供4个练习：1）情绪触发点追溯（暂停+四问）；2）内在小孩对话（回到童年场景+自我对话）；3）关系模式家谱图（画出三代关系模式）；4）「我陈述」代替「你指责」（句式练习）。',
      hook:'引出彩虹心理亲密关系咨询，提供依恋模式评估、内在小孩疗愈、强迫性重复阻断等专业服务。'
    },
    sources:[
      '参考武志红/腾讯新闻童年烂账热文（2026-08-02），用自己的案例和语言完全重写',
      '整合克莱因投射性认同理论和弗洛伊德强迫性重复理论',
      '加入至少1个原创案例（基于真实咨询经验改编，保护隐私）',
      '严禁大段照搬原文，每处引用不超过30字且须改写表达方式'
    ],
    books:[
      '《为何家会伤人》（武志红）：中国家庭动力学',
      '《依恋》（约翰·鲍比）：依恋理论与分离焦虑',
      '《精神分析导论》（弗洛伊德）：投射与重复强迫',
      '《内在小孩》（约翰·布雷迪）：内在小孩疗愈方法',
      '《深度关系》（武志红）：亲密关系中的自我认知'
    ]
  },
  {
    rank:3, score:93, topic:'社交面具：角色期待、自我损耗与社交媒体时代的真实自我困境', cat:'社交焦虑 · 自我成长',
    angle:'从社会心理学角色期待和自我损耗理论切入，帮助读者识别社交面具的代价，找回真实自我',
    audience:'18-35岁在不同社交平台维持不同人设、感到社交疲惫和自我认同模糊的都市年轻人',
    wordCount:'2500字',
    titles:{pro:'角色期待与自我损耗：社交媒体时代的真实自我表达困境',emo:'朋友圈岁月静好，微博发疯——你在害怕被谁看见真实的自己',viral:'为什么同一个人，在朋友圈和微博活成了两个人？ [推测/示例]'},
    structure:{
      opening:'朋友圈：时光荏苒，岁月静好。微博：这破日子什么时候是个头？同一个人，在两个平台过着两种截然不同的人生。',
      pain:'展开角色期待的社会心理学机制+自我损耗的认知资源消耗+聚光灯效应的认知偏差。长期维持多重社交面具导致自我认同模糊度是普通人的2.3倍。',
      mechanism:'角色期待（社会心理学）：在不同社会关系网中占据不同位置，他人对我们提出合乎身份的期待，我们下意识切换脚本迎合。自我损耗（鲍迈斯特）：意志力是有限资源，每切换一次角色面具都在消耗。聚光灯效应（季洛维奇）：高估他人对自己的关注程度。',
      method:'提供4个练习：1）社交面具审计（列出各平台角色+隐藏部分）；2）「真实时刻」记录（每天记录一个没有表演的时刻）；3）聚光灯效应破除实验（做一件害怕评价的事+观察结果）；4）建立「无表演空间」（小号/日记/挚友群）。',
      hook:'引出彩虹心理自我成长咨询，提供自我认同评估、社交焦虑咨询、真实自我探索等专业服务。'
    },
    sources:[
      '参考微博热搜/腾讯新闻社交面具热文（2026-08-02），用自己的案例和语言完全重写',
      '整合社会心理学角色期待理论和鲍迈斯特自我损耗理论',
      '加入至少1个原创案例（基于真实咨询经验改编，保护隐私）',
      '严禁大段照搬原文，每处引用不超过30字且须改写表达方式'
    ],
    books:[
      '《社会心理学》（戴维·迈尔斯）：角色期待与自我呈现',
      '《自控力》（凯利·麦格尼格尔）：意志力与自我损耗',
      '《被讨厌的勇气》（岸见一郎）：课题分离与真实自我',
      '《真实的幸福》（马丁·塞利格曼）：积极心理学与自我认同',
      '《深度关系》（武志红）：关系中的自我认知'
    ]
  }
];'''

content = re.sub(r'const ARTICLE_PLANS = \[.*?\];\s*\n\n', ARTICLE_PLANS + '\n\n', content, flags=re.DOTALL)

# ===== 4. Replace READY_ARTICLES =====
READY_ARTICLES = '''const READY_ARTICLES = [
  {
    rank:1,
    score:96,
    title:'推开门心就沉下去——你家是不是也有「情绪污染」',
    cat:'原生家庭 · 情绪心理',
    wordCount:'约2480字',
    readTime:'约7分钟',
    file:'article-2026-08-04-01-情绪污染.html',
    excerpt:'2026年8月，「情绪污染」一词在社交平台悄然发酵。推开门那一刻心就沉下去——这不是偶然，是家庭中最隐蔽的「情绪病毒」在蔓延。本文从踢猫效应、情绪感染链和家庭系统理论角度，解读情绪污染的传播机制，提供4个可操作的觉察练习（情绪污染源定位/家庭情绪温度计/15分钟情绪隔离带/家庭情绪会议），帮你净化家庭情绪环境。',
    keywords:'情绪污染|踢猫效应|情绪感染链|家庭系统理论|原生家庭|情绪管理'
  },
  {
    rank:2,
    score:95,
    title:'你气的不是眼前这个人，是当年那个无力的自己',
    cat:'亲密关系 · 原生家庭',
    wordCount:'约2560字',
    readTime:'约8分钟',
    file:'article-2026-08-04-02-童年烂账.html',
    excerpt:'武志红文章引发全网共鸣：很多争吵本质上都是「借题发挥」。当下的矛盾只是导火索，引爆的是积压了二三十年的情绪炸药。本文从投射性认同和强迫性重复角度，解读亲密关系中的错位争吵，提供4个觉察练习（情绪触发点追溯/内在小孩对话/关系模式家谱图/「我陈述」代替「你指责」），帮你识别童年烂账对当下关系的影响。',
    keywords:'童年烂账|投射性认同|强迫性重复|内在小孩|亲密关系|原生家庭'
  },
  {
    rank:3,
    score:93,
    title:'朋友圈岁月静好，微博发疯——你在害怕被谁看见真实的自己',
    cat:'社交焦虑 · 自我成长',
    wordCount:'约2420字',
    readTime:'约7分钟',
    file:'article-2026-08-04-03-社交面具.html',
    excerpt:'2026年8月微博热搜#朋友圈和微博的差别belike#引发全网共鸣。同一个人，在朋友圈是情绪稳定的成年人，在微博是随时可以崩溃的普通人。本文从角色期待、自我损耗和聚光灯效应角度，解读社交媒体时代的「真实自我」困境，提供4个练习（社交面具审计/「真实时刻」记录/聚光灯效应破除实验/建立「无表演空间」），帮你找回真实的自己。',
    keywords:'社交面具|角色期待|自我损耗|聚光灯效应|自我认同|社交焦虑'
  }
];'''

content = re.sub(r'const READY_ARTICLES = \[.*?\];', READY_ARTICLES, content, flags=re.DOTALL)

# ===== 5. Replace VIRAL_IDEAS =====
VIRAL_IDEAS = '''const VIRAL_IDEAS = [
  {n:1,title:'推开门心就沉下去——你家是不是也有「情绪污染」',desc:'#情绪污染#腾讯新闻热文引入→踢猫效应可视化→情绪感染链机制→家庭情绪污染三重危害→家庭情绪环境四维度评估→情绪净化四步法→家庭咨询入口。强共鸣+强专业+高转化。',platforms:['抖音','视频号','小红书'],color:'#ff6b6b'},
  {n:2,title:'你气的不是眼前这个人，是当年那个无力的自己',desc:'武志红热文引入→投射性认同概念→强迫性重复机制→内在小孩识别→伴侣vs父母角色区分→三个觉醒→亲密关系咨询。强共鸣+强专业+高转化。',platforms:['抖音','视频号','小红书'],color:'#feca57'},
  {n:3,title:'朋友圈岁月静好，微博发疯——你在害怕被谁看见真实的自己',desc:'#朋友圈和微博的差别belike#热搜引入→角色期待理论→自我损耗机制→聚光灯效应破除→无表演空间建立→自我认同咨询。强共鸣+年轻人话题+高传播。',platforms:['抖音','小红书'],color:'#48dbfb'},
  {n:4,title:'花钱请自己吃顿好的，你心跳加速了——「不配得感」正在隐秘毁掉你',desc:'#母女吃烧烤#热搜引入→不配得感概念→愧疚式教育机制→前额叶神经可塑性→「我值得」重塑练习→原生家庭咨询。强共鸣+强转化。',platforms:['抖音','视频号','小红书'],color:'#1dd1a1'},
  {n:5,title:'什么样的关系最养人？2026年爆火心理学共识',desc:'知乎年度热词引入→关系营养学概念→五大养人特质（舒服/包容/治愈/双向/成全）→依恋安全基地→情绪价值供给→关系健康度评估→亲密关系咨询。正面导向+强收藏+高传播。',platforms:['抖音','小红书'],color:'#a55eea'},
];'''

content = re.sub(r'const VIRAL_IDEAS = \[.*?\];', VIRAL_IDEAS, content, flags=re.DOTALL)

# ===== 6. Prepend OPTS entries =====
# Find the existing OPTS and prepend new entries
new_opts = '''  {t:'「情绪污染」家庭系统强转化',d:'TOP1 腾讯新闻热文发酵，踢猫效应+情绪感染链概念专业且可感知，家庭情绪环境评估工具转化路径清晰。',f:'配套家庭情绪环境自评量表+家庭咨询入口，可做系列（夫妻/亲子/代际）'},
  {t:'「童年烂账」亲密关系高转化',d:'TOP2 武志红背书+投射性认同+强迫性重复双理论支撑，内在小孩疗愈是核心咨询业务，转化路径极清晰。',f:'配套内在小孩识别练习+依恋模式评估+亲密关系咨询'},
  {t:'「社交面具」年轻人群强共鸣',d:'TOP3 微博热搜话题，角色期待+自我损耗理论精准命中年轻人社交焦虑， meme 属性强传播力高。',f:'配套社交面具审计+自我认同评估+真实自我探索咨询'},
  {t:'「不配得感」原生家庭系列延伸',d:'TOP4 愧疚式教育+不配得感概念精准，母女吃烧烤热搜事件自带传播属性，原生家庭咨询转化路径清晰。',f:'配套不配得感自测+前额叶重塑练习+原生家庭咨询'},
  {t:'「最养人的关系」正面收藏导向',d:'TOP5 正面导向+五大关键词易传播，收藏属性强，适合小红书9图+公众号长文双平台。',f:'配套关系健康度评估+情绪价值自测+亲密关系咨询'},
'''

opts_pattern = r'(const OPTS = \[)'
content = re.sub(opts_pattern, r'\1\n' + new_opts, content)

# ===== 7. Replace INSP_BOXES =====
new_insp_boxes = '''const INSP_BOXES = [
  {h:'重点账号',chips:['武志红心理','壹心理','KnowYourself','简单心理','心理学空间','咨询师之家']},
  {h:'本周热门话题',chips:['情绪污染','踢猫效应','童年烂账','投射性认同','强迫性重复','社交面具','角色期待','自我损耗','不配得感','愧疚式教育','最养人的关系','情绪感染链']},
  {h:'爆款标题范式',chips:['反常识标题（不是A是B）','热搜话题切入式','场景代入式','自测驱动传播式','童年创伤解读式','双平台对比式']},
  {h:'爆款内容结构',chips:['真实场景引入','心理机制解释','落地练习方法','测评转化钩子','认知重构专业深度']},
];'''

content = re.sub(r'const INSP_BOXES = \[.*?\];', new_insp_boxes, content, flags=re.DOTALL)

# ===== 8. Replace SRC_LINKS =====
new_src_links = '''const SRC_LINKS = [
  'https://new.qq.com/rain/a/20260801A06PH700','一个家庭最可怕的不是贫穷，而是「情绪污染」（2026-08-01）',
  'https://new.qq.com/rain/a/20260802A05GZO00','我们都试图在伴侣身上解决自己的童年烂账（2026-08-02）',
  'https://new.qq.com/rain/a/20260802A0AJZC00','「朋友圈和微博的差别belike」冲上热搜（2026-08-02）',
  'https://www.sohu.com/a/1057838031_122066679','别人骂你的时候，默念这一句话就赢了（2026-08-03）',
  'https://m.sohu.com/a/1055445594_122066679','什么样的关系最养人？2026年爆火心理学共识（2026）',
  'https://new.qq.com/rain/a/20260802A09W7N00','父母最大的失败，就是看不透家庭关系中这3个「残酷真相」（2026-08-02）',
  'https://new.qq.com/rain/a/20260802A00XB000','没有恐惧后，生命剩下的就是玩（2026-08-02）',
  'https://m.sohu.com/a/1057411466_122066679','人生本过客，何必千千结（2026）',
  'https://www.sohu.com/a/1057774378_122066679','爱自己才是人生的开始（2026）',
];'''

content = re.sub(r'const SRC_LINKS = \[.*?\];', new_src_links, content, flags=re.DOTALL)

# ===== 9. Replace SHOWCASE =====
new_showcase = '''const SHOWCASE = [
  {platform:'公众号',color:'#07c160',title:'推开门心就沉下去——你家是不是也有「情绪污染」',desc:'选题#1 适配。结构：陈慧回家场景代入→踢猫效应解析→情绪感染链机制→家庭情绪污染三重危害→情绪感染链可视化→家庭情绪环境四维度评估→情绪净化四步法（污染源定位/情绪温度计/15分钟隔离带/家庭情绪会议）→家庭咨询入口。适合2500字长文，标题用「共鸣型」。'},
  {platform:'小红书',color:'#ff2741',title:'朋友圈岁月静好，微博发疯——你在害怕被谁看见真实的自己',desc:'选题#3 适配。9图滑动卡片：图1-2 双平台动态对比引入→图3 角色期待理论→图4-5 自我损耗机制→图6 聚光灯效应破除→图7-8 社交面具审计+真实时刻记录→图9 建立「无表演空间」+自我认同咨询入口。文案口语化，标签#社交焦虑 #角色期待 #自我损耗 #真实自我 #心理咨询。'},
];'''

content = re.sub(r'const SHOWCASE = \[.*?\];', new_showcase, content, flags=re.DOTALL)

# ===== 10. Replace article sources =====
# Read article files
for i in range(3):
    article_file = rf"D:\workbuddy\2026-07-26-17-33-36\article-2026-08-04-0{i+1}-{'情绪污染' if i==0 else '童年烂账' if i==1 else '社交面具'}.html"
    with open(article_file, "r", encoding="utf-8") as f:
        article_html = f.read()
    
    # Extract content from .article-container
    match = re.search(r'<div class="article-container">(.*?)</div>\s*</body>', article_html, re.DOTALL)
    if match:
        article_content = match.group(1).strip()
    else:
        # fallback: extract everything inside body
        match = re.search(r'<body>.*?<div class="article-container">(.*?)</div>\s*</body>', article_html, re.DOTALL)
        if match:
            article_content = match.group(1).strip()
        else:
            article_content = article_html
    
    # Escape for JS string
    # Replace </script> inside content to avoid breaking the outer script tag
    article_content = article_content.replace('</script>', '<\\/script>')
    
    # Find and replace the article-source-i script block
    pattern = rf'(<script type="text/html" id="article-source-{i}">).*?(</script>)'
    replacement = rf'\1{article_content}\2'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open(wb_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Workbench updated successfully.")

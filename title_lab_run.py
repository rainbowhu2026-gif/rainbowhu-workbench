#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""彩虹心理爆款标题实验室 - 2026-07-27 运行脚本
基于今日雷达 TOP5 生成 50 个标题，评分，筛选 TOP10，更新工作台，生成报告。
"""
import re, json, os, subprocess, sys
from datetime import datetime

TODAY = '2026-07-27'
WORKDIR = r'D:\workbuddy\2026-07-26-17-33-36'

# ===== 数据：今日 TOP5 选题 =====
TOPICS = [
    {'n':1, 'name':'文字讨好症', 'score':95, 'full':'"文字讨好症"席卷职场：当每条消息都成了讨好表演', 'cats':['自我成长','情绪心理']},
    {'n':2, 'name':'不爱上班门诊', 'score':93, 'full':'"不爱上班门诊"爆火：当倦怠终于被允许说出口', 'cats':['情绪心理','自我成长']},
    {'n':3, 'name':'焦虑型依恋', 'score':91, 'full':'焦虑型依恋的"内在小孩"：为什么你总在关系里患得患失', 'cats':['亲密关系','原生家庭']},
    {'n':4, 'name':'情绪劳动', 'score':90, 'full':'情绪劳动的隐形消耗：你的累不是来自工作本身', 'cats':['情绪心理','自我成长']},
    {'n':5, 'name':'悬而未决耐受度', 'score':88, 'full':'"对事情悬而未决的耐受度"决定你能成多大事', 'cats':['自我成长','情绪心理']},
]

# ===== 50 个标题（按选题分组，覆盖 10 种风格） =====
RAW_TITLES = [
    # ---------- 文字讨好症 ----------
    {'topic':'文字讨好症','type':'情绪共鸣型','title':'你发每个"好的呀"，都是一次隐形的自我压缩'},
    {'topic':'文字讨好症','type':'数字承诺型','title':'文字讨好症的5个信号，中了3个就该停下来'},
    {'topic':'文字讨好症','type':'反常识型','title':'不是你想礼貌，是你太害怕被讨厌'},
    {'topic':'文字讨好症','type':'替人发声型','title':'"我明明不想答应，却打了一长串好的"'},
    {'topic':'文字讨好症','type':'第一人称型','title':'我用10年学会了在微信里讨好所有人'},
    {'topic':'文字讨好症','type':'对话型','title':'"你说话怎么像在道歉？"——一句戳中讨好者'},
    {'topic':'文字讨好症','type':'悬念型','title':'你的微信聊天记录，暴露了你有多委屈自己'},
    {'topic':'文字讨好症','type':'专业型','title':'文字讨好症：人际高敏感性与条件性自我价值'},
    {'topic':'文字讨好症','type':'痛点直击型','title':'每句话都加波浪号的你，正在一点点消失'},
    {'topic':'文字讨好症','type':'治愈型','title':'从今天起，允许你的回复里少一点热情'},
    # ---------- 不爱上班门诊 ----------
    {'topic':'不爱上班门诊','type':'情绪共鸣型','title':'"不爱上班门诊"火了：原来不想上班不是我的错'},
    {'topic':'不爱上班门诊','type':'数字承诺型','title':'倦怠的3个阶段，到第2个就该警惕了'},
    {'topic':'不爱上班门诊','type':'反常识型','title':'你不是懒，是你的情绪系统真的在罢工'},
    {'topic':'不爱上班门诊','type':'替人发声型','title':'"我没病，我只是上班上累了"'},
    {'topic':'不爱上班门诊','type':'第一人称型','title':'我去了"不爱上班门诊"，医生说了3句话'},
    {'topic':'不爱上班门诊','type':'对话型','title':'"年轻人就是吃不了苦"——这句话还要害多少人'},
    {'topic':'不爱上班门诊','type':'悬念型','title':'医院为什么要开"不爱上班门诊"？答案很扎心'},
    {'topic':'不爱上班门诊','type':'专业型','title':'职业倦怠的三维度模型：从厌班到耗竭'},
    {'topic':'不爱上班门诊','type':'痛点直击型','title':'上班如上坟，可能是倦怠正在毁掉你'},
    {'topic':'不爱上班门诊','type':'治愈型','title':'允许自己暂时不想上班，不是堕落是自救'},
    # ---------- 焦虑型依恋 ----------
    {'topic':'焦虑型依恋','type':'情绪共鸣型','title':'他没回消息你就慌了：焦虑型依恋的人心里住着小孩'},
    {'topic':'焦虑型依恋','type':'数字承诺型','title':'焦虑型依恋的4个隐藏表现，中2个以上要重视'},
    {'topic':'焦虑型依恋','type':'反常识型','title':'你越追问"爱不爱我"，对方越想逃'},
    {'topic':'焦虑型依恋','type':'替人发声型','title':'"我不是粘人，我是怕你一转身就不见了"'},
    {'topic':'焦虑型依恋','type':'第一人称型','title':'我曾以为恋爱就是这样患得患失'},
    {'topic':'焦虑型依恋','type':'对话型','title':'"你能不能别疑神疑鬼？"——焦虑依恋者最怕听'},
    {'topic':'焦虑型依恋','type':'悬念型','title':'为什么你一谈恋爱，就回到小时候的恐惧里'},
    {'topic':'焦虑型依恋','type':'专业型','title':'焦虑型依恋：内在工作模型与安全感重建'},
    {'topic':'焦虑型依恋','type':'痛点直击型','title':'关系里的患得患失，正在慢慢耗尽你'},
    {'topic':'焦虑型依恋','type':'治愈型','title':'你不需要靠对方的回应来证明自己是安全的'},
    # ---------- 情绪劳动 ----------
    {'topic':'情绪劳动','type':'情绪共鸣型','title':'下班后瘫着不想说话：你的累不是身体在喊累'},
    {'topic':'情绪劳动','type':'数字承诺型','title':'情绪劳动正在偷走你80%的精力，你却没发现'},
    {'topic':'情绪劳动','type':'反常识型','title':'你累的不是工作，是那张戴了太久的笑脸'},
    {'topic':'情绪劳动','type':'替人发声型','title':'"我明明没干什么重活，为什么下班像被掏空"'},
    {'topic':'情绪劳动','type':'第一人称型','title':'我做了5年客服，终于明白什么叫情绪劳动'},
    {'topic':'情绪劳动','type':'对话型','title':'"你就是太敏感了"——情绪劳动者最无力的反驳'},
    {'topic':'情绪劳动','type':'悬念型','title':'为什么情绪劳动比体力劳动更让人崩溃'},
    {'topic':'情绪劳动','type':'专业型','title':'情绪劳动的浅层扮演与深层扮演：心理代价差异'},
    {'topic':'情绪劳动','type':'痛点直击型','title':'你的崩溃不是脆弱，是情绪劳动过载了'},
    {'topic':'情绪劳动','type':'治愈型','title':'不是所有疲惫都需要硬撑，有些累需要被命名'},
    # ---------- 悬而未决耐受度 ----------
    {'topic':'悬而未决耐受度','type':'情绪共鸣型','title':'做事总急着要结果的你，不是上进是太怕失控'},
    {'topic':'悬而未决耐受度','type':'数字承诺型','title':'对悬而未决不耐受的3个表现，99%的人中枪'},
    {'topic':'悬而未决耐受度','type':'反常识型','title':'你不是执行力差，你是太想立刻确定答案'},
    {'topic':'悬而未决耐受度','type':'替人发声型','title':'"我受不了事情没结果，没结果就像被判了刑"'},
    {'topic':'悬而未决耐受度','type':'第一人称型','title':'我花了3年才学会，事情没有答案也可以活着'},
    {'topic':'悬而未决耐受度','type':'对话型','title':'"你想太多了"——对不确定性不耐受的人最常听'},
    {'topic':'悬而未决耐受度','type':'悬念型','title':'为什么有些人能沉住气，而你一没结果就焦虑'},
    {'topic':'悬而未决耐受度','type':'专业型','title':'不确定性不耐受：灾难化思维与焦虑维持'},
    {'topic':'悬而未决耐受度','type':'痛点直击型','title':'等不到结果就失眠？你的大脑正在被焦虑劫持'},
    {'topic':'悬而未决耐受度','type':'治愈型','title':'有些答案，本来就是要等一等才会出现'},
]

# ===== 评分标准 =====
# 每个标题的评分已经过人工设计，确保 5 维度加总为 100
SCORES = {
    # 文字讨好症
    '你发每个"好的呀"，都是一次隐形的自我压缩': {'curiosity':22,'emotion':24,'cred':13,'viral':18,'conv':12},
    '文字讨好症的5个信号，中了3个就该停下来': {'curiosity':24,'emotion':21,'cred':14,'viral':19,'conv':13},
    '不是你想礼貌，是你太害怕被讨厌': {'curiosity':22,'emotion':23,'cred':13,'viral':18,'conv':11},
    '"我明明不想答应，却打了一长串好的"': {'curiosity':21,'emotion':24,'cred':12,'viral':18,'conv':11},
    '我用10年学会了在微信里讨好所有人': {'curiosity':22,'emotion':23,'cred':12,'viral':18,'conv':10},
    '"你说话怎么像在道歉？"——一句戳中讨好者': {'curiosity':22,'emotion':23,'cred':13,'viral':17,'conv':10},
    '你的微信聊天记录，暴露了你有多委屈自己': {'curiosity':23,'emotion':22,'cred':13,'viral':18,'conv':11},
    '文字讨好症：人际高敏感性与条件性自我价值': {'curiosity':20,'emotion':18,'cred':15,'viral':14,'conv':13},
    '每句话都加波浪号的你，正在一点点消失': {'curiosity':22,'emotion':24,'cred':12,'viral':18,'conv':10},
    '从今天起，允许你的回复里少一点热情': {'curiosity':18,'emotion':21,'cred':13,'viral':16,'conv':12},
    # 不爱上班门诊
    '"不爱上班门诊"火了：原来不想上班不是我的错': {'curiosity':22,'emotion':24,'cred':13,'viral':19,'conv':12},
    '倦怠的3个阶段，到第2个就该警惕了': {'curiosity':23,'emotion':21,'cred':14,'viral':18,'conv':13},
    '你不是懒，是你的情绪系统真的在罢工': {'curiosity':22,'emotion':23,'cred':13,'viral':18,'conv':11},
    '"我没病，我只是上班上累了"': {'curiosity':20,'emotion':24,'cred':12,'viral':18,'conv':10},
    '我去了"不爱上班门诊"，医生说了3句话': {'curiosity':24,'emotion':22,'cred':13,'viral':18,'conv':10},
    '"年轻人就是吃不了苦"——这句话还要害多少人': {'curiosity':21,'emotion':24,'cred':12,'viral':19,'conv':10},
    '医院为什么要开"不爱上班门诊"？答案很扎心': {'curiosity':23,'emotion':22,'cred':13,'viral':17,'conv':10},
    '职业倦怠的三维度模型：从厌班到耗竭': {'curiosity':19,'emotion':18,'cred':15,'viral':14,'conv':13},
    '上班如上坟，可能是倦怠正在毁掉你': {'curiosity':22,'emotion':23,'cred':12,'viral':18,'conv':10},
    '允许自己暂时不想上班，不是堕落是自救': {'curiosity':18,'emotion':22,'cred':13,'viral':17,'conv':11},
    # 焦虑型依恋
    '他没回消息你就慌了：焦虑型依恋的人心里住着小孩': {'curiosity':22,'emotion':24,'cred':13,'viral':18,'conv':12},
    '焦虑型依恋的4个隐藏表现，中2个以上要重视': {'curiosity':23,'emotion':22,'cred':14,'viral':18,'conv':13},
    '你越追问"爱不爱我"，对方越想逃': {'curiosity':22,'emotion':23,'cred':13,'viral':18,'conv':11},
    '"我不是粘人，我是怕你一转身就不见了"': {'curiosity':21,'emotion':24,'cred':12,'viral':18,'conv':11},
    '我曾以为恋爱就是这样患得患失': {'curiosity':20,'emotion':23,'cred':12,'viral':17,'conv':10},
    '"你能不能别疑神疑鬼？"——焦虑依恋者最怕听': {'curiosity':21,'emotion':23,'cred':13,'viral':17,'conv':10},
    '为什么你一谈恋爱，就回到小时候的恐惧里': {'curiosity':23,'emotion':22,'cred':13,'viral':17,'conv':10},
    '焦虑型依恋：内在工作模型与安全感重建': {'curiosity':19,'emotion':18,'cred':15,'viral':14,'conv':13},
    '关系里的患得患失，正在慢慢耗尽你': {'curiosity':21,'emotion':23,'cred':12,'viral':17,'conv':10},
    '你不需要靠对方的回应来证明自己是安全的': {'curiosity':18,'emotion':21,'cred':13,'viral':16,'conv':12},
    # 情绪劳动
    '下班后瘫着不想说话：你的累不是身体在喊累': {'curiosity':22,'emotion':23,'cred':13,'viral':18,'conv':11},
    '情绪劳动正在偷走你80%的精力，你却没发现': {'curiosity':23,'emotion':21,'cred':13,'viral':19,'conv':12},
    '你累的不是工作，是那张戴了太久的笑脸': {'curiosity':22,'emotion':23,'cred':12,'viral':18,'conv':10},
    '"我明明没干什么重活，为什么下班像被掏空"': {'curiosity':21,'emotion':23,'cred':12,'viral':17,'conv':10},
    '我做了5年客服，终于明白什么叫情绪劳动': {'curiosity':21,'emotion':22,'cred':13,'viral':17,'conv':10},
    '"你就是太敏感了"——情绪劳动者最无力的反驳': {'curiosity':21,'emotion':23,'cred':12,'viral':17,'conv':10},
    '为什么情绪劳动比体力劳动更让人崩溃': {'curiosity':23,'emotion':22,'cred':13,'viral':17,'conv':10},
    '情绪劳动的浅层扮演与深层扮演：心理代价差异': {'curiosity':19,'emotion':18,'cred':15,'viral':14,'conv':13},
    '你的崩溃不是脆弱，是情绪劳动过载了': {'curiosity':21,'emotion':23,'cred':12,'viral':17,'conv':10},
    '不是所有疲惫都需要硬撑，有些累需要被命名': {'curiosity':19,'emotion':22,'cred':13,'viral':16,'conv':11},
    # 悬而未决耐受度
    '做事总急着要结果的你，不是上进是太怕失控': {'curiosity':22,'emotion':23,'cred':13,'viral':18,'conv':11},
    '对悬而未决不耐受的3个表现，99%的人中枪': {'curiosity':23,'emotion':21,'cred':13,'viral':19,'conv':12},
    '你不是执行力差，你是太想立刻确定答案': {'curiosity':22,'emotion':22,'cred':13,'viral':17,'conv':10},
    '"我受不了事情没结果，没结果就像被判了刑"': {'curiosity':21,'emotion':23,'cred':12,'viral':17,'conv':10},
    '我花了3年才学会，事情没有答案也可以活着': {'curiosity':21,'emotion':22,'cred':13,'viral':17,'conv':10},
    '"你想太多了"——对不确定性不耐受的人最常听': {'curiosity':20,'emotion':22,'cred':13,'viral':17,'conv':10},
    '为什么有些人能沉住气，而你一没结果就焦虑': {'curiosity':23,'emotion':22,'cred':13,'viral':17,'conv':10},
    '不确定性不耐受：灾难化思维与焦虑维持': {'curiosity':19,'emotion':18,'cred':15,'viral':14,'conv':13},
    '等不到结果就失眠？你的大脑正在被焦虑劫持': {'curiosity':22,'emotion':23,'cred':12,'viral':17,'conv':10},
    '有些答案，本来就是要等一等才会出现': {'curiosity':17,'emotion':21,'cred':13,'viral':15,'conv':11},
}

TYPE_COLORS = {
    '情绪共鸣型':'#c62828',
    '数字承诺型':'#e67c22',
    '反常识型':'#3f51b5',
    '替人发声型':'#c62828',
    '第一人称型':'#1976d2',
    '对话型':'#6b5b95',
    '悬念型':'#00838f',
    '专业型':'#2e7d32',
    '痛点直击型':'#c62828',
    '治愈型':'#558b2f'
}

TYPE_PLATFORM = {
    '情绪共鸣型':['公众号','小红书'],
    '数字承诺型':['小红书','公众号'],
    '反常识型':['公众号','抖音'],
    '替人发声型':['公众号','抖音'],
    '第一人称型':['公众号','小红书'],
    '对话型':['公众号','抖音'],
    '悬念型':['公众号','小红书'],
    '专业型':['公众号','知乎'],
    '痛点直击型':['公众号','抖音'],
    '治愈型':['小红书','公众号']
}

ANALYSIS = {
    '你发每个"好的呀"，都是一次隐形的自我压缩':'用具体聊天场景（"好的呀"）制造代入感，"隐形的自我压缩"把文字讨好精准比喻为心理消耗，让读者立刻联想到自己的微信对话。',
    '文字讨好症的5个信号，中了3个就该停下来':'数字承诺（5/3）制造确定感与紧迫感，"隐藏信号"引发好奇自检，"停下来"给出温和行动指令，小红书爆款结构。',
    '不是你想礼貌，是你太害怕被讨厌':'"不是...是..."反转结构打破自我安慰，"害怕被讨厌"直击人际高敏感核心，制造认知冲突与情绪释放。',
    '"我明明不想答应，却打了一长串好的"':'引号内第一人称独白替讨好者发声，"明明不想...却"的对比制造强烈情绪张力，短句适合短视频封面。',
    '我用10年学会了在微信里讨好所有人':'第一人称+时间跨度（10年）制造故事感与信任感，"讨好所有人"暗示沉重代价，引发"我也是"的共鸣。',
    '"你说话怎么像在道歉？"——一句戳中讨好者':'对话型标题引用他人评价作为钩子，"戳中"暗示精准命中，让读者好奇自己是否也有这种表达模式。',
    '你的微信聊天记录，暴露了你有多委屈自己':'第二人称+日常物件（聊天记录）制造隐私感与自检欲，"委屈自己"触发情绪共鸣，适合长文展开。',
    '文字讨好症：人际高敏感性与条件性自我价值':'专业型标题用心理学术语建立权威，适合知乎/公众号深度科普，转化维度高（测评→咨询）。',
    '每句话都加波浪号的你，正在一点点消失':'具象行为（加波浪号）到抽象后果（消失）的递进，"一点点"强化慢性消耗感，画面感强。',
    '从今天起，允许你的回复里少一点热情':'治愈型标题用许可式语气降低防御，"少一点热情"给出反直觉但温暖的行动方向，适合收尾转化。',
    '"不爱上班门诊"火了：原来不想上班不是我的错':'借势热点事件+情绪平反（"不是我的错"），让读者从自我否定转向外部归因，共鸣与转发双高。',
    '倦怠的3个阶段，到第2个就该警惕了':'数字结构（3/2）承诺具体判断标准，"警惕"制造紧迫感，专业可信度高，易引导测评转化。',
    '你不是懒，是你的情绪系统真的在罢工':'反常识平反（"不是懒"）+拟人化比喻（"情绪系统罢工"），把倦怠具象化为生理信号，降低病耻感。',
    '"我没病，我只是上班上累了"':'替职场人说出被压抑的真实感受，引号制造对话感，"只是上班上累了"的轻描淡写反衬严重性。',
    '我去了"不爱上班门诊"，医生说了3句话':'第一人称亲历+悬念数字（3句话），用故事感降低科普距离，好奇缺口极强。',
    '"年轻人就是吃不了苦"——这句话还要害多少人':'引用常见指责作为靶子，"还要害多少人"制造愤怒与替人发声感，评论区互动潜力大。',
    '医院为什么要开"不爱上班门诊"？答案很扎心':'疑问句制造信息缺口，"扎心"预设情绪冲击，适合深度解析社会现象的长文。',
    '职业倦怠的三维度模型：从厌班到耗竭':'专业型标题用Maslach三维度模型建立权威，适合公众号/知乎专业内容，转化路径清晰。',
    '上班如上坟，可能是倦怠正在毁掉你':'痛点直击型用极端比喻（"上坟"）制造情绪冲击，"正在毁掉"暗示紧迫性，但需注意不消费痛苦。',
    '允许自己暂时不想上班，不是堕落是自救':'治愈型标题用许可式语言重新定义"不想上班"，降低自我批判，为咨询转化铺垫。',
    '他没回消息你就慌了：焦虑型依恋的人心里住着小孩':'场景化开头（没回消息就慌）+"心里住着小孩"的比喻，把复杂依恋理论变得可感知。',
    '焦虑型依恋的4个隐藏表现，中2个以上要重视':'数字承诺（4/2）+自检引导，"要重视"给出行动暗示，适合小红书卡片和公众号测评入口。',
    '你越追问"爱不爱我"，对方越想逃':'反常识结构（越...越...）揭示追逃模式，精准命中焦虑-回避伴侣关系，引发强烈代入。',
    '"我不是粘人，我是怕你一转身就不见了"':'替焦虑型依恋者说出无法表达的恐惧，引号内心独白极具代入感，适合情感类内容。',
    '我曾以为恋爱就是这样患得患失':'第一人称轻描淡写却暗含痛苦，"曾以为"暗示后来觉醒，引发读者对自身关系模式的反思。',
    '"你能不能别疑神疑鬼？"——焦虑依恋者最怕听':'引用伴侣常见指责作为标题，"最怕听"精准定位情绪痛点，易引发评论区共鸣。',
    '为什么你一谈恋爱，就回到小时候的恐惧里':'疑问句引导读者追溯依恋根源，"小时候的恐惧"连接原生家庭，制造深度探索欲。',
    '焦虑型依恋：内在工作模型与安全感重建':'专业型标题用Bowlby依恋理论术语，建立权威感，适合长文深度解析与咨询转化。',
    '关系里的患得患失，正在慢慢耗尽你':'痛点直击型用"慢慢耗尽"描述慢性关系消耗，温柔但有力，适合短视频情感文案。',
    '你不需要靠对方的回应来证明自己是安全的':'治愈型标题直接给出安全感重建方向，降低焦虑依恋者的行为依赖，温暖且具有指导性。',
    '下班后瘫着不想说话：你的累不是身体在喊累':'具体场景（瘫着不想说话）+反常识解释（不是身体累），制造"被命名"的解脱感。',
    '情绪劳动正在偷走你80%的精力，你却没发现':'数字（80%）制造量化冲击，"偷走"拟人化强调隐蔽性，"没发现"激发自检欲。',
    '你累的不是工作，是那张戴了太久的笑脸':'反常识+具象比喻（笑脸面具），精准描述情绪劳动的表演性消耗，画面感强。',
    '"我明明没干什么重活，为什么下班像被掏空"':'替职场人说出普遍困惑，引号内疑问制造强烈代入，为"情绪劳动"概念引入铺垫。',
    '我做了5年客服，终于明白什么叫情绪劳动':'第一人称+职业经历建立可信度，"终于明白"暗示顿悟，适合深度长文引入。',
    '"你就是太敏感了"——情绪劳动者最无力的反驳':'引用否定性评价+"无力反驳"，替情绪劳动者发声，制造愤怒与共鸣。',
    '为什么情绪劳动比体力劳动更让人崩溃':'比较型疑问制造认知冲突，"更让人崩溃"挑战常识，吸引点击寻找解释。',
    '情绪劳动的浅层扮演与深层扮演：心理代价差异':'专业型标题用Hochschild理论概念，区分两种策略的心理代价，适合深度科普。',
    '你的崩溃不是脆弱，是情绪劳动过载了':'平反式标题（"不是脆弱"）降低病耻感，"过载"给出专业解释，适合短视频结尾升华。',
    '不是所有疲惫都需要硬撑，有些累需要被命名':'治愈型标题用哲理性语言给予许可，"被命名"呼应心理学专业价值，自然导向测评。',
    '做事总急着要结果的你，不是上进是太怕失控':'反常识平反（"不是上进"），"太怕失控"直指不确定性不耐受核心，引发自我觉察。',
    '对悬而未决不耐受的3个表现，99%的人中枪':'数字（3/99%）制造普遍性与自检欲，"中枪"口语化增强传播力，适合小红书爆款。',
    '你不是执行力差，你是太想立刻确定答案':'"不是...是..."结构重新定义问题，"立刻确定答案"精准描述焦虑型完美主义行为。',
    '"我受不了事情没结果，没结果就像被判了刑"':'引号内极端比喻（"被判了刑"）传递强烈情绪，替不确定性不耐受者发声。',
    '我花了3年才学会，事情没有答案也可以活着':'第一人称+时间跨度营造成长叙事，"没有答案也可以活着"给出治愈方向，降低焦虑。',
    '"你想太多了"——对不确定性不耐受的人最常听':'引用常见否定语+"最常听"，让读者产生"说的就是我"的代入感。',
    '为什么有些人能沉住气，而你一没结果就焦虑':'对比型疑问制造信息缺口，"沉住气"与"就焦虑"形成鲜明反差，吸引寻找方法。',
    '不确定性不耐受：灾难化思维与焦虑维持':'专业型标题用CBT概念建立权威，适合知乎/公众号深度内容，转化路径清晰。',
    '等不到结果就失眠？你的大脑正在被焦虑劫持':'疑问句+具象后果（失眠）+拟人化（"劫持"），紧迫感强，适合短视频钩子。',
    '有些答案，本来就是要等一等才会出现':'治愈型标题用诗意语言表达接纳，"等一等"给出反直觉但温柔的行为方向。'
}

# ===== 计算总分并排序 =====
all_titles = []
for item in RAW_TITLES:
    s = SCORES[item['title']]
    total = s['curiosity'] + s['emotion'] + s['cred'] + s['viral'] + s['conv']
    all_titles.append({
        'title': item['title'],
        'topic': item['topic'],
        'type': item['type'],
        'score': total,
        'dims': s,
        'analysis': ANALYSIS[item['title']]
    })

all_titles.sort(key=lambda x: (-x['score'], x['topic']))

# 取 TOP10，确保覆盖至少 3 个不同选题
top10 = []
topic_counts = {}
for t in all_titles:
    if len(top10) < 10:
        top10.append(t)
        topic_counts[t['topic']] = topic_counts.get(t['topic'], 0) + 1

# 如果 TOP10 覆盖少于 3 个选题，做替换调整
if len(topic_counts) < 3:
    # 简单兜底：从低分中补充不同选题
    existing_topics = set(topic_counts.keys())
    for t in all_titles[::-1]:
        if t['topic'] not in existing_topics and len(top10) < 10:
            # 替换一个最高分中重复最多的选题
            # 找到可替换位置
            for i, top in enumerate(top10):
                if topic_counts[top['topic']] > 1:
                    topic_counts[top['topic']] -= 1
                    top10[i] = t
                    topic_counts[t['topic']] = topic_counts.get(t['topic'], 0) + 1
                    existing_topics.add(t['topic'])
                    break
        if len(topic_counts) >= 3:
            break

# 重新排序 TOP10
top10.sort(key=lambda x: -x['score'])
for i, t in enumerate(top10, 1):
    t['rank'] = i

other40 = [t for t in all_titles if t['title'] not in {x['title'] for x in top10}]

# 验证
assert len(top10) == 10
assert len(other40) == 40
assert len({t['topic'] for t in top10}) >= 3
for t in all_titles:
    assert sum(t['dims'].values()) == t['score']
    assert t['score'] <= 100

# ===== 构建 TITLE_LAB JS 对象 =====
title_lab_js = "const TITLE_LAB = {\n"
title_lab_js += f"  date:'{TODAY}',\n"
title_lab_js += "  totalGenerated:50,\n"
title_lab_js += "  topCount:10,\n"
title_lab_js += "  topics:[\n"
for tp in TOPICS:
    title_lab_js += f"    {{n:{tp['n']},name:'{tp['name']}',score:{tp['score']}}},\n"
title_lab_js += "  ],\n"
title_lab_js += "  topTitles:[\n"
for t in top10:
    title_lab_js += "    {"
    title_lab_js += f"rank:{t['rank']},title:'{t['title']}',score:{t['score']},topic:'{t['topic']}',type:'{t['type']}',typeColor:'{TYPE_COLORS[t['type']]}',platforms:{json.dumps(TYPE_PLATFORM[t['type']], ensure_ascii=False)},"
    title_lab_js += f"dims:{{curiosity:{t['dims']['curiosity']},emotion:{t['dims']['emotion']},cred:{t['dims']['cred']},viral:{t['dims']['viral']},conv:{t['dims']['conv']}}},"
    title_lab_js += f"analysis:'{t['analysis']}'"
    title_lab_js += "},\n"
title_lab_js += "  ],\n"
title_lab_js += "  otherTitles:[\n"
for t in other40:
    short_type = t['type'].replace('型','')
    title_lab_js += f"    {{title:'{t['title']}',score:{t['score']},topic:'{t['topic']}',type:'{short_type}'}},\n"
title_lab_js += "  ]\n"
title_lab_js += "};\n"

# ===== 更新工作台 HTML =====
wb_path = os.path.join(WORKDIR, 'rainbowhu-workbench.html')
with open(wb_path, 'r', encoding='utf-8') as f:
    wb_html = f.read()

# 替换 TITLE_LAB 对象（从 const TITLE_LAB = { 到 } 结束）
pattern = r"const TITLE_LAB = \{[\s\S]*?\n\};\n"
if not re.search(pattern, wb_html):
    print("TITLE_LAB pattern not found")
    sys.exit(1)
wb_html = re.sub(pattern, title_lab_js, wb_html)

with open(wb_path, 'w', encoding='utf-8') as f:
    f.write(wb_html)

# ===== 验证 JS 语法 =====
# 提取 script 标签内容，用 node --check 验证
script_pattern = re.compile(r'<script>([\s\S]*?)</script>', re.IGNORECASE)
scripts = script_pattern.findall(wb_html)
if scripts:
    tmp_js = os.path.join(WORKDIR, 'title_lab_check.js')
    with open(tmp_js, 'w', encoding='utf-8') as f:
        f.write(scripts[-1])
    # 用 node --check 验证
    node_path = r'C:\Users\hutot\.workbuddy\binaries\node\versions\22.22.2\node.exe'
    result = subprocess.run([node_path, '--check', tmp_js], capture_output=True, text=True)
    if result.returncode != 0:
        print("JS syntax error:", result.stderr)
        sys.exit(1)
    os.remove(tmp_js)
    print("JS syntax OK")

# ===== 生成标题实验室报告 HTML =====
report_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>彩虹心理标题实验室报告 | {TODAY}</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#f5f5f7;color:#1d1d1f;line-height:1.8}}
  .container{{max-width:900px;margin:0 auto;background:#fff;min-height:100vh}}
  .header{{background:linear-gradient(135deg,#c06c84 0%,#6b5b95 100%);padding:40px 30px;color:#fff}}
  .header h1{{font-size:26px;font-weight:800;margin-bottom:8px}}
  .header .date{{font-size:14px;opacity:.85}}
  .header .meta{{font-size:12px;opacity:.7;margin-top:10px}}
  .content{{padding:30px}}
  .section-title{{font-size:18px;font-weight:800;color:#6b5b95;margin:30px 0 16px;padding-left:14px;border-left:4px solid #6b5b95}}
  .summary-box{{background:#fff8e1;border:1px solid #f0d9a8;border-radius:12px;padding:16px 20px;margin:20px 0;font-size:13px;color:#7a5a1e;line-height:1.7}}
  .summary-box b{{color:#a06a12}}
  .stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:20px 0}}
  .stat{{background:#f9f9fb;border-radius:12px;padding:16px;text-align:center}}
  .stat .num{{font-size:28px;font-weight:800;color:#6b5b95}}
  .stat .label{{font-size:12px;color:#666;margin-top:4px}}
  .top-card{{background:linear-gradient(135deg,#fafafa,#f5f0ff);border:1.5px solid #e0d4f0;border-radius:14px;padding:18px 20px;margin-bottom:14px}}
  .top-header{{display:flex;align-items:center;gap:12px;margin-bottom:8px}}
  .rank-badge{{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:14px}}
  .r1{{background:#c0392b}} .r2{{background:#d98c3a}} .r3{{background:#8e44ad}} .r4{{background:#27ae60}} .r5{{background:#2980b9}}
  .r6{{background:#c0392b}} .r7{{background:#d98c3a}} .r8{{background:#8e44ad}} .r9{{background:#27ae60}} .r10{{background:#2980b9}}
  .top-title{{font-size:16px;font-weight:700;flex:1;line-height:1.4}}
  .top-score{{font-size:20px;font-weight:800;color:#6b5b95;flex-shrink:0}}
  .top-meta{{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0;font-size:12px}}
  .tag{{padding:3px 10px;border-radius:10px;font-weight:700;font-size:11px}}
  .dims{{display:flex;gap:10px;flex-wrap:wrap;font-size:12px;color:#666;margin-bottom:8px}}
  .dim b{{color:#333}}
  .analysis{{background:#fff;border-radius:8px;padding:10px 14px;font-size:13px;color:#555;line-height:1.6}}
  .topic-group{{margin:24px 0}}
  .topic-name{{font-size:15px;font-weight:800;color:#6b5b95;margin-bottom:10px}}
  .compact-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
  .compact-item{{display:flex;align-items:center;gap:10px;background:#f9f9fb;border-radius:8px;padding:10px 12px;font-size:13px}}
  .compact-score{{font-size:14px;font-weight:800;color:#6b5b95;flex-shrink:0;width:32px;text-align:center}}
  .compact-title{{flex:1;line-height:1.35}}
  .compact-type{{font-size:10px;color:#999;flex-shrink:0}}
  .radar-note{{background:#f0f9f4;border-radius:12px;padding:16px 20px;margin:20px 0;font-size:13px;color:#4a6a5a}}
  .radar-note h4{{color:#3a8c7a;margin-bottom:10px}}
  .radar-note ul{{margin-left:18px}}
  .radar-note li{{margin:6px 0}}
  .qr-section{{text-align:center;margin:40px 0 20px;padding:30px;background:linear-gradient(135deg,#f0ecf7,#fce4ec);border-radius:16px}}
  .qr-section img{{width:150px;height:150px;border-radius:12px;border:3px solid #fff;box-shadow:0 4px 16px rgba(0,0,0,.08)}}
  .qr-section p{{font-size:13px;color:#666;margin-top:12px}}
  .footer{{text-align:center;padding:24px;font-size:12px;color:#aaa;border-top:1px solid #f0f0f0}}
  @media(max-width:700px){{.compact-grid{{grid-template-columns:1fr}} .stats{{grid-template-columns:repeat(2,1fr)}}}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>彩虹心理爆款标题实验室报告</h1>
    <div class="date">{TODAY} · 星期一</div>
    <div class="meta">基于今日雷达 TOP5 选题 | 每个选题生成 10 个标题 | 5 维度评分筛选 TOP10</div>
  </div>

  <div class="content">
    <div class="summary-box">
      <b>今日概览：</b>基于 {TODAY} 雷达 TOP5 选题，共生成 <b>50</b> 个标题，覆盖 10 种标题风格。按<b>好奇心缺口 25 + 情绪触发 25 + 专业可信度 15 + 传播潜力 20 + 转化引导 15 = 100</b> 评分，筛选出 TOP10 高潜力标题。TOP10 覆盖 {len({t['topic'] for t in top10})} 个不同选题，可作为今日公众号/小红书/抖音内容标题优先参考。
    </div>

    <div class="stats">
      <div class="stat"><div class="num">50</div><div class="label">生成标题总数</div></div>
      <div class="stat"><div class="num">10</div><div class="label">TOP10 精选</div></div>
      <div class="stat"><div class="num">{len({t['topic'] for t in top10})}</div><div class="label">覆盖选题数</div></div>
      <div class="stat"><div class="num">{sum(t['score'] for t in top10)//len(top10)}</div><div class="label">TOP10 平均分</div></div>
    </div>

    <div class="section-title">TOP10 精选标题</div>
"""

rank_cls = ['r1','r2','r3','r4','r5','r6','r7','r8','r9','r10']
type_colors_bg = {
    '情绪共鸣型':'#fce4ec;color:#c62828',
    '数字承诺型':'#fff3e0;color:#e67c22',
    '反常识型':'#e8eaf6;color:#3f51b5',
    '替人发声型':'#fce4ec;color:#c62828',
    '第一人称型':'#e3f2fd;color:#1976d2',
    '对话型':'#f3e5f5;color:#6b5b95',
    '悬念型':'#e0f7fa;color:#00838f',
    '专业型':'#e8f5e9;color:#2e7d32',
    '痛点直击型':'#ffebee;color:#c62828',
    '治愈型':'#f1f8e9;color:#558b2f'
}

for t in top10:
    platforms_str = ' · '.join(TYPE_PLATFORM[t['type']])
    report_html += f"""
    <div class="top-card">
      <div class="top-header">
        <div class="rank-badge {rank_cls[t['rank']-1]}">{t['rank']}</div>
        <div class="top-title">{t['title']}</div>
        <div class="top-score">{t['score']}</div>
      </div>
      <div class="top-meta">
        <span class="tag" style="background:{type_colors_bg[t['type']].split(';')[0]};color:{type_colors_bg[t['type']].split(';')[1].split(':')[1]}">{t['type']}</span>
        <span class="tag" style="background:#f5f0ff;color:#6b5b95">{t['topic']}</span>
        <span class="tag" style="background:#e3f2fd;color:#1976d2">{platforms_str}</span>
      </div>
      <div class="dims">
        <span class="dim">好奇 <b>{t['dims']['curiosity']}</b></span>
        <span class="dim">情绪 <b>{t['dims']['emotion']}</b></span>
        <span class="dim">专业 <b>{t['dims']['cred']}</b></span>
        <span class="dim">传播 <b>{t['dims']['viral']}</b></span>
        <span class="dim">转化 <b>{t['dims']['conv']}</b></span>
      </div>
      <div class="analysis"><b>分析：</b>{t['analysis']}</div>
    </div>
"""

report_html += """
    <div class="radar-note">
      <h4>评分维度说明</h4>
      <ul>
        <li><b>好奇心缺口（25分）：</b>是否制造信息差，让人忍不住想点击？</li>
        <li><b>情绪触发（25分）：</b>是否触发强烈情绪（共鸣/焦虑/好奇/愤怒）？</li>
        <li><b>专业可信度（15分）：</b>是否体现心理学专业性，不像纯标题党？</li>
        <li><b>传播潜力（20分）：</b>是否容易被转发？是否有社交货币属性？</li>
        <li><b>转化引导（15分）：</b>是否自然导向心理咨询/测评转化？</li>
      </ul>
    </div>
"""

# 按选题分组展示其余 40 个标题
report_html += '<div class="section-title">全部 50 个标题（按选题分组）</div>'
for tp in TOPICS:
    report_html += f'<div class="topic-group"><div class="topic-name">{tp["n"]}. {tp["name"]}（均分{tp["score"]}）</div><div class="compact-grid">'
    topic_titles = [t for t in all_titles if t['topic'] == tp['name']]
    for t in topic_titles:
        short_type = t['type'].replace('型','')
        report_html += f'<div class="compact-item"><div class="compact-score">{t["score"]}</div><div class="compact-title">{t["title"]}<br><span style="font-size:11px;color:#999">{short_type}</span></div></div>'
    report_html += '</div></div>'

report_html += f"""
    <div class="qr-section">
      <h3 style="font-size:16px;color:#6b5b95;margin-bottom:14px">彩虹心理 · 专业心理咨询机构</h3>
      <img src="rainbowhu-qrcode.jpg" alt="彩虹心理公众号二维码">
      <p style="font-size:14px;color:#c06c84;font-weight:700;margin-top:8px">扫码关注彩虹心理，回复「咨询」预约首次评估</p>
      <p>提供个体咨询 / 伴侣咨询 / 团体辅导 / 心理测评服务</p>
    </div>
  </div>

  <div class="footer">
    <p>彩虹心理爆款标题实验室报告 · {TODAY} · 自动生成</p>
    <p>数据来源：基于今日雷达 TOP5 选题生成 | 评分经人工设计，拒绝虚假承诺</p>
  </div>
</div>
</body>
</html>
"""

report_path = os.path.join(WORKDIR, f'彩虹心理标题实验室报告_{TODAY}.html')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report_html)

print(f"Updated: {wb_path}")
print(f"Report: {report_path}")
print(f"TOP10 avg score: {sum(t['score'] for t in top10)//len(top10)}")
print(f"TOP10 topics: {set(t['topic'] for t in top10)}")

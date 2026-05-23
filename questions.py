# MBTI 测评题库
# 每个维度 7 道情景对话式题目
# dimension: 维度名称, direction: 该选项对应的倾向

QUESTIONS = [
    # ===== E/I 维度 (第1-7题) =====
    {
        "id": 1,
        "dimension": "E/I",
        "scenario": "周末到了，你没有任何安排。朋友突然发消息说组了个局问你要不要来，你第一反应是？",
        "option_a": {"text": "好啊！马上收拾出门，人多热闹才开心", "direction": "E"},
        "option_b": {"text": "有点想拒绝...一个人待着刷手机也挺舒服的", "direction": "I"},
    },
    {
        "id": 2,
        "dimension": "E/I",
        "scenario": "你刚到一个新班级/新公司，中午吃饭时你会——",
        "option_a": {"text": "主动找人拼桌，顺便认识几个新朋友", "direction": "E"},
        "option_b": {"text": "找个安静的角落自己吃，等人主动来搭话", "direction": "I"},
    },
    {
        "id": 3,
        "dimension": "E/I",
        "scenario": "连续社交了好几天之后，你更想怎么恢复精力？",
        "option_a": {"text": "约朋友继续出去浪，社交本身就是充电", "direction": "E"},
        "option_b": {"text": "关上门一个人待着，安静独处才能回血", "direction": "I"},
    },
    {
        "id": 4,
        "dimension": "E/I",
        "scenario": "小组讨论时，你更习惯怎么表达想法？",
        "option_a": {"text": "边想边说，和别人碰撞灵感更有感觉", "direction": "E"},
        "option_b": {"text": "先在心里想清楚再说，不喜欢太随意的发言", "direction": "I"},
    },
    {
        "id": 5,
        "dimension": "E/I",
        "scenario": "如果你的手机一整天没响，你的感受是？",
        "option_a": {"text": "有点焦虑，总觉得自己被遗忘了", "direction": "E"},
        "option_b": {"text": "太爽了，终于没人打扰我了", "direction": "I"},
    },
    {
        "id": 6,
        "dimension": "E/I",
        "scenario": "你在社交场合中的状态更接近哪种？",
        "option_a": {"text": "认识的人超级多，走到哪都有人打招呼", "direction": "E"},
        "option_b": {"text": "就几个知心好友，但关系特别深", "direction": "I"},
    },
    {
        "id": 7,
        "dimension": "E/I",
        "scenario": "完成一个重要项目后，你更想怎么庆祝？",
        "option_a": {"text": "叫一堆朋友聚餐开趴，热闹庆祝一下", "direction": "E"},
        "option_b": {"text": "给自己买杯奶茶窝在家看剧，享受独处时光", "direction": "I"},
    },

    # ===== S/N 维度 (第8-14题) =====
    {
        "id": 8,
        "dimension": "S/N",
        "scenario": "读一本书或看一部电影时，你最容易被什么吸引？",
        "option_a": {"text": "具体的情节、人物、细节描写，越真实越好", "direction": "S"},
        "option_b": {"text": "背后的隐喻、主题和深层含义，越烧脑越好", "direction": "N"},
    },
    {
        "id": 9,
        "dimension": "S/N",
        "scenario": "老师布置了一篇论文，你会怎么开始？",
        "option_a": {"text": "先查资料、列大纲，按步骤一步步来", "direction": "S"},
        "option_b": {"text": "先发呆想一个有趣的切入点，灵感来了再动笔", "direction": "N"},
    },
    {
        "id": 10,
        "dimension": "S/N",
        "scenario": "和朋友聊天时，你更常聊什么？",
        "option_a": {"text": "最近发生的事、具体经历、生活琐事", "direction": "S"},
        "option_b": {"text": "各种假设、脑洞、未来畅想、哲学话题", "direction": "N"},
    },
    {
        "id": 11,
        "dimension": "S/N",
        "scenario": "你更信赖哪种判断？",
        "option_a": {"text": "亲眼看到的、有数据支撑的事实经验", "direction": "S"},
        "option_b": {"text": "直觉告诉我的、虽然说不清但就是觉得对的灵感", "direction": "N"},
    },
    {
        "id": 12,
        "dimension": "S/N",
        "scenario": "旅游时你更喜欢哪种玩法？",
        "option_a": {"text": "按攻略打卡知名景点，吃经典美食，不留遗憾", "direction": "S"},
        "option_b": {"text": "随心溜达，走走没走过的巷子，偶遇惊喜", "direction": "N"},
    },
    {
        "id": 13,
        "dimension": "S/N",
        "scenario": "面对一个新问题，你的第一反应更接近哪种？",
        "option_a": {"text": "先看过去类似问题是怎么解决的，照经验来", "direction": "S"},
        "option_b": {"text": "不管以前怎么做的，想想有没有全新的解法", "direction": "N"},
    },
    {
        "id": 14,
        "dimension": "S/N",
        "scenario": "你更欣赏哪种人？",
        "option_a": {"text": "脚踏实地、注重细节、靠谱稳当的人", "direction": "S"},
        "option_b": {"text": "天马行空、创意无限、敢想敢做的人", "direction": "N"},
    },

    # ===== T/F 维度 (第15-21题) =====
    {
        "id": 15,
        "dimension": "T/F",
        "scenario": "好朋友哭着找你倾诉失恋了，你第一反应是？",
        "option_a": {"text": "帮 Ta 理性分析这段关系的问题，给出客观建议", "direction": "T"},
        "option_b": {"text": "先陪 Ta 一起难过，告诉 Ta 你在，情绪比道理重要", "direction": "F"},
    },
    {
        "id": 16,
        "dimension": "T/F",
        "scenario": "团队里要淘汰一个人，一个能力差但人缘好，一个能力强但人品堪忧，你投谁？",
        "option_a": {"text": "留能力强的，团队产出才是核心，人品问题另说", "direction": "T"},
        "option_b": {"text": "留人缘好的，团队氛围和信任比能力更重要", "direction": "F"},
    },
    {
        "id": 17,
        "dimension": "T/F",
        "scenario": "做重要决定时，你更看重什么？",
        "option_a": {"text": "逻辑分析和客观事实，对错比人情重要", "direction": "T"},
        "option_b": {"text": "相关人员的感受和价值观，和谐比对错重要", "direction": "F"},
    },
    {
        "id": 18,
        "dimension": "T/F",
        "scenario": "有人当面批评你做的事，你的第一反应是？",
        "option_a": {"text": "先判断他说得对不对，有道理就接受", "direction": "T"},
        "option_b": {"text": "先感到不舒服或受伤，然后才去想他说得对不对", "direction": "F"},
    },
    {
        "id": 19,
        "dimension": "T/F",
        "scenario": "选课/选专业时，你更在意什么？",
        "option_a": {"text": "这门课的性价比、对未来发展的实际用处", "direction": "T"},
        "option_b": {"text": "自己喜不喜欢、老师好不好、课程氛围舒不舒服", "direction": "F"},
    },
    {
        "id": 20,
        "dimension": "T/F",
        "scenario": "你在争论中更常扮演什么角色？",
        "option_a": {"text": "坚持逻辑立场，即使这样会让人不高兴", "direction": "T"},
        "option_b": {"text": "主动退让或寻找折中方案，维护关系比赢更重要", "direction": "F"},
    },
    {
        "id": 21,
        "dimension": "T/F",
        "scenario": "如果朋友做了一个你认为很蠢的决定，你会？",
        "option_a": {"text": "直接告诉他哪里不对，真朋友就应该说实话", "direction": "T"},
        "option_b": {"text": "委婉提醒或者等他自己发现，怕说太直接伤感情", "direction": "F"},
    },

    # ===== J/P 维度 (第22-28题) =====
    {
        "id": 22,
        "dimension": "J/P",
        "scenario": "期末考试还有两周，你的复习状态是？",
        "option_a": {"text": "早就按计划在复习了，每天有每天的任务", "direction": "J"},
        "option_b": {"text": "还没开始...但相信最后几天爆肝也能搞定", "direction": "P"},
    },
    {
        "id": 23,
        "dimension": "J/P",
        "scenario": "出门旅行前，你的行李准备方式是？",
        "option_a": {"text": "提前列清单，头天晚上就收拾好，反复确认", "direction": "J"},
        "option_b": {"text": "出发前一小时才开始扔东西进箱子，走到哪算哪", "direction": "P"},
    },
    {
        "id": 24,
        "dimension": "J/P",
        "scenario": "你更喜欢哪种工作/学习节奏？",
        "option_a": {"text": "有明确的时间表和deadline，按部就班推进", "direction": "J"},
        "option_b": {"text": "自由灵活，跟着感觉走，deadline是第一生产力", "direction": "P"},
    },
    {
        "id": 25,
        "dimension": "J/P",
        "scenario": "你的桌面/房间通常是什么状态？",
        "option_a": {"text": "整整齐齐，东西都有固定位置", "direction": "J"},
        "option_b": {"text": "看起来有点乱，但我知道每样东西在哪", "direction": "P"},
    },
    {
        "id": 26,
        "dimension": "J/P",
        "scenario": "临时有计划变动，你的反应是？",
        "option_a": {"text": "有点烦躁，原计划被打乱了不太舒服", "direction": "J"},
        "option_b": {"text": "无所谓，甚至有点兴奋，变化才有意思", "direction": "P"},
    },
    {
        "id": 27,
        "dimension": "J/P",
        "scenario": "做一个项目时，你更倾向？",
        "option_a": {"text": "先定好整体框架和计划，再按步骤执行", "direction": "J"},
        "option_b": {"text": "先动手做做看，走一步看一步，随时调整", "direction": "P"},
    },
    {
        "id": 28,
        "dimension": "J/P",
        "scenario": "如果一件事你决定了要做，你会？",
        "option_a": {"text": "立刻行动，尽快完成，心里记着这事不舒服", "direction": "J"},
        "option_b": {"text": "不着急，deadline之前做完就行，说不定会有新想法", "direction": "P"},
    },
]

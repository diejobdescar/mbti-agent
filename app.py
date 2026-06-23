import streamlit as st
import random
from openai import OpenAI
from questions import QUESTIONS
from mbti_data import MBTI_TYPES, DIMENSION_INFO

# ========== 页面配置 ==========
st.set_page_config(
    page_title="MBTI 性格探索之旅",
    page_icon="🧠",
    layout="wide",
)

# ========== 自定义样式 ==========
st.markdown("""
<style>
    /* 聊天消息间距 */
    .stChatMessage { padding: 8px 0; }

    /* 结果大卡片 */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 36px 30px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(102,126,234,0.3);
    }
    .result-type {
        font-size: 56px;
        font-weight: 800;
        letter-spacing: 6px;
    }
    .result-name {
        font-size: 22px;
        margin-top: 8px;
        opacity: 0.92;
    }
    .result-motto {
        font-size: 14px;
        margin-top: 10px;
        opacity: 0.75;
        font-style: italic;
    }

    /* 双色进度条容器 */
    .dim-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 10px 0;
    }
    .dim-label-l {
        width: 52px;
        text-align: right;
        font-weight: 700;
        font-size: 15px;
        color: #667eea;
    }
    .dim-label-r {
        width: 52px;
        text-align: left;
        font-weight: 700;
        font-size: 15px;
        color: #764ba2;
    }
    .dual-bar-wrap {
        flex: 1;
        height: 22px;
        border-radius: 11px;
        overflow: hidden;
        display: flex;
        background: #f0f0f0;
    }
    .bar-left-seg {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #8fa0f5);
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 6px;
        font-size: 11px;
        color: white;
        font-weight: 600;
        min-width: 28px;
        transition: width 0.6s ease;
    }
    .bar-right-seg {
        height: 100%;
        background: linear-gradient(90deg, #9b68d6, #764ba2);
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding-left: 6px;
        font-size: 11px;
        color: white;
        font-weight: 600;
        min-width: 28px;
        transition: width 0.6s ease;
    }
    .dim-name-tag {
        font-size: 12px;
        color: #888;
        margin-top: -6px;
        margin-bottom: 6px;
        padding-left: 62px;
    }

    /* 趣味卡片 */
    .fun-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 20px 24px;
        border-radius: 14px;
        margin: 8px 0;
    }
    .fun-card-blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 20px 24px;
        border-radius: 14px;
        margin: 8px 0;
    }
    .fun-card-green {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 20px 24px;
        border-radius: 14px;
        margin: 8px 0;
    }
    .fun-card h3 { margin: 0 0 6px 0; font-size: 16px; opacity: 0.85; }
    .fun-card-blue h3 { margin: 0 0 6px 0; font-size: 16px; opacity: 0.85; }
    .fun-card-green h3 { margin: 0 0 6px 0; font-size: 16px; opacity: 0.85; }
    .fun-value { font-size: 24px; font-weight: 800; margin-bottom: 4px; }
    .fun-desc { font-size: 13px; opacity: 0.85; }

    /* 职业建议卡片 */
    .career-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 20px 24px;
        border-radius: 14px;
        margin: 10px 0;
        color: #5a2d0c;
    }

    /* 名言卡片 */
    .quote-card {
        border-left: 4px solid #667eea;
        background: #f8f7ff;
        padding: 16px 20px;
        border-radius: 0 12px 12px 0;
        margin: 10px 0;
        font-style: italic;
        color: #444;
    }

    /* 置信度标签 */
    .confidence-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-left: 8px;
    }
    .conf-high { background: #d4edda; color: #155724; }
    .conf-mid  { background: #fff3cd; color: #856404; }
    .conf-low  { background: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

# ========== 侧边栏：API Key ==========
with st.sidebar:
    st.header("⚙️ 设置")
    api_key = st.text_input(
        "DeepSeek API Key",
        type="password",
        help="在 https://platform.deepseek.com 获取你的 API Key",
    )
    if api_key:
        st.success("✅ API Key 已设置")
    else:
        st.warning("⚠️ 请先输入 API Key")

    st.divider()
    st.caption("🧠 MBTI 性格探索智能体 v2.0")
    st.caption("基于 DeepSeek API 的 AI 对话式测评")

    # 侧边栏显示当前进度
    if "phase" in st.session_state and st.session_state.phase == "testing":
        st.divider()
        st.caption(f"📍 当前进度：{st.session_state.current_q}/28 题")
        if "user_name" in st.session_state:
            st.caption(f"👤 测评者：{st.session_state.user_name}")

# ========== 初始化会话状态 ==========
defaults = {
    "messages": [],
    "current_q": 0,
    "answers": [],
    "phase": "onboarding",        # onboarding / testing / result
    "scores": {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0},
    "mbti_result": None,
    "analysis_data": {},           # 存储 AI 返回的结构化分析
    "user_name": "",
    "user_occupation": "",
    "shuffled_questions": [],      # 打乱后的题目顺序
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ========== DeepSeek API 调用 ==========
def call_deepseek(system_prompt, user_message, temperature=0.7, max_tokens=3000):
    """调用 DeepSeek API"""
    if not api_key:
        return "⚠️ 请先在侧边栏输入 API Key"
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ API 调用失败：{str(e)}"

# ========== 置信度计算 ==========
def get_confidence(score_a, score_b):
    """返回置信度等级和描述"""
    total = score_a + score_b
    if total == 0:
        return "mid", "未知"
    pct = max(score_a, score_b) / total
    if pct >= 0.70:
        return "high", "倾向明显"
    elif pct >= 0.57:
        return "mid", "有所倾向"
    else:
        return "low", "较为均衡"

# ========== 计算 MBTI 类型 ==========
def compute_mbti():
    s = st.session_state.scores
    mbti = ""
    mbti += "E" if s["E"] >= s["I"] else "I"
    mbti += "S" if s["S"] >= s["N"] else "N"
    mbti += "T" if s["T"] >= s["F"] else "F"
    mbti += "J" if s["J"] >= s["P"] else "P"
    return mbti

# ========== 终极分析 System Prompt ==========
SYSTEM_PROMPT_ANALYSIS = """你是一位资深的 MBTI 性格分析师，同时了解职业发展与积极心理学。
请根据用户的测评结果，生成一份结构化的 JSON 格式分析报告。

用户信息：
- 姓名：{user_name}
- 职业/专业：{occupation}
- MBTI 规则评分结果：{rule_result}
- 详细回答记录：
{answers_summary}

请严格按照以下 JSON 格式返回，不要有任何多余文字。每个字段控制在合理长度，确保整体能被完整解析：
{{
  "final_type": "XXXX",
  "type_confidence": "高/中/低",
  "core_personality": "2-3个段落，从思维运作方式、怎么感知世界、决策逻辑、内心真正在意什么四个角度剖析{user_name}的核心性格。口吻温暖、有洞察力，让用户有'说到我心里了'的感觉。每段80-120字。",
  "strengths": ["优势1", "优势2", "优势3", "优势4"],
  "blind_spots": ["盲区1（温和表述）", "盲区2", "盲区3"],
  "shadow_under_stress": "1-2个段落：在极度压力或崩溃时，{user_name}会呈现出什么样的另一面（阴影功能）？有哪些典型行为表现？每段60-80字。",
  "relationships": "1-2个段落：在友情、爱情、亲密关系中，{user_name}的典型行为模式、执念和习惯。容易吸引什么样的人，又容易和谁产生摩擦。每段60-80字。",
  "workplace_learning": "1-2个段落：适合什么样的工作环境和学习节奏，在团队中自然扮演什么角色，与什么类型的领导/同事最容易产生摩擦。每段60-80字。",
  "energy_management": "1-2个段落：什么具体场景或活动会让{user_name}快速充电，什么会快速耗尽能量。给出日常可操作的观察建议。每段60-80字。",
  "common_misconceptions": "1-2个段落：外界对这个MBTI类型最常见的误解是什么？真实的{user_name}和这些标签有哪些偏差？给用户一种'我懂你被误解'的共情。每段60-80字。",
  "growth_path": "1-2个段落：从'入门版'到'成熟版'该MBTI类型的成长路径。哪些特质需要发展，哪些习惯需要打破，给出2-3条具体可行的建议。每段60-80字。",
  "career_advice": "根据{occupation}这个职业/专业，结合MBTI类型给出2-3条具体的发展建议，要有针对性，不要泛泛而谈。控制在150字内。",
  "spirit_animal": "一种动物名称（用中文），要和该MBTI类型最贴切",
  "spirit_animal_reason": "一句话解释为什么像这种动物（20字内，有趣一点）",
  "color": "一种颜色（用中文，比如：深海蓝、晨雾灰、珊瑚橙等有意境的名字）",
  "color_reason": "一句话解释为什么是这种颜色（15字内）",
  "quote": "一句适合该MBTI类型的名人名言（中文，带出处）",
  "encouragement": "写给{user_name}的一句鼓励话（30字内，温暖有力量）"
}}"""

# ========== 辅助：渲染双色进度条 ==========
def render_dual_bar(left_letter, right_letter, left_score, right_score, dim_name):
    total = left_score + right_score
    left_pct = int(left_score / total * 100) if total > 0 else 50
    right_pct = 100 - left_pct

    conf_level, conf_text = get_confidence(left_score, right_score)
    winner = left_letter if left_score >= right_score else right_letter
    badge_class = f"conf-{conf_level}"

    st.markdown(f"""
    <div class="dim-row">
        <div class="dim-label-l">{left_letter} {left_pct}%</div>
        <div class="dual-bar-wrap">
            <div class="bar-left-seg" style="width:{left_pct}%">{left_letter}</div>
            <div class="bar-right-seg" style="width:{right_pct}%">{right_letter}</div>
        </div>
        <div class="dim-label-r">{right_pct}% {right_letter}</div>
        <span class="confidence-badge {badge_class}">{conf_text}</span>
    </div>
    <div class="dim-name-tag">{dim_name} · 倾向 {winner}</div>
    """, unsafe_allow_html=True)

# ============================================================
# ==================== 页面：信息收集 =======================
# ============================================================
if st.session_state.phase == "onboarding":
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px 20px;">
        <div style="font-size: 56px; margin-bottom: 12px;">🧠</div>
        <h1 style="font-size: 34px; margin-bottom: 10px;">MBTI 性格探索之旅</h1>
        <p style="font-size: 16px; color: #666; max-width: 480px; margin: 0 auto 8px;">
            由 AI 智能体引导你完成 28 道情景对话题，发现你真实的性格类型
        </p>
        <p style="font-size: 13px; color: #999; max-width: 460px; margin: 0 auto;">
            测试约 8-12 分钟 · 请凭第一直觉作答 · 没有对错之分 ✨
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("#### 👤 先告诉我一点关于你的信息")
        user_name_input = st.text_input(
            "你的名字或昵称",
            placeholder="叫你什么好？",
            max_chars=20,
        )
        user_occupation_input = st.text_input(
            "你的职业 / 专业",
            placeholder="例如：人力资源管理、产品经理、学生...",
            max_chars=30,
        )

        st.markdown("")

        if st.button("🚀 开始探索", use_container_width=True, type="primary"):
            if not api_key:
                st.error("请先在侧边栏输入 DeepSeek API Key！")
            elif not user_name_input.strip():
                st.warning("请填写你的名字或昵称～")
            elif not user_occupation_input.strip():
                st.warning("请填写你的职业或专业，这样结果会更有针对性哦～")
            else:
                st.session_state.user_name = user_name_input.strip()
                st.session_state.user_occupation = user_occupation_input.strip()
                # 打乱题目顺序（保证四个维度交叉出现）
                groups = {}
                for q in QUESTIONS:
                    groups.setdefault(q["dimension"], []).append(q)
                # 每个维度内部也随机
                for dim in groups:
                    random.shuffle(groups[dim])
                # 交叉合并：依次从每个维度取一题
                interleaved = []
                dim_keys = list(groups.keys())
                max_len = max(len(v) for v in groups.values())
                for i in range(max_len):
                    for dk in dim_keys:
                        if i < len(groups[dk]):
                            interleaved.append(groups[dk][i])
                st.session_state.shuffled_questions = interleaved
                st.session_state.phase = "testing"
                # 生成第一题
                q = interleaved[0]
                first_msg = (
                    f"你好，{st.session_state.user_name}！很高兴认识你～\n\n"
                    f"我们马上开始 28 道情景题，请根据第一直觉回答就好，答 A 或 B，"
                    f"也可以用自己的话描述你的感受。\n\n"
                    f"**第 1 题：**{q['scenario']}\n\n"
                    f"**A.** {q['option_a']['text']}\n"
                    f"**B.** {q['option_b']['text']}"
                )
                st.session_state.messages.append({"role": "assistant", "content": first_msg})
                st.rerun()

# ============================================================
# ==================== 页面：测评对话 =======================
# ============================================================
elif st.session_state.phase == "testing":
    # 进度条
    progress = st.session_state.current_q / 28
    st.progress(progress, text=f"📍 测评进度：{st.session_state.current_q}/28　　👤 {st.session_state.user_name}")

    # 显示历史消息
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 用户输入
    if prompt := st.chat_input(f"{st.session_state.user_name}，请输入你的回答（A / B 或用自己的话）..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 获取当前题目
        current_q = st.session_state.shuffled_questions[st.session_state.current_q]
        answer_lower = prompt.lower().strip()

        # 匹配选择
        if answer_lower in ["a", "选a", "1"]:
            chosen = "A"
        elif answer_lower in ["b", "选b", "2"]:
            chosen = "B"
        else:
            # 用 AI 判断（极简 prompt，节省 token）
            judge = call_deepseek(
                "你是MBTI判分助手，只回复单个字母A或B。",
                f"题：{current_q['scenario']}\nA:{current_q['option_a']['text']}\nB:{current_q['option_b']['text']}\n用户说：{prompt}\n选？",
                temperature=0.1,
                max_tokens=5,
            )
            chosen = "A" if "A" in judge.upper() else "B"

        # 更新得分
        if chosen == "A":
            direction = current_q["option_a"]["direction"]
        else:
            direction = current_q["option_b"]["direction"]
        st.session_state.scores[direction] += 1
        st.session_state.answers.append({
            "q_id": current_q["id"],
            "dimension": current_q["dimension"],
            "choice": chosen,
            "text": current_q[f"option_{chosen.lower()}"]["text"],
            "direction": direction,
        })

        st.session_state.current_q += 1

        if st.session_state.current_q >= 28:
            # ===== 测评完成，生成结果 =====
            st.session_state.phase = "result"
            mbti_type = compute_mbti()
            st.session_state.mbti_result = mbti_type

            answers_summary = "\n".join(
                f"第{a['q_id']}题（{a['dimension']}）：选{a['choice']} - {a['text']}"
                for a in st.session_state.answers
            )

            with st.spinner(f"🧠 AI 正在为 {st.session_state.user_name} 生成专属分析报告..."):
                raw = call_deepseek(
                    SYSTEM_PROMPT_ANALYSIS.format(
                        user_name=st.session_state.user_name,
                        occupation=st.session_state.user_occupation,
                        rule_result=mbti_type,
                        answers_summary=answers_summary,
                    ),
                    "请生成分析报告",
                    temperature=0.75,
                    max_tokens=4000,
                )

            # 解析 JSON
            import json, re
            try:
                # 提取 JSON 块
                match = re.search(r'\{.*\}', raw, re.DOTALL)
                if match:
                    data = json.loads(match.group())
                else:
                    data = {}
            except Exception:
                data = {}

            # 容错：如果解析失败用默认值
            if not data.get("final_type"):
                data["final_type"] = mbti_type
            st.session_state.analysis_data = data
            st.rerun()

        else:
            # ===== 下一题（直接输出，不调 AI，节省 token）=====
            next_q = st.session_state.shuffled_questions[st.session_state.current_q]
            q_num = st.session_state.current_q + 1

            # 偶尔加一句简短回应（纯本地生成，不调 API）
            quick_responses = [
                "明白了～", "好的，继续！", "收到～", "嗯嗯，下一题👇",
                "了解，接着来～", "好的！", "记录了～",
            ]
            ack = random.choice(quick_responses)

            next_msg = (
                f"{ack}\n\n"
                f"**第 {q_num} 题：**{next_q['scenario']}\n\n"
                f"**A.** {next_q['option_a']['text']}\n"
                f"**B.** {next_q['option_b']['text']}"
            )
            with st.chat_message("assistant"):
                st.markdown(next_msg)
            st.session_state.messages.append({"role": "assistant", "content": next_msg})

# ============================================================
# ==================== 页面：结果展示 =======================
# ============================================================
elif st.session_state.phase == "result":
    mbti = st.session_state.mbti_result
    data = st.session_state.analysis_data
    final_type = data.get("final_type", mbti)
    type_info = MBTI_TYPES.get(final_type, MBTI_TYPES.get(mbti, {}))
    name = st.session_state.user_name

    # ── 大卡片 ──
    st.markdown(f"""
    <div class="result-card">
        <div style="font-size:13px; opacity:0.7; margin-bottom:4px;">✨ {name} 的测评结果</div>
        <div class="result-type">{final_type}</div>
        <div class="result-name">{type_info.get('name', '')} — {type_info.get('motto', '')}</div>
    </div>
    """, unsafe_allow_html=True)

    # 核心性格剖析
    core = data.get("core_personality", type_info.get('traits', ''))
    if core:
        core_html = core.replace('\n', '<br>')
        st.markdown(f"""
        <div style="background: #f8f7ff; padding: 20px 24px; border-radius: 14px; margin: 16px 0; border-left: 4px solid #667eea;">
            <div style="font-size: 15px; color: #667eea; font-weight: 700; margin-bottom: 10px;">🪞 {name}，这是你的核心性格画像</div>
            <div style="font-size: 14px; color: #444; line-height: 1.8;">{core_html}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── 维度双色进度条 ──
    st.subheader("📊 各维度倾向分析")
    dims_info = [
        ("E", "I", "精力来源"),
        ("S", "N", "信息获取"),
        ("T", "F", "决策方式"),
        ("J", "P", "生活方式"),
    ]
    for l, r, dname in dims_info:
        render_dual_bar(l, r, st.session_state.scores[l], st.session_state.scores[r], dname)

    st.divider()

    # ── AI 核心分析 ──
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 💪 关键优势")
        for s in data.get("strengths", type_info.get("strengths", [])):
            st.markdown(f"- {s}")
    with col_r:
        st.markdown("#### 🔍 潜在盲区")
        for b in data.get("blind_spots", type_info.get("blind_spots", [])):
            st.markdown(f"- {b}")

    st.divider()

    # ── 深度性格剖析 ──
    st.subheader("🔮 深度性格剖析")

    if data.get("shadow_under_stress"):
        with st.expander("🌑 压力下的你（阴影面）"):
            st.markdown(data["shadow_under_stress"].replace('\n', '\n\n'))

    if data.get("relationships"):
        with st.expander("💞 关系模式"):
            st.markdown(data["relationships"].replace('\n', '\n\n'))

    if data.get("workplace_learning"):
        with st.expander("💼 职场与学习风格"):
            st.markdown(data["workplace_learning"].replace('\n', '\n\n'))

    if data.get("energy_management"):
        with st.expander("⚡ 能量管理"):
            st.markdown(data["energy_management"].replace('\n', '\n\n'))

    if data.get("common_misconceptions"):
        with st.expander("🎭 经典误解"):
            st.markdown(data["common_misconceptions"].replace('\n', '\n\n'))

    if data.get("growth_path"):
        with st.expander("🌱 成长方向"):
            st.markdown(data["growth_path"].replace('\n', '\n\n'))

    st.divider()

    # ── 职业/专业建议 ──
    if data.get("career_advice"):
        st.markdown("#### 🎯 专属职业发展建议")
        st.markdown(f"""
        <div class="career-card">
            <strong>针对「{st.session_state.user_occupation}」方向：</strong><br><br>
            {data['career_advice']}
        </div>
        """, unsafe_allow_html=True)
        st.divider()

    # ── 趣味板块 ──
    st.subheader("✨ 趣味性格标签")
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        animal = data.get("spirit_animal", "🦊 未知")
        animal_reason = data.get("spirit_animal_reason", "")
        st.markdown(f"""
        <div class="fun-card">
            <h3>🐾 你最像的动物</h3>
            <div class="fun-value">{animal}</div>
            <div class="fun-desc">{animal_reason}</div>
        </div>
        """, unsafe_allow_html=True)
    with fc2:
        color = data.get("color", "深邃紫")
        color_reason = data.get("color_reason", "")
        st.markdown(f"""
        <div class="fun-card-blue">
            <h3>🎨 你的代表色</h3>
            <div class="fun-value">{color}</div>
            <div class="fun-desc">{color_reason}</div>
        </div>
        """, unsafe_allow_html=True)
    with fc3:
        conf_level, conf_text = get_confidence(
            max(st.session_state.scores["E"], st.session_state.scores["I"]) +
            max(st.session_state.scores["S"], st.session_state.scores["N"]),
            max(st.session_state.scores["T"], st.session_state.scores["F"]) +
            max(st.session_state.scores["J"], st.session_state.scores["P"]),
        )
        overall_conf = data.get("type_confidence", "中")
        st.markdown(f"""
        <div class="fun-card-green">
            <h3>📈 结果置信度</h3>
            <div class="fun-value">{overall_conf}</div>
            <div class="fun-desc">基于 28 题综合分析</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── 名言 + 鼓励 ──
    quote = data.get("quote", "")
    encouragement = data.get("encouragement", f"{name}，你很棒！继续做真实的自己。")
    if quote:
        st.markdown(f"""
        <div class="quote-card">
            "{quote}"
        </div>
        """, unsafe_allow_html=True)
    st.success(f"💌 **给 {name} 的话：** {encouragement}")

    st.divider()

    # ── 详细信息折叠 ──
    with st.expander("🔍 查看完整类型档案"):
        st.markdown(f"**核心特质：** {type_info.get('traits', '')}")
        st.markdown("**关键优势：**")
        for s in type_info.get("strengths", []):
            st.markdown(f"- {s}")
        st.markdown("**潜在盲区：**")
        for b in type_info.get("blind_spots", []):
            st.markdown(f"- {b}")

    with st.expander("📋 查看答题详情"):
        for a in st.session_state.answers:
            st.markdown(f"**第{a['q_id']}题**（{a['dimension']}维度）：选 {a['choice']} → {a['direction']}+1")

    # ── 分享图下载 ──
    st.divider()
    st.markdown("#### 📤 分享你的结果")

    share_text = f"""✨ 我做了 MBTI 性格测评！

我的类型是：{final_type} · {type_info.get('name', '')}
"{type_info.get('motto', '')}"

各维度倾向：
E {st.session_state.scores['E']*100//7}% vs I {st.session_state.scores['I']*100//7}%
S {st.session_state.scores['S']*100//7}% vs N {st.session_state.scores['N']*100//7}%
T {st.session_state.scores['T']*100//7}% vs F {st.session_state.scores['F']*100//7}%
J {st.session_state.scores['J']*100//7}% vs P {st.session_state.scores['P']*100//7}%

我最像的动物：{data.get('spirit_animal', '')}
我的代表色：{data.get('color', '')}

"{data.get('quote', '')}"

— 基于 DeepSeek AI 的 MBTI 智能测评"""

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 下载结果文本",
            data=share_text.encode("utf-8"),
            file_name=f"MBTI_{final_type}_{name}.txt",
            mime="text/plain",
            use_container_width=True,
        )
        st.markdown("")
        if st.button("🔄 重新测试", use_container_width=True):
            for k in list(defaults.keys()):
                st.session_state[k] = defaults[k]
            st.rerun()

import streamlit as st
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
    .stChatMessage { padding: 8px 0; }
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        margin: 20px 0;
    }
    .result-type {
        font-size: 48px;
        font-weight: 800;
        letter-spacing: 4px;
    }
    .result-name {
        font-size: 20px;
        margin-top: 8px;
        opacity: 0.9;
    }
    .dimension-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 8px 0;
    }
    .bar-left, .bar-right {
        height: 24px;
        border-radius: 4px;
        transition: width 0.5s;
    }
    .bar-left { background: #667eea; }
    .bar-right { background: #764ba2; }
    .dim-label {
        width: 60px;
        text-align: center;
        font-weight: 600;
        font-size: 14px;
    }
    .percent { font-size: 12px; color: #666; min-width: 36px; }
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
    st.caption("🧠 MBTI 性格探索智能体 v1.0")
    st.caption("基于 DeepSeek API 的 AI 对话式测评")

# ========== 初始化会话状态 ==========
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "phase" not in st.session_state:
    st.session_state.phase = "welcome"  # welcome / testing / result
if "scores" not in st.session_state:
    st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
if "mbti_result" not in st.session_state:
    st.session_state.mbti_result = None
if "analysis" not in st.session_state:
    st.session_state.analysis = ""

# ========== DeepSeek API 调用 ==========
def call_deepseek(system_prompt, user_message, temperature=0.7):
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
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ API 调用失败：{str(e)}"

# ========== System Prompt ==========
SYSTEM_PROMPT_QUESTIONING = """你是一位专业且亲切的 MBTI 性格测评师。你的任务是通过对话式提问来了解用户的性格倾向。

当前你正在第 {question_num}/28 题。

请用以下方式提问：
1. 用自然、亲切的语气复述以下情景问题
2. 给出 A 和 B 两个选项，让用户选择
3. 如果用户回答模糊，用温和的方式追问
4. 不要透露这道题测的是哪个维度
5. 不要提前猜测或暗示用户的 MBTI 类型

当前题目：
{question_text}

选项A：{option_a}
选项B：{option_b}

请用你的话自然地提问，保留情景和选项的核心意思，但表达更生动亲切。"""

SYSTEM_PROMPT_ANALYSIS = """你是一位资深的 MBTI 性格分析师。根据用户在 28 道情景题中的所有回答，请进行综合分析。

用户的回答记录如下：
{answers_summary}

规则评分得出的 MBTI 类型为：{rule_result}

请你完成以下任务：
1. 分析用户在每个维度（E/I、S/N、T/F、J/P）上的倾向，结合具体回答给出判断依据
2. 给出你推断的 MBTI 类型（如果与规则评分结果不同，说明你的理由）
3. 生成一份详细的性格解析报告，包括：
   - 性格类型及名称
   - 核心特质描述（3-4句话概括）
   - 关键优势（列出3-4点）
   - 潜在盲区（列出2-3点，用温和的方式表述）
   - 适合的发展建议（2-3条具体建议）

请用温暖、专业但不过于学术的语气撰写，让用户读起来有"被理解"的感觉。"""

# ========== 欢迎页面 ==========
if st.session_state.phase == "welcome":
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <h1 style="font-size: 36px; margin-bottom: 12px;">🧠 MBTI 性格探索之旅</h1>
        <p style="font-size: 18px; color: #666; max-width: 500px; margin: 0 auto 30px;">
            由 AI 智能体引导你完成 28 道情景对话题<br>
            发现你真实的性格类型
        </p>
        <p style="font-size: 14px; color: #999; max-width: 460px; margin: 0 auto 40px;">
            测试大约需要 8-12 分钟，请根据第一直觉作答<br>
            没有对错之分，越真实越准确 ✨
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 开始探索", use_container_width=True, type="primary"):
            if not api_key:
                st.error("请先在侧边栏输入 DeepSeek API Key！")
            else:
                st.session_state.phase = "testing"
                st.session_state.current_q = 0
                # 生成第一条欢迎 + 第一题
                with st.spinner("AI 正在准备..."):
                    q = QUESTIONS[0]
                    ai_msg = call_deepseek(
                        SYSTEM_PROMPT_QUESTIONING.format(
                            question_num=1,
                            question_text=q["scenario"],
                            option_a=q["option_a"]["text"],
                            option_b=q["option_b"]["text"],
                        ),
                        "请开始提问",
                        temperature=0.8,
                    )
                st.session_state.messages.append({"role": "assistant", "content": ai_msg})
                st.rerun()

# ========== 测评对话页面 ==========
elif st.session_state.phase == "testing":
    # 显示进度
    progress = st.session_state.current_q / 28
    st.progress(progress, text=f"测评进度：{st.session_state.current_q}/28")

    # 显示历史消息
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 用户输入
    if prompt := st.chat_input("输入你的回答..."):
        # 记录用户回答
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 解析用户回答，更新得分
        current_q = QUESTIONS[st.session_state.current_q]
        answer_lower = prompt.lower().strip()

        # 简单匹配用户选择
        if answer_lower in ["a", "选a", "A", "选A", "1"]:
            direction = current_q["option_a"]["direction"]
            st.session_state.scores[direction] += 1
            st.session_state.answers.append({
                "q_id": current_q["id"],
                "dimension": current_q["dimension"],
                "choice": "A",
                "text": current_q["option_a"]["text"],
                "direction": direction,
            })
        elif answer_lower in ["b", "选b", "B", "选B", "2"]:
            direction = current_q["option_b"]["direction"]
            st.session_state.scores[direction] += 1
            st.session_state.answers.append({
                "q_id": current_q["id"],
                "dimension": current_q["dimension"],
                "choice": "B",
                "text": current_q["option_b"]["text"],
                "direction": direction,
            })
        else:
            # 用户没有直接选A/B，用AI判断倾向
            judge_prompt = f"""用户正在做MBTI测评，当前题目：
情景：{current_q["scenario"]}
选项A：{current_q["option_a"]["text"]}（倾向{current_q["option_a"]["direction"]}）
选项B：{current_q["option_b"]["text"]}（倾向{current_q["option_b"]["direction"]}）

用户的回答是："{prompt}"

请只回复A或B，表示用户的回答更接近哪个选项。只回复一个字母。"""
            judge_result = call_deepseek("你是一个MBTI测评判分助手。", judge_prompt, temperature=0.1)
            choice = judge_result.strip().upper()
            if "A" in choice:
                direction = current_q["option_a"]["direction"]
                st.session_state.scores[direction] += 1
                st.session_state.answers.append({
                    "q_id": current_q["id"],
                    "dimension": current_q["dimension"],
                    "choice": "A",
                    "text": current_q["option_a"]["text"],
                    "direction": direction,
                })
            else:
                direction = current_q["option_b"]["direction"]
                st.session_state.scores[direction] += 1
                st.session_state.answers.append({
                    "q_id": current_q["id"],
                    "dimension": current_q["dimension"],
                    "choice": "B",
                    "text": current_q["option_b"]["text"],
                    "direction": direction,
                })

        # 进入下一题或出结果
        st.session_state.current_q += 1

        if st.session_state.current_q >= 28:
            # 所有题目完成，生成结果
            st.session_state.phase = "result"
            # 规则评分
            mbti_type = ""
            mbti_type += "E" if st.session_state.scores["E"] >= st.session_state.scores["I"] else "I"
            mbti_type += "S" if st.session_state.scores["S"] >= st.session_state.scores["N"] else "N"
            mbti_type += "T" if st.session_state.scores["T"] >= st.session_state.scores["F"] else "F"
            mbti_type += "J" if st.session_state.scores["J"] >= st.session_state.scores["P"] else "P"
            st.session_state.mbti_result = mbti_type

            # AI 综合分析
            answers_summary = ""
            for a in st.session_state.answers:
                answers_summary += f"第{a['q_id']}题（{a['dimension']}维度）：选择了{a['choice']} - {a['text']}\n"

            with st.spinner("🧠 AI 正在分析你的性格..."):
                analysis = call_deepseek(
                    SYSTEM_PROMPT_ANALYSIS.format(
                        answers_summary=answers_summary,
                        rule_result=mbti_type,
                    ),
                    "请根据以上回答进行MBTI性格分析",
                    temperature=0.7,
                )
            st.session_state.analysis = analysis
            st.rerun()
        else:
            # 下一题
            next_q = QUESTIONS[st.session_state.current_q]
            with st.chat_message("assistant"):
                with st.spinner("AI 正在思考下一个问题..."):
                    ai_msg = call_deepseek(
                        SYSTEM_PROMPT_QUESTIONING.format(
                            question_num=st.session_state.current_q + 1,
                            question_text=next_q["scenario"],
                            option_a=next_q["option_a"]["text"],
                            option_b=next_q["option_b"]["text"],
                        ),
                        f"用户刚回答了第{st.session_state.current_q}题，请继续提问第{st.session_state.current_q + 1}题。用户的上一条回答：{prompt}",
                        temperature=0.8,
                    )
                st.markdown(ai_msg)
            st.session_state.messages.append({"role": "assistant", "content": ai_msg})

# ========== 结果页面 ==========
elif st.session_state.phase == "result":
    mbti = st.session_state.mbti_result
    type_info = MBTI_TYPES.get(mbti, {})

    # 大卡片展示类型
    st.markdown(f"""
    <div class="result-card">
        <div class="result-type">{mbti}</div>
        <div class="result-name">{type_info.get('name', '')} — "{type_info.get('motto', '')}"</div>
    </div>
    """, unsafe_allow_html=True)

    # 维度得分可视化
    st.subheader("📊 各维度倾向分析")
    dims = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]
    dim_names = ["精力来源", "信息获取", "决策方式", "生活方式"]

    for (left, right), name in zip(dims, dim_names):
        left_score = st.session_state.scores[left]
        right_score = st.session_state.scores[right]
        total = left_score + right_score
        left_pct = int(left_score / total * 100) if total > 0 else 50
        right_pct = 100 - left_pct

        col_l, col_bar, col_r = st.columns([2, 6, 2])
        with col_l:
            st.markdown(f"**{left}** <span style='font-size:12px;color:#888'>{DIMENSION_INFO[left[0]+'/'+right[0]][left[0]]}</span>", unsafe_allow_html=True)
        with col_bar:
            st.progress(left_pct / 100)
        with col_r:
            st.markdown(f"**{right}** <span style='font-size:12px;color:#888'>{DIMENSION_INFO[left[0]+'/'+right[0]][right[0]]}</span>", unsafe_allow_html=True)
        st.caption(f"{name}：{left} {left_pct}% — {right} {right_pct}%")

    st.divider()

    # AI 分析报告
    st.subheader("📝 AI 性格解析报告")
    st.markdown(st.session_state.analysis)

    st.divider()

    # 详细信息
    with st.expander("🔍 查看详细类型信息"):
        st.markdown(f"**核心特质：** {type_info.get('traits', '')}")
        st.markdown("**关键优势：**")
        for s in type_info.get("strengths", []):
            st.markdown(f"- {s}")
        st.markdown("**潜在盲区：**")
        for b in type_info.get("blind_spots", []):
            st.markdown(f"- {b}")

    with st.expander("📋 查看答题详情"):
        for a in st.session_state.answers:
            st.markdown(f"**第{a['q_id']}题**（{a['dimension']}维度）：选{a['choice']} → {a['direction']}+1")

    # 重新测试
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 重新测试", use_container_width=True):
            st.session_state.messages = []
            st.session_state.current_q = 0
            st.session_state.answers = []
            st.session_state.phase = "welcome"
            st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
            st.session_state.mbti_result = None
            st.session_state.analysis = ""
            st.rerun()

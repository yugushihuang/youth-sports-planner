import streamlit as st
import numpy as np

# ==========================================
# 1. 页面配置与状态初始化
# ==========================================
st.set_page_config(page_title="Sport & College Planner | 智能体教规划", layout="centered", page_icon="🏅")

if 'lang' not in st.session_state:
    st.session_state.lang = "中文"

# 心理测试的分数映射表 (A对应2分，B对应5分，C对应8分，D对应10分)
SCORE_MAP = [2, 5, 8, 10]

# ==========================================
# 2. 国际化 (i18n) 文本与场景化问卷字典
# ==========================================
UI = {
    "中文": {
        "title": "测一测：你的孩子最适合什么运动？",
        "subtitle": "西雅图大厂工程师数据建模 ✖️ NCAA 升学底层逻辑。算出身心契合度最高的“体教双轨”路线。",
        "sidebar_title": "⚙️ 偏好设置",
        "lang_switch": "🌐 语言 / Language",
        "faq_title": "👉 家长必看：什么是 NCAA？为什么科技圈都在卷体育爬藤？",
        "faq_content": """
        很多家长以为：“我又不想让娃做职业运动员，练这么苦有什么用？”
        
        其实，**体育是通往美国顶尖大学的超级捷径**。NCAA（全美大学体育协会）将大学体育分为了三个级别，玩法完全不同：
        
        🏆 **Division I (D1) - 顶级竞技场与全额奖学金**
        * **特点**：竞技水平极高，竞争最惨烈。
        * **回报**：大学会发放“全额体育奖学金 (Full Ride)”，相当于四年省下二三十万美金。
        * **适合**：极具天赋，且家庭愿意投入大量时间金钱打全美巡回赛的选手。
        
        🥈 **Division II (D2) - 高性价比的平衡区**
        * **特点**：竞技水平中上，提供部分奖学金 (Partial Scholarship)。
        * **回报**：能拿到钱，且没 D1 那么内卷。但注意，常春藤等最顶尖的学术名校不在这个级别。
        
        🎓 **Division III (D3) - 常春藤名校的聚集地（核心重点！）**
        * **特点**：包含哈佛、耶鲁等所有常春藤名校，以及 MIT、芝加哥大学等顶尖学府。
        * **规则**：D3 绝对不发体育奖学金！
        * **玩法**：教练手里掌握着极其宝贵的**“招生办支持权 (Admissions Support)”**。只要孩子有某项特长被教练看中，进入了教练的招募名单 (Recruit List)，并且高中的 GPA 达到了大学的基础门槛，教练就能直接去招生办要人。**你家孩子可以直接挤掉那些满分 GPA 但毫无特色、只能走常规申请 (Regular Decision) 的普通学霸！**
        
        **结论：体育练的不是肌肉，练的是顶尖名校最看重的：逆商、专注力与领导力。**
        """,
        "step1": "📝 第一步：身体硬件评估",
        "step1_cap": "填入真实的家庭数据，AI 将预估孩子的成年身高及发育特征。",
        "gender": "孩子性别",
        "age": "当前年龄 (岁)",
        "height": "当前身高 (cm)",
        "shoe": "与同龄人相比，孩子的鞋码/脚部特征：",
        "shoe_opt": ["明显偏小 (买鞋总买小一号)", "正常大众尺码", "明显偏大 (天生大脚)"],
        "mom_h": "母亲身高 (cm)",
        "mom_s": "母亲两臂展开长度 (cm) - 可选",
        "dad_h": "父亲身高 (cm)",
        "dad_s": "父亲两臂展开长度 (cm) - 可选",
        "unknown_span": "❓ 我不知道父母的具体臂展 (系统将按人类标准比例自动推算)",
        
        "step2": "⏳ 第二步：家庭资源与学业目标",
        "step2_cap": "体育是一场马拉松，拼的是家庭的后勤。",
        "acad": "当前学业期望水平（决定了时间分配权重）",
        "acad_opt": ["跟上学校进度即可", "学区中上游", "超前学习1-2年", "冲击高阶竞赛 (如 AMC/Kangaroo)"],
        "hours": "每周家庭能抽出多少小时用于体育？(含接送)",
        "budget": "家庭每年的体育花销预算",
        "budget_opt": ["基础班 (<$2k/年)", "中产进阶 ($5k/年，含少量私教)", "重金投入 (>$15k/年，跨州比赛)"],
        
        "step3": "🧠 第三步：场景化性格测试",
        "step3_cap": "不要猜测分数，请直接根据孩子在生活中的真实反应“对号入座”。",
        
        "psy_focus": "1. 【耐无聊指数】面对练琴、写字等枯燥任务时：",
        "psy_focus_opt": ["A. 极易分心，5分钟就坐不住", "B. 偶尔能坚持，但需要大人在旁边盯", "C. 能沉浸在自己的世界里半小时以上", "D. 极度专注，一旦投入打雷都不理会"],
        
        "psy_grit": "2. 【受挫恢复力】比赛或玩游戏输了时：",
        "psy_grit_opt": ["A. 崩溃大哭，直接放弃再也不玩了", "B. 生闷气，需要大人哄很久才能缓过来", "C. 马上擦干眼泪，要求再来一局", "D. 不仅要再来，还会拉着大人复盘怎么赢"],
        
        "psy_logic": "3. 【策略脑力】面对大人定的规则或要求时：",
        "psy_logic_opt": ["A. 乖乖听话，严格按大人的指示做", "B. 偶尔有自己的小主意", "C. 经常问“为什么”，喜欢跟大人讨价还价", "D. 疯狂找规则漏洞，甚至自己重新制定规则"],
        
        "psy_flex": "4. 【身体柔韧度】平时在家里活动时：",
        "psy_flex_opt": ["A. 比较僵硬，弯腰摸不到脚趾", "B. 正常同龄人水平", "C. 柔韧性很好，很容易下腰或劈叉", "D. 骨骼惊奇，柔软得像没有骨头一样"],
        
        "psy_perfection": "5. 【细节强迫症】画画或搭乐高时：",
        "psy_perfection_opt": ["A. 差不多就行，做事大开大合", "B. 正常完成任务即可", "C. 发现小瑕疵会懊恼一阵子想重做", "D. 极致强迫症，错一点点就要彻底推翻重来"],
        
        "psy_social": "6. 【社交依赖度】在课外活动或操场上：",
        "psy_social_opt": ["A. 极度社恐，只喜欢自己一个人躲在角落玩", "B. 慢热，熟了之后能融入小团体", "C. 害怕孤单，走到哪都必须有玩伴", "D. 终极社牛，永远是人群中心，喜欢指挥别人"],
        
        "psy_aggro": "7. 【肢体对抗欲】关于身体接触：",
        "psy_aggro_opt": ["A. 极度害怕身体碰撞，别人一碰就躲", "B. 正常跑跳，不主动推挤别人", "C. 喜欢玩抓人、摔跤等有轻微对抗的游戏", "D. 极度享受身体冲撞，像个小坦克一样横冲直撞"],
        
        "submit": "🚀 启动 AI 匹配与诊断引擎",
        "error_miss": "⚠️ 测评失败：您有漏选的题目！请将所有带 * 的输入框和下拉菜单填写完整。",
        "success": "✅ 行为特征解析完毕！专属诊断报告如下：",
        "res1_title": "🧬 诊断一：身体硬件与发育预估",
        "target_h": "预估成年身高 (Target Height)",
        "ape_index": "预估臂展特征 (Ape Index)",
        "foot_trait": "终端力学预判 (Foot Trait)",
        "res2_title": "🎯 诊断二：AI 智能匹配最高的三项运动",
        "res3_title": "⚠️ 诊断三：时间破产与防坑预警",
        "burnout_high": "🚨 红色警报：孩子极易受伤和厌学！每周训练不应超过自身年龄。",
        "burnout_low": "🟡 提示：训练强度偏佛系，健康但缺乏竞技壁垒。",
        "burnout_ok": "✅ 极佳的精力状态！完美兼顾身体与课业。",
        "cta_title": "📥 获取独家排期表，不做瞎焦虑的家长",
        "cta_desc": "**👇 添加主理人微信，获取属于你的定制方案 👇**\n### 💬 微信号：`BigMeiXiao`\n*备注【AI测评截图】，免费获取针对大西雅图/Bellevue学区的《体教统筹排期表》。*"
    },
    "English": {
        "title": "Which Sport is Best for Your Child?",
        "subtitle": "Seattle Big Tech data modeling + NCAA recruiting logic. Find the optimal Student-Athlete path.",
        "sidebar_title": "⚙️ Preferences",
        "lang_switch": "🌐 Language / 语言",
        "faq_title": "👉 Must Read: What is the NCAA? Why are Tech Parents Obsessed?",
        "faq_content": """
        Many parents think: "I don't want my kid to be a pro athlete, why train so hard?"
        
        In reality, **sports are the ultimate shortcut to elite US universities.** The NCAA divides college sports into three divisions with very different rules:
        
        🏆 **Division I (D1) - Elite Competition & Full Scholarships**
        * **Level**: The highest and most ruthless level of competition.
        * **Reward**: Coaches offer "Full Athletic Scholarships", saving $200k-$300k over four years.
        * **Fit**: For extremely talented athletes whose families can invest heavily in travel teams.
        
        🥈 **Division II (D2) - The Balanced Zone**
        * **Level**: High-level competition.
        * **Reward**: Offers Partial Scholarships. Great ROI, but top-tier academic schools (Ivy League) are not here.
        
        🎓 **Division III (D3) - The Ivy League Hack (Crucial!)**
        * **Level**: Home to the Ivy League (Harvard, Yale), MIT, UChicago, etc.
        * **Rule**: D3 does NOT offer athletic scholarships.
        * **The Hack**: Coaches hold a golden ticket called **"Admissions Support"**. If a coach wants your child on their team, and your child's GPA meets the academic baseline, the coach can pull them directly into the school. **Your child can bypass thousands of regular applicants who have perfect GPAs but no athletic edge!**
        
        **Conclusion: We aren't training muscles; we are training Grit, Focus, and Leadership.**
        """,
        "step1": "📝 Step 1: Physical Hardware",
        "step1_cap": "Enter real family data to predict adult height and physical traits.",
        "gender": "Child's Gender",
        "age": "Current Age (Years)",
        "height": "Current Height (cm)",
        "shoe": "Compared to peers, the child's shoe/foot size is:",
        "shoe_opt": ["Noticeably smaller", "Average size", "Noticeably larger (Flippers)"],
        "mom_h": "Mother's Height (cm)",
        "mom_s": "Mother's Arm Span (cm) - Optional",
        "dad_h": "Father's Height (cm)",
        "dad_s": "Father's Arm Span (cm) - Optional",
        "unknown_span": "❓ I don't know the exact arm spans (System will use standard human proportions)",
        
        "step2": "⏳ Step 2: Resources & Goals",
        "step2_cap": "Youth sports is a marathon; it relies on family logistics.",
        "acad": "Current Academic Expectation",
        "acad_opt": ["Keep up with school", "Above average", "1-2 years ahead", "Elite competitions (e.g., AMC)"],
        "hours": "Weekly hours available for sports? (incl. commute)",
        "budget": "Annual Sports Budget",
        "budget_opt": ["Basic (<$2k/yr)", "Intermediate ($5k/yr, some private)", "Elite (>$15k/yr, travel teams)"],
        
        "step3": "🧠 Step 3: Behavioral Scenarios",
        "step3_cap": "Select the scenario that best describes your child's real-life behavior.",
        
        "psy_focus": "1. [Focus] When doing boring/repetitive tasks:",
        "psy_focus_opt": ["A. Easily distracted, can't sit for 5 mins", "B. Persists briefly but needs adult supervision", "C. Can immerse themselves for over 30 mins", "D. Extreme focus; ignores everything around them"],
        
        "psy_grit": "2. [Grit] When losing a game:",
        "psy_grit_opt": ["A. Cries, quits, and refuses to play again", "B. Sulks and needs a long time to recover", "C. Wipes tears and immediately asks for a rematch", "D. Asks for a rematch and analyzes why they lost"],
        
        "psy_logic": "3. [Tactics] When facing rules:",
        "psy_logic_opt": ["A. Obediently follows instructions", "B. Occasionally has their own ideas", "C. Constantly asks 'why' and bargains", "D. Actively looks for loopholes or invents new rules"],
        
        "psy_flex": "4. [Flexibility] Physical flexibility at home:",
        "psy_flex_opt": ["A. Stiff; can't touch toes", "B. Average for their age", "C. Very flexible; can do splits easily", "D. Almost double-jointed; extremely bendy"],
        
        "psy_perfection": "5. [Perfectionism] When drawing or building Lego:",
        "psy_perfection_opt": ["A. Doesn't care about details; very rough", "B. Completes the task normally", "C. Gets upset over small flaws", "D. Extreme perfectionist; restarts if one thing is wrong"],
        
        "psy_social": "6. [Social] During recess or group activities:",
        "psy_social_opt": ["A. Introverted; prefers playing alone in a corner", "B. Slow to warm up, but integrates eventually", "C. Scared of being alone; needs constant companions", "D. Ultimate extrovert; always the center of attention and loves commanding others"],
        
        "psy_aggro": "7. [Aggression] Regarding physical contact:",
        "psy_aggro_opt": ["A. Afraid of contact; avoids it completely", "B. Runs normally; doesn't initiate pushing", "C. Enjoys tag or light wrestling", "D. Loves physical collisions; charges like a little tank"],
        
        "submit": "🚀 Launch AI Matching Engine",
        "error_miss": "⚠️ Error: Missing inputs! Please fill out all required fields.",
        "success": "✅ Behavioral traits parsed! Here is your exclusive report:",
        "res1_title": "🧬 Diagnosis 1: Physical Projections",
        "target_h": "Projected Target Height",
        "ape_index": "Projected Ape Index (Wingspan)",
        "foot_trait": "Terminal Biomechanics (Feet)",
        "res2_title": "🎯 Diagnosis 2: Top 3 Recommended Sports",
        "res3_title": "⚠️ Diagnosis 3: Burnout & Time Warning",
        "burnout_high": "🚨 RED ALERT: High risk of injury and burnout! Weekly hours should not exceed age.",
        "burnout_low": "🟡 Note: Relaxed pace. Healthy, but lacks competitive edge for recruiting.",
        "burnout_ok": "✅ Excellent energy balance! Perfect harmony of physical and academic load.",
        "cta_title": "📥 Get Your Exclusive Schedule & Stop Stressing",
        "cta_desc": "**👇 Add the Founder on WeChat for a Custom Plan 👇**\n### 💬 WeChat ID: `BigMeiXiao`\n*Mention [AI Report] for a free 15-min schedule audit & Bellevue/Seattle Club Guide.*"
    }
}

# 深度运动特征数据库 (带双语 Edu 科普)
SPORTS_DB = {
    "游泳 / Swimming": {
        "vector": np.array([0.7, 0.9, 1.0, 0.4, 0.6, 0.5, 1.0, 0.2, 0.1, 0.4]),
        "edu_CN": "🏊‍♂️ **[心肺发动机 & 绝对专注]**：在水下隔绝外界干扰，极大地锻炼“极其枯燥环境”下的深度专注力。",
        "edu_EN": "🏊‍♂️ **[Cardio Engine & Ultimate Focus]**：Water isolates noise, training deep focus in a highly repetitive environment."
    },
    "跳水 / Diving": {
        "vector": np.array([0.2, 0.3, 0.9, 1.0, 0.9, 0.8, 0.8, 0.4, 0.1, 0.5]),
        "edu_CN": "🦘 **[三维建模 & 胆识]**：滞空状态下完成大脑对身体的高速控制，是对前庭觉和胆量的顶级历练。系统敏锐捕捉到脚小的特征，压水花有巨大优势。",
        "edu_EN": "🦘 **[3D Spatial & Courage]**：Requires high-speed brain-body control in zero gravity. Smaller feet provide a massive advantage for a clean entry."
    },
    "体操 / Gymnastics": {
        "vector": np.array([0.1, 0.2, 0.1, 1.0, 0.9, 0.9, 0.9, 0.3, 0.2, 0.6]),
        "edu_CN": "🤸‍♀️ **[万物之母]**：建立无与伦比的“本体感受器”。有了体操底子，以后转练田径、跳水都是降维打击。",
        "edu_EN": "🤸‍♀️ **[The Mother of Sports]**：Builds unmatched proprioception. The ultimate physical foundation for any future sport."
    },
    "击剑 / Fencing": {
        "vector": np.array([0.6, 0.9, 0.1, 0.6, 0.8, 0.7, 0.6, 1.0, 0.2, 0.8]),
        "edu_CN": "🤺 **[动态西洋棋]**：零点几秒内预判对手意图并反击，极度锻炼逻辑推理，常春藤招生官最爱的“学霸运动”。",
        "edu_EN": "🤺 **[Dynamic Chess]**：High-speed mental warfare. Trains split-second logical reasoning; highly favored by the Ivy League."
    },
    "高尔夫 / Golf": {
        "vector": np.array([0.4, 0.5, 0.1, 0.6, 0.3, 1.0, 0.9, 0.9, 0.2, 1.0]),
        "edu_CN": "⛳ **[挫折管理]**：自己与自己的斗争。要求在巨大心理波动下瞬间清空负面情绪，练的是顶级的情绪管理 (EQ)。",
        "edu_EN": "⛳ **[Frustration Management]**：A battle against oneself. Trains the ultimate EQ to clear negative emotions instantly after a bad shot."
    },
    "网球 / Tennis": {
        "vector": np.array([0.7, 0.8, 0.1, 0.5, 0.8, 0.9, 0.7, 0.8, 0.1, 0.9]),
        "edu_CN": "🎾 **[孤胆英雄]**：禁止场外指导。必须像孤独的将军一样自己调整战术，培养独立领导力和临场应变能力。",
        "edu_EN": "🎾 **[The Lone Hero]**：No coaching allowed mid-match. Trains extreme independent decision-making and resilience."
    },
    "赛艇 / Rowing": {
        "vector": np.array([0.9, 0.9, 0.1, 0.3, 0.7, 0.8, 0.9, 0.2, 1.0, 0.7]),
        "edu_CN": "🚣‍♀️ **[齿轮般的协作]**：常春藤最古老的传统项目。要求8个人像一台机器一样精准同步，极度考验忍耐力与服从性。",
        "edu_EN": "🚣‍♀️ **[Ultimate Synchronization]**：The oldest Ivy League tradition. Requires complete ego surrender and synchronized endurance."
    },
    "水球 / Water Polo": {
        "vector": np.array([0.8, 0.9, 0.8, 0.5, 0.8, 0.7, 0.4, 0.8, 0.9, 0.5]),
        "edu_CN": "🤽‍♂️ **[全能战士]**：结合了游泳耐力、篮球视野和极强的水下身体对抗。缺氧状态下保持战术执行力，大局观极佳。",
        "edu_EN": "🤽‍♂️ **[Aquatic Gladiators]**：Combines swimming endurance with basketball vision and extreme physical contact."
    },
    "排球 / Volleyball": {
        "vector": np.array([1.0, 0.9, 0.1, 0.4, 0.9, 0.6, 0.4, 0.7, 1.0, 0.4]),
        "edu_CN": "🏐 **[情绪传导]**：球不能落地的运动，极其依赖队友间的补位和情绪鼓励，是培养高阶同理心和领导力的最佳运动。",
        "edu_EN": "🏐 **[Emotional Conductor]**：A sport where the ball cannot touch the ground. Teaches supreme empathy and active encouragement."
    }
}

# ==========================================
# 4. 侧边栏与语言切换逻辑
# ==========================================
st.sidebar.markdown(f"### {UI[st.session_state.lang]['sidebar_title']}")
selected_lang = st.sidebar.radio(UI[st.session_state.lang]['lang_switch'], ["中文", "English"])
if selected_lang != st.session_state.lang:
    st.session_state.lang = selected_lang
    st.rerun()

t = UI[st.session_state.lang]

# ==========================================
# 5. 前端 UI 与表单收集
# ==========================================
st.title(t["title"])
st.markdown(t["subtitle"])

with st.expander(t["faq_title"], expanded=False):
    st.markdown(t["faq_content"])

st.divider()

with st.form("main_form"):
    
    st.header(t["step1"])
    st.caption(t["step1_cap"])
    
    col1, col2 = st.columns(2)
    with col1:
        child_gender = st.selectbox(t["gender"], options=["女/Female", "男/Male"], index=None)
    with col2:
        child_age = st.number_input(t["age"], min_value=3, max_value=16, value=None)
        
    child_height = st.number_input(t["height"], min_value=80, max_value=200, value=None)
    shoe_size_trait = st.selectbox(t["shoe"], options=t["shoe_opt"], index=None)

    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        mom_h = st.number_input(t["mom_h"], min_value=140, max_value=190, value=None)
        mom_span = st.number_input(t["mom_s"], min_value=140, max_value=190, value=None)
    with p_col2:
        dad_h = st.number_input(t["dad_h"], min_value=150, max_value=210, value=None)
        dad_span = st.number_input(t["dad_s"], min_value=150, max_value=210, value=None)

    span_unknown = st.checkbox(t["unknown_span"])

    st.header(t["step2"])
    st.caption(t["step2_cap"])
    
    academic_level = st.selectbox(t["acad"], options=t["acad_opt"], index=None)
    weekly_budget_hours = st.selectbox(t["hours"], options=[2, 4, 6, 8, 10, 12, 15, 20, 25], index=None)
    budget_level = st.selectbox(t["budget"], options=t["budget_opt"], index=None)

    # 替换为场景化测试题
    st.header(t["step3"])
    st.caption(t["step3_cap"])
    
    psy_focus_ans = st.selectbox(t["psy_focus"], options=t["psy_focus_opt"], index=None)
    psy_grit_ans = st.selectbox(t["psy_grit"], options=t["psy_grit_opt"], index=None)
    psy_logic_ans = st.selectbox(t["psy_logic"], options=t["psy_logic_opt"], index=None)
    psy_flex_ans = st.selectbox(t["psy_flex"], options=t["psy_flex_opt"], index=None)
    psy_perfection_ans = st.selectbox(t["psy_perfection"], options=t["psy_perfection_opt"], index=None)
    psy_social_ans = st.selectbox(t["psy_social"], options=t["psy_social_opt"], index=None)
    psy_aggro_ans = st.selectbox(t["psy_aggro"], options=t["psy_aggro_opt"], index=None)

    submit_btn = st.form_submit_button(t["submit"], use_container_width=True)

# ==========================================
# 6. 后端算法解析与结果渲染
# ==========================================
if submit_btn:
    # 动态必填校验
    req_inputs = [child_gender, child_age, child_height, shoe_size_trait, mom_h, dad_h, 
                  academic_level, weekly_budget_hours, budget_level, 
                  psy_focus_ans, psy_grit_ans, psy_logic_ans, psy_flex_ans, psy_perfection_ans, psy_social_ans, psy_aggro_ans]
    
    if not span_unknown:
        req_inputs.extend([mom_span, dad_span])
    
    if any(v is None for v in req_inputs):
        st.error(t["error_miss"])
    else:
        st.success(t["success"])
        
        # 将选项 A/B/C/D 转换回底层算法需要的 1-10 分
        psy_focus = SCORE_MAP[t["psy_focus_opt"].index(psy_focus_ans)]
        psy_grit = SCORE_MAP[t["psy_grit_opt"].index(psy_grit_ans)]
        psy_logic = SCORE_MAP[t["psy_logic_opt"].index(psy_logic_ans)]
        psy_flex = SCORE_MAP[t["psy_flex_opt"].index(psy_flex_ans)]
        psy_perfection = SCORE_MAP[t["psy_perfection_opt"].index(psy_perfection_ans)]
        psy_social = SCORE_MAP[t["psy_social_opt"].index(psy_social_ans)]
        psy_aggro = SCORE_MAP[t["psy_aggro_opt"].index(psy_aggro_ans)]

        # 靶身高推算
        is_male = "男" in child_gender or "Male" in child_gender
        if is_male:
            target_height = (mom_h + dad_h + 13) / 2
        else:
            target_height = (mom_h + dad_h - 13) / 2
            
        # 臂展盲盒容错
        active_mom_span = mom_h if span_unknown else mom_span
        active_dad_span = dad_h if span_unknown else dad_span
        
        mom_index = active_mom_span - mom_h
        dad_index = active_dad_span - dad_h
        genetic_ape_index = (mom_index + dad_index) / 2
        
        st.header(t["res1_title"])
        st.info(f"**📏 {t['target_h']}：{target_height:.1f} cm**")
        
        span_note = " (基于标准人类比例自动推算)" if span_unknown else ""
        st.info(f"**🦅 {t['ape_index']}：{genetic_ape_index:+.1f} cm**{span_note}")
        st.info(f"**👣 {t['foot_trait']}：{shoe_size_trait}**")

        # 归一化运算
        budget_score = 0.3 if ("基础" in budget_level or "Basic" in budget_level) else (0.6 if ("中产" in budget_level or "Intermediate" in budget_level) else 1.0)
        
        user_vec = np.array([
            target_height / 195.0,  
            (target_height + genetic_ape_index) / 195.0, 
            0.2 if ("小" in shoe_size_trait or "smaller" in shoe_size_trait) else (1.0 if ("大" in shoe_size_trait or "larger" in shoe_size_trait) else 0.6), 
            psy_flex / 10.0,       
            psy_aggro / 10.0,      
            psy_grit / 10.0,       
            psy_focus / 10.0,      
            psy_logic / 10.0,      
            psy_social / 10.0,     
            budget_score           
        ])

        scores = {}
        for sport, data in SPORTS_DB.items():
            sport_vec = data["vector"]
            similarity = np.dot(user_vec, sport_vec) / (np.linalg.norm(user_vec) * np.linalg.norm(sport_vec))
            edu_key = "edu_CN" if st.session_state.lang == "中文" else "edu_EN"
            scores[sport] = {"score": round(similarity * 100, 1), "edu": data[edu_key]}

        sorted_sports = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
        
        st.divider()
        st.header(t["res2_title"])
        
        for i in range(3):
            sport_name = sorted_sports[i][0]
            sport_score = sorted_sports[i][1]["score"]
            sport_edu = sorted_sports[i][1]["edu"]
            
            st.markdown(f"### 🏆 Top {i+1}: {sport_name}")
            st.markdown(f"**Match: {sport_score}%**")
            st.write(sport_edu)
            st.markdown("---")

        st.divider()
        st.header(t["res3_title"])
        
        if weekly_budget_hours > child_age + 3:
            st.error(t["burnout_high"])
        elif weekly_budget_hours < child_age - 2:
            st.warning(t["burnout_low"])
        else:
            st.success(t["burnout_ok"])

        st.divider()
        st.header(t["cta_title"])
        st.success(t["cta_desc"])

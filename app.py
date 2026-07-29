import streamlit as st
import numpy as np

# ==========================================
# 1. 全局配置与状态管理
# ==========================================
st.set_page_config(page_title="Sport & College Planner | 智能体教规划", layout="centered", page_icon="🏅")

if 'lang' not in st.session_state:
    st.session_state.lang = "中文"

# 心理测试分数映射表 (严格索引映射)
SCORE_MAP = [2, 5, 8, 10]

# ==========================================
# 2. 完整无缺的多语言字典与配置库 (i18n)
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
        * **回报**：大学会发放“全额体育奖学金 (Full Ride)”，相当于四年省下二三十万美金。适合极具天赋且能全职投入的家庭。
        
        🥈 **Division II (D2) - 高性价比的平衡区**
        * **回报**：提供部分奖学金，性价比高。但注意，常春藤等最顶尖的学术名校不在这个级别。
        
        🎓 **Division III (D3) - 常春藤名校的聚集地（核心重点！）**
        * **特点**：包含哈佛、耶鲁等所有常春藤，以及 MIT、芝大等。**D3 绝对不发体育奖学金！**
        * **核心玩法**：教练手里掌握着极其宝贵的**“招生办支持权 (Admissions Support)”**。只要孩子有特长被教练看中，且高中的 GPA 达到基础门槛，教练就能直接去招生办要人。**可以直接挤掉那些满分 GPA 但毫无特色、只能走常规申请的普通学霸！**
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
        "psy_focus_opt": ["极易分心，5分钟就坐不住", "偶尔能坚持，但需要大人盯", "能沉浸在自己的世界里半小时以上", "极度专注，一旦投入打雷都不理会"],
        "psy_grit": "2. 【受挫恢复力】比赛或玩游戏输了时：",
        "psy_grit_opt": ["崩溃大哭，直接放弃再也不玩了", "生闷气，需要大人哄很久才能缓过来", "马上擦干眼泪，要求再来一局", "不仅要再来，还会拉着大人复盘怎么赢"],
        "psy_logic": "3. 【策略脑力】面对大人定的规则或要求时：",
        "psy_logic_opt": ["乖乖听话，严格按大人的指示做", "偶尔有自己的小主意", "经常问“为什么”，喜欢跟大人讨价还价", "疯狂找规则漏洞，甚至自己重新制定规则"],
        "psy_flex": "4. 【身体柔韧度】平时在家里活动时：",
        "psy_flex_opt": ["比较僵硬，弯腰摸不到脚趾", "正常同龄人水平", "柔韧性很好，很容易下腰或劈叉", "骨骼惊奇，柔软得像没有骨头一样"],
        "psy_perfection": "5. 【细节强迫症】画画或搭乐高时：",
        "psy_perfection_opt": ["差不多就行，做事大开大合", "正常完成任务即可", "发现小瑕疵会懊恼一阵子想重做", "极致强迫症，错一点点就要推翻重来"],
        "psy_social": "6. 【社交依赖度】在课外活动或操场上：",
        "psy_social_opt": ["极度社恐，只喜欢自己一个人躲在角落玩", "慢热，熟了之后能融入小团体", "害怕孤单，走到哪都必须有玩伴", "终极社牛，永远是人群中心，喜欢指挥别人"],
        "psy_aggro": "7. 【肢体对抗欲】关于身体接触：",
        "psy_aggro_opt": ["极度害怕身体碰撞，别人一碰就躲", "正常跑跳，不主动推挤别人", "喜欢玩抓人、摔跤等有轻微对抗的游戏", "极度享受身体冲撞，像个小坦克一样横冲直撞"],
        
        "submit": "🚀 启动 AI 定制引擎",
        "error_miss": "⚠️ 测评失败：您有漏选的题目！请将所有选项填写完整。",
        "success": "✅ 计算完毕！专属深度诊断报告如下：",
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
        "subtitle": "Seattle Big Tech Data Modeling ✖️ NCAA Recruiting Logic.",
        "sidebar_title": "⚙️ Preferences",
        "lang_switch": "🌐 Language / 语言",
        "faq_title": "👉 Must Read: What is the NCAA? Why are Tech Parents Obsessed?",
        "faq_content": """
        **Sports are the ultimate shortcut to elite US universities.**
        
        🏆 **Division I (D1) - Full Scholarships**
        * Full Athletic Scholarships saving $200k+. For extreme talents.
        
        🥈 **Division II (D2) - The Balanced Zone**
        * Partial scholarships. Great ROI but lacks Ivy League schools.
        
        🎓 **Division III (D3) - The Ivy League Hack (Crucial!)**
        * Home to Harvard, Yale, MIT, etc. D3 does NOT offer athletic money.
        * **The Hack**: Coaches hold **"Admissions Support"**. If a coach wants your child, they can pull them directly into the school, bypassing applicants with perfect GPAs but no sports!
        """,
        "step1": "📝 Step 1: Physical Hardware",
        "step1_cap": "Enter real family data to predict adult traits.",
        "gender": "Child's Gender",
        "age": "Current Age",
        "height": "Current Height (cm)",
        "shoe": "Child's shoe/foot size:",
        "shoe_opt": ["Noticeably smaller", "Average size", "Noticeably larger (Flippers)"],
        "mom_h": "Mother's Height (cm)",
        "mom_s": "Mother's Wingspan (cm) - Optional",
        "dad_h": "Father's Height (cm)",
        "dad_s": "Father's Wingspan (cm) - Optional",
        "unknown_span": "❓ I don't know the exact arm spans",
        
        "step2": "⏳ Step 2: Resources & Goals",
        "step2_cap": "Youth sports rely on family logistics.",
        "acad": "Academic Expectation",
        "acad_opt": ["Keep up", "Above average", "1-2 yrs ahead", "Elite (e.g., AMC)"],
        "hours": "Weekly hours for sports? (incl. commute)",
        "budget": "Annual Sports Budget",
        "budget_opt": ["Basic (<$2k/yr)", "Mid ($5k/yr)", "Elite (>$15k/yr, travel)"],
        
        "step3": "🧠 Step 3: Behavioral Scenarios",
        "step3_cap": "Select the true scenario.",
        "psy_focus": "1. [Focus] When doing boring tasks:",
        "psy_focus_opt": ["Easily distracted", "Persists briefly", "Immersed for 30+ mins", "Extreme focus"],
        "psy_grit": "2. [Grit] When losing a game:",
        "psy_grit_opt": ["Cries and quits", "Sulks for a long time", "Asks for a rematch", "Analyzes why they lost"],
        "psy_logic": "3. [Tactics] When facing rules:",
        "psy_logic_opt": ["Obedient", "Has own ideas", "Constantly asks 'why'", "Looks for loopholes"],
        "psy_flex": "4. [Flexibility] Physical flexibility:",
        "psy_flex_opt": ["Stiff", "Average", "Very flexible", "Extremely bendy"],
        "psy_perfection": "5. [Perfectionism] When drawing:",
        "psy_perfection_opt": ["Doesn't care", "Normal", "Upset over small flaws", "Extreme perfectionist"],
        "psy_social": "6. [Social] During group activities:",
        "psy_social_opt": ["Introverted", "Slow to warm up", "Needs companions", "Ultimate extrovert"],
        "psy_aggro": "7. [Aggression] Physical contact:",
        "psy_aggro_opt": ["Afraid of contact", "Normal", "Enjoys light wrestling", "Loves collisions"],
        
        "submit": "🚀 Launch AI Matching Engine",
        "error_miss": "⚠️ Error: Missing inputs!",
        "success": "✅ Data processed! Your report:",
        "res1_title": "🧬 Diagnosis 1: Physical Projections",
        "target_h": "Projected Target Height",
        "ape_index": "Projected Ape Index (Wingspan)",
        "foot_trait": "Terminal Biomechanics (Feet)",
        "res2_title": "🎯 Diagnosis 2: Top Recommended Sports",
        "res3_title": "⚠️ Diagnosis 3: Burnout & Time Warning",
        "burnout_high": "🚨 RED ALERT: High risk of injury and burnout! Weekly hours should not exceed age.",
        "burnout_low": "🟡 Note: Relaxed pace. Healthy, but lacks competitive edge for recruiting.",
        "burnout_ok": "✅ Excellent energy balance! Perfect harmony of physical and academic load.",
        "cta_title": "📥 Get Your Exclusive Schedule & Stop Stressing",
        "cta_desc": "**👇 Add the Founder on WeChat for a Custom Plan 👇**\n### 💬 WeChat ID: `BigMeiXiao`\n*Mention [AI Report] for a free schedule audit.*"
    }
}

# ==========================================
# 3. 超大型 NCAA 全系运动数据库 (22项)
# 向量维度: [身高红利, 臂展红利, 水感/脚码, 柔韧控制, 爆发力, 抗挫折力, 耐无聊度, 策略烧脑, 团队协作, 烧钱指数]
# ==========================================
SPORTS_DB = {
    # --- 水上运动 (Aquatics) ---
    "游泳 / Swimming (NCAA D1/D2/D3)": np.array([0.7, 0.9, 1.0, 0.4, 0.6, 0.5, 1.0, 0.2, 0.1, 0.4]),
    "跳水 / Diving (NCAA D1/D2/D3)": np.array([0.2, 0.3, 0.9, 1.0, 0.9, 0.8, 0.8, 0.4, 0.1, 0.5]),
    "水球 / Water Polo (NCAA D1/D2/D3)": np.array([0.8, 0.9, 0.8, 0.5, 0.8, 0.7, 0.4, 0.8, 0.9, 0.5]),
    "赛艇 / Rowing-Crew (NCAA D1/D2/D3)": np.array([0.9, 0.9, 0.1, 0.3, 0.7, 0.8, 0.9, 0.2, 1.0, 0.7]),
    
    # --- 技巧与精准 (Skill & Precision) ---
    "体操 / Gymnastics (NCAA D1/D2/D3)": np.array([0.1, 0.2, 0.1, 1.0, 0.9, 0.9, 0.9, 0.3, 0.2, 0.6]),
    "击剑 / Fencing (NCAA D1/D2/D3)": np.array([0.6, 0.9, 0.1, 0.6, 0.8, 0.7, 0.6, 1.0, 0.2, 0.8]),
    "高尔夫 / Golf (NCAA D1/D2/D3)": np.array([0.4, 0.5, 0.1, 0.6, 0.3, 1.0, 0.9, 0.9, 0.2, 1.0]),
    "步枪 / Rifle (NCAA Mixed)": np.array([0.3, 0.3, 0.1, 0.4, 0.1, 1.0, 1.0, 0.5, 0.1, 0.6]),
    "保龄球 / Bowling (NCAA Women)": np.array([0.4, 0.4, 0.1, 0.4, 0.2, 0.8, 0.9, 0.5, 0.3, 0.4]),
    "马术 / Equestrian (NCAA Emerging)": np.array([0.5, 0.5, 0.1, 0.6, 0.4, 0.7, 0.6, 0.5, 0.2, 1.0]),
    
    # --- 场地与球类 (Court & Field) ---
    "网球 / Tennis (NCAA D1/D2/D3)": np.array([0.7, 0.8, 0.1, 0.5, 0.8, 0.9, 0.7, 0.8, 0.1, 0.9]),
    "篮球 / Basketball (NCAA D1/D2/D3)": np.array([1.0, 1.0, 0.1, 0.4, 0.9, 0.6, 0.4, 0.8, 0.9, 0.4]),
    "排球 / Volleyball (NCAA D1/D2/D3)": np.array([1.0, 0.9, 0.1, 0.4, 0.9, 0.6, 0.4, 0.7, 1.0, 0.4]),
    "足球 / Soccer (NCAA D1/D2/D3)": np.array([0.5, 0.4, 0.1, 0.5, 0.8, 0.7, 0.5, 0.8, 1.0, 0.4]),
    "长曲棍球 / Lacrosse (NCAA D1/D2/D3)": np.array([0.6, 0.7, 0.1, 0.4, 0.8, 0.7, 0.4, 0.8, 0.9, 0.7]),
    "曲棍球 / Field Hockey (NCAA D1/D2/D3)": np.array([0.5, 0.5, 0.1, 0.6, 0.8, 0.7, 0.5, 0.8, 0.9, 0.6]),
    "棒球_垒球 / Baseball & Softball (NCAA D1/D2/D3)": np.array([0.6, 0.7, 0.1, 0.6, 0.7, 0.7, 0.7, 0.9, 0.8, 0.6]),
    "冰球 / Ice Hockey (NCAA D1/D2/D3)": np.array([0.6, 0.6, 0.1, 0.5, 1.0, 0.8, 0.6, 0.8, 0.9, 0.9]),
    
    # --- 速度与力量 (Speed & Power) ---
    "田径-短跑跳跃 / Track & Field - Sprints (NCAA D1/D2/D3)": np.array([0.8, 0.6, 0.1, 0.6, 1.0, 0.7, 0.7, 0.2, 0.1, 0.2]),
    "越野长跑 / Cross Country (NCAA D1/D2/D3)": np.array([0.4, 0.4, 0.1, 0.3, 0.3, 0.9, 1.0, 0.4, 0.6, 0.2]),
    "摔跤 / Wrestling (NCAA D1/D2/D3)": np.array([0.2, 0.4, 0.1, 0.8, 0.9, 0.9, 0.5, 0.6, 0.1, 0.2]),
    "滑雪 / Skiing (NCAA Mixed)": np.array([0.5, 0.5, 0.1, 0.8, 0.8, 0.9, 0.8, 0.6, 0.2, 0.9])
}

# ==========================================
# 4. 动态个性化计划生成引擎 (AI Engine)
# ==========================================
def generate_personalized_plan(sport, age, hours, budget_idx, acad_idx, lang):
    phase_cn = "探索采样期 (Sampling Phase)" if age <= 10 else "专项突破期 (Specialization Phase)"
    phase_en = "Sampling Phase" if age <= 10 else "Specialization Phase"
    
    s_hrs = int(hours * 0.6)
    c_hrs = int(hours * 0.2)
    r_hrs = hours - s_hrs - c_hrs
    if r_hrs < 1: r_hrs = 1
    
    if lang == "中文":
        md = f"#### 📅 针对 {age} 岁孩子的【{sport}】深度定制计划\n"
        md += f"**📍 当前阶段定位**：{phase_cn}。这个年龄段切忌过度追求单一项目的成绩，核心是打磨神经肌肉记忆和保持兴趣，为青春期后的爆发蓄力。\n\n"
        md += f"**⏱️ 精力分配矩阵 ({hours}小时/周)**：\n"
        md += f"- 🏅 **专项技术 ({s_hrs}h)**：主攻 {sport} 的核心技术动作。\n"
        md += f"- 🏋️ **跨项体能 ({c_hrs}h)**：千万别只练单项！必须用这部分时间练核心力量（如基础体操、跑跳），防止单侧肌肉过度劳损。\n"
        md += f"- 🧘 **强制恢复 ({r_hrs}h)**：留白时间，用于肌肉拉伸、按摩与睡眠，消化身体压力。\n\n"
        
        md += f"**💰 资金与路径策略**："
        if budget_idx == 2:
            md += "系统检测到预算极其充足。建议跳过大锅饭式的训练，直接寻找有 NCAA D1 背景的退役教练进行 1v1 私教，并提前注册全国协会账号准备跨州积分赛。\n\n"
        else:
            md += "性价比最高的路线：加入本地高水平 Club 的第一梯队，利用大班高强度的对抗氛围提升竞技状态，将大额资金留到 12 岁以后的关键招募期使用。\n\n"
            
        if acad_idx >= 2:
            md += f"**📚 学霸双轨护城河**：您对学业要求极高（竞赛级/超前）。**防坑警告**：千万不要在周一到周四晚上安排极度消耗体力的无氧训练！把耗体力的训练堆在周末，平时晚上必须留给数学与阅读拓展。**在 NCAA 招募中，高 GPA 是教练帮你去招生办要人的最后底牌。**"
    else:
        md = f"#### 📅 {age}-Year-Old {sport} Custom Blueprint\n"
        md += f"**📍 Phase**：{phase_en}. Focus on neuromuscular memory and passion, not just winning medals right now.\n"
        md += f"**⏱️ Time Allocation ({hours}h/wk)**: {s_hrs}h on-sport tech, {c_hrs}h cross-training (core/gymnastics to prevent overuse injuries), {r_hrs}h mandatory recovery/stretching.\n"
        if budget_idx == 2: md += "**💰 Strategy**: Budget allows for 1v1 ex-NCAA coaches. Start collecting national points.\n"
        else: md += "**💰 Strategy**: Join a highly competitive local club A-team. Save heavy spending for post-12 years old recruiting windows.\n"
        if acad_idx >= 2: md += "**📚 Academic Buffer**: Do NOT schedule heavy physical workouts on weeknights. Save weeknights for math/GPA prep. A high GPA is the ultimate leverage in NCAA recruiting."
    return md

def generate_athletic_enhancement(flex, aggro, focus, grit, lang):
    md = "#### 🔧 弱项补偿与底层能力提升指南\n" if lang == "中文" else "#### 🔧 Core Athletic Enhancement Plan\n"
    if lang == "中文":
        if flex <= 5: md += "- 🤸 **柔韧性赤字补偿**：系统检测到孩子身体略显僵硬。每天睡前必须增加 15 分钟静态拉伸（如坐姿体前屈）。柔韧性不足会极大增加未来韧带撕裂的风险。\n"
        if aggro <= 5: md += "- 🛡️ **对抗脱敏训练**：孩子目前比较抗拒肢体冲突。建议在家进行轻度的“抢枕头、拔河”等游戏，帮助大脑对物理接触产生安全脱敏。\n"
        if focus <= 5: md += "- ⏱️ **注意力切片法**：孩子难以长时间忍受枯燥。不要强制练一小时，采用“15分钟极度专注+3分钟游戏奖励”的番茄工作法，逐步拉长耐受区间。\n"
        if grit <= 5: md += "- 🧠 **逆商 (Grit) 刻意练习**：输了容易崩溃或放弃。在日常生活中刻意创造“稍微踮起脚尖才能赢”的微小挫折场景。当孩子在逆境中反败为胜时，狠狠表扬其**过程中的坚持**，而不是结果。\n"
    else:
        if flex <= 5: md += "- 🤸 **Flexibility Deficit**: Add 15m daily static stretching to prevent future ligament tears.\n"
        if aggro <= 5: md += "- 🛡️ **Contact Confidence**: Play light wrestling/tug-of-war games at home to desensitize the brain to physical contact.\n"
        if focus <= 5: md += "- ⏱️ **Focus Slicing**: Break trainings into 15-min intensive intervals with gamified rewards.\n"
        if grit <= 5: md += "- 🧠 **Grit Training**: Create micro-challenges where they must struggle to win. Praise the *effort*, not just the result, to build resilience.\n"
    return md

# ==========================================
# 5. 前端 UI 渲染
# ==========================================
st.sidebar.markdown(f"### {UI[st.session_state.lang]['sidebar_title']}")
selected_lang = st.sidebar.radio(UI[st.session_state.lang]['lang_switch'], ["中文", "English"])
if selected_lang != st.session_state.lang:
    st.session_state.lang = selected_lang
    st.rerun()
t = UI[st.session_state.lang]

st.title(t["title"])
st.markdown(t["subtitle"])
with st.expander(t["faq_title"], expanded=False): st.markdown(t["faq_content"])
st.divider()

with st.form("main_form"):
    st.header(t["step1"])
    st.caption(t["step1_cap"])
    
    col1, col2 = st.columns(2)
    with col1: child_gender = st.selectbox(t["gender"], options=["女/Female", "男/Male"], index=None)
    with col2: child_age = st.number_input(t["age"], min_value=3, max_value=16, value=None)
        
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
    acad_level = st.selectbox(t["acad"], options=t["acad_opt"], index=None)
    weekly_hrs = st.selectbox(t["hours"], options=[2, 4, 6, 8, 10, 12, 15, 20, 25, 30], index=None)
    budget_level = st.selectbox(t["budget"], options=t["budget_opt"], index=None)

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
# 6. 后端纯 Index 算法计算 (免疫多语言 Bug)
# ==========================================
if submit_btn:
    req = [child_gender, child_age, child_height, shoe_size_trait, mom_h, dad_h, 
           acad_level, weekly_hrs, budget_level, psy_focus_ans, psy_grit_ans, 
           psy_logic_ans, psy_flex_ans, psy_perfection_ans, psy_social_ans, psy_aggro_ans]
    if not span_unknown: req.extend([mom_span, dad_span])
    
    if any(v is None for v in req):
        st.error(t["error_miss"])
    else:
        st.success(t["success"])
        
        # 严格用数组的 Index 抓取分数，完美解决切语言 Bug
        shoe_idx = t["shoe_opt"].index(shoe_size_trait)
        acad_idx = t["acad_opt"].index(acad_level)
        budget_idx = t["budget_opt"].index(budget_level)
        
        psy_focus = SCORE_MAP[t["psy_focus_opt"].index(psy_focus_ans)]
        psy_grit = SCORE_MAP[t["psy_grit_opt"].index(psy_grit_ans)]
        psy_logic = SCORE_MAP[t["psy_logic_opt"].index(psy_logic_ans)]
        psy_flex = SCORE_MAP[t["psy_flex_opt"].index(psy_flex_ans)]
        psy_perfection = SCORE_MAP[t["psy_perfection_opt"].index(psy_perfection_ans)]
        psy_social = SCORE_MAP[t["psy_social_opt"].index(psy_social_ans)]
        psy_aggro = SCORE_MAP[t["psy_aggro_opt"].index(psy_aggro_ans)]

        # 硬件推算
        is_male = "男" in child_gender or "Male" in child_gender
        target_height = (mom_h + dad_h + 13)/2 if is_male else (mom_h + dad_h - 13)/2
        active_mom_s = mom_h if span_unknown else mom_span
        active_dad_s = dad_h if span_unknown else dad_span
        genetic_ape_index = ((active_mom_s - mom_h) + (active_dad_s - dad_h)) / 2
        
        st.header("1️⃣ " + t["res1_title"])
        st.info(f"**📏 {t['target_h']}：{target_height:.1f} cm**")
        st.info(f"**🦅 {t['ape_index']}：{genetic_ape_index:+.1f} cm**")
        st.info(f"**👣 {t['foot_trait']}：{shoe_size_trait}**")

        # 算法匹配
        budget_score = 0.3 if budget_idx == 0 else (0.6 if budget_idx == 1 else 1.0)
        shoe_score = 0.2 if shoe_idx == 0 else (1.0 if shoe_idx == 2 else 0.6)
        
        user_vec = np.array([
            target_height / 195.0, (target_height + genetic_ape_index) / 195.0, shoe_score, 
            psy_flex/10.0, psy_aggro/10.0, psy_grit/10.0, psy_focus/10.0, psy_logic/10.0, psy_social/10.0, budget_score           
        ])

        scores = {s: round((np.dot(user_vec, v) / (np.linalg.norm(user_vec) * np.linalg.norm(v))) * 100, 1) for s, v in SPORTS_DB.items()}
        sorted_sports = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_sport = sorted_sports[0][0]
        
        st.divider()
        st.header("2️⃣ " + t["res2_title"])
        for i in range(3):
            st.markdown(f"### 🏆 Top {i+1}: {sorted_sports[i][0]}")
            st.markdown(f"**系统契合度：{sorted_sports[i][1]}%**")
        
        # 个性化引擎
        st.success("✅ **AI 已为您生成深度执行蓝图：**" if st.session_state.lang == "中文" else "✅ **AI Deep Execution Blueprint:**")
        st.markdown(generate_personalized_plan(top_sport, child_age, weekly_hrs, budget_idx, acad_idx, st.session_state.lang))
        st.markdown(generate_athletic_enhancement(psy_flex, psy_aggro, psy_focus, psy_grit, st.session_state.lang))

        st.divider()
        st.header("3️⃣ " + t["res3_title"])
        if weekly_hrs > child_age + 3: st.error(t["burnout_high"])
        elif weekly_hrs < child_age - 2: st.warning(t["burnout_low"])
        else: st.success(t["burnout_ok"])

        st.divider()
        st.header(t["cta_title"])
        st.success(t["cta_desc"])

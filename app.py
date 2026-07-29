import streamlit as st
import numpy as np

# ==========================================
# 1. 全局配置与状态管理
# ==========================================
st.set_page_config(page_title="Sport & College Planner | 智能体教规划", layout="centered", page_icon="🏅")

# 解决多语言状态丢失的 Bug
if 'lang' not in st.session_state:
    st.session_state.lang = "中文"

SCORE_MAP = [2, 5, 8, 10]

# ==========================================
# 2. 多语言字典库 (新增运动状态与升学目标)
# ==========================================
UI = {
    "中文": {
        "title": "测一测：你的孩子最适合什么运动？",
        "subtitle": "西雅图大厂工程师数据建模 ✖️ NCAA 升学底层逻辑。算出身心契合度最高的“体教双轨”路线。",
        "sidebar_title": "偏好设置",
        "faq_title": "👉 家长必看：什么是 NCAA？为什么科技圈都在卷体育爬藤？",
        "faq_content": """
        **体育是通往美国顶尖大学的超级捷径**。NCAA 将大学体育分为三个级别，玩法完全不同：
        🏆 **Division I (D1) - 全额奖学金**：竞技水平极高，适合极具天赋且能全职投入的家庭。
        🥈 **Division II (D2) - 高性价比**：提供部分奖学金，但常春藤等顶尖学术名校不在这个级别。
        🎓 **Division III (D3) - 常春藤名校的聚集地（核心重点！）**：包含哈佛、耶鲁、MIT等。**D3 不发体育奖学金！** 但教练有**“招生办支持权 (Admissions Support)”**。只要孩子特长被看中，且 GPA 达标，教练就能直接去招生办把你“特招”进去，挤掉那些满分 GPA 但毫无特色的普通学霸！
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
        
        "step1_5": "🎯 第二步：当前状态与升学目标",
        "step1_5_cap": "告诉系统孩子目前的进度和您的终极目标，以生成最精准的路径。",
        "curr_status": "孩子目前的运动状态是？",
        "curr_status_opt": ["毫无基础 / 还在摸索阶段", "上兴趣班 / 刚起步 (每周1-2次)", "已入队 / 规律训练 (有固定教练)", "高水平竞技 / 常拿名次 (准备冲击积分赛)"],
        "curr_sport": "目前主攻或正在学的运动是？(若无填“无”，多项用空格隔开)",
        "target_col": "家庭对孩子未来的大学目标类型？",
        "target_col_opt": ["顺其自然 / 身体健康最重要", "综合类好大学 (Top 50 即可)", "冲刺顶级常春藤/MIT (极高学术与脑力要求)", "体育强校 (D1 全奖为核心目标)"],

        "step2": "⏳ 第三步：家庭资源与学业优先级",
        "step2_cap": "体育是一场马拉松，拼的是家庭的后勤。",
        "acad": "当前学业期望水平（决定了时间分配权重）",
        "acad_opt": ["跟上学校进度即可", "学区中上游", "超前学习1-2年", "冲击高阶竞赛 (如 AMC/Kangaroo)"],
        "hours": "每周家庭能抽出多少小时用于体育？(含接送)",
        "budget": "家庭每年的体育花销预算",
        "budget_opt": ["基础班 (<$2k/年)", "中产进阶 ($5k/年，含少量私教)", "重金投入 (>$15k/年，跨州比赛)"],
        
        "step3": "🧠 第四步：场景化性格测试",
        "step3_cap": "请直接根据孩子在生活中的真实反应“对号入座”。",
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
        "error_miss": "⚠️ 测评失败：您有漏选的必填项目！",
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
        "sidebar_title": "Preferences",
        "faq_title": "👉 Must Read: What is the NCAA? Why are Tech Parents Obsessed?",
        "faq_content": """
        **Sports are the ultimate shortcut to elite US universities.**
        🏆 **Division I (D1)**: Full Athletic Scholarships saving $200k+. For extreme talents.
        🥈 **Division II (D2)**: Partial scholarships. Great ROI but lacks Ivy League schools.
        🎓 **Division III (D3)**: Home to Harvard, Yale, MIT, etc. **D3 does NOT offer athletic money.** But Coaches hold **"Admissions Support"**. They can pull your child directly into the school, bypassing applicants with perfect GPAs but no sports!
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
        
        "step1_5": "🎯 Step 2: Current Status & College Goals",
        "step1_5_cap": "Tell us where you are now and where you want to go.",
        "curr_status": "Child's current sports status?",
        "curr_status_opt": ["No foundation / Still exploring", "Recreational classes (1-2x/week)", "Club Team / Consistent Training", "High Competitive / Regional+ Level"],
        "curr_sport": "Current sports played? (Type 'None' if N/A)",
        "target_col": "Target College Type?",
        "target_col_opt": ["Let it be / Health is priority", "Top 50 Universities", "Ivy League / MIT (High Academics)", "Sports Powerhouses (D1 Full Ride)"],

        "step2": "⏳ Step 3: Resources & Priorities",
        "step2_cap": "Youth sports rely on family logistics.",
        "acad": "Academic Expectation",
        "acad_opt": ["Keep up", "Above average", "1-2 yrs ahead", "Elite (e.g., AMC)"],
        "hours": "Weekly hours for sports? (incl. commute)",
        "budget": "Annual Sports Budget",
        "budget_opt": ["Basic (<$2k/yr)", "Mid ($5k/yr)", "Elite (>$15k/yr, travel)"],
        
        "step3": "🧠 Step 4: Behavioral Scenarios",
        "step3_cap": "Select the true scenario for your child.",
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
        "error_miss": "⚠️ Error: Missing inputs! Please fill all fields.",
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
# 3. 22项 NCAA 全系运动数据库
# ==========================================
SPORTS_DB = {
    # --- 水上运动 (Aquatics) ---
    "游泳 / Swimming (NCAA D1/D2/D3)": np.array([0.7, 0.9, 1.0, 0.4, 0.6, 0.5, 1.0, 0.2, 0.1, 0.4]),
    "跳水 / Diving (NCAA D1/D2/D3)": np.array([0.2, 0.3, 0.9, 1.0, 0.9, 0.8, 0.8, 0.4, 0.1, 0.5]),
    "水球 / Water Polo (NCAA D1/D2/D3)": np.array([0.8, 0.9, 0.8, 0.5, 0.8, 0.7, 0.4, 0.8, 0.9, 0.5]),
    "赛艇 / Rowing-Crew (Ivy/D1/D3)": np.array([0.9, 0.9, 0.1, 0.3, 0.7, 0.8, 0.9, 0.2, 1.0, 0.7]),
    
    # --- 技巧与精准 (Skill & Precision) ---
    "体操 / Gymnastics (NCAA D1/D2/D3)": np.array([0.1, 0.2, 0.1, 1.0, 0.9, 0.9, 0.9, 0.3, 0.2, 0.6]),
    "击剑 / Fencing (Ivy/D1/D3)": np.array([0.6, 0.9, 0.1, 0.6, 0.8, 0.7, 0.6, 1.0, 0.2, 0.8]),
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
    "棒垒球 / Baseball & Softball (NCAA D1/D2/D3)": np.array([0.6, 0.7, 0.1, 0.6, 0.7, 0.7, 0.7, 0.9, 0.8, 0.6]),
    "冰球 / Ice Hockey (NCAA D1/D2/D3)": np.array([0.6, 0.6, 0.1, 0.5, 1.0, 0.8, 0.6, 0.8, 0.9, 0.9]),
    
    # --- 速度与力量 (Speed & Power) ---
    "田径-短跑跳跃 / Track & Field (NCAA D1/D2/D3)": np.array([0.8, 0.6, 0.1, 0.6, 1.0, 0.7, 0.7, 0.2, 0.1, 0.2]),
    "越野长跑 / Cross Country (NCAA D1/D2/D3)": np.array([0.4, 0.4, 0.1, 0.3, 0.3, 0.9, 1.0, 0.4, 0.6, 0.2]),
    "摔跤 / Wrestling (NCAA D1/D2/D3)": np.array([0.2, 0.4, 0.1, 0.8, 0.9, 0.9, 0.5, 0.6, 0.1, 0.2]),
    "滑雪 / Skiing (NCAA Mixed)": np.array([0.5, 0.5, 0.1, 0.8, 0.8, 0.9, 0.8, 0.6, 0.2, 0.9])
}

# 标记“藤校/高录取率”的运动（用于升学目标反向加权）
IVY_SPORTS = ["击剑 / Fencing", "赛艇 / Rowing-Crew", "高尔夫 / Golf", "网球 / Tennis", "马术 / Equestrian", "长曲棍球 / Lacrosse"]

# ==========================================
# 4. 超级动态个性化计划生成引擎 (AI Engine)
# ==========================================
def generate_personalized_plan(sport, age, hours, status_idx, curr_sport_str, col_idx, acad_idx, lang):
    s_hrs = int(hours * 0.6)
    c_hrs = int(hours * 0.2)
    r_hrs = hours - s_hrs - c_hrs
    if r_hrs < 1: r_hrs = 1
    
    if lang == "中文":
        md = f"#### 📅 针对 {age} 岁孩子的深度定制路线图\n"
        
        # 结合现状给出衔接建议
        if status_idx == 0:
            md += f"**📍 破局建议 (当前零基础)**：系统推荐了【{sport}】。万事开头难，现阶段绝对不要一上来就高强度压迫，先报一个基础兴趣班，让孩子在玩耍中建立对这项运动的好感。\n\n"
        elif status_idx == 1:
            md += f"**📍 进阶建议 (当前兴趣班)**：孩子已经在练【{curr_sport_str}】。如果觉得遇到瓶颈，可以考虑将【{sport}】作为主项或强力副项，因为算法测算出它更契合孩子的基因与性格。建议本学期尝试参加一次选拔赛 (Tryout)。\n\n"
        elif status_idx >= 2:
            md += f"**📍 竞技建议 (已入队/高水平)**：孩子在【{curr_sport_str}】已经有了很好的训练基础。如果继续冲刺【{sport}】，必须引入极其精细的负荷管理，重点预防关节和韧带的损耗。\n\n"

        md += f"**⏱️ 科学精力分配矩阵 ({hours}小时/周)**：\n"
        md += f"- 🏅 **专项技术 ({s_hrs}h)**：主攻项目核心技术。\n"
        md += f"- 🏋️ **跨项体能 ({c_hrs}h)**：用这部分时间练反向肌肉或核心力量（如体操、跑跳），极大降低长期受伤率。\n"
        md += f"- 🧘 **强制恢复 ({r_hrs}h)**：拉伸、泡沫轴与深睡眠。\n\n"
        
        # 结合升学目标的残酷真相
        if col_idx == 2: # 常春藤
            md += "**🎓 【常春藤/MIT 冲刺策略】**：您选择了极高难度的学术名校。**注意：藤校 D3 教练只招收不会拉低全队平均 GPA 的孩子。** 把耗体能的训练堆在周末，周一到周四晚上必须留给数学与深度阅读。在招募中，高 GPA 是教练敢去招生办要你的底气！\n\n"
        elif col_idx == 3: # D1 强校
            md += "**🏆 【NCAA D1 全奖策略】**：目标 D1 意味着极其残酷的淘汰赛。12岁前注重基础，12岁后必须疯狂参加跨州级别以上的巡回赛积累积分，制作 Highlight Video 并尽早发给大学教练刷脸。\n\n"
        else:
            md += "**🌱 【综合平衡策略】**：目标综合好大学。保持运动能给文书极大的加分素材（体现领导力和挫折恢复力），不需要过度烧钱砸排名，保证身心健康与优异的在校成绩即可。\n\n"
    else:
        md = f"#### 📅 {age}-Year-Old Custom Blueprint\n"
        if status_idx == 0: md += f"**📍 Starter Advice**: System recommends 【{sport}】. Since you are starting fresh, begin with recreational classes. Focus strictly on fun to build passion first.\n\n"
        elif status_idx == 1: md += f"**📍 Transition Advice**: You are currently doing 【{curr_sport_str}】. Consider adding or shifting to 【{sport}】 as data shows higher genetic/psychological fit. Try out for a club team this season.\n\n"
        else: md += f"**📍 Elite Advice**: You have a strong foundation in 【{curr_sport_str}】. To peak in 【{sport}】, you must introduce strict load management to prevent burnout.\n\n"

        md += f"**⏱️ Time Allocation ({hours}h/wk)**: {s_hrs}h on-sport tech, {c_hrs}h cross-training (prevent overuse injuries), {r_hrs}h mandatory recovery.\n\n"
        
        if col_idx == 2: md += "**🎓 【Ivy League Strategy】**: Ivy D3 coaches only recruit athletes who won't tank the team's average GPA. Save weeknights for rigorous academics. A high GPA is your ultimate leverage!\n\n"
        elif col_idx == 3: md += "**🏆 【D1 Strategy】**: Focus on fundamentals until 12, then aggressively collect national points and build Highlight Videos to email coaches early.\n\n"
        else: md += "**🌱 【Balanced Strategy】**: Sports will act as a powerful essay builder (leadership/grit). No need to overspend on elite travel teams; balance health and grades.\n\n"
    return md

def generate_athletic_enhancement(flex, aggro, focus, grit, lang):
    md = "#### 🔧 弱项补偿与底层能力提升指南\n" if lang == "中文" else "#### 🔧 Core Athletic Enhancement Plan\n"
    if lang == "中文":
        if flex <= 5: md += "- 🤸 **柔韧性赤字补偿**：检测到孩子身体略显僵硬。每天睡前必须增加 15 分钟静态拉伸。柔韧性不足会极大增加未来韧带撕裂风险。\n"
        if aggro <= 5: md += "- 🛡️ **对抗脱敏训练**：孩子目前比较抗拒肢体冲突。建议在家进行轻度的“抢枕头、拔河”等游戏，帮助大脑对物理接触安全脱敏。\n"
        if focus <= 5: md += "- ⏱️ **注意力切片法**：孩子难以长时间忍受枯燥。采用“15分钟极度专注+3分钟游戏奖励”的番茄工作法，逐步拉长耐受区间。\n"
        if grit <= 5: md += "- 🧠 **逆商 (Grit) 刻意练习**：输了容易崩溃或放弃。刻意创造“稍微踮起脚尖才能赢”的微小挫折场景。狠狠表扬其过程中的坚持，而非结果。\n"
    else:
        if flex <= 5: md += "- 🤸 **Flexibility Deficit**: Add 15m daily static stretching to prevent future ligament tears.\n"
        if aggro <= 5: md += "- 🛡️ **Contact Confidence**: Play light wrestling/tug-of-war games at home to desensitize the brain to physical contact.\n"
        if focus <= 5: md += "- ⏱️ **Focus Slicing**: Break trainings into 15-min intensive intervals with gamified rewards.\n"
        if grit <= 5: md += "- 🧠 **Grit Training**: Create micro-challenges where they must struggle to win. Praise the *effort*, not just the result.\n"
    return md

# ==========================================
# 5. 侧边栏与绝对安全的语言切换机制
# ==========================================
st.sidebar.markdown(f"### ⚙️ {UI[st.session_state.lang]['sidebar_title']}")

selected_lang = st.sidebar.radio(
    "🌐 语言切换 / Language Switch", 
    ["中文", "English"],
    index=0 if st.session_state.lang == "中文" else 1,
    key="static_lang_radio_key"
)

if selected_lang != st.session_state.lang:
    st.session_state.lang = selected_lang
    st.rerun()

t = UI[st.session_state.lang]

# ==========================================
# 6. 前端 UI 与表单收集
# ==========================================
st.title(t["title"])
st.markdown(t["subtitle"])
with st.expander(t["faq_title"], expanded=False): st.markdown(t["faq_content"])
st.divider()

with st.form("main_form"):
    # 第一步：身体硬件
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

    # 第二步：新增的当前状态与升学目标
    st.header(t["step1_5"])
    st.caption(t["step1_5_cap"])
    curr_status_ans = st.selectbox(t["curr_status"], options=t["curr_status_opt"], index=None)
    curr_sport_ans = st.text_input(t["curr_sport"], placeholder="例如: 游泳, 体操 / None")
    target_col_ans = st.selectbox(t["target_col"], options=t["target_col_opt"], index=None)

    # 第三步：家庭资源
    st.header(t["step2"])
    st.caption(t["step2_cap"])
    acad_level = st.selectbox(t["acad"], options=t["acad_opt"], index=None)
    weekly_hrs = st.selectbox(t["hours"], options=[2, 4, 6, 8, 10, 12, 15, 20, 25, 30], index=None)
    budget_level = st.selectbox(t["budget"], options=t["budget_opt"], index=None)

    # 第四步：性格测试
    st.header(t["step3"])
    st.caption(t["step3_cap"])
    psy_focus_ans = st.selectbox(t["psy_focus"], options=t["psy_focus_opt"], index=None)
    psy_grit_ans = st.selectbox(t["psy_grit"], options=t["psy_grit_opt"], index=None)
    psy_logic_ans = st.selectbox(t["psy_logic"], options=t["psy_logic_opt"], index=None)
    psy_flex_ans = st.selectbox(t["psy_flex"], options=t["psy_flex_opt"], index=None)
    psy_perfection_ans = st.selectbox(t["psy_perfection"], options=t["psy_perfection_opt"], index=None)
    psy_social_ans = st.selectbox(t["psy_social"], options=t["psy_social_opt"], index=None)
    psy_aggro_ans = st.selectbox(t["psy_aggro"], options=t["psy_aggro_opt"], index=None)

    submit_btn = st.form_submit_button(t["submit"], use_container_width=True, key="static_submit_btn")

# ==========================================
# 7. 后端算法解析与渲染 (完美兼容双语切换)
# ==========================================
if submit_btn:
    # 动态必填校验 (文本框 curr_sport 允许空)
    req = [child_gender, child_age, child_height, shoe_size_trait, mom_h, dad_h, 
           curr_status_ans, target_col_ans, acad_level, weekly_hrs, budget_level, 
           psy_focus_ans, psy_grit_ans, psy_logic_ans, psy_flex_ans, psy_perfection_ans, psy_social_ans, psy_aggro_ans]
    if not span_unknown: req.extend([mom_span, dad_span])
    
    if any(v is None or str(v).strip() == "" for v in req):
        st.error(t["error_miss"])
    else:
        st.success(t["success"])
        
        # 索引抓取，绝对不死机
        shoe_idx = t["shoe_opt"].index(shoe_size_trait)
        acad_idx = t["acad_opt"].index(acad_level)
        budget_idx = t["budget_opt"].index(budget_level)
        status_idx = t["curr_status_opt"].index(curr_status_ans)
        col_idx = t["target_col_opt"].index(target_col_ans)
        
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

        # 数据归一化与相似度计算
        budget_score = 0.3 if budget_idx == 0 else (0.6 if budget_idx == 1 else 1.0)
        shoe_score = 0.2 if shoe_idx == 0 else (1.0 if shoe_idx == 2 else 0.6)
        
        user_vec = np.array([
            target_height / 195.0, (target_height + genetic_ape_index) / 195.0, shoe_score, 
            psy_flex/10.0, psy_aggro/10.0, psy_grit/10.0, psy_focus/10.0, psy_logic/10.0, psy_social/10.0, budget_score           
        ])

        scores = {}
        for sport, data in SPORTS_DB.items():
            similarity = (np.dot(user_vec, data) / (np.linalg.norm(user_vec) * np.linalg.norm(data))) * 100
            
            # 升学目标反向加权逻辑 (Ivy League Hack)
            if col_idx == 2 and any(ivy_sport in sport for ivy_sport in IVY_SPORTS):
                similarity *= 1.15 # 常春藤目标，强推击剑赛艇高尔夫等
            
            scores[sport] = round(similarity, 1)
            
        sorted_sports = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_sport = sorted_sports[0][0]
        
        st.divider()
        st.header("2️⃣ " + t["res2_title"])
        for i in range(3):
            st.markdown(f"### 🏆 Top {i+1}: {sorted_sports[i][0]}")
            st.markdown(f"**系统契合度：{sorted_sports[i][1]}%**")
        
        # 个性化引擎
        st.divider()
        st.success("✅ **AI 已为您生成深度执行蓝图：**" if st.session_state.lang == "中文" else "✅ **AI Deep Execution Blueprint:**")
        st.markdown(generate_personalized_plan(top_sport, child_age, weekly_hrs, status_idx, curr_sport_ans, col_idx, acad_idx, st.session_state.lang))
        st.markdown(generate_athletic_enhancement(psy_flex, psy_aggro, psy_focus, psy_grit, st.session_state.lang))

        st.divider()
        st.header("3️⃣ " + t["res3_title"])
        if weekly_hrs > child_age + 3: st.error(t["burnout_high"])
        elif weekly_hrs < child_age - 2: st.warning(t["burnout_low"])
        else: st.success(t["burnout_ok"])

        st.divider()
        st.header(t["cta_title"])
        st.success(t["cta_desc"])

import streamlit as st
import numpy as np

# ==========================================
# 1. 页面配置与移动端适配优化
# ==========================================
# 使用 centered 布局，在手机端显示更加集中、不会左右乱晃
st.set_page_config(page_title="你的孩子适合什么运动？", layout="centered", page_icon="🏅")

# ==========================================
# 2. 超大型 NCAA 运动特征与教育价值数据库
# ==========================================
# 向量维度: [身高红利, 臂展红利, 水感/脚码, 柔韧控制, 爆发力, 抗挫折力, 耐无聊度, 策略烧脑, 团队协作, 烧钱指数]
SPORTS_DB = {
    "游泳 (Swimming)": {
        "vector": np.array([0.7, 0.9, 1.0, 0.4, 0.6, 0.5, 1.0, 0.2, 0.1, 0.4]),
        "edu": "🏊‍♂️ **[心肺发动机 & 绝对专注]**：游泳是极佳的有氧底座。最重要的是，孩子在水下几个小时听不到外界干扰，能极大地锻炼在“极其枯燥环境”下的深度专注力。对于平时容易分心的孩子，这是最好的“入定”修行。"
    },
    "跳水 (Diving)": {
        "vector": np.array([0.2, 0.3, 0.9, 1.0, 0.9, 0.8, 0.8, 0.4, 0.1, 0.5]),
        "edu": "🦘 **[空中三维建模 & 胆识训练]**：跳水极度偏爱脚部尺码小的孩子（入水面积小，压水花有优势）。它要求孩子在零点几秒的失重状态下完成大脑对身体的高速控制，是对前庭觉、空间感知和胆量的顶级历练。"
    },
    "体操 (Gymnastics)": {
        "vector": np.array([0.1, 0.2, 0.1, 1.0, 0.9, 0.9, 0.9, 0.3, 0.2, 0.6]),
        "edu": "🤸‍♀️ **[所有运动的万物之母]**：练体操绝对不是为了去奥运会，而是建立无与伦比的“本体感受器”。有了体操的神经肌肉底子，孩子以后哪怕转练田径、跳水、花滑，都是降维打击。"
    },
    "击剑 (Fencing)": {
        "vector": np.array([0.6, 0.9, 0.1, 0.6, 0.8, 0.7, 0.6, 1.0, 0.2, 0.8]),
        "edu": "🤺 **[戴着面罩的动态西洋棋]**：击剑是高强度的“脑力博弈”。在零点几秒内预判对手意图、设下陷阱并反击，极度锻炼逻辑推理和瞬间决策能力。这也是常春藤名校招生官最爱的“学霸运动”。"
    },
    "高尔夫 (Golf)": {
        "vector": np.array([0.4, 0.5, 0.1, 0.6, 0.3, 1.0, 0.9, 0.9, 0.2, 1.0]),
        "edu": "⛳ **[极度的挫折管理与情绪控制]**：高尔夫是自己与自己的斗争。一个失误可能毁掉整局，它要求孩子在巨大的心理波动下，瞬间清空负面情绪、专注当下这一杆。练的是顶级的情绪管理（EQ）。"
    },
    "网球 (Tennis)": {
        "vector": np.array([0.7, 0.8, 0.1, 0.5, 0.8, 0.9, 0.7, 0.8, 0.1, 0.9]),
        "edu": "🎾 **[独立决策的孤胆英雄]**：网球赛场禁止教练场外指导。孩子必须像孤独的将军，自己在场上调整战术、消化落后的挫败感。这是培养独立领导力和临场应变能力的终极运动。"
    },
    "赛艇 (Rowing/Crew)": {
        "vector": np.array([0.9, 0.9, 0.1, 0.3, 0.7, 0.8, 0.9, 0.2, 1.0, 0.7]),
        "edu": "🚣‍♀️ **[极致的忍耐力与齿轮般的协作]**：常春藤最古老的传统项目。它不突出个人英雄主义，要求8个人像一台机器一样精准同步。极度考验忍耐力、服从性和团队牺牲精神。"
    },
    "水球 (Water Polo)": {
        "vector": np.array([0.8, 0.9, 0.8, 0.5, 0.8, 0.7, 0.4, 0.8, 0.9, 0.5]),
        "edu": "🤽‍♂️ **[水下绞肉机与全能战士]**：结合了游泳的耐力、篮球的视野和极强的水下身体对抗。要求在缺氧状态下依然保持团队战术执行力，是展现强悍生命力和大局观的绝佳载体。"
    },
    "排球 (Volleyball)": {
        "vector": np.array([1.0, 0.9, 0.1, 0.4, 0.9, 0.6, 0.4, 0.7, 1.0, 0.4]),
        "edu": "🏐 **[情绪传导与团队凝结剂]**：排球是一项球不能落地的运动，极其依赖队友间的补位和情绪鼓励。它是教导孩子如何在劣势时互相兜底、建立深厚同理心的最佳团队运动。"
    },
    "长曲棍球 (Lacrosse)": {
        "vector": np.array([0.6, 0.7, 0.1, 0.4, 0.8, 0.7, 0.4, 0.8, 0.9, 0.7]),
        "edu": "🥍 **[东海岸老钱家族的社交名片]**：在美国东北部和私立高中极度盛行。节奏极快、对抗激烈，能极好地锻炼孩子在高速移动中的手眼协调和空间战术素养。"
    },
    "篮球 (Basketball)": {
        "vector": np.array([1.0, 1.0, 0.1, 0.4, 0.9, 0.6, 0.4, 0.8, 0.9, 0.4]),
        "edu": "🏀 **[高压决策与空间撕裂]**：不仅仅是长得高就行。现代篮球极度考验孩子在场上瞬息万变的局势中，捕捉防守漏洞的“球商”。锻炼的是高速运动下的动态决策力。"
    },
    "足球 (Soccer)": {
        "vector": np.array([0.5, 0.4, 0.1, 0.5, 0.8, 0.7, 0.5, 0.8, 1.0, 0.4]),
        "edu": "⚽ **[开阔视野与长线耐力]**：场地最大、人数最多的运动。需要孩子具备极佳的有氧耐力，以及像雷达一样随时扫描全场、预判球路的大局观（Spatial Awareness）。"
    },
    "田径-短跨跳 (Track & Field - Sprints/Jumps)": {
        "vector": np.array([0.8, 0.6, 0.1, 0.6, 1.0, 0.7, 0.7, 0.2, 0.1, 0.2]),
        "edu": "🏃 **[纯粹爆发力与突破极限]**：最纯粹的竞技。没有复杂的战术，只有你和秒表。教会孩子如何通过科学的肌肉训练，极其诚实地面对自己身体的极限。"
    },
    "越野跑 (Cross Country)": {
        "vector": np.array([0.4, 0.4, 0.1, 0.3, 0.3, 0.9, 1.0, 0.4, 0.6, 0.2]),
        "edu": "🏃‍♀️ **[坚忍不拔的苦行僧]**：这项运动极其痛苦且枯燥。能坚持练越野跑的孩子，拥有任何藤校都无法拒绝的特质——逆天级别的毅力（Grit）和延迟满足能力。"
    },
    "摔跤 (Wrestling)": {
        "vector": np.array([0.2, 0.4, 0.1, 0.8, 0.9, 0.9, 0.5, 0.6, 0.1, 0.2]),
        "edu": "🤼 **[绝对的身体掌控与原始抗压]**：按体重分级，矮个子同样能称霸。这是最直接的零和博弈，极大锻炼孩子直面物理冲突的勇气和绝境中的求生欲。"
    },
    "马术 (Equestrian)": {
        "vector": np.array([0.5, 0.5, 0.1, 0.6, 0.4, 0.7, 0.6, 0.5, 0.2, 1.0]),
        "edu": "🐎 **[跨物种的情绪感知与同理心]**：NCAA 女子项目（很多藤校有校队）。你不仅要控制自己，还要感知一匹重达半吨的动物的情绪。这是对孩子“共情力”和“温柔而坚定的控制力”的终极考验。"
    },
    "步枪射击 (Rifle)": {
        "vector": np.array([0.3, 0.3, 0.1, 0.4, 0.1, 1.0, 1.0, 0.5, 0.1, 0.6]),
        "edu": "🎯 **[心如止水的禅宗境界]**：NCAA 男女混合项目。完全不需要跑跳爆发，要求的是极其可怕的微肌肉控制、呼吸调节和绝对的心理防线。适合极度沉静、专注力极高的孩子。"
    },
    "花样滑冰 (Figure Skating - 非NCAA但热门)": {
        "vector": np.array([0.3, 0.4, 0.1, 0.9, 0.8, 0.9, 0.9, 0.5, 0.1, 0.9]),
        "edu": "⛸️ **[冰上的抗压芭蕾]**：结合了极高的艺术表现力和极致的核心力量。孩子需要无数次在冰上摔倒再爬起来微笑着完成表演，对心智的磨练极其残酷且有效。"
    }
}

# ==========================================
# 3. 前端 UI 渲染与科普区
# ==========================================
st.title("测一测：你的孩子最适合什么运动？")
st.markdown("别再盲目跟风报班了！用硅谷工程师的**数据建模**，结合您家庭的真实基因与孩子的性格，帮您算出成功率最高的“体教结合”路线。")

# 移动端友好的折叠科普框
with st.expander("👉 家长必看：NCAA 升学和普通人有什么关系？", expanded=False):
    st.markdown("""
    很多家长以为：“我又不想让娃去奥运会，练这么苦有什么用？”
    
    其实在美国，**体育是通往顶尖大学的超级捷径**。NCAA（美国大学体育协会）是最大的推手：
    * **D1 级别**：全美顶尖。大学教练不仅想要你，还会给你发“全额体育奖学金”，四年省下几十万美金。
    * **D3 级别 (常春藤为主)**：这个最关键！D3 不发奖学金，但教练有**“招生办支持权 (Admissions Support)”**。只要你家孩子有一项特长被教练看中，加上成绩过线，教练就能直接去招生办把你“特招”进哈佛、MIT，直接挤掉那些只有死读书的满分学霸！
    
    **体育练的不是肌肉，练的是顶尖名校最看重的：逆商、专注力、领导力。**
    """)

st.divider()

# ==========================================
# 4. 表单收集区 (强制无默认值)
# ==========================================
st.header("📝 第一步：身体硬件评估")
st.caption("填入真实的家庭数据，AI 将预估孩子的成年身高及发育特征。")

# 辅助生成下拉选项（为了没有 default，添加一个 None）
score_options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
score_format = lambda x: f"{x} 分" if x is not None else "请滑动/选择评分..."

with st.form("main_form"):
    
    # --- 基础信息区 (使用单列或至多两列适应手机屏幕) ---
    col1, col2 = st.columns(2)
    with col1:
        child_gender = st.selectbox("孩子性别", options=["女", "男"], index=None, placeholder="请选择...")
    with col2:
        child_age = st.number_input("当前年龄 (岁)", min_value=3, max_value=16, value=None, placeholder="例如: 8")
        
    child_height = st.number_input("当前身高 (cm)", min_value=80, max_value=200, value=None, placeholder="例如: 130")
    shoe_size_trait = st.selectbox("与同龄人相比，孩子的鞋码/脚部特征：", 
                                   options=["明显偏小 (买鞋总买小一号)", "正常大众尺码", "明显偏大 (天生大脚)"], 
                                   index=None, placeholder="请评估脚部大小...")

    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    st.markdown("**父母基因数据 (用于公式倒推)**")
    
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        mom_h = st.number_input("母亲身高 (cm)", min_value=140, max_value=190, value=None, placeholder="例: 160")
        mom_span = st.number_input("母亲两臂展开长度 (cm)", min_value=140, max_value=190, value=None, placeholder="例: 160")
    with p_col2:
        dad_h = st.number_input("父亲身高 (cm)", min_value=150, max_value=210, value=None, placeholder="例: 175")
        dad_span = st.number_input("父亲两臂展开长度 (cm)", min_value=150, max_value=210, value=None, placeholder="例: 175")

    # --- 资源投入区 ---
    st.header("⏳ 第二步：家庭资源与学业目标")
    st.caption("体育是一场马拉松，拼的是家庭的后勤。")
    
    academic_level = st.selectbox("当前学业期望水平（决定了时间分配权重）", 
                                  options=["跟上学校进度即可", "学区中上游", "超前学习1-2年", "冲击高阶竞赛 (如 AMC/Kangaroo)"],
                                  index=None, placeholder="请选择学业目标...")
    
    weekly_budget_hours = st.selectbox("每周家庭能抽出多少小时用于体育？(含路上接送)",
                                       options=[2, 4, 6, 8, 10, 12, 15, 20, 25],
                                       index=None, placeholder="请选择每周小时数...")
    
    budget_level = st.selectbox("家庭每年的体育花销预算",
                                options=["基础班 (<$2,000/年)", "中产进阶 ($5,000/年，含少量私教)", "重金投入 (>$15,000/年，跨州打比赛)"],
                                index=None, placeholder="请选择预算范围...")

    # --- 心理与性格测试区 ---
    st.header("🧠 第三步：性格与行为测试 (1-10分)")
    st.caption("请根据孩子日常的真实表现评分，1分代表极其不符合，10分代表极其符合。")
    
    psy_focus = st.selectbox("1. 【耐无聊指数】能耐着性子做完极其枯燥重复的任务吗？", options=score_options, index=None, placeholder="请评分 (1-10)...")
    psy_grit = st.selectbox("2. 【受挫恢复力】游戏输了，是崩溃大哭，还是马上要求再来一局？", options=score_options, index=None, placeholder="请评分 (1-10)...")
    psy_logic = st.selectbox("3. 【策略脑力】喜欢按部就班，还是喜欢找规则漏洞、猜大人心思？", options=score_options, index=None, placeholder="请评分 (1-10)...")
    psy_flex = st.selectbox("4. 【身体柔韧度】平时在家里容易轻松做出下腰、一字马吗？", options=score_options, index=None, placeholder="请评分 (1-10)...")
    psy_perfection = st.selectbox("5. 【细节强迫症】做手工时，对一点点瑕疵也会非常在意想重做吗？", options=score_options, index=None, placeholder="请评分 (1-10)...")
    psy_social = st.selectbox("6. 【社交依赖度】喜欢一个人在角落玩，还是必须拉着一群人疯跑？", options=score_options, index=None, placeholder="请评分 (1-10)...")
    psy_aggro = st.selectbox("7. 【肢体对抗欲】在操场上，特别喜欢玩抓人、推挤碰撞的游戏吗？", options=score_options, index=None, placeholder="请评分 (1-10)...")

    # 提交按钮
    submit_btn = st.form_submit_button("🚀 启动 AI 匹配与诊断引擎", use_container_width=True)

# ==========================================
# 5. 核心逻辑处理与输出
# ==========================================
if submit_btn:
    # --- 表单必填项校验 ---
    inputs = [child_gender, child_age, child_height, shoe_size_trait, mom_h, mom_span, dad_h, dad_span, 
              academic_level, weekly_budget_hours, budget_level, 
              psy_focus, psy_grit, psy_logic, psy_flex, psy_perfection, psy_social, psy_aggro]
    
    if any(v is None for v in inputs):
        st.error("⚠️ 测评失败：您有漏填的选项！请将所有输入框和下拉菜单填写完整，以保证算法的准确性。")
    else:
        st.success("✅ 数据提取完毕！以下是为您生成的专属诊断报告：")
        
        # --- 算法 1：靶身高与遗传力学计算 ---
        if child_gender == "男":
            target_height = (mom_h + dad_h + 13) / 2
        else:
            target_height = (mom_h + dad_h - 13) / 2
            
        mom_index = mom_span - mom_h
        dad_index = dad_span - dad_h
        genetic_ape_index = (mom_index + dad_index) / 2
        
        st.header("🧬 诊断一：身体硬件与发育预估")
        st.markdown("通过您提供的父母数据，系统倒推了孩子的成年身体形态，这是选项的基石：")
        
        # 渲染移动端友好的指标卡片 (不用 columns，防止挤压)
        st.info(f"**📏 预估成年身高 (Target Height)：{target_height:.1f} cm**  \n*（注：基于父母基因公式推算，后天睡眠营养可干预 ±5cm）*")
        
        ape_desc = "臂展偏短 (极其适合举重、体操等需要核心发力集中的项目)" if genetic_ape_index < 0 else "臂展修长 (天生拥有游泳、篮球、击剑等项目的防守和划水红利)"
        st.info(f"**🦅 预估臂展特征 (Ape Index)：{genetic_ape_index:+.1f} cm**  \n*（结论：{ape_desc}）*")
        
        foot_desc = "脚部面积小，虽然水下推进力吃亏，但在跳水压水花、体操空中姿态控制上拥有顶级优势！" if "小" in shoe_size_trait else ("天生自带大脚蹼，水感好！" if "大" in shoe_size_trait else "各项发展均衡。")
        st.info(f"**👣 终端力学预判 (Foot Trait)：{shoe_size_trait}**  \n*（结论：{foot_desc}）*")

        # --- 算法 2：高维特征匹配引擎 ---
        # 归一化资金与时间权重
        budget_score = 0.3 if "基础" in budget_level else (0.6 if "中产" in budget_level else 1.0)
        
        user_vec = np.array([
            target_height / 195.0,  # 身高红利
            (target_height + genetic_ape_index) / 195.0, # 臂展红利
            0.2 if "小" in shoe_size_trait else (1.0 if "大" in shoe_size_trait else 0.6), # 水感脚码
            psy_flex / 10.0,       # 柔韧控制
            psy_aggro / 10.0,      # 爆发对抗
            psy_grit / 10.0,       # 抗挫折
            psy_focus / 10.0,      # 耐无聊
            psy_logic / 10.0,      # 策略脑力
            psy_social / 10.0,     # 社交依赖
            budget_score           # 烧钱指数承受力
        ])

        # 余弦相似度计算匹配池
        scores = {}
        for sport, data in SPORTS_DB.items():
            sport_vec = data["vector"]
            # 引入硬核惩罚机制：如果个子预估不到 165(女)/175(男)，且运动高度依赖身高(如篮球/排球)
            penalty = 1.0
            if sport_vec[0] >= 0.9: # 极度需要身高的运动
                if (child_gender == "女" and target_height < 168) or (child_gender == "男" and target_height < 183):
                    penalty = 0.7 # 惩罚 30% 分数
            
            # 如果预算极低，过滤掉马术高尔夫
            if budget_score < 0.4 and sport_vec[9] >= 0.9:
                penalty = 0.5

            similarity = np.dot(user_vec, sport_vec) / (np.linalg.norm(user_vec) * np.linalg.norm(sport_vec))
            scores[sport] = {"score": round(similarity * penalty * 100, 1), "edu": data["edu"]}

        sorted_sports = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
        
        st.divider()
        st.header("🎯 诊断二：AI 智能匹配最高的三项运动")
        st.markdown("系统已经为您过滤掉了天生劣势或容易让孩子产生抵触情绪的项目。以下是匹配度最高的选择，以及它们对大脑和性格发育的真实作用：")
        
        for i in range(3):
            sport_name = sorted_sports[i][0]
            sport_score = sorted_sports[i][1]["score"]
            sport_edu = sorted_sports[i][1]["edu"]
            
            # 手机端渲染友好的层级
            st.markdown(f"### 🏆 Top {i+1}: {sport_name}")
            st.markdown(f"**系统契合度：{sport_score}%**")
            st.write(sport_edu)
            st.markdown("---")

        st.divider()
        st.header("⚠️ 诊断三：时间破产与防坑预警")
        
        # 复杂的 Burnout 计算
        if weekly_budget_hours > child_age + 3:
            st.error(f"🚨 **红色警报：孩子极易受伤和厌学！** \n您家孩子今年 {child_age} 岁，但您预计每周投入高达 {weekly_budget_hours} 小时的训练。根据人体运动科学理论，儿童每周单项运动时间**不应超过自身年龄**，否则极易导致不可逆的骨骺板损伤，并让孩子彻底痛恨这项运动。")
        elif weekly_budget_hours < child_age - 2:
            st.warning(f"🟡 **提示：训练强度偏佛系。** \n每周 {weekly_budget_hours} 小时的运动量有助于身心健康，但如果目标是初中后走 NCAA 升学路线，这个强度在 10 岁以后可能无法积累足够的竞技壁垒。")
        else:
            st.success(f"✅ **极佳的精力状态！** \n每周 {weekly_budget_hours} 小时非常科学，完美兼顾了身体恢复、睡眠和课业。")
            
        if "竞赛" in academic_level or "超前" in academic_level:
            st.markdown(f"**💡 学业防坑建议**：系统检测到您的学术目标很高（{academic_level}）。切记，即使是走体育特长，美国顶尖名校依然对 GPA 有着极其严苛的滑窗要求。**每天无论练多晚，雷打不动的阅读与数学逻辑思考时间绝对不能被挤压！**")

        st.divider()
        st.header("📥 获取独家排期表，不做瞎焦虑的家长")
        st.markdown("""
        AI 算法只能给方向，真实的挑战在于**执行落地**。
        * 孩子每天练到晚上 8 点，回家还有一堆作业，怎么排表才能保证睡眠？
        * 练体操练出来的柔韧性，几年级转去练跳水最合适？
        * 本地到底哪些俱乐部是在坑钱，哪些是真的有通道？
        """)
        
        # 极其醒目的私域转化入口
        st.success("**👇 添加主理人微信，获取属于你的定制方案👇**")
        st.markdown("### 💬 微信号：`BigMeiXiao`")
        st.caption("备注【AI测评截图】，免费获取针对西雅图/Bellevue学区的《体教统筹时间排期表》及 15 分钟日程诊断。")

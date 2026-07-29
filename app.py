import streamlit as st
import pandas as pd
import numpy as np

# --- 页面全局配置 ---
st.set_page_config(page_title="NCAA Student-Athlete 全维规划引擎", layout="wide", page_icon="🧬")

# --- 后端数据库：运动多维特征矩阵与教育科普库 ---
# 维度：[身高依赖, 臂展依赖, 脚/掌水感依赖, 核心柔韧, 爆发力, 挫折抗压, 枯燥耐受, 策略烧脑, 烧钱指数]
SPORTS_DB = {
    "游泳 (Swimming)": {
        "vector": np.array([0.7, 0.9, 1.0, 0.4, 0.6, 0.5, 1.0, 0.2, 0.5]),
        "edu": "🏊‍♂️ **心肺与专注力培养皿**：游泳是极佳的有氧底座。它能最大化扩充心肺容量，且在水下隔绝外界声音的数小时中，极度锻炼孩子在极其枯燥环境下的深度专注力和内观能力（适合容易被外界干扰的孩子）。"
    },
    "跳水 (Diving)": {
        "vector": np.array([0.2, 0.3, 0.9, 1.0, 0.9, 0.8, 0.8, 0.4, 0.6]), # 水感这里指压水花/脚背控制
        "edu": "🦘 **失重状态下的空间建模**：很多人不知道，跳水极其看重较小的脚部尺码（极小化入水面积）。它在极其短暂的滞空时间内，强迫大脑进行超高速的三维空间动态计算，是对前庭觉和胆识的顶级历练。"
    },
    "体操 (Gymnastics)": {
        "vector": np.array([0.1, 0.2, 0.1, 1.0, 0.9, 0.9, 0.9, 0.3, 0.7]),
        "edu": "🤸‍♀️ **所有运动的‘万物之母’**：6-9岁练体操不是为了拿奥运冠军，而是为了建立无与伦比的本体感受（Proprioception）和神经肌肉募集能力。体操打底的孩子，未来转练任何项目（撑杆跳、跳水、花滑）都极具降维打击能力。"
    },
    "击剑 (Fencing)": {
        "vector": np.array([0.6, 0.9, 0.1, 0.6, 0.8, 0.7, 0.6, 1.0, 0.8]),
        "edu": "🤺 **带着面罩的动态国际象棋**：击剑不仅吃臂展，更是高强度的脑力博弈。它要求在零点几秒内预判对手的意图并做出防守反击，极度锻炼孩子的逻辑推理能力和快速决策力，深受常春藤招生官喜爱。"
    },
    "高尔夫 (Golf)": {
        "vector": np.array([0.4, 0.5, 0.1, 0.6, 0.3, 1.0, 0.9, 0.9, 1.0]),
        "edu": "⛳ **极致的挫折管理与情绪控制**：高尔夫是自己与自己的斗争。一个失误可能毁掉整局，它极其锻炼孩子在巨大心理波动下，瞬间清空负面情绪、专注当下这一杆的‘正念（Mindfulness）’能力。"
    },
    "网球 (Tennis)": {
        "vector": np.array([0.7, 0.8, 0.1, 0.5, 0.8, 0.9, 0.7, 0.8, 0.9]),
        "edu": "🎾 **独立决策与孤岛抗压**：网球赛场上禁止教练场外指导。孩子必须像一个孤独的将军，自己在场上调整战术、消化落后的挫败感。这是培养独立领导力和临场应变能力的顶级运动。"
    },
    "水球 (Water Polo)": {
        "vector": np.array([0.8, 0.9, 1.0, 0.5, 0.8, 0.7, 0.5, 0.8, 0.6]),
        "edu": "🤽‍♀️ **水下绞肉机与团队协作**：完美结合了游泳的耐力、篮球的视野和极强的水下身体对抗。要求在缺氧状态下依然保持团队战术执行力，展现极强的 Leadership。"
    }
}

st.title("🧬 NCAA 智库：青少年体育潜力与教育价值解码器")
st.markdown("基于生物遗传学、神经行为学及 NCAA D1/D3 录取大数据的全维匹配系统。帮助家庭用数据消除焦虑，用规划代替盲从。")
st.divider()

# --- 侧边栏：家庭资源与学业 ---
st.sidebar.header("📊 边界条件 (Boundary Inputs)")
academic_level = st.sidebar.select_slider("孩子当前数学/学术思维层级", options=["校内平均", "学区前20%", "超前学习1-2年", "竞赛级 (Math Kangaroo/AMC等)"], value="超前学习1-2年")
weekly_budget_hours = st.sidebar.number_input("每周家庭可投入最大时间 (含通勤与训练)", min_value=2, max_value=30, value=12)
commute_tolerance = st.sidebar.radio("单程通勤忍耐度", ["20分钟内", "跨桥/跨区 (45分钟左右)", "为了好教练可以开1小时以上"])

# --- 主表单模块 ---
with st.form("comprehensive_intake"):
    # 模块 1：基因与生物学特征
    st.header("🧬 模块一：基因靶向与体格发育测算")
    c1, c2, c3, c4 = st.columns(4)
    child_gender = c1.selectbox("性别", ["女", "男"])
    child_age = c2.number_input("当前年龄", 4, 15, 6)
    child_height = c3.number_input("当前身高 (cm)", 90, 190, 118)
    shoe_size_trait = c4.selectbox("鞋码/脚部特征", ["明显偏小", "正常", "明显偏大 (大脚掌)"])

    c5, c6, c7, c8 = st.columns(4)
    mom_h = c5.number_input("母亲身高 (cm)", 140, 190, 166)
    mom_span = c6.number_input("母亲臂展 (cm)", 140, 190, 162)
    dad_h = c7.number_input("父亲身高 (cm)", 150, 200, 178)
    dad_span = c8.number_input("父亲臂展 (cm)", 150, 200, 182)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 模块 2：神经认知与行为学测评
    st.header("🧠 模块二：神经心理学与行为倾向测评")
    st.caption("以下问题请家长客观评估孩子日常生活中的真实反应，这将极大影响项目的留存率。")
    
    col_psy1, col_psy2 = st.columns(2)
    with col_psy1:
        psy_focus = st.slider("1. 延迟满足与枯燥耐受度", 1, 10, 8, help="1分=需要高频刺激和新鲜感，10分=能耐受极其无聊的重复动作数月之久")
        psy_grit = st.slider("2. 逆商与挫折恢复力 (Grit)", 1, 10, 7, help="1分=一输就崩溃放弃，10分=迅速擦干眼泪复盘再战")
        psy_logic = st.slider("3. 动态博弈与逻辑推理欲", 1, 10, 6, help="1分=喜欢按部就班执行，10分=热衷于在规则中找漏洞、猜心理、下棋博弈")
    
    with col_psy2:
        psy_perfection = st.slider("4. 完美主义 vs 粗放掌控", 1, 10, 7, help="1分=差不多就行/大开大合，10分=死磕细节/对一个动作的极度强迫症")
        psy_social = st.slider("5. 孤岛作战 vs 团队依赖", 1, 10, 3, help="1分=完全享受一个人练习的孤独，10分=极度依赖队友的情绪价值和社交氛围")
        psy_aggro = st.slider("6. 物理对抗与侵略性", 1, 10, 4, help="1分=回避任何身体碰撞，10分=享受冲撞、零和博弈和抢夺")

    submit_btn = st.form_submit_button("⚙️ 初始化运算引擎", use_container_width=True)

# --- 数据处理与结果输出 ---
if submit_btn:
    st.success("✅ 数据模型计算完毕，以下为独家深度诊断报告。")
    
    # 1. 基因计算逻辑 (Genetics Math)
    # 靶身高计算 (Tanner-Whitehouse 简化版)
    if child_gender == "男":
        target_height = (mom_h + dad_h + 13) / 2
    else:
        target_height = (mom_h + dad_h - 13) / 2
        
    # 父母遗传臂展比例评估
    mom_index = mom_span - mom_h
    dad_index = dad_span - dad_h
    genetic_ape_index = (mom_index + dad_index) / 2
    
    st.header("🔬 一、 生物力学预测与基因面板")
    res_c1, res_c2, res_c3 = st.columns(3)
    res_c1.metric("预测成年靶身高 (Target Height)", f"{target_height:.1f} cm", delta="基于父母遗传常数")
    
    ape_status = "中等偏短 (-)" if genetic_ape_index < 0 else "修长 (+)"
    res_c2.metric("预测臂展基因指数 (Ape Index)", f"{genetic_ape_index:+.1f} cm", delta=ape_status, delta_color="off")
    
    foot_status = "水感推进力较弱 / 极佳的翻滚与空中压水花优势" if shoe_size_trait == "明显偏小" else "正常特征"
    res_c3.metric("足部力学特征定性", shoe_size_trait, delta=foot_status, delta_color="off")

    # 2. 向量化匹配算法 (Vector Matching)
    # 将用户行为数据转化为 9维 数组
    user_vec = np.array([
        target_height / 190.0,  # 简化归一化
        (target_height + genetic_ape_index) / 190.0,
        0.2 if shoe_size_trait == "明显偏小" else 0.8,
        psy_perfection / 10.0, # 柔韧/细节控制
        psy_aggro / 10.0,      # 爆发/对抗
        psy_grit / 10.0,       # 挫折抗压
        psy_focus / 10.0,      # 枯燥耐受
        psy_logic / 10.0,      # 策略博弈
        0.8 if weekly_budget_hours > 15 else 0.4 # 粗略算作烧钱/时间指数
    ])

    scores = {}
    for sport, data in SPORTS_DB.items():
        sport_vec = data["vector"]
        # 余弦相似度计算匹配百分比
        similarity = np.dot(user_vec, sport_vec) / (np.linalg.norm(user_vec) * np.linalg.norm(sport_vec))
        scores[sport] = {"score": round(similarity * 100, 1), "edu": data["edu"]}

    sorted_sports = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
    
    st.divider()
    st.header("🎯 二、 体育项目匹配度与教育价值解码")
    st.markdown("很多家长只看到了运动的表面技术，却忽略了不同项目对大脑神经回路的重塑作用。以下是系统为您匹配的最优解及底层教育逻辑：")
    
    for i in range(3):
        sport_name = sorted_sports[i][0]
        sport_score = sorted_sports[i][1]["score"]
        sport_edu = sorted_sports[i][1]["edu"]
        
        st.subheader(f"🥇 优先级 {i+1}: {sport_name} (综合匹配度: {sport_score}%)")
        st.info(sport_edu)

    st.divider()
    st.header("⏰ 三、 精力耗散与学术双轨预警 (Burnout Audit)")
    
    col_b1, col_b2 = st.columns([2, 1])
    with col_b1:
        if weekly_budget_hours > child_age + 2:
            st.error(f"🚨 **系统判定：时间破产风险极高！** 孩子当前 {child_age} 岁，但家庭设定的周负荷高达 {weekly_budget_hours} 小时。这个强度的训练极易引发早期的关节过度使用损伤（Overuse Injuries），并且会严重挤压孩子发呆、消化情绪和深层次思考（如逻辑数学拓展）的时间。")
        else:
            st.success(f"✅ **系统判定：精力生态极佳。** 当前设定的 {weekly_budget_hours} 小时训练量非常克制，完美符合 LTAD（长期运动员发展模型）的阶段建议，为学术竞赛（如 Math Kangaroo）留下了充足的脑力冗余。")
            
        st.markdown(f"**🧠 学术并行策略**：系统检测到孩子处于【{academic_level}】。对于 6-10 岁的儿童，NCAA 并不看重早期的运动成绩，反而更看重底层逻辑和学习习惯。千万不要为了每天多游 1000 米，牺牲了每日雷打不动的阅读与数学探索时间。")

    with col_b2:
        st.markdown("### 📥 独家交付物")
        st.markdown("""
        这仅仅是算法的初步侧写。真正的难点在于**执行**。
        
        您的日程中如果混杂了体操、跳水、游泳等高强度项目，如何排表才能保证不受伤？如何兼顾钢琴与数学？
        """)
        st.button("📲 添加主理人获取《定制版多项目冲突统筹表》")
        st.caption("西雅图/Bellevue 地区家长可附赠本地俱乐部红黑榜。")

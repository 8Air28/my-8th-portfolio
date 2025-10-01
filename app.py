import streamlit as st

# 履歴をセッションで保持
if "history" not in st.session_state:
    st.session_state.history = []

st.title("⚔ ダメージ計算ツール")

# 攻撃ステータス入力
st.subheader("攻撃側ステータス")
col1, col2, col3 = st.columns(3)
with col1:
    attack = st.number_input("攻撃力", 1, 999, 50)
    atk_bonus = st.number_input("技補正", 1, 5, 1)
with col2:
    atk_attr = st.selectbox("属性", ["火", "水", "木", "雷", "光", "闇"])
    atk_level = st.number_input("レベル", 1, 100, 50)
with col3:
    atk_times = st.number_input("回数", 1, 10, 1)
    crit_rate = st.slider("急所率(%)", 0, 100, 10)

# 防御ステータス入力
st.subheader("防御側ステータス")
col4, col5, col6 = st.columns(3)
with col4:
    defense = st.number_input("防御力", 0, 999, 30)
    def_bonus = st.number_input("防御補正", 1, 5, 1)
with col5:
    def_attr = st.selectbox("属性", ["火", "水", "木", "雷", "光", "闇"])
    def_level = st.number_input("レベル", 1, 100, 50)
with col6:
    evade = st.slider("回避率(%)", 0, 100, 5)

# 属性相性表
type_chart = {
    "火": {"木": 2, "水": 0.5, "雷": 1, "火": 1, "光": 1, "闇": 1},
    "木": {"雷": 2, "火": 0.5, "水": 1, "木": 1, "光": 1, "闇": 1},
    "雷": {"水": 2, "木": 0.5, "火": 1, "雷": 1, "光": 1, "闇": 1},
    "水": {"火": 2, "雷": 0.5, "木": 1, "水": 1, "光": 1, "闇": 1},
    "光": {"闇": 2, "光": 1, "火": 1, "水": 1, "木": 1, "雷": 1},
    "闇": {"光": 2, "闇": 1, "火": 1, "水": 1, "木": 1, "雷": 1},
}

# 計算ボタン
if st.button("計算する"):
    import random
    # 命中判定
    if random.random() < evade / 100:
        result = "攻撃を回避された！"
    else:
        # ダメージ計算
        crit = 1.5 if random.random() < crit_rate / 100 else 1
        type_mult = type_chart[atk_attr][def_attr]
        damage = max(1, int(((attack * atk_bonus * atk_level) / (defense * def_bonus * def_level + 1)) 
                            * atk_times * crit * type_mult))
        result = f"与えたダメージ: {damage} (急所:{'あり' if crit > 1 else 'なし'})"

    # 履歴保存
    st.session_state.history.insert(0, result)

# 履歴カード風UI
st.subheader("📜 ダメージ履歴")
st.markdown(
    """
    <style>
    .card {
        padding: 10px;
        margin: 8px 0;
        border-radius: 8px;
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

for i, h in enumerate(st.session_state.history[:10]):
    st.markdown(f"<div class='card'>#{i+1} {h}</div>", unsafe_allow_html=True)



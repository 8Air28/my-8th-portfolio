import streamlit as st

# ページ設定
st.set_page_config(
    page_title="⚔ ダメージ計算ツール",
    page_icon="⚔️",
    layout="centered"
)

st.title("⚔ ダメージ計算ツール")

st.markdown("""
このツールは攻撃側と防御側のステータスを入力すると、  
属性相性・急所補正を含めたダメージを計算します。
""")

# 属性補正設定
属性補正 = {
    ("火", "木"): 1.5,
    ("木", "雷"): 1.5,
    ("雷", "水"): 1.5,
    ("水", "火"): 1.5,
    ("光", "闇"): 1.5,
    ("闇", "光"): 1.5,
}

属性一覧 = ["火", "木", "雷", "水", "光", "闇"]

# 攻撃側ステータス入力
st.header("攻撃側ステータス")
攻撃力 = st.number_input("攻撃力", min_value=1, step=1, value=50)
技補正 = st.number_input("技補正 (倍率)", min_value=0.1, step=0.1, value=1.0)
攻撃属性 = st.selectbox("攻撃属性", 属性一覧)
攻撃レベル = st.number_input("攻撃レベル", min_value=1, step=1, value=50)
回数 = st.number_input("攻撃回数", min_value=1, step=1, value=1)
急所率 = st.slider("急所率 (%)", min_value=0, max_value=100, value=0)
命中 = st.slider("命中率 (%)", min_value=0, max_value=100, value=100)

# 防御側ステータス入力
st.header("防御側ステータス")
防御力 = st.number_input("防御力", min_value=0, step=1, value=30)
防御補正 = st.number_input("防御補正 (倍率)", min_value=0.1, step=0.1, value=1.0)
防御属性 = st.selectbox("防御属性", 属性一覧)
防御レベル = st.number_input("防御レベル", min_value=1, step=1, value=50)
回避 = st.slider("回避率 (%)", min_value=0, max_value=100, value=0)

# 計算
if st.button("計算する"):
    # 属性補正取得
    attr_coef = 属性補正.get((攻撃属性, 防御属性), 1.0)

    # 急所判定
    import random

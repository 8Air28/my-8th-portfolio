import streamlit as st

# ページ設定
st.set_page_config(
    page_title="ダメージ計算ツール",
    page_icon="⚔️",
    layout="centered"
)

# タイトル
st.title("⚔ ダメージ計算ツール")

st.markdown("""
このツールは攻撃力と防御力を入力すると、与えるダメージを計算します。  
属性相性・急所補正・命中/回避も対応。結果は履歴に保存されます。
""")

# 攻撃側入力
st.subheader("⚔ 攻撃側ステータス")
attack = st.number_input("攻撃力", min_value=1, step=1, value=50)
技補正 = st.slider("技補正", 0.1, 3.0, 1.0, 0.1)
属性攻撃 = st.selectbox("攻撃側属性", ["火", "木", "雷", "水", "光", "闇"])
攻撃レベル = st.number_input("攻撃側レベル", min_value=1, step=1, value=50)
攻撃回数 = st.number_input("攻撃回数", min_value=1, step=1, value=1)
急所率 = st.slider("急所率 (0〜1)", 0.0, 1.0, 0.0, 0.1)
命中 = st.slider("命中率 (%)", 0, 100, 100)

# 防御側入力
st.subheader("🛡 防御側ステータス")
defense = st.number_input("防御力", min_value=0, step=1, value=30)
防御補正 = st.slider("防御補正", 0.1, 3.0, 1.0, 0.1)
属性防御 = st.selectbox("防御側属性", ["火", "木", "雷", "水", "光", "闇"])
防御レベル = st.number_input("防御側レベル", min_value=1, step=1, value=50)
回避 = st.slider("回避率 (%)", 0, 100, 0)

# 計算ボタン
if st.button("計算する"):
    # 属性補正
    属性倍率 = {
        ("火", "木"): 2.0,
        ("木", "雷"): 2.0,
        ("雷", "水"): 2.0,
        ("水", "火"): 2.0,
        ("光", "闇"): 2.0,
        ("闇", "光"): 2.0
    }
    属性補正 = 属性倍率.get((属性攻撃, 属性防御), 1.0)

    # 急所補正
    急所補正 = 1.5 if 急所率 > 0 else 1.0

    # 命中・回避計算
    命中補正 = (命中 - 回避) / 100
    命中補正 = max(0, 命中補正)  # 0未満なら当たらない

    # ダメージ計算
    damage = max(1, (attack * 技補正 - defense * 防御補正) * 属性補正 * 急所補正 * 命中補正) * 攻撃回数

    st.success(f"✅ 与えたダメージ: {damage:.1f}")

    # 履歴保存
    if "履歴" not in st.session_state:
        st.session_state.履歴 = []
    st.session_state.履歴.append(
        f"Lv{攻撃レベル} {属性攻撃}攻撃 → Lv{防御レベル} {属性防御}防御: {damage:.1f}ダメージ"
    )

# 履歴表示
if "履歴" in st.session_state and len(st.session_state.履歴) > 0:
    st.markdown("---")
    st.subheader("📜 計算履歴")
    for h in reversed(st.session_state.履歴):
        st.write(h)

# フッター
st.markdown("""
---
作成者: 8Air28  
GitHub: [このポートフォリオ](https://github.com/8Air28/my-8th-portfolio)  
""")

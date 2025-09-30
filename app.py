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
シンプルだけどポートフォリオ向けに作りました。
""")

# 入力
attack = st.number_input("攻撃力", min_value=1, step=1, value=50)
defense = st.number_input("防御力", min_value=0, step=1, value=30)

# 計算ボタン
if st.button("計算する"):
    damage = max(1, attack - defense)
    st.success(f"✅ 与えたダメージ: {damage}")

# フッター
st.markdown("""
---
作成者: 8Air28  
GitHub: [このポートフォリオ](https://github.com/8Air28/my-8th-portfolio)  
""")

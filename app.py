import streamlit as st
import random

# ページ設定
st.set_page_config(
    page_title="ダメージ計算ツール",
    page_icon="⚔️",
    layout="centered"
)

st.title("⚔ ダメージ計算ツール")

st.markdown("""
このツールは攻撃側と防御側のステータスを入力して、与えるダメージを計算します。  
シンプルだけどポートフォリオ向けに作りました。
""")

# 相性表
attribute_chart = {
    "火": {"木": 1.5, "水": 0.5, "火": 1.0, "雷": 1.0, "光": 1.0, "闇": 1.0},
    "水": {"火": 1.5, "雷": 0.5, "木": 1.0, "水": 1.0, "光": 1.0, "闇": 1.0},
    "木": {"雷": 1.5, "火": 0.5, "水": 1.0, "木": 1.0, "光": 1.0, "闇": 1.0},
    "雷": {"水": 1.5, "木": 0.5, "火": 1.0, "雷": 1.0, "光": 1.0, "闇": 1.0},
    "光": {"闇": 1.5, "光": 1.0, "火": 1.0, "水": 1.0, "木": 1.0, "雷": 1.0},
    "闇": {"光": 1.5, "闇": 1.0, "火": 1.0, "水": 1.0, "木": 1.0, "雷": 1.0},
}

# セッションに履歴保存
if "history" not in st.session_state:
    st.session_state.history = []

# 攻撃側ステータス
st.subheader("攻撃側ステータス")
atk_power = st.number_input("攻撃力", min_value=1, step=1, value=50, key="atk_power")
atk_buff = st.slider("技補正(%)", 50, 200, 100, key="atk_buff")
atk_attr = st.selectbox("属性", ["火", "水", "木", "雷", "光", "闇"], key="atk_attr")
atk_level = st.number_input("レベル", min_value=1, step=1, value=50, key="atk_level")
atk_hits = st.number_input("回数", min_value=1, step=1, value=1, key="atk_hits")
atk_crit = st.slider("急所率(%)", 0, 100, 0, key="atk_crit")
atk_acc = st.slider("命中率(%)", 0, 100, 100, key="atk_acc")

# 防御側ステータス
st.subheader("防御側ステータス")
def_power = st.number_input("防御力", min_value=0, step=1, value=30, key="def_power")
def_buff = st.slider("防御補正(%)", 50, 200, 100, key="def_buff")
def_attr = st.selectbox("属性", ["火", "水", "木", "雷", "光", "闇"], key="def_attr")
def_level = st.number_input("レベル", min_value=1, step=1, value=50, key="def_level")
def_evade = st.slider("回避率(%)", 0, 100, 0, key="def_evade")

# ダメージ計算処理
def calculate_damage():
    # 補正を反映
    atk = atk_power * (atk_buff / 100)
    defense = def_power * (def_buff / 100)

    # 基本ダメージ
    base_damage = max(1, (atk * (atk_level / def_level)) - defense)

    # 属性補正
    multiplier = attribute_chart[atk_attr][def_attr]

    # 命中判定
    if random.random() > atk_acc / 100 * (1 - def_evade / 100):
        return "攻撃は外れた！"

    total_damage = 0
    crit_flag = False
    for _ in range(atk_hits):
        damage = base_damage * multiplier
        if random.random() < atk_crit / 100:
            damage *= 1.5
            crit_flag = True
        total_damage += int(damage)

    result = f"与えたダメージ: {total_damage}"
    if crit_flag:
        result += " (急所！)"
    return result

# 計算ボタン
if st.button("計算する", key="calc_button"):
    result = calculate_damage()
    st.success(result)
    st.session_state.history.insert(0, result)

# 履歴表示（カード風UI）
st.subheader("📜 計算履歴")

col1, col2 = st.columns([4,1])
with col2:
    if st.button("🗑 履歴クリア", key="clear_history"):
        st.session_state.history.clear()

for i, h in enumerate(st.session_state.history[:10]):  # 最新10件まで
    with st.container():
        st.markdown(f"""
        <div style="border:1px solid #ddd; border-radius:10px; padding:10px; margin:5px 0; background:#f9f9f9;">
            {i+1}. {h}
        </div>
        """, unsafe_allow_html=True)

# フッター
st.markdown("""
---
作成者: 8Air28  
GitHub: [このポートフォリオ](https://github.com/8Air28/my-8th-portfolio)  
""")

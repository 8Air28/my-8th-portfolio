import streamlit as st

# ページ設定
st.set_page_config(
    page_title="ダメージ計算ツール",
    page_icon="⚔️",
    layout="centered"
)

st.title("⚔ ダメージ計算ツール")

# --- 属性相性表 ---
def type_effectiveness(attacker, defender):
    if attacker == "火" and defender == "木":
        return 2.0
    elif attacker == "木" and defender == "雷":
        return 2.0
    elif attacker == "雷" and defender == "水":
        return 2.0
    elif attacker == "水" and defender == "火":
        return 2.0
    elif attacker == "光" and defender == "闇":
        return 2.0
    elif attacker == "闇" and defender == "光":
        return 2.0
    elif attacker == defender:
        return 0.5
    return 1.0

# --- 履歴の保持 ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- UI配置 ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 攻撃側ステータス")
    atk_power = st.number_input("攻撃力", min_value=1, step=1, value=50, key="atk_power")
    atk_buff = st.number_input("技補正", min_value=0.1, step=0.1, value=1.0, key="atk_buff")
    atk_attr = st.selectbox("属性", ["火", "水", "木", "雷", "光", "闇"], key="atk_attr")
    atk_level = st.number_input("レベル", min_value=1, step=1, value=10, key="atk_level")
    atk_times = st.number_input("回数", min_value=1, step=1, value=1, key="atk_times")
    crit_rate = st.slider("急所率 (%)", 0, 100, 10, key="crit_rate")
    accuracy = st.slider("命中 (%)", 1, 100, 95, key="accuracy")

with col2:
    st.markdown("### 防御側ステータス")
    def_power = st.number_input("防御力", min_value=0, step=1, value=30, key="def_power")
    def_buff = st.number_input("防御補正", min_value=0.1, step=0.1, value=1.0, key="def_buff")
    def_attr = st.selectbox("属性", ["火", "水", "木", "雷", "光", "闇"], key="def_attr")
    def_level = st.number_input("レベル", min_value=1, step=1, value=10, key="def_level")
    evasion = st.slider("回避 (%)", 0, 100, 5, key="evasion")

st.markdown("---")

# --- 計算処理 ---
if st.button("計算する"):
    # 基本ダメージ
    damage = max(1, int((atk_power * atk_buff) - (def_power * def_buff)))

    # 属性補正
    damage = int(damage * type_effectiveness(atk_attr, def_attr))

    # 急所補正（確率は簡易）
    crit = (crit_rate / 100) * 1.5 + (1 - crit_rate / 100) * 1.0
    damage = int(damage * crit)

    # 命中判定
    hit_rate = max(0, min(100, accuracy - evasion))

    # 複数回攻撃
    damage *= atk_times

    result_text = f"ダメージ予想: {damage}（{hit_rate}% ヒット率）"

    # 履歴に保存
    st.session_state.history.append({
        "result": result_text,
        "attacker": {
            "攻撃力": atk_power,
            "技補正": atk_buff,
            "属性": atk_attr,
            "レベル": atk_level,
            "回数": atk_times,
            "急所率": crit_rate,
            "命中": accuracy
        },
        "defender": {
            "防御力": def_power,
            "防御補正": def_buff,
            "属性": def_attr,
            "レベル": def_level,
            "回避": evasion
        }
    })

    st.success(result_text)

# --- 履歴表示（ツールチップ付きカード風UI） ---
st.markdown("## 📜 計算履歴")

tooltip_css = """
<style>
.tooltip {
  position: relative;
  display: inline-block;
  cursor: pointer;
  margin: 6px 0;
  padding: 10px 14px;
  background: white;
  border-radius: 10px;
  box-shadow: 2px 2px 6px rgba(0,0,0,0.15);
}
.tooltip .tooltiptext {
  visibility: hidden;
  width: 280px;
  background-color: #333;
  color: #fff;
  text-align: left;
  border-radius: 8px;
  padding: 10px;
  position: absolute;
  z-index: 1;
  bottom: 120%;
  left: 50%;
  margin-left: -140px;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 0.8em;
}
.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}
</style>
"""
st.markdown(tooltip_css, unsafe_allow_html=True)

for item in st.session_state.history[::-1]:
    attacker_info = "<br>".join([f"{k}: {v}" for k, v in item["attacker"].items()])
    defender_info = "<br>".join([f"{k}: {v}" for k, v in item["defender"].items()])
    details = f"<b>攻撃側</b><br>{attacker_info}<br><br><b>防御側</b><br>{defender_info}"

    st.markdown(
        f"""
        <div class="tooltip">{item['result']}
            <div class="tooltiptext">{details}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

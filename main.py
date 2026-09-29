import streamlit as st


# ============================================================
# 1. 페이지 기본 설정
# ============================================================

st.set_page_config(
    page_title="BBB PASS LAB",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# 2. 화면 디자인
# ============================================================

st.markdown(
    """
<style>

/* 전체 기본 글꼴 */
html, body, [class*="css"], .stApp {
    font-family: "Trebuchet MS", "Arial Rounded MT Bold", "Malgun Gothic", sans-serif;
}

/* 전체 배경 */
.stApp {
    background:
        linear-gradient(
            135deg,
            #f7fbff 0%,
            #eef5ff 45%,
            #f7f5ff 100%
        );
}

/* 본문 크기 */
.block-container {
    max-width: 1150px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

/* 상단 작은 글씨 */
.top-label {
    text-align: center;
    color: #6f7db7;
    font-size: 13px;
    letter-spacing: 4px;
    font-weight: 800;
    margin-bottom: 8px;
}

/* 메인 제목 */
.main-title {
    text-align: center;
    color: #24345d;
    font-size: 47px;
    font-weight: 900;
    margin-bottom: 8px;
    letter-spacing: -1px;
}

/* 부제목 */
.subtitle {
    text-align: center;
    color: #73809c;
    font-size: 16px;
    margin-bottom: 28px;
}

/* 구분선 */
.title-line {
    width: 60px;
    height: 3px;
    background: #7586d9;
    border-radius: 10px;
    margin: 0 auto 35px auto;
}

/* 기본 카드 */
.info-card {
    background: rgba(255,255,255,0.94);
    border: 1px solid #dae3f7;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 8px 25px rgba(63, 86, 140, 0.08);
    margin-bottom: 15px;
}

/* 상단 소개 박스 - 밝은 노란색 */
.intro-box {
    background: #fff9d9;
    border-left: 6px solid #f1d65c;
    border-radius: 14px;
    padding: 20px 22px;
    line-height: 1.9;
    color: #5d5a35;
    margin-top: 18px;
    margin-bottom: 14px;
}

/* 결과 카드 */
.result-card {
    background: white;
    border: 1px solid #dbe3f6;
    border-radius: 20px;
    padding: 28px;
    margin-top: 20px;
    box-shadow: 0 10px 30px rgba(55, 76, 125, 0.09);
}

/* 결과 점수 */
.score-number {
    text-align: center;
    font-size: 52px;
    color: #3d4f99;
    font-weight: 900;
    margin-bottom: 5px;
}

/* 결과 등급 */
.score-label {
    text-align: center;
    color: #69769c;
    font-size: 18px;
    font-weight: 700;
}

/* 좋은 요소 */
.good-box {
    background: #effaf5;
    border-left: 5px solid #59a884;
    border-radius: 10px;
    padding: 16px 18px;
    margin-top: 12px;
    line-height: 1.8;
}

/* 불리한 요소 */
.bad-box {
    background: #fff3f4;
    border-left: 5px solid #cf7380;
    border-radius: 10px;
    padding: 16px 18px;
    margin-top: 12px;
    line-height: 1.8;
}

/* 비교 설명 박스 */
.compare-box {
    background: #f6f8ff;
    border-left: 5px solid #798de3;
    border-radius: 10px;
    padding: 18px 20px;
    line-height: 1.9;
    margin-top: 16px;
}

/* 학습용 주의 박스 */
.notice-box {
    background: #fffbea;
    border-left: 5px solid #d9b84f;
    border-radius: 10px;
    padding: 17px 20px;
    line-height: 1.8;
    margin-top: 18px;
}

/* BBB 그림 박스 */
.diagram-wrap {
    background: white;
    border: 1px solid #dbe3f6;
    border-radius: 18px;
    padding: 20px;
    margin-top: 18px;
    margin-bottom: 20px;
    box-shadow: 0 8px 20px rgba(63, 86, 140, 0.06);
}

.diagram-title {
    text-align: center;
    color: #44558f;
    font-weight: 800;
    margin-bottom: 14px;
    font-size: 18px;
}

.diagram-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
}

.diagram-box {
    flex: 1;
    min-width: 180px;
    text-align: center;
    padding: 16px;
    border-radius: 14px;
    font-weight: 700;
    line-height: 1.7;
}

.blood-box {
    background: #ffe7ea;
    border: 2px solid #e39ca9;
    color: #8b4350;
}

.bbb-box {
    background: #e8f0ff;
    border: 2px solid #9eb7ea;
    color: #41598f;
}

.brain-box {
    background: #e9f9ef;
    border: 2px solid #9fd6af;
    color: #427254;
}

.arrow-box {
    font-size: 28px;
    font-weight: 900;
    color: #7685c5;
    min-width: 40px;
    text-align: center;
}

.diagram-note {
    margin-top: 14px;
    background: #f8faff;
    border-radius: 12px;
    padding: 14px 16px;
    line-height: 1.8;
    color: #5f6d8a;
}

/* 푸터 */
.footer {
    text-align: center;
    color: #98a2b8;
    font-size: 12px;
    margin-top: 50px;
}

/* 버튼 */
.stButton > button {
    width: 100%;
    height: 52px;
    border-radius: 10px;
    border: none;
    background: #45599e;
    color: white;
    font-weight: 800;
}

.stButton > button:hover {
    background: #354781;
    color: white;
    border: none;
}

/* metric 카드 */
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #dce4f5;
    border-radius: 14px;
    padding: 17px;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# 3. 점수 계산 함수
# ============================================================

def calculate_bbb_score(
    molecular_weight,
    lipid_solubility,
    polarity,
    charge,
    hydrogen_bond
):
    """
    입력한 분자 특성을 바탕으로
    BBB 통과에 유리한 정도를 0~100점으로 계산합니다.

    이 점수는 실제 의학적 예측값이 아니라
    학습용 단순 규칙 기반 모델입니다.
    """

    score = 0

    # ① 분자량
    if molecular_weight <= 400:
        score += 25
    elif molecular_weight <= 500:
        score += 18
    elif molecular_weight <= 600:
        score += 8
    else:
        score += 0

    # ② 지용성
    if lipid_solubility == "중간":
        score += 20
    elif lipid_solubility == "높음":
        score += 15
    elif lipid_solubility == "낮음":
        score += 5

    # ③ 극성
    if polarity == "낮음":
        score += 20
    elif polarity == "중간":
        score += 10
    elif polarity == "높음":
        score += 0

    # ④ 전하
    if charge == "전하 없음":
        score += 20
    elif charge == "전하 있음":
        score += 0

    # ⑤ 수소 결합 가능성
    if hydrogen_bond == "낮음":
        score += 15
    elif hydrogen_bond == "중간":
        score += 8
    elif hydrogen_bond == "높음":
        score += 0

    return score


# ============================================================
# 4. 점수에 따른 등급 함수
# ============================================================

def classify_score(score):

    if score >= 80:
        return "통과에 매우 유리한 조건", "🟢"
    elif score >= 60:
        return "통과에 비교적 유리한 조건", "🟡"
    elif score >= 40:
        return "통과 여부가 제한적인 조건", "🟠"
    else:
        return "통과에 불리한 조건", "🔴"


# ============================================================
# 5. 요인 분석 함수
# ============================================================

def analyze_factors(
    molecular_weight,
    lipid_solubility,
    polarity,
    charge,
    hydrogen_bond
):

    favorable = []
    unfavorable = []

    # 분자량
    if molecular_weight <= 500:
        favorable.append(
            "분자량이 비교적 작아 혈뇌장벽의 세포막을 통과하는 데 상대적으로 유리합니다."
        )
    else:
        unfavorable.append(
            "분자량이 커질수록 세포막을 직접 통과하기 어려워 혈뇌장벽 통과에 불리할 수 있습니다."
        )

    # 지용성
    if lipid_solubility in ["중간", "높음"]:
        favorable.append(
            "지용성이 있어 혈뇌장벽을 이루는 지질성 세포막을 통과하는 데 상대적으로 유리합니다."
        )
    else:
        unfavorable.append(
            "지용성이 낮아 지질막을 통한 수동 확산에 불리할 수 있습니다."
        )

    # 극성
    if polarity == "낮음":
        favorable.append(
            "극성이 낮아 물보다는 지질막을 통과하는 방향에 조금 더 유리합니다."
        )
    elif polarity == "높음":
        unfavorable.append(
            "극성이 높으면 물과 잘 상호작용하므로 지질성 막을 직접 통과하기 어려울 수 있습니다."
        )

    # 전하
    if charge == "전하 없음":
        favorable.append(
            "전하를 띠지 않아 세포막 내부의 소수성 환경을 통과하는 데 상대적으로 유리합니다."
        )
    else:
        unfavorable.append(
            "전하를 띤 분자는 막 내부로 들어가기 어려워 혈뇌장벽 통과에 불리할 수 있습니다."
        )

    # 수소 결합
    if hydrogen_bond == "낮음":
        favorable.append(
            "수소 결합 가능성이 낮아 물 분자와의 상호작용이 상대적으로 적어 막 투과에 유리할 수 있습니다."
        )
    elif hydrogen_bond == "높음":
        unfavorable.append(
            "수소 결합 가능성이 높으면 물과 더 강하게 상호작용하여 지질막을 통과하는 데 불리할 수 있습니다."
        )

    return favorable, unfavorable


# ============================================================
# 6. 비교 설명 함수
# ============================================================

def compare_molecules_detail(
    name_a,
    weight_a,
    lipid_a,
    polarity_a,
    charge_a,
    hydrogen_a,
    name_b,
    weight_b,
    lipid_b,
    polarity_b,
    charge_b,
    hydrogen_b
):
    """
    두 분자를 항목별로 비교해서
    왜 한 분자가 더 유리한지 설명합니다.
    """

    reasons_a = []
    reasons_b = []

    # 분자량 비교
    if weight_a < weight_b:
        reasons_a.append(
            f"분자량이 더 작습니다 ({weight_a} Da < {weight_b} Da). 일반적으로 더 작은 분자가 막 통과에 상대적으로 유리합니다."
        )
    elif weight_b < weight_a:
        reasons_b.append(
            f"분자량이 더 작습니다 ({weight_b} Da < {weight_a} Da). 일반적으로 더 작은 분자가 막 통과에 상대적으로 유리합니다."
        )

    # 지용성 비교
    lipid_rank = {"낮음": 1, "중간": 3, "높음": 2}
    if lipid_rank[lipid_a] > lipid_rank[lipid_b]:
        reasons_a.append(
            f"지용성 조건이 더 유리합니다 ({lipid_a}). 지질성 세포막을 통과하는 데 상대적으로 도움이 됩니다."
        )
    elif lipid_rank[lipid_b] > lipid_rank[lipid_a]:
        reasons_b.append(
            f"지용성 조건이 더 유리합니다 ({lipid_b}). 지질성 세포막을 통과하는 데 상대적으로 도움이 됩니다."
        )

    # 극성 비교
    polarity_rank = {"낮음": 3, "중간": 2, "높음": 1}
    if polarity_rank[polarity_a] > polarity_rank[polarity_b]:
        reasons_a.append(
            f"극성이 더 낮습니다 ({polarity_a}). 극성이 낮은 분자는 지질막 투과에 상대적으로 유리합니다."
        )
    elif polarity_rank[polarity_b] > polarity_rank[polarity_a]:
        reasons_b.append(
            f"극성이 더 낮습니다 ({polarity_b}). 극성이 낮은 분자는 지질막 투과에 상대적으로 유리합니다."
        )

    # 전하 비교
    charge_rank = {"전하 없음": 2, "전하 있음": 1}
    if charge_rank[charge_a] > charge_rank[charge_b]:
        reasons_a.append(
            "전하를 띠지 않습니다. 전하가 없는 분자는 막 내부의 소수성 환경을 통과하는 데 상대적으로 유리합니다."
        )
    elif charge_rank[charge_b] > charge_rank[charge_a]:
        reasons_b.append(
            "전하를 띠지 않습니다. 전하가 없는 분자는 막 내부의 소수성 환경을 통과하는 데 상대적으로 유리합니다."
        )

    # 수소 결합 비교
    hydrogen_rank = {"낮음": 3, "중간": 2, "높음": 1}
    if hydrogen_rank[hydrogen_a] > hydrogen_rank[hydrogen_b]:
        reasons_a.append(
            f"수소 결합 가능성이 더 낮습니다 ({hydrogen_a}). 수소 결합 가능성이 낮을수록 막 투과에 유리할 수 있습니다."
        )
    elif hydrogen_rank[hydrogen_b] > hydrogen_rank[hydrogen_a]:
        reasons_b.append(
            f"수소 결합 가능성이 더 낮습니다 ({hydrogen_b}). 수소 결합 가능성이 낮을수록 막 투과에 유리할 수 있습니다."
        )

    return reasons_a, reasons_b


# ============================================================
# 7. 결과 출력 함수
# ============================================================

def show_result(
    name,
    molecular_weight,
    lipid_solubility,
    polarity,
    charge,
    hydrogen_bond
):

    score = calculate_bbb_score(
        molecular_weight,
        lipid_solubility,
        polarity,
        charge,
        hydrogen_bond
    )

    level, icon = classify_score(score)

    favorable, unfavorable = analyze_factors(
        molecular_weight,
        lipid_solubility,
        polarity,
        charge,
        hydrogen_bond
    )

    st.markdown(
        f"""
<div class="result-card">

<div style="text-align:center; color:#7986a8; font-weight:700;">
{name}
</div>

<div class="score-number">
{score}
</div>

<div class="score-label">
{icon} {level}
</div>

</div>
""",
        unsafe_allow_html=True
    )

    st.progress(score)

    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.metric("분자량", f"{molecular_weight} Da")
    with m2:
        st.metric("지용성", lipid_solubility)
    with m3:
        st.metric("극성", polarity)
    with m4:
        st.metric("전하", charge)
    with m5:
        st.metric("수소 결합", hydrogen_bond)

    if favorable:
        good_text = ""
        for factor in favorable:
            good_text += f"✓ {factor}<br>"

        st.markdown(
            f"""
<div class="good-box">
<b>🟢 BBB 통과에 상대적으로 유리한 요소</b><br><br>
{good_text}
</div>
""",
            unsafe_allow_html=True
        )

    if unfavorable:
        bad_text = ""
        for factor in unfavorable:
            bad_text += f"• {factor}<br>"

        st.markdown(
            f"""
<div class="bad-box">
<b>🔴 BBB 통과에 상대적으로 불리한 요소</b><br><br>
{bad_text}
</div>
""",
            unsafe_allow_html=True
        )

    return score


# ============================================================
# 8. 공통 입력 함수
# ============================================================

def molecule_input(prefix):

    name = st.text_input(
        "분자 이름",
        placeholder="예: 분자 A",
        key=f"{prefix}_name"
    )

    molecular_weight = st.slider(
        "⚖️ 분자량 (Da)",
        min_value=100,
        max_value=1000,
        value=350,
        step=10,
        key=f"{prefix}_weight"
    )

    lipid_solubility = st.selectbox(
        "💧 지용성",
        ["선택하세요", "낮음", "중간", "높음"],
        key=f"{prefix}_lipid"
    )

    polarity = st.selectbox(
        "🧲 극성",
        ["선택하세요", "낮음", "중간", "높음"],
        key=f"{prefix}_polarity"
    )

    charge = st.selectbox(
        "⚡ 전하",
        ["선택하세요", "전하 없음", "전하 있음"],
        key=f"{prefix}_charge"
    )

    hydrogen_bond = st.selectbox(
        "🔗 수소 결합 가능성",
        ["선택하세요", "낮음", "중간", "높음"],
        key=f"{prefix}_hydrogen"
    )

    return (
        name,
        molecular_weight,
        lipid_solubility,
        polarity,
        charge,
        hydrogen_bond
    )


# ============================================================
# 9. 입력값 검증 함수
# ============================================================

def validate_input(
    name,
    lipid_solubility,
    polarity,
    charge,
    hydrogen_bond
):

    if not name.strip():
        st.warning("⚠️ 분자 이름을 입력해 주세요.")
        return False

    if lipid_solubility == "선택하세요":
        st.warning("⚠️ 지용성을 선택해 주세요.")
        return False

    if polarity == "선택하세요":
        st.warning("⚠️ 극성을 선택해 주세요.")
        return False

    if charge == "선택하세요":
        st.warning("⚠️ 전하 여부를 선택해 주세요.")
        return False

    if hydrogen_bond == "선택하세요":
        st.warning("⚠️ 수소 결합 가능성을 선택해 주세요.")
        return False

    return True


# ============================================================
# 10. 상단 화면
# ============================================================

st.markdown(
    '<div class="top-label">BLOOD-BRAIN BARRIER LEARNING LAB</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">🧠 BBB PASS LAB</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="subtitle">
분자의 특성을 바꾸면서 혈뇌장벽 통과에 어떤 조건이 영향을 주는지 알아보는 교육용 시뮬레이터
</div>
""",
    unsafe_allow_html=True
)

st.markdown(
    '<div class="title-line"></div>',
    unsafe_allow_html=True
)


# ============================================================
# 11. 상단 프로그램 설명 박스
# ============================================================

st.markdown(
    """
<div class="intro-box">

<b>📌 이 프로그램은 무엇인가요?</b><br><br>

이 프로그램은 <b>혈뇌장벽(BBB, Blood-Brain Barrier)</b>을 주제로,
분자의 여러 특성에 따라 BBB 통과에 얼마나 유리한지 학습해 보는
<b>교육용 시뮬레이터</b>입니다.

사용자는 분자량, 지용성, 극성, 전하, 수소 결합 가능성을 입력하고
그 결과를 점수와 설명으로 확인할 수 있습니다.
또한 두 분자를 비교하여 <b>어떤 특성이 더 유리하게 작용하는지</b>도 볼 수 있습니다.

<br><br>

⚠️ 이 프로그램은 실제 약물 개발이나 임상 판단을 위한 예측 도구가 아니라,
<b>혈뇌장벽과 분자 특성의 관계를 이해하기 위한 학습용 프로그램</b>입니다.

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# 12. 탭 구성
# 순서: BBB 원리 학습 → 분자 분석 → 두 분자 비교
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📚 BBB 원리 학습",
        "🔬 분자 분석",
        "⚖️ 두 분자 비교"
    ]
)


# ============================================================
# TAB 1. BBB 원리 학습
# ============================================================

with tab1:

    st.subheader("📚 혈뇌장벽과 분자 특성")

    st.markdown(
        """
### 🧠 1. 혈뇌장벽(BBB)이란?

혈뇌장벽은 혈액 속의 물질이 뇌 조직으로 들어가는 과정을 선택적으로 조절하는 장벽입니다.  
뇌는 우리 몸에서 매우 중요한 기관이기 때문에, 모든 물질이 자유롭게 드나들면
뇌의 환경이 쉽게 흔들릴 수 있습니다. 그래서 혈뇌장벽은 뇌를 보호하기 위해
필요한 물질은 선별적으로 통과시키고, 해로운 물질이나 불필요한 물질은 제한합니다.

혈뇌장벽은 주로 **모세혈관 내피세포**, 그 사이를 단단히 붙여 주는 **밀착연접(tight junction)**,
그리고 주변의 **성상세포(astrocyte)** 등의 도움으로 유지됩니다.
이 구조 덕분에 혈액 속 물질이 뇌로 무분별하게 들어가는 것이 어렵습니다.

쉽게 말하면, 혈뇌장벽은 **뇌를 보호하는 엄격한 출입문**과 같습니다.

---
"""
    )

    st.markdown(
        """
<div class="diagram-wrap">
<div class="diagram-title">🖼️ 혈뇌장벽 간단 도식</div>

<div class="diagram-row">
    <div class="diagram-box blood-box">
        혈액 속 물질<br>
        산소, 영양소, 약물, 독성 물질
    </div>
    <div class="arrow-box">→</div>
    <div class="diagram-box bbb-box">
        혈뇌장벽(BBB)<br>
        내피세포 + 밀착연접<br>
        선택적으로 통과 조절
    </div>
    <div class="arrow-box">→</div>
    <div class="diagram-box brain-box">
        뇌 조직<br>
        신경세포가 안정적으로 작동해야 하는 공간
    </div>
</div>

<div class="diagram-note">
BBB는 혈액 속 모든 물질을 뇌로 보내는 것이 아니라,
일부는 통과시키고 일부는 막으면서 뇌의 내부 환경을 안정적으로 유지합니다.
</div>
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
### ⚖️ 2. 분자량과 BBB 통과

분자량은 분자의 크기를 어느 정도 나타내는 값입니다.  
일반적으로 분자량이 너무 크면 혈뇌장벽을 이루는 세포막을 직접 통과하기 어려워집니다.
즉, **작은 분자일수록 상대적으로 BBB 통과에 유리**한 경향이 있습니다.

---

### 💧 3. 지용성과 BBB 통과

혈뇌장벽을 이루는 세포막은 지질 성분을 포함하고 있습니다.  
그래서 어느 정도 **지용성(지방에 잘 섞이는 성질)**이 있는 분자는
막을 통과하는 데 상대적으로 유리할 수 있습니다.

하지만 지용성이 무조건 높다고 다 좋은 것은 아니고,
이 프로그램에서는 학습용으로 **중간~높은 지용성**을 더 유리하게 반영했습니다.

---

### 🧲 4. 극성과 BBB 통과

극성이 높은 분자는 물과 잘 상호작용합니다.  
하지만 세포막은 지질성 구조이기 때문에,
극성이 너무 높으면 막을 통과하는 것이 어려워질 수 있습니다.

즉, **극성이 낮은 분자가 BBB를 직접 통과하는 데 상대적으로 유리**합니다.

---

### ⚡ 5. 전하와 BBB 통과

전하를 띠는 분자는 막 내부의 소수성 환경을 통과하기가 어렵습니다.  
그래서 **전하를 띠지 않는 중성 분자**가
BBB를 통한 수동 확산에 더 유리한 경우가 많습니다.

---

### 🔗 6. 수소 결합 가능성과 BBB 통과

수소 결합 가능성이 높은 분자는 주변의 물 분자와 더 강하게 상호작용할 수 있습니다.  
이런 성질은 물 환경에서는 도움이 될 수 있지만,
지질성 세포막을 직접 통과하는 데에는 불리하게 작용할 수 있습니다.

즉, **수소 결합 가능성이 낮을수록 BBB 통과에 상대적으로 유리할 수 있습니다.**

---

### 🚨 7. 실제 BBB는 더 복잡합니다

실제 혈뇌장벽 통과는 이 프로그램에서 다루는 요소 외에도
여러 조건의 영향을 받습니다.

- 특정 운반체 단백질의 존재
- 능동 수송
- 배출 수송체
- 분자의 정확한 구조
- 단백질 결합 정도
- 체내 대사

따라서 이 프로그램의 결과는 **실제 의학적 예측이 아니라 학습용 참고 결과**입니다.
"""
    )


# ============================================================
# TAB 2. 단일 분자 분석
# ============================================================

with tab2:

    st.subheader("🔬 분자 특성 분석")
    st.write("분자의 특성을 입력하고 BBB 통과에 유리한 정도를 확인해 보세요.")

    single_input = molecule_input("single")

    if st.button("🧠 BBB 조건 분석하기", key="single_button"):

        (
            name,
            molecular_weight,
            lipid_solubility,
            polarity,
            charge,
            hydrogen_bond
        ) = single_input

        if validate_input(
            name,
            lipid_solubility,
            polarity,
            charge,
            hydrogen_bond
        ):

            if molecular_weight >= 800:
                st.info(
                    "ℹ️ 매우 큰 분자에서는 단순한 물리화학적 특성만으로 BBB 통과를 설명하기 어렵습니다."
                )

            show_result(
                name,
                molecular_weight,
                lipid_solubility,
                polarity,
                charge,
                hydrogen_bond
            )


# ============================================================
# TAB 3. 두 분자 비교
# ============================================================

with tab3:

    st.subheader("⚖️ 두 분자의 조건 비교")
    st.write(
        "두 분자의 특성을 각각 입력하면 어떤 분자가 BBB 통과에 상대적으로 유리한지 비교할 수 있습니다."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🅰️ 분자 A")
        molecule_a = molecule_input("A")

    with col2:
        st.markdown("### 🅱️ 분자 B")
        molecule_b = molecule_input("B")

    if st.button("⚖️ 두 분자 비교하기", key="compare_button"):

        (
            name_a,
            weight_a,
            lipid_a,
            polarity_a,
            charge_a,
            hydrogen_a
        ) = molecule_a

        (
            name_b,
            weight_b,
            lipid_b,
            polarity_b,
            charge_b,
            hydrogen_b
        ) = molecule_b

        valid_a = validate_input(
            name_a,
            lipid_a,
            polarity_a,
            charge_a,
            hydrogen_a
        )

        valid_b = validate_input(
            name_b,
            lipid_b,
            polarity_b,
            charge_b,
            hydrogen_b
        )

        if valid_a and valid_b:

            if name_a.strip() == name_b.strip():
                st.warning("⚠️ 비교하기 쉽도록 서로 다른 분자 이름을 입력해 주세요.")
            else:
                score_a = calculate_bbb_score(
                    weight_a,
                    lipid_a,
                    polarity_a,
                    charge_a,
                    hydrogen_a
                )

                score_b = calculate_bbb_score(
                    weight_b,
                    lipid_b,
                    polarity_b,
                    charge_b,
                    hydrogen_b
                )

                st.markdown("---")
                st.subheader("📊 비교 결과")

                result1, result2 = st.columns(2)

                with result1:
                    level_a, icon_a = classify_score(score_a)
                    st.metric(label=f"🅰️ {name_a}", value=f"{score_a}점")
                    st.progress(score_a)
                    st.caption(f"{icon_a} {level_a}")

                with result2:
                    level_b, icon_b = classify_score(score_b)
                    st.metric(label=f"🅱️ {name_b}", value=f"{score_b}점")
                    st.progress(score_b)
                    st.caption(f"{icon_b} {level_b}")

                reasons_a, reasons_b = compare_molecules_detail(
                    name_a, weight_a, lipid_a, polarity_a, charge_a, hydrogen_a,
                    name_b, weight_b, lipid_b, polarity_b, charge_b, hydrogen_b
                )

                if score_a > score_b:
                    difference = score_a - score_b

                    st.success(
                        f"🧠 이 학습 모델에서는 **{name_a}**가 **{name_b}**보다 BBB 통과에 더 유리한 조건을 **{difference}점 더 많이** 갖고 있습니다."
                    )

                    reason_text = ""
                    for reason in reasons_a:
                        reason_text += f"✓ {reason}<br>"

                    if reason_text == "":
                        reason_text = "✓ 여러 조건이 조금씩 더 유리하게 작용했습니다.<br>"

                    st.markdown(
                        f"""
<div class="compare-box">
<b>왜 {name_a}가 더 잘 통과할 가능성이 높을까요?</b><br><br>
{reason_text}
</div>
""",
                        unsafe_allow_html=True
                    )

                elif score_b > score_a:
                    difference = score_b - score_a

                    st.success(
                        f"🧠 이 학습 모델에서는 **{name_b}**가 **{name_a}**보다 BBB 통과에 더 유리한 조건을 **{difference}점 더 많이** 갖고 있습니다."
                    )

                    reason_text = ""
                    for reason in reasons_b:
                        reason_text += f"✓ {reason}<br>"

                    if reason_text == "":
                        reason_text = "✓ 여러 조건이 조금씩 더 유리하게 작용했습니다.<br>"

                    st.markdown(
                        f"""
<div class="compare-box">
<b>왜 {name_b}가 더 잘 통과할 가능성이 높을까요?</b><br><br>
{reason_text}
</div>
""",
                        unsafe_allow_html=True
                    )

                else:
                    st.info("두 분자의 BBB 통과 조건 점수가 같습니다.")

                    st.markdown(
                        """
<div class="compare-box">
<b>왜 점수가 같을까요?</b><br><br>
두 분자의 분자량, 지용성, 극성, 전하, 수소 결합 가능성이
이 학습 모델에서 비슷한 수준으로 작용했기 때문입니다.
</div>
""",
                        unsafe_allow_html=True
                    )


# ============================================================
# 13. Footer
# ============================================================

st.markdown(
    """
<div class="footer">

BBB PASS LAB · BLOOD-BRAIN BARRIER LEARNING SIMULATOR<br><br>

교육 목적으로 제작된 규칙 기반 학습 모델입니다.

</div>
""",
    unsafe_allow_html=True
)

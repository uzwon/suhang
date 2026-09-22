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

/* 카드 */
.info-card {
    background: rgba(255,255,255,0.94);
    border: 1px solid #dae3f7;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 8px 25px rgba(63, 86, 140, 0.08);
    margin-bottom: 15px;
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

/* 주의 박스 */
.notice-box {
    background: #fffbea;
    border-left: 5px solid #d9b84f;
    border-radius: 10px;
    padding: 17px 20px;
    line-height: 1.8;
    margin-top: 18px;
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

    주의:
    실제 BBB 투과율을 예측하는 임상 모델이 아니라
    학습 목적의 단순화된 규칙 기반 모델입니다.
    """

    score = 0


    # --------------------------------------------------------
    # ① 분자량 점수
    # --------------------------------------------------------

    if molecular_weight <= 400:
        score += 25

    elif molecular_weight <= 500:
        score += 18

    elif molecular_weight <= 600:
        score += 8

    else:
        score += 0


    # --------------------------------------------------------
    # ② 지용성 점수
    # 지나치게 낮은 지용성보다
    # 적절한 지용성이 수동 확산에 상대적으로 유리하다고
    # 단순화하여 반영합니다.
    # --------------------------------------------------------

    if lipid_solubility == "중간":
        score += 20

    elif lipid_solubility == "높음":
        score += 15

    elif lipid_solubility == "낮음":
        score += 5


    # --------------------------------------------------------
    # ③ 극성 점수
    # --------------------------------------------------------

    if polarity == "낮음":
        score += 20

    elif polarity == "중간":
        score += 10

    elif polarity == "높음":
        score += 0


    # --------------------------------------------------------
    # ④ 전하 점수
    # --------------------------------------------------------

    if charge == "전하 없음":
        score += 20

    elif charge == "전하 있음":
        score += 0


    # --------------------------------------------------------
    # ⑤ 수소 결합 가능성
    # --------------------------------------------------------

    if hydrogen_bond == "낮음":
        score += 15

    elif hydrogen_bond == "중간":
        score += 8

    elif hydrogen_bond == "높음":
        score += 0


    return score


# ============================================================
# 4. 점수에 따른 결과 등급 함수
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
# 5. 각 조건을 설명하는 함수
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
            "분자량이 비교적 작아 수동 확산에 상대적으로 유리합니다."
        )

    else:

        unfavorable.append(
            "분자량이 큰 편이라 혈뇌장벽을 통과하는 데 불리한 요소가 될 수 있습니다."
        )


    # 지용성
    if lipid_solubility in ["중간", "높음"]:

        favorable.append(
            "지용성이 있어 세포막의 지질층을 통과하는 데 상대적으로 유리합니다."
        )

    else:

        unfavorable.append(
            "지용성이 낮아 세포막을 통한 수동 확산에 불리할 수 있습니다."
        )


    # 극성
    if polarity == "낮음":

        favorable.append(
            "극성이 낮아 지질막을 통한 확산에 상대적으로 유리합니다."
        )

    elif polarity == "높음":

        unfavorable.append(
            "극성이 높아 지질성 세포막을 통과하기 어려울 수 있습니다."
        )


    # 전하
    if charge == "전하 없음":

        favorable.append(
            "전하를 띠지 않아 막을 통한 수동 확산에 상대적으로 유리합니다."
        )

    else:

        unfavorable.append(
            "전하를 띤 분자는 지질막을 직접 통과하기 어려울 수 있습니다."
        )


    # 수소 결합
    if hydrogen_bond == "낮음":

        favorable.append(
            "수소 결합 가능성이 낮아 막 투과에 상대적으로 유리한 조건입니다."
        )

    elif hydrogen_bond == "높음":

        unfavorable.append(
            "수소 결합 가능성이 높아 물과 강하게 상호작용하여 수동 확산에 불리할 수 있습니다."
        )


    return favorable, unfavorable


# ============================================================
# 6. 결과 화면 출력 함수
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


    # 점수 진행 막대
    st.progress(
        score
    )


    # --------------------------------------------------------
    # 입력 조건 표시
    # --------------------------------------------------------

    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.metric(
            "분자량",
            f"{molecular_weight} Da"
        )

    with m2:
        st.metric(
            "지용성",
            lipid_solubility
        )

    with m3:
        st.metric(
            "극성",
            polarity
        )

    with m4:
        st.metric(
            "전하",
            charge
        )

    with m5:
        st.metric(
            "수소 결합",
            hydrogen_bond
        )


    # --------------------------------------------------------
    # 유리한 요소
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # 불리한 요소
    # --------------------------------------------------------

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
# 7. 공통 입력 함수
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
        [
            "선택하세요",
            "낮음",
            "중간",
            "높음"
        ],
        key=f"{prefix}_lipid"
    )


    polarity = st.selectbox(
        "🧲 극성",
        [
            "선택하세요",
            "낮음",
            "중간",
            "높음"
        ],
        key=f"{prefix}_polarity"
    )


    charge = st.selectbox(
        "⚡ 전하",
        [
            "선택하세요",
            "전하 없음",
            "전하 있음"
        ],
        key=f"{prefix}_charge"
    )


    hydrogen_bond = st.selectbox(
        "🔗 수소 결합 가능성",
        [
            "선택하세요",
            "낮음",
            "중간",
            "높음"
        ],
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
# 8. 입력값 검증 함수
# ============================================================

def validate_input(
    name,
    lipid_solubility,
    polarity,
    charge,
    hydrogen_bond
):

    # 예외 상황 1
    # 이름이 비어 있는 경우

    if not name.strip():

        st.warning(
            "⚠️ 분자 이름을 입력해 주세요."
        )

        return False


    # 예외 상황 2
    # 지용성을 선택하지 않은 경우

    if lipid_solubility == "선택하세요":

        st.warning(
            "⚠️ 지용성을 선택해 주세요."
        )

        return False


    # 예외 상황 3
    # 극성을 선택하지 않은 경우

    if polarity == "선택하세요":

        st.warning(
            "⚠️ 극성을 선택해 주세요."
        )

        return False


    # 예외 상황 4
    # 전하를 선택하지 않은 경우

    if charge == "선택하세요":

        st.warning(
            "⚠️ 전하 여부를 선택해 주세요."
        )

        return False


    # 예외 상황 5
    # 수소 결합 가능성을 선택하지 않은 경우

    if hydrogen_bond == "선택하세요":

        st.warning(
            "⚠️ 수소 결합 가능성을 선택해 주세요."
        )

        return False


    return True


# ============================================================
# 9. 상단 화면
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
분자의 특성을 바꾸면서 혈뇌장벽 통과에 어떤 조건이 영향을 주는지 알아보세요.
</div>
""",
    unsafe_allow_html=True
)

st.markdown(
    '<div class="title-line"></div>',
    unsafe_allow_html=True
)


# ============================================================
# 10. 중요한 안내
# ============================================================

st.markdown(
    """
<div class="notice-box">

<b>📌 이 프로그램은 무엇인가요?</b><br><br>

혈뇌장벽(BBB)은 혈액 속 물질이 뇌 조직으로 이동하는 것을
선택적으로 제한하는 구조입니다.

이 프로그램은 분자량, 지용성, 극성, 전하 등의 조건을 바꾸면서
어떤 특성이 BBB 통과에 상대적으로 유리하거나 불리한지를
학습하기 위한 <b>교육용 시뮬레이터</b>입니다.

<br><br>

⚠️ 실제 약물의 혈뇌장벽 투과 여부를 의학적으로 예측하거나
판단하는 프로그램이 아닙니다.

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# 11. 탭 구성
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "🔬 분자 분석",
        "⚖️ 두 분자 비교",
        "📚 BBB 원리 학습"
    ]
)


# ============================================================
# TAB 1
# 단일 분자 분석
# ============================================================

with tab1:

    st.subheader(
        "🔬 분자 특성 분석"
    )

    st.write(
        "분자의 특성을 입력하고 BBB 통과에 유리한 정도를 확인해 보세요."
    )


    single_input = molecule_input(
        "single"
    )


    if st.button(
        "🧠 BBB 조건 분석하기",
        key="single_button"
    ):

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

            # 분자량이 매우 큰 경우 추가 안내
            if molecular_weight >= 800:

                st.info(
                    "ℹ️ 매우 큰 분자에서는 단순한 물리화학적 특성만으로 "
                    "BBB 통과를 설명하기 어렵습니다."
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
# TAB 2
# 두 분자 비교
# ============================================================

with tab2:

    st.subheader(
        "⚖️ 두 분자의 조건 비교"
    )

    st.write(
        "두 분자의 특성을 각각 입력하면 어떤 분자가 "
        "BBB 통과에 상대적으로 유리한 조건인지 비교할 수 있습니다."
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # 분자 A 입력
    # --------------------------------------------------------

    with col1:

        st.markdown(
            "### 🅰️ 분자 A"
        )

        molecule_a = molecule_input(
            "A"
        )


    # --------------------------------------------------------
    # 분자 B 입력
    # --------------------------------------------------------

    with col2:

        st.markdown(
            "### 🅱️ 분자 B"
        )

        molecule_b = molecule_input(
            "B"
        )


    if st.button(
        "⚖️ 두 분자 비교하기",
        key="compare_button"
    ):

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

            # 예외 상황:
            # 두 분자의 이름이 같은 경우

            if name_a.strip() == name_b.strip():

                st.warning(
                    "⚠️ 비교하기 쉽도록 서로 다른 분자 이름을 입력해 주세요."
                )


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

                st.subheader(
                    "📊 비교 결과"
                )


                result1, result2 = st.columns(2)


                with result1:

                    level_a, icon_a = classify_score(
                        score_a
                    )

                    st.metric(
                        label=f"🅰️ {name_a}",
                        value=f"{score_a}점"
                    )

                    st.progress(
                        score_a
                    )

                    st.caption(
                        f"{icon_a} {level_a}"
                    )


                with result2:

                    level_b, icon_b = classify_score(
                        score_b
                    )

                    st.metric(
                        label=f"🅱️ {name_b}",
                        value=f"{score_b}점"
                    )

                    st.progress(
                        score_b
                    )

                    st.caption(
                        f"{icon_b} {level_b}"
                    )


                # ------------------------------------------------
                # 최종 비교
                # ------------------------------------------------

                if score_a > score_b:

                    difference = score_a - score_b

                    st.success(
                        f"🧠 이 학습 모델에서는 **{name_a}**가 "
                        f"**{name_b}**보다 BBB 통과에 유리한 조건을 "
                        f"**{difference}점 더 많이 갖고 있습니다.**"
                    )


                elif score_b > score_a:

                    difference = score_b - score_a

                    st.success(
                        f"🧠 이 학습 모델에서는 **{name_b}**가 "
                        f"**{name_a}**보다 BBB 통과에 유리한 조건을 "
                        f"**{difference}점 더 많이 갖고 있습니다.**"
                    )


                else:

                    st.info(
                        "두 분자의 BBB 통과 조건 점수가 같습니다."
                    )


# ============================================================
# TAB 3
# BBB 원리 학습
# ============================================================

with tab3:

    st.subheader(
        "📚 혈뇌장벽과 분자 특성"
    )


    st.markdown(
        """
### 🧠 1. 혈뇌장벽(BBB)이란?

혈뇌장벽은 혈액과 뇌 조직 사이에서 물질의 이동을 제한하는
선택적 장벽입니다.

뇌의 환경을 안정적으로 유지하고 불필요하거나 유해한 물질이
뇌 조직으로 쉽게 들어가는 것을 막는 역할을 합니다.

---

### ⚖️ 2. 분자량

일반적으로 분자의 크기가 커질수록 세포막을 직접 통과하는 것이
어려워질 수 있습니다.

이 프로그램에서는 분자량이 작을수록 상대적으로 높은 점수를
주도록 단순화했습니다.

---

### 💧 3. 지용성

세포막은 지질 성분을 포함하고 있기 때문에 어느 정도 지용성을 가진
분자는 막을 통한 수동 확산에 상대적으로 유리할 수 있습니다.

하지만 실제 BBB 투과는 지용성 하나만으로 결정되지 않습니다.

---

### 🧲 4. 극성

극성이 높은 분자는 물과 잘 상호작용하지만
지질성 세포막을 직접 통과하는 데에는 불리할 수 있습니다.

---

### ⚡ 5. 전하

강한 전하를 가진 분자는 지질막 내부로 들어가기 어려워
수동 확산에 불리할 수 있습니다.

---

### 🔗 6. 수소 결합

수소 결합 가능성이 높은 분자는 주변의 물 분자와 강하게 상호작용할 수 있어
막을 직접 통과하는 데 불리한 요인이 될 수 있습니다.

---

### 🚨 실제 BBB는 더 복잡합니다

실제 혈뇌장벽의 투과에는 이 프로그램에서 다루지 않는 요소도 존재합니다.

- 특정 운반체 단백질
- 능동 수송
- 배출 수송체
- 분자의 정확한 구조
- 단백질 결합
- 생체 내 대사

따라서 이 프로그램의 점수는 실제 약물의 BBB 투과율을 의미하지 않습니다.
"""
    )


# ============================================================
# 12. Footer
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

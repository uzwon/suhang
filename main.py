import streamlit as st
import random
from pathlib import Path


# ============================================================
# 1. 페이지 기본 설정
# ============================================================

st.set_page_config(
    page_title="NEURO CHECK-IN",
    page_icon="🏥",
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
            #101821 0%,
            #17232f 45%,
            #0c141c 100%
        );
}

/* 전체 본문 */
.block-container {
    max-width: 1100px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}


/* 상단 작은 글씨 */
.game-label {
    text-align: center;
    color: #6eb5c9;
    letter-spacing: 5px;
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 8px;
}


/* 메인 제목 */
.game-title {
    text-align: center;
    color: #f3f7f8;
    font-size: 48px;
    font-weight: 900;
    margin-bottom: 5px;
}


/* 부제목 */
.game-subtitle {
    text-align: center;
    color: #91a7b5;
    font-size: 16px;
    margin-bottom: 25px;
}


/* 경고선 */
.warning-line {
    width: 90px;
    height: 3px;
    margin: 0 auto 30px auto;
    border-radius: 10px;
    background: #bc4d5e;
}


/* 시작 설명 박스 */
.intro-box {
    background: rgba(239, 247, 249, 0.96);
    color: #233842;
    border-radius: 18px;
    padding: 26px 30px;
    line-height: 1.9;
    border: 1px solid #85aeb9;
    margin-bottom: 22px;
}


/* 근무 규칙 */
.rule-box {
    background: #172832;
    color: #dce8eb;
    border-left: 5px solid #d1a54b;
    border-radius: 12px;
    padding: 20px 22px;
    margin-top: 16px;
    line-height: 1.8;
}


/* 환자 카드 */
.patient-card {
    background: rgba(242, 247, 248, 0.98);
    color: #23343d;
    border-radius: 18px;
    padding: 24px;
    border: 1px solid #8fafba;
    box-shadow: 0 10px 30px rgba(0,0,0,0.28);
}


/* 환자 번호 */
.case-number {
    color: #3f7888;
    font-size: 13px;
    font-weight: 900;
    letter-spacing: 3px;
}


/* 환자 이름 */
.patient-name {
    font-size: 29px;
    font-weight: 900;
    color: #192c34;
    margin-top: 7px;
    margin-bottom: 17px;
}


/* 정보 */
.patient-info {
    background: #e8f0f2;
    border-radius: 12px;
    padding: 18px;
    line-height: 1.9;
    color: #354d57;
}


/* 기록 카드 */
.record-box {
    background: #f7f2df;
    color: #514d38;
    border: 1px solid #d9ce9d;
    border-radius: 12px;
    padding: 18px;
    line-height: 1.9;
    margin-top: 14px;
}


/* 이미지 없을 때 */
.image-placeholder {
    width: 100%;
    min-height: 330px;
    background:
        linear-gradient(
            145deg,
            #d8e7eb,
            #b9d0d7
        );
    border: 1px solid #91aab3;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #46626c;
    font-size: 85px;
    margin-bottom: 10px;
}


/* 결과 정답 */
.correct-box {
    background: #e8f7ef;
    border-left: 6px solid #4b9a70;
    color: #274a36;
    border-radius: 12px;
    padding: 20px;
    line-height: 1.8;
    margin-top: 20px;
}


/* 결과 오답 */
.wrong-box {
    background: #fbeaec;
    border-left: 6px solid #bd5967;
    color: #65343b;
    border-radius: 12px;
    padding: 20px;
    line-height: 1.8;
    margin-top: 20px;
}


/* 의료 설명 */
.medical-box {
    background: #eaf1fb;
    border-left: 6px solid #668ab6;
    color: #30485e;
    border-radius: 12px;
    padding: 20px;
    line-height: 1.8;
    margin-top: 14px;
}


/* 상태바 */
.status-box {
    background: rgba(224, 238, 241, 0.96);
    border-radius: 14px;
    padding: 15px;
    text-align: center;
    color: #243a42;
    font-weight: 800;
}


/* 버튼 */
.stButton > button {
    width: 100%;
    min-height: 53px;
    border-radius: 10px;
    font-weight: 800;
}


/* 제목들 */
h1, h2, h3 {
    color: #edf5f7 !important;
}


/* footer */
.footer {
    text-align: center;
    color: #708894;
    margin-top: 45px;
    font-size: 12px;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# 3. 게임에 사용할 환자 데이터
# ============================================================
#
# anomaly가 True인 경우:
# 실제 질환이 있어서가 아니라
# "기록상 존재할 수 없는 오류"가 있는 가상의 변칙 환자입니다.
#
# 실제 질환이 있는 환자를 변칙으로 분류하지 않습니다.
# ============================================================

PATIENTS = [

    {
        "id": 1,

        "name": "환자 A",

        "age": 54,

        "image": "images/patient01.png",

        "symptom": "갑자기 시작된 심한 두통",

        "consciousness": "명료",

        "exam": "신경학적 평가 및 영상검사 예정",

        "record":
            "접수 번호 N-2104 / 환자 팔찌 N-2104",

        "action": "진료실 입장",

        "anomaly": False,

        "answer_explanation":
            "접수 기록과 환자 정보에 변칙적인 오류가 없습니다. "
            "증상이 있으므로 의료진의 평가를 받을 수 있도록 진료실로 보내야 합니다.",

        "medical":
            "갑작스러운 심한 두통은 여러 원인과 관련될 수 있으므로 의료진의 평가가 필요합니다. "
            "이 게임에서는 질환을 직접 진단하지 않고, 적절한 진료 과정으로 연결하는 것을 학습합니다."
    },


    {
        "id": 2,

        "name": "환자 B",

        "age": 38,

        "image": "images/patient02.png",

        "symptom": "두통과 어지럼증",

        "consciousness": "명료",

        "exam": "추가 문진 필요",

        "record":
            "접수 번호 N-3817 / 환자 팔찌 N-3187",

        "action": "변칙 차단",

        "anomaly": True,

        "answer_explanation":
            "접수 기록의 번호는 N-3817인데 환자 팔찌에는 N-3187이 적혀 있습니다. "
            "환자 확인 정보가 일치하지 않는 변칙 기록입니다.",

        "medical":
            "실제 의료기관에서도 환자 확인은 매우 중요합니다. "
            "이름이나 등록번호 같은 정보를 확인하는 과정은 환자 안전과 연결됩니다."
    },


    {
        "id": 3,

        "name": "환자 C",

        "age": 17,

        "image": "images/patient03.png",

        "symptom": "반복되는 두통",

        "consciousness": "명료",

        "exam": "초기 문진 정보 부족",

        "record":
            "통증 위치와 발생 시간에 대한 정보가 기록되지 않음",

        "action": "추가 검사",

        "anomaly": False,

        "answer_explanation":
            "환자의 정보 자체에는 변칙이 없지만 증상에 대한 정보가 부족합니다. "
            "바로 분류하기보다 추가 확인이 필요합니다.",

        "medical":
            "환자 평가에서는 증상이 언제 시작됐는지, 어디가 아픈지, 얼마나 지속되는지 등 "
            "구체적인 정보를 확인하는 과정이 중요합니다."
    },


    {
        "id": 4,

        "name": "환자 D",

        "age": 63,

        "image": "images/patient04.png",

        "symptom": "보행이 불편하고 두통이 있음",

        "consciousness": "명료",

        "exam": "뇌 영상검사 자료 제출",

        "record":
            "기록 작성일: 2049년 11월 41일",

        "action": "변칙 차단",

        "anomaly": True,

        "answer_explanation":
            "기록 날짜가 존재할 수 없는 날짜인 '11월 41일'로 적혀 있습니다. "
            "의료 기록 자체에 변칙이 있습니다.",

        "medical":
            "실제 의료 기록에서는 날짜, 환자 정보, 검사 결과가 정확하게 기록되어야 합니다. "
            "기록 오류는 다른 환자의 자료와 혼동되는 문제를 만들 수 있습니다."
    },


    {
        "id": 5,

        "name": "환자 E",

        "age": 72,

        "image": "images/patient05.png",

        "symptom": "최근 기억력이 저하된 것 같다고 호소",

        "consciousness": "명료",

        "exam": "신경인지 평가 예정",

        "record":
            "접수 정보 및 환자 팔찌 일치",

        "action": "진료실 입장",

        "anomaly": False,

        "answer_explanation":
            "기록에서 이상한 점은 발견되지 않았습니다. "
            "증상에 대한 적절한 평가가 필요하므로 진료실로 안내합니다.",

        "medical":
            "기억력 변화에는 여러 원인이 있을 수 있습니다. "
            "실제 의료에서는 문진과 인지기능 평가 등을 통해 원인을 확인합니다."
    },


    {
        "id": 6,

        "name": "환자 F",

        "age": 45,

        "image": "images/patient06.png",

        "symptom": "팔의 감각이 평소와 다름",

        "consciousness": "명료",

        "exam": "신경학적 검사 필요",

        "record":
            "접수 시간 02:21 / 퇴원 시간 01:43",

        "action": "변칙 차단",

        "anomaly": True,

        "answer_explanation":
            "접수하기도 전에 퇴원한 것으로 기록되어 있어 시간 순서가 맞지 않습니다.",

        "medical":
            "의료 기록에서는 검사, 처치, 입퇴원 과정의 시간 순서가 정확해야 합니다. "
            "기록의 시간 정보도 중요한 확인 요소입니다."
    },


    {
        "id": 7,

        "name": "환자 G",

        "age": 28,

        "image": "images/patient07.png",

        "symptom": "목 부위 불편감과 손 저림",

        "consciousness": "명료",

        "exam": "증상 범위 확인 필요",

        "record":
            "손 저림이 어느 손에서 나타나는지 기록되지 않음",

        "action": "추가 검사",

        "anomaly": False,

        "answer_explanation":
            "기록에 변칙적인 오류는 없지만 어느 쪽 손에 증상이 있는지 등 "
            "판단에 필요한 정보가 부족합니다.",

        "medical":
            "신경계 증상을 평가할 때는 어느 부위에 증상이 나타나는지, "
            "한쪽인지 양쪽인지 등을 확인하는 과정이 중요합니다."
    },


    {
        "id": 8,

        "name": "환자 H",

        "age": 31,

        "image": "images/patient08.png",

        "symptom": "지속적인 어지럼증",

        "consciousness": "명료",

        "exam": "진료 대기",

        "record":
            "환자 사진 파일명: patient_H / 기록상 사진 파일명: patient_Q",

        "action": "변칙 차단",

        "anomaly": True,

        "answer_explanation":
            "환자 사진과 기록에 연결된 사진 파일명이 서로 다릅니다. "
            "다른 환자의 기록일 가능성이 있는 변칙입니다.",

        "medical":
            "검사 영상이나 환자 사진을 다른 환자의 기록과 잘못 연결하면 "
            "심각한 오류가 발생할 수 있어 정확한 환자 확인이 중요합니다."
    },


    {
        "id": 9,

        "name": "환자 I",

        "age": 14,

        "image": "images/patient09.png",

        "symptom": "운동 후 일시적인 두통",

        "consciousness": "명료",

        "exam": "보호자와 함께 방문",

        "record":
            "기본 정보 정상 / 추가 문진 예정",

        "action": "진료실 입장",

        "anomaly": False,

        "answer_explanation":
            "기록에서 변칙은 발견되지 않았습니다. "
            "증상에 대해 의료진이 평가할 수 있도록 진료실로 안내합니다.",

        "medical":
            "같은 두통이라도 발생 상황과 지속 시간 등 여러 정보를 함께 확인해야 합니다."
    },


    {
        "id": 10,

        "name": "환자 J",

        "age": 59,

        "image": "images/patient10.png",

        "symptom": "최근 균형을 잡기 어렵다고 느낌",

        "consciousness": "명료",

        "exam": "신경학적 평가 예정",

        "record":
            "나이: 59세 / 출생연도: 2019년",

        "action": "변칙 차단",

        "anomaly": True,

        "answer_explanation":
            "현재 나이와 출생연도가 서로 맞지 않습니다. "
            "환자 기본 정보가 논리적으로 일치하지 않는 변칙입니다.",

        "medical":
            "환자의 나이, 생년월일 같은 기본 정보는 검사 결과와 진료 기록을 "
            "정확한 사람에게 연결하기 위해 반드시 확인해야 합니다."
    }

]


# ============================================================
# 4. 게임 상태 초기화 함수
# ============================================================

def initialize_game():

    patient_order = list(
        range(len(PATIENTS))
    )

    # 게임을 시작할 때 환자 순서를 랜덤으로 섞음
    random.shuffle(patient_order)

    st.session_state.patient_order = patient_order

    st.session_state.current_case = 0

    st.session_state.score = 0

    st.session_state.lives = 3

    st.session_state.answered = False

    st.session_state.last_choice = None

    st.session_state.game_started = True

    st.session_state.game_over = False


# ============================================================
# 5. 다음 환자로 이동하는 함수
# ============================================================

def next_patient():

    st.session_state.current_case += 1

    st.session_state.answered = False

    st.session_state.last_choice = None

    # 모든 환자를 확인했거나 기회를 모두 사용한 경우
    if (
        st.session_state.current_case
        >= len(st.session_state.patient_order)
        or st.session_state.lives <= 0
    ):

        st.session_state.game_over = True


# ============================================================
# 6. 사용자 선택 확인 함수
# ============================================================

def check_answer(choice, patient):

    # 이미 답을 선택했다면 중복 처리하지 않음
    if st.session_state.answered:
        return

    st.session_state.last_choice = choice

    st.session_state.answered = True


    # 정답
    if choice == patient["action"]:

        if choice == "변칙 차단":
            st.session_state.score += 150

        elif choice == "추가 검사":
            st.session_state.score += 120

        else:
            st.session_state.score += 100


    # 오답
    else:

        st.session_state.lives -= 1


# ============================================================
# 7. 상단 게임 제목
# ============================================================

st.markdown(
    '<div class="game-label">NIGHT SHIFT · NEUROLOGY UNIT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-title">🏥 NEURO CHECK-IN</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-subtitle">야간 신경계 환자 접수실</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="warning-line"></div>',
    unsafe_allow_html=True
)


# ============================================================
# 8. 처음 실행할 때 Session State 준비
# ============================================================

if "game_started" not in st.session_state:

    st.session_state.game_started = False


if "game_over" not in st.session_state:

    st.session_state.game_over = False


# ============================================================
# 9. 게임 시작 화면
# ============================================================

if not st.session_state.game_started:

    st.markdown(
        """
<div class="intro-box">

<b>📋 야간 근무 지침</b><br><br>

당신은 오늘 밤 신경계 진료 병동의 접수 담당자입니다.

그런데 현재 병원 전산 시스템에서
<b>정체를 알 수 없는 기록 오류</b>가 발견되고 있습니다.

환자의 사진, 접수 기록, 증상 정보를 자세히 확인하세요.

<br><br>

정상적으로 진료가 필요한 환자는
<b>🏥 진료실로 안내</b>하고,

정보가 부족한 환자는
<b>🔍 추가 검사</b>를 선택하세요.

접수 기록에 존재할 수 없는 오류가 발견된다면
<b>🚨 변칙 차단</b>을 선택해야 합니다.

</div>
""",
        unsafe_allow_html=True
    )


    st.markdown(
        """
<div class="rule-box">

<b>⚠️ 중요 규칙</b><br><br>

• 실제 질환이나 장애는 '변칙'이 아닙니다.<br>

• 변칙은 환자의 <b>기록, 번호, 날짜, 시간 등의 비정상적인 오류</b>를 의미합니다.<br>

• 환자의 증상만 보고 질병을 직접 진단하지 마세요.<br>

• 총 10명의 환자를 안전하게 분류하면 근무가 종료됩니다.<br>

• 잘못 분류할 수 있는 기회는 총 3번입니다.

</div>
""",
        unsafe_allow_html=True
    )


    st.markdown("")

    if st.button(
        "🌙 야간 근무 시작",
        use_container_width=True
    ):

        initialize_game()

        st.rerun()


# ============================================================
# 10. 게임 진행 화면
# ============================================================

elif (
    st.session_state.game_started
    and not st.session_state.game_over
):

    # 현재 환자 불러오기
    patient_index = st.session_state.patient_order[
        st.session_state.current_case
    ]

    patient = PATIENTS[
        patient_index
    ]


    # --------------------------------------------------------
    # 상태 표시
    # --------------------------------------------------------

    s1, s2, s3 = st.columns(3)


    with s1:

        st.markdown(
            f"""
<div class="status-box">

CASE<br>
{st.session_state.current_case + 1} / {len(PATIENTS)}

</div>
""",
            unsafe_allow_html=True
        )


    with s2:

        st.markdown(
            f"""
<div class="status-box">

SCORE<br>
{st.session_state.score}

</div>
""",
            unsafe_allow_html=True
        )


    with s3:

        hearts = "❤️" * st.session_state.lives

        st.markdown(
            f"""
<div class="status-box">

남은 기회<br>
{hearts}

</div>
""",
            unsafe_allow_html=True
        )


    st.markdown("")


    # --------------------------------------------------------
    # 환자 정보 영역
    # --------------------------------------------------------

    image_col, info_col = st.columns(
        [1, 1.15]
    )


    # --------------------------------------------------------
    # 환자 이미지
    # --------------------------------------------------------

    with image_col:

        image_path = Path(
            patient["image"]
        )


        # 이미지가 실제로 존재하면 보여 줌
        if image_path.exists():

            st.image(
                str(image_path),
                use_container_width=True
            )


        # 아직 이미지가 없으면 임시 환자 아이콘 표시
        else:

            st.markdown(
                """
<div class="image-placeholder">

👤

</div>
""",
                unsafe_allow_html=True
            )

            st.caption(
                "환자 이미지 준비 중"
            )


    # --------------------------------------------------------
    # 환자 기록
    # --------------------------------------------------------

    with info_col:

        st.markdown(
            f"""
<div class="patient-card">

<div class="case-number">
PATIENT FILE · #{patient["id"]:02d}
</div>

<div class="patient-name">
{patient["name"]}
</div>

<div class="patient-info">

<b>나이</b><br>
{patient["age"]}세

<br><br>

<b>주호소</b><br>
{patient["symptom"]}

<br><br>

<b>의식 상태</b><br>
{patient["consciousness"]}

<br><br>

<b>예정 검사 / 평가</b><br>
{patient["exam"]}

</div>

<div class="record-box">

<b>📁 접수 기록</b><br><br>

{patient["record"]}

</div>

</div>
""",
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # 사용자가 아직 답하지 않은 경우
    # --------------------------------------------------------

    if not st.session_state.answered:

        st.markdown("### 🔎 이 환자를 어떻게 처리하시겠습니까?")


        b1, b2, b3 = st.columns(3)


        with b1:

            if st.button(
                "🏥 진료실 입장",
                use_container_width=True
            ):

                check_answer(
                    "진료실 입장",
                    patient
                )

                st.rerun()


        with b2:

            if st.button(
                "🔍 추가 검사",
                use_container_width=True
            ):

                check_answer(
                    "추가 검사",
                    patient
                )

                st.rerun()


        with b3:

            if st.button(
                "🚨 변칙 차단",
                use_container_width=True
            ):

                check_answer(
                    "변칙 차단",
                    patient
                )

                st.rerun()


    # --------------------------------------------------------
    # 사용자가 답을 선택한 후
    # --------------------------------------------------------

    else:

        correct = (
            st.session_state.last_choice
            == patient["action"]
        )


        # 정답
        if correct:

            st.markdown(
                f"""
<div class="correct-box">

<b>✅ 판단 성공</b><br><br>

선택한 처리:
<b>{st.session_state.last_choice}</b>

<br><br>

{patient["answer_explanation"]}

</div>
""",
                unsafe_allow_html=True
            )


        # 오답
        else:

            st.markdown(
                f"""
<div class="wrong-box">

<b>❌ 판단 실패</b><br><br>

선택한 처리:
<b>{st.session_state.last_choice}</b>

<br><br>

올바른 처리:
<b>{patient["action"]}</b>

<br><br>

{patient["answer_explanation"]}

</div>
""",
                unsafe_allow_html=True
            )


        # 의료 학습 설명
        st.markdown(
            f"""
<div class="medical-box">

<b>🧠 MEDICAL NOTE</b><br><br>

{patient["medical"]}

</div>
""",
            unsafe_allow_html=True
        )


        st.markdown("")


        if st.button(
            "다음 환자 →",
            use_container_width=True
        ):

            next_patient()

            st.rerun()


# ============================================================
# 11. 게임 종료 화면
# ============================================================

elif st.session_state.game_over:

    st.markdown("## 🌅 야간 근무 종료")


    score = st.session_state.score


    # 점수에 따른 결과
    if score >= 1100:

        grade = "S"

        message = (
            "뛰어난 관찰력으로 대부분의 환자를 정확하게 분류했습니다."
        )


    elif score >= 800:

        grade = "A"

        message = (
            "환자 정보와 기록을 꼼꼼하게 확인했습니다."
        )


    elif score >= 500:

        grade = "B"

        message = (
            "몇 가지 기록을 놓쳤지만 근무를 무사히 마쳤습니다."
        )


    else:

        grade = "C"

        message = (
            "환자 기록을 조금 더 세심하게 관찰할 필요가 있습니다."
        )


    st.markdown(
        f"""
<div class="patient-card" style="text-align:center;">

<div class="case-number">
NIGHT SHIFT REPORT
</div>

<div style="
font-size:70px;
font-weight:900;
color:#315e6b;
margin-top:15px;
">
{grade}
</div>

<div style="
font-size:25px;
font-weight:900;
margin-bottom:20px;
">
최종 점수 {score}
</div>

<div style="
line-height:1.8;
color:#52656d;
">
{message}
</div>

</div>
""",
        unsafe_allow_html=True
    )


    st.markdown(
        """
<div class="medical-box">

<b>📚 오늘의 근무에서 배운 점</b><br><br>

환자 분류에서는 단순히 증상만 보는 것이 아니라,
환자의 기본 정보와 기록이 서로 일치하는지 확인하는 과정도 중요합니다.

또한 실제 질환이 있다는 이유로 환자를 '비정상'으로 판단해서는 안 되며,
증상이 있는 환자는 의료진의 적절한 평가로 연결해야 합니다.

</div>
""",
        unsafe_allow_html=True
    )


    st.markdown("")


    if st.button(
        "🔄 다시 근무하기",
        use_container_width=True
    ):

        initialize_game()

        st.rerun()


# ============================================================
# 12. Footer
# ============================================================

st.markdown(
    """
<div class="footer">

NEURO CHECK-IN · EDUCATIONAL HOSPITAL GAME<br><br>

의학적 진단을 위한 프로그램이 아닌 교육용 게임입니다.

</div>
""",
    unsafe_allow_html=True
)

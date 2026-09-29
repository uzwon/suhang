import streamlit as st
import random
from pathlib import Path


# =========================================================
# 1. 페이지 설정
# =========================================================

st.set_page_config(
    page_title="NEURO NIGHT SHIFT",
    page_icon="🏥",
    layout="wide"
)


# =========================================================
# 2. CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top, #1c2833 0%, #0d141b 70%);
    color: white;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.game-title {
    text-align:center;
    font-size:48px;
    font-weight:900;
    color:#f4f7f8;
    letter-spacing:2px;
}

.game-subtitle {
    text-align:center;
    color:#8ba5b3;
    margin-bottom:25px;
}

.top-status {
    background:#17222c;
    border:1px solid #334653;
    border-radius:14px;
    padding:15px;
    text-align:center;
    color:#eef5f7;
}

.location-box {
    background:#eaf3f5;
    color:#263c46;
    border-radius:16px;
    padding:18px;
    margin:18px 0;
    border-left:6px solid #6897a7;
}

.patient-box {
    background:#f5f7f8;
    color:#23343c;
    border-radius:18px;
    padding:22px;
    border:1px solid #a5bbc4;
    min-height:350px;
}

.record-box {
    background:#fff7dd;
    color:#544c32;
    border-left:5px solid #d9b84f;
    padding:18px;
    border-radius:12px;
    margin-top:15px;
    line-height:1.8;
}

.success-box {
    background:#e9f7ef;
    color:#28513b;
    border-left:6px solid #60a87d;
    padding:18px;
    border-radius:12px;
    margin-top:15px;
}

.danger-box {
    background:#fae9ec;
    color:#643840;
    border-left:6px solid #c25c69;
    padding:18px;
    border-radius:12px;
    margin-top:15px;
}

.info-box {
    background:#eaf1fb;
    color:#30495e;
    border-left:6px solid #658ab5;
    padding:18px;
    border-radius:12px;
    margin-top:15px;
}

.inventory-box {
    background:#202e39;
    border:1px solid #405767;
    border-radius:14px;
    padding:15px;
    color:#f5f6f7;
}

.room-card {
    background:#17242e;
    border:1px solid #334b59;
    border-radius:14px;
    padding:16px;
    color:#e8f0f2;
    text-align:center;
    min-height:100px;
}

.stButton > button {
    width:100%;
    min-height:48px;
    border-radius:10px;
    font-weight:800;
}

hr {
    border-color:#334550;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. 이미지 경로
# =========================================================

IMAGE_FOLDER = Path("images")


# =========================================================
# 4. 환자 데이터
# =========================================================

PATIENTS = [

    {
        "id": 1,
        "name": "환자 A",
        "age": 19,
        "image": "patient01.png",

        "symptom": "두통과 어지럼증을 호소함",

        "record":
            "접수번호 N-1204 / 환자 팔찌 N-1204",

        "correct_action": "admit",

        "required_item": "신경학적 검사 키트",

        "reason":
            "접수 기록과 환자 확인 정보가 정상적으로 일치합니다.",

        "medical_note":
            "두통과 어지럼증은 여러 원인과 관련될 수 있으므로 "
            "증상만으로 판단하지 않고 의료진의 평가가 필요합니다."
    },


    {
        "id": 2,
        "name": "환자 B",
        "age": 46,
        "image": "patient02.png",

        "symptom": "손끝 감각이 평소와 다르다고 호소함",

        "record":
            "접수번호 N-3817 / 환자 팔찌 N-3187",

        "correct_action": "block",

        "required_item": None,

        "reason":
            "접수번호와 환자 팔찌 번호가 서로 다릅니다. "
            "기록상 변칙이 발견되었습니다.",

        "medical_note":
            "실제 의료기관에서도 환자 확인 정보가 정확히 일치하는지 "
            "확인하는 과정은 환자 안전과 관련됩니다."
    },


    {
        "id": 3,
        "name": "환자 C",
        "age": 17,
        "image": "patient03.png",

        "symptom": "반복되는 두통을 호소함",

        "record":
            "증상의 발생 시간과 위치가 기록되어 있지 않음",

        "correct_action": "check",

        "required_item": "문진 기록지",

        "extra_record":
            "추가 문진 결과: 두통 발생 시간과 위치가 확인되었으며 "
            "환자 확인 정보에는 이상이 없습니다.",

        "reason":
            "초기 기록만으로는 필요한 정보가 부족하므로 추가 확인이 필요합니다.",

        "medical_note":
            "신경계 증상을 평가할 때는 발생 시점, 위치, 지속 시간 등을 "
            "구체적으로 확인하는 과정이 중요합니다."
    },


    {
        "id": 4,
        "name": "환자 D",
        "age": 63,
        "image": "patient04.png",

        "symptom": "보행이 평소보다 불편하다고 호소함",

        "record":
            "검사 예정일: 2026년 11월 41일",

        "correct_action": "block",

        "required_item": None,

        "reason":
            "11월 41일은 존재하지 않는 날짜입니다. "
            "환자의 질환이 아니라 기록 자체에 변칙이 있습니다.",

        "medical_note":
            "의료 기록의 날짜와 시간은 정확해야 하며 "
            "기록 오류가 다른 환자 정보와의 혼동으로 이어질 수 있습니다."
    },


    {
        "id": 5,
        "name": "환자 E",
        "age": 72,
        "image": "patient05.png",

        "symptom": "최근 기억력 변화를 느낀다고 말함",

        "record":
            "환자 정보와 접수 기록이 모두 일치함",

        "correct_action": "admit",

        "required_item": "MRI 검사 안내서",

        "reason":
            "접수 기록에 변칙적인 오류가 없으므로 "
            "의료진의 평가를 받을 수 있도록 진료실로 안내합니다.",

        "medical_note":
            "기억력 변화는 다양한 원인과 관련될 수 있으며 "
            "실제 의료에서는 문진과 여러 검사를 통해 원인을 확인합니다."
    },


    {
        "id": 6,
        "name": "환자 F",
        "age": 31,
        "image": "patient06.png",

        "symptom": "지속적인 어지럼증을 호소함",

        "record":
            "접수 시간 02:21 / 퇴원 시간 01:43",

        "correct_action": "block",

        "required_item": None,

        "reason":
            "접수하기 전 이미 퇴원한 것으로 기록되어 있어 "
            "시간 순서가 논리적으로 맞지 않습니다.",

        "medical_note":
            "의료 기록에서는 검사, 처치, 입퇴원 과정의 시간 순서도 "
            "중요한 확인 요소입니다."
    },

]


# =========================================================
# 5. 게임 초기화
# =========================================================

def initialize_game():

    order = list(range(len(PATIENTS)))

    random.shuffle(order)

    st.session_state.started = True

    st.session_state.order = order

    st.session_state.case_number = 0

    st.session_state.location = "접수실"

    st.session_state.score = 0

    st.session_state.lives = 3

    st.session_state.inventory = []

    st.session_state.record_open = False

    st.session_state.patient_status = "reception"

    st.session_state.extra_checked = False

    st.session_state.result_message = ""

    st.session_state.game_over = False


# =========================================================
# 6. 현재 환자
# =========================================================

def get_current_patient():

    if st.session_state.case_number >= len(st.session_state.order):
        return None

    index = st.session_state.order[
        st.session_state.case_number
    ]

    return PATIENTS[index]


# =========================================================
# 7. 환자 이미지 표시
# =========================================================

def show_patient_image(patient):

    path = IMAGE_FOLDER / patient["image"]

    if path.exists():

        st.image(
            str(path),
            use_container_width=True
        )

    else:

        st.markdown(
            """
            <div style="
                height:360px;
                background:#d8e4e8;
                border-radius:18px;
                display:flex;
                justify-content:center;
                align-items:center;
                font-size:100px;
                color:#536a74;
            ">
                👤
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "이미지를 추가하면 여기에 환자 사진이 표시됩니다."
        )


# =========================================================
# 8. 환자 판단
# =========================================================

def judge_patient(action):

    patient = get_current_patient()

    correct = patient["correct_action"]


    if action == correct:

        if action == "block":

            st.session_state.score += 150

            st.session_state.patient_status = "completed"

            st.session_state.result_message = (
                "🚨 변칙 기록 발견! 올바르게 차단했습니다."
            )


        elif action == "check":

            st.session_state.score += 100

            st.session_state.patient_status = "need_record_room"

            st.session_state.result_message = (
                "🔍 추가 확인이 필요합니다. "
                "기록 확인실로 이동하세요."
            )


        elif action == "admit":

            st.session_state.score += 100

            st.session_state.patient_status = "treatment"

            st.session_state.result_message = (
                "🏥 정상 접수입니다. "
                "환자가 진료실로 이동했습니다."
            )


    else:

        st.session_state.lives -= 1

        st.session_state.result_message = (
            "❌ 판단이 올바르지 않습니다. "
            "기록을 다시 살펴보세요."
        )


        if st.session_state.lives <= 0:
            st.session_state.game_over = True


# =========================================================
# 9. 다음 환자
# =========================================================

def next_patient():

    st.session_state.case_number += 1

    st.session_state.location = "접수실"

    st.session_state.record_open = False

    st.session_state.patient_status = "reception"

    st.session_state.extra_checked = False

    st.session_state.result_message = ""

    st.session_state.inventory = []


    if st.session_state.case_number >= len(
        st.session_state.order
    ):

        st.session_state.game_over = True


# =========================================================
# 10. 위치 이동
# =========================================================

def move_to(room):

    st.session_state.location = room


# =========================================================
# 11. 물품 획득
# =========================================================

def get_supply(item):

    if item is None:

        st.warning(
            "현재 필요한 물품이 없습니다."
        )

        return


    if item in st.session_state.inventory:

        st.warning(
            "이미 가지고 있는 물품입니다."
        )

        return


    st.session_state.inventory.append(item)

    st.success(
        f"🎒 {item}을(를) 획득했습니다."
    )


# =========================================================
# 12. 진료 물품 적용
# =========================================================

def use_item():

    patient = get_current_patient()

    required_item = patient["required_item"]


    if required_item not in st.session_state.inventory:

        st.warning(
            f"📦 먼저 물품실에서 "
            f"'{required_item}'을(를) 가져오세요."
        )

        return


    st.session_state.inventory.remove(
        required_item
    )

    st.session_state.score += 100

    st.session_state.patient_status = "completed"

    st.session_state.result_message = (
        f"✅ {required_item} 준비 완료! "
        "환자의 진료 준비가 끝났습니다."
    )


# =========================================================
# 13. 상태 초기 설정
# =========================================================

if "started" not in st.session_state:

    st.session_state.started = False


if "game_over" not in st.session_state:

    st.session_state.game_over = False


# =========================================================
# 14. 제목
# =========================================================

st.markdown(
    '<div class="game-title">🏥 NEURO NIGHT SHIFT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-subtitle">'
    '야간 신경계 병원 · 기록 변칙 탐지 게임'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 15. 시작 화면
# =========================================================

if not st.session_state.started:

    st.markdown(
        """
        <div class="patient-box">

        <h2>🌙 야간 근무 시작</h2>

        당신은 오늘 밤 신경계 병동의 접수 담당자입니다.

        병원 전산 시스템에서 원인을 알 수 없는
        <b>기록 변칙</b>이 발생하고 있습니다.

        환자의 사진과 기록을 확인하세요.

        정상적인 환자는 진료실로 보내고,
        정보가 부족하면 추가 확인을 진행하세요.

        기록에 존재할 수 없는 오류가 있다면
        변칙 환자의 접수를 차단해야 합니다.

        <br><br>

        <b>※ 실제 질환이 있다는 이유로 변칙 환자가 되는 것은 아닙니다.</b><br>
        변칙은 게임 속 기록이나 사진에 존재하는 가상의 오류입니다.

        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")


    if st.button(
        "🌙 야간 근무 시작",
        use_container_width=True
    ):

        initialize_game()

        st.rerun()


# =========================================================
# 16. 게임 종료
# =========================================================

elif st.session_state.game_over:

    score = st.session_state.score


    if score >= 750:
        grade = "S"

    elif score >= 550:
        grade = "A"

    elif score >= 350:
        grade = "B"

    else:
        grade = "C"


    st.markdown(
        f"""
        <div class="patient-box"
             style="text-align:center;">

        <h2>🌅 NIGHT SHIFT COMPLETE</h2>

        <div style="
            font-size:90px;
            font-weight:900;
            color:#497d91;
        ">
            {grade}
        </div>

        <h2>최종 점수 {score}</h2>

        야간 근무가 종료되었습니다.

        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")


    if st.button(
        "🔄 다시 근무하기",
        use_container_width=True
    ):

        initialize_game()

        st.rerun()


# =========================================================
# 17. 실제 게임
# =========================================================

else:

    patient = get_current_patient()


    # -----------------------------------------------------
    # 상태창
    # -----------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.markdown(
            f"""
            <div class="top-status">
            CASE<br>
            <b>
            {st.session_state.case_number + 1}
            /
            {len(PATIENTS)}
            </b>
            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
            <div class="top-status">
            SCORE<br>
            <b>{st.session_state.score}</b>
            </div>
            """,
            unsafe_allow_html=True
        )


    with c3:

        hearts = "❤️" * st.session_state.lives

        st.markdown(
            f"""
            <div class="top-status">
            남은 기회<br>
            {hearts}
            </div>
            """,
            unsafe_allow_html=True
        )


    with c4:

        st.markdown(
            f"""
            <div class="top-status">
            현재 위치<br>
            <b>{st.session_state.location}</b>
            </div>
            """,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # 병원 지도
    # -----------------------------------------------------

    st.markdown("### 🗺️ 병원 이동")


    r1, r2, r3, r4 = st.columns(4)


    with r1:

        if st.button(
            "🖥️ 접수실",
            use_container_width=True
        ):

            move_to("접수실")
            st.rerun()


    with r2:

        if st.button(
            "📁 기록 확인실",
            use_container_width=True
        ):

            move_to("기록 확인실")
            st.rerun()


    with r3:

        if st.button(
            "📦 물품실",
            use_container_width=True
        ):

            move_to("물품실")
            st.rerun()


    with r4:

        if st.button(
            "🛏️ 진료실",
            use_container_width=True
        ):

            move_to("진료실")
            st.rerun()


    # -----------------------------------------------------
    # 인벤토리
    # -----------------------------------------------------

    if st.session_state.inventory:

        items = " · ".join(
            st.session_state.inventory
        )

    else:

        items = "비어 있음"


    st.markdown(
        f"""
        <div class="inventory-box">
        🎒 <b>INVENTORY</b><br>
        {items}
        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # 접수실
    # =====================================================

    if st.session_state.location == "접수실":

        st.markdown(
            '<div class="location-box">'
            '🖥️ <b>현재 위치 : 접수실</b><br>'
            '환자의 사진과 접수 기록을 확인하세요.'
            '</div>',
            unsafe_allow_html=True
        )


        left, right = st.columns(
            [1, 1.2]
        )


        with left:

            show_patient_image(
                patient
            )


        with right:

            st.markdown(
                f"""
                <div class="patient-box">

                <b>PATIENT FILE #{patient["id"]:02d}</b>

                <h2>{patient["name"]}</h2>

                <b>나이</b><br>
                {patient["age"]}세

                <br><br>

                <b>주호소</b><br>
                {patient["symptom"]}

                </div>
                """,
                unsafe_allow_html=True
            )


        if st.session_state.patient_status == "reception":

            if st.button(
                "📋 접수 기록 확인",
                use_container_width=True
            ):

                st.session_state.record_open = True

                st.rerun()


            if st.session_state.record_open:

                st.markdown(
                    f"""
                    <div class="record-box">

                    <b>📁 접수 기록</b><br><br>

                    {patient["record"]}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.markdown(
                    "### 어떻게 처리하시겠습니까?"
                )


                b1, b2, b3 = st.columns(3)


                with b1:

                    if st.button(
                        "🏥 진료실 입장",
                        use_container_width=True
                    ):

                        judge_patient(
                            "admit"
                        )

                        st.rerun()


                with b2:

                    if st.button(
                        "🔍 추가 확인",
                        use_container_width=True
                    ):

                        judge_patient(
                            "check"
                        )

                        st.rerun()


                with b3:

                    if st.button(
                        "🚨 변칙 차단",
                        use_container_width=True
                    ):

                        judge_patient(
                            "block"
                        )

                        st.rerun()


        # 변칙 차단 완료
        elif st.session_state.patient_status == "completed":

            st.markdown(
                f"""
                <div class="success-box">

                {st.session_state.result_message}

                <br><br>

                <b>판단 근거</b><br>
                {patient["reason"]}

                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <div class="info-box">

                <b>🧠 MEDICAL NOTE</b><br><br>

                {patient["medical_note"]}

                </div>
                """,
                unsafe_allow_html=True
            )


            if st.button(
                "다음 환자 접수 →",
                use_container_width=True
            ):

                next_patient()

                st.rerun()


        else:

            st.info(
                st.session_state.result_message
            )


    # =====================================================
    # 기록 확인실
    # =====================================================

    elif st.session_state.location == "기록 확인실":

        st.markdown(
            '<div class="location-box">'
            '📁 <b>현재 위치 : 기록 확인실</b><br>'
            '부족한 환자 기록을 추가로 확인할 수 있습니다.'
            '</div>',
            unsafe_allow_html=True
        )


        if (
            st.session_state.patient_status
            == "need_record_room"
        ):

            st.markdown(
                f"""
                <div class="patient-box">

                <h3>📂 {patient["name"]} 추가 기록</h3>

                현재 환자의 초기 기록에는
                필요한 정보가 부족합니다.

                </div>
                """,
                unsafe_allow_html=True
            )


            if st.button(
                "🔍 추가 기록 조회",
                use_container_width=True
            ):

                st.session_state.extra_checked = True

                st.session_state.score += 50


            if st.session_state.extra_checked:

                st.markdown(
                    f"""
                    <div class="record-box">

                    <b>추가 확인 결과</b><br><br>

                    {patient.get(
                        "extra_record",
                        "추가 기록이 확인되었습니다."
                    )}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                if st.button(
                    "🏥 진료실로 안내",
                    use_container_width=True
                ):

                    st.session_state.patient_status = (
                        "treatment"
                    )

                    st.session_state.result_message = (
                        "추가 확인이 끝났습니다. "
                        "이제 필요한 물품을 준비하세요."
                    )

                    move_to(
                        "물품실"
                    )

                    st.rerun()


        else:

            st.info(
                "현재 추가 확인이 필요한 환자가 없습니다."
            )


    # =====================================================
    # 물품실
    # =====================================================

    elif st.session_state.location == "물품실":

        st.markdown(
            '<div class="location-box">'
            '📦 <b>현재 위치 : 물품실</b><br>'
            '환자에게 필요한 물품을 직접 선택하세요.'
            '</div>',
            unsafe_allow_html=True
        )


        st.markdown("### 📦 물품 선반")


        item1, item2, item3 = st.columns(3)


        with item1:

            st.markdown(
                """
                <div class="room-card">
                🧠<br><br>
                신경학적 검사 키트
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "검사 키트 가져오기",
                use_container_width=True
            ):

                get_supply(
                    "신경학적 검사 키트"
                )


        with item2:

            st.markdown(
                """
                <div class="room-card">
                📄<br><br>
                MRI 검사 안내서
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "MRI 안내서 가져오기",
                use_container_width=True
            ):

                get_supply(
                    "MRI 검사 안내서"
                )


        with item3:

            st.markdown(
                """
                <div class="room-card">
                📝<br><br>
                문진 기록지
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "문진 기록지 가져오기",
                use_container_width=True
            ):

                get_supply(
                    "문진 기록지"
                )


        if (
            st.session_state.patient_status
            == "treatment"
        ):

            st.info(
                f"현재 환자에게 필요한 물품: "
                f"**{patient['required_item']}**"
            )


    # =====================================================
    # 진료실
    # =====================================================

    elif st.session_state.location == "진료실":

        st.markdown(
            '<div class="location-box">'
            '🛏️ <b>현재 위치 : 진료실</b><br>'
            '진료를 기다리는 환자에게 필요한 준비물을 전달하세요.'
            '</div>',
            unsafe_allow_html=True
        )


        if (
            st.session_state.patient_status
            == "treatment"
        ):

            left, right = st.columns(
                [1, 1.2]
            )


            with left:

                show_patient_image(
                    patient
                )


            with right:

                st.markdown(
                    f"""
                    <div class="patient-box">

                    <h2>🛏️ {patient["name"]}</h2>

                    환자가 진료를 기다리고 있습니다.

                    <br><br>

                    <b>필요한 준비물</b><br>

                    📦 {patient["required_item"]}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            if st.button(
                "🎒 가지고 있는 물품 전달",
                use_container_width=True
            ):

                use_item()

                st.rerun()


        elif (
            st.session_state.patient_status
            == "completed"
        ):

            st.markdown(
                f"""
                <div class="success-box">

                {st.session_state.result_message}

                <br><br>

                <b>판단 근거</b><br>
                {patient["reason"]}

                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <div class="info-box">

                <b>🧠 MEDICAL NOTE</b><br><br>

                {patient["medical_note"]}

                </div>
                """,
                unsafe_allow_html=True
            )


            if st.button(
                "다음 환자 접수 →",
                use_container_width=True
            ):

                next_patient()

                st.rerun()


        else:

            st.info(
                "현재 진료실에서 기다리는 환자가 없습니다."
            )

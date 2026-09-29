import streamlit as st
import random
from pathlib import Path


# =========================================================
# 1. 기본 설정
# =========================================================

st.set_page_config(
    page_title="NEURO NIGHT SHIFT",
    page_icon="🏥",
    layout="wide"
)

IMAGE_FOLDER = Path("images")


# =========================================================
# 2. 디자인
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        linear-gradient(
            180deg,
            #10171e 0%,
            #17232c 45%,
            #0c1217 100%
        );
    color: white;
}

.block-container {
    max-width: 1150px;
    padding-top: 1.4rem;
    padding-bottom: 4rem;
}

/* 게임 제목 */
.game-title {
    font-size: 38px;
    font-weight: 900;
    color: #f4f7f8;
    letter-spacing: 2px;
}

.game-subtitle {
    color: #8fa6b2;
    font-size: 14px;
}

/* 상태바 */
.status-card {
    background: #1b2832;
    border: 1px solid #354b59;
    border-radius: 13px;
    padding: 12px;
    text-align: center;
    color: #edf4f6;
}

/* 현재 장소 */
.location-box {
    background: #e9f2f4;
    color: #263c44;
    border-radius: 15px;
    border-left: 6px solid #6799a9;
    padding: 16px 20px;
    margin-top: 18px;
    margin-bottom: 20px;
}

/* 사진 카드 */
.photo-card {
    background: #dce8eb;
    border: 1px solid #8da7b1;
    border-radius: 18px;
    min-height: 430px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #526871;
    font-size: 100px;
}

/* 일반 카드 */
.panel {
    background: #f4f7f8;
    color: #253841;
    border-radius: 18px;
    padding: 22px;
    border: 1px solid #a3b8c1;
}

/* 검사 결과 */
.exam-box {
    background: #eaf1fa;
    color: #304b60;
    border-left: 6px solid #6588ad;
    border-radius: 12px;
    padding: 18px;
    margin-top: 15px;
    line-height: 1.8;
}

/* 정답 */
.success-box {
    background: #e7f6ed;
    color: #2f503c;
    border-left: 6px solid #5ba076;
    border-radius: 12px;
    padding: 18px;
    margin-top: 15px;
}

/* 실패 */
.danger-box {
    background: #f9e8eb;
    color: #64363e;
    border-left: 6px solid #bb5867;
    border-radius: 12px;
    padding: 18px;
    margin-top: 15px;
}

/* 물품 카드 */
.item-card {
    background: #f4f7f8;
    color: #293d46;
    border-radius: 15px;
    padding: 19px;
    border: 1px solid #a6b8c0;
    text-align: center;
    min-height: 120px;
}

/* 인벤토리 */
.inventory {
    background: #202e38;
    color: #eff4f5;
    border: 1px solid #405764;
    border-radius: 14px;
    padding: 14px 18px;
    margin-top: 12px;
}

/* 버튼 */
.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 10px;
    font-weight: 800;
}

/* 지도 */
.map-room {
    background: #edf3f4;
    color: #273a42;
    border-radius: 13px;
    border: 1px solid #a9bbc2;
    padding: 15px;
    text-align: center;
    margin-bottom: 6px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. 환자 데이터
# =========================================================
#
# anomaly:
#   True  = 얼굴 사진에 게임 속 가상의 변칙이 있음
#   False = 정상적인 환자
#
# admitted 환자만 진료실로 들어감
# =========================================================

PATIENTS = [

    {
        "id": 1,
        "image": "patient01.png",
        "anomaly": False,

        "exam_text":
            "환자는 두통과 어지럼증을 호소합니다. "
            "기본적인 신경학적 확인과 안정이 필요한 상태입니다.",

        "items": [
            "냉찜질 팩",
            "신경학적 검사 카드"
        ]
    },

    {
        "id": 2,
        "image": "patient02.png",
        "anomaly": True,

        "anomaly_reason":
            "얼굴 사진에서 눈의 위치가 비정상적으로 배열된 변칙이 발견되었습니다.",

        "exam_text": "",
        "items": []
    },

    {
        "id": 3,
        "image": "patient03.png",
        "anomaly": False,

        "exam_text":
            "환자는 최근 기억력 변화를 호소하고 있습니다. "
            "추가적인 인지 평가 준비가 필요합니다.",

        "items": [
            "인지검사 카드",
            "MRI 검사 안내서"
        ]
    },

    {
        "id": 4,
        "image": "patient04.png",
        "anomaly": True,

        "anomaly_reason":
            "얼굴 사진에서 좌우 얼굴 구조가 자연스럽지 않은 변칙이 발견되었습니다.",

        "exam_text": "",
        "items": []
    },

    {
        "id": 5,
        "image": "patient05.png",
        "anomaly": False,

        "exam_text":
            "환자는 손의 감각이 평소와 다르다고 호소합니다. "
            "신경계 상태 확인을 위한 기본 검사가 필요합니다.",

        "items": [
            "감각검사 카드",
            "반사검사 도구"
        ]
    },

    {
        "id": 6,
        "image": "patient06.png",
        "anomaly": True,

        "anomaly_reason":
            "사진 속 얼굴에 게임 설정상 존재할 수 없는 형태의 변칙이 나타납니다.",

        "exam_text": "",
        "items": []
    }
]


# =========================================================
# 4. 물품 목록
# =========================================================

ALL_ITEMS = [

    "냉찜질 팩",
    "신경학적 검사 카드",
    "인지검사 카드",
    "MRI 검사 안내서",
    "감각검사 카드",
    "반사검사 도구"
]


# =========================================================
# 5. 게임 초기화
# =========================================================

def initialize_game():

    order = list(range(len(PATIENTS)))

    random.shuffle(order)

    st.session_state.order = order

    st.session_state.patient_number = 0

    st.session_state.location = "데스크"

    st.session_state.score = 0

    st.session_state.lives = 3

    st.session_state.inventory = []

    st.session_state.started = True

    st.session_state.game_over = False

    st.session_state.patient_admitted = False

    st.session_state.examined = False

    st.session_state.completed = False

    st.session_state.message = ""


# =========================================================
# 6. 현재 환자
# =========================================================

def current_patient():

    if (
        st.session_state.patient_number
        >= len(st.session_state.order)
    ):
        return None

    patient_index = st.session_state.order[
        st.session_state.patient_number
    ]

    return PATIENTS[
        patient_index
    ]


# =========================================================
# 7. 이미지 표시
# =========================================================

def show_patient(patient):

    path = IMAGE_FOLDER / patient["image"]

    if path.exists():

        st.image(
            str(path),
            use_container_width=True
        )

    else:

        st.markdown(
            """
            <div class="photo-card">
            👤
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "images 폴더에 환자 사진을 넣으면 여기에 표시됩니다."
        )


# =========================================================
# 8. 장소 이동
# =========================================================

def move_room(room):

    st.session_state.location = room


# =========================================================
# 9. 새로운 환자
# =========================================================

def next_patient():

    st.session_state.patient_number += 1

    st.session_state.location = "데스크"

    st.session_state.inventory = []

    st.session_state.patient_admitted = False

    st.session_state.examined = False

    st.session_state.completed = False

    st.session_state.message = ""


    if (
        st.session_state.patient_number
        >= len(st.session_state.order)
    ):

        st.session_state.game_over = True


# =========================================================
# 10. 데스크 판단
# =========================================================

def desk_decision(choice):

    patient = current_patient()


    # --------------------------------------------
    # 병원 안으로 들임
    # --------------------------------------------

    if choice == "admit":

        if patient["anomaly"]:

            st.session_state.lives -= 1

            st.session_state.message = (
                "❌ 변칙 환자를 병원 안으로 들였습니다."
            )


            if st.session_state.lives <= 0:

                st.session_state.game_over = True


        else:

            st.session_state.score += 100

            st.session_state.patient_admitted = True

            st.session_state.location = "진료실"

            st.session_state.message = (
                "✅ 정상 환자입니다. "
                "환자가 진료실로 이동했습니다."
            )


    # --------------------------------------------
    # 출입 거부
    # --------------------------------------------

    elif choice == "block":

        if patient["anomaly"]:

            st.session_state.score += 150

            st.session_state.completed = True

            st.session_state.message = (
                "🚨 변칙 발견! "
                "병원 출입을 차단했습니다."
            )


        else:

            st.session_state.lives -= 1

            st.session_state.message = (
                "❌ 정상 환자의 출입을 막았습니다."
            )


            if st.session_state.lives <= 0:

                st.session_state.game_over = True


# =========================================================
# 11. 검사
# =========================================================

def examine_patient():

    st.session_state.examined = True

    st.session_state.score += 50

    st.session_state.message = (
        "🔍 검사가 완료되었습니다."
    )


# =========================================================
# 12. 물품 가져오기
# =========================================================

def add_item(item):

    if item not in st.session_state.inventory:

        # 최대 4개까지만 들 수 있음
        if len(st.session_state.inventory) >= 4:

            st.warning(
                "가방이 가득 찼습니다. 최대 4개까지 들 수 있습니다."
            )

            return


        st.session_state.inventory.append(
            item
        )

        st.success(
            f"🎒 {item}을(를) 인벤토리에 넣었습니다."
        )


    else:

        st.warning(
            "이미 가지고 있는 물품입니다."
        )


# =========================================================
# 13. 인벤토리에서 물품 적용
# =========================================================

def apply_items(selected_items):

    patient = current_patient()

    required = set(
        patient["items"]
    )

    selected = set(
        selected_items
    )


    if len(selected_items) != 2:

        st.warning(
            "치료에 사용할 물품 2개를 선택하세요."
        )

        return


    if selected == required:

        st.session_state.score += 200

        st.session_state.completed = True

        st.session_state.message = (
            "✅ 필요한 물품을 정확하게 적용했습니다. "
            "환자 진료가 완료되었습니다."
        )


    else:

        st.session_state.lives -= 1

        st.session_state.message = (
            "❌ 필요한 물품 조합이 아닙니다."
        )


        if st.session_state.lives <= 0:

            st.session_state.game_over = True


# =========================================================
# 14. Session State
# =========================================================

if "started" not in st.session_state:

    st.session_state.started = False


if "game_over" not in st.session_state:

    st.session_state.game_over = False


# =========================================================
# 15. 제목
# =========================================================

left_title, right_title = st.columns(
    [4, 1]
)


with left_title:

    st.markdown(
        """
        <div class="game-title">
        🏥 NEURO NIGHT SHIFT
        </div>

        <div class="game-subtitle">
        당신은 야간 근무를 맡은 의사입니다.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 16. 시작 화면
# =========================================================

if not st.session_state.started:

    st.markdown(
        """
        <div class="panel">

        <h2>🌙 오늘 밤, 당신은 당직 의사입니다.</h2>

        병원에 낯선 환자들이 찾아오기 시작했습니다.

        <br><br>

        데스크에서 환자의 <b>얼굴을 자세히 확인</b>하고
        병원 안으로 들일지 판단하세요.

        <br><br>

        정상 환자는 진료실에서 검사하고,
        필요한 물품을 직접 준비하여 적용해야 합니다.

        <br><br>

        그러나 얼굴에 이상한 변칙이 있는 환자를
        병원 안으로 들여서는 안 됩니다.

        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")


    if st.button(
        "🌙 당직 시작",
        use_container_width=True
    ):

        initialize_game()

        st.rerun()


# =========================================================
# 17. 게임 종료
# =========================================================

elif st.session_state.game_over:

    score = st.session_state.score


    if score >= 900:
        grade = "S"

    elif score >= 650:
        grade = "A"

    elif score >= 400:
        grade = "B"

    else:
        grade = "C"


    st.markdown(
        f"""
        <div class="panel"
        style="text-align:center;">

        <h2>🌅 당직 종료</h2>

        <div style="
        font-size:85px;
        font-weight:900;
        color:#527e91;
        ">
        {grade}
        </div>

        <h2>최종 점수 : {score}</h2>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "🔄 다시 시작",
        use_container_width=True
    ):

        initialize_game()

        st.rerun()


# =========================================================
# 18. 게임 플레이
# =========================================================

else:

    patient = current_patient()


    # =====================================================
    # 상단 상태바
    # =====================================================

    s1, s2, s3, s4 = st.columns(
        [1, 1, 1, 1]
    )


    with s1:

        st.markdown(
            f"""
            <div class="status-card">
            PATIENT<br>
            <b>
            {st.session_state.patient_number + 1}
            /
            {len(PATIENTS)}
            </b>
            </div>
            """,
            unsafe_allow_html=True
        )


    with s2:

        st.markdown(
            f"""
            <div class="status-card">
            SCORE<br>
            <b>{st.session_state.score}</b>
            </div>
            """,
            unsafe_allow_html=True
        )


    with s3:

        hearts = "❤️" * st.session_state.lives

        st.markdown(
            f"""
            <div class="status-card">
            LIFE<br>
            {hearts}
            </div>
            """,
            unsafe_allow_html=True
        )


    with s4:

        # ---------------------------------------------
        # 지도 버튼
        # ---------------------------------------------

        with st.popover(
            "🗺️ 병원 지도",
            use_container_width=True
        ):

            st.markdown("### 🏥 병원 내부 지도")

            st.markdown(
                """
                <div class="map-room">
                🖥️ 데스크
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "데스크로 이동",
                key="map_desk"
            ):

                move_room("데스크")
                st.rerun()


            st.markdown("↓")


            c1, c2 = st.columns(2)


            with c1:

                st.markdown(
                    """
                    <div class="map-room">
                    🛏️ 진료실
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "진료실로 이동",
                    key="map_treatment"
                ):

                    move_room("진료실")
                    st.rerun()


            with c2:

                st.markdown(
                    """
                    <div class="map-room">
                    📦 물품실
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "물품실로 이동",
                    key="map_supply"
                ):

                    move_room("물품실")
                    st.rerun()


    # =====================================================
    # 현재 위치
    # =====================================================

    st.markdown(
        f"""
        <div class="location-box">

        📍 현재 위치 :
        <b>{st.session_state.location}</b>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # 인벤토리
    # =====================================================

    inventory_text = (
        " · ".join(
            st.session_state.inventory
        )
        if st.session_state.inventory
        else "비어 있음"
    )


    st.markdown(
        f"""
        <div class="inventory">

        🎒 <b>INVENTORY</b>
        &nbsp;&nbsp; {inventory_text}

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # 메시지
    # =====================================================

    if st.session_state.message:

        st.info(
            st.session_state.message
        )


    # =====================================================
    # 🖥️ 데스크
    # =====================================================

    if st.session_state.location == "데스크":

        st.markdown("## 🖥️ 병원 데스크")

        st.caption(
            "환자의 얼굴만 보고 병원 안으로 들일지 판단하세요."
        )


        show_patient(
            patient
        )


        # -------------------------------------------------
        # 아직 판단 전
        # -------------------------------------------------

        if (
            not st.session_state.patient_admitted
            and not st.session_state.completed
        ):

            st.write("")

            b1, b2 = st.columns(2)


            with b1:

                if st.button(
                    "🏥 병원 안으로 들인다",
                    use_container_width=True
                ):

                    desk_decision(
                        "admit"
                    )

                    st.rerun()


            with b2:

                if st.button(
                    "🚨 출입을 막는다",
                    use_container_width=True
                ):

                    desk_decision(
                        "block"
                    )

                    st.rerun()


        # -------------------------------------------------
        # 변칙 처리 완료
        # -------------------------------------------------

        if (
            st.session_state.completed
            and patient["anomaly"]
        ):

            st.markdown(
                f"""
                <div class="success-box">

                <b>🚨 변칙 환자 차단 완료</b><br><br>

                {patient.get(
                    "anomaly_reason",
                    "사진 속 변칙을 발견했습니다."
                )}

                </div>
                """,
                unsafe_allow_html=True
            )


            if st.button(
                "다음 환자 →",
                use_container_width=True
            ):

                next_patient()
                st.rerun()


    # =====================================================
    # 🛏️ 진료실
    # =====================================================

    elif st.session_state.location == "진료실":

        st.markdown("## 🛏️ 진료실")


        if not st.session_state.patient_admitted:

            st.warning(
                "현재 진료실에 들어온 환자가 없습니다."
            )


        else:

            left, right = st.columns(
                [1, 1.1]
            )


            with left:

                show_patient(
                    patient
                )


            with right:

                st.markdown(
                    f"""
                    <div class="panel">

                    <h3>👤 환자 #{patient["id"]:02d}</h3>

                    환자가 진료실에서 기다리고 있습니다.

                    <br><br>

                    먼저 환자를 검사해 필요한 물품을 확인하세요.

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # -------------------------------------------------
            # 검사 전
            # -------------------------------------------------

            if not st.session_state.examined:

                if st.button(
                    "🔍 환자 검사",
                    use_container_width=True
                ):

                    examine_patient()

                    st.rerun()


            # -------------------------------------------------
            # 검사 완료
            # -------------------------------------------------

            else:

                item1 = patient["items"][0]
                item2 = patient["items"][1]


                st.markdown(
                    f"""
                    <div class="exam-box">

                    <b>🔍 검사 결과</b><br><br>

                    {patient["exam_text"]}

                    <br><br>

                    <b>필요한 물품</b><br><br>

                    ① {item1}<br>
                    ② {item2}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # ---------------------------------------------
                # 이미 진료 완료
                # ---------------------------------------------

                if st.session_state.completed:

                    st.markdown(
                        """
                        <div class="success-box">

                        ✅ 환자 진료가 완료되었습니다.

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    if st.button(
                        "다음 환자 →",
                        use_container_width=True
                    ):

                        next_patient()

                        st.rerun()


                # ---------------------------------------------
                # 치료 전
                # ---------------------------------------------

                else:

                    if not st.session_state.inventory:

                        st.warning(
                            "🎒 인벤토리가 비어 있습니다. "
                            "지도에서 물품실로 이동하세요."
                        )


                    else:

                        st.markdown(
                            "### 🎒 환자에게 적용할 물품 선택"
                        )


                        selected_items = st.multiselect(
                            "인벤토리에서 2개를 선택하세요.",
                            options=st.session_state.inventory,
                            max_selections=2
                        )


                        if st.button(
                            "🩺 선택한 물품 적용",
                            use_container_width=True
                        ):

                            apply_items(
                                selected_items
                            )

                            st.rerun()


    # =====================================================
    # 📦 물품실
    # =====================================================

    elif st.session_state.location == "물품실":

        st.markdown("## 📦 치료 물품실")

        st.caption(
            "필요하다고 생각하는 물품을 인벤토리에 담으세요."
        )


        # 3개씩 표시
        rows = [
            ALL_ITEMS[i:i + 3]
            for i in range(
                0,
                len(ALL_ITEMS),
                3
            )
        ]


        for row_index, row in enumerate(rows):

            columns = st.columns(
                len(row)
            )


            for index, item in enumerate(row):

                with columns[index]:

                    st.markdown(
                        f"""
                        <div class="item-card">

                        <div style="font-size:32px;">
                        🧰
                        </div>

                        <br>

                        <b>{item}</b>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    if st.button(
                        "🎒 가져가기",
                        key=f"item_{row_index}_{index}",
                        use_container_width=True
                    ):

                        add_item(
                            item
                        )

                        st.rerun()

import streamlit as st
import random
from pathlib import Path


# ============================================================
# 1. 기본 설정
# ============================================================

st.set_page_config(
    page_title="NEURO NIGHT SHIFT",
    page_icon="🏥",
    layout="wide"
)

IMAGE_FOLDER = Path("images")


# ============================================================
# 2. 전체 디자인
# ============================================================

st.markdown(
    """
<style>

/* ------------------------------------------------------------
   전체 화면
------------------------------------------------------------ */

.stApp {
    background:
        linear-gradient(
            90deg,
            #dfe8eb 0%,
            #dfe8eb 72%,
            #cbd8dc 72%,
            #cbd8dc 100%
        );

    color: #243740;
}


/* ------------------------------------------------------------
   병원 벽의 밤 창문
------------------------------------------------------------ */

.stApp::before {
    content: "";

    position: fixed;

    top: 105px;
    right: 32px;

    width: 265px;
    height: 220px;

    border: 12px solid #eef4f6;
    border-radius: 8px;

    box-sizing: border-box;

    background:

        /* 달 */
        radial-gradient(
            circle at 77% 23%,
            #fff5b8 0px,
            #fff5b8 20px,
            transparent 21px
        ),

        /* 별 */
        radial-gradient(
            circle at 15% 18%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 35% 34%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 54% 15%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 67% 42%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 25% 55%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        /* 밤하늘 */
        linear-gradient(
            180deg,
            #071426 0%,
            #102947 60%,
            #1e405e 100%
        );

    box-shadow:
        inset 0 0 0 3px #b4c5ca,
        0 8px 24px rgba(0, 0, 0, 0.16);

    z-index: 0;
}


/* 창문 세로 프레임 */
.stApp::after {
    content: "";

    position: fixed;

    top: 117px;
    right: 157px;

    width: 7px;
    height: 196px;

    background: #eef4f6;

    z-index: 1;
}


/* ------------------------------------------------------------
   본문 영역
------------------------------------------------------------ */

.block-container {
    position: relative;

    z-index: 2;

    max-width: 1030px;

    margin-left: 25px;

    margin-right: 315px;

    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* ------------------------------------------------------------
   제목
------------------------------------------------------------ */

.game-title {
    font-size: 42px;

    font-weight: 900;

    color: #20343e;

    letter-spacing: 2px;

    margin-bottom: 2px;
}

.game-subtitle {
    color: #58707b;

    font-size: 15px;

    margin-bottom: 20px;
}


/* ------------------------------------------------------------
   상단 상태창
------------------------------------------------------------ */

.status-card {
    background: #243943;

    border: 1px solid #425d68;

    border-radius: 13px;

    padding: 13px;

    text-align: center;

    box-shadow: 0 5px 16px rgba(35, 55, 65, 0.13);
}

.status-card,
.status-card * {
    color: #ffffff !important;
}


/* ------------------------------------------------------------
   현재 위치
------------------------------------------------------------ */

.location-box {
    background: rgba(248, 251, 252, 0.96);

    color: #263c45;

    border-left: 6px solid #6d9aaa;

    border-radius: 15px;

    padding: 16px 19px;

    margin-top: 18px;
    margin-bottom: 15px;

    box-shadow: 0 7px 20px rgba(40, 60, 70, 0.10);
}

.location-box * {
    color: #263c45 !important;
}


/* ------------------------------------------------------------
   일반 카드
------------------------------------------------------------ */

.panel {
    background: rgba(249, 252, 253, 0.97);

    border: 1px solid #aec1c8;

    border-radius: 18px;

    padding: 23px;

    color: #263a43;

    box-shadow: 0 8px 24px rgba(40, 60, 70, 0.12);
}

.panel * {
    color: #263a43 !important;
}


/* ------------------------------------------------------------
   환자 사진 영역
------------------------------------------------------------ */

.photo-card {
    background:
        linear-gradient(
            180deg,
            #e4edef 0%,
            #d1e0e4 100%
        );

    min-height: 430px;

    border: 1px solid #9eb2ba;

    border-radius: 18px;

    display: flex;

    justify-content: center;

    align-items: center;

    font-size: 100px;

    color: #5b7079;

    box-shadow: 0 8px 22px rgba(40, 60, 70, 0.10);
}


/* ------------------------------------------------------------
   검사 결과
------------------------------------------------------------ */

.exam-box {
    background: #eaf2fa;

    border-left: 6px solid #6588ad;

    border-radius: 13px;

    padding: 19px;

    color: #2e485d;

    line-height: 1.9;

    margin-top: 18px;
}

.exam-box * {
    color: #2e485d !important;
}


/* ------------------------------------------------------------
   성공
------------------------------------------------------------ */

.success-box {
    background: #e9f7ef;

    border-left: 6px solid #5ca078;

    border-radius: 13px;

    padding: 19px;

    color: #2b503a;

    line-height: 1.8;

    margin-top: 18px;
}

.success-box * {
    color: #2b503a !important;
}


/* ------------------------------------------------------------
   실패
------------------------------------------------------------ */

.danger-box {
    background: #fae9ec;

    border-left: 6px solid #bf5a69;

    border-radius: 13px;

    padding: 19px;

    color: #653941;

    line-height: 1.8;

    margin-top: 18px;
}

.danger-box * {
    color: #653941 !important;
}


/* ------------------------------------------------------------
   인벤토리
------------------------------------------------------------ */

.inventory {
    background: #273b45;

    border: 1px solid #435e6a;

    border-radius: 14px;

    padding: 14px 18px;

    margin-bottom: 15px;
}

.inventory,
.inventory * {
    color: white !important;
}


/* ------------------------------------------------------------
   물품 카드
------------------------------------------------------------ */

.item-card {
    background: rgba(250, 253, 254, 0.97);

    color: #253a43;

    border: 1px solid #abc0c7;

    border-radius: 15px;

    padding: 20px;

    text-align: center;

    min-height: 120px;

    box-shadow: 0 6px 18px rgba(40, 60, 70, 0.10);
}

.item-card * {
    color: #253a43 !important;
}


/* ------------------------------------------------------------
   지도 안의 장소
------------------------------------------------------------ */

.map-room {
    background: #eef4f6;

    color: #253940;

    border: 1px solid #adbec5;

    border-radius: 12px;

    padding: 13px;

    text-align: center;

    margin-bottom: 8px;

    font-weight: 800;
}

.map-room * {
    color: #253940 !important;
}


/* ------------------------------------------------------------
   Streamlit 기본 텍스트
------------------------------------------------------------ */

h1,
h2,
h3,
h4 {
    color: #243a43 !important;
}

p,
label {
    color: #2a4049;
}


/* ------------------------------------------------------------
   버튼
------------------------------------------------------------ */

.stButton > button {
    width: 100%;

    min-height: 48px;

    border-radius: 10px;

    font-weight: 800;

    border: 1px solid #94aab3;
}


/* ------------------------------------------------------------
   multiselect 글씨
------------------------------------------------------------ */

div[data-baseweb="select"] * {
    color: #253940 !important;
}


/* ------------------------------------------------------------
   popover 내부
------------------------------------------------------------ */

[data-testid="stPopoverBody"] {
    color: #253940;
}


/* ------------------------------------------------------------
   작은 화면에서는 창문 숨김
------------------------------------------------------------ */

@media (max-width: 900px) {

    .stApp::before,
    .stApp::after {
        display: none;
    }

    .block-container {
        margin-right: auto;
        margin-left: auto;
        max-width: 95%;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# 3. 환자 정보
# ============================================================

PATIENTS = [

    {
        "id": 1,

        "image": "patient01.png",

        "anomaly": False,

        "exam_text":
            "환자는 두통과 어지럼증을 호소합니다. "
            "신경계 상태를 확인하기 위한 기본 평가가 필요합니다.",

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
            "환자의 얼굴에서 게임 설정상 비정상적인 형태의 변칙이 발견되었습니다.",

        "exam_text": "",

        "items": []
    },


    {
        "id": 3,

        "image": "patient03.png",

        "anomaly": False,

        "exam_text":
            "환자는 최근 기억력 변화를 호소하고 있습니다. "
            "인지 상태를 확인하기 위한 평가 준비가 필요합니다.",

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
            "환자의 얼굴 구조가 자연스러운 사람의 얼굴과 다른 형태로 나타납니다.",

        "exam_text": "",

        "items": []
    },


    {
        "id": 5,

        "image": "patient05.png",

        "anomaly": False,

        "exam_text":
            "환자는 손의 감각이 평소와 다르다고 말합니다. "
            "기본적인 감각 및 반사 확인이 필요합니다.",

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
            "사진 속 얼굴에 게임 속 가상의 변칙이 나타나 있습니다.",

        "exam_text": "",

        "items": []
    }

]


# ============================================================
# 4. 물품 목록
# ============================================================

ALL_ITEMS = [

    "냉찜질 팩",

    "신경학적 검사 카드",

    "인지검사 카드",

    "MRI 검사 안내서",

    "감각검사 카드",

    "반사검사 도구"

]


# ============================================================
# 5. 게임 초기화
# ============================================================

def initialize_game():

    order = list(
        range(
            len(PATIENTS)
        )
    )

    random.shuffle(
        order
    )

    st.session_state.started = True

    st.session_state.game_over = False

    st.session_state.order = order

    st.session_state.patient_number = 0

    st.session_state.location = "데스크"

    st.session_state.score = 0

    st.session_state.lives = 3

    st.session_state.inventory = []

    st.session_state.patient_admitted = False

    st.session_state.examined = False

    st.session_state.completed = False

    st.session_state.message = ""


# ============================================================
# 6. 현재 환자
# ============================================================

def current_patient():

    if (
        st.session_state.patient_number
        >= len(st.session_state.order)
    ):

        return None


    index = st.session_state.order[
        st.session_state.patient_number
    ]


    return PATIENTS[
        index
    ]


# ============================================================
# 7. 환자 사진
# ============================================================

def show_patient(patient):

    image_path = (
        IMAGE_FOLDER
        /
        patient["image"]
    )


    if image_path.exists():

        st.image(
            str(image_path),
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
            "images 폴더에 환자 이미지를 추가하면 여기에 표시됩니다."
        )


# ============================================================
# 8. 방 이동
# ============================================================

def move_room(room):

    st.session_state.location = room


# ============================================================
# 9. 다음 환자
# ============================================================

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


# ============================================================
# 10. 데스크 판단
# ============================================================

def desk_decision(choice):

    patient = current_patient()


    # --------------------------------------------------------
    # 병원 안으로 들이기
    # --------------------------------------------------------

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
                "✅ 정상 환자입니다. 환자가 진료실로 이동했습니다."
            )


    # --------------------------------------------------------
    # 출입 차단
    # --------------------------------------------------------

    elif choice == "block":

        if patient["anomaly"]:

            st.session_state.score += 150

            st.session_state.completed = True

            st.session_state.message = (
                "🚨 변칙 환자를 발견해 출입을 차단했습니다."
            )


        else:

            st.session_state.lives -= 1

            st.session_state.message = (
                "❌ 정상 환자의 출입을 막았습니다."
            )


            if st.session_state.lives <= 0:

                st.session_state.game_over = True


# ============================================================
# 11. 환자 검사
# ============================================================

def examine_patient():

    st.session_state.examined = True

    st.session_state.score += 50

    st.session_state.message = (
        "🔍 환자 검사가 완료되었습니다."
    )


# ============================================================
# 12. 물품 가져오기
# ============================================================

def add_item(item):

    # 중복 방지
    if item in st.session_state.inventory:

        st.warning(
            "이미 인벤토리에 있는 물품입니다."
        )

        return


    # 최대 4개
    if len(st.session_state.inventory) >= 4:

        st.warning(
            "인벤토리가 가득 찼습니다. 최대 4개의 물품만 가지고 다닐 수 있습니다."
        )

        return


    st.session_state.inventory.append(
        item
    )

    st.success(
        f"🎒 {item}을(를) 인벤토리에 넣었습니다."
    )


# ============================================================
# 13. 물품 적용
# ============================================================

def apply_items(selected_items):

    patient = current_patient()


    # 두 개를 선택하지 않은 경우
    if len(selected_items) != 2:

        st.warning(
            "환자에게 적용할 물품 2개를 선택하세요."
        )

        return


    required_items = set(
        patient["items"]
    )

    selected_set = set(
        selected_items
    )


    # 정답
    if selected_set == required_items:

        st.session_state.score += 200

        st.session_state.completed = True

        st.session_state.message = (
            "✅ 필요한 물품 두 가지를 정확하게 적용했습니다. "
            "환자 처치가 완료되었습니다."
        )


    # 오답
    else:

        st.session_state.lives -= 1

        st.session_state.message = (
            "❌ 이 환자에게 필요한 물품 조합이 아닙니다."
        )


        if st.session_state.lives <= 0:

            st.session_state.game_over = True


# ============================================================
# 14. Session State 기본값
# ============================================================

if "started" not in st.session_state:

    st.session_state.started = False


if "game_over" not in st.session_state:

    st.session_state.game_over = False


# ============================================================
# 15. 게임 제목
# ============================================================

st.markdown(
    """
    <div class="game-title">
    🏥 NEURO NIGHT SHIFT
    </div>

    <div class="game-subtitle">
    당신은 오늘 밤 병원의 당직 의사입니다.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 16. 시작 화면
# ============================================================

if not st.session_state.started:

    st.markdown(
        """
        <div class="panel">

        <h2>🌙 야간 근무 안내</h2>

        오늘 밤 당신은 병원의 당직 의사입니다.

        <br><br>

        병원 데스크에 환자들이 한 명씩 찾아옵니다.

        <br><br>

        환자의 <b>얼굴을 자세히 관찰</b>한 뒤
        병원 안으로 들일지 출입을 막을지 판단하세요.

        <br><br>

        정상 환자를 병원 안으로 들이면
        진료실에서 검사를 실시할 수 있습니다.

        <br><br>

        검사 결과 필요한 물품 두 가지를 확인한 뒤,
        병원 지도를 이용해 물품실로 이동하고
        필요한 물품을 직접 가져오세요.

        <br><br>

        다시 진료실로 돌아와 인벤토리에서
        올바른 두 물품을 선택하면 환자 처치가 완료됩니다.

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


# ============================================================
# 17. 게임 종료
# ============================================================

elif st.session_state.game_over:

    final_score = st.session_state.score


    if final_score >= 900:

        grade = "S"


    elif final_score >= 650:

        grade = "A"


    elif final_score >= 400:

        grade = "B"


    else:

        grade = "C"


    st.markdown(
        f"""
        <div class="panel"
        style="text-align:center;">

        <h2>🌅 야간 근무 종료</h2>

        <div
        style="
        font-size:90px;
        font-weight:900;
        color:#557f91;
        margin-top:15px;
        margin-bottom:15px;
        ">
        {grade}
        </div>

        <h2>
        최종 점수 : {final_score}
        </h2>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")


    if st.button(
        "🔄 다시 시작",
        use_container_width=True
    ):

        initialize_game()

        st.rerun()


# ============================================================
# 18. 게임 플레이
# ============================================================

else:

    patient = current_patient()


    # ========================================================
    # 상단 상태 표시
    # ========================================================

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

            <b>
            {st.session_state.score}
            </b>

            </div>
            """,
            unsafe_allow_html=True
        )


    with s3:

        hearts = (
            "❤️"
            *
            st.session_state.lives
        )

        st.markdown(
            f"""
            <div class="status-card">

            LIFE<br>

            {hearts}

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # 병원 지도
    # ========================================================

    with s4:

        with st.popover(
            "🗺️ 병원 지도",
            use_container_width=True
        ):

            st.markdown(
                "### 🏥 병원 내부 지도"
            )


            # 데스크
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
                key="map_desk",
                use_container_width=True
            ):

                move_room(
                    "데스크"
                )

                st.rerun()


            st.markdown(
                "↓"
            )


            room1, room2 = st.columns(2)


            # 진료실
            with room1:

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
                    key="map_treatment",
                    use_container_width=True
                ):

                    move_room(
                        "진료실"
                    )

                    st.rerun()


            # 물품실
            with room2:

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
                    key="map_supply",
                    use_container_width=True
                ):

                    move_room(
                        "물품실"
                    )

                    st.rerun()


    # ========================================================
    # 현재 위치
    # ========================================================

    st.markdown(
        f"""
        <div class="location-box">

        📍 현재 위치 :
        <b>{st.session_state.location}</b>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # 인벤토리
    # ========================================================

    if st.session_state.inventory:

        inventory_text = " · ".join(
            st.session_state.inventory
        )


    else:

        inventory_text = "비어 있음"


    st.markdown(
        f"""
        <div class="inventory">

        🎒 <b>INVENTORY</b>

        &nbsp;&nbsp;

        {inventory_text}

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # 상태 메시지
    # ========================================================

    if st.session_state.message:

        st.info(
            st.session_state.message
        )


    # ========================================================
    # 🖥️ 데스크
    # ========================================================

    if st.session_state.location == "데스크":

        st.markdown(
            "## 🖥️ 병원 데스크"
        )


        st.caption(
            "환자의 얼굴만 보고 병원 안으로 들일지 판단하세요."
        )


        # 환자 얼굴
        show_patient(
            patient
        )


        # ----------------------------------------------------
        # 아직 판단하지 않은 경우
        # ----------------------------------------------------

        if (
            not st.session_state.patient_admitted
            and
            not st.session_state.completed
        ):

            st.write("")


            decision1, decision2 = st.columns(
                2
            )


            with decision1:

                if st.button(
                    "🏥 병원 안으로 들인다",
                    use_container_width=True
                ):

                    desk_decision(
                        "admit"
                    )

                    st.rerun()


            with decision2:

                if st.button(
                    "🚨 출입을 막는다",
                    use_container_width=True
                ):

                    desk_decision(
                        "block"
                    )

                    st.rerun()


        # ----------------------------------------------------
        # 변칙 환자 차단 성공
        # ----------------------------------------------------

        if (
            st.session_state.completed
            and
            patient["anomaly"]
        ):

            st.markdown(
                f"""
                <div class="success-box">

                <b>
                🚨 변칙 환자 차단 완료
                </b>

                <br><br>

                {patient.get(
                    "anomaly_reason",
                    "얼굴에서 변칙을 발견했습니다."
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


    # ========================================================
    # 🛏️ 진료실
    # ========================================================

    elif st.session_state.location == "진료실":

        st.markdown(
            "## 🛏️ 진료실"
        )


        # ----------------------------------------------------
        # 환자가 없는 경우
        # ----------------------------------------------------

        if not st.session_state.patient_admitted:

            st.warning(
                "현재 진료실에 들어온 환자가 없습니다."
            )


        # ----------------------------------------------------
        # 환자가 있는 경우
        # ----------------------------------------------------

        else:

            patient_col, info_col = st.columns(
                [1, 1.05]
            )


            with patient_col:

                show_patient(
                    patient
                )


            with info_col:

                st.markdown(
                    f"""
                    <div class="panel">

                    <h3>
                    👤 환자 #{patient["id"]:02d}
                    </h3>

                    환자가 진료실에서 기다리고 있습니다.

                    <br><br>

                    <b>
                    먼저 환자를 검사해 주세요.
                    </b>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # ------------------------------------------------
            # 검사 전
            # ------------------------------------------------

            if not st.session_state.examined:

                st.write("")


                if st.button(
                    "🔍 환자 검사",
                    use_container_width=True
                ):

                    examine_patient()

                    st.rerun()


            # ------------------------------------------------
            # 검사 완료
            # ------------------------------------------------

            else:

                required_item1 = patient[
                    "items"
                ][0]

                required_item2 = patient[
                    "items"
                ][1]


                st.markdown(
                    f"""
                    <div class="exam-box">

                    <b>
                    🔍 검사 결과
                    </b>

                    <br><br>

                    {patient["exam_text"]}

                    <br><br>

                    <b>
                    필요한 물품
                    </b>

                    <br><br>

                    ① {required_item1}

                    <br>

                    ② {required_item2}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # --------------------------------------------
                # 이미 치료 완료
                # --------------------------------------------

                if st.session_state.completed:

                    st.markdown(
                        """
                        <div class="success-box">

                        ✅ 환자 처치가 완료되었습니다.

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


                # --------------------------------------------
                # 치료 전
                # --------------------------------------------

                else:

                    st.write("")


                    if not st.session_state.inventory:

                        st.warning(
                            "🎒 현재 인벤토리가 비어 있습니다. "
                            "위쪽 병원 지도에서 물품실로 이동하세요."
                        )


                    else:

                        st.markdown(
                            "### 🎒 환자에게 적용할 물품"
                        )


                        selected_items = st.multiselect(
                            "인벤토리에서 정확히 2개의 물품을 선택하세요.",
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


    # ========================================================
    # 📦 물품실
    # ========================================================

    elif st.session_state.location == "물품실":

        st.markdown(
            "## 📦 치료 물품실"
        )


        st.caption(
            "검사 결과를 기억하고 필요한 물품을 직접 선택하세요."
        )


        # 물품을 3개씩 배치
        item_rows = [

            ALL_ITEMS[
                i:i + 3
            ]

            for i in range(
                0,
                len(ALL_ITEMS),
                3
            )

        ]


        for row_number, row in enumerate(
            item_rows
        ):

            columns = st.columns(
                len(row)
            )


            for item_number, item in enumerate(
                row
            ):

                with columns[
                    item_number
                ]:

                    st.markdown(
                        f"""
                        <div class="item-card">

                        <div
                        style="
                        font-size:36px;
                        margin-bottom:10px;
                        ">
                        🧰
                        </div>

                        <b>
                        {item}
                        </b>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    if st.button(
                        "🎒 가져가기",
                        key=(
                            f"item_"
                            f"{row_number}_"
                            f"{item_number}"
                        ),
                        use_container_width=True
                    ):

                        add_item(
                            item
                        )

                        st.rerun()

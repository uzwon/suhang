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

# 한 밤에 등장하는 환자 수
PATIENTS_PER_NIGHT = 5

# 정상 환자 1명 치료 성공 시 급여
NORMAL_PATIENT_REWARD = 600_000

# 변칙 환자가 진료실에 들어온 경우 감봉
ANOMALY_PENALTY = 200_000

# 상점의 목숨 +1 가격
LIFE_PRICE = 3_100_000


# ============================================================
# 2. 디자인
# ============================================================

st.markdown(
    """
<style>

/* ------------------------------------------------------------
   전체 병원 배경
------------------------------------------------------------ */

.stApp {
    background:
        linear-gradient(
            90deg,
            #e5edef 0%,
            #e5edef 73%,
            #d1dde1 73%,
            #d1dde1 100%
        );

    color: #263a43;
}


/* ------------------------------------------------------------
   오른쪽 병원 벽의 밤 창문
------------------------------------------------------------ */

.stApp::before {

    content: "";

    position: fixed;

    top: 105px;
    right: 35px;

    width: 260px;
    height: 225px;

    border: 12px solid #f3f7f8;

    border-radius: 8px;

    box-sizing: border-box;

    background:

        /* 달 */
        radial-gradient(
            circle at 78% 23%,
            #fff6bd 0px,
            #fff6bd 21px,
            transparent 22px
        ),

        /* 별 */
        radial-gradient(
            circle at 16% 18%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 32% 35%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 50% 18%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 65% 43%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 22% 63%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        linear-gradient(
            180deg,
            #061323 0%,
            #102a48 60%,
            #1b405e 100%
        );

    box-shadow:
        inset 0 0 0 3px #b7c8cd,
        0 8px 24px rgba(0,0,0,0.18);

    z-index: 0;
}


/* 창문 중앙 세로 프레임 */

.stApp::after {

    content: "";

    position: fixed;

    top: 117px;
    right: 157px;

    width: 7px;
    height: 201px;

    background: #f3f7f8;

    z-index: 1;
}


/* ------------------------------------------------------------
   본문
------------------------------------------------------------ */

.block-container {

    position: relative;

    z-index: 2;

    max-width: 1020px;

    margin-left: 25px;

    margin-right: 315px;

    padding-top: 1.3rem;
    padding-bottom: 4rem;
}


/* ------------------------------------------------------------
   제목
------------------------------------------------------------ */

.game-title {

    font-size: 40px;

    font-weight: 900;

    color: #203640;

    letter-spacing: 2px;
}

.game-subtitle {

    color: #617985;

    font-size: 14px;

    margin-bottom: 17px;
}


/* ------------------------------------------------------------
   상태 카드
------------------------------------------------------------ */

.status-card {

    background: #263b45;

    border: 1px solid #46616d;

    border-radius: 14px;

    padding: 13px;

    text-align: center;

    box-shadow: 0 5px 15px rgba(35,55,65,0.12);
}

.status-card,
.status-card * {

    color: white !important;
}


/* ------------------------------------------------------------
   현재 위치
------------------------------------------------------------ */

.location-box {

    background: rgba(249,252,253,0.97);

    border-left: 6px solid #739dac;

    border-radius: 15px;

    padding: 16px 19px;

    margin-top: 16px;
    margin-bottom: 13px;

    box-shadow: 0 6px 18px rgba(40,60,70,0.10);
}

.location-box,
.location-box * {

    color: #263c45 !important;
}


/* ------------------------------------------------------------
   일반 패널
------------------------------------------------------------ */

.panel {

    background: rgba(250,253,254,0.98);

    border: 1px solid #afc1c8;

    border-radius: 18px;

    padding: 22px;

    color: #273b44;

    box-shadow: 0 8px 22px rgba(40,60,70,0.11);
}

.panel,
.panel * {

    color: #273b44 !important;
}


/* ------------------------------------------------------------
   환자 사진
------------------------------------------------------------ */

.photo-card {

    min-height: 420px;

    background:
        linear-gradient(
            180deg,
            #e3edef 0%,
            #d2e0e4 100%
        );

    border: 1px solid #9fb3bb;

    border-radius: 18px;

    display: flex;

    justify-content: center;

    align-items: center;

    color: #5a717b;

    font-size: 100px;

    box-shadow: 0 7px 20px rgba(40,60,70,0.10);
}


/* ------------------------------------------------------------
   튜토리얼
------------------------------------------------------------ */

.tutorial-box {

    background: #fff6d8;

    border-left: 7px solid #dfbb4d;

    border-radius: 14px;

    padding: 19px;

    margin-top: 17px;

    line-height: 1.8;
}

.tutorial-box,
.tutorial-box * {

    color: #584e2c !important;
}


/* ------------------------------------------------------------
   검사 결과
------------------------------------------------------------ */

.exam-box {

    background: #eaf2fb;

    border-left: 6px solid #668ab2;

    border-radius: 13px;

    padding: 19px;

    margin-top: 17px;

    line-height: 1.9;
}

.exam-box,
.exam-box * {

    color: #304b60 !important;
}


/* ------------------------------------------------------------
   성공
------------------------------------------------------------ */

.success-box {

    background: #e9f7ef;

    border-left: 6px solid #5ca078;

    border-radius: 13px;

    padding: 18px;

    margin-top: 16px;

    line-height: 1.8;
}

.success-box,
.success-box * {

    color: #2d513b !important;
}


/* ------------------------------------------------------------
   변칙 환자
------------------------------------------------------------ */

.anomaly-box {

    background: #fbe9ec;

    border: 2px solid #bf5b69;

    border-left: 8px solid #b43e4f;

    border-radius: 14px;

    padding: 20px;

    margin-top: 17px;

    line-height: 1.8;

    box-shadow: 0 7px 20px rgba(160,50,65,0.12);
}

.anomaly-box,
.anomaly-box * {

    color: #6b3039 !important;
}


/* ------------------------------------------------------------
   인벤토리
------------------------------------------------------------ */

.inventory {

    background: #273d47;

    border: 1px solid #46616d;

    border-radius: 14px;

    padding: 14px 18px;

    margin-bottom: 15px;
}

.inventory,
.inventory * {

    color: white !important;
}


/* ------------------------------------------------------------
   물품
------------------------------------------------------------ */

.item-card {

    background: rgba(250,253,254,0.98);

    border: 1px solid #abc0c7;

    border-radius: 15px;

    padding: 18px;

    text-align: center;

    min-height: 120px;

    box-shadow: 0 5px 16px rgba(40,60,70,0.10);
}

.item-card,
.item-card * {

    color: #273b44 !important;
}


/* ------------------------------------------------------------
   급여
------------------------------------------------------------ */

.salary-box {

    background: #fff6d9;

    border-left: 7px solid #d9b94e;

    border-radius: 15px;

    padding: 21px;

    margin-top: 18px;

    line-height: 1.9;
}

.salary-box,
.salary-box * {

    color: #584d2c !important;
}


/* ------------------------------------------------------------
   상점
------------------------------------------------------------ */

.shop-card {

    background: rgba(251,253,254,0.98);

    border: 1px solid #afc1c7;

    border-radius: 16px;

    padding: 17px;

    text-align: center;

    min-height: 145px;

    box-shadow: 0 5px 16px rgba(40,60,70,0.10);
}

.shop-card,
.shop-card * {

    color: #273b44 !important;
}


/* ------------------------------------------------------------
   지도
------------------------------------------------------------ */

.map-room {

    background: #eef4f6;

    color: #263b44;

    border: 1px solid #adbec5;

    border-radius: 12px;

    padding: 12px;

    text-align: center;

    margin-bottom: 7px;

    font-weight: 800;
}


/* ------------------------------------------------------------
   캐릭터 카드
------------------------------------------------------------ */

.character-card {

    background:
        linear-gradient(
            180deg,
            #f7fbfc,
            #e8f0f2
        );

    border: 1px solid #adc0c7;

    border-radius: 18px;

    padding: 22px;

    text-align: center;
}

.character-preview {

    font-size: 72px;

    margin-bottom: 10px;
}

.custom-text {

    font-size: 14px;

    line-height: 1.9;

    color: #445c67;
}


/* ------------------------------------------------------------
   버튼
------------------------------------------------------------ */

.stButton > button {

    width: 100%;

    min-height: 48px;

    border-radius: 10px;

    font-weight: 800;
}


/* ------------------------------------------------------------
   기본 글자
------------------------------------------------------------ */

h1,
h2,
h3,
h4 {

    color: #263b44 !important;
}

p,
label {

    color: #2b414a;
}

div[data-baseweb="select"] * {

    color: #253941 !important;
}


/* ------------------------------------------------------------
   모바일
------------------------------------------------------------ */

@media (max-width: 900px) {

    .stApp::before,
    .stApp::after {

        display: none;
    }

    .block-container {

        margin-left: auto;

        margin-right: auto;

        max-width: 95%;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# 3. 환자 데이터
# ============================================================

PATIENTS = [

    {
        "id": 1,
        "image": "patient01.png",
        "anomaly": False,

        "exam_text":
            "기본적인 신경계 상태 확인이 필요합니다.",

        "items": [
            "신경학적 검사 키트",
            "활력징후 기록 카드"
        ]
    },


    {
        "id": 2,
        "image": "patient02.png",
        "anomaly": True,

        "exam_text":
            "현재 검사만으로는 변칙 여부를 알 수 없습니다.",

        "items": [
            "감각검사 카드",
            "신경학적 검사 키트"
        ]
    },


    {
        "id": 3,
        "image": "patient03.png",
        "anomaly": False,

        "exam_text":
            "인지 상태 확인을 위한 기본 평가가 필요합니다.",

        "items": [
            "인지검사 카드",
            "MRI 검사 안내서"
        ]
    },


    {
        "id": 4,
        "image": "patient04.png",
        "anomaly": True,

        "exam_text":
            "감각 및 반응 상태 확인이 필요합니다.",

        "items": [
            "감각검사 카드",
            "반사검사 도구"
        ]
    },


    {
        "id": 5,
        "image": "patient05.png",
        "anomaly": False,

        "exam_text":
            "신경계 반응 및 상태 확인이 필요합니다.",

        "items": [
            "반사검사 도구",
            "신경학적 검사 키트"
        ]
    },


    {
        "id": 6,
        "image": "patient06.png",
        "anomaly": True,

        "exam_text":
            "현재 기본 검사에서는 특별한 변칙을 알 수 없습니다.",

        "items": [
            "활력징후 기록 카드",
            "MRI 검사 안내서"
        ]
    },


    {
        "id": 7,
        "image": "patient07.png",
        "anomaly": False,

        "exam_text":
            "인지 및 기본 상태 확인이 필요합니다.",

        "items": [
            "인지검사 카드",
            "활력징후 기록 카드"
        ]
    },


    {
        "id": 8,
        "image": "patient08.png",
        "anomaly": False,

        "exam_text":
            "감각과 반응 상태 확인이 필요합니다.",

        "items": [
            "감각검사 카드",
            "반사검사 도구"
        ]
    }

]


# ============================================================
# 4. 치료 / 검사 물품
# ============================================================

ALL_ITEMS = [

    "신경학적 검사 키트",

    "활력징후 기록 카드",

    "감각검사 카드",

    "반사검사 도구",

    "인지검사 카드",

    "MRI 검사 안내서"

]


# ============================================================
# 5. 캐릭터 꾸미기 상품
# ============================================================

HAIR_ITEMS = {

    "단발": 0,

    "긴 머리": 1_200_000,

    "포니테일": 1_500_000
}


EYE_SHAPE_ITEMS = {

    "둥근 눈": 0,

    "웃는 눈": 900_000,

    "날카로운 눈": 1_100_000
}


EYE_COLOR_ITEMS = {

    "갈색": 0,

    "파란색": 800_000,

    "보라색": 1_000_000
}


# ============================================================
# 6. 프로필 초기화
# ============================================================

def initialize_profile():

    if "money" not in st.session_state:

        st.session_state.money = 0


    if "night" not in st.session_state:

        st.session_state.night = 1


    if "owned_hair" not in st.session_state:

        st.session_state.owned_hair = [
            "단발"
        ]


    if "owned_eye_shape" not in st.session_state:

        st.session_state.owned_eye_shape = [
            "둥근 눈"
        ]


    if "owned_eye_color" not in st.session_state:

        st.session_state.owned_eye_color = [
            "갈색"
        ]


    if "selected_hair" not in st.session_state:

        st.session_state.selected_hair = (
            "단발"
        )


    if "selected_eye_shape" not in st.session_state:

        st.session_state.selected_eye_shape = (
            "둥근 눈"
        )


    if "selected_eye_color" not in st.session_state:

        st.session_state.selected_eye_color = (
            "갈색"
        )


    # 상점에서 산 추가 목숨
    if "extra_lives" not in st.session_state:

        st.session_state.extra_lives = 0


# ============================================================
# 7. 밤 시작
# ============================================================

def start_night():

    patient_indices = list(
        range(
            len(PATIENTS)
        )
    )

    random.shuffle(
        patient_indices
    )


    st.session_state.night_patients = (
        patient_indices[:PATIENTS_PER_NIGHT]
    )


    st.session_state.current_case = 0

    st.session_state.location = "데스크"


    # 기본 체력 3 + 구매한 목숨
    st.session_state.health = (
        3
        +
        st.session_state.extra_lives
    )


    # 사용 후 초기화
    st.session_state.extra_lives = 0


    st.session_state.inventory = []

    st.session_state.patient_admitted = False

    st.session_state.patient_rejected = False

    st.session_state.examined = False

    st.session_state.completed = False

    st.session_state.anomaly_revealed = False

    st.session_state.anomaly_penalty_applied = False

    st.session_state.message = ""

    st.session_state.normal_treated = 0

    st.session_state.anomalies_admitted = 0

    st.session_state.anomalies_rejected = 0

    st.session_state.normal_rejected = 0

    st.session_state.night_finished = False

    st.session_state.salary_received = False

    st.session_state.game_started = True


# ============================================================
# 8. 현재 환자
# ============================================================

def current_patient():

    if (
        st.session_state.current_case
        >= len(
            st.session_state.night_patients
        )
    ):

        return None


    index = (
        st.session_state.night_patients[
            st.session_state.current_case
        ]
    )


    return PATIENTS[
        index
    ]


# ============================================================
# 9. 환자 사진
# ============================================================

def show_patient(patient):

    path = (
        IMAGE_FOLDER
        /
        patient["image"]
    )


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
            "images 폴더에 환자 사진을 추가하면 여기에 표시됩니다."
        )


# ============================================================
# 10. 장소 이동
# ============================================================

def move_room(room):

    patient = current_patient()


    # 변칙 환자가 실제 진료실에 들어온 경우
    # 급여 감봉 대상으로 기록
    if (
        room == "진료실"
        and
        st.session_state.patient_admitted
        and
        patient is not None
        and
        patient["anomaly"]
        and
        not st.session_state.anomaly_penalty_applied
    ):

        st.session_state.anomalies_admitted += 1

        st.session_state.anomaly_penalty_applied = True


    st.session_state.location = room


# ============================================================
# 11. 환자 입장 허용
# ============================================================

def admit_patient():

    st.session_state.patient_admitted = True

    st.session_state.message = (
        "🏥 환자의 병원 출입을 허용했습니다."
    )


    # 자동으로 진료실로 이동하지 않음


# ============================================================
# 12. 환자 출입 거절
# ============================================================

def reject_patient():

    patient = current_patient()


    st.session_state.patient_rejected = True

    st.session_state.completed = True


    if patient["anomaly"]:

        st.session_state.anomalies_rejected += 1

        st.session_state.message = (
            "🚨 환자의 출입을 막았습니다. "
            "확인 결과 변칙성 환자였습니다."
        )


    else:

        st.session_state.normal_rejected += 1

        st.session_state.message = (
            "⚠️ 환자의 출입을 막았습니다. "
            "확인 결과 정상 환자였습니다."
        )


# ============================================================
# 13. 환자 검사
# ============================================================

def examine_patient():

    st.session_state.examined = True

    st.session_state.message = (
        "🔍 환자 검사가 완료되었습니다."
    )


# ============================================================
# 14. 물품 획득
# ============================================================

def add_item(item):

    if item in st.session_state.inventory:

        st.warning(
            "이미 가지고 있는 물품입니다."
        )

        return


    if len(
        st.session_state.inventory
    ) >= 4:

        st.warning(
            "인벤토리는 최대 4개의 물품까지만 보관할 수 있습니다."
        )

        return


    st.session_state.inventory.append(
        item
    )


# ============================================================
# 15. 치료 물품 적용
# ============================================================

def apply_items(selected_items):

    patient = current_patient()


    if len(selected_items) != 2:

        st.warning(
            "환자에게 적용할 물품 2개를 선택하세요."
        )

        return


    required = set(
        patient["items"]
    )

    selected = set(
        selected_items
    )


    if selected != required:

        st.session_state.message = (
            "❌ 필요한 물품 조합이 아닙니다. "
            "검사 결과를 다시 확인해 주세요."
        )

        return


    st.session_state.completed = True


    # --------------------------------------------------------
    # 변칙 환자
    # --------------------------------------------------------

    if patient["anomaly"]:

        st.session_state.health -= 1

        st.session_state.anomaly_revealed = True

        st.session_state.message = (
            "🚨 변칙성 환자입니다! "
            "치료 과정에서 데미지를 입었습니다."
        )


    # --------------------------------------------------------
    # 정상 환자
    # --------------------------------------------------------

    else:

        st.session_state.normal_treated += 1

        st.session_state.message = (
            "✅ 정상 환자 치료가 완료되었습니다."
        )


# ============================================================
# 16. 다음 환자
# ============================================================

def next_patient():

    st.session_state.current_case += 1


    # 체력 소진
    if st.session_state.health <= 0:

        st.session_state.night_finished = True

        return


    # 오늘의 모든 환자 완료
    if (
        st.session_state.current_case
        >= len(
            st.session_state.night_patients
        )
    ):

        st.session_state.night_finished = True

        return


    st.session_state.location = "데스크"

    st.session_state.inventory = []

    st.session_state.patient_admitted = False

    st.session_state.patient_rejected = False

    st.session_state.examined = False

    st.session_state.completed = False

    st.session_state.anomaly_revealed = False

    st.session_state.anomaly_penalty_applied = False

    st.session_state.message = ""


# ============================================================
# 17. 급여 정산
# ============================================================

def receive_salary():

    if st.session_state.salary_received:

        return


    # 정상 환자 한 명당 60만 원
    treatment_pay = (
        st.session_state.normal_treated
        *
        NORMAL_PATIENT_REWARD
    )


    # 진료실에 들어온 변칙 환자 한 명당 20만 원 감봉
    penalty = (
        st.session_state.anomalies_admitted
        *
        ANOMALY_PENALTY
    )


    final_salary = max(
        0,
        treatment_pay - penalty
    )


    st.session_state.last_treatment_pay = (
        treatment_pay
    )

    st.session_state.last_penalty = (
        penalty
    )

    st.session_state.last_salary = (
        final_salary
    )


    st.session_state.money += (
        final_salary
    )


    st.session_state.salary_received = True


# ============================================================
# 18. 꾸미기 상품 구매
# ============================================================

def buy_cosmetic(
    item_name,
    price,
    category
):

    if st.session_state.money < price:

        st.warning(
            "보유 금액이 부족합니다."
        )

        return


    if category == "hair":

        if item_name in st.session_state.owned_hair:
            return

        st.session_state.owned_hair.append(
            item_name
        )


    elif category == "eye_shape":

        if item_name in st.session_state.owned_eye_shape:
            return

        st.session_state.owned_eye_shape.append(
            item_name
        )


    elif category == "eye_color":

        if item_name in st.session_state.owned_eye_color:
            return

        st.session_state.owned_eye_color.append(
            item_name
        )


    st.session_state.money -= (
        price
    )


# ============================================================
# 19. 목숨 구매
# ============================================================

def buy_life():

    if st.session_state.money < LIFE_PRICE:

        st.warning(
            "목숨을 구매하기 위한 돈이 부족합니다."
        )

        return


    st.session_state.money -= (
        LIFE_PRICE
    )

    st.session_state.extra_lives += 1


# ============================================================
# 20. 캐릭터 표시
# ============================================================

def show_character():

    hair = st.session_state.selected_hair

    eye_shape = (
        st.session_state.selected_eye_shape
    )

    eye_color = (
        st.session_state.selected_eye_color
    )


    hair_symbol = {

        "단발": "💇🏻‍♀️",

        "긴 머리": "👩🏻",

        "포니테일": "👱🏻‍♀️"

    }.get(
        hair,
        "👩🏻"
    )


    eye_symbol = {

        "둥근 눈": "● ●",

        "웃는 눈": "⌒ ⌒",

        "날카로운 눈": "◢ ◣"

    }.get(
        eye_shape,
        "● ●"
    )


    eye_color_symbol = {

        "갈색": "🟤",

        "파란색": "🔵",

        "보라색": "🟣"

    }.get(
        eye_color,
        "🟤"
    )


    st.markdown(
        f"""
        <div class="character-card">

        <div class="character-preview">
        {hair_symbol}
        </div>

        <b>당직 의사</b>

        <br><br>

        <div class="custom-text">

        머리 : <b>{hair}</b><br>

        눈 모양 : <b>{eye_shape}</b>
        &nbsp; {eye_symbol}<br>

        눈 색깔 :
        <b>{eye_color}</b>
        &nbsp; {eye_color_symbol}

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 21. 기본 프로필 설정
# ============================================================

initialize_profile()


if "game_started" not in st.session_state:

    st.session_state.game_started = False


# ============================================================
# 22. 제목
# ============================================================

st.markdown(
    """
    <div class="game-title">
    🏥 NEURO NIGHT SHIFT
    </div>

    <div class="game-subtitle">
    야간 병원 근무 · 변칙 환자 관찰 게임
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 23. 최초 시작 화면
# ============================================================

if not st.session_state.game_started:

    left, right = st.columns(
        [1.7, 1]
    )


    with left:

        st.markdown(
            f"""
            <div class="panel">

            <h2>
            🌙 NIGHT {st.session_state.night}
            </h2>

            오늘 밤 당신은 병원의
            <b>당직 의사</b>입니다.

            <br><br>

            데스크에 찾아오는 환자의 얼굴을 확인하고
            병원에 들일지 거절할지 판단하세요.

            <br><br>

            병원 안으로 들인 환자는
            직접 병원 지도를 이용해 진료실로 이동한 뒤
            검사해야 합니다.

            <br><br>

            변칙성 환자를 치료하면
            데미지를 입게 됩니다.

            </div>
            """,
            unsafe_allow_html=True
        )


    with right:

        show_character()


    st.write("")


    if st.button(
        "🌙 야간 근무 시작",
        use_container_width=True
    ):

        start_night()

        st.rerun()


# ============================================================
# 24. 밤 종료 및 상점
# ============================================================

elif st.session_state.night_finished:

    if not st.session_state.salary_received:

        receive_salary()


    st.markdown(
        f"""
        <div class="salary-box">

        <h2>
        🌅 NIGHT {st.session_state.night} 종료
        </h2>

        정상 치료 환자 :
        <b>
        {st.session_state.normal_treated}명
        </b>

        <br><br>

        정상 환자 치료 급여 :

        <b>
        {st.session_state.last_treatment_pay:,}원
        </b>

        <br>

        (1명당 600,000원)

        <br><br>

        진료실에 들어온 변칙 환자 :

        <b>
        {st.session_state.anomalies_admitted}명
        </b>

        <br><br>

        변칙 환자 감봉 :

        <b>
        -{st.session_state.last_penalty:,}원
        </b>

        <br>

        (1명당 -200,000원)

        <br><br>

        ─────────────────────

        <br>

        <b>
        최종 지급 급여 :
        {st.session_state.last_salary:,}원
        </b>

        <br><br>

        💰 현재 보유 금액 :

        <b>
        {st.session_state.money:,}원
        </b>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        "## 🛍️ 야간 근무 상점"
    )


    st.caption(
        "아무것도 구매하지 않고 바로 다음 밤으로 넘어가도 됩니다."
    )


    # ========================================================
    # 목숨 구매
    # ========================================================

    st.markdown(
        "### ❤️ 생존 아이템"
    )


    life_col1, life_col2 = st.columns(
        [1, 1]
    )


    with life_col1:

        st.markdown(
            f"""
            <div class="shop-card">

            <div style="font-size:40px;">
            ❤️
            </div>

            <br>

            <b>목숨 +1</b>

            <br><br>

            다음 밤의 시작 체력이
            1 증가합니다.

            <br><br>

            <b>
            {LIFE_PRICE:,}원
            </b>

            </div>
            """,
            unsafe_allow_html=True
        )


        if st.button(
            "❤️ 목숨 구매",
            use_container_width=True
        ):

            buy_life()

            st.rerun()


    with life_col2:

        show_character()


    # ========================================================
    # 머리
    # ========================================================

    st.markdown(
        "### 💇 머리 모양"
    )


    hair_columns = st.columns(
        3
    )


    for index, (
        name,
        price
    ) in enumerate(
        HAIR_ITEMS.items()
    ):

        with hair_columns[index]:

            st.markdown(
                f"""
                <div class="shop-card">

                <div style="font-size:38px;">
                💇‍♀️
                </div>

                <br>

                <b>{name}</b>

                <br><br>

                {price:,}원

                </div>
                """,
                unsafe_allow_html=True
            )


            if name in st.session_state.owned_hair:

                if st.button(
                    "착용",
                    key=f"hair_wear_{name}",
                    use_container_width=True
                ):

                    st.session_state.selected_hair = (
                        name
                    )

                    st.rerun()


            else:

                if st.button(
                    "구매",
                    key=f"hair_buy_{name}",
                    use_container_width=True
                ):

                    buy_cosmetic(
                        name,
                        price,
                        "hair"
                    )

                    st.rerun()


    # ========================================================
    # 눈 모양
    # ========================================================

    st.markdown(
        "### 👁️ 눈 모양"
    )


    eye_columns = st.columns(
        3
    )


    for index, (
        name,
        price
    ) in enumerate(
        EYE_SHAPE_ITEMS.items()
    ):

        with eye_columns[index]:

            st.markdown(
                f"""
                <div class="shop-card">

                <div style="font-size:34px;">
                👀
                </div>

                <br>

                <b>{name}</b>

                <br><br>

                {price:,}원

                </div>
                """,
                unsafe_allow_html=True
            )


            if name in st.session_state.owned_eye_shape:

                if st.button(
                    "착용",
                    key=f"eye_shape_use_{name}",
                    use_container_width=True
                ):

                    st.session_state.selected_eye_shape = (
                        name
                    )

                    st.rerun()


            else:

                if st.button(
                    "구매",
                    key=f"eye_shape_buy_{name}",
                    use_container_width=True
                ):

                    buy_cosmetic(
                        name,
                        price,
                        "eye_shape"
                    )

                    st.rerun()


    # ========================================================
    # 눈 색
    # ========================================================

    st.markdown(
        "### 🎨 눈 색깔"
    )


    color_columns = st.columns(
        3
    )


    for index, (
        name,
        price
    ) in enumerate(
        EYE_COLOR_ITEMS.items()
    ):

        with color_columns[index]:

            symbol = {

                "갈색": "🟤",

                "파란색": "🔵",

                "보라색": "🟣"

            }[name]


            st.markdown(
                f"""
                <div class="shop-card">

                <div style="font-size:35px;">
                {symbol}
                </div>

                <br>

                <b>{name}</b>

                <br><br>

                {price:,}원

                </div>
                """,
                unsafe_allow_html=True
            )


            if name in st.session_state.owned_eye_color:

                if st.button(
                    "착용",
                    key=f"eye_color_use_{name}",
                    use_container_width=True
                ):

                    st.session_state.selected_eye_color = (
                        name
                    )

                    st.rerun()


            else:

                if st.button(
                    "구매",
                    key=f"eye_color_buy_{name}",
                    use_container_width=True
                ):

                    buy_cosmetic(
                        name,
                        price,
                        "eye_color"
                    )

                    st.rerun()


    # ========================================================
    # 상점을 이용하지 않고 넘어가기 가능
    # ========================================================

    st.write("")

    st.markdown("---")


    if st.button(
        "🌙 구매하지 않고 다음 밤으로 넘어가기",
        use_container_width=True
    ):

        st.session_state.night += 1

        start_night()

        st.rerun()


# ============================================================
# 25. 실제 게임
# ============================================================

else:

    patient = current_patient()


    # ========================================================
    # 상단 상태창
    # ========================================================

    s1, s2, s3, s4 = st.columns(
        4
    )


    with s1:

        st.markdown(
            f"""
            <div class="status-card">

            🌙 NIGHT

            <br>

            <b>
            {st.session_state.night}
            </b>

            </div>
            """,
            unsafe_allow_html=True
        )


    with s2:

        st.markdown(
            f"""
            <div class="status-card">

            PATIENT

            <br>

            <b>
            {st.session_state.current_case + 1}
            /
            {PATIENTS_PER_NIGHT}
            </b>

            </div>
            """,
            unsafe_allow_html=True
        )


    with s3:

        hearts = (
            "❤️"
            *
            st.session_state.health
        )


        st.markdown(
            f"""
            <div class="status-card">

            HEALTH

            <br>

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
                "### 🏥 병원 내부"
            )


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


            room1, room2 = st.columns(
                2
            )


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
    # 돈 표시
    # ========================================================

    st.caption(
        f"💰 보유 금액 : "
        f"{st.session_state.money:,}원"
    )


    # ========================================================
    # 현재 위치
    # ========================================================

    st.markdown(
        f"""
        <div class="location-box">

        📍 현재 위치 :
        <b>
        {st.session_state.location}
        </b>

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

        &nbsp;

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
    # 데스크
    # ========================================================

    if st.session_state.location == "데스크":

        st.markdown(
            "## 🖥️ 병원 데스크"
        )


        st.caption(
            "환자의 얼굴을 보고 병원 출입 여부를 결정하세요."
        )


        show_patient(
            patient
        )


        # 아직 판단 전
        if (
            not st.session_state.patient_admitted
            and
            not st.session_state.patient_rejected
        ):

            choice1, choice2 = st.columns(
                2
            )


            with choice1:

                if st.button(
                    "🏥 환자를 병원 안으로 들인다",
                    use_container_width=True
                ):

                    admit_patient()

                    st.rerun()


            with choice2:

                if st.button(
                    "🚫 환자의 출입을 거절한다",
                    use_container_width=True
                ):

                    reject_patient()

                    st.rerun()


        # ----------------------------------------------------
        # 입장을 허용한 경우
        # ----------------------------------------------------

        elif st.session_state.patient_admitted:

            st.markdown(
                """
                <div class="tutorial-box">

                <b>📍 TUTORIAL</b>

                <br><br>

                환자가 병원 안으로 들어왔습니다.

                <br><br>

                화면 위의
                <b>🗺️ 병원 지도</b>를 눌러

                <b>🛏️ 진료실</b>로 직접 이동하세요.

                </div>
                """,
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # 출입을 거절한 경우
        # ----------------------------------------------------

        elif st.session_state.patient_rejected:

            if patient["anomaly"]:

                st.markdown(
                    """
                    <div class="success-box">

                    <b>
                    🚨 변칙성 환자였습니다.
                    </b>

                    <br><br>

                    병원 출입을 성공적으로 차단했습니다.

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            else:

                st.markdown(
                    """
                    <div class="anomaly-box">

                    <b>
                    ⚠️ 정상 환자였습니다.
                    </b>

                    <br><br>

                    정상 환자를 거절했기 때문에
                    해당 환자에 대한 치료 급여는 받을 수 없습니다.

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
    # 진료실
    # ========================================================

    elif st.session_state.location == "진료실":

        st.markdown(
            "## 🛏️ 진료실"
        )


        if not st.session_state.patient_admitted:

            st.warning(
                "현재 진료실로 들어온 환자가 없습니다."
            )


        else:

            patient_col, info_col = st.columns(
                [1, 1]
            )


            with patient_col:

                show_patient(
                    patient
                )


            with info_col:

                st.markdown(
                    """
                    <div class="panel">

                    <h3>
                    👤 환자 진료
                    </h3>

                    환자가 진료실에서 기다리고 있습니다.

                    <br><br>

                    먼저 검사를 실시해 주세요.

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # 검사 전
            if not st.session_state.examined:

                if st.button(
                    "🔍 환자 검사",
                    use_container_width=True
                ):

                    examine_patient()

                    st.rerun()


            # 검사 후
            else:

                item1 = patient[
                    "items"
                ][0]

                item2 = patient[
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

                    ① {item1}

                    <br>

                    ② {item2}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # 치료 완료
                if st.session_state.completed:

                    if st.session_state.anomaly_revealed:

                        st.markdown(
                            """
                            <div class="anomaly-box">

                            <h3>
                            🚨 변칙성 환자입니다!
                            </h3>

                            물품을 적용하는 순간
                            변칙 반응이 발생했습니다.

                            <br><br>

                            ❤️ 체력 -1

                            <br><br>

                            또한 이 변칙성 환자를
                            진료실까지 들였기 때문에
                            오늘 급여에서
                            <b>200,000원</b>이 차감됩니다.

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    else:

                        st.markdown(
                            """
                            <div class="success-box">

                            <h3>
                            ✅ 정상 환자 치료 완료
                            </h3>

                            정상적으로 치료했습니다.

                            <br><br>

                            오늘 급여 계산 시
                            <b>600,000원</b>이 추가됩니다.

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


                # 치료 전
                else:

                    if not st.session_state.inventory:

                        st.markdown(
                            """
                            <div class="tutorial-box">

                            필요한 물품을 확인했습니다.

                            <br><br>

                            🗺️ <b>병원 지도</b>를 눌러
                            📦 <b>물품실</b>로 이동하세요.

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    else:

                        st.markdown(
                            "### 🎒 치료에 사용할 물품 선택"
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


    # ========================================================
    # 물품실
    # ========================================================

    elif st.session_state.location == "물품실":

        st.markdown(
            "## 📦 병원 물품실"
        )


        st.caption(
            "검사 결과를 기억하고 필요한 물품을 선택하세요."
        )


        rows = [

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
            rows
        ):

            cols = st.columns(
                len(row)
            )


            for item_number, item in enumerate(
                row
            ):

                with cols[
                    item_number
                ]:

                    st.markdown(
                        f"""
                        <div class="item-card">

                        <div style="font-size:36px;">
                        🧰
                        </div>

                        <br>

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

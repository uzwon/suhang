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

PATIENTS_PER_NIGHT = 5

NORMAL_REWARD = 100


# ============================================================
# 2. 전체 디자인
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   전체 병원 배경
============================================================ */

.stApp {
    background:
        linear-gradient(
            90deg,
            #e4ecee 0%,
            #e4ecee 73%,
            #d2dfe2 73%,
            #d2dfe2 100%
        );

    color: #263a43;
}


/* ============================================================
   오른쪽 병원 벽의 밤 창문
============================================================ */

.stApp::before {

    content: "";

    position: fixed;

    top: 105px;
    right: 35px;

    width: 260px;
    height: 225px;

    border: 12px solid #f1f5f6;

    border-radius: 8px;

    box-sizing: border-box;

    background:

        /* 달 */
        radial-gradient(
            circle at 77% 24%,
            #fff6bf 0px,
            #fff6bf 21px,
            transparent 22px
        ),

        /* 별 */
        radial-gradient(
            circle at 15% 17%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 31% 37%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 50% 20%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 66% 43%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 24% 63%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        linear-gradient(
            180deg,
            #071426 0%,
            #102949 60%,
            #1b405f 100%
        );

    box-shadow:
        inset 0 0 0 3px #b8c8cd,
        0 8px 24px rgba(0,0,0,0.18);

    z-index: 0;
}


/* 창문 중앙 세로틀 */
.stApp::after {

    content: "";

    position: fixed;

    top: 117px;
    right: 157px;

    width: 7px;
    height: 201px;

    background: #f1f5f6;

    z-index: 1;
}


/* ============================================================
   본문
============================================================ */

.block-container {

    position: relative;

    z-index: 2;

    max-width: 1020px;

    margin-left: 25px;

    margin-right: 315px;

    padding-top: 1.3rem;

    padding-bottom: 4rem;
}


/* ============================================================
   제목
============================================================ */

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


/* ============================================================
   상태창
============================================================ */

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


/* ============================================================
   현재 위치
============================================================ */

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


/* ============================================================
   일반 패널
============================================================ */

.panel {

    background: rgba(250,253,254,0.97);

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


/* ============================================================
   환자 사진
============================================================ */

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


/* ============================================================
   검사 결과
============================================================ */

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


/* ============================================================
   성공
============================================================ */

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


/* ============================================================
   변칙 경고
============================================================ */

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


/* ============================================================
   인벤토리
============================================================ */

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


/* ============================================================
   아이템
============================================================ */

.item-card {

    background: rgba(250,253,254,0.97);

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


/* ============================================================
   상점
============================================================ */

.shop-card {

    background: rgba(251,253,254,0.98);

    border: 1px solid #afc1c7;

    border-radius: 16px;

    padding: 18px;

    text-align: center;

    min-height: 150px;

    box-shadow: 0 6px 18px rgba(40,60,70,0.10);
}

.shop-card,
.shop-card * {

    color: #273b44 !important;
}


/* ============================================================
   캐릭터
============================================================ */

.character-card {

    background:

        linear-gradient(
            180deg,
            #eef4f6 0%,
            #dce8eb 100%
        );

    border-radius: 18px;

    border: 1px solid #abc0c7;

    padding: 22px;

    text-align: center;

    min-height: 245px;
}

.character-face {

    font-size: 75px;

    margin-bottom: 10px;
}

.character-accessory {

    font-size: 35px;

    margin-bottom: 6px;
}


/* ============================================================
   급여 정산
============================================================ */

.salary-box {

    background: #fff6d9;

    border-left: 7px solid #d8b84c;

    border-radius: 14px;

    padding: 20px;

    margin-top: 18px;

    line-height: 1.8;
}

.salary-box,
.salary-box * {

    color: #584e2c !important;
}


/* ============================================================
   지도
============================================================ */

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


/* ============================================================
   버튼
============================================================ */

.stButton > button {

    width: 100%;

    min-height: 48px;

    border-radius: 10px;

    font-weight: 800;
}


/* ============================================================
   기본 글씨
============================================================ */

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


/* multiselect */
div[data-baseweb="select"] * {

    color: #253941 !important;
}


/* ============================================================
   모바일
============================================================ */

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
            "환자는 두통과 어지럼증을 호소합니다. "
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
            "검사 결과만으로는 특별한 변칙이 확인되지 않습니다. "
            "필요한 처치를 준비하세요.",

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
            "최근 기억력 변화가 있어 인지 상태 확인을 위한 "
            "기본 평가 준비가 필요합니다.",

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
            "환자는 손의 감각 변화를 호소하고 있습니다. "
            "검사 단계에서는 특별한 변칙이 나타나지 않습니다.",

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
            "균형감과 반응 상태를 확인하기 위한 기본 검사가 필요합니다.",

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
            "환자는 지속적인 어지럼증을 호소합니다. "
            "현재 검사만으로는 변칙 여부를 알 수 없습니다.",

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
            "최근 집중력 변화가 있어 간단한 인지 평가가 필요합니다.",

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
            "손의 감각 및 반응 상태 확인을 위한 준비가 필요합니다.",

        "items": [
            "감각검사 카드",
            "반사검사 도구"
        ]
    }

]


# ============================================================
# 4. 물품 목록
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
# 5. 꾸미기 아이템
# ============================================================

SHOP_ITEMS = {

    "파란 가운": {
        "price": 0,
        "type": "coat",
        "symbol": "🩵"
    },

    "분홍 가운": {
        "price": 300,
        "type": "coat",
        "symbol": "🩷"
    },

    "보라 가운": {
        "price": 450,
        "type": "coat",
        "symbol": "💜"
    },

    "검정 가운": {
        "price": 600,
        "type": "coat",
        "symbol": "🖤"
    },

    "둥근 안경": {
        "price": 250,
        "type": "accessory",
        "symbol": "👓"
    },

    "별 배지": {
        "price": 200,
        "type": "badge",
        "symbol": "⭐"
    },

    "뇌 배지": {
        "price": 400,
        "type": "badge",
        "symbol": "🧠"
    }

}


# ============================================================
# 6. 전체 게임 최초 초기화
# ============================================================

def initialize_profile():

    if "money" not in st.session_state:

        st.session_state.money = 0


    if "owned_items" not in st.session_state:

        st.session_state.owned_items = [
            "파란 가운"
        ]


    if "selected_coat" not in st.session_state:

        st.session_state.selected_coat = (
            "파란 가운"
        )


    if "selected_accessory" not in st.session_state:

        st.session_state.selected_accessory = (
            "없음"
        )


    if "selected_badge" not in st.session_state:

        st.session_state.selected_badge = (
            "없음"
        )


    if "night" not in st.session_state:

        st.session_state.night = 1


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
        patient_indices[
            :PATIENTS_PER_NIGHT
        ]
    )


    st.session_state.current_case = 0

    st.session_state.location = "데스크"

    st.session_state.health = 3

    st.session_state.inventory = []

    st.session_state.patient_admitted = False

    st.session_state.examined = False

    st.session_state.completed = False

    st.session_state.anomaly_revealed = False

    st.session_state.message = ""

    st.session_state.normal_treated = 0

    st.session_state.anomalies_found = 0

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
            "환자 이미지가 아직 등록되지 않았습니다."
        )


# ============================================================
# 10. 장소 이동
# ============================================================

def move_room(room):

    st.session_state.location = room


# ============================================================
# 11. 환자 입장
# ============================================================

def admit_patient():

    st.session_state.patient_admitted = True

    st.session_state.location = "진료실"

    st.session_state.message = (
        "🏥 환자가 진료실로 이동했습니다."
    )


# ============================================================
# 12. 환자 검사
# ============================================================

def examine_patient():

    st.session_state.examined = True

    st.session_state.message = (
        "🔍 검사가 완료되었습니다. "
        "필요한 물품을 확인하세요."
    )


# ============================================================
# 13. 물품 가져오기
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
            "인벤토리는 최대 4개까지 보관할 수 있습니다."
        )

        return


    st.session_state.inventory.append(
        item
    )


# ============================================================
# 14. 물품 적용
# ============================================================

def apply_items(selected_items):

    patient = current_patient()


    if len(selected_items) != 2:

        st.warning(
            "적용할 물품 2개를 선택하세요."
        )

        return


    correct_items = set(
        patient["items"]
    )

    chosen_items = set(
        selected_items
    )


    if chosen_items != correct_items:

        st.session_state.message = (
            "❌ 필요한 물품 조합이 아닙니다. "
            "검사 결과를 다시 확인하세요."
        )

        return


    # --------------------------------------------------------
    # 물품이 맞으면 치료 진행
    # --------------------------------------------------------

    st.session_state.completed = True


    # --------------------------------------------------------
    # 변칙 환자
    # --------------------------------------------------------

    if patient["anomaly"]:

        st.session_state.health -= 1

        st.session_state.anomaly_revealed = True

        st.session_state.anomalies_found += 1

        st.session_state.message = (
            "🚨 변칙성 환자입니다! "
            "처치 과정에서 변칙 반응이 발생해 "
            "당신이 데미지를 입었습니다."
        )


    # --------------------------------------------------------
    # 정상 환자
    # --------------------------------------------------------

    else:

        st.session_state.normal_treated += 1

        st.session_state.message = (
            "✅ 정상 환자 치료 완료!"
        )


# ============================================================
# 15. 다음 환자
# ============================================================

def next_patient():

    st.session_state.current_case += 1


    # 체력이 없으면 밤 종료
    if st.session_state.health <= 0:

        st.session_state.night_finished = True

        return


    # 모든 환자 처리 완료
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

    st.session_state.examined = False

    st.session_state.completed = False

    st.session_state.anomaly_revealed = False

    st.session_state.message = ""


# ============================================================
# 16. 급여 받기
# ============================================================

def receive_salary():

    if st.session_state.salary_received:

        return


    salary = (
        st.session_state.normal_treated
        *
        NORMAL_REWARD
    )


    st.session_state.money += salary

    st.session_state.last_salary = salary

    st.session_state.salary_received = True


# ============================================================
# 17. 아이템 구매
# ============================================================

def buy_item(item_name):

    info = SHOP_ITEMS[
        item_name
    ]


    if item_name in st.session_state.owned_items:

        return


    if st.session_state.money < info["price"]:

        st.warning(
            "돈이 부족합니다."
        )

        return


    st.session_state.money -= (
        info["price"]
    )

    st.session_state.owned_items.append(
        item_name
    )


# ============================================================
# 18. 캐릭터 표시
# ============================================================

def show_character():

    coat = SHOP_ITEMS[
        st.session_state.selected_coat
    ]["symbol"]


    accessory = ""

    badge = ""


    if (
        st.session_state.selected_accessory
        != "없음"
    ):

        accessory = SHOP_ITEMS[
            st.session_state.selected_accessory
        ]["symbol"]


    if (
        st.session_state.selected_badge
        != "없음"
    ):

        badge = SHOP_ITEMS[
            st.session_state.selected_badge
        ]["symbol"]


    st.markdown(
        f"""
        <div class="character-card">

        <div class="character-face">
        🧑‍⚕️
        </div>

        <div style="font-size:42px;">
        {coat}
        </div>

        <div class="character-accessory">
        {accessory}
        </div>

        <div style="font-size:30px;">
        {badge}
        </div>

        <br>

        <b>당직 의사</b>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 19. 프로필 초기화
# ============================================================

initialize_profile()


if "game_started" not in st.session_state:

    st.session_state.game_started = False


# ============================================================
# 20. 제목
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
# 21. 처음 시작 화면
# ============================================================

if not st.session_state.game_started:

    left, right = st.columns(
        [1.8, 1]
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

            찾아오는 환자를 병원 안으로 들이고
            진료실에서 검사를 진행하세요.

            <br><br>

            검사 결과에 따라 필요한 물품 두 가지를
            물품실에서 준비하여 환자에게 적용해야 합니다.

            <br><br>

            하지만 환자들 중 일부는
            <b>변칙성 환자</b>입니다.

            <br><br>

            변칙성 여부는 치료 전까지 알 수 없습니다.

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
# 22. 밤 종료 화면
# ============================================================

elif st.session_state.night_finished:

    if not st.session_state.salary_received:

        receive_salary()


    left, right = st.columns(
        [1.3, 1]
    )


    with left:

        st.markdown(
            f"""
            <div class="salary-box">

            <h2>
            🌅 NIGHT {st.session_state.night} 종료
            </h2>

            정상적으로 치료한 환자 :
            <b>{st.session_state.normal_treated}명</b>

            <br><br>

            발견된 변칙 환자 :
            <b>{st.session_state.anomalies_found}명</b>

            <br><br>

            급여 :

            <b>
            {st.session_state.last_salary}원
            </b>

            <br><br>

            현재 보유 금액 :

            <b>
            {st.session_state.money}원
            </b>

            </div>
            """,
            unsafe_allow_html=True
        )


    with right:

        show_character()


    st.markdown(
        "## 🛍️ 캐릭터 꾸미기 상점"
    )


    # ========================================================
    # 가운 상점
    # ========================================================

    st.markdown(
        "### 🥼 가운"
    )


    coat_names = [

        name

        for name, info
        in SHOP_ITEMS.items()

        if info["type"] == "coat"
    ]


    coat_columns = st.columns(
        len(coat_names)
    )


    for index, item_name in enumerate(
        coat_names
    ):

        item = SHOP_ITEMS[
            item_name
        ]


        with coat_columns[
            index
        ]:

            st.markdown(
                f"""
                <div class="shop-card">

                <div style="font-size:40px;">
                {item["symbol"]}
                </div>

                <br>

                <b>
                {item_name}
                </b>

                <br><br>

                {item["price"]}원

                </div>
                """,
                unsafe_allow_html=True
            )


            if (
                item_name
                in st.session_state.owned_items
            ):

                if st.button(
                    "착용",
                    key=f"wear_{item_name}",
                    use_container_width=True
                ):

                    st.session_state.selected_coat = (
                        item_name
                    )

                    st.rerun()


            else:

                if st.button(
                    "구매",
                    key=f"buy_{item_name}",
                    use_container_width=True
                ):

                    buy_item(
                        item_name
                    )

                    st.rerun()


    # ========================================================
    # 액세서리
    # ========================================================

    st.markdown(
        "### 👓 액세서리 / 배지"
    )


    other_items = [

        name

        for name, info
        in SHOP_ITEMS.items()

        if info["type"]
        != "coat"
    ]


    columns = st.columns(
        len(other_items)
    )


    for index, item_name in enumerate(
        other_items
    ):

        item = SHOP_ITEMS[
            item_name
        ]


        with columns[
            index
        ]:

            st.markdown(
                f"""
                <div class="shop-card">

                <div style="font-size:40px;">
                {item["symbol"]}
                </div>

                <br>

                <b>
                {item_name}
                </b>

                <br><br>

                {item["price"]}원

                </div>
                """,
                unsafe_allow_html=True
            )


            if (
                item_name
                in st.session_state.owned_items
            ):

                if st.button(
                    "착용",
                    key=f"use_{item_name}",
                    use_container_width=True
                ):

                    if (
                        item["type"]
                        == "accessory"
                    ):

                        st.session_state.selected_accessory = (
                            item_name
                        )


                    elif (
                        item["type"]
                        == "badge"
                    ):

                        st.session_state.selected_badge = (
                            item_name
                        )


                    st.rerun()


            else:

                if st.button(
                    "구매",
                    key=f"shop_{item_name}",
                    use_container_width=True
                ):

                    buy_item(
                        item_name
                    )

                    st.rerun()


    st.write("")


    if st.button(
        "🌙 다음 밤 시작",
        use_container_width=True
    ):

        st.session_state.night += 1

        start_night()

        st.rerun()


# ============================================================
# 23. 실제 게임
# ============================================================

else:

    patient = current_patient()


    # ========================================================
    # 상단 상태
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
    # 지도
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
                key="desk_move",
                use_container_width=True
            ):

                move_room(
                    "데스크"
                )

                st.rerun()


            rooms = st.columns(
                2
            )


            with rooms[0]:

                st.markdown(
                    """
                    <div class="map-room">
                    🛏️ 진료실
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                if st.button(
                    "진료실 이동",
                    key="treatment_move",
                    use_container_width=True
                ):

                    move_room(
                        "진료실"
                    )

                    st.rerun()


            with rooms[1]:

                st.markdown(
                    """
                    <div class="map-room">
                    📦 물품실
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                if st.button(
                    "물품실 이동",
                    key="supply_move",
                    use_container_width=True
                ):

                    move_room(
                        "물품실"
                    )

                    st.rerun()


    # ========================================================
    # 돈
    # ========================================================

    st.caption(
        f"💰 현재 보유 금액 : "
        f"{st.session_state.money}원"
    )


    # ========================================================
    # 위치
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
    # 메시지
    # ========================================================

    if st.session_state.message:

        st.info(
            st.session_state.message
        )


    # ========================================================
    # 데스크
    # ========================================================

    if (
        st.session_state.location
        == "데스크"
    ):

        st.markdown(
            "## 🖥️ 병원 데스크"
        )


        st.caption(
            "새로운 환자가 병원에 도착했습니다."
        )


        show_patient(
            patient
        )


        if not st.session_state.patient_admitted:

            if st.button(
                "🏥 환자를 병원 안으로 들인다",
                use_container_width=True
            ):

                admit_patient()

                st.rerun()


        else:

            st.info(
                "환자는 이미 진료실로 이동했습니다."
            )


    # ========================================================
    # 진료실
    # ========================================================

    elif (
        st.session_state.location
        == "진료실"
    ):

        st.markdown(
            "## 🛏️ 진료실"
        )


        if not st.session_state.patient_admitted:

            st.warning(
                "현재 진료실에 환자가 없습니다."
            )


        else:

            left, right = st.columns(
                [1, 1.05]
            )


            with left:

                show_patient(
                    patient
                )


            with right:

                st.markdown(
                    """
                    <div class="panel">

                    <h3>
                    👤 환자 진료
                    </h3>

                    환자가 진료를 기다리고 있습니다.

                    <br><br>

                    먼저 검사를 진행하세요.

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # =================================================
            # 검사 전
            # =================================================

            if not st.session_state.examined:

                if st.button(
                    "🔍 환자 검사하기",
                    use_container_width=True
                ):

                    examine_patient()

                    st.rerun()


            # =================================================
            # 검사 후
            # =================================================

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


                # =================================================
                # 치료 완료
                # =================================================

                if st.session_state.completed:

                    if st.session_state.anomaly_revealed:

                        st.markdown(
                            """
                            <div class="anomaly-box">

                            <h3>
                            🚨 변칙성 환자입니다!
                            </h3>

                            치료를 적용하는 순간
                            비정상적인 반응이 나타났습니다.

                            <br><br>

                            당신은 변칙 반응의 영향으로
                            <b>체력 1</b>을 잃었습니다.

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

                            환자에게 필요한 처치를
                            정상적으로 완료했습니다.

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


                # =================================================
                # 치료 전
                # =================================================

                else:

                    if not st.session_state.inventory:

                        st.warning(
                            "🎒 필요한 물품을 가지러 "
                            "병원 지도에서 물품실로 이동하세요."
                        )


                    else:

                        selected_items = st.multiselect(
                            "환자에게 적용할 물품 2개를 선택하세요.",
                            options=st.session_state.inventory,
                            max_selections=2
                        )


                        if st.button(
                            "🩺 물품 적용",
                            use_container_width=True
                        ):

                            apply_items(
                                selected_items
                            )

                            st.rerun()


    # ========================================================
    # 물품실
    # ========================================================

    elif (
        st.session_state.location
        == "물품실"
    ):

        st.markdown(
            "## 📦 병원 물품실"
        )


        st.caption(
            "검사 결과를 기억하고 필요한 물품을 가져가세요."
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


        for row_index, row in enumerate(
            rows
        ):

            cols = st.columns(
                len(row)
            )


            for index, item in enumerate(
                row
            ):

                with cols[
                    index
                ]:

                    st.markdown(
                        f"""
                        <div class="item-card">

                        <div style="font-size:35px;">
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
                        key=f"item_{row_index}_{index}",
                        use_container_width=True
                    ):

                        add_item(
                            item
                        )

                        st.rerun()

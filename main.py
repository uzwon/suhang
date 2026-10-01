import streamlit as st
import random
from pathlib import Path


# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="NIGHT SHIFT : WARD 13",
    page_icon="🏥",
    layout="wide"
)

IMAGE_FOLDER = Path("images")

PATIENTS_PER_NIGHT = 6

NORMAL_REWARD = 600_000
ANOMALY_PENALTY = 200_000
ANOMALY_BLOCK_BONUS = 150_000

EXTRA_LIFE_PRICE = 3_100_000


# ============================================================
# 디자인
# ============================================================

st.markdown("""
<style>

/* 전체 병원 */
.stApp {
    background:
        linear-gradient(
            90deg,
            #dfe9eb 0%,
            #dfe9eb 72%,
            #c9d7db 72%,
            #c9d7db 100%
        );
}

/* 오른쪽 야간 병원 창문 */
.stApp::before {
    content:"";

    position:fixed;

    width:260px;
    height:235px;

    right:30px;
    top:90px;

    border:12px solid #edf3f5;
    border-radius:8px;

    background:

        radial-gradient(
            circle at 76% 23%,
            #fff2ad 0px,
            #fff2ad 22px,
            transparent 23px
        ),

        radial-gradient(
            circle at 15% 20%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 35% 35%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 55% 18%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 65% 55%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        linear-gradient(
            180deg,
            #06111e,
            #102b49 60%,
            #1d405c
        );

    box-shadow:
        inset 0 0 0 3px #b9c8cd,
        0 12px 30px rgba(0,0,0,0.18);

    z-index:0;
}

/* 창문 가운데 틀 */
.stApp::after {
    content:"";

    position:fixed;

    width:7px;
    height:211px;

    right:157px;
    top:102px;

    background:#edf3f5;

    z-index:1;
}


/* 실제 게임 영역 */
.block-container {
    position:relative;
    z-index:5;

    max-width:1030px;

    margin-left:20px;
    margin-right:315px;

    padding-top:1.3rem;
    padding-bottom:4rem;
}


/* 타이틀 */
.main-title {
    font-size:42px;
    font-weight:900;

    color:#213741;

    letter-spacing:2px;
}

.subtitle {
    color:#617983;
    margin-bottom:17px;
}


/* 상태 표시 */
.status {
    background:#263b46;

    border:1px solid #435f6b;

    border-radius:14px;

    padding:13px;

    text-align:center;

    box-shadow:0 6px 18px rgba(40,60,70,0.15);
}

.status,
.status * {
    color:white !important;
}


/* 기본 카드 */
.card {
    background:rgba(250,253,254,0.97);

    border:1px solid #adc0c7;

    border-radius:18px;

    padding:22px;

    color:#263a43;

    box-shadow:0 8px 24px rgba(40,60,70,0.11);
}

.card,
.card * {
    color:#263a43 !important;
}


/* 현재 장소 */
.location {
    background:#f5fafb;

    border-left:6px solid #6d99a9;

    padding:15px 18px;

    border-radius:14px;

    margin:15px 0;

    box-shadow:0 5px 16px rgba(40,60,70,0.08);
}

.location,
.location * {
    color:#263b44 !important;
}


/* 환자 사진 */
.patient-photo {
    min-height:390px;

    display:flex;

    justify-content:center;
    align-items:center;

    background:
        linear-gradient(
            #e4edef,
            #d2e1e4
        );

    border:1px solid #a1b5bc;

    border-radius:18px;

    font-size:100px;

    box-shadow:0 7px 20px rgba(40,60,70,0.10);
}


/* 이벤트 */
.event-box {
    background:#fff5d7;

    border-left:7px solid #daaF42;

    border-radius:14px;

    padding:17px;

    margin:13px 0;
}

.event-box,
.event-box * {
    color:#584d29 !important;
}


/* 튜토리얼 */
.guide-box {
    background:#e9f2fa;

    border-left:7px solid #6489ae;

    border-radius:14px;

    padding:18px;

    margin:15px 0;
}

.guide-box,
.guide-box * {
    color:#304c61 !important;
}


/* 성공 */
.success-box {
    background:#e7f5ed;

    border-left:7px solid #5a9d75;

    border-radius:14px;

    padding:18px;

    margin-top:15px;
}

.success-box,
.success-box * {
    color:#2c503a !important;
}


/* 변칙 */
.anomaly-box {
    background:#f9e8ec;

    border:2px solid #bd5968;
    border-left:8px solid #a93448;

    border-radius:14px;

    padding:19px;

    margin-top:15px;
}

.anomaly-box,
.anomaly-box * {
    color:#692f39 !important;
}


/* 위험도 */
.threat-low {
    color:#41745a;
    font-weight:900;
}

.threat-mid {
    color:#a07527;
    font-weight:900;
}

.threat-high {
    color:#9b3543;
    font-weight:900;
}


/* 인벤토리 */
.inventory {
    background:#253b46;

    border-radius:14px;

    padding:14px 18px;

    margin-bottom:14px;
}

.inventory,
.inventory * {
    color:white !important;
}


/* 아이템 */
.item-card {
    background:#f8fbfc;

    border:1px solid #adc0c7;

    border-radius:15px;

    padding:18px;

    min-height:115px;

    text-align:center;

    box-shadow:0 5px 15px rgba(40,60,70,0.08);
}

.item-card,
.item-card * {
    color:#273c45 !important;
}


/* 지도 */
.map-card {
    background:#eef4f6;

    border:1px solid #afc0c7;

    border-radius:12px;

    padding:11px;

    text-align:center;

    font-weight:800;

    margin-bottom:6px;
}


/* 상점 */
.shop {
    background:#f8fbfc;

    border:1px solid #adc0c7;

    border-radius:15px;

    padding:17px;

    min-height:145px;

    text-align:center;
}

.shop,
.shop * {
    color:#263b44 !important;
}


/* 캐릭터 */
.character {
    background:
        linear-gradient(
            #f8fcfd,
            #e5eef1
        );

    border:1px solid #adc1c7;

    border-radius:18px;

    padding:20px;

    text-align:center;
}

.character-icon {
    font-size:80px;
}


/* 급여 */
.salary {
    background:#fff5d8;

    border-left:7px solid #d4ad3d;

    border-radius:15px;

    padding:21px;

    line-height:1.9;
}

.salary,
.salary * {
    color:#574c29 !important;
}


/* 버튼 */
.stButton > button {
    width:100%;

    min-height:48px;

    border-radius:10px;

    font-weight:800;
}


/* 글씨 */
h1,h2,h3,h4 {
    color:#263b44 !important;
}

p,label {
    color:#2d434c;
}

div[data-baseweb="select"] * {
    color:#263b44 !important;
}


/* 모바일 */
@media(max-width:900px) {

    .stApp::before,
    .stApp::after {
        display:none;
    }

    .block-container {
        margin:auto;
        max-width:95%;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 환자
# ============================================================

PATIENTS = [

    {
        "id":1,
        "image":"patient01.png",

        "anomaly":False,

        "public_clue":
            "눈에 띄는 이상은 없다.",

        "verification":
            "병원 예약 정보와 신원 정보가 모두 일치한다.",

        "exam":
            "신경계 기본 상태와 활력징후 확인이 필요하다.",

        "items":[
            "신경학적 검사 키트",
            "활력징후 기록 카드"
        ]
    },


    {
        "id":2,
        "image":"patient02.png",

        "anomaly":True,

        "public_clue":
            "환자가 거의 눈을 깜빡이지 않는 것처럼 보인다.",

        "verification":
            "예약된 사진과 현재 환자의 얼굴 특징 일부가 일치하지 않는다.",

        "exam":
            "검사 단계에서는 명확한 변칙 반응이 나타나지 않는다.",

        "items":[
            "감각검사 카드",
            "신경학적 검사 키트"
        ]
    },


    {
        "id":3,
        "image":"patient03.png",

        "anomaly":False,

        "public_clue":
            "피곤해 보이지만 특별한 이상은 없다.",

        "verification":
            "접수 기록과 예약 시간이 모두 정상적으로 확인된다.",

        "exam":
            "인지 상태와 기본 반응 확인이 필요하다.",

        "items":[
            "인지검사 카드",
            "MRI 검사 안내서"
        ]
    },


    {
        "id":4,
        "image":"patient04.png",

        "anomaly":True,

        "public_clue":
            "환자 사진이 순간적으로 흐려 보이는 느낌이 든다.",

        "verification":
            "CCTV에 환자가 병원 입구로 들어오는 장면이 기록되어 있지 않다.",

        "exam":
            "감각과 반응 검사가 필요하지만 검사만으로 변칙 여부는 확인되지 않는다.",

        "items":[
            "감각검사 카드",
            "반사검사 도구"
        ]
    },


    {
        "id":5,
        "image":"patient05.png",

        "anomaly":False,

        "public_clue":
            "표정이 긴장되어 있으나 외형적 특이점은 없다.",

        "verification":
            "신원 정보와 예약 기록이 정확히 일치한다.",

        "exam":
            "반응과 신경 상태 확인이 필요하다.",

        "items":[
            "반사검사 도구",
            "신경학적 검사 키트"
        ]
    },


    {
        "id":6,
        "image":"patient06.png",

        "anomaly":True,

        "public_clue":
            "환자의 모습이 어딘가 부자연스럽지만 정확히 설명하기 어렵다.",

        "verification":
            "오늘 병원 예약자 명단에 존재하지 않는 사람이다.",

        "exam":
            "검사에서는 일반 환자와 비슷한 반응이 나타난다.",

        "items":[
            "활력징후 기록 카드",
            "MRI 검사 안내서"
        ]
    },


    {
        "id":7,
        "image":"patient07.png",

        "anomaly":False,

        "public_clue":
            "평범한 모습의 환자다.",

        "verification":
            "접수·예약·신원 기록이 모두 일치한다.",

        "exam":
            "인지 상태와 활력징후 기록이 필요하다.",

        "items":[
            "인지검사 카드",
            "활력징후 기록 카드"
        ]
    },


    {
        "id":8,
        "image":"patient08.png",

        "anomaly":False,

        "public_clue":
            "불안해 보이지만 특별한 외형적 이상은 없다.",

        "verification":
            "예약 정보 및 환자 번호가 정상이다.",

        "exam":
            "감각과 반응 확인이 필요하다.",

        "items":[
            "감각검사 카드",
            "반사검사 도구"
        ]
    }

]


# ============================================================
# 물품
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
# 야간 랜덤 이벤트
# ============================================================

EVENTS = [

    {
        "name":"평온한 병원",

        "text":
            "병원이 평온하다. 특별한 방해 요소는 없다.",

        "effect":"normal"
    },


    {
        "name":"복도 조명 깜빡임",

        "text":
            "복도 조명이 계속 깜빡인다. 오늘 환자들의 얼굴이 평소보다 불분명하게 느껴진다.",

        "effect":"dark"
    },


    {
        "name":"CCTV 오류",

        "text":
            "보안 시스템 일부에 오류가 발생했다. 이번 환자는 추가 조회를 사용할 수 없다.",

        "effect":"no_check"
    },


    {
        "name":"이상한 방송",

        "text":
            "병원 방송에서 알아들을 수 없는 잡음이 들린다. 변칙 위험도가 증가했다.",

        "effect":"threat"
    },


    {
        "name":"응급 호출",

        "text":
            "다른 병동의 호출 때문에 시간이 부족하다. 신중하게 판단해야 한다.",

        "effect":"rush"
    }

]


# ============================================================
# 캐릭터 꾸미기
# ============================================================

HAIRS = {

    "단발":0,

    "긴 머리":1_200_000,

    "포니테일":1_500_000

}


EYE_SHAPES = {

    "둥근 눈":0,

    "웃는 눈":900_000,

    "날카로운 눈":1_100_000

}


EYE_COLORS = {

    "갈색":0,

    "파란색":800_000,

    "보라색":1_000_000

}


# ============================================================
# 기본 계정
# ============================================================

def initialize_profile():

    defaults = {

        "money":0,

        "night":1,

        "owned_hair":["단발"],

        "owned_eye_shape":["둥근 눈"],

        "owned_eye_color":["갈색"],

        "hair":"단발",

        "eye_shape":"둥근 눈",

        "eye_color":"갈색",

        "extra_life":0,

        "game_started":False

    }


    for key,value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ============================================================
# 밤 시작
# ============================================================

def start_night():

    patient_order = list(
        range(
            len(PATIENTS)
        )
    )

    random.shuffle(
        patient_order
    )


    st.session_state.patients = (
        patient_order[:PATIENTS_PER_NIGHT]
    )


    st.session_state.case = 0

    st.session_state.location = "데스크"

    st.session_state.health = (
        3 + st.session_state.extra_life
    )

    st.session_state.extra_life = 0


    st.session_state.inventory = []

    st.session_state.admitted = False

    st.session_state.rejected = False

    st.session_state.examined = False

    st.session_state.completed = False

    st.session_state.anomaly_revealed = False

    st.session_state.penalty_registered = False

    st.session_state.checked = False


    st.session_state.normal_treated = 0

    st.session_state.anomalies_admitted = 0

    st.session_state.anomalies_blocked = 0

    st.session_state.normal_rejected = 0


    st.session_state.check_tokens = 2

    st.session_state.threat = 0


    st.session_state.current_event = (
        random.choice(EVENTS)
    )


    st.session_state.message = ""

    st.session_state.night_finished = False

    st.session_state.salary_done = False

    st.session_state.game_started = True


# ============================================================
# 현재 환자
# ============================================================

def patient():

    if st.session_state.case >= len(
        st.session_state.patients
    ):

        return None


    index = (
        st.session_state.patients[
            st.session_state.case
        ]
    )


    return PATIENTS[index]


# ============================================================
# 환자 이미지
# ============================================================

def patient_image(p):

    path = (
        IMAGE_FOLDER
        /
        p["image"]
    )


    if path.exists():

        st.image(
            str(path),
            use_container_width=True
        )


    else:

        st.markdown(
            """
            <div class="patient-photo">
            👤
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 장소 이동
# ============================================================

def move(room):

    p = patient()


    if (
        room == "진료실"
        and
        st.session_state.admitted
        and
        p["anomaly"]
        and
        not st.session_state.penalty_registered
    ):

        st.session_state.anomalies_admitted += 1

        st.session_state.penalty_registered = True

        st.session_state.threat += 15


    st.session_state.location = room


# ============================================================
# 추가 기록 확인
# ============================================================

def verify_patient():

    event = st.session_state.current_event


    if event["effect"] == "no_check":

        st.session_state.message = (
            "📵 CCTV와 기록 서버가 현재 작동하지 않습니다."
        )

        return


    if st.session_state.check_tokens <= 0:

        st.session_state.message = (
            "⚠️ 오늘 사용할 수 있는 추가 조회권을 모두 사용했습니다."
        )

        return


    st.session_state.check_tokens -= 1

    st.session_state.checked = True


# ============================================================
# 환자 입장
# ============================================================

def admit():

    st.session_state.admitted = True

    st.session_state.message = (
        "🏥 환자의 병원 출입을 허용했습니다."
    )


# ============================================================
# 환자 거절
# ============================================================

def reject():

    p = patient()


    st.session_state.rejected = True

    st.session_state.completed = True


    if p["anomaly"]:

        st.session_state.anomalies_blocked += 1

        st.session_state.threat = max(
            0,
            st.session_state.threat - 10
        )

        st.session_state.message = (
            "🚨 출입을 차단했습니다. "
            "확인 결과 변칙 환자였습니다."
        )


    else:

        st.session_state.normal_rejected += 1

        st.session_state.message = (
            "⚠️ 정상 환자를 거절했습니다."
        )


# ============================================================
# 검사
# ============================================================

def examine():

    st.session_state.examined = True

    st.session_state.message = (
        "🔍 검사 완료. 필요한 물품을 확인하세요."
    )


# ============================================================
# 물품 가져오기
# ============================================================

def take_item(item):

    if item in st.session_state.inventory:

        return


    if len(st.session_state.inventory) >= 4:

        st.session_state.message = (
            "🎒 인벤토리는 최대 4칸입니다."
        )

        return


    st.session_state.inventory.append(
        item
    )


# ============================================================
# 치료
# ============================================================

def treat(selected):

    p = patient()


    if len(selected) != 2:

        st.session_state.message = (
            "⚠️ 물품 두 개를 선택하세요."
        )

        return


    if set(selected) != set(
        p["items"]
    ):

        st.session_state.message = (
            "❌ 필요한 물품 조합이 아닙니다."
        )

        return


    st.session_state.completed = True


    if p["anomaly"]:

        st.session_state.health -= 1

        st.session_state.threat += 25

        st.session_state.anomaly_revealed = True

        st.session_state.message = (
            "🚨 변칙 반응 발생!"
        )


    else:

        st.session_state.normal_treated += 1

        st.session_state.message = (
            "✅ 정상 환자 처치 완료!"
        )


# ============================================================
# 다음 환자
# ============================================================

def next_patient():

    st.session_state.case += 1


    if (
        st.session_state.case
        >= PATIENTS_PER_NIGHT
        or
        st.session_state.health <= 0
    ):

        st.session_state.night_finished = True

        return


    st.session_state.location = "데스크"

    st.session_state.inventory = []

    st.session_state.admitted = False

    st.session_state.rejected = False

    st.session_state.examined = False

    st.session_state.completed = False

    st.session_state.anomaly_revealed = False

    st.session_state.penalty_registered = False

    st.session_state.checked = False


    st.session_state.current_event = (
        random.choice(EVENTS)
    )


    if (
        st.session_state.current_event["effect"]
        == "threat"
    ):

        st.session_state.threat += 10


    st.session_state.message = ""


# ============================================================
# 급여
# ============================================================

def calculate_salary():

    if st.session_state.salary_done:

        return


    normal_pay = (
        st.session_state.normal_treated
        *
        NORMAL_REWARD
    )


    anomaly_penalty = (
        st.session_state.anomalies_admitted
        *
        ANOMALY_PENALTY
    )


    block_bonus = (
        st.session_state.anomalies_blocked
        *
        ANOMALY_BLOCK_BONUS
    )


    total = max(
        0,
        normal_pay
        -
        anomaly_penalty
        +
        block_bonus
    )


    st.session_state.normal_pay = normal_pay

    st.session_state.anomaly_penalty = anomaly_penalty

    st.session_state.block_bonus = block_bonus

    st.session_state.salary = total


    st.session_state.money += total

    st.session_state.salary_done = True


# ============================================================
# 구매
# ============================================================

def buy(name, price, category):

    if st.session_state.money < price:

        st.warning(
            "돈이 부족합니다."
        )

        return


    if category == "hair":

        if name not in st.session_state.owned_hair:

            st.session_state.owned_hair.append(
                name
            )


    elif category == "eye_shape":

        if name not in st.session_state.owned_eye_shape:

            st.session_state.owned_eye_shape.append(
                name
            )


    elif category == "eye_color":

        if name not in st.session_state.owned_eye_color:

            st.session_state.owned_eye_color.append(
                name
            )


    st.session_state.money -= price


# ============================================================
# 목숨 구매
# ============================================================

def buy_life():

    if st.session_state.money < EXTRA_LIFE_PRICE:

        st.warning(
            "돈이 부족합니다."
        )

        return


    st.session_state.money -= (
        EXTRA_LIFE_PRICE
    )

    st.session_state.extra_life += 1


# ============================================================
# 캐릭터
# ============================================================

def character():

    hair_icon = {

        "단발":"💇🏻‍♀️",

        "긴 머리":"👩🏻",

        "포니테일":"👱🏻‍♀️"

    }[
        st.session_state.hair
    ]


    eye = {

        "둥근 눈":"● ●",

        "웃는 눈":"⌒ ⌒",

        "날카로운 눈":"◢ ◣"

    }[
        st.session_state.eye_shape
    ]


    eye_color = {

        "갈색":"🟤",

        "파란색":"🔵",

        "보라색":"🟣"

    }[
        st.session_state.eye_color
    ]


    st.markdown(
        f"""
        <div class="character">

        <div class="character-icon">
        {hair_icon}
        </div>

        <b>당직 의사</b>

        <br><br>

        머리 : {st.session_state.hair}

        <br>

        눈 : {eye}

        <br>

        눈 색 : {eye_color}

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 초기화
# ============================================================

initialize_profile()


# ============================================================
# 제목
# ============================================================

st.markdown(
    """
    <div class="main-title">
    NIGHT SHIFT : WARD 13
    </div>

    <div class="subtitle">
    22:00 ─ 06:00 · 야간 병원 당직
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 처음 화면
# ============================================================

if not st.session_state.game_started:

    a,b = st.columns(
        [1.7,1]
    )


    with a:

        st.markdown(
            f"""
            <div class="card">

            <h2>
            🌙 NIGHT {st.session_state.night}
            </h2>

            오늘 밤에도 병원에는
            환자들이 찾아옵니다.

            <br><br>

            하지만 모든 사람이
            진짜 환자인 것은 아닙니다.

            <br><br>

            얼굴과 행동을 관찰하고,
            필요하다면 제한된
            <b>추가 기록 조회권</b>을 사용하세요.

            <br><br>

            정상 환자를 치료하면 급여를 받지만,
            변칙 환자를 진료실까지 들이면
            병원의 위험도와 감봉이 증가합니다.

            </div>
            """,
            unsafe_allow_html=True
        )


    with b:

        character()


    if st.button(
        "🌙 야간 근무 시작",
        use_container_width=True
    ):

        start_night()

        st.rerun()


# ============================================================
# 밤 종료
# ============================================================

elif st.session_state.night_finished:

    calculate_salary()


    st.markdown(
        f"""
        <div class="salary">

        <h2>
        🌅 NIGHT {st.session_state.night} 종료
        </h2>

        정상 치료 :
        <b>{st.session_state.normal_treated}명</b>

        <br>

        정상 치료 급여 :
        <b>{st.session_state.normal_pay:,}원</b>

        <br><br>

        진료실에 들어온 변칙 :
        <b>{st.session_state.anomalies_admitted}명</b>

        <br>

        변칙 감봉 :
        <b>-{st.session_state.anomaly_penalty:,}원</b>

        <br><br>

        출입 차단 성공 :
        <b>{st.session_state.anomalies_blocked}명</b>

        <br>

        보안 보너스 :
        <b>+{st.session_state.block_bonus:,}원</b>

        <br><br>

        ──────────────────

        <br>

        오늘 지급액 :
        <b>{st.session_state.salary:,}원</b>

        <br>

        현재 보유 금액 :
        <b>{st.session_state.money:,}원</b>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        "## 🛍️ 야간 상점"
    )

    st.caption(
        "아무것도 사지 않고 바로 다음 밤으로 넘어가도 됩니다."
    )


    # --------------------------------------------------------
    # 목숨
    # --------------------------------------------------------

    c1,c2 = st.columns(2)


    with c1:

        st.markdown(
            f"""
            <div class="shop">

            <div style="font-size:42px;">
            ❤️
            </div>

            <b>추가 목숨 +1</b>

            <br><br>

            다음 밤에 체력이 1 증가합니다.

            <br><br>

            {EXTRA_LIFE_PRICE:,}원

            </div>
            """,
            unsafe_allow_html=True
        )


        if st.button(
            "❤️ 구매",
            use_container_width=True
        ):

            buy_life()

            st.rerun()


    with c2:

        character()


    # --------------------------------------------------------
    # 머리
    # --------------------------------------------------------

    st.markdown(
        "### 💇 머리"
    )


    cols = st.columns(3)


    for i,(name,price) in enumerate(
        HAIRS.items()
    ):

        with cols[i]:

            st.markdown(
                f"""
                <div class="shop">

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
                    key=f"hair_{name}",
                    use_container_width=True
                ):

                    st.session_state.hair = name

                    st.rerun()


            else:

                if st.button(
                    "구매",
                    key=f"buyhair_{name}",
                    use_container_width=True
                ):

                    buy(
                        name,
                        price,
                        "hair"
                    )

                    st.rerun()


    # --------------------------------------------------------
    # 눈 모양
    # --------------------------------------------------------

    st.markdown(
        "### 👁️ 눈 모양"
    )


    cols = st.columns(3)


    for i,(name,price) in enumerate(
        EYE_SHAPES.items()
    ):

        with cols[i]:

            st.markdown(
                f"""
                <div class="shop">

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
                    key=f"eye_{name}",
                    use_container_width=True
                ):

                    st.session_state.eye_shape = name

                    st.rerun()


            else:

                if st.button(
                    "구매",
                    key=f"buyeye_{name}",
                    use_container_width=True
                ):

                    buy(
                        name,
                        price,
                        "eye_shape"
                    )

                    st.rerun()


    # --------------------------------------------------------
    # 눈 색
    # --------------------------------------------------------

    st.markdown(
        "### 🎨 눈 색"
    )


    cols = st.columns(3)


    for i,(name,price) in enumerate(
        EYE_COLORS.items()
    ):

        with cols[i]:

            st.markdown(
                f"""
                <div class="shop">

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
                    key=f"color_{name}",
                    use_container_width=True
                ):

                    st.session_state.eye_color = name

                    st.rerun()


            else:

                if st.button(
                    "구매",
                    key=f"buycolor_{name}",
                    use_container_width=True
                ):

                    buy(
                        name,
                        price,
                        "eye_color"
                    )

                    st.rerun()


    st.markdown("---")


    if st.button(
        "🌙 상점을 나가고 다음 밤 시작",
        use_container_width=True
    ):

        st.session_state.night += 1

        start_night()

        st.rerun()


# ============================================================
# 게임 중
# ============================================================

else:

    p = patient()


    # --------------------------------------------------------
    # 상태창
    # --------------------------------------------------------

    s1,s2,s3,s4,s5 = st.columns(
        5
    )


    with s1:

        st.markdown(
            f"""
            <div class="status">
            NIGHT<br>
            <b>{st.session_state.night}</b>
            </div>
            """,
            unsafe_allow_html=True
        )


    with s2:

        st.markdown(
            f"""
            <div class="status">
            PATIENT<br>
            <b>
            {st.session_state.case + 1}/{PATIENTS_PER_NIGHT}
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
            <div class="status">
            HEALTH<br>
            {hearts}
            </div>
            """,
            unsafe_allow_html=True
        )


    with s4:

        st.markdown(
            f"""
            <div class="status">
            조회권<br>
            <b>
            🔍 {st.session_state.check_tokens}
            </b>
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # 지도
    # --------------------------------------------------------

    with s5:

        with st.popover(
            "🗺️ MAP",
            use_container_width=True
        ):

            st.markdown(
                "### 병원 지도"
            )


            st.markdown(
                '<div class="map-card">🖥️ 접수 데스크</div>',
                unsafe_allow_html=True
            )


            if st.button(
                "데스크",
                key="desk"
            ):

                move("데스크")

                st.rerun()


            a,b = st.columns(2)


            with a:

                st.markdown(
                    '<div class="map-card">🛏️ 진료실</div>',
                    unsafe_allow_html=True
                )


                if st.button(
                    "진료실",
                    key="treat_room"
                ):

                    move("진료실")

                    st.rerun()


            with b:

                st.markdown(
                    '<div class="map-card">📦 물품실</div>',
                    unsafe_allow_html=True
                )


                if st.button(
                    "물품실",
                    key="supply"
                ):

                    move("물품실")

                    st.rerun()


    # --------------------------------------------------------
    # 돈
    # --------------------------------------------------------

    st.caption(
        f"💰 보유 금액 {st.session_state.money:,}원"
    )


    # --------------------------------------------------------
    # 위험도
    # --------------------------------------------------------

    threat = st.session_state.threat


    if threat < 30:

        threat_name = "안정"

        threat_class = "threat-low"


    elif threat < 60:

        threat_name = "주의"

        threat_class = "threat-mid"


    else:

        threat_name = "위험"

        threat_class = "threat-high"


    st.markdown(
        f"""
        병원 변칙 위험도 :
        <span class="{threat_class}">
        {threat}% · {threat_name}
        </span>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # 위치
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="location">

        📍 현재 위치 :
        <b>{st.session_state.location}</b>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # 랜덤 이벤트
    # --------------------------------------------------------

    event = st.session_state.current_event


    st.markdown(
        f"""
        <div class="event-box">

        <b>⚡ {event["name"]}</b>

        <br><br>

        {event["text"]}

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # 인벤토리
    # --------------------------------------------------------

    inv = (
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
        &nbsp;
        {inv}

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.session_state.message:

        st.info(
            st.session_state.message
        )


    # ========================================================
    # 데스크
    # ========================================================

    if st.session_state.location == "데스크":

        st.markdown(
            "## 🖥️ 야간 접수 데스크"
        )


        left,right = st.columns(
            [1,1]
        )


        with left:

            patient_image(
                p
            )


        with right:

            st.markdown(
                f"""
                <div class="card">

                <h3>
                환자 #{p["id"]:02d}
                </h3>

                <b>
                👁️ 관찰
                </b>

                <br><br>

                {p["public_clue"]}

                <br><br>

                아직 이 사람이 정상인지
                변칙인지 확실하지 않습니다.

                </div>
                """,
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # 기록 조회
        # ----------------------------------------------------

        if (
            not st.session_state.admitted
            and
            not st.session_state.rejected
        ):

            if not st.session_state.checked:

                if st.button(
                    "🔍 추가 기록 조회",
                    use_container_width=True
                ):

                    verify_patient()

                    st.rerun()


            if st.session_state.checked:

                st.markdown(
                    f"""
                    <div class="guide-box">

                    <b>📁 추가 조회 결과</b>

                    <br><br>

                    {p["verification"]}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            a,b = st.columns(2)


            with a:

                if st.button(
                    "🏥 병원 출입 허용",
                    use_container_width=True
                ):

                    admit()

                    st.rerun()


            with b:

                if st.button(
                    "🚫 출입 차단",
                    use_container_width=True
                ):

                    reject()

                    st.rerun()


        # ----------------------------------------------------
        # 병원 출입 허용
        # ----------------------------------------------------

        elif st.session_state.admitted:

            st.markdown(
                """
                <div class="guide-box">

                <b>📍 NEXT OBJECTIVE</b>

                <br><br>

                환자를 병원 안으로 들였습니다.

                <br><br>

                상단의 <b>🗺️ MAP</b>을 열고
                직접 <b>진료실</b>로 이동하세요.

                </div>
                """,
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # 출입 차단
        # ----------------------------------------------------

        elif st.session_state.rejected:

            if p["anomaly"]:

                st.markdown(
                    """
                    <div class="success-box">

                    <h3>
                    🚨 변칙 환자 차단 성공
                    </h3>

                    위험한 환자를 병원 밖에서
                    차단했습니다.

                    <br><br>

                    위험도 감소 +
                    보안 보너스 지급 대상

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            else:

                st.markdown(
                    """
                    <div class="anomaly-box">

                    <h3>
                    ⚠️ 정상 환자였습니다
                    </h3>

                    정상 환자를 돌려보냈습니다.

                    <br><br>

                    해당 환자의 치료 급여를
                    받을 수 없습니다.

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


        if not st.session_state.admitted:

            st.warning(
                "현재 진료실에 환자가 없습니다."
            )


        else:

            left,right = st.columns(
                [1,1]
            )


            with left:

                patient_image(
                    p
                )


            with right:

                st.markdown(
                    """
                    <div class="card">

                    <h3>
                    환자 검사
                    </h3>

                    이 시점에서도 아직
                    정상 환자인지 변칙 환자인지
                    알 수 없습니다.

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            if not st.session_state.examined:

                if st.button(
                    "🩺 검사 시작",
                    use_container_width=True
                ):

                    examine()

                    st.rerun()


            else:

                st.markdown(
                    f"""
                    <div class="guide-box">

                    <b>검사 결과</b>

                    <br><br>

                    {p["exam"]}

                    <br><br>

                    필요한 물품

                    <br><br>

                    ① {p["items"][0]}

                    <br>

                    ② {p["items"][1]}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                if st.session_state.completed:

                    if st.session_state.anomaly_revealed:

                        st.markdown(
                            """
                            <div class="anomaly-box">

                            <h2>
                            🚨 ANOMALY DETECTED
                            </h2>

                            물품을 적용한 순간
                            환자에게 변칙 반응이 나타났습니다.

                            <br><br>

                            ❤️ 체력 -1

                            <br>

                            병원 위험도 +25

                            <br>

                            급여 -200,000원

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    else:

                        st.markdown(
                            """
                            <div class="success-box">

                            <h3>
                            ✅ 치료 성공
                            </h3>

                            정상 환자의 진료를
                            완료했습니다.

                            <br><br>

                            💰 +600,000원
                            급여 계산 대상

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


                else:

                    if not st.session_state.inventory:

                        st.markdown(
                            """
                            <div class="guide-box">

                            <b>📍 NEXT OBJECTIVE</b>

                            <br><br>

                            필요한 물품을 확인했습니다.

                            <br><br>

                            🗺️ MAP을 열어
                            <b>물품실</b>로 이동하세요.

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    else:

                        selected = st.multiselect(
                            "환자에게 사용할 물품 2개",
                            st.session_state.inventory,
                            max_selections=2
                        )


                        if st.button(
                            "🩺 물품 적용",
                            use_container_width=True
                        ):

                            treat(
                                selected
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
            "필요한 물품을 기억해서 직접 가져가세요."
        )


        rows = [

            ALL_ITEMS[
                i:i+3
            ]

            for i in range(
                0,
                len(ALL_ITEMS),
                3
            )

        ]


        for r,row in enumerate(
            rows
        ):

            cols = st.columns(
                len(row)
            )


            for i,item in enumerate(
                row
            ):

                with cols[i]:

                    st.markdown(
                        f"""
                        <div class="item-card">

                        <div style="font-size:35px;">
                        🧰
                        </div>

                        <br>

                        <b>{item}</b>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    if st.button(
                        "🎒 챙기기",
                        key=f"take_{r}_{i}",
                        use_container_width=True
                    ):

                        take_item(
                            item
                        )

                        st.rerun()


        if st.session_state.examined:

            st.markdown(
                """
                <div class="guide-box">

                물품을 챙겼다면
                🗺️ MAP을 열어
                다시 <b>진료실</b>로 돌아가세요.

                </div>
                """,
                unsafe_allow_html=True
            )

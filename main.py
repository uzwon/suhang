import streamlit as st
import random
from pathlib import Path


# ============================================================
# 1. 기본 설정
# ============================================================

st.set_page_config(
    page_title="MIDNIGHT ER : NIGHT DUTY",
    page_icon="🏥",
    layout="wide"
)

IMAGE_FOLDER = Path("images")

# 한 밤에 처리하는 턴 수
SHIFT_TURNS = 8

# 급여
BASE_REWARD = 600_000
TRIAGE_BONUS = 100_000
TEST_BONUS = 50_000
VIP_BONUS = 150_000

# 상점
EXTRA_LIFE_PRICE = 3_100_000


# ============================================================
# 2. CSS / 게임 디자인
# ============================================================

st.markdown("""
<style>

/* ============================================================
   전체 병원 배경
============================================================ */

.stApp {
    background:
        linear-gradient(
            90deg,
            #e1eaed 0%,
            #e1eaed 72%,
            #cbd8dc 72%,
            #cbd8dc 100%
        );

    color: #263a43;
}


/* ============================================================
   오른쪽 병원 벽의 밤 창문
============================================================ */

.stApp::before {

    content: "";

    position: fixed;

    top: 82px;
    right: 28px;

    width: 275px;
    height: 250px;

    border: 13px solid #eff4f5;

    border-radius: 8px;

    box-sizing: border-box;

    background:

        /* 달 */
        radial-gradient(
            circle at 78% 23%,
            #fff5b4 0px,
            #fff5b4 23px,
            transparent 24px
        ),

        /* 별 */
        radial-gradient(
            circle at 14% 18%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 29% 32%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 46% 15%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 61% 39%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 24% 61%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        radial-gradient(
            circle at 71% 65%,
            white 0px,
            white 2px,
            transparent 3px
        ),

        /* 밤하늘 */
        linear-gradient(
            180deg,
            #050e18 0%,
            #0d2540 55%,
            #1a3d59 100%
        );

    box-shadow:
        inset 0 0 0 3px #b5c5ca,
        0 12px 30px rgba(0,0,0,0.18);

    z-index: 0;
}


/* 창문 중앙 틀 */

.stApp::after {

    content: "";

    position: fixed;

    top: 95px;
    right: 161px;

    width: 7px;
    height: 224px;

    background: #eff4f5;

    z-index: 1;
}


/* ============================================================
   실제 게임 화면
============================================================ */

.block-container {

    position: relative;

    z-index: 5;

    max-width: 1060px;

    margin-left: 18px;
    margin-right: 325px;

    padding-top: 1.15rem;
    padding-bottom: 4rem;
}


/* ============================================================
   타이틀
============================================================ */

.game-title {

    font-size: 43px;

    font-weight: 900;

    letter-spacing: 2px;

    color: #1f3540;

    line-height: 1.1;
}

.game-subtitle {

    font-size: 14px;

    color: #607985;

    margin-top: 5px;

    margin-bottom: 18px;
}


/* ============================================================
   상태바
============================================================ */

.status-card {

    background:
        linear-gradient(
            180deg,
            #293f4a,
            #21343e
        );

    border: 1px solid #45616d;

    border-radius: 14px;

    padding: 12px;

    text-align: center;

    box-shadow: 0 5px 15px rgba(35,55,65,0.14);
}

.status-card,
.status-card * {

    color: white !important;
}


/* ============================================================
   기본 카드
============================================================ */

.game-card {

    background: rgba(250,253,254,0.98);

    border: 1px solid #adc0c7;

    border-radius: 18px;

    padding: 21px;

    color: #273b44;

    box-shadow: 0 8px 22px rgba(40,60,70,0.11);
}

.game-card,
.game-card * {

    color: #273b44 !important;
}


/* ============================================================
   현재 장소
============================================================ */

.location-box {

    background: rgba(248,252,253,0.97);

    border-left: 6px solid #6e9cac;

    border-radius: 14px;

    padding: 14px 18px;

    margin-top: 14px;
    margin-bottom: 14px;

    box-shadow: 0 5px 14px rgba(40,60,70,0.08);
}

.location-box,
.location-box * {

    color: #273b44 !important;
}


/* ============================================================
   대기실 환자 카드
============================================================ */

.patient-card {

    background:
        linear-gradient(
            180deg,
            #fbfdfe 0%,
            #f1f6f7 100%
        );

    border: 1px solid #b2c3c9;

    border-radius: 16px;

    padding: 16px;

    min-height: 220px;

    box-shadow: 0 5px 15px rgba(40,60,70,0.09);
}

.patient-card,
.patient-card * {

    color: #273b44 !important;
}


/* VIP 카드 */

.vip-card {

    background:
        linear-gradient(
            180deg,
            #fff9e8 0%,
            #fff3cc 100%
        );

    border: 2px solid #d3ad45;

    border-radius: 16px;

    padding: 16px;

    min-height: 220px;

    box-shadow: 0 5px 15px rgba(160,120,40,0.12);
}

.vip-card,
.vip-card * {

    color: #554929 !important;
}


/* ============================================================
   환자 이미지
============================================================ */

.patient-image-placeholder {

    min-height: 340px;

    display: flex;

    justify-content: center;
    align-items: center;

    border-radius: 18px;

    border: 1px solid #9fb3bb;

    background:
        linear-gradient(
            180deg,
            #e4edef,
            #d3e1e4
        );

    font-size: 100px;

    box-shadow: 0 7px 20px rgba(40,60,70,0.10);
}


/* ============================================================
   골든타임
============================================================ */

.golden-safe {

    color: #39745a !important;

    font-weight: 900;
}

.golden-warning {

    color: #a37523 !important;

    font-weight: 900;
}

.golden-danger {

    color: #a43c49 !important;

    font-weight: 900;
}


/* ============================================================
   안내
============================================================ */

.guide-box {

    background: #eaf2fb;

    border-left: 7px solid #678bb1;

    border-radius: 14px;

    padding: 17px;

    margin-top: 14px;

    line-height: 1.8;
}

.guide-box,
.guide-box * {

    color: #304b60 !important;
}


/* ============================================================
   이벤트
============================================================ */

.event-box {

    background: #fff5d8;

    border-left: 7px solid #d8b047;

    border-radius: 14px;

    padding: 16px;

    margin: 12px 0;

    line-height: 1.8;
}

.event-box,
.event-box * {

    color: #584d2a !important;
}


/* ============================================================
   응급 경고
============================================================ */

.emergency-alert {

    background:
        linear-gradient(
            90deg,
            #7f2936,
            #a33648
        );

    border: 2px solid #d46f7d;

    border-radius: 14px;

    padding: 17px;

    margin: 13px 0;

    text-align: center;

    box-shadow: 0 7px 20px rgba(150,30,50,0.20);

    animation: pulse 1.4s infinite;
}

.emergency-alert,
.emergency-alert * {

    color: white !important;
}

@keyframes pulse {

    0% {
        opacity: 1;
    }

    50% {
        opacity: 0.78;
    }

    100% {
        opacity: 1;
    }
}


/* ============================================================
   성공
============================================================ */

.success-box {

    background: #e8f6ee;

    border-left: 7px solid #5ba077;

    border-radius: 14px;

    padding: 18px;

    margin-top: 15px;

    line-height: 1.8;
}

.success-box,
.success-box * {

    color: #2d503b !important;
}


/* ============================================================
   실패
============================================================ */

.fail-box {

    background: #fae9ec;

    border-left: 7px solid #bd5968;

    border-radius: 14px;

    padding: 18px;

    margin-top: 15px;

    line-height: 1.8;
}

.fail-box,
.fail-box * {

    color: #673842 !important;
}


/* ============================================================
   랭크
============================================================ */

.rank-box {

    background:
        linear-gradient(
            135deg,
            #253b46,
            #355463
        );

    border: 1px solid #557480;

    border-radius: 20px;

    padding: 24px;

    text-align: center;

    box-shadow: 0 10px 26px rgba(30,50,60,0.18);
}

.rank-box,
.rank-box * {

    color: white !important;
}

.rank-letter {

    font-size: 90px;

    font-weight: 900;

    line-height: 1;
}


/* ============================================================
   상점
============================================================ */

.shop-card {

    background: #f8fbfc;

    border: 1px solid #b1c2c8;

    border-radius: 16px;

    padding: 16px;

    min-height: 150px;

    text-align: center;

    box-shadow: 0 5px 14px rgba(40,60,70,0.08);
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
            #f8fcfd,
            #e7eff2
        );

    border: 1px solid #adc0c7;

    border-radius: 18px;

    padding: 20px;

    text-align: center;

    box-shadow: 0 6px 18px rgba(40,60,70,0.09);
}

.character-big {

    font-size: 80px;

    margin-bottom: 8px;
}


/* ============================================================
   로그
============================================================ */

.log-box {

    background: #253842;

    border-radius: 13px;

    padding: 13px;

    margin-top: 9px;

    font-family: monospace;

    font-size: 13px;
}

.log-box,
.log-box * {

    color: #dce8ec !important;
}


/* ============================================================
   버튼
============================================================ */

.stButton > button {

    width: 100%;

    min-height: 47px;

    border-radius: 10px;

    font-weight: 800;
}


/* ============================================================
   텍스트
============================================================ */

h1,
h2,
h3,
h4 {

    color: #263b44 !important;
}

p,
label {

    color: #2c424b;
}

div[data-baseweb="select"] * {

    color: #263b44 !important;
}


/* ============================================================
   모바일
============================================================ */

@media(max-width:900px) {

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
""", unsafe_allow_html=True)


# ============================================================
# 3. 환자 케이스
# ============================================================

PATIENT_CASES = [

    {
        "case": "탈수 의심",

        "symptom":
            "어지럼증과 심한 갈증을 호소한다.",

        "extra_info":
            "오늘 하루 물을 거의 마시지 못했다고 한다.",

        "severity": "중등",

        "best_test": "혈액검사",

        "test_result":
            "수분 부족을 의심할 수 있는 결과가 확인되었다.",

        "treatment":
            "수액 처치"
    },


    {
        "case": "팔 골절 의심",

        "symptom":
            "넘어진 뒤 팔에 심한 통증을 호소한다.",

        "extra_info":
            "팔을 움직일 때 통증이 심해지고 붓기가 있다.",

        "severity": "중등",

        "best_test": "X-ray",

        "test_result":
            "골절이 의심되는 소견이 확인되었다.",

        "treatment":
            "고정 처치"
    },


    {
        "case": "저혈당 의심",

        "symptom":
            "식은땀을 흘리고 기운이 없으며 어지러워한다.",

        "extra_info":
            "오늘 식사를 거의 하지 못했다고 한다.",

        "severity": "응급",

        "best_test": "혈액검사",

        "test_result":
            "혈당이 낮은 상태로 확인되었다.",

        "treatment":
            "포도당 공급"
    },


    {
        "case": "천식 증상",

        "symptom":
            "숨이 차고 기침이 계속된다고 말한다.",

        "extra_info":
            "평소 천식 관련 진료를 받은 적이 있다고 한다.",

        "severity": "응급",

        "best_test": "추가 문진",

        "test_result":
            "과거 호흡기 증상 및 치료 이력이 확인되었다.",

        "treatment":
            "호흡기 처치 준비"
    },


    {
        "case": "폐 감염 의심",

        "symptom":
            "고열과 기침, 가슴의 불편감을 호소한다.",

        "extra_info":
            "며칠 전부터 열이 지속되고 숨을 쉴 때 답답하다고 한다.",

        "severity": "중등",

        "best_test": "X-ray",

        "test_result":
            "폐에 염증이 의심되는 소견이 확인되었다.",

        "treatment":
            "감염 치료 준비"
    },


    {
        "case": "급성 복통",

        "symptom":
            "오른쪽 아랫배가 갑자기 심하게 아프다고 한다.",

        "extra_info":
            "시간이 지날수록 통증이 심해지고 구역감을 느낀다고 한다.",

        "severity": "응급",

        "best_test": "CT",

        "test_result":
            "복부에서 빠른 전문 평가가 필요한 소견이 확인되었다.",

        "treatment":
            "외과 응급 호출"
    },


    {
        "case": "급성 신경계 이상 의심",

        "symptom":
            "말이 평소보다 어눌하고 한쪽 팔에 힘이 잘 들어가지 않는다.",

        "extra_info":
            "증상이 갑자기 시작되었다고 보호자가 설명한다.",

        "severity": "응급",

        "best_test": "CT",

        "test_result":
            "신경계 응급 상황을 배제하기 위한 즉각적인 전문 평가가 필요하다.",

        "treatment":
            "신경계 응급 호출"
    },


    {
        "case": "긴장성 두통 의심",

        "symptom":
            "머리가 조이는 것처럼 아프다고 한다.",

        "extra_info":
            "최근 잠을 제대로 자지 못했고 피로가 심했다고 한다.",

        "severity": "경증",

        "best_test": "추가 문진",

        "test_result":
            "응급 신경학적 징후는 확인되지 않았으며 추가 관찰이 필요하다.",

        "treatment":
            "안정 및 경과 관찰"
    }

]


ALL_TREATMENTS = [

    "수액 처치",

    "고정 처치",

    "포도당 공급",

    "호흡기 처치 준비",

    "감염 치료 준비",

    "외과 응급 호출",

    "신경계 응급 호출",

    "안정 및 경과 관찰"

]


PATIENT_NAMES = [

    "김민서",

    "이서윤",

    "박지후",

    "최유진",

    "정하람",

    "조수아",

    "윤지안",

    "한서진",

    "오지우",

    "신예린",

    "임서아",

    "강민지"

]


# ============================================================
# 4. 랜덤 야간 이벤트
# ============================================================

EVENTS = [

    {
        "name": "평온한 야간",

        "text":
            "복도가 조용합니다. 현재 특별한 사건은 없습니다.",

        "effect": "none"
    },


    {
        "name": "🚑 구급차 도착",

        "text":
            "응급 환자를 태운 구급차가 도착했습니다!",

        "effect": "ambulance"
    },


    {
        "name": "⚡ 순간 정전",

        "text":
            "병원 일부 전원이 잠시 불안정합니다. 이번 턴에는 CT를 사용할 수 없습니다.",

        "effect": "ct_down"
    },


    {
        "name": "☕ 야간 커피",

        "text":
            "간호사가 커피를 가져왔습니다. 에너지 +1",

        "effect": "energy"
    },


    {
        "name": "📢 응급 호출 방송",

        "text":
            "삐-삐-! 응급실에 긴장감이 높아집니다.",

        "effect": "alarm"
    },


    {
        "name": "🩺 지원 인턴",

        "text":
            "인턴이 업무를 도와줍니다. 평판 +1",

        "effect": "reputation"
    },


    {
        "name": "⭐ VIP 내원",

        "text":
            "병원 관계자가 VIP 환자가 도착했다고 알려옵니다.",

        "effect": "vip"
    }

]


# ============================================================
# 5. 캐릭터 꾸미기
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
# 6. 계정 초기화
# ============================================================

def initialize_profile():

    defaults = {

        "money": 0,

        "night": 1,

        "extra_life": 0,

        "owned_hair": [
            "단발"
        ],

        "owned_eye_shape": [
            "둥근 눈"
        ],

        "owned_eye_color": [
            "갈색"
        ],

        "hair": "단발",

        "eye_shape": "둥근 눈",

        "eye_color": "갈색",

        "game_started": False

    }


    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ============================================================
# 7. 환자 생성
# ============================================================

def create_patient(
    force_emergency=False,
    force_vip=False
):

    case = random.choice(
        PATIENT_CASES
    ).copy()


    # 응급 환자를 강제로 만들어야 하는 경우
    if force_emergency:

        emergency_cases = [

            c for c in PATIENT_CASES

            if c["severity"] == "응급"

        ]

        case = random.choice(
            emergency_cases
        ).copy()


    severity = case[
        "severity"
    ]


    if severity == "응급":

        golden_limit = 2


    elif severity == "중등":

        golden_limit = 4


    else:

        golden_limit = 6


    patient = {

        **case,

        "uid":
            random.randint(
                10000,
                99999
            ),

        "name":
            random.choice(
                PATIENT_NAMES
            ),

        "age":
            random.randint(
                15,
                78
            ),

        "waiting":
            0,

        "golden_limit":
            golden_limit,

        "vip":
            force_vip
            or
            random.random() < 0.12,

        "image":
            f"patient{random.randint(1,8):02d}.png"

    }


    return patient


# ============================================================
# 8. 대기열 채우기
# ============================================================

def fill_waiting_room():

    while len(
        st.session_state.waiting_room
    ) < 4:

        st.session_state.waiting_room.append(
            create_patient()
        )


# ============================================================
# 9. 게임 시작
# ============================================================

def start_night():

    st.session_state.turns_left = (
        SHIFT_TURNS
    )


    st.session_state.health = (
        3
        +
        st.session_state.extra_life
    )


    st.session_state.extra_life = 0


    st.session_state.reputation = 5

    st.session_state.energy = 4


    st.session_state.waiting_room = []

    fill_waiting_room()


    st.session_state.active_patient = None

    st.session_state.phase = "waiting"


    st.session_state.extra_interview_done = False

    st.session_state.triage_choice = None

    st.session_state.triage_correct = False

    st.session_state.test_correct = False

    st.session_state.test_result = ""

    st.session_state.treatment_options = []


    st.session_state.success_count = 0

    st.session_state.fail_count = 0

    st.session_state.missed_count = 0

    st.session_state.triage_correct_count = 0

    st.session_state.test_correct_count = 0

    st.session_state.vip_success_count = 0


    st.session_state.salary = 0

    st.session_state.score = 0


    st.session_state.logs = []


    st.session_state.current_event = {

        "name": "근무 시작",

        "text":
            "22:00. 야간 응급실 근무가 시작되었습니다.",

        "effect": "none"

    }


    st.session_state.message = ""

    st.session_state.shift_over = False

    st.session_state.salary_settled = False

    st.session_state.game_started = True


# ============================================================
# 10. 환자 얼굴 이미지
# ============================================================

def show_patient_image(
    patient,
    big=True
):

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

        if big:

            height = 340
            font = 100

        else:

            height = 120
            font = 55


        st.markdown(
            f"""
            <div
            class="patient-image-placeholder"
            style="
                min-height:{height}px;
                font-size:{font}px;
            ">
            👤
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 11. 랜덤 이벤트
# ============================================================

def trigger_event():

    event = random.choice(
        EVENTS
    )


    st.session_state.current_event = (
        event
    )


    effect = event[
        "effect"
    ]


    if effect == "energy":

        st.session_state.energy = min(
            6,
            st.session_state.energy + 1
        )


    elif effect == "reputation":

        st.session_state.reputation = min(
            7,
            st.session_state.reputation + 1
        )


    elif effect == "ambulance":

        st.session_state.waiting_room.append(

            create_patient(
                force_emergency=True
            )

        )


    elif effect == "vip":

        st.session_state.waiting_room.append(

            create_patient(
                force_vip=True
            )

        )


# ============================================================
# 12. 대기시간 증가
# ============================================================

def update_waiting_time():

    survivors = []


    for patient in st.session_state.waiting_room:

        patient["waiting"] += 1


        if (
            patient["waiting"]
            >=
            patient["golden_limit"]
        ):

            st.session_state.missed_count += 1

            st.session_state.reputation -= 1

            st.session_state.score -= 600


            st.session_state.logs.append(

                f"⚠️ {patient['name']} 환자가 "
                f"골든타임을 초과했습니다."

            )


        else:

            survivors.append(
                patient
            )


    st.session_state.waiting_room = (
        survivors
    )


# ============================================================
# 13. 턴 종료
# ============================================================

def finish_turn():

    st.session_state.turns_left -= 1


    update_waiting_time()


    if (
        st.session_state.turns_left <= 0
        or
        st.session_state.health <= 0
        or
        st.session_state.reputation <= 0
    ):

        st.session_state.shift_over = True

        return


    trigger_event()

    fill_waiting_room()


    st.session_state.active_patient = None

    st.session_state.phase = "waiting"

    st.session_state.extra_interview_done = False

    st.session_state.triage_choice = None

    st.session_state.triage_correct = False

    st.session_state.test_correct = False

    st.session_state.test_result = ""

    st.session_state.treatment_options = []

    st.session_state.message = ""


# ============================================================
# 14. 환자 선택
# ============================================================

def select_patient(uid):

    selected = None

    remaining = []


    for patient in st.session_state.waiting_room:

        if patient["uid"] == uid:

            selected = patient

        else:

            remaining.append(
                patient
            )


    st.session_state.waiting_room = (
        remaining
    )


    st.session_state.active_patient = (
        selected
    )


    st.session_state.phase = "interview"

    st.session_state.message = ""


# ============================================================
# 15. 추가 문진
# ============================================================

def extra_interview():

    if st.session_state.extra_interview_done:

        return


    if st.session_state.energy <= 0:

        st.session_state.message = (
            "⚠️ 에너지가 부족해 추가 문진을 할 수 없습니다."
        )

        return


    st.session_state.energy -= 1

    st.session_state.extra_interview_done = True

    st.session_state.message = (
        st.session_state.active_patient[
            "extra_info"
        ]
    )


# ============================================================
# 16. 트리아지 선택
# ============================================================

def submit_triage(choice):

    patient = (
        st.session_state.active_patient
    )


    st.session_state.triage_choice = (
        choice
    )


    if (
        choice
        ==
        patient["severity"]
    ):

        st.session_state.triage_correct = True

        st.session_state.triage_correct_count += 1

        st.session_state.score += 300


    else:

        st.session_state.triage_correct = False


    st.session_state.phase = "test"


# ============================================================
# 17. 검사 진행
# ============================================================

def perform_test(test):

    patient = (
        st.session_state.active_patient
    )


    # 정전 이벤트일 때 CT 사용 불가
    if (
        st.session_state.current_event["effect"]
        ==
        "ct_down"
        and
        test == "CT"
    ):

        st.session_state.message = (
            "⚡ CT 전원 오류로 검사를 진행할 수 없습니다. "
            "다른 검사를 선택하세요."
        )

        return


    if (
        test
        ==
        patient["best_test"]
    ):

        st.session_state.test_correct = True

        st.session_state.test_correct_count += 1

        st.session_state.score += 200


        st.session_state.test_result = (
            patient["test_result"]
        )


    elif test == "검사 없이 치료":

        st.session_state.test_correct = False

        st.session_state.test_result = (
            "추가 검사를 생략했습니다. "
            "현재 정보만으로 치료를 결정해야 합니다."
        )


    else:

        st.session_state.test_correct = False

        st.session_state.test_result = (
            "결정적인 정보를 얻지 못했습니다."
        )


    correct = patient[
        "treatment"
    ]


    wrong_choices = [

        x for x in ALL_TREATMENTS

        if x != correct

    ]


    options = [
        correct
    ]


    options.extend(

        random.sample(
            wrong_choices,
            3
        )

    )


    random.shuffle(
        options
    )


    st.session_state.treatment_options = (
        options
    )


    st.session_state.phase = "treatment"

    st.session_state.message = ""


# ============================================================
# 18. 치료
# ============================================================

def submit_treatment(choice):

    patient = (
        st.session_state.active_patient
    )


    if (
        choice
        ==
        patient["treatment"]
    ):

        reward = BASE_REWARD


        if st.session_state.triage_correct:

            reward += (
                TRIAGE_BONUS
            )


        if st.session_state.test_correct:

            reward += (
                TEST_BONUS
            )


        if patient["vip"]:

            reward += (
                VIP_BONUS
            )

            st.session_state.vip_success_count += 1


        st.session_state.salary += reward

        st.session_state.success_count += 1

        st.session_state.score += 1000


        st.session_state.message = (
            f"✅ 치료 성공! "
            f"{reward:,}원의 급여가 추가됩니다."
        )


        st.session_state.logs.append(

            f"✅ {patient['name']} 치료 성공"

        )


    else:

        st.session_state.fail_count += 1

        st.session_state.score -= 500

        st.session_state.reputation -= 1


        # 응급 환자를 잘못 치료했을 때
        if patient["severity"] == "응급":

            st.session_state.health -= 1


        st.session_state.message = (
            "❌ 치료 판단이 적절하지 않았습니다."
        )


        st.session_state.logs.append(

            f"❌ {patient['name']} 치료 실패"

        )


    st.session_state.phase = "result"


# ============================================================
# 19. 휴식
# ============================================================

def rest_turn():

    st.session_state.energy = min(
        6,
        st.session_state.energy + 2
    )


    st.session_state.logs.append(
        "☕ 휴게실에서 잠시 쉬었습니다."
    )


    finish_turn()


# ============================================================
# 20. 점수 계산
# ============================================================

def calculate_final_rank():

    score = st.session_state.score


    score += (
        st.session_state.reputation
        *
        100
    )


    if score >= 6500:

        return "S"


    elif score >= 4500:

        return "A"


    elif score >= 2500:

        return "B"


    return "C"


# ============================================================
# 21. 급여 지급
# ============================================================

def settle_salary():

    if st.session_state.salary_settled:

        return


    st.session_state.money += (
        st.session_state.salary
    )


    st.session_state.salary_settled = True


# ============================================================
# 22. 캐릭터 표시
# ============================================================

def show_character():

    hair = {

        "단발":
            "💇🏻‍♀️",

        "긴 머리":
            "👩🏻",

        "포니테일":
            "👱🏻‍♀️"

    }[
        st.session_state.hair
    ]


    eye_shape = {

        "둥근 눈":
            "● ●",

        "웃는 눈":
            "⌒ ⌒",

        "날카로운 눈":
            "◢ ◣"

    }[
        st.session_state.eye_shape
    ]


    eye_color = {

        "갈색":
            "🟤",

        "파란색":
            "🔵",

        "보라색":
            "🟣"

    }[
        st.session_state.eye_color
    ]


    st.markdown(
        f"""
        <div class="character-card">

        <div class="character-big">
        {hair}
        </div>

        <b>
        야간 응급실 의사
        </b>

        <br><br>

        머리 :
        <b>{st.session_state.hair}</b>

        <br>

        눈 :
        <b>{st.session_state.eye_shape}</b>
        &nbsp; {eye_shape}

        <br>

        눈 색 :
        <b>{st.session_state.eye_color}</b>
        &nbsp; {eye_color}

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 23. 상점 구매
# ============================================================

def buy_item(
    name,
    price,
    category
):

    if (
        st.session_state.money
        <
        price
    ):

        st.warning(
            "보유 금액이 부족합니다."
        )

        return


    if category == "hair":

        if (
            name
            not in
            st.session_state.owned_hair
        ):

            st.session_state.owned_hair.append(
                name
            )


    elif category == "eye_shape":

        if (
            name
            not in
            st.session_state.owned_eye_shape
        ):

            st.session_state.owned_eye_shape.append(
                name
            )


    elif category == "eye_color":

        if (
            name
            not in
            st.session_state.owned_eye_color
        ):

            st.session_state.owned_eye_color.append(
                name
            )


    st.session_state.money -= (
        price
    )


# ============================================================
# 24. 목숨 구매
# ============================================================

def buy_life():

    if (
        st.session_state.money
        <
        EXTRA_LIFE_PRICE
    ):

        st.warning(
            "목숨을 구매할 돈이 부족합니다."
        )

        return


    st.session_state.money -= (
        EXTRA_LIFE_PRICE
    )


    st.session_state.extra_life += 1


# ============================================================
# 초기화
# ============================================================

initialize_profile()


# ============================================================
# 제목
# ============================================================

st.markdown(
    """
    <div class="game-title">
    MIDNIGHT ER
    </div>

    <div class="game-subtitle">
    NIGHT DUTY · 22:00 — 06:00
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 시작 화면
# ============================================================

if not st.session_state.game_started:

    left, right = st.columns(
        [1.7, 1]
    )


    with left:

        st.markdown(
            f"""
            <div class="game-card">

            <h2>
            🌙 NIGHT {st.session_state.night}
            </h2>

            오늘 밤 당신은
            <b>야간 응급실 담당 의사</b>입니다.

            <br><br>

            환자들은 동시에 찾아오지만
            모두를 한 번에 진료할 수는 없습니다.

            <br><br>

            대기 환자의 상태와
            <b>골든타임</b>을 확인해
            누구를 먼저 치료할지 결정하세요.

            <br><br>

            문진 → 중증도 분류 → 검사 → 치료의
            모든 판단은 당신이 직접 해야 합니다.

            <br><br>

            <b>
            VIP 여부는 의료적 우선순위를 바꾸지 않습니다.
            환자의 상태가 가장 중요합니다.
            </b>

            </div>
            """,
            unsafe_allow_html=True
        )


    with right:

        show_character()


    st.write("")


    if st.button(
        "🏥 야간 근무 시작",
        use_container_width=True
    ):

        start_night()

        st.rerun()


# ============================================================
# 야간 근무 종료
# ============================================================

elif st.session_state.shift_over:

    settle_salary()


    rank = calculate_final_rank()


    left, right = st.columns(
        [1.2, 1]
    )


    with left:

        st.markdown(
            f"""
            <div class="rank-box">

            <div>
            NIGHT {st.session_state.night} RESULT
            </div>

            <br>

            <div class="rank-letter">
            {rank}
            </div>

            <br>

            성공 치료 :
            <b>{st.session_state.success_count}명</b>

            <br><br>

            실패 :
            <b>{st.session_state.fail_count}명</b>

            <br><br>

            골든타임 초과 :
            <b>{st.session_state.missed_count}명</b>

            <br><br>

            트리아지 정답 :
            <b>{st.session_state.triage_correct_count}회</b>

            <br><br>

            검사 선택 정답 :
            <b>{st.session_state.test_correct_count}회</b>

            <br><br>

            VIP 치료 성공 :
            <b>{st.session_state.vip_success_count}명</b>

            </div>
            """,
            unsafe_allow_html=True
        )


    with right:

        st.markdown(
            f"""
            <div class="game-card">

            <h3>
            💰 급여 정산
            </h3>

            오늘 급여

            <br>

            <b style="font-size:25px;">
            {st.session_state.salary:,}원
            </b>

            <br><br>

            현재 보유 금액

            <br>

            <b style="font-size:25px;">
            {st.session_state.money:,}원
            </b>

            <br><br>

            최종 점수

            <br>

            <b>
            {st.session_state.score}
            </b>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # 근무 기록
    # ========================================================

    with st.expander(
        "📋 오늘의 응급실 기록"
    ):

        if not st.session_state.logs:

            st.write(
                "기록이 없습니다."
            )


        for log in st.session_state.logs:

            st.write(
                "•",
                log
            )


    # ========================================================
    # 상점
    # ========================================================

    st.markdown(
        "## 🛍️ 야간 근무 상점"
    )


    st.caption(
        "원하는 게 없으면 아무것도 사지 않고 바로 다음 밤으로 넘어가도 됩니다."
    )


    life_col, char_col = st.columns(
        2
    )


    with life_col:

        st.markdown(
            f"""
            <div class="shop-card">

            <div style="font-size:42px;">
            ❤️
            </div>

            <b>
            추가 목숨 +1
            </b>

            <br><br>

            다음 밤 시작 체력이
            1 증가합니다.

            <br><br>

            <b>
            {EXTRA_LIFE_PRICE:,}원
            </b>

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


    with char_col:

        show_character()


    # ========================================================
    # 머리
    # ========================================================

    st.markdown(
        "### 💇 머리 모양"
    )


    cols = st.columns(3)


    for index, (
        name,
        price
    ) in enumerate(
        HAIR_ITEMS.items()
    ):

        with cols[index]:

            st.markdown(
                f"""
                <div class="shop-card">

                <b>{name}</b>

                <br><br>

                {price:,}원

                </div>
                """,
                unsafe_allow_html=True
            )


            if (
                name
                in
                st.session_state.owned_hair
            ):

                if st.button(
                    "착용",
                    key=f"hair_use_{name}",
                    use_container_width=True
                ):

                    st.session_state.hair = (
                        name
                    )

                    st.rerun()


            else:

                if st.button(
                    "구매",
                    key=f"hair_buy_{name}",
                    use_container_width=True
                ):

                    buy_item(
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


    cols = st.columns(3)


    for index, (
        name,
        price
    ) in enumerate(
        EYE_SHAPE_ITEMS.items()
    ):

        with cols[index]:

            st.markdown(
                f"""
                <div class="shop-card">

                <b>{name}</b>

                <br><br>

                {price:,}원

                </div>
                """,
                unsafe_allow_html=True
            )


            if (
                name
                in
                st.session_state.owned_eye_shape
            ):

                if st.button(
                    "착용",
                    key=f"eye_use_{name}",
                    use_container_width=True
                ):

                    st.session_state.eye_shape = (
                        name
                    )

                    st.rerun()


            else:

                if st.button(
                    "구매",
                    key=f"eye_buy_{name}",
                    use_container_width=True
                ):

                    buy_item(
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


    cols = st.columns(3)


    for index, (
        name,
        price
    ) in enumerate(
        EYE_COLOR_ITEMS.items()
    ):

        with cols[index]:

            symbol = {

                "갈색":
                    "🟤",

                "파란색":
                    "🔵",

                "보라색":
                    "🟣"

            }[name]


            st.markdown(
                f"""
                <div class="shop-card">

                <div style="font-size:30px;">
                {symbol}
                </div>

                <b>{name}</b>

                <br><br>

                {price:,}원

                </div>
                """,
                unsafe_allow_html=True
            )


            if (
                name
                in
                st.session_state.owned_eye_color
            ):

                if st.button(
                    "착용",
                    key=f"color_use_{name}",
                    use_container_width=True
                ):

                    st.session_state.eye_color = (
                        name
                    )

                    st.rerun()


            else:

                if st.button(
                    "구매",
                    key=f"color_buy_{name}",
                    use_container_width=True
                ):

                    buy_item(
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
# 실제 게임
# ============================================================

else:

    # ========================================================
    # 상단 상태바
    # ========================================================

    s1, s2, s3, s4, s5 = st.columns(
        5
    )


    with s1:

        st.markdown(
            f"""
            <div class="status-card">

            NIGHT

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

            남은 시간

            <br>

            <b>
            {st.session_state.turns_left}
            TURN
            </b>

            </div>
            """,
            unsafe_allow_html=True
        )


    with s3:

        hearts = (
            "❤️"
            *
            max(
                0,
                st.session_state.health
            )
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


    with s4:

        st.markdown(
            f"""
            <div class="status-card">

            평판

            <br>

            ⭐ {st.session_state.reputation}

            </div>
            """,
            unsafe_allow_html=True
        )


    with s5:

        st.markdown(
            f"""
            <div class="status-card">

            에너지

            <br>

            ⚡ {st.session_state.energy}

            </div>
            """,
            unsafe_allow_html=True
        )


    st.caption(
        f"💰 현재 예상 급여 : "
        f"{st.session_state.salary:,}원"
    )


    # ========================================================
    # 현재 장소
    # ========================================================

    phase_names = {

        "waiting":
            "응급실 대기실",

        "interview":
            "초진실",

        "test":
            "검사 선택",

        "treatment":
            "진료실",

        "result":
            "처치 결과"

    }


    st.markdown(
        f"""
        <div class="location-box">

        📍 현재 위치 :
        <b>
        {phase_names[
            st.session_state.phase
        ]}
        </b>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # 야간 이벤트
    # ========================================================

    event = (
        st.session_state.current_event
    )


    if event["effect"] in [
        "ambulance",
        "alarm"
    ]:

        st.markdown(
            f"""
            <div class="emergency-alert">

            <b>
            🚨 삐 — 삐 — 삐 —
            </b>

            <br><br>

            <b>
            {event["name"]}
            </b>

            <br>

            {event["text"]}

            </div>
            """,
            unsafe_allow_html=True
        )


    else:

        st.markdown(
            f"""
            <div class="event-box">

            <b>
            {event["name"]}
            </b>

            <br><br>

            {event["text"]}

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
    # 1. 대기실
    # ========================================================

    if st.session_state.phase == "waiting":

        st.markdown(
            "## 🪑 응급실 대기실"
        )


        st.caption(
            "골든타임과 환자 상태를 확인하고 누구를 먼저 진료할지 선택하세요."
        )


        patient_columns = st.columns(
            2
        )


        for index, patient in enumerate(
            st.session_state.waiting_room
        ):

            with patient_columns[
                index % 2
            ]:

                remaining_time = (

                    patient["golden_limit"]
                    -
                    patient["waiting"]

                )


                if remaining_time >= 4:

                    golden_class = (
                        "golden-safe"
                    )


                elif remaining_time >= 2:

                    golden_class = (
                        "golden-warning"
                    )


                else:

                    golden_class = (
                        "golden-danger"
                    )


                severity_icon = {

                    "경증":
                        "🟢",

                    "중등":
                        "🟠",

                    "응급":
                        "🔴"

                }[
                    patient["severity"]
                ]


                if patient["vip"]:

                    card_class = (
                        "vip-card"
                    )

                    vip_text = (
                        "⭐ VIP"
                    )


                else:

                    card_class = (
                        "patient-card"
                    )

                    vip_text = ""


                st.markdown(
                    f"""
                    <div class="{card_class}">

                    <div style="
                    display:flex;
                    justify-content:space-between;
                    ">

                    <b>
                    {patient["name"]}
                    </b>

                    <b>
                    {vip_text}
                    </b>

                    </div>

                    <br>

                    {patient["age"]}세

                    <br><br>

                    <b>
                    현재 증상
                    </b>

                    <br>

                    {patient["symptom"]}

                    <br><br>

                    중증도 힌트 :

                    {severity_icon}
                    {patient["severity"]}

                    <br><br>

                    <span class="{golden_class}">

                    ⏱️ 골든타임
                    {remaining_time} TURN

                    </span>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                if st.button(
                    f"🩺 {patient['name']} 진료",
                    key=f"patient_{patient['uid']}",
                    use_container_width=True
                ):

                    select_patient(
                        patient["uid"]
                    )

                    st.rerun()


        # 휴식
        st.write("")


        if st.button(
            "☕ 휴게실에서 1턴 쉬기 · 에너지 +2",
            use_container_width=True
        ):

            rest_turn()

            st.rerun()


        # 로그
        if st.session_state.logs:

            with st.expander(
                "📟 응급실 상황 로그"
            ):

                for log in st.session_state.logs:

                    st.markdown(
                        f"""
                        <div class="log-box">
                        {log}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


    # ========================================================
    # 2. 초진 / 문진
    # ========================================================

    elif st.session_state.phase == "interview":

        patient = (
            st.session_state.active_patient
        )


        left, right = st.columns(
            [1, 1.05]
        )


        with left:

            show_patient_image(
                patient
            )


        with right:

            vip_badge = (

                "⭐ VIP 환자"

                if patient["vip"]

                else ""
            )


            st.markdown(
                f"""
                <div class="game-card">

                <h3>
                {patient["name"]}
                </h3>

                {patient["age"]}세

                <br>

                {vip_badge}

                <br><br>

                <b>
                주호소
                </b>

                <br><br>

                {patient["symptom"]}

                <br><br>

                환자 상태를 평가하고
                중증도를 분류하세요.

                </div>
                """,
                unsafe_allow_html=True
            )


            if not st.session_state.extra_interview_done:

                if st.button(
                    "🗣️ 추가 문진하기 · 에너지 -1",
                    use_container_width=True
                ):

                    extra_interview()

                    st.rerun()


            else:

                st.markdown(
                    f"""
                    <div class="guide-box">

                    <b>
                    🗣️ 추가 문진
                    </b>

                    <br><br>

                    {patient["extra_info"]}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


        st.markdown(
            "### 🚦 중증도 분류"
        )


        triage_choice = st.radio(

            "환자의 현재 상태를 선택하세요.",

            [
                "경증",
                "중등",
                "응급"
            ],

            horizontal=True

        )


        if st.button(
            "📋 트리아지 확정",
            use_container_width=True
        ):

            submit_triage(
                triage_choice
            )

            st.rerun()


    # ========================================================
    # 3. 검사
    # ========================================================

    elif st.session_state.phase == "test":

        patient = (
            st.session_state.active_patient
        )


        st.markdown(
            f"""
            <div class="game-card">

            <h3>
            🧪 검사 선택
            </h3>

            환자 :
            <b>
            {patient["name"]}
            </b>

            <br><br>

            어떤 검사를 우선 시행할지
            판단하세요.

            </div>
            """,
            unsafe_allow_html=True
        )


        if (
            st.session_state.current_event["effect"]
            ==
            "ct_down"
        ):

            st.markdown(
                """
                <div class="emergency-alert">

                ⚡ CT 장비 전원 오류

                <br>

                현재 CT 검사는 사용할 수 없습니다.

                </div>
                """,
                unsafe_allow_html=True
            )


        test_choice = st.radio(

            "검사 선택",

            [
                "추가 문진",
                "혈액검사",
                "X-ray",
                "CT",
                "검사 없이 치료"
            ]

        )


        if st.button(
            "🧪 검사 진행",
            use_container_width=True
        ):

            perform_test(
                test_choice
            )

            st.rerun()


    # ========================================================
    # 4. 치료
    # ========================================================

    elif st.session_state.phase == "treatment":

        patient = (
            st.session_state.active_patient
        )


        st.markdown(
            f"""
            <div class="guide-box">

            <b>
            🧪 검사 결과
            </b>

            <br><br>

            {st.session_state.test_result}

            </div>
            """,
            unsafe_allow_html=True
        )


        if patient["severity"] == "응급":

            st.markdown(
                """
                <div class="emergency-alert">

                🚨 삐 — 삐 — 삐 —

                <br>

                응급 환자입니다.

                <br>

                빠르게 올바른 처치를 선택하세요.

                </div>
                """,
                unsafe_allow_html=True
            )


        st.markdown(
            "### 🩺 최종 처치 선택"
        )


        treatment_choice = st.radio(

            "환자에게 필요한 처치를 선택하세요.",

            st.session_state.treatment_options

        )


        if st.button(
            "💉 처치 실행",
            use_container_width=True
        ):

            submit_treatment(
                treatment_choice
            )

            st.rerun()


    # ========================================================
    # 5. 결과
    # ========================================================

    elif st.session_state.phase == "result":

        patient = (
            st.session_state.active_patient
        )


        treatment_success = (

            "치료 성공"
            in
            st.session_state.message

        )


        if treatment_success:

            reward = BASE_REWARD


            if st.session_state.triage_correct:

                reward += (
                    TRIAGE_BONUS
                )


            if st.session_state.test_correct:

                reward += (
                    TEST_BONUS
                )


            if patient["vip"]:

                reward += (
                    VIP_BONUS
                )


            st.markdown(
                f"""
                <div class="success-box">

                <h3>
                ✅ 치료 성공
                </h3>

                {patient["name"]} 환자의
                처치가 완료되었습니다.

                <br><br>

                기본 급여
                +{BASE_REWARD:,}원

                <br>

                트리아지 보너스
                +{
                    TRIAGE_BONUS
                    if st.session_state.triage_correct
                    else 0
                :,}원

                <br>

                검사 보너스
                +{
                    TEST_BONUS
                    if st.session_state.test_correct
                    else 0
                :,}원

                <br>

                VIP 보너스
                +{
                    VIP_BONUS
                    if patient["vip"]
                    else 0
                :,}원

                <br><br>

                <b>
                총 +{reward:,}원
                </b>

                </div>
                """,
                unsafe_allow_html=True
            )


        else:

            st.markdown(
                f"""
                <div class="fail-box">

                <h3>
                ❌ 처치 실패
                </h3>

                선택한 처치가
                환자의 상태와 맞지 않았습니다.

                <br><br>

                이 게임에서 설정된
                적절한 처치는

                <br><br>

                <b>
                {patient["treatment"]}
                </b>

                이었습니다.

                </div>
                """,
                unsafe_allow_html=True
            )


        if st.button(
            "➡️ 응급실 대기실로 돌아가기",
            use_container_width=True
        ):

            finish_turn()

            st.rerun()

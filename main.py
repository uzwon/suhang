import streamlit as st
import random
from pathlib import Path


# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="MIDNIGHT ER : NIGHT DUTY",
    page_icon="🏥",
    layout="wide"
)

IMAGE_FOLDER = Path("images")

SHIFT_CASES = 8                  # 한 밤에 처리할 최대 환자 수
BASE_REWARD = 600_000            # 정상 환자 치료 기본 보상
TRIAGE_BONUS = 100_000           # 중증도 분류 정답 보너스
TEST_BONUS = 50_000              # 적절한 검사 선택 보너스
EXTRA_LIFE_PRICE = 3_100_000     # 추가 목숨 가격


# ============================================================
# 디자인
# ============================================================

st.markdown("""
<style>

/* 전체 배경 */
.stApp {
    background:
        linear-gradient(
            90deg,
            #e3ecef 0%,
            #e3ecef 72%,
            #d0dce0 72%,
            #d0dce0 100%
        );
}

/* 오른쪽 창문 */
.stApp::before {
    content: "";
    position: fixed;
    top: 90px;
    right: 30px;
    width: 270px;
    height: 240px;
    border: 12px solid #eef4f6;
    border-radius: 8px;
    box-sizing: border-box;
    background:
        radial-gradient(circle at 78% 24%, #fff5b8 0px, #fff5b8 22px, transparent 23px),
        radial-gradient(circle at 18% 20%, white 0px, white 2px, transparent 3px),
        radial-gradient(circle at 38% 35%, white 0px, white 2px, transparent 3px),
        radial-gradient(circle at 58% 18%, white 0px, white 2px, transparent 3px),
        radial-gradient(circle at 70% 48%, white 0px, white 2px, transparent 3px),
        linear-gradient(180deg, #071320 0%, #102b49 60%, #1c4362 100%);
    box-shadow:
        inset 0 0 0 3px #b8c8cd,
        0 10px 24px rgba(0,0,0,0.18);
    z-index: 0;
}

/* 창문 틀 */
.stApp::after {
    content: "";
    position: fixed;
    top: 102px;
    right: 160px;
    width: 7px;
    height: 216px;
    background: #eef4f6;
    z-index: 1;
}

.block-container {
    position: relative;
    z-index: 5;
    max-width: 1040px;
    margin-left: 20px;
    margin-right: 320px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}

/* 제목 */
.game-title {
    font-size: 42px;
    font-weight: 900;
    color: #213742;
    letter-spacing: 2px;
}
.game-sub {
    color: #607985;
    margin-bottom: 16px;
}

/* 상태 카드 */
.stat-card {
    background: #263b46;
    border: 1px solid #44606c;
    border-radius: 14px;
    padding: 13px;
    text-align: center;
    box-shadow: 0 5px 16px rgba(40,60,70,0.14);
}
.stat-card, .stat-card * {
    color: white !important;
}

/* 일반 카드 */
.card {
    background: rgba(250,253,254,0.98);
    border: 1px solid #afc1c8;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 8px 22px rgba(40,60,70,0.10);
}
.card, .card * {
    color: #273b44 !important;
}

/* 현재 위치 */
.location-box {
    background: #f6fbfc;
    border-left: 6px solid #6f9bab;
    border-radius: 14px;
    padding: 15px 18px;
    margin: 14px 0;
    box-shadow: 0 5px 14px rgba(40,60,70,0.08);
}
.location-box, .location-box * {
    color: #273b44 !important;
}

/* 대기 환자 카드 */
.queue-card {
    background: #f9fbfc;
    border: 1px solid #b4c4ca;
    border-radius: 16px;
    padding: 16px;
    min-height: 200px;
    box-shadow: 0 5px 14px rgba(40,60,70,0.08);
}
.queue-card, .queue-card * {
    color: #273b44 !important;
}

/* 환자 사진 */
.patient-photo {
    min-height: 360px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(180deg, #e4edef 0%, #d4e2e6 100%);
    border: 1px solid #a2b6bd;
    border-radius: 18px;
    font-size: 96px;
    box-shadow: 0 6px 18px rgba(40,60,70,0.10);
}

/* 안내 */
.guide-box {
    background: #eaf2fb;
    border-left: 7px solid #6689b0;
    border-radius: 14px;
    padding: 17px;
    margin-top: 14px;
}
.guide-box, .guide-box * {
    color: #304b60 !important;
}

/* 이벤트 */
.event-box {
    background: #fff5d9;
    border-left: 7px solid #d9b24a;
    border-radius: 14px;
    padding: 16px;
    margin-top: 10px;
}
.event-box, .event-box * {
    color: #574d2b !important;
}

/* 성공 */
.success-box {
    background: #e8f6ee;
    border-left: 7px solid #5ca078;
    border-radius: 14px;
    padding: 18px;
    margin-top: 15px;
}
.success-box, .success-box * {
    color: #2d503b !important;
}

/* 실패 */
.fail-box {
    background: #faeaed;
    border-left: 7px solid #bf5b69;
    border-radius: 14px;
    padding: 18px;
    margin-top: 15px;
}
.fail-box, .fail-box * {
    color: #673942 !important;
}

/* 인벤토리 느낌 카드 */
.inventory-box {
    background: #263c46;
    border-radius: 14px;
    padding: 13px 17px;
    margin-bottom: 14px;
}
.inventory-box, .inventory-box * {
    color: white !important;
}

/* 상점 */
.shop-card {
    background: #f8fbfc;
    border: 1px solid #b2c3c9;
    border-radius: 16px;
    padding: 16px;
    min-height: 145px;
    text-align: center;
    box-shadow: 0 5px 14px rgba(40,60,70,0.08);
}
.shop-card, .shop-card * {
    color: #273b44 !important;
}

/* 캐릭터 카드 */
.character-card {
    background: linear-gradient(180deg, #f8fcfd 0%, #e8f0f2 100%);
    border: 1px solid #afc1c8;
    border-radius: 18px;
    padding: 22px;
    text-align: center;
}
.character-big {
    font-size: 72px;
    margin-bottom: 10px;
}

/* 버튼 */
.stButton > button {
    width: 100%;
    min-height: 46px;
    border-radius: 10px;
    font-weight: 800;
}

/* 글씨 */
h1, h2, h3, h4 {
    color: #263b44 !important;
}
p, label {
    color: #2b414a;
}
div[data-baseweb="select"] * {
    color: #263b44 !important;
}

/* 모바일 */
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
""", unsafe_allow_html=True)


# ============================================================
# 환자 데이터
# ============================================================

PATIENT_TEMPLATES = [
    {
        "case": "탈수",
        "symptom": "심한 어지럼증과 갈증을 호소한다.",
        "hint": "입술이 마르고, 오늘 물을 거의 못 마셨다고 한다.",
        "severity": "중등",
        "best_test": "혈액검사",
        "test_result": "수분 부족이 의심되는 수치가 확인되었다.",
        "treatment": "수액 처치"
    },
    {
        "case": "골절",
        "symptom": "넘어진 뒤 팔 통증을 크게 호소한다.",
        "hint": "팔을 움직일 때 매우 아파하며 붓기가 보인다.",
        "severity": "중등",
        "best_test": "X-ray",
        "test_result": "뼈의 골절 소견이 확인되었다.",
        "treatment": "깁스/고정"
    },
    {
        "case": "저혈당",
        "symptom": "식은땀을 흘리며 기운이 없고 어지러워 보인다.",
        "hint": "오늘 식사를 거의 못 했다고 한다.",
        "severity": "응급",
        "best_test": "혈액검사",
        "test_result": "혈당이 매우 낮게 측정되었다.",
        "treatment": "포도당 투여"
    },
    {
        "case": "천식 악화",
        "symptom": "숨이 차고 기침을 자주 한다.",
        "hint": "평소 천식이 있으며 숨소리가 거칠다.",
        "severity": "응급",
        "best_test": "추가 문진",
        "test_result": "과거 천식 병력이 있고 흡입기 사용 경험이 있다.",
        "treatment": "기관지 흡입치료"
    },
    {
        "case": "폐렴 의심",
        "symptom": "고열과 기침, 가슴 불편감을 호소한다.",
        "hint": "열이 높고 숨을 쉴 때 답답하다고 한다.",
        "severity": "중등",
        "best_test": "X-ray",
        "test_result": "폐에 염증이 의심되는 음영이 확인되었다.",
        "treatment": "항생제 처치"
    },
    {
        "case": "급성 충수염",
        "symptom": "오른쪽 아랫배가 심하게 아프다고 한다.",
        "hint": "통증이 점점 심해지고 구역감을 동반한다.",
        "severity": "응급",
        "best_test": "CT",
        "test_result": "충수돌기 염증이 의심되는 소견이 보인다.",
        "treatment": "응급수술 호출"
    },
    {
        "case": "뇌졸중 의심",
        "symptom": "말이 어눌하고 한쪽 팔다리 힘이 약하다.",
        "hint": "얼굴 한쪽이 처져 보이며 보호자가 매우 급해한다.",
        "severity": "응급",
        "best_test": "CT",
        "test_result": "뇌 이상이 의심되어 즉시 전문 진료가 필요하다.",
        "treatment": "뇌 CT 후 신경과 호출"
    },
    {
        "case": "긴장성 두통",
        "symptom": "머리가 조이고 아프다고 호소한다.",
        "hint": "시험 준비로 며칠째 잠을 잘 못 잤다고 한다.",
        "severity": "경증",
        "best_test": "추가 문진",
        "test_result": "과로와 수면 부족으로 인한 두통 가능성이 높다.",
        "treatment": "안정 및 진통제"
    }
]

ALL_TREATMENTS = [
    "수액 처치",
    "깁스/고정",
    "포도당 투여",
    "기관지 흡입치료",
    "항생제 처치",
    "응급수술 호출",
    "뇌 CT 후 신경과 호출",
    "안정 및 진통제"
]

NAMES = ["김민서", "이서윤", "박지후", "최유진", "정하람", "조수아", "윤지안", "한서진", "오지우", "신예린"]


# ============================================================
# 상점 데이터
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
# 이벤트
# ============================================================

EVENTS = [
    {"name": "조용한 야간", "text": "응급실이 비교적 조용하다. 특별한 효과는 없다.", "effect": "none"},
    {"name": "야간 커피", "text": "간호사가 커피를 건네줬다. 에너지 +1", "effect": "energy"},
    {"name": "친절한 인턴", "text": "인턴이 도와준다. 평판 +1", "effect": "reputation"},
    {"name": "구급차 도착", "text": "추가 환자가 한 명 더 대기실에 도착했다.", "effect": "extra_patient"},
    {"name": "복도 소란", "text": "응급실이 어수선하다. 대기 환자들의 불만이 커진다.", "effect": "tension"}
]


# ============================================================
# 기본 프로필 초기화
# ============================================================

def initialize_profile():
    defaults = {
        "wallet": 0,
        "night": 1,
        "owned_hair": ["단발"],
        "owned_eye_shape": ["둥근 눈"],
        "owned_eye_color": ["갈색"],
        "hair": "단발",
        "eye_shape": "둥근 눈",
        "eye_color": "갈색",
        "extra_life": 0,
        "game_started": False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================
# 환자 생성
# ============================================================

def make_patient():
    template = random.choice(PATIENT_TEMPLATES).copy()
    template["uid"] = random.randint(10000, 99999)
    template["name"] = random.choice(NAMES)
    template["age"] = random.randint(12, 78)
    template["waiting"] = 0
    return template


def fill_queue(target=4):
    while len(st.session_state.queue) < target:
        st.session_state.queue.append(make_patient())


# ============================================================
# 밤 시작
# ============================================================

def start_shift():
    st.session_state.turns_left = SHIFT_CASES
    st.session_state.health = 3 + st.session_state.extra_life
    st.session_state.extra_life = 0
    st.session_state.reputation = 5
    st.session_state.energy = 4

    st.session_state.saved = 0
    st.session_state.failed = 0
    st.session_state.shift_earnings = 0

    st.session_state.queue = []
    fill_queue(4)

    st.session_state.active_patient = None
    st.session_state.phase = "waiting"

    st.session_state.triage_choice = None
    st.session_state.triage_bonus_current = 0
    st.session_state.test_bonus_current = 0
    st.session_state.test_result = ""
    st.session_state.treatment_options = []

    st.session_state.event_text = "야간 근무가 시작되었습니다."
    st.session_state.message = ""
    st.session_state.shift_over = False
    st.session_state.logs = []

    st.session_state.game_started = True


# ============================================================
# 이벤트 적용
# ============================================================

def apply_random_event():
    event = random.choice(EVENTS)
    st.session_state.event_text = f"⚡ {event['name']} : {event['text']}"

    if event["effect"] == "energy":
        st.session_state.energy = min(6, st.session_state.energy + 1)

    elif event["effect"] == "reputation":
        st.session_state.reputation = min(7, st.session_state.reputation + 1)

    elif event["effect"] == "extra_patient":
        st.session_state.queue.append(make_patient())

    elif event["effect"] == "tension":
        for p in st.session_state.queue:
            p["waiting"] += 1


# ============================================================
# 대기 환자 시간 흐름
# ============================================================

def age_waiting_patients():
    remaining = []

    for p in st.session_state.queue:
        p["waiting"] += 1

        if p["severity"] == "응급":
            limit = 2
        elif p["severity"] == "중등":
            limit = 4
        else:
            limit = 5

        if p["waiting"] >= limit:
            st.session_state.failed += 1
            st.session_state.reputation -= 1
            st.session_state.logs.append(
                f"{p['name']} 환자가 너무 오래 기다리다 돌아갔습니다."
            )
        else:
            remaining.append(p)

    st.session_state.queue = remaining


# ============================================================
# 턴 종료
# ============================================================

def end_turn():
    st.session_state.turns_left -= 1
    age_waiting_patients()
    apply_random_event()
    fill_queue(4)

    st.session_state.active_patient = None
    st.session_state.phase = "waiting"
    st.session_state.triage_choice = None
    st.session_state.triage_bonus_current = 0
    st.session_state.test_bonus_current = 0
    st.session_state.test_result = ""
    st.session_state.treatment_options = []

    if st.session_state.turns_left <= 0 or st.session_state.reputation <= 0 or st.session_state.health <= 0:
        st.session_state.shift_over = True


# ============================================================
# 환자 선택
# ============================================================

def choose_patient(uid):
    selected = None
    new_queue = []

    for p in st.session_state.queue:
        if p["uid"] == uid:
            selected = p
        else:
            new_queue.append(p)

    st.session_state.queue = new_queue
    st.session_state.active_patient = selected
    st.session_state.phase = "consult"
    st.session_state.message = ""


# ============================================================
# 추가 문진
# ============================================================

def ask_more():
    if st.session_state.energy <= 0:
        st.session_state.message = "에너지가 부족합니다."
        return

    st.session_state.energy -= 1
    st.session_state.message = st.session_state.active_patient["hint"]


# ============================================================
# 트리아지 결정
# ============================================================

def confirm_triage(choice):
    st.session_state.triage_choice = choice

    if choice == st.session_state.active_patient["severity"]:
        st.session_state.triage_bonus_current = TRIAGE_BONUS
    else:
        st.session_state.triage_bonus_current = 0

    st.session_state.phase = "test"


# ============================================================
# 검사 진행
# ============================================================

def do_test(test_name):
    patient = st.session_state.active_patient
    st.session_state.test_bonus_current = 0

    if test_name == patient["best_test"]:
        st.session_state.test_bonus_current = TEST_BONUS
        st.session_state.test_result = patient["test_result"]
    elif test_name == "검사 없이 바로 치료":
        st.session_state.test_result = "추가 검사를 생략하고 바로 치료를 시도합니다."
    else:
        st.session_state.test_result = "결정적인 정보는 얻지 못했습니다."

    options = [patient["treatment"]]
    wrongs = [x for x in ALL_TREATMENTS if x != patient["treatment"]]
    options.extend(random.sample(wrongs, 3))
    random.shuffle(options)

    st.session_state.treatment_options = options
    st.session_state.phase = "treatment"


# ============================================================
# 치료 진행
# ============================================================

def treat_patient(choice):
    patient = st.session_state.active_patient

    if choice == patient["treatment"]:
        reward = BASE_REWARD + st.session_state.triage_bonus_current + st.session_state.test_bonus_current
        st.session_state.shift_earnings += reward
        st.session_state.saved += 1
        st.session_state.message = f"치료 성공! 이번 환자로 {reward:,}원을 벌었습니다."
    else:
        if patient["severity"] == "응급":
            st.session_state.reputation -= 2
            st.session_state.health -= 1
        else:
            st.session_state.reputation -= 1

        st.session_state.failed += 1
        st.session_state.message = "치료에 실패했습니다."

    st.session_state.phase = "result"


# ============================================================
# 휴게실 쉬기
# ============================================================

def take_rest():
    st.session_state.energy = min(6, st.session_state.energy + 2)
    st.session_state.message = "잠깐 쉬면서 에너지를 회복했습니다. (+2)"
    end_turn()


# ============================================================
# 급여 정산
# ============================================================

def settle_salary():
    if "salary_settled" not in st.session_state:
        st.session_state.salary_settled = False

    if not st.session_state.salary_settled:
        st.session_state.wallet += st.session_state.shift_earnings
        st.session_state.salary_settled = True


# ============================================================
# 캐릭터 표시
# ============================================================

def show_character():
    hair_icon = {
        "단발": "💇🏻‍♀️",
        "긴 머리": "👩🏻",
        "포니테일": "👱🏻‍♀️"
    }[st.session_state.hair]

    eye_shape_text = {
        "둥근 눈": "● ●",
        "웃는 눈": "⌒ ⌒",
        "날카로운 눈": "◢ ◣"
    }[st.session_state.eye_shape]

    eye_color_text = {
        "갈색": "🟤",
        "파란색": "🔵",
        "보라색": "🟣"
    }[st.session_state.eye_color]

    st.markdown(f"""
    <div class="character-card">
        <div class="character-big">{hair_icon}</div>
        <b>야간 응급실 의사</b>
        <br><br>
        머리 : <b>{st.session_state.hair}</b><br>
        눈 모양 : <b>{st.session_state.eye_shape}</b> {eye_shape_text}<br>
        눈 색 : <b>{st.session_state.eye_color}</b> {eye_color_text}
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 구매
# ============================================================

def buy_life():
    if st.session_state.wallet < EXTRA_LIFE_PRICE:
        st.warning("돈이 부족합니다.")
        return

    st.session_state.wallet -= EXTRA_LIFE_PRICE
    st.session_state.extra_life += 1


def buy_item(name, price, category):
    if st.session_state.wallet < price:
        st.warning("돈이 부족합니다.")
        return

    if category == "hair":
        if name not in st.session_state.owned_hair:
            st.session_state.owned_hair.append(name)

    elif category == "eye_shape":
        if name not in st.session_state.owned_eye_shape:
            st.session_state.owned_eye_shape.append(name)

    elif category == "eye_color":
        if name not in st.session_state.owned_eye_color:
            st.session_state.owned_eye_color.append(name)

    st.session_state.wallet -= price


# ============================================================
# 이미지 표시
# ============================================================

def show_patient_image():
    patient = st.session_state.active_patient
    if patient is None:
        return

    # 지금은 이미지 없어도 되게 처리
    st.markdown("""
    <div class="patient-photo">
    👤
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 초기화
# ============================================================

initialize_profile()


# ============================================================
# 제목
# ============================================================

st.markdown("""
<div class="game-title">MIDNIGHT ER : NIGHT DUTY</div>
<div class="game-sub">응급실 운영 · 진단 · 치료 시뮬레이션</div>
""", unsafe_allow_html=True)


# ============================================================
# 시작 화면
# ============================================================

if not st.session_state.game_started:
    c1, c2 = st.columns([1.7, 1])

    with c1:
        st.markdown(f"""
        <div class="card">
            <h2>🌙 NIGHT {st.session_state.night}</h2>
            오늘 밤 너는 야간 응급실 담당 의사야.
            <br><br>
            대기 환자들 중 누구를 먼저 진료할지 고르고,
            증상을 파악한 뒤 중증도를 분류하고,
            필요한 검사와 치료를 선택해야 해.
            <br><br>
            환자를 정확히 치료하면 급여를 받지만,
            실수하면 평판과 체력이 깎여.
            <br><br>
            한밤을 무사히 운영해 보자.
        </div>
        """, unsafe_allow_html=True)

    with c2:
        show_character()

    st.write("")

    if st.button("🏥 야간 응급실 시작", use_container_width=True):
        start_shift()
        st.session_state.salary_settled = False
        st.rerun()


# ============================================================
# 밤 종료
# ============================================================

elif st.session_state.shift_over:
    settle_salary()

    st.markdown(f"""
    <div class="card">
        <h2>🌅 NIGHT {st.session_state.night} 종료</h2>
        살린 환자 수 : <b>{st.session_state.saved}명</b><br><br>
        치료 실패 / 놓친 환자 수 : <b>{st.session_state.failed}명</b><br><br>
        이번 밤 급여 : <b>{st.session_state.shift_earnings:,}원</b><br><br>
        현재 보유 금액 : <b>{st.session_state.wallet:,}원</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🛍️ 상점")

    left, right = st.columns([1, 1])

    with left:
        st.markdown(f"""
        <div class="shop-card">
            <div style="font-size:40px;">❤️</div>
            <b>목숨 +1</b><br><br>
            다음 밤 시작 체력 +1<br><br>
            <b>{EXTRA_LIFE_PRICE:,}원</b>
        </div>
        """, unsafe_allow_html=True)

        if st.button("❤️ 목숨 구매", use_container_width=True):
            buy_life()
            st.rerun()

    with right:
        show_character()

    st.markdown("### 💇 머리")
    hair_cols = st.columns(3)
    for i, (name, price) in enumerate(HAIR_ITEMS.items()):
        with hair_cols[i]:
            st.markdown(f"""
            <div class="shop-card">
                <b>{name}</b><br><br>
                {price:,}원
            </div>
            """, unsafe_allow_html=True)

            if name in st.session_state.owned_hair:
                if st.button("착용", key=f"hair_{name}", use_container_width=True):
                    st.session_state.hair = name
                    st.rerun()
            else:
                if st.button("구매", key=f"buyhair_{name}", use_container_width=True):
                    buy_item(name, price, "hair")
                    st.rerun()

    st.markdown("### 👁️ 눈 모양")
    eye_cols = st.columns(3)
    for i, (name, price) in enumerate(EYE_SHAPE_ITEMS.items()):
        with eye_cols[i]:
            st.markdown(f"""
            <div class="shop-card">
                <b>{name}</b><br><br>
                {price:,}원
            </div>
            """, unsafe_allow_html=True)

            if name in st.session_state.owned_eye_shape:
                if st.button("착용", key=f"eyeshape_{name}", use_container_width=True):
                    st.session_state.eye_shape = name
                    st.rerun()
            else:
                if st.button("구매", key=f"buyeyeshape_{name}", use_container_width=True):
                    buy_item(name, price, "eye_shape")
                    st.rerun()

    st.markdown("### 🎨 눈 색")
    color_cols = st.columns(3)
    for i, (name, price) in enumerate(EYE_COLOR_ITEMS.items()):
        with color_cols[i]:
            st.markdown(f"""
            <div class="shop-card">
                <b>{name}</b><br><br>
                {price:,}원
            </div>
            """, unsafe_allow_html=True)

            if name in st.session_state.owned_eye_color:
                if st.button("착용", key=f"eyecolor_{name}", use_container_width=True):
                    st.session_state.eye_color = name
                    st.rerun()
            else:
                if st.button("구매", key=f"buyeyecolor_{name}", use_container_width=True):
                    buy_item(name, price, "eye_color")
                    st.rerun()

    st.write("")
    if st.button("🌙 구매하지 않고 다음 밤으로", use_container_width=True):
        st.session_state.night += 1
        start_shift()
        st.session_state.salary_settled = False
        st.rerun()


# ============================================================
# 게임 진행 중
# ============================================================

else:
    s1, s2, s3, s4, s5 = st.columns(5)

    with s1:
        st.markdown(f"""
        <div class="stat-card">
            NIGHT<br><b>{st.session_state.night}</b>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown(f"""
        <div class="stat-card">
            남은 턴<br><b>{st.session_state.turns_left}</b>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        hearts = "❤️" * max(0, st.session_state.health)
        st.markdown(f"""
        <div class="stat-card">
            체력<br>{hearts}
        </div>
        """, unsafe_allow_html=True)

    with s4:
        st.markdown(f"""
        <div class="stat-card">
            평판<br><b>{st.session_state.reputation}</b>
        </div>
        """, unsafe_allow_html=True)

    with s5:
        st.markdown(f"""
        <div class="stat-card">
            에너지<br><b>{st.session_state.energy}</b>
        </div>
        """, unsafe_allow_html=True)

    st.caption(f"💰 현재 예상 급여 : {st.session_state.shift_earnings:,}원")

    phase_name = {
        "waiting": "대기실",
        "consult": "진찰실 - 문진",
        "test": "검사실 - 검사 선택",
        "treatment": "진료실 - 치료 선택",
        "result": "결과 확인"
    }[st.session_state.phase]

    st.markdown(f"""
    <div class="location-box">
        📍 현재 위치 : <b>{phase_name}</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="event-box">
        {st.session_state.event_text}
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.message:
        st.info(st.session_state.message)

    # --------------------------------------------------------
    # 1) 대기실
    # --------------------------------------------------------
    if st.session_state.phase == "waiting":
        st.markdown("## 🪑 응급실 대기실")
        st.caption("누구를 먼저 진료할지 선택하세요. 너무 오래 기다리면 평판이 떨어집니다.")

        qcols = st.columns(2)

        for idx, p in enumerate(st.session_state.queue):
            with qcols[idx % 2]:
                severity_emoji = {
                    "경증": "🟢",
                    "중등": "🟠",
                    "응급": "🔴"
                }[p["severity"]]

                st.markdown(f"""
                <div class="queue-card">
                    <b>{p['name']}</b> / {p['age']}세<br><br>
                    증상 : {p['symptom']}<br><br>
                    긴급도 힌트 : {severity_emoji} {p['severity']} 가능성<br><br>
                    대기 시간 : {p['waiting']}턴
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"{p['name']} 환자 보기", key=f"pick_{p['uid']}", use_container_width=True):
                    choose_patient(p["uid"])
                    st.rerun()

        st.write("")
        if st.button("☕ 1턴 쉬고 에너지 +2", use_container_width=True):
            take_rest()
            st.rerun()

        if st.session_state.logs:
            with st.expander("오늘의 응급실 기록 보기"):
                for log in st.session_state.logs:
                    st.write("•", log)

    # --------------------------------------------------------
    # 2) 문진
    # --------------------------------------------------------
    elif st.session_state.phase == "consult":
        patient = st.session_state.active_patient

        left, right = st.columns([1, 1])

        with left:
            show_patient_image()

        with right:
            st.markdown(f"""
            <div class="card">
                <h3>{patient['name']} / {patient['age']}세</h3>
                <b>주증상</b><br><br>
                {patient['symptom']}<br><br>
                먼저 환자를 더 문진하거나,
                바로 중증도를 판단할 수 있습니다.
            </div>
            """, unsafe_allow_html=True)

            if st.button("🗣️ 추가 문진하기 (에너지 -1)", use_container_width=True):
                ask_more()
                st.rerun()

        st.markdown("### 중증도 분류")
        triage = st.radio(
            "이 환자의 중증도를 선택하세요.",
            ["경증", "중등", "응급"],
            horizontal=True
        )

        if st.button("📋 중증도 확정", use_container_width=True):
            confirm_triage(triage)
            st.rerun()

    # --------------------------------------------------------
    # 3) 검사 선택
    # --------------------------------------------------------
    elif st.session_state.phase == "test":
        patient = st.session_state.active_patient

        st.markdown(f"""
        <div class="guide-box">
            <b>{patient['name']} 환자</b><br><br>
            어떤 검사를 먼저 진행할지 선택하세요.
        </div>
        """, unsafe_allow_html=True)

        test_choice = st.radio(
            "검사 선택",
            ["추가 문진", "혈액검사", "X-ray", "CT", "검사 없이 바로 치료"],
            horizontal=False
        )

        if st.button("🧪 검사 진행", use_container_width=True):
            do_test(test_choice)
            st.rerun()

    # --------------------------------------------------------
    # 4) 치료 선택
    # --------------------------------------------------------
    elif st.session_state.phase == "treatment":
        patient = st.session_state.active_patient

        st.markdown(f"""
        <div class="guide-box">
            <b>검사 결과</b><br><br>
            {st.session_state.test_result}<br><br>
            이제 가장 적절한 치료를 선택하세요.
        </div>
        """, unsafe_allow_html=True)

        treatment = st.radio(
            "치료 선택",
            st.session_state.treatment_options,
            horizontal=False
        )

        if st.button("💉 치료 실행", use_container_width=True):
            treat_patient(treatment)
            st.rerun()

    # --------------------------------------------------------
    # 5) 결과 확인
    # --------------------------------------------------------
    elif st.session_state.phase == "result":
        patient = st.session_state.active_patient

        if "치료 성공" in st.session_state.message:
            st.markdown(f"""
            <div class="success-box">
                <h3>✅ 치료 성공</h3>
                {patient['name']} 환자를 성공적으로 치료했습니다.<br><br>
                기본 급여 : {BASE_REWARD:,}원<br>
                트리아지 보너스 : {st.session_state.triage_bonus_current:,}원<br>
                검사 보너스 : {st.session_state.test_bonus_current:,}원
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="fail-box">
                <h3>❌ 치료 실패</h3>
                {patient['name']} 환자의 치료 판단이 적절하지 않았습니다.<br><br>
                실제 필요한 치료는 <b>{patient['treatment']}</b>였습니다.
            </div>
            """, unsafe_allow_html=True)

        if st.button("➡️ 다음 환자로", use_container_width=True):
            end_turn()
            st.rerun()

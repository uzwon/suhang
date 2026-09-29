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

/* 전체 배경 */
.stApp {
    background:
        linear-gradient(
            180deg,
            #0b1117 0%,
            #121c24 45%,
            #0a1015 100%
        );
    color: #eaf2f5;
}

/* 본문 폭 */
.block-container {
    max-width: 1180px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}

/* 제목 */
.game-title {
    font-size: 40px;
    font-weight: 900;
    color: #f5fbfd;
    letter-spacing: 2px;
    line-height: 1.2;
}

.game-subtitle {
    color: #98b0bc;
    font-size: 14px;
    margin-top: 4px;
}

/* 상단 상태 카드 */
.status-card {
    background: #16232d;
    border: 1px solid #314654;
    border-radius: 15px;
    padding: 14px;
    text-align: center;
    color: #edf5f7;
    box-shadow: 0 6px 20px rgba(0,0,0,0.18);
}

/* 현재 위치 카드 */
.location-box {
    background: linear-gradient(135deg, #edf5f7 0%, #e3eef1 100%);
    color: #243941;
    border-radius: 16px;
    border-left: 6px solid #6c98a8;
    padding: 18px 20px;
    margin-top: 18px;
    margin-bottom: 18px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}

/* 기본 패널 */
.panel {
    background: linear-gradient(180deg, #f7fbfc 0%, #edf4f6 100%);
    color: #253941;
    border-radius: 18px;
    padding: 22px;
    border: 1px solid #abc0c8;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

/* 사진 카드 */
.photo-card {
    background: linear-gradient(180deg, #d9e8ec 0%, #cfe0e5 100%);
    border: 1px solid #8da7b1;
    border-radius: 18px;
    min-height: 430px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #4f6670;
    font-size: 100px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

/* 검사 결과 */
.exam-box {
    background: #eaf1fa;
    color: #2e495e;
    border-left: 6px solid #668ab1;
    border-radius: 12px;
    padding: 18px;
    margin-top: 15px;
    line-height: 1.8;
}

/* 성공 박스 */
.success-box {
    background: #e8f7ee;
    color: #2c503b;
    border-left: 6px solid #5ca277;
    border-radius: 12px;
    padding: 18px;
    margin-top: 15px;
    line-height: 1.8;
}

/* 실패 박스 */
.danger-box {
    background: #faeaed;
    color: #673942;
    border-left: 6px solid #bf5b6b;
    border-radius: 12px;
    padding: 18px;
    margin-top: 15px;
    line-height: 1.8;
}

/* 물품 카드 */
.item-card {
    background: linear-gradient(180deg, #f7fbfc 0%, #edf4f6 100%);
    color: #283d46;
    border-radius: 15px;
    padding: 19px;
    border: 1px solid #a8bcc4;
    text-align: center;
    min-height: 120px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
}

/* 인벤토리 */
.inventory {
    background: linear-gradient(180deg, #1c2b35 0%, #18252e 100%);
    color: #eef5f7;
    border: 1px solid #405866;
    border-radius: 14px;
    padding: 14px 18px;
    margin-top: 12px;
    margin-bottom: 14px;
}

/* 지도 안 방 카드 */
.map-room {
    background: #eef4f6;
    color: #243841;
    border-radius: 13px;
    border: 1px solid #adbec5;
    padding: 15px;
    text-align: center;
    margin-bottom: 8px;
    font-weight: 700;
}

/* 밤 창문 */
.night-window-wrap {
    background: linear-gradient(180deg, #eef4f6 0%, #e2edf0 100%);
    border: 1px solid #b0c0c7;
    border-radius: 18px;
    padding: 14px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    margin-top: 18px;
    margin-bottom: 18px;
}

.night-window-title {
    color: #2a4048;
    font-weight: 800;
    margin-bottom: 12px;
    font-size: 15px;
}

.night-window {
    position: relative;
    width: 100%;
    height: 190px;
    border-radius: 14px;
    overflow: hidden;
    background: linear-gradient(180deg, #07131f 0%, #11263d 55%, #1a3552 100%);
    border: 6px solid #d8e5ea;
    box-sizing: border-box;
}

.window-frame-v1, .window-frame-v2 {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 6px;
    background: rgba(220,235,240,0.95);
    left: 33.3%;
}

.window-frame-v2 {
    left: 66.6%;
}

.window-frame-h {
    position: absolute;
    left: 0;
    right: 0;
    height: 6px;
    top: 50%;
    background: rgba(220,235,240,0.95);
}

.moon {
    position: absolute;
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: #fff6bf;
    top: 22px;
    right: 38px;
    box-shadow: 0 0 22px rgba(255,244,180,0.75);
}

.star {
    position: absolute;
    width: 4px;
    height: 4px;
    background: white;
    border-radius: 50%;
    opacity: 0.9;
}

.s1 { top: 30px; left: 50px; }
.s2 { top: 52px; left: 150px; }
.s3 { top: 74px; left: 245px; }
.s4 { top: 38px; left: 310px; }
.s5 { top: 64px; left: 420px; }
.s6 { top: 95px; left: 520px; }
.s7 { top: 118px; left: 120px; }
.s8 { top: 100px; left: 360px; }

.city {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 72px;
    background:
        linear-gradient(180deg, transparent 0%, transparent 25%, #0d1b28 26%, #0d1b28 100%);
}

.b1, .b2, .b3, .b4, .b5, .b6 {
    position: absolute;
    bottom: 0;
    background: #102234;
}

.b1 { left: 18px;  width: 55px; height: 52px; }
.b2 { left: 95px;  width: 70px; height: 86px; }
.b3 { left: 182px; width: 48px; height: 64px; }
.b4 { left: 252px; width: 78px; height: 104px; }
.b5 { left: 350px; width: 65px; height: 72px; }
.b6 { left: 438px; width: 92px; height: 96px; }

.window-note {
    margin-top: 10px;
    color: #546a74;
    font-size: 13px;
}

/* 버튼 */
.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 10px;
    font-weight: 800;
}

/* alert text 가독성 */
.stAlert {
    color: #1f2f36;
}

/* 멀티셀렉트 텍스트 가독성 */
div[data-baseweb="select"] * {
    color: #22363f !important;
}

/* popover 안 글씨 */
[data-testid="stPopover"] * {
    color: #22363f;
}

/* 일반 텍스트 */
p, li, div, label, span {
    line-height: 1.6;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. 환자 데이터
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
    if st.session_state.patient_number >= len(st.session_state.order):
        return None

    patient_index = st.session_state.order[st.session_state.patient_number]
    return PATIENTS[patient_index]


# =========================================================
# 7. 이미지 표시
# =========================================================

def show_patient(patient):
    path = IMAGE_FOLDER / patient["image"]

    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.markdown(
            """
            <div class="photo-card">
            👤
            </div>
            """,
            unsafe_allow_html=True
        )
        st.caption("images 폴더에 환자 사진을 넣으면 여기에 표시됩니다.")


# =========================================================
# 8. 밤 창문 표시
# =========================================================

def render_night_window():
    st.markdown(
        """
        <div class="night-window-wrap">
            <div class="night-window-title">🌙 병원 창문 밖 야경</div>
            <div class="night-window">
                <div class="moon"></div>

                <div class="star s1"></div>
                <div class="star s2"></div>
                <div class="star s3"></div>
                <div class="star s4"></div>
                <div class="star s5"></div>
                <div class="star s6"></div>
                <div class="star s7"></div>
                <div class="star s8"></div>

                <div class="window-frame-v1"></div>
                <div class="window-frame-v2"></div>
                <div class="window-frame-h"></div>

                <div class="city">
                    <div class="b1"></div>
                    <div class="b2"></div>
                    <div class="b3"></div>
                    <div class="b4"></div>
                    <div class="b5"></div>
                    <div class="b6"></div>
                </div>
            </div>
            <div class="window-note">
                고요한 밤, 병원은 아직 깨어 있습니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 9. 장소 이동
# =========================================================

def move_room(room):
    st.session_state.location = room


# =========================================================
# 10. 새로운 환자
# =========================================================

def next_patient():
    st.session_state.patient_number += 1
    st.session_state.location = "데스크"
    st.session_state.inventory = []
    st.session_state.patient_admitted = False
    st.session_state.examined = False
    st.session_state.completed = False
    st.session_state.message = ""

    if st.session_state.patient_number >= len(st.session_state.order):
        st.session_state.game_over = True


# =========================================================
# 11. 데스크 판단
# =========================================================

def desk_decision(choice):
    patient = current_patient()

    if choice == "admit":
        if patient["anomaly"]:
            st.session_state.lives -= 1
            st.session_state.message = "❌ 변칙 환자를 병원 안으로 들였습니다."
            if st.session_state.lives <= 0:
                st.session_state.game_over = True
        else:
            st.session_state.score += 100
            st.session_state.patient_admitted = True
            st.session_state.location = "진료실"
            st.session_state.message = "✅ 정상 환자입니다. 환자가 진료실로 이동했습니다."

    elif choice == "block":
        if patient["anomaly"]:
            st.session_state.score += 150
            st.session_state.completed = True
            st.session_state.message = "🚨 변칙 발견! 병원 출입을 차단했습니다."
        else:
            st.session_state.lives -= 1
            st.session_state.message = "❌ 정상 환자의 출입을 막았습니다."
            if st.session_state.lives <= 0:
                st.session_state.game_over = True


# =========================================================
# 12. 검사
# =========================================================

def examine_patient():
    st.session_state.examined = True
    st.session_state.score += 50
    st.session_state.message = "🔍 검사가 완료되었습니다."


# =========================================================
# 13. 물품 가져오기
# =========================================================

def add_item(item):
    if item not in st.session_state.inventory:
        if len(st.session_state.inventory) >= 4:
            st.warning("가방이 가득 찼습니다. 최대 4개까지 들 수 있습니다.")
            return

        st.session_state.inventory.append(item)
        st.success(f"🎒 {item}을(를) 인벤토리에 넣었습니다.")
    else:
        st.warning("이미 가지고 있는 물품입니다.")


# =========================================================
# 14. 인벤토리에서 물품 적용
# =========================================================

def apply_items(selected_items):
    patient = current_patient()
    required = set(patient["items"])
    selected = set(selected_items)

    if len(selected_items) != 2:
        st.warning("치료에 사용할 물품 2개를 선택하세요.")
        return

    if selected == required:
        st.session_state.score += 200
        st.session_state.completed = True
        st.session_state.message = "✅ 필요한 물품을 정확하게 적용했습니다. 환자 진료가 완료되었습니다."
    else:
        st.session_state.lives -= 1
        st.session_state.message = "❌ 필요한 물품 조합이 아닙니다."
        if st.session_state.lives <= 0:
            st.session_state.game_over = True


# =========================================================
# 15. Session State
# =========================================================

if "started" not in st.session_state:
    st.session_state.started = False

if "game_over" not in st.session_state:
    st.session_state.game_over = False


# =========================================================
# 16. 제목
# =========================================================

left_title, right_title = st.columns([4, 1])

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
# 17. 시작 화면
# =========================================================

if not st.session_state.started:
    st.markdown(
        """
        <div class="panel">

        <h2 style="color:#233942;">🌙 오늘 밤, 당신은 당직 의사입니다.</h2>

        <div style="color:#2f4650;">
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

        </div>
        """,
        unsafe_allow_html=True
    )

    render_night_window()

    st.write("")

    if st.button("🌙 당직 시작", use_container_width=True):
        initialize_game()
        st.rerun()


# =========================================================
# 18. 게임 종료
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
        <div class="panel" style="text-align:center;">
        <h2 style="color:#233942;">🌅 당직 종료</h2>

        <div style="
        font-size:85px;
        font-weight:900;
        color:#527e91;
        ">
        {grade}
        </div>

        <h2 style="color:#233942;">최종 점수 : {score}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    render_night_window()

    if st.button("🔄 다시 시작", use_container_width=True):
        initialize_game()
        st.rerun()


# =========================================================
# 19. 게임 플레이
# =========================================================

else:
    patient = current_patient()

    # 상단 상태바
    s1, s2, s3, s4 = st.columns([1, 1, 1, 1])

    with s1:
        st.markdown(
            f"""
            <div class="status-card">
            PATIENT<br>
            <b>{st.session_state.patient_number + 1}/{len(PATIENTS)}</b>
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
        with st.popover("🗺️ 병원 지도", use_container_width=True):
            st.markdown("### 🏥 병원 내부 지도")

            st.markdown('<div class="map-room">🖥️ 데스크</div>', unsafe_allow_html=True)
            if st.button("데스크로 이동", key="map_desk"):
                move_room("데스크")
                st.rerun()

            st.markdown("↓")

            c1, c2 = st.columns(2)

            with c1:
                st.markdown('<div class="map-room">🛏️ 진료실</div>', unsafe_allow_html=True)
                if st.button("진료실로 이동", key="map_treatment"):
                    move_room("진료실")
                    st.rerun()

            with c2:
                st.markdown('<div class="map-room">📦 물품실</div>', unsafe_allow_html=True)
                if st.button("물품실로 이동", key="map_supply"):
                    move_room("물품실")
                    st.rerun()

    # 현재 위치 + 야간 창문
    loc_col, window_col = st.columns([2.2, 1])

    with loc_col:
        st.markdown(
            f"""
            <div class="location-box">
            📍 현재 위치 : <b>{st.session_state.location}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    with window_col:
        render_night_window()

    # 인벤토리
    inventory_text = " · ".join(st.session_state.inventory) if st.session_state.inventory else "비어 있음"

    st.markdown(
        f"""
        <div class="inventory">
        🎒 <b>INVENTORY</b>&nbsp;&nbsp; {inventory_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    # 메시지
    if st.session_state.message:
        st.info(st.session_state.message)

    # =====================================================
    # 데스크
    # =====================================================

    if st.session_state.location == "데스크":
        st.markdown("## 🖥️ 병원 데스크")
        st.caption("환자의 얼굴만 보고 병원 안으로 들일지 판단하세요.")

        show_patient(patient)

        if not st.session_state.patient_admitted and not st.session_state.completed:
            st.write("")
            b1, b2 = st.columns(2)

            with b1:
                if st.button("🏥 병원 안으로 들인다", use_container_width=True):
                    desk_decision("admit")
                    st.rerun()

            with b2:
                if st.button("🚨 출입을 막는다", use_container_width=True):
                    desk_decision("block")
                    st.rerun()

        if st.session_state.completed and patient["anomaly"]:
            st.markdown(
                f"""
                <div class="success-box">
                <b>🚨 변칙 환자 차단 완료</b><br><br>
                {patient.get("anomaly_reason", "사진 속 변칙을 발견했습니다.")}
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("다음 환자 →", use_container_width=True):
                next_patient()
                st.rerun()

    # =====================================================
    # 진료실
    # =====================================================

    elif st.session_state.location == "진료실":
        st.markdown("## 🛏️ 진료실")

        if not st.session_state.patient_admitted:
            st.warning("현재 진료실에 들어온 환자가 없습니다.")
        else:
            left, right = st.columns([1, 1.1])

            with left:
                show_patient(patient)

            with right:
                st.markdown(
                    f"""
                    <div class="panel">
                    <h3 style="color:#233942;">👤 환자 #{patient["id"]:02d}</h3>

                    <div style="color:#304853;">
                    환자가 진료실에서 기다리고 있습니다.

                    <br><br>

                    먼저 환자를 검사해 필요한 물품을 확인하세요.
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            if not st.session_state.examined:
                if st.button("🔍 환자 검사", use_container_width=True):
                    examine_patient()
                    st.rerun()

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

                if st.session_state.completed:
                    st.markdown(
                        """
                        <div class="success-box">
                        ✅ 환자 진료가 완료되었습니다.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button("다음 환자 →", use_container_width=True):
                        next_patient()
                        st.rerun()

                else:
                    if not st.session_state.inventory:
                        st.warning("🎒 인벤토리가 비어 있습니다. 지도에서 물품실로 이동하세요.")
                    else:
                        st.markdown("### 🎒 환자에게 적용할 물품 선택")

                        selected_items = st.multiselect(
                            "인벤토리에서 2개를 선택하세요.",
                            options=st.session_state.inventory,
                            max_selections=2
                        )

                        if st.button("🩺 선택한 물품 적용", use_container_width=True):
                            apply_items(selected_items)
                            st.rerun()

    # =====================================================
    # 물품실
    # =====================================================

    elif st.session_state.location == "물품실":
        st.markdown("## 📦 치료 물품실")
        st.caption("필요하다고 생각하는 물품을 인벤토리에 담으세요.")

        rows = [ALL_ITEMS[i:i + 3] for i in range(0, len(ALL_ITEMS), 3)]

        for row_index, row in enumerate(rows):
            columns = st.columns(len(row))

            for index, item in enumerate(row):
                with columns[index]:
                    st.markdown(
                        f"""
                        <div class="item-card">
                        <div style="font-size:32px;">🧰</div>
                        <br>
                        <b>{item}</b>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button("🎒 가져가기", key=f"item_{row_index}_{index}", use_container_width=True):
                        add_item(item)
                        st.rerun()

import math
from datetime import datetime

import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# 1. App settings and fixed educational model parameters
# ---------------------------------------------------------
st.set_page_config(
    page_title="Oral pH Lab",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded",
)

STIMULUS_PRESETS = {
    "약한 산 생성 자극": {
        "drop": 0.7,
        "half_life": 22,
        "example": "식사 후 비교적 작은 산도 변화가 나타나는 상황을 단순화한 값",
    },
    "중간 산 생성 자극": {
        "drop": 1.1,
        "half_life": 30,
        "example": "탄수화물 간식 섭취 뒤의 산도 변화를 단순화한 값",
    },
    "강한 산 생성 자극": {
        "drop": 1.5,
        "half_life": 38,
        "example": "당류가 포함된 간식·음료 섭취 뒤의 변화를 단순화한 값",
    },
}

RECOVERY_OPTIONS = {
    "기본 회복": 1.00,
    "물로 입안을 헹군 상황": 0.85,
    "침 분비가 증가한 상황": 0.72,
}


# ---------------------------------------------------------
# 2. Reusable functions
# ---------------------------------------------------------
def parse_intake_times(raw_text: str, total_minutes: int) -> list[int]:
    """Convert comma-separated intake times into a validated integer list."""
    if not raw_text.strip():
        raise ValueError("섭취 시각을 한 개 이상 입력해 주세요.")

    try:
        times = [int(item.strip()) for item in raw_text.split(",") if item.strip()]
    except ValueError as error:
        raise ValueError("섭취 시각은 0, 30, 60처럼 정수와 쉼표로 입력해 주세요.") from error

    if not times:
        raise ValueError("섭취 시각을 한 개 이상 입력해 주세요.")
    if len(times) > 8:
        raise ValueError("한 번에 입력할 수 있는 섭취 시각은 최대 8개입니다.")
    if len(times) != len(set(times)):
        raise ValueError("같은 섭취 시각이 중복되었습니다. 중복 값을 삭제해 주세요.")
    if min(times) < 0 or max(times) > total_minutes:
        raise ValueError(f"섭취 시각은 0분부터 {total_minutes}분 사이여야 합니다.")

    return sorted(times)


def simulate_ph_curve(
    intake_times: list[int],
    baseline_ph: float,
    critical_ph: float,
    drop_strength: float,
    recovery_half_life: float,
    total_minutes: int,
) -> pd.DataFrame:
    """Create a conceptual oral pH curve using exponential recovery."""
    if baseline_ph <= critical_ph:
        raise ValueError("평상시 pH는 임계 pH보다 크게 설정해 주세요.")
    if recovery_half_life <= 0:
        raise ValueError("회복 반감기는 0보다 커야 합니다.")

    current_ph = baseline_ph
    recovery_rate = 1 - math.exp(-math.log(2) / recovery_half_life)
    records = []

    for minute in range(total_minutes + 1):
        # Each intake event causes a conceptual immediate pH drop.
        if minute in intake_times:
            current_ph = max(3.8, current_ph - drop_strength)

        records.append(
            {
                "시간(분)": minute,
                "개념 pH": round(current_ph, 3),
                "임계 pH": critical_ph,
                "임계값 미만": current_ph < critical_ph,
            }
        )

        # Salivary buffering is represented as exponential recovery.
        current_ph += (baseline_ph - current_ph) * recovery_rate

    return pd.DataFrame(records)


def calculate_exposure_metrics(data: pd.DataFrame, critical_ph: float) -> dict:
    """Calculate educational exposure indicators from a simulated curve."""
    below = data["개념 pH"] < critical_ph
    total_below = int(below.sum())

    longest_run = 0
    current_run = 0
    for is_below in below:
        if is_below:
            current_run += 1
            longest_run = max(longest_run, current_run)
        else:
            current_run = 0

    if total_below == 0:
        exposure_label = "임계값 미만 구간 없음"
    elif longest_run <= 20:
        exposure_label = "짧은 임계값 미만 구간"
    else:
        exposure_label = "긴 임계값 미만 구간"

    return {
        "min_ph": float(data["개념 pH"].min()),
        "total_below": total_below,
        "longest_run": longest_run,
        "exposure_label": exposure_label,
    }


def format_intake_times(intake_times: list[int]) -> str:
    """Return intake times as readable Korean text."""
    return ", ".join(f"{minute}분" for minute in intake_times)


def show_metrics(metrics: dict) -> None:
    """Display the three main simulation metrics."""
    first, second, third = st.columns(3)
    first.metric("최저 개념 pH", f"{metrics['min_ph']:.2f}")
    second.metric("임계값 미만 누적 시간", f"{metrics['total_below']}분")
    third.metric("최장 연속 노출", f"{metrics['longest_run']}분")
    st.info(f"노출 구간 요약: **{metrics['exposure_label']}**")


def add_history_record(name: str, intake_times: list[int], metrics: dict) -> None:
    """Save a compact result in the current Streamlit session."""
    st.session_state.history.append(
        {
            "실행 시각": datetime.now().strftime("%H:%M:%S"),
            "시나리오": name,
            "섭취 시각": format_intake_times(intake_times),
            "최저 개념 pH": round(metrics["min_ph"], 2),
            "임계값 미만 시간(분)": metrics["total_below"],
            "최장 연속 노출(분)": metrics["longest_run"],
        }
    )


def draw_ph_chart(data: pd.DataFrame) -> None:
    """Draw pH and critical-pH lines with Streamlit's built-in chart."""
    st.line_chart(
        data,
        x="시간(분)",
        y=["개념 pH", "임계 pH"],
        color=["#15A7A7", "#F05D5E"],
        height=390,
    )


def apply_styles() -> None:
    """Apply a clean dental-clinic-inspired visual style."""
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #F7FCFC 0%, #EEF8FA 55%, #F8F5FF 100%);
        }
        .main .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }
        h1, h2, h3 { color: #163B47; letter-spacing: -0.02em; }
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid #D8EAED;
            border-radius: 18px;
            padding: 16px;
            box-shadow: 0 8px 22px rgba(31, 92, 104, 0.07);
        }
        .hero {
            padding: 24px 26px;
            border-radius: 24px;
            color: white;
            background: linear-gradient(120deg, #128C8C, #55BFC4);
            box-shadow: 0 12px 30px rgba(20, 130, 135, 0.18);
            margin-bottom: 22px;
        }
        .hero h1 { color: white; margin: 0 0 8px 0; }
        .hero p { margin: 0; opacity: 0.95; }
        .small-note { color: #55717A; font-size: 0.92rem; }
        div.stButton > button, div.stDownloadButton > button {
            border-radius: 12px;
            border: 1px solid #B9DDE0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# 3. Screen functions
# ---------------------------------------------------------
def render_simulator_screen() -> None:
    st.subheader("나만의 구강 pH 시나리오 만들기")
    st.write("섭취 시각과 회복 조건을 바꾸며 개념 pH 곡선의 변화를 관찰해 보세요.")

    with st.form("simulation_form"):
        left, right = st.columns(2)
        with left:
            scenario_name = st.text_input("시나리오 이름", value="나의 간식 섭취 패턴")
            preset_name = st.selectbox("산 생성 자극 수준", list(STIMULUS_PRESETS))
            intake_text = st.text_input(
                "섭취 시각(분)",
                value="0, 45, 90",
                help="0, 30, 60처럼 쉼표로 구분하세요. 최대 8회까지 입력할 수 있습니다.",
            )
            recovery_name = st.selectbox("회복 상황", list(RECOVERY_OPTIONS))

        with right:
            baseline_ph = st.slider("평상시 개념 pH", 6.2, 7.4, 6.8, 0.1)
            critical_ph = st.slider(
                "관찰용 임계 pH",
                5.0,
                5.8,
                5.5,
                0.1,
                help="실제 임계값은 개인과 환경에 따라 달라질 수 있습니다.",
            )
            total_minutes = st.slider("관찰 시간", 120, 360, 240, 30)

        submitted = st.form_submit_button("시뮬레이션 실행", use_container_width=True)

    if submitted:
        if not scenario_name.strip():
            st.error("시나리오 이름을 입력해 주세요.")
            return

        try:
            intake_times = parse_intake_times(intake_text, total_minutes)
            preset = STIMULUS_PRESETS[preset_name]
            adjusted_half_life = preset["half_life"] * RECOVERY_OPTIONS[recovery_name]
            data = simulate_ph_curve(
                intake_times=intake_times,
                baseline_ph=baseline_ph,
                critical_ph=critical_ph,
                drop_strength=preset["drop"],
                recovery_half_life=adjusted_half_life,
                total_minutes=total_minutes,
            )
            metrics = calculate_exposure_metrics(data, critical_ph)
        except ValueError as error:
            st.error(str(error))
            return

        st.session_state.latest_data = data
        st.session_state.latest_metrics = metrics
        st.session_state.latest_name = scenario_name.strip()
        st.session_state.latest_times = intake_times
        add_history_record(scenario_name.strip(), intake_times, metrics)

    if st.session_state.latest_data is not None:
        st.markdown(f"### {st.session_state.latest_name} 결과")
        show_metrics(st.session_state.latest_metrics)
        draw_ph_chart(st.session_state.latest_data)

        st.caption(
            "청록색은 단순화한 개념 pH, 빨간색은 사용자가 설정한 관찰용 임계값입니다. "
            "임계값 아래에 머무는 시간이 길수록 탈회가 일어날 수 있는 환경을 더 오래 모사합니다."
        )

        csv_data = st.session_state.latest_data.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "결과 CSV 다운로드",
            data=csv_data,
            file_name="oral_ph_simulation.csv",
            mime="text/csv",
        )

    with st.expander("현재 세션의 실행 기록 보기"):
        if st.session_state.history:
            st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
            if st.button("실행 기록 지우기"):
                st.session_state.history = []
                st.rerun()
        else:
            st.warning("아직 저장된 실행 기록이 없습니다. 먼저 시뮬레이션을 실행해 주세요.")


def render_comparison_screen() -> None:
    st.subheader("한 번 섭취와 반복 섭취 비교")
    st.write("같은 자극이라도 섭취 간격이 짧아질 때 회복 곡선이 어떻게 달라지는지 비교합니다.")

    left, right = st.columns(2)
    with left:
        preset_name = st.selectbox(
            "비교할 산 생성 자극",
            list(STIMULUS_PRESETS),
            index=1,
            key="compare_preset",
        )
        interval = st.slider("반복 섭취 간격", 15, 90, 40, 5)
    with right:
        repeat_count = st.slider("반복 섭취 횟수", 2, 6, 4)
        compare_minutes = st.slider("비교 관찰 시간", 120, 360, 240, 30, key="compare_minutes")

    if st.button("두 패턴 비교하기", use_container_width=True):
        repeated_times = [interval * index for index in range(repeat_count)]
        if repeated_times[-1] > compare_minutes:
            st.error("마지막 섭취 시각이 관찰 시간을 넘습니다. 횟수나 간격을 줄여 주세요.")
            return

        preset = STIMULUS_PRESETS[preset_name]
        single_data = simulate_ph_curve(
            [0], 6.8, 5.5, preset["drop"], preset["half_life"], compare_minutes
        )
        repeated_data = simulate_ph_curve(
            repeated_times,
            6.8,
            5.5,
            preset["drop"],
            preset["half_life"],
            compare_minutes,
        )

        comparison = pd.DataFrame(
            {
                "시간(분)": single_data["시간(분)"],
                "한 번 섭취": single_data["개념 pH"],
                "반복 섭취": repeated_data["개념 pH"],
                "임계 pH": single_data["임계 pH"],
            }
        )
        st.session_state.comparison_data = comparison
        st.session_state.single_metrics = calculate_exposure_metrics(single_data, 5.5)
        st.session_state.repeated_metrics = calculate_exposure_metrics(repeated_data, 5.5)

    if st.session_state.comparison_data is not None:
        st.line_chart(
            st.session_state.comparison_data,
            x="시간(분)",
            y=["한 번 섭취", "반복 섭취", "임계 pH"],
            color=["#68B8C4", "#7A65C7", "#F05D5E"],
            height=420,
        )

        single = st.session_state.single_metrics
        repeated = st.session_state.repeated_metrics
        st.markdown("### 비교 결과")
        comparison_table = pd.DataFrame(
            [
                ["한 번 섭취", single["min_ph"], single["total_below"], single["longest_run"]],
                ["반복 섭취", repeated["min_ph"], repeated["total_below"], repeated["longest_run"]],
            ],
            columns=["패턴", "최저 개념 pH", "임계값 미만 누적 시간", "최장 연속 노출"],
        )
        st.dataframe(comparison_table, use_container_width=True, hide_index=True)
        st.success(
            "이 개념 모형에서는 회복되기 전에 새로운 섭취가 반복되면 pH가 임계값 아래에 "
            "머무는 시간이 길어질 수 있음을 확인할 수 있습니다."
        )


def render_learning_screen() -> None:
    st.subheader("원리 학습과 확인 퀴즈")
    st.markdown(
        """
        **모형의 핵심 원리**

        - 구강 세균이 발효 가능한 탄수화물을 이용하면 산성 환경이 형성될 수 있습니다.
        - 침의 완충 작용은 낮아진 pH가 평상시 수준으로 돌아오는 데 도움을 줍니다.
        - 섭취가 반복되면 충분히 회복되기 전에 새로운 pH 하강이 겹칠 수 있습니다.
        - 치아 탈회는 pH 하나만으로 결정되지 않으며 침, 불소, 치면세균막, 섭취 습관 등 여러 요인의 영향을 받습니다.
        """
    )

    questions = [
        {
            "question": "이 앱의 pH 곡선은 무엇을 의미할까요?",
            "options": ["개인의 실제 충치 진단", "원리를 이해하기 위한 개념 모형", "치과 처방 결과"],
            "answer": "원리를 이해하기 위한 개념 모형",
        },
        {
            "question": "섭취 간격이 너무 짧을 때 나타날 수 있는 변화는 무엇일까요?",
            "options": ["회복 전 새로운 하강이 겹친다", "항상 pH가 7로 고정된다", "침의 기능이 완전히 사라진다"],
            "answer": "회복 전 새로운 하강이 겹친다",
        },
        {
            "question": "침의 완충 작용을 모형에서는 어떻게 표현했나요?",
            "options": ["pH의 점진적 회복", "pH의 영구적 하강", "섭취 횟수의 삭제"],
            "answer": "pH의 점진적 회복",
        },
        {
            "question": "탈회 가능성에 영향을 주는 요인으로 적절하지 않은 것은?",
            "options": ["침과 불소", "섭취 습관", "휴대전화 배경화면 색상"],
            "answer": "휴대전화 배경화면 색상",
        },
    ]

    with st.form("quiz_form"):
        user_answers = []
        for index, item in enumerate(questions, start=1):
            user_answers.append(
                st.radio(
                    f"{index}. {item['question']}",
                    item["options"],
                    index=None,
                    key=f"quiz_{index}",
                )
            )
        quiz_submitted = st.form_submit_button("정답 확인", use_container_width=True)

    if quiz_submitted:
        unanswered = sum(answer is None for answer in user_answers)
        if unanswered:
            st.error(f"아직 답하지 않은 문제가 {unanswered}개 있습니다.")
            return

        score = sum(
            answer == item["answer"] for answer, item in zip(user_answers, questions)
        )
        st.metric("퀴즈 점수", f"{score} / {len(questions)}")
        if score == len(questions):
            st.success("모든 원리를 정확하게 이해했습니다!")
        else:
            st.info("틀린 문항의 원리를 위 설명에서 다시 확인해 보세요.")

        for index, (answer, item) in enumerate(zip(user_answers, questions), start=1):
            if answer == item["answer"]:
                st.write(f"✅ {index}번 정답")
            else:
                st.write(f"❌ {index}번 정답: **{item['answer']}**")


# ---------------------------------------------------------
# 4. Main app
# ---------------------------------------------------------
apply_styles()

if "history" not in st.session_state:
    st.session_state.history = []
if "latest_data" not in st.session_state:
    st.session_state.latest_data = None
if "latest_metrics" not in st.session_state:
    st.session_state.latest_metrics = None
if "latest_name" not in st.session_state:
    st.session_state.latest_name = ""
if "latest_times" not in st.session_state:
    st.session_state.latest_times = []
if "comparison_data" not in st.session_state:
    st.session_state.comparison_data = None
if "single_metrics" not in st.session_state:
    st.session_state.single_metrics = None
if "repeated_metrics" not in st.session_state:
    st.session_state.repeated_metrics = None

st.markdown(
    """
    <div class="hero">
        <h1>🦷 Oral pH Lab</h1>
        <p>구강 산도 변화와 치아 탈회 환경을 탐구하는 교육용 시뮬레이터</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Oral pH Lab")
    page = st.radio(
        "화면 선택",
        ["pH 시뮬레이션", "패턴 비교", "원리 학습·퀴즈"],
    )
    st.divider()
    st.markdown("**이 앱의 목적**")
    st.caption(
        "음식 섭취 뒤 구강 pH가 낮아졌다가 회복되는 과정을 단순화하여 탐구합니다."
    )
    st.warning(
        "이 앱은 교육용 개념 모형이며 실제 구강 pH 측정, 충치 위험 진단 또는 치료 지시를 제공하지 않습니다."
    )

if page == "pH 시뮬레이션":
    render_simulator_screen()
elif page == "패턴 비교":
    render_comparison_screen()
else:
    render_learning_screen()

st.divider()
st.markdown(
    "<p class='small-note'>모형의 수치는 원리 비교를 위한 상대적 설정값입니다. "
    "실제 구강 환경은 개인별 침 분비, 치면세균막, 불소 노출, 식습관 등에 따라 달라질 수 있습니다.</p>",
    unsafe_allow_html=True,
)


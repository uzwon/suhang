from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# Streamlit 기본 설정
# ============================================================

st.set_page_config(
    page_title="MIDNIGHT HOSPITAL",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 MIDNIGHT HOSPITAL")

st.caption(
    "픽셀 병원 어드벤처 · 방향키/WASD 이동 · Shift 달리기 · Space 상호작용 · R 재시작"
)


# ============================================================
# 게임 HTML / CSS / JavaScript 불러오기
# ============================================================

WEB_DIR = Path(__file__).parent / "web"

html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
css = (WEB_DIR / "style.css").read_text(encoding="utf-8")
js = (WEB_DIR / "script.js").read_text(encoding="utf-8")

# components.html 은 iframe(srcdoc)으로 렌더링되어 상대 경로 파일을 못 읽으므로
# style.css / script.js 내용을 HTML 안에 직접 끼워 넣는다
game_html = (
    html
    .replace('<link rel="stylesheet" href="style.css">', f"<style>\n{css}</style>")
    .replace('<script src="script.js"></script>', f"<script>\n{js}</script>")
)


# ============================================================
# Streamlit 페이지에 게임 삽입
# ============================================================

components.html(
    game_html,
    height=1190,
    scrolling=False
)

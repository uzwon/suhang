import base64
import json
import mimetypes
import re
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
# 게임 HTML / CSS / JavaScript / 에셋 불러오기
# ============================================================

WEB_DIR = Path(__file__).parent / "web"

mimetypes.add_type("font/woff2", ".woff2")


def data_uri(relative_path):
    """web 폴더 안의 파일을 data URI 문자열로 바꾼다."""
    path = WEB_DIR / relative_path
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def inline_css(match):
    css = (WEB_DIR / match.group(1)).read_text(encoding="utf-8")
    # 글꼴처럼 CSS 가 url("assets/...") 로 부르는 파일도 data URI 로 넣는다
    css = re.sub(
        r'url\("(assets/[^"]+)"\)',
        lambda m: f'url("{data_uri(m.group(1))}")',
        css,
    )
    return f"<style>\n{css}</style>"


def inline_js(match):
    js = (WEB_DIR / match.group(1)).read_text(encoding="utf-8")
    return f"<script>\n{js}</script>"


# components.html 은 iframe(srcdoc)으로 렌더링되어 상대 경로 파일을 못 읽으므로
# CSS / JS 내용은 HTML 안에 직접 끼워 넣고,
# 스프라이트 PNG 는 data URI 로 바꿔 window.ASSET_URLS 로 넘겨준다 (web/sprites.js 가 사용)
asset_urls = {
    path.relative_to(WEB_DIR).as_posix(): data_uri(path.relative_to(WEB_DIR))
    for path in sorted((WEB_DIR / "assets" / "sprites").glob("*.png"))
}

html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
html = re.sub(r'<link rel="stylesheet" href="([^"]+)">', inline_css, html)
html = re.sub(r'<script src="([^"]+)"></script>', inline_js, html)
game_html = html.replace(
    "<head>",
    f"<head>\n<script>window.ASSET_URLS = {json.dumps(asset_urls)};</script>",
    1,
)


# ============================================================
# Streamlit 페이지에 게임 삽입
# ============================================================

components.html(
    game_html,
    height=1060,
    scrolling=False
)

"""
MIDNIGHT HOSPITAL 도트 에셋 빌드 스크립트

게임에 쓰이는 모든 도트(타일, 캐릭터, 오브젝트, UI)를 이 파일에서 문자 격자로 찍고
web/assets/sprites/*.png 스프라이트 시트와 web/assets/atlas.js 를 만든다.

    python tools/build_sprites.py                    # PNG + atlas.js 생성
    python tools/build_sprites.py --preview out.png  # 확대 미리보기도 함께 저장

격자 규칙
    - 한 글자 = 한 픽셀, '.' 은 투명
    - 글자 → 색은 PALETTE (스프라이트마다 일부 글자를 바꿔 쓸 수 있다)
    - 게임에서는 도트 1픽셀을 화면 2픽셀로 그린다 (타일 16px → 32px)

PNG 를 도트 툴(Aseprite, Piskel 등)로 직접 고쳐도 된다. 다만 이 스크립트를 다시
실행하면 PNG 가 새로 만들어지므로, 그때는 이 파일의 격자도 같이 고쳐야 한다.
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent.parent
SPRITE_DIR = ROOT / "web" / "assets" / "sprites"
ATLAS_PATH = ROOT / "web" / "assets" / "atlas.js"

SHEET_WIDTH = 256


# ============================================================
# 팔레트 (Endesga 32 기반)
# ============================================================

PALETTE = {
    ".": None,
    # 차가운 무채색
    "0": "#181425",
    "1": "#262b44",
    "2": "#3a4466",
    "3": "#5a6988",
    "4": "#8b9bb4",
    "5": "#c0cbdc",
    "6": "#ffffff",
    # 갈색 / 피부
    "d": "#3e2731",
    "W": "#733e39",
    "w": "#b86f50",
    "K": "#e4a672",
    "S": "#c28569",
    "s": "#e8b796",
    "k": "#ead4aa",
    # 빨강
    "r": "#a22633",
    "R": "#e43b44",
    "P": "#ff0044",
    "p": "#f6757a",
    # 주황 / 노랑
    "o": "#be4a2f",
    "O": "#d77643",
    "y": "#f77622",
    "Y": "#feae34",
    "L": "#fee761",
    # 초록
    "g": "#63c74d",
    "G": "#3e8948",
    "h": "#265c42",
    "H": "#193c3e",
    # 파랑
    "b": "#124e89",
    "B": "#0099db",
    "c": "#2ce8f5",
    # 보라
    "v": "#68386c",
    "V": "#b55088",
    # 반투명 (그림자 / 얼룩)
    ",": "#00000038",
    ";": "#ffffff30",
}

# 스테이지별 바닥 / 벽 색 (같은 타일 도안을 색만 바꿔 3세트로 만든다)
STAGE_TILE_COLORS = {
    # STAGE 1 · 정전된 본관 (푸른 회색)
    "s1": {
        "A": "#aab6cb", "a": "#95a2ba", "b": "#8e9bb4", "q": "#8692ac", "g": "#717e9a",
        "T": "#2f3756", "t": "#29304c", "U": "#6a7aa0",
        "u": "#7f8dab", "n": "#414c69", "m": "#64739a", "M": "#59678c",
        "z": "#3fb8c4", "Z": "#2a8592", "e": "#343d5a", "E": "#22273d",
    },
    # STAGE 2 · 격리 연구동 (초록 회색)
    "s2": {
        "A": "#a4bdb0", "a": "#8fa89b", "b": "#88a194", "q": "#80998c", "g": "#6a8377",
        "T": "#253a39", "t": "#203332", "U": "#5b8378",
        "u": "#78a096", "n": "#3a544f", "m": "#5c8177", "M": "#52746b",
        "z": "#e0b44a", "Z": "#a8822f", "e": "#2c4541", "E": "#1b2a2a",
    },
    # STAGE 3 · 옥상 연결 병동 (보라 회색)
    "s3": {
        "A": "#b8b1cf", "a": "#a39bbd", "b": "#9c94b7", "q": "#938bae", "g": "#7c7598",
        "T": "#352e4f", "t": "#2e2845", "U": "#7368a0",
        "u": "#8d83b0", "n": "#4b446e", "m": "#73689a", "M": "#675c8c",
        "z": "#e07a9a", "Z": "#a85572", "e": "#393155", "E": "#28223b",
    },
}

# 환자복 색 (환자 1 / 2 / 3)
GOWN_COLORS = [
    {"7": "#b4dcf5", "8": "#77b8e8", "9": "#4a82b8"},
    {"7": "#bfe6b5", "8": "#83c985", "9": "#55925a"},
    {"7": "#fdeb94", "8": "#f2c14e", "9": "#b8862b"},
]


# ============================================================
# 격자 도우미
# ============================================================

def grid(text):
    """여러 줄 문자열 → 줄 목록 (앞뒤 공백 제거)"""
    return [line.strip() for line in text.strip().splitlines() if line.strip()]


def mirror(half):
    """왼쪽 절반만 찍은 좌우 대칭 도트를 완성한다."""
    return [row + row[::-1] for row in half]


def flip(rows):
    return [row[::-1] for row in rows]


def paint(rows, x, y, patch):
    """rows 의 (x, y) 위치에 patch 를 덮어 쓴다. patch 의 공백은 건너뛴다."""
    rows = [list(row) for row in rows]
    for dy, line in enumerate(patch):
        for dx, ch in enumerate(line):
            if ch != " ":
                rows[y + dy][x + dx] = ch
    return ["".join(row) for row in rows]


def recolor(rows, mapping):
    return ["".join(mapping.get(ch, ch) for ch in row) for row in rows]


def blank(w, h):
    return ["." * w for _ in range(h)]


# ============================================================
# 스프라이트 시트
# ============================================================

class Sheet:
    def __init__(self, name):
        self.name = name
        self.sprites = []

    def add(self, name, rows, pal=None, anchor=None):
        width = len(rows[0])
        for i, row in enumerate(rows):
            if len(row) != width:
                raise ValueError(f"{name}: {i}번째 줄 길이 {len(row)} (기대값 {width})\n  {row}")
        colors = dict(PALETTE)
        if pal:
            colors.update(pal)
        for row in rows:
            for ch in row:
                if ch not in colors:
                    raise ValueError(f"{name}: 팔레트에 없는 글자 '{ch}'")
        height = len(rows)
        ax, ay = anchor if anchor else (width // 2, height - 1)
        self.sprites.append({"name": name, "rows": rows, "colors": colors, "w": width, "h": height, "ax": ax, "ay": ay})

    def build(self):
        # 선반(shelf) 방식으로 왼쪽 위부터 차례대로 배치
        x = y = shelf = 0
        for sprite in self.sprites:
            if x + sprite["w"] > SHEET_WIDTH:
                x, y, shelf = 0, y + shelf, 0
            sprite["x"], sprite["y"] = x, y
            x += sprite["w"]
            shelf = max(shelf, sprite["h"])
        image = Image.new("RGBA", (SHEET_WIDTH, y + shelf), (0, 0, 0, 0))
        pixels = image.load()
        for sprite in self.sprites:
            for py, row in enumerate(sprite["rows"]):
                for px, ch in enumerate(row):
                    color = sprite["colors"][ch]
                    if color:
                        pixels[sprite["x"] + px, sprite["y"] + py] = hex_to_rgba(color)
        return image


def hex_to_rgba(value):
    value = value.lstrip("#")
    r, g, b = int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
    a = int(value[6:8], 16) if len(value) == 8 else 255
    return (r, g, b, a)


TILES = Sheet("tiles")
CHARACTERS = Sheet("characters")
OBJECTS = Sheet("objects")
UI = Sheet("ui")

ANIMS = {}


# ============================================================
# 타일 (16x16)
# ============================================================

FLOOR = grid("""
AAAAAAAAAAAAAAAg
Aaaaaaaaaaaaaaag
Aaaaaaaaqaaaaaag
Aaaaaaaaaaaaaaag
Aaaqaaaaaaaaaaag
Aaaaaaaaaaaaaaag
Aaaaaaaaaaaqaaag
Aaaaaaaaaaaaaaag
Aaaaaaaaaaaaaaag
Aaaaaqaaaaaaaaag
Aaaaaaaaaaaaaaag
Aaaaaaaaaaaaqaag
Aaaaaaaaaaaaaaag
Aaqaaaaaaaaaaaag
Aaaaaaaaaaaaaaag
gggggggggggggggg
""")

FLOOR_CRACK = grid("""
................
................
................
.........,......
........,.......
.......,,.......
......,.........
.....,..........
.....,,.........
......,.........
................
................
................
................
................
................
""")

FLOOR_STAIN = grid("""
................
................
................
................
................
.......,,,......
.....,,,,,,.....
.....,,,,,,,....
......,,,,,.....
........,.......
................
................
................
................
................
................
""")

# 벽 윗면 (아래에도 벽이 있을 때)
WALL_CAP = grid("""
TTTTTTTTTTTTTTTT
TTTTTTTTTTTTTTTT
TTtTTTTTTTTTtTTT
TTTTTTTTTTTTTTTT
TTTTTTTtTTTTTTTT
TTTTTTTTTTTTTTTT
TTTTTTTTTTTTTTTT
TtTTTTTTTTTtTTTT
TTTTTTTTTTTTTTTT
TTTTTTTTTTTTTTTT
TTTTTtTTTTTTTTTT
TTTTTTTTTTTTTTtT
TTTTTTTTTTTTTTTT
TTTTTTTTtTTTTTTT
TTTTTTTTTTTTTTTT
TTTTTTTTTTTTTTTT
""")

# 벽 앞면 (바로 아래가 바닥일 때 보이는 벽)
WALL_FRONT = grid("""
TTTTTTTTTTTTTTTT
TTTTTTTTTTTTTTTT
uuuuuuuuuuuuuuuu
nnnnnnnnnnnnnnnn
mmmmmmmmmmmmmmmm
mmmmmmmmmmmmmmmm
mmmmmmmmmmmmmmmm
mmmmmmmmmmmmmmmm
mmmmmmmmmmmmmmmm
zzzzzzzzzzzzzzzz
ZZZZZZZZZZZZZZZZ
MMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMM
eeeeeeeeeeeeeeee
EEEEEEEEEEEEEEEE
""")


def edge_piece(cells):
    rows = [list("." * 16) for _ in range(16)]
    for x, y, ch in cells:
        rows[y][x] = ch
    return ["".join(row) for row in rows]


EDGE_PIECES = {
    # 벽 윗면 테두리 (그 방향에 벽이 없을 때)
    "rim_n": edge_piece([(x, 0, "U") for x in range(16)]),
    "rim_e": edge_piece([(15, y, "U") for y in range(16)]),
    "rim_w": edge_piece([(0, y, "U") for y in range(16)]),
    # 옆 칸이 벽 앞면일 때: 앞면이 시작되는 높이부터 옆선
    "rim_e_low": edge_piece([(15, y, "U") for y in range(2, 16)]),
    "rim_w_low": edge_piece([(0, y, "U") for y in range(2, 16)]),
    # 벽 앞면 옆선
    "front_e": edge_piece([(15, y, "U") for y in range(2)] + [(15, y, "E") for y in range(2, 16)]),
    "front_w": edge_piece([(0, y, "U") for y in range(2)] + [(0, y, "E") for y in range(2, 16)]),
    # 안쪽 모서리 (대각선 방향만 바닥일 때)
    "corner_ne": edge_piece([(15, 0, "U")]),
    "corner_nw": edge_piece([(0, 0, "U")]),
}


def build_tiles():
    for stage, colors in STAGE_TILE_COLORS.items():
        TILES.add(f"{stage}_floor_a", FLOOR, colors, (0, 0))
        TILES.add(f"{stage}_floor_b", recolor(FLOOR, {"a": "b"}), colors, (0, 0))
        TILES.add(f"{stage}_wall_cap", WALL_CAP, colors, (0, 0))
        TILES.add(f"{stage}_wall_front", WALL_FRONT, colors, (0, 0))
        for name, rows in EDGE_PIECES.items():
            TILES.add(f"{stage}_{name}", rows, colors, (0, 0))
    TILES.add("floor_crack", FLOOR_CRACK, anchor=(0, 0))
    TILES.add("floor_stain", FLOOR_STAIN, anchor=(0, 0))


# ============================================================
# 캐릭터 (16x20, 기준점은 발밑 가운데)
# ============================================================

DOCTOR_DOWN = mirror(grid("""
....0000
...0WwwW
..0WwWWW
..0WWWWW
..0WWWWW
..0Wssss
..0Ws0ss
..0Ws0ss
..0Wpsss
...0Ssss
...0566S
..0566BB
..0566BB
..0566BB
..0s56bb
...056bb
...05550
....0220
....0110
....0000
"""))
# 가슴의 출입증, 목에 건 청진기
DOCTOR_DOWN = paint(DOCTOR_DOWN, 10, 12, ["c"])
DOCTOR_DOWN = paint(DOCTOR_DOWN, 5, 11, ["3", "3", " 3"])

DOCTOR_UP = mirror(grid("""
....0000
...0WwwW
..0WwWWW
..0WWWWW
..0WWWWW
..0WWWWW
..0WWWWW
..0WWWWW
..0dWWWW
...0dddd
...05666
..056666
..056666
..056666
..0s5666
...05666
...05550
....0220
....0110
....0000
"""))
DOCTOR_UP = paint(DOCTOR_UP, 7, 14, ["55", "55"])

DOCTOR_LEFT = grid("""
.....000000.....
....0WWwwWWW0...
...0WWwWWWWWW0..
..0WWWWWWWWWWW0.
..0WWWWWWWWWWW0.
..0ssssWWWWWWW0.
..0s0ssSWWWWWW0.
.0ss0ssSWWWWWd0.
..0pssssWWWWd0..
...0SsssS0dd0...
....0SS66650....
...0B566666650..
...0B566556650..
...0B566556650..
...0b5666ss650..
...0b566666650..
....05555550....
.....022220.....
....0111110.....
....0000000.....
""")
DOCTOR_LEFT = paint(DOCTOR_LEFT, 6, 11, ["c"])

PATIENT_DOWN = mirror(grid("""
....0000
...0dddd
..0ddddd
..066666
..0ddddd
..0dssss
..0ds0ss
..0ds0ss
..0dpsss
...0Ssss
...0877S
..087777
..087877
..087777
..0s8777
...08777
...09990
....0ss0
....0660
....0000
"""))

PATIENT_UP = mirror(grid("""
....0000
...0dddd
..0ddddd
..066666
..0ddddd
..0ddddd
..0ddddd
..0ddddd
..0ddddd
...0dddd
...08777
..087777
..087877
..087777
..0s8777
...08777
...09990
....0ss0
....0660
....0000
"""))

PATIENT_LEFT = grid("""
.....000000.....
....0ddddddd0...
...0ddddddddd0..
..0666666666660.
..0ddddddddddd0.
..0ssssddddddd0.
..0s0ssSdddddd0.
.0ss0ssSdddddd0.
..0pssssdddd0...
...0SsssS0dd0...
....0SS77780....
...0877777780...
...0877799780...
...0877799780...
...08777ss780...
...0877777780...
....09999990....
.....0ssss0.....
....0666660.....
....0000000.....
""")

# 걷기 동작 (아래 3줄만 바꾼다)
LEGS_FRONT = {
    "pants": {
        "a": ["....02200110....", "....01100000....", "....0000........"],
        "b": ["....01100220....", "....00000110....", "........0000...."],
    },
    "bare": {
        "a": ["....0ss00660....", "....06600000....", "....0000........"],
        "b": ["....06600ss0....", "....00000660....", "........0000...."],
    },
}
LEGS_SIDE = {
    "pants": ["....02200220....", "...0110..0110...", "...0000..0000..."],
    "bare": ["....0ss00ss0....", "...0660..0660...", "...0000..0000..."],
}


def with_legs(rows, legs):
    return rows[:-3] + legs


def add_walker(prefix, down, up, left, legs, pal=None):
    """한 캐릭터의 4방향 x 3프레임 스프라이트와 걷기 애니메이션을 등록한다."""
    frames = {
        "down": [down, with_legs(down, LEGS_FRONT[legs]["a"]), with_legs(down, LEGS_FRONT[legs]["b"])],
        "up": [up, with_legs(up, LEGS_FRONT[legs]["b"]), with_legs(up, LEGS_FRONT[legs]["a"])],
        "left": [left, with_legs(left, LEGS_SIDE[legs]), left],
    }
    frames["right"] = [flip(rows) for rows in frames["left"]]
    for direction, rows_list in frames.items():
        for index, rows in enumerate(rows_list):
            CHARACTERS.add(f"{prefix}_{direction}_{index}", rows, pal, (8, 19))
        ANIMS[f"{prefix}_walk_{direction}"] = [
            f"{prefix}_{direction}_1", f"{prefix}_{direction}_0",
            f"{prefix}_{direction}_2", f"{prefix}_{direction}_0",
        ]


# ------------------------------------------------------------
# 그림자 (몸통은 흰색으로 찍고 게임에서 색을 입힌다)
# ------------------------------------------------------------

GHOST_BODY = mirror(grid("""
........
.....000
...00666
..066666
.0666666
.0666666
.0666666
06666666
06666666
06666666
06666666
06666666
06666666
06666666
"""))
GHOST_TAILS = [
    ["0666006666006660", ".00....00....00."],
    ["0066666006666600", "...000....000..."],
]


def shade_ghost(rows):
    """오른쪽과 아래쪽을 한 단계 어둡게 칠해 입체감을 준다."""
    rows = [list(row) for row in rows]
    for y, row in enumerate(rows):
        filled = [x for x, ch in enumerate(row) if ch == "6"]
        if filled and y >= 3:
            for x in filled[-2:]:
                row[x] = "5"
        if y >= 12:
            for x in filled:
                if row[x] == "6":
                    row[x] = "5"
    rows[4][4] = rows[4][5] = ";"
    return ["".join(row) for row in rows]


def ghost_eyes(direction, angry):
    rows = [list("." * 16) for _ in range(16)]
    eye = [".66.", "6666", "6666", ".66."]
    px, py = {"down": (1, 2), "up": (1, 0), "left": (0, 1), "right": (2, 1)}[direction]
    pupil = "P" if angry else "1"
    for ex in (3, 9):
        for y, line in enumerate(eye):
            for x, ch in enumerate(line):
                if ch != ".":
                    rows[5 + y][ex + x] = ch
        for y in range(2):
            for x in range(2):
                rows[5 + py + y][ex + px + x] = pupil
    if angry:
        # 화난 눈썹
        for x, y in [(3, 4), (4, 4), (5, 5), (6, 5), (12, 4), (11, 4), (10, 5), (9, 5)]:
            rows[y][x] = "0"
    return ["".join(row) for row in rows]


SHADOW_S = grid("""
...,,,,,,...
.,,,,,,,,,,.
.,,,,,,,,,,.
...,,,,,,...
""")


def build_characters():
    add_walker("doctor", DOCTOR_DOWN, DOCTOR_UP, DOCTOR_LEFT, "pants")
    for index, gown in enumerate(GOWN_COLORS):
        add_walker(f"patient{index + 1}", PATIENT_DOWN, PATIENT_UP, PATIENT_LEFT, "bare", gown)

    for index, tail in enumerate(GHOST_TAILS):
        CHARACTERS.add(f"ghost_{index}", shade_ghost(GHOST_BODY + tail), anchor=(8, 8))
    ANIMS["ghost_float"] = ["ghost_0", "ghost_1"]
    for direction in ("down", "up", "left", "right"):
        CHARACTERS.add(f"ghost_eyes_{direction}", ghost_eyes(direction, False), anchor=(8, 8))
        CHARACTERS.add(f"ghost_eyes_{direction}_angry", ghost_eyes(direction, True), anchor=(8, 8))

    CHARACTERS.add("shadow", SHADOW_S, anchor=(6, 2))


# ============================================================
# 오브젝트 (기준점은 타일 아래쪽 가운데)
# ============================================================

LOCKER = grid("""
..000000000000..
..055555555550..
..054444444430..
..054111111430..
..054444444430..
..054111111430..
..054444444430..
..054111111430..
..054444444430..
..054444444430..
..054444444430..
..054444446430..
..054444442430..
..054444444430..
..054444444430..
..054455554430..
..054433334430..
..054444444430..
..054444444430..
..054444444430..
..053333333330..
..022222222220..
..000000000000..
...00......00...
""")
LOCKER_HIDDEN = paint(LOCKER, 5, 5, ["1L11L1"])


def framed(inner, edge="0", top=None, bottom=None):
    """폭 10짜리 안쪽 줄들을 '..0' + 안쪽 + '0..' 로 감싼다."""
    rows = [f"..{edge}{line}{edge}.." for line in inner]
    if top:
        rows = top + rows
    if bottom:
        rows = rows + bottom
    return rows


VENDING = framed(
    [
        "pRRRRRRRRr",
        "R66666666r",
        "Rr6RR66R6r",
        "rrrrrrrrrr",
        "R000000RRr",
        "R0kkkk0R6r",
        "R0cBLg0R4r",
        "R0BbYG0R6r",
        "R044440R4r",
        "R0gRcB0R1r",
        "R0GrBb0R1r",
        "R044440RRr",
        "R0LcgR0RRr",
        "R0YBGr0RRr",
        "R0kkkk0RRr",
        "R000000RRr",
        "RRRRRRRRRr",
        "Rr00000rRr",
        "Rr01110rRr",
        "RrrrrrrrRr",
        "rrrrrrrrrr",
        "1111111111",
    ],
    top=["..000000000000.."],
    bottom=["..000000000000..", "................"],
)

DESK = grid("""
................
................
..0000000.......
..0cBBBB0..00...
..0BBBBb0.0kk0..
..0000000.0kk0..
.....0....0000..
.00000000000000.
.0KKKKKKKKKKKK0.
.0wwwwwwwwwwww0.
.0WWWWWWWWWWWW0.
.0wwwwWwwwwWww0.
.0wwwwWwwwwWww0.
.0wwwwWwwwwWww0.
.0WWWWWWWWWWWW0.
.00000000000000.
""")

NURSE_STATION = grid("""
................
..........0000..
..........0cB0..
..........0BB0..
...........00...
.00000000000000.
.06666666666660.
.05555555555550.
.0cccccccccccc0.
.066666gg666660.
.06666gggg66660.
.06666gggg66660.
.066666gg666660.
.05555555555550.
.04444444444440.
.00000000000000.
""")

BED = grid("""
................
.00000000000000.
.05555555555550.
.04444444444440.
.06655555555660.
.06566666666560.
.06555555555560.
.06666666666660.
.0cccccccccccc0.
.0BBBBBBBBBBBB0.
.0BBBBBBBBBBBb0.
.0BBBBBBBBBBbb0.
.0bbbbbbbbbbbb0.
.04444444444440.
.00000000000000.
..0..........0..
""")

BED_HEAD = BED[:9] + [
    ".0BBBBBBBBBBBB0.",
    ".0BBBBBBBBBBBb0.",
    ".0BBBBBBBBBBBb0.",
    ".0BBBBBBBBBBBb0.",
    ".0BBBBBBBBBBBb0.",
    ".0BBBBBBBBBBBb0.",
    ".0BBBBBBBBBBBb0.",
]
BED_FOOT = [
    ".0BBBBBBBBBBBb0.",
    ".0BBBBBBBBBBBb0.",
    ".0BBBBBBBBBBBb0.",
    ".0BBBBBBBBBBBb0.",
    ".0BBBBBBBBBBBb0.",
    ".0BBBBBBBBBBbb0.",
    ".0BBBBBBBBBBbb0.",
    ".0BBBBBBBBBBbb0.",
    ".0bbbbbbbbbbbb0.",
    ".00000000000000.",
    ".05555555555550.",
    ".04444444444440.",
    ".00000000000000.",
    "..0..........0..",
    "................",
    "................",
]
BED_PAL = {"B": "#8fc6e0", "b": "#5f97b8", "c": "#d4ecf7"}

WHEELCHAIR = grid("""
................
...00...........
...040..........
...040..........
...0b0..........
...0b0..........
...0b00000000...
...0bbbbbbbbb0..
..0000000000400.
..04444440..040.
.0440004400.040.
.0401110400.040.
.0401610400.040.
.0401110400.0440
.0440004400.0000
..04444440......
""")

PLANT = grid("""
................
.......00.......
......0gg0..00..
..00..0gG0.0gg0.
.0gg0.0gG00gG0..
.0gGG00gG0gG0...
..0gGGgGGGG0....
...0gGGGGhG00...
..0gggGGhhGgg0..
...00GGhhGG00...
.....0hhhh0.....
....0OOOOOO0....
....0yOOOOo0....
.....0OOOo0.....
.....0OOoo0.....
......0000......
""")

CCTV_OFF = grid("""
................
.000000..000000.
.0bbBb0..0bBbb0.
.0bBbb0..0bbBb0.
.0bbbb0..0bbbb0.
.000000..000000.
...00......00...
.00000000000000.
.04444444444440.
.03R3g3333L3330.
.02222222222220.
.02111111111120.
.02122222222120.
.02111111111120.
.02222222222220.
.00000000000000.
""")
CCTV_ON = [
    paint(CCTV_OFF, 2, 2, ["c66c", "cc1c", "c11c"]),
    paint(CCTV_OFF, 2, 2, ["cccc", "6666", "c1cc"]),
]
for i in range(2):
    CCTV_ON[i] = paint(CCTV_ON[i], 10, 2, ["c1cc", "c11c", "cccc"] if i == 0 else ["cc1c", "cccc", "6666"])

GENERATOR_BASE = framed(
    [
        "5555555555",
        "4444444443",
        "4101010103",
        "4444444443",
        "4101010103",
        "4444444443",
        "4222222223",
        "42RR2kkk23",
        "42RR2k0k23",
        "4222222223",
        "4444444443",
        "40Y0Y0Y0Y3",
        "4Y0Y0Y0Y03",
        "3333333333",
    ],
    top=["................", "..000000000000.."],
    bottom=["..000000000000..", "...00......00...", "................"],
)


def generator_frame(lamp, needle):
    rows = paint(GENERATOR_BASE, 5, 9, [lamp, lamp])
    return paint(rows, 8, 9, [needle])


GENERATOR_OFF = [generator_frame("RR", "k0k"), generator_frame("rr", "k0k")]
GENERATOR_ON = [generator_frame("gg", "kk0"), generator_frame("gG", "0kk")]


def door(frame, sign, panel, sill="3"):
    """16x24 문. sign 은 위쪽 표시판(10칸), panel 은 문짝 16줄(10칸)."""
    rows = [
        ".00000000000000.",
        f".0{frame * 12}0.",
        f".0{frame}{sign}{frame}0.",
        f".0{frame * 12}0.",
        f".0{frame}0000000000{frame}0.",
    ]
    rows += [f".0{frame}{line}{frame}0." for line in panel]
    rows += [
        f".0{sill * 12}0.",
        ".00000000000000.",
        "................",
    ]
    return rows


ELEVATOR_CLOSED = [
    "4655335564",
    "4565335654",
    "4555335554",
    "4555335554",
    "4555335554",
    "4555335554",
    "4555335554",
    "4555335554",
    "4555335554",
    "4555335554",
    "4555335554",
    "4555335554",
    "4555335554",
    "4555335554",
    "4444334444",
    "4444334444",
]
ELEVATOR_OPEN = ["43kkkkkk34"] * 12 + ["43KKKKKK34"] * 4

DECON_CLOSED = [
    "4555555554",
    "455YYYY554",
    "455Y00Y554",
    "455YYYY554",
    "4555555554",
    "4444444444",
    "4555555554",
    "4555555564",
    "4555555524",
    "4555555554",
    "4444444444",
    "4555555554",
    "4Y0Y0Y0Y04",
    "40Y0Y0Y0Y4",
    "4555555554",
    "4444444444",
]
DECON_OPEN = ["40cccccc04"] * 4 + ["40c6cc6c04"] + ["40cccccc04"] * 7 + ["40BBBBBB04"] * 4

ROOF_CLOSED = [
    "3444444443",
    "3455555543",
    "3451111543",
    "3451bb1543",
    "3451111543",
    "3455555543",
    "3444444443",
    "3444444463",
    "3555555523",
    "3444444443",
    "3444444443",
    "3455555543",
    "3454444543",
    "3455555543",
    "3444444443",
    "3333333333",
]
ROOF_OPEN = ["31bbbbbb13"] * 2 + ["31b6bbbb13"] + ["31bbbbbb13"] * 5 + ["31kkkkkk13"] * 8

SECURITY_CLOSED = [
    "bBcBBbBBcB",
    "bcBBBbBcBB",
    "bBBBBbBBBB",
    "bBBBBbBBBB",
    "bBBBBbBBBB",
    "bBBBcbBBBc",
    "bBBcBbBBcB",
    "bBcBBbBcBB",
    "bcBBBbcBBB",
    "bBBBBbBBBB",
    "bBBBBbBBBB",
    "bBBBBbBBBB",
    "bBBBBbBBBB",
    "bBBBBbBBBB",
    "2222222222",
    "2222222222",
]
SECURITY_OPEN = ["bB111111Bb"] * 14 + ["2211111122"] * 2

SHUTTER_CLOSED = [
    "4444444444",
    "3333333333",
    "4444444444",
    "3333333333",
    "4444444444",
    "3333LL3333",
    "444LL44444",
    "33LLLL3333",
    "4444LL4444",
    "3333L33333",
    "4444444444",
    "3333333333",
    "4444444444",
    "3333333333",
    "4444444444",
    "3333333333",
]
SHUTTER_OPEN = ["4444444444", "3333333333", "4444444444", "0000000000"] + ["1111111111"] * 12


def card_reader(rows, led):
    return paint(rows, 13, 9, ["0", led, "k", "0"])


TERMINAL_GLYPHS = {
    "A": [".X.", "X.X", "XXX", "X.X", "X.X"],
    "B": ["XX.", "X.X", "XX.", "X.X", "XX."],
    "C": [".XX", "X..", "X..", "X..", ".XX"],
}


def terminal(letter, active):
    background, glyph = ("h", "g") if active else ("b", "c")
    screen = [background * 8 for _ in range(7)]
    screen = paint(screen, 2, 1, [line.replace("X", glyph).replace(".", " ") for line in TERMINAL_GLYPHS[letter]])
    screen = paint(screen, 7, 6, ["L" if active else "R"])
    rows = [
        "................",
        "..000000000000..",
        "..022222222220..",
    ]
    rows += [f"..02{line}20.." for line in screen]
    rows += [
        "..022222222220..",
        "..000000000000..",
        "......0220......",
        "....00000000....",
        "...0555555550...",
        "...0545454540...",
        "...0444444440...",
        "...0000000000...",
    ]
    return rows


KEYCARD = grid("""
................
................
................
................
................
...0000000000...
...0BBBBBBBB0...
...0B66BBccB0...
...0B66BLLLB0...
...0BBBBBBBB0...
...0bbbbbbbb0...
...0000000000...
................
................
................
................
""")

FUSE = grid("""
................
................
......0000......
.....055550.....
.....044440.....
.....0LYYO0.....
.....0LYYO0.....
.....0L66O0.....
.....0LrrO0.....
.....0LYYO0.....
.....0LYYO0.....
.....055550.....
.....044440.....
......0000......
................
................
""")

BATTERY = grid("""
................
......0000......
......0540......
....00000000....
....0ggggGG0....
....0gggLGG0....
....0ggLLGG0....
....0gLLLLG0....
....0ggLLgG0....
....0ggLggG0....
....0ggggGG0....
....0GGGGhh0....
....00000000....
................
................
................
""")

MASTER_KEY = grid("""
................
................
................
................
...0000.........
..0LLYO0........
.0LY00YO0000000.
.0Y0..0YYYYYYYO0
.0YO00OO0000OO0.
..0OOOO0....0O0.
...0000......0..
................
................
................
................
................
""")

RECORD = grid("""
................
......0000......
....00055000....
...0w054450w0...
...0wkkkkkkw0...
...0wk3333kw0...
...0wkkkkkkw0...
...0wk333kkw0...
...0wkkkkkkw0...
...0wk3333kw0...
...0wkkkkkkw0...
...0wk33kkkw0...
...0wkkkkkkW0...
...0WWWWWWWW0...
....00000000....
................
""")

MEMO = paint(recolor(RECORD, {"k": "L", "3": "y"}), 5, 9, ["RRRR"])

EVAC_ZONE = grid("""
gggg........gggg
gGGG........GGGg
gG............Gg
gG............Gg
.......66.......
......6666......
.....666666.....
.......66.......
.......66.......
.......66.......
................
................
gG............Gg
gG............Gg
gGGG........GGGg
gggg........gggg
""")

WINDOW = grid("""
................
................
................
..000000000000..
..055555555550..
..051b65511bk50.
..051bb5511bb50.
..0511b55111b50.
..055555555550..
..051bb5511bb50.
..0511b55111b50.
..051115511150..
..044444444440..
..000000000000..
................
................
""")


def build_objects():
    OBJECTS.add("locker", LOCKER, anchor=(8, 23))
    OBJECTS.add("locker_hidden", LOCKER_HIDDEN, anchor=(8, 23))
    OBJECTS.add("vending", VENDING, anchor=(8, 23))
    OBJECTS.add("desk", DESK, anchor=(8, 15))
    OBJECTS.add("nurse_station", NURSE_STATION, anchor=(8, 15))
    OBJECTS.add("bed", BED, BED_PAL, anchor=(8, 15))
    OBJECTS.add("bed_head", BED_HEAD, BED_PAL, anchor=(8, 15))
    OBJECTS.add("bed_foot", BED_FOOT, BED_PAL, anchor=(8, 15))
    OBJECTS.add("wheelchair", WHEELCHAIR, anchor=(8, 15))
    OBJECTS.add("plant", PLANT, anchor=(8, 15))
    OBJECTS.add("cctv", CCTV_OFF, anchor=(8, 15))
    for i, rows in enumerate(CCTV_ON):
        OBJECTS.add(f"cctv_on_{i}", rows, anchor=(8, 15))
    ANIMS["cctv_on"] = ["cctv_on_0", "cctv_on_1"]
    for i, rows in enumerate(GENERATOR_OFF):
        OBJECTS.add(f"generator_off_{i}", rows, anchor=(8, 19))
    for i, rows in enumerate(GENERATOR_ON):
        OBJECTS.add(f"generator_on_{i}", rows, anchor=(8, 19))
    ANIMS["generator_off"] = ["generator_off_0", "generator_off_1"]
    ANIMS["generator_on"] = ["generator_on_0", "generator_on_1"]

    OBJECTS.add("elevator_closed", door("2", "11LL11RR11", ELEVATOR_CLOSED), anchor=(8, 23))
    OBJECTS.add("elevator_open", door("2", "11LL11gg11", ELEVATOR_OPEN), anchor=(8, 23))
    OBJECTS.add("decon_closed", door("2", "Y0Y0RR0Y0Y", DECON_CLOSED), anchor=(8, 23))
    OBJECTS.add("decon_open", door("2", "Y0Y0gg0Y0Y", DECON_OPEN), anchor=(8, 23))
    OBJECTS.add("roof_closed", door("2", "GG66GGGRRG", ROOF_CLOSED), anchor=(8, 23))
    OBJECTS.add("roof_open", door("2", "GG66GGGggG", ROOF_OPEN), anchor=(8, 23))
    OBJECTS.add("security_closed", card_reader(door("3", "1111111111", SECURITY_CLOSED), "R"), anchor=(8, 23))
    OBJECTS.add("security_open", card_reader(door("3", "1111111111", SECURITY_OPEN), "g"), anchor=(8, 23))
    OBJECTS.add("shutter_closed", door("2", "1111RR1111", SHUTTER_CLOSED), anchor=(8, 23))
    OBJECTS.add("shutter_open", door("2", "1111gg1111", SHUTTER_OPEN), anchor=(8, 23))

    for letter in "ABC":
        OBJECTS.add(f"terminal_{letter}", terminal(letter, False), anchor=(8, 17))
        OBJECTS.add(f"terminal_{letter}_on", terminal(letter, True), anchor=(8, 17))

    OBJECTS.add("keycard", KEYCARD, anchor=(8, 12))
    OBJECTS.add("fuse", FUSE, anchor=(8, 13))
    OBJECTS.add("battery", BATTERY, anchor=(8, 12))
    OBJECTS.add("master_key", MASTER_KEY, anchor=(8, 11))
    OBJECTS.add("record", RECORD, anchor=(8, 14))
    OBJECTS.add("memo", MEMO, anchor=(8, 14))
    OBJECTS.add("evac_zone", EVAC_ZONE, anchor=(0, 0))
    OBJECTS.add("window", WINDOW, anchor=(0, 0))


# ============================================================
# UI
# ============================================================

HEART = grid("""
.00...00.
0pR0.0RR0
0pRR0RRr0
0RRRRRRr0
.0RRRRr0.
..0RRr0..
...0r0...
....0....
""")
HEART_EMPTY = recolor(HEART, {"R": "2", "p": "3", "r": "1"})

ICON_CLOCK = grid("""
..00000..
.0666660.
066616660
066616660
066611160
066666660
066666660
.0666660.
..00000..
""")

ICON_BOLT = grid("""
....000
...0LL0
..0LL0.
.0LL000
0LLLLL0
000LL0.
..0LL0.
.0LL0..
.000...
""")

ICON_EYE = grid("""
..00000..
.0666660.
066111660
066101660
066111660
.0666660.
..00000..
""")

ICON_CROSS = grid("""
.0000000.
066ggg660
066ggg660
0ggggggg0
0ggggggg0
0ggggggg0
066ggg660
066ggg660
.0000000.
""")

ICON_TARGET = grid("""
..00000..
.0RRRRR0.
0RR666RR0
0R6RRR6R0
0R6R6R6R0
0R6RRR6R0
0RR666RR0
.0RRRRR0.
..00000..
""")

ICON_BAG = grid("""
...000...
..0...0..
.0000000.
0wwwwwww0
0wWWkWWw0
0wwwkwww0
0wwwwwww0
0WWWWWWW0
.0000000.
""")

ICON_TERMINAL = grid("""
000000000
0bbbbbbb0
0bcbbbbb0
0bbbcbbb0
0bbbbbbb0
000000000
...020...
..00000..
.........
""")

ICON_DOC = grid("""
.0000000.
.0kkkkk0.
.0k333k0.
.0kkkkk0.
.0k333k0.
.0kkkkk0.
.0k33kk0.
.0kkkkk0.
.0000000.
""")

ICON_ALERT = grid("""
.000.
0RRR0
0RRR0
0RRR0
.0R0.
.0R0.
..0..
.000.
.0R0.
.000.
""")

BUBBLE_ALERT = grid("""
.0000000.
066666660
0666R6660
0666R6660
0666R6660
066666660
0666R6660
066666660
.0006000.
...060...
....0....
""")
BUBBLE_HEART = grid("""
.0000000.
066666660
06R666R60
0RRR6RRR0
0RRRRRRR0
06RRRRR60
066RRR660
0666R6660
.0006000.
...060...
....0....
""")
BUBBLE_DOTS = grid("""
.0000000.
066666660
066666660
060606060
066666660
066666660
.0006000.
...060...
....0....
""")

SPARKLES = [
    grid("""
.......
.......
...6...
..666..
...6...
.......
.......
"""),
    grid("""
.......
...6...
...6...
.66L66.
...6...
...6...
.......
"""),
    grid("""
...6...
...6...
.......
66.L.66
.......
...6...
...6...
"""),
]

MARKER = grid("""
0000000
0LLLLL0
.0LLL0.
..0L0..
...0...
""")


def keycap(arrow):
    base = grid("""
.0000000000000.
055555555555550
056666666666640
056666666666640
056666666666640
056666666666640
056666666666640
056666666666640
056666666666640
056666666666640
054444444444440
053333333333330
.0000000000000.
""")
    up = ["...1...", "..111..", ".11111.", "1111111", "..111..", "..111..", "..111.."]
    shapes = {
        "up": up,
        "down": up[::-1],
        "left": ["".join(row[i] for row in up) for i in range(7)],
        "right": ["".join(row[i] for row in up)[::-1] for i in range(7)],
    }
    return paint(base, 4, 2, [line.replace(".", " ") for line in shapes[arrow]])


def build_ui():
    UI.add("heart", HEART, anchor=(0, 0))
    UI.add("heart_empty", HEART_EMPTY, anchor=(0, 0))
    UI.add("icon_clock", ICON_CLOCK, anchor=(0, 0))
    UI.add("icon_bolt", ICON_BOLT, anchor=(0, 0))
    UI.add("icon_eye", ICON_EYE, anchor=(0, 0))
    UI.add("icon_alert", ICON_ALERT, anchor=(0, 0))
    UI.add("icon_cross", ICON_CROSS, anchor=(0, 0))
    UI.add("icon_target", ICON_TARGET, anchor=(0, 0))
    UI.add("icon_bag", ICON_BAG, anchor=(0, 0))
    UI.add("icon_terminal", ICON_TERMINAL, anchor=(0, 0))
    UI.add("icon_doc", ICON_DOC, anchor=(0, 0))
    UI.add("bubble_alert", BUBBLE_ALERT, anchor=(4, 10))
    UI.add("bubble_heart", BUBBLE_HEART, anchor=(4, 10))
    UI.add("bubble_dots", BUBBLE_DOTS, anchor=(4, 8))
    for i, rows in enumerate(SPARKLES):
        UI.add(f"sparkle_{i}", rows, anchor=(3, 3))
    ANIMS["sparkle"] = ["sparkle_0", "sparkle_1", "sparkle_2", "sparkle_1", "sparkle_0", "sparkle_0"]
    UI.add("marker", MARKER, anchor=(3, 4))
    for arrow in ("up", "down", "left", "right"):
        UI.add(f"key_{arrow}", keycap(arrow), anchor=(0, 0))


# ============================================================
# 출력
# ============================================================

def write_atlas(sheets):
    lines = [
        "// 이 파일은 tools/build_sprites.py 가 자동으로 만든다. 직접 고치지 말 것.",
        "// frames: 이름 → [시트, x, y, 폭, 높이, 기준점 x, 기준점 y]",
        "window.SPRITE_ATLAS = {",
        "  sheets: {",
    ]
    for sheet in sheets:
        lines.append(f'    {sheet.name}: "assets/sprites/{sheet.name}.png",')
    lines += ["  },", "  frames: {"]
    for sheet in sheets:
        for s in sheet.sprites:
            lines.append(f'    {s["name"]}: ["{sheet.name}", {s["x"]}, {s["y"]}, {s["w"]}, {s["h"]}, {s["ax"]}, {s["ay"]}],')
    lines += ["  },", "  anims: {"]
    for name, frames in ANIMS.items():
        lines.append(f"    {name}: [{', '.join(repr(f).replace(chr(39), chr(34)) for f in frames)}],")
    lines += ["  },", "};", ""]
    ATLAS_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_preview(sheets, path, scale=5):
    """모든 스프라이트를 확대해서 이름과 함께 한 장에 늘어놓는다."""
    cells = []
    for sheet in sheets:
        image = Image.open(SPRITE_DIR / f"{sheet.name}.png")
        for s in sheet.sprites:
            crop = image.crop((s["x"], s["y"], s["x"] + s["w"], s["y"] + s["h"]))
            cells.append((s["name"], crop.resize((s["w"] * scale, s["h"] * scale), Image.NEAREST)))
    columns, cell_w, cell_h = 10, 24 * scale, 24 * scale + 14
    rows = (len(cells) + columns - 1) // columns
    preview = Image.new("RGBA", (columns * cell_w, rows * cell_h), "#20243a")
    draw = ImageDraw.Draw(preview)
    for i, (name, sprite) in enumerate(cells):
        x, y = (i % columns) * cell_w, (i // columns) * cell_h
        draw.rectangle([x + 2, y + 2, x + cell_w - 3, y + cell_h - 16], fill="#9aa3b8")
        preview.alpha_composite(sprite, (x + (cell_w - sprite.width) // 2, y + (cell_h - 14 - sprite.height) // 2))
        draw.text((x + 4, y + cell_h - 13), name, fill="#ffffff")
    preview.save(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--preview", help="확대 미리보기 PNG 저장 경로")
    args = parser.parse_args()

    build_tiles()
    build_characters()
    build_objects()
    build_ui()

    sheets = [TILES, CHARACTERS, OBJECTS, UI]
    SPRITE_DIR.mkdir(parents=True, exist_ok=True)
    for sheet in sheets:
        sheet.build().save(SPRITE_DIR / f"{sheet.name}.png")
        print(f"{sheet.name}.png : 스프라이트 {len(sheet.sprites)}개")
    write_atlas(sheets)
    print(f"atlas.js : {ATLAS_PATH.relative_to(ROOT)}")

    if args.preview:
        write_preview(sheets, args.preview)
        print(f"미리보기 : {args.preview}")


if __name__ == "__main__":
    main()

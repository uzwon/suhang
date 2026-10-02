import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# STREAMLIT 기본 설정
# ============================================================

st.set_page_config(
    page_title="MIDNIGHT HOSPITAL",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 MIDNIGHT HOSPITAL")
st.caption(
    "픽셀 병원 탈출 어드벤처 · 방향키/WASD 이동 · Space 상호작용 · R 현재 테마 재시작"
)


# ============================================================
# 실제 게임
# HTML + JavaScript Canvas를 Streamlit 안에서 실행
# ============================================================

game_html = r"""
<!DOCTYPE html>
<html lang="ko">

<head>
<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
    user-select: none;
}

html,
body {
    margin: 0;
    padding: 0;
    background: #dce7ea;
    font-family: Arial, "Malgun Gothic", sans-serif;
}

body {
    overflow: hidden;
}

.wrap {
    padding: 12px;
}

.topbar {
    background: linear-gradient(180deg, #263f4a, #1e333d);
    color: white;
    border-radius: 16px;
    padding: 14px 18px;
    margin-bottom: 12px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.14);
}

.title {
    font-size: 28px;
    font-weight: 900;
    letter-spacing: 2px;
}

.subtitle {
    margin-top: 5px;
    font-size: 13px;
    opacity: 0.9;
}

.layout {
    display: flex;
    gap: 12px;
    align-items: flex-start;
}

.game-area {
    position: relative;
    background: #edf4f6;
    border: 2px solid #9db3bb;
    border-radius: 16px;
    padding: 10px;
}

#messageBar {
    min-height: 48px;
    margin-bottom: 8px;
    padding: 10px 13px;

    background: #fff3d5;

    border-left: 6px solid #d5ae45;
    border-radius: 10px;

    color: #594c29;
    font-size: 14px;
    line-height: 1.5;
}

canvas {
    display: block;

    width: 1056px;
    height: 640px;

    border: 3px solid #688792;
    border-radius: 8px;

    background: #132832;

    image-rendering: pixelated;
    image-rendering: crisp-edges;

    outline: none;
}

.help {
    margin-top: 8px;
    padding: 9px 12px;

    background: #e4eff2;
    border-radius: 10px;

    color: #2b4751;
    font-size: 13px;
    line-height: 1.6;
}

.side {
    width: 280px;
    flex: 0 0 280px;
}

.card {
    margin-bottom: 10px;
    padding: 14px;

    background: #fbfdfe;

    border: 1px solid #acbec5;
    border-radius: 14px;
}

.card h3 {
    margin: 0 0 10px 0;
    color: #263e47;
    font-size: 17px;
}

.theme-card {
    padding: 11px;

    background: #263e48;
    border-radius: 9px;

    color: white;
    line-height: 1.6;
    font-size: 13px;
}

.objective {
    padding: 10px;

    background: #e8f1fb;

    border-left: 5px solid #6b8eb4;
    border-radius: 9px;

    color: #304c61;
    font-size: 13px;
    line-height: 1.65;
}

.stat {
    margin-bottom: 7px;
    font-size: 13px;
}

.item {
    margin-bottom: 6px;
    padding: 7px 9px;

    background: #edf4f6;
    border-radius: 8px;

    font-size: 13px;
}

.log {
    margin-bottom: 5px;
    padding: 7px;

    background: #283b44;
    border-radius: 8px;

    color: #dbe8eb;

    font-family: monospace;
    font-size: 11px;
    line-height: 1.5;
}

button {
    width: 100%;
    padding: 11px;

    border: none;
    border-radius: 10px;

    background: #416675;
    color: white;

    font-weight: 800;
    cursor: pointer;
}

button:hover {
    filter: brightness(1.08);
}

.dpad {
    display: grid;

    grid-template-columns: 46px 46px 46px;
    grid-template-rows: 42px 42px 42px;

    justify-content: center;

    margin-top: 10px;
    gap: 3px;
}

.dpad button {
    padding: 0;
    font-size: 20px;
}

.empty {
    visibility: hidden;
}

.overlay {
    position: absolute;

    top: 68px;
    left: 10px;

    width: 1056px;
    height: 640px;

    display: none;

    align-items: center;
    justify-content: center;

    background: rgba(6, 14, 20, 0.76);

    border-radius: 8px;

    z-index: 20;
}

.overlay-box {
    width: 460px;
    padding: 26px;

    background: white;

    border-radius: 18px;

    text-align: center;

    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
}

.overlay-title {
    margin-bottom: 12px;

    color: #213942;

    font-size: 32px;
    font-weight: 900;
}

.overlay-text {
    margin-bottom: 18px;

    color: #344e58;

    line-height: 1.8;
}

@media(max-width:1450px) {

    .layout {
        flex-direction: column;
    }

    .side {
        width: 100%;
        flex: auto;
    }

    canvas {
        width: 100%;
        height: auto;
    }
}

</style>
</head>


<body tabindex="0">


<div class="wrap">


    <div class="topbar">

        <div class="title">
            MIDNIGHT HOSPITAL
        </div>

        <div
            class="subtitle"
            id="subtitleText">
        </div>

    </div>


    <div class="layout">


        <div class="game-area">


            <div id="messageBar">
                게임을 불러오는 중입니다.
            </div>


            <canvas
                id="game"
                width="1056"
                height="640"
                tabindex="0">
            </canvas>


            <div class="help">

                <b>조작법</b><br>

                방향키 / WASD : 이동<br>

                Space / Enter : 상호작용<br>

                R : 현재 테마 처음부터 다시 시작


                <div class="dpad">

                    <button class="empty">.</button>

                    <button
                        onmousedown="pressDirection('ArrowUp')"
                        onmouseup="releaseDirection('ArrowUp')"
                        onmouseleave="releaseDirection('ArrowUp')">
                        ↑
                    </button>

                    <button class="empty">.</button>


                    <button
                        onmousedown="pressDirection('ArrowLeft')"
                        onmouseup="releaseDirection('ArrowLeft')"
                        onmouseleave="releaseDirection('ArrowLeft')">
                        ←
                    </button>

                    <button onclick="interact()">
                        ◎
                    </button>

                    <button
                        onmousedown="pressDirection('ArrowRight')"
                        onmouseup="releaseDirection('ArrowRight')"
                        onmouseleave="releaseDirection('ArrowRight')">
                        →
                    </button>


                    <button class="empty">.</button>

                    <button
                        onmousedown="pressDirection('ArrowDown')"
                        onmouseup="releaseDirection('ArrowDown')"
                        onmouseleave="releaseDirection('ArrowDown')">
                        ↓
                    </button>

                    <button class="empty">.</button>

                </div>

            </div>


            <div
                class="overlay"
                id="overlay">

                <div
                    class="overlay-box"
                    id="overlayBox">
                </div>

            </div>


        </div>


        <div class="side">


            <div class="card">

                <h3>🏥 현재 테마</h3>

                <div
                    class="theme-card"
                    id="themeBox">
                </div>

            </div>


            <div class="card">

                <h3>🎯 현재 목표</h3>

                <div
                    class="objective"
                    id="objectiveBox">
                </div>

            </div>


            <div class="card">

                <h3>📊 상태</h3>

                <div id="statusBox">
                </div>

            </div>


            <div class="card">

                <h3>🎒 인벤토리</h3>

                <div id="inventoryBox">
                </div>

            </div>


            <div class="card">

                <h3>📟 야간 기록</h3>

                <div id="logBox">
                </div>

            </div>


            <button onclick="restartCurrentTheme()">
                🔄 현재 테마 다시 시작
            </button>


        </div>


    </div>


</div>


<script>


// ============================================================
// HTML 요소
// ============================================================

const canvas =
    document.getElementById("game");

const ctx =
    canvas.getContext("2d");

ctx.imageSmoothingEnabled = false;


const messageBar =
    document.getElementById("messageBar");

const objectiveBox =
    document.getElementById("objectiveBox");

const statusBox =
    document.getElementById("statusBox");

const inventoryBox =
    document.getElementById("inventoryBox");

const logBox =
    document.getElementById("logBox");

const themeBox =
    document.getElementById("themeBox");

const subtitleText =
    document.getElementById("subtitleText");

const overlay =
    document.getElementById("overlay");

const overlayBox =
    document.getElementById("overlayBox");


// ============================================================
// 맵 공통 설정
// ============================================================

const TILE = 32;

const COLS = 33;

const ROWS = 20;


// ============================================================
// 테마 3개
//
// 같은 병원이지만
// 각 구역마다 구조, 분위기, 아이템 이름이 바뀜.
// ============================================================

const LEVELS = [


    // --------------------------------------------------------
    // THEME 1
    // --------------------------------------------------------

    {

        title:
            "THEME 1 · 정전된 본관",

        story:
            "병원 본관 전체가 정전됐다. 비상 전력을 복구하고 엘리베이터를 작동시켜야 한다.",

        time:
            420,

        palette: {

            floor1: "#b6c8ce",
            floor2: "#adc1c8",

            wall1: "#334f5b",
            wall2: "#4d6974",
            wall3: "#607d87"

        },

        labels: {

            K: "출입카드",

            F: "퓨즈",

            B: "비상 배터리",

            P: "발전기",

            M: "마스터 키",

            E: "엘리베이터",

            C: "보안문",

            D: "전원문",

            W: "창문",

            T: "안내 데스크",

            H: "병원 침대",

            Q: "휠체어",

            N: "간호 스테이션",

            V: "자판기"

        },

        map: [

            "#################################",
            "#S....W....T......#............E#",
            "#......######.....#.............#",
            "#......#....#.....#....H........#",
            "#......#.K..#..........H........#",
            "#......#....#####...............#",
            "#......####..............######.#",
            "#....C........F.................#",
            "#...............................#",
            "#..B..............######........#",
            "#.................#....#........#",
            "#.................#....#........#",
            "#.P...............#....#......D.#",
            "#.................#....#........#",
            "#.....######......#....######...#",
            "#.....#....#......#.............#",
            "#..N..#....#..M...#.......Q.....#",
            "#.....######................V...#",
            "#...............................#",
            "#################################"

        ]

    },


    // --------------------------------------------------------
    // THEME 2
    // --------------------------------------------------------

    {

        title:
            "THEME 2 · 격리 연구동",

        story:
            "본관을 빠져나왔지만 격리 연구동의 자동문이 잠겼다. 연구동 제어 시스템을 복구해야 한다.",

        time:
            390,

        palette: {

            floor1: "#b9cbbd",
            floor2: "#aebfaf",

            wall1: "#314d48",
            wall2: "#486b64",
            wall3: "#5b8279"

        },

        labels: {

            K: "연구동 카드",

            F: "제어 퓨즈",

            B: "백업 배터리",

            P: "격리 제어판",

            M: "격리구역 키",

            E: "제독실 출구",

            C: "격리문",

            D: "자동 보안문",

            W: "관찰창",

            T: "연구 데스크",

            H: "격리 침대",

            Q: "휠체어",

            N: "간호 스테이션",

            V: "음료 자판기"

        },

        map: [

            "#################################",
            "#S..W.............#............E#",
            "#....#####........#.............#",
            "#....#...#........#...H...H.....#",
            "#..T.#.K.#........#.............#",
            "#....#...#####....#....######...#",
            "#....#####........#....#....#...#",
            "#.......C......F.......#....#...#",
            "#......................#....#...#",
            "#..B......######..............#.#",
            "#.........#....#......######..#.#",
            "#.........#....#......#....#..#.#",
            "#.P.......#....#......#....#..D.#",
            "#.........######......#....#....#",
            "#.....................######....#",
            "#....N......................Q...#",
            "#............M..................#",
            "#.........................V.....#",
            "#...............................#",
            "#################################"

        ]

    },


    // --------------------------------------------------------
    // THEME 3
    // --------------------------------------------------------

    {

        title:
            "THEME 3 · 옥상 연결 병동",

        story:
            "마지막 출구는 옥상 연결 통로다. 비상 제어 장치를 복구하고 옥상 출입문을 열어야 한다.",

        time:
            360,

        palette: {

            floor1: "#c7c3d4",
            floor2: "#b8b4c8",

            wall1: "#44425b",
            wall2: "#5b5875",
            wall3: "#716d8f"

        },

        labels: {

            K: "비상 출입카드",

            F: "옥상 제어 퓨즈",

            B: "무전기 배터리",

            P: "비상 제어반",

            M: "옥상 마스터키",

            E: "옥상 출구",

            C: "방화문",

            D: "옥상 보안문",

            W: "야간 창문",

            T: "병동 데스크",

            H: "병원 침대",

            Q: "휠체어",

            N: "간호 스테이션",

            V: "자판기"

        },

        map: [

            "#################################",
            "#S........W........#...........E#",
            "#..######..........#............#",
            "#..#....#..........#....H.......#",
            "#..#.K..#..T.......#............#",
            "#..#....#####......#....#####...#",
            "#..######..........#....#...#...#",
            "#.....C.......F.........#...#...#",
            "#.......................#...#...#",
            "#..B.........#####..............#",
            "#............#...#.....#####....#",
            "#............#...#.....#...#....#",
            "#.P..........#...#.....#...#..D.#",
            "#............#####.....#...#....#",
            "#......................#####....#",
            "#....N......................Q...#",
            "#...............M...............#",
            "#.........................V.....#",
            "#...............................#",
            "#################################"

        ]

    }

];


// ============================================================
// 게임 변수
// ============================================================

let currentLevelIndex = 0;

let player;

let state;

let keys = {};

let ghosts = [];

let lastTime =
    performance.now();

let invulnerable = 0;


// ============================================================
// 현재 레벨 가져오기
// ============================================================

function currentLevel() {

    return LEVELS[
        currentLevelIndex
    ];

}


// ============================================================
// 맵 검증
//
// 수행평가의 예외/오류 처리에도 활용 가능.
// 맵 길이나 필수 아이템이 잘못되면 게임이 조용히 고장나는
// 대신 오류 화면을 띄운다.
// ============================================================

function validateLevel(level) {

    if (
        !level
        ||
        !Array.isArray(level.map)
        ||
        level.map.length !== ROWS
    ) {

        return {
            ok: false,
            message: "맵의 세로 크기가 올바르지 않습니다."
        };

    }


    for (
        let y = 0;
        y < level.map.length;
        y++
    ) {

        if (
            level.map[y].length !== COLS
        ) {

            return {

                ok: false,

                message:
                    "맵 "
                    +
                    (y + 1)
                    +
                    "번째 줄의 길이가 올바르지 않습니다."

            };

        }

    }


    const requiredSymbols = [

        "S",
        "K",
        "F",
        "B",
        "P",
        "M",
        "E"

    ];


    for (
        const symbol
        of
        requiredSymbols
    ) {

        if (
            !findTileInLevel(
                level,
                symbol
            )
        ) {

            return {

                ok: false,

                message:
                    "필수 오브젝트 "
                    +
                    symbol
                    +
                    "가 맵에 없습니다."

            };

        }

    }


    return {
        ok: true
    };

}


// ============================================================
// 특정 레벨에서 타일 찾기
// ============================================================

function findTileInLevel(
    level,
    symbol
) {

    for (
        let y = 0;
        y < ROWS;
        y++
    ) {

        for (
            let x = 0;
            x < COLS;
            x++
        ) {

            if (
                level.map[y][x]
                ===
                symbol
            ) {

                return {

                    x: x,

                    y: y

                };

            }

        }

    }


    return null;

}


// ============================================================
// 현재 맵에서 타일 찾기
// ============================================================

function findTile(symbol) {

    return findTileInLevel(
        currentLevel(),
        symbol
    );

}


// ============================================================
// 타일 중앙 좌표
// ============================================================

function tileCenter(
    x,
    y
) {

    return {

        x:
            x * TILE
            +
            TILE / 2,

        y:
            y * TILE
            +
            TILE / 2

    };

}


// ============================================================
// 전체 게임 시작
// ============================================================

function startWholeGame() {

    currentLevelIndex = 0;

    startLevel();

}


// ============================================================
// 현재 테마 시작
// ============================================================

function startLevel() {

    const level =
        currentLevel();


    const validation =
        validateLevel(
            level
        );


    if (
        !validation.ok
    ) {

        showFatalError(
            validation.message
        );

        return;

    }


    const start =
        findTile("S");


    player = {

        x:
            start.x * TILE + 1,

        y:
            start.y * TILE - 4,


        // 화면에 보이는 캐릭터 크기

        spriteW:
            30,

        spriteH:
            38,


        // 실제 충돌 판정은 발 근처만

        hitW:
            12,

        hitH:
            8,

        hitOffsetX:
            9,

        hitOffsetY:
            20,


        speed:
            160,


        facing:
            "down",

        walking:
            false,

        walkFrame:
            0,

        walkTimer:
            0

    };


    state = {

        hearts:
            4,

        time:
            level.time,

        hasKeycard:
            false,

        hasFuse:
            false,

        hasBattery:
            false,

        powerOn:
            false,

        hasMasterKey:
            false,

        won:
            false,

        lost:
            false,

        logs:
            [],

        score:
            0

    };


    ghosts = createGhostsForLevel();


    invulnerable = 0;


    state.logs.push(
        "현재 구역 진입 : "
        +
        level.title
    );


    state.logs.push(
        "출구 시스템이 잠겨 있습니다."
    );


    setMessage(
        level.story
    );


    subtitleText.innerHTML =
        level.title
        +
        " · 방향키/WASD로 직접 이동";


    overlay.style.display =
        "none";


    updatePanels();


    canvas.focus();

}


// ============================================================
// 레벨별 그림자 NPC
// ============================================================

function createGhostsForLevel() {

    if (
        currentLevelIndex === 0
    ) {

        return [

            {

                x:
                    23 * TILE,

                y:
                    7 * TILE,

                w:
                    20,

                h:
                    20,

                color:
                    "#957cff",

                speed:
                    43,

                active:
                    true,

                path: [

                    tileCenter(23, 7),

                    tileCenter(29, 7),

                    tileCenter(29, 12),

                    tileCenter(23, 12)

                ],

                pathIndex:
                    1

            }

        ];

    }


    if (
        currentLevelIndex === 1
    ) {

        return [

            {

                x:
                    20 * TILE,

                y:
                    5 * TILE,

                w:
                    20,

                h:
                    20,

                color:
                    "#54d5b0",

                speed:
                    48,

                active:
                    true,

                path: [

                    tileCenter(20, 5),

                    tileCenter(27, 5),

                    tileCenter(27, 10),

                    tileCenter(20, 10)

                ],

                pathIndex:
                    1

            },


            {

                x:
                    6 * TILE,

                y:
                    15 * TILE,

                w:
                    20,

                h:
                    20,

                color:
                    "#99e85b",

                speed:
                    40,

                active:
                    true,

                path: [

                    tileCenter(6, 15),

                    tileCenter(12, 15),

                    tileCenter(12, 18),

                    tileCenter(6, 18)

                ],

                pathIndex:
                    1

            }

        ];

    }


    return [

        {

            x:
                21 * TILE,

            y:
                5 * TILE,

            w:
                20,

            h:
                20,

            color:
                "#ff7da9",

            speed:
                53,

            active:
                true,

            path: [

                tileCenter(21, 5),

                tileCenter(29, 5),

                tileCenter(29, 10),

                tileCenter(21, 10)

            ],

            pathIndex:
                1

        },


        {

            x:
                8 * TILE,

            y:
                14 * TILE,

            w:
                20,

            h:
                20,

            color:
                "#bd8cff",

            speed:
                47,

            active:
                true,

            path: [

                tileCenter(8, 14),

                tileCenter(17, 14),

                tileCenter(17, 18),

                tileCenter(8, 18)

            ],

            pathIndex:
                1

        }

    ];

}


// ============================================================
// 현재 테마 재시작
// ============================================================

function restartCurrentTheme() {

    startLevel();

}


// ============================================================
// 다음 테마
// ============================================================

function nextTheme() {

    if (
        currentLevelIndex
        <
        LEVELS.length - 1
    ) {

        currentLevelIndex += 1;

        startLevel();

        return;

    }


    startWholeGame();

}


// ============================================================
// 치명적 맵 오류 처리
// ============================================================

function showFatalError(message) {

    overlayBox.innerHTML = `

        <div class="overlay-title">

            MAP ERROR

        </div>


        <div class="overlay-text">

            게임 맵을 불러오는 중 문제가 발생했습니다.

            <br><br>

            ${message}

        </div>


        <button onclick="startWholeGame()">

            게임 다시 불러오기

        </button>

    `;


    overlay.style.display =
        "flex";

}


// ============================================================
// 메시지
// ============================================================

function setMessage(text) {

    messageBar.innerHTML =
        text;

}


// ============================================================
// 로그
// ============================================================

function addLog(text) {

    state.logs.unshift(
        text
    );


    if (
        state.logs.length > 7
    ) {

        state.logs.pop();

    }


    updatePanels();

}


// ============================================================
// 오른쪽 UI
// ============================================================

function updatePanels() {

    const level =
        currentLevel();


    themeBox.innerHTML = `

        <b>
        ${level.title}
        </b>

        <br><br>

        ${level.story}

    `;


    let objective = "";


    if (
        !state.hasKeycard
    ) {

        objective =
            "① <b>"
            +
            level.labels.K
            +
            "</b>를 찾아.";

    }

    else if (
        !state.hasFuse
    ) {

        objective =
            "② <b>"
            +
            level.labels.F
            +
            "</b>를 찾아.";

    }

    else if (
        !state.hasBattery
    ) {

        objective =
            "③ <b>"
            +
            level.labels.B
            +
            "</b>를 찾아.";

    }

    else if (
        !state.powerOn
    ) {

        objective =
            "④ <b>"
            +
            level.labels.P
            +
            "</b>으로 가서 전원을 복구해.";

    }

    else if (
        !state.hasMasterKey
    ) {

        objective =
            "⑤ <b>"
            +
            level.labels.M
            +
            "</b>를 찾아.";

    }

    else {

        objective =
            "⑥ <b>"
            +
            level.labels.E
            +
            "</b>로 이동해 다음 구역으로 가!";

    }


    objectiveBox.innerHTML =
        objective;


    const minutes =
        Math.floor(
            state.time / 60
        );


    const seconds =
        Math.floor(
            state.time % 60
        )
        .toString()
        .padStart(
            2,
            "0"
        );


    statusBox.innerHTML = `

        <div class="stat">

            <b>테마</b>
            ${currentLevelIndex + 1}
            /
            ${LEVELS.length}

        </div>


        <div class="stat">

            <b>시간</b>
            ${minutes}:${seconds}

        </div>


        <div class="stat">

            <b>체력</b>

            ${"❤️".repeat(
                Math.max(
                    0,
                    state.hearts
                )
            )}

        </div>


        <div class="stat">

            <b>전원</b>

            ${
                state.powerOn
                ?
                "✅ ON"
                :
                "❌ OFF"
            }

        </div>

    `;


    inventoryBox.innerHTML = `

        <div class="item">

            ${
                state.hasKeycard
                ?
                "✅ "
                +
                level.labels.K

                :

                "⬜ "
                +
                level.labels.K
            }

        </div>


        <div class="item">

            ${
                state.hasFuse
                ?
                "✅ "
                +
                level.labels.F

                :

                "⬜ "
                +
                level.labels.F
            }

        </div>


        <div class="item">

            ${
                state.hasBattery
                ?
                "✅ "
                +
                level.labels.B

                :

                "⬜ "
                +
                level.labels.B
            }

        </div>


        <div class="item">

            ${
                state.hasMasterKey
                ?
                "✅ "
                +
                level.labels.M

                :

                "⬜ "
                +
                level.labels.M
            }

        </div>

    `;


    logBox.innerHTML =

        state.logs

        .map(

            log =>
                `<div class="log">${log}</div>`

        )

        .join("");

}


// ============================================================
// 실제 장애물
//
// 가구와 창문은 이동을 막지 않음.
// 벽과 조건부 문만 막음.
// ============================================================

function tileBlocked(
    tx,
    ty
) {

    if (
        tx < 0
        ||
        ty < 0
        ||
        tx >= COLS
        ||
        ty >= ROWS
    ) {

        return true;

    }


    const symbol =
        currentLevel().map[ty][tx];


    if (
        symbol === "#"
    ) {

        return true;

    }


    if (
        symbol === "C"
        &&
        !state.hasKeycard
    ) {

        return true;

    }


    if (
        symbol === "D"
        &&
        !state.powerOn
    ) {

        return true;

    }


    return false;

}


// ============================================================
// 플레이어 충돌
// ============================================================

function collisionAt(
    newX,
    newY
) {

    const left =
        newX
        +
        player.hitOffsetX;


    const right =
        left
        +
        player.hitW
        -
        1;


    const top =
        newY
        +
        player.hitOffsetY;


    const bottom =
        top
        +
        player.hitH
        -
        1;


    const points = [

        {
            x: left,
            y: top
        },

        {
            x: right,
            y: top
        },

        {
            x: left,
            y: bottom
        },

        {
            x: right,
            y: bottom
        }

    ];


    for (
        const point
        of
        points
    ) {

        const tx =
            Math.floor(
                point.x / TILE
            );


        const ty =
            Math.floor(
                point.y / TILE
            );


        if (
            tileBlocked(
                tx,
                ty
            )
        ) {

            return true;

        }

    }


    return false;

}


// ============================================================
// 플레이어 이동
// ============================================================

function updatePlayer(dt) {

    let dx = 0;

    let dy = 0;


    if (
        keys["ArrowLeft"]
        ||
        keys["a"]
        ||
        keys["A"]
    ) {

        dx -= 1;

        player.facing =
            "left";

    }


    if (
        keys["ArrowRight"]
        ||
        keys["d"]
        ||
        keys["D"]
    ) {

        dx += 1;

        player.facing =
            "right";

    }


    if (
        keys["ArrowUp"]
        ||
        keys["w"]
        ||
        keys["W"]
    ) {

        dy -= 1;

        player.facing =
            "up";

    }


    if (
        keys["ArrowDown"]
        ||
        keys["s"]
        ||
        keys["S"]
    ) {

        dy += 1;

        player.facing =
            "down";

    }


    player.walking =
        dx !== 0
        ||
        dy !== 0;


    if (
        dx !== 0
        &&
        dy !== 0
    ) {

        dx *= 0.707106;

        dy *= 0.707106;

    }


    const movementX =
        dx
        *
        player.speed
        *
        dt;


    const movementY =
        dy
        *
        player.speed
        *
        dt;


    // X축과 Y축을 따로 판정
    // 벽에 닿아도 벽을 따라 미끄러지듯 이동

    if (
        !collisionAt(
            player.x + movementX,
            player.y
        )
    ) {

        player.x +=
            movementX;

    }


    if (
        !collisionAt(
            player.x,
            player.y + movementY
        )
    ) {

        player.y +=
            movementY;

    }


    if (
        player.walking
    ) {

        player.walkTimer +=
            dt;


        if (
            player.walkTimer > 0.14
        ) {

            player.walkFrame =
                player.walkFrame === 0
                ?
                1
                :
                0;


            player.walkTimer =
                0;

        }

    }

    else {

        player.walkFrame =
            0;

    }

}


// ============================================================
// 플레이어 중심
// ============================================================

function playerCenter() {

    return {

        x:
            player.x + 15,

        y:
            player.y + 23

    };

}


// ============================================================
// 특정 오브젝트와 가까운지
// ============================================================

function nearTile(
    symbol,
    distance = 42
) {

    const tile =
        findTile(
            symbol
        );


    if (
        !tile
    ) {

        return false;

    }


    const pc =
        playerCenter();


    const tc =
        tileCenter(
            tile.x,
            tile.y
        );


    return (

        Math.hypot(

            pc.x - tc.x,

            pc.y - tc.y

        )

        <=

        distance

    );

}


// ============================================================
// 상호작용
// ============================================================

function interact() {

    canvas.focus();


    if (
        state.won
        ||
        state.lost
    ) {

        return;

    }


    const labels =
        currentLevel().labels;


    // --------------------------------------------------------
    // 출입카드
    // --------------------------------------------------------

    if (
        nearTile("K")
        &&
        !state.hasKeycard
    ) {

        state.hasKeycard =
            true;


        state.score +=
            100;


        setMessage(
            "🪪 "
            +
            labels.K
            +
            "를 획득했어!"
        );


        addLog(
            labels.K
            +
            " 확보."
        );


        return;

    }


    // --------------------------------------------------------
    // 퓨즈
    // --------------------------------------------------------

    if (
        nearTile("F")
        &&
        !state.hasFuse
    ) {

        state.hasFuse =
            true;


        state.score +=
            100;


        setMessage(
            "🧰 "
            +
            labels.F
            +
            "를 획득했어!"
        );


        addLog(
            labels.F
            +
            " 확보."
        );


        return;

    }


    // --------------------------------------------------------
    // 배터리
    // --------------------------------------------------------

    if (
        nearTile("B")
        &&
        !state.hasBattery
    ) {

        state.hasBattery =
            true;


        state.score +=
            100;


        setMessage(
            "🔋 "
            +
            labels.B
            +
            "를 획득했어!"
        );


        addLog(
            labels.B
            +
            " 확보."
        );


        return;

    }


    // --------------------------------------------------------
    // 발전기 / 제어판
    // 필요한 아이템이 없을 때의 예외처리
    // --------------------------------------------------------

    if (
        nearTile("P")
    ) {

        if (
            state.powerOn
        ) {

            setMessage(
                "⚡ "
                +
                labels.P
                +
                "은 이미 작동 중이야."
            );


            return;

        }


        if (
            state.hasFuse
            &&
            state.hasBattery
        ) {

            state.powerOn =
                true;


            state.score +=
                300;


            setMessage(
                "⚡ "
                +
                labels.P
                +
                " 작동 성공!"
            );


            addLog(
                "전원 시스템 복구."
            );


            return;

        }


        const needed =
            [];


        if (
            !state.hasFuse
        ) {

            needed.push(
                labels.F
            );

        }


        if (
            !state.hasBattery
        ) {

            needed.push(
                labels.B
            );

        }


        setMessage(

            "⚠️ "
            +
            labels.P
            +
            "을 사용하려면 "
            +
            needed.join(", ")
            +
            "가 필요해."

        );


        return;

    }


    // --------------------------------------------------------
    // 마스터키
    // 전원 미복구 시 예외처리
    // --------------------------------------------------------

    if (
        nearTile("M")
        &&
        !state.hasMasterKey
    ) {

        if (
            !state.powerOn
        ) {

            setMessage(
                "🚪 전원을 먼저 복구해야 "
                +
                labels.M
                +
                "를 얻을 수 있어."
            );


            return;

        }


        state.hasMasterKey =
            true;


        state.score +=
            200;


        setMessage(
            "🗝️ "
            +
            labels.M
            +
            "를 획득했어!"
        );


        addLog(
            labels.M
            +
            " 확보."
        );


        return;

    }


    // --------------------------------------------------------
    // 출구
    // --------------------------------------------------------

    if (
        nearTile("E")
    ) {

        if (
            state.powerOn
            &&
            state.hasMasterKey
        ) {

            state.score +=
                500;


            clearCurrentTheme();


            return;

        }


        const needed =
            [];


        if (
            !state.powerOn
        ) {

            needed.push(
                "전원 복구"
            );

        }


        if (
            !state.hasMasterKey
        ) {

            needed.push(
                labels.M
            );

        }


        setMessage(

            "🚪 "
            +
            labels.E
            +
            "를 이용하려면 "
            +
            needed.join(", ")
            +
            "가 필요해."

        );


        return;

    }


    // --------------------------------------------------------
    // 잠긴 카드 보안문
    // --------------------------------------------------------

    if (
        nearTile("C")
        &&
        !state.hasKeycard
    ) {

        setMessage(
            "🔒 "
            +
            labels.C
            +
            "을 열려면 "
            +
            labels.K
            +
            "가 필요해."
        );


        return;

    }


    // --------------------------------------------------------
    // 잠긴 전원문
    // --------------------------------------------------------

    if (
        nearTile("D")
        &&
        !state.powerOn
    ) {

        setMessage(
            "⚡ "
            +
            labels.D
            +
            "은 전원이 복구되어야 열려."
        );


        return;

    }


    setMessage(
        "주변에 지금 사용할 수 있는 물건이 없어."
    );

}


// ============================================================
// 테마 클리어
// ============================================================

function clearCurrentTheme() {

    state.won =
        true;


    const level =
        currentLevel();


    const timeBonus =
        Math.floor(
            state.time
        );


    state.score +=
        timeBonus;


    if (
        currentLevelIndex
        <
        LEVELS.length - 1
    ) {

        overlayBox.innerHTML = `

            <div class="overlay-title">

                THEME CLEAR

            </div>


            <div class="overlay-text">

                <b>
                ${level.title}
                </b>

                클리어!

                <br><br>

                현재 구역에서 탈출했지만
                병원에는 아직 빠져나가야 할 구역이 남아 있어.

                <br><br>

                다음 테마

                <br>

                <b>
                ${LEVELS[currentLevelIndex + 1].title}
                </b>

            </div>


            <button onclick="nextTheme()">

                다음 테마로 이동 →

            </button>

        `;


        overlay.style.display =
            "flex";


        return;

    }


    // 마지막 테마 클리어

    overlayBox.innerHTML = `

        <div class="overlay-title">

            HOSPITAL ESCAPED!

        </div>


        <div class="overlay-text">

            마지막 옥상 출구까지 열었다.

            <br><br>

            세 개의 병원 구역을 모두 통과해
            탈출에 성공했어!

            <br><br>

            <b>
            MIDNIGHT HOSPITAL COMPLETE
            </b>

        </div>


        <button onclick="startWholeGame()">

            처음부터 다시 플레이

        </button>

    `;


    overlay.style.display =
        "flex";

}


// ============================================================
// 화면 방향키
// ============================================================

function pressDirection(direction) {

    keys[direction] =
        true;


    canvas.focus();

}


function releaseDirection(direction) {

    keys[direction] =
        false;

}


// ============================================================
// 그림자 NPC 이동
// ============================================================

function updateGhosts(dt) {

    if (
        invulnerable > 0
    ) {

        invulnerable -=
            dt;

    }


    ghosts.forEach(

        ghost => {

            if (
                !ghost.active
            ) {

                return;

            }


            const target =
                ghost.path[
                    ghost.pathIndex
                ];


            const centerX =
                ghost.x
                +
                ghost.w / 2;


            const centerY =
                ghost.y
                +
                ghost.h / 2;


            const dx =
                target.x
                -
                centerX;


            const dy =
                target.y
                -
                centerY;


            const distance =
                Math.hypot(
                    dx,
                    dy
                );


            if (
                distance < 3
            ) {

                ghost.pathIndex =
                    (
                        ghost.pathIndex + 1
                    )
                    %
                    ghost.path.length;

            }

            else {

                ghost.x +=
                    (
                        dx / distance
                    )
                    *
                    ghost.speed
                    *
                    dt;


                ghost.y +=
                    (
                        dy / distance
                    )
                    *
                    ghost.speed
                    *
                    dt;

            }


            if (
                invulnerable <= 0
            ) {

                const pc =
                    playerCenter();


                const gc = {

                    x:
                        ghost.x
                        +
                        ghost.w / 2,

                    y:
                        ghost.y
                        +
                        ghost.h / 2

                };


                if (
                    Math.hypot(

                        pc.x - gc.x,

                        pc.y - gc.y

                    )
                    <
                    21
                ) {

                    state.hearts -=
                        1;


                    invulnerable =
                        1.4;


                    const start =
                        findTile("S");


                    player.x =
                        start.x * TILE + 1;


                    player.y =
                        start.y * TILE - 4;


                    setMessage(
                        "👻 병원 안의 수상한 그림자와 부딪혔어! 체력 -1"
                    );


                    addLog(
                        "그림자와 충돌. 시작 위치로 복귀."
                    );


                    if (
                        state.hearts <= 0
                    ) {

                        state.lost =
                            true;


                        showGameOver(
                            "체력이 모두 소진됐어."
                        );

                    }

                }

            }

        }

    );

}


// ============================================================
// GAME OVER
// ============================================================

function showGameOver(reason) {

    overlayBox.innerHTML = `

        <div class="overlay-title">

            GAME OVER

        </div>


        <div class="overlay-text">

            ${reason}

            <br><br>

            현재 테마를 다시 도전할 수 있어.

        </div>


        <button onclick="restartCurrentTheme()">

            현재 테마 다시 시작

        </button>

    `;


    overlay.style.display =
        "flex";

}


// ============================================================
// 사각형 그리기
// ============================================================

function rect(
    x,
    y,
    w,
    h,
    color
) {

    ctx.fillStyle =
        color;


    ctx.fillRect(

        Math.round(x),

        Math.round(y),

        w,

        h

    );

}


// ============================================================
// 바닥
// ============================================================

function drawFloor() {

    const level =
        currentLevel();


    for (
        let y = 0;
        y < ROWS;
        y++
    ) {

        for (
            let x = 0;
            x < COLS;
            x++
        ) {

            if (
                level.map[y][x]
                !==
                "#"
            ) {

                const floorColor =

                    (
                        x + y
                    )
                    %
                    2
                    ===
                    0

                    ?

                    level.palette.floor1

                    :

                    level.palette.floor2;


                rect(

                    x * TILE,

                    y * TILE,

                    TILE,

                    TILE,

                    floorColor

                );


                // 작은 병원 바닥 무늬

                rect(

                    x * TILE + 5,

                    y * TILE + 5,

                    3,

                    3,

                    "rgba(255,255,255,0.12)"

                );

            }

        }

    }

}


// ============================================================
// 벽
// ============================================================

function drawWalls() {

    const level =
        currentLevel();


    for (
        let y = 0;
        y < ROWS;
        y++
    ) {

        for (
            let x = 0;
            x < COLS;
            x++
        ) {

            if (
                level.map[y][x]
                ===
                "#"
            ) {

                rect(

                    x * TILE,

                    y * TILE,

                    TILE,

                    TILE,

                    level.palette.wall1

                );


                rect(

                    x * TILE + 3,

                    y * TILE + 3,

                    TILE - 6,

                    TILE - 6,

                    level.palette.wall2

                );


                rect(

                    x * TILE + 6,

                    y * TILE + 6,

                    TILE - 12,

                    TILE - 12,

                    level.palette.wall3

                );

            }

        }

    }

}


// ============================================================
// 오브젝트 이름표
//
// 사용자가 무엇인지 바로 알아볼 수 있게
// 오브젝트 밑에 작은 한글 이름 표시
// ============================================================

function drawObjectLabel(
    text,
    centerX,
    y
) {

    if (
        !text
    ) {

        return;

    }


    ctx.save();


    ctx.font =
        '9px "Malgun Gothic", sans-serif';


    ctx.textAlign =
        "center";


    ctx.textBaseline =
        "middle";


    const textWidth =
        ctx.measureText(text).width;


    const boxWidth =
        Math.min(
            textWidth + 8,
            72
        );


    rect(

        centerX - boxWidth / 2,

        y - 7,

        boxWidth,

        13,

        "rgba(20,37,45,0.78)"

    );


    ctx.fillStyle =
        "#ffffff";


    ctx.fillText(

        text,

        centerX,

        y

    );


    ctx.restore();

}


// ============================================================
// 병원 가구
// ============================================================

function drawFurniture() {

    const level =
        currentLevel();


    for (
        let y = 0;
        y < ROWS;
        y++
    ) {

        for (
            let x = 0;
            x < COLS;
            x++
        ) {

            const symbol =
                level.map[y][x];


            const px =
                x * TILE;


            const py =
                y * TILE;


            // ------------------------------------------------
            // 창문
            // ------------------------------------------------

            if (
                symbol === "W"
            ) {

                rect(
                    px + 3,
                    py + 2,
                    26,
                    19,
                    "#9fb7c1"
                );

                rect(
                    px + 5,
                    py + 4,
                    22,
                    15,
                    "#153954"
                );

                rect(
                    px + 15,
                    py + 4,
                    2,
                    15,
                    "#d1e9f4"
                );

                rect(
                    px + 5,
                    py + 11,
                    22,
                    2,
                    "#d1e9f4"
                );


                // 별

                rect(
                    px + 8,
                    py + 6,
                    2,
                    2,
                    "#ffffff"
                );


                rect(
                    px + 22,
                    py + 15,
                    2,
                    2,
                    "#ffffff"
                );


                drawObjectLabel(
                    level.labels.W,
                    px + 16,
                    py + 28
                );

            }


            // ------------------------------------------------
            // 데스크
            // ------------------------------------------------

            if (
                symbol === "T"
            ) {

                rect(
                    px + 4,
                    py + 5,
                    24,
                    13,
                    "#8d674a"
                );

                rect(
                    px + 4,
                    py + 3,
                    24,
                    4,
                    "#bb916b"
                );

                rect(
                    px + 7,
                    py + 18,
                    3,
                    6,
                    "#70503b"
                );

                rect(
                    px + 22,
                    py + 18,
                    3,
                    6,
                    "#70503b"
                );


                drawObjectLabel(
                    level.labels.T,
                    px + 16,
                    py + 29
                );

            }


            // ------------------------------------------------
            // 침대
            // ------------------------------------------------

            if (
                symbol === "H"
            ) {

                rect(
                    px + 2,
                    py + 5,
                    28,
                    15,
                    "#d8e6eb"
                );

                rect(
                    px + 4,
                    py + 7,
                    9,
                    6,
                    "#b9d5df"
                );

                rect(
                    px + 13,
                    py + 7,
                    15,
                    11,
                    "#f6fafb"
                );


                drawObjectLabel(
                    level.labels.H,
                    px + 16,
                    py + 28
                );

            }


            // ------------------------------------------------
            // 휠체어
            // ------------------------------------------------

            if (
                symbol === "Q"
            ) {

                rect(
                    px + 7,
                    py + 4,
                    10,
                    6,
                    "#66859b"
                );

                rect(
                    px + 4,
                    py + 12,
                    8,
                    8,
                    "#33474f"
                );

                rect(
                    px + 17,
                    py + 12,
                    8,
                    8,
                    "#33474f"
                );


                drawObjectLabel(
                    level.labels.Q,
                    px + 16,
                    py + 28
                );

            }


            // ------------------------------------------------
            // 간호 스테이션
            // ------------------------------------------------

            if (
                symbol === "N"
            ) {

                rect(
                    px + 3,
                    py + 6,
                    26,
                    13,
                    "#e7f0f3"
                );

                rect(
                    px + 5,
                    py + 3,
                    22,
                    5,
                    "#73a8ba"
                );

                rect(
                    px + 10,
                    py + 10,
                    12,
                    5,
                    "#9cc6d3"
                );


                drawObjectLabel(
                    level.labels.N,
                    px + 16,
                    py + 28
                );

            }


            // ------------------------------------------------
            // 자판기
            // ------------------------------------------------

            if (
                symbol === "V"
            ) {

                rect(
                    px + 7,
                    py + 2,
                    18,
                    22,
                    "#bd4755"
                );

                rect(
                    px + 9,
                    py + 5,
                    14,
                    8,
                    "#cfebf4"
                );

                rect(
                    px + 10,
                    py + 16,
                    12,
                    4,
                    "#f3d26e"
                );


                drawObjectLabel(
                    level.labels.V,
                    px + 16,
                    py + 29
                );

            }


            // ------------------------------------------------
            // 카드 보안문
            // ------------------------------------------------

            if (
                symbol === "C"
            ) {

                rect(
                    px + 5,
                    py + 1,
                    22,
                    23,
                    state.hasKeycard
                    ?
                    "#74aa89"
                    :
                    "#517fb5"
                );


                drawObjectLabel(
                    level.labels.C,
                    px + 16,
                    py + 29
                );

            }


            // ------------------------------------------------
            // 전원 보안문
            // ------------------------------------------------

            if (
                symbol === "D"
            ) {

                rect(
                    px + 5,
                    py + 1,
                    22,
                    23,
                    state.powerOn
                    ?
                    "#74aa89"
                    :
                    "#806044"
                );


                drawObjectLabel(
                    level.labels.D,
                    px + 16,
                    py + 29
                );

            }


            // ------------------------------------------------
            // 발전기 / 제어반
            // ------------------------------------------------

            if (
                symbol === "P"
            ) {

                rect(
                    px + 3,
                    py + 4,
                    26,
                    18,
                    "#485d66"
                );

                rect(
                    px + 8,
                    py + 8,
                    16,
                    9,
                    "#273940"
                );

                rect(
                    px + 10,
                    py + 11,
                    4,
                    4,
                    state.powerOn
                    ?
                    "#83ef86"
                    :
                    "#db6464"
                );

                rect(
                    px + 18,
                    py + 11,
                    4,
                    4,
                    "#e8c854"
                );


                drawObjectLabel(
                    level.labels.P,
                    px + 16,
                    py + 29
                );

            }


            // ------------------------------------------------
            // 출구 / 엘리베이터
            // ------------------------------------------------

            if (
                symbol === "E"
            ) {

                rect(
                    px + 2,
                    py + 1,
                    28,
                    23,
                    "#6e858e"
                );

                rect(
                    px + 5,
                    py + 3,
                    10,
                    20,
                    "#a4b9c0"
                );

                rect(
                    px + 17,
                    py + 3,
                    10,
                    20,
                    "#a4b9c0"
                );

                rect(
                    px + 10,
                    py + 5,
                    12,
                    3,
                    state.powerOn
                    ?
                    "#71e883"
                    :
                    "#d45e67"
                );


                drawObjectLabel(
                    level.labels.E,
                    px + 16,
                    py + 29
                );

            }

        }

    }

}


// ============================================================
// 아이템 그리기 + 이름표
// ============================================================

function drawItems() {

    const level =
        currentLevel();


    for (
        let y = 0;
        y < ROWS;
        y++
    ) {

        for (
            let x = 0;
            x < COLS;
            x++
        ) {

            const symbol =
                level.map[y][x];


            const px =
                x * TILE;


            const py =
                y * TILE;


            // ------------------------------------------------
            // 출입카드
            // ------------------------------------------------

            if (
                symbol === "K"
                &&
                !state.hasKeycard
            ) {

                rect(
                    px + 6,
                    py + 5,
                    20,
                    11,
                    "#438bed"
                );

                rect(
                    px + 9,
                    py + 8,
                    5,
                    4,
                    "#e4f4ff"
                );

                rect(
                    px + 17,
                    py + 8,
                    6,
                    3,
                    "#23548b"
                );


                drawObjectLabel(
                    level.labels.K,
                    px + 16,
                    py + 25
                );

            }


            // ------------------------------------------------
            // 퓨즈
            // ------------------------------------------------

            if (
                symbol === "F"
                &&
                !state.hasFuse
            ) {

                rect(
                    px + 9,
                    py + 3,
                    14,
                    17,
                    "#e5c44e"
                );

                rect(
                    px + 11,
                    py + 6,
                    10,
                    4,
                    "#fff3aa"
                );


                drawObjectLabel(
                    level.labels.F,
                    px + 16,
                    py + 27
                );

            }


            // ------------------------------------------------
            // 배터리
            // ------------------------------------------------

            if (
                symbol === "B"
                &&
                !state.hasBattery
            ) {

                rect(
                    px + 9,
                    py + 3,
                    14,
                    18,
                    "#46a760"
                );

                rect(
                    px + 13,
                    py + 1,
                    6,
                    3,
                    "#d6e4e8"
                );

                rect(
                    px + 13,
                    py + 9,
                    6,
                    2,
                    "#c5f5ce"
                );


                drawObjectLabel(
                    level.labels.B,
                    px + 16,
                    py + 28
                );

            }


            // ------------------------------------------------
            // 마스터 키
            // ------------------------------------------------

            if (
                symbol === "M"
                &&
                !state.hasMasterKey
            ) {

                rect(
                    px + 7,
                    py + 7,
                    13,
                    4,
                    "#f0c13b"
                );

                rect(
                    px + 18,
                    py + 5,
                    7,
                    8,
                    "#f0c13b"
                );


                drawObjectLabel(
                    level.labels.M,
                    px + 16,
                    py + 25
                );

            }

        }

    }

}


// ============================================================
// 플레이어 캐릭터
// ============================================================

function drawPlayer() {

    const x =
        Math.round(
            player.x
        );


    const y =
        Math.round(
            player.y
        );


    // 캐릭터 바닥 그림자

    rect(
        x + 5,
        y + 34,
        20,
        4,
        "rgba(0,0,0,0.20)"
    );


    // 외곽선

    rect(
        x + 6,
        y,
        18,
        5,
        "#253038"
    );

    rect(
        x + 4,
        y + 4,
        22,
        12,
        "#253038"
    );

    rect(
        x + 6,
        y + 16,
        18,
        17,
        "#253038"
    );


    // 갈색 머리

    rect(
        x + 7,
        y + 1,
        16,
        5,
        "#684334"
    );

    rect(
        x + 5,
        y + 5,
        20,
        5,
        "#79513e"
    );

    rect(
        x + 5,
        y + 9,
        4,
        7,
        "#684334"
    );

    rect(
        x + 21,
        y + 9,
        4,
        7,
        "#684334"
    );


    // 얼굴

    rect(
        x + 9,
        y + 8,
        12,
        9,
        "#f3c4a3"
    );


    // 얼굴 방향

    if (
        player.facing === "down"
    ) {

        rect(
            x + 11,
            y + 11,
            2,
            2,
            "#1e2528"
        );

        rect(
            x + 17,
            y + 11,
            2,
            2,
            "#1e2528"
        );

        rect(
            x + 14,
            y + 15,
            3,
            1,
            "#a96764"
        );

    }


    if (
        player.facing === "left"
    ) {

        rect(
            x + 10,
            y + 11,
            2,
            2,
            "#1e2528"
        );

    }


    if (
        player.facing === "right"
    ) {

        rect(
            x + 18,
            y + 11,
            2,
            2,
            "#1e2528"
        );

    }


    // 의료복

    rect(
        x + 11,
        y + 19,
        9,
        11,
        "#4ca8bb"
    );


    // 흰 가운

    rect(
        x + 6,
        y + 19,
        6,
        14,
        "#ffffff"
    );

    rect(
        x + 19,
        y + 19,
        6,
        14,
        "#ffffff"
    );

    rect(
        x + 11,
        y + 19,
        3,
        14,
        "#f9ffff"
    );

    rect(
        x + 17,
        y + 19,
        3,
        14,
        "#f9ffff"
    );


    // 명찰

    rect(
        x + 20,
        y + 21,
        4,
        3,
        "#5294dd"
    );


    // 팔

    rect(
        x + 3,
        y + 21,
        4,
        9,
        "#f7fbfc"
    );

    rect(
        x + 24,
        y + 21,
        4,
        9,
        "#f7fbfc"
    );


    // 손

    rect(
        x + 3,
        y + 29,
        4,
        3,
        "#efbc9b"
    );

    rect(
        x + 24,
        y + 29,
        4,
        3,
        "#efbc9b"
    );


    // 걷기 애니메이션

    if (
        player.walkFrame === 1
        &&
        player.walking
    ) {

        rect(
            x + 9,
            y + 32,
            6,
            4,
            "#344f76"
        );

        rect(
            x + 18,
            y + 31,
            6,
            5,
            "#344f76"
        );

    }

    else {

        rect(
            x + 9,
            y + 31,
            6,
            5,
            "#344f76"
        );

        rect(
            x + 17,
            y + 31,
            6,
            5,
            "#344f76"
        );

    }


    // 신발

    rect(
        x + 8,
        y + 35,
        7,
        3,
        "#202b32"
    );

    rect(
        x + 17,
        y + 35,
        7,
        3,
        "#202b32"
    );


    // 청진기

    rect(
        x + 13,
        y + 20,
        1,
        6,
        "#31464f"
    );

    rect(
        x + 14,
        y + 25,
        5,
        1,
        "#31464f"
    );

    rect(
        x + 18,
        y + 24,
        2,
        3,
        "#31464f"
    );

}


// ============================================================
// 그림자 NPC
// ============================================================

function drawGhost(ghost) {

    if (
        !ghost.active
    ) {

        return;

    }


    const x =
        Math.round(
            ghost.x
        );


    const y =
        Math.round(
            ghost.y
        );


    rect(
        x + 2,
        y + 2,
        16,
        13,
        ghost.color
    );

    rect(
        x + 4,
        y + 14,
        4,
        6,
        ghost.color
    );

    rect(
        x + 9,
        y + 14,
        4,
        6,
        ghost.color
    );

    rect(
        x + 14,
        y + 14,
        4,
        6,
        ghost.color
    );

    rect(
        x + 5,
        y + 6,
        2,
        2,
        "#ffffff"
    );

    rect(
        x + 12,
        y + 6,
        2,
        2,
        "#ffffff"
    );

}


// ============================================================
// 야간 어둠
// ============================================================

function drawDarkness() {

    if (
        state.powerOn
    ) {

        return;

    }


    ctx.fillStyle =
        "rgba(5,18,28,0.22)";


    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

}


// ============================================================
// HUD
// ============================================================

function drawHud() {

    ctx.fillStyle =
        "rgba(18,42,52,0.90)";


    ctx.fillRect(
        0,
        0,
        canvas.width,
        26
    );


    ctx.fillStyle =
        "#ffffff";


    ctx.font =
        '12px monospace';


    const minutes =
        Math.floor(
            state.time / 60
        );


    const seconds =
        Math.floor(
            state.time % 60
        )
        .toString()
        .padStart(
            2,
            "0"
        );


    ctx.fillText(
        "THEME "
        +
        (currentLevelIndex + 1)
        +
        "/"
        +
        LEVELS.length,
        10,
        17
    );


    ctx.fillText(
        "TIME "
        +
        minutes
        +
        ":"
        +
        seconds,
        125,
        17
    );


    ctx.fillText(
        "HP "
        +
        "♥".repeat(
            Math.max(
                0,
                state.hearts
            )
        ),
        250,
        17
    );


    ctx.fillText(
        "POWER "
        +
        (
            state.powerOn
            ?
            "ON"
            :
            "OFF"
        ),
        370,
        17
    );

}


// ============================================================
// 렌더링
// ============================================================

function render() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    drawFloor();

    drawWalls();

    drawFurniture();

    drawItems();


    // 어둠을 캐릭터보다 먼저 그려
    // 캐릭터가 검게 보이지 않도록 함.

    drawDarkness();


    ghosts.forEach(

        ghost =>
            drawGhost(
                ghost
            )

    );


    drawPlayer();


    drawHud();

}


// ============================================================
// 게임 업데이트
// ============================================================

function update(dt) {

    if (
        !state
        ||
        state.won
        ||
        state.lost
    ) {

        return;

    }


    state.time -=
        dt;


    if (
        state.time <= 0
    ) {

        state.time =
            0;


        state.lost =
            true;


        showGameOver(
            "제한 시간이 끝났어."
        );


        return;

    }


    updatePlayer(
        dt
    );


    updateGhosts(
        dt
    );


    updatePanels();

}


// ============================================================
// 게임 루프
// ============================================================

function gameLoop(now) {

    const dt =

        Math.min(

            (
                now - lastTime
            )
            /
            1000,

            0.05

        );


    lastTime =
        now;


    if (
        state
    ) {

        update(
            dt
        );


        render();

    }


    requestAnimationFrame(
        gameLoop
    );

}


// ============================================================
// 키보드 입력
// ============================================================

function handleKeyDown(event) {

    const key =
        event.key;


    const gameKeys = [

        "ArrowLeft",
        "ArrowRight",
        "ArrowUp",
        "ArrowDown",

        "w",
        "W",
        "a",
        "A",
        "s",
        "S",
        "d",
        "D",

        " ",
        "Enter"

    ];


    if (
        gameKeys.includes(
            key
        )
    ) {

        event.preventDefault();

    }


    keys[key] =
        true;


    if (
        key === " "
        ||
        key === "Enter"
    ) {

        interact();

    }


    if (
        key === "r"
        ||
        key === "R"
    ) {

        restartCurrentTheme();

    }

}


function handleKeyUp(event) {

    keys[event.key] =
        false;

}


document.addEventListener(
    "keydown",
    handleKeyDown,
    true
);


document.addEventListener(
    "keyup",
    handleKeyUp,
    true
);


canvas.addEventListener(
    "mousedown",
    () => {

        canvas.focus();


        setMessage(
            "✅ 게임 입력 활성화. 방향키 또는 WASD로 움직일 수 있어."
        );

    }
);


window.addEventListener(
    "blur",
    () => {

        keys = {};

    }
);


// ============================================================
// 시작
// ============================================================

window.addEventListener(
    "load",
    () => {

        startWholeGame();


        requestAnimationFrame(
            gameLoop
        );

    }
);


</script>


</body>
</html>
"""


components.html(
    game_html,
    height=1180,
    scrolling=False
)

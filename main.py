import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# Streamlit 설정
# ============================================================

st.set_page_config(
    page_title="MIDNIGHT HOSPITAL",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 MIDNIGHT HOSPITAL")
st.caption(
    "픽셀 병원 어드벤처 · 방향키/WASD 이동 · Space 상호작용 · R 현재 스테이지 재시작"
)


# ============================================================
# 게임 HTML
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
    overflow: hidden;
}

.wrap {
    padding: 12px;
}

.topbar {
    background: linear-gradient(180deg, #263f4a, #1d333d);
    color: white;
    border-radius: 16px;
    padding: 14px 18px;
    margin-bottom: 12px;
}

.title {
    font-size: 29px;
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
    padding: 10px;

    background: #edf4f6;

    border: 2px solid #9db3bb;
    border-radius: 16px;
}

#messageBar {
    min-height: 49px;

    margin-bottom: 8px;
    padding: 10px 13px;

    background: #fff3d5;

    border-left: 6px solid #d5ae45;
    border-radius: 10px;

    color: #594c29;

    font-size: 14px;
    line-height: 1.55;
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
    width: 285px;
    flex: 0 0 285px;
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

.stage-card {
    padding: 11px;

    background: #263f49;

    border-radius: 9px;

    color: white;

    font-size: 13px;
    line-height: 1.65;
}

.objective {
    padding: 10px;

    background: #e8f1fb;

    border-left: 5px solid #6b8eb4;
    border-radius: 9px;

    color: #304c61;

    font-size: 13px;
    line-height: 1.7;
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

    margin-top: 9px;

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

    background: rgba(5, 13, 19, 0.77);

    border-radius: 8px;

    z-index: 20;
}

.overlay-box {
    width: 470px;

    padding: 26px;

    background: white;

    border-radius: 18px;

    text-align: center;
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

                R : 현재 스테이지 처음부터 다시 시작


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

                <h3>🏥 현재 스테이지</h3>

                <div
                    class="stage-card"
                    id="stageBox">
                </div>

            </div>


            <div class="card">

                <h3>🎯 미션</h3>

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

                <h3 id="progressTitle">
                    🎒 인벤토리
                </h3>

                <div id="progressBox">
                </div>

            </div>


            <div class="card">

                <h3>📟 야간 기록</h3>

                <div id="logBox">
                </div>

            </div>


            <button onclick="restartStage()">

                🔄 현재 스테이지 다시 시작

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

ctx.imageSmoothingEnabled =
    false;


const messageBar =
    document.getElementById("messageBar");

const objectiveBox =
    document.getElementById("objectiveBox");

const statusBox =
    document.getElementById("statusBox");

const progressBox =
    document.getElementById("progressBox");

const progressTitle =
    document.getElementById("progressTitle");

const logBox =
    document.getElementById("logBox");

const stageBox =
    document.getElementById("stageBox");

const subtitleText =
    document.getElementById("subtitleText");

const overlay =
    document.getElementById("overlay");

const overlayBox =
    document.getElementById("overlayBox");


// ============================================================
// 맵 설정
// ============================================================

const TILE = 32;

const COLS = 33;

const ROWS = 20;


// ============================================================
// 스테이지 데이터
// ============================================================

const LEVELS = [


    // ========================================================
    // STAGE 1
    // 아이템 탐색 / 전력 복구
    // ========================================================

    {

        type:
            "collect",

        title:
            "STAGE 1 · 정전된 본관",

        story:
            "병원 본관 전체가 정전됐다. 필요한 부품을 찾아 비상 전력을 복구하고 엘리베이터를 작동시켜라.",

        time:
            420,

        palette: {

            floor1: "#b6c8ce",

            floor2: "#adc1c8",

            wall1: "#334f5b",

            wall2: "#4d6974",

            wall3: "#607d87"

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


    // ========================================================
    // STAGE 2
    // 단말기 순서 퍼즐
    // A → B → C
    // ========================================================

    {

        type:
            "switch",

        title:
            "STAGE 2 · 격리 연구동",

        story:
            "격리 시스템이 잠겨 있다. 연구동 곳곳의 세 제어 단말기를 정해진 순서대로 작동시켜 제독실을 열어라.",

        time:
            390,

        palette: {

            floor1: "#bacbbd",

            floor2: "#adbfaf",

            wall1: "#304c47",

            wall2: "#476a62",

            wall3: "#5c8379"

        },

        map: [

            "#################################",
            "#S...W....T.....................#",
            "#..#####...........#####........#",
            "#..#...#...........#...#........#",
            "#..#...#....A......#...#........#",
            "#..#...#####.......#...#####....#",
            "#..#...............#............#",
            "#..#####....#####..#....#####...#",
            "#......#....#...#..#....#...#...#",
            "#......#..B.#...#.......#...#...#",
            "#......#....#...#####...#...#...#",
            "#..H...#....#...........#...#...#",
            "#......#####......C.....#####...#",
            "#...............................#",
            "#....N...........Q..............#",
            "#...............................#",
            "#.................V.............#",
            "#.............................X.#",
            "#...............................#",
            "#################################"

        ]

    },


    // ========================================================
    // STAGE 3
    // 환자 구조
    // ========================================================

    {

        type:
            "rescue",

        title:
            "STAGE 3 · 옥상 연결 병동",

        story:
            "옥상 출구로 향하기 전 병동에 남아 있는 환자 세 명을 찾아야 한다. 모두 구조한 뒤 옥상으로 이동하라.",

        time:
            360,

        palette: {

            floor1: "#c7c3d4",

            floor2: "#b8b4c8",

            wall1: "#44425b",

            wall2: "#5b5875",

            wall3: "#716d8f"

        },

        map: [

            "#################################",
            "#S...W.....T....................#",
            "#..#####.............#####......#",
            "#..#...#.............#...#......#",
            "#..#p..#.......H.....#...#......#",
            "#..#...#####.........#...#####..#",
            "#..#.........................#..#",
            "#..#####....#####............#..#",
            "#......#....#...#....q.......#..#",
            "#......#....#...#............#..#",
            "#......#....#...#####........#..#",
            "#..H...#....#.................#.#",
            "#......#####........r...........#",
            "#...............................#",
            "#....N...........Q..............#",
            "#...............................#",
            "#.................V.............#",
            "#.............................R.#",
            "#...............................#",
            "#################################"

        ]

    }

];


// ============================================================
// 게임 변수
// ============================================================

let currentLevelIndex =
    0;

let player;

let state;

let keys =
    {};

let ghosts =
    [];

let invulnerable =
    0;

let lastTime =
    performance.now();


// ============================================================
// 현재 레벨
// ============================================================

function level() {

    return LEVELS[
        currentLevelIndex
    ];

}


// ============================================================
// 현재 맵에서 기호 찾기
// ============================================================

function findTile(symbol) {

    const currentMap =
        level().map;


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
                currentMap[y][x]
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
// 타일 중심
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
// 게임 시작
// ============================================================

function startWholeGame() {

    currentLevelIndex =
        0;


    startStage();

}


// ============================================================
// 스테이지 시작
// ============================================================

function startStage() {

    const start =
        findTile("S");


    // 맵 오류 처리

    if (
        !start
    ) {

        showFatalError(
            "시작 위치 S가 없습니다."
        );

        return;

    }


    player = {

        x:
            start.x * TILE + 1,

        y:
            start.y * TILE - 4,


        // 캐릭터는 크게 보임

        spriteW:
            30,

        spriteH:
            38,


        // 충돌은 발 주변만

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
            level().time,

        score:
            0,

        won:
            false,

        lost:
            false,

        logs:
            [],


        // STAGE 1

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


        // STAGE 2

        switchProgress:
            0,


        // STAGE 3

        rescuedP:
            false,

        rescuedQ:
            false,

        rescuedR:
            false

    };


    ghosts =
        createGhosts();


    invulnerable =
        0;


    state.logs.push(

        "현재 구역 진입 : "
        +
        level().title

    );


    setMessage(
        level().story
    );


    subtitleText.innerHTML =
        level().title
        +
        " · 방향키/WASD로 이동";


    overlay.style.display =
        "none";


    updatePanels();


    canvas.focus();

}


// ============================================================
// 현재 스테이지 다시 시작
// ============================================================

function restartStage() {

    startStage();

}


// ============================================================
// 그림자 NPC
// ============================================================

function createGhosts() {

    if (
        currentLevelIndex === 0
    ) {

        return [

            {

                x:
                    23 * TILE,

                y:
                    8 * TILE,

                w:
                    20,

                h:
                    20,

                speed:
                    42,

                color:
                    "#9277ff",

                path: [

                    tileCenter(23, 8),

                    tileCenter(29, 8),

                    tileCenter(29, 13),

                    tileCenter(23, 13)

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
                    21 * TILE,

                y:
                    6 * TILE,

                w:
                    20,

                h:
                    20,

                speed:
                    49,

                color:
                    "#4fd9ab",

                path: [

                    tileCenter(21, 6),

                    tileCenter(28, 6),

                    tileCenter(28, 12),

                    tileCenter(21, 12)

                ],

                pathIndex:
                    1

            },


            {

                x:
                    5 * TILE,

                y:
                    14 * TILE,

                w:
                    20,

                h:
                    20,

                speed:
                    42,

                color:
                    "#94e758",

                path: [

                    tileCenter(5, 14),

                    tileCenter(12, 14),

                    tileCenter(12, 18),

                    tileCenter(5, 18)

                ],

                pathIndex:
                    1

            }

        ];

    }


    return [

        {

            x:
                20 * TILE,

            y:
                6 * TILE,

            w:
                20,

            h:
                20,

            speed:
                52,

            color:
                "#ff74a9",

            path: [

                tileCenter(20, 6),

                tileCenter(29, 6),

                tileCenter(29, 12),

                tileCenter(20, 12)

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

            speed:
                46,

            color:
                "#be8dff",

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

    stageBox.innerHTML = `

        <b>
            ${level().title}
        </b>

        <br><br>

        ${level().story}

    `;


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

            <b>진행</b>

            ${currentLevelIndex + 1}
            /
            ${LEVELS.length}

        </div>


        <div class="stat">

            <b>남은 시간</b>

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

    `;


    // ========================================================
    // STAGE 1 UI
    // ========================================================

    if (
        level().type === "collect"
    ) {

        progressTitle.innerHTML =
            "🎒 인벤토리";


        let objective = "";


        if (
            !state.hasKeycard
        ) {

            objective =
                "① <b>출입카드</b>를 찾아.";

        }

        else if (
            !state.hasFuse
        ) {

            objective =
                "② <b>퓨즈</b>를 찾아.";

        }

        else if (
            !state.hasBattery
        ) {

            objective =
                "③ <b>비상 배터리</b>를 찾아.";

        }

        else if (
            !state.powerOn
        ) {

            objective =
                "④ <b>발전기</b>로 가서 전원을 복구해.";

        }

        else if (
            !state.hasMasterKey
        ) {

            objective =
                "⑤ <b>마스터 키</b>를 찾아.";

        }

        else {

            objective =
                "⑥ <b>엘리베이터</b>로 이동해 탈출해!";

        }


        objectiveBox.innerHTML =
            objective;


        progressBox.innerHTML = `

            <div class="item">

                ${
                    state.hasKeycard
                    ?
                    "✅ 출입카드"
                    :
                    "⬜ 출입카드"
                }

            </div>


            <div class="item">

                ${
                    state.hasFuse
                    ?
                    "✅ 퓨즈"
                    :
                    "⬜ 퓨즈"
                }

            </div>


            <div class="item">

                ${
                    state.hasBattery
                    ?
                    "✅ 비상 배터리"
                    :
                    "⬜ 비상 배터리"
                }

            </div>


            <div class="item">

                ${
                    state.powerOn
                    ?
                    "✅ 전원 복구"
                    :
                    "⬜ 전원 복구"
                }

            </div>


            <div class="item">

                ${
                    state.hasMasterKey
                    ?
                    "✅ 마스터 키"
                    :
                    "⬜ 마스터 키"
                }

            </div>

        `;

    }


    // ========================================================
    // STAGE 2 UI
    // ========================================================

    if (
        level().type === "switch"
    ) {

        progressTitle.innerHTML =
            "🖥️ 격리 시스템";


        const sequenceText = [

            "A",

            "A → B",

            "A → B → C",

            "완료"

        ][
            state.switchProgress
        ];


        objectiveBox.innerHTML = `

            연구동의 단말기를

            <br><br>

            <b>
            A → B → C
            </b>

            <br><br>

            순서로 작동시켜.

            <br>

            순서를 틀리면 시스템이 초기화돼.

        `;


        progressBox.innerHTML = `

            <div class="item">

                현재 진행 :
                <b>
                ${sequenceText}
                </b>

            </div>


            <div class="item">

                ${
                    state.switchProgress >= 1
                    ?
                    "✅ 단말기 A"
                    :
                    "⬜ 단말기 A"
                }

            </div>


            <div class="item">

                ${
                    state.switchProgress >= 2
                    ?
                    "✅ 단말기 B"
                    :
                    "⬜ 단말기 B"
                }

            </div>


            <div class="item">

                ${
                    state.switchProgress >= 3
                    ?
                    "✅ 단말기 C"
                    :
                    "⬜ 단말기 C"
                }

            </div>

        `;

    }


    // ========================================================
    // STAGE 3 UI
    // ========================================================

    if (
        level().type === "rescue"
    ) {

        progressTitle.innerHTML =
            "🩺 구조 현황";


        const rescueCount =

            Number(
                state.rescuedP
            )

            +

            Number(
                state.rescuedQ
            )

            +

            Number(
                state.rescuedR
            );


        objectiveBox.innerHTML = `

            병동에 남아 있는

            <b>환자 3명</b>을 찾아

            Space 키로 구조해.

            <br><br>

            모두 구조한 뒤

            <b>옥상 출구</b>로 이동해.

        `;


        progressBox.innerHTML = `

            <div class="item">

                구조 인원 :

                <b>
                    ${rescueCount} / 3명
                </b>

            </div>


            <div class="item">

                ${
                    state.rescuedP
                    ?
                    "✅ 환자 1 구조"
                    :
                    "⬜ 환자 1"
                }

            </div>


            <div class="item">

                ${
                    state.rescuedQ
                    ?
                    "✅ 환자 2 구조"
                    :
                    "⬜ 환자 2"
                }

            </div>


            <div class="item">

                ${
                    state.rescuedR
                    ?
                    "✅ 환자 3 구조"
                    :
                    "⬜ 환자 3"
                }

            </div>

        `;

    }


    logBox.innerHTML =

        state.logs

        .map(

            log =>
                `<div class="log">${log}</div>`

        )

        .join("");

}


// ============================================================
// 타일 충돌
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
        level().map[ty][tx];


    if (
        symbol === "#"
    ) {

        return true;

    }


    // STAGE 1 카드 보안문

    if (
        level().type === "collect"
        &&
        symbol === "C"
        &&
        !state.hasKeycard
    ) {

        return true;

    }


    // STAGE 1 전원문

    if (
        level().type === "collect"
        &&
        symbol === "D"
        &&
        !state.powerOn
    ) {

        return true;

    }


    // STAGE 2 출구

    if (
        level().type === "switch"
        &&
        symbol === "X"
        &&
        state.switchProgress < 3
    ) {

        return true;

    }


    // STAGE 3 옥상 출구

    if (
        level().type === "rescue"
        &&
        symbol === "R"
        &&
        rescueCount() < 3
    ) {

        return true;

    }


    return false;

}


// ============================================================
// 충돌 판정
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

    let dx =
        0;

    let dy =
        0;


    if (
        keys["ArrowLeft"]
        ||
        keys["a"]
        ||
        keys["A"]
    ) {

        dx -=
            1;

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

        dx +=
            1;

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

        dy -=
            1;

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

        dy +=
            1;

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

        dx *=
            0.707106;

        dy *=
            0.707106;

    }


    const moveX =
        dx
        *
        player.speed
        *
        dt;


    const moveY =
        dy
        *
        player.speed
        *
        dt;


    if (
        !collisionAt(
            player.x + moveX,
            player.y
        )
    ) {

        player.x +=
            moveX;

    }


    if (
        !collisionAt(
            player.x,
            player.y + moveY
        )
    ) {

        player.y +=
            moveY;

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
// 특정 오브젝트 근처 확인
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
// STAGE 3 구조 인원
// ============================================================

function rescueCount() {

    return (

        Number(
            state.rescuedP
        )

        +

        Number(
            state.rescuedQ
        )

        +

        Number(
            state.rescuedR
        )

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


    // ========================================================
    // STAGE 1
    // ========================================================

    if (
        level().type === "collect"
    ) {

        if (
            nearTile("K")
            &&
            !state.hasKeycard
        ) {

            state.hasKeycard =
                true;


            setMessage(
                "🪪 출입카드를 획득했어!"
            );


            addLog(
                "출입카드 확보."
            );


            return;

        }


        if (
            nearTile("F")
            &&
            !state.hasFuse
        ) {

            state.hasFuse =
                true;


            setMessage(
                "🧰 발전기용 퓨즈를 획득했어!"
            );


            addLog(
                "퓨즈 확보."
            );


            return;

        }


        if (
            nearTile("B")
            &&
            !state.hasBattery
        ) {

            state.hasBattery =
                true;


            setMessage(
                "🔋 비상 배터리를 획득했어!"
            );


            addLog(
                "배터리 확보."
            );


            return;

        }


        if (
            nearTile("P")
        ) {

            if (
                state.powerOn
            ) {

                setMessage(
                    "⚡ 발전기는 이미 작동하고 있어."
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


                setMessage(
                    "⚡ 비상 발전기가 작동했다! 병원 전원이 복구됐어."
                );


                addLog(
                    "병원 전력 복구."
                );


                return;

            }


            const missing =
                [];


            if (
                !state.hasFuse
            ) {

                missing.push(
                    "퓨즈"
                );

            }


            if (
                !state.hasBattery
            ) {

                missing.push(
                    "배터리"
                );

            }


            setMessage(

                "⚠️ 발전기 작동에 "
                +
                missing.join(", ")
                +
                "가 필요해."

            );


            return;

        }


        if (
            nearTile("M")
            &&
            !state.hasMasterKey
        ) {

            if (
                !state.powerOn
            ) {

                setMessage(
                    "🔒 전원이 복구되어야 마스터 키 보관함이 열린다."
                );


                return;

            }


            state.hasMasterKey =
                true;


            setMessage(
                "🗝️ 마스터 키를 획득했어!"
            );


            addLog(
                "마스터 키 확보."
            );


            return;

        }


        if (
            nearTile("E")
        ) {

            if (
                state.powerOn
                &&
                state.hasMasterKey
            ) {

                clearStage();

            }

            else {

                setMessage(
                    "🚪 엘리베이터가 아직 잠겨 있어."
                );

            }


            return;

        }

    }


    // ========================================================
    // STAGE 2
    // ========================================================

    if (
        level().type === "switch"
    ) {

        if (
            nearTile("A")
        ) {

            activateTerminal(
                "A",
                0
            );


            return;

        }


        if (
            nearTile("B")
        ) {

            activateTerminal(
                "B",
                1
            );


            return;

        }


        if (
            nearTile("C")
        ) {

            activateTerminal(
                "C",
                2
            );


            return;

        }


        if (
            nearTile("X")
        ) {

            if (
                state.switchProgress >= 3
            ) {

                clearStage();

            }

            else {

                setMessage(
                    "☣️ 제독실 출구가 잠겨 있어. A → B → C 순서로 단말기를 작동시켜야 해."
                );

            }


            return;

        }

    }


    // ========================================================
    // STAGE 3
    // ========================================================

    if (
        level().type === "rescue"
    ) {

        if (
            nearTile("p")
            &&
            !state.rescuedP
        ) {

            state.rescuedP =
                true;


            setMessage(
                "🩺 환자 1을 안전한 대기 구역으로 이동시켰어!"
            );


            addLog(
                "환자 1 구조."
            );


            return;

        }


        if (
            nearTile("q")
            &&
            !state.rescuedQ
        ) {

            state.rescuedQ =
                true;


            setMessage(
                "🩺 환자 2를 구조했어!"
            );


            addLog(
                "환자 2 구조."
            );


            return;

        }


        if (
            nearTile("r")
            &&
            !state.rescuedR
        ) {

            state.rescuedR =
                true;


            setMessage(
                "🩺 환자 3을 구조했어!"
            );


            addLog(
                "환자 3 구조."
            );


            return;

        }


        if (
            nearTile("R")
        ) {

            if (
                rescueCount() >= 3
            ) {

                clearStage();

            }

            else {

                setMessage(

                    "🚪 아직 병동에 환자가 남아 있어. 현재 "
                    +
                    rescueCount()
                    +
                    "/3명 구조 완료."

                );

            }


            return;

        }

    }


    setMessage(
        "주변에 지금 상호작용할 수 있는 물체가 없어."
    );

}


// ============================================================
// STAGE 2 단말기 퍼즐
// ============================================================

function activateTerminal(
    name,
    requiredProgress
) {

    // 이미 완료한 단말기

    if (
        state.switchProgress >
        requiredProgress
    ) {

        setMessage(
            "🖥️ 단말기 "
            +
            name
            +
            "은 이미 활성화되어 있어."
        );


        return;

    }


    // 정확한 순서

    if (
        state.switchProgress ===
        requiredProgress
    ) {

        state.switchProgress +=
            1;


        setMessage(

            "✅ 단말기 "
            +
            name
            +
            " 활성화 성공!"

        );


        addLog(

            "격리 단말기 "
            +
            name
            +
            " 활성화."

        );


        if (
            state.switchProgress === 3
        ) {

            setMessage(
                "✅ A → B → C 연결 완료! 제독실 출구가 열렸다."
            );


            addLog(
                "격리 시스템 해제."
            );

        }


        return;

    }


    // 순서를 틀림

    state.switchProgress =
        0;


    state.time =
        Math.max(
            0,
            state.time - 20
        );


    setMessage(

        "⚠️ 순서가 틀렸어! 격리 시스템이 초기화되고 시간 -20초. 다시 A부터 시작해야 해."

    );


    addLog(
        "단말기 순서 오류 → 시스템 초기화."
    );

}


// ============================================================
// 스테이지 클리어
// ============================================================

function clearStage() {

    state.won =
        true;


    if (
        currentLevelIndex
        <
        LEVELS.length - 1
    ) {

        const nextLevel =
            LEVELS[
                currentLevelIndex + 1
            ];


        overlayBox.innerHTML = `

            <div class="overlay-title">

                STAGE CLEAR

            </div>


            <div class="overlay-text">

                <b>
                    ${level().title}
                </b>

                완료!

                <br><br>

                다음 구역으로 이동합니다.

                <br><br>

                <b>
                    ${nextLevel.title}
                </b>

                <br><br>

                ${nextLevel.story}

            </div>


            <button onclick="nextStage()">

                다음 스테이지 →

            </button>

        `;


        overlay.style.display =
            "flex";


        return;

    }


    overlayBox.innerHTML = `

        <div class="overlay-title">

            HOSPITAL ESCAPED!

        </div>


        <div class="overlay-text">

            세 개의 병원 구역을 모두 통과했어!

            <br><br>

            정전된 본관에서는 전력을 복구하고,

            <br>

            연구동에서는 격리 시스템을 해제하고,

            <br>

            마지막 병동에서는 남아 있던 환자들을 모두 구조했어.

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
// 다음 스테이지
// ============================================================

function nextStage() {

    currentLevelIndex +=
        1;


    startStage();

}


// ============================================================
// 오류 화면
// ============================================================

function showFatalError(text) {

    overlayBox.innerHTML = `

        <div class="overlay-title">

            MAP ERROR

        </div>


        <div class="overlay-text">

            ${text}

        </div>


        <button onclick="startWholeGame()">

            다시 불러오기

        </button>

    `;


    overlay.style.display =
        "flex";

}


// ============================================================
// 그림자 이동
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

            const target =
                ghost.path[
                    ghost.pathIndex
                ];


            const cx =
                ghost.x
                +
                ghost.w / 2;


            const cy =
                ghost.y
                +
                ghost.h / 2;


            const dx =
                target.x - cx;


            const dy =
                target.y - cy;


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
                        start.x
                        *
                        TILE
                        +
                        1;


                    player.y =
                        start.y
                        *
                        TILE
                        -
                        4;


                    setMessage(
                        "👻 그림자에게 닿았어! 체력 -1"
                    );


                    addLog(
                        "그림자와 충돌."
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

            현재 스테이지부터 다시 도전할 수 있어.

        </div>


        <button onclick="restartStage()">

            다시 도전

        </button>

    `;


    overlay.style.display =
        "flex";

}


// ============================================================
// 방향 버튼
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
// 픽셀 사각형
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
// 이름표
// ============================================================

function drawLabel(
    text,
    centerX,
    y
) {

    ctx.save();


    ctx.font =
        '9px "Malgun Gothic", sans-serif';


    ctx.textAlign =
        "center";


    ctx.textBaseline =
        "middle";


    const width =
        Math.min(
            ctx.measureText(text).width + 8,
            78
        );


    rect(

        centerX - width / 2,

        y - 7,

        width,

        13,

        "rgba(18,34,42,0.82)"

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
// 바닥
// ============================================================

function drawFloor() {

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
                level().map[y][x]
                !==
                "#"
            ) {

                const floor =

                    (
                        x + y
                    )
                    %
                    2
                    ===
                    0

                    ?

                    level().palette.floor1

                    :

                    level().palette.floor2;


                rect(

                    x * TILE,

                    y * TILE,

                    TILE,

                    TILE,

                    floor

                );


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
                level().map[y][x]
                ===
                "#"
            ) {

                rect(

                    x * TILE,

                    y * TILE,

                    TILE,

                    TILE,

                    level().palette.wall1

                );


                rect(

                    x * TILE + 3,

                    y * TILE + 3,

                    TILE - 6,

                    TILE - 6,

                    level().palette.wall2

                );


                rect(

                    x * TILE + 6,

                    y * TILE + 6,

                    TILE - 12,

                    TILE - 12,

                    level().palette.wall3

                );

            }

        }

    }

}


// ============================================================
// 공통 병원 장식
// ============================================================

function drawFurniture() {

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
                level().map[y][x];


            const px =
                x * TILE;


            const py =
                y * TILE;


            // 창문

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


                drawLabel(
                    "창문",
                    px + 16,
                    py + 28
                );

            }


            // 데스크

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


                drawLabel(
                    "안내 데스크",
                    px + 16,
                    py + 28
                );

            }


            // 병원 침대

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


                drawLabel(
                    "병원 침대",
                    px + 16,
                    py + 28
                );

            }


            // 간호 스테이션

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


                drawLabel(
                    "간호 스테이션",
                    px + 16,
                    py + 28
                );

            }


            // 휠체어

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


                drawLabel(
                    "휠체어",
                    px + 16,
                    py + 28
                );

            }


            // 자판기

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


                drawLabel(
                    "자판기",
                    px + 16,
                    py + 29
                );

            }

        }

    }

}


// ============================================================
// STAGE 1 오브젝트
// ============================================================

function drawStage1Objects() {

    if (
        level().type !== "collect"
    ) {

        return;

    }


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
                level().map[y][x];


            const px =
                x * TILE;


            const py =
                y * TILE;


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


                drawLabel(
                    "출입카드",
                    px + 16,
                    py + 25
                );

            }


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


                drawLabel(
                    "퓨즈",
                    px + 16,
                    py + 27
                );

            }


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


                drawLabel(
                    "비상 배터리",
                    px + 16,
                    py + 28
                );

            }


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


                drawLabel(
                    "발전기",
                    px + 16,
                    py + 29
                );

            }


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


                drawLabel(
                    "마스터 키",
                    px + 16,
                    py + 25
                );

            }


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


                drawLabel(
                    "보안문",
                    px + 16,
                    py + 29
                );

            }


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


                drawLabel(
                    "전원문",
                    px + 16,
                    py + 29
                );

            }


            if (
                symbol === "E"
            ) {

                drawExitDoor(
                    px,
                    py,
                    "엘리베이터",
                    state.powerOn
                    &&
                    state.hasMasterKey
                );

            }

        }

    }

}


// ============================================================
// STAGE 2 오브젝트
// ============================================================

function drawStage2Objects() {

    if (
        level().type !== "switch"
    ) {

        return;

    }


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
                level().map[y][x];


            const px =
                x * TILE;


            const py =
                y * TILE;


            if (
                symbol === "A"
            ) {

                drawTerminal(
                    px,
                    py,
                    "단말기 A",
                    state.switchProgress >= 1,
                    "#4d9cff"
                );

            }


            if (
                symbol === "B"
            ) {

                drawTerminal(
                    px,
                    py,
                    "단말기 B",
                    state.switchProgress >= 2,
                    "#f0c44d"
                );

            }


            if (
                symbol === "C"
            ) {

                drawTerminal(
                    px,
                    py,
                    "단말기 C",
                    state.switchProgress >= 3,
                    "#de6ca5"
                );

            }


            if (
                symbol === "X"
            ) {

                drawExitDoor(
                    px,
                    py,
                    "제독실 출구",
                    state.switchProgress >= 3
                );

            }

        }

    }

}


// ============================================================
// 단말기
// ============================================================

function drawTerminal(
    px,
    py,
    label,
    active,
    accent
) {

    rect(
        px + 6,
        py + 3,
        20,
        20,
        "#344b53"
    );


    rect(
        px + 9,
        py + 6,
        14,
        9,
        active
        ?
        "#7cef94"
        :
        accent
    );


    rect(
        px + 10,
        py + 18,
        4,
        3,
        "#cbd7da"
    );


    rect(
        px + 17,
        py + 18,
        4,
        3,
        "#cbd7da"
    );


    drawLabel(
        label,
        px + 16,
        py + 29
    );

}


// ============================================================
// STAGE 3 오브젝트
// ============================================================

function drawStage3Objects() {

    if (
        level().type !== "rescue"
    ) {

        return;

    }


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
                level().map[y][x];


            const px =
                x * TILE;


            const py =
                y * TILE;


            if (
                symbol === "p"
                &&
                !state.rescuedP
            ) {

                drawPatient(
                    px,
                    py,
                    "환자 1",
                    "#77b8e8"
                );

            }


            if (
                symbol === "q"
                &&
                !state.rescuedQ
            ) {

                drawPatient(
                    px,
                    py,
                    "환자 2",
                    "#83c985"
                );

            }


            if (
                symbol === "r"
                &&
                !state.rescuedR
            ) {

                drawPatient(
                    px,
                    py,
                    "환자 3",
                    "#e5a26c"
                );

            }


            if (
                symbol === "R"
            ) {

                drawExitDoor(
                    px,
                    py,
                    "옥상 출구",
                    rescueCount() >= 3
                );

            }

        }

    }

}


// ============================================================
// 환자 캐릭터
// ============================================================

function drawPatient(
    px,
    py,
    label,
    clothes
) {

    // 머리

    rect(
        px + 11,
        py + 3,
        10,
        5,
        "#544038"
    );


    // 얼굴

    rect(
        px + 12,
        py + 7,
        8,
        7,
        "#efc3a5"
    );


    // 눈

    rect(
        px + 13,
        py + 9,
        1,
        1,
        "#222"
    );

    rect(
        px + 18,
        py + 9,
        1,
        1,
        "#222"
    );


    // 환자복

    rect(
        px + 9,
        py + 14,
        14,
        9,
        clothes
    );


    drawLabel(
        label,
        px + 16,
        py + 29
    );

}


// ============================================================
// 출구
// ============================================================

function drawExitDoor(
    px,
    py,
    label,
    open
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
        open
        ?
        "#6fe484"
        :
        "#d45f68"
    );


    drawLabel(
        label,
        px + 16,
        py + 29
    );

}


// ============================================================
// 플레이어
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


    // 그림자

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


    // 머리

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


    // 다리

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

}


// ============================================================
// 그림자
// ============================================================

function drawGhost(
    ghost
) {

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
// 어둠 효과
// ============================================================

function drawDarkness() {

    let alpha =
        0.18;


    if (
        currentLevelIndex === 0
    ) {

        alpha =
            state.powerOn
            ?
            0.04
            :
            0.23;

    }


    if (
        currentLevelIndex === 1
    ) {

        alpha =
            0.10;

    }


    if (
        currentLevelIndex === 2
    ) {

        alpha =
            0.13;

    }


    ctx.fillStyle =
        "rgba(5,18,28,"
        +
        alpha
        +
        ")";


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
        "12px monospace";


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
        "STAGE "
        +
        (currentLevelIndex + 1)
        +
        "/3",
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


    drawStage1Objects();

    drawStage2Objects();

    drawStage3Objects();


    // 캐릭터보다 먼저 어둠 표시

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
// 업데이트
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
                now
                -
                lastTime
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

function handleKeyDown(
    event
) {

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

        restartStage();

    }

}


function handleKeyUp(
    event
) {

    keys[
        event.key
    ] =
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
            "✅ 게임 입력 활성화. 방향키 또는 WASD로 움직여."
        );

    }
);


window.addEventListener(
    "blur",
    () => {

        keys =
            {};

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
    height=1190,
    scrolling=False
)

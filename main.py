import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="MIDNIGHT HOSPITAL",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 MIDNIGHT HOSPITAL")
st.caption(
    "픽셀 병원 어드벤처 · 방향키/WASD 이동 · Shift 달리기 · Space 상호작용/숨기 · R 현재 스테이지 재시작"
)

game_html = r'''
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

    font-family:
        Arial,
        "Malgun Gothic",
        sans-serif;

    overflow: hidden;
}

.wrap {
    padding: 12px;
}

.topbar {
    background:
        linear-gradient(
            180deg,
            #263f4a,
            #1d333d
        );

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
    min-height: 50px;

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
    width: 290px;
    flex: 0 0 290px;
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

.stat,
.item {
    margin-bottom: 7px;
    font-size: 13px;
}

.item {
    padding: 7px 9px;

    background: #edf4f6;

    border-radius: 8px;
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

    grid-template-columns:
        46px
        46px
        46px;

    grid-template-rows:
        42px
        42px
        42px;

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

    background:
        rgba(
            5,
            13,
            19,
            0.78
        );

    border-radius: 8px;

    z-index: 20;
}

.overlay-box {
    width: 480px;

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

.choice-row {
    display: flex;

    gap: 10px;
}

.choice-row button {
    flex: 1;
}

.small {
    margin-top: 8px;

    color: #67808a;

    font-size: 12px;
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

                <b>조작법</b>

                <br>

                방향키 / WASD : 이동

                <br>

                Shift + 이동 : 달리기
                (스태미나 사용)

                <br>

                Space / Enter :
                상호작용 · 숨기/나오기 · 미니게임 판정

                <br>

                R :
                현재 스테이지 처음부터 다시 시작


                <div class="dpad">

                    <button class="empty">
                        .
                    </button>

                    <button
                        onmousedown="pressDirection('ArrowUp')"
                        onmouseup="releaseDirection('ArrowUp')"
                        onmouseleave="releaseDirection('ArrowUp')">
                        ↑
                    </button>

                    <button class="empty">
                        .
                    </button>


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


                    <button class="empty">
                        .
                    </button>


                    <button
                        onmousedown="pressDirection('ArrowDown')"
                        onmouseup="releaseDirection('ArrowDown')"
                        onmouseleave="releaseDirection('ArrowDown')">
                        ↓
                    </button>


                    <button class="empty">
                        .
                    </button>

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

                <h3>
                    🏥 현재 스테이지
                </h3>

                <div
                    class="stage-card"
                    id="stageBox">
                </div>

            </div>


            <div class="card">

                <h3>
                    🎯 미션
                </h3>

                <div
                    class="objective"
                    id="objectiveBox">
                </div>

            </div>


            <div class="card">

                <h3>
                    📊 상태
                </h3>

                <div id="statusBox">
                </div>

            </div>


            <div class="card">

                <h3 id="progressTitle">
                    🎒 진행
                </h3>

                <div id="progressBox">
                </div>

            </div>


            <div class="card">

                <h3>
                    📟 야간 기록
                </h3>

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
// 기본 맵 설정
// ============================================================

const TILE =
    32;

const COLS =
    33;

const ROWS =
    20;


// ============================================================
// 스테이지 데이터
// ============================================================

const LEVELS = [


    // ========================================================
    // STAGE 1
    // 아이템 + 발전기 + 추격전
    // ========================================================

    {

        type:
            "collect",

        title:
            "STAGE 1 · 정전된 본관",

        story:
            "본관 전체가 정전됐다. 부품을 찾아 발전기를 복구한 뒤, 추격을 피해 엘리베이터로 탈출하라.",

        time:
            430,

        palette: {

            floor1:
                "#b6c8ce",

            floor2:
                "#adc1c8",

            wall1:
                "#334f5b",

            wall2:
                "#4d6974",

            wall3:
                "#607d87"

        },

        map: [

            "#################################",
            "#S....W..h.T.....#.............E#",
            "#......######....#....Z.........#",
            "#......#....#....#....H....G....#",
            "#......#.K..#.........H.........#",
            "#......#....#####...............#",
            "#......####..............######.#",
            "#....C........F.................#",
            "#.........................h.....#",
            "#..B..............######........#",
            "#.................#....#........#",
            "#.....G...........#....#........#",
            "#.P...............#....#......D.#",
            "#.................#....#........#",
            "#.....######......#....######...#",
            "#.....#....#......#.............#",
            "#..N..#....#..M...#.......Q.....#",
            "#.....######................V...#",
            "#...............................#",
            "#################################"

        ],

        records: [

            {

                x:
                    12,

                y:
                    8,

                text:
                    "기록 1: 정전 직전 자동문 제어기에 이상 신호가 남아 있다."

            },

            {

                x:
                    26,

                y:
                    15,

                text:
                    "기록 2: 야간 직원이 발전기실에서 반복되는 경보음을 들었다."

            }

        ]

    },


    // ========================================================
    // STAGE 2
    // 랜덤 단말기 순서 퍼즐
    // ========================================================

    {

        type:
            "switch",

        title:
            "STAGE 2 · 격리 연구동",

        story:
            "격리 시스템이 잠겼다. 연구 메모나 CCTV에서 단말기 순서를 확인하고 올바른 순서로 제어 단말기를 작동시켜라.",

        time:
            400,

        palette: {

            floor1:
                "#bacbbd",

            floor2:
                "#adbfaf",

            wall1:
                "#304c47",

            wall2:
                "#476a62",

            wall3:
                "#5c8379"

        },

        map: [

            "#################################",
            "#S...W..h.T.....................#",
            "#..#####...........#####........#",
            "#..#...#.....Z.....#...#........#",
            "#..#...#....A......#...#........#",
            "#..#...#####.......#...#####....#",
            "#..#............L..#............#",
            "#..#####....#####..#....#####...#",
            "#......#....#...#..#....#...#...#",
            "#......#..B.#...#.......#...#...#",
            "#..G...#....#...#####...#...#...#",
            "#..H...#....#...........#...#...#",
            "#......#####......C.....#####...#",
            "#.........................h.....#",
            "#....N...........Q..............#",
            "#...............................#",
            "#.................V.............#",
            "#.............................X.#",
            "#...............................#",
            "#################################"

        ],

        records: [

            {

                x:
                    27,

                y:
                    4,

                text:
                    "기록 3: 격리 단말기의 순서는 매 야간 점검 때 무작위로 재설정된다."

            },

            {

                x:
                    6,

                y:
                    17,

                text:
                    "기록 4: 잘못된 단말기 입력은 시스템을 초기화한다."

            }

        ]

    },


    // ========================================================
    // STAGE 3
    // 환자 위치 랜덤 + 구조 미션
    // ========================================================

    {

        type:
            "rescue",

        title:
            "STAGE 3 · 옥상 연결 병동",

        story:
            "옥상 출구로 향하기 전에 병동에 남은 환자 3명을 찾아 구조하라. 환자 위치는 매번 달라진다.",

        time:
            370,

        palette: {

            floor1:
                "#c7c3d4",

            floor2:
                "#b8b4c8",

            wall1:
                "#44425b",

            wall2:
                "#5b5875",

            wall3:
                "#716d8f"

        },

        map: [

            "#################################",
            "#S...W..h..T....................#",
            "#..#####.............#####......#",
            "#..#...#......Z......#...#......#",
            "#..#...#.......H.....#...#......#",
            "#..#...#####.........#...#####..#",
            "#..#.........................#..#",
            "#..#####....#####............#..#",
            "#......#....#...#............#..#",
            "#......#....#...#............#..#",
            "#...G..#....#...#####........#..#",
            "#..H...#....#.................#.#",
            "#......#####....................#",
            "#.........................h.....#",
            "#....N...........Q..............#",
            "#...............................#",
            "#.................V.............#",
            "#.............................R.#",
            "#...............................#",
            "#################################"

        ],

        patientCandidates: [

            {
                x:
                    5,

                y:
                    4
            },

            {
                x:
                    14,

                y:
                    6
            },

            {
                x:
                    24,

                y:
                    7
            },

            {
                x:
                    11,

                y:
                    13
            },

            {
                x:
                    20,

                y:
                    15
            },

            {
                x:
                    27,

                y:
                    11
            }

        ],

        records: [

            {

                x:
                    8,

                y:
                    16,

                text:
                    "기록 5: 옥상 통로는 모든 병동 인원이 확인된 뒤에만 개방된다."

            },

            {

                x:
                    28,

                y:
                    5,

                text:
                    "기록 6: 야간 대피 규정에는 환자 확인 절차가 우선이라고 적혀 있다."

            }

        ]

    }

];


// ============================================================
// 게임 변수
// ============================================================

let currentLevelIndex =
    0;

let player =
    null;

let state =
    null;

let keys =
    {};

let ghosts =
    [];

let invulnerable =
    0;

let lastTime =
    performance.now();

let meta =
    null;


// ============================================================
// 현재 스테이지
// ============================================================

function level() {

    return LEVELS[
        currentLevelIndex
    ];

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
// 타일 찾기
// ============================================================

function findTile(
    symbol
) {

    const map =
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
                map[y][x]
                ===
                symbol
            ) {

                return {

                    x:
                        x,

                    y:
                        y

                };

            }

        }

    }


    return null;

}


// ============================================================
// 배열 섞기
// ============================================================

function shuffled(
    array
) {

    const result =
        [...array];


    for (
        let i =
            result.length - 1;

        i > 0;

        i--
    ) {

        const j =
            Math.floor(
                Math.random()
                *
                (i + 1)
            );


        const temp =
            result[i];


        result[i] =
            result[j];


        result[j] =
            temp;

    }


    return result;

}


// ============================================================
// 전체 게임 시작
// ============================================================

function startWholeGame() {

    meta = {

        totalRecords:
            0,

        stageResults:
            [],

        allPatientsRescued:
            false

    };


    currentLevelIndex =
        0;


    startStage();

}


// ============================================================
// 스테이지 초기화
// ============================================================

function startStage() {

    const start =
        findTile("S");


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

        stamina:
            100,

        score:
            0,


        won:
            false,

        lost:
            false,


        logs:
            [],


        hidden:
            false,

        hideSeconds:
            0,


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

        sequence:
            shuffled(
                [
                    "A",
                    "B",
                    "C"
                ]
            ),

        sequenceKnown:
            false,


        // STAGE 3

        patients:
            [],


        // 수집 기록

        records:
            level().records.map(

                (record, index) => ({

                    ...record,

                    id:
                        index,

                    collected:
                        false

                })

            ),


        // CCTV

        cctvTimer:
            0,

        recordRevealTimer:
            0,


        // 추격전

        chaseTimer:
            0,


        // 발전기 미니게임

        miniGame:
            null,


        // 선택형 이벤트

        choiceOpen:
            false,

        choiceTriggered:
            false,

        choiceTimer:
            32
            +
            Math.random()
            *
            18,


        // 랜덤 이벤트

        eventTimer:
            18
            +
            Math.random()
            *
            15,

        event: {

            blackout:
                0,

            enemyBoost:
                0,

            alarm:
                0

        },


        // 임시 봉쇄

        lockedGate:
            null

    };


    // --------------------------------------------------------
    // 3스테이지 환자 랜덤 배치
    // --------------------------------------------------------

    if (
        level().type
        ===
        "rescue"
    ) {

        const chosen =
            shuffled(
                level().patientCandidates
            )
            .slice(
                0,
                3
            );


        state.patients =
            chosen.map(

                (position, index) => ({

                    id:
                        index + 1,

                    x:
                        position.x,

                    y:
                        position.y,

                    rescued:
                        false

                })

            );

    }


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
        " · Shift 달리기 · Space 상호작용";


    overlay.style.display =
        "none";


    updatePanels();


    canvas.focus();

}


// ============================================================
// 현재 스테이지 재시작
// ============================================================

function restartStage() {

    startStage();

}


// ============================================================
// 그림자 생성
// ============================================================

function createGhosts() {

    if (
        currentLevelIndex
        ===
        0
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

                    tileCenter(
                        23,
                        8
                    ),

                    tileCenter(
                        29,
                        8
                    ),

                    tileCenter(
                        29,
                        13
                    ),

                    tileCenter(
                        23,
                        13
                    )

                ],

                pathIndex:
                    1

            }

        ];

    }


    if (
        currentLevelIndex
        ===
        1
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

                    tileCenter(
                        21,
                        6
                    ),

                    tileCenter(
                        28,
                        6
                    ),

                    tileCenter(
                        28,
                        12
                    ),

                    tileCenter(
                        21,
                        12
                    )

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

                    tileCenter(
                        5,
                        14
                    ),

                    tileCenter(
                        12,
                        14
                    ),

                    tileCenter(
                        12,
                        18
                    ),

                    tileCenter(
                        5,
                        18
                    )

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

                tileCenter(
                    20,
                    6
                ),

                tileCenter(
                    29,
                    6
                ),

                tileCenter(
                    29,
                    12
                ),

                tileCenter(
                    20,
                    12
                )

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

                tileCenter(
                    8,
                    14
                ),

                tileCenter(
                    17,
                    14
                ),

                tileCenter(
                    17,
                    18
                ),

                tileCenter(
                    8,
                    18
                )

            ],

            pathIndex:
                1

        }

    ];

}


// ============================================================
// 메시지
// ============================================================

function setMessage(
    text
) {

    messageBar.innerHTML =
        text;

}


// ============================================================
// 로그
// ============================================================

function addLog(
    text
) {

    state.logs.unshift(
        text
    );


    if (
        state.logs.length
        >
        7
    ) {

        state.logs.pop();

    }


    updatePanels();

}


// ============================================================
// 플레이어 중심
// ============================================================

function playerCenter() {

    return {

        x:
            player.x
            +
            15,

        y:
            player.y
            +
            23

    };

}


// ============================================================
// 위치와 가까운지
// ============================================================

function nearPos(
    x,
    y,
    distance = 42
) {

    const playerPosition =
        playerCenter();


    const target =
        tileCenter(
            x,
            y
        );


    return (

        Math.hypot(

            playerPosition.x
            -
            target.x,

            playerPosition.y
            -
            target.y

        )

        <=

        distance

    );

}


// ============================================================
// 특정 기호와 가까운지
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


    return nearPos(
        tile.x,
        tile.y,
        distance
    );

}


// ============================================================
// 게이트 위치
// ============================================================

function allGateTiles() {

    const result =
        [];


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
                "G"
            ) {

                result.push(
                    {
                        x:
                            x,

                        y:
                            y
                    }
                );

            }

        }

    }


    return result;

}


// ============================================================
// 환자 구조 수
// ============================================================

function rescueCount() {

    return state.patients.filter(

        patient =>
            patient.rescued

    ).length;

}


// ============================================================
// 현재 스테이지 기록 수
// ============================================================

function stageRecordCount() {

    return state.records.filter(

        record =>
            record.collected

    ).length;

}


// ============================================================
// UI 갱신
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
            3

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


        <div class="stat">

            <b>스태미나</b>

            ${Math.round(
                state.stamina
            )}
            / 100

        </div>


        <div class="stat">

            <b>상태</b>

            ${
                state.hidden
                ?
                "🫥 숨는 중"

                :

                state.chaseTimer > 0
                ?
                "🚨 추격 중"

                :

                "탐색 중"
            }

        </div>


        <div class="stat">

            <b>야간 기록</b>

            ${stageRecordCount()}
            /
            ${state.records.length}

        </div>

    `;


    // ========================================================
    // STAGE 1
    // ========================================================

    if (
        level().type
        ===
        "collect"
    ) {

        progressTitle.innerHTML =
            "🎒 인벤토리";


        let objective =
            "";


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
                "④ <b>발전기</b> 수리 미니게임을 성공시켜.";

        }

        else if (
            !state.hasMasterKey
        ) {

            objective =
                "⑤ 추격을 피하면서 <b>마스터 키</b>를 찾아.";

        }

        else {

            objective =
                "⑥ <b>엘리베이터</b>로 탈출해!";

        }


        objectiveBox.innerHTML =
            objective;


        progressBox.innerHTML = `

            <div class="item">

                ${
                    state.hasKeycard
                    ?
                    "✅"
                    :
                    "⬜"
                }

                출입카드

            </div>


            <div class="item">

                ${
                    state.hasFuse
                    ?
                    "✅"
                    :
                    "⬜"
                }

                퓨즈

            </div>


            <div class="item">

                ${
                    state.hasBattery
                    ?
                    "✅"
                    :
                    "⬜"
                }

                비상 배터리

            </div>


            <div class="item">

                ${
                    state.powerOn
                    ?
                    "✅"
                    :
                    "⬜"
                }

                발전기 복구

            </div>


            <div class="item">

                ${
                    state.hasMasterKey
                    ?
                    "✅"
                    :
                    "⬜"
                }

                마스터 키

            </div>

        `;

    }


    // ========================================================
    // STAGE 2
    // ========================================================

    else if (
        level().type
        ===
        "switch"
    ) {

        progressTitle.innerHTML =
            "🖥️ 격리 시스템";


        const shownSequence =

            state.sequenceKnown

            ?

            state.sequence.join(
                " → "
            )

            :

            "??? → ??? → ???";


        objectiveBox.innerHTML = `

            연구 메모 또는 CCTV로

            <b>
                단말기 순서
            </b>

            를 확인한 뒤 입력해.

            <br><br>

            확인된 순서:

            <b>
                ${shownSequence}
            </b>

        `;


        progressBox.innerHTML = `

            <div class="item">

                <b>
                    진행
                </b>

                ${state.switchProgress}
                / 3

            </div>


            <div class="item">

                순서를 틀리면

                <b>
                    시스템 초기화
                </b>

                +

                시간 -20초

            </div>

        `;

    }


    // ========================================================
    // STAGE 3
    // ========================================================

    else {

        progressTitle.innerHTML =
            "🩺 구조 현황";


        objectiveBox.innerHTML = `

            무작위 위치에 있는

            <b>
                환자 3명
            </b>

            을 모두 구조한 뒤

            옥상 출구로 이동해.

        `;


        progressBox.innerHTML = `

            <div class="item">

                <b>
                    구조 인원
                </b>

                ${rescueCount()}
                / 3

            </div>


            ${state.patients.map(

                patient => `

                    <div class="item">

                        ${
                            patient.rescued
                            ?
                            "✅"
                            :
                            "⬜"
                        }

                        환자 ${patient.id}

                    </div>

                `

            ).join("")}

        `;

    }


    logBox.innerHTML =

        state.logs.map(

            log =>
                `<div class="log">${log}</div>`

        ).join("");

}


// ============================================================
// 장애물
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
        symbol
        ===
        "#"
    ) {

        return true;

    }


    // STAGE 1 보안문

    if (
        level().type
        ===
        "collect"
        &&
        symbol
        ===
        "C"
        &&
        !state.hasKeycard
    ) {

        return true;

    }


    if (
        level().type
        ===
        "collect"
        &&
        symbol
        ===
        "D"
        &&
        !state.powerOn
    ) {

        return true;

    }


    // STAGE 2 출구

    if (
        level().type
        ===
        "switch"
        &&
        symbol
        ===
        "X"
        &&
        state.switchProgress < 3
    ) {

        return true;

    }


    // STAGE 3 옥상 출구

    if (
        level().type
        ===
        "rescue"
        &&
        symbol
        ===
        "R"
        &&
        rescueCount() < 3
    ) {

        return true;

    }


    // 랜덤 이벤트 임시 봉쇄

    if (
        state.lockedGate
        &&
        state.lockedGate.x
        ===
        tx
        &&
        state.lockedGate.y
        ===
        ty
    ) {

        return true;

    }


    return false;

}


// ============================================================
// 충돌
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
            x:
                left,

            y:
                top
        },

        {
            x:
                right,

            y:
                top
        },

        {
            x:
                left,

            y:
                bottom
        },

        {
            x:
                right,

            y:
                bottom
        }

    ];


    for (
        const point
        of
        points
    ) {

        const tx =
            Math.floor(
                point.x
                /
                TILE
            );


        const ty =
            Math.floor(
                point.y
                /
                TILE
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
// 플레이어 이동 + 스태미나
// ============================================================

function updatePlayer(
    dt
) {

    if (
        state.hidden
        ||
        state.miniGame
        ||
        state.choiceOpen
    ) {

        return;

    }


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


    // --------------------------------------------------------
    // Shift 달리기
    // --------------------------------------------------------

    const running =

        (
            keys["Shift"]
            ||
            keys["ShiftLeft"]
            ||
            keys["ShiftRight"]
        )

        &&

        player.walking

        &&

        state.stamina > 0;


    let speed =
        player.speed;


    if (
        running
    ) {

        speed =
            245;


        state.stamina =
            Math.max(
                0,
                state.stamina
                -
                32
                *
                dt
            );

    }

    else {

        state.stamina =
            Math.min(
                100,
                state.stamina
                +
                18
                *
                dt
            );

    }


    const moveX =
        dx
        *
        speed
        *
        dt;


    const moveY =
        dy
        *
        speed
        *
        dt;


    if (
        !collisionAt(
            player.x
            +
            moveX,

            player.y
        )
    ) {

        player.x +=
            moveX;

    }


    if (
        !collisionAt(
            player.x,

            player.y
            +
            moveY
        )
    ) {

        player.y +=
            moveY;

    }


    // 걷기 애니메이션

    if (
        player.walking
    ) {

        player.walkTimer +=
            dt;


        if (
            player.walkTimer
            >
            0.14
        ) {

            player.walkFrame =

                1
                -
                player.walkFrame;


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
// 가장 가까운 특정 기호
// ============================================================

function findNearestSymbol(
    symbol,
    distance
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
                level().map[y][x]
                ===
                symbol
                &&
                nearPos(
                    x,
                    y,
                    distance
                )
            ) {

                return {

                    x:
                        x,

                    y:
                        y

                };

            }

        }

    }


    return null;

}


// ============================================================
// 상호작용
// ============================================================

function interact() {

    canvas.focus();


    if (
        !state
        ||
        state.won
        ||
        state.lost
        ||
        state.choiceOpen
    ) {

        return;

    }


    // --------------------------------------------------------
    // 미니게임 중 Space
    // --------------------------------------------------------

    if (
        state.miniGame
    ) {

        finishMiniGame();

        return;

    }


    // --------------------------------------------------------
    // 숨는 중이면 밖으로
    // --------------------------------------------------------

    if (
        state.hidden
    ) {

        state.hidden =
            false;


        state.hideSeconds =
            0;


        setMessage(
            "숨는 곳에서 나왔어."
        );


        return;

    }


    // --------------------------------------------------------
    // 숨는 곳
    // --------------------------------------------------------

    const hideSpot =
        findNearestSymbol(
            "h",
            42
        );


    if (
        hideSpot
    ) {

        state.hidden =
            true;


        state.hideSeconds =
            0;


        setMessage(
            "🫥 숨는 곳에 들어왔어. 6초가 지나면 제한시간이 더 빠르게 줄어들어."
        );


        return;

    }


    // --------------------------------------------------------
    // 야간 기록
    // --------------------------------------------------------

    const record =
        state.records.find(

            item =>

                !item.collected
                &&
                nearPos(
                    item.x,
                    item.y,
                    42
                )

        );


    if (
        record
    ) {

        record.collected =
            true;


        meta.totalRecords +=
            1;


        state.score +=
            120;


        setMessage(

            "📄 야간 기록을 발견했어: "
            +
            record.text

        );


        addLog(
            "야간 기록 조각 확보."
        );


        return;

    }


    // --------------------------------------------------------
    // CCTV
    // --------------------------------------------------------

    const cctv =
        findTile(
            "Z"
        );


    if (
        cctv
        &&
        nearPos(
            cctv.x,
            cctv.y,
            42
        )
    ) {

        state.cctvTimer =
            12;


        state.recordRevealTimer =
            12;


        if (
            level().type
            ===
            "switch"
        ) {

            state.sequenceKnown =
                true;

        }


        setMessage(
            "📹 CCTV를 12초간 확인할 수 있어. 적·환자·기록 위치가 미니맵에 표시돼."
        );


        addLog(
            "CCTV 활성화."
        );


        return;

    }


    // --------------------------------------------------------
    // 연구 메모
    // --------------------------------------------------------

    if (
        level().type
        ===
        "switch"
    ) {

        const note =
            findTile(
                "L"
            );


        if (
            note
            &&
            nearPos(
                note.x,
                note.y,
                42
            )
        ) {

            state.sequenceKnown =
                true;


            setMessage(

                "📝 연구 메모: 단말기 순서는 "
                +
                state.sequence.join(
                    " → "
                )
                +
                " 이다."

            );


            addLog(
                "단말기 순서 확인."
            );


            return;

        }

    }


    // --------------------------------------------------------
    // 각 스테이지 상호작용
    // --------------------------------------------------------

    if (
        level().type
        ===
        "collect"
    ) {

        interactStage1();

    }

    else if (
        level().type
        ===
        "switch"
    ) {

        interactStage2();

    }

    else {

        interactStage3();

    }

}


// ============================================================
// STAGE 1
// ============================================================

function interactStage1() {

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


    // 발전기

    if (
        nearTile("P")
    ) {

        if (
            state.powerOn
        ) {

            setMessage(
                "⚡ 발전기는 이미 작동 중이야."
            );


            return;

        }


        if (
            state.hasFuse
            &&
            state.hasBattery
        ) {

            startGeneratorMiniGame();

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
            missing.join(
                ", "
            )
            +
            "가 필요해."

        );


        return;

    }


    // 마스터 키

    if (
        nearTile("M")
        &&
        !state.hasMasterKey
    ) {

        if (
            !state.powerOn
        ) {

            setMessage(
                "🔒 전원을 먼저 복구해야 해."
            );


            return;

        }


        state.hasMasterKey =
            true;


        setMessage(
            "🗝️ 마스터 키 획득! 추격이 끝났다면 엘리베이터로 이동해."
        );


        addLog(
            "마스터 키 확보."
        );


        return;

    }


    // 엘리베이터

    if (
        nearTile("E")
    ) {

        if (
            state.powerOn
            &&
            state.hasMasterKey
        ) {

            clearStage();

            return;

        }


        setMessage(
            "🚪 엘리베이터가 아직 잠겨 있어."
        );


        return;

    }


    setMessage(
        "주변에 지금 상호작용할 수 있는 물체가 없어."
    );

}


// ============================================================
// 발전기 타이밍 미니게임
// ============================================================

function startGeneratorMiniGame() {

    state.miniGame = {

        type:
            "timing",

        pos:
            0.05,

        dir:
            1

    };


    setMessage(
        "🛠️ 발전기 수리: 움직이는 표시가 초록 구간에 들어왔을 때 Space를 눌러!"
    );

}


// ============================================================
// 미니게임 판정
// ============================================================

function finishMiniGame() {

    const game =
        state.miniGame;


    if (
        !game
    ) {

        return;

    }


    // 성공

    if (
        game.pos >= 0.42
        &&
        game.pos <= 0.58
    ) {

        state.miniGame =
            null;


        state.powerOn =
            true;


        state.chaseTimer =
            20;


        state.score +=
            300;


        setMessage(
            "⚡ 발전기 복구 성공! 경보가 울리며 그림자가 20초 동안 추격한다!"
        );


        addLog(
            "발전기 복구 → 추격전 시작."
        );

    }

    // 실패

    else {

        state.miniGame =
            null;


        state.time =
            Math.max(
                0,
                state.time - 10
            );


        setMessage(
            "❌ 수리 타이밍 실패! 시간 -10초. 다시 시도해."
        );


        addLog(
            "발전기 수리 실패."
        );

    }

}


// ============================================================
// STAGE 2
// ============================================================

function interactStage2() {

    for (
        const name
        of
        [
            "A",
            "B",
            "C"
        ]
    ) {

        if (
            nearTile(
                name
            )
        ) {

            activateTerminal(
                name
            );


            return;

        }

    }


    if (
        nearTile("X")
    ) {

        if (
            state.switchProgress
            >=
            3
        ) {

            clearStage();

        }

        else {

            setMessage(
                "☣️ 제독실 출구가 잠겨 있어. 올바른 순서로 단말기를 활성화해야 해."
            );

        }


        return;

    }


    setMessage(
        "주변에 지금 상호작용할 수 있는 물체가 없어."
    );

}


// ============================================================
// 랜덤 순서 단말기
// ============================================================

function activateTerminal(
    name
) {

    const expected =
        state.sequence[
            state.switchProgress
        ];


    if (
        name
        ===
        expected
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
            "단말기 "
            +
            name
            +
            " 활성화."
        );


        if (
            state.switchProgress
            ===
            3
        ) {

            setMessage(
                "✅ 격리 시스템 해제! 제독실 출구가 열렸다."
            );


            addLog(
                "격리 시스템 해제."
            );

        }

    }

    else {

        state.switchProgress =
            0;


        state.time =
            Math.max(
                0,
                state.time - 20
            );


        setMessage(
            "⚠️ 잘못된 순서! 시스템 초기화 + 시간 -20초."
        );


        addLog(
            "단말기 순서 오류."
        );

    }

}


// ============================================================
// STAGE 3
// ============================================================

function interactStage3() {

    const patient =
        state.patients.find(

            person =>

                !person.rescued
                &&
                nearPos(
                    person.x,
                    person.y,
                    42
                )

        );


    if (
        patient
    ) {

        patient.rescued =
            true;


        state.score +=
            180;


        setMessage(
            "🩺 환자 "
            +
            patient.id
            +
            "을 안전 구역으로 안내했어!"
        );


        addLog(
            "환자 "
            +
            patient.id
            +
            " 구조."
        );


        if (
            rescueCount()
            ===
            3
        ) {

            meta.allPatientsRescued =
                true;


            setMessage(
                "✅ 환자 3명 모두 구조 완료! 옥상 출구가 열렸다."
            );

        }


        return;

    }


    if (
        nearTile("R")
    ) {

        if (
            rescueCount()
            ===
            3
        ) {

            clearStage();

        }

        else {

            setMessage(

                "🚪 아직 환자가 남아 있어. 현재 "
                +
                rescueCount()
                +
                "/3명 구조."

            );

        }


        return;

    }


    setMessage(
        "주변에 지금 상호작용할 수 있는 물체가 없어."
    );

}


// ============================================================
// 랜덤 이벤트
// ============================================================

function triggerRandomEvent() {

    const options = [

        "blackout",

        "boost",

        "alarm",

        "announcement",

        "lockdown"

    ];


    const randomEvent =

        options[
            Math.floor(
                Math.random()
                *
                options.length
            )
        ];


    // 정전

    if (
        randomEvent
        ===
        "blackout"
    ) {

        state.event.blackout =
            8;


        setMessage(
            "💡 랜덤 이벤트: 갑작스러운 정전! 8초 동안 시야가 어두워진다."
        );


        addLog(
            "랜덤 이벤트: 정전."
        );

    }


    // 적 속도 증가

    else if (
        randomEvent
        ===
        "boost"
    ) {

        state.event.enemyBoost =
            10;


        setMessage(
            "⚠️ 랜덤 이벤트: 그림자 움직임이 빨라졌다!"
        );


        addLog(
            "랜덤 이벤트: 그림자 속도 증가."
        );

    }


    // 경고등

    else if (
        randomEvent
        ===
        "alarm"
    ) {

        state.event.alarm =
            8;


        setMessage(
            "🚨 랜덤 이벤트: 비상 경고등이 점멸한다."
        );


        addLog(
            "랜덤 이벤트: 경고등."
        );

    }


    // 안내 방송

    else if (
        randomEvent
        ===
        "announcement"
    ) {

        const messages = [

            "📢 안내 방송: 동쪽 복도는 안전합니다. ...정말일까?",

            "📢 안내 방송: 모든 환자는 현재 위치에서 대기하십시오.",

            "📢 안내 방송: 옥상 출입구 점검 중입니다."

        ];


        setMessage(

            messages[
                Math.floor(
                    Math.random()
                    *
                    messages.length
                )
            ]

        );


        addLog(
            "랜덤 이벤트: 수상한 안내 방송."
        );

    }


    // 임시 봉쇄

    else {

        const gates =
            allGateTiles();


        if (
            gates.length
            >
            0
        ) {

            const selected =

                gates[
                    Math.floor(
                        Math.random()
                        *
                        gates.length
                    )
                ];


            state.lockedGate = {

                x:
                    selected.x,

                y:
                    selected.y,

                remaining:
                    8

            };


            setMessage(
                "🔒 랜덤 이벤트: 특정 복도가 8초 동안 임시 봉쇄됐다!"
            );


            addLog(
                "랜덤 이벤트: 임시 봉쇄."
            );

        }

    }


    state.eventTimer =

        18
        +
        Math.random()
        *
        18;

}


// ============================================================
// 선택형 이벤트
// ============================================================

function maybeShowChoiceEvent(
    dt
) {

    if (
        state.choiceTriggered
        ||
        state.choiceOpen
    ) {

        return;

    }


    state.choiceTimer -=
        dt;


    if (
        state.choiceTimer
        <=
        0
    ) {

        state.choiceTriggered =
            true;


        state.choiceOpen =
            true;


        overlayBox.innerHTML = `

            <div class="overlay-title">

                수상한 호출

            </div>


            <div class="overlay-text">

                멀리서 간호사실 호출음과

                왼쪽 복도에서 나는 소리가

                동시에 들린다.

                <br><br>

                어디를 먼저 확인할까?

            </div>


            <div class="choice-row">

                <button
                    onclick="chooseEvent('nurse')">

                    간호사실 확인

                </button>


                <button
                    onclick="chooseEvent('hall')">

                    왼쪽 복도 조사

                </button>

            </div>

        `;


        overlay.style.display =
            "flex";

    }

}


// ============================================================
// 선택 결과
// ============================================================

function chooseEvent(
    choice
) {

    state.choiceOpen =
        false;


    overlay.style.display =
        "none";


    // 시간 보상 + 적 강화

    if (
        choice
        ===
        "nurse"
    ) {

        state.time +=
            20;


        state.event.enemyBoost =
            Math.max(
                state.event.enemyBoost,
                10
            );


        setMessage(
            "☎️ 간호사실에서 비상 시계를 찾아 +20초. 대신 그림자가 10초간 빨라졌다."
        );


        addLog(
            "선택 이벤트: 시간 +20 / 적 속도 증가."
        );

    }


    // 기록 위치 확인 + 시간 손해

    else {

        state.recordRevealTimer =
            15;


        state.time =
            Math.max(
                0,
                state.time - 10
            );


        setMessage(
            "🔎 왼쪽 복도를 조사해 기록 위치가 15초간 미니맵에 표시된다. 대신 시간 -10초."
        );


        addLog(
            "선택 이벤트: 기록 위치 공개 / 시간 -10."
        );

    }

}


// ============================================================
// 랭크 계산
// ============================================================

function calculateRank() {

    const timeRatio =
        Math.max(
            0,
            state.time
            /
            level().time
        );


    const records =
        stageRecordCount();


    let points =

        state.hearts * 120

        +

        timeRatio * 480

        +

        records * 120;


    if (
        level().type
        ===
        "rescue"
    ) {

        points +=
            rescueCount()
            *
            60;

    }


    if (
        level().type
        ===
        "switch"
        &&
        state.switchProgress
        ===
        3
    ) {

        points +=
            120;

    }


    if (
        points
        >=
        950
    ) {

        return "S";

    }


    if (
        points
        >=
        760
    ) {

        return "A";

    }


    if (
        points
        >=
        560
    ) {

        return "B";

    }


    return "C";

}


// ============================================================
// 스테이지 클리어
// ============================================================

function clearStage() {

    state.won =
        true;


    const rank =
        calculateRank();


    meta.stageResults.push(

        {

            stage:
                currentLevelIndex + 1,

            rank:
                rank,

            records:
                stageRecordCount(),

            hearts:
                state.hearts,

            time:
                Math.floor(
                    state.time
                )

        }

    );


    if (
        currentLevelIndex
        <
        LEVELS.length - 1
    ) {

        const next =
            LEVELS[
                currentLevelIndex + 1
            ];


        overlayBox.innerHTML = `

            <div class="overlay-title">

                STAGE CLEAR · ${rank} RANK

            </div>


            <div class="overlay-text">

                <b>
                    ${level().title}
                </b>

                완료!

                <br><br>

                기록

                ${stageRecordCount()}
                /
                ${state.records.length}

                ·

                체력

                ${state.hearts}
                /4

                ·

                남은 시간

                ${Math.floor(
                    state.time
                )}
                초

                <br><br>

                다음 스테이지

                <br>

                <b>
                    ${next.title}
                </b>

                <br>

                ${next.story}

            </div>


            <button onclick="nextStage()">

                다음 스테이지 →

            </button>

        `;


        overlay.style.display =
            "flex";

    }

    else {

        showFinalEnding(
            rank
        );

    }

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
// 최종 엔딩 분기
// ============================================================

function showFinalEnding(
    lastRank
) {

    let endingTitle =
        "탈출 엔딩";


    let endingText =
        "세 구역을 통과해 병원에서 무사히 빠져나왔다.";


    // --------------------------------------------------------
    // 진실 엔딩
    // 기록 6개 전부 수집
    // --------------------------------------------------------

    if (
        meta.totalRecords
        >=
        6
    ) {

        endingTitle =
            "진실 엔딩";


        endingText =
            "야간 기록 6개를 모두 회수해 병원의 시스템 이상과 야간 사고 기록까지 확인한 뒤 탈출했다.";

    }


    // --------------------------------------------------------
    // 구조 엔딩
    // --------------------------------------------------------

    else if (
        meta.allPatientsRescued
        &&
        meta.totalRecords >= 3
    ) {

        endingTitle =
            "구조 엔딩";


        endingText =
            "병동의 환자들을 모두 구조하고 충분한 기록까지 확보한 뒤 옥상으로 탈출했다.";

    }


    const ranks =

        meta.stageResults
        .map(
            result =>
                result.rank
        )
        .concat(
            lastRank
        )
        .join(
            " · "
        );


    overlayBox.innerHTML = `

        <div class="overlay-title">

            ${endingTitle}

        </div>


        <div class="overlay-text">

            ${endingText}

            <br><br>

            <b>
                전체 야간 기록
            </b>

            ${meta.totalRecords}
            /6

            <br>

            <b>
                스테이지 랭크
            </b>

            ${ranks}

            <br><br>

            MIDNIGHT HOSPITAL COMPLETE

        </div>


        <button onclick="startWholeGame()">

            처음부터 다시 플레이

        </button>

    `;


    overlay.style.display =
        "flex";

}


// ============================================================
// GAME OVER
// ============================================================

function showGameOver(
    reason
) {

    overlayBox.innerHTML = `

        <div class="overlay-title">

            GAME OVER

        </div>


        <div class="overlay-text">

            ${reason}

            <br><br>

            현재 스테이지부터

            다시 도전할 수 있어.

        </div>


        <button onclick="restartStage()">

            다시 도전

        </button>

    `;


    overlay.style.display =
        "flex";

}


// ============================================================
// 치명적인 오류
// ============================================================

function showFatalError(
    text
) {

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

function updateGhosts(
    dt
) {

    if (
        invulnerable
        >
        0
    ) {

        invulnerable -=
            dt;

    }


    const boosted =

        state.event.enemyBoost > 0

        ?

        1.55

        :

        1;


    ghosts.forEach(

        ghost => {

            let targetX;

            let targetY;


            // ------------------------------------------------
            // 추격 중에는 플레이어 추적
            // ------------------------------------------------

            if (
                state.chaseTimer > 0
                &&
                !state.hidden
            ) {

                const playerPosition =
                    playerCenter();


                targetX =
                    playerPosition.x;


                targetY =
                    playerPosition.y;

            }

            // 평소에는 순찰
            else {

                const target =
                    ghost.path[
                        ghost.pathIndex
                    ];


                targetX =
                    target.x;


                targetY =
                    target.y;

            }


            const centerX =
                ghost.x
                +
                ghost.w / 2;


            const centerY =
                ghost.y
                +
                ghost.h / 2;


            const dx =
                targetX
                -
                centerX;


            const dy =
                targetY
                -
                centerY;


            const distance =
                Math.hypot(
                    dx,
                    dy
                );


            if (
                distance < 3
                &&
                !(
                    state.chaseTimer > 0
                    &&
                    !state.hidden
                )
            ) {

                ghost.pathIndex =

                    (
                        ghost.pathIndex + 1
                    )

                    %

                    ghost.path.length;

            }

            else if (
                distance > 0
            ) {

                const chaseMultiplier =

                    state.chaseTimer > 0
                    &&
                    !state.hidden

                    ?

                    1.65

                    :

                    1;


                ghost.x +=

                    (
                        dx
                        /
                        distance
                    )

                    *
                    ghost.speed

                    *
                    boosted

                    *
                    chaseMultiplier

                    *
                    dt;


                ghost.y +=

                    (
                        dy
                        /
                        distance
                    )

                    *
                    ghost.speed

                    *
                    boosted

                    *
                    chaseMultiplier

                    *
                    dt;

            }


            // ------------------------------------------------
            // 숨은 상태가 아니면 충돌 판정
            // ------------------------------------------------

            if (
                !state.hidden
                &&
                invulnerable <= 0
            ) {

                const playerPosition =
                    playerCenter();


                const ghostCenter = {

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

                        playerPosition.x
                        -
                        ghostCenter.x,

                        playerPosition.y
                        -
                        ghostCenter.y

                    )

                    <
                    21
                ) {

                    state.hearts -=
                        1;


                    invulnerable =
                        1.4;


                    const start =
                        findTile(
                            "S"
                        );


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
                        "👻 그림자에게 붙잡혔어! 체력 -1"
                    );


                    addLog(
                        "그림자와 충돌."
                    );


                    if (
                        state.hearts
                        <=
                        0
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
// 시간 기반 시스템
// ============================================================

function updateTimedSystems(
    dt
) {

    // CCTV

    if (
        state.cctvTimer > 0
    ) {

        state.cctvTimer -=
            dt;

    }


    // 기록 위치 표시

    if (
        state.recordRevealTimer > 0
    ) {

        state.recordRevealTimer -=
            dt;

    }


    // 추격

    if (
        state.chaseTimer > 0
    ) {

        state.chaseTimer -=
            dt;


        if (
            state.chaseTimer <= 0
        ) {

            state.chaseTimer =
                0;


            setMessage(
                "✅ 추격이 끝났다. 그림자가 다시 순찰로 돌아갔어."
            );

        }

    }


    // 랜덤 이벤트 시간

    const eventNames = [

        "blackout",

        "enemyBoost",

        "alarm"

    ];


    for (
        const eventName
        of
        eventNames
    ) {

        if (
            state.event[
                eventName
            ]
            >
            0
        ) {

            state.event[
                eventName
            ] =

                Math.max(

                    0,

                    state.event[
                        eventName
                    ]
                    -
                    dt

                );

        }

    }


    // --------------------------------------------------------
    // 임시 봉쇄
    // --------------------------------------------------------

    if (
        state.lockedGate
    ) {

        state.lockedGate.remaining -=
            dt;


        if (
            state.lockedGate.remaining
            <=
            0
        ) {

            state.lockedGate =
                null;


            setMessage(
                "🔓 임시 봉쇄가 해제됐다."
            );

        }

    }


    // --------------------------------------------------------
    // 숨기
    // --------------------------------------------------------

    if (
        state.hidden
    ) {

        state.hideSeconds +=
            dt;


        // 6초 이상 숨으면 시간 추가 감소

        if (
            state.hideSeconds
            >
            6
        ) {

            state.time =
                Math.max(

                    0,

                    state.time
                    -
                    dt
                    *
                    1.4

                );

        }


        // 12초 이상이면 강제로 나옴

        if (
            state.hideSeconds
            >
            12
        ) {

            state.hidden =
                false;


            state.hideSeconds =
                0;


            setMessage(
                "⏳ 너무 오래 숨어 있어 자동으로 밖으로 나왔어."
            );

        }

    }


    // --------------------------------------------------------
    // 발전기 미니게임
    // --------------------------------------------------------

    if (
        state.miniGame
        &&
        state.miniGame.type
        ===
        "timing"
    ) {

        state.miniGame.pos +=

            state.miniGame.dir

            *

            dt

            *

            0.72;


        if (
            state.miniGame.pos
            >=
            1
        ) {

            state.miniGame.pos =
                1;


            state.miniGame.dir =
                -1;

        }


        if (
            state.miniGame.pos
            <=
            0
        ) {

            state.miniGame.pos =
                0;


            state.miniGame.dir =
                1;

        }

    }


    // --------------------------------------------------------
    // 랜덤 이벤트 발생
    // --------------------------------------------------------

    state.eventTimer -=
        dt;


    if (
        state.eventTimer <= 0
        &&
        !state.choiceOpen
        &&
        !state.miniGame
    ) {

        triggerRandomEvent();

    }


    // 선택 이벤트

    maybeShowChoiceEvent(
        dt
    );

}


// ============================================================
// 업데이트
// ============================================================

function update(
    dt
) {

    if (
        !state
        ||
        state.won
        ||
        state.lost
        ||
        state.choiceOpen
    ) {

        return;

    }


    state.time -=
        dt;


    if (
        state.time
        <=
        0
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


    updateTimedSystems(
        dt
    );


    updatePlayer(
        dt
    );


    updateGhosts(
        dt
    );


    updatePanels();

}


// ============================================================
// 사각형 그리기
// ============================================================

function rect(
    x,
    y,
    width,
    height,
    color
) {

    ctx.fillStyle =
        color;


    ctx.fillRect(

        Math.round(
            x
        ),

        Math.round(
            y
        ),

        width,

        height

    );

}


// ============================================================
// 물체 이름표
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

            ctx.measureText(
                text
            ).width
            +
            8,

            80

        );


    rect(

        centerX
        -
        width / 2,

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

                const floorColor =

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

                    floorColor

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
// 공통 병원 오브젝트
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
                symbol
                ===
                "W"
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


            // 안내 데스크

            if (
                symbol
                ===
                "T"
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
                symbol
                ===
                "H"
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
                symbol
                ===
                "N"
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
                symbol
                ===
                "Q"
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
                symbol
                ===
                "V"
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


            // 숨는 곳

            if (
                symbol
                ===
                "h"
            ) {

                rect(
                    px + 5,
                    py + 3,
                    22,
                    20,
                    "#657a86"
                );

                rect(
                    px + 8,
                    py + 5,
                    16,
                    17,
                    "#d2e0e5"
                );

                rect(
                    px + 15,
                    py + 5,
                    2,
                    17,
                    "#8aa0aa"
                );


                drawLabel(
                    "숨는 곳",
                    px + 16,
                    py + 29
                );

            }


            // CCTV

            if (
                symbol
                ===
                "Z"
            ) {

                rect(
                    px + 4,
                    py + 3,
                    24,
                    18,
                    "#344b53"
                );

                rect(
                    px + 7,
                    py + 6,
                    18,
                    10,
                    "#6bb2d2"
                );

                rect(
                    px + 12,
                    py + 22,
                    8,
                    3,
                    "#65777e"
                );


                drawLabel(
                    "CCTV",
                    px + 16,
                    py + 29
                );

            }


            // 연구 메모

            if (
                symbol
                ===
                "L"
            ) {

                rect(
                    px + 8,
                    py + 4,
                    16,
                    19,
                    "#efe2b6"
                );

                rect(
                    px + 11,
                    py + 8,
                    10,
                    2,
                    "#827557"
                );

                rect(
                    px + 11,
                    py + 13,
                    10,
                    2,
                    "#827557"
                );


                drawLabel(
                    "연구 메모",
                    px + 16,
                    py + 29
                );

            }


            // 임시 봉쇄

            if (
                symbol
                ===
                "G"
                &&
                state.lockedGate
                &&
                state.lockedGate.x
                ===
                x
                &&
                state.lockedGate.y
                ===
                y
            ) {

                rect(
                    px + 4,
                    py + 1,
                    24,
                    24,
                    "#9b3f49"
                );

                rect(
                    px + 8,
                    py + 4,
                    4,
                    18,
                    "#e56570"
                );

                rect(
                    px + 20,
                    py + 4,
                    4,
                    18,
                    "#e56570"
                );


                drawLabel(
                    "임시 봉쇄",
                    px + 16,
                    py + 29
                );

            }

        }

    }

}


// ============================================================
// 출구 그리기
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
// 스테이지별 오브젝트
// ============================================================

function drawStageObjects() {

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


            // =================================================
            // STAGE 1
            // =================================================

            if (
                level().type
                ===
                "collect"
            ) {

                // 출입카드

                if (
                    symbol
                    ===
                    "K"
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


                // 퓨즈

                if (
                    symbol
                    ===
                    "F"
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


                // 배터리

                if (
                    symbol
                    ===
                    "B"
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


                // 발전기

                if (
                    symbol
                    ===
                    "P"
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


                // 마스터 키

                if (
                    symbol
                    ===
                    "M"
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


                // 보안문

                if (
                    symbol
                    ===
                    "C"
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


                // 전원문

                if (
                    symbol
                    ===
                    "D"
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


                // 엘리베이터

                if (
                    symbol
                    ===
                    "E"
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


            // =================================================
            // STAGE 2
            // =================================================

            else if (
                level().type
                ===
                "switch"
            ) {

                if (
                    [
                        "A",
                        "B",
                        "C"
                    ].includes(
                        symbol
                    )
                ) {

                    const index =
                        state.sequence.indexOf(
                            symbol
                        );


                    const done =

                        index >= 0

                        &&

                        index
                        <
                        state.switchProgress;


                    rect(
                        px + 6,
                        py + 3,
                        20,
                        20,
                        "#344b53"
                    );


                    let terminalColor =
                        "#de6ca5";


                    if (
                        symbol
                        ===
                        "A"
                    ) {

                        terminalColor =
                            "#4d9cff";

                    }


                    if (
                        symbol
                        ===
                        "B"
                    ) {

                        terminalColor =
                            "#f0c44d";

                    }


                    rect(
                        px + 9,
                        py + 6,
                        14,
                        9,

                        done
                        ?
                        "#7cef94"
                        :
                        terminalColor
                    );


                    drawLabel(
                        "단말기 "
                        +
                        symbol,

                        px + 16,
                        py + 29
                    );

                }


                if (
                    symbol
                    ===
                    "X"
                ) {

                    drawExitDoor(

                        px,
                        py,

                        "제독실 출구",

                        state.switchProgress
                        >=
                        3

                    );

                }

            }


            // =================================================
            // STAGE 3
            // =================================================

            else {

                if (
                    symbol
                    ===
                    "R"
                ) {

                    drawExitDoor(

                        px,
                        py,

                        "옥상 출구",

                        rescueCount()
                        >=
                        3

                    );

                }

            }

        }

    }

}


// ============================================================
// 야간 기록
// ============================================================

function drawRecords() {

    for (
        const record
        of
        state.records
    ) {

        if (
            record.collected
        ) {

            continue;

        }


        const px =
            record.x
            *
            TILE;


        const py =
            record.y
            *
            TILE;


        rect(
            px + 9,
            py + 4,
            14,
            17,
            "#f4e7b8"
        );


        rect(
            px + 12,
            py + 8,
            8,
            2,
            "#8e805f"
        );


        rect(
            px + 12,
            py + 13,
            8,
            2,
            "#8e805f"
        );


        drawLabel(
            "야간 기록",
            px + 16,
            py + 29
        );

    }

}


// ============================================================
// 환자 그리기
// ============================================================

function drawPatients() {

    if (
        level().type
        !==
        "rescue"
    ) {

        return;

    }


    for (
        const patient
        of
        state.patients
    ) {

        if (
            patient.rescued
        ) {

            continue;

        }


        const px =
            patient.x
            *
            TILE;


        const py =
            patient.y
            *
            TILE;


        const colors = [

            "#77b8e8",

            "#83c985",

            "#e5a26c"

        ];


        const clothes =
            colors[
                patient.id - 1
            ];


        rect(
            px + 11,
            py + 3,
            10,
            5,
            "#544038"
        );


        rect(
            px + 12,
            py + 7,
            8,
            7,
            "#efc3a5"
        );


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


        rect(
            px + 9,
            py + 14,
            14,
            9,
            clothes
        );


        drawLabel(
            "환자 "
            +
            patient.id,

            px + 16,
            py + 29
        );

    }

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


    if (
        state.hidden
    ) {

        ctx.globalAlpha =
            0.35;

    }


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
        player.facing
        ===
        "down"
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

    else if (
        player.facing
        ===
        "left"
    ) {

        rect(
            x + 10,
            y + 11,
            2,
            2,
            "#1e2528"
        );

    }

    else if (
        player.facing
        ===
        "right"
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
        player.walkFrame
        ===
        1
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


    ctx.globalAlpha =
        1;

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
// 어둠 + 경고등
// ============================================================

function drawDarkness() {

    let alpha =
        0.18;


    if (
        currentLevelIndex
        ===
        0
    ) {

        alpha =

            state.powerOn

            ?

            0.04

            :

            0.23;

    }


    if (
        currentLevelIndex
        ===
        1
    ) {

        alpha =
            0.10;

    }


    if (
        currentLevelIndex
        ===
        2
    ) {

        alpha =
            0.13;

    }


    // 랜덤 정전

    if (
        state.event.blackout
        >
        0
    ) {

        alpha =
            Math.max(
                alpha,
                0.55
            );

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


    // 경고등

    if (
        state.event.alarm
        >
        0
        &&
        Math.floor(
            state.event.alarm
            *
            6
        )
        %
        2
        ===
        0
    ) {

        ctx.fillStyle =
            "rgba(210,40,55,0.12)";


        ctx.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

    }

}


// ============================================================
// CCTV 미니맵
// ============================================================

function drawMiniMap() {

    if (
        state.cctvTimer <= 0
        &&
        state.recordRevealTimer <= 0
    ) {

        return;

    }


    const scale =
        4;


    const width =
        COLS
        *
        scale;


    const height =
        ROWS
        *
        scale;


    const startX =
        canvas.width
        -
        width
        -
        14;


    const startY =
        34;


    rect(
        startX - 5,
        startY - 5,
        width + 10,
        height + 10,
        "rgba(18,32,40,0.88)"
    );


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

            rect(

                startX
                +
                x * scale,

                startY
                +
                y * scale,

                scale,

                scale,

                level().map[y][x]
                ===
                "#"

                ?

                "#48606b"

                :

                "#b8c8cc"

            );

        }

    }


    // 플레이어

    const playerPosition =
        playerCenter();


    rect(

        startX
        +
        Math.floor(
            playerPosition.x
            /
            TILE
        )
        *
        scale,

        startY
        +
        Math.floor(
            playerPosition.y
            /
            TILE
        )
        *
        scale,

        scale,

        scale,

        "#39e57d"

    );


    // CCTV 활성화 시 적 표시

    if (
        state.cctvTimer
        >
        0
    ) {

        for (
            const ghost
            of
            ghosts
        ) {

            rect(

                startX
                +
                Math.floor(
                    (
                        ghost.x + 10
                    )
                    /
                    TILE
                )
                *
                scale,

                startY
                +
                Math.floor(
                    (
                        ghost.y + 10
                    )
                    /
                    TILE
                )
                *
                scale,

                scale,

                scale,

                "#ff5d7a"

            );

        }


        // 환자 표시

        for (
            const patient
            of
            state.patients
        ) {

            if (
                !patient.rescued
            ) {

                rect(

                    startX
                    +
                    patient.x
                    *
                    scale,

                    startY
                    +
                    patient.y
                    *
                    scale,

                    scale,

                    scale,

                    "#67b9ff"

                );

            }

        }

    }


    // 기록 위치

    if (
        state.recordRevealTimer
        >
        0
    ) {

        for (
            const record
            of
            state.records
        ) {

            if (
                !record.collected
            ) {

                rect(

                    startX
                    +
                    record.x
                    *
                    scale,

                    startY
                    +
                    record.y
                    *
                    scale,

                    scale,

                    scale,

                    "#ffd85c"

                );

            }

        }

    }


    ctx.fillStyle =
        "#ffffff";


    ctx.font =
        "10px monospace";


    ctx.fillText(
        "CCTV MAP",
        startX,
        startY - 8
    );

}


// ============================================================
// 발전기 미니게임 화면
// ============================================================

function drawMiniGame() {

    if (
        !state.miniGame
    ) {

        return;

    }


    rect(
        250,
        238,
        556,
        150,
        "rgba(17,31,38,0.94)"
    );


    ctx.fillStyle =
        "#ffffff";


    ctx.font =
        'bold 18px "Malgun Gothic"';


    ctx.textAlign =
        "center";


    ctx.fillText(
        "발전기 수리 타이밍",
        528,
        270
    );


    ctx.font =
        '13px "Malgun Gothic"';


    ctx.fillText(
        "표시가 초록 구간에 들어왔을 때 Space",
        528,
        295
    );


    // 바

    rect(
        330,
        325,
        396,
        20,
        "#233740"
    );


    // 성공 구간

    rect(
        330
        +
        396 * 0.42,

        325,

        396 * 0.16,

        20,

        "#52d981"
    );


    // 움직이는 표시

    const pointerX =

        330

        +

        396
        *
        state.miniGame.pos;


    rect(
        pointerX - 4,
        319,
        8,
        32,
        "#ffe067"
    );


    ctx.textAlign =
        "left";

}


// ============================================================
// HUD
// ============================================================

function drawHud() {

    rect(
        0,
        0,
        canvas.width,
        26,
        "rgba(18,42,52,0.90)"
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


    ctx.fillText(
        "STA "
        +
        Math.round(
            state.stamina
        ),
        370,
        17
    );


    if (
        state.chaseTimer
        >
        0
    ) {

        ctx.fillText(
            "CHASE "
            +
            Math.ceil(
                state.chaseTimer
            )
            +
            "s",
            470,
            17
        );

    }


    if (
        state.hidden
    ) {

        ctx.fillText(
            "HIDDEN",
            590,
            17
        );

    }

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

    drawStageObjects();

    drawRecords();

    drawPatients();


    // 어둠은 캐릭터보다 먼저

    drawDarkness();


    ghosts.forEach(
        drawGhost
    );


    drawPlayer();


    drawMiniMap();


    drawMiniGame();


    drawHud();

}


// ============================================================
// 게임 루프
// ============================================================

function gameLoop(
    now
) {

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

        "Enter",

        "Shift"

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


// ============================================================
// 키 해제
// ============================================================

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


// ============================================================
// 화면 클릭
// ============================================================

canvas.addEventListener(
    "mousedown",
    () => {

        canvas.focus();


        setMessage(
            "✅ 게임 입력 활성화."
        );

    }
);


// ============================================================
// 창에서 벗어났을 때 키 초기화
// ============================================================

window.addEventListener(
    "blur",
    () => {

        keys =
            {};

    }
);


// ============================================================
// 화면 방향 버튼
// ============================================================

function pressDirection(
    direction
) {

    keys[
        direction
    ] =
        true;


    canvas.focus();

}


function releaseDirection(
    direction
) {

    keys[
        direction
    ] =
        false;

}


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
'''

components.html(
    game_html,
    height=1190,
    scrolling=False
)

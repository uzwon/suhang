import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="MIDNIGHT HOSPITAL",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 MIDNIGHT HOSPITAL")
st.caption("픽셀 병원 탈출 게임 · 방향키/WASD 이동 · Space 상호작용 · R 재시작")


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
    background: #dde8ec;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

.wrap {
    padding: 12px;
}

.topbar {
    background: linear-gradient(180deg, #29434f, #203640);
    color: white;
    border-radius: 16px;
    padding: 14px 18px;
    margin-bottom: 12px;
}

.title {
    font-size: 28px;
    font-weight: 900;
    letter-spacing: 2px;
}

.subtitle {
    font-size: 13px;
    margin-top: 5px;
    opacity: 0.9;
}

.layout {
    display: flex;
    gap: 12px;
    align-items: flex-start;
}

.game-area {
    background: #edf4f6;
    border: 2px solid #9db3bb;
    border-radius: 16px;
    padding: 10px;
    position: relative;
}

#messageBar {
    background: #fff3d5;
    border-left: 6px solid #d5ae45;
    border-radius: 10px;
    padding: 10px 13px;
    margin-bottom: 8px;
    min-height: 48px;
    color: #594c29;
    font-size: 14px;
}

canvas {
    display: block;
    border: 3px solid #688792;
    border-radius: 8px;
    background: #132832;
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    outline: none;
}

.help {
    margin-top: 8px;
    background: #e4eff2;
    border-radius: 10px;
    padding: 9px 12px;
    font-size: 13px;
    line-height: 1.55;
    color: #2b4751;
}

.side {
    width: 270px;
}

.card {
    background: #fbfdfe;
    border: 1px solid #acbec5;
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 10px;
}

.card h3 {
    margin: 0 0 10px 0;
    font-size: 17px;
    color: #263e47;
}

.objective {
    background: #e8f1fb;
    border-left: 5px solid #6b8eb4;
    border-radius: 9px;
    padding: 10px;
    color: #304c61;
    font-size: 13px;
    line-height: 1.6;
}

.item {
    background: #edf4f6;
    border-radius: 8px;
    padding: 7px 9px;
    margin-bottom: 6px;
    font-size: 13px;
}

.stat {
    margin-bottom: 7px;
    font-size: 13px;
}

.log {
    background: #283b44;
    color: #dbe8eb;
    border-radius: 8px;
    padding: 7px;
    margin-bottom: 5px;
    font-family: monospace;
    font-size: 11px;
}

button {
    width: 100%;
    border: none;
    border-radius: 10px;
    padding: 11px;
    background: #416675;
    color: white;
    font-weight: 800;
    cursor: pointer;
}

.overlay {
    position: absolute;
    top: 68px;
    left: 10px;
    width: 896px;
    height: 576px;
    background: rgba(7, 15, 20, 0.72);
    display: none;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
}

.overlay-box {
    width: 420px;
    background: white;
    border-radius: 18px;
    padding: 24px;
    text-align: center;
}

.overlay-title {
    font-size: 34px;
    font-weight: 900;
    margin-bottom: 12px;
}

.overlay-text {
    line-height: 1.7;
    margin-bottom: 18px;
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

@media(max-width:1250px) {

    .layout {
        flex-direction: column;
    }

    .side {
        width: 100%;
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

    <div class="subtitle">
        병원 내부를 직접 탐색해 전원을 복구하고 탈출하세요.
    </div>

</div>


<div class="layout">


<div class="game-area">


<div id="messageBar">
    화면을 클릭한 뒤 방향키 또는 WASD로 움직여 보세요.
</div>


<canvas
    id="game"
    width="896"
    height="576"
    tabindex="0">
</canvas>


<div class="help">

    <b>조작법</b><br>

    방향키 / WASD : 이동<br>
    Space / Enter : 상호작용<br>
    R : 게임 재시작


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

    <h3>📟 기록</h3>

    <div id="logBox">
    </div>

</div>


<button onclick="resetGame()">
    🔄 게임 다시 시작
</button>


</div>


</div>

</div>


<script>


/* ============================================================
   HTML 요소
============================================================ */

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

const overlay =
    document.getElementById("overlay");

const overlayBox =
    document.getElementById("overlayBox");


/* ============================================================
   맵
============================================================ */

const TILE = 32;

const COLS = 28;

const ROWS = 18;


/*
중요:

W = 창문
T = 데스크
H = 침대
Q = 휠체어
N = 간호 스테이션
V = 자판기

이 장식물들은 이제 이동을 막지 않음.

오직

# = 벽
C = 카드 보안문
D = 전원 보안문

만 캐릭터를 막음.
*/

const MAP = [

    "############################",
    "#S....W....T.....#........E#",
    "#......######....#..........#",
    "#......#....#....#..........#",
    "#......#.K..#...........H...#",
    "#......#....####............#",
    "#......####.................#",
    "#....C.......F..............#",
    "#...........................#",
    "#..B........................#",
    "#...........................#",
    "#...........................#",
    "#.P.......................D.#",
    "#...........................#",
    "#...........................#",
    "#.............M.......Q.....#",
    "#..N...................V....#",
    "############################"

];


const FLOOR_COLORS = [

    "#b6c8ce",
    "#b2c5cb",
    "#bdced3",
    "#acc0c7"

];


/* ============================================================
   게임 변수
============================================================ */

let player;

let state;

let keys = {};

let ghosts = [];

let lastTime =
    performance.now();

let invulnerable = 0;


/* ============================================================
   타일 위치 찾기
============================================================ */

function findTile(symbol) {

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
                MAP[y][x]
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


/* ============================================================
   타일 중심
============================================================ */

function tileCenter(x, y) {

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


/* ============================================================
   초기화
============================================================ */

function resetGame() {

    const start =
        findTile("S");


    /*
    캐릭터는 크게 보이지만
    실제 충돌은 작은 발 영역만 사용
    */

    player = {

        x:
            start.x * TILE + 1,

        y:
            start.y * TILE - 4,

        spriteW:
            30,

        spriteH:
            38,

        hitW:
            12,

        hitH:
            8,

        hitOffsetX:
            9,

        hitOffsetY:
            20,

        speed:
            155,

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

        hearts: 4,

        time: 420,

        hasKeycard: false,

        hasFuse: false,

        hasBattery: false,

        powerOn: false,

        hasMasterKey: false,

        won: false,

        lost: false,

        logs: []

    };


    ghosts = [

        {

            x:
                20 * TILE,

            y:
                5 * TILE,

            w: 20,

            h: 20,

            color:
                "#957cff",

            speed:
                43,

            active:
                true,

            path: [

                tileCenter(20, 5),

                tileCenter(25, 5),

                tileCenter(25, 10),

                tileCenter(20, 10)

            ],

            pathIndex:
                1

        }

    ];


    invulnerable = 0;


    state.logs.push(
        "22:00 — 병원 셔터가 내려갔습니다."
    );


    state.logs.push(
        "엘리베이터의 전원이 꺼졌습니다."
    );


    state.logs.push(
        "출입카드를 먼저 찾아보세요."
    );


    setMessage(
        "✅ 이제 창문과 병원 가구 때문에 막히지 않아. 자유롭게 이동해 봐!"
    );


    overlay.style.display =
        "none";


    updatePanels();


    canvas.focus();
}


/* ============================================================
   메시지
============================================================ */

function setMessage(text) {

    messageBar.innerHTML =
        text;
}


/* ============================================================
   로그
============================================================ */

function addLog(text) {

    state.logs.unshift(text);


    if (
        state.logs.length > 7
    ) {

        state.logs.pop();
    }


    updatePanels();
}


/* ============================================================
   오른쪽 UI
============================================================ */

function updatePanels() {

    let objective = "";


    if (
        !state.hasKeycard
    ) {

        objective =
            "1. <b>출입카드</b>를 찾아.";

    }

    else if (
        !state.hasFuse
    ) {

        objective =
            "2. 발전기 수리에 필요한 <b>퓨즈</b>를 찾아.";

    }

    else if (
        !state.hasBattery
    ) {

        objective =
            "3. <b>비상 배터리</b>를 찾아.";

    }

    else if (
        !state.powerOn
    ) {

        objective =
            "4. 발전기로 가서 <b>전원을 복구</b>해.";

    }

    else if (
        !state.hasMasterKey
    ) {

        objective =
            "5. <b>마스터 키</b>를 찾아.";

    }

    else {

        objective =
            "6. 엘리베이터에서 <b>탈출</b>해!";
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
                "🪪 출입카드"
                :
                "⬜ 출입카드"
            }
        </div>

        <div class="item">
            ${
                state.hasFuse
                ?
                "🧰 퓨즈"
                :
                "⬜ 퓨즈"
            }
        </div>

        <div class="item">
            ${
                state.hasBattery
                ?
                "🔋 비상 배터리"
                :
                "⬜ 비상 배터리"
            }
        </div>

        <div class="item">
            ${
                state.hasMasterKey
                ?
                "🗝️ 마스터 키"
                :
                "⬜ 마스터 키"
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


/* ============================================================
   핵심 수정
   실제 장애물
============================================================ */

function tileBlocked(tx, ty) {

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
        MAP[ty][tx];


    /*
    ★ 가장 중요한 수정 ★

    창문 W
    책상 T
    침대 H
    휠체어 Q
    간호 스테이션 N
    자판기 V

    전부 장애물 판정 제거
    */


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


/* ============================================================
   캐릭터 충돌
============================================================ */

function collisionAt(newX, newY) {

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


/* ============================================================
   이동
============================================================ */

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


    /*
    X / Y 따로 판정

    벽에 닿더라도
    벽을 따라 이동 가능
    */

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


/* ============================================================
   플레이어 중심
============================================================ */

function playerCenter() {

    return {

        x:
            player.x + 15,

        y:
            player.y + 23

    };
}


/* ============================================================
   타일 근처
============================================================ */

function nearTile(
    symbol,
    distance = 41
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


/* ============================================================
   상호작용
============================================================ */

function interact() {

    canvas.focus();


    if (
        state.won
        ||
        state.lost
    ) {

        return;
    }


    if (
        nearTile("K")
        &&
        !state.hasKeycard
    ) {

        state.hasKeycard =
            true;


        setMessage(
            "🪪 출입카드를 주웠어!"
        );


        addLog(
            "출입카드 확보."
        );


        updatePanels();

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
            "🧰 퓨즈를 주웠어!"
        );


        addLog(
            "퓨즈 확보."
        );


        updatePanels();

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
            "🔋 비상 배터리를 찾았어!"
        );


        addLog(
            "배터리 확보."
        );


        updatePanels();

        return;
    }


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

            state.powerOn =
                true;


            setMessage(
                "⚡ 병원 전원이 복구됐어!"
            );


            addLog(
                "병원 전원 복구."
            );


            updatePanels();

        }

        else {

            const needed =
                [];


            if (
                !state.hasFuse
            ) {

                needed.push(
                    "퓨즈"
                );
            }


            if (
                !state.hasBattery
            ) {

                needed.push(
                    "배터리"
                );
            }


            setMessage(

                "⚠️ 발전기에 "
                +
                needed.join(", ")
                +
                "가 필요해."

            );
        }


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
                "🚪 전원을 먼저 복구해야 해."
            );

            return;
        }


        state.hasMasterKey =
            true;


        setMessage(
            "🗝️ 마스터 키를 찾았어!"
        );


        addLog(
            "마스터 키 확보."
        );


        updatePanels();

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

            state.won =
                true;


            showResult(
                "ESCAPED!",
                "엘리베이터가 작동했습니다.<br><br>병원 탈출 성공!"
            );

        }

        else {

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
                    "마스터 키"
                );
            }


            setMessage(

                "🚪 엘리베이터 이용에 "
                +
                needed.join(", ")
                +
                "가 필요해."

            );
        }


        return;
    }


    setMessage(
        "주변에 상호작용할 물건이 없어."
    );
}


/* ============================================================
   결과 화면
============================================================ */

function showResult(
    title,
    text
) {

    overlayBox.innerHTML = `

        <div class="overlay-title">
            ${title}
        </div>

        <div class="overlay-text">
            ${text}
        </div>

        <button onclick="resetGame()">
            다시 시작
        </button>

    `;


    overlay.style.display =
        "flex";
}


/* ============================================================
   화면 방향키
============================================================ */

function pressDirection(direction) {

    keys[direction] =
        true;

    canvas.focus();
}


function releaseDirection(direction) {

    keys[direction] =
        false;
}


/* ============================================================
   적
============================================================ */

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


            const cx =
                ghost.x
                +
                ghost.w / 2;


            const cy =
                ghost.y
                +
                ghost.h / 2;


            const dx =
                target.x
                -
                cx;


            const dy =
                target.y
                -
                cy;


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
                    20
                ) {

                    state.hearts -=
                        1;


                    invulnerable =
                        1.5;


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
                        "👻 그림자와 부딪혔어! 체력 -1"
                    );


                    updatePanels();


                    if (
                        state.hearts <= 0
                    ) {

                        state.lost =
                            true;


                        showResult(
                            "GAME OVER",
                            "체력이 모두 소진됐어."
                        );
                    }
                }
            }
        }
    );
}


/* ============================================================
   그리기 도우미
============================================================ */

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


/* ============================================================
   바닥
============================================================ */

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
                MAP[y][x]
                !==
                "#"
            ) {

                rect(

                    x * TILE,

                    y * TILE,

                    TILE,

                    TILE,

                    FLOOR_COLORS[
                        (x + y)
                        %
                        FLOOR_COLORS.length
                    ]

                );


                rect(

                    x * TILE + 5,

                    y * TILE + 5,

                    4,

                    4,

                    "rgba(255,255,255,0.12)"

                );
            }
        }
    }
}


/* ============================================================
   벽
============================================================ */

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
                MAP[y][x]
                ===
                "#"
            ) {

                rect(

                    x * TILE,

                    y * TILE,

                    TILE,

                    TILE,

                    "#334f5b"

                );


                rect(

                    x * TILE + 3,

                    y * TILE + 3,

                    TILE - 6,

                    TILE - 6,

                    "#4d6974"

                );


                rect(

                    x * TILE + 6,

                    y * TILE + 6,

                    TILE - 12,

                    TILE - 12,

                    "#5d7a85"

                );
            }
        }
    }
}


/* ============================================================
   가구 / 병원 장식
============================================================ */

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
                MAP[y][x];


            const px =
                x * TILE;


            const py =
                y * TILE;


            /* 창문 */

            if (
                symbol === "W"
            ) {

                rect(
                    px + 3,
                    py + 3,
                    26,
                    23,
                    "#9fb7c1"
                );

                rect(
                    px + 5,
                    py + 5,
                    22,
                    19,
                    "#376d91"
                );

                rect(
                    px + 15,
                    py + 5,
                    2,
                    19,
                    "#d4edf7"
                );

                rect(
                    px + 5,
                    py + 13,
                    22,
                    2,
                    "#d4edf7"
                );

                /* 밤하늘 */

                rect(
                    px + 7,
                    py + 7,
                    7,
                    5,
                    "#173750"
                );

                rect(
                    px + 18,
                    py + 7,
                    7,
                    5,
                    "#173750"
                );

                rect(
                    px + 7,
                    py + 16,
                    7,
                    6,
                    "#173750"
                );

                rect(
                    px + 18,
                    py + 16,
                    7,
                    6,
                    "#173750"
                );
            }


            /* 데스크 */

            if (
                symbol === "T"
            ) {

                rect(
                    px + 4,
                    py + 9,
                    24,
                    14,
                    "#8d674a"
                );

                rect(
                    px + 4,
                    py + 7,
                    24,
                    4,
                    "#b58c67"
                );

                rect(
                    px + 7,
                    py + 23,
                    3,
                    7,
                    "#70503b"
                );

                rect(
                    px + 22,
                    py + 23,
                    3,
                    7,
                    "#70503b"
                );
            }


            /* 침대 */

            if (
                symbol === "H"
            ) {

                rect(
                    px + 2,
                    py + 8,
                    28,
                    16,
                    "#d8e6eb"
                );

                rect(
                    px + 4,
                    py + 10,
                    9,
                    7,
                    "#b9d5df"
                );

                rect(
                    px + 13,
                    py + 10,
                    15,
                    12,
                    "#f6fafb"
                );

                rect(
                    px + 3,
                    py + 24,
                    3,
                    6,
                    "#657b84"
                );

                rect(
                    px + 26,
                    py + 24,
                    3,
                    6,
                    "#657b84"
                );
            }


            /* 휠체어 */

            if (
                symbol === "Q"
            ) {

                rect(
                    px + 6,
                    py + 8,
                    11,
                    7,
                    "#66859b"
                );

                rect(
                    px + 11,
                    py + 4,
                    3,
                    6,
                    "#66859b"
                );

                rect(
                    px + 4,
                    py + 17,
                    9,
                    9,
                    "#33474f"
                );

                rect(
                    px + 17,
                    py + 17,
                    9,
                    9,
                    "#33474f"
                );

                rect(
                    px + 15,
                    py + 11,
                    7,
                    3,
                    "#7593a7"
                );
            }


            /* 간호 스테이션 */

            if (
                symbol === "N"
            ) {

                rect(
                    px + 3,
                    py + 10,
                    26,
                    14,
                    "#e7f0f3"
                );

                rect(
                    px + 5,
                    py + 7,
                    22,
                    5,
                    "#73a8ba"
                );

                rect(
                    px + 10,
                    py + 13,
                    12,
                    6,
                    "#9cc6d3"
                );
            }


            /* 자판기 */

            if (
                symbol === "V"
            ) {

                rect(
                    px + 7,
                    py + 3,
                    18,
                    27,
                    "#bd4755"
                );

                rect(
                    px + 9,
                    py + 6,
                    14,
                    10,
                    "#cfebf4"
                );

                rect(
                    px + 10,
                    py + 18,
                    12,
                    5,
                    "#f3d26e"
                );

                rect(
                    px + 12,
                    py + 26,
                    8,
                    2,
                    "#343f44"
                );
            }


            /* 카드 보안문 */

            if (
                symbol === "C"
            ) {

                rect(
                    px + 5,
                    py + 2,
                    22,
                    28,
                    state.hasKeycard
                    ?
                    "#74aa89"
                    :
                    "#517fb5"
                );
            }


            /* 전원 보안문 */

            if (
                symbol === "D"
            ) {

                rect(
                    px + 5,
                    py + 2,
                    22,
                    28,
                    state.powerOn
                    ?
                    "#74aa89"
                    :
                    "#806044"
                );
            }


            /* 발전기 */

            if (
                symbol === "P"
            ) {

                rect(
                    px + 3,
                    py + 7,
                    26,
                    19,
                    "#485d66"
                );

                rect(
                    px + 8,
                    py + 11,
                    16,
                    10,
                    "#273940"
                );

                rect(
                    px + 10,
                    py + 14,
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
                    py + 14,
                    4,
                    4,
                    "#e8c854"
                );
            }


            /* 엘리베이터 */

            if (
                symbol === "E"
            ) {

                rect(
                    px + 2,
                    py + 2,
                    28,
                    28,
                    "#6e858e"
                );

                rect(
                    px + 5,
                    py + 4,
                    10,
                    24,
                    "#a4b9c0"
                );

                rect(
                    px + 17,
                    py + 4,
                    10,
                    24,
                    "#a4b9c0"
                );

                rect(
                    px + 10,
                    py + 7,
                    12,
                    3,
                    state.powerOn
                    ?
                    "#71e883"
                    :
                    "#d45e67"
                );
            }
        }
    }
}


/* ============================================================
   아이템
============================================================ */

function drawItems() {

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
                MAP[y][x];


            const px =
                x * TILE;


            const py =
                y * TILE;


            /* 출입카드 */

            if (
                symbol === "K"
                &&
                !state.hasKeycard
            ) {

                rect(
                    px + 6,
                    py + 10,
                    20,
                    12,
                    "#438bed"
                );

                rect(
                    px + 9,
                    py + 13,
                    5,
                    4,
                    "#e4f4ff"
                );

                rect(
                    px + 17,
                    py + 13,
                    6,
                    3,
                    "#23548b"
                );
            }


            /* 퓨즈 */

            if (
                symbol === "F"
                &&
                !state.hasFuse
            ) {

                rect(
                    px + 9,
                    py + 7,
                    14,
                    18,
                    "#e5c44e"
                );

                rect(
                    px + 11,
                    py + 10,
                    10,
                    4,
                    "#fff3aa"
                );

                rect(
                    px + 12,
                    py + 21,
                    8,
                    2,
                    "#927418"
                );
            }


            /* 배터리 */

            if (
                symbol === "B"
                &&
                !state.hasBattery
            ) {

                rect(
                    px + 9,
                    py + 7,
                    14,
                    20,
                    "#46a760"
                );

                rect(
                    px + 13,
                    py + 4,
                    6,
                    4,
                    "#d6e4e8"
                );

                rect(
                    px + 13,
                    py + 13,
                    6,
                    2,
                    "#c5f5ce"
                );
            }


            /* 마스터 키 */

            if (
                symbol === "M"
                &&
                !state.hasMasterKey
            ) {

                rect(
                    px + 8,
                    py + 13,
                    13,
                    4,
                    "#f0c13b"
                );

                rect(
                    px + 19,
                    py + 11,
                    6,
                    8,
                    "#f0c13b"
                );

                rect(
                    px + 21,
                    py + 13,
                    2,
                    2,
                    "#9f7511"
                );
            }
        }
    }
}


/* ============================================================
   플레이어 캐릭터
============================================================ */

function drawPlayer() {

    const x =
        Math.round(
            player.x
        );


    const y =
        Math.round(
            player.y
        );


    /* 바닥 그림자 */

    rect(
        x + 5,
        y + 34,
        20,
        4,
        "rgba(0,0,0,0.20)"
    );


    /* 캐릭터 외곽선 */

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


    /* 갈색 머리 */

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


    /* 얼굴 */

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


    /* 청록색 의료복 */

    rect(
        x + 11,
        y + 19,
        9,
        11,
        "#4ca8bb"
    );


    /* 흰 의사가운 */

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


    /* 명찰 */

    rect(
        x + 20,
        y + 21,
        4,
        3,
        "#5294dd"
    );


    /* 팔 */

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


    /* 손 */

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


    /* 다리 걷기 애니메이션 */

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


    /* 신발 */

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


    /* 청진기 */

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


/* ============================================================
   그림자
============================================================ */

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


/* ============================================================
   어둠
============================================================ */

function drawDarkness() {

    if (
        state.powerOn
    ) {

        return;
    }


    ctx.fillStyle =
        "rgba(5,18,28,0.23)";


    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );
}


/* ============================================================
   HUD
============================================================ */

function drawHud() {

    ctx.fillStyle =
        "rgba(18,42,52,0.88)";


    ctx.fillRect(
        0,
        0,
        canvas.width,
        25
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
        "TIME "
        +
        minutes
        +
        ":"
        +
        seconds,
        10,
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
        170,
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
        300,
        17
    );
}


/* ============================================================
   렌더링
============================================================ */

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


    /*
    어둠은 캐릭터보다 먼저
    */

    drawDarkness();


    ghosts.forEach(

        ghost =>
            drawGhost(
                ghost
            )

    );


    /*
    캐릭터를 가장 위에
    */

    drawPlayer();


    drawHud();
}


/* ============================================================
   업데이트
============================================================ */

function update(dt) {

    if (
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


        showResult(
            "GAME OVER",
            "시간 안에 병원에서 탈출하지 못했어."
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


/* ============================================================
   게임 루프
============================================================ */

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


    update(
        dt
    );


    render();


    requestAnimationFrame(
        gameLoop
    );
}


/* ============================================================
   키보드
============================================================ */

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

        resetGame();
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
            "✅ 방향키 입력 활성화!"
        );
    }
);


window.addEventListener(
    "blur",
    () => {

        keys = {};
    }
);


/* ============================================================
   시작
============================================================ */

window.addEventListener(
    "load",
    () => {

        resetGame();


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
    height=1050,
    scrolling=False
)

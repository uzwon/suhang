import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="MIDNIGHT HOSPITAL",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 MIDNIGHT HOSPITAL")
st.caption("픽셀 스타일 병원 탈출 게임 · 방향키 이동 / Space 상호작용 / R 재시작")

game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>MIDNIGHT HOSPITAL</title>
<style>
* {
    box-sizing: border-box;
    user-select: none;
}

body {
    margin: 0;
    background: linear-gradient(180deg, #dbe7ea 0%, #eef4f6 100%);
    font-family: Arial, sans-serif;
    color: #20353d;
}

.wrap {
    width: 100%;
    padding: 14px;
}

.topbar {
    background: linear-gradient(180deg, #2b4753, #213842);
    color: white;
    border-radius: 18px;
    padding: 16px 18px;
    margin-bottom: 14px;
    box-shadow: 0 8px 18px rgba(0,0,0,0.14);
}

.title {
    font-size: 30px;
    font-weight: 900;
    letter-spacing: 2px;
    margin-bottom: 6px;
}

.subtitle {
    font-size: 13px;
    opacity: 0.96;
}

.layout {
    display: flex;
    gap: 14px;
    align-items: flex-start;
}

.left-panel {
    flex: 0 0 auto;
}

.right-panel {
    flex: 1 1 auto;
    min-width: 270px;
}

.canvas-wrap {
    background: linear-gradient(180deg, #edf5f7, #dde8ec);
    border: 2px solid #9db3bb;
    border-radius: 18px;
    padding: 12px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.09);
    position: relative;
}

#messageBar {
    background: #fff4d8;
    border-left: 6px solid #d7b14a;
    color: #5c4e28;
    border-radius: 12px;
    padding: 12px 14px;
    font-size: 14px;
    margin-bottom: 10px;
    min-height: 54px;
    line-height: 1.55;
}

canvas {
    display: block;
    background: #10222b;
    border: 3px solid #6f8e98;
    border-radius: 12px;
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    outline: none;
}

.controls {
    margin-top: 10px;
    background: #edf5f7;
    border-radius: 12px;
    padding: 10px 12px;
    font-size: 13px;
    color: #2d4750;
    line-height: 1.6;
}

.card {
    background: rgba(251, 253, 254, 0.98);
    border: 1px solid #afc1c8;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
}

.card h3 {
    margin: 0 0 10px 0;
    color: #243b44;
    font-size: 18px;
}

.hud-line {
    margin: 8px 0;
    line-height: 1.5;
    font-size: 14px;
}

.inventory-item {
    background: #eef5f7;
    border: 1px solid #c7d6db;
    border-radius: 10px;
    padding: 8px 10px;
    margin-bottom: 8px;
    font-size: 14px;
}

.log {
    font-family: monospace;
    background: #253842;
    color: #d9e9ee;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 8px;
    font-size: 12px;
    line-height: 1.5;
}

.button {
    width: 100%;
    border: none;
    border-radius: 12px;
    background: linear-gradient(180deg, #4f7382, #375a69);
    color: white;
    font-weight: 800;
    padding: 12px;
    cursor: pointer;
    font-size: 15px;
    box-shadow: 0 5px 12px rgba(0,0,0,0.10);
}

.button:hover {
    filter: brightness(1.05);
}

.objective {
    background: #e9f2fb;
    border-left: 6px solid #6b8db3;
    color: #304c62;
    border-radius: 12px;
    padding: 12px 14px;
    line-height: 1.65;
    font-size: 14px;
}

.hint {
    color: #5f7882;
    font-size: 13px;
    margin-top: 8px;
    line-height: 1.5;
}

.overlay {
    position: absolute;
    inset: 12px;
    display: none;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 20px;
    background: rgba(8, 17, 24, 0.65);
    border-radius: 12px;
}

.overlay-box {
    width: 85%;
    max-width: 500px;
    background: linear-gradient(180deg, #f9fcfd, #e9f1f4);
    border: 2px solid #9eb4bc;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.25);
}

.overlay-title {
    font-size: 34px;
    font-weight: 900;
    color: #223842;
    margin-bottom: 12px;
    letter-spacing: 1px;
}

.overlay-text {
    color: #324b55;
    line-height: 1.8;
    margin-bottom: 18px;
    font-size: 15px;
}

.small {
    font-size: 12px;
    color: #70868e;
    margin-top: 8px;
}

@media (max-width: 1300px) {
    .layout {
        flex-direction: column;
    }

    .right-panel {
        width: 100%;
    }

    canvas {
        width: 100%;
        height: auto;
    }
}
</style>
</head>
<body>
<div class="wrap">
    <div class="topbar">
        <div class="title">MIDNIGHT HOSPITAL</div>
        <div class="subtitle">병원 내부를 탐색하고 아이템을 모아 전원을 복구한 뒤 엘리베이터로 탈출하세요.</div>
    </div>

    <div class="layout">
        <div class="left-panel">
            <div class="canvas-wrap">
                <div id="messageBar">게임 화면을 한 번 클릭한 뒤 방향키로 이동해 봐. Space 키로 상호작용할 수 있어.</div>
                <canvas id="game" width="896" height="576" tabindex="0"></canvas>

                <div class="controls">
                    <b>조작법</b><br>
                    ← ↑ ↓ → : 이동<br>
                    Space : 아이템 줍기 / 발전기 / 엘리베이터 상호작용<br>
                    R : 게임 재시작
                </div>

                <div class="overlay" id="overlay">
                    <div class="overlay-box" id="overlayBox"></div>
                </div>
            </div>
        </div>

        <div class="right-panel">
            <div class="card">
                <h3>🎯 목표</h3>
                <div class="objective" id="objectiveBox"></div>
                <div class="hint">
                    출입카드, 퓨즈, 배터리, 마스터 키를 모아 병원에서 빠져나가세요.
                </div>
            </div>

            <div class="card">
                <h3>📊 상태</h3>
                <div id="statusBox"></div>
            </div>

            <div class="card">
                <h3>🎒 인벤토리</h3>
                <div id="inventoryBox"></div>
            </div>

            <div class="card">
                <h3>📝 야간 기록</h3>
                <div id="logBox"></div>
            </div>

            <button class="button" onclick="resetGame()">🔄 새로 시작</button>
        </div>
    </div>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
ctx.imageSmoothingEnabled = false;

const overlay = document.getElementById("overlay");
const overlayBox = document.getElementById("overlayBox");
const messageBar = document.getElementById("messageBar");
const objectiveBox = document.getElementById("objectiveBox");
const statusBox = document.getElementById("statusBox");
const inventoryBox = document.getElementById("inventoryBox");
const logBox = document.getElementById("logBox");

const TILE = 32;
const COLS = 28;
const ROWS = 18;

const MAP = [
    "############################",
    "#S....W....T.....#........E#",
    "#.####.######.##.#.######..#",
    "#.#..#.#....#..#.#.#....#..#",
    "#.#..#.#.K..#..#...#..H.#..#",
    "#....#.#....####...#....#..#",
    "####.#.####....#.#.#.##.#..#",
    "#....C....#..F.#.#.#....#..#",
    "#.######.#.####.#.#.####.#.#",
    "#..B...#.#....#.#.#....#...#",
    "#.###.#.#.##.#.#.#.##.#.#..#",
    "#...#.#...#..#.#...#..#.#..#",
    "#.P.#.###.#.##.#.###.#.#D.##",
    "#...#.....#....#.....#....##",
    "#.#####.####.######.####...#",
    "#.....#....#..M..#....Q....#",
    "#..N..#....#######....V....#",
    "############################"
];

const FLOOR_COLORS = ["#b7c9cf", "#b1c4ca", "#c0d1d6", "#aec1c7"];

let player;
let state;
let keys = {};
let lastTime = performance.now();
let invuln = 0;
const ghosts = [];

function findTile(ch) {
    for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
            if (MAP[y][x] === ch) {
                return {x, y};
            }
        }
    }
    return null;
}

function tileCenter(tx, ty) {
    return {
        x: tx * TILE + TILE / 2,
        y: ty * TILE + TILE / 2
    };
}

function resetGame() {
    const s = findTile("S");

    player = {
        x: s.x * TILE + 2,
        y: s.y * TILE - 2,
        w: 28,
        h: 34,
        speed: 2.35,
        facing: "down",
        walking: false,
        walkFrame: 0,
        walkTimer: 0
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
        logs: [],
        message: "병원에 갇혔어. 아이템을 모으고 전원을 복구한 뒤 엘리베이터로 탈출해."
    };

    ghosts.length = 0;

    ghosts.push({
        x: 17 * TILE + 4,
        y: 2 * TILE + 2,
        w: 22,
        h: 22,
        speed: 1.0,
        path: [
            tileCenter(17, 2),
            tileCenter(24, 2),
            tileCenter(24, 7),
            tileCenter(17, 7)
        ],
        idx: 1,
        active: true,
        color: "#8a72ff"
    });

    ghosts.push({
        x: 18 * TILE + 4,
        y: 13 * TILE + 2,
        w: 22,
        h: 22,
        speed: 1.05,
        path: [
            tileCenter(18, 13),
            tileCenter(23, 13),
            tileCenter(23, 16),
            tileCenter(18, 16)
        ],
        idx: 1,
        active: false,
        color: "#ff74ad"
    });

    ghosts.push({
        x: 3 * TILE + 4,
        y: 14 * TILE + 2,
        w: 22,
        h: 22,
        speed: 0.95,
        path: [
            tileCenter(2, 13),
            tileCenter(5, 13),
            tileCenter(5, 16),
            tileCenter(2, 16)
        ],
        idx: 1,
        active: false,
        color: "#7ae3ff"
    });

    state.logs.push("22:00 — 병원 셔터가 내려갔습니다.");
    state.logs.push("엘리베이터는 전원이 꺼져 있습니다.");
    state.logs.push("출입카드와 발전기 부품을 찾아야 합니다.");

    setMessage(state.message);
    overlay.style.display = "none";
    updatePanels();
}

function setMessage(msg) {
    state.message = msg;
    messageBar.innerHTML = msg;
}

function addLog(msg) {
    state.logs.unshift(msg);
    if (state.logs.length > 8) {
        state.logs.pop();
    }
    updatePanels();
}

function updatePanels() {
    let objective = "";

    if (!state.hasKeycard) {
        objective = "1) <b>출입카드</b>를 찾아 잠긴 보안문을 열어.";
    } else if (!state.hasFuse) {
        objective = "2) <b>퓨즈</b>를 찾아. 발전기 수리에 필요해.";
    } else if (!state.hasBattery) {
        objective = "3) <b>배터리</b>를 찾아. 비상 발전기에 필요해.";
    } else if (!state.powerOn) {
        objective = "4) <b>발전기</b>를 작동시켜 병원 전원을 복구해.";
    } else if (!state.hasMasterKey) {
        objective = "5) 보안 구역에서 <b>마스터 키</b>를 찾아.";
    } else {
        objective = "6) <b>엘리베이터</b>로 가서 병원에서 탈출해!";
    }

    objectiveBox.innerHTML = objective;

    const mins = Math.floor(state.time / 60);
    const secs = Math.max(0, Math.floor(state.time % 60)).toString().padStart(2, "0");
    const hearts = "❤️".repeat(Math.max(0, state.hearts));

    statusBox.innerHTML = `
        <div class="hud-line"><b>남은 시간</b> : ${mins}:${secs}</div>
        <div class="hud-line"><b>체력</b> : ${hearts || "없음"}</div>
        <div class="hud-line"><b>전원 상태</b> : ${state.powerOn ? "✅ 복구됨" : "❌ 꺼짐"}</div>
        <div class="hud-line"><b>탈출 가능 여부</b> : ${canEscape() ? "✅ 가능" : "❌ 아직 불가"}</div>
    `;

    inventoryBox.innerHTML = `
        <div class="inventory-item">${state.hasKeycard ? "🪪 출입카드" : "⬜ 출입카드 없음"}</div>
        <div class="inventory-item">${state.hasFuse ? "🧰 퓨즈" : "⬜ 퓨즈 없음"}</div>
        <div class="inventory-item">${state.hasBattery ? "🔋 배터리" : "⬜ 배터리 없음"}</div>
        <div class="inventory-item">${state.hasMasterKey ? "🗝️ 마스터 키" : "⬜ 마스터 키 없음"}</div>
    `;

    logBox.innerHTML = state.logs.map(log => `<div class="log">${log}</div>`).join("");
}

function canEscape() {
    return state.powerOn && state.hasMasterKey;
}

function isObstacle(ch) {
    return ["#", "W", "T", "H", "Q", "N", "V"].includes(ch);
}

function isBlockedTile(tx, ty) {
    if (tx < 0 || ty < 0 || tx >= COLS || ty >= ROWS) {
        return true;
    }

    const ch = MAP[ty][tx];

    if (isObstacle(ch)) return true;

    if (ch === "C" && !state.hasKeycard) return true;
    if (ch === "D" && !state.powerOn) return true;

    return false;
}

function collidesWall(nx, ny) {
    const points = [
        {x: nx, y: ny},
        {x: nx + player.w - 1, y: ny},
        {x: nx, y: ny + player.h - 1},
        {x: nx + player.w - 1, y: ny + player.h - 1}
    ];

    for (const p of points) {
        const tx = Math.floor(p.x / TILE);
        const ty = Math.floor(p.y / TILE);
        if (isBlockedTile(tx, ty)) return true;
    }
    return false;
}

function movePlayer(dt = 0.016) {
    let dx = 0;
    let dy = 0;

    player.walking = false;

    if (keys["ArrowLeft"]) {
        dx -= 1;
        player.facing = "left";
        player.walking = true;
    }
    if (keys["ArrowRight"]) {
        dx += 1;
        player.facing = "right";
        player.walking = true;
    }
    if (keys["ArrowUp"]) {
        dy -= 1;
        player.facing = "up";
        player.walking = true;
    }
    if (keys["ArrowDown"]) {
        dy += 1;
        player.facing = "down";
        player.walking = true;
    }

    if (dx !== 0 && dy !== 0) {
        dx *= 0.7071;
        dy *= 0.7071;
    }

    const mx = dx * player.speed;
    const my = dy * player.speed;

    if (!collidesWall(player.x + mx, player.y)) {
        player.x += mx;
    }

    if (!collidesWall(player.x, player.y + my)) {
        player.y += my;
    }

    if (player.walking) {
        player.walkTimer += dt;
        if (player.walkTimer > 0.16) {
            player.walkFrame = player.walkFrame === 0 ? 1 : 0;
            player.walkTimer = 0;
        }
    } else {
        player.walkFrame = 0;
    }
}

function playerCenter() {
    return {
        x: player.x + player.w / 2,
        y: player.y + player.h / 2
    };
}

function isNearTile(ch, dist = 32) {
    const pos = findTile(ch);
    if (!pos) return false;

    const c = playerCenter();
    const t = tileCenter(pos.x, pos.y);

    return Math.hypot(c.x - t.x, c.y - t.y) <= dist;
}

function interact() {
    if (state.won || state.lost) return;

    if (isNearTile("K") && !state.hasKeycard) {
        state.hasKeycard = true;
        setMessage("🪪 출입카드를 주웠어! 이제 파란 보안문을 열 수 있어.");
        addLog("간호 구역에서 출입카드를 발견했습니다.");
        updatePanels();
        return;
    }

    if (isNearTile("F") && !state.hasFuse) {
        state.hasFuse = true;
        setMessage("🧰 퓨즈를 주웠어! 발전기 수리에 쓸 수 있어.");
        addLog("검사실 근처에서 퓨즈를 확보했습니다.");
        updatePanels();
        return;
    }

    if (isNearTile("B") && !state.hasBattery) {
        state.hasBattery = true;
        setMessage("🔋 배터리를 주웠어! 비상 발전기에 필요해.");
        addLog("창고 구역에서 대형 배터리를 찾았습니다.");
        updatePanels();
        return;
    }

    if (isNearTile("P")) {
        if (state.powerOn) {
            setMessage("⚡ 이미 병원 전원이 복구되어 있어.");
            return;
        }

        if (state.hasFuse && state.hasBattery) {
            state.powerOn = true;
            ghosts[1].active = true;
            ghosts[2].active = true;
            setMessage("⚡ 발전기가 작동했어! 병원 전원이 복구되었어.");
            addLog("비상 발전기를 복구했습니다.");
            addLog("추가 순찰 그림자가 움직이기 시작했습니다.");
            updatePanels();
        } else {
            const need = [];
            if (!state.hasFuse) need.push("퓨즈");
            if (!state.hasBattery) need.push("배터리");
            setMessage("⚠️ 발전기를 고치려면 " + need.join(", ") + "가 필요해.");
        }
        return;
    }

    if (isNearTile("M") && !state.hasMasterKey) {
        if (!state.powerOn) {
            setMessage("🚪 보안 구역이 잠겨 있어. 먼저 전원을 복구해야 해.");
            return;
        }
        state.hasMasterKey = true;
        setMessage("🗝️ 마스터 키를 손에 넣었어! 이제 엘리베이터를 사용할 수 있을지도 몰라.");
        addLog("원장실 안쪽에서 마스터 키를 확보했습니다.");
        updatePanels();
        return;
    }

    if (isNearTile("E")) {
        if (canEscape()) {
            state.won = true;
            setMessage("🎉 탈출 성공!");
            addLog("엘리베이터 작동 성공. 탈출 완료.");

            showOverlay(
                "ESCAPED!",
                "엘리베이터를 작동시켜 병원에서 탈출하는 데 성공했어.<br><br>" +
                "남은 체력 : " + "❤️".repeat(state.hearts) + "<br>" +
                "남은 시간 : " +
                Math.floor(state.time / 60) + ":" +
                Math.floor(state.time % 60).toString().padStart(2, "0")
            );
        } else {
            const need = [];
            if (!state.powerOn) need.push("전원 복구");
            if (!state.hasMasterKey) need.push("마스터 키");
            setMessage("🚪 엘리베이터를 쓰려면 아직 " + need.join(", ") + "가 필요해.");
        }
        return;
    }

    if (isNearTile("C") && !state.hasKeycard) {
        setMessage("🪪 이 파란 보안문을 열려면 출입카드가 필요해.");
        return;
    }

    if (isNearTile("D") && !state.powerOn) {
        setMessage("⚡ 이 문은 전원이 복구되어야 열려.");
        return;
    }

    setMessage("여기서는 지금 할 수 있는 상호작용이 없어.");
}

function showOverlay(title, text) {
    overlayBox.innerHTML = `
        <div class="overlay-title">${title}</div>
        <div class="overlay-text">${text}</div>
        <button class="button" onclick="resetGame()">다시 시작</button>
        <div class="small">R 키를 눌러도 재시작할 수 있어.</div>
    `;
    overlay.style.display = "flex";
}

function checkGameOver() {
    if (state.time <= 0 && !state.won && !state.lost) {
        state.lost = true;
        setMessage("⏰ 시간이 다 되었어...");
        addLog("06:00 — 탈출에 실패했습니다.");
        showOverlay(
            "GAME OVER",
            "시간이 지나 버렸어.<br><br>병원에서 빠져나오지 못했어."
        );
    }

    if (state.hearts <= 0 && !state.won && !state.lost) {
        state.lost = true;
        setMessage("💀 더 이상 버틸 수 없어...");
        addLog("그림자에게 여러 번 붙잡혔습니다.");
        showOverlay(
            "GAME OVER",
            "체력이 모두 소진되었어."
        );
    }
}

function resetPlayerPosition() {
    const s = findTile("S");
    player.x = s.x * TILE + 2;
    player.y = s.y * TILE - 2;
}

function rectsOverlap(a, b) {
    return (
        a.x < b.x + b.w &&
        a.x + a.w > b.x &&
        a.y < b.y + b.h &&
        a.y + a.h > b.y
    );
}

function moveGhost(g) {
    if (!g.active) return;

    const target = g.path[g.idx];
    const cx = g.x + g.w / 2;
    const cy = g.y + g.h / 2;

    const dx = target.x - cx;
    const dy = target.y - cy;
    const dist = Math.hypot(dx, dy);

    if (dist < 2) {
        g.idx = (g.idx + 1) % g.path.length;
        return;
    }

    g.x += (dx / dist) * g.speed;
    g.y += (dy / dist) * g.speed;
}

function updateGhosts(dt) {
    if (invuln > 0) {
        invuln -= dt;
    }

    ghosts.forEach(g => {
        moveGhost(g);

        if (!state.won && !state.lost && invuln <= 0 && rectsOverlap(player, g)) {
            state.hearts -= 1;
            invuln = 1.2;
            resetPlayerPosition();
            setMessage("👻 그림자에게 붙잡혔어! 체력이 1 감소했어.");
            addLog("그림자 순찰자와 충돌했습니다. 체력 감소.");
            updatePanels();
            checkGameOver();
        }
    });
}

function drawPixelRect(x, y, w, h, color) {
    ctx.fillStyle = color;
    ctx.fillRect(Math.round(x), Math.round(y), w, h);
}

function drawFloor() {
    for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
            const ch = MAP[y][x];
            if (ch !== "#") {
                const color = FLOOR_COLORS[(x + y) % FLOOR_COLORS.length];
                drawPixelRect(x * TILE, y * TILE, TILE, TILE, color);

                ctx.fillStyle = "rgba(255,255,255,0.10)";
                ctx.fillRect(x * TILE + 6, y * TILE + 6, 4, 4);
                ctx.fillRect(x * TILE + 22, y * TILE + 20, 3, 3);
            }
        }
    }
}

function drawWalls() {
    for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
            if (MAP[y][x] === "#") {
                drawPixelRect(x * TILE, y * TILE, TILE, TILE, "#355360");
                drawPixelRect(x * TILE + 2, y * TILE + 2, TILE - 4, TILE - 4, "#4d6d79");
                drawPixelRect(x * TILE + 5, y * TILE + 5, TILE - 10, TILE - 10, "#63838e");
            }
        }
    }
}

function drawWindow(px, py) {
    drawPixelRect(px + 4, py + 4, 24, 20, "#ebf7fb");
    drawPixelRect(px + 6, py + 6, 20, 16, "#7eb8d6");
    drawPixelRect(px + 15, py + 6, 2, 16, "#dff5ff");
    drawPixelRect(px + 6, py + 13, 20, 2, "#dff5ff");
    drawPixelRect(px + 3, py + 3, 26, 22, "#9fb7c1");
}

function drawDesk(px, py) {
    drawPixelRect(px + 4, py + 10, 24, 12, "#a6805d");
    drawPixelRect(px + 6, py + 8, 20, 4, "#c59c73");
    drawPixelRect(px + 6, py + 22, 3, 8, "#876349");
    drawPixelRect(px + 23, py + 22, 3, 8, "#876349");
}

function drawBed(px, py) {
    drawPixelRect(px + 3, py + 8, 26, 14, "#e9f1f5");
    drawPixelRect(px + 4, py + 9, 8, 5, "#cfe2ea");
    drawPixelRect(px + 12, py + 9, 16, 12, "#f7fbfd");
    drawPixelRect(px + 2, py + 22, 3, 6, "#8ca0a9");
    drawPixelRect(px + 26, py + 22, 3, 6, "#8ca0a9");
}

function drawWheelchair(px, py) {
    drawPixelRect(px + 6, py + 8, 10, 6, "#6f8ca3");
    drawPixelRect(px + 12, py + 5, 3, 5, "#6f8ca3");
    drawPixelRect(px + 5, py + 15, 7, 7, "#465862");
    drawPixelRect(px + 16, py + 15, 8, 8, "#465862");
    drawPixelRect(px + 15, py + 10, 6, 2, "#7e97ac");
}

function drawNurseStation(px, py) {
    drawPixelRect(px + 4, py + 10, 24, 14, "#f0f5f7");
    drawPixelRect(px + 6, py + 8, 20, 3, "#9bc8d8");
    drawPixelRect(px + 10, py + 13, 12, 5, "#80b1c0");
}

function drawVending(px, py) {
    drawPixelRect(px + 6, py + 3, 18, 26, "#c85e66");
    drawPixelRect(px + 8, py + 6, 14, 10, "#deeff7");
    drawPixelRect(px + 10, py + 18, 10, 4, "#f6e18b");
    drawPixelRect(px + 12, py + 24, 6, 2, "#505f66");
}

function drawDoorsAndObjects() {
    for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
            const ch = MAP[y][x];
            const px = x * TILE;
            const py = y * TILE;

            if (ch === "W") drawWindow(px, py);
            if (ch === "T") drawDesk(px, py);
            if (ch === "H") drawBed(px, py);
            if (ch === "Q") drawWheelchair(px, py);
            if (ch === "N") drawNurseStation(px, py);
            if (ch === "V") drawVending(px, py);

            if (ch === "C") {
                drawPixelRect(px + 4, py + 2, 24, 28, state.hasKeycard ? "#6fa98c" : "#5e88be");
                drawPixelRect(px + 8, py + 6, 16, 20, state.hasKeycard ? "#8ec3a8" : "#7ca2d0");
                drawPixelRect(px + 20, py + 16, 3, 3, "#f5f0d5");
            }

            if (ch === "D") {
                drawPixelRect(px + 4, py + 2, 24, 28, state.powerOn ? "#86b48e" : "#8f6d45");
                drawPixelRect(px + 8, py + 6, 16, 20, state.powerOn ? "#9cd2a7" : "#a98457");
                drawPixelRect(px + 20, py + 16, 3, 3, "#f6efd6");
            }

            if (ch === "E") {
                drawPixelRect(px + 2, py + 2, 28, 28, "#758b93");
                drawPixelRect(px + 5, py + 4, 10, 24, "#a7bcc3");
                drawPixelRect(px + 17, py + 4, 10, 24, "#a7bcc3");
                drawPixelRect(px + 15, py + 14, 2, 4, "#445860");
                drawPixelRect(px + 10, py + 8, 12, 4, state.powerOn ? "#95f089" : "#d96e6e");
            }

            if (ch === "P") {
                drawPixelRect(px + 2, py + 6, 28, 20, "#58707a");
                drawPixelRect(px + 6, py + 10, 20, 12, "#364952");
                drawPixelRect(px + 9, py + 13, 4, 4, state.powerOn ? "#97ff8d" : "#d66e6e");
                drawPixelRect(px + 17, py + 13, 4, 4, state.powerOn ? "#97ff8d" : "#f0cc5f");
            }
        }
    }
}

function drawItems() {
    for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
            const ch = MAP[y][x];
            const px = x * TILE;
            const py = y * TILE;

            if (ch === "K" && !state.hasKeycard) {
                drawPixelRect(px + 7, py + 11, 18, 10, "#6fa8ff");
                drawPixelRect(px + 10, py + 14, 4, 3, "#d9f1ff");
                drawPixelRect(px + 18, py + 14, 4, 3, "#36506d");
            }

            if (ch === "F" && !state.hasFuse) {
                drawPixelRect(px + 10, py + 8, 12, 16, "#e8c85e");
                drawPixelRect(px + 9, py + 9, 14, 4, "#fff2ab");
                drawPixelRect(px + 11, py + 20, 10, 2, "#8e6c1f");
            }

            if (ch === "B" && !state.hasBattery) {
                drawPixelRect(px + 10, py + 7, 12, 18, "#65bd71");
                drawPixelRect(px + 13, py + 4, 6, 4, "#bcd2d9");
                drawPixelRect(px + 13, py + 12, 6, 2, "#dfffe0");
            }

            if (ch === "M" && !state.hasMasterKey) {
                drawPixelRect(px + 10, py + 12, 10, 4, "#efc04f");
                drawPixelRect(px + 18, py + 11, 5, 6, "#efc04f");
                drawPixelRect(px + 21, py + 12, 2, 2, "#8e6a13");
            }
        }
    }
}

function drawRoomLabels() {
    ctx.fillStyle = "rgba(20,45,58,0.78)";
    ctx.font = "10px monospace";

    ctx.fillText("LOBBY", 42, 28);
    ctx.fillText("WINDOW", 176, 28);
    ctx.fillText("NURSE", 275, 154);
    ctx.fillText("XRAY", 429, 248);
    ctx.fillText("STORAGE", 53, 315);
    ctx.fillText("GEN", 43, 411);
    ctx.fillText("DIRECTOR", 434, 506);
    ctx.fillText("CAFE", 746, 539);
    ctx.fillText("EXIT", 812, 28);
}

function drawPlayer() {
    const x = Math.round(player.x);
    const y = Math.round(player.y);

    if (invuln > 0 && Math.floor(invuln * 10) % 2 === 0) {
        return;
    }

    drawPixelRect(x + 4, y + 29, 20, 4, "rgba(25,45,55,0.28)");

    const hair = "#5a382b";

    drawPixelRect(x + 7, y + 1, 13, 4, hair);
    drawPixelRect(x + 5, y + 4, 17, 5, hair);
    drawPixelRect(x + 4, y + 7, 4, 7, hair);
    drawPixelRect(x + 19, y + 7, 4, 7, hair);

    drawPixelRect(x + 7, y + 7, 13, 9, "#f3c5a5");

    drawPixelRect(x + 5, y + 9, 2, 4, "#e8b493");
    drawPixelRect(x + 20, y + 9, 2, 4, "#e8b493");

    if (player.facing === "down") {
        drawPixelRect(x + 9, y + 10, 2, 2, "#2d3538");
        drawPixelRect(x + 16, y + 10, 2, 2, "#2d3538");
        drawPixelRect(x + 12, y + 14, 4, 1, "#a76e68");
    }

    if (player.facing === "left") {
        drawPixelRect(x + 8, y + 10, 2, 2, "#2d3538");
        drawPixelRect(x + 6, y + 13, 2, 1, "#a76e68");
    }

    if (player.facing === "right") {
        drawPixelRect(x + 17, y + 10, 2, 2, "#2d3538");
        drawPixelRect(x + 19, y + 13, 2, 1, "#a76e68");
    }

    if (player.facing === "up") {
        drawPixelRect(x + 9, y + 9, 2, 1, "#2d3538");
        drawPixelRect(x + 16, y + 9, 2, 1, "#2d3538");
    }

    drawPixelRect(x + 11, y + 16, 6, 3, "#e9b695");

    drawPixelRect(x + 8, y + 18, 11, 8, "#63a6b4");

    drawPixelRect(x + 4, y + 18, 6, 10, "#f4f7f7");
    drawPixelRect(x + 17, y + 18, 6, 10, "#f4f7f7");
    drawPixelRect(x + 9, y + 18, 3, 10, "#ffffff");
    drawPixelRect(x + 15, y + 18, 3, 10, "#ffffff");

    drawPixelRect(x + 12, y + 18, 1, 10, "#b9cdd2");
    drawPixelRect(x + 14, y + 18, 1, 10, "#b9cdd2");

    drawPixelRect(x + 17, y + 20, 4, 3, "#80b7d2");

    drawPixelRect(x + 2, y + 19, 3, 8, "#f4f7f7");
    drawPixelRect(x + 22, y + 19, 3, 8, "#f4f7f7");

    drawPixelRect(x + 2, y + 26, 3, 3, "#f0bea0");
    drawPixelRect(x + 22, y + 26, 3, 3, "#f0bea0");

    const pants = "#354f72";

    if (player.walking && player.walkFrame === 1) {
        drawPixelRect(x + 7, y + 27, 5, 3, pants);
        drawPixelRect(x + 16, y + 26, 5, 4, pants);

        drawPixelRect(x + 5, y + 30, 7, 2, "#283139");
        drawPixelRect(x + 16, y + 30, 7, 2, "#283139");
    } else {
        drawPixelRect(x + 7, y + 26, 5, 4, pants);
        drawPixelRect(x + 15, y + 26, 5, 4, pants);

        drawPixelRect(x + 6, y + 30, 6, 2, "#283139");
        drawPixelRect(x + 15, y + 30, 6, 2, "#283139");
    }

    drawPixelRect(x + 11, y + 19, 1, 5, "#35464d");
    drawPixelRect(x + 12, y + 23, 4, 1, "#35464d");
    drawPixelRect(x + 16, y + 22, 2, 2, "#35464d");
}

function drawGhost(g) {
    if (!g.active) return;

    const x = Math.round(g.x);
    const y = Math.round(g.y);

    drawPixelRect(x + 3, y + 2, 14, 12, g.color);
    drawPixelRect(x + 5, y + 14, 3, 5, g.color);
    drawPixelRect(x + 9, y + 14, 3, 5, g.color);
    drawPixelRect(x + 13, y + 14, 3, 5, g.color);

    drawPixelRect(x + 6, y + 6, 2, 2, "#fffbff");
    drawPixelRect(x + 12, y + 6, 2, 2, "#fffbff");
}

function drawDarkness() {
    if (state.powerOn) return;

    const c = playerCenter();

    ctx.fillStyle = "rgba(3,15,24,0.43)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.save();
    ctx.globalCompositeOperation = "destination-out";

    const radius = 145;
    const grad = ctx.createRadialGradient(c.x, c.y, 18, c.x, c.y, radius);
    grad.addColorStop(0, "rgba(0,0,0,1)");
    grad.addColorStop(1, "rgba(0,0,0,0)");

    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(c.x, c.y, radius, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
}

function drawHud() {
    ctx.fillStyle = "rgba(15,36,46,0.75)";
    ctx.fillRect(0, 0, canvas.width, 24);

    ctx.font = "12px monospace";
    ctx.fillStyle = "#ffffff";

    const mins = Math.floor(state.time / 60);
    const secs = Math.max(0, Math.floor(state.time % 60)).toString().padStart(2, "0");

    ctx.fillText("TIME " + mins + ":" + secs, 10, 16);
    ctx.fillText("HP " + "♥".repeat(Math.max(0, state.hearts)), 170, 16);
    ctx.fillText("POWER " + (state.powerOn ? "ON" : "OFF"), 300, 16);
}

function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawFloor();
    drawWalls();
    drawDoorsAndObjects();
    drawItems();
    drawRoomLabels();

    ghosts.forEach(g => drawGhost(g));
    drawPlayer();

    drawDarkness();
    drawHud();
}

function update(dt) {
    if (state.won || state.lost) return;

    state.time -= dt;
    if (state.time < 0) state.time = 0;

    movePlayer(dt);
    updateGhosts(dt);

    updatePanels();
    checkGameOver();
}

function gameLoop(now) {
    const dt = Math.min((now - lastTime) / 1000, 0.05);
    lastTime = now;

    update(dt);
    render();

    requestAnimationFrame(gameLoop);
}

window.addEventListener("keydown", (e) => {
    if (["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", " "].includes(e.key)) {
        e.preventDefault();
    }

    keys[e.key] = true;

    if (e.key === " " || e.key === "Enter") {
        interact();
    }

    if (e.key.toLowerCase() === "r") {
        resetGame();
    }
});

window.addEventListener("keyup", (e) => {
    keys[e.key] = false;
});

canvas.addEventListener("click", () => {
    canvas.focus();
    setMessage("게임 화면에 포커스가 맞춰졌어. 방향키로 움직일 수 있어.");
});

window.addEventListener("load", () => {
    resetGame();
    canvas.focus();
    requestAnimationFrame(gameLoop);
});
</script>
</body>
</html>
"""

components.html(
    game_html,
    height=1080,
    scrolling=False
)

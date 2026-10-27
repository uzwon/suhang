// ============================================================
// HTML 요소
// ============================================================

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
ctx.imageSmoothingEnabled = false;

// 게임 메시지
const messageBar = document.getElementById("messageBar");

// 오른쪽 UI
const objectiveBox = document.getElementById("objectiveBox");
const statusBox = document.getElementById("statusBox");
const progressBox = document.getElementById("progressBox");
const progressTitle = document.getElementById("progressTitle");
const logBox = document.getElementById("logBox");
const stageBox = document.getElementById("stageBox");
const subtitleText = document.getElementById("subtitleText");

// 결과 Overlay
const overlay = document.getElementById("overlay");
const overlayBox = document.getElementById("overlayBox");

// ============================================================
// 프롤로그 관련 HTML 요소
// ============================================================
// 프롤로그 전체 화면
const prologueOverlay = document.getElementById("prologueOverlay");

// 프롤로그 제목
const prologueTitle = document.getElementById("prologueTitle");

// 프롤로그 설명
const prologueText = document.getElementById("prologueText");

// 프롤로그 하단 팁
const tutorialTip = document.getElementById("tutorialTip");

// 현재 페이지 번호
const prologuePageNumber = document.getElementById("prologuePageNumber");

// 이전 / 다음 버튼
const previousTutorialButton = document.getElementById(
  "previousTutorialButton",
);
const nextTutorialButton = document.getElementById("nextTutorialButton");

// 프롤로그용 그림 Canvas
const tutorialCanvas = document.getElementById("tutorialCanvas");
const tutorialCtx = tutorialCanvas.getContext("2d");
tutorialCtx.imageSmoothingEnabled = false;

// ============================================================
// 맵 설정
// ============================================================

const TILE = 32;
const COLS = 33;
const ROWS = 20;

// 거리: 타일, 각도: 라디안, 회전 속도: 라디안/초.
const VISION_RADIUS = 2.5;
const FLASHLIGHT_DISTANCE = 7;
const FLASHLIGHT_ANGLE = 75 * Math.PI / 180;
const VISION_TURN_SPEED = 10;
const VISION_REVERSE_SPEED = 32;
const VISION_DIAGONAL_HOLD = 0.1;
const EXPLORED_DARKNESS = 0.78;
const UNEXPLORED_DARKNESS = 0.995;
const PRESENCE_DISTANCE = 6;
const GHOST_SIGHT_DISTANCE = 5;
const GHOST_SIGHT_ANGLE = Math.PI / 2;
const GHOST_NEAR_DISTANCE = 1.5;
const GHOST_REACTION_TIME = 0.4;
const GHOST_SEARCH_TIME = 2;
const GHOST_CORNER_GRACE = 2.5;
const GHOST_CHASE_MULTIPLIER = 3.6;
const fogCanvas = document.createElement("canvas");
const fogContext = fogCanvas.getContext("2d");

// ============================================================
// 스테이지 데이터
// ============================================================

const LEVELS = [
  // ========================================================
  // STAGE 1
  // ========================================================

  {
    type: "collect",
    title: "STAGE 1 · 정전된 본관",
    story:
      "본관 전체가 정전됐다. 부품을 찾아 발전기를 수리하고 추격을 피해 엘리베이터로 탈출하라.",
    time: 430,
    palette: {
      floor1: "#b6c8ce",
      floor2: "#adc1c8",
      wall1: "#334f5b",
      wall2: "#4d6974",
      wall3: "#607d87",
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
      "#################################",
    ],
    records: [
      {
        x: 12,
        y: 8,
        text: "기록 1: 정전 직전 자동문 제어기에 이상 신호가 남아 있다.",
      },
      {
        x: 26,
        y: 15,
        text: "기록 2: 발전기실에서 반복되는 경보음이 기록되었다.",
      },
    ],
  },

  // ========================================================
  // STAGE 2
  // ========================================================

  {
    type: "switch",
    title: "STAGE 2 · 격리 연구동",
    story:
      "격리 시스템이 잠겼다. 연구 메모 또는 CCTV에서 순서를 확인하고 세 단말기를 올바르게 작동시켜라.",
    time: 400,
    palette: {
      floor1: "#bacbbd",
      floor2: "#adbfaf",
      wall1: "#304c47",
      wall2: "#476a62",
      wall3: "#5c8379",
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
      "#################################",
    ],
    records: [
      {
        x: 27,
        y: 4,
        text: "기록 3: 격리 단말기의 순서는 매 야간 점검 때 무작위로 변경된다.",
      },
      {
        x: 6,
        y: 17,
        text: "기록 4: 잘못된 입력은 격리 시스템을 초기화한다.",
      },
    ],
  },

  // ========================================================
  // STAGE 3
  // ========================================================

  {
    type: "rescue",
    title: "STAGE 3 · 옥상 연결 병동",
    story:
      "병동에 남은 환자를 찾아 상태를 안정화한 뒤 대피구역까지 직접 데려와라. 세 명 모두 구조하면 마지막 추격이 시작된다.",
    time: 520,
    palette: {
      floor1: "#c7c3d4",
      floor2: "#b8b4c8",
      wall1: "#44425b",
      wall2: "#5b5875",
      wall3: "#716d8f",
    },
    map: [
      "#################################",
      "#SY..W..h..T....................#",
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
      "#################################",
    ],
    patientCandidates: [
      {
        x: 5,
        y: 4,
      },
      {
        x: 14,
        y: 6,
      },
      {
        x: 24,
        y: 7,
      },
      {
        x: 11,
        y: 13,
      },
      {
        x: 20,
        y: 15,
      },
      {
        x: 27,
        y: 11,
      },
    ],
    records: [
      {
        x: 8,
        y: 16,
        text: "기록 5: 옥상 통로는 모든 병동 인원이 확인된 뒤에만 개방된다.",
      },
      {
        x: 28,
        y: 6,
        text: "기록 6: 야간 대피 규정은 환자 확인을 우선하도록 한다.",
      },
    ],
  },
];

// ============================================================
// 게임 핵심 변수
// ============================================================

let currentLevelIndex = 0;

// 플레이어 정보
let player = null;

// 현재 스테이지 상태
let state = null;

// 그림자 적 배열
let ghosts = [];

// 현재 눌린 키
let keys = {};

// 그림자 충돌 직후 무적시간
let invulnerable = 0;

// 프레임 시간 계산용
let lastTime = performance.now();

// 전체 게임 기록
let meta = null;

// 프롤로그 현재 페이지
let tutorialPageIndex = 0;

// 프롤로그를 완료했는지
let tutorialFinished = false;

// ============================================================
// 프롤로그 페이지 데이터
// ============================================================

const TUTORIAL_PAGES = [
  // --------------------------------------------------------
  // PAGE 1
  // --------------------------------------------------------

  {
    title: "한밤중, 병원에 갇혔다.",
    text: `
            당신은 야간 근무 중이던 의료진입니다.
            갑작스러운 정전과 시스템 오류로 병원의 출입문이 모두 잠겼습니다.
            <br><br>
            병원 곳곳을 직접 탐색하고, 필요한 장비를 찾고,
            시스템을 복구하면서 마지막 옥상 출구까지 도달해야 합니다.
            `,
    tip: "💡 총 3개의 스테이지가 있으며, 스테이지마다 탈출 방법이 달라집니다.",
    scene: "intro",
  },

  // --------------------------------------------------------
  // PAGE 2
  // --------------------------------------------------------

  {
    title: "이 캐릭터가 바로 당신입니다.",
    text: `
            흰색 의사가운을 입은 캐릭터가 플레이어입니다.
            병원의 복도를 직접 돌아다니며 물건을 조사하고 미션을 해결합니다.
            <br><br>
            물체 근처에서 <b>Space</b>를 누르면 아이템 획득,
            기계 조작, 환자 구조 등 다양한 상호작용을 할 수 있습니다.
            `,
    tip: "🎮 방향키 또는 WASD로 이동하고, Shift를 누른 채 움직이면 스태미나를 사용해 빠르게 달릴 수 있습니다.",
    scene: "player",
  },

  // --------------------------------------------------------
  // PAGE 3
  // --------------------------------------------------------

  {
    title: "발전기를 복구하려면 부품이 필요합니다.",
    text: `
            첫 번째 스테이지에서는 <b>출입카드</b>, <b>퓨즈</b>,
            <b>비상 배터리</b>를 찾아야 합니다.
            <br><br>
            특히 퓨즈와 배터리를 확보한 뒤 발전기로 이동하면
            발전기 수리 미니게임을 진행할 수 있습니다.
            노란 포인터가 초록색 영역에 들어왔을 때 Space를 눌러야 성공합니다.
            `,
    tip: "⚡ 발전기를 켜는 순간 병원의 경보가 작동하고 그림자가 플레이어를 추격할 수 있습니다.",
    scene: "items",
  },

  // --------------------------------------------------------
  // PAGE 4
  // --------------------------------------------------------

  {
    title: "이 그림자를 발견하면 조심하세요.",
    text: `
            색깔이 있는 유령 모양의 캐릭터가 병원 안을 돌아다니는 <b>그림자</b>입니다.
            평소에는 정해진 구역을 순찰하지만,
            특정 미션을 완료하거나 경보가 발생하면 플레이어의 위치를 감지하고 직접 추격합니다.
            <br><br>
            그림자와 부딪히면 체력이 감소합니다.
            위험할 때는 달리거나 병원의 <b>숨는 곳</b>에 들어가 추격을 피할 수 있습니다.
            `,
    tip: "🫥 숨는 곳 옆에서 Space → 숨기 / 다시 Space → 나오기. 추격 중에 특히 유용합니다.",
    scene: "enemy",
  },

  // --------------------------------------------------------
  // PAGE 5
  // --------------------------------------------------------

  {
    title: "준비 완료! 이제 병원을 탈출하세요.",
    text: `
            <b>STAGE 1</b>에서는 아이템을 모아 발전기를 수리하고 엘리베이터를 작동시킵니다.
            <br>
            <b>STAGE 2</b>에서는 CCTV와 연구 메모를 이용해 단말기 순서를 찾아야 합니다.
            <br>
            <b>STAGE 3</b>에서는 환자 3명을 찾고 서로 다른 미니게임으로 상태를 안정화한 뒤,
            직접 대피구역까지 호송해야 합니다.
            <br><br>
            병원에는 <b>CCTV</b>와 <b>야간 기록</b>도 숨겨져 있습니다.
            `,
    tip: "🏥 목표를 모르겠을 때는 화면 오른쪽의 '미션'을 확인하세요. 이제 게임을 시작할 수 있습니다.",
    scene: "final",
  },
];

// ============================================================
// 현재 레벨 반환
// ============================================================

function level() {
  return LEVELS[currentLevelIndex];
}

// ============================================================
// 배열 무작위 섞기
// ============================================================

function shuffled(array) {
  const result = [...array];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const temp = result[i];
    result[i] = result[j];
    result[j] = temp;
  }
  return result;
}

// ============================================================
// 특정 타일 찾기
// ============================================================

function findTile(symbol) {
  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      if (level().map[y][x] === symbol) {
        return {
          x: x,
          y: y,
        };
      }
    }
  }
  return null;
}

// ============================================================
// 타일 중앙 좌표
// ============================================================

function tileCenter(x, y) {
  return {
    x: x * TILE + TILE / 2,
    y: y * TILE + TILE / 2,
  };
}

// ============================================================
// 프롤로그 시작
// ============================================================

function showPrologue() {
  // 아직 실제 게임은 시작하지 않는다.
  tutorialPageIndex = 0;
  prologueOverlay.style.display = "flex";
  drawTutorialPage();
}

// ============================================================
// 현재 프롤로그 페이지 표시
// ============================================================

function drawTutorialPage() {
  const page = TUTORIAL_PAGES[tutorialPageIndex];
  prologueTitle.innerHTML = page.title;
  prologueText.innerHTML = page.text;
  tutorialTip.innerHTML = page.tip;
  prologuePageNumber.innerHTML =
    tutorialPageIndex + 1 + " / " + TUTORIAL_PAGES.length;

  // 첫 페이지에서는 이전 버튼 비활성화
  previousTutorialButton.style.visibility =
    tutorialPageIndex === 0 ? "hidden" : "visible";

  // 마지막 페이지에서는 버튼을 '게임 시작'으로 변경
  if (tutorialPageIndex === TUTORIAL_PAGES.length - 1) {
    nextTutorialButton.innerHTML = "게임 시작 ▶";
    nextTutorialButton.className = "start-button";
  } else {
    nextTutorialButton.innerHTML = "다음 →";
    nextTutorialButton.className = "";
  }
  drawTutorialScene(page.scene);
}

// ============================================================
// 다음 프롤로그 페이지
// ============================================================

function nextTutorialPage() {
  if (tutorialPageIndex < TUTORIAL_PAGES.length - 1) {
    tutorialPageIndex += 1;
    drawTutorialPage();
    return;
  }

  // 마지막 페이지에서 게임 시작
  tutorialFinished = true;
  prologueOverlay.style.display = "none";
  startWholeGame();
}

// ============================================================
// 이전 프롤로그 페이지
// ============================================================

function previousTutorialPage() {
  if (tutorialPageIndex > 0) {
    tutorialPageIndex -= 1;
    drawTutorialPage();
  }
}

// ============================================================
// 프롤로그 그림
// ============================================================
// 게임과 같은 스프라이트를 4배로 확대해서 보여 준다.

const TUTORIAL_SCALE = 4;

function tutorialSprite(name, x, y, options = {}) {
  Sprites.draw(tutorialCtx, name, x, y, { scale: TUTORIAL_SCALE, ...options });
}

function tutorialLabel(text, x, y) {
  drawTag(tutorialCtx, text, x, y, "light");
}

// 벽 한 줄과 바닥 타일
function drawTutorialBackground() {
  const size = ART_TILE * TUTORIAL_SCALE;
  for (let x = 0; x < tutorialCanvas.width; x += size) {
    tutorialSprite("s1_wall_front", x, -16);
    for (let y = 48; y < tutorialCanvas.height; y += size) {
      const even = (x / size + (y - 48) / size) % 2 === 0;
      tutorialSprite(even ? "s1_floor_a" : "s1_floor_b", x, y);
    }
  }
  tutorialCtx.fillStyle = "rgba(12, 10, 28, 0.32)";
  tutorialCtx.fillRect(0, 48, tutorialCanvas.width, 8);
}

// 발밑 그림자 + 캐릭터
function tutorialCharacter(name, x, y) {
  tutorialSprite("shadow", x, y);
  tutorialSprite(name, x, y);
}

// 4px 도트로 만든 > 모양 화살표
function drawTutorialChevron(x, y, alpha) {
  tutorialCtx.globalAlpha = alpha;
  tutorialCtx.fillStyle = "#e43b44";
  for (let i = 0; i < 5; i++) {
    tutorialCtx.fillRect(x + i * 4, y + i * 4, 8, 4);
    tutorialCtx.fillRect(x + i * 4, y + 32 - i * 4, 8, 4);
  }
  tutorialCtx.globalAlpha = 1;
}

// SPACE 키 모양
function drawTutorialSpaceKey(x, y, pressed) {
  const g = tutorialCtx;
  const w = 152;
  const h = 60;
  const press = pressed ? 4 : 0;
  g.fillStyle = "#181425";
  g.fillRect(x + 4, y, w - 8, h);
  g.fillRect(x, y + 4, w, h - 8);
  g.fillStyle = "#5a6988";
  g.fillRect(x + 4, y + 4, w - 8, h - 8);
  g.fillStyle = "#c0cbdc";
  g.fillRect(x + 4, y + 4 + press, w - 8, h - 16);
  g.fillStyle = "#ffffff";
  g.fillRect(x + 8, y + 8 + press, w - 16, h - 24);
  g.fillStyle = "#262b44";
  g.font = "bold 24px " + FONT;
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.fillText("SPACE", x + w / 2, y + 26 + press);
}

function drawTutorialScene(scene, time = 0) {
  const g = tutorialCtx;
  g.clearRect(0, 0, tutorialCanvas.width, tutorialCanvas.height);
  drawTutorialBackground();
  const bob = Math.round(Math.sin(time * 3)) * 4;

  // --------------------------------------------------------
  // PAGE 1
  // --------------------------------------------------------

  if (scene === "intro") {
    tutorialSprite("elevator_closed", 120, 208);
    tutorialLabel("잠긴 병원 출구", 120, 226);

    tutorialCharacter(Sprites.anim("doctor_walk_down", time, 6), 390, 204);
    tutorialLabel("플레이어", 390, 226);

    tutorialSprite("shadow", 650, 178, { alpha: 0.6 });
    tutorialSprite(Sprites.anim("ghost_float", time, 4), 650, 140 + bob, { tint: "#957cff", alpha: 0.92 });
    tutorialSprite("ghost_eyes_left_angry", 650, 140 + bob);
    tutorialLabel("정체불명의 그림자", 650, 226);
  }

  // --------------------------------------------------------
  // PAGE 2
  // --------------------------------------------------------

  else if (scene === "player") {
    const directions = ["down", "left", "up", "right"];
    const facing = directions[Math.floor(time / 1.2) % 4];
    tutorialCharacter(Sprites.anim("doctor_walk_" + facing, time, 7), 150, 204);
    tutorialLabel("흰 가운 = 나", 150, 226);

    // 지금 걷는 방향의 키를 노랗게 표시
    const keys = { up: [366, 70], left: [302, 128], down: [366, 128], right: [430, 128] };
    for (const [direction, [x, y]] of Object.entries(keys)) {
      if (direction === facing) {
        g.fillStyle = "#feae34";
        g.fillRect(x - 4, y - 4, 68, 60);
      }
      tutorialSprite("key_" + direction, x, y);
    }
    tutorialLabel("방향키 / WASD", 396, 226);

    drawTutorialSpaceKey(570, 104, time % 1.2 < 0.25);
    tutorialLabel("상호작용", 645, 226);
  }

  // --------------------------------------------------------
  // PAGE 3
  // --------------------------------------------------------

  else if (scene === "items") {
    const items = [
      ["keycard", 90, "출입카드"],
      ["fuse", 230, "퓨즈"],
      ["battery", 370, "비상 배터리"],
    ];
    items.forEach(([name, x, label], index) => {
      const itemBob = Math.round(Math.sin(time * 3 + index)) * 4;
      tutorialSprite("shadow", x, 136, { alpha: 0.7 });
      tutorialSprite(name, x, 134 + itemBob);
      tutorialLabel(label, x, 160);
    });
    tutorialSprite(Sprites.anim("generator_on", time, 6), 560, 150);
    tutorialLabel("발전기", 560, 160);

    // 타이밍 게이지 (게임과 같은 구간)
    const pointer = 0.5 + 0.5 * Math.sin(time * 2.2);
    drawTimingBar(g, pointer, 150, 186, 480, 0.42, 0.58);
    tutorialLabel("노란 포인터를 초록 구간에서 멈추기", 390, 230);
  }

  // --------------------------------------------------------
  // PAGE 4
  // --------------------------------------------------------

  else if (scene === "enemy") {
    const ghostX = 120 + Math.round(Math.sin(time * 2) * 16 / 4) * 4;
    tutorialSprite("shadow", ghostX, 178, { alpha: 0.6 });
    tutorialSprite(Sprites.anim("ghost_float", time, 4), ghostX, 140 + bob, { tint: "#ff74a9", alpha: 0.92 });
    tutorialSprite("ghost_eyes_right_angry", ghostX, 140 + bob);
    tutorialLabel("그림자 · 피해야 함", 130, 226);

    for (let i = 0; i < 3; i++) {
      const offset = (time * 48 + i * 44) % 132;
      drawTutorialChevron(Math.round((236 + offset) / 4) * 4, 124, 1 - offset / 132);
    }

    tutorialCharacter(Sprites.anim("doctor_walk_right", time, 12), 465, 204);
    tutorialLabel("Shift로 달리기", 465, 226);

    tutorialSprite(time % 3 < 1.5 ? "locker" : "locker_hidden", 665, 208);
    tutorialLabel("숨는 곳", 665, 226);
  }

  // --------------------------------------------------------
  // PAGE 5
  // --------------------------------------------------------

  else if (scene === "final") {
    tutorialSprite(Sprites.anim("cctv_on", time, 5), 98, 168);
    tutorialLabel("CCTV", 98, 190);

    tutorialSprite("record", 245, 160 + bob);
    tutorialLabel("야간 기록", 245, 190);

    tutorialCharacter("patient1_down_0", 392, 172);
    Sprites.draw(tutorialCtx, "bubble_alert", 420, 96 + bob, { scale: 3 });
    tutorialLabel("구조할 환자", 392, 190);

    tutorialSprite("evac_zone", 516, 104);
    tutorialLabel("대피 구역", 548, 190);

    tutorialSprite("roof_open", 692, 172);
    tutorialLabel("최종 출구", 692, 190);

    drawTag(g, "탐색 → 퍼즐 → 구조 → 탈출", 390, 226, "focus");
  }
  g.textAlign = "left";
}

// ============================================================
// 전체 게임 시작
// ============================================================

function startWholeGame() {
  meta = {
    totalRecords: 0,
    stageResults: [],
    allPatientsRescued: false,
  };
  currentLevelIndex = 0;
  startStage();
}

// ============================================================
// 스테이지 초기화
// ============================================================

function startStage() {
  const start = findTile("S");
  if (!start) {
    showFatalError("시작 위치를 찾을 수 없습니다.");
    return;
  }

  // ========================================================
  // 플레이어
  // ========================================================

  player = {
    x: start.x * TILE + 1,
    y: start.y * TILE - 4,

    // 실제 충돌 영역
    hitW: 12,
    hitH: 8,
    hitOffsetX: 9,
    hitOffsetY: 20,

    // 기본 걷기 속도
    speed: 160,

    // 현재 보는 방향
    facing: "down",

    // 걷기 애니메이션
    walking: false,
    walkFrame: 0,
    walkTimer: 0,
  };

  // ========================================================
  // 현재 스테이지 상태
  // ========================================================

  state = {
    // 체력
    hearts: 4,

    // 제한시간
    time: level().time,

    // 달리기에 사용하는 스태미나
    stamina: 100,

    // 게임 종료 여부
    won: false,
    lost: false,

    // 숨기 관련
    hidden: false,
    hideSeconds: 0,

    // 로그
    logs: [],

    // ----------------------------------------------------
    // STAGE 1
    // ----------------------------------------------------

    hasKeycard: false,
    hasFuse: false,
    hasBattery: false,
    powerOn: false,
    hasMasterKey: false,

    // ----------------------------------------------------
    // STAGE 2
    // ----------------------------------------------------

    switchProgress: 0,

    // A/B/C 무작위 순서
    sequence: shuffled(["A", "B", "C"]),

    // 순서를 확인했는지
    sequenceKnown: false,

    // ----------------------------------------------------
    // STAGE 3
    // ----------------------------------------------------

    patients: [],

    // 현재 호송 중인 환자 번호
    escortPatientId: null,

    // 마지막 탈출 단계
    finalEscapeStarted: false,

    // ----------------------------------------------------
    // 추격
    // ----------------------------------------------------

    explored: new Uint8Array(COLS * ROWS),
    vision: { angle: Math.PI / 2, target: Math.PI / 2, diagonal: null, pending: null, elapsed: 0 },
    chaseTimer: 0,

    // CCTV 활성시간
    cctvTimer: 0,

    // 현재 미니게임
    miniGame: null,

    // ----------------------------------------------------
    // 야간 기록
    // ----------------------------------------------------

    records: level().records.map((record, index) => ({
      ...record,
      id: index,
      collected: false,
    })),

    // ----------------------------------------------------
    // 이벤트 효과
    // ----------------------------------------------------

    event: {
      blackout: 0,
      enemyBoost: 0,
      alarm: 0,
    },
  };

  // ========================================================
  // STAGE 3 환자 위치 무작위 설정
  // ========================================================

  if (level().type === "rescue") {
    const chosen = shuffled(level().patientCandidates).slice(0, 3);
    state.patients = chosen.map((position, index) => ({
      id: index + 1,
      x: position.x,
      y: position.y,

      // 환자 안정화 여부
      stabilized: false,

      // 현재 따라오는지
      following: false,

      // 최종 구조 완료
      rescued: false,

      // 환자별 미니게임
      mission: ["timing", "direction", "memory"][index],
    }));
  }
  ghosts = createGhosts();
  ghosts.forEach(initializeGhostAI);
  invulnerable = 0;

  // 이 스테이지의 바닥과 벽을 미리 그려 둔다
  staticLayer = buildStaticLayer();
  followTrail = [];
  followPatientId = null;
  state.logs.push("현재 구역 진입 : " + level().title);
  setMessage(level().story);
  subtitleText.innerHTML = level().title + " · Shift 달리기 · Space 상호작용";
  overlay.style.display = "none";
  updatePanels();
  canvas.focus();
}

// ============================================================
// 재시작
// ============================================================

function restartStage() {
  // 프롤로그가 아직 끝나지 않았다면 무시
  if (!tutorialFinished) {
    return;
  }
  startStage();
}

// ============================================================
// 그림자 생성
// ============================================================

function createGhosts() {
  if (currentLevelIndex === 0) {
    return [
      {
        x: 23 * TILE,
        y: 8 * TILE,
        w: 20,
        h: 20,
        speed: 42,
        color: "#9277ff",
        path: [
          tileCenter(24, 8),
          tileCenter(29, 8),
          tileCenter(29, 13),
          tileCenter(24, 13),
        ],
        pathIndex: 1,
      },
    ];
  }
  if (currentLevelIndex === 1) {
    return [
      {
        x: 21 * TILE,
        y: 6 * TILE,
        w: 20,
        h: 20,
        speed: 49,
        color: "#4fd9ab",
        path: [
          tileCenter(21, 6),
          tileCenter(30, 6),
          tileCenter(30, 13),
          tileCenter(21, 13),
        ],
        pathIndex: 1,
      },
      {
        x: 5 * TILE,
        y: 14 * TILE,
        w: 20,
        h: 20,
        speed: 42,
        color: "#94e758",
        path: [
          tileCenter(5, 14),
          tileCenter(12, 14),
          tileCenter(12, 18),
          tileCenter(5, 18),
        ],
        pathIndex: 1,
      },
    ];
  }
  return [
    {
      x: 20 * TILE,
      y: 6 * TILE,
      w: 20,
      h: 20,
      speed: 53,
      color: "#ff74a9",
      path: [
        tileCenter(21, 6),
        tileCenter(28, 6),
        tileCenter(28, 12),
        tileCenter(21, 12),
      ],
      pathIndex: 1,
    },
    {
      x: 8 * TILE,
      y: 14 * TILE,
      w: 20,
      h: 20,
      speed: 47,
      color: "#be8dff",
      path: [
        tileCenter(8, 14),
        tileCenter(17, 14),
        tileCenter(17, 18),
        tileCenter(8, 18),
      ],
      pathIndex: 1,
    },
  ];
}

// ============================================================
// 메시지
// ============================================================

function setMessage(text) {
  messageBar.innerHTML = text;
}

// ============================================================
// 로그
// ============================================================

function addLog(text) {
  state.logs.unshift(text);
  if (state.logs.length > 7) {
    state.logs.pop();
  }
  updatePanels();
}

// ============================================================
// 플레이어 중심
// ============================================================

function playerCenter() {
  return {
    x: player.x + 15,
    y: player.y + 23,
  };
}

// ============================================================
// 특정 위치와 거리 확인
// ============================================================

function nearPos(x, y, distance = 42) {
  const pc = playerCenter();
  const tc = tileCenter(x, y);
  return Math.hypot(pc.x - tc.x, pc.y - tc.y) <= distance;
}

// ============================================================
// 특정 오브젝트 근처인지
// ============================================================

function nearTile(symbol, distance = 42) {
  const tile = findTile(symbol);
  if (!tile) {
    return false;
  }
  return nearPos(tile.x, tile.y, distance);
}

// ============================================================
// 구조 완료 인원
// ============================================================

function rescueCount() {
  if (level().type !== "rescue") {
    return 0;
  }
  return state.patients.filter((patient) => patient.rescued).length;
}

// ============================================================
// 현재 스테이지 기록 수
// ============================================================

function stageRecordCount() {
  return state.records.filter((record) => record.collected).length;
}

// ============================================================
// 오른쪽 UI 업데이트
// ============================================================

// 인벤토리 한 줄 (아이콘 + 이름 + 체크)
function panelItem(done, icon, label, scale = 1) {
  return `
        <div class="item ${done ? "done" : ""}">
            <span class="item-icon">${Sprites.icon(icon, scale)}</span>
            <span class="item-name">${label}</span>
            <span class="check"></span>
        </div>
    `;
}

function updatePanels() {
  stageBox.innerHTML = `
        <b>
            ${level().title}
        </b>
        <p>
            ${level().story}
        </p>
    `;
  const minutes = Math.floor(state.time / 60);
  const seconds = Math.floor(state.time % 60)
    .toString()
    .padStart(2, "0");
  const hearts = [0, 1, 2, 3]
    .map((index) => Sprites.icon(index < state.hearts ? "heart" : "heart_empty", 2))
    .join("");
  const mode = state.hidden
    ? ["숨는 중", "hidden"]
    : state.chaseTimer > 0
      ? ["추격 중", "danger"]
      : ["탐색 중", ""];
  statusBox.innerHTML = `
      <div class="stat-grid">
        <div class="stat">
            <span>진행</span>
            <b>${currentLevelIndex + 1} / 3</b>
        </div>
        <div class="stat">
            <span>남은 시간</span>
            <b class="${state.time < 60 ? "warn" : ""}">${minutes}:${seconds}</b>
        </div>
        <div class="stat">
            <span>체력</span>
            <b class="hearts">${hearts}</b>
        </div>
        <div class="stat">
            <span>스태미나</span>
            <b class="meter ${state.stamina < 30 ? "low" : ""}"><i style="width:${Math.round(state.stamina)}%"></i></b>
        </div>
        <div class="stat">
            <span>상태</span>
            <b class="badge ${mode[1]}">${mode[0]}</b>
        </div>
        <div class="stat">
            <span>야간 기록</span>
            <b>${stageRecordCount()} / ${state.records.length}</b>
        </div>
      </div>
    `;

  // ========================================================
  // STAGE 1
  // ========================================================

  if (level().type === "collect") {
    progressTitle.innerHTML = Sprites.icon("icon_bag", 2, "icon") + "인벤토리";
    let objective = "";
    if (!state.hasKeycard) {
      objective = "① <b>출입카드</b>를 찾아.";
    } else if (!state.hasFuse) {
      objective = "② <b>퓨즈</b>를 찾아.";
    } else if (!state.hasBattery) {
      objective = "③ <b>비상 배터리</b>를 찾아.";
    } else if (!state.powerOn) {
      objective = "④ <b>발전기 미니게임</b>을 성공시켜.";
    } else if (!state.hasMasterKey) {
      objective = "⑤ 추격을 피하면서 <b>마스터 키</b>를 찾아.";
    } else {
      objective = "⑥ <b>엘리베이터</b>로 탈출해.";
    }
    objectiveBox.innerHTML = objective;
    progressBox.innerHTML =
      panelItem(state.hasKeycard, "keycard", "출입카드") +
      panelItem(state.hasFuse, "fuse", "퓨즈") +
      panelItem(state.hasBattery, "battery", "비상 배터리") +
      panelItem(state.powerOn, "icon_bolt", "전원 복구") +
      panelItem(state.hasMasterKey, "master_key", "마스터 키");
  }

  // ========================================================
  // STAGE 2
  // ========================================================

  else if (level().type === "switch") {
    progressTitle.innerHTML = Sprites.icon("icon_terminal", 2, "icon") + "격리 시스템";
    const sequenceText = state.sequenceKnown
      ? state.sequence.join(" → ")
      : "??? → ??? → ???";
    objectiveBox.innerHTML = `
            연구 메모 또는 CCTV에서
            <b>
                단말기 순서
            </b>
            를 확인해.
            <br><br>
            현재 확인된 순서:
            <b>
                ${sequenceText}
            </b>
        `;
    const chips = state.sequence
      .map((symbol, index) => {
        const label = state.sequenceKnown ? symbol : "?";
        const done = index < state.switchProgress ? "done" : "";
        return `<span class="chip ${done}">${label}</span>`;
      })
      .join("");
    progressBox.innerHTML = `
            <div class="item">
                <span class="item-name">단말기 진행</span>
                <b>${state.switchProgress}/3</b>
            </div>
            <div class="chips">${chips}</div>
            <div class="item note">
                잘못 누르면 <b>초기화 + 시간 -20초</b>
            </div>
        `;
  }

  // ========================================================
  // STAGE 3
  // ========================================================

  else {
    progressTitle.innerHTML = Sprites.icon("bubble_heart", 2, "icon") + "구조 현황";
    let objective = "";
    if (state.escortPatientId !== null) {
      objective = `
                환자가 따라오고 있어.
                <br><br>
                시작 지점 옆의
                <b>
                    대피 구역
                </b>
                으로 데려가서 Space를 눌러.
            `;
    } else if (rescueCount() < 3) {
      objective = `
                병원을 탐색해 환자를 찾고
                각각의
                <b>
                    안정화 미니게임
                </b>
                을 완료해.
                <br><br>
                안정화 후 환자를 대피구역까지
                호송해야 해.
            `;
    } else {
      objective = `
                환자 3명 모두 구조 완료!
                <br><br>
                <b>
                    최종 추격을 피해서
                    옥상 출구로 탈출해.
                </b>
            `;
    }
    objectiveBox.innerHTML = objective;
    progressBox.innerHTML = `
            <div class="item">
                <span class="item-name">구조 완료</span>
                <b>${rescueCount()}/3</b>
            </div>
            ${state.patients
              .map((patient) =>
                panelItem(
                  patient.rescued,
                  "patient" + patient.id + "_down_0",
                  "환자 " +
                    patient.id +
                    " · " +
                    (patient.rescued
                      ? "구조 완료"
                      : patient.following
                        ? "호송 중"
                        : patient.stabilized
                          ? "안정화 완료"
                          : "미발견/미처치"),
                ),
              )
              .join("")}
        `;
  }
  logBox.innerHTML = state.logs
    .map((log) => `<div class="log">${log}</div>`)
    .join("");
}

// ============================================================
// 장애물 처리
// ============================================================

function tileBlocked(tx, ty) {
  if (tx < 0 || ty < 0 || tx >= COLS || ty >= ROWS) {
    return true;
  }
  const symbol = level().map[ty][tx];
  if (symbol === "#") {
    return true;
  }

  // STAGE 1 카드 보안문
  if (level().type === "collect" && symbol === "C" && !state.hasKeycard) {
    return true;
  }

  // STAGE 1 전원문
  if (level().type === "collect" && symbol === "D" && !state.powerOn) {
    return true;
  }

  // STAGE 2 출구
  if (level().type === "switch" && symbol === "X" && state.switchProgress < 3) {
    return true;
  }

  // STAGE 3 출구
  if (level().type === "rescue" && symbol === "R" && rescueCount() < 3) {
    return true;
  }
  return false;
}

// ============================================================
// 충돌 판정
// ============================================================

function collisionAt(newX, newY) {
  const left = newX + player.hitOffsetX;
  const right = left + player.hitW - 1;
  const top = newY + player.hitOffsetY;
  const bottom = top + player.hitH - 1;
  const points = [
    {
      x: left,
      y: top,
    },
    {
      x: right,
      y: top,
    },
    {
      x: left,
      y: bottom,
    },
    {
      x: right,
      y: bottom,
    },
  ];
  for (const point of points) {
    const tx = Math.floor(point.x / TILE);
    const ty = Math.floor(point.y / TILE);
    if (tileBlocked(tx, ty)) {
      return true;
    }
  }
  return false;
}

// ============================================================
// 플레이어 이동
// ============================================================

function updatePlayer(dt) {
  if (state.hidden || state.miniGame) {
    return;
  }
  let dx = 0;
  let dy = 0;
  if (keys["ArrowLeft"] || keys["a"] || keys["A"]) {
    dx -= 1;
    player.facing = "left";
  }
  if (keys["ArrowRight"] || keys["d"] || keys["D"]) {
    dx += 1;
    player.facing = "right";
  }
  if (keys["ArrowUp"] || keys["w"] || keys["W"]) {
    dy -= 1;
    player.facing = "up";
  }
  if (keys["ArrowDown"] || keys["s"] || keys["S"]) {
    dy += 1;
    player.facing = "down";
  }
  updateVisionDirection(dx, dy, dt);
  player.walking = dx !== 0 || dy !== 0;

  // 대각선 이동 속도 보정
  if (dx !== 0 && dy !== 0) {
    dx *= 0.707106;
    dy *= 0.707106;
  }

  // Shift + 이동 시 달리기
  const running = keys["Shift"] && player.walking && state.stamina > 0;
  let speed = player.speed;
  if (running) {
    speed = 245;
    state.stamina = Math.max(0, state.stamina - 32 * dt);
  } else {
    state.stamina = Math.min(100, state.stamina + 18 * dt);
  }
  const moveX = dx * speed * dt;
  const moveY = dy * speed * dt;

  // X와 Y 충돌을 따로 검사
  if (!collisionAt(player.x + moveX, player.y)) {
    player.x += moveX;
  }
  if (!collisionAt(player.x, player.y + moveY)) {
    player.y += moveY;
  }
  // 걷기 애니메이션 4프레임 (달릴 때는 더 빠르게)
  if (player.walking) {
    player.walkTimer += dt;
    if (player.walkTimer > (running ? 0.09 : 0.13)) {
      player.walkFrame = (player.walkFrame + 1) % 4;
      player.walkTimer = 0;
    }
  } else {
    player.walkFrame = 0;
  }
}

// ============================================================
// 숨는 곳 확인
// ============================================================

function nearHideSpot() {
  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      if (level().map[y][x] === "h" && nearPos(x, y, 42)) {
        return true;
      }
    }
  }
  return false;
}

// ============================================================
// Space / Enter 상호작용
// ============================================================

function interact() {
  if (!state || state.won || state.lost || !tutorialFinished) {
    return;
  }
  canvas.focus();

  // ========================================================
  // 미니게임 중 Space
  // ========================================================

  if (state.miniGame) {
    if (state.miniGame.type === "generator") {
      finishGeneratorMiniGame();
    } else if (state.miniGame.type === "patientTiming") {
      handlePatientTiming();
    }
    return;
  }

  // ========================================================
  // 숨는 곳에서 나오기
  // ========================================================

  if (state.hidden) {
    state.hidden = false;
    state.hideSeconds = 0;
    setMessage("숨는 곳에서 나왔어.");
    return;
  }

  // ========================================================
  // 숨기
  // ========================================================

  if (nearHideSpot()) {
    state.hidden = true;
    state.hideSeconds = 0;
    setMessage("🫥 숨는 곳에 들어왔어. Space를 다시 누르면 나올 수 있어.");
    return;
  }

  // ========================================================
  // 야간 기록 수집
  // ========================================================

  const record = state.records.find(
    (item) => !item.collected && nearPos(item.x, item.y, 42),
  );
  if (record) {
    record.collected = true;
    meta.totalRecords += 1;
    setMessage("📄 " + record.text);
    addLog("야간 기록 확보.");
    return;
  }

  // ========================================================
  // CCTV
  // ========================================================

  const cctv = findTile("Z");
  if (cctv && nearPos(cctv.x, cctv.y, 42)) {
    state.cctvTimer = 12;
    if (level().type === "switch") {
      state.sequenceKnown = true;
      setMessage(
        "📹 CCTV 확인: 단말기 순서는 " + state.sequence.join(" → ") + " 이야.",
      );
    } else {
      setMessage("📹 CCTV를 확인했어.");
    }
    return;
  }

  // 스테이지별 상호작용
  if (level().type === "collect") {
    interactStage1();
  } else if (level().type === "switch") {
    interactStage2();
  } else {
    interactStage3();
  }
}

// ============================================================
// STAGE 1
// ============================================================

function interactStage1() {
  if (nearTile("K") && !state.hasKeycard) {
    state.hasKeycard = true;
    setMessage("🪪 출입카드를 획득했어.");
    return;
  }
  if (nearTile("F") && !state.hasFuse) {
    state.hasFuse = true;
    setMessage("🧰 퓨즈를 획득했어.");
    return;
  }
  if (nearTile("B") && !state.hasBattery) {
    state.hasBattery = true;
    setMessage("🔋 비상 배터리를 획득했어.");
    return;
  }

  // 발전기
  if (nearTile("P")) {
    if (state.hasFuse && state.hasBattery && !state.powerOn) {
      startGeneratorMiniGame();
      return;
    }
    if (state.powerOn) {
      setMessage("발전기는 이미 작동 중이야.");
      return;
    }
    setMessage("⚠️ 발전기를 켜려면 퓨즈와 비상 배터리가 모두 필요해.");
    return;
  }

  // 마스터 키
  if (nearTile("M") && !state.hasMasterKey) {
    if (!state.powerOn) {
      setMessage("🔒 전원을 먼저 복구해야 해.");
      return;
    }
    state.hasMasterKey = true;
    setMessage("🗝️ 마스터 키를 획득했어.");
    return;
  }

  // 엘리베이터
  if (nearTile("E")) {
    if (state.powerOn && state.hasMasterKey) {
      clearStage();
    } else {
      setMessage("🚪 엘리베이터가 아직 잠겨 있어.");
    }
    return;
  }
  setMessage("주변에 지금 사용할 수 있는 물체가 없어.");
}

// ============================================================
// 발전기 미니게임
// ============================================================

function startGeneratorMiniGame() {
  state.miniGame = {
    type: "generator",

    // 포인터 위치 0~1
    pos: 0,

    // 이동 방향
    dir: 1,
  };
  setMessage("🛠️ 노란 표시가 초록 영역 안에 들어왔을 때 Space를 눌러!");
}

// ============================================================
// 발전기 판정
// ============================================================

function finishGeneratorMiniGame() {
  const game = state.miniGame;
  if (game.pos >= 0.42 && game.pos <= 0.58) {
    state.miniGame = null;
    state.powerOn = true;

    // 발전기 복구 순간 추격 시작
    state.chaseTimer = Infinity;

    // 빨간 경고등
    state.event.alarm = Infinity;
    setMessage(
      "⚡ 발전기 복구 성공! 스테이지를 클리어할 때까지 경보가 울리고 그림자가 추격한다! 달리거나 숨는 곳을 이용해!",
    );
    addLog("발전기 복구 → 그림자 추격 시작.");
  } else {
    state.miniGame = null;
    state.time = Math.max(0, state.time - 10);
    setMessage("❌ 수리 타이밍 실패! 시간 -10초.");
  }
}

// ============================================================
// STAGE 2
// ============================================================

function interactStage2() {
  const note = findTile("L");

  // 연구 메모 확인
  if (note && nearPos(note.x, note.y, 42)) {
    state.sequenceKnown = true;
    setMessage("📝 연구 메모: 단말기 순서는 " + state.sequence.join(" → "));
    return;
  }

  // A/B/C 단말기
  for (const symbol of ["A", "B", "C"]) {
    if (nearTile(symbol)) {
      activateTerminal(symbol);
      return;
    }
  }

  // 제독실 출구
  if (nearTile("X")) {
    if (state.switchProgress === 3) {
      clearStage();
    } else {
      setMessage("☣️ 격리 시스템을 먼저 해제해야 해.");
    }
    return;
  }
  setMessage("주변에 지금 사용할 수 있는 물체가 없어.");
}

// ============================================================
// 단말기 입력
// ============================================================

function activateTerminal(symbol) {
  const expected = state.sequence[state.switchProgress];
  if (symbol === expected) {
    state.switchProgress += 1;
    setMessage("✅ 단말기 " + symbol + " 활성화 성공.");
    if (state.switchProgress === 3) {
      state.chaseTimer = Infinity;
      state.event.alarm = Infinity;
      setMessage("✅ 격리 시스템 해제! 스테이지를 클리어할 때까지 경보가 울리고 그림자가 추격한다!");
    }
  } else {
    state.switchProgress = 0;
    state.time = Math.max(0, state.time - 20);
    setMessage("⚠️ 잘못된 순서! 시스템 초기화 + 시간 -20초.");
  }
}

// ============================================================
// STAGE 3
// ============================================================

function interactStage3() {
  // ========================================================
  // 환자 호송 중
  // ========================================================

  if (state.escortPatientId !== null) {
    // 대피구역 도착
    if (nearTile("Y", 50)) {
      const patient = state.patients.find(
        (item) => item.id === state.escortPatientId,
      );
      patient.following = false;
      patient.rescued = true;
      state.escortPatientId = null;
      setMessage("✅ 환자 " + patient.id + "을 대피구역까지 이동시켰어.");
      addLog("환자 " + patient.id + " 구조 완료.");

      // 3명 모두 구조
      if (rescueCount() === 3) {
        meta.allPatientsRescued = true;
        state.finalEscapeStarted = true;

        // 스테이지 클리어까지 마지막 추격
        state.chaseTimer = Infinity;
        state.event.alarm = Infinity;
        setMessage(
          "🚨 환자 3명 모두 구조 완료! 옥상 출구가 열렸다. 마지막 추격을 피해서 탈출해!",
        );
      }
      return;
    }
    setMessage("🚶 환자를 시작 지점 옆의 대피 구역으로 데려가야 해.");
    return;
  }

  // ========================================================
  // 근처 환자
  // ========================================================

  const patient = state.patients.find(
    (item) => !item.rescued && !item.following && nearPos(item.x, item.y, 43),
  );
  if (patient) {
    // 이미 안정화됐다면 바로 호송
    if (patient.stabilized) {
      startEscort(patient);
      return;
    }
    startPatientMission(patient);
    return;
  }

  // 옥상 출구
  if (nearTile("R")) {
    if (rescueCount() === 3) {
      clearStage();
    } else {
      setMessage("🚪 아직 구조하지 못한 환자가 있어.");
    }
    return;
  }
  setMessage("주변에 상호작용할 대상이 없어.");
}

// ============================================================
// 환자별 미니게임
// ============================================================

function startPatientMission(patient) {
  // ========================================================
  // 환자 1 : 타이밍 게임
  // ========================================================

  if (patient.mission === "timing") {
    state.miniGame = {
      type: "patientTiming",
      patientId: patient.id,
      pos: 0,
      dir: 1,

      // 성공 횟수
      success: 0,
    };
    setMessage("🩺 환자 1 안정화: 초록 구간에 맞춰 Space를 2번 성공시켜.");
    return;
  }

  // ========================================================
  // 환자 2 : 방향키 기억
  // ========================================================

  if (patient.mission === "direction") {
    const choices = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"];
    const sequence = [];
    for (let i = 0; i < 5; i++) {
      sequence.push(choices[Math.floor(Math.random() * choices.length)]);
    }
    state.miniGame = {
      type: "patientDirection",
      patientId: patient.id,

      // 기억해야 하는 방향키 배열
      sequence: sequence,

      // 3초간 보여주기
      reveal: 3,

      // 현재 입력한 위치
      inputIndex: 0,
    };
    setMessage("🧠 환자 2 안정화: 3초 동안 표시되는 방향키 5개를 기억해.");
    return;
  }

  // ========================================================
  // 환자 3 : 숫자 기억
  // ========================================================

  const numbers = [];
  for (let i = 0; i < 5; i++) {
    numbers.push(String(1 + Math.floor(Math.random() * 4)));
  }
  state.miniGame = {
    type: "patientMemory",
    patientId: patient.id,

    // 기억해야 할 숫자 배열
    sequence: numbers,
    reveal: 3,
    inputIndex: 0,
  };
  setMessage("🧠 환자 3 안정화: 숫자 코드 5개를 기억해.");
}

// ============================================================
// 환자 1 타이밍
// ============================================================

function handlePatientTiming() {
  const game = state.miniGame;
  if (game.pos >= 0.4 && game.pos <= 0.6) {
    game.success += 1;
    if (game.success >= 2) {
      finishPatientMission(game.patientId);
    } else {
      setMessage("✅ 1회 성공! 한 번 더 맞춰.");
    }
  } else {
    // 실패하면 성공 횟수 초기화
    game.success = 0;
    state.time = Math.max(0, state.time - 6);
    setMessage("❌ 타이밍 실패. 시간 -6초. 다시 2번 성공해야 해.");
  }
}

// ============================================================
// 환자 2 방향키 입력
// ============================================================

function handleDirectionInput(key) {
  const game = state.miniGame;
  if (!game || game.type !== "patientDirection" || game.reveal > 0) {
    return false;
  }
  const expected = game.sequence[game.inputIndex];
  if (key === expected) {
    game.inputIndex += 1;
    if (game.inputIndex >= game.sequence.length) {
      finishPatientMission(game.patientId);
    } else {
      setMessage("✅ " + game.inputIndex + "/5 입력 성공");
    }
  } else {
    // 지금 게임이 끝났습니다
    state.miniGame = null;
    setMessage("❌ 방향키가 틀렸어. 미니게임이 종료됐어.");
  }
  return true;
}

// ============================================================
// 환자 3 숫자 입력
// ============================================================

function handleMemoryInput(key) {
  const game = state.miniGame;
  if (!game || game.type !== "patientMemory" || game.reveal > 0) {
    return false;
  }
  const expected = game.sequence[game.inputIndex];
  if (key === expected) {
    game.inputIndex += 1;
    if (game.inputIndex >= game.sequence.length) {
      finishPatientMission(game.patientId);
    } else {
      setMessage("✅ " + game.inputIndex + "/5 입력 성공");
    }
  } else {
    state.miniGame = null;
    setMessage("❌ 숫자가 틀렸어. 미니게임이 종료됐어.");
  }
  return true;
}

// ============================================================
// 환자 안정화 완료
// ============================================================

function finishPatientMission(patientId) {
  const patient = state.patients.find((item) => item.id === patientId);
  patient.stabilized = true;
  state.miniGame = null;
  setMessage(
    "✅ 환자 " + patient.id + " 상태 안정화 완료! 이제 대피 구역까지 데려가.",
  );
  startEscort(patient);
}

// ============================================================
// 환자 호송
// ============================================================

function startEscort(patient) {
  if (state.escortPatientId !== null) {
    setMessage("이미 다른 환자를 호송 중이야.");
    return;
  }
  patient.following = true;
  state.escortPatientId = patient.id;
  setMessage(
    "🚶 환자 " +
      patient.id +
      "이 따라오고 있어. 시작 지점 옆 대피 구역으로 이동해.",
  );
}

// ============================================================
// 그림자 이동
// ============================================================

// 상하좌우를 BFS로 탐색하여 최단 경로의 다음 타일을 반환한다.
function findGhostStep(startX, startY, targetX, targetY) {
  if (tileBlocked(targetX, targetY)) return null;
  const start = startY * COLS + startX;
  const target = targetY * COLS + targetX;
  if (start === target) return null;
  const parents = new Int32Array(COLS * ROWS).fill(-1);
  const queue = [start];
  parents[start] = start;
  for (let head = 0; head < queue.length; head++) {
    const current = queue[head];
    const x = current % COLS;
    const y = Math.floor(current / COLS);
    for (const [nx, ny] of [[x, y - 1], [x + 1, y], [x, y + 1], [x - 1, y]]) {
      if (tileBlocked(nx, ny)) continue;
      const next = ny * COLS + nx;
      if (parents[next] !== -1) continue;
      parents[next] = current;
      if (next === target) {
        let step = next;
        while (parents[step] !== start) step = parents[step];
        return tileCenter(step % COLS, Math.floor(step / COLS));
      }
      queue.push(next);
    }
  }
  return null;
}

function ghostCollisionAt(ghost, x, y) {
  return [[x, y], [x + ghost.w - 1, y],
    [x, y + ghost.h - 1], [x + ghost.w - 1, y + ghost.h - 1]]
    .some(([px, py]) => tileBlocked(Math.floor(px / TILE), Math.floor(py / TILE)));
}

function initializeGhostAI(ghost) {
  ghost.mode = "patrol";
  ghost.modeTime = 0;
  ghost.unseenTime = 0;
  ghost.lastSeen = null;
  ghost.alarmActive = false;
  const target = ghost.path[ghost.pathIndex];
  ghost.faceX = target.x - (ghost.x + ghost.w / 2);
  ghost.faceY = target.y - (ghost.y + ghost.h / 2);
}

function ghostSeesPlayer(ghost) {
  if (state.hidden) return false;
  const origin = { x: ghost.x + ghost.w / 2, y: ghost.y + ghost.h / 2 };
  const playerPos = playerCenter();
  const dx = playerPos.x - origin.x, dy = playerPos.y - origin.y;
  const distance = Math.hypot(dx, dy), angle = Math.atan2(dy, dx);
  if (distance > GHOST_SIGHT_DISTANCE * TILE) return false;
  const facing = Math.atan2(ghost.faceY, ghost.faceX);
  const offset = Math.abs(Math.atan2(Math.sin(angle - facing), Math.cos(angle - facing)));
  if (distance > GHOST_NEAR_DISTANCE * TILE && offset > GHOST_SIGHT_ANGLE / 2) return false;
  return castVisionRay(angle, distance, false, origin) >= distance - 0.01;
}

function setGhostMode(ghost, mode) {
  if (ghost.mode === mode) return;
  ghost.mode = mode;
  ghost.modeTime = 0;
  ghost.unseenTime = 0;
  // 이동 중에는 다음 타일 중심까지 진행해 기존 충돌/BFS 정렬을 유지한다.
}

function beginGhostReturn(ghost) {
  const x = Math.floor((ghost.x + ghost.w / 2) / TILE);
  const y = Math.floor((ghost.y + ghost.h / 2) / TILE);
  const candidates = ghost.path.map((point, index) => ({ point, index }))
    .sort((a, b) => Math.hypot(a.point.x - ghost.x, a.point.y - ghost.y)
      - Math.hypot(b.point.x - ghost.x, b.point.y - ghost.y));
  const nearest = candidates.find(({ point }) => {
    const tx = Math.floor(point.x / TILE), ty = Math.floor(point.y / TILE);
    return (tx === x && ty === y) || findGhostStep(x, y, tx, ty);
  });
  ghost.pathIndex = (nearest || candidates[0]).index;
  setGhostMode(ghost, "return");
}

function updateGhostAI(ghost, dt) {
  const visible = ghostSeesPlayer(ghost);
  const alarm = state.chaseTimer > 0;
  const alarmEnded = ghost.alarmActive && !alarm;
  ghost.alarmActive = alarm;
  ghost.modeTime += dt;
  if (alarm && !state.hidden) {
    ghost.lastSeen = { ...playerCenter() };
    setGhostMode(ghost, "chase");
  } else if (alarmEnded && ghost.mode === "chase") {
    if (visible) ghost.lastSeen = { ...playerCenter() };
    else setGhostMode(ghost, "lost");
  }
  if (ghost.mode === "patrol" || ghost.mode === "return") {
    if (visible) {
      ghost.lastSeen = { ...playerCenter() };
      setGhostMode(ghost, "alert");
      setMessage("👁️ 그림자에게 발견됐다!");
    }
  } else if (ghost.mode === "alert") {
    if (visible) ghost.lastSeen = { ...playerCenter() };
    if (ghost.modeTime >= GHOST_REACTION_TIME) setGhostMode(ghost, state.hidden ? "lost" : "chase");
  } else if (ghost.mode === "chase") {
    if (visible || (alarm && !state.hidden)) {
      ghost.lastSeen = { ...playerCenter() }; ghost.unseenTime = 0;
    } else {
      ghost.unseenTime += dt;
      if (state.hidden || ghost.unseenTime >= GHOST_CORNER_GRACE) setGhostMode(ghost, "lost");
    }
  } else if (ghost.mode === "lost" || ghost.mode === "search") {
    if (visible) {
      ghost.lastSeen = { ...playerCenter() }; setGhostMode(ghost, "chase");
    } else if (ghost.mode === "search") {
      const angle = Math.atan2(ghost.faceY, ghost.faceX) + dt * Math.PI;
      ghost.faceX = Math.cos(angle); ghost.faceY = Math.sin(angle);
      if (ghost.modeTime >= GHOST_SEARCH_TIME) beginGhostReturn(ghost);
    }
  }
  if (ghost.mode === "alert" || ghost.mode === "search") return null;
  if (ghost.mode === "chase" || ghost.mode === "lost") return ghost.lastSeen;
  return ghost.path[ghost.pathIndex];
}

// 피격 시 원격으로 문제를 끝내거나 환자를 스폰으로 옮길 수 없도록 정리한다.
function interruptPatientInteraction() {
  state.miniGame = null;
  if (state.escortPatientId !== null) {
    const patient = state.patients.find((item) => item.id === state.escortPatientId);
    const position = followTrail[0] || playerCenter();
    let x = Math.floor(position.x / TILE), y = Math.floor(position.y / TILE);
    if (tileBlocked(x, y)) {
      const center = playerCenter();
      x = Math.floor(center.x / TILE); y = Math.floor(center.y / TILE);
    }
    if (patient) {
      patient.following = false;
      patient.x = x;
      patient.y = y;
    }
    state.escortPatientId = null;
  }
  followTrail = [];
  followPatientId = null;
}

function updateGhosts(dt) {
  if (invulnerable > 0) {
    invulnerable -= dt;
  }

  // 적 속도 증가 이벤트가 활성화된 경우
  const boosted = state.event.enemyBoost > 0 ? 1.5 : 1;
  ghosts.forEach((ghost) => {
    const target = updateGhostAI(ghost, dt);
    const chasing = ghost.mode === "chase";
    const cx = ghost.x + ghost.w / 2;
    const cy = ghost.y + ghost.h / 2;
    const tx = Math.floor(cx / TILE);
    const ty = Math.floor(cy / TILE);
    if (target) {
    const targetX = Math.floor(target.x / TILE);
    const targetY = Math.floor(target.y / TILE);
    const center = tileCenter(tx, ty);

    // 타일 중심까지 이동을 마친 뒤 최신 플레이어 위치로 다시 탐색한다.
    if (ghost.nextStep && tileBlocked(
      Math.floor(ghost.nextStep.x / TILE), Math.floor(ghost.nextStep.y / TILE),
    )) ghost.nextStep = null;
    if (!ghost.nextStep) {
      if (Math.hypot(center.x - cx, center.y - cy) > 0.01) {
        ghost.nextStep = center;
      } else if (tx === targetX && ty === targetY) {
        ghost.nextStep = { x: target.x, y: target.y };
      } else {
        ghost.nextStep = findGhostStep(tx, ty, targetX, targetY);
      }
    }
    if (Math.hypot(target.x - cx, target.y - cy) < 3) {
      if (ghost.mode === "patrol") ghost.pathIndex = (ghost.pathIndex + 1) % ghost.path.length;
      else if (ghost.mode === "return") setGhostMode(ghost, "patrol");
      else if (ghost.mode === "lost") {
        ghost.nextStep = null;
        setGhostMode(ghost, "search");
      }
    }
    if (ghost.nextStep && ghost.mode !== "search") {
      const dx = ghost.nextStep.x - cx;
      const dy = ghost.nextStep.y - cy;
      const distance = Math.hypot(dx, dy);
      const step = Math.min(distance, ghost.speed * boosted * (chasing ? GHOST_CHASE_MULTIPLIER : 1) * dt);
      if (distance > 0) {
        // 눈이 바라볼 방향
        ghost.faceX = dx;
        ghost.faceY = dy;
        const x = ghost.x + dx / distance * step;
        const y = ghost.y + dy / distance * step;
        if (!ghostCollisionAt(ghost, x, y)) {
          ghost.x = x;
          ghost.y = y;
        } else {
          ghost.nextStep = null;
        }
      }
      if (step >= distance) ghost.nextStep = null;
    }
    }

    // =================================================
    // 플레이어와 충돌
    // =================================================

    if (!state.hidden && invulnerable <= 0) {
      const pc = playerCenter();
      const gc = {
        x: ghost.x + 10,
        y: ghost.y + 10,
      };
      if (Math.hypot(pc.x - gc.x, pc.y - gc.y) < 21) {
        ghost.lastSeen = { ...pc };
        setGhostMode(ghost, "lost");
        // 체력 감소
        state.hearts -= 1;

        // 연속 충돌 방지
        invulnerable = 1.4;
        const start = findTile("S");

        // 시작 위치로 복귀
        interruptPatientInteraction();
        player.x = start.x * TILE + 1;
        player.y = start.y * TILE - 4;
        setMessage("👻 그림자와 부딪혔어! 체력 -1");
        if (state.hearts <= 0) {
          state.lost = true;
          showGameOver("체력이 모두 소진됐어.");
        }
      }
    }
  });
}

// ============================================================
// 시간 시스템
// ============================================================

function updateTimedSystems(dt) {
  // CCTV
  if (state.cctvTimer > 0) {
    state.cctvTimer -= dt;
  }

  // 추격시간
  if (state.chaseTimer > 0) {
    state.chaseTimer -= dt;
    if (state.chaseTimer <= 0) {
      state.chaseTimer = 0;
      setMessage("✅ 경보가 멈췄어. 그림자의 시야를 피해 따돌려!");
    }
  }

  // 적 속도 증가
  if (state.event.enemyBoost > 0) {
    state.event.enemyBoost -= dt;
  }

  // 정전 효과
  if (state.event.blackout > 0) {
    state.event.blackout -= dt;
  }

  // 경고등
  if (state.event.alarm > 0) {
    state.event.alarm -= dt;
  }

  // 숨은 시간
  if (state.hidden) {
    state.hideSeconds += dt;

    // 너무 오래 숨어 있으면 시간 추가 감소
    if (state.hideSeconds > 7) {
      state.time = Math.max(0, state.time - dt * 1.5);
    }
  }

  // ========================================================
  // 미니게임 시간 업데이트
  // ========================================================

  if (state.miniGame) {
    const game = state.miniGame;

    // 타이밍 미니게임 포인터 이동
    if (game.type === "generator" || game.type === "patientTiming") {
      game.pos += game.dir * dt * 0.75;
      if (game.pos >= 1) {
        game.pos = 1;
        game.dir = -1;
      }
      if (game.pos <= 0) {
        game.pos = 0;
        game.dir = 1;
      }
    }

    // 기억 미니게임
    if (game.type === "patientDirection" || game.type === "patientMemory") {
      if (game.reveal > 0) {
        game.reveal -= dt;
        if (game.reveal <= 0) {
          setMessage(
            game.type === "patientDirection"
              ? "이제 기억한 방향키 순서를 입력해!"
              : "이제 기억한 숫자 코드를 키보드 1~4로 입력해!",
          );
        }
      }
    }
  }
}

// ============================================================
// 게임 업데이트
// ============================================================

function update(dt) {
  if (!state || state.won || state.lost || !tutorialFinished) {
    return;
  }

  // 제한시간 감소
  state.time -= dt;
  if (state.time <= 0) {
    state.time = 0;
    state.lost = true;
    showGameOver("제한 시간이 끝났어.");
    return;
  }
  updateTimedSystems(dt);
  updatePlayer(dt);
  updateFollower();
  updateGhosts(dt);
  updatePanels();
}

// ============================================================
// 랭크 계산
// ============================================================

function calculateRank() {
  let points =
    state.hearts * 120 +
    (state.time / level().time) * 500 +
    stageRecordCount() * 120;
  if (points >= 900) {
    return "S";
  }
  if (points >= 720) {
    return "A";
  }
  if (points >= 540) {
    return "B";
  }
  return "C";
}

// ============================================================
// 스테이지 클리어
// ============================================================

function clearStage() {
  // stageRecordCount() : 현재 스테이지에서 수집한 기록 수
  // state.records.length : 현재 스테이지에서 존재하는 기록 수
  if (stageRecordCount() < state.records.length) {
    setMessage("⚠️ 아직 수집하지 못한 야간 기록이 있어. 모두 수집해야 해.");
    return;
  }
  // 우승로직
  state.won = true;
  state.event.alarm = 0;
  state.chaseTimer = 0;
  const rank = calculateRank();
  meta.stageResults.push({
    stage: currentLevelIndex + 1,
    rank: rank,
  });
  if (currentLevelIndex < 2) {
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
                다음 구역으로 이동합니다.
                <br><br>
                <b>
                    ${LEVELS[currentLevelIndex + 1].title}
                </b>
                <br><br>
                ${LEVELS[currentLevelIndex + 1].story}
            </div>
            <button onclick="nextStage()">
                다음 스테이지 →
            </button>
        `;
    overlay.style.display = "flex";
  } else {
    showFinalEnding();
  }
}

// ============================================================
// 다음 스테이지
// ============================================================

function nextStage() {
  currentLevelIndex += 1;
  startStage();
}

// ============================================================
// 최종 엔딩
// ============================================================

function showFinalEnding() {
  let title = "탈출 엔딩";
  let text = "세 개의 병원 구역을 모두 통과해 탈출에 성공했다.";
  if (meta.totalRecords >= 6 && meta.allPatientsRescued) {
    title = "진실 구조 엔딩";
    text =
      "모든 환자를 구조하고 야간 기록까지 모두 확보한 뒤 병원에서 탈출했다.";
  } else if (meta.allPatientsRescued) {
    title = "구조 엔딩";
    text = "병동에 남아 있던 환자 세 명을 모두 구조한 뒤 옥상으로 탈출했다.";
  }
  overlayBox.innerHTML = `
        <div class="overlay-title">
            ${title}
        </div>
        <div class="overlay-text">
            ${text}
            <br><br>
            <b>
                야간 기록
            </b>
            ${meta.totalRecords}/6
            <br>
            <b>
                스테이지 랭크
            </b>
            ${meta.stageResults.map((result) => result.rank).join(" · ")}
        </div>
        <button onclick="startWholeGame()">
            처음부터 다시 플레이
        </button>
    `;
  overlay.style.display = "flex";
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
            현재 스테이지를 다시 도전할 수 있어.
        </div>
        <button onclick="restartStage()">
            다시 도전
        </button>
    `;
  overlay.style.display = "flex";
}

// ============================================================
// 오류
// ============================================================

function showFatalError(reason) {
  overlayBox.innerHTML = `
        <div class="overlay-title">
            MAP ERROR
        </div>
        <div class="overlay-text">
            ${reason}
        </div>
        <button onclick="startWholeGame()">
            다시 불러오기
        </button>
    `;
  overlay.style.display = "flex";
}

// ============================================================
// 화면 그리기 준비
// ============================================================
// 맵과 캐릭터는 도트 해상도(타일 16px)의 worldCanvas 에 그린 뒤
// 게임 Canvas 에 2배로 확대해서 옮긴다. 그래서 모든 도트 크기가 같다.
// 이름표 · HUD · 미니게임은 확대한 다음 게임 Canvas 에 바로 그린다.

// 도트 1픽셀 = 화면 2픽셀
const PIXEL = 2;
const ART_TILE = TILE / PIXEL;

const FONT = '"Galmuri11", "Malgun Gothic", sans-serif';

const worldCanvas = document.createElement("canvas");
worldCanvas.width = COLS * ART_TILE;
worldCanvas.height = ROWS * ART_TILE;
const wctx = worldCanvas.getContext("2d");
wctx.imageSmoothingEnabled = false;

// 어둠과 조명을 그리는 레이어
const lightCanvas = document.createElement("canvas");
lightCanvas.width = worldCanvas.width;
lightCanvas.height = worldCanvas.height;
const lctx = lightCanvas.getContext("2d");

// 스테이지 시작 때 한 번만 그려 두는 바닥 + 벽
let staticLayer = null;

// 화면 가장자리를 어둡게 하는 비네트
let vignetteLayer = null;

// 애니메이션 시간 (초)
let animTime = 0;

// 호송 중인 환자가 따라오는 플레이어 발자국
let followTrail = [];
let followPatientId = null;
let followFacing = "down";

// 화면 좌표(px) → 도트 좌표
function art(value) {
  return Math.round(value / PIXEL);
}

function playerFeet() {
  return {
    x: player.x + 15,
    y: player.y + 28,
  };
}

function isWall(x, y) {
  if (x < 0 || y < 0 || x >= COLS || y >= ROWS) {
    return true;
  }
  return level().map[y][x] === "#";
}

// 타일마다 고정된 0~1 값 (바닥 얼룩 위치에 사용)
function tileNoise(x, y) {
  const n = Math.sin(x * 127.1 + y * 311.7 + currentLevelIndex * 74.7) * 43758.5453;
  return n - Math.floor(n);
}

function hexToRgba(hex, alpha) {
  const value = parseInt(hex.slice(1), 16);
  return `rgba(${value >> 16}, ${(value >> 8) & 255}, ${value & 255}, ${alpha})`;
}

// ============================================================
// 호송 중인 환자 따라오기
// ============================================================

// 환자가 플레이어 발자국 몇 개 뒤를 따라올지
const FOLLOW_GAP = 10;

function updateFollower() {
  if (state.escortPatientId === null) {
    followPatientId = null;
    return;
  }
  const feet = playerFeet();

  // 호송 시작: 환자가 서 있던 자리에서 플레이어 쪽으로 걸어온다
  if (followPatientId !== state.escortPatientId) {
    const patient = state.patients.find((item) => item.id === state.escortPatientId);
    const start = tileCenter(patient.x, patient.y);
    start.y += 12;
    followTrail = [];
    for (let i = 0; i <= FOLLOW_GAP; i++) {
      const t = i / FOLLOW_GAP;
      followTrail.push({
        x: start.x + (feet.x - start.x) * t,
        y: start.y + (feet.y - start.y) * t,
      });
    }
    followPatientId = state.escortPatientId;
    return;
  }

  const last = followTrail[followTrail.length - 1];
  const distance = Math.hypot(feet.x - last.x, feet.y - last.y);

  // 불연속 이동이 발생해도 환자를 순간이동시키지 않고 현장에 남긴다.
  if (distance > 64) {
    interruptPatientInteraction();
  } else if (distance >= 3) {
    followTrail.push({ x: feet.x, y: feet.y });
    if (followTrail.length > FOLLOW_GAP + 1) {
      followTrail.shift();
    }
  }
}

// ============================================================
// 바닥 + 벽 (스테이지 시작 때 한 번만 그린다)
// ============================================================

function buildStaticLayer() {
  const layer = document.createElement("canvas");
  layer.width = worldCanvas.width;
  layer.height = worldCanvas.height;
  const g = layer.getContext("2d");
  const prefix = "s" + (currentLevelIndex + 1);

  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      const px = x * ART_TILE;
      const py = y * ART_TILE;
      if (isWall(x, y)) {
        drawWallTile(g, prefix, x, y, px, py);
        continue;
      }
      Sprites.draw(g, prefix + ((x + y) % 2 === 0 ? "_floor_a" : "_floor_b"), px, py);
      const noise = tileNoise(x, y);
      if (noise < 0.05) {
        Sprites.draw(g, "floor_crack", px, py);
      } else if (noise < 0.08) {
        Sprites.draw(g, "floor_stain", px, py);
      }

      // 벽이 바닥에 드리우는 그림자
      if (isWall(x, y - 1)) {
        g.fillStyle = "rgba(12, 10, 28, 0.34)";
        g.fillRect(px, py, ART_TILE, 2);
        g.fillStyle = "rgba(12, 10, 28, 0.16)";
        g.fillRect(px, py + 2, ART_TILE, 2);
      }
      if (isWall(x - 1, y)) {
        g.fillStyle = "rgba(12, 10, 28, 0.22)";
        g.fillRect(px, py, 2, ART_TILE);
      }
    }
  }

  // 벽에 붙은 창문, 바닥에 칠한 대피 구역
  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      const symbol = level().map[y][x];
      if (symbol === "W") {
        const wy = isWall(x, y - 1) ? y - 1 : y;
        Sprites.draw(g, "window", x * ART_TILE, wy * ART_TILE);
      }
      if (symbol === "Y") {
        Sprites.draw(g, "evac_zone", x * ART_TILE, y * ART_TILE);
      }
    }
  }
  return layer;
}

// 주변 벽 모양에 맞춰 윗면/앞면과 테두리 조각을 고른다
function drawWallTile(g, prefix, x, y, px, py) {
  const n = isWall(x, y - 1);
  const e = isWall(x + 1, y);
  const s = isWall(x, y + 1);
  const w = isWall(x - 1, y);
  const piece = (name) => Sprites.draw(g, prefix + "_" + name, px, py);

  if (s) {
    // 아래도 벽이면 윗면만 보인다
    piece("wall_cap");
    if (!e) {
      piece("rim_e");
    } else if (!isWall(x + 1, y + 1)) {
      piece("rim_e_low");
    }
    if (!w) {
      piece("rim_w");
    } else if (!isWall(x - 1, y + 1)) {
      piece("rim_w_low");
    }
  } else {
    // 아래가 바닥이면 벽 앞면이 보인다
    piece("wall_front");
    if (!e) {
      piece("front_e");
    }
    if (!w) {
      piece("front_w");
    }
  }
  if (!n) {
    piece("rim_n");
  }
  if (n && e && !isWall(x + 1, y - 1)) {
    piece("corner_ne");
  }
  if (n && w && !isWall(x - 1, y - 1)) {
    piece("corner_nw");
  }
}

// ============================================================
// 맵 기호 → 오브젝트 스프라이트
// ============================================================

function nearestHideSpot() {
  const pc = playerCenter();
  let best = null;
  let bestDistance = Infinity;
  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      if (level().map[y][x] !== "h") {
        continue;
      }
      const center = tileCenter(x, y);
      const distance = Math.hypot(pc.x - center.x, pc.y - center.y);
      if (distance < bestDistance) {
        best = { x, y };
        bestDistance = distance;
      }
    }
  }
  return best;
}

function terminalActive(symbol) {
  return state.sequence.slice(0, state.switchProgress).includes(symbol);
}

function propSprite(symbol, x, y, hiddenSpot) {
  const map = level().map;
  const type = level().type;

  // 모든 스테이지 공통
  if (symbol === "T") return { name: "desk" };
  if (symbol === "N") return { name: "nurse_station" };
  if (symbol === "Q") return { name: "wheelchair" };
  if (symbol === "V") return { name: "vending" };
  if (symbol === "G") return { name: "plant" };
  if (symbol === "H") {
    const above = y > 0 && map[y - 1][x] === "H";
    const below = y < ROWS - 1 && map[y + 1][x] === "H";
    return { name: above ? "bed_foot" : below ? "bed_head" : "bed" };
  }
  if (symbol === "h") {
    const hiddenHere = hiddenSpot && hiddenSpot.x === x && hiddenSpot.y === y;
    return { name: hiddenHere ? "locker_hidden" : "locker" };
  }
  if (symbol === "Z") {
    return { name: state.cctvTimer > 0 ? Sprites.anim("cctv_on", animTime, 6) : "cctv" };
  }

  // STAGE 1
  if (type === "collect") {
    if (symbol === "K" && !state.hasKeycard) return { name: "keycard", item: true };
    if (symbol === "F" && !state.hasFuse) return { name: "fuse", item: true };
    if (symbol === "B" && !state.hasBattery) return { name: "battery", item: true };
    if (symbol === "M" && !state.hasMasterKey) return { name: "master_key", item: true };
    if (symbol === "P") {
      return {
        name: state.powerOn
          ? Sprites.anim("generator_on", animTime, 8)
          : Sprites.anim("generator_off", animTime, 2),
      };
    }
    if (symbol === "C") return { name: state.hasKeycard ? "security_open" : "security_closed" };
    if (symbol === "D") return { name: state.powerOn ? "shutter_open" : "shutter_closed" };
    if (symbol === "E") {
      return { name: state.powerOn && state.hasMasterKey ? "elevator_open" : "elevator_closed" };
    }
  }

  // STAGE 2
  if (type === "switch") {
    if (["A", "B", "C"].includes(symbol)) {
      return { name: "terminal_" + symbol + (terminalActive(symbol) ? "_on" : "") };
    }
    if (symbol === "L") return { name: "memo", item: true };
    if (symbol === "X") return { name: state.switchProgress === 3 ? "decon_open" : "decon_closed" };
  }

  // STAGE 3
  if (type === "rescue" && symbol === "R") {
    return { name: rescueCount() === 3 ? "roof_open" : "roof_closed" };
  }
  return null;
}

// ============================================================
// 오브젝트 · 캐릭터 그리기
// ============================================================

// 떠 있는 아이템 + 반짝임
function drawItem(name, cx, bottom, seed) {
  const bob = Math.round(Math.sin(animTime * 3 + seed));
  Sprites.draw(wctx, "shadow", cx, bottom - 2, { alpha: 0.8 });
  Sprites.draw(wctx, name, cx, bottom - 3 + bob);
  const cycle = (animTime + seed * 0.7) % 2.4;
  if (cycle < 0.6) {
    Sprites.draw(wctx, Sprites.animFrames("sparkle")[Math.floor(cycle / 0.1)], cx + 5, bottom - 12 + bob);
  }
}

function drawPatient(patient, cx, bottom) {
  Sprites.draw(wctx, "shadow", cx, bottom);
  Sprites.draw(wctx, "patient" + patient.id + "_down_0", cx, bottom);
  const bob = Math.round(Math.sin(animTime * 4 + patient.id));
  Sprites.draw(wctx, patient.stabilized ? "bubble_heart" : "bubble_alert", cx + 6, bottom - 21 + bob);
}

function drawFollower() {
  const position = followTrail[0];
  const next = followTrail[1];
  const dx = next.x - position.x;
  const dy = next.y - position.y;
  if (dx !== 0 || dy !== 0) {
    followFacing = Math.abs(dx) > Math.abs(dy) ? (dx < 0 ? "left" : "right") : dy < 0 ? "up" : "down";
  }
  const prefix = "patient" + state.escortPatientId;
  const name = player.walking
    ? Sprites.anim(prefix + "_walk_" + followFacing, animTime, 7)
    : prefix + "_" + followFacing + "_0";
  Sprites.draw(wctx, "shadow", art(position.x), art(position.y));
  Sprites.draw(wctx, name, art(position.x), art(position.y));
}

function drawPlayer() {
  const feet = playerFeet();
  const name = player.walking
    ? Sprites.animFrames("doctor_walk_" + player.facing)[player.walkFrame]
    : "doctor_" + player.facing + "_0";

  // 숨는 중이면 흐리게, 맞은 직후 무적 시간에는 깜빡인다
  let alpha = 1;
  if (state.hidden) {
    alpha = 0.3;
  } else if (invulnerable > 0 && Math.floor(invulnerable * 10) % 2 === 0) {
    alpha = 0.35;
  }
  Sprites.draw(wctx, "shadow", art(feet.x), art(feet.y), { alpha });
  Sprites.draw(wctx, name, art(feet.x), art(feet.y), { alpha });
}

function ghostPosition(ghost, index) {
  return {
    x: art(ghost.x + ghost.w / 2),
    y: art(ghost.y + ghost.h / 2) - 2 + Math.round(Math.sin(animTime * 3 + index * 1.7) * 1.5),
  };
}

// 움직이는 방향을 쳐다보고, 추격 중에는 눈이 빨개진다
function ghostEyes(ghost) {
  const fx = ghost.faceX || 0;
  const fy = ghost.faceY || 1;
  const direction = Math.abs(fx) > Math.abs(fy) ? (fx < 0 ? "left" : "right") : fy < 0 ? "up" : "down";
  const angry = ghost.mode === "chase";
  return "ghost_eyes_" + direction + (angry ? "_angry" : "");
}

function drawGhost(ghost, index) {
  const visibility = ghostVisibility(ghost);
  if (visibility.alpha <= 0) return;
  const p = ghostPosition(ghost, index);
  Sprites.draw(wctx, "shadow", p.x, art(ghost.y + ghost.h / 2) + 9, { alpha: 0.7 * visibility.alpha });
  Sprites.draw(wctx, Sprites.anim("ghost_float", animTime + index * 0.3, 4), p.x, p.y, {
    tint: ghost.color,
    alpha: 0.9 * visibility.alpha,
  });
  Sprites.draw(wctx, ghostEyes(ghost), p.x, p.y, { alpha: visibility.alpha });
}

// 화면 아래쪽에 있는 것일수록 나중에 그려서 앞에 보이게 한다
function collectDrawables() {
  const list = [];
  const map = level().map;
  const hiddenSpot = state.hidden ? nearestHideSpot() : null;

  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      const prop = propSprite(map[y][x], x, y, hiddenSpot);
      if (!prop) {
        continue;
      }
      const cx = x * ART_TILE + ART_TILE / 2;
      const bottom = (y + 1) * ART_TILE - 1;
      if (prop.item) {
        list.push({ sortY: bottom - 6, draw: () => drawItem(prop.name, cx, bottom, x + y) });
      } else {
        list.push({ sortY: bottom, draw: () => Sprites.draw(wctx, prop.name, cx, bottom) });
      }

      // 숨어 있는 사물함 위에 "..." 말풍선
      if (prop.name === "locker_hidden") {
        const bob = Math.round(Math.sin(animTime * 3));
        list.push({ sortY: bottom + 1, draw: () => Sprites.draw(wctx, "bubble_dots", cx + 5, bottom - 25 + bob) });
      }
    }
  }

  for (const record of state.records) {
    if (record.collected) {
      continue;
    }
    const cx = record.x * ART_TILE + ART_TILE / 2;
    const bottom = (record.y + 1) * ART_TILE - 1;
    list.push({ sortY: bottom - 6, draw: () => drawItem("record", cx, bottom, record.x + record.y) });
  }

  if (level().type === "rescue") {
    for (const patient of state.patients) {
      if (patient.rescued || patient.following) {
        continue;
      }
      const cx = patient.x * ART_TILE + ART_TILE / 2;
      const bottom = (patient.y + 1) * ART_TILE - 2;
      list.push({ sortY: bottom, draw: () => drawPatient(patient, cx, bottom) });
    }
    if (state.escortPatientId !== null && followTrail.length > 1) {
      list.push({ sortY: art(followTrail[0].y), draw: drawFollower });
    }
  }

  list.push({ sortY: art(playerFeet().y), draw: drawPlayer });

  ghosts.forEach((ghost, index) => {
    list.push({ sortY: art(ghost.y + ghost.h / 2) + 8, draw: () => drawGhost(ghost, index) });
  });

  return list.sort((a, b) => a.sortY - b.sortY);
}

// ============================================================
// 조명
// ============================================================
// 어둠을 깔고, 빛이 있는 곳은 계단 모양 원으로 지워서 도트 느낌의 조명을 만든다.

// [반지름 비율, 지우는 정도]
function darknessLevel() {
  if (state.event.blackout > 0) {
    return 0.82;
  }
  if (currentLevelIndex === 0) {
    return state.powerOn ? 0.36 : 0.6;
  }
  return currentLevelIndex === 1 ? 0.46 : 0.52;
}

function updateVisionDirection(dx, dy, dt) {
  const v = state.vision;
  if (dx && dy) {
    v.target = v.diagonal = Math.atan2(dy, dx);
    v.pending = null;
  } else if (dx || dy) {
    const next = Math.atan2(dy, dx);
    if (v.diagonal !== null && next !== v.target) {
      if (v.pending !== next) { v.pending = next; v.elapsed = 0; }
      v.elapsed += dt;
      if (v.elapsed >= VISION_DIAGONAL_HOLD) {
        v.target = next; v.diagonal = null; v.pending = null;
      }
    } else v.target = next;
  } else {
    if (v.pending !== null && v.diagonal !== null) v.target = v.diagonal;
    v.pending = null;
  }
  const delta = Math.atan2(Math.sin(v.target - v.angle), Math.cos(v.target - v.angle));
  const speed = Math.abs(delta) >= Math.PI * 2 / 3 ? VISION_REVERSE_SPEED : VISION_TURN_SPEED;
  v.angle += Math.sign(delta) * Math.min(Math.abs(delta), speed * dt);
  v.angle = Math.atan2(Math.sin(v.angle), Math.cos(v.angle));
}

// DDA: 다음 타일 경계까지 이동하며 벽과 잠긴 문에서 정지한다.
function castVisionRay(angle, limit, remember = false, origin = playerCenter()) {
  const p = origin, dx = Math.cos(angle), dy = Math.sin(angle);
  let x = Math.floor(p.x / TILE), y = Math.floor(p.y / TILE), distance = 0;
  const sx = dx >= 0 ? 1 : -1, sy = dy >= 0 ? 1 : -1;
  const stepX = Math.abs(dx) < 1e-9 ? Infinity : TILE / Math.abs(dx);
  const stepY = Math.abs(dy) < 1e-9 ? Infinity : TILE / Math.abs(dy);
  let edgeX = Math.abs(dx) < 1e-9 ? Infinity : ((dx >= 0 ? x + 1 : x) * TILE - p.x) / dx;
  let edgeY = Math.abs(dy) < 1e-9 ? Infinity : ((dy >= 0 ? y + 1 : y) * TILE - p.y) / dy;
  while (distance <= limit) {
    if (x < 0 || y < 0 || x >= COLS || y >= ROWS) return distance;
    if (remember) state.explored[y * COLS + x] = 1;
    if (tileBlocked(x, y)) return distance;
    if (Math.abs(edgeX - edgeY) < 1e-7) {
      if (tileBlocked(x + sx, y) || tileBlocked(x, y + sy)) return edgeX;
      distance = edgeX; x += sx; y += sy; edgeX += stepX; edgeY += stepY;
    } else if (edgeX < edgeY) {
      distance = edgeX; x += sx; edgeX += stepX;
    } else { distance = edgeY; y += sy; edgeY += stepY; }
  }
  return limit;
}

function visionStrength(distance, angle) {
  const circle = Math.max(0, 1 - Math.pow(distance / (VISION_RADIUS * TILE), 3));
  const offset = Math.abs(Math.atan2(Math.sin(angle - state.vision.angle), Math.cos(angle - state.vision.angle)));
  const angular = Math.max(0, Math.min(1, (FLASHLIGHT_ANGLE / 2 - offset) / (FLASHLIGHT_ANGLE * 0.18)));
  return Math.max(circle, angular * Math.max(0, 1 - Math.pow(distance / (FLASHLIGHT_DISTANCE * TILE), 2)));
}

function ghostVisibility(ghost) {
  const p = playerCenter();
  const dx = ghost.x + ghost.w / 2 - p.x, dy = ghost.y + ghost.h / 2 - p.y;
  const distance = Math.hypot(dx, dy), angle = Math.atan2(dy, dx);
  const sight = castVisionRay(angle, distance) >= distance - 0.01;
  return { distance, angle, sight, alpha: sight ? visionStrength(distance, angle) : 0 };
}

function drawDarkness() {
  const p = playerCenter(), count = 1440, ranges = new Float32Array(count);
  for (let i = 0; i < count; i++) {
    const angle = i * Math.PI * 2 / count;
    const offset = Math.abs(Math.atan2(Math.sin(angle - state.vision.angle), Math.cos(angle - state.vision.angle)));
    ranges[i] = castVisionRay(angle, (offset < FLASHLIGHT_ANGLE / 2 ? FLASHLIGHT_DISTANCE : VISION_RADIUS) * TILE, true);
  }
  const width = Math.ceil(canvas.width / 4), height = Math.ceil(canvas.height / 4);
  if (fogCanvas.width !== width || fogCanvas.height !== height) {
    fogCanvas.width = width; fogCanvas.height = height;
  }
  const frame = fogContext.createImageData(width, height);
  const memory = (x, y) => x >= 0 && y >= 0 && x < COLS && y < ROWS ? state.explored[y * COLS + x] : 0;
  const ambient = darknessLevel();
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const wx = (x + 0.5) * canvas.width / width, wy = (y + 0.5) * canvas.height / height;
      const dx = wx - p.x, dy = wy - p.y, distance = Math.hypot(dx, dy), angle = Math.atan2(dy, dx);
      const ray = Math.round((angle + Math.PI * 2) % (Math.PI * 2) / (Math.PI * 2) * count) % count;
      const lit = distance <= ranges[ray] + 2 ? visionStrength(distance, angle) : 0;
      // 탐험한 타일 사이를 보간해 기억 영역의 가장자리를 부드럽게 만든다.
      const tx = wx / TILE - 0.5, ty = wy / TILE - 0.5;
      const ix = Math.floor(tx), iy = Math.floor(ty), fx = tx - ix, fy = ty - iy;
      const explored = (memory(ix, iy) * (1 - fx) + memory(ix + 1, iy) * fx) * (1 - fy)
        + (memory(ix, iy + 1) * (1 - fx) + memory(ix + 1, iy + 1) * fx) * fy;
      const base = UNEXPLORED_DARKNESS + (EXPLORED_DARKNESS - UNEXPLORED_DARKNESS) * explored;
      const index = (y * width + x) * 4;
      frame.data[index] = 5; frame.data[index + 1] = 6; frame.data[index + 2] = 20;
      frame.data[index + 3] = Math.round((base + (ambient * 0.35 - base) * lit) * 255);
    }
  }
  fogContext.putImageData(frame, 0, 0);
  ctx.save(); ctx.imageSmoothingEnabled = true;
  ctx.drawImage(fogCanvas, 0, 0, canvas.width, canvas.height);
  ctx.restore();
}

function drawGhostSignals() {
  ghosts.forEach((ghost, index) => {
    const v = ghostVisibility(ghost);
    if (v.sight) {
      const p = ghostPosition(ghost, index);
      Sprites.draw(ctx, ghostEyes(ghost), p.x * PIXEL, p.y * PIXEL, { scale: PIXEL, alpha: 0.12 + 0.88 * v.alpha });
      if (v.alpha > 0 && (ghost.mode === "alert" || ghost.mode === "return")) {
        ctx.save();
        ctx.globalAlpha = v.alpha;
        ctx.font = "bold 22px " + FONT;
        ctx.textAlign = "center";
        ctx.textBaseline = "bottom";
        ctx.fillStyle = ghost.mode === "alert" ? "#fee761" : "#e8ecf6";
        ctx.strokeStyle = "#0b0c18";
        ctx.lineWidth = 3;
        const marker = ghost.mode === "alert" ? "!" : "?";
        ctx.strokeText(marker, p.x * PIXEL, p.y * PIXEL - 24);
        ctx.fillText(marker, p.x * PIXEL, p.y * PIXEL - 24);
        ctx.restore();
      }
    }
    const proximity = Math.max(0, 1 - v.distance / (PRESENCE_DISTANCE * TILE));
    if (!proximity) return;
    const dx = Math.cos(v.angle), dy = Math.sin(v.angle);
    const edge = Math.min(canvas.width / 2 / Math.max(0.001, Math.abs(dx)), canvas.height / 2 / Math.max(0.001, Math.abs(dy)));
    const x = canvas.width / 2 + dx * edge, y = canvas.height / 2 + dy * edge;
    const pulse = 0.25 + 0.75 * (0.5 + 0.5 * Math.sin(animTime * (3 + proximity * 10)));
    const glow = ctx.createRadialGradient(x, y, 0, x, y, 160);
    glow.addColorStop(0, `rgba(228, 30, 50, ${proximity * pulse * 0.65})`);
    glow.addColorStop(1, "rgba(228, 30, 50, 0)");
    ctx.fillStyle = glow; ctx.fillRect(0, 0, canvas.width, canvas.height);
  });
}

function getVignette() {
  if (!vignetteLayer) {
    vignetteLayer = document.createElement("canvas");
    vignetteLayer.width = canvas.width;
    vignetteLayer.height = canvas.height;
    const g = vignetteLayer.getContext("2d");
    const cx = canvas.width / 2;
    const cy = canvas.height / 2;
    const gradient = g.createRadialGradient(cx, cy, canvas.height * 0.4, cx, cy, canvas.width * 0.62);
    gradient.addColorStop(0, "rgba(4, 4, 14, 0)");
    gradient.addColorStop(1, "rgba(4, 4, 14, 0.5)");
    g.fillStyle = gradient;
    g.fillRect(0, 0, canvas.width, canvas.height);
  }
  return vignetteLayer;
}

// ============================================================
// 이름표
// ============================================================

const TAG_STYLES = {
  normal: { edge: "#0b0c18", fill: "#262b44", text: "#e8ecf6" },
  focus: { edge: "#0b0c18", fill: "#feae34", text: "#181425" },
  light: { edge: "#0b0c18", fill: "#2a3050", text: "#ffffff" },
};

// 모서리를 한 칸씩 깎은 도트 이름표
function drawTag(g, text, cx, cy, style = "normal", alpha = 1) {
  const colors = TAG_STYLES[style];
  g.save();
  g.globalAlpha = alpha;
  g.font = (style === "focus" ? "bold " : "") + "12px " + FONT;
  const w = Math.ceil(g.measureText(text).width / 2) * 2 + 12;
  const h = 18;
  const x = Math.round((cx - w / 2) / 2) * 2;
  const y = Math.round((cy - h / 2) / 2) * 2;
  g.fillStyle = colors.edge;
  g.fillRect(x + 2, y, w - 4, h);
  g.fillRect(x, y + 2, w, h - 4);
  g.fillStyle = colors.fill;
  g.fillRect(x + 2, y + 2, w - 4, h - 4);
  g.fillStyle = colors.text;
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.fillText(text, x + w / 2, y + h / 2 + 1);
  g.restore();
}

// 이름표를 붙일 대상 (top: 머리 위 표시를 띄울 높이)
function labelTargets() {
  const targets = [];
  const add = (x, y, label, options = {}) => targets.push({ x, y, label, interact: true, top: -6, ...options });
  const type = level().type;

  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      const symbol = level().map[y][x];
      if (symbol === "h") add(x, y, "숨는 곳", { top: -22 });
      if (symbol === "Z") add(x, y, "CCTV");

      if (type === "collect") {
        if (symbol === "K" && !state.hasKeycard) add(x, y, "출입카드");
        if (symbol === "F" && !state.hasFuse) add(x, y, "퓨즈");
        if (symbol === "B" && !state.hasBattery) add(x, y, "비상 배터리");
        if (symbol === "P") add(x, y, "발전기", { top: -14 });
        if (symbol === "M" && !state.hasMasterKey) add(x, y, "마스터 키");
        if (symbol === "E") add(x, y, "엘리베이터", { top: -22 });
        if (symbol === "C") add(x, y, "보안문", { interact: false });
        if (symbol === "D") add(x, y, "전원문", { interact: false });
      }
      if (type === "switch") {
        if (["A", "B", "C"].includes(symbol)) add(x, y, "단말기 " + symbol, { top: -10 });
        if (symbol === "L") add(x, y, "연구 메모");
        if (symbol === "X") add(x, y, "제독실 출구", { top: -22 });
      }
      if (type === "rescue") {
        if (symbol === "Y") add(x, y, "대피 구역", { interact: state.escortPatientId !== null, range: 50 });
        if (symbol === "R") add(x, y, "옥상 출구", { top: -22 });
      }
    }
  }

  for (const record of state.records) {
    if (!record.collected) add(record.x, record.y, "야간 기록");
  }
  for (const patient of state.patients) {
    if (!patient.rescued && !patient.following) {
      add(patient.x, patient.y, "환자 " + patient.id, { top: -34, range: 43 });
    }
  }
  return targets;
}

function drawLabels() {
  const pc = playerCenter();
  const bob = Math.round(Math.sin(animTime * 6)) * 2;
  for (const target of labelTargets()) {
    const cx = target.x * TILE + TILE / 2;
    const cy = target.y * TILE + TILE / 2;

    const angle = Math.atan2(cy - pc.y, cx - pc.x);
    const range = Math.hypot(cx - pc.x, cy - pc.y);
    if (castVisionRay(angle, range) < range - 0.01 || visionStrength(range, angle) < 0.1) continue;

    // Space 로 바로 쓸 수 있는 대상은 노랗게 강조
    const near = target.interact && !state.hidden && nearPos(target.x, target.y, target.range || 42);
    const distance = Math.hypot(pc.x - cx, pc.y - cy);
    const alpha = near ? 1 : distance < 170 ? 0.92 : 0.6;
    drawTag(ctx, target.label, cx, target.y * TILE + TILE + 8, near ? "focus" : "normal", alpha);
    if (near) {
      Sprites.draw(ctx, "marker", cx, target.y * TILE + target.top + bob, { scale: 2 });
    }
  }
}

// ============================================================
// HUD (화면 아래 벽 위에 표시)
// ============================================================

// 모서리를 깎은 도트 창
function drawPanel(g, x, y, w, h, fill = "rgba(22, 25, 46, 0.94)", edge = "#3a4466") {
  g.fillStyle = "#0b0c18";
  g.fillRect(x + 2, y, w - 4, h);
  g.fillRect(x, y + 2, w, h - 4);
  g.fillStyle = edge;
  g.fillRect(x + 2, y + 2, w - 4, h - 4);
  g.fillStyle = fill;
  g.fillRect(x + 4, y + 4, w - 8, h - 8);
}

function hudText(text, x, y, color = "#e8ecf6", align = "left") {
  ctx.fillStyle = color;
  ctx.font = "12px " + FONT;
  ctx.textAlign = align;
  ctx.textBaseline = "middle";
  ctx.fillText(text, x, y);
}

function drawHud() {
  const y = canvas.height - 30;
  const mid = y + 13;
  const blink = Math.floor(animTime * 4) % 2 === 0;

  // 왼쪽: 체력 + 스태미나
  drawPanel(ctx, 6, y, 216, 26);
  for (let i = 0; i < 4; i++) {
    Sprites.draw(ctx, i < state.hearts ? "heart" : "heart_empty", 14 + i * 22, y + 5, { scale: 2 });
  }
  Sprites.draw(ctx, "icon_bolt", 108, y + 4, { scale: 2 });
  const barWidth = 84;
  ctx.fillStyle = "#0b0c18";
  ctx.fillRect(126, y + 7, barWidth + 4, 12);
  ctx.fillStyle = "#262b44";
  ctx.fillRect(128, y + 9, barWidth, 8);
  ctx.fillStyle = state.stamina > 30 ? "#feae34" : "#e43b44";
  ctx.fillRect(128, y + 9, Math.round((barWidth * state.stamina) / 200) * 2, 8);
  ctx.fillStyle = "rgba(255, 255, 255, 0.28)";
  ctx.fillRect(128, y + 9, Math.round((barWidth * state.stamina) / 200) * 2, 2);

  // 상태 배지
  let badgeX = 230;
  if (state.chaseTimer > 0) {
    drawPanel(ctx, badgeX, y, 112, 26, blink ? "#a22633" : "#6b1a26", "#e43b44");
    Sprites.draw(ctx, "icon_alert", badgeX + 10, y + 3, { scale: 2 });
    hudText("경보·추격", badgeX + 32, mid);
    badgeX += 120;
  }
  if (state.hidden) {
    drawPanel(ctx, badgeX, y, 104, 26, "rgba(22, 25, 46, 0.94)", "#5a6988");
    Sprites.draw(ctx, "icon_eye", badgeX + 8, y + 6, { scale: 2 });
    hudText("숨는 중", badgeX + 32, mid);
  }

  // 가운데: 스테이지 이름
  ctx.font = "12px " + FONT;
  const titleWidth = Math.ceil(ctx.measureText(level().title).width / 2) * 2 + 28;
  const titleX = Math.round((canvas.width - titleWidth) / 4) * 2;
  drawPanel(ctx, titleX, y, titleWidth, 26);
  hudText(level().title, canvas.width / 2, mid, "#c0cbdc", "center");

  // 오른쪽: 야간 기록 + 남은 시간
  const minutes = Math.floor(state.time / 60);
  const seconds = Math.floor(state.time % 60).toString().padStart(2, "0");
  const lowTime = state.time < 60;
  drawPanel(ctx, canvas.width - 206, y, 200, 26);
  Sprites.draw(ctx, "icon_doc", canvas.width - 198, y + 4, { scale: 2 });
  hudText("기록 " + stageRecordCount() + "/" + state.records.length, canvas.width - 176, mid);
  Sprites.draw(ctx, "icon_clock", canvas.width - 92, y + 4, { scale: 2 });
  hudText(minutes + ":" + seconds, canvas.width - 70, mid, lowTime && blink ? "#e43b44" : "#ffffff");
}

// ============================================================
// 미니게임 화면
// ============================================================

function directionSprite(key) {
  return {
    ArrowUp: "key_up",
    ArrowDown: "key_down",
    ArrowLeft: "key_left",
    ArrowRight: "key_right",
  }[key];
}

function centerText(text, y, font, color = "#ffffff") {
  ctx.fillStyle = color;
  ctx.font = font;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(text, canvas.width / 2, y);
}

// 기억 미니게임의 칸 5개 (확인한 칸은 내용, 남은 칸은 ?)
function drawMemorySlots(game, drawContent) {
  const size = 52;
  const gap = 14;
  const startX = Math.round((canvas.width - (size * 5 + gap * 4)) / 2);
  const y = 300;
  game.sequence.forEach((value, index) => {
    const x = startX + index * (size + gap);
    const shown = game.reveal > 0 || index < game.inputIndex;
    const current = game.reveal <= 0 && index === game.inputIndex;
    drawPanel(ctx, x, y, size, size, shown ? "#2a3050" : "#181c33", current ? "#feae34" : "#3a4466");
    if (shown) {
      drawContent(value, x + size / 2, y + size / 2);
    } else {
      centerTextAt("?", x + size / 2, y + size / 2 + 1, "bold 24px " + FONT, "#5a6988");
    }
  });
}

function centerTextAt(text, x, y, font, color) {
  ctx.fillStyle = color;
  ctx.font = font;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(text, x, y);
}

// 기억 미니게임 상단의 남은 시간 막대
function drawRevealBar(game) {
  if (game.reveal <= 0) {
    return;
  }
  const width = 330;
  const x = Math.round((canvas.width - width) / 2);
  ctx.fillStyle = "#0b0c18";
  ctx.fillRect(x - 2, 372, width + 4, 10);
  ctx.fillStyle = "#262b44";
  ctx.fillRect(x, 374, width, 6);
  ctx.fillStyle = "#2ce8f5";
  ctx.fillRect(x, 374, Math.round((width * Math.max(0, game.reveal)) / 6) * 2, 6);
}

function drawMiniGame() {
  if (!state.miniGame) {
    return;
  }
  const game = state.miniGame;
  ctx.fillStyle = "rgba(6, 7, 16, 0.5)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  drawPanel(ctx, 268, 190, 520, 220, "rgba(20, 23, 43, 0.98)", "#5a6988");

  // 발전기
  if (game.type === "generator") {
    centerText("발전기 수리", 236, "bold 24px " + FONT);
    centerText("노란 표시가 초록 구간에 들어왔을 때 Space", 268, "12px " + FONT, "#8b9bb4");
    drawTimingBar(ctx, game.pos, 330, 318, 396, 0.42, 0.58);
  }

  // 환자 1
  if (game.type === "patientTiming") {
    centerText("환자 1 상태 안정화", 236, "bold 24px " + FONT);
    centerText("초록 구간에 맞춰 Space · 2번 성공하면 안정화", 268, "12px " + FONT, "#8b9bb4");
    drawTimingBar(ctx, game.pos, 330, 318, 396, 0.4, 0.6);
    for (let i = 0; i < 2; i++) {
      Sprites.draw(ctx, i < game.success ? "heart" : "heart_empty", 504 + i * 30, 366, { scale: 2 });
    }
  }

  // 환자 2
  if (game.type === "patientDirection") {
    centerText("환자 2 · 방향 기억", 236, "bold 24px " + FONT);
    centerText(
      game.reveal > 0 ? "순서를 기억해!" : "기억한 순서대로 방향키 입력 · " + game.inputIndex + "/5",
      268,
      "12px " + FONT,
      "#8b9bb4",
    );
    drawMemorySlots(game, (key, x, y) => Sprites.draw(ctx, directionSprite(key), x - 15, y - 13, { scale: 2 }));
    drawRevealBar(game);
  }

  // 환자 3
  if (game.type === "patientMemory") {
    centerText("환자 3 · 숫자 기억", 236, "bold 24px " + FONT);
    centerText(
      game.reveal > 0 ? "숫자 코드를 기억해!" : "키보드 숫자 1~4 로 입력 · " + game.inputIndex + "/5",
      268,
      "12px " + FONT,
      "#8b9bb4",
    );
    drawMemorySlots(game, (value, x, y) => centerTextAt(value, x, y + 1, "bold 24px " + FONT, "#fee761"));
    drawRevealBar(game);
  }
  ctx.textAlign = "left";
}

// 타이밍 바 (zoneStart ~ zoneEnd 가 성공 구간)
function drawTimingBar(g, position, x, y, width, zoneStart, zoneEnd) {
  const height = 20;
  drawPanel(g, x - 8, y - 8, width + 16, height + 16, "#10121f", "#3a4466");
  g.fillStyle = "#262b44";
  g.fillRect(x, y, width, height);
  g.fillStyle = "#1b1f33";
  for (let i = 1; i < 12; i++) {
    g.fillRect(x + Math.round((width * i) / 24) * 2, y, 2, height);
  }
  const zoneX = x + Math.round((width * zoneStart) / 2) * 2;
  const zoneWidth = Math.round((width * (zoneEnd - zoneStart)) / 2) * 2;
  g.fillStyle = "#3e8948";
  g.fillRect(zoneX, y, zoneWidth, height);
  g.fillStyle = "#63c74d";
  g.fillRect(zoneX, y, zoneWidth, height - 6);

  const pointer = Math.round((x + width * position) / 2) * 2;
  g.fillStyle = "#0b0c18";
  g.fillRect(pointer - 5, y - 10, 10, height + 20);
  g.fillStyle = "#fee761";
  g.fillRect(pointer - 3, y - 8, 6, height + 16);
  g.fillStyle = "#ffffff";
  g.fillRect(pointer - 3, y - 8, 2, height + 16);
}

// ============================================================
// 전체 렌더링
// ============================================================

function render() {
  // 1) 도트 해상도로 맵 · 오브젝트 · 캐릭터
  wctx.drawImage(staticLayer, 0, 0);
  for (const item of collectDrawables()) {
    item.draw();
  }

  // 2) 어둠과 조명, 어둠 속에서도 빛나는 그림자의 눈
  ctx.drawImage(worldCanvas, 0, 0, canvas.width, canvas.height);
  drawDarkness();
  drawGhostSignals();

  // 3) 경보 (빨간 빛이 맥박처럼 깜빡인다)
  if (state.event.alarm > 0) {
    const strength = 0.08 + 0.1 * (0.5 + 0.5 * Math.sin(animTime * 9));
    ctx.fillStyle = `rgba(228, 59, 68, ${strength})`;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  // 4) 2배로 확대해서 게임 Canvas 에 옮기고 글자 UI 를 올린다
  ctx.drawImage(getVignette(), 0, 0);
  drawLabels();
  drawHud();
  drawMiniGame();
}

// ============================================================
// 게임 루프
// ============================================================

function gameLoop(now) {
  const dt = Math.min((now - lastTime) / 1000, 0.05);
  lastTime = now;
  animTime += dt;

  // 프롤로그가 끝난 뒤에만 실제 게임 실행
  if (state && tutorialFinished) {
    update(dt);
    render();
  } else if (!tutorialFinished) {
    // 프롤로그 그림도 움직이게 매 프레임 다시 그린다
    drawTutorialScene(TUTORIAL_PAGES[tutorialPageIndex].scene, animTime);
  }
  requestAnimationFrame(gameLoop);
}

// ============================================================
// 키보드 입력
// ============================================================

function handleKeyDown(event) {
  // 프롤로그 중에는 게임 키 입력을 막는다.
  if (!tutorialFinished) {
    return;
  }
  const key = event.key;

  // ========================================================
  // 환자 2 방향키 미니게임
  // ========================================================

  if (state && state.miniGame) {
    const game = state.miniGame;
    if (
      game.type === "patientDirection" &&
      game.reveal <= 0 &&
      ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(key)
    ) {
      event.preventDefault();
      handleDirectionInput(key);
      return;
    }

    // ====================================================
    // 환자 3 숫자 기억
    // ====================================================

    if (
      game.type === "patientMemory" &&
      game.reveal <= 0 &&
      ["1", "2", "3", "4"].includes(key)
    ) {
      event.preventDefault();
      handleMemoryInput(key);
      return;
    }
  }
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
    "Shift",
  ];
  if (gameKeys.includes(key)) {
    event.preventDefault();
  }
  keys[key] = true;

  // Space / Enter
  if (key === " " || key === "Enter") {
    interact();
  }

  // R
  if (key === "r" || key === "R") {
    restartStage();
  }
}

// ============================================================
// 키 해제
// ============================================================

function handleKeyUp(event) {
  keys[event.key] = false;
}

document.addEventListener("keydown", handleKeyDown, true);

document.addEventListener("keyup", handleKeyUp, true);

// ============================================================
// Canvas 클릭
// ============================================================

canvas.addEventListener("mousedown", () => {
  if (tutorialFinished) {
    canvas.focus();
    setMessage("✅ 게임 입력 활성화.");
  }
});

// ============================================================
// 브라우저 포커스를 잃으면 키 초기화
// ============================================================

window.addEventListener("blur", () => {
  keys = {};
});

// ============================================================
// 화면 방향키
// ============================================================

function pressDirection(direction) {
  if (!tutorialFinished) {
    return;
  }
  keys[direction] = true;
  canvas.focus();
}

function releaseDirection(direction) {
  keys[direction] = false;
}

// ============================================================
// 페이지 로드
// ============================================================

// 도트 글꼴을 기다린다 (실패해도 기본 글꼴로 계속 진행)
function loadFonts() {
  if (!document.fonts) {
    return Promise.resolve();
  }
  return Promise.all([
    document.fonts.load("12px Galmuri11"),
    document.fonts.load("bold 12px Galmuri11"),
  ]).catch(() => {});
}

// HTML 에 data-sprite 로 적어 둔 자리에 도트 아이콘을 넣는다
function fillSpriteIcons() {
  document.querySelectorAll("[data-sprite]").forEach((element) => {
    element.outerHTML = Sprites.icon(element.dataset.sprite, Number(element.dataset.scale || 1), "icon");
  });
}

function showLoadError(error) {
  setMessage("⚠️ 게임 에셋을 불러오지 못했습니다. " + error.message);
  prologueOverlay.style.display = "none";
  overlayBox.innerHTML = `
        <div class="overlay-title">
            LOAD ERROR
        </div>
        <div class="overlay-text">
            ${error.message}
            <br><br>
            web/assets 폴더가 index.html 옆에 있는지 확인해 줘.
        </div>
        <button onclick="location.reload()">
            다시 불러오기
        </button>
    `;
  overlay.style.display = "flex";
}

window.addEventListener("load", () => {
  // 스프라이트와 글꼴을 먼저 불러온 뒤 프롤로그부터 보여준다.
  Promise.all([Sprites.load(), loadFonts()])
    .then(() => {
      fillSpriteIcons();
      showPrologue();
      requestAnimationFrame(gameLoop);
    })
    .catch(showLoadError);
});

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
// 프롤로그용 사각형
// ============================================================

function tutorialRect(x, y, w, h, color) {
  tutorialCtx.fillStyle = color;
  tutorialCtx.fillRect(Math.round(x), Math.round(y), w, h);
}

// ============================================================
// 프롤로그용 라벨
// ============================================================

function tutorialLabel(text, x, y) {
  tutorialCtx.font = 'bold 13px "Malgun Gothic"';
  tutorialCtx.textAlign = "center";
  const width = tutorialCtx.measureText(text).width + 16;
  tutorialRect(x - width / 2, y - 11, width, 22, "rgba(25,43,51,0.88)");
  tutorialCtx.fillStyle = "#ffffff";
  tutorialCtx.fillText(text, x, y + 5);
}

// ============================================================
// 프롤로그용 플레이어 캐릭터
// ============================================================

function drawTutorialPlayer(x, y, scale = 3) {
  const r = (px, py, w, h, color) => {
    tutorialRect(x + px * scale, y + py * scale, w * scale, h * scale, color);
  };

  // 외곽
  r(6, 0, 18, 5, "#253038");
  r(4, 4, 22, 12, "#253038");
  r(6, 16, 18, 17, "#253038");

  // 머리
  r(7, 1, 16, 5, "#684334");
  r(5, 5, 20, 5, "#79513e");

  // 얼굴
  r(9, 8, 12, 9, "#f3c4a3");

  // 눈
  r(11, 11, 2, 2, "#20272b");
  r(17, 11, 2, 2, "#20272b");

  // 의료복
  r(11, 19, 9, 11, "#4ca8bb");

  // 가운
  r(6, 19, 6, 14, "#ffffff");
  r(19, 19, 6, 14, "#ffffff");

  // 바지
  r(9, 31, 6, 5, "#344f76");
  r(17, 31, 6, 5, "#344f76");

  // 신발
  r(8, 35, 7, 3, "#202b32");
  r(17, 35, 7, 3, "#202b32");
}

// ============================================================
// 프롤로그용 그림자
// ============================================================

function drawTutorialGhost(x, y, color, scale = 4) {
  const r = (px, py, w, h, c) => {
    tutorialRect(x + px * scale, y + py * scale, w * scale, h * scale, c);
  };
  r(2, 2, 16, 13, color);
  r(4, 14, 4, 6, color);
  r(9, 14, 4, 6, color);
  r(14, 14, 4, 6, color);

  // 눈
  r(5, 6, 2, 2, "#ffffff");
  r(12, 6, 2, 2, "#ffffff");
}

// ============================================================
// 프롤로그용 카드
// ============================================================

function drawTutorialCard(x, y) {
  tutorialRect(x, y, 68, 38, "#438bed");
  tutorialRect(x + 10, y + 10, 16, 13, "#edf7ff");
  tutorialRect(x + 35, y + 10, 22, 5, "#245788");
}

// ============================================================
// 프롤로그용 퓨즈
// ============================================================

function drawTutorialFuse(x, y) {
  tutorialRect(x + 15, y, 38, 55, "#e5c44e");
  tutorialRect(x + 20, y + 8, 28, 12, "#fff3aa");
}

// ============================================================
// 프롤로그용 배터리
// ============================================================

function drawTutorialBattery(x, y) {
  tutorialRect(x + 12, y + 8, 42, 54, "#46a760");
  tutorialRect(x + 25, y, 16, 9, "#d6e4e8");
  tutorialRect(x + 25, y + 27, 15, 6, "#d7f9de");
}

// ============================================================
// 프롤로그용 발전기
// ============================================================

function drawTutorialGenerator(x, y) {
  tutorialRect(x, y, 100, 65, "#485d66");
  tutorialRect(x + 17, y + 15, 64, 30, "#273940");
  tutorialRect(x + 25, y + 23, 14, 14, "#e86666");
  tutorialRect(x + 56, y + 23, 14, 14, "#e8c854");
}

// ============================================================
// 프롤로그용 숨는 곳
// ============================================================

function drawTutorialHideSpot(x, y) {
  tutorialRect(x, y, 80, 82, "#657a86");
  tutorialRect(x + 12, y + 8, 56, 66, "#d2e0e5");
  tutorialRect(x + 38, y + 8, 5, 66, "#8aa0aa");
}

// ============================================================
// 프롤로그용 CCTV
// ============================================================

function drawTutorialCCTV(x, y) {
  tutorialRect(x, y, 85, 60, "#344b53");
  tutorialRect(x + 10, y + 10, 65, 34, "#6bb2d2");
  tutorialRect(x + 31, y + 61, 24, 8, "#65777e");
}

// ============================================================
// 프롤로그용 환자
// ============================================================

function drawTutorialPatient(x, y, color) {
  tutorialRect(x + 22, y, 30, 16, "#544038");
  tutorialRect(x + 25, y + 14, 24, 23, "#efc3a5");
  tutorialRect(x + 15, y + 36, 45, 32, color);
}

// ============================================================
// 프롤로그 장면 그리기
// ============================================================

function drawTutorialScene(scene) {
  // 화면 초기화
  tutorialCtx.clearRect(0, 0, tutorialCanvas.width, tutorialCanvas.height);

  // 바닥
  tutorialCtx.fillStyle = "#bacacf";
  tutorialCtx.fillRect(0, 0, tutorialCanvas.width, tutorialCanvas.height);

  // 바닥 타일 느낌
  for (let x = 0; x < 780; x += 48) {
    tutorialCtx.fillStyle = "rgba(255,255,255,0.13)";
    tutorialCtx.fillRect(x, 0, 2, 245);
  }
  for (let y = 0; y < 245; y += 48) {
    tutorialCtx.fillStyle = "rgba(255,255,255,0.13)";
    tutorialCtx.fillRect(0, y, 780, 2);
  }

  // --------------------------------------------------------
  // PAGE 1
  // --------------------------------------------------------

  if (scene === "intro") {
    // 왼쪽 병원 문
    tutorialRect(35, 30, 170, 165, "#536c76");
    tutorialRect(50, 45, 63, 135, "#a8bdc4");
    tutorialRect(125, 45, 63, 135, "#a8bdc4");
    tutorialRect(82, 58, 77, 10, "#d95f69");
    tutorialLabel("잠긴 병원 출구", 120, 215);

    // 가운데 플레이어
    drawTutorialPlayer(330, 65, 3);
    tutorialLabel("플레이어", 375, 205);

    // 오른쪽 그림자
    drawTutorialGhost(600, 75, "#957cff", 4);
    tutorialLabel("정체불명의 그림자", 640, 205);
  }

  // --------------------------------------------------------
  // PAGE 2
  // --------------------------------------------------------

  else if (scene === "player") {
    drawTutorialPlayer(90, 42, 4);
    tutorialLabel("흰 가운 = 나", 150, 215);

    // 방향키
    tutorialRect(370, 58, 52, 52, "#426675");
    tutorialRect(310, 118, 52, 52, "#426675");
    tutorialRect(370, 118, 52, 52, "#426675");
    tutorialRect(430, 118, 52, 52, "#426675");
    tutorialCtx.fillStyle = "#ffffff";
    tutorialCtx.font = "bold 28px Arial";
    tutorialCtx.textAlign = "center";
    tutorialCtx.fillText("↑", 396, 94);
    tutorialCtx.fillText("←", 336, 154);
    tutorialCtx.fillText("↓", 396, 154);
    tutorialCtx.fillText("→", 456, 154);
    tutorialLabel("방향키 / WASD", 396, 210);

    // Space 키
    tutorialRect(570, 90, 150, 58, "#416675");
    tutorialCtx.fillStyle = "#ffffff";
    tutorialCtx.font = "bold 20px Arial";
    tutorialCtx.fillText("SPACE", 645, 126);
    tutorialLabel("상호작용", 645, 190);
  }

  // --------------------------------------------------------
  // PAGE 3
  // --------------------------------------------------------

  else if (scene === "items") {
    drawTutorialCard(45, 60);
    tutorialLabel("출입카드", 79, 130);
    drawTutorialFuse(205, 50);
    tutorialLabel("퓨즈", 238, 130);
    drawTutorialBattery(350, 43);
    tutorialLabel("비상 배터리", 383, 130);
    drawTutorialGenerator(530, 45);
    tutorialLabel("발전기", 580, 130);

    // 타이밍 게이지
    tutorialRect(150, 180, 480, 18, "#263a43");
    tutorialRect(352, 180, 76, 18, "#52d981");
    tutorialRect(387, 171, 7, 36, "#ffe067");
    tutorialLabel("노란 포인터를 초록 구간에서 멈추기", 390, 225);
  }

  // --------------------------------------------------------
  // PAGE 4
  // --------------------------------------------------------

  else if (scene === "enemy") {
    // 그림자
    drawTutorialGhost(90, 70, "#ff74a9", 4);
    tutorialLabel("그림자 · 피해야 함", 130, 200);

    // 추격 화살표
    tutorialCtx.fillStyle = "#a24f5f";
    tutorialCtx.font = "bold 42px Arial";
    tutorialCtx.textAlign = "center";
    tutorialCtx.fillText("→ → →", 330, 120);

    // 플레이어
    drawTutorialPlayer(420, 60, 3);
    tutorialLabel("Shift로 달리기", 465, 200);

    // 숨는 곳
    drawTutorialHideSpot(625, 52);
    tutorialLabel("숨는 곳", 665, 200);
  }

  // --------------------------------------------------------
  // PAGE 5
  // --------------------------------------------------------

  else if (scene === "final") {
    // CCTV
    drawTutorialCCTV(55, 60);
    tutorialLabel("CCTV", 98, 160);

    // 기록
    tutorialRect(225, 55, 60, 78, "#f4e7b8");
    tutorialRect(238, 73, 34, 5, "#8e805f");
    tutorialRect(238, 89, 34, 5, "#8e805f");
    tutorialLabel("야간 기록", 255, 160);

    // 환자
    drawTutorialPatient(360, 55, "#77b8e8");
    tutorialLabel("구조할 환자", 397, 160);

    // 대피 구역
    tutorialRect(525, 62, 85, 65, "#5ba878");
    tutorialRect(539, 75, 57, 39, "#9fe2b8");
    tutorialLabel("대피 구역", 567, 160);

    // 출구
    tutorialRect(670, 50, 75, 90, "#6e858e");
    tutorialRect(682, 60, 23, 72, "#a4b9c0");
    tutorialRect(711, 60, 23, 72, "#a4b9c0");
    tutorialRect(694, 67, 28, 8, "#6fe484");
    tutorialLabel("최종 출구", 708, 160);
    tutorialCtx.fillStyle = "#395761";
    tutorialCtx.font = 'bold 18px "Malgun Gothic"';
    tutorialCtx.textAlign = "center";
    tutorialCtx.fillText("탐색 → 퍼즐 → 구조 → 탈출", 390, 220);
  }
  tutorialCtx.textAlign = "left";
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
  invulnerable = 0;
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

function updatePanels() {
  stageBox.innerHTML = `
        <b>
            ${level().title}
        </b>
        <br><br>
        ${level().story}
    `;
  const minutes = Math.floor(state.time / 60);
  const seconds = Math.floor(state.time % 60)
    .toString()
    .padStart(2, "0");
  statusBox.innerHTML = `
        <div class="stat">
            <b>진행</b>
            ${currentLevelIndex + 1}/3
        </div>
        <div class="stat">
            <b>남은 시간</b>
            ${minutes}:${seconds}
        </div>
        <div class="stat">
            <b>체력</b>
            ${"❤️".repeat(Math.max(0, state.hearts))}
        </div>
        <div class="stat">
            <b>스태미나</b>
            ${Math.round(state.stamina)}/100
        </div>
        <div class="stat">
            <b>상태</b>
            ${
              state.hidden
                ? "🫥 숨는 중"
                : state.chaseTimer > 0
                  ? "🚨 추격 중"
                  : "탐색 중"
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

  if (level().type === "collect") {
    progressTitle.innerHTML = "🎒 인벤토리";
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
    progressBox.innerHTML = `
            <div class="item">
                ${state.hasKeycard ? "✅" : "⬜"}
                출입카드
            </div>
            <div class="item">
                ${state.hasFuse ? "✅" : "⬜"}
                퓨즈
            </div>
            <div class="item">
                ${state.hasBattery ? "✅" : "⬜"}
                비상 배터리
            </div>
            <div class="item">
                ${state.powerOn ? "✅" : "⬜"}
                전원 복구
            </div>
            <div class="item">
                ${state.hasMasterKey ? "✅" : "⬜"}
                마스터 키
            </div>
        `;
  }

  // ========================================================
  // STAGE 2
  // ========================================================

  else if (level().type === "switch") {
    progressTitle.innerHTML = "🖥️ 격리 시스템";
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
    progressBox.innerHTML = `
            <div class="item">
                단말기 진행:
                <b>
                    ${state.switchProgress}/3
                </b>
            </div>
            <div class="item">
                잘못 누르면
                <b>
                    초기화 + 시간 -20초
                </b>
            </div>
        `;
  }

  // ========================================================
  // STAGE 3
  // ========================================================

  else {
    progressTitle.innerHTML = "🩺 구조 현황";
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
                <b>
                    구조 완료
                </b>
                ${rescueCount()}/3
            </div>
            ${state.patients
              .map(
                (patient) => `
                    <div class="item">
                        ${
                          patient.rescued
                            ? "✅ 구조 완료"
                            : patient.following
                              ? "🚶 호송 중"
                              : patient.stabilized
                                ? "🩺 안정화 완료"
                                : "⬜ 미발견/미처치"
                        }
                        · 환자 ${patient.id}
                    </div>
                `,
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
  if (player.walking) {
    player.walkTimer += dt;
    if (player.walkTimer > 0.14) {
      player.walkFrame = 1 - player.walkFrame;
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
    state.chaseTimer = 20;

    // 빨간 경고등
    state.event.alarm = 20;
    setMessage(
      "⚡ 발전기 복구 성공! 경보가 울리며 그림자가 20초 동안 추격한다! 달리거나 숨는 곳을 이용해!",
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
      state.chaseTimer = 15;
      state.event.alarm = 15;
      setMessage("✅ 격리 시스템 해제! 경보 때문에 그림자가 15초간 추격한다!");
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

        // 마지막 25초 추격
        state.chaseTimer = 25;
        state.event.alarm = 25;
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

function updateGhosts(dt) {
  if (invulnerable > 0) {
    invulnerable -= dt;
  }

  // 적 속도 증가 이벤트가 활성화된 경우
  const boosted = state.event.enemyBoost > 0 ? 1.5 : 1;
  ghosts.forEach((ghost) => {
    const chasing = state.chaseTimer > 0 && !state.hidden;
    const target = chasing ? playerCenter() : ghost.path[ghost.pathIndex];
    const cx = ghost.x + ghost.w / 2;
    const cy = ghost.y + ghost.h / 2;
    const tx = Math.floor(cx / TILE);
    const ty = Math.floor(cy / TILE);
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
        if (chasing) ghost.nextStep = { x: target.x, y: target.y };
      } else {
        ghost.nextStep = findGhostStep(tx, ty, targetX, targetY);
      }
    }
    if (!chasing && Math.hypot(target.x - cx, target.y - cy) < 3) {
      ghost.pathIndex = (ghost.pathIndex + 1) % ghost.path.length;
    }
    if (ghost.nextStep) {
      const dx = ghost.nextStep.x - cx;
      const dy = ghost.nextStep.y - cy;
      const distance = Math.hypot(dx, dy);
      const step = Math.min(distance, ghost.speed * boosted * (chasing ? 1.65 : 1) * dt);
      if (distance > 0) {
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
        // 체력 감소
        state.hearts -= 1;

        // 연속 충돌 방지
        invulnerable = 1.4;
        const start = findTile("S");

        // 시작 위치로 복귀
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
      setMessage("✅ 그림자의 추격이 끝났어. 다시 순찰 상태로 돌아갔어.");
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
// Canvas 사각형
// ============================================================

function rect(x, y, w, h, color) {
  ctx.fillStyle = color;
  ctx.fillRect(Math.round(x), Math.round(y), w, h);
}

// ============================================================
// 오브젝트 이름표
// ============================================================

function drawLabel(text, centerX, y) {
  ctx.save();
  ctx.font = '9px "Malgun Gothic", sans-serif';
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  const width = Math.min(ctx.measureText(text).width + 8, 82);
  rect(centerX - width / 2, y - 7, width, 13, "rgba(18,34,42,0.82)");
  ctx.fillStyle = "#ffffff";
  ctx.fillText(text, centerX, y);
  ctx.restore();
}

// ============================================================
// 바닥
// ============================================================

function drawFloor() {
  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      if (level().map[y][x] !== "#") {
        const floorColor =
          (x + y) % 2 === 0 ? level().palette.floor1 : level().palette.floor2;
        rect(x * TILE, y * TILE, TILE, TILE, floorColor);
      }
    }
  }
}

// ============================================================
// 벽
// ============================================================

function drawWalls() {
  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      if (level().map[y][x] === "#") {
        rect(x * TILE, y * TILE, TILE, TILE, level().palette.wall1);
        rect(
          x * TILE + 3,
          y * TILE + 3,
          TILE - 6,
          TILE - 6,
          level().palette.wall2,
        );
        rect(
          x * TILE + 6,
          y * TILE + 6,
          TILE - 12,
          TILE - 12,
          level().palette.wall3,
        );
      }
    }
  }
}

// ============================================================
// 병원 공통 오브젝트
// ============================================================

function drawFurniture() {
  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      const symbol = level().map[y][x];
      const px = x * TILE;
      const py = y * TILE;

      // 창문
      if (symbol === "W") {
        rect(px + 3, py + 2, 26, 19, "#9fb7c1");
        rect(px + 5, py + 4, 22, 15, "#153954");
        drawLabel("창문", px + 16, py + 28);
      }

      // 안내 데스크
      if (symbol === "T") {
        rect(px + 4, py + 5, 24, 13, "#8d674a");
        rect(px + 4, py + 3, 24, 4, "#bb916b");
        drawLabel("안내 데스크", px + 16, py + 28);
      }

      // 침대
      if (symbol === "H") {
        rect(px + 2, py + 5, 28, 15, "#d8e6eb");
        rect(px + 4, py + 7, 9, 6, "#b9d5df");
        drawLabel("병원 침대", px + 16, py + 28);
      }

      // 간호 스테이션
      if (symbol === "N") {
        rect(px + 3, py + 6, 26, 13, "#e7f0f3");
        rect(px + 5, py + 3, 22, 5, "#73a8ba");
        drawLabel("간호 스테이션", px + 16, py + 28);
      }

      // 휠체어
      if (symbol === "Q") {
        rect(px + 7, py + 4, 10, 6, "#66859b");
        rect(px + 4, py + 12, 8, 8, "#33474f");
        rect(px + 17, py + 12, 8, 8, "#33474f");
        drawLabel("휠체어", px + 16, py + 28);
      }

      // 자판기
      if (symbol === "V") {
        rect(px + 7, py + 2, 18, 22, "#bd4755");
        rect(px + 9, py + 5, 14, 8, "#cfebf4");
        drawLabel("자판기", px + 16, py + 29);
      }

      // 숨는 곳
      if (symbol === "h") {
        rect(px + 5, py + 3, 22, 20, "#657a86");
        rect(px + 8, py + 5, 16, 17, "#d2e0e5");
        rect(px + 15, py + 5, 2, 17, "#8aa0aa");
        drawLabel("숨는 곳", px + 16, py + 29);
      }

      // CCTV
      if (symbol === "Z") {
        rect(px + 4, py + 3, 24, 18, "#344b53");
        rect(px + 7, py + 6, 18, 10, "#6bb2d2");
        drawLabel("CCTV", px + 16, py + 29);
      }

      // STAGE 3 대피구역
      if (symbol === "Y") {
        rect(px + 2, py + 3, 28, 18, "#5ba878");
        rect(px + 6, py + 7, 20, 10, "#9fe2b8");
        drawLabel("대피 구역", px + 16, py + 29);
      }
    }
  }
}

// ============================================================
// 출구
// ============================================================

function drawExitDoor(px, py, label, open) {
  rect(px + 2, py + 1, 28, 23, "#6e858e");
  rect(px + 5, py + 3, 10, 20, "#a4b9c0");
  rect(px + 17, py + 3, 10, 20, "#a4b9c0");

  // 초록 = 사용 가능 / 빨강 = 잠김
  rect(px + 10, py + 5, 12, 3, open ? "#6fe484" : "#d45f68");
  drawLabel(label, px + 16, py + 29);
}

// ============================================================
// 스테이지 특수 오브젝트
// ============================================================

function drawStageObjects() {
  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      const symbol = level().map[y][x];
      const px = x * TILE;
      const py = y * TILE;

      // =================================================
      // STAGE 1
      // =================================================

      if (level().type === "collect") {
        // 카드
        if (symbol === "K" && !state.hasKeycard) {
          rect(px + 6, py + 5, 20, 11, "#438bed");
          rect(px + 9, py + 8, 5, 4, "#e4f4ff");
          drawLabel("출입카드", px + 16, py + 25);
        }

        // 퓨즈
        if (symbol === "F" && !state.hasFuse) {
          rect(px + 9, py + 3, 14, 17, "#e5c44e");
          drawLabel("퓨즈", px + 16, py + 27);
        }

        // 배터리
        if (symbol === "B" && !state.hasBattery) {
          rect(px + 9, py + 3, 14, 18, "#46a760");
          drawLabel("비상 배터리", px + 16, py + 28);
        }

        // 발전기
        if (symbol === "P") {
          rect(px + 3, py + 4, 26, 18, "#485d66");
          rect(px + 8, py + 8, 16, 8, "#273940");
          drawLabel("발전기", px + 16, py + 29);
        }

        // 마스터 키
        if (symbol === "M" && !state.hasMasterKey) {
          rect(px + 7, py + 7, 18, 6, "#f0c13b");
          drawLabel("마스터 키", px + 16, py + 25);
        }

        // 카드 보안문
        if (symbol === "C") {
          rect(
            px + 5,
            py + 1,
            22,
            23,
            state.hasKeycard ? "#74aa89" : "#517fb5",
          );
          drawLabel("보안문", px + 16, py + 29);
        }

        // 전원문
        if (symbol === "D") {
          rect(px + 5, py + 1, 22, 23, state.powerOn ? "#74aa89" : "#806044");
          drawLabel("전원문", px + 16, py + 29);
        }

        // 엘리베이터
        if (symbol === "E") {
          drawExitDoor(
            px,
            py,
            "엘리베이터",
            state.hasMasterKey && state.powerOn,
          );
        }
      }

      // =================================================
      // STAGE 2
      // =================================================

      if (level().type === "switch") {
        // 단말기
        if (["A", "B", "C"].includes(symbol)) {
          rect(px + 6, py + 3, 20, 20, "#344b53");
          rect(px + 9, py + 6, 14, 9, "#6bb2d2");
          drawLabel("단말기 " + symbol, px + 16, py + 29);
        }

        // 연구 메모
        if (symbol === "L") {
          rect(px + 8, py + 4, 16, 19, "#efe2b6");
          drawLabel("연구 메모", px + 16, py + 29);
        }

        // 제독실 출구
        if (symbol === "X") {
          drawExitDoor(px, py, "제독실 출구", state.switchProgress === 3);
        }
      }

      // =================================================
      // STAGE 3
      // =================================================

      if (level().type === "rescue" && symbol === "R") {
        drawExitDoor(px, py, "옥상 출구", rescueCount() === 3);
      }
    }
  }
}

// ============================================================
// 환자
// ============================================================

function drawPatients() {
  if (level().type !== "rescue") {
    return;
  }
  for (const patient of state.patients) {
    // 이미 구조되거나 따라오면 원래 자리에서는 숨김
    if (patient.rescued || patient.following) {
      continue;
    }
    const px = patient.x * TILE;
    const py = patient.y * TILE;
    const colors = ["#77b8e8", "#83c985", "#e5a26c"];

    // 머리
    rect(px + 11, py + 3, 10, 5, "#544038");

    // 얼굴
    rect(px + 12, py + 7, 8, 7, "#efc3a5");

    // 환자복
    rect(px + 9, py + 14, 14, 9, colors[patient.id - 1]);
    drawLabel("환자 " + patient.id, px + 16, py + 29);
  }
}

// ============================================================
// 호송 중인 환자
// ============================================================

function drawEscortPatient() {
  if (state.escortPatientId === null) {
    return;
  }
  const patient = state.patients.find(
    (item) => item.id === state.escortPatientId,
  );

  // 플레이어 뒤쪽에 표시
  const x = player.x - 22;
  const y = player.y + 9;
  rect(x + 7, y, 10, 5, "#544038");
  rect(x + 8, y + 5, 8, 7, "#efc3a5");
  rect(x + 5, y + 12, 14, 9, "#88b9d5");
  ctx.fillStyle = "#ffffff";
  ctx.font = '9px "Malgun Gothic"';
  ctx.fillText("환자 " + patient.id, x, y + 30);
}

// ============================================================
// 야간 기록
// ============================================================

function drawRecords() {
  for (const record of state.records) {
    if (record.collected) {
      continue;
    }
    const px = record.x * TILE;
    const py = record.y * TILE;
    rect(px + 9, py + 4, 14, 17, "#f4e7b8");
    rect(px + 12, py + 8, 8, 2, "#8e805f");
    drawLabel("야간 기록", px + 16, py + 29);
  }
}

// ============================================================
// 플레이어 그리기
// ============================================================

function drawPlayer() {
  const x = Math.round(player.x);
  const y = Math.round(player.y);

  // 숨는 중이면 반투명
  if (state.hidden) {
    ctx.globalAlpha = 0.35;
  }

  // 바닥 그림자
  rect(x + 5, y + 34, 20, 4, "rgba(0,0,0,0.20)");

  // 검은 외곽선
  rect(x + 6, y, 18, 5, "#253038");
  rect(x + 4, y + 4, 22, 12, "#253038");
  rect(x + 6, y + 16, 18, 17, "#253038");

  // 머리
  rect(x + 7, y + 1, 16, 5, "#684334");
  rect(x + 5, y + 5, 20, 5, "#79513e");

  // 얼굴
  rect(x + 9, y + 8, 12, 9, "#f3c4a3");

  // 눈
  if (player.facing === "down") {
    rect(x + 11, y + 11, 2, 2, "#1e2528");
    rect(x + 17, y + 11, 2, 2, "#1e2528");
  }

  // 의료복
  rect(x + 11, y + 19, 9, 11, "#4ca8bb");

  // 흰 의사가운
  rect(x + 6, y + 19, 6, 14, "#ffffff");
  rect(x + 19, y + 19, 6, 14, "#ffffff");

  // 바지
  rect(x + 9, y + 31, 6, 5, "#344f76");
  rect(x + 17, y + 31, 6, 5, "#344f76");

  // 신발
  rect(x + 8, y + 35, 7, 3, "#202b32");
  rect(x + 17, y + 35, 7, 3, "#202b32");
  ctx.globalAlpha = 1;
}

// ============================================================
// 그림자 그리기
// ============================================================

function drawGhost(ghost) {
  const x = Math.round(ghost.x);
  const y = Math.round(ghost.y);
  rect(x + 2, y + 2, 16, 13, ghost.color);
  rect(x + 4, y + 14, 4, 6, ghost.color);
  rect(x + 9, y + 14, 4, 6, ghost.color);
  rect(x + 14, y + 14, 4, 6, ghost.color);

  // 눈
  rect(x + 5, y + 6, 2, 2, "#ffffff");
  rect(x + 12, y + 6, 2, 2, "#ffffff");
}

// ============================================================
// 어둠 및 경고 효과
// ============================================================

function drawDarkness() {
  let alpha = currentLevelIndex === 0 ? (state.powerOn ? 0.05 : 0.23) : 0.12;

  // 추가 정전
  if (state.event.blackout > 0) {
    alpha = 0.55;
  }
  ctx.fillStyle = "rgba(5,18,28," + alpha + ")";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // 경고등
  if (state.event.alarm > 0 && Math.floor(state.event.alarm * 6) % 2 === 0) {
    ctx.fillStyle = "rgba(210,40,55,0.14)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }
}

// ============================================================
// 미니게임 화면
// ============================================================

function drawMiniGame() {
  if (!state.miniGame) {
    return;
  }
  const game = state.miniGame;
  rect(245, 220, 566, 190, "rgba(17,31,38,0.96)");
  ctx.fillStyle = "#ffffff";
  ctx.textAlign = "center";
  ctx.font = 'bold 18px "Malgun Gothic"';

  // 발전기
  if (game.type === "generator") {
    ctx.fillText("발전기 수리", 528, 255);
    ctx.font = '13px "Malgun Gothic"';
    ctx.fillText("노란 표시가 초록 구간에 들어왔을 때 Space", 528, 285);
    drawTimingBar(game.pos, 330);
  }

  // 환자 1
  if (game.type === "patientTiming") {
    ctx.fillText("환자 1 상태 안정화", 528, 250);
    ctx.font = '13px "Malgun Gothic"';
    ctx.fillText(
      "초록 구간에 맞춰 Space · 성공 " + game.success + "/2",
      528,
      280,
    );
    drawTimingBar(game.pos, 330);
  }

  // 환자 2
  if (game.type === "patientDirection") {
    ctx.fillText("환자 2 · 방향 기억", 528, 250);
    ctx.font = '30px "Malgun Gothic"';
    if (game.reveal > 0) {
      ctx.fillText(game.sequence.map(directionSymbol).join("   "), 528, 325);
    } else {
      ctx.fillText("입력 " + game.inputIndex + "/5", 528, 325);
    }
  }

  // 환자 3
  if (game.type === "patientMemory") {
    ctx.fillText("환자 3 · 숫자 기억", 528, 250);
    ctx.font = "32px monospace";
    if (game.reveal > 0) {
      ctx.fillText(game.sequence.join("   "), 528, 325);
    } else {
      ctx.fillText("입력 " + game.inputIndex + "/5", 528, 325);
      ctx.font = '13px "Malgun Gothic"';
      ctx.fillText("키보드 숫자 1~4 사용", 528, 360);
    }
  }
  ctx.textAlign = "left";
}

// ============================================================
// 타이밍 바
// ============================================================

function drawTimingBar(position, y) {
  // 전체 바
  rect(330, y, 396, 20, "#233740");

  // 성공 영역
  rect(330 + 396 * 0.4, y, 396 * 0.2, 20, "#52d981");

  // 노란 포인터
  const pointer = 330 + 396 * position;
  rect(pointer - 4, y - 6, 8, 32, "#ffe067");
}

// ============================================================
// 방향키 이름 → 화살표
// ============================================================

function directionSymbol(key) {
  const map = {
    ArrowUp: "↑",
    ArrowDown: "↓",
    ArrowLeft: "←",
    ArrowRight: "→",
  };
  return map[key];
}

// ============================================================
// HUD
// ============================================================

function drawHud() {
  rect(0, 0, canvas.width, 26, "rgba(18,42,52,0.90)");
  ctx.fillStyle = "#ffffff";
  ctx.font = "12px monospace";
  const minutes = Math.floor(state.time / 60);
  const seconds = Math.floor(state.time % 60)
    .toString()
    .padStart(2, "0");
  ctx.fillText("STAGE " + (currentLevelIndex + 1) + "/3", 10, 17);
  ctx.fillText("TIME " + minutes + ":" + seconds, 125, 17);
  ctx.fillText("HP " + "♥".repeat(Math.max(0, state.hearts)), 250, 17);
  ctx.fillText("STA " + Math.round(state.stamina), 370, 17);

  // 추격 상태
  if (state.chaseTimer > 0) {
    ctx.fillText("CHASE " + Math.ceil(state.chaseTimer) + "s", 470, 17);
  }

  // 숨는 상태
  if (state.hidden) {
    ctx.fillText("HIDDEN", 600, 17);
  }
}

// ============================================================
// 전체 렌더링
// ============================================================

function render() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawFloor();
  drawWalls();
  drawFurniture();
  drawStageObjects();
  drawRecords();
  drawPatients();

  // 어둠을 캐릭터보다 먼저 그려 캐릭터 가시성 유지
  drawDarkness();
  ghosts.forEach(drawGhost);
  drawEscortPatient();
  drawPlayer();
  drawMiniGame();
  drawHud();
}

// ============================================================
// 게임 루프
// ============================================================

function gameLoop(now) {
  const dt = Math.min((now - lastTime) / 1000, 0.05);
  lastTime = now;

  // 프롤로그가 끝난 뒤에만 실제 게임 실행
  if (state && tutorialFinished) {
    update(dt);
    render();
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

window.addEventListener("load", () => {
  // 게임을 바로 시작하지 않고 프롤로그부터 보여준다.
  showPrologue();
  requestAnimationFrame(gameLoop);
});

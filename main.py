import pygame
import sys
import random
from pathlib import Path


# ============================================================
# NEURO NIGHT SHIFT
# 신경계 병원 야간 근무 게임
# ============================================================

pygame.init()


# ============================================================
# 1. 기본 화면 설정
# ============================================================

WIDTH = 1200
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEURO NIGHT SHIFT")

clock = pygame.time.Clock()

FPS = 60


# ============================================================
# 2. 색상
# ============================================================

BG = (29, 37, 45)
FLOOR = (201, 211, 214)
WALL = (91, 108, 116)

WHITE = (245, 247, 248)
BLACK = (25, 29, 31)

BLUE = (74, 118, 158)
LIGHT_BLUE = (153, 193, 213)

GREEN = (88, 154, 115)
LIGHT_GREEN = (178, 221, 193)

RED = (176, 72, 82)
LIGHT_RED = (238, 184, 190)

YELLOW = (218, 182, 86)
CREAM = (244, 235, 207)

PURPLE = (130, 112, 170)

GRAY = (120, 132, 138)
DARK_GRAY = (59, 71, 78)

PLAYER_COLOR = (68, 139, 190)
PATIENT_COLOR = (204, 156, 139)


# ============================================================
# 3. 글꼴
# ============================================================

font_big = pygame.font.SysFont(
    "malgungothic",
    42,
    bold=True
)

font_title = pygame.font.SysFont(
    "malgungothic",
    29,
    bold=True
)

font = pygame.font.SysFont(
    "malgungothic",
    21
)

font_small = pygame.font.SysFont(
    "malgungothic",
    17
)


# ============================================================
# 4. 병원 맵 공간
# ============================================================

# 접수대
reception = pygame.Rect(
    410,
    100,
    300,
    90
)

# 진료실
treatment_room = pygame.Rect(
    820,
    90,
    310,
    230
)

# 물품실
supply_room = pygame.Rect(
    60,
    390,
    280,
    240
)

# 변칙 환자 격리구역
quarantine = pygame.Rect(
    840,
    440,
    280,
    180
)

# 병원 입구
entrance = pygame.Rect(
    520,
    650,
    160,
    60
)

# 환자 진료 위치
patient_bed_position = pygame.Vector2(
    955,
    230
)

# 환자 접수 위치
patient_reception_position = pygame.Vector2(
    560,
    230
)


# ============================================================
# 5. 플레이어
# ============================================================

player = pygame.Rect(
    560,
    540,
    38,
    46
)

player_speed = 4


# ============================================================
# 6. 환자 데이터
# ============================================================

PATIENT_DATA = [

    {
        "name": "환자 A",
        "age": 19,

        "symptom":
            "두통과 어지럼증을 호소하고 있습니다.",

        "record":
            "접수번호 N-1204 / 팔찌번호 N-1204",

        "anomaly": False,

        "needs_more_check": False,

        "item": "냉찜질 팩",

        "image": "assets/patient01.png",

        "medical_note":
            "두통은 원인이 다양하므로 증상만으로 판단하지 않고 "
            "추가적인 의료진 평가가 필요합니다."
    },


    {
        "name": "환자 B",
        "age": 46,

        "symptom":
            "손끝 감각이 평소와 다르다고 합니다.",

        "record":
            "접수번호 N-3817 / 팔찌번호 N-3187",

        "anomaly": True,

        "needs_more_check": False,

        "item": None,

        "image": "assets/patient02.png",

        "medical_note":
            "접수번호와 환자 팔찌 번호가 일치하지 않습니다. "
            "의료기관에서는 정확한 환자 확인이 매우 중요합니다."
    },


    {
        "name": "환자 C",
        "age": 17,

        "symptom":
            "반복적으로 두통을 느낀다고 합니다.",

        "record":
            "통증 발생 시간과 위치에 대한 기록이 없습니다.",

        "anomaly": False,

        "needs_more_check": True,

        "item": "신경학적 체크리스트",

        "image": "assets/patient03.png",

        "medical_note":
            "증상이 언제 시작됐는지, 어느 부위에서 나타나는지 등의 "
            "정보가 부족하면 추가 확인이 필요합니다."
    },


    {
        "name": "환자 D",
        "age": 63,

        "symptom":
            "보행이 평소보다 불편하다고 합니다.",

        "record":
            "검사 예정일 : 2026년 11월 41일",

        "anomaly": True,

        "needs_more_check": False,

        "item": None,

        "image": "assets/patient04.png",

        "medical_note":
            "11월 41일은 존재할 수 없는 날짜입니다. "
            "환자의 질환이 아니라 기록 자체에 변칙이 있는 경우입니다."
    },


    {
        "name": "환자 E",
        "age": 72,

        "symptom":
            "최근 기억력 변화를 느낀다고 합니다.",

        "record":
            "환자 정보와 접수 기록이 정상적으로 일치합니다.",

        "anomaly": False,

        "needs_more_check": False,

        "item": "MRI 검사 안내서",

        "image": "assets/patient05.png",

        "medical_note":
            "기억력 변화는 다양한 원인과 관련될 수 있어 "
            "진료와 평가를 통해 원인을 확인해야 합니다."
    },


    {
        "name": "환자 F",
        "age": 31,

        "symptom":
            "지속적인 어지럼증을 호소합니다.",

        "record":
            "접수시간 02:21 / 퇴원시간 01:43",

        "anomaly": True,

        "needs_more_check": False,

        "item": None,

        "image": "assets/patient06.png",

        "medical_note":
            "접수하기 전에 퇴원한 것으로 기록되어 있어 "
            "시간 순서가 논리적으로 맞지 않습니다."
    }

]


# ============================================================
# 7. 게임 상태 변수
# ============================================================

score = 0
lives = 3

current_patient_index = 0

game_over = False
game_started = False

show_record = False
show_message = False

message = ""

current_patient = None

patient_rect = pygame.Rect(
    560,
    680,
    38,
    46
)

patient_state = "entering"

# entering
# reception
# treatment
# waiting_item
# completed
# leaving
# quarantine

inventory = None

needed_item = None

decision_made = False

additional_check_done = False

patient_order = list(
    range(len(PATIENT_DATA))
)

random.shuffle(patient_order)


# ============================================================
# 8. 이미지 불러오기 함수
# ============================================================

def load_patient_image(path):

    image_path = Path(path)

    if not image_path.exists():
        return None

    try:

        image = pygame.image.load(
            str(image_path)
        ).convert_alpha()

        image = pygame.transform.smoothscale(
            image,
            (210, 210)
        )

        return image

    except pygame.error:

        return None


# ============================================================
# 9. 텍스트 함수
# ============================================================

def draw_text(
    text,
    x,
    y,
    color=BLACK,
    selected_font=None
):

    if selected_font is None:
        selected_font = font

    surface = selected_font.render(
        text,
        True,
        color
    )

    screen.blit(
        surface,
        (x, y)
    )


def draw_center_text(
    text,
    center_x,
    y,
    color=WHITE,
    selected_font=None
):

    if selected_font is None:
        selected_font = font

    surface = selected_font.render(
        text,
        True,
        color
    )

    rect = surface.get_rect(
        center=(center_x, y)
    )

    screen.blit(
        surface,
        rect
    )


# ============================================================
# 10. 환자 불러오기
# ============================================================

def load_next_patient():

    global current_patient
    global patient_rect
    global patient_state
    global show_record
    global decision_made
    global additional_check_done
    global needed_item
    global inventory

    if current_patient_index >= len(patient_order):
        return False

    data_index = patient_order[
        current_patient_index
    ]

    current_patient = PATIENT_DATA[
        data_index
    ]

    patient_rect.x = 560
    patient_rect.y = 680

    patient_state = "entering"

    show_record = False

    decision_made = False

    additional_check_done = False

    needed_item = None

    inventory = None

    return True


# ============================================================
# 11. 게임 초기화
# ============================================================

def reset_game():

    global score
    global lives
    global current_patient_index
    global game_over
    global game_started
    global patient_order
    global inventory

    score = 0
    lives = 3

    current_patient_index = 0

    game_over = False
    game_started = True

    inventory = None

    patient_order = list(
        range(len(PATIENT_DATA))
    )

    random.shuffle(
        patient_order
    )

    load_next_patient()


# ============================================================
# 12. 거리 판정
# ============================================================

def near_object(
    rect1,
    rect2,
    distance=75
):

    expanded = rect2.inflate(
        distance,
        distance
    )

    return expanded.colliderect(
        rect1
    )


# ============================================================
# 13. 플레이어 이동
# ============================================================

def move_player():

    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dx -= player_speed

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dx += player_speed

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        dy -= player_speed

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dy += player_speed


    player.x += dx
    player.y += dy


    # 화면 밖 이동 방지
    player.x = max(
        10,
        min(
            player.x,
            WIDTH - player.width - 10
        )
    )

    player.y = max(
        70,
        min(
            player.y,
            HEIGHT - player.height - 10
        )
    )


# ============================================================
# 14. 환자 NPC 이동
# ============================================================

def move_patient():

    global patient_state

    if current_patient is None:
        return


    # --------------------------------------------------------
    # 병원 입구 -> 접수대
    # --------------------------------------------------------

    if patient_state == "entering":

        target = patient_reception_position

        current = pygame.Vector2(
            patient_rect.x,
            patient_rect.y
        )

        direction = target - current

        if direction.length() > 5:

            direction = direction.normalize()

            patient_rect.x += direction.x * 2
            patient_rect.y += direction.y * 2

        else:

            patient_rect.x = int(target.x)
            patient_rect.y = int(target.y)

            patient_state = "reception"


    # --------------------------------------------------------
    # 접수대 -> 진료실
    # --------------------------------------------------------

    elif patient_state == "treatment":

        target = patient_bed_position

        current = pygame.Vector2(
            patient_rect.x,
            patient_rect.y
        )

        direction = target - current

        if direction.length() > 5:

            direction = direction.normalize()

            patient_rect.x += direction.x * 2

            patient_rect.y += direction.y * 2

        else:

            patient_rect.x = int(target.x)
            patient_rect.y = int(target.y)

            patient_state = "waiting_item"


    # --------------------------------------------------------
    # 종료 후 밖으로 이동
    # --------------------------------------------------------

    elif patient_state == "leaving":

        target = pygame.Vector2(
            580,
            760
        )

        current = pygame.Vector2(
            patient_rect.x,
            patient_rect.y
        )

        direction = target - current

        if direction.length() > 5:

            direction = direction.normalize()

            patient_rect.x += direction.x * 3

            patient_rect.y += direction.y * 3


# ============================================================
# 15. 맵 그리기
# ============================================================

def draw_map():

    screen.fill(
        FLOOR
    )


    # --------------------------------------------------------
    # 바닥 구역선
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        WALL,
        (0, 60, WIDTH, 12)
    )


    # --------------------------------------------------------
    # 접수대
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        BLUE,
        reception,
        border_radius=12
    )

    draw_center_text(
        "RECEPTION",
        reception.centerx,
        reception.centery,
        WHITE,
        font_title
    )


    # --------------------------------------------------------
    # 진료실
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        LIGHT_GREEN,
        treatment_room,
        border_radius=14
    )

    pygame.draw.rect(
        screen,
        GREEN,
        treatment_room,
        4,
        border_radius=14
    )

    draw_text(
        "🩺 진료실",
        840,
        110,
        BLACK,
        font_title
    )


    # 병상
    pygame.draw.rect(
        screen,
        WHITE,
        (930, 190, 150, 70),
        border_radius=12
    )

    draw_text(
        "BED",
        982,
        212,
        GRAY,
        font_small
    )


    # --------------------------------------------------------
    # 물품실
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        CREAM,
        supply_room,
        border_radius=14
    )

    pygame.draw.rect(
        screen,
        YELLOW,
        supply_room,
        4,
        border_radius=14
    )

    draw_text(
        "📦 물품실",
        90,
        415,
        BLACK,
        font_title
    )


    # 선반
    for y in [
        480,
        535,
        590
    ]:

        pygame.draw.rect(
            screen,
            YELLOW,
            (100, y, 190, 28),
            border_radius=5
        )


    # --------------------------------------------------------
    # 격리 구역
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        LIGHT_RED,
        quarantine,
        border_radius=14
    )

    pygame.draw.rect(
        screen,
        RED,
        quarantine,
        4,
        border_radius=14
    )

    draw_text(
        "⚠ 기록 확인 구역",
        865,
        465,
        BLACK,
        font_title
    )


    # --------------------------------------------------------
    # 입구
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        LIGHT_BLUE,
        entrance,
        border_radius=12
    )

    draw_center_text(
        "병원 입구",
        entrance.centerx,
        675,
        BLACK,
        font
    )


# ============================================================
# 16. 플레이어 그리기
# ============================================================

def draw_player():

    pygame.draw.rect(
        screen,
        PLAYER_COLOR,
        player,
        border_radius=9
    )

    pygame.draw.circle(
        screen,
        (236, 202, 180),
        (
            player.centerx,
            player.y + 10
        ),
        9
    )

    draw_center_text(
        "YOU",
        player.centerx,
        player.y - 11,
        DARK_GRAY,
        font_small
    )


# ============================================================
# 17. 환자 그리기
# ============================================================

def draw_patient():

    if current_patient is None:
        return


    pygame.draw.rect(
        screen,
        PATIENT_COLOR,
        patient_rect,
        border_radius=9
    )

    pygame.draw.circle(
        screen,
        (238, 204, 184),
        (
            patient_rect.centerx,
            patient_rect.y + 10
        ),
        9
    )

    draw_center_text(
        current_patient["name"],
        patient_rect.centerx,
        patient_rect.y - 12,
        DARK_GRAY,
        font_small
    )


# ============================================================
# 18. 상단 HUD
# ============================================================

def draw_hud():

    pygame.draw.rect(
        screen,
        BG,
        (0, 0, WIDTH, 60)
    )

    draw_text(
        "NEURO NIGHT SHIFT",
        20,
        15,
        WHITE,
        font_title
    )

    draw_text(
        f"CASE {current_patient_index + 1}/{len(PATIENT_DATA)}",
        560,
        18,
        WHITE,
        font
    )

    draw_text(
        f"SCORE {score}",
        760,
        18,
        WHITE,
        font
    )

    hearts = "♥ " * lives

    draw_text(
        hearts,
        980,
        17,
        LIGHT_RED,
        font
    )


# ============================================================
# 19. 도움말
# ============================================================

def draw_help():

    help_text = ""

    if patient_state == "reception" and near_object(
        player,
        patient_rect
    ):

        help_text = "E : 환자 기록 확인"


    elif patient_state == "waiting_item":

        if needed_item and near_object(
            player,
            supply_room
        ):

            help_text = (
                f"E : {needed_item} 가져오기"
            )


        elif inventory and near_object(
            player,
            patient_rect
        ):

            help_text = (
                "E : 환자에게 물품 전달"
            )


    if help_text:

        pygame.draw.rect(
            screen,
            BG,
            (
                390,
                640,
                420,
                52
            ),
            border_radius=12
        )

        draw_center_text(
            help_text,
            600,
            666,
            WHITE,
            font
        )


# ============================================================
# 20. 환자 기록 창
# ============================================================

def draw_patient_record():

    if not show_record:
        return


    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 155)
    )

    screen.blit(
        overlay,
        (0, 0)
    )


    panel = pygame.Rect(
        190,
        85,
        820,
        550
    )

    pygame.draw.rect(
        screen,
        WHITE,
        panel,
        border_radius=22
    )


    pygame.draw.rect(
        screen,
        BLUE,
        (
            panel.x,
            panel.y,
            panel.width,
            65
        ),
        border_top_left_radius=22,
        border_top_right_radius=22
    )


    draw_text(
        "PATIENT CHECK-IN RECORD",
        225,
        104,
        WHITE,
        font_title
    )


    # --------------------------------------------------------
    # 환자 사진
    # --------------------------------------------------------

    patient_image = load_patient_image(
        current_patient["image"]
    )


    if patient_image:

        screen.blit(
            patient_image,
            (
                235,
                190
            )
        )


    else:

        pygame.draw.rect(
            screen,
            LIGHT_BLUE,
            (
                235,
                190,
                210,
                210
            ),
            border_radius=15
        )

        draw_center_text(
            "환자 사진",
            340,
            290,
            DARK_GRAY,
            font_title
        )


    # --------------------------------------------------------
    # 환자 정보
    # --------------------------------------------------------

    draw_text(
        current_patient["name"],
        490,
        185,
        BLACK,
        font_title
    )


    draw_text(
        f"나이 : {current_patient['age']}세",
        490,
        235
    )


    draw_text(
        "증상",
        490,
        285,
        BLUE,
        font
    )


    draw_text(
        current_patient["symptom"],
        490,
        320,
        BLACK,
        font_small
    )


    draw_text(
        "접수 기록",
        490,
        370,
        BLUE,
        font
    )


    draw_text(
        current_patient["record"],
        490,
        405,
        BLACK,
        font_small
    )


    # --------------------------------------------------------
    # 선택 버튼 안내
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        LIGHT_GREEN,
        (
            225,
            485,
            220,
            60
        ),
        border_radius=10
    )

    draw_center_text(
        "1  진료실 입장",
        335,
        515,
        BLACK,
        font
    )


    pygame.draw.rect(
        screen,
        CREAM,
        (
            490,
            485,
            220,
            60
        ),
        border_radius=10
    )

    draw_center_text(
        "2  추가 확인",
        600,
        515,
        BLACK,
        font
    )


    pygame.draw.rect(
        screen,
        LIGHT_RED,
        (
            755,
            485,
            220,
            60
        ),
        border_radius=10
    )

    draw_center_text(
        "3  변칙 차단",
        865,
        515,
        BLACK,
        font
    )


    draw_center_text(
        "ESC : 기록 닫기",
        600,
        590,
        GRAY,
        font_small
    )


# ============================================================
# 21. 메시지 창
# ============================================================

def draw_message_box():

    if not show_message:
        return


    pygame.draw.rect(
        screen,
        BG,
        (
            280,
            570,
            640,
            90
        ),
        border_radius=14
    )

    draw_center_text(
        message,
        600,
        615,
        WHITE,
        font_small
    )


# ============================================================
# 22. 환자 처리 판정
# ============================================================

def choose_patient_action(choice):

    global score
    global lives
    global show_record
    global patient_state
    global decision_made
    global needed_item
    global message
    global show_message
    global additional_check_done

    if decision_made:
        return


    correct_choice = None


    if current_patient["anomaly"]:

        correct_choice = "quarantine"


    elif current_patient["needs_more_check"]:

        correct_choice = "check"


    else:

        correct_choice = "treatment"


    # --------------------------------------------------------
    # 정답
    # --------------------------------------------------------

    if choice == correct_choice:

        score += 100

        decision_made = True

        show_record = False

        if choice == "quarantine":

            patient_state = "quarantine"

            score += 50

            message = (
                "변칙 기록을 발견했습니다! +150점"
            )

            show_message = True


        elif choice == "check":

            additional_check_done = True

            patient_state = "treatment"

            needed_item = current_patient[
                "item"
            ]

            message = (
                "추가 확인이 필요합니다. "
                "환자를 진료실로 안내합니다."
            )

            show_message = True


        elif choice == "treatment":

            patient_state = "treatment"

            needed_item = current_patient[
                "item"
            ]

            message = (
                "정상 접수입니다. "
                "환자가 진료실로 이동합니다."
            )

            show_message = True


    # --------------------------------------------------------
    # 오답
    # --------------------------------------------------------

    else:

        lives -= 1

        message = (
            "판단이 올바르지 않습니다. "
            "환자 기록을 다시 확인하세요."
        )

        show_message = True


# ============================================================
# 23. 물품 획득
# ============================================================

def collect_item():

    global inventory
    global message
    global show_message

    if needed_item is None:

        message = (
            "현재 필요한 물품이 없습니다."
        )

        show_message = True

        return


    if inventory is None:

        inventory = needed_item

        message = (
            f"{needed_item}을(를) 가져왔습니다."
        )

        show_message = True


    else:

        message = (
            "이미 물품을 가지고 있습니다."
        )

        show_message = True


# ============================================================
# 24. 환자에게 물품 적용
# ============================================================

def apply_item_to_patient():

    global inventory
    global patient_state
    global score
    global message
    global show_message

    if inventory != needed_item:

        message = (
            "필요한 물품을 먼저 가져오세요."
        )

        show_message = True

        return


    inventory = None

    score += 100

    patient_state = "leaving"

    message = (
        f"{needed_item} 전달 완료! +100점"
    )

    show_message = True


# ============================================================
# 25. 다음 환자
# ============================================================

def finish_current_patient():

    global current_patient_index
    global game_over

    current_patient_index += 1

    if (
        current_patient_index
        >= len(patient_order)
        or lives <= 0
    ):

        game_over = True

        return


    load_next_patient()


# ============================================================
# 26. 시작 화면
# ============================================================

def draw_start_screen():

    screen.fill(
        BG
    )


    draw_center_text(
        "NEURO NIGHT SHIFT",
        WIDTH // 2,
        170,
        WHITE,
        font_big
    )


    draw_center_text(
        "야간 신경계 병원 근무",
        WIDTH // 2,
        225,
        LIGHT_BLUE,
        font_title
    )


    draw_center_text(
        "환자의 기록을 확인하고 병원 안을 직접 이동하세요.",
        WIDTH // 2,
        310,
        WHITE,
        font
    )


    draw_center_text(
        "정상 환자는 진료실로, 기록 변칙은 차단해야 합니다.",
        WIDTH // 2,
        350,
        WHITE,
        font
    )


    draw_center_text(
        "진료 환자에게 필요한 물품은 물품실에서 직접 가져오세요.",
        WIDTH // 2,
        390,
        WHITE,
        font
    )


    pygame.draw.rect(
        screen,
        BLUE,
        (
            430,
            470,
            340,
            75
        ),
        border_radius=14
    )


    draw_center_text(
        "SPACE : 야간 근무 시작",
        WIDTH // 2,
        507,
        WHITE,
        font_title
    )


    draw_center_text(
        "이동 : WASD / 방향키   |   상호작용 : E",
        WIDTH // 2,
        610,
        GRAY,
        font_small
    )


# ============================================================
# 27. 게임 종료 화면
# ============================================================

def draw_game_over():

    screen.fill(
        BG
    )


    if score >= 900:

        grade = "S"

        comment = (
            "뛰어난 관찰력으로 야간 근무를 마쳤습니다!"
        )


    elif score >= 650:

        grade = "A"

        comment = (
            "환자 기록을 꼼꼼하게 확인했습니다."
        )


    elif score >= 400:

        grade = "B"

        comment = (
            "몇몇 기록을 놓쳤지만 근무를 완료했습니다."
        )


    else:

        grade = "C"

        comment = (
            "환자 기록을 조금 더 자세히 살펴보세요."
        )


    draw_center_text(
        "NIGHT SHIFT COMPLETE",
        WIDTH // 2,
        150,
        WHITE,
        font_big
    )


    draw_center_text(
        grade,
        WIDTH // 2,
        290,
        LIGHT_BLUE,
        pygame.font.SysFont(
            "arial",
            95,
            bold=True
        )
    )


    draw_center_text(
        f"FINAL SCORE : {score}",
        WIDTH // 2,
        390,
        WHITE,
        font_title
    )


    draw_center_text(
        comment,
        WIDTH // 2,
        445,
        WHITE,
        font
    )


    draw_center_text(
        "R : 다시 근무하기",
        WIDTH // 2,
        550,
        YELLOW,
        font_title
    )


# ============================================================
# 28. 메인 게임 루프
# ============================================================

running = True


while running:

    # --------------------------------------------------------
    # 이벤트 처리
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


        if event.type == pygame.KEYDOWN:

            # ------------------------------------------------
            # 시작 화면
            # ------------------------------------------------

            if not game_started:

                if event.key == pygame.K_SPACE:

                    reset_game()


            # ------------------------------------------------
            # 게임 종료 화면
            # ------------------------------------------------

            elif game_over:

                if event.key == pygame.K_r:

                    reset_game()


            # ------------------------------------------------
            # 실제 플레이
            # ------------------------------------------------

            else:

                # 기록창 ESC 닫기
                if event.key == pygame.K_ESCAPE:

                    show_record = False


                # 기록창 선택
                if show_record:

                    if event.key == pygame.K_1:

                        choose_patient_action(
                            "treatment"
                        )


                    elif event.key == pygame.K_2:

                        choose_patient_action(
                            "check"
                        )


                    elif event.key == pygame.K_3:

                        choose_patient_action(
                            "quarantine"
                        )


                # E키 상호작용
                elif event.key == pygame.K_e:

                    # 접수 환자 확인
                    if (
                        patient_state
                        == "reception"
                        and near_object(
                            player,
                            patient_rect
                        )
                    ):

                        show_record = True


                    # 물품실
                    elif (
                        patient_state
                        == "waiting_item"
                        and near_object(
                            player,
                            supply_room
                        )
                    ):

                        collect_item()


                    # 환자에게 물품 전달
                    elif (
                        patient_state
                        == "waiting_item"
                        and inventory
                        and near_object(
                            player,
                            patient_rect
                        )
                    ):

                        apply_item_to_patient()


    # ========================================================
    # 화면별 처리
    # ========================================================

    if not game_started:

        draw_start_screen()


    elif game_over:

        draw_game_over()


    else:

        # ----------------------------------------------------
        # 플레이어 이동
        # ----------------------------------------------------

        if not show_record:

            move_player()


        # ----------------------------------------------------
        # 환자 NPC 이동
        # ----------------------------------------------------

        move_patient()


        # ----------------------------------------------------
        # 환자 퇴장 완료 판정
        # ----------------------------------------------------

        if (
            patient_state == "leaving"
            and patient_rect.y > HEIGHT + 10
        ):

            finish_current_patient()


        # ----------------------------------------------------
        # 변칙 환자 처리 후 잠시 다음 환자로
        # ----------------------------------------------------

        if patient_state == "quarantine":

            patient_rect.x += 3

            if patient_rect.x > WIDTH + 30:

                finish_current_patient()


        # ----------------------------------------------------
        # 남은 기회가 0
        # ----------------------------------------------------

        if lives <= 0:

            game_over = True


        # ----------------------------------------------------
        # 화면 그리기
        # ----------------------------------------------------

        draw_map()

        draw_patient()

        draw_player()

        draw_hud()

        draw_help()


        # 인벤토리
        if inventory:

            pygame.draw.rect(
                screen,
                BG,
                (
                    25,
                    90,
                    320,
                    48
                ),
                border_radius=10
            )

            draw_text(
                f"🎒 {inventory}",
                45,
                102,
                WHITE,
                font_small
            )


        draw_patient_record()

        draw_message_box()


    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()
sys.exit()

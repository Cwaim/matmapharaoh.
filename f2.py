import pygame
import sys
import random
import time

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ game
WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Nhiệm vụ 2: Lời nguyền Pharaoh")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SAND = (194, 178, 128)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Font chữ
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 20)

# Biến điều khiển
clock = pygame.time.Clock()
FPS = 60
timer = 30  # Đếm ngược 30 giây
flashlight_uses = 3
character_pos = [50, 50]
path_trail = []
flashlight_active = False
game_state = "play"  # play, success, fail
selected_stone = None

# Hình ảnh
bg_image = pygame.transform.scale(pygame.image.load("bg2.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
character_image = pygame.transform.scale(pygame.image.load("A2.png"), (120, 120))
flashlight_image = pygame.transform.scale(pygame.image.load("flashlight.png"), (80, 80))
stone_image = pygame.transform.scale(pygame.image.load("stone.png"), (100, 100))
large_stone_image = pygame.transform.scale(pygame.image.load("stone.png"), (200, 200))
treasure_chest = pygame.transform.scale(pygame.image.load("treasure.png"), (150, 150))
scroll_piece = pygame.transform.scale(pygame.image.load("path2.png"), (100, 100))

# Đá trong mê cung
stones = [
    {"pos": [300, 300], "size": "large", "direction": "horizontal", "speed": 0.5},  # Giảm từ 2 xuống 1
    {"pos": [800, 400], "size": "large", "direction": "vertical", "speed": 0.25},    # Giảm từ 3 xuống 2
    {"pos": [600, 200], "size": "small", "direction": "horizontal", "speed": 0.5},
    {"pos": [500, 500], "size": "large", "direction": "vertical", "speed": 0.25},
    {"pos": [900, 600], "size": "small", "direction": "horizontal", "speed": 0.5},
    {"pos": [400, 100], "size": "large", "direction": "horizontal", "speed":1},
    {"pos": [700, 300], "size": "small", "direction": "vertical", "speed": 0.25}
]

# Mê cung
maze_layout = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def draw_maze():
    for row_idx, row in enumerate(maze_layout):
        for col_idx, tile in enumerate(row):
            x = col_idx * 100
            y = row_idx * 100
            if tile == 1:
                pygame.draw.rect(screen, SAND, (x, y, 100, 100))
    for trail in path_trail:
        pygame.draw.rect(screen, GRAY, trail)

def draw_stones():
    for stone in stones:
        image = stone_image if stone["size"] == "small" else large_stone_image
        screen.blit(image, stone["pos"])
        update_stones()


def update_stones():
    for stone in stones:
        stone_width = 200 if stone["size"] == "large" else 100
        stone_height = stone_width

        # Cập nhật vị trí đá
        if stone["direction"] == "horizontal":
            stone["pos"][0] += stone["speed"]
            if stone["pos"][0] > WINDOW_WIDTH - stone_width or stone["pos"][0] < 0:
                stone["speed"] = -stone["speed"]  # Đổi hướng di chuyển
        elif stone["direction"] == "vertical":
            stone["pos"][1] += stone["speed"]
            if stone["pos"][1] > WINDOW_HEIGHT - stone_height or stone["pos"][1] < 0:
                stone["speed"] = -stone["speed"]  # Đổi hướng di chuyển


def draw_flashlight_uses():
    flashlight_surface = font.render(f"Đèn pin: {flashlight_uses} lần", True, WHITE)
    screen.blit(flashlight_surface, (WINDOW_WIDTH - 250, 20))
    screen.blit(flashlight_image, (WINDOW_WIDTH - 350, 10))
    
def use_flashlight():
    global flashlight_uses, flashlight_active  # Sử dụng biến toàn cục
    if flashlight_uses > 0:  # Kiểm tra còn lượt sử dụng không
        for stone in stones:
            stone_rect = pygame.Rect(
                stone["pos"],
                (200, 200) if stone["size"] == "large" else (100, 100)
            )
            character_rect = pygame.Rect(character_pos, (120, 120))
            if stone_rect.colliderect(character_rect):  # Kiểm tra nếu nhân vật gần đá
                stone["size"] = "small"  # Thu nhỏ đá
                flashlight_uses -= 1  # Giảm lượt sử dụng
                flashlight_active = True
                return  # Thoát ngay khi thu nhỏ được đá

def check_collision():
    for stone in stones:
        stone_rect = pygame.Rect(stone["pos"], (100, 100))
        character_rect = pygame.Rect(character_pos, (120, 120))
        if stone_rect.colliderect(character_rect):
            return True
    return False

def draw_treasure():
    screen.blit(treasure_chest, (1200, 100))

def check_treasure_interaction():
    treasure_rect = pygame.Rect(1200, 100, 150, 150)
    character_rect = pygame.Rect(character_pos, (120, 120))
    return treasure_rect.colliderect(character_rect)

def show_message(message, color):
    message_surface = font.render(message, True, color)
    screen.blit(message_surface, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2))

def draw_timer():
    timer_surface = font.render(f"Thời gian còn lại: {timer} giây", True, RED)
    screen.blit(timer_surface, (50, 20))

def interact_with_treasure():
    # Vẽ khung thông báo khi tương tác với rương kho báu
    treasure_message_rect = pygame.Rect(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 150, 400, 300)
    pygame.draw.rect(screen, BLACK, treasure_message_rect)
    pygame.draw.rect(screen, WHITE, treasure_message_rect, 3)

    # Nội dung thông báo
    treasure_font = pygame.font.SysFont("Arial", 24)
    treasure_message = [
        "Chúc mừng! Bạn đã tìm thấy kho báu!",
        "Một mảnh bản đồ đã được tiết lộ!"
    ]
    for i, line in enumerate(treasure_message):
        message_surface = treasure_font.render(line, True, WHITE)
        screen.blit(message_surface, (treasure_message_rect.x + 20, treasure_message_rect.y + 40 + i * 50))

    # Vẽ hình ảnh mảnh bùa
    screen.blit(scroll_piece, (treasure_message_rect.x + 150, treasure_message_rect.y + 150))

    # Vẽ nút tiếp theo
    next_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, treasure_message_rect.y + 250, 200, 50)
    pygame.draw.rect(screen, (34, 177, 76), next_button_rect)
    next_button_text = treasure_font.render("TIẾP THEO", True, WHITE)
    screen.blit(next_button_text, (next_button_rect.x + 50, next_button_rect.y + 10))

    return next_button_rect

start_ticks = pygame.time.get_ticks()

running = True
start_ticks = pygame.time.get_ticks()  # Đếm ngược thời gian

while running:
    screen.blit(bg_image, (0, 0))
    draw_maze()
    draw_stones()
    screen.blit(character_image, character_pos)
    draw_flashlight_uses()
    draw_treasure()
    draw_timer()

    # Cập nhật thời gian đếm ngược
    seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
    if seconds_passed >= 1:
        timer -= 1
        start_ticks = pygame.time.get_ticks()

    # Kiểm tra thời gian hết
    if timer <= 0:
        show_message("Bạn thất bại!", RED)
        pygame.display.flip()
        time.sleep(3)
        running = False

    # Xử lý các sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        speed = 20  # Tốc độ di chuyển nhân vật

        # Xử lý di chuyển nhân vật
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                character_pos[1] -= speed  # Di chuyển lên
            elif event.key == pygame.K_DOWN:
                character_pos[1] += speed  # Di chuyển xuống
            elif event.key == pygame.K_LEFT:
                character_pos[0] -= speed  # Di chuyển sang trái
            elif event.key == pygame.K_RIGHT:
                character_pos[0] += speed  # Di chuyển sang phải

            # Xử lý nhấn phím Space để sử dụng đèn pin
            elif event.key == pygame.K_SPACE:
                if flashlight_uses > 0:  # Kiểm tra số lượt đèn pin còn lại
                    flashlight_uses -= 1  # Trừ lượt sử dụng
                    flashlight_active = True

                    # Tìm viên đá gần nhất và thu nhỏ nếu gần
                    for stone in stones:
                        stone_rect = pygame.Rect(
                            stone["pos"],
                            (200, 200) if stone["size"] == "large" else (100, 100)
                        )
                        character_rect = pygame.Rect(character_pos, (120, 120))
                        if stone_rect.colliderect(character_rect):
                            stone["size"] = "small"  # Thu nhỏ đá
                            break

    # Hiệu ứng đèn pin
    if flashlight_active:
        # Thu nhỏ đá gần nhân vật
        for stone in stones:
            stone_rect = pygame.Rect(
                stone["pos"],
                (200, 200) if stone["size"] == "large" else (100, 100)
            )
            character_rect = pygame.Rect(character_pos, (120, 120))
            if stone_rect.colliderect(character_rect):
                stone["size"] = "small"  # Thu nhỏ đá
                break
        flashlight_active = False  # Đặt lại trạng thái

    # Kiểm tra va chạm với đá
    if check_collision():
            show_message("Bạn đã va phải đá!", RED)
            pygame.display.flip()
            time.sleep(3)
            pygame.quit()
            sys.exit()

    # Kiểm tra tương tác với rương
    if check_treasure_interaction():
        next_button_rect = interact_with_treasure()
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if next_button_rect.collidepoint(event.pos):
                        running = False  # Thoát màn chơi
                        break

    pygame.display.flip()
    clock.tick(FPS)

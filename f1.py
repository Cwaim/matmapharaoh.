import pygame
import sys

def run(screen, clock, FPS):
# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ game
WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Xác ướp và mảnh bản đồ")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
GREEN = (34, 177, 76)

# Font chữ
dialogue_font = pygame.font.SysFont("Arial", 26)
hint_font = pygame.font.SysFont("Arial", 22)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Nạp hình ảnh
bg_image = pygame.transform.scale(pygame.image.load("bg1.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))  # Nền Ai Cập
mummy_image = pygame.transform.scale(pygame.image.load("mummy.png"), (200, 300))  # Hình ảnh xác ướp
map_piece_image = pygame.transform.scale(pygame.image.load("path1.png"), (150, 150))  # Mảnh bản đồ
characters = {
    "Mèo Dora": pygame.transform.scale(pygame.image.load("A1.png"), (200, 180)),
    "Shinobi": pygame.transform.scale(pygame.image.load("B1.png"), (200, 180)),
    "Sutake": pygame.transform.scale(pygame.image.load("C1.png"), (200, 180))
}

# Vị trí nhân vật
character_positions = {
    "Mèo Dora": (50, 500),
    "Shinobi": (250, 500),
    "Sutake": (450, 500),
    "Xác ướp": (1100, 350)
}

# Lời thoại
dialogues = [
    "Xác ướp: Ta là người bảo vệ kho báu của Pharaoh!",
    "Mèo Dora: Chúng tôi không muốn lấy kho báu, chỉ cần mảnh bản đồ!",
    "Xác ướp: Nếu các ngươi giải được bí ẩn, đây là phần thưởng của các ngươi.",
    "Shinobi: Cảm ơn! Mảnh bản đồ này sẽ dẫn chúng ta đi tiếp.",
    "Sutake: Đi nào, tiếp tục cuộc hành trình thôi!"
]
dialogue_index = 0

# Biến trạng thái
show_map_piece = False
show_next_button = False

# Nút tiếp theo
next_button_rect = pygame.Rect((WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 200, 150, 50))

# Hàm hiển thị lời thoại
def draw_dialogue():
    global show_characters
    if dialogue_index < len(dialogues):
        dialogue_surface = dialogue_font.render(dialogues[dialogue_index], True, WHITE)
        dialogue_box = pygame.Rect(50, 650, 1200, 80)  # Vị trí khung thoại
        pygame.draw.rect(screen, BLACK, dialogue_box)
        pygame.draw.rect(screen, WHITE, dialogue_box, 2)
        screen.blit(dialogue_surface, (dialogue_box.x + 10, dialogue_box.y + 10))

        # Hiển thị nhân vật theo lời thoại
        current_speaker = dialogues[dialogue_index].split(":")[0]
        if current_speaker in character_positions:
            if current_speaker == "Xác ướp":
                screen.blit(mummy_image, character_positions["Xác ướp"])
            else:
                screen.blit(characters[current_speaker], character_positions[current_speaker])
    else:
        # Khi hết lời thoại, ẩn khung thoại và nhân vật
        show_characters = False

# Hàm hiển thị mảnh bản đồ
def draw_map_piece():
    map_piece_box = pygame.Rect(WINDOW_WIDTH // 2 - 100, 300, 200, 200)
    pygame.draw.rect(screen, WHITE, map_piece_box)
    pygame.draw.rect(screen, BLACK, map_piece_box, 2)
    screen.blit(map_piece_image, (map_piece_box.x + 25, map_piece_box.y + 25))

# Hàm hiển thị nút tiếp theo
def draw_next_button():
    pygame.draw.rect(screen, BLUE, next_button_rect)
    next_text = hint_font.render("TIẾP THEO", True, WHITE)
    screen.blit(next_text, (next_button_rect.x + 30, next_button_rect.y + 10))

# Vòng lặp chính
running = True
while running:
    screen.blit(bg_image, (0, 0))  # Hiển thị nền

    if show_map_piece:
        draw_map_piece()  # Hiển thị mảnh bản đồ
        if show_next_button:
            draw_next_button()  # Hiển thị nút tiếp theo
    else:
        draw_dialogue()  # Hiển thị lời thoại

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if next_button_rect.collidepoint(mouse_pos) and show_next_button:
                print("Chuyển sang nhiệm vụ tiếp theo")
                running = False
        elif event.type == pygame.KEYDOWN:
            if dialogue_index < len(dialogues) - 1:
                dialogue_index += 1
            else:
                show_map_piece = True
                show_next_button = True

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

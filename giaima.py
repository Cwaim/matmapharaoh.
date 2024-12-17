import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ game
WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Giải mã chữ tượng hình")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
GREEN = (34, 177, 76)
HINT_BG = (30, 30, 30)

# Font chữ
font = pygame.font.Font("NotoSansEgyptianHieroglyphs-Regular.ttf", 36)
dialogue_font = pygame.font.SysFont("Arial", 26)
hint_font = pygame.font.SysFont("Arial", 22)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Nạp hình ảnh
bg_image = pygame.transform.scale(pygame.image.load("bg1.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
characters = {
    "Mèo Dora": pygame.transform.scale(pygame.image.load("A1.png"), (150, 150)),
    "Shinobi": pygame.transform.scale(pygame.image.load("B1.png"), (150, 150)),
    "Sutake": pygame.transform.scale(pygame.image.load("C1.png"), (150, 150))
}

# Vị trí nhân vật
character_positions = {"Mèo Dora": (50, 450), "Shinobi": (50, 450), "Sutake": (50, 450)}
show_characters = True

# Gợi ý
hint_button_rect = pygame.Rect((WINDOW_WIDTH - 200, 50, 150, 50))
hint_text = [
    "Vương triều thứ 18, khoảng từ năm 1550 TCN đến năm 1292 TCN.",
    "Đây là thời kỳ thịnh vượng vượt bậc của Ai Cập cổ đại.",
    "Pharaoh nổi tiếng như Thutmose III, Amenhotep III, Akhenaten,",
    "và Tutankhamun đã đưa đất nước đến đỉnh cao quyền lực.",
    "Tên Thutmose III viết như sau: 𓏏𓇋𓅱𓆑𓏥 (Thutmose).",
    "Danh hiệu 'Chúa tể của hai vùng đất' thường kèm ký tự:",
    "𓅓𓆑 để thể hiện quyền lực tối cao của ông.",
    "Hãy sắp xếp các ký hiệu tượng hình để giải mã bí ẩn!"
]
show_hint = False

# Ký hiệu chữ tượng hình
symbols = ["𓋴", "𓂩", "𓏺", "𓂋", "𓏤", "𓄿", "𓏥", "𓈎", "𓏏"]
correct_order = ["𓋴", "𓂩", "𓏺", "𓂋", "𓏤", "𓄿", "𓏥", "𓈎", "𓏏"]
symbol_positions = [(100 + i * 100, 450) for i in range(len(symbols))]
target_positions = [(150 + i * 80, 150) for i in range(len(correct_order))]
placed_symbols = [None] * len(correct_order)

# Nút hoàn thành
finish_button_rect = pygame.Rect((WINDOW_WIDTH - 200, 120, 150, 50))

# Lời thoại
dialogues = [
    "Mèo Dora: Đây là bức tường chữ tượng hình bí ẩn!",
    "Shinobi: Chúng ta cần ghép đúng để mở cánh cửa.",
    "Sutake: Sai sẽ kích hoạt bẫy đấy, cẩn thận!"
]
dialogue_index = 0

# Biến trạng thái
dragging_symbol = None
dragging_index = None
victory = False

# Hàm kiểm tra chiến thắng
def check_victory():
    return placed_symbols == correct_order

# Hàm hiển thị gợi ý
def draw_hint():
    hint_box = pygame.Rect(50, 100, 1100, 250)
    pygame.draw.rect(screen, HINT_BG, hint_box)
    pygame.draw.rect(screen, WHITE, hint_box, 2)
    for i, line in enumerate(hint_text):
        hint_surface = hint_font.render(line, True, WHITE)
        screen.blit(hint_surface, (hint_box.x + 10, hint_box.y + 10 + i * 30))

# Hàm hiển thị lời thoại
def draw_dialogue():
    global show_characters
    if dialogue_index < len(dialogues):
        dialogue_surface = dialogue_font.render(dialogues[dialogue_index], True, WHITE)
        dialogue_box = pygame.Rect(50, 600, 900, 80)
        pygame.draw.rect(screen, BLACK, dialogue_box)
        pygame.draw.rect(screen, WHITE, dialogue_box, 2)
        screen.blit(dialogue_surface, (dialogue_box.x + 10, dialogue_box.y + 10))

        # Hiển thị nhân vật
        current_character = dialogues[dialogue_index].split(":")[0]
        if show_characters and current_character in characters:
            screen.blit(characters[current_character], character_positions[current_character])
    else:
        # Khi hết lời thoại, ẩn nhân vật và khung thoại
        show_characters = False

# Hàm hiển thị ký hiệu
def draw_symbols():
    for i, pos in enumerate(symbol_positions):
        pygame.draw.rect(screen, WHITE, (*pos, 80, 80))
        pygame.draw.rect(screen, BLACK, (*pos, 80, 80), 2)
        symbol_text = font.render(symbols[i], True, BLACK)
        screen.blit(symbol_text, (pos[0] + 10, pos[1] + 10))

# Hàm hiển thị khung điền ký hiệu
def draw_target_positions():
    for i, pos in enumerate(target_positions):
        pygame.draw.rect(screen, WHITE, (*pos, 80, 80))
        pygame.draw.rect(screen, BLACK, (*pos, 80, 80), 2)
        if placed_symbols[i]:
            symbol_text = font.render(placed_symbols[i], True, BLACK)
            screen.blit(symbol_text, (pos[0] + 10, pos[1] + 10))

# Hàm hiển thị màn hình chiến thắng
def draw_victory_screen():
    victory_box = pygame.Rect(WINDOW_WIDTH // 2 - 300, WINDOW_HEIGHT // 2 - 100, 600, 200)
    pygame.draw.rect(screen, WHITE, victory_box)
    pygame.draw.rect(screen, BLACK, victory_box, 3)

    victory_text = dialogue_font.render("Chúc mừng! Bạn đã giải mã thành công!", True, BLACK)
    screen.blit(victory_text, (victory_box.x + 50, victory_box.y + 50))

# Vòng lặp chính
running = True
while running:
    screen.blit(bg_image, (0, 0))  # Hiển thị nền

    if victory:
        draw_victory_screen()
    else:
        draw_symbols()  # Hiển thị ký hiệu
        draw_target_positions()  # Khung điền ký hiệu
        draw_dialogue()  # Lời thoại
        pygame.draw.rect(screen, GREEN, hint_button_rect)
        pygame.draw.rect(screen, BLUE, finish_button_rect)
        screen.blit(hint_font.render("GỢI Ý", True, WHITE), (hint_button_rect.x + 30, hint_button_rect.y + 10))
        screen.blit(hint_font.render("HOÀN THÀNH", True, WHITE), (finish_button_rect.x + 10, finish_button_rect.y + 10))
        if show_hint:
            draw_hint()

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if hint_button_rect.collidepoint(mouse_pos):
                show_hint = not show_hint
            elif finish_button_rect.collidepoint(mouse_pos):
                if check_victory():
                    victory = True
                else:
                    placed_symbols = [None] * len(correct_order)
            for i, pos in enumerate(symbol_positions):
                if pygame.Rect(*pos, 80, 80).collidepoint(mouse_pos):
                    dragging_symbol = symbols[i]
                    dragging_index = i
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_symbol:
                for i, pos in enumerate(target_positions):
                    if pygame.Rect(*pos, 80, 80).collidepoint(event.pos):
                        placed_symbols[i] = dragging_symbol
                        break
            dragging_symbol = None

        elif event.type == pygame.KEYDOWN:
            if dialogue_index < len(dialogues):
                dialogue_index += 1

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

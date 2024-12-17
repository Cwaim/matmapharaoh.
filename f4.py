import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ game
WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Chặng cuối: Ghép bản đồ và nhận Sách Tiên Tri")

# Màu sắc và FPS
WHITE, BLACK, GREEN = (255, 255, 255), (0, 0, 0), (34, 177, 76)
clock = pygame.time.Clock()
FPS = 60

# Tải hình ảnh
bg_image = pygame.transform.scale(pygame.image.load("bg1.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
map_pieces = [
    {"image": pygame.image.load(f"path{i+1}.png"), "pos": [300 + i * 200, 100], "placed": False} for i in range(4)
]
map_full_image = pygame.transform.scale(pygame.image.load("map.png"), (400, 400))
chest_image = pygame.transform.scale(pygame.image.load("treasure.png"), (200, 200))
book_image = pygame.transform.scale(pygame.image.load("sách tiên tri.png"), (100, 100))
character_images = [
    pygame.transform.scale(pygame.image.load("A1.png"), (150, 150)),
    pygame.transform.scale(pygame.image.load("B1.png"), (150, 150)),
    pygame.transform.scale(pygame.image.load("C1.png"), (150, 150))
]

# Khu vực ghép bản đồ
board_rect = pygame.Rect(500, 200, 400, 400)
placed_positions = [(500, 200), (650, 200), (500, 350), (650, 350)]
placed_pieces = []

# Trạng thái game
current_stage = "puzzle"  # puzzle -> chest -> dialogue
selected_piece = None
map_completed = False
chest_and_book_visible = False
show_final_dialogue = False

# Font chữ
font = pygame.font.SysFont("Arial", 30)

# Vẽ hướng dẫn và thông báo
def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Vẽ khu vực ghép bản đồ
def draw_puzzle():
    pygame.draw.rect(screen, BLACK, board_rect)
    pygame.draw.rect(screen, WHITE, board_rect, 3)
    for i, piece in enumerate(map_pieces):
        if not piece["placed"]:
            screen.blit(pygame.transform.scale(piece["image"], (150, 150)), piece["pos"])
    for i, pos in enumerate(placed_positions):
        if i < len(placed_pieces):
            screen.blit(pygame.transform.scale(placed_pieces[i]["image"], (150, 150)), pos)

# Vẽ bản đồ hoàn chỉnh, rương và sách
def draw_chest_and_book():
    screen.blit(map_full_image, (500, 200))
    screen.blit(chest_image, (600, 500))
    screen.blit(book_image, (625, 520))

# Vẽ đối thoại của nhân vật
dialogues = [
    "A1: \"Chúng ta đã ghép xong bản đồ rồi!\"",
    "B1: \"Nhìn xem! Có một rương kho báu trên bản đồ.\"",
    "C1: \"Đúng vậy! Chúng ta đã tìm được Sách Tiên Tri.\"",
    "A1: \"Cuối cùng cũng hoàn thành nhiệm vụ tại Ai Cập.\""
]
def draw_dialogue_box(text):
    pygame.draw.rect(screen, BLACK, (50, 600, 1266, 150))
    pygame.draw.rect(screen, WHITE, (50, 600, 1266, 150), 3)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (70, 630))

# Vòng lặp chính
def game_loop():
    global current_stage, selected_piece, map_completed, chest_and_book_visible, show_final_dialogue
    running = True
    dialogue_index = 0
    
    while running:
        screen.fill(WHITE)
        screen.blit(bg_image, (0, 0))

        # Giai đoạn ghép bản đồ
        if current_stage == "puzzle":
            draw_text("Kéo các mảnh bản đồ vào khu vực ghép.", 50, 50)
            draw_puzzle()
            if map_completed:
                current_stage = "chest"

        # Khi bản đồ hoàn thành
        elif current_stage == "chest":
            if not chest_and_book_visible:
                chest_and_book_visible = True
            draw_chest_and_book()
            draw_text("Chúc mừng! Bạn đã hoàn thành nhiệm vụ!", 500, 650)
            draw_text("Nhấn SPACE để tiếp tục.", 500, 700)

        # Hiển thị đối thoại sau khi nhận sách
        elif current_stage == "dialogue":
            for i, img in enumerate(character_images):
                screen.blit(img, (50 + i * 200, 400))
            draw_dialogue_box(dialogues[dialogue_index])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Xử lý kéo thả bản đồ
            if current_stage == "puzzle":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for piece in map_pieces:
                        if not piece["placed"] and pygame.Rect(*piece["pos"], 150, 150).collidepoint(mouse_pos):
                            selected_piece = piece
                elif event.type == pygame.MOUSEBUTTONUP:
                    if selected_piece:
                        for i, pos in enumerate(placed_positions):
                            if pygame.Rect(*pos, 150, 150).collidepoint(event.pos) and selected_piece not in placed_pieces:
                                placed_pieces.append(selected_piece)
                                selected_piece["placed"] = True
                                break
                        selected_piece = None
                if all(piece["placed"] for piece in map_pieces):
                    map_completed = True

            # Xử lý chuyển sang đối thoại
            if current_stage == "chest" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_stage = "dialogue"

            # Xử lý đối thoại
            if current_stage == "dialogue" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if dialogue_index < len(dialogues) - 1:
                        dialogue_index += 1
                    else:
                        running = False  # Kết thúc game sau lời thoại cuối cùng

        pygame.display.flip()
        clock.tick(FPS)

# Chạy game
game_loop()

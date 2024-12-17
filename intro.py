# Import thư viện
import pygame, sys, os
import time, random, PIL, math

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ game
WINDOW_WIDTH = 1366
WINDOW_HEIGHT = 768

# Tạo cửa sổ game
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Truy tìm lịch sử")

# Khung hình mỗi giây
clock = pygame.time.Clock()
FPS = 60

# Nạp ảnh nền
bg_image1 = pygame.image.load("nhanobi.jpg")  # Ảnh nhà
bg_image2 = pygame.image.load("bg.png")  # Ảnh Ai Cập

# Resize ảnh để vừa với cửa sổ game
bg_image1 = pygame.transform.scale(bg_image1, (WINDOW_WIDTH, WINDOW_HEIGHT))
bg_image2 = pygame.transform.scale(bg_image2, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Nạp ảnh nhân vật
character_images = [
    pygame.image.load("A1.png"),  # Thay bằng đường dẫn đúng
    pygame.image.load("B1.png"),
    pygame.image.load("C1.png")
]

# Resize các nhân vật
character_images = [pygame.transform.scale(img, (300, 300)) for img in character_images]

# Tọa độ các nhân vật (bên trái màn hình)
character_positions = [(50, 500), (200, 500), (350, 500)]

def run(screen, clock):
    
# Tạo font chữ
font = pygame.font.SysFont("Arial", 30)  # Font chung
next_button_font = pygame.font.SysFont("Arial", 18)  # Font cho nút "TIẾP THEO"

# Tạo nút Start
start_button_color = (34, 177, 76)  # Màu xanh lá
start_button_rect = pygame.Rect((WINDOW_WIDTH // 2 - 100, 600, 200, 60))
start_button_text = font.render("START", True, (255, 255, 255))

# Tạo nút TIẾP THEO
next_button_color = (0, 128, 255)  # Màu xanh dương
next_button_rect = pygame.Rect((WINDOW_WIDTH - 200, WINDOW_HEIGHT - 100, 150, 50))
next_button_text = next_button_font.render("TIẾP THEO", True, (255, 255, 255))

# Biến trạng thái màn hình
current_screen = "intro"  # intro -> chặng 1 Ai Cập -> nhiệm vụ 1
selected_character = None

dialogues = [
    ("Mèo Dora", "Đây là Ai Cập cổ đại sao? Thật tuyệt vời!"),
    ("Shinobi", "Đúng vậy! Nhưng chúng ta phải tìm 'Sách Tiên Tri' nhanh thôi!"),
    ("Sutake", "Tôi nghe nói nó được giấu trong một kim tự tháp nào đó.")
]
dialogue_index = 0

# Hàm hiển thị nhiệm vụ nhỏ
def display_task(screen, task_text):
    task_rect = pygame.Rect((50, 50, 500, 100))
    pygame.draw.rect(screen, (0, 0, 0), task_rect)
    pygame.draw.rect(screen, (255, 255, 255), task_rect, 3)
    task_font = pygame.font.SysFont("Arial", 24)
    task_render = task_font.render(task_text, True, (255, 255, 255))
    screen.blit(task_render, (task_rect.x + 10, task_rect.y + 10))

# Vòng lặp chính
while True:
    # Lấy sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Nếu nhấp vào từng nhân vật
            if current_screen == "intro":
                for i, (x, y) in enumerate(character_positions):
                    if x <= mouse_pos[0] <= x + 150 and y <= mouse_pos[1] <= y + 150:
                        selected_character = i  # Lưu chỉ số của nhân vật đã chọn

            # Nếu nhấp vào nút Start
            if current_screen == "intro" and start_button_rect.collidepoint(mouse_pos):
                current_screen = "chapter1"  # Chuyển sang chặng 1 Ai Cập

            # Nếu nhấp vào nút TIẾP THEO
            if current_screen == "chapter1" and next_button_rect.collidepoint(mouse_pos):
                if dialogue_index < len(dialogues) - 1:
                    dialogue_index += 1  # Chuyển sang lời thoại tiếp theo
                else:
                    current_screen = "mission1"  # Chuyển sang màn hình nhiệm vụ 1

    # Xử lý hiển thị theo trạng thái
    if current_screen == "intro":
        # Hiển thị màn hình giới thiệu
        screen.blit(bg_image1, (0, 0))  # Hiển thị nền

        # Hiển thị từng nhân vật
        for i, (x, y) in enumerate(character_positions):
            screen.blit(character_images[i], (x, y))

        # Hiển thị khung giới thiệu nhân vật nếu đã chọn
        if selected_character is not None:
            info_box = pygame.Rect(800, 300, 500, 300)
            pygame.draw.rect(screen, (0, 0, 0), info_box)
            pygame.draw.rect(screen, (255, 255, 255), info_box, 3)
            info_font = pygame.font.SysFont("Arial", 24)

            # Nội dung giới thiệu từng nhân vật
            character_info = [
                [" Mèo Dora", "Vai trò: thủ lĩnh nắm giữ túi bảo bối", "Sở thích: ăn bánh rán", "Ghét: chuột"],
                [" Shinobi", "Vai trò: người ghi nhớ và thuyết phục", "Sở thích: ăn bánh mì", "Sở đoản: hay quên"],
                [" Sutake", "Vai trò: người hỗ trợ", "Sở thích: tìm kiếm vật phẩm", "Sở đoản: sợ ma"]
            ]

            for i, line in enumerate(character_info[selected_character]):
                info_render = info_font.render(line, True, (255, 255, 255))
                screen.blit(info_render, (info_box.x + 10, info_box.y + 10 + i * 50))

        # Vẽ nút Start
        pygame.draw.rect(screen, start_button_color, start_button_rect)
        screen.blit(start_button_text, (start_button_rect.x + 50, start_button_rect.y + 15))

    elif current_screen == "chapter1":
        # Hiển thị màn hình chặng Ai Cập
        screen.blit(bg_image2, (0, 0))  # Nền Ai Cập

        # Hiển thị lời thoại và nhân vật tương ứng
        if dialogue_index < len(dialogues):
            character_name, dialogue = dialogues[dialogue_index]

            # Hiển thị nhân vật
            if character_name == "Mèo Dora":
                screen.blit(character_images[0], (50, 400))
            elif character_name == "Shinobi":
                screen.blit(character_images[1], (50, 400))
            elif character_name == "Sutake":
                screen.blit(character_images[2], (50, 400))

            # Hiển thị khung thoại
            dialogue_box = pygame.Rect(300, 600, 800, 100)
            pygame.draw.rect(screen, (0, 0, 0), dialogue_box)
            pygame.draw.rect(screen, (255, 255, 255), dialogue_box, 3)
            dialogue_font = pygame.font.SysFont("Arial", 24)     
            dialogue_render = dialogue_font.render(f"{character_name}: {dialogue}", True, (255, 255, 255))
            screen.blit(dialogue_render, (dialogue_box.x + 10, dialogue_box.y + 10))

        # Vẽ nút TIẾP THEO
        pygame.draw.rect(screen, next_button_color, next_button_rect)
        screen.blit(next_button_text, (next_button_rect.x + 25, next_button_rect.y + 10))

    elif current_screen == "mission1":
        # Hiển thị màn hình nhiệm vụ 1
        screen.fill((0, 0, 0))
        display_task(screen, "Nhiệm vụ 1: Tìm đường vào kim tự tháp.")
        
     if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False  # Thoát khỏi file này

    # Cập nhật màn hình
    pygame.display.update()
    clock.tick(FPS)
import pygame
import sys
import os
import time

# Khởi tạo Pygame và Mixer
pygame.init()
pygame.mixer.init()  # Khởi tạo âm thanh

# Cấu hình chung
WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Truy tìm lịch sử - Game Hoàn Chỉnh")
clock = pygame.time.Clock()
FPS = 60

# Chèn nhạc nền
def play_background_music():
    music_path = "Nhac-Chuong-Doraemon-Ban-Goc-Khong-Loi.mp3"  # Đường dẫn tới nhạc nền
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)  # Tải nhạc
        pygame.mixer.music.play(-1)  # Phát nhạc lặp lại
        pygame.mixer.music.set_volume(0.5)  # Đặt âm lượng (0.0 - 1.0)
    else:
        print("Không tìm thấy tệp nhạc nền!")

# Tạo hàm chạy file con
def run_file(file_name):
    if os.path.exists(file_name):  # Kiểm tra file tồn tại
        os.system(f"python {file_name}")  # Gọi file Python khác
    else:
        print(f"File không tồn tại: {file_name}")
        error_screen(f"Không tìm thấy {file_name}")  # Hiển thị màn hình lỗi

# Hàm màn hình chờ chuyển tiếp giữa các file
def waiting_screen(text="Nhấn SPACE để tiếp tục"):
    font = pygame.font.SysFont("Arial", 30)
    running = True
    alpha = 0  # Hiệu ứng nhấp nháy
    direction = 1

    while running:
        screen.fill((0, 0, 0))
        # Hiệu ứng chữ nhấp nháy
        alpha += direction * 5
        if alpha >= 255 or alpha <= 50:
            direction *= -1

        # Vẽ chữ
        text_surface = font.render(text, True, (255, 255, 255))
        text_surface.set_alpha(alpha)
        screen.blit(text_surface, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False

# Màn hình lỗi khi file không tìm thấy
def error_screen(message="Lỗi không xác định"):
    font = pygame.font.SysFont("Arial", 40)
    screen.fill((0, 0, 0))
    error_surface = font.render(message, True, (255, 0, 0))
    screen.blit(error_surface, (WINDOW_WIDTH // 2 - 300, WINDOW_HEIGHT // 2))
    pygame.display.flip()
    time.sleep(2)  # Hiển thị lỗi trong 2 giây trước khi thoát game

# Màn hình loading
def loading_screen(message="Đang tải..."):
    font = pygame.font.SysFont("Arial", 35)
    loading_running = True
    dots = ""

    while loading_running:
        screen.fill((0, 0, 0))
        dots += "." if len(dots) < 3 else ""
        loading_surface = font.render(message + dots, True, (255, 255, 255))
        screen.blit(loading_surface, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2))
        pygame.display.flip()
        time.sleep(0.5)  # Giả lập thời gian tải

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        loading_running = False

# Trình tự chạy các file con
def main():
    play_background_music()  # Phát nhạc nền
    
    # Màn hình giới thiệu
    loading_screen("Đang tải màn giới thiệu")
    run_file("C:/Project/assets/images/intro.py")
    waiting_screen("Màn hình giới thiệu xong! Nhấn SPACE để tiếp tục...")

    # Nhiệm vụ mê cung
    loading_screen("Đang tải nhiệm vụ mê cung")
    run_file("C:/Project/assets/images/maze.py")
    waiting_screen("Hoàn thành mê cung! Nhấn SPACE để tiếp tục...")

    # Giải mã chữ tượng hình
    loading_screen("Đang tải giải mã chữ tượng hình")
    run_file("C:/Project/assets/images/giaima.py")
    waiting_screen("Giải mã chữ tượng hình thành công! Nhấn SPACE để tiếp tục...")

    # Nhiệm vụ trung gian F1
    loading_screen("Đang tải nhiệm vụ F1")
    run_file("C:/Project/assets/images/f1.py")
    waiting_screen("Hoàn thành nhiệm vụ F1! Nhấn SPACE để tiếp tục...")

    # Nhiệm vụ F2
    loading_screen("Đang tải nhiệm vụ F2")
    run_file("C:/Project/assets/images/f2.py")
    waiting_screen("Hoàn thành nhiệm vụ F2! Nhấn SPACE để tiếp tục...")

    # Nhiệm vụ F3
    loading_screen("Đang tải nhiệm vụ F3")
    run_file("C:/Project/assets/images/f3.py")
    waiting_screen("Hoàn thành nhiệm vụ F3! Nhấn SPACE để tiếp tục...")

    # Ghép bản đồ và kết thúc
    loading_screen("Đang tải nhiệm vụ cuối cùng")
    run_file("C:/Project/assets/images/f4.py")
    waiting_screen("Chúc mừng! Bạn đã hoàn thành game!")

if __name__ == "__main__":
    main()


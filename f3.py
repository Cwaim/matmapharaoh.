import pygame
import sys
import time

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ game
WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Nhiệm vụ 3: Giao tiếp với Pharaoh trẻ")

# Màu sắc
WHITE, BLACK, GREEN, RED, BLUE = (255, 255, 255), (0, 0, 0), (34, 177, 76), (255, 0, 0), (0, 128, 255)

# Clock và FPS
clock = pygame.time.Clock()
FPS = 60

# Nạp hình ảnh
bg_image = pygame.transform.scale(pygame.image.load("bg3.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
pharaoh_image = pygame.transform.scale(pygame.image.load("pharaoh.png"), (200, 300))
character_a1 = pygame.transform.scale(pygame.image.load("A1.png"), (150, 150))
character_b1 = pygame.transform.scale(pygame.image.load("B1.png"), (150, 150))
machine_image = pygame.transform.scale(pygame.image.load("machine.png"), (80, 80))  # Máy riêng biệt
character_c1 = pygame.transform.scale(pygame.image.load("C1.png"), (150, 150))
map_piece_1 = pygame.transform.scale(pygame.image.load("path3.png"), (150, 150))
map_piece_2 = pygame.transform.scale(pygame.image.load("path4.png"), (150, 150))

# Biến trạng thái
current_phase = 1
question_index = 0
fail = False
task_completed = False
answer_feedback_time = 0
answer_selected = None
answer_correct = False
dialogue_finished = False

# Danh sách câu hỏi và đáp án
questions = [
    {"question": "Ai là vị thần mặt trời của Ai Cập?", "options": ["Horus", "Ra"], "answer": "Ra"},
    {"question": "Kim tự tháp Giza được xây dựng cho pharaoh nào?", "options": ["Khufu", "Ramses"], "answer": "Khufu"},
    {"question": "Pharaoh Tutankhamun lên ngôi vua khi bao nhiêu tuổi?", "options": ["9 tuổi", "19 tuổi"], "answer": "9 tuổi"}
]

# Đoạn hội thoại
dialogues = [
    "Pharaoh: \"Ta là vua của đất nước, ngươi là ai?\"",
    "B1: \"Chúng tôi là nhóm du hành thời gian, không phải kẻ thù!\"",
    "Pharaoh: \"Ngươi có thể chứng minh điều đó không?\"",
    "B1: \"Hãy để chúng tôi trả lời các câu hỏi để chứng minh kiến thức của mình.\""
]

# Hàm hiển thị chữ
def draw_text(text, x, y, font_size=28, color=WHITE):
    font = pygame.font.SysFont("Arial", font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Hiển thị nhân vật và hội thoại
def draw_characters():
    screen.blit(pharaoh_image, (WINDOW_WIDTH - 300, 200))
    screen.blit(character_a1, (100, 550))
    screen.blit(character_b1, (300, 550))
    screen.blit(machine_image, (350, 500))  # Máy gần nhân vật B1
    screen.blit(character_c1, (500, 550))

def draw_dialogue(dialogue):
    pygame.draw.rect(screen, BLACK, (50, 600, 1266, 150))  # Khung thoại
    pygame.draw.rect(screen, WHITE, (50, 600, 1266, 150), 3)
    draw_text(dialogue, 80, 630, font_size=28, color=WHITE)

def draw_question():
    global answer_selected, answer_correct
    question = questions[question_index]
    pygame.draw.rect(screen, WHITE, (100, 100, 1100, 400))
    pygame.draw.rect(screen, BLACK, (100, 100, 1100, 400), 3)
    draw_text(question["question"], 150, 200, font_size=32, color=BLACK)
    
    # Xác định màu câu trả lời
    color_a = GREEN if answer_selected == "A" and answer_correct else RED if answer_selected == "A" else BLACK
    color_b = GREEN if answer_selected == "B" and answer_correct else RED if answer_selected == "B" else BLACK
    
    draw_text("A: " + question["options"][0], 150, 300, font_size=28, color=color_a)
    draw_text("B: " + question["options"][1], 150, 350, font_size=28, color=color_b)
    draw_text("(Nhấn A hoặc B để chọn đáp án)", 100, 450, font_size=20, color=BLACK)

def draw_completion():
    pygame.draw.rect(screen, BLACK, (300, 300, 800, 300))
    pygame.draw.rect(screen, GREEN, (300, 300, 800, 300), 3)
    draw_text("Chúc mừng! Nhiệm vụ hoàn thành!", 400, 350, font_size=36, color=WHITE)
    screen.blit(map_piece_1, (500, 400))
    screen.blit(map_piece_2, (700, 400))
    draw_text("(Bấm SPACE để tiếp tục)", 500, 550, font_size=24, color=WHITE)

# Vòng lặp game
def game_loop():
    global question_index, fail, task_completed, answer_feedback_time, answer_selected, answer_correct, dialogue_finished
    running = True
    dialogue_index = 0

    while running:
        screen.blit(bg_image, (0, 0))
        draw_characters()

        if not dialogue_finished:
            draw_dialogue(dialogues[dialogue_index])
        elif task_completed:
            draw_completion()
        elif fail:
            draw_text("Pharaoh: \"Ngươi là kẻ lừa đảo! Bắt giữ chúng!\"", 100, 100, RED)
        else:
            draw_question()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not dialogue_finished and event.key == pygame.K_SPACE:
                    dialogue_index += 1
                    if dialogue_index >= len(dialogues):
                        dialogue_finished = True
                elif dialogue_finished and not answer_selected:
                    if event.key == pygame.K_a or event.key == pygame.K_b:
                        answer_selected = "A" if event.key == pygame.K_a else "B"
                        selected_option = questions[question_index]["options"][0 if answer_selected == "A" else 1]
                        if selected_option == questions[question_index]["answer"]:
                            answer_correct = True
                            question_index += 1
                            if question_index >= len(questions):
                                task_completed = True
                        else:
                            answer_correct = False
                            fail = True
                        answer_feedback_time = time.time()
                if task_completed and event.key == pygame.K_SPACE:
                    running = False
            
        # Hiển thị màu đúng/sai trong 3s
        if answer_selected and time.time() - answer_feedback_time > 3:
            answer_selected = None

        pygame.display.flip()
        clock.tick(FPS)

# Chạy game
game_loop()

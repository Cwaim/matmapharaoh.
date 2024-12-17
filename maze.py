import pygame
import random

# Kích thước cửa sổ game
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 680  # Thêm không gian cho khu vực thông tin bên dưới
CELL_SIZE = 40

# Số hàng và cột của mê cung
COLS = WINDOW_WIDTH // CELL_SIZE
ROWS = (WINDOW_HEIGHT - 80) // CELL_SIZE  # Giảm chiều cao mê cung để chừa không gian hiển thị

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Tạo cửa sổ game
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Maze with Binoculars")
clock = pygame.time.Clock()
FPS = 60

# Nạp ảnh xác ướp, người chơi và ống nhòm
mummy_image = pygame.image.load("mummy.png")
mummy_image = pygame.transform.scale(mummy_image, (CELL_SIZE, CELL_SIZE))
player_image = pygame.image.load("A1.png")
player_image = pygame.transform.scale(player_image, (CELL_SIZE, CELL_SIZE))
binocular_image = pygame.image.load("binocular.png")
binocular_image = pygame.transform.scale(binocular_image, (50, 50))

# Vị trí ống nhòm trên giao diện
binocular_position = (WINDOW_WIDTH - 70, WINDOW_HEIGHT - 70)
binocular_uses = 5
binocular_active = False
binocular_timer = 0
binocular_duration = 10000  # Thời gian sử dụng tối đa: 10 giây

# Vị trí nút điều khiển
arrow_size = 50
arrow_up = pygame.image.load("up.png")
arrow_down = pygame.image.load("down.png")
arrow_left = pygame.image.load("left.png")
arrow_right = pygame.image.load("right.png")

arrow_up = pygame.transform.scale(arrow_up, (arrow_size, arrow_size))
arrow_down = pygame.transform.scale(arrow_down, (arrow_size, arrow_size))
arrow_left = pygame.transform.scale(arrow_left, (arrow_size, arrow_size))
arrow_right = pygame.transform.scale(arrow_right, (arrow_size, arrow_size))

arrow_positions = {
    "up": (350, 600),
    "down": (350, 640),
    "left": (300, 640),
    "right": (400, 640)
}

# Lớp Cell đại diện cho từng ô trong mê cung
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

    def draw(self, screen):
        x = self.x * CELL_SIZE
        y = self.y * CELL_SIZE
        if self.visited:
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

        if self.walls["top"]:
            pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls["right"]:
            pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls["bottom"]:
            pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls["left"]:
            pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE), 2)

# Hàm kiểm tra ô lân cận
def get_neighbors(cell, grid):
    neighbors = []
    directions = [
        (0, -1, "top", "bottom"),  # Lên
        (1, 0, "right", "left"),  # Phải
        (0, 1, "bottom", "top"),  # Xuống
        (-1, 0, "left", "right"),  # Trái
    ]

    for dx, dy, current_wall, neighbor_wall in directions:
        nx, ny = cell.x + dx, cell.y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS:
            neighbor = grid[ny][nx]
            if not neighbor.visited:
                neighbors.append((neighbor, current_wall, neighbor_wall))

    return neighbors

# Hàm tạo mê cung
def generate_maze():
    grid = [[Cell(x, y) for x in range(COLS)] for y in range(ROWS)]
    stack = []
    current = grid[0][0]
    current.visited = True

    while True:
        neighbors = get_neighbors(current, grid)
        if neighbors:
            next_cell, current_wall, neighbor_wall = random.choice(neighbors)
            current.walls[current_wall] = False
            next_cell.walls[neighbor_wall] = False
            stack.append(current)
            current = next_cell
            current.visited = True
        elif stack:
            current = stack.pop()
        else:
            break

    return grid

# Lớp Mummy đại diện cho xác ướp
class Mummy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, grid):
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Lên, phải, xuống, trái
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and not grid[self.y][self.x].walls["top" if dy == -1 else "bottom" if dy == 1 else "left" if dx == -1 else "right"]:
                self.x = nx
                self.y = ny
                break

    def draw(self, screen):
        screen.blit(mummy_image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

# Hàm kiểm tra xác ướp gần
def check_mummy_ahead(player_pos, mummy_pos):
    px, py = player_pos
    mx, my = mummy_pos
    return abs(px - mx) <= 1 and abs(py - my) <= 1

# Tạo mê cung
grid = generate_maze()
mummy = Mummy(COLS // 2, ROWS // 2)

# Người chơi
player_pos = [0, 0]

# Vòng lặp chính
running = True
mummy_move_timer = 0
mummy_move_delay = 800
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Kiểm tra nhấp vào nút điều khiển
            for direction, pos in arrow_positions.items():
                if pos[0] <= mouse_pos[0] <= pos[0] + arrow_size and pos[1] <= mouse_pos[1] <= pos[1] + arrow_size:
                    if direction == "up" and not grid[player_pos[1]][player_pos[0]].walls["top"]:
                        player_pos[1] -= 1
                    elif direction == "down" and not grid[player_pos[1]][player_pos[0]].walls["bottom"]:
                        player_pos[1] += 1
                    elif direction == "left" and not grid[player_pos[1]][player_pos[0]].walls["left"]:
                        player_pos[0] -= 1
                    elif direction == "right" and not grid[player_pos[1]][player_pos[0]].walls["right"]:
                        player_pos[0] += 1

            # Kiểm tra nhấp vào ống nhòm
            if binocular_position[0] <= mouse_pos[0] <= binocular_position[0] + 50 and \
               binocular_position[1] <= mouse_pos[1] <= binocular_position[1] + 50:
                if binocular_uses > 0:
                    binocular_active = True
                    binocular_timer = pygame.time.get_ticks()
                    binocular_uses -= 1

    # Cập nhật trạng thái ống nhòm
    if binocular_active:
        current_time = pygame.time.get_ticks()
        if current_time - binocular_timer > binocular_duration:
            binocular_active = False

    # Di chuyển xác ướp
    current_time = pygame.time.get_ticks()
    if current_time - mummy_move_timer > mummy_move_delay:
        mummy.move(grid)
        mummy_move_timer = current_time

    # Vẽ màn hình
    screen.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(screen)
    screen.blit(player_image, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE))
    mummy.draw(screen)

    # Vẽ ống nhòm
    screen.blit(binocular_image, binocular_position)
    uses_text = pygame.font.SysFont("Arial", 20).render(f"Uses: {binocular_uses}", True, BLACK)
    screen.blit(uses_text, (binocular_position[0] - 50, binocular_position[1] - 20))

    # Hiển thị cảnh báo nếu ống nhòm hoạt động
    if binocular_active and check_mummy_ahead(player_pos, [mummy.x, mummy.y]):
        warning_text = pygame.font.SysFont("Arial", 24).render("Cảnh báo: Xác ướp gần!", True, RED)
        screen.blit(warning_text, (WINDOW_WIDTH // 2 - 150, 10))

    # Hiển thị nút điều khiển
    screen.blit(arrow_up, arrow_positions["up"])
    screen.blit(arrow_down, arrow_positions["down"])
    screen.blit(arrow_left, arrow_positions["left"])
    screen.blit(arrow_right, arrow_positions["right"])

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

import pygame
import random
import sys

# ---------- 初始化 ----------
pygame.init()

# ---------- 游戏参数 ----------
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10  # 速度

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
DARK_GREEN = (30, 150, 30)
GRAY = (40, 40, 40)

# ---------- 创建窗口 ----------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 贪吃蛇 - Python版")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# ---------- 游戏变量 ----------
def reset_game():
    """重置游戏状态"""
    global snake, direction, food, score, game_over
    # 蛇：初始在中间，长度为3
    snake = [
        [GRID_WIDTH // 2, GRID_HEIGHT // 2],
        [GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2],
        [GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2]
    ]
    direction = [1, 0]  # 初始向右
    score = 0
    game_over = False
    spawn_food()

def spawn_food():
    """生成食物，确保不在蛇身上"""
    global food
    while True:
        food = [
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        ]
        if food not in snake:
            break

# ---------- 绘制函数 ----------
def draw_grid():
    """绘制网格线（可选）"""
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def draw_snake():
    """绘制蛇"""
    for i, segment in enumerate(snake):
        x, y = segment[0] * GRID_SIZE, segment[1] * GRID_SIZE
        color = GREEN if i == 0 else DARK_GREEN  # 蛇头亮色
        pygame.draw.rect(screen, color, (x + 1, y + 1, GRID_SIZE - 2, GRID_SIZE - 2))
        
        # 蛇头加眼睛
        if i == 0:
            eye_size = 3
            if direction[0] == 1:  # 向右
                pygame.draw.circle(screen, WHITE, (x + GRID_SIZE - 6, y + 6), eye_size)
                pygame.draw.circle(screen, WHITE, (x + GRID_SIZE - 6, y + GRID_SIZE - 6), eye_size)
            elif direction[0] == -1:  # 向左
                pygame.draw.circle(screen, WHITE, (x + 6, y + 6), eye_size)
                pygame.draw.circle(screen, WHITE, (x + 6, y + GRID_SIZE - 6), eye_size)
            elif direction[1] == -1:  # 向上
                pygame.draw.circle(screen, WHITE, (x + 6, y + 6), eye_size)
                pygame.draw.circle(screen, WHITE, (x + GRID_SIZE - 6, y + 6), eye_size)
            elif direction[1] == 1:  # 向下
                pygame.draw.circle(screen, WHITE, (x + 6, y + GRID_SIZE - 6), eye_size)
                pygame.draw.circle(screen, WHITE, (x + GRID_SIZE - 6, y + GRID_SIZE - 6), eye_size)

def draw_food():
    """绘制食物（苹果样式）"""
    x, y = food[0] * GRID_SIZE + GRID_SIZE // 2, food[1] * GRID_SIZE + GRID_SIZE // 2
    pygame.draw.circle(screen, RED, (x, y), GRID_SIZE // 2 - 2)
    # 高光
    pygame.draw.circle(screen, (255, 150, 150), (x - 3, y - 3), 3)

def draw_score():
    """显示分数"""
    text = font.render(f"分数: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def draw_game_over():
    """游戏结束遮罩"""
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    text1 = font.render("💀 游戏结束", True, WHITE)
    text2 = font.render(f"最终得分: {score}", True, WHITE)
    text3 = font.render("按 R 重新开始", True, (200, 200, 200))
    
    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 - 10))
    screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 2 + 40))

# ---------- 主循环 ----------
reset_game()

while True:
    # ----- 事件处理 -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
                continue
            
            # 方向控制（禁止掉头）
            if event.key == pygame.K_UP and direction[1] != 1:
                direction = [0, -1]
            elif event.key == pygame.K_DOWN and direction[1] != -1:
                direction = [0, 1]
            elif event.key == pygame.K_LEFT and direction[0] != 1:
                direction = [-1, 0]
            elif event.key == pygame.K_RIGHT and direction[0] != -1:
                direction = [1, 0]

    # ----- 游戏逻辑（如果没结束）-----
    if not game_over:
        # 计算新蛇头
        head = snake[0]
        new_head = [head[0] + direction[0], head[1] + direction[1]]
        
        # 检测是否吃到食物
        is_eating = (new_head == food)
        
        # 构建新蛇
        new_snake = [new_head] + snake
        
        if not is_eating:
            new_snake.pop()  # 没吃到移除尾巴
        
        # ----- 碰撞检测 -----
        # 撞墙
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            game_over = True
        
        # 撞自己（检查新蛇头是否和身体重叠，位置0是头，从1开始检查）
        if not game_over:
            for i in range(1, len(new_snake)):
                if new_snake[i] == new_head:
                    game_over = True
                    break
        
        # 更新游戏状态
        if not game_over:
            snake = new_snake
            if is_eating:
                score += 1
                spawn_food()
                # 每吃5个加速一次
                if score % 5 == 0:
                    FPS = min(FPS + 2, 25)  # 最快到25帧

    # ----- 绘制 -----
    screen.fill(BLACK)
    draw_grid()
    draw_food()
    draw_snake()
    draw_score()
    
    if game_over:
        draw_game_over()
    
    pygame.display.flip()
    clock.tick(FPS)
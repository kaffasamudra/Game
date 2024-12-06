import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Membuat window dengan ukuran tertentu
pygame.display.set_caption("Brick Breaker Game")  # Judul game

# Warna dalam RGB
WHITE = (255, 255, 255)  # Warna putih
BLUE = (0, 0, 255)       # Warna biru
RED = (255, 0, 0)        # Warna merah
BLACK = (0, 0, 0)        # Warna hitam
YELLOW = (255, 255, 0)   # Warna kuning

# Ukuran paddle dan kecepatannya
PADDLE_WIDTH = 100           # Lebar paddle normal
PADDLE_HEIGHT = 10           # Tinggi paddle
PADDLE_WIDTH_LARGE = 150     # Lebar paddle saat diperbesar
paddle_speed = 8             # Kecepatan paddle
PADDLE_LARGE_DURATION = 5000  # Durasi paddle besar dalam milidetik (5 detik)

# Ukuran dan kecepatan bola
BALL_SIZE = 5
ball_speed = 4

# Ukuran dan jumlah brick
BRICK_WIDTH = 10
BRICK_HEIGHT = 5
BRICK_ROWS = 20         # Jumlah baris brick
BRICK_COLUMNS = 27     # Jumlah kolom brick

# Font untuk teks pada layar
font = pygame.font.Font(None, 36)

# Fungsi untuk mengatur ulang game
def reset_game():
    """
    Fungsi untuk mengatur ulang game ke kondisi awal.
    """
    global paddle_x, paddle_y, balls, bricks, items, game_over, game_won, paddle_large, paddle_large_timer
    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
    balls = [{'x': SCREEN_WIDTH // 2, 'y': SCREEN_HEIGHT // 2, 'speed_x': ball_speed * random.choice((1, -1)), 'speed_y': -ball_speed}]
    bricks = []
    for row in range(BRICK_ROWS):
        brick_row = []
        for col in range(BRICK_COLUMNS):
            brick_x = col * (BRICK_WIDTH + 10) + 35
            brick_y = row * (BRICK_HEIGHT + 5) + 30
            brick = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
            brick_row.append(brick)
        bricks.append(brick_row)
    items = []
    game_over = False
    game_won = False
    paddle_large = False
    paddle_large_timer = 0  # Reset timer saat game direset

# Menjalankan fungsi reset untuk memulai game pertama kali
reset_game()

# Loop utama game
running = True
clock = pygame.time.Clock()

while running:
    # Hitung waktu per frame (delta_time) dalam milidetik
    delta_time = clock.tick(60)  # Membatasi kecepatan frame rate ke 60 FPS
    screen.fill(BLACK)  # Bersihkan layar dengan warna hitam

    # Event handling untuk keluar dari game atau mereset
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (game_over or game_won):
                reset_game()  # Reset game jika "Game Over" atau "You Win" dan tekan "R"

    if not game_over and not game_won:
        # Periksa apakah paddle besar masih aktif
        if paddle_large:
            paddle_large_timer -= delta_time  # Kurangi timer paddle besar
            if paddle_large_timer <= 0:  # Jika timer habis
                paddle_large = False  # Kembalikan paddle ke ukuran normal
                paddle_large_timer = 0  # Reset timer

        # Gerakan paddle menggunakan tombol panah
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - (PADDLE_WIDTH_LARGE if paddle_large else PADDLE_WIDTH):
            paddle_x += paddle_speed

        # Gerakan bola dan deteksi tabrakan
        for ball in balls:
            ball['x'] += ball['speed_x']
            ball['y'] += ball['speed_y']
            # Tabrakan dengan dinding
            if ball['x'] <= 0 or ball['x'] >= SCREEN_WIDTH - BALL_SIZE:
                ball['speed_x'] = -ball['speed_x']
            if ball['y'] <= 0:
                ball['speed_y'] = -ball['speed_y']
            if ball['y'] >= SCREEN_HEIGHT:
                balls.remove(ball)  # Hapus bola jika jatuh ke bawah
                if not balls:
                    game_over = True  # Game over jika semua bola jatuh

        # Menang jika semua brick habis
        if not any(bricks):
            game_won = True

        # Tabrakan dengan paddle
        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH_LARGE if paddle_large else PADDLE_WIDTH, PADDLE_HEIGHT)
        for ball in balls:
            ball_rect = pygame.Rect(ball['x'], ball['y'], BALL_SIZE, BALL_SIZE)
            if ball_rect.colliderect(paddle_rect):
                ball['speed_y'] = -ball['speed_y']

        # Tabrakan dengan brick dan mengeluarkan item
        for row in bricks:
            for brick in row:
                ball_hit = False
                for ball in balls:
                    ball_rect = pygame.Rect(ball['x'], ball['y'], BALL_SIZE, BALL_SIZE)
                    if ball_rect.colliderect(brick):
                        ball['speed_y'] = -ball['speed_y']
                        row.remove(brick)
                        ball_hit = True
                        if random.random() < 0.2:  # 20% peluang keluarkan item
                            item_type = random.choice(["paddle_large", "ball_clone"])
                            item = {'type': item_type, 'x': brick.x + BRICK_WIDTH // 2, 'y': brick.y + BRICK_HEIGHT // 2}
                            items.append(item)
                        break
                if ball_hit:
                    break

        # Gerakan dan efek item
        for item in items[:]:
            item['y'] += 3  # Kecepatan jatuh item
            item_rect = pygame.Rect(item['x'], item['y'], 20, 20)
            if item_rect.colliderect(paddle_rect):
                if item['type'] == "paddle_large":
                    paddle_large = True
                    paddle_large_timer = PADDLE_LARGE_DURATION  # Set timer paddle besar
                elif item['type'] == "ball_clone":
                    if len(balls) == 1:  # Tambah bola jadi 5
                        for _ in range(4):
                            balls.append({'x': balls[0]['x'], 'y': balls[0]['y'], 'speed_x': ball_speed * random.choice((1, -1)), 'speed_y': -ball_speed})
                items.remove(item)
            elif item['y'] > SCREEN_HEIGHT:
                items.remove(item)

        # Gambar paddle, bola, brick, dan item di layar
        pygame.draw.rect(screen, BLUE, paddle_rect)
        for ball in balls:
            pygame.draw.ellipse(screen, WHITE, (ball['x'], ball['y'], BALL_SIZE, BALL_SIZE))
        for row in bricks:
            for brick in row:
                pygame.draw.rect(screen, RED, brick)
        for item in items:
            pygame.draw.circle(screen, YELLOW, (item['x'], item['y']), 10)

    else:
        # Tampilkan pesan "Game Over" atau "You Win!" dan instruksi ulang
        message = "You Win! Press 'R' to Restart" if game_won else "Game Over! Press 'R' to Restart"
        text = font.render(message, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))

    # Perbarui layar
    pygame.display.flip()

pygame.quit()  # Keluar dari Pygame setelah loop berakhir

import pygame
import random
import sys

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
screen_width = 600
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("car racing_god mode")

# Warna
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Mengatur FPS
clock = pygame.time.Clock()
FPS = 60

# Ukuran mobil
car_width = 25
car_height = 50

# Jumlah rintangan
num_obstacles = 10
obstacle_width = 50
obstacle_height = 50

# Memuat gambar jalan dan menskalanya agar sesuai dengan ukuran layar
road_image = pygame.image.load("road.png")
road_image = pygame.transform.scale(road_image, (screen_width, screen_height))

# Koordinat awal untuk dua gambar jalan yang akan digulirkan
road_y1 = 0
road_y2 = -screen_height

# Fungsi untuk menggambar mobil
def draw_car(x, y, invincible):
    color = GREEN if invincible else RED  # Ubah warna mobil saat invincibility aktif
    pygame.draw.rect(screen, color, [x, y, car_width, car_height])

# Fungsi untuk menggambar rintangan
def draw_obstacle(obstacle_x, obstacle_y):
    pygame.draw.rect(screen, CYAN, [obstacle_x, obstacle_y, obstacle_width, obstacle_height])

# Fungsi untuk menggambar item spesial
def draw_special_item(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), 15)

# Game loop utama
def game_loop():
    global road_y1, road_y2
    # Koordinat awal mobil pemain
    car_x = (screen_width * 0.45)
    car_y = (screen_height * 0.8)
    car_x_change = 0
    car_y_change = 0

    # Pengaturan awal rintangan
    obstacles = []
    for _ in range(num_obstacles):
        x = random.randrange(0, screen_width - obstacle_width)
        y = random.randrange(-1500, -100)  # Atur rintangan secara acak di luar layar awalnya
        obstacles.append([x, y])

    obstacle_speed = 8

    # Pengaturan item spesial
    special_item_x = random.randint(0, screen_width)
    special_item_y = random.randint(-1000, -100)
    special_item_active = False
    invincibility_timer = 0
    special_item_spawn_timer = 300  # Jeda kemunculan item spesial (5 detik)

    # Skor awal
    score = 0
    font = pygame.font.SysFont(None, 40)

    # Fungsi untuk menampilkan skor
    def show_score(score):
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

    running = True
    game_over = False

    while running:
        # Menutup game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Kontrol mobil dengan panah kiri, kanan, atas, dan bawah
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car_x_change = -8
                elif event.key == pygame.K_RIGHT:
                    car_x_change = 8
                elif event.key == pygame.K_UP:
                    car_y_change = -8
                elif event.key == pygame.K_DOWN:
                    car_y_change = 8
                elif game_over and event.key == pygame.K_RETURN:
                    # Restart game jika "Enter" ditekan setelah game over
                    game_loop()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    car_x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    car_y_change = 0

        # Update posisi mobil
        if not game_over:
            car_x += car_x_change
            car_y += car_y_change

            # Menggerakkan gambar jalan
            road_y1 += obstacle_speed
            road_y2 += obstacle_speed

            # Mengulangi gambar jalan jika sudah melewati layar
            if road_y1 >= screen_height:
                road_y1 = -screen_height
            if road_y2 >= screen_height:
                road_y2 = -screen_height

            # Menggambar latar belakang jalan
            screen.blit(road_image, (0, road_y1))
            screen.blit(road_image, (0, road_y2))

            # Menggambar rintangan dan memperbarui posisinya
            for obstacle in obstacles:
                draw_obstacle(obstacle[0], obstacle[1])
                obstacle[1] += obstacle_speed

                # Jika rintangan melewati layar, respawn di atas
                if obstacle[1] > screen_height:
                    obstacle[1] = random.randrange(-1500, -100)
                    obstacle[0] = random.randrange(0, screen_width - obstacle_width)
                    score += 1  # Tambah skor saat melewati rintangan
                    obstacle_speed += 0.05  # Perlahan tingkatkan kecepatan rintangan

                # Deteksi tabrakan jika invincibility tidak aktif
                if not special_item_active:
                    if car_y < obstacle[1] + obstacle_height and car_y + car_height > obstacle[1]:
                        if car_x > obstacle[0] and car_x < obstacle[0] + obstacle_width or \
                           car_x + car_width > obstacle[0] and car_x + car_width < obstacle[0] + obstacle_width:
                            game_over = True

            # Mengatur kemunculan item spesial
            if special_item_spawn_timer <= 0:
                draw_special_item(special_item_x, special_item_y)
                special_item_y += obstacle_speed

                # Deteksi jika mobil mengambil item spesial
                if car_y < special_item_y + 15 and car_y + car_height > special_item_y - 15:
                    if car_x > special_item_x - 15 and car_x < special_item_x + 15 or \
                       car_x + car_width > special_item_x - 15 and car_x + car_width < special_item_x + 15:
                        special_item_active = True
                        invincibility_timer = 180  # Durasi invincibility selama 3 detik
                        special_item_spawn_timer = 300  # Set ulang timer spawn
                        special_item_x = random.randint(0, screen_width)
                        special_item_y = random.randint(-1000, -100)
            else:
                special_item_spawn_timer -= 1

            # Update invincibility timer
            if special_item_active:
                invincibility_timer -= 1
                if invincibility_timer <= 0:
                    special_item_active = False

            # Menggambar indikator invincibility
            if special_item_active:
                invincibility_text = font.render("Invincibility Active!", True, GREEN)
                screen.blit(invincibility_text, (screen_width - 200, 10))

            # Menggambar mobil pemain
            draw_car(car_x, car_y, special_item_active)
            show_score(score)

            # Jika mobil keluar layar, game over
            if car_x > screen_width - car_width or car_x < 0 or car_y > screen_height - car_height or car_y < 0:
                game_over = True

        else:
            # Tampilkan Game Over dan instruksi restart
            game_over_font = pygame.font.SysFont(None, 75)
            game_over_text = game_over_font.render("Game Over", True, RED)
            restart_text = font.render("Press Enter to Restart", True, WHITE)
            screen.blit(game_over_text, (screen_width / 2 - 150, screen_height / 2 - 50))
            screen.blit(restart_text, (screen_width / 2 - 150, screen_height / 2 + 50))

        pygame.display.flip()
        clock.tick(FPS)

game_loop()
pygame.quit()
sys.exit()

import pygame
import sys

# Ekran boyutları
WIDTH, HEIGHT = 800, 600
# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Pencere başlığı
TITLE = "Bezier Eğrisi"

# İki nokta arasındaki kontrol noktaları belirlemek için işlev
def interpolate(p0, p1, t):
    return p0 + (p1 - p0) * t

# Bezier eğrisi için nokta hesaplama işlevi
def bezier(p0, p1, p2, p3, t):
    return interpolate(interpolate(interpolate(p0, p1, t), interpolate(p1, p2, t), t), interpolate(interpolate(p1, p2, t), interpolate(p2, p3, t), t), t)

# Pygame başlatma
pygame.init()
# Ekran oluşturma
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Başlangıç ve bitiş noktaları
p0 = (100, 300)
p3 = (700, 300)
# Kontrol noktaları
p1 = (400, 400)
p2 = (400, 400)

# Ana döngü
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Arka planı temizleme
    screen.fill(WHITE)

    # Bezier eğrisini çizme
    for i in range(101):
        t = i / 100
        x, y = bezier(p0[0], p1[0], p2[0], p3[0], t), bezier(p0[1], p1[1], p2[1], p3[1], t)
        pygame.draw.circle(screen, BLACK, (int(x), int(y)), 2)

    # Kontrol noktalarını çizme
    pygame.draw.circle(screen, BLACK, p0, 5)
    pygame.draw.circle(screen, BLACK, p1, 5)
    pygame.draw.circle(screen, BLACK, p2, 5)
    pygame.draw.circle(screen, BLACK, p3, 5)

    # Kontrol noktalarını birleştirme
    #pygame.draw.lines(screen, BLACK, False, [p0, p1, p2, p3], 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

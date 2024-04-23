import pygame
import sys
import math
from pygame.locals import *

# Pencere boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Araba boyutları
CAR_WIDTH = 50
CAR_HEIGHT = 100

# Renkler
BLACK = (0, 0, 0)

# Araba resmi yükleme
car_image = pygame.image.load("car.png")

# Araba sınıfı
class Car:
    def __init__(self):
        self.x = (SCREEN_WIDTH - CAR_WIDTH) // 2
        self.y = SCREEN_HEIGHT - CAR_HEIGHT - 50
        self.angle = 0
        self.speed = 0
        self.max_speed = 5

    def draw(self, screen):
        rotated_car = pygame.transform.rotate(car_image, self.angle)
        screen.blit(rotated_car, (self.x, self.y))

    def move(self, keys):
        if keys[K_LEFT]:
            self.angle += 5
        if keys[K_RIGHT]:
            self.angle -= 5
        if keys[K_UP]:
            self.speed = min(self.speed + 0.1, self.max_speed)
        if keys[K_DOWN]:
            self.speed = max(self.speed - 0.1, -self.max_speed)

        # Arabayı ileri veya geri hareket ettirme
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))

# Ana oyun döngüsü
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Araba Simülasyonu")

    clock = pygame.time.Clock()
    car = Car()

    while True:
        screen.fill(BLACK)
        
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        car.move(keys)
        car.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()


import pygame
import sys
import math

# Ekran boyutları
WIDTH, HEIGHT = 1500, 900

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (25, 12, 63)

class CirclePath:
    def __init__(self, screen, outer_circle_center, outer_circle_radius, inner_circle_center, inner_circle_radius):
        self.screen = screen
        self.outer_circle_center = outer_circle_center
        self.outer_circle_radius = outer_circle_radiusç
        self.inner_circle_center = inner_circle_center
        self.inner_circle_radius = inner_circle_radius

    def draw(self):
        raise NotImplementedError("Subclasses must implement draw method")

class BottomRightPath(CirclePath):
    def draw(self, z):
        draw_circle_quarter(self.screen, z, self.outer_circle_radius, z, self.inner_circle_radius, 'bottom_right')
        
class BottomLeftPath(CirclePath):
    def draw(self):
        draw_circle_quarter(self.screen, self.outer_circle_center, self.outer_circle_radius, self.inner_circle_center, self.inner_circle_radius, 'bottom_left')
        
class TopRightPath(CirclePath):
    def draw(self, y):
        draw_circle_quarter(self.screen, y, self.outer_circle_radius, y, self.inner_circle_radius, 'top_right')
        
class TopLeftPath(CirclePath):
    def draw(self, x):
        draw_circle_quarter(self.screen, x, self.outer_circle_radius, x, self.inner_circle_radius, 'top_left')

class StraightPath:
    def __init__(self, screen):
        self.screen = screen

    def draw(self, top_left_corner):
        rectangle_size = (50, 150)
        draw_rectangle(self.screen, WHITE, top_left_corner, rectangle_size)

class StraighttwoPath:
    def __init__(self, screen):
        self.screen = screen

    def draw(self, top_left_corner):
        rectangle_size = (300, 50)
        draw_rectangle(self.screen, WHITE, top_left_corner, rectangle_size)


def draw_circle_quarter(screen, center, outer_radius, inner_center, inner_radius, quarter):
    # Hangi çeyrek çizilecekse ona göre açıları belirle
    angles = {
        'top_left': (math.pi, 1.5 * math.pi),
        'top_right': (1.5 * math.pi, 2 * math.pi),
        'bottom_left': (0.5 * math.pi, math.pi),
        'bottom_right': (0, 0.5 * math.pi)
    }
    
    angle_start, angle_end = angles[quarter]

    # İç çember
    pygame.draw.arc(screen, WHITE, (inner_center[0] - inner_radius, inner_center[1] - inner_radius, inner_radius * 2, inner_radius * 2), angle_start, angle_end, 2)
    
    # Dış çember
    pygame.draw.arc(screen, WHITE, (center[0] - outer_radius, center[1] - outer_radius, outer_radius * 2, outer_radius * 2), angle_start, angle_end, 2)

    # Çeyreğin son noktasını hesapla
    x_end = inner_center[0] + inner_radius * math.cos(angle_end)
    y_end = inner_center[1] + inner_radius * math.sin(angle_end)
    bottom_right_end = (x_end, y_end)


def draw_rectangle(screen, rect_color, rect_pos, rect_size):
    # Ekrana bir dikdörtgen çiz
    pygame.draw.rect(screen, rect_color, pygame.Rect(rect_pos, rect_size), 2)  # 2 pixel çizgi kalınlığı

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Çemberin Çeyrekleri")

    clock = pygame.time.Clock()

    # Büyük çemberin merkezi ve yarıçapı
    outer_circle_center = (WIDTH // 2, HEIGHT // 2)
    outer_circle_radius = 150

    # İç çemberin merkezi ve yarıçapı
    inner_circle_center = outer_circle_center
    inner_circle_radius = 100

    screen.fill(BLACK)

    # BottomRightPath'i çiz
    bottom_right_path = BottomRightPath(screen, outer_circle_center, outer_circle_radius, inner_circle_center, inner_circle_radius)
    point = (150,350)
    bottom_right_path.draw(point)

    # BottomRightPath'in son noktasını al
    bottom_right_end = point[0] + inner_circle_radius, point[1] 
    # StraightPath'in başlangıç noktasını belirle
    straight_path_start = bottom_right_end
    # StraightPath'i çi
    straight_path = StraightPath(screen)
    straight_path.draw(straight_path_start)

    end_point = straight_path_start[0] + 150 , straight_path_start[1] + 150
    top_left_path = TopLeftPath(screen, outer_circle_center, outer_circle_radius, inner_circle_center, inner_circle_radius)
    top_left_path.draw(end_point)

    top_left_end = end_point[0] ,end_point[1] + 100
    straight_two_path_start = top_left_end
    straight_two_path = StraighttwoPath(screen)
    straight_two_path.draw(straight_two_path_start)

    end = top_left_end[0] + 300 , top_left_end[1] - 100
    top_right_path = TopRightPath(screen, outer_circle_center, outer_circle_radius, inner_circle_center, inner_circle_radius)
    top_right_path.draw(end)
    
    top_right_end = end[0] + 100 ,end[1] - 150
    straight_path_start = top_right_end
    straight_path = StraightPath(screen)
    straight_path.draw(straight_path_start)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


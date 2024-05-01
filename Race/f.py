import pygame
import sys
import random
import math
from math import radians, cos, sin, atan2, degrees
from shapely.geometry import Polygon, LineString
import numpy as np

black = (105, 105, 105)
white = (248, 248, 255)
red = (200, 0, 0)
green = (154, 205, 50)
blue = (0, 0, 200)
gri = (179, 238, 58)
R = (169, 0, 0)
w = (253, 245, 230)

class Environment:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1500, 1000
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("F1 Yarışı")
        self.clock = pygame.time.Clock()

        self.car_img_original = pygame.image.load('car.png')
        self.car_img = pygame.transform.scale(self.car_img_original, (120, 60))
        self.car_position = [self.WIDTH // 2, self.HEIGHT - 110]
        self.car_speed = 5

        self.images = {
            'f2': pygame.image.load('f2.png'),
            'backk': pygame.image.load('backk.png'),
            'bayrak': pygame.image.load('bayrak.png'),
            'arka': pygame.image.load('arka.png')
        }

        self.shapes_drawn = False
        self.square_positions = []  # Karelerin konumlarını tutmak için bir liste ekliyoruz

    def generate_non_intersecting_points(self, center_x, center_y, num_points, radius):
        angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(num_points)])
        return [(center_x + radius * math.cos(angle), center_y + radius * math.sin(angle)) for angle in angles]

    def draw_filled_area_between_shapes(self):
        self.screen.fill((253, 245, 230))
        points = self.generate_non_intersecting_points(self.WIDTH // 2 - 100, self.HEIGHT// 2 + 100, 15, 300)
        poly = Polygon(points)
        smoothed_poly = poly.buffer(50, resolution=32)  

        line = LineString(smoothed_poly.exterior.coords)  
        offset_line_right = line.parallel_offset(60, 'right', join_style=2)  
        offset_line_left = line.parallel_offset(4, 'left', join_style=2)  
        offset_line_left2 = line.parallel_offset(10, 'left', join_style=2)  
        offset_line_right3 = line.parallel_offset(64, 'right', join_style=2)  

        merged_coords_right = list(line.coords) + list(offset_line_right.coords)[::-1]  
        merged_polygon_right = Polygon(merged_coords_right)

        smoothed_coords = list(smoothed_poly.exterior.coords)
        offset_coords_right = list(offset_line_right.coords)
        offset_coords_left = list(offset_line_left.coords)
        offset_coords_left2 = list(offset_line_left2.coords)
        offset_coords_right3 = list(offset_line_right3.coords)

        self.screen.fill((253, 245, 230))
        # Poligonların koordinatlarını çiz
        pygame.draw.polygon(self.screen, black, smoothed_coords, 5)  # Orijinal poligonu çiz
        pygame.draw.polygon(self.screen, black, offset_coords_right, 5)  # Sağa ofset poligonu çiz
        pygame.draw.polygon(self.screen, green, offset_coords_left, 5)  # Sola ofset poligonu çiz
        pygame.draw.polygon(self.screen, gri, offset_coords_left2, 5)  # Sola ofset poligonu çiz
        pygame.draw.polygon(self.screen, green, offset_coords_right3, 5)  # Sağa ofset poligonu çiz
        pygame.draw.polygon(self.screen, black, list(merged_polygon_right.exterior.coords), 0)  # Aradaki alanı beyaz ile doldur

    def save_positions_to_file(self, file_name):
        with open(file_name, 'w') as file:
            for pos in self.square_positions:
                file.write(f"{pos[0]}, {pos[1]}\n")

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.shapes_drawn = False  
                    elif event.key == pygame.K_s:  # 's' tuşuna basıldığında ekranı kaydet
                        pygame.image.save(self.screen, "map.png")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Sol tıklama
                        # Tıklanan yere karenin konumunu ekleyelim
                        self.square_positions.append(event.pos)
                        self.save_positions_to_file("positions.txt")

            if not self.shapes_drawn:
                self.draw_filled_area_between_shapes()
                self.shapes_drawn = True

            keys = pygame.key.get_pressed()
            
            self.screen.blit(self.images['arka'], (0, 0))
            self.screen.blit(self.images['f2'], (self.WIDTH - 500, self.HEIGHT - 15 - self.images['f2'].get_height()))
            self.screen.blit(self.images['backk'], (self.WIDTH - self.images['backk'].get_width(), self.HEIGHT - self.images['backk'].get_height()))
            self.screen.blit(self.images['bayrak'], (0, self.HEIGHT - self.images['bayrak'].get_height()))

            # Kareleri çiz
            for pos in self.square_positions:
                pygame.draw.rect(self.screen, R, (pos[0], pos[1], 5, 5))

            pygame.draw.rect(self.screen, (169, 0, 0), (0, 0, self.WIDTH, self.HEIGHT), 5)
            pygame.draw.rect(self.screen, (169, 0, 0), (0, 200, 1300, 800), 3)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Environment()
    game.main()
    
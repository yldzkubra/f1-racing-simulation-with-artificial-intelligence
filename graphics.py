#graphics.py
import numpy as np
import math
import pygame


class Graphics:
    def __init__(self, dimensions, robot_img_path, map_img_path):
        pygame.init()
        
        self.sensor_color = (127, 255, 0)
        
        # map
        self.robot = pygame.image.load(robot_img_path)
        self.robot = pygame.transform.scale(self.robot, (30, 30)) 
        self.map_img = pygame.image.load(map_img_path)
        
        self.height, self.width = dimensions
        
        # window settings
        pygame.display.set_caption("Obstacle Avoidance")
        
        self.map = pygame.display.set_mode((self.width, self.height))
        self.map.blit(self.map_img, (0, 0))
    
    
    def draw_robot(self, x0, y0, q0):
        rotated = pygame.transform.rotozoom(self.robot, math.degrees(q0), 1)
        rect = rotated.get_rect(center=(x0, y0))
        self.map.blit(rotated, rect)
    
    
    def draw_sensor_data(self, point_cloud):
        for point in point_cloud:
            pygame.draw.circle(self.map, self.sensor_color, point, 3, 0)
        
              
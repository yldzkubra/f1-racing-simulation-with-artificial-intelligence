#main.py
import math
import pygame
from robot import Robot
from graphics import Graphics
from ultrasonic import Ultrasonic


MAP_DIMENSIONS = (1000, 1500)
ROBOT_PATH = "car.png"
MAP_PATH = "map.png"

def set_start_position_from_file(file_name):
        with open(file_name, 'r') as file:
            position = file.readline().strip().split(',')
            start_position = (int(position[0]), int(position[1]))
        return start_position

if __name__ == "__main__":
    
    gfx = Graphics(MAP_DIMENSIONS, ROBOT_PATH, MAP_PATH)
    
    # robot
    start = set_start_position_from_file("positions.txt")
    # Başlangıç pozisyonunu al
    x0, y0, q0 =start[0], start[1], -1.5708
    xg, yg = 650, 700
    robot = Robot( x0, y0, q0, xg, yg, 0.01 * 3779.52)
   
    
    # sensor
    sensor_range = 150, math.radians(15)
    ultra_sonic = Ultrasonic(sensor_range, gfx.map)
    
    time_step = 0
    last_time = pygame.time.get_ticks()
    
    running = True
    # simulation loop
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        time_step = (pygame.time.get_ticks() - last_time)/1000
        last_time = pygame.time.get_ticks()
        
        gfx.map.blit(gfx.map_img, (0, 0))
        robot.kinematics(time_step)
        gfx.draw_robot(robot.x0, robot.y0, robot.q0)
        point_cloud = ultra_sonic.sense_obstacles(robot.x0, robot.y0, robot.q0)
        robot.avoid_obstacles(point_cloud, time_step)
        gfx.draw_sensor_data(point_cloud)
        
        pygame.display.update()
                
          
    
    
    
    
    

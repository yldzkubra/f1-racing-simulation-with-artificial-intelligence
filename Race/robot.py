import pygame
import math
import numpy as np


def distance(point1, point2):
    point1 = np.array(point1)
    point2 = np.array(point2)
    return np.linalg.norm(point1 - point2)


class Robot:
    def __init__(self, x0, y0, q0, xg, yg, width):

        self.meters_to_pixel = 3779.52
        self.w = width

        self.x0, self.y0, self.q0 = x0, y0, q0  # Initial position
        self.xg, self.yg = xg, yg  # Target pose

        self.vl = 0.01*self.meters_to_pixel
        self.vr = 0.01*self.meters_to_pixel

        
        self.max_speed = 0.02*self.meters_to_pixel
        self.min_speed = 0.02*self.meters_to_pixel
        
        self.closest_obs = None

        self.min_obs_dist = 20
        self.count_down = 0

        
        
    def avoid_obstacles(self, point_cloud, time_step):
        closest_obs = None
        dist = np.inf
        
        if len(point_cloud) > 1:
            for point in point_cloud:
                if dist > distance([self.x0, self.y0], point):
                    dist = distance([self.x0, self.y0], point)
                    closest_obs = (point, dist)

            if closest_obs[1] < self.min_obs_dist and self.count_down > 0:
                self.count_down -= time_step
                self.move_backward()
            else:
                self.count_down = 5
                self.move_forward()
            print(closest_obs[1])
    
    def move_backward(self):
        self.vr = -self.min_speed
        self.vl = -self.min_speed/2
        
    def move_forward(self):
        self.vr = self.min_speed
        self.vl = self.min_speed
        
    def kinematics(self, time_step):
        
        self.x0 += ((self.vl + self.vr)/2) * math.cos(self.q0) *time_step
        self.y0 -= ((self.vl + self.vr)/2) * math.sin(self.q0) *time_step
        
        self.q0 += (self.vr - self.vl) / self.w * time_step
        
        
        #if self.q0 > 2*math.pi or self.q0 < -2*math.pi:
            #self.q0 = 0
        
        self.vr = max(min(self.max_speed, self.vr), self.min_speed)
        self.vl = max(min(self.max_speed, self.vl), self.min_speed)
             
                    
                
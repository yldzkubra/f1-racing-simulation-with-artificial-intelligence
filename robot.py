#robot.py
import pygame
import math
import numpy as np


def distance(point1, point2):
    point1 = np.array(point1)
    point2 = np.array(point2)
    return np.linalg.norm(point1 - point2)

def read_and_rearrange_positions(file_name):
        target_points = []
        with open(file_name, 'r') as file:
            lines = file.readlines()  # Tüm satırları bir liste olarak oku
            
            # Koordinatları parse et ve listeye ekle
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    x, y = int(parts[0]), int(parts[1])
                    target_points.append((x, y))

        # Liste elemanlarını yeniden düzenle
        if len(target_points) >= 2:
            # İlk elemanı al ve sona ekle
            first_element = target_points.pop(0)
            # İkinci elemanı (şimdi ilk olan) al ve başa ekle
            second_element = target_points.pop(0)
            target_points.insert(0, second_element)
            target_points.append(first_element)
            

        return target_points



class Robot:
    def __init__(self, x0, y0, q0,  width):

        self.meters_to_pixel = 3779.52
        self.w = width

        self.x0, self.y0, self.q0 = x0, y0, q0  # Initial position
        
        
        self.target_points = read_and_rearrange_positions("positions.txt")
        self.current_target_index = 0
        self.update_target()

        self.vl = 0.01*self.meters_to_pixel
        self.vr = 0.01*self.meters_to_pixel

        self.max_speed = 0.02*self.meters_to_pixel
        self.min_speed = 0.02*self.meters_to_pixel
        
        self.closest_obs = None

       # PI Controller parameters
        self.Kp = 0.1  # Proportional gain
        self.Ki = 0.02  # Integral gain
        self.integral_error = 0  # Integral of error
        self.previous_error = 0  # Previous error

    def update_target(self):
        self.xg, self.yg = self.target_points[self.current_target_index]

    def check_target_reached(self):
        target_x, target_y = self.target_points[self.current_target_index]
        if distance((self.x0, self.y0), (target_x, target_y)) < 10:
            self.current_target_index += 1
            if self.current_target_index >= len(self.target_points):
                self.current_target_index = 0
            self.update_target()
        

    def grass(self, point_cloud ):
        self.closest_obs = None
        dist = np.inf
        
        if len(point_cloud) > 1:
            for point in point_cloud:
                if dist > distance([self.x0, self.y0], point):
                    dist = distance([self.x0, self.y0], point)
                    self.closest_obs = (point, dist)
        
    def kinematics(self, time_step):
        error = distance((self.x0, self.y0), (self.xg, self.yg))
        
        # Update integral of error
        self.integral_error += error * time_step

        # Calculate control action
        control_action = self.Kp * error + self.Ki * self.integral_error

        # Update velocities based on control action
        self.vl = max(min(self.max_speed, self.vl + control_action), self.min_speed)
        self.vr = max(min(self.max_speed, self.vr + control_action), self.min_speed)

        # Update position and orientation
        self.x0 += ((self.vl + self.vr) / 2) * math.cos(self.q0) * time_step
        self.y0 -= ((self.vl + self.vr) / 2) * math.sin(self.q0) * time_step
        self.q0 += (self.vr - self.vl) / self.w * time_step
    

    def turn_left(self):
        self.q0 -= math.radians(10)  # 5 derece sola dön
        if self.q0 < -math.pi:
            self.q0 += 2 * math.pi

    def turn_right(self):
        self.q0 += math.radians(10)  # 5 derece sağa dön
        if self.q0 > math.pi:
            self.q0 -= 2 * math.pi
            
    def move_backward(self):
        self.vr = -self.min_speed
        self.vl = -self.min_speed/2
        
    def move_forward(self):
        self.vr = self.min_speed
        self.vl = self.min_speed


    def calculate_reward(self, WIDTH, HEIGHT):
        track_width = 60
        cx = 650  # Pistin merkezi x koordinatı
        cy = 600  # Pistin merkezi y koordinatı

        # Robotun pist merkezine olan mesafesini hesapla
        distance_from_center = np.sqrt((self.x0 - cx)**2 + (self.y0 - cy)**2)
        # Robotun hedefe olan mesafesini hesapla
        distance_to_goal = np.sqrt((self.x0 - self.xg)**2 + (self.y0 - self.yg)**2)

        # Ödülü başlangıçta 0 olarak ayarla
        reward = 0.0

        # Pist merkezine olan mesafeye göre ödülü hesapla
        normalized_distance_from_center = distance_from_center / (track_width / 2)
        if distance_from_center < track_width / 2:
            reward += (1 - normalized_distance_from_center) * 10  # Pist içinde kalındıkça ödül
        else:
            reward -= 20  # Pist dışına çıkıldığında büyük bir ceza

        # Hedefe olan mesafeye göre ödülü artır
        max_distance = np.sqrt(WIDTH**2 + HEIGHT**2)
        normalized_distance_to_goal = distance_to_goal / max_distance
        reward += (1 - normalized_distance_to_goal) * 10  # Hedefe yaklaştıkça ödül artar

        # En yakın engelle olan mesafeye bağlı olarak ceza ekle
        if self.closest_obs is not None and self.closest_obs[1] < 45:
            reward -= 50  # Engellere çok yaklaşıldığında ceza

        return reward


    def step(self, action, time_step):
        running = True

        # Apply the action to update velocities
        if action == 0 : #"accelerate"
            self.move_forward()
        elif action == 1: #"brake":
            self.move_backward()
        elif action == 2: #"turn_right":
             self.turn_left()
        elif action == 3: #"turn_left":
            self.turn_right()

        # Update car kinematics
        self.kinematics(time_step)  # Consider defining your time_step or pass it as parameter

        # Check if new position is close to the target
        self.check_target_reached()

        # Calculate reward
        reward = self.calculate_reward(1500, 1000)

        # Determine if the episode has ended
        done = self.current_target_index == 3  # Reset after a complete loop or define another terminal condition
        if self.closest_obs is not None and self.closest_obs[1] < 14:
                running = False



        # Return the new observable state, reward, and done status
        new_state = (self.x0, self.y0, self.q0)
        return new_state, reward, done, running


  
                    
                
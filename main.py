#main.py
import pygame
import math
import numpy as np
from robot import Robot
from agent_brain import QLearningAgent
from graphics import Graphics
from ultrasonic import Ultrasonic

# Oyun ayarları ve sabitleri
MAP_DIMENSIONS = (1000, 1500)
ROBOT_PATH = "car.png"
MAP_PATH = "map.png"
ACTIONS = [0, 1, 2, 3]  # Eylem seti: hızlan, fren yap, sağa dön, sola dön
NUM_EPISODES = 100

# Başlangıç pozisyonunu dosyadan ayarla
def set_start_position_from_file(file_name):
    with open(file_name, 'r') as file:
        position = file.readline().strip().split(',')
        start_position = (int(position[0]), int(position[1]), -1.5708)  # Açıyı da ekle
    return start_position

if __name__ == "__main__":

    gfx = Graphics(MAP_DIMENSIONS, ROBOT_PATH, MAP_PATH)

    # Create Q-Learning agent
    x_bins = np.linspace(0, MAP_DIMENSIONS[1], num=10)
    y_bins = np.linspace(0, MAP_DIMENSIONS[0], num=10)
    q_bins = np.linspace(-180, 180, num=12)
    agent = QLearningAgent(x_bins, y_bins, q_bins, ACTIONS)

    sensor_range = (150, math.radians(15))
    ultra_sonic = Ultrasonic(sensor_range, gfx.map)

    time_step = 0
    last_time = pygame.time.get_ticks()

    done = False
    for episode in range(NUM_EPISODES):
        print("----START------")

        total_reward = 0

        start = set_start_position_from_file("positions.txt")
        x0, y0, q0 =start[0], start[1], start[2]
        robot = Robot( x0, y0, q0,  0.01 * 3779.52)
        state = agent.discretize_state(robot.x0, robot.y0, robot.q0) # Başlangıç durumunu sıfırla

        if done:
            print("---FINISH-----")
            break

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            time_step = (pygame.time.get_ticks() - last_time)/1000
            last_time = pygame.time.get_ticks()
            
            gfx.map.blit(gfx.map_img, (0, 0))
            gfx.draw_robot(robot.x0, robot.y0, robot.q0)
            #print(robot.x0)
            #robot.kinematics(time_step)
            point_cloud = ultra_sonic.sense_obstacles(robot.x0, robot.y0, robot.q0)
            robot.grass(point_cloud)
            gfx.draw_sensor_data(point_cloud)

            action = agent.choose_action(state)
            next_state, reward, done, running = robot.step(action, time_step)  # Ajanın eylemini uygula ve yeni durum bilgisini al
            next_state = agent.discretize_state(next_state[0],next_state[1], next_state[2])
            agent.learn(state, action, reward, next_state, robot.closest_obs )  # RL ajanı bu deneyimden öğrenir
            state = next_state
            total_reward += reward

            if not running:
             break

            pygame.display.update()

        print(f"Episode {episode+1}: Total Reward = {total_reward}")

   

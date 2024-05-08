#agent_brain.py
# Importing libraries
import numpy as np
import pandas as pd


class QLearningAgent:
    def __init__(self,  x_bins, y_bins, q_bins, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.x_bins = x_bins
        self.y_bins = y_bins
        self.q_bins = q_bins
        self.actions = actions
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy

       # Creating full Q-table for all cells
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
    
    def discretize_state(self, x, y, q):
        x_bin = np.digitize(x, self.x_bins)
        y_bin = np.digitize(y, self.y_bins)
        q_bin = np.digitize(q, self.q_bins)
        return f"{x_bin}_{y_bin}_{q_bin}"     
    

    def choose_action(self, observation):
        self.check_state_exist(observation)
        if np.random.uniform() < self.epsilon:
            state_action = self.q_table.loc[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            action = state_action.idxmax()
        else:
            # Choosing random action - left 10 % for choosing randomly
            action = np.random.choice(self.actions)
        return action
    

    def learn(self, state, action, reward, next_state, closest_obs):
        self.check_state_exist(next_state)
        q_predict = self.q_table.loc[state, action]

        # Bellman denklemi ile Q-değeri güncelleme
        if closest_obs is not None and closest_obs[1] < 25:
            # Sonraki durum için maksimum Q-değeri
            q_target = reward  # Terminal durumda gelecek ödül yoktur
        else:
            q_target = reward + self.gamma * self.q_table.loc[next_state, :].max()

        self.q_table.loc[state, action] += self.lr * (q_target - q_predict)
        return self.q_table.loc[state, action]
    

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            new_state = pd.DataFrame([0]*len(self.actions), index=self.q_table.columns).T
            new_state.index = [state]
            
            # Concatenate the new state DataFrame to the existing q_table
            self.q_table = pd.concat([self.q_table, new_state])



    

    
    

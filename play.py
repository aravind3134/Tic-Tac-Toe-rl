from Game import Game
import numpy as np

class Experience(object):


def play():
    game = Game()
    state = game.get_current_status()
    game_over = game.game_over(state)
    experience = []

    while not game_over:
        old_state = state

def random_strategy(self, state):
    random_strategy_successful = 0
    random_x = np.random.int(3)
    random_y = np.random.int(3)
    while random_strategy_successful == 0:
        if state[random_x][random_y]== 0:
            state[random_x][random_y] = 2
            random_strategy_successful = 1

def static_preference_strategy(self, state):
    if state[1][1] == 0:
        state[1][1] = 2
    else:
        for i in range(3):
            for j in range(3):
                if state[i][j] == 1:
                    if state[i][j+1] == 0 and j<2:
                        state[i][j+1] = 2
                    if state[i][j-1] == 0 and j>0:
                        state[i][j-1] = 2
                    if state[i-1][j] == 0 and i>0:
                        state[i-1][j] = 2
                    if state[i+1][j] == 0 and i<2:
                        state[i+1][j] = 2

def get_empty_spaces(state):
    for i in range(3):
        for j in range(3):
            if state[i, j] == 0:

def highest_reward_strategy(self, state):
    self.state = state
    available_empty_spaces = get_empty_spaces(state)
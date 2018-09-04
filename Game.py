import numpy as np

ACTION_X = 1  # user input
ACTION_O = 2  # computer input

class Game(object):
    """ Represents  tic tac toe game and interacts with the person to play.
    Inputs: User Selection comes with a random position selected and the choice to use 'x' or 'o'.
    """
    def __init__(self, state, play_first, initial_score = 0):
        self._score = initial_score
        self.comp_successful = 0
        self.user_successful = 0
        self.comp_won = 0
        self.user_won = 0
        if (play_first == 1):
            self._state = np.zeros((3,3), dtype=np.int)
            self.select_random_position(self._state)
            self.comp_successful = 0
        else:
            self._state = state
            while(self.comp_successful== 0):
                self.select_random_position(self._state)
            self.comp_successful = 0

    # def is_selection_available(self, present_selection):
    #    for row in range(3):
    def select_random_position(self, state):
        self._state = state
        empty_index_x = np.random.choice(3)
        empty_index_y = np.random.choice(3)
        if(self._state[empty_index_x] [empty_index_y] == 0):
            self._state[empty_index_x] [empty_index_y] = ACTION_O   # => 2 - computer input
            self.comp_successful = 1
        else:
            self.comp_successful = 0

    def let_user_select(self, state):
        self._state = state
        empty_index_x = np.random.choice (3)
        empty_index_y = np.random.choice (3)
        if (self._state[empty_index_x] [empty_index_y] == 0):
            self._state[empty_index_x] [empty_index_y] = ACTION_X  # => 1 - user input
            self.user_successful = 1
        else:
            self.user_successful = 0

    # def _select_positon(self, ):
    def get_current_status(self):
        return self._state

    def print_state(self):
        state = self._state
        state1 = [0] * 3
        print("=====================")
        for i in range(3):
            for j in range(3):
                if state[i][j] == 1:
                    state1[j] = 'x'
                elif state[i][j] == 2:
                    state1[j] = 'o'
                else:
                    state1[j] = '-'
            print(state1)
        print("=====================")

    def get_actual_user_input(self, row_position, column_position):
        self._state[row_position][column_position] = 1

    def get_comp_success_status(self):
        return self.comp_successful

    def get_user_success_status(self):
        return self.user_successful

    def game_over(self, state):
        self._state = state
        if np.count_nonzero(state) == 9:
            return 1
        else:
            return 0

    def generate_user_reward(self, state):
        reward = 0
        count_diag = 0
        count_antidiag = 0
        count_cols = 0
        count_rows = 0
        self._state = state
        # print ("State in reward:\n", self._state)
        for i in range (3):
            for j in range (3):
                if self._state[i][j] == ACTION_X:
                    count_cols = count_cols + 1
                    if count_cols == 3:
                        reward = 2
                        count_cols = 0
                        self.user_won = 1
                if self._state[j][i] == ACTION_X:
                    count_rows = count_rows + 1
                    if count_rows == 3:
                        reward = 2
                        count_rows = 0
                        self.user_won = 1
            if self._state[i][i] == ACTION_X:
                count_diag = count_diag + 1
                if count_diag == 3:
                    reward = 2
                    count_diag = 0
                    self.user_won = 1
            if self._state[i][2 - i] == ACTION_X:
                count_antidiag = count_antidiag + 1
                if count_antidiag == 3:
                    reward = 2
                    count_antidiag = 0
                    self.user_won = 1
            count_cols= 0
            count_rows = 0
        return reward

    def generate_comp_reward(self, state):
        reward = 0
        count = 0
        count1 = 0
        count2 = 0
        count3 = 0
        self._state = state
        # print("State in reward:\n", self._state)
        for i in range(3):
            for j in range(3):
                if self._state[i][j] == ACTION_O:
                    count2 = count2 + 1
                    if count2 == 2:
                        reward = 1
                    if count2 == 3:
                        reward = 2
                        count2 = 0
                        self.comp_won = 1
                        break
                if self._state[j][i] == ACTION_O:
                    count3 = count3 + 1
                    if count3 == 2:
                        reward = 1
                    if count3 == 3:
                        reward = 2
                        count3 = 0
                        self.comp_won = 1
                        break
            if reward == 2:
                break
            if self._state[i][i] == ACTION_O:
                count = count + 1
                if count == 2:
                    reward = 1
                if count == 3:
                    reward = 2
                    count = 0
                    self.comp_won = 1
                    break
            if self._state[i][2 - i] == ACTION_O:
                count1 = count1 + 1
                if count1 == 2:
                    reward = 1
                if count1 == 3:
                    reward = 2
                    count1 = 0
                    self.comp_won = 1
                    break
            count2 = 0
            count3 = 0
        return reward

    def is_training(self):
        return self.train

    def play(self, state, user_successful, comp_successful, status_train_or_test):
        if status_train_or_test == 'P':
            self.train = 0
        else:
            self.train = 1
        self._state = state
        self.user_successful = user_successful
        self.comp_successful = comp_successful
        while self.user_successful == 0:
            if self.is_training() != 0:
                self.let_user_select(self._state)
            else:
                if self.comp_won == 0:
                    self.print_state()
                    row_number = int (input ("Select a position in grid.\nEnter row number[0, 1, 2]:"))
                    column_number = int (input ("Enter Column number too![0,1,2]: "))
                    self._state[row_number][column_number] = ACTION_X
                    self.user_successful = 1
                    if self.generate_user_reward(self._state) == 2:
                        self.user_won = 1
                else:
                    break
        self.user_successful = 0
        self._state = self.get_current_status()
        if self.game_over(self._state)!= 1 and self.user_won == 0:
            while self.comp_successful == 0:
                self.select_random_position(self._state)
            self.comp_successful = 0

def main():
    # user_preference = "yes"
    train_or_play = input("Do you want to play the game or train the game?\n Enter P to play it or T to train it:")
    user_preference = input ("Do you want to play first?? Please enter yes or no: ")
    state = np.zeros ((3, 3), dtype=np.int)
    if user_preference == "yes":
        print("User plays!!!")
        if train_or_play == 'T':
            empty_index_x = np.random.choice(3)
            empty_index_y = np.random.choice(3)
            state[empty_index_x, empty_index_y] = ACTION_X   # => 1 - user input
        else:
            print("Sample to give u an idea. The Game has 3 rows and 3 columns")
            print(" __ __ __")
            print("|__|__|__|")
            print("|__|__|__|")
            print("|__|__|__|")
            row_number = int(input("Select a position in grid.\nEnter row number[0, 1, 2]:"))
            column_number = int(input("Enter Column number too![0,1,2]: "))
            print(row_number, column_number)
            state[row_number, column_number] = ACTION_X
        play_first = 0
        game = Game(state, play_first)
    else:
        play_first = 1
        print("Computer plays!!!")
        game = Game(state, play_first)
    print ("User uses 'x' and Comp uses 'o'")
    # print("Entering play!")
    # game.play(game.get_current_status())
    game_over = game.game_over(game.get_current_status())
    while game_over== 0 and game.comp_won ==0 and game.user_won == 0:
        # game.get_actual_user_input(1, 2)
        game_current_status = game.get_current_status()
        game_user_input_succeeded = game.get_user_success_status()
        game_comp_input_succeeded = game.get_comp_success_status()
        game.play(game_current_status, game_user_input_succeeded, game_comp_input_succeeded, train_or_play)
        game_over = game.game_over(game.get_current_status())
        comp_reward = game.generate_comp_reward (game.get_current_status ())
        user_reward = game.generate_user_reward (game.get_current_status ())
        if game_over == 1 or game.comp_won == 1 or game.user_won == 1:
            print("Final Result:")
            game.print_state()
            print ("Comp Reward:", comp_reward)
            print ("User Reward:", user_reward)
            if comp_reward == 2 or user_reward == 2:
                if comp_reward == user_reward:
                    print ("Game drawn")
                elif comp_reward > user_reward:
                    print ("Comp wins!")
                else:
                    print ("User wins!!")
            break

if __name__ == "__main__":
    main()

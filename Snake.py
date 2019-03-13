import copy

import numpy as np


class Snake:
    def __init__(self, board):
        self.input_size = 4
        self.output_size = 4
        self.fruit = []
        self.board = board
        self.snake = [[int(self.board[0] / 2), int(self.board[1] / 2) - 2],
                      [int(self.board[0] / 2), int(self.board[1] / 2) - 1],
                      [int(self.board[0] / 2), int(self.board[1] / 2)]]
        self.score = 0
        self.new_fruit()
        self.max_time = board[0] * board[1]

    def run_genome(self, g, save_replay=False):
        order = g.assemble()
        done = False
        time = 0
        last_time = 0
        frames = []
        while not done:
            time += 1
            action = np.argmax(g.run(self.get_state(), order))
            if self.act(action):
                last_time = time
            if save_replay:
                frames.append(copy.deepcopy([self.snake, self.fruit, self.score, action]))
            done = self.is_dead()
            if time - last_time >= self.max_time:
                done = True  # hasen't gotten a fruit in a while but should have been able to.
        score = self.score + time/self.max_time
        # Rewards first and formost score and then staying alive,
        self.reset()
        return score, frames

    def act(self, action):
        if action == 0:
            self.snake.append([self.snake[-1][0], self.snake[-1][1] + 1])
            # move up
        elif action == 1:
            self.snake.append([self.snake[-1][0] + 1, self.snake[-1][1]])
            # move right
        elif action == 2:
            self.snake.append([self.snake[-1][0], self.snake[-1][1] - 1])
            # move down
        elif action == 3:
            self.snake.append([self.snake[-1][0] - 1, self.snake[-1][1]])
            # move left
        else:
            print("Not an Action")
            return False

        if self.snake[-1][0] == self.fruit[0] and self.snake[-1][1] == self.fruit[1]:
            self.score += 1
            self.new_fruit()
            return True
            # landed on fruit
        else:
            self.snake = self.snake[1:]
            return False

    def reset(self):
        self.snake = [[int(self.board[0] / 2), int(self.board[1] / 2) - 2],
                      [int(self.board[0] / 2), int(self.board[1] / 2) - 1],
                      [int(self.board[0] / 2), int(self.board[1] / 2)]]
        self.score = 0
        self.new_fruit()

    def new_fruit(self):
        grid = np.vstack((np.meshgrid(np.linspace(0, self.board[0], num=self.board[0], endpoint=False),
                                      np.linspace(0, self.board[1], num=self.board[1], endpoint=False))[0].flatten(),
                          np.meshgrid(np.linspace(0, self.board[0], num=self.board[0], endpoint=False),
                                      np.linspace(0, self.board[1], num=self.board[1], endpoint=False))[1].flatten())).T
        for p in self.snake:
            np.delete(grid, np.where(np.all(grid == np.array(p), axis=1)))  # make more efficient
        self.fruit = list(grid[np.random.randint(grid.shape[0])])

    def is_dead(self):
        if self.snake[-1][0] >= self.board[0] or self.snake[-1][1] >= self.board[1] or self.snake[-1][1] < 0 or \
                self.snake[-1][0] < 0:
            # out of bounds
            return True
        if self.snake[-1] in self.snake[:-1]:
            # hit itself
            return True
        return False

    def get_state(self):
        """ 
          |  
        - o -
          |   
        Snake sees in 4 directions
        """
        # if value is positive then it indicates that it sees the fruit there else it sees wall or itself

        obstacles = np.array(self.snake[:-1] + [[self.snake[-1][0], 0], [0, self.snake[-1][1]], [self.snake[-1][0], self.board[1]], [self.board[0], self.snake[-1][1]], self.fruit])
        dist = obstacles - self.snake[-1]

        up_dist = dist[(dist[:, 0] == 0) & (dist[:, 1] >= 0)]
        up_dist = up_dist[np.argmin(up_dist[:, 1])]
        up_index = np.where((dist[:, 0] == up_dist[0]) & (dist[:, 1] == up_dist[1]))[0][0]
        if up_index == len(dist) - 1:
            up_dist = self.board[1] - up_dist[1]
        else:
            up_dist = up_dist[1] - self.board[1]

        down_dist = dist[(dist[:, 0] == 0) & (dist[:, 1] <= 0)]
        down_dist = down_dist[np.argmax(down_dist[:, 1])]
        down_index = np.where((dist[:, 0] == down_dist[0]) & (dist[:, 1] == down_dist[1]))[0][0]
        if down_index == len(dist) - 1:
            down_dist = self.board[1] - down_dist[1]
        else:
            down_dist = down_dist[1] - self.board[1]

        left_dist = dist[(dist[:, 1] == 0) & (dist[:, 0] <= 0)]
        left_dist = left_dist[np.argmax(left_dist[:, 1])]
        left_index = np.where((dist[:, 0] == left_dist[0]) & (dist[:, 1] == left_dist[1]))[0][0]
        if left_index == len(dist) - 1:
            left_dist = self.board[1] - left_dist[1]
        else:
            left_dist = left_dist[1] - self.board[1]

        right_dist = dist[(dist[:, 1] == 0) & (dist[:, 0] >= 0)]
        right_dist = right_dist[np.argmin(right_dist[:,1])]
        right_index = np.where((dist[:,0] == right_dist[0]) & (dist[:,1] == right_dist[1]))[0][0]
        if right_index == len(dist) - 1:
            right_dist = self.board[1] - right_dist[1]
        else:
            right_dist = right_dist[1] - self.board[1]

        return [up_dist, right_dist, down_dist, left_dist]

    def print_frame(self, frame):
        board = np.full(self.board, '.')
        snake = frame[0]
        fruit = frame[1]

        for s in snake:
            if 0 <= s[0] < self.board[0] and 0 <= s[1] < self.board[0]:
                board[s[0]][s[1]] = 'o'

        board[int(fruit[0])][int(fruit[1])] = '@'

        string = '\n'.join('\t'.join(x for x in y) for y in board)
        print("Action: {}".format(frame[3]))
        print("Score raw: {}".format(frame[2]))
        print(string)

    def image_frame(self, frame):
        board = np.full(self.board, 0)
        snake = frame[0]
        fruit = frame[1]
        for s in snake:
            if 0 <= s[0] < self.board[0] and 0 <= s[1] < self.board[0]:
                board[s[0]][s[1]] = 1

        board[int(fruit[0])][int(fruit[1])] = 1

        return board
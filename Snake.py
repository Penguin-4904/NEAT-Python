import numpy as np


class Snake():
    def __init__(self, board, goal):
        self.input_size = 4
        self.output_size = 4
        self.snake = [[int(board[0] / 2), int(board[1] / 2)]]
        self.fruit = []
        self.board = board
        self.score = 0
        self.new_fruit()
        self.goal = goal
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
                frames.append([self.snake, self.fruit])
            done = self.is_dead()
            if time - last_time >= self.max_time:
                done = True  # hasen't gotten a fruit in a while but should have been able to.
        score = (self.score + time) / (time + self.goal)
        # Rewards first and formost score and then staying alive,
        # but also looks for efficiency after the goal is met.
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
        self.snake = [[int(self.board[0] / 2), int(self.board[1] / 2)]]
        self.score = 0
        self.new_fruit()

    def new_fruit(self):
        grid = np.vstack((np.meshgrid(np.linspace(0, self.board[0], num=self.board[0], endpoint=False),
                                     np.linspace(0, self.board[1], num=self.board[1], endpoint=False))[0].flatten(),
                          np.meshgrid(np.linspace(0, self.board[0], num=self.board[0], endpoint=False),
                                     np.linspace(0, self.board[1], num=self.board[1], endpoint=False))[1].flatten())).T
        for p in self.snake:
            np.delete(grid, np.where(np.all(grid == np.array(p), axis=1)))  # make more efficient
        self.fruit = grid[np.random.randint(grid.shape[0])]

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

        # up
        see_up = []
        up_dist = self.snake[-1][1] - self.board[1]
        for s in self.snake[:-1]:
            if (s[0] - self.snake[-1][0]) == 0 and (s[1] - self.snake[-1][1]) > 0:
                see_up.append(s)
        if (self.fruit[0] - self.snake[-1][0]) == 0 and (self.fruit[1] - self.snake[-1][1]) > 0:
            see_up.append(self.fruit)
        see_up.sort(key=lambda x: x[1] - self.snake[-1][1])
        if len(see_up) > 0:
            up_dist = self.snake[-1][1] - see_up[0][1]
            if (self.fruit in see_up) and up_dist == (self.snake[-1][1] - self.fruit[1]):
                up_dist = -up_dist

        # right
        see_right = []
        right_dist = self.snake[-1][0] - self.board[0]
        for s in self.snake[:-1]:
            if (s[1] - self.snake[-1][1]) == 0 and (s[0] - self.snake[-1][0]) > 0:
                see_right.append(s)
        if (self.fruit[1] - self.snake[-1][1]) == 0 and (self.fruit[0] - self.snake[-1][0]) > 0:
            see_right.append(self.fruit)
        see_right.sort(key=lambda x: x[0] - self.snake[-1][0])
        if len(see_right) > 0:
            right_dist = self.snake[-1][0] - see_right[0][0]
            if (self.fruit in see_right) and right_dist == (self.snake[-1][0] - self.fruit[0]):
                right_dist = -right_dist

        # down
        see_down = []
        down_dist = - self.snake[-1][1]
        for s in self.snake[:-1]:
            if (s[0] - self.snake[-1][0]) == 0 and (s[1] - self.snake[-1][1]) < 0:
                see_down.append(s)
        if (self.fruit[0] - self.snake[-1][0]) == 0 and (self.fruit[1] - self.snake[-1][1]) < 0:
            see_down.append(self.fruit)
        see_down.sort(key=lambda x: self.snake[-1][1] - x[1])
        if len(see_down) > 0:
            down_dist = -(self.snake[-1][1] - see_down[0][1])
            if (self.fruit in see_down) and down_dist == (self.snake[-1][1] - self.fruit[1]):
                down_dist = -down_dist

        # left
        see_left = []
        left_dist = - self.snake[-1][0]
        for s in self.snake[:-1]:
            if (s[1] - self.snake[-1][1]) == 0 and (s[0] - self.snake[-1][0]) < 0:
                see_left.append(s)
        if (self.fruit[1] - self.snake[-1][1]) == 0 and (self.fruit[0] - self.snake[-1][0]) < 0:
            see_left.append(self.fruit)
        see_left.sort(key=lambda x: self.snake[-1][0] - x[0])
        if len(see_left) > 0:
            left_dist = -(self.snake[-1][0] - see_left[0][0])
            if (self.fruit in see_left) and left_dist == (self.snake[-1][0] - self.fruit[0]):
                left_dist = -left_dist

        return [up_dist, right_dist, down_dist, left_dist]

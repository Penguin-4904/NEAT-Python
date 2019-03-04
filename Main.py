from Environment import Environment
from Snake import Snake
import time

snake = Snake([10, 10], 9)
test = Environment(snake, dist=[5, 1, .2], mutation_rates=[0.8, 0.05, 0.01])
print(type(test))
test.create(1000)

t = time.time()
for i in range(100):
    top_score = test.generation(replay=[0, 1]).score
    print("Generation: {}, Time: {}, Max Score: {}".format(i, round(time.time()-t, 2), round(top_score, 4))
    t = time.time()

print(len(test.species))
champ = test.generation(replay=[1, 0])
# print(champ[1].last_play)

for i, f in enumerate(champ[0].last_play):
    print("New Frame: {}".format(i))
    snake.print_frame(f)

# print(champ[1].score)
# print(len(champ[1].nodes))
# print(len(test.species[1]))

print(champ[0].score)
print(len(champ[0].nodes))
print(len(test.species[0]))

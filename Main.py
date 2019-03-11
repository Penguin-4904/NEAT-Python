from Environment import Environment
from Snake import Snake
import time

snake = Snake([10, 10], 9)
test = Environment(snake, dist=[.8, 1, .5], mutation_rates=[0.8, 0.05, 0.01], keep=.3)
print(type(test))
test.create(200)

t = time.time()
for i in range(400):
    r = test.generation(replay=[1, 3])
    r.sort(key=lambda x: sorted(x, key=lambda y: y.score * len(x), reverse=True)[0].score * len(x), reverse = True)
    top_score = r[0][0].score * len(r[0])
    print("Generation: {}, Time: {}, Max Score: {}, Species Sizes: {}".format(i, round(time.time()-t, 2), round(top_score, 4), [len(s) for s in test.species]))
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

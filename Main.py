from Environment import Environment
from Snake import Snake
import time
import copy

from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = plt.axes()

snake = Snake([10, 10])
test = Environment(snake, dist=[1.01, 1, .1], mutation_rates=[0.8, 0.05, 0.01], keep=.33, randomness=0)
test.create(200)

t = time.time()
best_score = 0
best_play = []
top_scores = []
for i in range(500):
    species = [len(s) for s in test.species]
    r = test.generation(replay=[1, 3])
    sort = sorted(r, key=lambda x: sorted(x, key=lambda y: y.score * len(x), reverse=True)[0].score * len(x),
                  reverse=True)
    top_score = sort[0][0].score * len(sort[0])
    if top_score > best_score:
        best_score = copy.copy(top_score)
        best_play = copy.copy(sort[0][0].last_play)
    top_scores.append(top_score)
    print("Generation: {}, Time: {}, Best Score: {}, Best Score Species: {}, Species Sizes: {}"
          .format(i, round(time.time() - t, 2), round(top_score, 4), r.index(sort[0]), species))
    t = time.time()

def animate(n):
    return ax.imshow(snake.image_frame(best_play[n])),


anim = animation.FuncAnimation(fig, animate, frames=len(best_play), blit=True)
anim.save('Score ' + str(best_score) + '.gif', fps=10)

fig = plt.figure()
ax = plt.axes()

plt.xlabel("Generation")
plt.ylabel("Best Score")
ax.plot(top_scores)
plt.savefig('plot1.jpg')
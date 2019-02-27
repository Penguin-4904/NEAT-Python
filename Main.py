from Enviorment import Enviorment
from Snake import Snake

snake = Snake([10, 10], 9)
test = Enviorment(snake, mutation_rates=[0.8, 0.05, 0.01])
print(type(test))
test.create(10)
champ = test.generation()

print(champ.last_play)
for i, f in enumerate(champ.last_play):
    print("new frame: {}".format(i))
    snake.print_frame(f)
print(champ.score)
print(len(champ.nodes))
from Enviorment import Enviorment
from Snake import Snake

snake = Snake([10, 10], 9)
test = Enviorment(snake, dist=[5, 1, .2], mutation_rates=[0.8, 0.05, 0.01])
print(type(test))
test.create(100)

for i in range(100):
    test.generation()
    print("Generation: {}".format(i))

print(len(test.species))
champ = test.generation(replay=[1,0])
#print(champ[1].last_play)

for i, f in enumerate(champ[1].last_play):
    print("New Frame: {}".format(i))
    snake.print_frame(f)

print(champ[1].score)
print(len(champ[1].nodes))
print(len(test.species[1]))

print(champ[0].score)
print(len(champ[0].nodes))
print(len(test.species[0]))
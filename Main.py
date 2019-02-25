from Enviorment import Enviorment
from Snake import Snake

snake = Snake([10, 10], 9)
test = Enviorment(snake)
print(type(test))
test.create(10)
test.generation([3, 3])

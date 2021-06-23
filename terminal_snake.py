import random

class Snake():
    keys = {"w" : "up", "s" : "down", "a" : "left", "d" : "right"}
    opposite_directions = {"up" : "down", "down" : "up", "left" : "right", "right" : "left"}
    direction_changes = {"up" : (-1, 0), "down": (1, 0), "left" : (0, -1), "right" : (0, 1)}
    
    def __init__(self, body, direction):
        self.body = body
        self.direction = direction

    def change_direction(self, key): 
        if key != "":
            new_direction = Snake.keys[key]
            if new_direction != Snake.opposite_directions[self.direction]:
                self.direction = new_direction

    def change_position(self):
        current_pos = self.body[0]
        add = Snake.direction_changes[self.direction]
        new_pos = tuple([current_pos[i] + add[i] for i in range(2)])
        self.body.insert(0, new_pos)
        self.body = self.body[:-1]

    def increase_length(self, game):
        end_pos = self.body[-1]
        new_pos_options = []
        for direction in Snake.direction_changes:
            new_pos = tuple([end_pos[i] + Snake.direction_changes[direction][i] for i in range(2)])
            new_pos_options.append(new_pos)
        final_options = []
        for i in new_pos_options:
            if i[0] in range(game.height) and i[1] in range(game.width):
                if i not in self.body:
                    final_options.append(i)
        index = random.randint(0, (len(final_options) - 1))
        new_pos = final_options[index]
        self.body.append(new_pos)
########################################    
class Game():
    high_score = 0

    def __init__(self, size, snake):
        self.score = 0
        self.height, self.width = size
        self.snake = snake
             
    def create_matrix(self):
        matrix = [[" " for col in range(self.width)] for row in range(self.height)]
        return matrix
                
    def set_apple_pos(self):
        new_row = random.randint(0, self.height)
        new_col = random.randint(0, self.width)
        while (new_row, new_col) in self.snake.body:
            new_row = random.randint(0, self.height)
            new_col = random.randint(0, self.width)
        self.apple_position = (new_row, new_col)

    def apple_eaten(self):
        snake_position = self.snake.body[0]
        if snake_position == self.apple_position:
            self.score += 1
            return True
        else:
            return False

    def render(self):
        board = self.create_matrix()
        apple_row, apple_col = self.apple_position
        board[apple_row][apple_col] = "*"
        body = self.snake.body
        for i in range(len(body)):
            row, col = body[i]
            if i == 0:
                board[row][col] = "X"
            else:
                board[row][col] = "O"
        print("+" + "=" * (self.width * 2 + 1) + "+")
        for i in board:
            print("| " + (" ".join(map(str,i))+ " |"))
        print("+" + "=" * (self.width * 2 + 1) + "+")

    def is_over(self):
        new_position = self.snake.body[0]
        new_row, new_col = new_position
        if self.snake.body.count(new_position) > 1:
            print("You crashed into yourself!") 
            return True
        elif new_row not in range(self.height) or new_col not in range(self.width):
            print("You crashed into a wall!")
            return True
        else:
            return False
########################################
def get_direction():
    direction_input = input()
    while direction_input not in ["w", "a", "s", "d", ""]:
        direction_input = input() 
    return direction_input
########################################
play_again = ""
while play_again != "N":
    snake = Snake([(3,3),(3,4),(3,5),(4,5)], "left")
    game = Game((10,10), snake)
    game.set_apple_pos()
    while game.is_over() == False:
        game.render()
        direction = get_direction()
        snake.change_direction(direction)
        snake.change_position()
        if game.apple_eaten():
            snake.increase_length(game)
            game.set_apple_pos()
        
    print("Game over!\n\n\tYOUR SCORE: " + str(game.score))
    if game.score <= Game.high_score:
        print("\n\tCURRENT HIGH SCORE: " + str(Game.high_score))
    else:
        print("\n\tPREVIOUS HIGH SCORE: " + str(Game.high_score))
        Game.high_score = game.score
        print("\tNEW HIGH SCORE: " + str(Game.high_score))
    
    play_again = input("\nWould you like to play again? (Y/N) ")
    while play_again not in ("Y", "N"):
        play_again = input("Please input again: ")

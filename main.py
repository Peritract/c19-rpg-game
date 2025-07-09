import curses
from _curses import window
from random import randint, choice

class Player:

    def __init__(self, x :int=5, y :int=5, health: int=10, money: int=0):
        self.name = choice(["Raymond", "Niall", "Nic", "Yacquub", "Yvonne", "Dan"])
        self.x = x
        self.y = y
        self.health = health
        self.money = money
        self.dead = False

    def move(self, direction: str, grid: list[list[str]]):
        new_loc = [self.x, self.y]
        if direction == "l":
            new_loc = [self.x - 1, self.y]
        elif direction == "r":
            new_loc = [self.x + 1, self.y]
        elif direction == "u":
            new_loc = [self.x, self.y - 1]
        elif direction == "d":
            new_loc = [self.x, self.y + 1]

        char_at = grid[new_loc[1]][new_loc[0]]
        if char_at != "#":
            self.x = new_loc[0]
            self.y = new_loc[1]
            if char_at == "^":
                self.health -= 1
                if self.health <= 0:
                    self.die()
            elif char_at == "*":
                self.money += 1
                grid[new_loc[1]][new_loc[0]] = " "
                    
    def die(self):
        self.dead = True

        

class Grid:

    def __init__(self, width: int=60, height: int=20):
        self.w = width
        self.h = height
        self.tiles = self.make_tiles()
        self.player = Player(self.w // 2, self.h // 2)

    def make_tiles(self) -> list[list[str]]:
        """Adds a bunch of walls to the map."""
        
        # Create an empty map
        tiles = [
            [
                " "
                for x in range(self.w)
            ]
            for y in range(self.h)
        ]

        # Add walls at the edges
        for y in range(self.h):
            for x in range(self.w):
                if x == 0 or y == 0 or x == self.w - 1 or y == self.h - 1:
                    tiles[y][x] = "#"
                else:
                    percent_chance = randint(0, 100)
                    if percent_chance <= 15:
                        tiles[y][x] = "^"
                    elif percent_chance > 95:
                        tiles[y][x] = "*"


        return tiles

    def display_grid(self, screen: window):
        """Display the grid on screen."""
        for y in range(self.h):
            for x in range(self.w):
                screen.addch(y, x, self.tiles[y][x])
        
        # Display the player
        screen.addch(self.player.y, self.player.x, "@")

    def display_ui(self, screen: window):
        screen.addstr(1, self.w + 5, f"NAME: {self.player.name}")
        screen.addstr(3, self.w + 5, f"HEALTH: {self.player.health}")
        screen.addstr(5, self.w + 5, f"MONEY: {self.player.money}")

    def handle_input(self, user_input):
        if user_input in "wasd":
            dir = {"w": "u", "a": "l", "s": "d", "d": "r"}[user_input]
            self.player.move(dir, self.tiles)


def play_game(screen: window):
    g = Grid()
    running = True
    while running and not g.player.dead:
        screen.clear()
        g.display_grid(screen)
        g.display_ui(screen)
        screen.refresh()
        user_input = screen.getkey() # Pause and wait for user input    

        # End the game
        if user_input == "q":
            running = False
        else:
            g.handle_input(user_input)

if __name__ == "__main__":

    curses.wrapper(play_game)
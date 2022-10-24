import pygame
import random

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


class Figure:  # definition of tetris pieces/tetrominoes
    x = 0
    y = 0
    # pieces are built by selecting 4 elements from this matrix
    # [0, 1, 2, 3]
    # [4, 5, 6, 7]
    # [8, 9,10,11]
    # [12,13,14,15]

    figures = [  # each row is a different tetris piece and its rotations
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # I-piece
        [[4, 5, 9, 10], [2, 6, 5, 9]],  # z-piece
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # s-piece
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # j-piece
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # l-piece
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # t-piece
        [[1, 2, 5, 6]],  # O-piece
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def reset(self):
        self.x = 3
        self.y = 0
        return self

    def rotate(self): # when rotate is called, find the next value on its row in figures
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

    def reverse_rotate(self):
        self.rotation = (self.rotation - 1) % len(self.figures[self.type])

class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None
    hold_field = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    hold_figure = None
    holdable = True
    hold_x = 5
    hold_y = 30
    hold_height = 4
    hold_width = 4

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        self.hold_figure = None #this defines what piece is being held, default is none
        self.holdable = True
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self): # spawns new piece at the top of the screen
        self.figure = Figure(3, 0)

    def intersects(self): #collision detection
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        self.holdable = True
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def reverse_rotate(self):
        old_rotation = self.figure.rotation
        self.figure.reverse_rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def hold(self):
        old_figure = self.figure
        if self.holdable:
            self.holdable = False
            if self.hold_figure == None:
                self.hold_figure = old_figure
                self.new_figure()
            else:
                self.figure = Figure.reset(self.hold_figure)
                self.hold_figure = old_figure
        else:
            return


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                game.rotate()
            if event.key == pygame.K_x:
                game.reverse_rotate()
            if event.key == pygame.K_UP:
                game.hold()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressing_down = False

    screen.fill(WHITE)

    for i in range(game.height): # draws playing area
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])


    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])
   # make sure this is all hold
    for i in range(game.hold_height): # draws playing area
        for j in range(game.hold_width):
            pygame.draw.rect(screen, GRAY, [game.hold_x + game.zoom * j, game.hold_y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.hold_field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.hold_x + game.zoom * j + 1, game.hold_y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.hold_figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.hold_figure.image():
                    pygame.draw.rect(screen, colors[game.hold_figure.color],
                                     [game.hold_x + game.zoom * (j) + 1,
                                      game.hold_y + game.zoom * (i) + 1,
                                      game.zoom - 2, game.zoom - 2])



    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
# view raw
# tetris.py hosted with ❤ by GitHub

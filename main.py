import pygame
from game import Game, X, O
from _thread import start_new_thread
from random import choice

pygame.font.init()

class Window:
    def __init__(self, size):
        self.size = size
        self.screen = pygame.display.set_mode(size)
        self.running = False
        self.playing = False
        self.game = Game()
        self.state = self.game.initial_state
        self.player_side = choice([X, O])
        self.player = X
        self.winner = 0
        self.font = pygame.font.SysFont("Arial", 32, True, False)
        self.fontbig = pygame.font.SysFont("Arial", 256, True, False)
    def draw(self):
        self.screen.fill((33, 88, 88))
        unit = min(self.size)//3
        origin = (self.size[0]//2-unit*3//2, self.size[1]//2-unit*3//2)
        for r in range(3):
            for c in range(3):
                letter = self.state[r][c]
                x = origin[0] + c*unit
                y = origin[1] + r*unit
                if letter == O or letter == X:
                    if letter == X: image = self.fontbig.render("X",False, (0, 0, 192))
                    if letter == O: image = self.fontbig.render("O",False, (192, 0, 0))
                    self.screen.blit(image, (x + unit//2 - image.get_width()//2, y + unit//2 - image.get_height()//2))
        pygame.draw.line(self.screen, (0, 0, 0), (origin[0] + unit//7, origin[1] + unit   ), (origin[0] + unit*20//7, origin[1] + unit     ), max(1, unit//16))
        pygame.draw.line(self.screen, (0, 0, 0), (origin[0] + unit//7, origin[1] + unit*2 ), (origin[0] + unit*20//7, origin[1] + unit*2   ), max(1, unit//16))
        pygame.draw.line(self.screen, (0, 0, 0), (origin[0] + unit   , origin[1] + unit//7), (origin[0] + unit     , origin[1] + unit*20//7), max(1, unit//16))
        pygame.draw.line(self.screen, (0, 0, 0), (origin[0] + unit*2 , origin[1] + unit//7), (origin[0] + unit*2   , origin[1] + unit*20//7), max(1, unit//16))
        if self.playing:
            if self.player != self.player_side:
                text = self.font.render("Opponent's turn...", False, (192, 192, 192))
                self.screen.blit(text, (self.size[0]//2 - text.get_width()//2, self.size[1]*90//100))
        else:
            if   self.winner == X:  text = self.font.render("X wins!", False, (192, 192, 192))
            elif self.winner == O:  text = self.font.render("O wins!", False, (192, 192, 192))
            else:                   text = self.font.render("No winner!", False, (192, 192, 192))
            self.screen.blit(text, (self.size[0]//2 - text.get_width()//2, self.size[1]*85//100))
            text = self.font.render("Click anywhere to start new game.", False, (192, 192, 192))
            self.screen.blit(text, (self.size[0]//2 - text.get_width()//2, self.size[1]*90//100))
        pygame.display.flip()
    def gameloop(self):
        self.state = self.game.initial_state
        clock = pygame.time.Clock()
        self.playing = True
        while self.running and self.playing:
            clock.tick(60)
            if self.game.terminal(self.state):
                self.winner = self.game.utility(self.state)
                self.playing = False
                continue
            self.actions = self.game.actions(self.state)
            self.player = self.game.player(self.state)
            if self.player != self.player_side:
                empty = 0
                for r in range(3):
                    for c in range(3):
                        if self.state[r][c] == 0:
                            empty += 1
                if empty == 9:
                    action = choice(self.actions)
                else:
                    action = self.game.best_action(self.state)
                if action in self.actions:
                    self.state = self.game.result(self.state, action)
                continue
            while self.running and self.playing and self.player == self.player_side:
                clock.tick(60)
                self.player = self.game.player(self.state)
    def mainloop(self):
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.playing:
                        if self.player == self.player_side:
                            unit = min(self.size)//3
                            origin = (self.size[0]//2-unit*3//2, self.size[1]//2-unit*3//2)
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            r = (mouse_y - origin[1]) // unit
                            c = (mouse_x - origin[0]) // unit
                            action = (r, c, self.player_side)
                            if action in self.actions:
                                self.state = self.game.result(self.state, action)
                    else:
                        self.state = [[0 for i in range(3)] for i in range(3)]
                        self.player_side = choice([X, O])
                        start_new_thread(self.gameloop,())
            self.draw()

if __name__ == "__main__":
    size = (1200, 800)
    window = Window(size)
    window.mainloop()
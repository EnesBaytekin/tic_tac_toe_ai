from random import choice

X = 1
O = -1

class Game:
    def __init__(self):
        self.initial_state = [[0 for j in range(3)] for i in range(3)]
    def draw(self, state):
        for line in state:
            for value in line:
                char = "_"
                if value == X: char = "X"
                if value == O: char = "O"
                print(char, end=" ")
            print()
    def player(self, state):
        x = 0
        o = 0
        for line in state:
            for char in line:
                if   char == X: x += 1
                elif char == O: o += 1
        if o == x:  return X
        else:       return O
    def actions(self, state):
        actions = []
        player = self.player(state)
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    actions.append( (r, c, player) )
        return actions
    def result(self, state, action):
        r, c, player = action
        result = [[state[r][c] for c in range(3)] for r in range(3)]
        result[r][c] = player
        return result
    def terminal(self, state):
        rows = state
        columns = [[state[r][c] for r in range(3)] for c in range(3)]
        diagonals = [[state[i][i] for i in range(3)], [state[2-i][i] for i in range(3)]]
        for line in rows+columns+diagonals:
            if len(list(set(line))) == 1:
                if line[0] != 0:
                    return True
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    return False
        return True
    def utility(self, state):
        rows = state
        columns = [[state[r][c] for r in range(3)] for c in range(3)]
        diagonals = [[state[i][i] for i in range(3)], [state[2-i][i] for i in range(3)]]
        for line in rows+columns+diagonals:
            if len(list(set(line))) == 1:
                if line[0] == X: return X
                if line[0] == O: return O
        return 0
    def max_value(self, state):
        terminal = self.terminal(state)
        if terminal:
            return self.utility(state)
        v = -10
        for action in self.actions(state):
            value = self.min_value(self.result(state, action))
            if value > v:
                v = value
        return v
    def min_value(self, state):
        terminal = self.terminal(state)
        if terminal:
            return self.utility(state)
        v = 10
        for action in self.actions(state):
            value = self.max_value(self.result(state, action))
            if value < v:
                v = value
        return v
    def best_action(self, state):
        pairs = []
        if self.player(state) == X:
            for action in self.actions(state):
                value = self.min_value(self.result(state, action))
                pairs.append( (action, value) )
            sorted_pairs = sorted(pairs, key=lambda pair: pair[1])
            best_value = sorted_pairs[-1][1]
        else:
            for action in self.actions(state):
                value = self.max_value(self.result(state, action))
                pairs.append( (action, value) )
            sorted_pairs = sorted(pairs, key=lambda pair: pair[1])
            best_value = sorted_pairs[0][1]
        bests = [pair for pair in sorted_pairs if pair[1] == best_value]
        action = choice(bests)[0]
        return action

def main():
    from os import system
    game = Game()
    state = game.initial_state
    system("cls")
    letter = input("choose letter (x, o): ")
    if   letter.lower() == "x": letter = X
    elif letter.lower() == "o": letter = O
    system("cls")
    game.draw(state)
    running = True
    while running:
        actions = game.actions(state)
        player = game.player(state)
        if player == letter:
            try:
                r = int(input("row   : "))
                c = int(input("column: "))
            except:
                system("cls")
                game.draw(state)
                continue
            action = (r, c, player)
        else:
            action = game.best_action(state)
        if action in actions:
            state = game.result(state, action)
        system("cls")
        game.draw(state)
        if game.terminal(state):
            winner = game.utility(state)
            print()
            if   winner == X:   print("X wins!")
            elif winner == O:   print("O wins!")
            else:               print("No winner!")
            running = False

if __name__ == "__main__":
    main()
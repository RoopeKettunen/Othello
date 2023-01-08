
import random


class RandomBot:
    def __init__(self):
        self.white = "O"
        self.black = "@"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None

    def best_strategy(self, board, color):
        # returns best move
        self.x_max = len(board)
        self.y_max = len(board[0])
        if color == "#000000":
            color = "@"
        else:
            color = "O"
        all = self.find_moves(board, color)
        index = random.randint(0, len(all) -1)
        ''' Your code goes here '''
        best_move = all[index]  # change this
        return best_move, 0

    def stones_left(self, board):
        count = 0
        for x in range(0,8):
            for y in range(0,8):
                if board[x][y] == ".":
                    count += 1
        # returns number of stones that can still be placed (empty spots)
        return count

    def find_moves(self, board, color):
        moves_found = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                flipped_stones = self.find_flipped(board, i, j, color)
                if len(flipped_stones) > 0:
                    moves_found.append([i, j])
        return moves_found

    def find_flipped(self, board, x, y, color):
        if board[x][y] != ".":
            return []
        flipped_stones = []
        for incr in self.directions:
            temp_flip = []
            x_pos = x + incr[0]
            y_pos = y + incr[1]
            while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                if board[x_pos][y_pos] == ".":
                    break
                if board[x_pos][y_pos] == color:
                    flipped_stones += temp_flip
                    break
                temp_flip.append([x_pos, y_pos])
                x_pos += incr[0]
                y_pos += incr[1]
        return flipped_stones


class Best_AI_bot:

    def __init__(self):
        self.white = "O"
        self.black = "@"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None

    def best_strategy(self, board, color):
        self.x_max = len(board)
        self.y_max = len(board[0])
        if color == "#000000":
            color = "@"
        else:
            color = "O"
        print(board)

        count = 0
        for x in range(0, 8):
            for y in range(0, 8):
                if board[x][y] != ".":
                    count += 1
        if color == self.black:
            if count > 50:
                ret = self.alphabeta(board, color, 7, -10000, 10000, [0, 0])
                print(ret)
                best_move = ret[1]
            else:
                ret = self.alphabeta(board, color, 5, -10000, 10000, [0, 0])
                print(ret)
                best_move = ret[1]
        else:
            if count > 50:
                ret = self.alphabeta(board, color, 6, -10000, 10000, [0, 0])
                print(ret)
                best_move = ret[1]
            else:
                ret = self.alphabeta(board, color, 4, -10000, 10000, [0, 0])
                print(ret)
                best_move = ret[1]

        return best_move, 0

    def minimax(self, board, color, search_depth, move):
        l = self.find_moves(board, color)
        if search_depth == 0 or len(l) == 0:
            return self.evaluate(board, color, l), move
        if color == self.black:
            children = []
            for e in l:
                children.append(self.make_move(board, color, e, self.find_flipped(board, e[0], e[1], color)))
            vals = []
            for c in children:
                color = self.opposite_color[color]
                vals.append(self.minimax(c, color, search_depth - 1, l[children.index(c)])[0])
            max = -100
            i = 0
            for x in range(0, len(vals)):
                if vals[x] > max:
                    max = vals[x]
                    i = x

            return max, l[i]

        else:
            children = []
            for e in l:
                children.append(self.make_move(board, color, e, self.find_flipped(board, e[0], e[1], color)))
            vals = []
            for c in children:
                color = self.opposite_color[color]
                vals.append(self.minimax(c, color, search_depth - 1, l[children.index(c)])[0])
            min = 100
            i = 0
            for x in range(0, len(vals)):
                if vals[x] < min:
                    min = vals[x]
                    i = x

            return min, l[i]


    def negamax(self, board, color, search_depth):
        # returns best "value"
        return 1

    def alphabeta(self, board, color, search_depth, alpha, beta, move):
        l = self.find_moves(board, color)
        if search_depth == 0 or len(l) == 0:
            return self.evaluate(board, color, l), move
        children = []
        for e in l:
            children.append(self.make_move(board, color, e, self.find_flipped(board, e[0], e[1], color)))
        if color == self.black:
            vals = []
            val = -1000
            for c in children:
                tick = self.alphabeta(c, self.opposite_color[color], search_depth-1, alpha,beta, l[children.index(c)])[0]
                vals.append(tick)
                chunk = -10000
                i = 0
                for x in range(0, len(vals)):
                    if vals[x] > chunk:
                        chunk = vals[x]
                        i = x
                val = max(val, tick)
                alpha = max(alpha, val)
                if alpha >= beta:
                    break
            return val, l[i]

        else:
            vals = []
            val = 1000
            for c in children:
                tick = self.alphabeta(c, self.opposite_color[color], search_depth-1, alpha,beta, l[children.index(c)])[0]
                vals.append(tick)
                chink = 10000
                i = 0
                for x in range(0, len(vals)):
                    if vals[x] < chink:
                        chink = vals[x]
                        i = x
                val = min(val, tick)
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return val, l[i]
    def make_key(self, board, color):
        # hashes the board
        return 1

    def stones_left(self, board):
        # returns number of stones that can still be placed
        return 1

    def make_move(self, board, color, move, flipped):
        nb = []
        for x in range(0, 8):
            nb.append([])
            for y in range(0, 8):
                nb[x].append(board[x][y])

        nb[move[0]][move[1]] = color
        for a in flipped:
            nb[a[0]][a[1]] = color
        return nb

    def evaluate(self, board, color, possible_moves):
        oc = self.opposite_color[color]
        counts = [0, 0]
        for x in range(0, 8):
            for y in range(0, 8):
                if board[x][y] == oc:
                    if (x ==0 and y==0) or (x ==0 and y== 7) or (x == 7 and y ==0) or (x ==7 and y ==7):

                        counts[0] += 10
                    elif x == 0 or x == 7 or y == 0 or y == 7:
                        counts[0] += 1
                elif board[x][y] == color:
                    if (x ==0 and y==0) or (x ==0 and y== 7) or (x == 7 and y ==0) or (x ==7 and y ==7):
                        counts[1] += 10
                    elif x == 0 or x == 7 or y == 0 or y == 7:
                        counts[1] += 1
        heuristic =  counts[0] - counts[1]
        return heuristic


    def score(self, board, color):
        # returns the score of the board
        return 1

    def find_moves(self, board, color):
        moves_found = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                flipped_stones = self.find_flipped(board, i, j, color)
                if len(flipped_stones) > 0:
                    moves_found.append([i, j])
        return moves_found

    def find_flipped(self, board, x, y, color):
        if board[x][y] != ".":
            return []
        flipped_stones = []
        for incr in self.directions:
            temp_flip = []
            x_pos = x + incr[0]
            y_pos = y + incr[1]
            while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                if board[x_pos][y_pos] == ".":
                    break
                if board[x_pos][y_pos] == color:
                    flipped_stones += temp_flip
                    break
                temp_flip.append([x_pos, y_pos])
                x_pos += incr[0]
                y_pos += incr[1]
        return flipped_stones
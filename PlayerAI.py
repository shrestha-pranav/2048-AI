from random import randint
from BaseAI import BaseAI
import op
import time
import heuristic as hr

# s -> current state
# a, b -> alpha, beta
# d -> recursion depth
class PlayerAI(BaseAI):
    def __init__(self):
        self.nodes_expanded = 0

    def getMove(self, grid):
        self.time = time.clock()

        for i in range(4):
            for j in range(4):
                grid.map[i][j] = op.log_mod[grid.map[i][j]]
        x = op.bitify_grid_int(grid.map)
        self.transtable = {}
        

        (move, _) = self.maximize(x, -float('inf'), float('inf'))
        print self.nodes_expanded, self.reason, 
        self.nodes_expanded = 0
        return move

    def chance(self, s, a, b, d):
        self.nodes_expanded += 1
        return 0.1 * self.minimize(2, s, a, b, d) + \
                0.9 * self.minimize(1, s, a, b, d)

    def minimize(self, new_val, s, a, b, d=0):
        self.nodes_expanded += 1
        cells = op.getAvailableCells(s)

        if d >= 4 or (time.clock() - self.time >= 0.1):
            self.reason = "Stack limit" if d>=4 else "Time limit"
            # r = op.get_rows(s)
            return hr.score_heur_board(s)

        minUtility = float('inf')
        for cell in cells:
            child = op.set_cell(s, cell[0], cell[1], new_val)
            (_, utility) = self.maximize(child, a, b, d)

            if utility < minUtility: minUtility = utility
            if minUtility <= a: break
            if minUtility < b: b = minUtility
        return minUtility

    def maximize(self, s, a, b, d=0):
        self.nodes_expanded += 1
        moves = op.getAvailableMoves(s)

        if not moves: return (None, -100000000000)
        (maxMove, maxUtility) = (None, -float('inf'))
        for move in moves:
            child = op.move_grid(s, move)

            utility = self.chance(child, a, b, d+1)
            if utility > maxUtility: (maxMove, maxUtility) = (move, utility)
            if maxUtility >= b: break
            if maxUtility > a: a = maxUtility
        return (maxMove, maxUtility)

    def __del__(self):
        print self.nodes_expanded
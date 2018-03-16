from random import randint
from BaseAI import BaseAI
import op
import time
import heuristic as hr

# s -> current state
# a, b -> alpha, beta
# d -> recursion depth
class PlayerAI(BaseAI):
    def getMove(self, grid):
        self.time = time.clock()

        # for i in range(4):
        #     for j in range(4):
        #         grid.map[i][j] = min(15, op.log_mod[grid.map[i][j]])
        # x = op.bitify_grid_int(grid.map)
        x = grid

        self.max_depth = 2
        prev_move = None
        while True:
            self.max_depth += 1
            (move, _) = self.maximize(x, -float('inf'), float('inf'))
            if time.clock()-self.time < 0.18:
                prev_move = move
            elif prev_move is not None:
                return prev_move
            else:
                from random import randint
                moves = op.getAvailableMoves(grid)
                return moves[randint(0, len(moves)-1)]

    def chance(self, s, a, b, d):
        if time.clock()-self.time>=0.18: return 0
        return 0.1*self.minimize(2,s,a,b,d)+ 0.9*self.minimize(1,s,a,b,d)

    def minimize(self, new_val, s, a, b, d=0):
        if d>=self.max_depth: return hr.score_heur_board(s)

        cells = op.getAvailableCells(s)
        minUtility = float('inf')
        for cell in cells:
            child = op.set_cell(s, cell[0], cell[1], new_val)
            (_, utility) = self.maximize(child, a, b, d)

            if utility < minUtility: minUtility = utility
            if minUtility <= a: break
            if minUtility < b: b = minUtility
        return minUtility

    def maximize(self, s, a, b, d=0):
        if time.clock()-self.time>=0.18: return (None, 0)
        moves = op.getAvailableMoves(s)

        if not moves: return (None, -16283176000)
        (maxMove, maxUtility) = (None, -float('inf'))
        for move in moves:
            child = op.move_grid(s, move)

            utility = self.chance(child, a, b, d+1)
            if utility > maxUtility: (maxMove, maxUtility) = (move, utility)
            if maxUtility >= b: break
            if maxUtility > a: a = maxUtility
        return (maxMove, maxUtility)
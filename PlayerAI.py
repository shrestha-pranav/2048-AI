from BaseAI import BaseAI
from random import randint
import op
import time
import heuristic as hr

# s -> current state
# a, b -> alpha, beta
# d -> recursion depth
# p -> probability
class PlayerAI(BaseAI):
    def getMove(self, grid):
        self.time = time.clock()

        # Convert grid to a single 64-bit integer
        for i in range(4):
            for j in range(4):
                grid.map[i][j] = min(15, op.log_mod[grid.map[i][j]])
        x = op.bitify_grid(grid.map)


        #Implementing a IDS to hopefully save time
        prev_move = None
        self.max_depth = 2
        while True:
            self.max_depth += 1
            (move, _) = self.maximize(x, -float('inf'), float('inf'), 0, 0)
            if time.clock()-self.time < 0.18:
                prev_move = move
            elif prev_move is not None:
                return prev_move
            else:
                moves = op.getAvailableMoves(x)
                return moves[randint(0, len(moves)-1)]

    def chance(self, s, a, b, d, p):
        if time.clock()-self.time>=0.18: return 0

        # Unlikely getting more than three 4's in a row
        if p==3: return self.minimize(1,s,a,b,d,p)
        return 0.1*self.minimize(2,s,a,b,d,p+1)+ 0.9*self.minimize(1,s,a,b,d,p)

    def minimize(self, new_val, s, a, b, d, p):
        if d>=self.max_depth: return hr.eval(s)

        minUtility = float('inf')
        r = op.get_rows(s)
        for x in range(4):
            for y in op.empty_tiles[r[x]]:
                child = op.set_cell(s, x, y, new_val)
                (_, utility) = self.maximize(child, a, b, d, p)

                if utility < minUtility: minUtility = utility
                if minUtility <= a: break
                if minUtility < b: b = minUtility
        return minUtility

    def maximize(self, s, a, b, d, p):
        if time.clock()-self.time>=0.18: return (None, 0)
        
        moves = op.getAvailableMoves(s)
        if not moves: return (None, -16283176000)

        (maxMove, maxUtility) = (None, -float('inf'))
        for move in moves:
            child = op.move_grid(s, move)

            utility = self.chance(child, a, b, d+1, p)
            if utility > maxUtility: (maxMove, maxUtility) = (move, utility)
            if maxUtility >= b: break
            if maxUtility > a: a = maxUtility
        return (maxMove, maxUtility)
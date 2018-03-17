from Grid       import Grid
from PlayerAI   import PlayerAI
from Displayer  import Displayer
from random     import randint
import time
import op

class GameManager:
    def __init__(self, log):
        self.log = log
        self.grid = 0
        self.displayer = Displayer()
        self.playerAI  = PlayerAI()

    def maxTile(self):
        return max([op.max_tiles[(self.grid>>(16*i))&0xffff] for i in range(4)])

    def getTile(self):
        return 1 if randint(0,99)<90 else 2
    
    def insertRandomTile(self):
        x1, x2, y1, y2 = randint(0,3), randint(0,3), randint(0,3), randint(0,3)
        while x1==x2 and y1==y2: x2, y2 = randint(0,3), randint(0,3)

        g = op.set_cell(self.grid, x1, y1, self.getTile())
        return op.set_cell(self.grid, x2, y2, self.getTile())

    def start(self):
        self.grid = self.insertRandomTile()

        # Player AI Goes First
        turn  = 0
        count = 0

        while op.getAvailableMoves(self.grid):
            move = None

            if turn:
                move = self.playerAI.getMove(self.grid)
                if move == None: break
                self.grid = op.move_grid(self.grid, move)

            else:
                cells = op.getAvailableCells(self.grid)
                cell  = cells[randint(0, len(cells) - 1)] if cells else None
                
                self.grid = op.set_cell(self.grid, cell[0], cell[1], self.getTile())

            turn = 1 - turn
            count += 1
            self.displayer.display(self.grid)

        print self.log, op.debitify_grid(self.grid), self.maxTile()
        return (self.log, op.debitify_grid(self.grid), self.maxTile())

def main():
    gameManager = GameManager("g1")
    gameManager.start()

if __name__ == '__main__':
    main()

from BaseDisplayer import BaseDisplayer
import platform
import os
import op
from Grid import Grid

colorMap = {
    0     : 97 ,
    2     : 40 ,
    4     : 100,
    8     : 47 ,
    16    : 107,
    32    : 46 ,
    64    : 106,
    128   : 44 ,
    256   : 104,
    512   : 42 ,
    1024  : 102,
    2048  : 43 ,
    4096  : 103,
    8192  : 45 ,
    16384 : 105,
    32768 : 41 ,
    65536 : 101,
}

listMap =  colorMap.items() + [(op.log_mod[k],v) for (k,v) in colorMap.items() if op.log_mod[k] not in colorMap]
colorMap = {k:v for (k,v) in listMap}

cTemp = "\x1b[%dm%7s\x1b[0m "

class Displayer(BaseDisplayer):
    def __init__(self):
        if "Windows" == platform.system():
            self.display = self.winDisplay
        else:
            self.display = self.unixDisplay

    def display(self, grid):
        pass

    def winDisplay(self, grid):
        for i in xrange(grid.size):
            for j in xrange(grid.size):
                print "%6d  " % grid.map[i][j],
            print ""
        print ""

    def unixDisplay(self, grid):
        for i in xrange(3 * 4):
            for j in xrange(4):
                if isinstance(grid, Grid):
                    v = grid.map[i / 3][j]
                else:
                    v = op.get_cell(grid, i/3, j)

                if i % 3 == 1:
                    string = str(v).center(7, " ")
                else:
                    string = " "

                print cTemp %  (colorMap[v], string),
            print ""

            if i % 3 == 2:
                print ""

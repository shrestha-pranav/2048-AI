import math
import op

heuristics  = [0] * 2**16 # Pre-calculate eval for every row
corners     = [0] * 2**16

# Evaluation function sums over every row and column
eval  = lambda g: eval2(g) + eval2(op.transpose(g)) + 100 * corn(g)
eval2 = lambda g: sum([heuristics[(g>>16*i)&0xffff] for i in [0,1,2,3]])
corn  = lambda g: max(corners[g>>48], corners[g%(2**16)]) # Bonus for corner tile

# Monotonicity and max tile bonus settings
maxwts     = [0]*10 + [3.3, 10.0, 33.3, 100.0, 333.3, 1000.0]
mono_wts   = [[i**4-j**4 if i>j else 0 for i in range(20)] for j in range(20)]


# Pre-compute heuristics to save time
for i in range(65536):
    r = op.debitify_row(i)

    # Count number of empty tiles
    empty = (r[0]==0) + (r[1]==0) + (r[2]==0) + (r[3]==0)

    # Count the number of merges
    merges = prev = 0
    for j in range(4):
        if r[j] == 0: continue
        merges, prev = merges+(prev==r[j]), r[j]

    # Algorithm for monotonicity. Selects the lowest monotonicity
    mono_left = mono_right = 0.0
    for j in [1,2,3]:
        mono_left  += mono_wts[r[j-1]][r[j]]
        mono_right += mono_wts[r[j]][r[j-1]]
    monot = mono_left if mono_left < mono_right else mono_right

    # Bonuses for getting 1024+ tiles
    maxTiles = maxwts[r[0]]+maxwts[r[1]]+maxwts[r[2]]+maxwts[r[3]]

    corners[i] = max(r[0], r[3]) # Corners
    heuristics[i] = 300000 + 250*empty + 700*merges - 50*monot + 1000*maxTiles
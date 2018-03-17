import math 
import op

heuristics  = [0] * 2**16
eval  = lambda g: eval2(g) + eval2(op.transpose(g))
eval2 = lambda g: sum([heuristics[(g>>16*i)&0xffff] for i in [0,1,2,3]])

LOST_PENALTY = 200000.0
MERGES_WEIGHT = 700.0
EMPTY_WEIGHT = 270.0

# Monotonicity settings
MON_POWER = 4.0
MON_WEIGHT = 47.0
mono = [i**4.0 for i in range(20)]

# SUM_POWER = 3.5
# SUM_WEIGHT = 11.0
# MAX_WEIGHT = 11.0
# powsum = [i**SUM_POWER for i in range(20)]
# maxwts = [0]*10 + [i**3.5 for i in range(10,20)]
MAX_WEIGHT = 1000.0
maxwts = [0]*10 + [3.3, 10.0, 33.3, 100.0, 333.3, 1000.0] 

for i in range(65536):
    r = op.debitify_row(i)

    # total = powsum[r[0]] + powsum[r[1]] + powsum[r[2]] + powsum[r[3]]
    # Count number of empty tiles
    empty = (r[0]==0)+(r[1]==0)+(r[2]==0)+(r[3]==0)

    merges = prev = 0
    if r[0] != 0: prev = r[0]
    if r[1] != 0: merges, prev = merges+(prev==r[1]), r[1]
    if r[2] != 0: merges, prev = merges+(prev==r[2]), r[2]
    if r[3] != 0: merges, prev = merges+(prev==r[3]), r[3]

    # Algorithm for monotonicity. Selects the lowest monotonicity
    mon_left = mon_right = 0.0
    for j in [1,2,3]:
        if r[j-1] > r[j]: mon_left += mono[r[j-1]] - mono[r[j]]
        else: mon_right+= mono[r[j]] - mono[r[j-1]]
    monotonicity = mon_left if mon_left < mon_right else mon_right

    maxTiles = maxwts[r[0]]+maxwts[r[1]]+maxwts[r[2]]+maxwts[r[3]]

    heuristics[i] = LOST_PENALTY + EMPTY_WEIGHT*empty + MERGES_WEIGHT*merges - \
        MON_WEIGHT*monotonicity + maxTiles * MAX_WEIGHT #+ SUM_WEIGHT*total 


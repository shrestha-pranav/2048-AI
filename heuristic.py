import math 
import op

heuristics  = [0] * 2**16
log = [0] * 2**16

LOST_PENALTY = 200000.0
MON_WEIGHT = 47.0
SUM_WEIGHT = 11.0
MERGES_WEIGHT = 700.0
EMPTY_WEIGHT = 270.0

MON_POWER = 4.0
SUM_POWER = 3.5
monpow = [i**MON_POWER for i in range(20)]
powsum = [i**SUM_POWER for i in range(20)]

for i in range(65536):
    r = op.debitify_row(i)

    total = powsum[r[0]] + powsum[r[1]] + powsum[r[2]] + powsum[r[3]]
    empty = (r[0]==0)+(r[1]==0)+(r[2]==0)+(r[3]==0)

    merges = prev = 0
    if r[0] != 0: prev = r[0]
    if r[1] != 0: (merges, prev) = (merges+(prev==r[1]), r[1])
    if r[2] != 0: (merges, prev) = (merges+(prev==r[2]), r[2])
    if r[3] != 0: (merges, prev) = (merges+(prev==r[3]), r[3])

    mon_left = mon_right = 0.0
    for j in [1,2,3]:
        if r[j-1] > r[j]: mon_left += monpow[r[j-1]] - monpow[r[j]]
        else: mon_right+= monpow[r[j]] - monpow[r[j-1]]

    monotonicity = mon_left if mon_left < mon_right else mon_right

    log[i] = [LOST_PENALTY, EMPTY_WEIGHT*empty, MERGES_WEIGHT*merges, -MON_WEIGHT*monotonicity, SUM_WEIGHT*total]
    heuristics[i] = LOST_PENALTY + EMPTY_WEIGHT*empty + MERGES_WEIGHT*merges - \
        MON_WEIGHT*monotonicity + SUM_WEIGHT*total

score_helper = lambda g: sum([heuristics[(g>>16*i)&0xffff] for i in range(4)])
score_heur_board = lambda g: score_helper(g) + score_helper(op.transpose(g))
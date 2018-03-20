import math

# Constant time lookups
modlog  = [0] + [2**i for i in range(1,20)]
log_mod = {modlog[i]:i for i in range(20)}
index   = [[60-16*i-4*j for j in range(4)] for i in range(4)]

# Converts rows from and to 16-bit integers
bitify_row    = lambda r:  r[3]|r[2]<<4|r[1]<<8|r[0]<<12
debitify_row  = lambda r: [(r>>12)&0xF, (r>>8)&0xF, (r>>4)&0xF, r&0xF]

# Convert grid from and to 64-bit integers
bitify_grid   = lambda g: sum([(bitify_row(g[3-i])<<16*i) for i in range(4)])
debitify_grid = lambda g: [debitify_row(r) for r in get_rows(g)]

# Returns or sets g[i][j] 
get_cell = lambda g,i,j: (g>>index[i][j])%16
set_cell = lambda g,i,j,v: (g&~(15<<index[i][j])) | (v<<index[i][j])

# Returns rows or cols as 16-bit integers
get_rows = lambda g: [(g>>16*3), (g>>16*2)%(2**16), (g>>16)%(2**16), g%(2**16)]
get_cols = lambda g: get_rows(transpose(g))

# Transposes a 4x4 grid using bit-shift operations
diag = genMask([0,5,10,15])
a1, a2 = (genMask([1,6,11]), genMask([4,9,14]))
b1, b2 = (genMask([2,7]), genMask([8,13]))
c1, c2 = (genMask([3]), genMask([12]))

genMask = lambda positions: sum([0xF<<(4*pos) for pos in positions])
transpose = lambda g: g&diag|(g&a1)<<12|(g&a2)>>12| \
                        (g&b1)<<24|(g&b2)>>24|(g&c1)<<36|(g&c2)>>36

# Move 4-cells to the left and right
def move(cells):
    lefts , li = [0,0,0,0], 0
    rights, ri = [0,0,0,0], 3
    prev = 0
    for i in [0,1,2,3]:
        if prev==0: prev = cells[i]
        elif prev==cells[i]:
            lefts[li] = prev+1
            prev, li  = 0, li+1
        else:
            lefts[li] = prev
            prev, li  = cells[i], li+1
    if prev != 0 : lefts[li] = prev

    prev=0
    for i in [3,2,1,0]:
        if prev==0:
            prev = cells[i]
        elif prev==cells[i]:
            rights[ri], prev, ri = prev+1, 0, ri-1
        else:
            rights[ri], prev, ri = prev, cells[i], ri-1
    if prev !=0 : rights[ri] = prev

    left, right = False, False
    for i in range(4):
        if cells[i] != lefts[i] : left = lefts
        if cells[i] != rights[i]: right = rights
    return left, right


# Generate constant-time lookups for row optimization
map_left        = [0]*2**16
map_right       = [0]*2**16
map_exist_left  = [False]*2**16
map_exist_right = [False]*2**16

for g in range(65536):
    row = debitify_row(g)
    rev_row = [row[3], row[2], row[1], row[0]]

    tmp1, tmp2 = move(row)
    map_exist_left[g]  = (tmp1 is not False)
    map_exist_right[g] = (tmp2 is not False)

    map_left[g]  = bitify_row(tmp1) if map_exist_left[g] else g
    map_right[g] = bitify_row(tmp2) if map_exist_right[g] else g

def getAvailableMoves(g):
    r, c = get_rows(g), get_cols(g)
    moves = [False, False, False, False]
    for i in range(4):
        if map_exist_left[c[i]]:  moves[0] = True
        if map_exist_right[c[i]]: moves[1] = True
        if map_exist_left[r[i]]:  moves[2] = True
        if map_exist_right[r[i]]: moves[3] = True
    return [i for i in range(4) if moves[i]]

def getAvailableCells(g):
    r = get_rows(g)
    cells = []
    for i in range(4):
        for j in empty_tiles[r[i]]: cells.append((i,j))
    return cells

def move_grid(g, move):
    if move < 2: 
        return transpose(move_grid(transpose(g), move+2))

    m = map_right if move==3 else map_left
    r = get_rows(g)
    
    return (m[r[0]]<<48) + (m[r[1]]<<32) + (m[r[2]]<<16) + (m[r[3]])
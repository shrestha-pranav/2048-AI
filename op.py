import math

# Constant time lookups
modlog  = [0] + [2**i for i in range(1,20)]
log_mod = {modlog[i]:i for i in range(20)}
index   = [[60-16*i-4*j for j in range(4)] for i in range(4)]

# Converts 4 elements into 16-bit integer
bitify_row      = lambda row:  sum([(row[3-i]<<4*i) for i in range(4)])
bitify_grid_int = lambda grid: sum([(bitify_row(grid[3-i])<<16*i) for i in range(4)])

# Convert 16-bit integer to 4 elements
debitify_row  = lambda r: [(r>>12)&0xf, (r>>8)&0xf, (r>>4)&0xf, r&0xf]
debitify_grid = lambda g: [debitify_row(r) for r in get_rows(g)]

# returns or sets g[i][j] 
get_cell = lambda g,i,j: (g>>index[i][j])%16
set_cell = lambda g,i,j,v: (g&~(15<<index[i][j])) | (v<<index[i][j])

# returns rows or cols as 16-bit integers
get_rows = lambda g: [(g>>16*3), (g>>16*2)%(2**16), (g>>16)%(2**16), g%(2**16)]
get_cols = lambda g: get_rows(transpose(g))

# Bit-shift convert rows to columns
def transpose(g):
    tmasks = [0xF0F00F0FF0F00F0F, 0x0000F0F00000F0F0, 0x0F0F00000F0F0000]
    a = [g&tmasks[i] for i in range(3)]
    a = a[0] | (a[1]<<12) | (a[2]>>12)
    tmasks = [0xFF00FF0000FF00FF, 0x00FF00FF00000000, 0x00000000FF00FF00]
    b = [a&tmasks[i] for i in range(3)]
    return b[0] | (b[1]>>24) | (b[2]<<24)

# Move 4-cells to the left and right
def move(cells):
    i = 0
    vals = [cells[i] for i in [0,1,2,3] if cells[i] != 0]
    if len(vals) > 1:
        i = 0
        while i < len(vals) - 1:
            if vals[i] == vals[i+1]:
                vals[i] += 1
                del vals[i+1]
            i += 1

    lefts = [vals[i] if i<len(vals) else 0 for i in range(4)]

    vals = [cells[i] for i in [3,2,1,0] if cells[i] != 0]
    if len(vals)>1:
        i=0
        while i<len(vals) - 1:
            if vals[i] == vals[i+1]:
                vals[i] += 1
                del vals[i+1]
            i += 1
    right = [vals[i] if i<len(vals) else 0 for i in range(4)]
    right = [right[3], right[2], right[1], right[0]]

    left_exist, right_exist = False, False
    for i in range(4):
        if cells[i] != lefts[i]: left_exist = lefts
        if cells[i] != right[i]: right_exist = right
    return left_exist, right_exist


# Generate constant-time lookups for row optimization
map_left        = [0]*2**16
map_right       = [0]*2**16
map_exist_left  = [False]*2**16
map_exist_right = [False]*2**16
sort_tiles      = [0]*2**16
empty_tiles     = [0]*2**16
max_tiles       = [0]*2**16

for g in range(65536):
    row = debitify_row(g)
    rev_row = [row[3], row[2], row[1], row[0]]

    tmp1, tmp2 = move(row)
    map_exist_left[g]  = (tmp1 is not False)
    map_exist_right[g] = (tmp2 is not False)

    map_left[g]  = bitify_row(tmp1) if map_exist_left[g] else g
    map_right[g] = bitify_row(tmp2) if map_exist_right[g] else bitify_row(rev_row)

    sort_tiles[g]  = bitify_row(sorted(row, reverse=True))
    empty_tiles[g] = [i for i in range(4) if row[i]==0] #sum([row[i]==0 for i in range(4)])

    max_tiles[g] = max(row)

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
    c = get_cols(g) if move<2 else get_rows(g)
    m = map_left if move%2==0 else map_right

    res = (m[c[0]]<<48) + (m[c[1]]<<32) + (m[c[2]]<<16) + (m[c[3]])
    if move<2: res = transpose(res) 
    return res
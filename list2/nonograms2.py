import random

def create_nonogram_info(x, y, row_patterns, col_patterns):
    board = [random.getrandbits(y) for _ in range(x)]

    cols = [0] * y
    for i in range(x):
        for j in range(y):
            if board[i] & (1 << (y - 1 - j)):
                cols[j] |= (1 << (x - 1 - i))

    rows_to_fix = [opt_changes(board[i], row_patterns[i]) for i in range(x)]
    cols_to_fix = [opt_changes(cols[j], col_patterns[j]) for j in range(y)]

    return board, cols, rows_to_fix, cols_to_fix

def opt_changes(sequence, patterns):
    return min((sequence ^ p).bit_count() for p in patterns)

def generate_patterns(length, blocks):
    if not blocks or blocks == [0]:
        return [0]
 
    result = []
 
    def backtrack(start, idx, current):
        if idx == len(blocks):
            result.append(current)
            return
 
        block = blocks[idx]
        min_space = sum(blocks[idx:]) + (len(blocks) - idx - 1)
 
        for pos in range(start, length - min_space + 1):
            block_bits = ((1 << block) - 1) << (length - pos - block)
            backtrack(pos + block + 1, idx + 1, current | block_bits)
 
    backtrack(0, 0, 0)
    return result
    
def fix_col(board, cols, col_idx, row_patterns, col_patterns, x, y):
    best = float('inf')
    candidates = []

    for i in range(x):
        row_mask = 1 << (y - 1 - col_idx)
        col_mask = 1 << (x - 1 - i)

        new_row = board[i] ^ row_mask
        new_col = cols[col_idx] ^ col_mask

        score = (
            opt_changes(new_row, row_patterns[i]) +
            opt_changes(new_col, col_patterns[col_idx])
        )

        if score < best:
            best = score
            candidates = [i]
        elif score == best:
            candidates.append(i)

    return random.choice(candidates)

def fix_row(board, cols, row_idx, row_patterns, col_patterns, x, y):
    best = float('inf')
    candidates = []

    for j in range(y):
        row_mask = 1 << (y - 1 - j)
        col_mask = 1 << (x - 1 - row_idx)

        new_row = board[row_idx] ^ row_mask
        new_col = cols[j] ^ col_mask

        score = (
            opt_changes(new_row, row_patterns[row_idx]) +
            opt_changes(new_col, col_patterns[j])
        )

        if score < best:
            best = score
            candidates = [j]
        elif score == best:
            candidates.append(j)

    return random.choice(candidates)


def solver(data):
    x, y = (int(a) for a in data[0].split())

    rows = [list(map(int, line.split())) for line in data[1:x+1]]
    cols_desc = [list(map(int, line.split())) for line in data[x+1:x+y+1]]

    row_patterns = [generate_patterns(y, rows[i]) for i in range(x)]
    col_patterns = [generate_patterns(x, cols_desc[j]) for j in range(y)]

    board, cols, rows_to_fix, cols_to_fix = create_nonogram_info(
        x, y, row_patterns, col_patterns
    )

    iters = max(2048, x * y * 100)
    p_random = 0.1

    while sum(rows_to_fix) + sum(cols_to_fix) != 0:

        if iters < 1:
            board, cols, rows_to_fix, cols_to_fix = create_nonogram_info(
                x, y, row_patterns, col_patterns
            )
            iters = max(2048, x * y * 100)

        iters -= 1

        change_columns = random.randint(0, 1)

        if change_columns:
            bad_cols = [j for j in range(y) if cols_to_fix[j] > 0]
            if not bad_cols:
                continue

            col_idx = random.choice(bad_cols)

            if random.random() < p_random:
                row_idx = random.randrange(x)
            else:
                row_idx = fix_col(board, cols, col_idx, row_patterns, col_patterns, x, y)

        else:
            bad_rows = [i for i in range(x) if rows_to_fix[i] > 0]
            if not bad_rows:
                continue

            row_idx = random.choice(bad_rows)

            if random.random() < p_random:
                col_idx = random.randrange(y)
            else:
                col_idx = fix_row(board, cols, row_idx, row_patterns, col_patterns, x, y)

        row_mask = 1 << (y - 1 - col_idx)
        col_mask = 1 << (x - 1 - row_idx)

        board[row_idx] ^= row_mask
        cols[col_idx] ^= col_mask

        rows_to_fix[row_idx] = opt_changes(board[row_idx], row_patterns[row_idx])
        cols_to_fix[col_idx] = opt_changes(cols[col_idx], col_patterns[col_idx])

    return board, x, y

def main():
    data  =  open("zad_input.txt").read().split("\n")
    result,x , y = solver(data)
    mapping = {0: '.', 1: '#'}

    with open("zad_output.txt","w") as file:
        for row in result:
            bits = format(row, f'0{y}b')
            file.write(''.join('#' if b == '1' else '.' for b in bits))
            file.write('\n')
        file.close()
    
if __name__ == "__main__":
    main()
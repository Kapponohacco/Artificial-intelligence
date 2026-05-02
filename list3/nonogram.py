import random


def create_nonogram_info(x, y):
    rows = [0] * x
    cols = [0] * y
    rows_final = [0] * x
    cols_final = [0] * y

    return rows, rows_final, cols, cols_final


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

def trim_patterns(patterns, final, value):
    trimmed = [p for p in patterns if (p ^ value) & final == 0]
    return trimmed

def row_inference(x, y, rows, rows_final, cols, cols_final, row_patterns, col_patterns):
    changed = False
    for row_idx in range(x):
        patterns = row_patterns[row_idx]
 
        # Empty pattern list means this branch is a contradiction
        if not patterns:
            return rows, rows_final, cols, cols_final, col_patterns, changed, True
 
        common_ones  =  patterns[0] & ~rows_final[row_idx]
        common_zeros = ~patterns[0] & ~rows_final[row_idx]
 
        for p in patterns[1:]:
            common_ones  &= p
            common_zeros &= ~p
 
        for col_idx in range(y):
            mask = 1 << (y - 1 - col_idx)
            bit  = 1 << (x - 1 - row_idx)
 
            if common_ones & mask:
                changed = True
                rows_final[row_idx] |= mask
                rows[row_idx]       |= mask
                cols_final[col_idx] |= bit
                cols[col_idx]       |= bit
 
            elif common_zeros & mask:
                changed = True
                rows_final[row_idx] |= mask
                rows[row_idx]       &= ~mask
                cols_final[col_idx] |= bit
                cols[col_idx]       &= ~bit
 
    for col_idx in range(y):
        col_patterns[col_idx] = trim_patterns(
            col_patterns[col_idx], cols_final[col_idx], cols[col_idx]
        )
        if not col_patterns[col_idx]:
            return rows, rows_final, cols, cols_final, col_patterns, changed, True
 
    return rows, rows_final, cols, cols_final, col_patterns, changed, False
 
def col_inference(x, y, rows, rows_final, cols, cols_final, row_patterns, col_patterns):
    changed = False
    for col_idx in range(y):
        patterns = col_patterns[col_idx]
 
        # Empty pattern list means this branch is a contradiction
        if not patterns:
            return rows, rows_final, cols, cols_final, row_patterns, changed, True
 
        common_ones  =  patterns[0] & ~cols_final[col_idx]
        common_zeros = ~patterns[0] & ~cols_final[col_idx]
 
        for p in patterns[1:]:
            common_ones  &= p
            common_zeros &= ~p
 
        for row_idx in range(x):
            mask = 1 << (x - 1 - row_idx)
            bit  = 1 << (y - 1 - col_idx)
 
            if common_ones & mask:
                changed = True
                cols[col_idx]       |= mask
                cols_final[col_idx] |= mask
                rows[row_idx]       |= bit
                rows_final[row_idx] |= bit
 
            elif common_zeros & mask:
                changed = True
                cols[col_idx]       &= ~mask
                cols_final[col_idx] |= mask
                rows[row_idx]       &= ~bit
                rows_final[row_idx] |= bit
 
    for row_idx in range(x):
        row_patterns[row_idx] = trim_patterns(
            row_patterns[row_idx], rows_final[row_idx], rows[row_idx]
        )
        if not row_patterns[row_idx]:
            return rows, rows_final, cols, cols_final, row_patterns, changed, True
 
    return rows, rows_final, cols, cols_final, row_patterns, changed, False

def evaluate_pattern(x, y, row_idx, pattern, cols_patterns):
    score = 0

    for col_idx in range(y):
        bit = (pattern >> (y - 1 - col_idx)) & 1

        possible = 0
        for cp in cols_patterns[col_idx]:
            col_bit = (cp >> (x - 1 - row_idx)) & 1
            if col_bit == bit:
                possible += 1

        score += possible

    return score

def solve_backtrack(x, y, rows, rows_final, cols, cols_final, row_patterns, col_patterns):

    changed = True
    while changed:
        rows, rows_final, cols, cols_final, col_patterns, changed_row, invalid = row_inference(x,y,rows,rows_final,cols,cols_final,row_patterns,col_patterns)
        if invalid:
            return None
        rows, rows_final, cols, cols_final, row_patterns, changed_col, invalid = col_inference(x,y,rows,rows_final,cols,cols_final,row_patterns,col_patterns)
        if invalid:
            return None
        changed = changed_col | changed_row
    
    if all(r == (1 << y) - 1 for r in rows_final):
        return rows
    
    chosen_idx = None 
    min_patterns = float("inf")
    for row_idx in range(x):
        if len(row_patterns[row_idx]) < min_patterns and len(row_patterns[row_idx]) > 1:
            chosen_idx = row_idx
            min_patterns = len(row_patterns[row_idx])
    
    if chosen_idx is None:
        return None

    patterns = row_patterns[chosen_idx]
    scored_patterns = [
        (evaluate_pattern(x, y, chosen_idx, p, col_patterns), p)
        for p in patterns
    ]
    scored_patterns.sort(reverse = True)

    for _, pattern in scored_patterns:
        new_rows = rows.copy()
        new_rows_final = rows_final.copy()
        new_cols = cols.copy()
        new_cols_final = cols_final.copy()
        new_row_patterns = [p.copy() for p in row_patterns]
        new_col_patterns = [p.copy() for p in col_patterns]

        new_rows[chosen_idx] = pattern
        new_rows_final[chosen_idx] = (1 << y) - 1
        new_row_patterns[chosen_idx] = [pattern]

        valid = True
        for col_idx in range(y):
            bit = (pattern >> (y - 1 - col_idx)) & 1
            mask = 1 << (x - 1 - chosen_idx)

            if bit:
                new_cols[col_idx] |= mask
            else:
                new_cols[col_idx] &= ~mask

            new_cols_final[col_idx] |= mask

            new_col_patterns[col_idx] = trim_patterns(
                new_col_patterns[col_idx],
                new_cols_final[col_idx],
                new_cols[col_idx]
            )

            if not new_col_patterns[col_idx]:
                valid = False
                break

        if not valid:
            continue

        result = solve_backtrack(
            x, y,
            new_rows, new_rows_final,
            new_cols, new_cols_final,
            new_row_patterns, new_col_patterns
        )

        if result:
            return result

    return None

def solver(data):
    x, y = (int(a) for a in data[0].split())

    rows_desc = [list(map(int, line.split())) for line in data[1:x+1]]
    cols_desc = [list(map(int, line.split())) for line in data[x+1:x+y+1]]

    row_patterns = [generate_patterns(y, rows_desc[i]) for i in range(x)]
    col_patterns = [generate_patterns(x, cols_desc[j]) for j in range(y)]

    rows, rows_final, cols, cols_final = create_nonogram_info(
        x, y
    )

    result =  solve_backtrack(x, y, rows, rows_final, cols, cols_final, row_patterns, col_patterns)

    return result ,x, y

        
            

def main():
    data  =  open("zad_input.txt").read().split("\n")
    result, x, y = solver(data)
    with open("zad_output.txt","w") as file:
        for row in result:
            bits = format(row, f'0{y}b')
            file.write(''.join('#' if b == '1' else '.' for b in bits))
            file.write('\n')
        file.close()
    
if __name__ == "__main__":
    main()
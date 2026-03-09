import numpy as np

def create_nonogram_info(x,y,rows,cols):
    nonogram = np.random.randint(2, size = (x,y))
    rows_to_fix = [opt_changes(nonogram[i],rows[i]) for i in range(x)]
    cols_to_fix = [opt_changes(nonogram[:,i],cols[i]) for i in range(y)]

    return nonogram,rows_to_fix,cols_to_fix

def opt_changes(sequence: np.ndarray, dist):
    current = np.count_nonzero(sequence[:dist])
    counter = current
    opt = current
    for i in range(1,len(sequence) - dist+1):
        current = current - sequence[i-1] + sequence[i+dist-1]
        counter += sequence[i+dist-1]
        if current > opt:
            opt = current

    return dist - opt + counter - opt

def fix_col(nonogram, idx,rows,cols):
    cand = 0 
    best_score = float('inf')

    for i in range(len(nonogram[:,idx])):
        nonogram[i,idx] ^= 1
        score = opt_changes(nonogram[i], rows[i]) + opt_changes(nonogram[:,idx],cols[idx])
        if score < best_score:
            cand = i
            best_score = score
        nonogram[i,idx] ^= 1

    return cand

def fix_row(nonogram, idx,rows,cols):
    cand = 0 
    best_score = float('inf')

    for i in range(len(nonogram[idx])):
        nonogram[idx,i] ^= 1
        score = opt_changes(nonogram[idx], rows[idx]) + opt_changes(nonogram[:,i],cols[i])
        if score < best_score:
            cand = i
            best_score = score
        nonogram[idx,i] ^= 1

    return cand

def solver(data):
    x,y = int(data[0]),int(data[1])
    rows = [int(num) for num in data[2:x+2]]
    cols = [int(num) for num in data[x+2:y+x+2]]
    nonogram, rows_to_fix, cols_to_fix = create_nonogram_info(x,y,rows,cols)
    
    iters = 150
    while (sum(rows_to_fix) + sum(cols_to_fix)) != 0:
        if iters < 1:
            nonogram, rows_to_fix, cols_to_fix = create_nonogram_info(x,y,rows,cols)
            iters = 150

        change_columns = np.random.randint(2)
        if change_columns:
            col_idx = np.random.randint(y)
            if cols_to_fix[col_idx] == 0:
                continue
            row_idx = fix_col(nonogram,col_idx,rows,cols)
        else:
            row_idx = np.random.randint(x)
            if rows_to_fix[row_idx] ==  0:
                continue
            col_idx = fix_row(nonogram,row_idx,rows,cols)
        nonogram[row_idx,col_idx] ^= 1
        rows_to_fix[row_idx] = opt_changes(nonogram[row_idx],rows[row_idx])
        cols_to_fix[col_idx] = opt_changes(nonogram[:,col_idx],cols[col_idx])

    return nonogram


def main():
    data  =  open("zad5_input.txt").read().split()
    result = solver(data)
    mapping = {0: '.', 1: '#'}

    with open("zad5_output.txt","w") as file:
        for line in result:
            for character in line:
                file.write(mapping[character])
            file.write('\n')
        file.close()
    
if __name__ == "__main__":
    main()
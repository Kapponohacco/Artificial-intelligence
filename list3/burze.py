import sys
import os

def B(i,j):
    return 'B_%d_%d' % (i,j)

def storms(rows, cols, triples, out):
    R = len(rows)
    C = len(cols)
    variables = [B(i,j) for i in range(R) for j in range(C)]

    print(':- use_module(library(clpfd)).', file=out)
    print('solve([' + ', '.join(variables) + ']) :- ', file=out)

    cs = []

    
    for v in variables:
        cs.append('%s in 0..1' % v)# Dziedzina: każda komórka to 0 lub 1

    for i in range(R):
        row_vars = [B(i,j) for j in range(C)]
        cs.append('sum([' + ', '.join(row_vars) + '], #=, %d)' % rows[i])# Sumy wierszy

    
    for j in range(C):
        col_vars = [B(i,j) for i in range(R)]
        cs.append('sum([' + ', '.join(col_vars) + '], #=, %d)' % cols[j])# Sumy kolumn

    #Każda komórka '1' musi mieć co najmniej jednego sąsiada pionowego i poziomego
    # (Zapewnia to wymiar min. 2x2 dla prostokątów)
    for i in range(R):
        for j in range(C):
            v_neighbors = []
            if i > 0:   v_neighbors.append(B(i-1,j))
            if i < R-1: v_neighbors.append(B(i+1,j))
            
            h_neighbors = []
            if j > 0:   h_neighbors.append(B(i,j-1))
            if j < C-1: h_neighbors.append(B(i,j+1))

            if v_neighbors:
                cs.append(r'%s #=< %s' % (B(i,j), ' + '.join(v_neighbors)))
            else:
                cs.append('%s #= 0' % B(i,j))

            if h_neighbors:
                cs.append(r'%s #=< %s' % (B(i,j), ' + '.join(h_neighbors)))
            else:
                cs.append('%s #= 0' % B(i,j))

    # Ograniczenia podsiatki 2x2 (Prostokątność i brak stykania się rogami)
    for i in range(R-1):
        for j in range(C-1):
            a, b, c, d = B(i,j), B(i,j+1), B(i+1,j), B(i+1,j+1)
            # 1. Brak kształtu L
            cs.append(r'%s + %s + %s + %s #\= 3' % (a, b, c, d))
            # 2. Brak połączeń po przekątnej
            cs.append(r'%s + %s #=< %s + %s + 1' % (a, d, b, c))
            cs.append(r'%s + %s #=< %s + %s + 1' % (b, c, a, d))

    # Pola z polecenia 
    for r, c, val in triples:
        cs.append('%s #= %d' % (B(r, c), val))

    for constraint in cs:
        print('    ' + constraint + ',', file=out)

    print('    labeling([ff], [' + ', '.join(variables) + ']).', file=out)
    print(file=out)
    print(':- solve(X), write(X), nl, halt.', file=out)

def parse_input(lines):
    if not lines:
        return [], [], []
    rows = list(map(int, lines[0].split()))
    cols = list(map(int, lines[1].split()))
    triples = []
    for line in lines[2:]:
        if line.strip():
            triples.append(list(map(int, line.split())))
    return rows, cols, triples

if __name__ == "__main__":
    input_path = 'zad_input.txt'
    output_path = 'zad_output.txt'

    if os.path.exists(input_path):
        with open(input_path, 'r') as f_in:
            r, c, t = parse_input(f_in.readlines())
        with open(output_path, 'w') as f_out:
            storms(r, c, t, f_out)
    else:
        r, c, t = parse_input(sys.stdin.readlines())
        storms(r, c, t, sys.stdout)
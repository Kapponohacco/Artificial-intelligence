import sys
import os


def V(i,j):
    return 'V%d_%d' % (i,j)
    
def domains(Vs):
    return [ q + ' in 1..9' for q in Vs ]
    
def all_different(Qs):
    return 'all_distinct([' + ', '.join(Qs) + '])'
    
def get_column(j):
    return [V(i,j) for i in range(9)] 
            
def get_row(i):
    return [V(i,j) for j in range(9)] 

def get_box(bi, bj):
    return [V(bi*3 + i, bj*3 + j) for i in range(3) for j in range(3)]
 
def horizontal():   
    return [all_different(get_row(i)) for i in range(9)]

def vertical():
    return [all_different(get_column(j)) for j in range(9)]

def boxes():
    return [all_different(get_box(bi, bj)) for bi in range(3) for bj in range(3)]


def print_constraints(Cs, indent, d, out):
    position = indent
    print (indent * ' ', end='', file=out)
    for c in Cs:
        print (c + ',', end=' ', file=out)
        position += len(c)
        if position > d:
            position = indent
            print (file=out)
            print (indent * ' ', end='', file=out)

      
def sudoku(assigments, out):
    variables = [ V(i,j) for i in range(9) for j in range(9)]
    
    print (':- use_module(library(clpfd)).', file=out)
    print ('solve([' + ', '.join(variables) + ']) :- ', file=out)
    
    
    cs = domains(variables) + vertical() + horizontal() + boxes() #TODO: did something! :) (added box constraints)
    for i,j,val in assigments:
        cs.append( '%s #= %d' % (V(i,j), val) )
    
    print_constraints(cs, 4, 70, out)
    print (file=out)
    print ('    labeling([ff], [' +  ', '.join(variables) + ']).', file=out)
    print (file=out)
    print (':- solve(X), write(X), nl.', file=out)


def parse_input_lines(lines):
    row = 0
    triples = []
    for x in lines:
        x = x.strip()
        if len(x) == 9:
            for i in range(9):
                if x[i] != '.':
                    triples.append((row, i, int(x[i])))
            row += 1
            if row == 9:
                break
    return triples

if __name__ == "__main__":
    input_path = 'zad_input.txt'
    output_path = 'zad_output.txt'

    use_file_io = os.path.exists(input_path)

    if use_file_io:
        with open(input_path, 'r') as f_in:
            triples = parse_input_lines(f_in)
        with open(output_path, 'w') as f_out:
            sudoku(triples, f_out)
    else:
        triples = parse_input_lines(sys.stdin)
        sudoku(triples, sys.stdout)
    
"""
89.356.1.
3...1.49.
....2985.
9.7.6432.
.........
.6389.1.4
.3298....
.78.4....
.5.637.48

53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79

3.......1
4..386...
.....1.4.
6.924..3.
..3......
......719
........6
2.7...3..
"""    

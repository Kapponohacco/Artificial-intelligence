from queue import Queue
from collections import deque

'''
Zadanie 1
Sprawdzamy BFS-em wszytkie możliwe pozycje. 
Z kazdego board-state'u generujemy wszystkie inne mozliwe board-state po 1 ruchu, i sprawdzamy
czy dane ustawienie było już kiedyś sprawdzane, nastepnie wszystkie mozliwe ruchy wrzycamy do kolejki.
Przy okazji zapisujemy które ruchy powstały z których stateów, żeby móc je potem odtworzyć.
'''

MAPPING = {
    'a': '1',
    'b': '2',
    'c': '3',
    'd': '4',
    'e': '5',
    'f': '6',
    'g': '7',
    'h': '8'
}

def generate_moves(move):
    # tura, biały król, biała wieża, czrny król
    if move[0] == 'black':
        return move_black(move[1:])
    if move[0] == 'white':
        return move_white(move[1:])

def valid_move(moved_piece, other_pieces):
    if (moved_piece % 10 == 0 or
    moved_piece % 10 == 9 or
    moved_piece // 10 == 0 or
    moved_piece // 10 == 9 or
    moved_piece in other_pieces):
        return False
    return True

def kings_close(king, other_piece):
    for i in range(-1,2):
        for j in range(-1,2):
            if king + i * 10 + j == other_piece:
                return True
    return False

def black_king_in_check(moved_black_king, white_king, white_rook):
    #kolumna
    if moved_black_king % 10 == white_rook % 10:
        step = 10 if moved_black_king > white_rook else -10
    #wiersz
    elif moved_black_king // 10 == white_rook // 10:
        step = 1 if moved_black_king > white_rook else -1
    else:
        return False

    current = white_rook + step
    while current != moved_black_king:
        if current == white_king:
            return False
        current += step

    return True

def move_black(board):#bialy krol, biala wieza, czrny krol
    moves = [] 
    wk, wr, bk = board

    for i in range(-1,2):
        for j in range(-1,2):
            if i != 0 or j != 0:
                nbk = bk + i*10 + j

                if (valid_move(nbk,[wk,wr]) and not
                black_king_in_check(nbk,wk,wr) and not
                kings_close(nbk,wk)):
                    
                    new_move = ('white',wk,wr,nbk)
                    moves.append(new_move)
    return moves

def move_white(board):
    moves = [] 
    wk, wr, bk = board
    for i in range(-1,2):
        for j in range(-1,2):
            if i != 0 or j != 0:
                nwk = wk + i*10 + j

                if (valid_move(nwk,[bk, wr]) and not
                    kings_close(nwk,bk)):

                    new_move = ('black',nwk,wr,bk)
                    moves.append(new_move)

    directions = [1, -1, 10, -10]  #prawy,lewy,gora,dol

    for d in directions:
        nwr = wr
        while True:
            nwr += d

            if not valid_move(nwr, [wk, bk]):
                break

            if kings_close(wk,nwr) or not kings_close(bk,nwr):
                new_move = ('black', wk, nwr, bk)
                moves.append(new_move)

    return moves

def calculate_number_of_moves(move: list):
    global VISITED
    VISITED = set()
    parent = {}

    queue = Queue()
    base = tuple(move)

    queue.put(base)
    VISITED.add(base)
    parent[base] = None

    while not queue.empty():
        current = queue.get()

        turn, wk, wr, bk = current

        possible_moves = generate_moves(current)

        if (turn == 'black' and
            possible_moves == [] and
            black_king_in_check(bk, wk, wr)):

            path = deque()
            node = current
            while node is not None:
                path.append(node)
                node = parent[node]

            return 0, path

        for new_move in possible_moves:
            if new_move not in VISITED:
                VISITED.add(new_move)
                parent[new_move] = current
                queue.put(new_move)

    return 1, deque()


def main():
    move = open("zad1_input.txt").read().split()

    for enum, position in enumerate(move[1:]):
        move[enum+1] = int(MAPPING[position[0]] + position[1])

    control,res = calculate_number_of_moves(move)
    
    debug = 0
    if control == 1:
        ans = 'INF'
    else:
        ans = 0
        while (len(res) != 0):
            move = res.pop()
            if debug:
                print(move)
            ans+=1
        ans = str(ans-1) #the first board state is not counted as a move
    with open("zad1_output.txt", "w") as output:
        output.write(ans)
        output.close()

if __name__ == "__main__":
    main()
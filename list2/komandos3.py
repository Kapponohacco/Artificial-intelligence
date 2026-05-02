from queue import PriorityQueue
import math
from collections import deque
import itertools

def precompute_distances(end, empty):
    q = deque()
    dists = {}
    for goal in end:
        q.append((goal, 0))
        dists[goal] = 0
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        curr, dist = q.popleft()
        for x, y in dirs:
            new_row, new_col = curr[0] + x, curr[1] + y
            if (new_row, new_col) in empty and (new_row, new_col) not in dists:
                dists[(new_row, new_col)] = dist + 1
                q.append(((new_row, new_col), dist + 1))
    return dists

def calculate_heuristic(state, exact_dists):
    max_dist = 0
    for k in state:
        d = exact_dists[k]
        if d > max_dist:
            max_dist = d
    return max_dist
    
def move_state(state, x, y, empty):
    new_state = set()
    for row, col in state:
        new_row, new_col = row + x, col + y

        if (new_row, new_col) in empty:
            new_state.add((new_row, new_col))
        else:
            new_state.add((row, col))

    return frozenset(new_state)

def solve():

    try:
        with open("zad_input.txt") as f:
            grid = f.readlines()
    except FileNotFoundError:
        print("Nie udalo sie otworzyc pliku zad_input.txt")
        return

    if not grid:
        return

    grid = [list(line.strip('\n')) for line in grid if line.strip('\n')]

    start = set()
    end = set()
    empty = set()

    len_row = len(grid)
    len_col = len(grid[0])

    for row in range (len_row):
        for col in range(len_col):
            pos = (row,col)
            if grid[row][col] != '#':
                empty.add(pos)
            if grid[row][col] in ('S','B'):
                start.add(pos)
            if grid[row][col] in ('G','B'):
                end.add(pos)

    dirs = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    heuristic_weight = 1.15
    exact_dists = precompute_distances(end, empty)

    current_state = frozenset(start)
    phase1_moves = ""
    target_k = 4 #poziom "niepewności" tolerowany przez BFS
    visited = {current_state}

    while len(current_state) > target_k:
        q = deque([(current_state, "")])
        visited.add(current_state)
        found_reduction = False
        
        while q:
            state, path = q.popleft()

            for m_name, (x, y) in dirs.items():
                n_state = move_state(state, x, y, empty)
                if n_state not in visited:
                    if len(n_state) < len(current_state):
                        phase1_moves += path + m_name
                        current_state = n_state
                        found_reduction = True
                        break
                    visited.add(n_state)
                    q.append((n_state, path + m_name))
                
            if found_reduction:
                break
                
        if not found_reduction:
            break

    queue = PriorityQueue()
    counter = itertools.count() #w momencie gdy wartosc heury jest taka sama,potrzebujemy rozstrzygniecia, aby priorityqueue nie porownywalo frozensetów
    initial_heur = heuristic_weight * calculate_heuristic(current_state, exact_dists)
    queue.put((0 + initial_heur, next(counter), current_state, phase1_moves))
    visited = {current_state}
    
    while not queue.empty():
        f_cost, _, state, path = queue.get()

        if all(p in end for p in state):
            print(len(path))
            with open('zad_output.txt', 'w') as f:
                f.write(path)
            return
        
        for m_name, (x, y) in dirs.items():
            new_state = move_state(state, x, y, empty)
            if new_state not in visited:
                visited.add(new_state)
                new_path = path + m_name
                f_n = len(new_path) + heuristic_weight * calculate_heuristic(new_state, exact_dists)
                queue.put((f_n, next(counter), new_state, new_path))
                
    print("Brak rozwiazania")

if __name__ == '__main__':
    solve()
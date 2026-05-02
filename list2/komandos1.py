from collections import deque

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
        with open('zad_input.txt') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Nie udalo sie otworzyc pliku zad_input.txt")
        return

    grid = [list(line.strip('\n')) for line in lines if line.strip('\n')]
    if not grid:
        return

    starts = set()
    goals = set()
    empty = set()
    
    len_rows = len(grid)
    len_cols = len(grid[0])
    
    for r in range(len_rows):
        for c in range(len_cols):
            char = grid[r][c]
            pos = (r, c)
            if char != '#':
                empty.add(pos)
            if char in ('S', 'B'):
                starts.add(pos)
            if char in ('G', 'B'):
                goals.add(pos)

    dirs = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    #Faza 1
    current_state = frozenset(starts)
    phase1_moves = ""
    target_k = 2 #poziom "niepewności" tolerowany przez BFS
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

    #faza 2
    q = deque([(current_state, phase1_moves)])
    visited = {current_state}
    
    while q:
        state, path = q.popleft()
        
        if all(p in goals for p in state):
            with open('zad_output.txt', 'w') as f:
                f.write(path)
            return
            
        if len(path) >= 150:
            continue
            
        for m_name, (dr, dc) in dirs.items():
            n_state = move_state(state, dr, dc, empty)
            if n_state not in visited:
                visited.add(n_state)
                q.append((n_state, path + m_name))
                
    print("Brak rozwiazania")

if __name__ == '__main__':
    solve()

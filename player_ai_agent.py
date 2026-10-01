from typing import List, Tuple, Any

def play(board: List[List[int]], choices: List[int], player: int, memory: Any) -> Tuple[int, Any]:
    
    opponent = 1 - player
    n_cols = len(board)
    n_rows = n_cols
    target = 4 if n_cols > 6 else 3
    

    # Build grid (rows x cols) with -1 = empty
    grid = [[-1] * n_cols for _ in range(n_rows)]
    heights = [len(col) for col in board]
    
    for c in range(n_cols):
        for r, val in enumerate(board[c]):
            grid[n_rows - 1 - r][c] = val

    legal_choices = [c for c in choices if heights[c] < n_rows]
    move = None
    return choose_move_with_strategy(grid, legal_choices, heights, player,opponent, n_rows, n_cols, target, memory)

def choose_move_with_strategy(grid, legal_choices, heights, player, opponent, n_rows, n_cols, target, memory):
    # check if I win
    move,memory = find_winning_move(grid, legal_choices, heights, player, n_rows, n_cols, target, memory)
    if move is not None:
        return move, memory
        
    # Block opponent's winning move
    move,memory = find_blocking_move(grid, legal_choices, heights, opponent, n_rows, n_cols, target, memory)
    if move is not None:
        return move, memory
  
    # 3. Create a double threat?
    move = find_double_threat_move(grid, legal_choices, heights, player, n_rows, n_cols, target)
    if move is not None:
        return move, memory
    
    # Best move to maximize my sequence
    return choose_best_move(grid, legal_choices, heights, player, opponent, n_rows, n_cols, target), memory
    
def choose_best_move(grid, legal_choices, heights, player, opponent, n_rows, n_cols, target):
    best_move = legal_choices[0]
    best_score = -1

    for col in legal_choices:
        row = n_rows - 1 - heights[col]
        
        # Skip if this move lets opponent win immediately
        if _move_allows_opponent_win(grid, col, player, opponent, heights, n_rows, n_cols, target):
            continue
            
        score = _get_max_sequence(grid, row, col, player, n_rows, n_cols)
        if score > best_score:
            best_score = score
            best_move = col

    return best_move
    
def find_winning_move(grid, legal_choices, heights, player, n_rows, n_cols, target, memory=None):
    for col in legal_choices:
        row = n_rows - 1 - heights[col]
        if _check_win(grid, row, col, player, n_rows, n_cols, target): 
            return col, memory
    return None, memory
        
def find_blocking_move(grid, legal_choices, heights, opponent, n_rows, n_cols, target, memory=None):
    for col in legal_choices:
        row = n_rows - 1 - heights[col]
        if row < 0:
            continue
        if _check_win(grid, row, col, opponent, n_rows, n_cols, target):
            return col, memory
    return None, memory

def _check_win(grid, row, col, player, n_rows, n_cols, target):
    if grid[row][col] != -1:
        return False

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1  # Count the hypothetical move at (row, col)

        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < n_rows and 0 <= c < n_cols and grid[r][c] == player:
            count += 1
            r += dr
            c += dc

        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < n_rows and 0 <= c < n_cols and grid[r][c] == player:
            count += 1
            r -= dr
            c -= dc

        if count >= target:
            return True

    return False

def _get_max_sequence(grid, row, col, player, n_rows, n_cols):
    if grid[row][col] != -1:
        return 0
        
    max_count = 0
    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        count = 1
        for sign in (1, -1):
            r, c = row + sign * dr, col + sign * dc
            while 0 <= r < n_rows and 0 <= c < n_cols and grid[r][c] == player:
                count += 1
                r += sign * dr
                c += sign * dc
        max_count = max(max_count, count)
    return max_count
def _move_allows_opponent_win(grid, col, player, opponent, heights, n_rows, n_cols, target):
    # Make a copy of the grid
    temp_grid = [row[:] for row in grid]
    
    # Place your piece
    my_row = n_rows - 1 - heights[col]
    if my_row < 0:
        return False
    temp_grid[my_row][col] = player

    # Check if opponent can win in any column
    for opp_col in range(n_cols):
        if heights[opp_col] >= n_rows:
            continue
            
        # Compute opponent's row after your move
        if opp_col == col:
            opp_row = my_row - 1
        else:
            opp_row = n_rows - 1 - heights[opp_col]
            
        if opp_row < 0:
            continue

        # Check if opponent wins by playing here
        if _check_win(temp_grid, opp_row, opp_col, opponent, n_rows, n_cols, target):
            return True

    return False
def _count_winning_moves(grid, legal_choices, heights, player, n_rows, n_cols, target):
    count = 0
    for col in legal_choices:
        row = n_rows - 1 - heights[col]
        if row >= 0 and _check_win(grid, row, col, player, n_rows, n_cols, target):
            count += 1
    return count

def find_double_threat_move(grid, legal_choices, heights, player, n_rows, n_cols, target):
    for col in legal_choices:
        # Simulate playing in col
        temp_grid = [row[:] for row in grid]
        row = n_rows - 1 - heights[col]
        if row < 0:
            continue
        temp_grid[row][col] = player

        # Compute new heights
        new_heights = heights[:]
        new_heights[col] += 1

        # Find legal choices for next turn (after this move)
        next_legal = [c for c in range(n_cols) if new_heights[c] < n_rows]

        # Count how many winning moves YOU would have next turn
        win_count = _count_winning_moves(
            temp_grid, next_legal, new_heights, player, n_rows, n_cols, target
        )

        if win_count >= 2:
            return col  # Double threat found!

    return None
# main.py
import curses
import time
import random

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]]  # T
]

WIDTH = 10
HEIGHT = 20

def draw_board(stdscr, board, score):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Score: {score}")
    for y, row in enumerate(board):
        stdscr.addstr(y + 1, 0, "|" + "".join("[]" if cell else "  " for cell in row) + "|")
    stdscr.addstr(HEIGHT + 1, 0, "+" + "--" * WIDTH + "+")
    stdscr.refresh()

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

def check_collision(board, shape, offset):
    ox, oy = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + ox < 0 or x + ox >= WIDTH or y + oy >= HEIGHT or board[y + oy][x + ox]:
                    return True
    return False

def merge(board, shape, offset):
    ox, oy = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[y + oy][x + ox] = 1

def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    cleared = HEIGHT - len(new_board)
    return [[0]*WIDTH for _ in range(cleared)] + new_board, cleared

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(200)

    board = [[0]*WIDTH for _ in range(HEIGHT)]
    shape = random.choice(SHAPES)
    offset = [WIDTH // 2 - len(shape[0]) // 2, 0]
    score = 0

    while True:
        draw_board(stdscr, board, score)
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_LEFT:
            offset[0] -= 1
            if check_collision(board, shape, offset): offset[0] += 1
        elif key == curses.KEY_RIGHT:
            offset[0] += 1
            if check_collision(board, shape, offset): offset[0] -= 1
        elif key == curses.KEY_DOWN:
            offset[1] += 1
            if check_collision(board, shape, offset): offset[1] -= 1
        elif key == ord('w'):
            new_shape = rotate(shape)
            if not check_collision(board, new_shape, offset): shape = new_shape

        # gravity
        offset[1] += 1
        if check_collision(board, shape, offset):
            offset[1] -= 1
            merge(board, shape, offset)
            board, cleared = clear_lines(board)
            score += cleared * 100
            shape = random.choice(SHAPES)
            offset = [WIDTH // 2 - len(shape[0]) // 2, 0]
            if check_collision(board, shape, offset):
                stdscr.addstr(HEIGHT // 2, 0, "GAME OVER")
                stdscr.refresh()
                time.sleep(2)
                break

curses.wrapper(main)

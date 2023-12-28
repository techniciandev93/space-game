import time
import asyncio
import curses
import random
from itertools import cycle

from fire_animation import fire


SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""

    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            # https://docs.python.org/3/library/curses.html#curses.window.getch
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


def get_frame_size(text):
    """Calculate size of multiline text fragment, return pair — number of rows and colums."""

    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


def draw(canvas, tic_timeout, frame1, frame2):
    coord_y, coord_x = canvas.getmaxyx()

    simbols = ['+', '*', '.', ':', "'"]

    coroutines = []
    canvas.border()
    canvas.nodelay(True)
    for y in range(1, coord_y):
        for x in range(
                random.randint(1, 4),
                coord_x - 1,
                random.randint(3, int((coord_x - 1) * 0.3))
        ):
            simbol = random.choice(simbols)
            coroutines.append(blink(canvas, y, x, simbol))

    coroutines.append(fire(canvas, coord_y//2, coord_x//2+2))

    animate_spaceship_iterator = cycle([frame1, frame2])
    coroutines.append(animate_spaceship(animate_spaceship_iterator, canvas, coord_y//2, coord_x//2, coord_y, coord_x))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
                canvas.refresh()
                curses.curs_set(False)
            except StopIteration:
                coroutines.remove(coroutine)
        time.sleep(tic_timeout)


async def blink(canvas, row, column, symbol='*'):
    random_sleep = random.randint(1, 3)
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for i in range(4 * random_sleep):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(3 * random_sleep):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for i in range(5 * random_sleep):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(2 * random_sleep):
            await asyncio.sleep(0)


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas, erase text instead of drawing if negative=True is specified."""

    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            # Check that current position it is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


async def animate_spaceship(animate_spaceship_iterator, canvas, row, column, max_coord_y, max_coord_x):
    while True:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)

        frame = next(animate_spaceship_iterator)
        frame_rows, frame_columns = get_frame_size(frame)

        new_row = row + rows_direction
        new_column = column + columns_direction

        if 0 < new_row < max_coord_y - frame_rows:
            row = new_row

        if 0 < new_column < max_coord_x - frame_columns:
            column = new_column

        draw_frame(canvas, row, column, frame)
        canvas.refresh()
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)


def read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


if __name__ == '__main__':
    rocket_frame_path_1 = 'animation_frames/rocket_frame_1.txt'
    rocket_frame_path_2 = 'animation_frames/rocket_frame_2.txt'
    rocket_frame_one = read_file(rocket_frame_path_1)
    rocket_frame_two = read_file(rocket_frame_path_2)

    tic_timeout = 0.1
    curses.update_lines_cols()
    curses.wrapper(draw, tic_timeout, rocket_frame_one, rocket_frame_two)

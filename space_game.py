import time
import curses
import random
from itertools import cycle
from os import listdir
from os.path import isfile, join

from fly_garbage_animation import fill_orbit_with_garbage
from game_scenario import display_year, increase_year
from spaceship_animation import animate_spaceship
from stars_animation import blink


def draw(canvas, tic_timeout, frame1, frame2, garbage_frames):
    coord_y, coord_x = canvas.getmaxyx()
    spaceship_y = coord_y // 2
    spaceship_x = coord_x // 2

    initial_character_spacing = 1
    end_character_spacing = 4
    max_x = coord_x - 1
    simbol_spacing_factor = 0.3
    simbol_min_spacing = 3
    shot_adjustment_x = 2

    simbols = ['+', '*', '.', ':', "'"]

    coroutines = []
    canvas.border()
    canvas.nodelay(True)
    for y in range(1, coord_y):
        for x in range(
                random.randint(initial_character_spacing, end_character_spacing),
                max_x,
                random.randint(simbol_min_spacing, int(max_x * simbol_spacing_factor))
        ):
            simbol = random.choice(simbols)
            offset_tics = random.randint(1, 3)
            coroutines.append(blink(canvas, y, x, offset_tics, simbol))

    animate_spaceship_iterator = cycle([frame1, frame1, frame2, frame2])
    coroutines.append(animate_spaceship(animate_spaceship_iterator, canvas, spaceship_y, spaceship_x, coord_y,
                                        coord_x, shot_adjustment_x, coroutines))

    coroutines.append(fill_orbit_with_garbage(canvas, coord_x, coroutines, garbage_frames))
    coroutines.append(increase_year())
    coroutines.append(display_year(canvas, coord_x))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        curses.curs_set(False)
        time.sleep(tic_timeout)


def read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


if __name__ == '__main__':
    garbage_path = 'animation_frames/garbage/'
    garbage_frames = []

    for file in listdir(garbage_path):
        file_full_path = join(garbage_path, file)
        if isfile(file_full_path):
            file_frame = read_file(file_full_path)
            garbage_frames.append(file_frame)

    rocket_frame_path_1 = 'animation_frames/rocket_frame_1.txt'
    rocket_frame_path_2 = 'animation_frames/rocket_frame_2.txt'
    rocket_frame_one = read_file(rocket_frame_path_1)
    rocket_frame_two = read_file(rocket_frame_path_2)

    tic_timeout = 0.1
    curses.update_lines_cols()
    curses.wrapper(draw, tic_timeout,
                   rocket_frame_one,
                   rocket_frame_two,
                   garbage_frames)

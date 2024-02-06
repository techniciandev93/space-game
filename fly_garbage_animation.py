import random

from async_sleep import sleep
from explosion import explode
from game_animation import draw_frame, get_frame_size
from game_scenario import get_garbage_delay_tics
from obstacles import Obstacle

obstacles = []
obstacles_in_last_collisions = []


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()
    frame_rows, frame_columns = get_frame_size(garbage_frame)

    column = max(column, 2)
    column = min(column, columns_number - frame_columns - 1)

    row = 1

    new_obstacle = Obstacle(row, column, frame_rows, frame_columns)
    obstacles.append(new_obstacle)

    try:
        while row < rows_number:
            if new_obstacle in obstacles_in_last_collisions:
                obstacles_in_last_collisions.remove(new_obstacle)
                await explode(canvas, row + frame_rows // 2, column + frame_columns // 2)
                return

            draw_frame(canvas, row, column, garbage_frame)
            await sleep()
            draw_frame(canvas, row, column, garbage_frame, negative=True)
            row += speed
            new_obstacle.row = row
    finally:
        obstacles.remove(new_obstacle)


async def fill_orbit_with_garbage(canvas, coord_x, coroutines, trash_frames):
    while True:
        delay_tics = get_garbage_delay_tics()
        if delay_tics:
            column = random.randint(1, coord_x - 1)
            garbage_frame = random.choice(trash_frames)
            garbage_coroutine = fly_garbage(canvas, column, garbage_frame, speed=0.4)
            coroutines.append(garbage_coroutine)
            await sleep(tics=delay_tics)
        await sleep()

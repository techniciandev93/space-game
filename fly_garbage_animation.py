import asyncio
import random

from async_sleep import sleep
from game_animation import draw_frame, get_frame_size
from obstacles import Obstacle, show_obstacles

obstacles = []


async def fly_garbage(canvas, column, garbage_frame, coroutines, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()
    frame_rows, frame_columns = get_frame_size(garbage_frame)

    column = max(column, 2)
    column = min(column, columns_number - frame_columns - 1)

    row = 0
    global obstacles

    new_obstacle = Obstacle(row, column, frame_rows, frame_columns)
    obstacles.append(new_obstacle)

    coroutine = show_obstacles(canvas, obstacles)
    coroutines.append(coroutine)

    try:
        while row < rows_number:
            # if new_obstacle in obstacles_in_last_collisions:
            #     obstacles_in_last_collisions.remove(new_obstacle)
            #     await explode(canvas, row + frame_rows // 2, column + frame_columns // 2)
            #     return

            draw_frame(canvas, row, column, garbage_frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, garbage_frame, negative=True)
            row += speed
            new_obstacle.row = row
    finally:
        obstacles.remove(new_obstacle)


async def fill_orbit_with_garbage(canvas, coord_x, coroutines, trash_frames):
    while True:
        await sleep(tics=10)
        column = random.randint(1, coord_x - 1)
        garbage_frame = random.choice(trash_frames)
        garbage_coroutine = fly_garbage(canvas, column, garbage_frame, coroutines, speed=0.4)
        coroutines.append(garbage_coroutine)
        await sleep()


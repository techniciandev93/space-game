import asyncio
import random

from async_sleep import sleep
from game_animation import draw_frame, get_frame_size
from obstacles import Obstacle


obstacles = []


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    global obstacles
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    obstacle = Obstacle(row, column, get_frame_size(garbage_frame))
    obstacles.append(obstacle)

    # while row < rows_number:
    #     draw_frame(canvas, row, column, garbage_frame)
    #     await sleep()
    #     draw_frame(canvas, row, column, garbage_frame, negative=True)
    #     row += speed

    try:
        while column > 0:
            garbage_frame, row, col = obstacle.dump_bounding_box()

            draw_frame(canvas, row, column, garbage_frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, garbage_frame, negative=True)
            obstacle.column = column
            row += speed

            #if obstacle in obstacles and obstacle.has_collision(spaceship_y, spaceship_x):
                # Здесь можно добавить логику для обработки столкновения
            #    pass

            for obstacle in obstacles.copy():
                if obstacle.column < 0:
                    obstacles.remove(obstacle)
    finally:
        obstacles.remove(obstacle)


async def fill_orbit_with_garbage(canvas, coord_x, coroutines, trash_frames):
    while True:
        await sleep(tics=10)
        column = random.randint(1, coord_x - 1)
        garbage_frame = random.choice(trash_frames)
        garbage_coroutine = fly_garbage(canvas, column, garbage_frame, speed=0.4)
        coroutines.append(garbage_coroutine)
        await sleep()


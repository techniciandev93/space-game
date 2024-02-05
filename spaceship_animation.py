from async_sleep import sleep
from explosion import explode
from fire_animation import fire
from fly_garbage_animation import obstacles
from game_animation import read_controls, get_frame_size, draw_frame
from game_scenario import YEAR
from physics import update_speed


async def animate_spaceship(animate_spaceship_iterator, canvas, row, column, max_coord_y, max_coord_x,
                            shot_adjustment_x, coroutines):
    row_speed = column_speed = 0
    for frame in animate_spaceship_iterator:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        frame_rows, frame_columns = get_frame_size(frame)

        for obstacle in obstacles:
            if obstacle.has_collision(row, column, frame_rows, frame_columns):
                await explode(canvas, row + frame_rows // 2, column + frame_columns // 2)
                coroutines.append(show_gameover(canvas, max_coord_y, max_coord_x))
                return

        if space_pressed and YEAR >= 2020:
            coroutines.append(fire(canvas, row, column + 2))

        row_speed, column_speed = update_speed(row_speed, column_speed, rows_direction, columns_direction)
        row += row_speed
        column += column_speed

        row = max(0, min(row, max_coord_y - frame_rows))
        column = max(0, min(column, max_coord_x - frame_columns))

        if space_pressed:
            coroutines.append(fire(canvas, row, column + shot_adjustment_x))
            await sleep()

        draw_frame(canvas, round(row), round(column), frame)
        await sleep()
        draw_frame(canvas, round(row), round(column), frame, negative=True)


async def show_gameover(canvas, height_window, width_window):
    with open('animation_frames/gameover.txt', 'r') as file:
        game_over_frame = file.read()
    game_over_frame_rows, game_over_frame_columns = get_frame_size(game_over_frame)
    while True:
        draw_frame(canvas,
                   height_window // 2 - game_over_frame_rows // 2,
                   width_window // 2 - game_over_frame_columns // 2,
                   game_over_frame)
        await sleep()

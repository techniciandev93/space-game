from async_sleep import sleep
from fire_animation import fire
from game_animation import read_controls, get_frame_size, draw_frame
from physics import update_speed


async def animate_spaceship(animate_spaceship_iterator, canvas, row, column, max_coord_y, max_coord_x,
                            shot_adjustment_x, coroutines):
    row_speed = column_speed = 0
    for frame in animate_spaceship_iterator:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)

        frame_rows, frame_columns = get_frame_size(frame)

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


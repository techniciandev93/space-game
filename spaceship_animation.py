import asyncio

from game_animation import read_controls, get_frame_size, draw_frame


async def animate_spaceship(animate_spaceship_iterator, canvas, row, column, max_coord_y, max_coord_x):
    for frame in animate_spaceship_iterator:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)

        frame_rows, frame_columns = get_frame_size(frame)

        new_row = row + rows_direction
        new_column = column + columns_direction

        if 0 < new_row < max_coord_y - frame_rows:
            row = new_row

        if 0 < new_column < max_coord_x - frame_columns:
            column = new_column

        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)

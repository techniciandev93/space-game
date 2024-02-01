import curses

from async_sleep import sleep


async def blink(canvas, row, column, offset_tics, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(tics=4 * offset_tics)

        canvas.addstr(row, column, symbol)
        await sleep(tics=3 * offset_tics)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(tics=5 * offset_tics)

        canvas.addstr(row, column, symbol)
        await sleep(tics=2 * offset_tics)

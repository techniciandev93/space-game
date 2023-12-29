import asyncio
import curses


async def blink(canvas, row, column, offset_tics, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for i in range(4 * offset_tics):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(3 * offset_tics):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for i in range(5 * offset_tics):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(2 * offset_tics):
            await asyncio.sleep(0)

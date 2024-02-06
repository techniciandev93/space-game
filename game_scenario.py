import curses

from async_sleep import sleep

PHRASES = {
    # Только на английском, Repl.it ломается на кириллице
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Take the plasma gun! Shoot the garbage!",
}

YEAR = 1957


def get_year():
    global YEAR
    return YEAR


def get_garbage_delay_tics():
    if YEAR < 1961:
        return None
    elif YEAR < 1969:
        return 20
    elif YEAR < 1981:
        return 14
    elif YEAR < 1995:
        return 10
    elif YEAR < 2010:
        return 8
    elif YEAR < 2020:
        return 6
    else:
        return 2


async def display_year(canvas, width_window):
    global YEAR, PHRASES
    phrase = ''

    table_height = 3
    table_win = canvas.derwin(table_height, width_window, canvas.getmaxyx()[0] - table_height, 0)

    while True:
        if YEAR in PHRASES.keys():
            phrase = PHRASES[YEAR]
        table_win.clear()
        table_win.addstr(1, 1, f'YEAR {YEAR} | {phrase}', curses.A_BOLD)
        table_win.refresh()
        await sleep()


async def increase_year():
    global YEAR
    while True:
        await sleep(15)
        YEAR += 1

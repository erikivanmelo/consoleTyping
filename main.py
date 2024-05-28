import curses
SCREEN_START_X = SCREEN_START_Y = 5

COLOR_BASE = 1
COLOR_CORRECT = 2
COLOR_WRONG = 3
SPACE = "\u2022"

def main():
    screen = curses.initscr()
    curses.start_color()
    if not curses.has_colors():
        raise Exception("The colors are not supported in this console")

    curses.cbreak()
    curses.curs_set(1)
    curses.noecho()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    text = open("text.txt","r").read()

    #set screen size
    screen_height, screen_width = screen.getmaxyx()

    cursor_x = SCREEN_START_X
    cursor_y = SCREEN_START_Y

    initial_text(screen, text, screen_width)
    screen.move(cursor_y, cursor_x)
    i = 0
    while True:
        key = screen.getkey()
        i = checkKey(screen, key, i, text, screen_width)

    curses.nocbreak()
    curses.endwin()

def textPositionToSreenPosition(number_key, text, screen_width):
    width = screen_width - SCREEN_START_X
    x = SCREEN_START_X
    y = SCREEN_START_Y
    words = text.split()
    i = 0
    increase = 0
    leave = False
    for word in words:
        wlen = len(word)
        if x + wlen + 1 > width:
            x = SCREEN_START_X
            y += 1
        if i + wlen + 1 <= number_key:
            increase = wlen + 1
        else:
            increase = number_key - i
            leave = True
        x += increase
        i += increase
        increase = 0
        if leave:
            break
    return x, y

def checkKey(screen, key, number_key, text, screen_width):
    x, y = textPositionToSreenPosition(number_key, text, screen_width)
    if key in ('KEY_BACKSPACE', '\b', '\x7f'):
        if number_key == 0:
            return 0
        number_key -= 1
        x, y = textPositionToSreenPosition(number_key, text, screen_width)
        ch = SPACE if text[number_key] == " " else text[number_key]
        screen.addch(y, x, ch, curses.color_pair(COLOR_BASE))
    else:
        if number_key >= len(text):
            return len(text)
        x, y = textPositionToSreenPosition(number_key, text, screen_width)
        ch = SPACE if text[number_key] == " " else text[number_key]
        screen.addch(y, x, ch, curses.color_pair( COLOR_CORRECT if key == text[number_key] else COLOR_WRONG) )
        number_key += 1
    x, y = textPositionToSreenPosition(number_key, text, screen_width)
    screen.move(y, x)
    return number_key

def initial_text(screen, text, screen_width):
    words = text.split()
    x = SCREEN_START_X
    y = SCREEN_START_Y
    width = screen_width - SCREEN_START_X

    for word in words:
        if x + len(word) + 1 > width:
            x = SCREEN_START_X
            y += 1
        screen.addstr(y, x, word + SPACE, curses.color_pair(COLOR_BASE))
        x += len(word) + 1

if __name__ == "__main__":
    main()

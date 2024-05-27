import curses
screenStartX = screenStartY = 5


def initialText(screen, text, screenWidth):
    words = text.split()
    x = screenStartX
    y = screenStartY
    width = screenWidth - screenStartX

    for word in words:
        if (x + len(word) + 1 >= width or '\n' in word):
            x = screenStartX
            y += 1
        screen.addstr(y, x, word + " ")
        x += len(word) + 1

def main():
    screen = curses.initscr()
    curses.start_color()
    if not curses.has_colors():
        raise Exception("The colors are not supported in this console")

    curses.cbreak()
    curses.curs_set(1)
    curses.noecho()

    text = open("text.txt","r").read()

    #set screen size
    screenHeight, screenWidth = screen.getmaxyx()

    cursorX = screenStartX
    cursorY = screenStartY

    screen.move(cursorX, cursorY)
    initialText(screen, text, screenWidth)
    screen.getch()

    #Curses End
    curses.nocbreak()
    curses.endwin()

if __name__ == "__main__":
    main()


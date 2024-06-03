import curses
class ConsoleTyping:
    SCREEN_START_X = 5
    SCREEN_START_Y = 5
    COLOR_BASE     = 1
    COLOR_CORRECT  = 2
    COLOR_WRONG    = 3
    SPACE          = "\u2022"

    original_text = ""
    typed_text    = ""
    screen        = None
    screen_height = 0
    screen_width  = 0
    cursor_x      = 0
    cursor_y      = 0

    def __init__(self):
        self.screen = curses.initscr()
        curses.start_color()
        if not curses.has_colors():
            raise Exception("The colors are not supported in this console")

        curses.cbreak()
        curses.curs_set(1)
        curses.noecho()

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        self.original_text = open("text.txt","r").read()
        self.screen_height, self.screen_width = self.screen.getmaxyx()
        self.cursor_x = self.SCREEN_START_X
        self.cursor_y = self.SCREEN_START_Y
        self.screen.move(self.cursor_y, self.cursor_x)

    def __del__(self):
        curses.nocbreak()
        curses.endwin()

    def run(self):
        self.initial_text()
        current_char_index = 0
        while True:
            current_char_index = self.checkKey(self.screen.getkey(), current_char_index)


    def textPositionToSreenPosition(self, char_index):
        width = self.screen_width - self.SCREEN_START_X
        x = self.SCREEN_START_X
        y = self.SCREEN_START_Y
        words = self.original_text.split()
        i = 0
        increase = 0
        leave = False
        for word in words:
            wlen = len(word)
            if x + wlen + 1 > width:
                x = self.SCREEN_START_X
                y += 1
            if i + wlen + 1 <= char_index:
                increase = wlen + 1
            else:
                increase = char_index - i
                leave = True
            x += increase
            i += increase
            increase = 0
            if leave:
                break
        return x, y

    def checkKey(self, key, char_index):
        x, y = self.textPositionToSreenPosition(char_index)
        if key in ('KEY_BACKSPACE', '\b', '\x7f'):
            if char_index == 0:
                return 0
            char_index -= 1
            x, y = self.textPositionToSreenPosition(char_index)
            ch = self.SPACE if self.original_text[char_index] == " " else self.original_text[char_index]
            self.screen.addch(y, x, ch, curses.color_pair(self.COLOR_BASE))
        else:
            if char_index >= len(self.original_text):
                return len(self.original_text)
            x, y = self.textPositionToSreenPosition(char_index)
            ch = self.SPACE if self.original_text[char_index] == " " else self.original_text[char_index]
            self.screen.addch(y, x, ch, curses.color_pair( self.COLOR_CORRECT if key == self.original_text[char_index] else self.COLOR_WRONG) )
            char_index += 1
        x, y = self.textPositionToSreenPosition(char_index)
        self.screen.move(y, x)
        return char_index

    def initial_text(self):
        words = self.original_text.split()
        x = self.SCREEN_START_X
        y = self.SCREEN_START_Y
        width = self.screen_width - self.SCREEN_START_X

        for word in words:
            if x + len(word) + 1 > width:
                x = self.SCREEN_START_X
                y += 1
            self.screen.addstr(y, x, word + self.SPACE, curses.color_pair(self.COLOR_BASE))
            x += len(word) + 1


if __name__ == "__main__":
    consoleTyping = ConsoleTyping()
    consoleTyping.run()
    del consoleTyping

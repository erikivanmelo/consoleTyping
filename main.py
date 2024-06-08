import curses
import typing
class ConsoleTyping:
    COLOR_BASE     = 1
    COLOR_CORRECT  = 2
    COLOR_WRONG    = 3
    SPACE          = "\u2022"

    horizontal_margin = 5
    vertical_margin = 5
    original_text = ""
    typed_text    = ""
    cursor_positions = dict()
    screen        = None
    screen_height = 0
    screen_width  = 0
    cursor_x      = 0
    cursor_y      = 0

    def __init__(self):
        self.screen = curses.initscr()
        self.screen.keypad(True)
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
        self.cursor_x = self.horizontal_margin
        self.cursor_y = self.vertical_margin
        self.calculate_cursor_positions()

    def __del__(self):
        curses.nocbreak()
        curses.endwin()

    def run(self):
        self.initial_text()
        self.draw_border()
        current_char_index = 0
        key = None
        self.screen.move(self.cursor_y, self.cursor_x)
        while key != '\033':
            key = self.screen.getkey()
            current_char_index = self.checkKey(key, current_char_index)

    def draw_border(self):
        y = self.vertical_margin - 1
        x = self.horizontal_margin - 1
        height = (self.screen_height - (self.vertical_margin * 2)) + 2
        width = (self.screen_width - (self.horizontal_margin * 2)) + 2

        self.screen.hline(y, x, curses.ACS_HLINE, width)
        self.screen.hline(y + height - 1, x, curses.ACS_HLINE, width)

        self.screen.vline(y, x, curses.ACS_VLINE, height)
        self.screen.vline(y, x + width - 1, curses.ACS_VLINE, height)

        self.screen.addch(y, x, curses.ACS_ULCORNER)            # Esquina superior izquierda
        self.screen.addch(y, x + width - 1, curses.ACS_URCORNER) # Esquina superior derecha
        self.screen.addch(y + height - 1, x, curses.ACS_LLCORNER) # Esquina inferior izquierda
        self.screen.addch(y + height - 1, x + width - 1, curses.ACS_LRCORNER) # Esquina inferior derecha

    def calculate_cursor_positions(self):
        width = self.screen_width - self.horizontal_margin
        x = self.horizontal_margin
        y = self.vertical_margin
        words = self.original_text.split()
        text_index = 0
        for word in words:
            word += " "
            wlen = len(word)
            if x + wlen > width:
                x = self.horizontal_margin
                y += 1
            for word_index in range(wlen):
                self.cursor_positions[text_index] = (x + word_index, y)
                text_index += 1
            x += wlen

    def checkKey(self, key, char_index):
        x, y = self.cursor_positions[char_index]
        if key in ('KEY_BACKSPACE', '\b', '\x7f'):
            if char_index == 0:
                return 0
            char_index -= 1
            x, y = self.cursor_positions[char_index]
            ch = self.SPACE if self.original_text[char_index] == " " else self.original_text[char_index]
            self.screen.addch(y, x, ch, curses.color_pair(self.COLOR_BASE))
        else:
            if char_index >= len(self.original_text):
                return len(self.original_text)
            x, y = self.cursor_positions[char_index]
            ch = self.SPACE if self.original_text[char_index] == " " else self.original_text[char_index]
            self.screen.addch(y, x, ch, curses.color_pair( self.COLOR_CORRECT if key == self.original_text[char_index] else self.COLOR_WRONG) )
            char_index += 1
        x, y = self.cursor_positions[char_index]
        self.screen.move(y, x)
        return char_index

    def initial_text(self):
        words = self.original_text.split()
        x = self.horizontal_margin
        y = self.vertical_margin
        width = self.screen_width - self.horizontal_margin

        for word in words:
            if x + len(word) + 1 > width:
                x = self.horizontal_margin
                y += 1
            self.screen.addstr(y, x, word + self.SPACE, curses.color_pair(self.COLOR_BASE))
            x += len(word) + 1


if __name__ == "__main__":
    consoleTyping = ConsoleTyping()
    consoleTyping.run()
    del consoleTyping

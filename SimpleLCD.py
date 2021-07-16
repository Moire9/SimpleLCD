from gpiozero import OutputDevice
from time import sleep
from typing import *

# https://www.sparkfun.com/datasheets/LCD/HD44780.pdf

"""
Example code:


lcd = LCD(26, 13, 19,  18, 21, 20, 16, 12, 25, 24, 23, two_lines = True)    
lcd.write("Hello, World!")
lcd.home()
lcd.write("hh")
input()
"""

class LCD:
    font: Dict[str, Tuple[int, int, int, int, int, int, int, int]]  = {
        " ": (0,0,1,0,0,0,0,0),
        "!": (0,0,1,0,0,0,0,1),
        '"': (0,0,1,0,0,0,1,0),
        "#": (0,0,1,0,0,0,1,1),
        "$": (0,0,1,0,0,1,0,0),
        "%": (0,0,1,0,0,1,0,1),
        "&": (0,0,1,0,0,1,1,0),
        "'": (0,0,1,0,0,1,1,1),
        "(": (0,0,1,0,1,0,0,0),
        ")": (0,0,1,0,1,0,0,1),
        "*": (0,0,1,0,1,0,1,0),
        "+": (0,0,1,0,1,0,1,1),
        ",": (0,0,1,0,1,1,0,0),
        "-": (0,0,1,0,1,1,0,1),
        ".": (0,0,1,0,1,1,1,0),
        "/": (0,0,1,0,1,1,1,1),

        "0": (0,0,1,1,0,0,0,0),
        "1": (0,0,1,1,0,0,0,1),
        "2": (0,0,1,1,0,0,1,0),
        "3": (0,0,1,1,0,0,1,1),
        "4": (0,0,1,1,0,1,0,0),
        "5": (0,0,1,1,0,1,0,1),
        "6": (0,0,1,1,0,1,1,0),
        "7": (0,0,1,1,0,1,1,1),
        "8": (0,0,1,1,1,0,0,0),
        "9": (0,0,1,1,1,0,0,1),
        ":": (0,0,1,1,1,0,1,0),
        ";": (0,0,1,1,1,0,1,1),
        "<": (0,0,1,1,1,1,0,0),
        "=": (0,0,1,1,1,1,0,1),
        ">": (0,0,1,1,1,1,1,0),
        "?": (0,0,1,1,1,1,1,1),

        "@": (0,1,0,0,0,0,0,0),
        "A": (0,1,0,0,0,0,0,1),
        "B": (0,1,0,0,0,0,1,0),
        "C": (0,1,0,0,0,0,1,1),
        "D": (0,1,0,0,0,1,0,0),
        "E": (0,1,0,0,0,1,0,1),
        "F": (0,1,0,0,0,1,1,0),
        "G": (0,1,0,0,0,1,1,1),
        "H": (0,1,0,0,1,0,0,0),
        "I": (0,1,0,0,1,0,0,1),
        "J": (0,1,0,0,1,0,1,0),
        "K": (0,1,0,0,1,0,1,1),
        "L": (0,1,0,0,1,1,0,0),
        "M": (0,1,0,0,1,1,0,1),
        "N": (0,1,0,0,1,1,1,0),
        "O": (0,1,0,0,1,1,1,1),

        "P": (0,1,0,1,0,0,0,0),
        "Q": (0,1,0,1,0,0,0,1),
        "R": (0,1,0,1,0,0,1,0),
        "S": (0,1,0,1,0,0,1,1),
        "T": (0,1,0,1,0,1,0,0),
        "U": (0,1,0,1,0,1,0,1),
        "V": (0,1,0,1,0,1,1,0),
        "W": (0,1,0,1,0,1,1,1),
        "X": (0,1,0,1,1,0,0,0),
        "Y": (0,1,0,1,1,0,0,1),
        "Z": (0,1,0,1,1,0,1,0),
        "[": (0,1,0,1,1,0,1,1),
        "¥": (0,1,0,1,1,1,0,0),
        "]": (0,1,0,1,1,1,0,1),
        "^": (0,1,0,1,1,1,1,0),
        "_": (0,1,0,1,1,1,1,1),

        "`": (0,1,1,0,0,0,0,0),
        "a": (0,1,1,0,0,0,0,1),
        "b": (0,1,1,0,0,0,1,0),
        "c": (0,1,1,0,0,0,1,1),
        "d": (0,1,1,0,0,1,0,0),
        "e": (0,1,1,0,0,1,0,1),
        "f": (0,1,1,0,0,1,1,0),
        "g": (0,1,1,0,0,1,1,1),
        "h": (0,1,1,0,1,0,0,0),
        "i": (0,1,1,0,1,0,0,1),
        "j": (0,1,1,0,1,0,1,0),
        "k": (0,1,1,0,1,0,1,1),
        "l": (0,1,1,0,1,1,0,0),
        "m": (0,1,1,0,1,1,0,1),
        "n": (0,1,1,0,1,1,1,0),
        "o": (0,1,1,0,1,1,1,1),

        "p": (0,1,1,1,0,0,0,0),
        "q": (0,1,1,1,0,0,0,1),
        "r": (0,1,1,1,0,0,1,0),
        "s": (0,1,1,1,0,0,1,1),
        "t": (0,1,1,1,0,1,0,0),
        "u": (0,1,1,1,0,1,0,1),
        "v": (0,1,1,1,0,1,1,0),
        "w": (0,1,1,1,0,1,1,1),
        "x": (0,1,1,1,1,0,0,0),
        "y": (0,1,1,1,1,0,0,1),
        "z": (0,1,1,1,1,0,1,0),
        "{": (0,1,1,1,1,0,1,1),
        "|": (0,1,1,1,1,1,0,0),
        "}": (0,1,1,1,1,1,0,1),
        "←": (0,1,1,1,1,1,1,0),
        "→": (0,1,1,1,1,1,1,1)
    }

    def __init__(self, rs: Union[int, OutputDevice], rw: Union[int, OutputDevice], e: Union[int, OutputDevice], *data: Union[int, OutputDevice], cursor: bool = True, blink: bool = False, two_lines: bool = False, large_font: bool = False):
        if len(data) != 8: raise ValueError()

        self.rs = OutputDevice(rs) if type(rs) is int else rs
        self.rw = OutputDevice(rw) if type(rs) is int else rs
        self.e  = OutputDevice(e ) if type(rs) is int else rs
        
        self.e.off()
        
        self.data: List[OutputDevice] = list(map(OutputDevice, data))

        # init
        [self.push(*p) for p in (
            (0,0,0,0,1,1,two_lines,large_font,0,0), 
            (0,0,0,0,0,0,1,1,cursor,blink), 
            (0,0,0,0,0,0,0,1,1,0)
        )]

    def submit(self):
        self.e.on()
        self.e.off()

    def push(self, *data: int):
        """
        Send commands to the LCD.
        `data` is up to 10 bits to be sent, which are sent over RS, RW, and then D0-D7.
        If less than 10 bits are passed, the last pins of those mentioned above will not have their state changed.
        """
        self.rs.value = data[0]
        self.rw.value = data[1]
        for i in range(len(data) - 2): self.data[7 - i].value = int(data[i + 2])
        self.submit()

    def write(self, text: Union[str, Iterable[str]]):
        """
        Write a string to the LCD. Supported characters are all ASCII, as well as the Japanese Yen symbol (¥) and Unicode Arrows U+2190 and U+2192 (← & →)
        """
        [self.text(*LCD.font[char]) for char in text]

    def text(self, *data: int):
        """
        Write a character to the LCD, using its character code. Useful if you need to write symbols not supported by thislibrary.
        """
        self.push(1, 0, *data)



    def clear(self):
        """
        Clears the display and resets cursor position to the first slot.
        """
        self.push(0,0,0,0,0,0,0,0,0,1)

    def home(self):
        """
        Move cursor to the first slot. This command takes a much longer time to be processed than others, hence the sleep call.
        """
        self.push(0,0,0,0,0,0,0,0,1,0)
        sleep(0.0016)

    def move_cursor(self, amount: int):
        """
        Move the cursor `amount` steps forward. If `amount` is negative, move the cursor `-amount` steps backward.
        """
        self._move(amount, 0)

    def display_shift(self, amount: int):
        """
        Shift the display `amount` steps forward. If `amount` is negative, shift the display `-amount` steps backward.
        """
        self._move(amount, 1)

    def _move(self, amount: int, t: int):
        if amount == 0: return
        d = amount > 0
        [self.push(0,0,0,0,0,1,t,d,0,0) for x in range(abs(amount))]


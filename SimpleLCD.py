"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
"""

# https://www.sparkfun.com/datasheets/LCD/HD44780.pdf

from RPi import GPIO
from time import sleep
from typing import *

class Pin:
    def __init__(self, num: int):
        self.num = num
        GPIO.setup(num, GPIO.OUT)

    def on(self):
        self.set(1)

    def off(self):
        self.set(0)

    def set(self, val: Union[int, bool]):
        GPIO.output(self.num, bool(val))

class LCD:
    def __init__(self, rs: int, rw: int, e: int, *data: int, two_lines: bool = False, large_font: bool = False, power: bool = True, cursor: bool = True, blink: bool = False, ltr: bool = True, autoscroll: bool = False):
        if len(data) != 8: raise ValueError()

        GPIO.setmode(GPIO.BCM)
        
        self.rs = Pin(rs)
        self.rw = Pin(rw)
        self.e  = Pin(e)
        
        self.e.off()
        
        self.data: List[OutputDevice] = list(map(Pin, data))

        # Initialize
        self.push(0,0,0,0,1,1,two_lines,large_font)

        self.configure(power=True, cursor=cursor, blink=blink, ltr=ltr, autoscroll=autoscroll, override=True)

        self.clear()

    def submit(self):
        self.e.on()
        self.e.off()

    def push(self, *data: int):
        """
        Send commands to the LCD.
        `data` is up to 10 bits to be sent, which are sent over RS, RW, and then D0-D7.
        If less than 10 bits are passed, the last pins of those mentioned above will not have their state changed.
        """
        self.rs.set(data[0])
        self.rw.set(data[1])
        for i in range(len(data) - 2): self.data[7 - i].set(int(data[i + 2]))
        self.submit()

    def write(self, text: Any):
        """
        Write a string to the LCD. Supported characters are all ASCII, as well as the Japanese Yen symbol (¥) and Unicode Arrows U+2190 and U+2192 (← & →)
        """
        [self.text(*font[char]) for char in str(text)]

    def text(self, *data: int):
        """
        Write a character to the LCD, using its character code. Useful if you need to write symbols not supported by thislibrary.
        """
        self.push(1, 0, *data)

    def configure(self, power: Optional[bool] = None, cursor: Optional[bool] = None, blink: Optional[bool] = None, ltr: Optional[bool] = None, autoscroll: Optional[bool] = None, override: bool = False):
        """
        Configure the LCD. You can turn on or off the display, toggle the cursor, and set whether or not it blinks.
        """
        if power is not None: self.power = power
        if cursor is not None: self.cursor = cursor
        if blink is not None: self.blink = blink
        if ltr is not None: self.ltr = ltr
        if autoscroll is not None: self.autoscroll = autoscroll

        if override or power != None or cursor != None or blink != None: self.push(0,0,0,0,0,0,1,self.power,self.cursor,self.blink)
        
        if override or ltr != None or autoscroll != None: self.push(0,0,0,0,0,0,0,1,self.ltr,self.autoscroll)

    def close(self, clear = False, shutdown = False):
        """
        Closes the LCD by releasing allocated GPIO pins. Optionally clear text and turn off the screen.
        Using this object after it has been closed is a very bad idea!
        """
        if clear: self.clear()
        if shutdown: self.configure(power = False)
        
        GPIO.cleanup()

    def clear(self):
        """
        Clears the display and resets cursor position to the first slot.
        """
        self.push(0,0,0,0,0,0,0,0,0,1)
        sleep(0.0016)

    def home(self):
        """
        Move cursor to the first slot. This command takes a much longer time to be processed than others, hence the sleep call.
        """
        self.push(0,0,0,0,0,0,0,0,1,0)
        sleep(0.0016)

    def move(self, amount: int):
        """
        Move the cursor `amount` steps forward. If `amount` is negative, move the cursor `-amount` steps backward.
        """
        self._scrl(amount, 0)

    def scroll(self, amount: int):
        """
        Shift the display `amount` steps forward. If `amount` is negative, shift the display `-amount` steps backward.
        """
        self._scrl(-amount, 1)

    def _scrl(self, amount: int, t: int):
        if amount == 0: return
        d = amount > 0
        [self.push(0,0,0,0,0,1,t,d,0,0) for x in range(abs(amount))]

    def __del__(self): self.close()

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

# SimpleLCD
Small & simple python library for controlling and using a Hitachi HD44780U breadboard LCD on a Raspberry Pi.

## Usage
No dependencies, other than RPi.GPIO, which is pre-installed. Single file library - just download the file and drop it into your project.

```py
from SimpleLCD import LCD
lcd = LCD(20, 21, 26, 19, 13, 6, 5, 22, 27, 17, 4)
lcd.write("Hello, World!")
lcd.home()
lcd.write("HELLO")
lcd.move(8)
lcd.print("!!!")
```

Run `help(LCD)` at the interpreter to see all methods. Documentation is included.

Make sure to `del(lcd)` or `lcd.close()` after use in order for RPi to release the pin channels (you shouldn't need to do this if your program exits immediately).

## License
SimpleLCD is licensed under the Unlicense. You can do whatever you want. Except for controlling LCDs on nuclear weapons, please.

## More Info
To learn more about the LCD, other commands, and to build your own, please look at the [datasheet](https://www.sparkfun.com/datasheets/LCD/HD44780.pdf).


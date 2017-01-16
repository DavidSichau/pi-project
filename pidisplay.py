from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

sense = SenseHat()

class PiDisplay:
    def __init__(self, bg_colour):
        self.black = (0, 0, 0)
        self.bg = bg_colour

        self.x = 0
        self.y = 0

    def set_pos(self, posx, posy, colour):
        "sense.set_pixel(self.x, self.y, self.black)"
        sense.set_pixel((posx/40),(posy/40),colour)
        self.x = posx/40
        self.y = posy/40

    def set_pos_rocket(self, posx, posy, colour):
        if posx > 280 or posx < 0 or posy > 280 or posy < 0:
            lives = 1
        else:
            sense.set_pixel(self.x, self.y, self.black)
            sense.set_pixel((posx/40),(posy/40),colour)
            self.x = posx/40
            self.y = posy/40



        




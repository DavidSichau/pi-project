from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

sense = SenseHat()

class PiDisplay:
    def __init__(self, bg_colour):
        self.bg = bg_colour

    def set_ally_pos(self, posx, posy, colour):
        sense.set_pixel((posx/40),(posy/40),colour)

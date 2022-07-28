import pygame as pg


# Timer
FPS = 60
timer = pg.time.Clock()

# Graphic
pg.init()
W, H = 1920/2, 1080/2
main_window = pg.display.set_mode((W, H))
# colors
background = (0, 0, 0)

# Data
to_tick = []
to_check = []
keyboard = pg.key.get_pressed() # For later use


# Classes and supporting functions
class Halt:
    """Halt function for skip_frames after it was used."""
    def __init__(self, func, skip_frames) -> None:
        self.func = func
        self.current = 0
        self.skip_frames = skip_frames
        to_tick.append(self)

    def __call__(self, *args, **kwargs):
        """return func() if check(), else return False."""
        if self.check():
            return self.func(*args, **kwargs)
        return False

    def tick(self) -> None:
        """Must be called each frame to work correctly."""
        if self.current > 0:
            self.current -= 1

    def check(self) -> bool:
        """return True if the skip_frames frames has passed, else False."""
        if self.current <= 0:
            self.current = self.skip_frames
            return True
        return False

def tick_all():
    for func in to_tick:
        func.tick()


class Keys:
    """Call the function when the given keys are pressed."""
    def __init__(self, func, *keys: tuple) -> None:
        self.func = func
        self.keys = keys
        to_check.append(self)

    @staticmethod
    def key_check(keys) -> bool:
        """return True if the keys were pressed, else False."""
        for key in keys:
            if type(key) in [list, tuple]:
                for k in key:
                    if not keyboard[k]:
                        break
                else:
                    return True
            elif keyboard[key]:
                return True  
        return False

    def check(self, *args, **kwargs) -> bool:
        """Check the keys and return func(), or return False."""
        if self.key_check(self.keys):
            self.func(*args, **kwargs)
            return True
        return False

def check_all():
    for func in to_check:
        if func.check():
            break


test_func = Halt(lambda: print("Works"), FPS/2)
test_keys = Keys(test_func, [pg.K_a, pg.K_d], pg.K_p, pg.K_q)
test_keys2 = Keys(Halt(lambda: print("Works 2"), FPS), pg.K_q, pg.K_s)

executing = True
while executing:
    for el in pg.event.get():
        if el.type == pg.QUIT:
            executing = False

    keyboard = pg.key.get_pressed()
    main_window.fill(background)

    check_all()
    tick_all()

    pg.display.update()
    timer.tick(FPS)
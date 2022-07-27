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


test_func = Halt(lambda a: print("Works", a), FPS/2)


executing = True
while executing:
    for el in pg.event.get():
        if el.type == pg.QUIT:
            executing = False

    keyboard = pg.key.get_pressed()
    main_window.fill(background)

    tick_all()
    test_func(":)")
    pg.display.update()
    timer.tick(FPS)
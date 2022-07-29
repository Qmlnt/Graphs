import pygame as pg
from Graphs import Graph
import json
from time import ctime


# Timer
FPS = 60
timer = pg.time.Clock()
key_cooldown = FPS/5

# Graphic
pg.init()
W, H = 1920/2, 1080/2
main_window = pg.display.set_mode((W, H))
# colors
background = (0, 0, 0)
dot_color = (255, 255, 255)
dot_number_color = (255, 0, 0)
edge_color = (0, 255, 0)
edge_number_color = (255, 0, 255)
selected_color = (255, 0, 255)
selected_number_color = (0, 255, 0)
# sizes
edge_width = 4
dot_radius = 15
# fonts
number_font = pg.font.SysFont("Comic Sans MS", dot_radius*2)

# Data
graph = Graph()
dots = {}
dot_name = 0
selected = []
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


# Main functions
def distance(pos1: tuple, pos2: tuple) -> int:
    """Return the distance between two positions."""
    return int(((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2) ** 0.5)

def find_dot(position: tuple, dot_rad: int):
    """Find a dot close to the position."""
    for dot in dots:
        if distance(position, dots[dot]) <= dot_rad:
            return dot

def add_dot():
    """Add a dot to the graph."""
    global dot_name
    mouse_position = pg.mouse.get_pos()
    if find_dot(mouse_position, dot_radius*2) is None:
        dots[str(dot_name)] = mouse_position
        graph.add_vertex(str(dot_name))
        dot_name += 1

def select_dot():
    """Try to find a dot and select or unselect it."""
    mouse_position = pg.mouse.get_pos()
    dot = find_dot(mouse_position, dot_radius)
    if dot in selected:
        selected.remove(dot)
    elif dot is not None:
        selected.append(dot)

def rem_selected():
    """Remove selected dots from the graph."""
    for dot in selected:
        del dots[dot]
        graph.rem_vertex(dot)
    selected.clear()

def connect_dots():
    """Add or remove an edge between two dots."""
    if len(selected) == 2:
        first, second = selected
        if not graph.rem_edge(first, second):
            graph.add_edge(first, second, distance(dots[first], dots[second]))

def escape():
    """Undo selection."""
    if selected:
        selected.clear()


# Functionality
Keys(Halt(add_dot, key_cooldown), pg.K_a)
Keys(Halt(select_dot, key_cooldown), pg.K_s)
Keys(Halt(escape, key_cooldown), pg.K_ESCAPE)
Keys(Halt(rem_selected, key_cooldown), pg.K_d, pg.K_DELETE)
Keys(Halt(connect_dots, key_cooldown), pg.K_c, pg.K_e)


executing = True
while executing:
    for el in pg.event.get():
        if el.type == pg.QUIT:
            executing = False

    keyboard = pg.key.get_pressed()
    check_all()
    tick_all()

    main_window.fill(background)
    # edges and their weights
    for edge in graph.get_edges():
        pg.draw.line(main_window, edge_color, dots[edge[0]], dots[edge[1]], edge_width)
        number = number_font.render(str(graph.get_weight(edge[0], edge[1])), True, edge_number_color)
        center = (round((dots[edge[0]][0] + dots[edge[1]][0])/2), round((dots[edge[0]][1] + dots[edge[1]][1])/2))
        main_window.blit(number, number.get_rect(center=center))
    # main dots
    for dot, pos in dots.items():
        pg.draw.circle(main_window, dot_color, pos, dot_radius)
        number = number_font.render(dot, True, dot_number_color)
        main_window.blit(number, number.get_rect(center=(pos[0], pos[1]-1)))
    # selected dots
    for dot in selected:
        pg.draw.circle(main_window, selected_color, dots[dot], dot_radius)
        number = number_font.render(dot, True, selected_number_color)
        main_window.blit(number, number.get_rect(center=(dots[dot][0], dots[dot][1]-1)))

    pg.display.update()
    timer.tick(FPS)
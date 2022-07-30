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
dot_color = (100, 100, 255)
dot_number_color = (0, 255, 0)
edge_color = (100, 200, 255)
edge_number_color = (255, 200, 100)
path_color = (255, 100, 100)
selected_color = (200, 0, 255)
selected_number_color = (255, 255, 255)
text_on_colour = (100, 255, 100)
text_off_colour = (150, 50, 100)
# sizes
edge_width = 4
path_width = 6
dot_radius = 15
move_speed = 1
# fonts
number_font = pg.font.SysFont("Comic Sans MS", dot_radius*2)
def_font = "Arial"
def_text_size = 40

# Data
graph = Graph()
dots = {}
dot_name = 0
path = []
path_distance = 0
selected = []
to_tick = []
to_check = []
to_select = []
keyboard = pg.key.get_pressed() # For later use
edge_mode = False


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


class Keys:
    """Call the function when the given keys are pressed."""
    def __init__(self, func, *keys: tuple, block: bool = True) -> None:
        self.func = func
        self.keys = keys
        self.block = block
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
        """Check the keys and return True if not block, else False."""
        if self.key_check(self.keys):
            self.func(*args, **kwargs)
            if self.block:
                return True
        return False


class Select:
    """Call given function when given number of dots were selected."""
    def __init__(self, func, number: int, block: bool = True, stop = lambda: False) -> None:
        self.func = func
        self.number = number
        self.block = block
        self.stop = stop
        to_select.append(self)

    def check(self):
        """return True if not block, else False."""
        if self.stop():
            to_select.remove(self)
        if len(selected) == self.number:
            self.func()
            if self.block:
                return True
        return False


def tick_all():
    for func in to_tick:
        func.tick()

def check_all():
    for func in to_check:
        if func.check():
            break
    for func in to_select:
        if func.check():
            break


# Main functions
def save(save_as: str = None):
    """Save the graph."""
    if not save_as:
        save_as = f"graphs/{ctime()}.json".replace(':', '-')
    with open(save_as, "w") as file:
        json.dump([dot_name, dots, graph.graph], file)
    print("Saved to ", save_as)

def load(path: str = None):
    """Load some graph."""
    global dot_name, dots, graph
    selected.clear()
    if not path:
        path = input("What file to open: ")
    with open(path, 'r') as file:
        dot_name, dots, graph.graph = json.load(file)
    print("Loaded from ", path)


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

def select_all():
    """Select all dots in the graph."""
    global selected
    selected = list(dots.keys())

def move(x: int = 0, y: int = 0):
    """Move selected dots."""
    for dot in selected:
        dots[dot] = (dots[dot][0] + x, dots[dot][1] + y)

def rem_selected():
    """Remove selected dots from the graph."""
    for dot in selected:
        del dots[dot]
        graph.rem_vertex(dot)
        if dot in path:
            path.clear()
            print("The path was cleared as it had a removed dot")
    print("Removed:", selected)
    selected.clear()


def edge_mode_func():
    """Add or remove an edge between two dots."""
    first, second = selected
    if not graph.rem_edge(first, second):
        graph.add_edge(first, second, distance(dots[first], dots[second]))
    selected.remove(selected[0])

def toggle_edge_mode():
    """Enable or disable edge mode."""
    global edge_mode
    if edge_mode:
        edge_mode = False
        print("Edge mode off")
    else:
        edge_mode = True
        print("Edge mode on")
        Select(edge_mode_func, 2, stop=lambda: not edge_mode)

def dijkstras_algorithm():
    """Count shortest path using Dijkstra's algorithm."""
    global path_distance, path
    start, end = selected
    result = graph.dijkstras_algorithm(start, end)
    path_distance = result[end][0]
    path = [end]
    while path[-1] != start:
        if result[path[-1]][1] == '-':
            path_distance = "Not connected!"
            break
        path.append(result[path[-1]][1])
    selected.clear()
    print(path_distance, path[::-1])

def escape():
    """Unselect selected, quit edge_mode, clear path, remove Select classes."""
    global edge_mode, to_check
    if selected:
        selected.clear()
    elif edge_mode:
        edge_mode = False
        print("Edge mode off")
    elif to_select:
        # to_select.clear() should do, but may cause problems.
        for func in to_select:
            func.stop = lambda: True
    elif path:
        path.clear()

def text(font: str, size: int, color: tuple, content: str) -> pg.Surface:
    """Return rendered text."""
    return pg.font.SysFont(font, size).render(content, True, color)


# Functionality
Keys(Halt(lambda: Select(dijkstras_algorithm, 2, True, lambda: len(selected) == 2), key_cooldown), pg.K_j)
Keys(Halt(save, key_cooldown), [pg.K_LCTRL, pg.K_s])
Keys(Halt(load, key_cooldown), [pg.K_LCTRL, pg.K_l])
Keys(Halt(select_all, key_cooldown), [pg.K_LCTRL, pg.K_a])
Keys(Halt(escape, key_cooldown), pg.K_ESCAPE)
Keys(Halt(add_dot, key_cooldown), pg.K_a)
Keys(Halt(select_dot, key_cooldown), pg.K_s)
Keys(Halt(rem_selected, key_cooldown), pg.K_d, pg.K_DELETE)
Keys(Halt(toggle_edge_mode, key_cooldown), pg.K_c, pg.K_e)
Keys(lambda: move(0, -move_speed), pg.K_UP, block=False)
Keys(lambda: move(0, move_speed), pg.K_DOWN, block=False)
Keys(lambda: move(-move_speed, 0), pg.K_LEFT, block=False)
Keys(lambda: move(move_speed, 0), pg.K_RIGHT, block=False)

edge_mode_on_text = text(def_font, def_text_size, text_on_colour, "Edge mode")
edge_mode_off_text = text(def_font, def_text_size, text_off_colour, "Edge mode")
selection_on_text =  text(def_font, def_text_size, text_on_colour, "Pending selection")
selection_off_text =  text(def_font, def_text_size, text_off_colour, "Pending selection")

load("graphs/Sat Jul 30 09-13-52 2022.json")  # Feel like this should to be here.

# Main cycle.
executing = True
while executing:
    for el in pg.event.get():
        if el.type == pg.QUIT:
            executing = False

    keyboard = pg.key.get_pressed()
    check_all()
    tick_all()

    main_window.fill(background)
    # edges
    edges = graph.get_edges()
    for edge in edges:
        pg.draw.line(main_window, edge_color, dots[edge[0]], dots[edge[1]], edge_width)
    # path edges
    for i in range(len(path)-1):
        pg.draw.line(main_window, path_color, dots[path[i]], dots[path[i+1]], path_width)
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
    # weight of the edges
    for edge in edges:
        number = number_font.render(str(graph.get_weight(edge[0], edge[1])), True, edge_number_color)
        center = (round((dots[edge[0]][0] + dots[edge[1]][0])/2), round((dots[edge[0]][1] + dots[edge[1]][1])/2))
        main_window.blit(number, number.get_rect(center=center))
    # text
    if edge_mode:
        main_window.blit(edge_mode_on_text, edge_mode_on_text.get_rect(right=W-5))
    else:
        main_window.blit(edge_mode_off_text, edge_mode_off_text.get_rect(right=W-5))
    # Selection
    main_window.blit(selection_on_text if to_select else selection_off_text, (5,0))
    # Path length
    if path_distance:
        txt = text(def_font, def_text_size, text_on_colour, str(path_distance))
        main_window.blit(txt, txt.get_rect(centerx = W/2))

    pg.display.update()
    timer.tick(FPS)
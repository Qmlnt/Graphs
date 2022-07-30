# Graphs
Pygame script to build graphs and analyze them
_____
## Controls
- Mouse position is being used:
  - `A` to add a dot.[^1]
  - `S` to select or unselect a dot.
- Needs selection:
  - `D` or `Delete` to delete selected dots and all edges to them.
  - `E` or `C` to toggle edge mode.[^2]
  - `J` to use Dijkstra's algorithm.[^3]
  - Arrows to move selected dots.
- Independent:
  - `Esc` to escape.[^4]
  - `Ctrl`+`A` to select all.
- Terminal being used:
  - `Ctrl`+`S` to save the graph.
  - `Ctrl`+`L` to load the graph.[^5]

[^1]: Will not add the dot if it would collide with the other dot.
[^2]: Select two dots and they will connect/disconnect, the last dot will remain selected, so one can choose another dot and they will connect/disconnect, and so on.
[^3]: Select two dots and Dijkstra's algorithm will find the shortest distance and its path.
[^4]: Uselect / disable edge mode / disable all pending selections / clear path.
[^5]: Don't want to load? Enter anything other than an existing path.

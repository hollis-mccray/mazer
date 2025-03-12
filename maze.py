from graphics import Cell
import random
import time

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1= y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed != None:
            random.seed(seed)

        self._create_cells()

    def _create_cells(self):
        for i in range(self._num_cols):
            column = [Cell(self._win) for j in range(self._num_rows)]
            self._cells.append(column)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)

    def _draw_cell(self, i, j):
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = self._x1 + (i + 1) * self._cell_size_x
        y2 = self._y1 + (j + 1) * self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            if i - 1 > -1 and self._cells[i - 1][j].visited == False:
                to_visit.append("left")
            if i + 1 < self._num_cols and self._cells[i + 1][j].visited == False:
                to_visit.append("right")
            if j - 1 > -1 and self._cells[i][j - 1].visited == False:
                to_visit.append("up")
            if j + 1 < self._num_rows and self._cells[i][j + 1].visited == False:
                to_visit.append("down")
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            else:
                direction = random.choice(to_visit)
                print(f"{i}, {j}, {direction}")
                match direction:
                    case "left":
                        self._cells[i][j].has_left_wall = False
                        self._cells[i - 1][j].has_right_wall = False
                        self._draw_cell(i, j)
                        self._break_walls_r(i - 1, j)
                    case "right":
                        self._cells[i][j].has_right_wall = False
                        self._cells[i + 1][j].has_left_wall = False
                        self._draw_cell(i, j)
                        self._break_walls_r(i + 1, j)
                    case "up":
                        self._cells[i][j].has_top_wall = False
                        self._cells[i][j - 1].has_bottom_wall = False
                        self._draw_cell(i, j)
                        self._break_walls_r(i, j - 1)
                    case "down":
                        self._cells[i][j].has_bottom_wall = False
                        self._cells[i][j + 1].has_top_wall = False
                        self._draw_cell(i, j)
                        self._break_walls_r(i, j + 1)
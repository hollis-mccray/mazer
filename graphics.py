from tkinter import Tk, BOTH, Canvas
import time

class Window():

    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "The Amazing Mazer"
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)

        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        x1 = self.p1.x
        y1 = self.p1.y
        x2 = self.p2.x
        y2 = self.p2.y
        canvas.create_line(
            x1, y1, x2, y2, fill=fill_color, width=2
        )

class Cell():
    def __init__(self, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            line =  l = Line(
                Point(self._x1, self._y1),
                Point(self._x1, self._y2)
            )
            self._win.draw_line(l, "black")
        if self.has_right_wall:
            line =  l = Line(
                Point(self._x2, self._y1),
                Point(self._x2, self._y2)
            )
            self._win.draw_line(l, "black")
        if self.has_top_wall:
            line =  l = Line(
                Point(self._x1, self._y1),
                Point(self._x2, self._y1)
            )
            self._win.draw_line(l, "black")
        if self.has_bottom_wall:
            line =  l = Line(
                Point(self._x1, self._y2),
                Point(self._x2, self._y2)
            )
            self._win.draw_line(l, "black")

    def draw_move(self, to_cell, undo=False):
        p1 = Point(
           (self._x1 + self._x2) // 2,
           (self._y1 + self._y2) // 2,
        )
        p2 = Point(
           (to_cell._x1 + to_cell._x2) // 2,
           (to_cell._y1 + to_cell._y2) // 2,
        )
        if undo:
            color = "grey"
        else:
            color = "red"
        move = Line(p1, p2)
        self._win.draw_line(move, color)

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
    ):
        self._x1 = x1
        self._y1= y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._create_cells()

    def _create_cells(self):
        self._cells = []
        for i in range(self._num_cols):
            column = [Cell(self._win) for j in range(self._num_rows)]
            self._cells.append(column)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self.draw_cell(i, j)

    def _draw_cell(self, i, j):
        x1 = self._x1 + i * self._cell_size_x
        x2 = self._x1 + (i + 1) * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        y2 = self._y1 + (j + 1) * self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(.05)

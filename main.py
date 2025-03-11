from graphics import Window, Line, Point, Cell


def main():
    win = Window(800, 600)
    c = Cell(win)
    c.has_bottom_wall = False
    c.draw(50, 50, 100, 100)
    c2 = Cell(win)
    c2.has_top_wall = False
    c2.draw(50, 100, 100, 150)
    c.draw_move(c2, True)

    win.wait_for_close()

main()

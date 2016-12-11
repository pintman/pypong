import tkinter
import threading


class Sprite:
    """Ein Sprite ist ein Objekt auf dem Canvas, das bewegt werden kann."""
    def __init__(self, canvas, position, width_height):
        self.canvas = canvas
        self.rect = self.canvas.create_rectangle(position[0], position[1],
                                                 position[0] + width_height[0],
                                                 position[1] + width_height[1],
                                                 fill="black")

    def start(self):
        """Starte den Sprite."""
        self._tick()

    def _tick(self):
        self.update()
        th = threading.Thread(target=self._tick)
        th.start()

    def ueberlappt_mit(self, anderer_sprite):
        """Prüft, ob der Sprite mit dem anderen Sprite überlappt."""
        raise NotImplementedError() # TODO
        x_y_this = self.position()
        x_y_that = anderer_sprite.position()

        self.canvas.find_overlapping()

    def position(self):
        return self.canvas.coords(self.rect)

    def update(self):
        """Diese Methode muss von den ableitenden Klassen überschrieben werden.
        In jedem Zyklus wird sie einmal aufgerufen."""

        raise Exception("Muss überschrieben werden!")

    def bewegen(self, delta_x, delta_y):
        """Bewege den Sprite um (delta_x, delta_y). Positive Werte bewegen nach
        rechts, negative Werte nach links."""

        print(delta_x, delta_y)
        self.canvas.move(self.rect, delta_x, delta_y)


class Schlaeger(Sprite):
    def __init__(self, canvas, position):
        super().__init__(canvas, position, (10, 50))

    def update(self):
        pass

    def hoch(self):
        self.bewegen(0, -10)
        
    def runter(self):
        self.bewegen(0, +10)


class Ball(Sprite):
    def __init__(self, canvas, position):
        super().__init__(canvas, position, (10, 10))
        self.dir = (1, 0)

    def update(self):
        self.bewegen(self.dir[0], self.dir[1])


class Pong:
    def __init__(self):
        self.fenster = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.fenster)
        self.canvas.pack()

        self.schlaeger_links = Schlaeger(self.canvas, (0, 10))
        self.schlaeger_links.start()
        self.schlaeger_rechts = Schlaeger(self.canvas, (200, 10))
        self.schlaeger_rechts.start()

        self.ball = Ball(self.canvas, (10, 100))
        self.ball.start()

        btn = tkinter.Button(self.fenster, text="^", command=self.btn_up_click)
        btn.pack()        
        btn = tkinter.Button(self.fenster, text="v",
                             command=self.schlaeger_links.runter)
        btn.pack()        

        self.fenster.mainloop()

    def btn_up_click(self):
        self.schlaeger_links.hoch()
        
pong = Pong()

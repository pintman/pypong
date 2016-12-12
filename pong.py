import tkinter
import threading
import random
import eapi.hw


class Sprite:
    """Ein Sprite ist ein Objekt auf dem Canvas, das bewegt werden kann."""
    def __init__(self, canvas, position, width_height):
        self.canvas = canvas
        self.rect = self.canvas.create_rectangle(position[0], position[1],
                                                 position[0] + width_height[0],
                                                 position[1] + width_height[1],
                                                 fill="black")

    def start(self):
        """Starte den Sprite. In jedem Zyklus wird die update-Methode
        aufgerufen. Hier muss der Sprite seine eigentliche Arbeit leisten."""

        self._tick()

    def _tick(self):
        self.update()
        th = threading.Thread(target=self._tick)
        th.start()

    def finde_ueberlappung(self):
        """Prüft, ob der Sprite mit anderen Sprites überlappt und gibt diese
        zurück."""

        coords = self.position()
        elemente = self.canvas.find_overlapping(*coords)

        # sich selbst von der Überlappung ausnehmen
        return [e for e in elemente if e != self.rect]

    def position(self):
        """Liefert die Koordinaten in Form von vier Punkten."""
        return self.canvas.coords(self.rect)

    def update(self):
        """Diese Methode muss von den ableitenden Klassen überschrieben werden.
        Nach dem Aufruf von start, wird diese Methode in jedem Zyklus einmal
        aufgerufen."""

        raise Exception("Muss überschrieben werden!")

    def bewegen(self, delta_x, delta_y):
        """Bewege den Sprite um (delta_x, delta_y). Positive Werte bewegen nach
        rechts, negative Werte nach links."""

        self.canvas.move(self.rect, delta_x, delta_y)

    def spielfeld_breite_hoehe(self):
        """Liefert Breite und Höhe des Spielfeldes."""
        breite = int(self.canvas["width"])
        hoehe = int(self.canvas["height"])

        return breite, hoehe

    def innerhalb_spielfeld(self):
        """Prüft, ob der Sprite innerhalb des Spielfeldes ist."""
        b, h = self.spielfeld_breite_hoehe()
        x1, y1, x2, y2 = self.position()

        return (0 <= x1 <= b and
                0 <= y1 <= h and
                0 <= x2 <= b and
                0 <= y2 <= h)


class Schlaeger(Sprite):
    def __init__(self, canvas, ea_modul, position):
        super().__init__(canvas, position, (10, 50))
        self.ea_modul = ea_modul

    def update(self):
        """Bewegt den Schläger hoch oder runter. Verlässt der Schläger hierbei
        den sichtbaren Bereich, wird die Bewegung in der entgegen gesetzten
        Richtung korrigiert."""

        if self.ea_modul.taster_gedrueckt(0):
            self.hoch()
            if not self.innerhalb_spielfeld():
                self.runter()

        if self.ea_modul.taster_gedrueckt(1):
            self.runter()
            if not self.innerhalb_spielfeld():
                self.hoch()

    def hoch(self):
        self.bewegen(0, -10)
        
    def runter(self):
        self.bewegen(0, +10)


class Ball(Sprite):
    def __init__(self, canvas, position):
        super().__init__(canvas, position, (10, 10))
        self.direction = [1,
                          # y-Komponente zufällig wählen
                          random.randint(-100, 100) / 100
                          ]

    def update(self):
        self.bewegen(self.direction[0], self.direction[1])

        if self._beruehrt_wand_oben_unten():
            self.direction[1] *= -1

        elemente = self.finde_ueberlappung()
        if len(elemente) > 0:
            self.direction[0] *= -1
            self.direction[1] *= -1

    def _beruehrt_wand_oben_unten(self):
        breite, hoehe = self.spielfeld_breite_hoehe()

        return (self.position()[0] < 0 or
                self.position()[0] > breite or
                self.position()[1] < 0 or
                self.position()[1] > hoehe)


class Pong:
    def __init__(self, eamodul_links, eamodul_rechts, breite=300, hoehe=200):
        fenster = tkinter.Tk()
        canvas = tkinter.Canvas(fenster, width=breite, height=hoehe)
        canvas.pack()

        schlaeger_links = Schlaeger(canvas, eamodul_links, (0, hoehe/2))
        schlaeger_links.start()
        schlaeger_rechts = Schlaeger(canvas, eamodul_rechts,
                                     (breite-10, hoehe/2))
        schlaeger_rechts.start()

        ball = Ball(canvas, (breite/2, hoehe/2))
        ball.start()

        btn = tkinter.Button(fenster, text="<- ^", command=schlaeger_links.hoch)
        btn.pack()        
        btn = tkinter.Button(fenster, text="<- v",
                             command=schlaeger_links.runter)
        btn.pack()        

        btn = tkinter.Button(fenster, text="^ ->",
                             command=schlaeger_rechts.hoch)
        btn.pack()
        btn = tkinter.Button(fenster, text="v ->",
                             command=schlaeger_rechts.runter)
        btn.pack()

        fenster.mainloop()


def main():
    eam_links = eapi.hw.EAModul()
    eam_rechts = eapi.hw.EAModul()
    pong = Pong(eamodul_links=eam_links, eamodul_rechts=eam_rechts)

if __name__ == "__main__":
    main()

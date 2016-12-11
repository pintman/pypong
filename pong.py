import tkinter

class Schlaeger:
    def __init__(self, canvas):
        self.canvas = canvas
        self.rect = self.canvas.create_rectangle(10,200,20,200-50,
                                                 fill="black")

    def hoch(self):
        self.canvas.move(self.rect, 0, -10) # move rectangle up
        
    def runter(self):
        self.canvas.move(self.rect, 0, +10) # move rectangle down

class Pong:
    def __init__(self):
        self.fenster = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.fenster)
        self.canvas.pack()

        self.schlaeger = Schlaeger(self.canvas)

        btn = tkinter.Button(self.fenster, text="^", command=self.btn_up_click)
        btn.pack()        
        btn = tkinter.Button(self.fenster, text="v", command=self.schlaeger.runter)
        btn.pack()        

        self.fenster.mainloop()

    def btn_up_click(self):
        self.schlaeger.hoch()
        
pong = Pong()


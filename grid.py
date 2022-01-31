import csv
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, RIGHT

root = Tk()
root.title('Kakuro')
root.geometry('500x500')

        filetypes = (
            ('Fichier csv', '*.csv'),
            ('Tous les fichiers', '*.*')
        )

# layout all of the main containers
root.grid_rowconfigure(9, weight=1)
root.grid_columnconfigure(9, weight=1)
center.grid(row=1, sticky="nsew")

# create the center widgets
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)

cells = {}
for row in range(9):
    for column in range(9):
        cell = Frame(center, bg='white', highlightbackground="black",
                     highlightcolor="black", highlightthickness=1,
                     width=50, height=50,  padx=3,  pady=3)
        cell.grid(row=row, column=column)
        cells[(row, column)] = cell

root.mainloop()

#def main():
#    a = Grid(r"C:\Users\nolan\OneDrive\Bureau\kakuro_ex.csv")
class Case_vide:
        def __init__(self, x ,y, valeur, sumx, sumy):
            self.x=x
            self.y=y
            self.valeur=valeur
            self.sumx=sumx
            self.sumy=sumy

class Grid:
    def __init__(self, path):
        with open(path, newline='') as f:
            reader = csv.reader(f)
            grid = [[elt.split("\\") for elt in row] for row in reader]
            for i in grid:
                print(i)
    
if __name__ == '__main__':
    main()

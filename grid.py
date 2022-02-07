import csv
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, RIGHT, Label, LabelFrame
from tkinter.filedialog import askopenfilename
from functools import partial


class Case_vide:
    def __init__(self, x, y, valeur, sumx, sumy):
        self.x = x
        self.y = y
        self.valeur = valeur
        self.sumx = sumx
        self.sumy = sumy


class Grid:
    def __init__(self):
        self.root = Tk()
        self.root.title('Kakuro')

        self.label_kakuro = Label(self.root, text="Kakuro")
        self.label_kakuro.grid(row=0, column=0)

        self.bouton_kakuro = Button(self.root, text="Jouer !", command=self.jeu_debut)
        self.bouton_kakuro.grid(row=1, column=0)

    def jeu_debut(self):
        self.label_kakuro.destroy()
        self.bouton_kakuro.destroy()

        filetypes = (
            ('Fichier csv', '*.csv'),
            ('Tous les fichiers', '*.*')
        )

        filename = askopenfilename(title='Ouvrez une grille', initialdir='%USERPROFILE%/Desktop', filetypes=filetypes)

        with open(filename, "r") as file:
            reader = csv.reader(file)
            grid = [[elt.split("\\") for elt in row] for row in reader]
            self.cases_modifiables = []  # format : (lig, col)
            self.cases_sommes = []  # format : (somme, "v"/"h", lig, col)
            for lig in range(len(grid)):
                for col in range(len(grid[lig])):
                    if grid[lig][col] == [" ", " "]:  # la case est grise sans somme, on ignore
                        continue
                    elif grid[lig][col] == [" "]:  # la case est blanche, on peut la modifier
                        self.cases_modifiables.append((lig, col))
                    else:
                        if grid[lig][col][0] != [" "]:
                            self.cases_sommes.append((grid[lig][col][0], 'v', lig, col))
                        if grid[lig][col][1] != [" "]:
                            self.cases_sommes.append((grid[lig][col][1], 'h', lig, col))

        # création du conteneur de toutes les cells
        self.center = Frame(self.root, bg='white', width=450, height=450, padx=3, pady=3)

        # create the center widgets
        self.center.grid(row=1, sticky="nsew")
        self.center.grid_rowconfigure(0, weight=1)
        self.center.grid_columnconfigure(1, weight=1)

        self.cells = {}  # format (row, column) : (Frame, Case|Canvas)
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if (row, column) in self.cases_modifiables:
                    cell = Frame(self.center, bg='white', highlightbackground="black",
                                 highlightcolor="black", highlightthickness=1,
                                 width=50, height=50, padx=3, pady=3)
                    cell.grid(row=row, column=column)
                    case = ""
                    self.cells[(row, column)] = (cell, case)
                else:
                    cell = Frame(self.center, bg='gray', highlightbackground="black",
                                 highlightcolor="black", highlightthickness=1,
                                 width=50, height=50)
                    cell.grid(row=row, column=column)
                    canvas = Canvas(cell, bg='gray', borderwidth=0, highlightthickness=0,
                                    width=48, height=48)
                    canvas.grid()
                    self.cells[(row, column)] = (cell, canvas)


def click(Btn):
    # test the button command click
    s = "Button %s clicked" % Btn
    root.title(s)


# creation de la frame pour le numpad
# relief='groove' and labelanchor='nw' are default
lf = LabelFrame(root, text=" numpad ", bd=3) #deplacer pour root
lf.pack(padx=15, pady=10)

# liste avec les buttons
Btn_list = [
    '7', '8', '9',
    '4', '5', '6',
    '1', '2', '3',
    '', 'erase', '']
# cree et positionne les buttons
r = 1  # row
c = 0  # column
n = 0
Btn = list(range(len(Btn_list)))
for label in Btn_list:
    # partial takes care of function and argument
    cmd = partial(click, label)
    # cree les buttons
    Btn[n] = tk.Button(lf, text=label, width=5, command=cmd)
    # positionne les buttons
    Btn[n].grid(row=r, column=c)
    # augmentaion de l'index du boutton
    n = n + 1
    # diposition column et row
    c = c + 1
    if c > 3:
        c = 0
        r = r + 1


def main():
    a = Grid()  # r"C:\Users\nolan\OneDrive\Bureau\kakuro_ex.csv")
    a.root.mainloop()


if __name__ == '__main__':
    main()

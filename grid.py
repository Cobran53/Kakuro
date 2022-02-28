import csv
from tkinter import Tk, LabelFrame, Canvas, Frame, Button, Label, StringVar, Entry
from tkinter.filedialog import askopenfilename
from functools import partial


class Grid:
    def __init__(self):
        self.root = Tk()
        self.root.title('Kakuro')

        self.label_kakuro = Label(self.root, text="Kakuro", font=("Arial", 15, "bold"))
        self.label_kakuro.grid(row=0, column=0)

        self.label_directory = Label(self.root, text="Dossier des niveaux :")
        self.var_directory = StringVar(value=expanduser(r"~\Desktop"))
        self.entry_directory = Entry(self.root, textvariable=self.var_directory, width=50)
        self.bouton_parcourir = Button(self.root, text="Parcourir", command=self.parcourir)
        self.label_directory.grid(row=1, column=0)
        self.entry_directory.grid(row=2, column=0)
        self.bouton_parcourir.grid(row=3, column=0)

        self.bouton_kakuro = Button(self.root, text="Jouer !", command=self.jeu_debut)
        self.bouton_kakuro.grid(row=4, column=0)

    def parcourir(self):
        directory = askdirectory(title="Ouvrez le dossier contenant les niveaux", initialdir=self.var_directory.get(),
                                 mustexist=True)
        self.var_directory.set(directory)

    def jeu_debut(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        filetypes = (
            ('Fichier csv', '*.csv'),
            ('Tous les fichiers', '*.*')
        )

        filename = askopenfilename(title='Ouvrez une grille', initialdir=self.var_directory.get(), filetypes=filetypes)

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
                        if grid[lig][col][0] not in ([" "], "", " "):
                            self.cases_sommes.append((grid[lig][col][0], 'v', lig, col))
                        if grid[lig][col][1] not in ([" "], "", " "):
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
                    case = Case_vide(row, column, cell)
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

        for somme in self.cases_sommes:
            if somme[1] == "h":
                self.cells[(somme[2], somme[3])][1].create_text(40, 25, text=str(somme[0]), state="disabled",
                                                                font=("Segoe UI", 10, "bold"))
                self.cells[(somme[2], somme[3])][1].create_line(48, 0, 24, 24, 48, 48, width=3, joinstyle="miter")
                horizontal = somme[3] + 1
                while (somme[2], horizontal) in self.cases_modifiables and horizontal != 9:
                    self.cells[(somme[2], horizontal)][1].sumx = somme[0]
                    horizontal += 1
                if horizontal != 9:
                    self.cells[(somme[2], horizontal)][1].create_text(7, 25, text=str(somme[0]), state="disabled",
                                                                      font=("Segoe UI", 10, "bold"))
                    self.cells[(somme[2], horizontal)][1].create_line(0, 0, 24, 24, 0, 48, width=3, joinstyle="miter")
            elif somme[1] == "v":
                self.cells[(somme[2], somme[3])][1].create_text(25, 40, text=str(somme[0]), state="disabled",
                                                                font=("Segoe UI", 10, "bold"))
                self.cells[(somme[2], somme[3])][1].create_line(0, 48, 24, 24, 48, 48, width=3, joinstyle="miter")
                vertical = somme[2] + 1
                while (vertical, somme[3]) in self.cases_modifiables and vertical != 9:
                    self.cells[(vertical, somme[3])][1].sumy = somme[0]
                    vertical += 1
                if vertical != 9:
                    self.cells[(vertical, somme[3])][1].create_text(25, 7, text=str(somme[0]), state="disabled",
                                                                    font=("Segoe UI", 10, "bold"))
                    self.cells[(vertical, somme[3])][1].create_line(0, 0, 24, 24, 48, 0, width=3, joinstyle="miter")


class Case_vide:
    def __init__(self, x, y, parent, valeur="", sumx=0, sumy=0):
        self.x = x
        self.y = y
        self.valeur = valeur
        self.sumx = sumx
        self.sumy = sumy
        self.canvas = Canvas(parent, bg='white', borderwidth=0, highlightthickness=0, width=42, height=42)
        self.canvas.bind('<Button-1>', self.canvas_click_event)
        self.canvas.pack()

    def canvas_click_event(self, event):
        self.canvas.create_oval(event.x, event.y, event.x + 5, event.y + 5)

    def draw(self, numero):
        dico = {1: ((10, 32, 32, 32), (21, 32, 21, 10), (21, 10, ))}


def click(Btn):
    # test the button command click
    s = "Button %s clicked" % Btn
    Tk.title(s)


# creation de la frame pour le numpad
# relief='groove' and labelanchor='nw' are default
lf = LabelFrame(Tk(), text=" numpad ", bd=3) #deplacer pour root
lf.pack(padx=15, pady=10)

# liste avec les buttons
Btn_list = [
    '7', '8', '9',
    '4', '5', '6',
    '1', '2', '3',
    'accueil', 'effacer', 'option']
# cree et positionne les buttons
r = 1  # row
c = 0  # column
n = 0
Btn = list(range(len(Btn_list)))
for label in Btn_list:
    # partial takes care of function and argument
    cmd = partial(click, label)
    # cree les buttons
    Btn[n] = Button(lf, text=label, width=5, command=cmd)
    # positionne les buttons
    Btn[n].grid(row=r, column=c)
    # augmentaion de l'index du boutton
    n = n + 1
    # diposition column et row
    c = c + 1
    if c > 2:
        c = 0
        r = r + 1


def main():
    a = Grid()  # r"C:\Users\nolan\OneDrive\Bureau\kakuro_ex.csv")
    a.root.mainloop()


if __name__ == '__main__':
    main()

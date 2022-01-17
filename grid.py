import csv


class Grid:
    def __init__(self, path):
        with open(path, newline='') as f:
            reader = csv.reader(f)
            grid = [[elt.split("\\") for elt in row] for row in reader]
            for i in grid:
                print(i)


def main():
    a = Grid(r"C:\Users\nolan\OneDrive\Bureau\kakuro_ex.csv")


if __name__ == '__main__':
    main()

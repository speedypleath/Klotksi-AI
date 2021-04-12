import copy
class Table:
    """
    Tabla ce reprezinta o configuratie a jocului
    n: Numarul de linii (am incercat sa o fac variabila statica) 
    m: Numarul de coloane
    tiles: Matrice de nXm care reprezinta tabla propriu-zisa
    """ 
    m = 5
    n = 4

    def __init__(self, tiles):
        self.tiles = tiles

    def __str__(self):
        rez = ""
        for line in self.tiles:
            for x in line:
                rez += x
            rez += '\n'
        return rez

    def __eq__(self, other):
        return self.tiles == other.tiles

    def special_block(self):
        """Functie care gaseste pozitia blocului special

        Returns:
            O lista cu casutele pe care se afla blocul special
        """ 
        block = []
        for i in range(self.__class__.n):
            for j in range(self.__class__.m):
                if self.tiles[i][j] == '*':
                    block.append((i, j))
        return block

    def blocks(self):
        """Functie care gaseste blocurile de pe tabla curenta

        Returns:
            Un dictionar in care cheile sunt numele blocurilor iar valorile sunt casutele pe care acestea se afla
        """ 
        blocks = dict()
        for i in range(self.__class__.n):
            for j in range(self.__class__.m):
                if self.tiles[i][j] not in ['*', '.', '#']:
                    if not blocks.get(self.tiles[i][j]):
                        blocks[self.tiles[i][j]] = []
                    blocks[self.tiles[i][j]].append((i, j))
        return blocks

    def down(self, key, value):
        """Functie care muta un bloc in jos
        Args:
            key: Numele blocului mutat
            value: Casutele pe care se afla blocul

        Returns:
            O tabla noua cu blocul mutat daca aceasta poate fi generata, altfel nimic
        """ 
        new_table = Table(copy.deepcopy(self.tiles))
        value.sort(key=lambda x: x[0], reverse=True)
        for i, j in value:
            if i == self.__class__.n - 1 and key != '*':
                return None
            if new_table.tiles[i + 1][j] in ['.', key] or i == self.__class__.n - 1:
                if i != self.__class__.n - 1:
                    new_table.tiles[i + 1][j] = key
                new_table.tiles[i][j] = '.'
            else:
                return None
        return new_table

    def up(self, key, value):
        """Functie care muta un bloc in sus
        Args:
            key: Numele blocului mutat
            value: Casutele pe care se afla blocul

        Returns:
            O tabla noua cu blocul mutat daca aceasta poate fi generata, altfel nimic
        """ 
        new_table = Table(copy.deepcopy(self.tiles))
        value.sort(key=lambda x: x[0])
        for i, j in value:
            if i == 0 and key != '*':
                return None
            if new_table.tiles[i - 1][j] in ['.', key] or i == 0:
                if i != 0:
                    new_table.tiles[i - 1][j] = key
                new_table.tiles[i][j] = '.'
            else:
                return None
        return new_table

    def right(self, key, value):
        """Functie care muta un bloc la dreapta
        Args:
            key: Numele blocului mutat
            value: Casutele pe care se afla blocul

        Returns:
            O tabla noua cu blocul mutat daca aceasta poate fi generata, altfel nimic
        """ 
        new_table = Table(copy.deepcopy(self.tiles))
        value.sort(key=lambda x: x[1], reverse=True)
        for i, j in value:
            if j == 0 and key != '*':
                return None
            if new_table.tiles[i][j + 1] in ['.', key]:
                if j != 0:
                    new_table.tiles[i][j + 1] = key
                new_table.tiles[i][j] = '.'
            else:
                return None
        return new_table

    def left(self, key, value):
        """Functie care muta un bloc la stanga
        Args:
            key: Numele blocului mutat
            value: Casutele pe care se afla blocul

        Returns:
            O tabla noua cu blocul mutat daca aceasta poate fi generata, altfel nimic
        """ 
        new_table = Table(copy.deepcopy(self.tiles))
        value.sort(key=lambda x: x[1])
        for i, j in value:
            if j == self.__class__.m - 1 and key != '#':
                return None
            if new_table.tiles[i][j - 1] in ['.', key]:
                if j != self.__class__.m - 1:
                    new_table.tiles[i][j - 1] = key
                new_table.tiles[i][j] = '.' if self.tiles[i][j + 1] != key else key
            else:
                return None
        return new_table
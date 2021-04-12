from Table import Table
class NodParcurgere:
    """
    Informatii despre un nod din arborele de parcurgere (nu din graful initial)
    info: O tabla care reprezinta configuratia nodului
    parinte: Nodul format din configuratie in care lipseste ultima mutare
    g, h, f: semnificatiile standard din curs
    """ 
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.f = self.g + self.h

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return sir

    def __str__(self):
        sir = str(self.info)
        sir += '->'
        while self.parinte is not None:
            nod = self.parinte
            sir += str(nod.info) + '->'
        return sir

    def __eq__(self, other):
        return self.info == other.info

    def __gt__(self, other):
        return self.f > other.f

    def __hash__(self):
        return hash(str(self.info))

    def contine_in_drum(self, info_nod_nou):
        """Functie care verifica daca un nod se afla in drumul nodului curent
        Args:
            info_nod_nou: Nodul verificat

        Returns:
            True daca nodul se gaseste in drum, False altfel
        """ 
        nod_drum = self
        while nod_drum is not None:
            if info_nod_nou == nod_drum.info:
                return True
            nod_drum = nod_drum.parinte

        return False

    def obtine_drum(self):
        """Functie care obtine drumul catre nodul curent

        Returns:
            O lista cu toate nodurile din drumul pana la nodul curent
        """ 
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afis_drum(self):
        """Functie care afiseaza drumul catre nodul curent

        Returns:
            Un string ce contine drumul catre nodul curent, gata de afisat
        """ 
        l = self.obtine_drum()
        rez = ""
        for i in range(len(l)):
            rez += str(i) + ": (cost " + str(l[i].g) + ")\n"
            rez += str(l[i].info)
        return rez


class Graph:
    """
    Graful problemei
    start: Configuratie initiala, preluata din fisierul de input
    iesire: O lista care contine blocurile ce formeaza iesirea
    """ 
    def __init__(self, nume_fisier):
        f = open(nume_fisier, 'r')
        aux = f.read().split("\n")
        for i in range(len(aux)):
            aux[i] = list(aux[i])
        Table.n = len(aux)
        Table.m = len(aux[0])
        self.start = Table(aux)
        self.iesire = self.gaseste_iesire()

    def gaseste_iesire(self):
        """Functie care determina unde se afla iesirea din grid
        """ 
        nod = self.start.tiles
        m = len(nod) - 1
        for i in range(len(nod[0])):
            if nod[0][i] != '#':
                return (0, i), (0, nod[0].index('#', i) - 1)
            if nod[m][i] != '#':
                return (m, i), (m, nod[m].index('#', i) - 1)
        n = len(nod[0]) - 1
        for i in range(m + 1):
            if nod[i][0] != '#':
                start = i
                while nod[i][0] != '#':
                    i += 1
                return (start, 0), (i - 1, 0)
            elif nod[i][n] != '#':
                start = i
                while nod[i][n] != '#':
                    i += 1
                return (start, n), (i - 1, n)

    def testeaza_scop(self, nod_curent):
        """Functie care testeaza daca s-a gasit o solutie
        Args:
            nod_curent: Nodul care este evaluat

        Returns:
            True daca nodul este nod scop, False altfel
        """ 
        for i, j in self.iesire:
            if nod_curent.tiles[i][j] != '*':
                return False
        return True

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def move(self, nod_curent, key, block, tip_euristica, cost_mutare):
        """Functie care muta un bloc in fiecare directie
        Args:
            nod_curent: Nodul pentru care sunt generati succesorii
            key: Numele blocului care este mutat
            block: Pozitiile pe care se afla blocul
            tip_euristica: Numele euristicii alese
            cost_mutare: Costul pentru a muta blocul ales

        Returns:
            O lista care contine blocul mutat in fiecare directie posibila
        """ 
        rez = []
        if a := nod_curent.info.up(key, block):
            nod_nou = NodParcurgere(a, nod_curent, nod_curent.g + cost_mutare,
                                    self.calculeaza_h(nod_curent.info, tip_euristica))
            if not nod_curent.contine_in_drum(nod_nou.info):
                rez.append(nod_nou)
        if a := nod_curent.info.right(key, block):
            nod_nou = NodParcurgere(a, nod_curent, nod_curent.g + cost_mutare,
                                    self.calculeaza_h(nod_curent.info, tip_euristica))
            if not nod_curent.contine_in_drum(nod_nou.info):
                rez.append(nod_nou)
        if a := nod_curent.info.down(key, block):
            nod_nou = NodParcurgere(a, nod_curent, nod_curent.g + cost_mutare,
                                    self.calculeaza_h(nod_curent.info, tip_euristica))
            if not nod_curent.contine_in_drum(nod_nou.info):
                rez.append(nod_nou)
        if a := nod_curent.info.left(key, block):
            nod_nou = NodParcurgere(a, nod_curent, nod_curent.g + cost_mutare,
                                    self.calculeaza_h(nod_curent.info, tip_euristica))
            if not nod_curent.contine_in_drum(nod_nou.info):
                rez.append(nod_nou)
        return rez

    def genereaza_succesori(self, nod_curent, tip_euristica):
        """Functie care genereaza succesori
        Args:
            nod_curent: Nodul pentru care sunt generati succesorii
            tip_euristica: Numele euristicii alese

        Returns:
            Lista de succesori ai nodului expandat
        """ 
        lista_succesori = []
        blocks = nod_curent.info.blocks()
        for key in blocks:
            lista_succesori.extend(self.move(nod_curent, key, blocks[key], tip_euristica, len(blocks[key])))
        rez = self.move(nod_curent, '*', nod_curent.info.special_block(), tip_euristica, 1)
        lista_succesori.extend(rez)

        return lista_succesori

    def calculeaza_h(self, nod, tip_euristica="euristica banala"):
        """Functie care calculeaza h
        Args:
            nod: Nodul care este evaluat
            tip_euristica: Numele euristicii alese

        Returns:
            h
        """   
        if tip_euristica == "euristica banala":
            if not self.testeaza_scop(nod):
                return 1
            return 0
        elif tip_euristica == "distanta manhattan":
            #euristica admisibila 
            value = nod.special_block()
            distance = float('inf')
            for i, j in value:
                for x, y in self.iesire:
                    distance = min(distance, abs(x - i) + abs(y - j))
            return distance
        elif tip_euristica == "nivel":
            #euristica admisibila 
            return self.level(nod) - 2
        elif tip_euristica == "numar blocuri":
            #euristica admisibila
            return self.level(nod) - 2 + self.blocks_no(nod) 
        elif tip_euristica == "blocuri langa":
            #euristica neadmisibila(input 5)
            value = nod.special_block()
            nr_blocuri = 0
            for i, j in value:
                if nod.tiles[i - 1][j] not in ['.', '#']:
                    nr_blocuri += 1
                if nod.tiles[i + 1][j] not in ['.', '#']:
                    nr_blocuri += 1
                if nod.tiles[i][j - 1] not in ['.', '#']:
                    nr_blocuri += 1
                if nod.tiles[i][j + 1] not in ['.', '#']:
                    nr_blocuri += 1
            return nr_blocuri
        else:
            raise Exception("Euristica invalida: " + tip_euristica)

    def blocks_no(self, nod):
        value = nod.special_block()
        nr_blocuri = 0
        a = float("inf")
        b = 0
        c = self.level(nod)
        for i, j in self.iesire:
            if nod.tiles[i][j] != '.':
                nr_blocuri += 1
            a = min(j, a)
            b = max(j, b)
            
        for i, j in value:
            a = min(j, a)
            b = max(j, b)
        
        for i in range(1, c):
            for j in range(a, b):
                if nod.tiles[i][j] not in ['.', '#']:
                    nr_blocuri += 1
        return nr_blocuri

    def level(self, nod):
        """Functie care determina nivelul blocului special fata de iesire
        (probabil ar fi fost mai usor sa rotesc la inceput tabla in loc sa verific de fiecare data in ce directie e iesirea dar acum e prea tarziu)

        Args:
            nod: Nodul care este evaluat

        Returns:
            Nivelul blocului special fata de iesire
        """      
        value = nod.special_block()
        if self.iesire[0][0] == 0:
            value.sort(key=lambda x: x[0])
            return value[-1][0]
        elif self.iesire[0][0] == nod.__class__.n - 1:
            value.sort(key=lambda x: x[0], reverse=True)
            return nod.__class__.n - value[-1][0]
        elif self.iesire[0][1] == 0:
            value.sort(key=lambda x: x[0])
            return value[-1][1]
        elif self.iesire[0][1] == nod.__class__.n - 1:
            value.sort(key=lambda x: x[0], reverse=True)
            return nod.__class__.m - value[-1][0]

    def exit_direction(self, nod):
        """Functie care determina in ce directie se afla iesirea

        Args:
            nod: Nodul care va fi mutat spre iesire

        Returns:
            Directia in care trebuie mutat nodul
        """
        if self.iesire[0][0] == 0:
            return nod.info.up
        elif self.iesire[0][0] == nod.__class__.n - 1:
            return nod.info.down
        elif self.iesire[0][1] == 0:
            return nod.info.left
        elif self.iesire[0][1] == nod.__class__.n - 1:
            return nod.info.right

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir
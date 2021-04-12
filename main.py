from PrioritySet import PrioritySet
from Table import Table
from Graph import Graph, NodParcurgere
import time
import os
import sys
def move_out(gr, nod_curent):
    """Functie care muta blocul special inafara gridului, atunci cand acesta se afla pe iesire

    Args:
        gr: Graful programului
        nod_curent: Solutia gasita

    Returns:
        Un nod nou format prin mutarea blocului special in directia iesirii pana cand acesta iese din grid
    """
    direction = gr.exit_direction(nod_curent)
    while nod_curent.info.special_block() != []:
        parent = NodParcurgere(direction('*', nod_curent.info.special_block()), nod_curent, nod_curent.g + 1,
                     gr.calculeaza_h(nod_curent.info, tip_euristica))
        nod_curent = parent
        direction = gr.exit_direction(nod_curent)
    return nod_curent


def check_timeout(start_time, timeout):
    """Functie care verifica daca algoritmul a intrat in timeout

    Args:
        start_time: Timpul la care a fost inceputa cautarea solutiei actuale
        timeout: Timpul maxim setat pentru timeout

    Returns:
        un mesaj in cazul in care s-a intrat in timeout, altfel nimic
    """
    rez = ""
    if time.time() - start_time > timeout:
        rez += "Timeout...\n"
        return rez
    return None


def uniform_cost(gr, nr_solutii_cautate, tip_euristica, timeout):
    """UCS

    Args:
        gr: Graful programului
        nr_solutii_cautate: Numarul de solutii cautate
        tip_euristica: Acest parametru nu este folosit pt UCS
        timeout: Timpul maxim de timeout

    Returns:
        Solutia problemei sub forma unui string
    """
    c = [NodParcurgere(gr.start, None, 0)]
    rez = ""
    start_time = time.time()
    nr_iteratii = 0
    while len(c)>0:
        nr_iteratii += 1
        check = check_timeout(start_time, timeout)
        if check is not None:
            return check
        nod_curent=c.pop(0)
        if gr.testeaza_scop(nod_curent.info):
            rez += "Solutie: " + '\n'
            rez += move_out(gr, nod_curent).afis_drum() + '\n'
            rez += "\n----------------\n"
            rez += str(nr_iteratii) + ' iteratii in ' + str(time.time() - start_time) + ' sec\n'
            start_time = time.time()
            nr_solutii_cautate-=1
            if nr_solutii_cautate==0:
                return rez
            continue
        l_succesori=gr.genereaza_succesori(nod_curent)

        for s in l_succesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].g>=s.g :
                    gasit_loc=True
                    break
            if gasit_loc:
                c.insert(i,s)
            else:
                c.append(s)

    return "fara solutii"


def a_star(gr, nr_solutii_cautate, tip_euristica, timeout):
    """A*(optimizat)

    Args:
        gr: Graful programului
        nr_solutii_cautate: Acest parametru nu este folosit pt A*
        tip_euristica: Numele euristicii alese
        timeout: Timpul maxim de timeout

    Returns:
        Solutia problemei sub forma unui string
    """
    start_time = time.time()
    rez = ""
    c = PrioritySet()
    closed = set()
    c.add(NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start)), 0)
    nr_iteratii = 0
    while not c.empty():
        check = check_timeout(start_time, timeout)
        if check is not None:
            return check
        nod_curent = c.pop()
        closed.add(nod_curent)
        nr_iteratii += 1
        if gr.testeaza_scop(nod_curent.info):
            rez += "Solutie: " + '\n'
            rez += move_out(gr, nod_curent).afis_drum() + '\n'
            rez += "\n----------------\n"
            rez += str(nr_iteratii) + ' iteratii in ' + str(time.time() - start_time) + ' sec\n'
            return rez
        l_succesori = gr.genereaza_succesori(nod_curent, tip_euristica=tip_euristica)

        for s in l_succesori:
            if s not in closed:
                c.add(pri=s.f, d=s)

    return "fara solutii"


def a_star_multiplesol(gr, nr_solutii_cautate, tip_euristica, timeout):
    """A* cu solutii multiple(neoptimizat)

    Args:
        gr: Graful programului
        nr_solutii_cautate: Numarul de solutii cautate
        tip_euristica: Numele euristicii alese
        timeout: Timpul maxim de timeout

    Returns:
        Solutia problemei sub forma unui string
    """
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    rez = ""
    start_time = time.time()
    nr_iteratii = 0
    while len(c)>0:
        nr_iteratii += 1
        check = check_timeout(start_time, timeout)
        if check is not None:
            return check
        nod_curent=c.pop(0)
        if gr.testeaza_scop(nod_curent.info):
            rez += "Solutie: " + '\n'
            rez += move_out(gr, nod_curent).afis_drum() + '\n'
            rez += "\n----------------\n"
            rez += str(nr_iteratii) + ' iteratii in ' + str(time.time() - start_time) + ' sec\n'
            start_time = time.time()
            nr_solutii_cautate-=1
            if nr_solutii_cautate==0:
                return rez
            continue
        l_succesori=gr.genereaza_succesori(nod_curent)

        for s in l_succesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].f>=s.f :
                    gasit_loc=True
                    break
            if gasit_loc:
                c.insert(i,s)
            else:
                c.append(s)

    return "fara solutii"


def a_star_iterativ(gr, nr_solutii_cautate, tip_euristica, timeout):
    pass


def menu():
    """Meniu de selectare pentru algoritmul utilizat, numarul de solutii si euristica folosita

    Returns:
        algoritmul utilizat, numarul de solutii si euristica folosita
    """
    nr_solutii_cautate = None
    while True:
        print("Selecteaza algoritm:\n1.UCS\n2.A*\n3.A*_nsol\n4.IDA*\n")
        optiune = input()
        if optiune in ["UCS", '1']:
            algoritm = uniform_cost
            break
        elif optiune in ["A*", '2']:
            algoritm = a_star
            nr_solutii_cautate = 1
            break
        elif optiune in ["A*_nsol", '3']:
            algoritm = a_star_multiplesol
            break
        elif optiune in ["IDA*", '4']:
            algoritm = a_star_iterativ
            nr_solutii_cautate = 1
            break
        else:
            print("Optiunea nu e valabila !!")
    if nr_solutii_cautate is None:
        while True:
            print("Alege numarul de solutii:")
            optiune = input()
            try:
                nr_solutii_cautate = int(optiune)
                break
            except ValueError:
                print("Nu este un numar !!")
    if algoritm != uniform_cost:
        while True:
            print("Selecteaza euristica:\n1.euristica banala\n2.distanta manhattan\n3.nivel\n4.numar blocuri\n")
            optiune = input()
            if optiune in ["euristica banala", '1']:
                tip_euristica = "euristica banala"
                break
            elif optiune in ["distanta manhattan", '2']:
                tip_euristica = "distanta manhattan"
                break
            elif optiune in ["nivel", '3']:
                tip_euristica = "nivel"
                break
            elif optiune in ["numar blocuri", '4']:
                tip_euristica = "numar blocuri"
                break
            else:
                print("Optiunea nu e valabila !!")
    else:
        tip_euristica = "euristica banala"
    return algoritm, nr_solutii_cautate, tip_euristica


if __name__ == '__main__':
    algoritm, nr_solutii_cautate, tip_euristica = menu()
    src = sys.argv[1]
    dest = sys.argv[2]
    timeout = sys.argv[3]
    lista_fisiere = os.listdir(src)
    for nume_fisier in lista_fisiere:
        gr = Graph(src + '/' + nume_fisier)
        f = open(dest + '/' + nume_fisier, 'w')
        if gr.start.special_block() == []:
            f.write("Starea initiala e stare finala \n" + 
            str(NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start)).afis_drum()))
        else:
            rez = algoritm(gr, nr_solutii_cautate, tip_euristica, float(timeout))
            f.write(rez)
        f.close()

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
        rez += "Timeout... " + str(time.time() - start_time) + " sec\n"
        return rez
    return None


def construieste_drum(gr, nod_curent, tip_euristica, limita, nr_solutii_cautate, start_time, nr_iteratii, return_string, timeout):
    """DFS pentru IDA*

    Args:
        gr: Graful programului
        nod_curent: Nodul expandat
        tip_euristica: Numele euristicii selectate
        limita: Inaltimea maxima pana la care este expandat nodul
        start_time: Timpul la care a fost inceputa cautarea solutiei actuale
        nr_iteratii: Numarul de noduri expandate
        return_string: Solutia problemei sub forma unui string

    Returns:
        nr_solutii_cautate: Numarul de solutii cautate, actualizat in cazul in care s-a gasit o solutie
        rez: Un mesaj care notifica terminarea algoritmului in cazul in care s-au gasit toate solutiile, altfel limita noua de adancime
        nr_iteratii: Numarul de noduri expandate (necesar pentru a actualiza valoarea recursiv)
        return_string: Solutia problemei sub forma unui string (necesar pentru a actualiza valoarea recursiv)
    """
    check = check_timeout(start_time, timeout)
    if check is not None:
        return 0, "gata", check, nr_iteratii
    l_succesori = []
    if nod_curent.f > limita:
        return nr_solutii_cautate, nod_curent.f, return_string, nr_iteratii
    if gr.testeaza_scop(nod_curent.info) and nod_curent.f == limita:
        return_string += "Solutie: " + '\n'
        aux = move_out(gr, nod_curent)
        return_string += aux.afis_drum() + '\n'
        return_string += "\n----------------\n"
        return_string += str(nr_iteratii) + ' iteratii in ' + str(time.time() - start_time) + ' sec\n'
        return_string += "----------------\n\n"
        return_string += "numarul maxim de noduri din memorie: " + str(len(aux.obtine_drum())) + '\n'
        start_time = time.time()
        nr_solutii_cautate-=1
        if nr_solutii_cautate == 0:
            return 0, "gata", return_string, nr_iteratii
    else:
        nr_iteratii += 1
        l_succesori = gr.genereaza_succesori(nod_curent, tip_euristica)	
    minim = float('inf')
    for s in l_succesori:
        nr_solutii_cautate, rez, return_string, nr_iteratii = construieste_drum(gr, s, tip_euristica, limita, nr_solutii_cautate, start_time, nr_iteratii, return_string, timeout)
        if rez == "gata":
            return 0, "gata", return_string, nr_iteratii
        if rez < minim:
            minim = rez
    return nr_solutii_cautate, minim, return_string, nr_iteratii


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
    max_memory = 1
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
            rez += "----------------\n\n"
            rez += "numarul maxim de noduri din memorie: " + str(max_memory) + '\n'
            start_time = time.time()
            nr_solutii_cautate -= 1
            if nr_solutii_cautate == 0:
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
        max_memory = max(max_memory, len(c))
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
    max_memory = 1
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
            rez += "numarul maxim de noduri din memorie: " + str(max_memory) + '\n'
            return rez
        l_succesori = gr.genereaza_succesori(nod_curent, tip_euristica=tip_euristica)

        for s in l_succesori:
            if s not in closed:
                c.add(pri=s.f, d=s)
        max_memory = max(max_memory, len(c))
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
    max_memory = 1
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
            rez += "numarul maxim de noduri din memorie: " + str(max_memory) + '\n'
            rez += "----------------\n\n"
            start_time = time.time()
            nr_solutii_cautate-=1
            if nr_solutii_cautate==0:
                return rez
            continue
        l_succesori=gr.genereaza_succesori(nod_curent, tip_euristica)

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
        max_memory = max(max_memory, len(c))
    return "fara solutii"


def a_star_iterativ(gr, nr_solutii_cautate, tip_euristica, timeout):
    """IDA*

    Args:
        gr: Graful programului
        nr_solutii_cautate: Numarul de solutii cautate
        tip_euristica: Numele euristicii alese
        timeout: Timpul maxim de timeout

    Returns:
        Solutia problemei sub forma unui string
    """
    start_time = time.time()
    return_string = ""
    nod_start = NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))
    nr_iteratii = 0
    limita = nod_start.f
    while True:
        check = check_timeout(start_time, timeout)
        if check is not None:
            return check
        nr_solutii_cautate, rez, return_string, nr_iteratii = construieste_drum(gr, nod_start, tip_euristica, limita, nr_solutii_cautate, start_time, nr_iteratii, return_string, timeout)
        if rez == "gata":
            break
        if rez==float('inf'):
            return_string = "fara solutii"
            break
        limita = rez
    return return_string

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
            print("Selecteaza euristica:\n1.euristica banala\n2.distanta manhattan\n3.nivel\n4.numar blocuri\n5.blocuri langa\n")
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
            elif optiune in ["blocuri langa", '5']:
                tip_euristica = "blocuri langa"
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

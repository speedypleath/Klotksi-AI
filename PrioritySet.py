import heapq
class HeapContainer(object):
    """
    Container pentru elementele unei cozi de prioritati
    value: Valoarea elementului
    priority: Prioritatea elementului
    (am adaugat acest container pentru a putea redefini operatorii de comparatie, nu stiu sincer dc nu mergea cu tupluri)
    """ 
    def __init__(self, priority, value):
        self.priority = priority
        self.value = value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

class PrioritySet(object):
    """
    Coada de prioritati cu elemente distince
    heap: Coada de prioritati propriu-zisa
    set: Container utilizat pentru a testa daca un element se afla deja in coada
    (am folosit-o pentru a implementa A* optimizat, clasa e partial luata de pe net partial implementata de mine(~70%))
    """ 
    def __init__(self):
        self.heap = []
        self.set = set()

    def add(self, d, pri):
        """Functie care adauga un element in container. In caz ca elementul se afla deja in coada se incearca actualizarea prioritatii
        Args:
            d: Valoarea elementului adaugat
            pri: Prioritatea elementului adaugat
        """ 
        if d not in self.set:
            heapq.heappush(self.heap, HeapContainer(pri, d))
            self.set.add(d)
        else:
            for i, x in enumerate(self.heap):
                if x.value == d:
                    self.heap[i] = x if x.priority < pri else HeapContainer(pri, d)

    def pop(self):
        """Functie care scoate ultimul element din container

        Returns:
            Valoarea ultimului element din container
        """ 
        x = heapq.heappop(self.heap)
        self.set.remove(x.value)
        return x.value

    def empty(self):
        """Functie care verifica daca containerul actual este gol

        Returns:
            True daca containerul este gol, False altfel
        """ 
        return len(self.heap) == 0

    def __len__(self):
        return len(self.heap)
import functools
from BCU.BSF import Nodo

def compara(x, y):
    return x.get_costo() - y.get_costo()
def buscar_solucion_UCS(conexiones, estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inicial)
    nodo_inicial.set_costo(0)
    nodos_frontera.append(nodo_inicial)
    while not solucionado and len(nodos_frontera) != 0:
        nodos_frontera = sorted(nodos_frontera, key=functools.cmp_to_key(compara))
        nodo = nodos_frontera[0]
        nodos_visitados.append(nodos_frontera.pop(0))
        if nodo.get_datos() == solucion:
            solucionado = True
            return nodo
        else:
            dato_nodo = nodo.get_datos()
            lista_hijos = []
            for un_hijo in conexiones.get(dato_nodo, {}):                
                hijo = Nodo(un_hijo)
                coste = conexiones[dato_nodo][un_hijo]
                hijo.set_costo(nodo.get_costo() + coste)
                hijo.set_padre(nodo)
                lista_hijos.append(hijo)
                
                if not hijo.en_lista(nodos_visitados):
                    if hijo.en_lista(nodos_frontera):               
                        for n in nodos_frontera:
                            if n.igual(hijo) and n.get_costo() > hijo.get_costo():
                                nodos_frontera.remove(n)
                                nodos_frontera.append(hijo)
                    else:
                        nodos_frontera.append(hijo)
                
                nodo.set_hijos(lista_hijos)
    
    return None  

class Nodo:
    def __init__(self, datos, padre=None):
        self.datos = datos
        self.padre = padre
        self.hijos = []
        self.coste = 0
    
    def set_costo(self, coste):
        self.coste = coste
    
    def get_costo(self):
        return self.coste
    
    def set_hijos(self, hijos):
        self.hijos = hijos
    
    def get_hijos(self):
        return self.hijos
    
    def set_padre(self, padre):
        self.padre = padre
    
    def get_padre(self):
        return self.padre
    
    def get_datos(self):
        return self.datos
    
    def igual(self, nodo):
        return self.get_datos() == nodo.get_datos()
    
    def en_lista(self, lista_nodos):
        for n in lista_nodos:
            if self.igual(n):
                return True
        return False

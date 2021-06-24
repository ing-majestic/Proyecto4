from graphviz import Digraph
import random
from collections import defaultdict
from heapq import *

#lista de pares key/value
padre = dict()
costos = dict()


class Graphviz():

    #constructor
    def __init__(self, name):
        self.graphvis = {}
        self.name = str(name)
        self.dot = Digraph(name,comment='The Round Graph')
    #Función que agrega nodo con etiqueta para generar el archivo GV y PNG
    def agregaNodol(self,v,et,el):
        vs = str(v)
        es = str(et)
        ex = str(el)
        self.dot.node(vs, es, xlabel= ex)
    #Función que agrega nodo sin etiqueta para generar el archivo GV y PNG
    def agregaNodo(self,v,et):
        vs = str(v)
        es = str(et)
        self.dot.node(vs, es)
    #Función que permite crear la lista en formato adecuado
    def listaedges(self,l2,a,b):
        c = str(a) + str(b)
        l2.append(c)
    #funcion que agrega arista por arista con una variable c con valor false o true
    def agregaedge(self, a, b, f):
        c = str(a)
        d = str(b)
        e = str(f)
        self.dot.edge(c , d, constraint='false', label = e)
    #Función que permite agregar la lista de conexiónes
    def agregaedges(self,l2):
        self.dot.edges(l2)
    #Función encargada de generar el archivo GV como el PNG
    def imprimegrafo(self, nodos):
        #print('-------Impresion y generacion GV de Grafo')
        self.dot.format = 'png'
        a ='Graphviz-output/'
        b = a + str(self.name)+'_'+str(nodos)+'.gv'
        self.dot.render(b, view = True)
        #print(self.dot.source) #doctest: +NORMALIZE_WHITESPACE

class Vertice:
    #Se definen los verices del grafo
    def __init__(self, i):
        self.id = i
        self.vecinos = []
        self.visitado = False
        self.padre = None
        self.distancia = float('inf')

    def agregarVecino(self, v, p):
        if v not in self.vecinos:
            self.vecinos.append([v, p])

#BUSCAR ARBOL MINIMO

#crea listas key/value con los nodos y asigna costos
def armar_serie(nodo):
    padre[nodo] = nodo
    costos[nodo] = 0

#busca el nodo padre del ingresado y lo retorna
def buscar(nodo):
    if padre[nodo] != nodo:
        padre[nodo] = buscar(padre[nodo])
    return padre[nodo]

#toma la desicion de tomar los nodos con la menor arista
def unir(nodo1, nodo2):

    #toma la raiz de cada nodo
    raiz1 = buscar(nodo1)
    raiz2 = buscar(nodo2)
    #corrobora que el padre de los nodos sea distinto para no crear ciclos
    if raiz1 != raiz2:
        #Comprueba que el costo que almacena la llave costos[raiz1] sea mayor
        #de serlo, se almacena raiz1 en la llave padre[raiz2]
        if costos[raiz1] > costos[raiz2]:

            #asigna un nodo el nodo de destino a la tupla
            #si raiz1 == A y raiz2 == C se almacena en la lista padre el valor "C:A"
            padre[raiz2] = raiz1

        else:
            padre[raiz1] = raiz2

            if costos[raiz1] == costos[raiz2]:
                costos[raiz2] += 1

#BUSCAR ARBOL MINIMO  kruskal
def kruskal(grafo, N):
    k = Graphviz("1_Kruskal_")


    for nodo in grafo['nodos']:
        armar_serie(nodo)

    arbol_minimo = list()
    #transforma las aristas en listas
    aristas = list(grafo['aristas'])
    #ordena las aristas de menos a mayor
    aristas.sort()
    lcostos = []

    #recorre las aristas ordenadas
    for arista in aristas:
        costo, nodo1, nodo2 = arista

        if buscar(nodo1) != buscar(nodo2):
            unir(nodo1, nodo2)
            #agrega la arista a la lista
            arbol_minimo.append(arista)
            k.agregaedge(nodo1, nodo2, costo)
            lcostos.append(costo)
    costo_total = sum(lcostos)
    print("Kruskal MTS: ",costo_total)
    k.imprimegrafo(N)
    #print(lcostos)
    return arbol_minimo

#BUSCAR ARBOL MINIMO

def prim( grafo, N ):
    k = Graphviz("2_PRIM_")
    #crea listas en base a un indice comun, en este caso los indices seran los nodos 1 y 2
    #en cada indice se almacena la tupla (c, n1, n2)
    conn = defaultdict( list )
    for c,n1,n2 in grafo['aristas']:
        #direccionamiento
        conn[ n1 ].append( (c, n1, n2) )
        conn[ n2 ].append( (c, n2, n1) )

    recorrido = []
    lcostos = []
    #toma el nodo inicial
    usado = set( grafo['nodos'][0] )
    #toma las aristas que contienen el nodo inicial
    nueva_arista = conn[ grafo['nodos'][0] ][:]

    #mantiene en la posicion 0 el menor valor de la lista
    heapify( nueva_arista )

    while nueva_arista:
        #saca el primer valor de la lista y lo almacena en costo, n1, n2
        costo, n1, n2 = heappop( nueva_arista )
        #pregunta si el nodo final de la arista no ha sido visitado
        if n2 not in usado:
            usado.add( n2 )
            #agrega la arista al recorrido
            recorrido.append( ( costo, n1, n2  ) )
            k.agregaedge(n1, n2, costo)
            lcostos.append(costo)
            #print "recorrido",recorrido

            #recorre la lista de nodos invertidos y en caso de que no se aya pasado por el nodo lo agrega a la lista de aristas.
            for e in conn[ n2 ]:
                # e[2] corresponde al "nodo de llegada"
                if e[ 2 ] not in usado:
                    #agrega "e" a nueva_arista
                    heappush( nueva_arista, e )
    costo_total = sum(lcostos)
    print("Prim MTS: ",costo_total)
    k.imprimegrafo(N)
    return recorrido

#diccionario
g = Graphviz('1_primary')
#Pide el numero de nodos que tendra el Grafo
print ("-----GRAFO PRINCIPAL------")
print ("Ingresa el numero de nodos: ")
N = int(input())
node = str(N)
l = list(range(1,N+1))
b= [str(x) for x in l]
l2 = []

for v in b:
    g.agregaNodo(v,v)

for i in b:
    random.shuffle(b)
    x = random.randint(1,len(b)/2)
    for i in range(0, x - 1, 2):
        a = b[i]
        c = b[i + 1]
        #Pesos aleatorios por arista para calculo de dikstra
        lab = random.randrange(30)
        #agregan aristas al grafo
        l2.append((lab, a, c))
        #Se genera la lista para el archivo GV
        g.agregaedge(a, c, lab)

grafo = {
        'nodos': b,
        'aristas': l2
        }

g.imprimegrafo(N)
print("nodos: ", b)
print("aristas: ", l2)
print ("kruskal: ", kruskal(grafo, N))
print ("prim: ", prim(grafo, N))
print("nodos: ", b)
print("aristas: ", l2)

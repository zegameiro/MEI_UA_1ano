# -*- coding: utf-8 -*-

# main.py

from simplegraph import SimpleGraph

# menu
def menu():
    print("*** MENU ***")
    print("1. Listar Triplos")
    print("2. Filtrar Triplos")
    print("3. Pesquisar Triplos")
    print("---------------------")
    print("4. Carregar Grafo")
    print("5. Guardar Grafo")
    print("6. Fundir Grafos")
    print("---------------------")
    print("7. Inserir Novo Triplo")
    print("8. Remover Triplo")
    print("---------------------")
    print("0. Sair")
    print("---------------------")
    return int(input("Opcao: "))


def listgraph():
    print("Listar Triplos")
    _graph.printAllTriples()


def filtergraph():
    print("Filtrar Triplos")
    sub = input("Sujeito: ")
    if len(sub)==0: sub = None
    pred = input("Predicado: ")
    if len(pred)==0: pred = None
    obj = input("Objeto: ")
    if len(obj)==0: obj = None
    t = _graph.triples(sub, pred, obj)
    SimpleGraph.printTriples(t)


def search():
    print("Nomes dos realizadores de filmes.")
    lista = _graph.query( [('?film','directed_by', '?real'),
                           ('?real','name','?realname')
                           ] )
    conj = set()
    for a in lista:
        conj.add(a['realname'])
    for a in sorted(conj):
        print(a)

def search_all_movies():
    print("Nome de todos os filmes.")
    lista = _graph.query([('?film', 'directed_by', '?director'),
                          ('?film', 'name', '?name')
                          ])
    for a in lista:
        print(a['name'])

def search_director_film():
    print("Realizador de um dado filme (Top Gun).")
    lista = _graph.query([('?film', 'name', 'Top Gun'),
                          ('?film', 'directed_by', '?director'),
                          ('?director', 'name', '?directorname')
                        ])
    for a in lista:
        print(a['directorname'])

def search_actors_film():
    print("Atores de um dado filme (Top Gun).")
    lista = _graph.query([('?film', 'name', 'Top Gun'),
                          ('?film', 'starring', '?actor'),
                          ('?actor', 'name', '?actorname')
                        ])
    for a in lista:
        print(a['actorname'])

def search_movies_director():
    print("Lista de filmes de um dado realizador (Tony Scott).")
    lista = _graph.query([('?director', 'name', 'Tony Scott'),
                          ('?film', 'directed_by', '?director'),
                          ('?film', 'name', '?filmname')
                        ])
    for a in lista:
        print(a['filmname'])

def search_movies_actor():
    print("Lista de filmes onde entra um dado ator (Tom Cruise).")
    lista = _graph.query([('?actor', 'name', 'Tom Cruise'),
                          ('?film', 'starring', '?actor'),
                          ('?film', 'name', '?filmname')
                        ])
    for a in lista:
        print(a['filmname'])

def search_actors_director_movies():
    print("Lista de atores orientados por um dado realizador e em que filmes (Tony Scott).")
    lista = _graph.query([('?director', 'name', 'Tony Scott'),
                          ('?film', 'directed_by', '?director'),
                          ('?film', 'starring', '?actor'),
                          ('?actor', 'name', '?actorname'),
                          ('?film', 'name', '?filmname')
                        ])
    for a in lista:
        print("Actor Name: ", a['actorname'], " Film Name: ", a['filmname'])

def search_director_actor_movies():
    print("Lista de realizadores que já orientaram um dado ator e em que filmes (Tom Cruise).")
    lista = _graph.query([('?actor', 'name', 'Tom Cruise'),
                          ('?film', 'starring', '?actor'),
                          ('?film', 'directed_by', '?director'),
                          ('?director', 'name', '?directorname'),
                          ('?film', 'name', '?filmname')
                        ])
    for a in lista:
        print("Director Name: ", a['directorname'], " Film Name: ", a['filmname'])

def loadgraph():
    print("Carregar Grafo")
    _graph.load(input("Nome do ficheiro: "))


def storegraph():
    print("Guarda Grafo")
    _graph.save(input("Nome do ficheiro: "))


def mergegraphs():
    print("Fusao de Grafos")
    g = SimpleGraph()
    g.load(input("Nome do ficheiro: "))
    for sub, pred, obj in g.triples(None, None, None):
        _graph.add(sub, pred, obj)


def inserttriple():
    print("Inserir triplo")
    sub = input("Sujeito: ")
    pred = input("Predicado: ")
    obj = input("Objeto: ")
    _graph.add(sub, pred, obj)


def removetriple():
    print("Remover triplo")
    sub = input("Sujeito: ")
    if len(sub) == 0: sub = None
    pred = input("Predicado: ")
    if len(pred) == 0: pred = None
    obj = input("Objeto: ")
    if len(obj) == 0: obj = None
    _graph.remove(sub, pred, obj)


def run(op):
    _funcs[op-1]()


# inicio do modulo
if __name__ == "__main__":
    _funcs = (listgraph, filtergraph, search_actors_director_movies,loadgraph, storegraph, mergegraphs, inserttriple, removetriple)
    _graph = SimpleGraph()

    while(True):
        op = menu()
        if op == 0:
            break
        run(op)


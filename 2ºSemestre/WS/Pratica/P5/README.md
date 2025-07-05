## Queries

### 1. Conjunto de Predicados no Grafo

```sparql
SELECT DISTINCT ?predicate {
    ?s ?predicate ?o
}
ORDER BY ?predicate
```

### 2. Pesquisa de filmes realizados por um Realizador, dado o seu nome

```sparql
PREFIX fb: <http://movies.org/pred/>
SELECT ?movie  
WHERE {
    ?real fb:name "Steven Spielberg" .
    ?film fb:directed_by ?real .
    ?film fb:name ?movie .
}
```

### 3. Pesquisa de atores com participação num filme, dado o seu nome

```sparql
PREFIX fb: <http://movies.org/pred/>
SELECT ?actor_name
WHERE {
    ?film fb:name "The Terminal" .
    ?film fb:starring ?actor .
    ?actor fb:name ?actor_name .
}
```

### 4. Pesquisa de atores com quem um dado realizador trabalhou.

```sparql
PREFIX fb: <http://movies.org/pred/>
SELECT DISTINCT ?actor_name
WHERE {
    ?dir fb:name "Steven Spielberg" .
    ?film fb:directed_by ?dir .
    ?film fb:starring ?actor .
    ?actor fb:name ?actor_name .
}
```

### 5. Pesquisa de atores com quem um dado ator trabalhou.

```sparql
PREFIX fb:<http://movies.org/pred/>
SELECT DISTINCT ?actor_name
WHERE {
    ?actor fb:name "Morgan Freeman" .
    ?film fb:starring ?actor .
    ?film fb:starring ?actor2 .
    ?actor2 fb:name ?actor_name .
    FILTER (?actor != ?actor2)
}
```

### 6. Pesquisa de pessoas com quem um dado ator trabalhou.

```sparql
PREFIX fb:<http://movies.org/pred/>
SELECT DISTINCT ?person_name
WHERE {
    ?actor fb:name "Morgan Freeman" .
    ?film fb:starring ?actor .
    
    ?film fb:starring ?oact .
    ?film fb:directed_by ?dir .
    { ?oact fb:name ?person_name . }
    UNION
    { ?dir fb:name ?person_name . }
    FILTER (?actor != ?oact)
}
```

### 7. Pesquisa de pessoas com quem uma dada pessoa trabalhou.

```sparql
PREFIX fb:<http://movies.org/pred/>
SELECT DISTINCT ?person_name
WHERE {
    ?person fb:name "Steven Spielberg" .
    { ?film fb:starring ?person . }
    UNION
    { ?film fb:directed_by ?person . }
    
    ?film fb:starring ?oact .
    ?film fb:directed_by ?dir .
    { ?oact fb:name ?person_name . }
    UNION
    { ?dir fb:name ?person_name . }
    FILTER (?person != ?oact && ?dir != ?person)
}
```

### 8. Descrição total de um filme, dado o seu nome

```sparql
PREFIX fb:<http://movies.org/pred/>
DESCRIBE ?movie
WHERE {
    ?movie fb:name "Blade Runner" .
}
```




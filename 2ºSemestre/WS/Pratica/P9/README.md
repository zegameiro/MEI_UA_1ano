# Practical class 9

### 1. Lista das entidades (URI e Nome) do tipo “foaf:Person”

```sparql
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX celp: <http://mydata.com/celp/>
PREFIX celc: <http://mydata.com/celc/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?uri ?name
WHERE {
  ?uri a foaf:Person .
  ?uri foaf:name ?name .
}
```

### 2. Lista de entidades (URI) do tipo “foaf:Group” e os nomes das celebridades nesses grupos, ordenada pelas entidades tipo “foaf:Group”

```sparql
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX celp: <http://mydata.com/celp/>
PREFIX celc: <http://mydata.com/celc/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?group ?celebrity ?name
WHERE {
  ?group a foaf:Group ;
        celp:with ?celebrity .
  ?celebrity foaf:name ?name .
}
ORDER BY ?group
```

### 3. Lista de entidades do tipo “foaf:Person” (pessoas) e o valor da sua propriedade “foaf:name” (nome genérico)

```sparql
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX celp: <http://mydata.com/celp/>
PREFIX celc: <http://mydata.com/celc/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?person ?name
WHERE {
  ?person a foaf:Person ;
          foaf:name ?name .
}
```

### 4. Lista de entidades (URI) do tipo “foaf:Group” e o valor da sua propriedade “celp.limit”, ordenada pelas entidades tipo “foaf:Group” e pelo valores de “celp.limit”

```sparql
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX celp: <http://mydata.com/celp/>
PREFIX celc: <http://mydata.com/celc/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?group ?limit
WHERE {
  ?group a foaf:Group ;
         celp:limit ?limit .
}
ORDER BY ?group ?limit
```
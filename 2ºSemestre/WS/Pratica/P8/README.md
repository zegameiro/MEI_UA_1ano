# Practical class 8

### 1. Triplos dos indivíduos com uma propriedade de domínio igual a celc:Celebrity;

```sparql
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX celp: <http://mydata.com/celp/>
PREFIX celc: <http://mydata.com/celc/>

SELECT ?subject ?property ?object
WHERE {
    ?property rdfs:domain celc:Celebrity .
    ?subject ?property ?object .
}
```

### 2. triplos dos indivíduos com uma propriedade de domínio igual a celc:Relationship;

```sparql
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX celp: <http://mydata.com/celp/>
PREFIX celc: <http://mydata.com/celc/>

SELECT ?subject ?property ?object
WHERE {
    ?property rdfs:domain celc:Relationship .
    ?subject ?property ?object .
}
```

### 3. Triplos dos indivíduos ligados a uma propriedade com gama de valores do tipo literal.

```sparql
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX celp: <http://mydata.com/celp/>
PREFIX celc: <http://mydata.com/celc/>

SELECT ?subject ?property ?object
WHERE {
    ?property rdfs:range rdfs:Literal .
    ?subject ?property ?object .
}
```

### 4. Entidades do tipo celc:Celebrity e seus nomes;

```sparql
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX celc: <http://mydata.com/celc/>

SELECT ?subject ?name
WHERE {
    ?subject a celc:Celebrity .
    ?subject dc:title ?name .
}
```

### 5. entidades do tipo celc:Relationship e suas propriedades com valores do tipo literal.

```sparql
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX celc: <http://mydata.com/celc/>

SELECT ?subject ?property
WHERE {
    ?subject a celc:Relationship .
    ?subject ?property ?object .
    ?property rdfs:range rdfs:Literal .
}
```
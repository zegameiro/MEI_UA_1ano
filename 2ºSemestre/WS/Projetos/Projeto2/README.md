# Segundo Projeto Prático para a cadeira de Web Semântica 2024/2025

Este trabalho tem como objetivo dar continuidade ao desenvolvimento do sistema de informação semântico iniciado no TP1, aprofundando a sua complexidade e funcionalidades. Para isso, foi criado uma ontologia detalhada que descreve o domínio dos dados, permitindo classificações automáticas e a inferência de novas relações entre entidades. O sistema foi enriquecido com dados externos provenientes da DBpedia e da Wikidata, bem como pela publicação dos dados nas páginas web do próprio sistema. A implementaçãao recorre a tecnologias como Python/Django, GraphDB, SPARQL, RDF,OWL, Protégé, entre outras, promovendo uma forte integração entre os diferentes components e uma interface mais funcional para o utilizador.

## Nota: 16

## Como executar o projeto

1. Clonar o repositório:
```bash
git clone git@github.com:zegameiro/WS_Second_Assignment.git
```

2. Navegar até ao diretório do projeto, criar um ambiente virtual e instalar as dependências:
```bash
cd WS_Second_Assignment/src
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Construir uma imagem Docker para o GraphDB (se não tiver instalado localmente) através do ficheiro `docker-compose.yml`:
```bash
docker compose up --build
```

4. Aceder ao GraphDB através do link [http://localhost:7200/](http://localhost:7200/), criar um novo repositório com o nome `f1-pitstop` e com um conjunto de regras de inferência do tipo `OWL-Max(Optimized)`.

5. Importar os ficheiros `f1_data.n3` e `f1_ontology.n3` por esta ordem e importar apenas o segundo ficheiro quando o primeiro já estiver completamente carregado.

6. Abrir outro terminal (caso esteja a usar o Docker) e iniciar o servidor Django:
```bash
cd f1-djangoApp
python manage.py runserver
```

7. Aplicação estará disponível no link [http://localhost:8000/](http://localhost:8000/).

## Ficheiros

Os ficheiros que contém os dados semânticos encontram-se no diretório `./WS_2_Proj_107969_108840_109018/src/semantic_data`, estão lá presentes 3 ficheiros:
- `f1_data.n3`, contém os dados do dataset no formato **N3**;
- `f1_ontology.n3`, contém a ontologia definida;
- `f1_data_ontology.n3`, contém a ontologia definida e os dados em formato N3, tudo no mesmo ficheiro.

As regras de inferência SPIN encontram-se no ficheiro `./WS_2_Proj_107969_108840_109018/src/f1-djangoApp/f1App/inference_rules.py`.

## Autores

- [João Andrade](https://github.com/WildBunnie)
- [José Gameiro](https://github.com/zegameiro)
- [Tomás Victal](https://github.com/fungame2270)

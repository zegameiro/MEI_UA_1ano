# Primeiro Projeto Prático para a cadeira de Web Semântica 2024/2025

## Nota: 15

## Overview

O nosso trabalho foca-se no desenvolvimento de um sistema de informação baseado na web, utilizando dados da Fórmula 1. O conjunto de dados que escolhemos abrange informações detalhadas sobre as corridas, temporatas, pilotos, construtores e qualificações para os pilotos e construtores abrangendo desde o início da competição em 1950 até a  temporadamais recente de 2024. Estes dados foram extraídos de um dataset do kaggle e depois foram transformados para o formato N3 com auxílio de um script de python.

## Dataset

[https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)

O conjunto de dados é composto por múltiplos ficheiros CSV que contêm informações detalhadas sobre circuitos, equipas, pilotos, corridas, resultados e estatísticas relacionadas com a Fórmula 1. Sendo estes:

- **circuits.csv**: Informação sobre os circuitos, incluindo ID, nome, localização, coordenadas e URL.
- **constructor_results.csv**: Resultados das equipas por corrida, incluindo pontos e estado.
- **constructor_standing.csv**: Classificação das equipas em cada corrida, incluindo posição, pontos e vitórias.
- **constructors.csv**: Informação sobre as equipas, incluindo nome, nacionalidade e URL.
- **driver_standing.csv**: Classificação dos pilotos em cada corrida, com pontos, posição e vitórias.
- **drivers.csv**: Informação sobre os pilotos, incluindo nome, número, código, data de nascimento e URL.
- **qualifying.csv**: Resultados das sessões de qualificação, incluindo tempos das voltas.
- **races.csv**: Detalhes das corridas, incluindo ano, circuito, datas das sessões e URL.
- **results.csv**: Resultados das corridas, incluindo posição, pontos, tempos e estatísticas.
- **seasons.csv**: Informação sobre as temporadas, incluindo ano e URL.
- **sprint_results.csv**: Resultados das corridas sprint.
- **status.csv**: Estado dos pilotos e equipas durante as corridas.

Criámos um ficheiro que transforma todos estes dados para o formato N3, que é um formato de serialização de dados RDF. O ficheiro `data_converter.py` contém funções para ler os dados dos ficheiros CSV e gerar as tripletas RDF correspondentes. 

Para o executar basta:

1. Criar um virtual environment:
```bash
python3 -m venv venv
```

2. Ativar o virtual environment:
```bash
source venv/bin/activate
```

3. Instalar as dependências:
```bash
cd src/
pip install -r requirements.txt
```

4. Executar o script:
```bash
python3 data_converter.py
```
O script irá gerar um ficheiro `data.n3` na pasta `output`, que contém os dados transformados para o formato N3.

## Estrutura do projeto

A estrutura do projeto é a seguinte:

```bash
.
├── data
│   ├── circuits.csv
│   ├── constructor_results.csv
│   ├── constructors.csv
│   ├── constructor_standings.csv
│   ├── drivers.csv
│   ├── driver_standings.csv
│   ├── qualifying.csv
│   ├── races.csv
│   ├── results.csv
│   ├── seasons.csv
│   ├── sprint_results.csv
│   ├── status.csv
│   └── unused
│       ├── lap_times.csv
│       └── pit_stops.csv
├── docs
│   ├── WS_Pitstop_Report.pdf
│   └── ws.tp1-v2.pdf
├── LICENSE
├── README.md
└── src
    ├── data_converter.py
    ├── docker-compose.yml
    ├── f1-backend
    │   ├── app
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── constants.py
    │   │   ├── __init__.py
    │   │   ├── migrations
    │   │   │   └── __init__.py
    │   │   ├── models.py
    │   │   ├── repositories
    │   │   │   ├── circuits.py
    │   │   │   ├── constructor.py
    │   │   │   ├── driver.py
    │   │   │   ├── races.py
    │   │   │   └── seasons.py
    │   │   ├── services
    │   │   │   ├── circuits.py
    │   │   │   ├── constructors.py
    │   │   │   ├── driver.py
    │   │   │   ├── races.py
    │   │   │   └── seasons.py
    │   │   ├── tests.py
    │   │   └── views.py
    │   ├── db.sqlite3
    │   ├── f1_pitstop
    │   │   ├── asgi.py
    │   │   ├── envs.py
    │   │   ├── graph_db.py
    │   │   ├── __init__.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   └── wsgi.py
    │   └── manage.py
    ├── f1-frontend
    │   ├── eslint.config.js
    │   ├── index.html
    │   ├── package.json
    │   ├── package-lock.json
    │   ├── public
    │   │   ├── backGround.jpg
    │   │   ├── f1_car.png
    │   │   ├── f1_logo.png
    │   │   └── vite.svg
    │   ├── README.md
    │   ├── src
    │   │   ├── assets
    │   │   │   └── react.svg
    │   │   ├── components
    │   │   │   ├── Button
    │   │   │   │   └── index.jsx
    │   │   │   ├── index.jsx
    │   │   │   ├── Modal
    │   │   │   │   └── index.jsx
    │   │   │   ├── NavBar
    │   │   │   │   └── index.jsx
    │   │   │   ├── NavBarLink
    │   │   │   │   └── index.jsx
    │   │   │   └── Table
    │   │   │       ├── ConstructorsTable.jsx
    │   │   │       ├── DriversTable.jsx
    │   │   │       ├── index.jsx
    │   │   │       ├── RacesTable.jsx
    │   │   │       └── SeasonsTable.jsx
    │   │   ├── index.css
    │   │   ├── main.jsx
    │   │   ├── pages
    │   │   │   ├── Constructors
    │   │   │   │   └── index.jsx
    │   │   │   ├── DriverProfile
    │   │   │   │   ├── index.jsx
    │   │   │   │   └── utils.jsx
    │   │   │   ├── Drivers
    │   │   │   │   └── index.jsx
    │   │   │   ├── Home
    │   │   │   │   └── index.jsx
    │   │   │   ├── index.jsx
    │   │   │   ├── RaceProfile
    │   │   │   │   └── index.jsx
    │   │   │   ├── Races
    │   │   │   │   └── index.jsx
    │   │   │   ├── RacesYears
    │   │   │   │   └── index.jsx
    │   │   │   ├── Root
    │   │   │   │   └── index.jsx
    │   │   │   ├── Season
    │   │   │   │   ├── card.jsx
    │   │   │   │   └── index.jsx
    │   │   │   ├── Seasons
    │   │   │   │   └── index.jsx
    │   │   │   └── SeasonsAdd
    │   │   │       └── index.jsx
    │   │   ├── routes.jsx
    │   │   └── services
    │   │       ├── circuitsService.js
    │   │       ├── client.jsx
    │   │       ├── constructorService.js
    │   │       ├── driversService.js
    │   │       ├── index.jsx
    │   │       ├── racesService.js
    │   │       └── seasonsService.js
    │   └── vite.config.js
    ├── output
    │   └── data.n3
    └── requirements.txt

35 directories, 94 files
```

## Como executar o projeto

Para executar o projeto, siga os seguintes passos:

1. Clonar o repositório:
```bash
git clone https://github.com/zegameiro/WS_First_Assignment
```

2. Navegar para o diretório do projeto:
```bash
cd WS_First_Assignment/src/
```

3. Executar o comando:
```bash
docker compose up --build
```

Os serviços serão iniciados e estarão disponíveis nos seguintes endereços:

| Serviço | URL |
| :-----: | :--: |
|  Frontend | [localhost:5173](http://localhost:5173) |
|  Backend  | [localhost:8000](http://localhost:8000) |
|  GraphDB | [localhost:7200](http://localhost:7200) |

## Autores

- [João Andrade](https://github.com/WildBunnie)
- [José Gameiro](https://github.com/zegameiro)
- [Tomás Victal](https://github.com/fungame2270)



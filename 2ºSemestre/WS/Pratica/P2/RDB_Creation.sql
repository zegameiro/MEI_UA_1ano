CREATE TABLE Local
(
  ID        TEXT,
  Nome      TEXT,
  Descricao TEXT
);

CREATE TABLE Evento
(
  ID        TEXT,
  Nome      TEXT,
  Data      DATE,
  Inicio    TEXT,
  Fim       TEXT,
  Descricao TEXT,
  Local_ID  TEXT
);

CREATE TABLE Pessoa
(
  ID        TEXT,
  Nome      TEXT,
  Email     TEXT,
  Evento_ID TEXT
);

INSERT INTO Local VALUES('l1','UA','Universidade de Aveiro');
INSERT INTO Local VALUES('l2','UC','Universidade de Coimbra');
INSERT INTO Local VALUES('l3','UP','Universidade do Porto');
INSERT INTO Local VALUES('l4','UL','Universidade de Lisboa');

INSERT INTO Evento VALUES('e1','Abertura UA','2017-09-20', '09:00', '18:00', 'Festa comemorativa da abertura do ano letivo na Universidade de Aveiro', 'l1');
INSERT INTO Evento VALUES('e2','Abertura UC','2017-09-30', '10:00', '19:00', 'Festa comemorativa da abertura do ano letivo na Universidade de Coimbra', 'l2');
INSERT INTO Evento VALUES('e3','Abertura UP','2017-09-25', '13:00', '20:00', 'Festa comemorativa da abertura do ano letivo na Universidade do Porto', 'l3');
INSERT INTO Evento VALUES('e4','Abertura UL','2017-09-27', '15:00', '23:00', 'Festa comemorativa da abertura do ano letivo na Universidade de Lisboa', 'l4');

INSERT INTO Pessoa VALUES('p1','João','joao@ua.pt','e1');
INSERT INTO Pessoa VALUES('p2','José','jose@uc.pt','e2');
INSERT INTO Pessoa VALUES('p3','Manuel','manuel@up.pt','e3');
INSERT INTO Pessoa VALUES('p4','Joaquim','joaquim@ul.pt','e4');
INSERT INTO Pessoa VALUES('p5','Antonio','antonio@ua.pt',NULL);

-- Queries 


-- 1. Description of all the people that participated in events

SELECT P.Nome, P.Email, E.Nome AS Evento
FROM Pessoa P
JOIN Evento E ON P.Evento_ID = E.ID;


-- 2. Description of all the events and places where they took place

SELECT E.Nome, E.Data, E.Inicio, E.Fim, E.Descricao, L.Nome AS Local
FROM Evento E
JOIN Local L ON E.Local_ID = L.ID;


-- 3. Description of all the events that took place in the Universidade de Aveiro

SELECT E.Nome, E.Data, E.Inicio, E.Fim, E.Descricao, L.Nome AS Local
FROM Evento E
JOIN Local L ON E.Local_ID = L.ID
WHERE L.Nome = 'UA';


-- 4. Description of all the events that have a start at 10:00 and end at 19:00

SELECT E.Nome, E.Data, E.Inicio, E.Fim, E.Descricao, L.Nome AS Local
FROM Evento E
JOIN Local L ON E.Local_ID = L.ID
WHERE E.Inicio = '10:00' AND E.Fim = '19:00';


-- 5. Which people participated in the event "Abertura UL"

SELECT P.Nome, P.Email, E.Nome AS Evento
FROM Pessoa P
JOIN Evento E ON P.Evento_ID = E.ID
WHERE E.Nome = 'Abertura UL';


-- 6. Which people participated in the event "Abertura UP" at the time 17:00

SELECT P.Nome, P.Email, E.Nome AS Evento
FROM Pessoa P
JOIN Evento E ON P.Evento_ID = E.ID
WHERE E.Nome = 'Abertura UP' AND E.Inicio <= '17:00' AND E.Fim >= '17:00';
CREATE TABLE KeyValueStore (
    EntityID   TEXT, 
    Attribute  TEXT,  
    Value      TEXT
);

-- Local

-- INSERT Local 1
INSERT INTO KeyValueStore VALUES('l1','Tipo','Local');
INSERT INTO KeyValueStore VALUES('l1','Nome','UA');
INSERT INTO KeyValueStore VALUES('l1','Descricao','Universidade de Aveiro');

-- INSERT Local 2
INSERT INTO KeyValueStore VALUES('l2','Tipo','Local');
INSERT INTO KeyValueStore VALUES('l2','Nome','UP');
INSERT INTO KeyValueStore VALUES('l2','Descricao','Universidade de Porto');

-- INSERT Local 3
INSERT INTO KeyValueStore VALUES('l3','Tipo','Local');
INSERT INTO KeyValueStore VALUES('l3','Nome','UL');
INSERT INTO KeyValueStore VALUES('l3','Descricao','Universidade de Lisboa');

-- Eventos

-- INSERT Evento 1
INSERT INTO KeyValueStore VALUES('e1','Tipo','Evento');
INSERT INTO KeyValueStore VALUES('e1','Nome','Abertura UA');
INSERT INTO KeyValueStore VALUES('e1','Data','2017-09-20');
INSERT INTO KeyValueStore VALUES('e1','Inicio','09:00');
INSERT INTO KeyValueStore VALUES('e1','Fim','18:00');
INSERT INTO KeyValueStore VALUES('e1','Descricao','Festa comemorativa da abertura do ano letivo na Universidade de Aveiro');
INSERT INTO KeyValueStore VALUES('e1','Local_ID','l1');

-- INSERT Evento 2
INSERT INTO KeyValueStore VALUES('e2','Tipo','Evento');
INSERT INTO KeyValueStore VALUES('e2','Nome','Abertura UC');
INSERT INTO KeyValueStore VALUES('e2','Data','2017-09-30');
INSERT INTO KeyValueStore VALUES('e2','Inicio','10:00');
INSERT INTO KeyValueStore VALUES('e2','Fim','19:00');
INSERT INTO KeyValueStore VALUES('e2','Descricao','Festa comemorativa da abertura do ano letivo na Universidade de Coimbra');
INSERT INTO KeyValueStore VALUES('e2','Local_ID','l2');

-- INSERT Evento 3
INSERT INTO KeyValueStore VALUES('e3','Tipo','Evento');
INSERT INTO KeyValueStore VALUES('e3','Nome','Abertura UP');
INSERT INTO KeyValueStore VALUES('e3','Data','2017-09-25');
INSERT INTO KeyValueStore VALUES('e3','Inicio','13:00');
INSERT INTO KeyValueStore VALUES('e3','Fim','20:00');
INSERT INTO KeyValueStore VALUES('e3','Descricao','Festa comemorativa da abertura do ano letivo na Universidade do Porto');
INSERT INTO KeyValueStore VALUES('e3','Local_ID','l3');

-- INSERT Evento 4
INSERT INTO KeyValueStore VALUES('e4','Tipo','Evento');
INSERT INTO KeyValueStore VALUES('e4','Nome','Abertura UL');
INSERT INTO KeyValueStore VALUES('e4','Data','2017-09-27');
INSERT INTO KeyValueStore VALUES('e4','Inicio','15:00');
INSERT INTO KeyValueStore VALUES('e4','Fim','23:00');
INSERT INTO KeyValueStore VALUES('e4','Descricao','Festa comemorativa da abertura do ano letivo na Universidade de Lisboa');
INSERT INTO KeyValueStore VALUES('e4','Local_ID','l4');

INSERT INTO KeyValueStore (EntityID,Attribute,Value) VALUES
    ('p1','Tipo','Pessoa'),
    ('p1','Nome','João'),
    ('p1','mail','joao@ua.pt'),
    ('p1','evento','e1');
    
INSERT INTO KeyValueStore (EntityID,Attribute,Value) VALUES
    ('p1','Tipo','Pessoa'),
    ('p1','Nome','José'),
    ('p1','mail','joao@ua.pt'),
    ('p1','evento','e2');

INSERT INTO KeyValueStore (EntityID,Attribute,Value) VALUES
    ('p1','Tipo','Pessoa'),
    ('p1','Nome','Manuel'),
    ('p1','mail','manuel@up.pt'),
    ('p1','evento','e3');

INSERT INTO KeyValueStore (EntityID,Attribute,Value) VALUES
    ('p1','Tipo','Pessoa'),
    ('p1','Nome','Joaquim'),
    ('p1','mail','joaquim@ul.pt'),
    ('p1','evento','e4');

INSERT INTO KeyValueStore (EntityID,Attribute,Value) VALUES
    ('p1','Tipo','Pessoa'),
    ('p1','Nome','Antonio'),
    ('p1','mail','antonio@ua.pt'),
    ('p1','evento',NULL);


-- 1. Description of all the people that participated in events

SELECT p.Value AS Nome, p2.Value AS Email, e.Value AS Evento
FROM KeyValueStore p
JOIN KeyValueStore p2 ON p.EntityID = p2.EntityID AND p2.Attribute = 'mail'
JOIN KeyValueStore p3 ON p.EntityID = p3.EntityID AND p3.Attribute = 'evento'
JOIN KeyValueStore e ON p3.Value = e.EntityID AND e.Attribute = 'Nome'
WHERE p.Attribute = 'Nome';


-- 2. Description of all the events and places where they took place

SELECT e.Value AS Evento, d.Value AS Data, i.Value AS Inicio, f.Value AS Fim, 
       desc.Value AS Descricao, l.Value AS Local
FROM KeyValueStore e
JOIN KeyValueStore d ON e.EntityID = d.EntityID AND d.Attribute = 'Data'
JOIN KeyValueStore i ON e.EntityID = i.EntityID AND i.Attribute = 'Inicio'
JOIN KeyValueStore f ON e.EntityID = f.EntityID AND f.Attribute = 'Fim'
JOIN KeyValueStore desc ON e.EntityID = desc.EntityID AND desc.Attribute = 'Descricao'
JOIN KeyValueStore l_id ON e.EntityID = l_id.EntityID AND l_id.Attribute = 'Local_ID'
JOIN KeyValueStore l ON l_id.Value = l.EntityID AND l.Attribute = 'Nome'
WHERE e.Attribute = 'Nome';


-- 3. Description of all the events that took place in the Universidade de Aveiro

SELECT e.Value AS Evento, d.Value AS Data, i.Value AS Inicio, f.Value AS Fim, 
       desc.Value AS Descricao, l.Value AS Local
FROM KeyValueStore e
JOIN KeyValueStore d ON e.EntityID = d.EntityID AND d.Attribute = 'Data'
JOIN KeyValueStore i ON e.EntityID = i.EntityID AND i.Attribute = 'Inicio'
JOIN KeyValueStore f ON e.EntityID = f.EntityID AND f.Attribute = 'Fim'
JOIN KeyValueStore desc ON e.EntityID = desc.EntityID AND desc.Attribute = 'Descricao'
JOIN KeyValueStore l_id ON e.EntityID = l_id.EntityID AND l_id.Attribute = 'Local_ID'
JOIN KeyValueStore l ON l_id.Value = l.EntityID AND l.Attribute = 'Nome'
WHERE e.Attribute = 'Nome' AND l.Value = 'UA';


-- 4. Description of all the events that have a start at 10:00 and end at 19:00

SELECT e.Value AS Evento, d.Value AS Data, i.Value AS Inicio, f.Value AS Fim, 
       desc.Value AS Descricao, l.Value AS Local
FROM KeyValueStore e
JOIN KeyValueStore d ON e.EntityID = d.EntityID AND d.Attribute = 'Data'
JOIN KeyValueStore i ON e.EntityID = i.EntityID AND i.Attribute = 'Inicio'
JOIN KeyValueStore f ON e.EntityID = f.EntityID AND f.Attribute = 'Fim'
JOIN KeyValueStore desc ON e.EntityID = desc.EntityID AND desc.Attribute = 'Descricao'
JOIN KeyValueStore l_id ON e.EntityID = l_id.EntityID AND l_id.Attribute = 'Local_ID'
JOIN KeyValueStore l ON l_id.Value = l.EntityID AND l.Attribute = 'Nome'
WHERE e.Attribute = 'Nome' AND i.Value = '10:00' AND f.Value = '19:00';


-- 5. Description of all the people that participated in events

SELECT p.Value AS Nome, p2.Value AS Email, e.Value AS Evento
FROM KeyValueStore p
JOIN KeyValueStore p2 ON p.EntityID = p2.EntityID AND p2.Attribute = 'mail'
JOIN KeyValueStore p3 ON p.EntityID = p3.EntityID AND p3.Attribute = 'evento'
JOIN KeyValueStore e ON p3.Value = e.EntityID AND e.Attribute = 'Nome'
WHERE p.Attribute = 'Nome' AND e.Value = 'Abertura UL';


-- 6. Description of all the events that took place in the Universidade de Aveiro

SELECT p.Value AS Nome, p2.Value AS Email, e.Value AS Evento
FROM KeyValueStore p
JOIN KeyValueStore p2 ON p.EntityID = p2.EntityID AND p2.Attribute = 'mail'
JOIN KeyValueStore p3 ON p.EntityID = p3.EntityID AND p3.Attribute = 'evento'
JOIN KeyValueStore e ON p3.Value = e.EntityID AND e.Attribute = 'Nome'
JOIN KeyValueStore i ON p3.Value = i.EntityID AND i.Attribute = 'Inicio'
JOIN KeyValueStore f ON p3.Value = f.EntityID AND f.Attribute = 'Fim'
WHERE p.Attribute = 'Nome' 
  AND e.Value = 'Abertura UP' 
  AND i.Value <= '17:00' 
  AND f.Value >= '17:00';

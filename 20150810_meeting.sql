CREATE TABLE metabolites 
(
metabolite_id int NOT NULL,
InCHI_identifier text,
InCHI_key varchar(255),
SMILES text,
monoisotopic_mass double,
sum_formula varchar(255),
PRIMARY KEY (metabolite_id)
);

CREATE TABLE hmdb 
(
metabolite_id int,
hmdb_id varchar(255),
kingdom varchar(255),
super_class varchar(255),
class varchar(255),
subclass varchar(255)
);

CREATE TABLE substituents 
(
metabolite_id int,
name varchar(255),
db_origin varchar(255)
);

CREATE TABLE biological_origin 
(
metabolite_id int,
origin_name varchar(255),
db_origin varchar(255)
);


INSERT INTO metabolites
(metabolite_id, SMILES, monoisotopic_mass)
VALUES 
(1, 'CH', 500),
(2, 'CHN', 700),
(3, 'CHO', 800),
(4, 'CHON', 900);


INSERT INTO hmdb
(metabolite_id, hmdb_id, kingdom)
VALUES 
(1, 'HMDB4', 'alcohol'),
(2, 'HMDB9', 'cyclic hydrocarbon');


for tag in xml_file:
  hmdb_identfier = extract_tag("hmdb", tag)
  prepare_sql = "INSERT INTO metabolites (xx, yy, zz) VALUES (%s, %s, %s)" % (hmdb_identifier, kingdom ... )
  send_query( prepare_sql )
  send_query( prepared_query, [hmdb_identifier, kingdom] )






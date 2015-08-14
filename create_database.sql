CREATE DATABASE metabolomics;

USE metabolomics;

CREATE TABLE metabolites 
(
metabolite_id int NOT NULL,
InCHI text,
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







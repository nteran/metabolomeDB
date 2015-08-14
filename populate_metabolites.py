#!/usr/bin/python
"""populate_metabolites.py: 
This script goes through a megadb file and outputs sql code
python populate_metabolites.py megadatabase.20150813-230628.txt > populate_metabolites.txt
mysql -u root < /Users/nat2/Box\ Sync/Snyder/metabolome/populate_metabolites.txt
megadb:
DB_ID	INCHI	SMILES	mass	chem_formula	inchiKey
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
"""
import sys

def prep_str(item):
		if (item is None):
			return 'null'
		else:
			return "'"+item+"'"
    	
def prep_num(item):
		if (item is None):
			return 'null'
		else:
			return item

megadb_old= open(sys.argv[1], 'r')
print 'USE metabolomics;'
for line in megadb_old:
	line.rstrip('\n')
	col = line.split("\t")
	col[5]=col[5].rstrip('\n')
	#replace any "" with NULL
	print 'INSERT INTO metabolites\n(metabolite_id, InCHI, SMILES, monoisotopic_mass, sum_formula, InChI_Key)\nVALUES'
	print '(%s, %s, %s, %s, %s, %s)' % (prep_str(col[0]),prep_str(col[1]),prep_str(col[2]),prep_num(col[3]),prep_str(col[4]),prep_str(col[5]))
	print ';'
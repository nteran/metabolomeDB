#!/usr/bin/python
"""assign_internalids.py: 
This script goes through a megadb, subdb
megadb and record them in the sourcesdb

python assign_internalids.py megadatabase.20150806.txt example_subdatabase_1.txt
python assign_internalids.py megadatabase.20150806.txt HMDB_parsed.20150813.txt
old subdatabases should be structured such that:
INCHI	SMILES	mass	chem_formula	inchiKey	origdb_ID	other	info
megadb:
DB_ID	INCHI	SMILES	mass	chem_formula	inchiKey
new subdb will be
DB_ID	origdb_ID	other	info
"""

import sys
import time
import shutil

null=""
######################
#     Prep Files     #
######################
#may want to change this, but I think it'd be best to keep old db files and make new, timestamped output files
megadb_old= open(sys.argv[1], 'r')

timestr = time.strftime("%Y%m%d-%H%M%S")

col = sys.argv[1].split('.')
megadb_new=str(col[0]+"."+timestr+".txt")

col = sys.argv[2].split('.')
subdb_new=str(col[0]+"."+timestr+".txt")
		
print "\nnew files will be:\n"+megadb_new+"\n"+subdb_new

#read in files

megadbinchi={}
megadbsmiles={}
######################
# Collect ID Numbers #
######################
#create a dictionary of megadatabase entries
for line in megadb_old:
	col = line.split("\t")
	#if inchi exists, inchi=metab-id
	#print line
	megadbid=col.pop(0)
	inchi=col[0]
	smiles=col[1]
	mass=col[2]
	if inchi != null:
		megadbinchi[inchi]=megadbid
#otherwise add smiles
	elif smiles != null:
		megadbsmiles[smiles]=megadbid
"""		
#otherwise use mass. Can be used to throw a flag later
#	else:
#		if mass in megadbmass:
#			megadbmass[mass]=str(megadb[mass]+"\t"+megadbid)
#		else:
#	 		megadbmass[mass]=megadbid"""
#figure out what the biggest number is
lastid=int(megadbid)
megadb_old.close()

#copy over megadbfile
shutil.copyfile(sys.argv[1], megadb_new)
megadb_new=open(megadb_new, 'a')

subdb_new=open(subdb_new, 'w')

subdb_old= open(sys.argv[2], 'r')

#######################
# Process subdatabase #
#######################
#INCHI	SMILES	mass	chem_formula	inchiKey	origdb_ID	other	info
#go through subdatabase
for line in subdb_old:
	col = line.split("\t")
	inchi=col.pop(0)
	smiles=col.pop(0)
	mass=col.pop(0)
	chem_formula=col.pop(0)
	inchiKey=col.pop(0)
	newline='\t'.join(map(str,col))
#if the inchi id in megadb, fetch the metab-id and add to line
	if inchi in megadbinchi:
		metabid = megadbinchi[inchi]
		subdb_new.write(metabid+"\t"+newline+"\n")
	elif smiles in megadbsmiles:
		metabid = megadbsmiles[smiles]
		subdb_new.write(metabid+"\t"+newline)
#theoretically you could now check the mass, but this may lead to oversimplification of diverse data
#if no id exists yet, make one up and add it to megadb file and hash, subdb file, and sourcedb hash
	else:
		newid=lastid+1
		lastid=newid
		newid=str(newid)
		#to megadb file
		megadb_new.write("\n"+newid.zfill(8)+"\t"+inchi+"\t"+smiles+"\t"+mass+"\t"+chem_formula+"\t"+inchiKey)
		subdb_new.write(newid.zfill(8)+"\t"+newline)
		#and correct hash
		if inchi != null:
			megadbinchi[inchi]=newid.zfill(8)
		elif smiles != null:
			megadbsmiles[smiles]=newid.zfill(8)
		#otherwise use mass, can add here flag w else statement if needed
subdb_new.close()
megadb_new.close()















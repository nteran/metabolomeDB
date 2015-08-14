#!/usr/bin/python
"""parse_hmdb.py: 
This script parses a modified hmdb file.
$find /Users/nat2/Downloads/hmdb_metabolites/. -print | xargs -n1000 grep -h -v "<?xml version=" >> ALLHMDB.xml
where ALLHMDB.xml alread had <data>, then $echo "</data>" >> ALL_HMDB.xml 
"""
import xml.etree.cElementTree as ET #permits xml parsing trees
import sys
#################EDIT THIS COMPONENT TO CHANGE DATA RETURNED#############################
"""Each start of an branch should be a new list, nested.
to return example0	example1	example2	example3, example4	example5,example6
<metabolite>
	<accession>example0
	<smiles>example1</example
	<biofluids_locations>
		<biofluids>example2</biofluids>
	</biofluids_locations>
	<class>
		<kingdom>example3</kingdom>
		<class>example4</class>
		<substituents>
			<substituent>example5</substituent>
			<substituent>example6</substituent>
	</class>
Set:
information=[
	'accession',
	'smiles',
	['biofluids_locations', 'biofluids'],
	['class', 'kingdom', 'class']
	['class', ['substituents', 'substituent']],
	]
"""
information=[
	"inchi",
	"smiles",
	"monisotopic_moleculate_weight", 
	"chemical_formula",
	"inchikey", #order doesn't matter after this
	"accession", 
	['taxonomy', 'kingdom'],
	['taxonomy','super_class'], 
	['taxonomy','class'],
	['taxonomy','subclass'],
	["ontology", ["origins", "origin"]], #csv
	["ontology", ["biofunctions", "biofunction"]], #csv
	["ontology", ["cellular_locations", "cellular_location"]], #csv
	['biofluid_locations', 'biofluid'], #csv
	['taxonomy', ['substituents', 'substituent']], #csv
	['pathways', ['pathway', 'name']] #csv
#	['normal_concentrations', ['concentration', ['references', ['reference', 'reference_text']]]]
	]

def addToAnsw(prevans, newitem):
		if (newitem is None):
			return prevans
		elif (len(prevans)>0):
			return prevans+', '+newitem#return values
		else:
			return newitem

def pullRelevant(info,branch):
			answ=""
#		for item in info:
			if isinstance(info, list): #if item is a list 
				if isinstance(info[1], list): #and second element is a list
					for newbranch in branch.findall(info[0]):
#						print newbranch
#						print info[1]
						if (len(answ)>0):
							answ=answ+', '+pullRelevant(info[1],newbranch)#return values
						else:
							answ=pullRelevant(info[1],newbranch)
				elif len(item)<=2: #if item is a list and second element the only element
#					print "flag2"
					for i in branch.findall(info[0]):
						for j in i.findall(info[1]):
							answ=addToAnsw(answ, j.text)
				else: #if item is a list and there are lots of items in the list
					length=len(info)
					count=length-1
					last=0-count#grab all but the first item in the list
					for k in info[last:]:
						if isinstance(k, list): #if the instance is a list
							pullRelevant(k, i)#recurse; I don't think this should happen
						else: #otherwise, concatenate by commas
							for i in branch.findall(info[0]):
								for j in i.findall(k):
									answ=addToAnsw(answ, j.text)
			else: #if item isn't a list
				for i in branch.findall(info):
					answ= i.text
			if not(answ is None):
				return answ
					


#Retrieve filenames from user open files
#SPLITS AT . => FILES OF NAME.SUBNAME.XML WILL BE RENAMED NAME_PARSED.TXT
infile=sys.argv[1]
col = infile.split('.')
prefix=col[0]
#outfile=prefix+'_parsed.txt' #will write to same location as infile

tree = ET.parse(infile)
root = tree.getroot()
#outfile=open(outfile, 'w')


count=1
for metabolite in root.findall('metabolite'):
	for item in information:
		answ=pullRelevant(item,metabolite)
		if answ is None:
			sys.stdout.write('\t')
		else:
			sys.stdout.write(str(answ)+'\t')
	sys.stdout.write('http://www.hmdb.ca/metabolites/'+metabolite.find("accession").text+"\n")
	
	

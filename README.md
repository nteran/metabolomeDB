# Metabolomics Databases
This set of commands processes files from the internet into an internal specific database format.

nteran@stanford.edu

## Establish Databases
```bash
$> mysql -u root < create_databases.sql
```

## HMDB
XML files were obtained in July 2015 from hmdb.ca and downloaded to a file named hmdb_metabolites

The folder of improperly formatted xml files was condensed into one better formatted xml file.
```bash
$> echo "<data>" > ALL_HMDB.xml
$> find /Users/nat2/Downloads/hmdb_metabolites/. -print | xargs -n1000 grep -h -v "<?xml version=" >> ALLHMDB.xml
$> echo "</data>" >> ALL_HMDB.xml 
```
The xml file was then turned into a tab separated value text file. 

The output selection can be modified by changing the list at the beginning of the file. However, downstream files are dependent on this output order, so any changes should be done with caution and downstream scripts should be modified.
```bash
$> python parse_hmdb.py ALL_HMDB.xml > HMDB.txt
```
This entries of this tsv file was then added to a "megadatabase file" that is equivalent to the existing metabolites sql database.

A dummy file can be initialized by
```bash
$> echo '1\tInChI\tsmiles\tmass\tchem_f\tInChIKey' > megadb.txt
```

The internal ids can be assigned to the HMDB file and the megadb updated by
```bash
$> python assign_internalids.py megadb.txt HMDB.txt
```

This will output two new files, both named with the original file name and a time stamp:

*megadb.20150810-121323.txt*
which all the pre-existing internal id numbers as well as newly created internal ids for the molecules contained in HMDB

*HMDB.20150810-121323.txt*
which contains a table of the HMDB molecules identified by the internal id with the information in the megadb removed (i.e. there is no longer a SMILES entry)

The megadb file can be turned into a set of sql commands by using populate metabolites.py

```bash
$> python populate_metabolites.py megadatabase.20150810-121323.txt > populate_metabolites.txt
$> mysql -u root < /Users/nat2/Box\ Sync/Snyder/metabolome/populate_metabolites.txt
```

Where the database and table have already been established as described in Establish Databases

## Data
The script relies on a user-downloaded file to parse the directory structure (this is to avoid storing sensitive information online, and ensure that all users are intended to have access to the information they are reading).
Be sure that your version of the file is the one whose address is defined as `STRUCTURED_FILE` on line 13.

To obtain this file, you can either manually generate it (by expanding all categories of the lookup of possible *Assignment Groups* on ServiceNow, and then copy/pasting that entire page into a file) or request a copy from your supervisor.

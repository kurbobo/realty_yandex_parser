# realty_parser
Parser for realty sites in order to get data

# execution

When you use our program for the first time, run data_base_creation.py in order to create database and then run search_cian.py.

search_cian.py will save all flats in database and if there was no exceptions, everything will be also saved in cain.csv

# save from mongo to csv

In order to save database in csv file use the following command 

`mongoexport --host=localhost --db=flats --collection=coll --type csv --fieldFile fields.txt --out=database.csv --quiet`

import os
import sys
sys.path.insert(1, '../search')
import parser_tools as pt
import pymongo
os.chdir('../ads_texts')
ads_list = os.listdir()
# соединяемся с сервером базы данных
# (по умолчанию подключение осуществляется на localhost:27017)
connect = pymongo.MongoClient('localhost', 27017, maxPoolSize=200)
# выбираем базу данных
db = connect.flats
# выбираем коллекцию документов
# db.coll
import tqdm
for ad in tqdm.tqdm(ads_list):
	with open(ad, 'r') as ad:
				x = ''.join(ad.readlines())
				year =  pt.building_year_parser(x)
				if year is not None:
					# print('updated')
					myquery = { "id": int(ad.name[:-4]), "Building_year": None}
					newvalues = { "$set": { "Building_year": year } }
					db.coll.update_many(myquery, newvalues)
connect.close()

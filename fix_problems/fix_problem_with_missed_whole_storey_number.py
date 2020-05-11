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
				whole_storey_number =  pt.whole_storeys_parser(x)
				if whole_storey_number is not None:
					# print('updated')
					myquery = { "id": int(ad.name[:-4]), "whole_storey_number": [None, None]}
					newvalues = { "$set": { "whole_storey_number": whole_storey_number } }
					db.coll.update_many(myquery, newvalues)
connect.close()

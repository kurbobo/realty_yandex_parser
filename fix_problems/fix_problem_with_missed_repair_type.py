import time
import os
import sys
sys.path.insert(1, '../search')
import parser_tools as pt
import pymongo
from multiprocessing.dummy import Pool as ThreadPool 
from multiprocessing import cpu_count


os.chdir('../ads_texts')
ads_list = os.listdir()
# соединяемся с сервером базы данных
# (по умолчанию подключение осуществляется на localhost:27017)
connect = pymongo.MongoClient('localhost', 27017, maxPoolSize=200)
# выбираем коллекцию документов

coll = connect.flats.coll
thread_pool_size = cpu_count()
pool = ThreadPool(thread_pool_size) 

def my_function(ad):
	with open(ad, 'r') as ad:
		x = ''.join(ad.readlines())
		repair =  pt.repair_type_parser(x)
		if repair is not None:
			# print('updated')
			myquery = { "id": int(ad.name[:-4]), "repair_type": None}
			newvalues = { "$set": { "repair_type": repair } }
			coll.update_many(myquery, newvalues)
start = time.time()
pool.map(my_function, ads_list)

print('ended in ', time.time()-start)

connect.close()

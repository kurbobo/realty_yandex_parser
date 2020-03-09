import pymongo
from datetime import datetime, timedelta
from search_cian import crawler


myclient = pymongo.MongoClient('localhost', 27017, maxPoolSize=200)
db = myclient.flats
# выбираем коллекцию документов
mycol = db.coll
past = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
print('past = ', past)
i = 0
for old_dict in mycol.find({ 'date_of_adding_to_db': {"$lt": past}}):
	try:
		crawler(old_dict['id'], i)
		i+=1
	except:
		myclient.close()
		
myclient.close()
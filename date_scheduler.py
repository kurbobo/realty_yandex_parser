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
for old_dict in mycol.find({ 'date_of_adding_to_db': {"$lt": past}, 'seen_as_old': { "$exists": False } , 'visitors': {"$ne": None}}):
	# try:
		print('hey', old_dict['id'])
		crawler(old_dict['id'], i)
		myquery = { "_id":  old_dict['_id']}
		newvalues = { "$set": { 'seen_as_old': True } }
		mycol.update_one(myquery, newvalues)
		print('hey', old_dict['id'])
		i+=1
	# except:
	# 	print('error')
	# 	myclient.close()
	# 	break
		
myclient.close()
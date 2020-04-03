import pymongo
from datetime import datetime, timedelta
from search_cian import crawler
import argparse
def updating_crawler(page_id, mongo_id, stop_trying_treshhold):
	crawler(page_id, stop_trying_treshhold)
	myquery = { "_id":  mongo_id}
	newvalues = { "$set": { 'seen_as_old': True } }
	mycol.update_one(myquery, newvalues)
	print('updated', page_id)

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--only_visitors", help="update ads only for ads with visitor's statistics", action='store_true')
	parser.add_argument("-n", "--number_of_tries", help="how many attempts for every ad to make", default=100)
	args = parser.parse_args()
	myclient = pymongo.MongoClient('localhost', 27017, maxPoolSize=200)
	db = myclient.flats
	# выбираем коллекцию документов
	mycol = db.coll
	past = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
	print('past = ', past)
	import multiprocessing as mp
	num_of_cores = mp.cpu_count()-2
	print('Start execution with ' + str(num_of_cores) + ' cores.')
	pool = mp.Pool(num_of_cores)
	dct = { 'date_of_adding_to_db': {"$lt": past}, 'seen_as_old': { "$exists": False } , 'active': True}
	if args.only_visitors:
		dct['visitors'] = {"$ne": None}
	for old_dict in mycol.find(dct):
		try:
			pool.apply_async(updating_crawler, args=(old_dict['id'], old_dict['_id'], args.number_of_tries))
			# updating_crawler(old_dict['id'], old_dict['_id'])
		except:
			print('error')
			myclient.close()
			break
	pool.close()
	pool.join()
	myclient.close()
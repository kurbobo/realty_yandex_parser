import pymongo
from datetime import datetime, timedelta
from parser_tools import update_data
def add_if_different(old_dict, updated_dict, date, collection,  string):
	if not (ld_dict[string] == updated_dict[string]):
		if type(old_dict[string]) is dict:
			lst_value = old_dict[string]
			lst_value.append(updated_dict[string])
			lst_date = old_dict['date_of_adding_to_db']
			lst_date.append(updated_dict['date_of_adding_to_db'])
		else:
			lst_value = [old_dict[string], updated_dict[string]]
			lst_date = [date, datetime.today().strftime('%Y-%m-%d')]
		myquery = { "id":  old_dict['id']}
		newvalues = { "$set": { string: lst_value } }
		collection.update_one(myquery, newvalues)
		newtimes = { "$set": { 'date_of_adding_to_db': lst_date } }
		collection.update_one(myquery, newtimes)


myclient = pymongo.MongoClient('localhost', 27017, maxPoolSize=200)
db = myclient.flats
# выбираем коллекцию документов
mycol = db.coll
past = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')

for old_dict in mycol.find({ 'date_of_adding_to_db': {"$lt": past}}):
# for x in mycol.find({ 'visitors': {"$ne": None}}):
  visitors_dict = old_dict['visitors']
  purchase_price =  old_dict['total_price']
  elem_id = old_dict['id']
  price_per_sq_meter = old_dict['price_per_sq_meter']
  total_number_views = old_dict['total_number_views']
  date = old_dict['date_of_adding_to_db'] 
  active = old_dict['active']
  updated_dict = update_data(elem_id)
  if updated_dict is None:
  	continue
  else:
	  add_if_different(old_dict, updated_dict, date, mycol,  'visitors')
	  add_if_different(old_dict, updated_dict, date, mycol,  'total_price')
	  add_if_different(old_dict, updated_dict, date, mycol,  'price_per_sq_meter')
	  add_if_different(old_dict, updated_dict, date, mycol,  'total_number_views')
	  add_if_different(old_dict, updated_dict, date, mycol,  'active')


#   x.update_one({
#   'date_of_adding_to_db': p['_id']
# },{
#   '$set': {
#     'd.a': existing + 1
#   }
# }, upsert=False)
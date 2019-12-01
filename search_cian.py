from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from time import clock
import pandas as pd
from parser_tools import *
import pymongo
import time
import os


number_of_pages = 200
open('cian.txt','w').close()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--headless")
driver = os.path.join("/usr/local/bin","chromedriver")
prefs = {'disk-cache-size': 4096}
chrome_options.add_experimental_option("prefs", prefs)


start = clock()


db_free = 1

initial_id = 220833621
num_of_nodes = 2

def parser(flat_string):
	amount_of_rooms, total_square = amount_and_square_parser(flat_string)
	storey_number, whole_storeys = storey_number_parser(flat_string)
	total_price, price_per_sq_meter = price_parser(flat_string)
	bathroom_num, bathroom_separate = bathroom_parser(flat_string)
	city, district,  municipal, street, building = address_parser(flat_string)
	element_dict = {'id': id_num_parser(flat_string),
					'Number_of_rooms': amount_of_rooms,
					'housing_complex': housing_complex_parser(flat_string),
					'total_area': total_square,
					'living_area': living_area_parser(flat_string),
					'kitchen_area': kitchen_area_parser(flat_string),
					'storey_number': storey_number,
					'whole_storey_number': whole_storeys,
					'Building_year': building_year_parser(flat_string),
					'total_price': int(total_price),
					'price_per_sq_meter': int(price_per_sq_meter),
					'city' : city,
					'district' : district,
					'municipal' : municipal,
					'street' : street,
					'building' : building,
					'type_of_flat':type_of_flat_parser(flat_string),
					'сeiling_height': seiling_hight_parser(flat_string),
					'bathroom_number': bathroom_num,
					'bathroom_separated': bathroom_separate,
					'windows_to_street': windows_to_street_parser(flat_string),
					'house_type': house_type_parser(flat_string),
					'ceiling_type': ceiling_type_parser(flat_string),
					'porch_num': porch_num_parser(flat_string),
					'central_heating': central_heating_parser(flat_string),
					'service_elevator_number': elevator_service_parser(flat_string),
					'passengers_elevator_number': elevator_passangers_parser(flat_string),
					'emergency_condition': emergency_condition_parser(flat_string),
					'room1_square': room1_square_parser(flat_string),
					'room2_square': room2_square_parser(flat_string),
					'room3_square': room3_square_parser(flat_string),
					'latitude': latitude(city, street, building),
					'longitude': longitude(city, street, building),
					'visitors' : visitors_parser(flat_string),
					'date_of_place': date_of_place_parser(flat_string),
					'total_number_views': total_number_views_parser(flat_string)}
	return element_dict

def crawler(page_id):
	try:
		with open( 'ads_texts/'+ str(page_id) + '.txt', 'a', encoding='utf-8') as output_file:

			browser = webdriver.Chrome(chrome_options=chrome_options)
			print('.')

			# Get the URL of next page to be parsed
			browser.get("https://spb.cian.ru/sale/flat/" + str(page_id) + "/")

			element_list = list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--header--2Ayiz')))
			element_list += ["address:\n"]
			element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('address.a10a3f92e9--address--140Ec')))
			element_list += ["\n"]
			element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--description--10czU')))
			element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--price-container--29gwP')))
			element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--section_divider--1zGrv')))
			element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--offer_card_page-main--1glTM a10a3f92e9--aside_banner--2FWCV')))
			element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--offer_card_page-bti--2BrZ7')))
			element_list += ["\n"]
			element_list += ["ID_num: " + str(page_id)]
			element_list += ["\n"]
			try:
				browser.find_element_by_css_selector('a.a10a3f92e9--link--1t8n1.a10a3f92e9--link--2mJJk').click()
				time.sleep(0.5)
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--information--AyP9e')))
				element_list += ["\n"]
				for elementName in browser.find_elements_by_css_selector("path.highcharts-point"):
					hover = ActionChains(browser).move_to_element(elementName).click().perform()
					time.sleep(0.1)
					element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector("g.highcharts-label.highcharts-tooltip.highcharts-color-undefined")))
					element_list += ["\n"]
			except:
				print("No info about visitors in ad: " + str(page_ad))
			element_str = "".join(element_list)
			for text in element_list:
				output_file.write(text + '\n')
			output_file.write('-------------------------------------------------------------------------\n')
			info_dict = parser(element_str)
			info_dict.update( {'pic_urls' : list(map(lambda x: x.get_attribute("src"), browser.find_elements_by_css_selector('img.fotorama__img')))})
			# соединяемся с сервером базы данных
			# (по умолчанию подключение осуществляется на localhost:27017)
			connect = pymongo.MongoClient('localhost', 27017, maxPoolSize=200)
			# выбираем базу данных
			db = connect.flats
			# выбираем коллекцию документов
			db.user
			global db_free
			while db_free == 0:
				time.sleep(0.01)
			else:
				db_free = 0
				db.coll.insert_one(info_dict)
				db_free = 1
			connect.close()
			browser.quit()
			return 0

	except Exception as e:
		print("Error has occured in: " + str(page_id))
		print(e)
		browser.quit()
		return 1


if __name__=="__main__":
	import multiprocessing as mp
	print("ololo")
	pool = mp.Pool(processes=2)
	pool.map(crawler, list(i + initial_id for i in range(0, 15)))


print('Parsing is done!!!')


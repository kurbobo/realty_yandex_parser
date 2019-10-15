from selenium import webdriver
import sqlite3
from time import clock
import pandas as pd
from parser_tools import *


number_of_pages = 1
open('cian.txt','w').close()
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096}
chrome_options.add_experimental_option("prefs", prefs)
info_list = []
conn = sqlite3.connect('cian.db')
cur = conn.cursor()
start = clock()


def parser(flat_string):
	amount_of_rooms, total_square = amount_and_square_parser(flat_string)
	storey_number, whole_storeys = storey_number_parser(flat_string)
	total_price, price_per_sq_meter = price_parser(flat_string)
	bathroom_num, bathroom_separate = bathroom_parser(flat_string)
	city, district,  municipal, street, building = address_parser(flat_string)
	if ('к' in building or 'К' in building) and building is not None:
		lst = building.split('к')
		building_for_coordinates = lst[0] + ' к' + lst[1]
	else:
		building_for_coordinates = building
	print(building_for_coordinates)
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
					'elevator_service': elevator_service_parser(flat_string),
					'elevator_passangers': elevator_passangers_parser(flat_string),
					'emergency_condition': emergency_condition_parser(flat_string),
					'room1_square': room1_square_parser(flat_string),
					'room2_square': room2_square_parser(flat_string),
					'room3_square': room3_square_parser(flat_string),
					'latitude': latitude(city + ',' + street + ',' + building_for_coordinates),
					'longitude': longitude(city + ',' + street + ',' + building_for_coordinates)}
	return element_dict


try:
	with open('cian.txt', 'a', encoding='utf-8') as output_file:
		browser = webdriver.Chrome(chrome_options=chrome_options)
		browser.get("https://spb.cian.ru/kupit-kvartiru-1-komn-ili-2-komn/")
		for page_num in range(0,number_of_pages):
			page_num += 1
			print(page_num)
			# Get the URL of next page to be parsed
			try:
				new_window_url = browser.find_element_by_xpath('//a[@class="_93444fe79c--list-itemLink--3o7_6" and text()="'+str(i)+'"]').get_attribute("href")
			except:
				new_window_url = browser.find_element_by_xpath('//a[@class="_93444fe79c--list-itemLink--3o7_6" and text()=".."]').get_attribute("href")

			# Get URLs of all current ads for parsing
			ads_on_page = list(map(lambda x: x.get_attribute("href"), browser.find_elements_by_xpath(
				'//a[@class="link_component-link-xUBVR4w6" and text()="Подробнее"]')))
			# Open every ad to find more info_dict
			for page_ad in ads_on_page:
				browser.get(page_ad)
				element_list = list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--header--2Ayiz')))
				element_list += ["address:\n"]
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('address.a10a3f92e9--address--140Ec')))
				element_list += ["\n"]
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--description--10czU')))
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--price-container--29gwP')))
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--section_divider--1zGrv')))
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--offer_card_page-main--1glTM a10a3f92e9--aside_banner--2FWCV')))
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--offer_card_page-bti--2BrZ7')))
				element_list += ["ID_num: " + str(page_ad.split('/')[-2])]
				element_str = "".join(element_list)
				for text in element_list:
					output_file.write(text + '\n')
				output_file.write('-------------------------------------------------------------------------\n')
				info_dict = parser(element_str)
				columns = ', '.join(info_dict.keys())
				placeholders = ':' + ', :'.join(info_dict.keys())
				query = 'INSERT INTO flats (%s) VALUES (%s)' % (columns, placeholders)
				cur.execute(query, info_dict)
				info_list.append(info_dict)
				conn.commit()
			# Open next page with search results
			browser.get(new_window_url)
except Exception as e:
	print(e)

finally:
	end = clock()
	df = pd.DataFrame(info_list)
	df.to_csv('cian.csv', sep='\t', index=False)
	print('Parsing done in ' + str(end - start) + ' seconds.')
	conn.close()
	browser.quit()

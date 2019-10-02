from selenium import webdriver
from time import clock
import re
import pandas as pd
number_of_pages = 1
open('cian.txt','w').close()
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096}
chrome_options.add_experimental_option("prefs", prefs)
info_list = []
start = clock()
def housing_complex_parser(flat_string):
	reg_for_hc = r'в\s+ЖК\s+«\w+\s*\w*»'
	if bool(re.search(reg_for_hc, flat_string))==False:
		housing_complex = None
	else: housing_complex = re.search(reg_for_hc , flat_string).group(0).split('«')[1].split('»')[0]
	return housing_complex
def amount_and_square_parser(flat_string):
	string_with_amount_and_square = re.search(r'\d+-комн.\s+квартира,\s+\d+,?\d*', flat_string).group(0)
	if bool(string_with_amount_and_square)==False:
		amount_of_rooms = total_square = None
	else:
		amount_of_rooms, total_square = re.findall('\s*\d+,?\d*', string_with_amount_and_square)
		amount_of_rooms, total_square = int(amount_of_rooms), float(total_square.replace(',', '.'))
	return amount_of_rooms, total_square
def living_area_parser(flat_string):
	reg_for_liv_ar = re.search(r'\d+,?\d*\s+\w+\sЖилая', flat_string)
	if bool(reg_for_liv_ar)==False:
		living_area = None
	else:
		living_area = reg_for_liv_ar.group(0).split()[0]
		living_area = float(living_area.replace(',', '.'))
	return living_area
def kitchen_area_parser(flat_string):
	reg_for_liv_ar = re.search(r'\d+,?\d*\s+\w+\sКухня', flat_string)
	if bool(reg_for_liv_ar)==False:
		kitchen_area = None
	else:
		kitchen_area = reg_for_liv_ar.group(0).split()[0]
		kitchen_area = float(kitchen_area.replace(',', '.'))
	return kitchen_area
def storey_number_parser(flat_string):
	reg_for_liv_ar = re.search(r'\d+\s+из\s+\d+\s*Этаж', flat_string)
	if bool(reg_for_liv_ar)==False:
		storey_number = None, None
	else:
		storey_number = reg_for_liv_ar.group(0).split()[0], reg_for_liv_ar.group(0).split()[2]
	return storey_number
def building_year_parser(flat_string):
	reg_for_building_year = re.search(r'\d+\s*Построен', flat_string)
	if bool(reg_for_building_year)==False:
		building_year = None
	else:
		building_year = int(reg_for_building_year.group(0).split()[0])
	return building_year
def price_parser(flat_string):
	reg_for_price = re.search(r'\d+\s*\d*\s*\d*\s*₽\s*'*2, flat_string)
	if bool(reg_for_price)==False:
		price, dens = None, None
	else:
		fin = reg_for_price.group(0).replace(' ','').replace('\n','').split('₽')
		price, dens =fin[0] , fin[1] 
	return price, dens
def parser(flat_string):
	amount_of_rooms, total_square = amount_and_square_parser(flat_string)
	storey_number, whole_storeys = storey_number_parser(flat_string)
	total_price, price_per_sq_meter = price_parser(flat_string)
	element_dict = {'Number of rooms': amount_of_rooms, 'total_area': total_square, 
	'housing_complex': housing_complex_parser(flat_string), 'living_area':living_area_parser(flat_string),
	'kitchen_area': kitchen_area_parser(flat_string), 'storey_number': storey_number, 'whole_storey_number': whole_storeys,
	'Building_year': building_year_parser(flat_string), 'total_price': int(total_price), 'price_per_sq_meter':int(price_per_sq_meter)}
	return element_dict
try:
	with open('cian.txt', 'a', encoding='utf-8') as output_file:
		browser = webdriver.Chrome(chrome_options=chrome_options)
		browser.get("https://spb.cian.ru/kupit-kvartiru-1-komn-ili-2-komn/")
		for page_num in range(0,number_of_pages):
			page_num+=1
			print(page_num)
			# Get the URL of next page to be parsed
			try:
				new_window_url = browser.find_element_by_xpath('//a[@class="_93444fe79c--list-itemLink--3o7_6" and text()="'+str(i)+'"]').get_attribute("href")
			except:
				new_window_url = browser.find_element_by_xpath('//a[@class="_93444fe79c--list-itemLink--3o7_6" and text()=".."]').get_attribute("href")

			# Get URLs of all current ads for parsing
			ads_on_page = list(map(lambda x: x.get_attribute("href"), browser.find_elements_by_xpath(
				'//a[@class="link_component-link-xUBVR4w6" and text()="Подробнее"]')))
			# Open every ad to find more info
			# TODO: find more appropriate css selectors for more accurate parsing
			for page_ad in ads_on_page:
				browser.get(page_ad)
				element_list = list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--header--2Ayiz')))
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--description--10czU')))
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--price-container--29gwP')))
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--section_divider--1zGrv')))
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--offer_card_page-bti--2BrZ7')))
				element_str = "".join(element_list)
				for text in element_list:
					output_file.write(text+ '\n')
				output_file.write('-------------------------------------------------------------------------\n')
				info_list.append(parser(element_str))
				print(parser(element_str))
			# Open next page with search results
			browser.get(new_window_url)
finally:
	end = clock()
	df = pd.DataFrame(info_list)
	df.to_csv('cian.csv', sep='\t',index=False)
	print('Parsing done in ' + str(end - start) + ' seconds.')
	browser.quit()
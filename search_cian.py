from selenium import webdriver
from time import clock
import re
number_of_pages = 1
open('cian.txt','w').close()
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096}
chrome_options.add_experimental_option("prefs", prefs)
start = clock()
def housing_complex_parser(flat_string):
	reg_for_hc = r'в\s+ЖК\s+«\w+\s*\w*»'
	if bool(re.search(reg_for_hc, flat_string))==False:
		housing_complex = None
	else: housing_complex = re.search(reg_for_hc , flat_string).group(0).split('«')[1].split('»')[0]
	return housing_complex
def amount_and_square_parser(flat_string):
	string_with_amount_and_square = re.search(r'\d+-комн.\s+квартира,\s+\d+,?\d*', flat_string).group(0)
	amount_of_rooms, total_square = re.findall('\s*\d+,?\d*', string_with_amount_and_square)
	return int(amount_of_rooms), float(total_square.replace(',', '.'))
def living_area_parser(flat_string):
	reg_for_liv_ar = re.search(r'\d+,?\d*\s+\w+\sЖилая', flat_string)
	if bool(reg_for_liv_ar)==False:
		living_area = None
	else:
		living_area = reg_for_liv_ar.group(0).split()[0]
	return living_area
def parser(flat_string):
	amount_of_rooms, total_square = amount_and_square_parser(flat_string)
	element_dict = {'Number of flats': amount_of_rooms, 'total_area': total_square, 
	'housing complex': housing_complex_parser(flat_string), 'living_area':living_area_parser(flat_string)}
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
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--price--1HD9F a10a3f92e9--price--residential--2ev_G')))
				# element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--offer_card_page-main--1glTM a10a3f92e9--aside_banner--2FWCV')))
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--section_divider--1zGrv')))
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--offer_card_page-bti--2BrZ7')))
				element_str = "".join(element_list)
				for text in element_list:
					output_file.write(text+ '\n')
				output_file.write('-------------------------------------------------------------------------\n')
				# element_dict = {'Number of flats':(re.search(r'\d+-комн.\s+квартира,\s+\d+,\d+',element_str).group(0))}
				# print(element_str)
				print(parser(element_str))
			# Open next page with search results
			browser.get(new_window_url)
finally:
	end = clock()
	print('Parsing done in ' + str(end - start) + ' seconds.')
	browser.quit()
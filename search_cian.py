from selenium import webdriver
number_of_pages = 100
open('cian.txt','w').close()
try:
	with open('cian.txt', 'a', encoding='utf-8') as output_file:
		browser = webdriver.Firefox()
		browser.get("https://spb.cian.ru/kupit-kvartiru-1-komn-ili-2-komn/")
		for page_num in range(2,number_of_pages):
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
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--offer_card_page-main--1glTM a10a3f92e9--aside_banner--2FWCV')))
				element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--offer_card_page-bti--2BrZ7')))
				for text in element_list:
					output_file.write(text)
			# Open next page with search results
			browser.get(new_window_url)
finally:
	browser.quit()


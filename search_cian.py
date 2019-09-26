from selenium import webdriver
n = 100
open('cian.txt','w').close()
try:
	with open('cian.txt', 'a', encoding='utf-8') as f:
		browser = webdriver.Firefox()
		browser.get("https://spb.cian.ru/kupit-kvartiru-1-komn-ili-2-komn/")
		for i in range(2,n):
			print(i)
			# button =browser.find_element_by_css_selector('li._93444fe79c--list-item--2KxXr:nth-child('+str(n)+')')
			element_list =list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.c6e8ba5398--info-container--A11gU')))
			for text in element_list:
				f.write(text)
			try:
				new_window_url = browser.find_element_by_xpath('//a[@class="_93444fe79c--list-itemLink--3o7_6" and text()="'+str(i)+'"]').get_attribute("href")
			except:
				new_window_url = browser.find_element_by_xpath('//a[@class="_93444fe79c--list-itemLink--3o7_6" and text()=".."]').get_attribute("href")
			# browser.find_element_by_css_selector(':nth-child('+str(i)+') > a._93444fe79c--list-itemLink--3o7_6').get_attribute("href")
			print(new_window_url)
			browser.get(new_window_url)
finally:
	browser.quit()
	# print(element_list)

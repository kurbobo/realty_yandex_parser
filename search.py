from selenium import webdriver
try:
	browser = webdriver.Firefox()
	browser.get("https://realty.yandex.ru/sankt-peterburg/kupit/kvartira/")
	while(True):
		element_list =list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.OffersSerpItem__main')))
		# for elem in element_list:
		# 	lst.append(elem.text)
finally:
	browser.quit()
	print(element_list)

from selenium import webdriver
try:
	element_list = []
	browser = webdriver.Firefox()
	browser.get("https://realty.yandex.ru/sankt-peterburg/kupit/kvartira/")
	while(True):
		element_list =list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.OffersSerpItem__main')))
except:
	print(browser.find_element_by_css_selector('div.OffersSerpItem__main'))
finally:
	browser.quit()
	print(element_list)

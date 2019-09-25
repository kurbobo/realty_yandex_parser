from selenium import webdriver
try:
	element_list = []
	browser = webdriver.Firefox()
	browser.get("https://spb.cian.ru/kupit-kvartiru-1-komn-ili-2-komn/")
	element_list =list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.c6e8ba5398--info-container--A11gU')))
finally:
	browser.quit()
	print(element_list)

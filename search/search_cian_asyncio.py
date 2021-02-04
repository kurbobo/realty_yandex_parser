import time
import traceback
import random
import os
import sys
from parser_manage_tools import *
import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from state_dict_class import MyGlobals
import subprocess
import multiprocessing as mp
from collections import Counter
    
class Crawler(object):
    """
    class for crawing cian
    :param page_id: integer, must be positive. Describes the id of the page, from which
    we should start crawling
    :param tbb_dir: string, the path to the tor-browser
    :return: None
    """
    def __init__(self, page_id, tbb_dir=None, loop=None):
        self.page_id = page_id
        self.tbb_dir = tbb_dir
        self.loop = loop
    def __call__(self):
        time.sleep(1*random.random())
        if self.page_id not in MyGlobals.state_dict.keys():
            MyGlobals.state_dict[self.page_id] = None
        loop.run_in_executor(executor, self.download_data)
        print('Ad with number: ' + str(self.page_id) + ' finished parsing.')
    def download_data(self):
        today_date = datetime.datetime.today().strftime('%Y-%m-%d')
        with open('/home/alex/Alex/big_data/realty_parser/ads_texts/'+ str(self.page_id) + '.txt', 'a', encoding='utf-8') as output_file:
            xvfb_display = start_xvfb()
            # browser = webdriver.Chrome(options=chrome_options)
            browser = TorBrowserDriver(self.tbb_dir)
            # Get the URL of next page to be parsed
            browser.get("https://spb.cian.ru/sale/flat/" + str(self.page_id) + "/")
            #колонка с количеством комнат, метражом, адресом
            element_list = list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--header--2Ayiz')))
            element_list += ["address:\n"]
            #колонка конкретно с адресом
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('address.a10a3f92e9--address--140Ec')))
            element_list += ["\n"]
            # колонка с путем до объявления а также с датой обновления и ссылкой на статистику объявлений 
            element_list += list(map(lambda x: x.text+'\n', browser.find_elements_by_css_selector('div.a10a3f92e9--offer_card_page-top--o2SYS')))
            #хз что это
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--description--10czU')))
            #информация по площади и этаэности
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--info-block--3cWJy')))
            #цена квартиры
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--price-container--29gwP')))
            #общая информация
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--section_divider--1zGrv')))
            #
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--offer_card_page-main--1glTM a10a3f92e9--aside_banner--2FWCV')))
            ## о доме (год постройки, тип дома и тд)
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--offer_card_page-bti--2BrZ7')))
            element_list += ["\n"]
            element_list += ["ID_num: " + str(self.page_id)]
            element_list += ["\n"]
            #хз
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--container--1In69')))
            element_list += ["\n"]
            purchase_price, purchase_dynamics, rent_price, rent_dynamics = pars_house_analytics(browser)
            # dst = district
            price_per_meter_in_dst, price_per_meter_in_dst_dynamics, price_per_house_in_dst, price_per_house_in_dst_dynamics, rent_price_in_dst, rent_dynamics_in_dst = pars_district_analytics(browser)
            price_range = pars_price_range(browser)
            try:
                browser.find_element_by_css_selector('a.a10a3f92e9--link--1t8n1.a10a3f92e9--link--2mJJk').click()
                element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--information--AyP9e')))
                element_list += ["\n"]
                for elementName in browser.find_elements_by_css_selector("path.highcharts-point"):
                    hover = ActionChains(browser).move_to_element(elementName).click().perform()
                    element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector("g.highcharts-label.highcharts-tooltip.highcharts-color-undefined")))
                    element_list += ["\n"]
            except:
                print("No info about visitors in ad: " + str(self.page_id))
            element_str = "".join(element_list)
            for text in element_list:
                output_file.write(text + '\n')
            output_file.write('-------------------------------------------------------------------------\n')
            info_dict = str_to_dict_parser(element_str)
            if info_dict['total_price'] is None and info_dict['address'] is None:
                browser.quit()
                stop_xvfb(xvfb_display)
                MyGlobals.state_dict[self.page_id] = 2
                time.sleep(10*random.random())
                return 2
            info_dict['price_range'] = price_range
            info_dict['purchase_price'] = purchase_price
            info_dict['purchase_dynamics'] = purchase_dynamics
            info_dict['rent_price'] = rent_price
            info_dict['rent_dynamics'] = rent_dynamics
            info_dict['price_per_meter_in_dst'] = price_per_meter_in_dst
            info_dict['price_per_meter_in_dst_dynamics'] = price_per_meter_in_dst_dynamics
            info_dict['price_per_house_in_dst'] = price_per_house_in_dst
            info_dict['price_per_house_in_dst_dynamics'] = price_per_house_in_dst_dynamics
            info_dict['rent_price_in_dst'] = rent_price_in_dst
            info_dict['rent_dynamics_in_dst'] = rent_dynamics_in_dst
            info_dict['cian_id'] = self.page_id

            info_dict['date_of_adding_to_db'] =  today_date
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
            stop_xvfb(xvfb_display)
            MyGlobals.state_dict[self.page_id] = 0
            return 0
if __name__=="__main__":
    #for automatic getting of current initial_id
    initial_id = int(subprocess.check_output(["./get_last_ad.sh"]))
    state_dict = {}
    N = 500
    executor = ThreadPoolExecutor(mp.cpu_count() * 2)
    loop = asyncio.get_event_loop()
    for ad in range(N):#100000
        if ad>=N-10:
            break
        crawler = Crawler(initial_id + ad, tbb_dir = "/home/alex/Alex/big_data/tor-browser_en-US", loop=loop)
        crawler()
    for _ in range(4):
        if Counter(MyGlobals.state_dict.values())[None]>N/4:
            loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks(loop), return_exceptions=True))   


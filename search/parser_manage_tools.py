from tbselenium.tbdriver import TorBrowserDriver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from tbselenium.utils import start_xvfb, stop_xvfb
import pymongo
from state_dict_class import MyGlobals
import datetime
import time
from parser_tools import *
db_free = 1
def str_to_dict_parser(flat_string):
    element_dict = {'id': id_num_parser(flat_string),
                    'Number_of_rooms': number_of_rooms_parser(flat_string),
                    'housing_complex': housing_complex_parser(flat_string),
                    'total_area': total_square_parser(flat_string),
                    'living_area': living_area_parser(flat_string),
                    'kitchen_area': kitchen_area_parser(flat_string),
                    'storey_number': storey_number_parser(flat_string),
                    'whole_storey_number': whole_storeys_parser(flat_string),
                    'Building_year': building_year_parser(flat_string),
                    'total_price': total_price_parser(flat_string),
                    'price_per_sq_meter': price_per_sq_meter_parser(flat_string),
                    'address' : address_parser(flat_string),
                    'type_of_flat':type_of_flat_parser(flat_string),
                    'сeiling_height': seiling_hight_parser(flat_string),
                    'bathroom_number': bathroom_num_parser(flat_string),
                    'bathroom_separated': bathroom_separate_parser(flat_string),
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
                    'latitude': latitude(address_parser(flat_string)),
                    'longitude': longitude(address_parser(flat_string)),
                    'visitors' : visitors_parser(flat_string),
                    'date_of_place': date_of_place_parser(flat_string),
                    'total_number_views': total_number_views_parser(flat_string),
                    'active': active_parser(flat_string), 
                    'trade_type': rent_or_sale_parser(flat_string)
                    }
    return element_dict

def download_data(page_id, tbb_dir):
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    print('start download_data')
    # try:
    with open('/home/alex/Alex/big_data/realty_parser/ads_texts/'+ str(page_id) + '.txt', 'a', encoding='utf-8') as output_file:
        xvfb_display = start_xvfb()
        # browser = webdriver.Chrome(options=chrome_options)
        browser = TorBrowserDriver(tbb_dir)
        # Get the URL of next page to be parsed
        browser.get("https://spb.cian.ru/sale/flat/" + str(page_id) + "/")
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
        element_list += ["ID_num: " + str(page_id)]
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
            print("No info about visitors in ad: " + str(page_id))
        element_str = "".join(element_list)
        for text in element_list:
            output_file.write(text + '\n')
        output_file.write('-------------------------------------------------------------------------\n')
        info_dict = str_to_dict_parser(element_str)
        # print(info_dict)
        if info_dict['total_price'] is None and info_dict['address'] is None:
            browser.quit()
            stop_xvfb(xvfb_display)
            print('MyGlobals.state_dict[page_id] = 2')
            MyGlobals.state_dict[page_id] = 2
            print('state_dict 2 is ', MyGlobals.state_dict)
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
        info_dict['cian_id'] = page_id

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
        print('MyGlobals.state_dict[page_id] = 0')
        MyGlobals.state_dict[page_id] = 0
        print('state_dict 0 is ', MyGlobals.state_dict)
        return 0

    # except Exception as exception:
    #     print("Error has occured in: " + str(page_id))
    #     print(exception)
    #     f= open("errors.txt","a+")
    #     f.write(str(page_id) + "\n")
    #     browser.quit()
    #     stop_xvfb(xvfb_display)
    #     return 1
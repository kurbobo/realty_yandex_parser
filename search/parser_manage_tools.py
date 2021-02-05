from tbselenium.tbdriver import TorBrowserDriver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from tbselenium.utils import start_xvfb, stop_xvfb
import pymongo
from state_dict_class import MyGlobals
import datetime
import time
import random
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

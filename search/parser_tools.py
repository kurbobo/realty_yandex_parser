import re
from geopy.geocoders import Nominatim
import datetime
from datetime import timedelta

correct_building_name = ['address:\n', 'р-н ', 'На карте', 'дор. ', 'просп.', 'ул.', 'наб.', 'ш.', 'пер.']


def housing_complex_parser(flat_string):
	reg_for_hc = r'в\s+ЖК\s+«(\w+\s*\w*)+»'
	if bool(re.search(reg_for_hc, flat_string))==False:
		housing_complex = None
	else: housing_complex = re.search(reg_for_hc , flat_string).group(0).split('«')[1].split('»')[0]
	return housing_complex


def address_parser(flat_string):
	reg_for_address = re.search(r'address:\n.+', flat_string)
	if bool(reg_for_address)==False:
		address_list = None
	else:
		reg_for_address = reg_for_address.group(0)
		for name in correct_building_name:
			reg_for_address = reg_for_address.replace(name, '')
		address_list = reg_for_address.split(',')
	return address_list


def number_of_rooms_parser(flat_string):
	reg_for_number_of_rooms = re.search(r'\d+-комн.\s+квартира,\s+\d+,?\d*', flat_string)
	studio = re.search(r'Студия', flat_string)#????
	if bool(reg_for_number_of_rooms)==False and bool(studio)==False:
		number_of_rooms = None
	else:
		if bool(reg_for_number_of_rooms):
			reg_for_number_of_rooms = reg_for_number_of_rooms.group(0)
			number_of_rooms, total_square = re.findall('\s*\d+,?\d*', reg_for_number_of_rooms)
			number_of_rooms = int(number_of_rooms)
		else:
			number_of_rooms = '0.8'
	return number_of_rooms

def total_square_parser(flat_string):
	reg_for_total_square = re.search(r'\d+-комн.\s+квартира,\s+\d+,?\d*', flat_string)
	studio = re.search(r'Студия,\s+\d+,?\d*', flat_string)
	if bool(reg_for_total_square)==False and bool(studio)==False:
		total_square = None
	else:
		if bool(reg_for_total_square):
			reg_for_total_square = reg_for_total_square.group(0)
			amount_of_rooms, total_square = re.findall('\s*\d+,?\d*', reg_for_total_square)
			total_square = float(total_square.replace(',', '.'))
		else:
			studio = studio.group(0)
			total_square = re.findall('\s*\d+,?\d*', studio)[0]
			total_square = float(total_square.replace(',', '.'))
	return total_square
# print(total_square_parser('1-комн. квартира, 41 м²'))
# print(total_square_parser('Студия, 15,4 м²'))
# print(number_of_rooms_parser('1-комн. квартира, 41 м²'))
# print(number_of_rooms_parser('Студия, 15,4 м²'))


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


def type_of_flat_parser(flat_string):
	reg_for_type = re.search(r'Тип жилья\s+\w+', flat_string)
	if bool(reg_for_type)==False:
		type_of_flat = None
	else:
		type_of_flat = reg_for_type.group(0).split()[-1]
	return type_of_flat


def storey_number_parser(flat_string):
	reg_for_storey_number = re.search(r'\d+\s+из\s+\d+\s*Этаж', flat_string)
	if bool(reg_for_storey_number)==False:
		storey_number = None, None
	else:
		storey_number = reg_for_storey_number.group(0).split()[0]
	return storey_number


def whole_storeys_parser(flat_string):
	reg_for_whole_storeys = re.search(r'\d+\s+из\s+\d+\s*Этаж', flat_string)
	if bool(reg_for_whole_storeys)==False:
		whole_storeys = None, None
	else:
		whole_storeys = reg_for_whole_storeys.group(0).split()[2]
	return whole_storeys


def building_year_parser(flat_string):
	reg_for_building_year = re.search(r'\d+\s*Построен', flat_string)
	reg_for_building_year_in_common_info =re.search(r'Год постройки\s+\d+', flat_string)
	if not bool(reg_for_building_year) and not bool(reg_for_building_year_in_common_info):
		building_year = None
	elif bool(reg_for_building_year):
		building_year = int(reg_for_building_year.group(0).split()[0])
	elif bool(reg_for_building_year_in_common_info):
		building_year = int(reg_for_building_year_in_common_info.group(0).split()[-1])
	return building_year
# with open('ex.txt', 'r') as f:
# 	flat = "".join(f.readlines())
# print(flat)
# print(building_year_parser(flat))

def total_price_parser(flat_string):
	reg_for_total_price_sale = re.search(r'\d+\s*\d*\s*\d*\s*₽\s*'*2, flat_string)
	reg_for_total_price_rent = re.search(r'\d+\s*\d*\s*\d*\s*₽/.', flat_string)
	if not bool(reg_for_total_price_sale) and not bool(reg_for_total_price_rent):
		total_price = None
	else:
		if bool(reg_for_total_price_sale):
			fin = reg_for_total_price_sale.group(0).replace(' ','').replace('\n','').split('₽')
			total_price = int(fin[0])
		else:
			fin = reg_for_total_price_rent.group(0).replace(' ','').replace('\n','').split('₽')
			total_price = int(fin[0])
	return total_price
# print(total_price_parser('40 000 ₽/мес.'))

def price_per_sq_meter_parser(flat_string):
	reg_for_price_per_sq_meter = re.search(r'\d+\s*\d*\s*\d*\s*₽\s*'*2, flat_string)
	if bool(reg_for_price_per_sq_meter)==False:
		price_per_sq_meter = None
	else:
		fin = reg_for_price_per_sq_meter.group(0).replace(' ','').replace('\n','').split('₽')
		price_per_sq_meter = int(fin[1])
	return price_per_sq_meter


def seiling_hight_parser(flat_string):
    try:
        reg_for_ceiling_height = re.search(r'Высота потолков\s+\w+', flat_string)
        if bool(reg_for_ceiling_height)==False:
            ceiling_height = None
        else:
            try:
                ceiling_height = float(reg_for_ceiling_height.group(0).split()[-1])
            except Exception:
            	ceiling_height = float(reg_for_ceiling_height.group(0).split('\n')[-1])
        return ceiling_height
    except:
        return None
# print(seiling_hight_parser('Высота потолков\n2'))

def bathroom_num_parser(flat_string):
	reg_for_bathroom_num = re.search(r'Санузел\s+\d+\s+\w+', flat_string)
	if bool(reg_for_bathroom_num)==False:
		bathroom_num = None
	else:
		bathroom_num = int(reg_for_bathroom_num.group(0).split()[1])
	return bathroom_num


def bathroom_separate_parser(flat_string):
	reg_for_bathroom_separate = re.search(r'Санузел\s+\d+\s+\w+', flat_string)
	if bool(reg_for_bathroom_separate)==False:
		bathroom_separate = None
	else:
		bathroom_separate = 'Yes' if "разд" in reg_for_bathroom_separate.group(0).split()[2] else 'No'
	return bathroom_separate


def windows_to_street_parser(flat_string):
	reg_for_windows_to_street = re.search(r'Вид из окон\s+\w+\s+\w+', flat_string)
	if bool(reg_for_windows_to_street)==False:
		windows_to_street = None
	else:
		windows_to_street = 'Yes' if "двор" in reg_for_windows_to_street.group(0).split() else 'No'
	return windows_to_street


def house_type_parser(flat_string):
	reg_for_house_type = re.search(r'Тип дома\s+\w+', flat_string)
	if bool(reg_for_house_type)==False:
		house_type = None
	else:
		house_type = reg_for_house_type.group(0).split()[-1]
	return house_type


def ceiling_type_parser(flat_string):
	reg_for_ceiling_type = re.search(r'Тип перекрытий\s+\w+', flat_string)
	if bool(reg_for_ceiling_type)==False:
		ceiling_type = None
	else:
		ceiling_type = reg_for_ceiling_type.group(0).split()[-1]
	return ceiling_type


def porch_num_parser(flat_string):
    try:
        reg_for_porch_num = re.search(r'Подъезды\s+\w+', flat_string)
        if bool(reg_for_porch_num)==False:
            porch_num = None
        else:
            try:
                porch_num = int(reg_for_porch_num.group(0).split()[-1])
            except UnicodeEncodeError:
                print('UnicodeEncodeError in porch_num_parser')
                print(removeNonAscii(reg_for_porch_num.group(0)))
                porch_num = int(removeNonAscii(reg_for_porch_num.group(0)).split()[-1])
        return porch_num
    except:
        return None
        


def central_heating_parser(flat_string):
	reg_for_central_heating = re.search(r'Отопление\s+\w+', flat_string)
	if bool(reg_for_central_heating)==False:
		central_heating = None
	else:
		central_heating = 'Yes' if "Центральное" in reg_for_central_heating.group(0).split() else 'No'
	return central_heating


def elevator_service_parser(flat_string):
	reg_for_elevator_service = re.search(r'\d+\s*пассажирских', flat_string)
	if bool(reg_for_elevator_service)==False:
		elevator_service = None
	else:
		elevator_service = int(reg_for_elevator_service.group(0).split()[0])
	return elevator_service


def elevator_passangers_parser(flat_string):
	reg_for_elevator_passangers = re.search(r'\d+\s*пассажирских', flat_string)
	if bool(reg_for_elevator_passangers)==False:
		elevator_passangers = None
	else:
		elevator_passangers = int(reg_for_elevator_passangers.group(0).split()[0])
	return elevator_passangers


def emergency_condition_parser(flat_string):
	reg_for_emergency_condition = re.search(r'Аварийность\s+\w+', flat_string)
	if bool(reg_for_emergency_condition)==False:
		emergency_condition = None
	else:
		emergency_condition = 'No' if "Нет" in reg_for_emergency_condition.group(0).split() else 'Yes'
	return emergency_condition


def room1_square_parser(flat_string):
	reg_for_room1_square = re.search(r'Площадь комнат\s+\w+', flat_string)
	if bool(reg_for_room1_square)==False:
		room1_square = None
	else:
		try:
			room1_square = float(reg_for_room1_square.group(0).split('-')[0].split('\n')[1])
		except:
			room1_square = None
	return room1_square


def room2_square_parser(flat_string):
	reg_for_room2_square = re.search(r'Площадь комнат\s+\w+.*', flat_string)
	if bool(reg_for_room2_square)==False:
		room2_square = None
	else:
		try:
			room2_square = float(reg_for_room2_square.group(0).split('-')[1].split()[0])
		except:
			room2_square = None
	return room2_square


def room3_square_parser(flat_string):
	reg_for_room3_square = re.search(r'Площадь комнат\s+\w+.*', flat_string)
	if bool(reg_for_room3_square)==False:
		room3_square = None
	else:
		try:
			room3_square = float(reg_for_room3_square.group(0).split('-')[2].split()[0])
		except:
			room3_square = None
	return room3_square


def id_num_parser(flat_string):
	reg_for_id_num = re.search(r'ID_num:\s+\w+.*', flat_string)
	if bool(reg_for_id_num)==False:
		id_num = None
	else:
		id_num = int(reg_for_id_num.group(0).split()[-1])
	return id_num

def building_for_coordinates(building):
	if ('к' in building) and building is not None:
		lst = building.split('к')
		building_correct = lst[0] + ' к' + lst[1]
	elif ('К' in building) and building is not None:
		lst = building.split('К')
		building_correct = lst[0] + ' к' + lst[1]
	else:
		building_correct = building
	return building_correct


def latitude(address):
	if address is None:
		return None
	place = str(address[0]) + ',' + str(address[-2]) + ',' + building_for_coordinates(str(address[-1]))
	nom = Nominatim()
	n = nom.geocode(place)
	if n is None:
		place = str(address[0]) + ',' + str(address[-3]) + ',' + building_for_coordinates(str(address[-2]))
		nom = Nominatim()
		n = nom.geocode(place)
		if n is None:
			return None
		else:
			return n.latitude
	else:
		return n.latitude


def longitude(address):
	if address is None:
		return None
	place = str(address[0]) + ',' + str(address[-2]) + ',' + building_for_coordinates(str(address[-1]))
	nom = Nominatim()
	n = nom.geocode(place)
	if n is None:
		place = str(address[0]) + ',' + str(address[-3]) + ',' + building_for_coordinates(str(address[-2]))
		nom = Nominatim()
		n = nom.geocode(place)
		if n is None:
			return None
		else:
			print('longitude =', n.longitude)
			return n.longitude
	else:
		print('longitude =', n.longitude)
		return n.longitude


def visitors_parser(flat_string):
	reg_for_visitors = re.findall(r'Количество просмотров.+', flat_string)
	if bool(reg_for_visitors)==False:
		visitors = None
	else:
		visitors = {}
		today = datetime.datetime.today()
		oneday = timedelta(days=1)
		previousday = today - oneday
		for visitor_day in reg_for_visitors:
			visitors.update({previousday.strftime('%Y-%m-%d'): visitor_day.split()[-1]})
			previousday = previousday - oneday
	return visitors

def date_of_place_parser(flat_string):
	reg_for_date_of_place = re.search(r'с даты создания объявления.*', flat_string)
	if bool(reg_for_date_of_place)==False:
		date_of_place = None
	else:
		try:
			date_of_place = ''.join(re.findall(r'\d*\.\d*\.\d*', reg_for_date_of_place.group(0)))
		except:
			date_of_place = None
	return date_of_place

def total_number_views_parser(flat_string):
	reg_for_total_number_views = re.search(r'.*с даты создания объявления', flat_string)
	if bool(reg_for_total_number_views)==False:
		total_number_views = None
	else:
		try:
			total_number_views = ''.join(re.findall(r'\d*', reg_for_total_number_views.group(0)))
		except:
			total_number_views = None
	return total_number_views
def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)

def active_parser(flat_string):
	reg_active = re.search(r'Объявление снято с публикации', flat_string)
	if bool(reg_active)==True:
		central_heating = False
	else:
		central_heating = True
	return central_heating

def rent_or_sale_parser(flat_string):
	reg = re.search(r'Недвижимость в\s.+', flat_string)
	if not bool(reg):
		return None
	else:
		for i in reg.group(0).split():
			if 'Продажа' in i:
				return 'sale'
			if 'АрендаАренда' in i:
				return 'rent_long'
			elif 'ПосуточноАренда' in i:
				return 'rent_short'
		return None
# print(rent_or_sale_parser('Недвижимость в Санкт-ПетербургеАрендаАренда 2-комнатных квартир \n'))

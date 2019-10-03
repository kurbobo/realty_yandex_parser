import re
def housing_complex_parser(flat_string):
	reg_for_hc = r'в\s+ЖК\s+«(\w+\s*\w*)+»'
	if bool(re.search(reg_for_hc, flat_string))==False:
		housing_complex = None
	else: housing_complex = re.search(reg_for_hc , flat_string).group(0).split('«')[1].split('»')[0]
	return housing_complex
def address_parser(flat_string):
	st = str(flat_string.split('\n')[1]+flat_string.split('\n')[2]).split('⋅')[0].replace('Санкт-Петербург,', '').replace('На карте', '').strip()
	if bool(re.search(r'р-н\s+\w+,\s*', st))==False:
		print(st)
		st = None
	else:
		st = st.replace(re.search(r'р-н\s+\w+,\s*', st).group(0),'').strip()
		if bool(re.search(r'в\s+ЖК\s+«(\w+\s*\w*)+»', st)):
			st = st.replace(re.search(r'в\s+ЖК\s+«(\w+\s*\w*)+»', st).group(0),'').strip().strip(',').strip()
	return st
def amount_and_square_parser(flat_string):
	string_with_amount_and_square = re.search(r'\d+-комн.\s+квартира,\s+\d+,?\d*', flat_string).group(0)
	if bool(string_with_amount_and_square)==False:
		amount_of_rooms = total_square = None
	else:
		amount_of_rooms, total_square = re.findall('\s*\d+,?\d*', string_with_amount_and_square)
		amount_of_rooms, total_square = int(amount_of_rooms), float(total_square.replace(',', '.'))
	return amount_of_rooms, total_square
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
	reg_for_liv_ar = re.search(r'\d+\s+из\s+\d+\s*Этаж', flat_string)
	if bool(reg_for_liv_ar)==False:
		storey_number = None, None
	else:
		storey_number = reg_for_liv_ar.group(0).split()[0], reg_for_liv_ar.group(0).split()[2]
	return storey_number
def building_year_parser(flat_string):
	reg_for_building_year = re.search(r'\d+\s*Построен', flat_string)
	if bool(reg_for_building_year)==False:
		building_year = None
	else:
		building_year = int(reg_for_building_year.group(0).split()[0])
	return building_year
def price_parser(flat_string):
	reg_for_price = re.search(r'\d+\s*\d*\s*\d*\s*₽\s*'*2, flat_string)
	if bool(reg_for_price)==False:
		price, dens = None, None
	else:
		fin = reg_for_price.group(0).replace(' ','').replace('\n','').split('₽')
		price, dens =fin[0] , fin[1] 
	return price, dens
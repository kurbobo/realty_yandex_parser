import sqlite3
conn = sqlite3.connect('cian.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE flats
             (Number_of_rooms integer, housing_complex text, total_area real, living_area real, kitchen_area, real, storey_number integer, whole_storey_number integer, Building_year integer, total_price integer, price_per_sq_meter integer, address text, type_of_flat text)''')
# my_dict = {'Number_of_rooms': 1, 'housing_complex': 'Дом на набережной', 'total_area': 44.0, 'living_area': 15.6, 'kitchen_area': 15.7, 'storey_number': '2', 'whole_storey_number': '20', 'Building_year': 2018, 'total_price': 6790000, 'price_per_sq_meter': 154318, 'address': 'Дом 5, сдан Невская застава, Общественный пер., 5', 'type_of_flat': 'Вторичка'}
# columns = ', '.join(my_dict.keys())
# placeholders = ':'+', :'.join(my_dict.keys())
# query = 'INSERT INTO my_table (%s) VALUES (%s)' % (columns, placeholders)
# print(query)
# cur.execute(query, my_dict)
conn.commit()
conn.close()
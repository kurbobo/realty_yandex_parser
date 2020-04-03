import sqlite3
conn = sqlite3.connect('cian.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE flats
             (id integer,
             Number_of_rooms integer,
             housing_complex text,
             total_area real,
             living_area real,
             kitchen_area real,
             storey_number integer,
             whole_storey_number integer,
             Building_year integer,
             total_price integer,
             price_per_sq_meter integer,
             city text,
             district text,
             municipal text,
             street text,
             building text,
             type_of_flat text,
             сeiling_height real,
             bathroom_number integer,
             bathroom_separated text,
             windows_to_street text,
             house_type text,
             ceiling_type text,
             porch_num integer,
             central_heating text,
             elevator_service integer,
             elevator_passangers integer,
             emergency_condition text,
             room1_square real,
             room2_square real,
             room3_square real,
             latitude real,
             longitude real)''')
conn.commit()
conn.close()
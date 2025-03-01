import pypyodbc as odbc

ask = input('SKU: ')

DRIVER_NAME = 'YOUR_DRIVER_NAME'
SERVER_NAME = 'YOUR_SERVER_NAME'
DATABASE_NAME = 'YOUR_DATABASE_NAME'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

# Establish a connection to the database
connection = odbc.connect(connection_string)
cursor = connection.cursor()

extract_data_query = """
    SELECT SKU FROM SNKRS
"""

cursor.execute(extract_data_query)
for data in cursor:
    sku = data[0] #Extract the first iondex in a tuple. Exp: from ('FJ1909-100',) extract only FJ1909-100
    print(sku)

    if ask == sku:
        print('SKU present!')

    else:
        print('adding sku to database!')

cursor.close()
connection.close()




# import mysql.connector
# from datetime import datetime
# import random
# host = 'localhost'
# user = 'admin'
# password = 'pass'
# database = 'coke'
# connection = mysql.connector.connect(host=host, user=user, password=password, database=database,auth_plugin='example')
# cursor = connection.cursor()
# create_table_query = """
# CREATE TABLE mer_details (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255),
#     OrderDate DATE,
#     amount DECIMAL(10, 2),
#     orderStatus VARCHAR(50),
#     phonenumber VARCHAR(15)
# )
# """
# cursor.execute(create_table_query)
# connection.commit()



import mysql.connector
from datetime import datetime
import random
host = 'localhost'
user = 'admin'
password = 'pass'
database = 'coke'
connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
cursor = connection.cursor()

sample_name = "hariya"
sample_order_date = "2024-05-26"
sample_amount = round(random.uniform(10.0, 1000.0), 2)
sample_order_status = "Completed"
sample_phone_number = "8374125"

insert_data_query = """
INSERT INTO mer_details (name, OrderDate, amount, orderStatus, phonenumber)
VALUES (%s, %s, %s, %s, %s)
"""
cursor.execute(insert_data_query, (sample_name, sample_order_date, sample_amount, sample_order_status, sample_phone_number))
connection.commit()
cursor.close()
connection.close()


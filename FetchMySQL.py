import mysql.connector

host = 'localhost'  # Change this to the host of your MySQL service
user = 'admin'      # Change this to your MySQL username
password = 'pass'   # Change this to your MySQL password
database = 'coke'  # Change this to your MySQL database name

connection = mysql.connector.connect(host=host, user=user, password=password, database=database)

cursor = connection.cursor()
id=78910

select_query = f'''SELECT * from mer_details where id=1;'''


# Execute the query
cursor.execute(select_query)

# Fetch all the rows
result_rows = cursor.fetchall()

# Display the fetched data
for row in result_rows:
    # Format each row in the desired format
    formatted_row = ", ".join(f"{column} is {value}" for column, value in zip(cursor.column_names, row))
    print(formatted_row)

# Close the cursor and connection
cursor.close()
connection.close()
  
    
import csv
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
try:
	connection = mysql.connector.connect(host = 'database-1.c3ao3x2iwh4o.ap-south-1.rds.amazonaws.com',database = 'employee_db', user = 'admin', password ='rajesh024')
	mysql_empsql_insert_query = "INSERT INTO employee(empid, empname, empaddress) VALUES (%s, %s, %s)"
	rows = []
	with open('csv_trial_2.csv', newline = '') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			rows.append(row.values())
	cursor = connection.cursor()
	cursor.executemany(mysql_empsql_insert_query, rows)
	connection.commit()
	print(cursor.rowcount, "Record inserted successfully into employee table")
	sql_select_query = " select * from employee"
	cursor = connection.cursor()
	cursor.execute(sql_select_query)
	records = cursor.fetchall()
	print("Total number of rows in employee table is: ",cursor.rowcount)
	print("\nPrinting each employee record")
	for row in records:
		print('empid = ', row[0])
		print('empname = ', row[1])
		print('empaddress = ', row[2])
	cursor.close()
except mysql.connector.Error as error:
	print("Failed to insert record into employee table{}".format(error))
    
    
#finally:
#	if(connection.is_connected()):
#	    connection.close()
#	    print("MySQL connection is closed")
        
        
from flask import Flask
import mysql.connector

app=Flask(__name__)

@app.route('/')
def act():
    mydb=mysql.connector.connect(host='dbs-activity-2239911.cce6vsqxmplt.us-east-2.rds.amazonaws.com', user='rajesh', password='Password')
    cur = mydb.cursor()
    cur.execute("create database db_act17")
    mydb=mysql.connector.connect(host='dbs-activity-2239911.cce6vsqxmplt.us-east-2.rds.amazonaws.com', user='rajesh', password='Password',database='db_act17')

    cur=mydb.cursor()
    s="CREATE TABLE employee(empid integer(5),empname varchar(20),empsalary float(10,2))"
    cur.execute(s)

    cur=mydb.cursor()
    s="INSERT INTO employee (empid,empname,empsalary) VALUES(%s,%s,%s)"
    b=[(1111, 'Sagar' ,50000),(2222,'Ravi Kiran',45000),(3333,'Sowmya',55000),(4444,'Divya',40000),(5555,'Vasanthi',37500)]
    cur.executemany(s,b)
    mydb.commit()
    #fetching or reading the data from database
    s="SELECT * from employee"
    cur.execute(s)
    x=cur.fetchall()
    # for i in x:
    
    #     print(i)

    #updating the table record
    s="UPDATE employee SET empsalary=empsalary+10000 WHERE empsalary<35000"
    cur.execute(s)
    mydb.commit()
    #fetching the updated table record
    s="SELECT * from employee"
    cur.execute(s)
    r=cur.fetchall()
    # k=[]
    # for i in r:
    #     k.append(i)
    # k=tuple(k)
    return str(r) 


if __name__=="__main__":
    app.run() 
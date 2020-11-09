import mysql.connector

mydb = mysql.connector.connect(
  host="172.19.0.6",
  user="root",
  password="root123!@#",
  database="bookxpress",
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM store_products")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
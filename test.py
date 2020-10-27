import json
from operator import itemgetter
import math
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import os

def bmi_calculation():
    #Load JSON data in read mode
    path = os.getcwd()
    data = json.load(open('bmi.json', 'r'))
    #data = json.load(open('E:\\D_Drive\\prgrm\\Python\\bmi.json', 'r'))

    #Fetch height as ht and weight as wt from data in list format
    ht = list(map(itemgetter('HeightCm'), data))
    wt = list(map(itemgetter('WeightKg'), data))

    #Calculate the body mass index(BMI) and save all in a list bmi
    bmi = []
    for i in range(len(ht)):
        bmi.append(round((wt[i])/(math.pow((ht[i]/100), 2)),2))


    overweight_count = 0
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(user='root', password='password', host='127.0.0.1', database='mydb')
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE table1 ADD BMI float(100, 2), ADD people_Category varchar(200), ADD People_risk varchar(200);")

        #Insert the required values using bmi list
        for value in bmi:
            cursor.execute ("""INSERT INTO table1 BMI VALUES (?)""", value)
            if value < 18.4:
                cursor.execute ("""INSERT INTO table1 people_Category, People_risk VALUES ('Underweight', 'Malnutrition risk')""")
            elif value > 18.5 and value < 24.9:
                cursor.execute ("""INSERT INTO table1 people_Category, People_risk VALUES ('Normal weight', 'Low risk')""")
            elif value > 25 and value < 29.9:
                cursor.execute ("""INSERT INTO table1 people_Category, People_risk VALUES ('Overweight', 'Enhanced risk')""")
                overweight_count += 1
            elif value > 30 and value < 34.9:
                cursor.execute ("""INSERT INTO table1 people_Category, People_risk VALUES ('Moderately obese', 'Medium risk')""")
            elif value > 35 and value < 39.9:
                cursor.execute ("""INSERT INTO table1 people_Category, People_risk VALUES ('Severely obese', 'High risk')""")
            elif value > 40:
                cursor.execute ("""INSERT INTO table1 people_Category, People_risk VALUES ('Very severely obese', 'Very high risk')""")


        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    print("BMI values: ",bmi)
    print("Total number of Overweight people is: ",overweight_count)



if __name__ == "__main__":
    bmi_calculation()

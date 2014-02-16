import sqlite3
import datetime

if __name__ == "__main__":
    products = []
    products.append((0,"-","-",0,"none",0,1))
    for each in products:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            sql = "insert into Reading(readingID, date, time, reading, averageReading, sensorID, readingTypeID) values (?,?,?,?,?,?,?)"
            cursor.execute(sql,each)
            db.commit()

    products = []
    products.append((1,"Moisture"))
    products.append((2,"Sun"))
    products.append((3,"Rain"))
    for each in products:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            sql = "insert into Sensor_Type(sensorTypeID, sensorType) values (?,?)"
            cursor.execute(sql,each)
            db.commit()

    products = []
    products.append((1,"Moisture"))
    products.append((2,"Intensity"))
    products.append((3,"Rainfall"))
    for each in products:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            sql = "insert into Reading_Type(readingTypeID, readingType) values (?,?)"
            cursor.execute(sql,each)
            db.commit()

    volume = 15.0
    products = []
    products.append((volume,))
    for each in products:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            sql = "insert into Flowerbed(volume) values (?)"
            cursor.execute(sql,each)
            db.commit()

    rate = 0.017
    products = []
    products.append((1,rate))
    for each in products:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            sql = "insert into Valve(flowerbedID, rate) values (?,?)"
            cursor.execute(sql,each)
            db.commit()


    products = []
    products.append((2,0))
    products.append((3,0))
    products.append((1,1))
    for each in products:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            sql = "insert into Sensor(sensorTypeID, flowerbedID) values(?,?)"
            cursor.execute(sql,each)
            db.commit()


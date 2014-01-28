import sqlite3
import datetime

if __name__ == "__main__":
    products = []
    now = datetime.datetime(2013,9,8,17,40)
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),27,25,3,1))
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),28,25,3,1))
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),29,25,3,1))
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),30,25,3,1))
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),31,25,4,1))
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),32,25,4,1))
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),33,25,5,1))
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),34,25,5,1))
    for each in products:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            sql = "insert into Reading(date, time, reading, averageReading, sensorID, readingTypeID) values (?,?,?,?,?,?)"
            cursor.execute(sql,each)
            db.commit()

    products = []
    now = datetime.datetime(2013,9,8,23,40)
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),0.3,250,2,3))
    now = datetime.datetime(2013,8,9,12,50)
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),0.5,500,2,3))
    now = datetime.datetime(2013,9,9,11,40)
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),1.7,750,2,3))
    now = datetime.datetime(2013,12,16,23,40)
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),0.1,1000,2,3))
    now = datetime.datetime(2014,1,1,17,40)
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),0.5,1250,2,3))
    now = datetime.datetime(2014,1,3,19,40)
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),0.8,1500,2,3))
    now = datetime.datetime(2014,1,7,9,28)
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),0.1,1750,2,3))
    now = datetime.datetime(2011,9,8,17,40)
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),2.1,2000,2,3))
    for each in products:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            sql = "insert into Reading(date, time, reading, averageReading, sensorID, readingTypeID) values (?,?,?,?,?,?)"
            cursor.execute(sql,each)
            db.commit()

    products = []
    now = datetime.datetime(2013,9,8)
    products.append((now.strftime("%Y/%m/%d"),"",0.3,0,1,2))
    now = datetime.datetime(2013,9,9)
    products.append((now.strftime("%Y/%m/%d"),"",0.5,0,1,2))
    now = datetime.datetime(2013,9,10)
    products.append((now.strftime("%Y/%m/%d"),"",1.7,0,1,2))
    now = datetime.datetime(2013,12,25)
    products.append((now.strftime("%Y/%m/%d"),"",0.1,0,1,2))
    now = datetime.datetime(2014,1,1)
    products.append((now.strftime("%Y/%m/%d"),"",0.5,0,1,2))
    now = datetime.datetime(2014,1,3)
    products.append((now.strftime("%Y/%m/%d"),"",0.8,0,1,2))
    now = datetime.datetime(2014,1,7)
    products.append((now.strftime("%Y/%m/%d"),"",0.1,0,1,2))
    now = datetime.datetime(2011,9,8)
    products.append((now.strftime("%Y/%m/%d"),"",2.1,0,1,2))
    for each in products:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            sql = "insert into Reading(date, time, reading, averageReading, sensorID, readingTypeID) values (?,?,?,?,?,?)"
            cursor.execute(sql,each)
            db.commit()

    products = []
    now = datetime.datetime(2013,9,8)
    products.append(("Roses",now.strftime("%Y/%m/%d"),"These are some notes",5,1))
    products.append(("Lilies",now.strftime("%Y/%m/%d"),"These are some notes",5,1))
    products.append(("Daffodils",now.strftime("%Y/%m/%d"),"These are some notes",5,1))
    products.append(("Cake",now.strftime("%Y/%m/%d"),"These are some notes",5,1))
    products.append(("Roses",now.strftime("%Y/%m/%d"),"These are some notes",5,3))
    products.append(("Lilies",now.strftime("%Y/%m/%d"),"These are some notes",5,2))
    products.append(("Daffodils",now.strftime("%Y/%m/%d"),"These are some notes",5,3))
    products.append(("Cake",now.strftime("%Y/%m/%d"),"These are some notes",5,4))
    products.append(("Roses",now.strftime("%Y/%m/%d"),"These are some notes",5,5))
    products.append(("Lilies",now.strftime("%%Y/%m/%d"),"These are some notes",5,7))
    products.append(("Daffodils",now.strftime("%Y/%m/%d"),"These are some notes",5,6))
    products.append(("Cake",now.strftime("%Y/%m/%d"),"These are some notes",5,8))
    for each in products:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            sql = "insert into Plant(plantGrowing, datePlanted, notes, waterNeed, flowerbedID) values (?,?,?,?,?)"
            cursor.execute(sql,each)
            db.commit()
    
    products = []
    now = datetime.datetime(2014,1,20,17,40)
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),20,5,16,1,2,1,1))
    now = datetime.datetime(2014,1,17,15,26)
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),20,5,16,3,4,1,1))
    now = datetime.datetime(2013,5,11,8,59)
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),20,5,16,5,6,1,1))
    now = datetime.datetime(2002,1,20,17,40)
    products.append((now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),20,5,16,7,8,1,1))
    for each in products:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            sql = "insert into Operation(date, time, duration, amount, cost, readingBeforeID, readingAfterID, valveID, flowerbedID) values (?,?,?,?,?,?,?,?,?)"
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

    products = []
    products.append((1,))
    products.append((2,))
    products.append((3,))
    products.append((4,))
    products.append((5,))
    products.append((6,))
    products.append((7,))
    products.append((8,))
    for each in products:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            sql = "insert into Flowerbed(flowerbedID) values (?)"
            cursor.execute(sql,each)
            db.commit()

    products = []
    products.append((1,))
    products.append((2,))
    products.append((3,))
    products.append((4,))
    products.append((5,))
    products.append((6,))
    products.append((7,))
    products.append((8,))
    for each in products:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            sql = "insert into Valve(flowerbedID) values (?)"
            cursor.execute(sql,each)
            db.commit()


    products = []
    products.append((2,0))
    products.append((3,0))
    products.append((1,1))
    products.append((1,1))
    products.append((1,1))
    products.append((1,2))
    products.append((1,2))
    products.append((1,2))
    for each in products:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            sql = "insert into Sensor(sensorTypeID, flowerbedID) values(?,?)"
            cursor.execute(sql,each)
            db.commit()


import sqlite3
import datetime
import random

#this file is a substitute for using serial ports to take readings
#it generates random numbers within the allowed range for each reading


def get_new_readings_moisture():
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("select sensorID,hardwareAddress from Sensor where sensorTypeID = 1")
        sensorValues = cursor.fetchall()
        numSensors = len(sensorValues)
    
    newReadings = []
    
    #random
    for each in sensorValues:
        newReading = str(random.randint(0,1))
        newReading += "."
        newReading += str(random.randint(0,9))
        newReading += str(random.randint(0,9))
        newReading += str(random.randint(0,9))
        newReading = float(newReading)
        now = datetime.datetime.today()
        newReadings.append([now.strftime("%Y/%m/%d"),now.strftime("%H:%M"), newReading, "TEMPORARY", each[0], 1])
    return newReadings


def add_to_database_moisture(newReadings):
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        for each in newReadings:
            value = (each[4],)
            cursor.execute("select flowerbedID from Sensor where sensorID = ?", value)
            temp = cursor.fetchall()[0]
            cursor.execute("select sensorID from Sensor where flowerbedID = ?", temp)
            temp = []
            for each2 in cursor.fetchall():
                for each2 in each2:
                    temp.append(each2)
            totalReading = 0
            numReadings = 0
            for each2 in newReadings:
                if each2[4] in temp:
                    totalReading += each2[2]
                    numReadings += 1
            averageReading = totalReading / numReadings
            averageReading = round(averageReading,3)
            each[3] = averageReading
            values = (each[0],each[1],each[2],each[3],each[4],each[5])
            cursor.execute("""insert into Reading(
                              date, time, reading, averageReading,
                              sensorID, readingTypeID)
                              values(?,?,?,?,?,?)""", values)
            db.commit()
            

def get_new_readings_sunlight():
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("select sensorID,hardwareAddress from Sensor where sensorTypeID = 2")
        sensorValues = cursor.fetchall()
        numSensors = len(sensorValues)
    
    newReadings = []
    
    #random
    for each in sensorValues:
        newReading = str(random.randint(300,800))
        newReading += "."
        newReading += str(random.randint(0,9))
        newReading = float(newReading)
        now = datetime.datetime.today()
        newReadings.append([now.strftime("%Y/%m/%d"),"-", newReading, "-", each[0], 2])
    return newReadings


def add_to_database_sunlight(newReadings):
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        for each in newReadings:
            values = (each[0],each[1],each[2],each[3],each[4],each[5])
            cursor.execute("""insert into Reading(
                              date, time, reading, averageReading,
                              sensorID, readingTypeID)
                              values(?,?,?,?,?,?)""", values)
            db.commit()


def get_new_readings_rainfall():
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("select sensorID,hardwareAddress from Sensor where sensorTypeID = 3")
        sensorValues = cursor.fetchall()
        numSensors = len(sensorValues)
    
    newReadings = []

    #random
    for each in sensorValues:
        newReading2 = str(random.randint(0,9))
        newReading2 += "."
        newReading2 += str(random.randint(0,9))
        newReading2 += str(random.randint(0,9))
        newReading2 += str(random.randint(0,9))
        newReading = random.randint(1,86400)
        now = datetime.datetime.today()
        newReadings.append([now.strftime("%Y/%m/%d"),now.strftime("%H:%M"), newReading, newReading2, each[0], 3])
    return newReadings


def add_to_database_rainfall(newReadings):
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        for each in newReadings:
            values = (each[0],each[1],each[2],each[3],each[4],each[5])
            cursor.execute("""insert into Reading(
                              date, time, reading, averageReading,
                              sensorID, readingTypeID)
                              values(?,?,?,?,?,?)""", values)
            

if __name__ == "__main__":
    newReadings = get_new_readings_moisture()
    add_to_database_moisture(newReadings)
    
    newReadings = get_new_readings_sunlight()
    add_to_database_sunlight(newReadings)
    
    newReadings = get_new_readings_rainfall()
    add_to_database_rainfall(newReadings)

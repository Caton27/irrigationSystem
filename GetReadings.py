import serial
import sqlite3
import datetime


def get_new_readings_moisture():
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("select sensorID,hardwareAddress from Sensor where sensorTypeID = 1")
        sensorValues = cursor.fetchall()
        numSensors = len(sensorValues)
    
    newReadings = []
    
    #serial
    ser = serial.Serial('COM3', 9600, timeout = 10)
    for each in sensorValues:
        dataToSend = "M" + str(each[1]) + "?\n"
        ser.write(bytearray(dataToSend,'ascii'))
        newReading = float(ser.readline(5))
        now = datetime.datetime.today()
        newReadings.append([now.strftime("%Y/%m/%d"),now.strftime("%H:%M"), newReading, "TEMPORARY", each[0], 1])
    ser.close()
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
    
    #serial
    ser = serial.Serial('COM3', 9600, timeout = 10)
    for each in sensorValues:
        dataToSend = "S" + str(each[1]) + "?\n"
        ser.write(bytearray(dataToSend,'ascii'))
        newReading = float(ser.readline(5))
        now = datetime.datetime.today()
        newReadings.append([now.strftime("%Y/%m/%d"),"-", newReading, "-", each[0], 2])
    ser.close()
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
    
    #serial
    ser = serial.Serial('COM3', 9600, timeout = 10)
    for each in sensorValues:
        dataToSend = "R" + str(each[1]) + "?\n"
        ser.write(bytearray(dataToSend,'ascii'))
        newReading = str(ser.readline(12))
        newReading2 = newReading[-5:]
        newReading = newReading[:-7]
        now = datetime.datetime.today()
        newReadings.append([now.strftime("%Y/%m/%d"),now.strftime("%H:%M"), newReading, newReading2, each[0], 3])
    ser.close()
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

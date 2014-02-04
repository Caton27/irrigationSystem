import serial
import sqlite3
import datetime


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
            


if __name__ == "__main__":
    newReadings = get_new_readings_sunlight()
    add_to_database_sunlight(newReadings)

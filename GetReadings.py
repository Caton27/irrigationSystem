import serial
import sqlite3
import datetime

#cost of water per litre
universalCost = 0.00205


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

        sensorsTemp = []
        cursor.execute("select operationID, readingBeforeID from Operation where readingAfterID = 0")
        operationTemp = cursor.fetchall()
        for each in operationTemp:
            cursor.execute("select sensorID from Reading where readingID = ?", (each[0],))
            sensorsTemp.append((cursor.fetchall()[0][0], each[0]))
        
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
            
            
            for each2 in sensorsTemp:
                if each[4] == each2[0]:
                    cursor.execute("select readingID from Reading where sensorID = ?", (each[4],))
                    results = cursor.fetchall()[-1][0]
                    values2 = (results, each2[1])
                    cursor.execute("""UPDATE Operation
                                      SET readingAfterID = ?
                                      WHERE operationID = ?""", values2)            
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

def calculate_need(newReadings):
    sensorIDs = []
    flowerbedIDs = []
    operations = []
    
    for each in newReadings:
        sensorIDs.append([each[4],each[3]])
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        for each in sensorIDs:
            cursor.execute("select flowerbedID from Sensor where sensorID  = ?", (each[0],))
            result = (cursor.fetchall())[0][0]
            add = True
            for each2 in flowerbedIDs:
                if str(each2[0]) == str(result):
                    add = False
            if add == True:
                flowerbedIDs.append([result,each[1]])
                
    number = 0
    for each in flowerbedIDs:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            cursor.execute("select waterNeed from Plant where flowerbedID = ?", (each[0],))
            result = cursor.fetchall()
            each.append([])
            for each2 in result:
                each[2].append(each2[0])
                
            total = 0
            num = 0
            for each2 in each[2]:
                try:
                    total += float(each2)
                    num += 1
                except ValueError:
                    pass
            try:
                average = total / num
            except ZeroDivisionError:
                average = 1.0
            each[2] = average

            difference = each[1] - each[2]
            if difference < 0:
                difference  = 0
            else:
                difference = round(difference, 3)
                each.append(difference)

                now = datetime.datetime.today()
                cursor.execute("select valveID from Valve where flowerbedID = ?", (each[0],))
                try:
                    valve = cursor.fetchall()[0][0]
                except IndexError:
                    valve = "-"

                cursor.execute("select rate from Valve where flowerbedID = ?", (each[0],))
                try:
                    rate = cursor.fetchall()[0][0]
                except IndexError:
                    rate = 0.017

                cursor.execute("select volume from Flowerbed where flowerbedID = ?", (each[0],))
                try:
                    volume = float(cursor.fetchall()[0][0])
                except IndexError and TypeError:
                    volume = 15.0
                
                amount = difference * volume
                amount = round(amount,4)
                
                duration = amount / rate
                duration = round(duration,0)
                
                cost = amount * universalCost
                cost = round(cost,5)

                averageReading = each[1]
                cursor.execute("select readingID from Reading where averageReading = ?", (each[1],))
                result = cursor.fetchall()
                
                operations.append([now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),duration,amount,cost,result[0][0],0,valve,each[0]])
                number += 1
            
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        for each in operations:
            cursor.execute("""insert into Operation(
                              date, time, duration, amount, cost, readingBeforeID, readingAfterID, valveID, flowerbedID)
                              values (?,?,?,?,?,?,?,?,?)""", (each[0],each[1],each[2],each[3],each[4],each[5],each[6],each[7],each[8]))
        db.commit()
    return operations


def water_plants(operations):
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        for each in operations:
            ser = serial.Serial('COM3', 9600, timeout = 10)
            cursor.execute("select hardwareAddress from Valve where valveID = ?", (each[7],))
            results = cursor.fetchAll()[0][0]
            dataToSend = "W" + str(results) + "," + str(each[2]) + "?\n"
            ser.write(bytearray(dataToSend, "ascii"))
            ser.close()



if __name__ == "__main__":
    newReadings = get_new_readings_moisture()
    add_to_database_moisture(newReadings)
    calculate_need(newReadings)
    
    newReadings = get_new_readings_sunlight()
    add_to_database_sunlight(newReadings)
    
    newReadings = get_new_readings_rainfall()
    add_to_database_rainfall(newReadings)

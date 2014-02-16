import sqlite3
import datetime
import random

#this file is a substitute for using serial ports to take readings
#it generates random numbers within the allowed range for each reading

#still needs to be properly defined
#cost of water per litre
universalCost = 0.5


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

        sensorsTemp = []
        cursor.execute("select operationID, readingBeforeID from Operation where readingAfterID = 0")
        operationTemp = cursor.fetchall()
        print(operationTemp)
        print("***")
        for each in operationTemp:
            cursor.execute("select sensorID from Reading where readingID = ?", (each[0],))
            sensorsTemp.append((cursor.fetchall()[0][0], each[0]))
        print(sensorsTemp)
        print("***")
        
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
            for each2 in sensorsTemp:
                if each[4] == each2[0]:
                    #insert each[4] into Operation where operationID = each2[1] for field readingAfterID
                    pass
            
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
                    rate = 5

                cursor.execute("select volume from Flowerbed where flowerbedID = ?", (each[0],))
                try:
                    volume = float(cursor.fetchall()[0][0])
                except IndexError and TypeError:
                    volume = 5.0
                
                amount = difference * volume
                amount = round(amount,3)
                
                duration = amount / rate
                duration = round(duration,0)
                
                cost = amount * universalCost
                cost = round(cost,3)

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
            

                  
if __name__ == "__main__":
    newReadings = get_new_readings_moisture()
    add_to_database_moisture(newReadings)
##    calculate_need(newReadings)
    
    newReadings = get_new_readings_sunlight()
    add_to_database_sunlight(newReadings)
    
    newReadings = get_new_readings_rainfall()
    add_to_database_rainfall(newReadings)

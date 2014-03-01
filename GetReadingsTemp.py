import sqlite3
import datetime
import random

#this file is a substitute for using serial ports to take readings
#it generates random numbers within the allowed range for each reading

#cost of water per litre
universalCost = 0.00205


def get_new_readings_moisture():
    #this function generates a reading for each moisture sensor present in the system
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("select sensorID,hardwareAddress from Sensor where sensorTypeID = 1")
        sensorValues = cursor.fetchall()
        #the number of moisture sensors that are present in the database
        numSensors = len(sensorValues)
    
    newReadings = []
    
    #for each sensor returned from the database
    for each in sensorValues:
        #intended minimum value is 0, intended maximum value is 2
        #a reading of 2 is not possible, the actual maximum is 1.999
        #step-by step creates the random number as a string
        newReading = str(random.randint(0,1))
        newReading += "."
        newReading += str(random.randint(0,9))
        newReading += str(random.randint(0,9))
        newReading += str(random.randint(0,9))
        #converts to float
        newReading = float(newReading)
        now = datetime.datetime.today()
        #new readings is a list holding the reading for the moisture sensor
        newReadings.append([now.strftime("%Y/%m/%d"),now.strftime("%H:%M"), newReading, "TEMPORARY", each[0], 1])
    return newReadings


def add_to_database_moisture(newReadings):
    #this function adds the moisture readings to the database
    #aswell as calculating the average reading
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
            #variables set up to enable calculation of the average reading
            totalReading = 0
            numReadings = 0
            for each2 in newReadings:
                if each2[4] in temp:
                    totalReading += each2[2]
                    numReadings += 1
            averageReading = totalReading / numReadings
            #rounded to 3 decimal places
            averageReading = round(averageReading,3)
            each[3] = averageReading
            values = (each[0],each[1],each[2],each[3],each[4],each[5])
            cursor.execute("""insert into Reading(
                              date, time, reading, averageReading,
                              sensorID, readingTypeID)
                              values(?,?,?,?,?,?)""", values)
            db.commit()
            
            #inserts readingAfterID into operations
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
    #this function generates a reading for each sunlight sensor present in the system
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("select sensorID,hardwareAddress from Sensor where sensorTypeID = 2")
        sensorValues = cursor.fetchall()
        #the number of sunlight sensors that are present in the database
        numSensors = len(sensorValues)
    
    newReadings = []
    
    #for each sensor returned from the database
    for each in sensorValues:
        #intended minimum value is 0, intended maximum value is 1000
        #a reading of 1000 is not possible, the actual maximum is 999.9
        #realistic readings between 300 and 800 are used
        #step-by step creates the random number as a string
        newReading = str(random.randint(300,800))
        newReading += "."
        newReading += str(random.randint(0,9))
        #converts to float
        newReading = float(newReading)
        now = datetime.datetime.today()
        #new readings is a list holding the reading for the sunlight sensor
        newReadings.append([now.strftime("%Y/%m/%d"),"-", newReading, "-", each[0], 2])
    return newReadings


def add_to_database_sunlight(newReadings):
    #this function adds the sunlight readings to the database
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
    #this function generates a reading for each rainfall sensor present in the system
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("select sensorID,hardwareAddress from Sensor where sensorTypeID = 3")
        sensorValues = cursor.fetchall()
        #the number of rainfall sensors that are present in the database
        numSensors = len(sensorValues)
    
    newReadings = []

    #for each sensor returned from the database
    for each in sensorValues:
        #intended minimum value is 0, intended maximum value is 86400 for duration
        #intended minimum value is 0, intended maximum value is 10 for depth
        #a reading of 10 is not possible, the actual maximum is 9.999
        #step-by step creates the random number as a string
        newReading2 = str(random.randint(0,9))
        newReading2 += "."
        newReading2 += str(random.randint(0,9))
        newReading2 += str(random.randint(0,9))
        newReading2 += str(random.randint(0,9))
        #creates the duration in 1 step
        newReading = random.randint(1,86400)
        now = datetime.datetime.today()
        #new readings is a list holding the reading for the moisture sensor
        newReadings.append([now.strftime("%Y/%m/%d"),now.strftime("%H:%M"), newReading, newReading2, each[0], 3])
    return newReadings


def add_to_database_rainfall(newReadings):
    #this function adds the rainfall readings to the database
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        for each in newReadings:
            values = (each[0],each[1],each[2],each[3],each[4],each[5])
            cursor.execute("""insert into Reading(
                              date, time, reading, averageReading,
                              sensorID, readingTypeID)
                              values(?,?,?,?,?,?)""", values)

def calculate_need(newReadings):
    #this function calculates whether or not a flowerbed needs watering
    sensorIDs = []
    flowerbedIDs = []
    operations = []
    
    for each in newReadings:
        #sensorID and averageReading added to the list sensorIDs
        sensorIDs.append([each[4],each[3]])
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        for each in sensorIDs:
            cursor.execute("select flowerbedID from Sensor where sensorID  = ?", (each[0],))
            result = (cursor.fetchall())[0][0]
            add = True
            #check to see if another moisture sensor with the same flowerbedID has been added
            #this avoids duplication of data
            for each2 in flowerbedIDs:
                if str(each2[0]) == str(result):
                    add = False
            if add == True:
                #flowerbedID and averageReading added to the list flowerbedIDs
                flowerbedIDs.append([result,each[1]])
    
    number = 0
    #for each flowerbed that has had a reading taken
    for each in flowerbedIDs:
        with sqlite3.connect("FlowerbedDatabase.db") as db:
            cursor = db.cursor()
            cursor.execute("select waterNeed from Plant where flowerbedID = ?", (each[0],))
            result = cursor.fetchall()
            #empty list added to the list flowerbedIDs to hold waterNeeds
            each.append([])
            for each2 in result:
                #waterNeeds added to the list flowerbedIDs
                each[2].append(each2[0])
            #averages the water need across all plants in that flowerbed
            #if no water need is present, a default value of 1.0 is used
            total = 0
            num = 0
            for each2 in each[2]:
                try:
                    total += float(each2)
                    num += 1
                except ValueError:
                    pass
            try:
                #average calculated
                average = total / num
            except ZeroDivisionError:
                #default value assigned
                average = 1.0
            each[2] = average

            #calculates the difference between the ideal moisture level and the measured one
            difference = each[1] - each[2]
            if difference < 0:
                #if difference is equal to  or less than 0, no operation is required
                #if difference < 0, it is assigned to 0 for simplicitys sake
                difference  = 0
            else:
                #rounded for conveniance
                difference = round(difference, 3)
                #added to the list flowerbedIDs
                each.append(difference)

                now = datetime.datetime.today()
                cursor.execute("select valveID from Valve where flowerbedID = ?", (each[0],))
                #trys to get the valveID assigned to the particular flowerbed
                try:
                    valve = cursor.fetchall()[0][0]
                except IndexError:
                    #if no valve is present, a null value is assigned
                    valve = "-"

                cursor.execute("select rate from Valve where flowerbedID = ?", (each[0],))
                #trys to get the rate from the valve in the database
                try:
                    rate = cursor.fetchall()[0][0]
                except IndexError:
                    #if no rate is present, a default rate is assigned
                    rate = 0.017

                cursor.execute("select volume from Flowerbed where flowerbedID = ?", (each[0],))
                #trys to get the volume required for the given flowerbed
                try:
                    volume = float(cursor.fetchall()[0][0])
                except IndexError and TypeError:
                    #if no volume is present, a default volume is assigned
                    volume = 15.0

                #total volume of water (L) required for the operation
                amount = difference * volume
                amount = round(amount,4)

                #duration (s) that the valve must remain open for
                duration = amount / rate
                duration = round(duration,0)

                #the cost of the water that has been used
                cost = amount * universalCost
                cost = round(cost,5)

                #gets the readingID from the database
                averageReading = each[1]
                cursor.execute("select readingID from Reading where averageReading = ?", (each[1],))
                result = cursor.fetchall()

                #adds the operation to the list operations
                operations.append([now.strftime("%Y/%m/%d"),now.strftime("%H:%M"),duration,amount,cost,result[0][0],0,valve,each[0]])
                #increments number
                number += 1
            
    with sqlite3.connect("FlowerbedDatabase.db") as db:
        cursor = db.cursor()
        #for each operation that will occur
        for each in operations:
            #added to database
            cursor.execute("""insert into Operation(
                              date, time, duration, amount, cost, readingBeforeID, readingAfterID, valveID, flowerbedID)
                              values (?,?,?,?,?,?,?,?,?)""", (each[0],each[1],each[2],each[3],each[4],each[5],each[6],each[7],each[8]))
        db.commit()
    return operations

                  
if __name__ == "__main__":
    newReadings = get_new_readings_moisture()
    add_to_database_moisture(newReadings)
    calculate_need(newReadings)
    
    newReadings = get_new_readings_sunlight()
    add_to_database_sunlight(newReadings)
    
    newReadings = get_new_readings_rainfall()
    add_to_database_rainfall(newReadings)

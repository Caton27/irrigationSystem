import sqlite3

def create_table(db_name,table_name,sql):
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            cursor.execute("select name from sqlite_master where name = ?",(table_name,))
            result = cursor.fetchall()
            if len(result) == 0:
                #enables foreign keys
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.execute(sql)
                db.commit()
            else:
                pass

def sql_statements():
    #sqls holds the various strings required to create the tables for the database
    sqls = []

    #creates table for Flowerbed
    sqls.append("""create table Flowerbed(
                  flowerbedID Integer,
                  volume Float,
                  primary key(flowerbedID))""")

    #creates table for Valve
    sqls.append("""create table Valve(
                  valveID Integer,
                  flowerbedID Integer,
                  rate Float,
                  hardwareAddress Text,
                  primary key(valveID),
                  foreign key(FlowerbedID) references Flowerbed(flowerbedID)
                  on update cascade on delete restrict)""")

    #creates table for Plant
    sqls.append("""create table Plant(
                  plantID Integer,
                  plantGrowing Text,
                  datePlanted Text,
                  waterNeed Float,
                  notes Text,
                  flowerbedID Integer,
                  primary key(plantID),
                  foreign key(flowerbedID) references Flowerbed(flowerbedID)
                  on update cascade on delete restrict)""")

    #creates table for Sensor_Type
    sqls.append("""create table Sensor_Type(
                  sensorTypeID Integer,
                  sensorType Text,
                  primary key(sensorTypeID))""")

    #creates table for Sensor
    sqls.append("""create table Sensor(
                  sensorID Integer,
                  sensorTypeID Integer,
                  flowerbedID Integer,
                  hardwareAddress Text,
                  primary key(sensorID),
                  foreign key(sensorTypeID) references Sensor_Type(sensorTypeID)
                  on update cascade on delete restrict,
                  foreign key(flowerbedID) references Flowerbed(flowerbedID)
                  on update cascade on delete restrict)""")

    #creates table for Reading_Type
    sqls.append("""create table Reading_Type(
                  readingTypeID Integer,
                  readingType Text,
                  primary key(readingTypeID))""")

    #creates table for Reading
    sqls.append("""create table Reading(
                  readingID Integer,
                  date Text,
                  time Text,
                  reading Float,
                  averageReading Float,
                  sensorID Integer,
                  readingTypeID Integer,
                  primary key(readingID),
                  foreign key(sensorID) references Sensor(sensorID)
                  on update cascade on delete restrict,
                  foreign key(readingTypeID) references Reading_Type(readingTypeID)
                  on update cascade on delete restrict)""")

    #creates table for Operation
    sqls.append("""create table Operation(
                  operationID Integer,
                  date Text,
                  time Text,
                  duration Integer,
                  amount Float,
                  cost Float,
                  readingBeforeID Integer,
                  readingAfterID Integer,
                  valveID Integer,
                  flowerbedID Integer,
                  primary key(operationID),
                  foreign key(readingBeforeID) references Reading(readingID)
                  on update cascade on delete restrict,
                  foreign key(readingAfterID) references Reading(readingID)
                  on update cascade on delete restrict,
                  foreign key(valveID) references Valve(valveID)
                  on update cascade on delete restrict,
                  foreign key(flowerbedID) references Flowerbed(flowerbedID)
                  on update cascade on delete restrict)""")
    return sqls


if __name__ == "__main__":
    db_name = "FlowerbedDatabase.db"
    #tableList holds the names of all the tables
    tableList = ["Flowerbed","Valve","Plant","Sensor_Type","Sensor","Reading_Type","Reading","Operation"]
    sqls = sql_statements()
    num = 0
    for each in sqls:
        create_table(db_name,tableList[num],each)
        num += 1

import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


f = "school.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
# Open csv files
students_file = csv.DictReader(open("peeps.csv"))
courses_file = csv.DictReader(open("courses.csv"))

# Create DB tables
studentsTable = "CREATE TABLE students (age INTEGER, name TEXT, id INTEGER PRIMARY KEY);"
coursesTable = "CREATE TABLE courses (code TEXT, mark INTEGER, id INTEGER);"
c.execute(studentsTable)
c.execute(coursesTable)

# Populate students
for row in students_file:
    age = row['age']
    name = row['name']
    id = row['id']

    addUser = "INSERT INTO students VALUES (%s, '%s', %s);" % (age, name, id)
    c.execute(addUser)

# Populate courses
for row in courses_file:
    code = row['code']
    mark = row['mark']
    id = row['id']

    addCourse = "INSERT INTO courses VALUES ('%s', %s, %s);" % (code, mark, id)
    c.execute(addCourse)

#==========================================================
db.commit() #save changes
db.close()  #close database



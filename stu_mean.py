import sqlite3
import csv

f = "school.db"

db = sqlite3.connect(f)
c = db.cursor()


command = "SELECT students.id, name, mark FROM students,courses WHERE students.id = courses.id;"
students = c.execute(command)

command = "CREATE TABLE peeps_avg (id INTEGER PRIMARY KEY, average NUMERICAL);"
#c.execute(command)

for student in students:
    print student[0]




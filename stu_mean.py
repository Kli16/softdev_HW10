import sqlite3
import csv

f = "school.db"

db = sqlite3.connect(f)
c = db.cursor()


getStudentGrades = "SELECT students.id, name, mark FROM students, courses WHERE students.id = courses.id;"
grades = c.execute(getStudentGrades)

createPeepTable = "CREATE TABLE peeps_avg (id INTEGER PRIMARY KEY, average NUMERICAL);"
#c.execute(createPeepTable)

# Grade dictionary<id, mark>
studentGrades = {}

# Populate grade dict
def populateStudentGrades():
    for student in grades:
        id = student[0];
        mark = student[2];
    
        if id in studentGrades:
            studentGrades[id].append(mark)
        else:
            studentGrades[id] = []
            studentGrades[id].append(mark)
            
# Look through grade dictionary, while replacing array of grades with average
def gradesAvg():
    for studentId in studentGrades:
        total = 0
        for grade in studentGrades[studentId]:
            total += grade
        studentGrades[studentId] = float(total) / (len(studentGrades[studentId])) # Calculate average

def getStudentName(uid):
    getStudentsName = "SELECT name FROM students WHERE %d = id;" % (uid)
    name = c.execute(getStudentsName)
    for n in name:
        return  n[0]


def displayStudents():
    for studentId in studentGrades:
        name = getStudentName(studentId)
        print "Student Id: %d, Name: %s, Average: %s" % (studentId, name, studentGrades[studentId])

    
populateStudentGrades()
gradesAvg()
displayStudents()

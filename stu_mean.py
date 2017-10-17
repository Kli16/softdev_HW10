import sqlite3
import csv

f = "school.db"

db = sqlite3.connect(f)
c = db.cursor()


getStudentGrades = "SELECT students.id, name, mark FROM students, courses WHERE students.id = courses.id;"
grades = c.execute(getStudentGrades)

# CREATED IN DB BUILDER
#createPeepAvgTable = "CREATE TABLE peeps_avg (id INTEGER PRIMARY KEY, average NUMERICAL);"
#c.execute(createPeepAvgTable)

# Grade dictionary<id, mark>
studentGrades = {}

# Populate grade dict
def populate_student_grades():
    for student in grades:
        id = student[0];
        mark = student[2];
    
        if id in studentGrades:
            studentGrades[id].append(mark)
        else:
            studentGrades[id] = []
            studentGrades[id].append(mark)
            
# Look through grade dictionary, while replacing array of grades with average
def grades_avg():
    for studentId in studentGrades:
        total = 0
        for grade in studentGrades[studentId]:
            total += grade
        studentGrades[studentId] = float(total) / (len(studentGrades[studentId])) # Calculate average

# Student name from id
def get_student_name(uid):
    getStudentsName = "SELECT name FROM students WHERE %d = id;" % (uid)
    name = c.execute(getStudentsName)
    for n in name:
        return  n[0]

# Display student id, name, avg
def display_students():
    for studentId in studentGrades:
        name = get_student_name(studentId)
        print "Student Id: %d, Name: %s, Average: %s" % (studentId, name, studentGrades[studentId])

# Populate peeps_avg table in db
def populate_peep_avg_table():
    # Populate students
    for studentId in studentGrades:
        id = studentId
        average = studentGrades[studentId]
        
        addStudentAvg = "INSERT INTO peeps_avg VALUES (%s, %s);" % (id, average)
        c.execute(addStudentAvg)

# Update student average
def update_average(id):
    total = 0
    count = 0
    getGrades = "SELECT mark FROM courses WHERE %d = id;" % (id)
    grades = c.execute(getGrades)
    
    for grade in grades:
        total += grade[0]
        count += 1

    newAvg = float(total) / count
    
    updateAverage = "UPDATE peeps_avg SET average = %s WHERE %d = id;" % (newAvg ,id)
    c.execute(updateAverage)

    studentGrades[id] = newAvg

# Add course to db and csv
def add_course(code, mark, id):
    addCourse = "INSERT INTO courses VALUES ('%s', %s, %s);" % (code, mark, id)
    c.execute(addCourse)

    # Add to csv
    with open('courses.csv', 'a') as csvfile:
        fieldnames = ['code', 'mark', 'id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'code': code, 'mark': mark, 'id': id})
        
populate_student_grades()
grades_avg()
display_students()
populate_peep_avg_table()

print "\nAdding courses (Cookie Eating - 170 & Free Pd - 16) for student 1..."
add_course("Cookie Eating", 170, 1)
add_course("Free Pd", 16, 1)

print "\nUpdating average...\n"
update_average(1)
display_students()


#==========================================================
db.commit() #save changes
db.close()  #close database

import pytest
import System
import json

# 1. login - System.py
# The login function takes a name and password and sets the user for the program. 
# Verify that the correct user is created with this test, and use the json files 
# to check that it adds the correct data to the user.

def test_login(grading_system):
    # makes a professor user
    username = 'goggins'
    password = 'augurrox'
    grading_system.login(username, password)
    if grading_system.usr.name != username:
        assert False
    if grading_system.usr.password != password:
        assert False
    if grading_system.usr.courses[0] != 'databases':
        assert False
    if grading_system.usr.courses[1] != 'software_engineering':
        assert False

# 2. check_password - System.py
# This function checks that the password is correct. 
# Enter several different formats of passwords to verify 
# that the password returns correctly if the passwords are the same.

def test_check_password(grading_system):
    assert grading_system.check_password('goggins', 'augurrox')
    assert not grading_system.check_password('goggins', 'augurroxx')
    assert grading_system.check_password('akend3','123454321')
    assert not grading_system.check_password('akend3','999999999')


# 3. change_grade - Staff.py
# This function will change the grade of a student and updates the database. 
# Verify that the correct grade is changed on the correct user in the database.

def test_change_grade(grading_system):
    grading_system.login('goggins', 'augurrox')
    grading_system.usr.change_grade('hdjsr7', 'software_engineering', 'assignment1', 50)
    with open('Data/users.json') as f:
            data = json.load(f)
    if data['hdjsr7']['courses']['software_engineering']['assignment1']['grade'] != 50:
        assert False

# 4. create_assignment Staff.py
# This function allows the staff to create a new assignment. 
# Verify that an assignment is created with the correct due date 
# in the correct course in the database.

def test_create_assignment(grading_system):
    grading_system.login('goggins', 'augurrox')
    grading_system.usr.create_assignment('test_assignment', '1/1/20', 'software_engineering')
    with open('Data/courses.json') as f:
        data = json.load(f)
    if data['software_engineering']['assignments']['test_assignment']['due_date'] != '1/1/20':
        assert False

# 5. add_student - Professor.py
# This function allows the professor to add a student to a course. 
# Verify that a student will be added to the correct course in the database.

def test_add_student(grading_system):
    grading_system.login('goggins', 'augurrox')
    grading_system.usr.add_student('akend3', 'software_engineering')
    with open('Data/users.json') as f:
        data = json.load(f)
    if 'software_engineering' not in data['akend3']['courses']:
        assert False

# 6. drop_student Professor.py
# This function allows the professor to drop a student in a course. 
# Verify that the student is added and dropped from the correct course in the database.

def test_drop_student(grading_system):
    grading_system.login('goggins', 'augurrox')
    grading_system.usr.drop_student('hdjsr7', 'software_engineering')
    with open('Data/users.json') as f:
        data = json.load(f)
    if 'software_engineering' in data['hdjsr7']['courses']:
        assert False

# 7. submit_assignment - Student.py
# This function allows a student to submit an assignment. 
# Verify that the database is updated with the correct assignment, 
# submission, submission dateand in the correct course.

def test_submit_assignment(grading_system):
    grading_system.login('akend3', '123454321')
    grading_system.usr.submit_assignment('databases', 'assignment1', 'new submission', '1/1/23')
    with open('Data/users.json') as f:
        data = json.load(f)
    if data['akend3']['courses']['databases']['assignment1']['submission_date'] != '1/1/23':
        assert False
    if data['akend3']['courses']['databases']['assignment1']['submission'] != 'new submission':
        assert False
    if data['akend3']['courses']['databases']['assignment1']['ontime'] == True:
        assert False

# 8. check_ontime - Student.py
# This function checks if an assignment is submitted on time. 
# Verify that it will return true if the assignment is on time, 
# and false if the assignment is late.

def test_check_ontime(grading_system):
    grading_system.login('hdjsr7', 'pass1234')
    if grading_system.usr.check_ontime('1/1/20','1/1/19') != False:
        assert False
    if grading_system.usr.check_ontime('1/1/19','1/1/20') != True:
        assert False

# 9. check_grades - Student.py
# This function returns the users grades for a specific course. 
# Verify the correct grades are returned for the correct user.

def test_check_grades(grading_system):
    grading_system.login('yted91', 'imoutofpasswordnames')
    grades = grading_system.usr.check_grades('software_engineering')
    if grades[0] != ['assignment1', 43]:
        assert False
    if grades[1] != ['assignment2', 22]:
        assert False

# 10. view_assignments - Student.py
# This function returns assignments and their due dates for a specific course. 
# Verify that the correct assignments for the correct course are returned.

def test_view_assignments(grading_system):
    grading_system.login('akend3', '123454321')
    assignments = grading_system.usr.view_assignments('databases')
    if assignments[0] != ['assignment1', '1/6/20']:
        assert False
    if assignments[1] != ['assignment2', '2/6/20']:
        assert False


# Personal test 1
# Does the program allow professors to add students to courses they're not teaching?

def test_add_student_to_other_course(grading_system):
    grading_system.login('saab', 'boomr345')
    grading_system.usr.add_student('yted91', 'databases')
    with open('Data/users.json') as f:
        data = json.load(f)
    if 'databases' in data['yted91']['courses']:
        assert False

# Personal test 2
# Does the program allow professors to remove students from courses they're not teaching?

def test_drop_student_from_other_course(grading_system):
    grading_system.login('saab', 'boomr345')
    grading_system.usr.drop_student('yted91', 'cloud_computing')
    with open('Data/users.json') as f:
        data = json.load(f)
    if 'cloud_computing' not in data['yted91']['courses']:
        assert False

# Personal test 3
# Does the program allow a staff member to create an assignment in a course they don't teach?

def test_create_assignment_for_other_course(grading_system):
    grading_system.login('saab', 'boomr345')
    grading_system.usr.create_assignment('Malicious assignment', '12/12/24', 'cloud_computing')
    with open('Data/courses.json') as f:
        data = json.load(f)
    if 'Malicious assignment' in data['cloud_computing']['assignments']:
        assert False

# Personal test 4
# What if a user tries to check grades from a course they aren't apart of?

def test_check_grades_from_wrong_course(grading_system):
    grading_system.login('yted91', 'imoutofpasswordnames')
    grades = grading_system.usr.check_grades('comp_sci')


# Personal test 5
# Is a TA allowed to change a grade in a course they don't teach?

def test_change_grade_for_wrong_course(grading_system):
    grading_system.login('cmhbf5', 'bestTA')
    with open('Data/users.json') as f:
        data = json.load(f)
    grading_system.usr.change_grade('akend3', 'databases', 'assignment1', 50)
    with open('Data/users.json') as f:
        data2 = json.load(f)
    if data['akend3']['courses']['databases']['assignment1']['grade'] != data2['akend3']['courses']['databases']['assignment1']['grade']:
        assert False


@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem
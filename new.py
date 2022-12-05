import sqlite3
import bcrypt
import csv
from datetime import datetime

connection = sqlite3.connect("capstone.db")
cursor = connection.cursor()


def competency_tracking_tool():
    with open("capstone.sql") as db:
        data = db.read()

    cursor.executescript(data)
    connection.commit()


def login_menu():
    print(
        """
    Competency Tracking Tool
    ************************
    Login
    -----"""
    )

    email = input("Enter Email: ")
    password = input("Enter Password: ")

    email_check = "SELECT password, user_type FROM Users WHERE email = ?;"

    result = cursor.execute(email_check, (email,)).fetchone()

    hashed_pass = result[0]
    user_type = result[1]

    if hashed_pass == password:
        if user_type == "user":
            while True:
                user_menu()

        elif user_type == "manager":
            while True:
                manager_menu()
    else:
        print("Incorrect Information")
    return


def user_menu():
    while True:
        print(
            """
        Competency Tracking Tool
        ************************

        User Menu
        ---------
        1. View competency and assessment data
        2. Change name
        3. Change password
        4. Log Out
        """
        )
        option = input("Enter Option: ")
        if option == "1":
            view_comp_ass_data()
        elif option == "2":
            change_name()
        elif option == "3":
            change_password()
        elif option == "4":
            print("You have been logged out.")
            break
        else:
            print("Choose from Menu.")
        return


def manager_menu():
    while True:
        print(
            """
        Competency Tracking Tool
        ************************

        Manager Menu
        ------------
        1. view all users(in a list)
        2. search for users(by first or last name)
        3. view a report of all users and their competency levels for a given competency
        4. view a competency level report for an individual user
        5. view a list of assessments for a given user
        6. Add (user, competency, assessment to a competency, assessment result for a user for an assessment)
        7. Edit (user info, competency, assessment, assessment result(update/delete))
        8. Export report to CSV (competency report by competency and users, competency report for a single user) 
        9. Import assessment results from CSV (contains columns- user_id, assessment_id, score, date_taken)
        10. Log Out
        """
        )
        return


class Users:
    def __init__(
        user,
        first_name,
        last_name,
        phone,
        email,
        password,
        hire_date,
        user_type=0,
        user_id=None,
        date_created=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        active=True,
    ):

        user.user_id = (user_id,)
        user.first_name = (first_name,)
        user.last_name = (last_name,)
        user.phone = (phone,)
        user.email = (email,)
        user.password = bcrypt.hashpw(password.encode(), salt=bcrypt.gensalt()).decode()
        user.hire_date = (hire_date,)
        user.user_type = user_type
        user.date_created = (date_created,)
        user.active = (active,)
        pass


class Competencies:
    def __init__(
        self,
        comp_name,
        comp_id=None,
        date_created=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ):
        self.comp_id = (comp_id,)
        self.comp_name = (comp_name,)
        self.date_created = date_created
        return


class Assessment_Results:
    def __init__(
        assr,
        user_id,
        score,
        manager,
        result_id=None,
        ass_id=None,
        date_taken=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ):
        assr.result_id = (result_id,)
        assr.user_id = (user_id,)
        assr.score = (score,)
        assr.date_taken = (date_taken,)
        assr.manager = (manager,)
        assr.ass_id = ass_id
        return


class Assessment_Data:
    def __init__(assd, ass_id, comp_id, date_created):
        assd.ass_id = (ass_id,)
        assd.comp_id = (comp_id,)
        assd.date_created = (date_created,)
        return


def view_comp_and_ass_data():
    view = cursor.execute(
        """SELECT (Competencies.comp_name, Assessment_Results.(ass_id, score, date_taken, manager) FROM Competencies
                          JOIN Assessment_Data
                          ON Competencies.comp_id = Assessment_Data.comp_id
                          JOIN Assessment_results
                          ON Assessment_Data.ass_id = Assessmrnt_Results.ass_id;"""
    )
    result = cursor.execute(view).fetchall()
    headers = [
        "Comp Name",
        "Assessment_ID",
        "User ID",
        "Score",
        "Date Taken",
        "Manager",
    ]
    print(
        #    comp name      assessment id     user id         score         date taken      manager
        f"{headers[0]:<11}{headers[1]:>5}{headers[2]:>5}{headers[3]:>5}{headers[4]:>10}{headers[5]:>14}"
    )
    print(
        f'{"---------":<11}{"------------":>5}{"----------":>5}{"-------------":>5}{"-----------":>10}{"---------------":>14}'
    )
    for row in result:
        row = [str(i) for i in row]
        print(
            f"{row[0]:<11}{row[1]:>5}{row[2]:>8}{row[3]:>5}{row[4]:>10}{row[5]:>14}"
        )

    return
# change name/edit password

def add(user):
    query = """INSERT INTO Users (first_name, phone, email, password, active, date_created, hire_date, user_type) 
               VALUES (?,?,?,?,?,?,?,?)"""
    cursor.execute(
        query,
        (
            user.first_name,
            user.last_name,           
            user.phone,
            user.email,
            user.password,
            user.active,
            user.date_created,
            user.hire_date,
            user.user_type
        )
    )
    connection.commit()
    return 

def update_user_info():

def change_own_info():
    view_users()
    user = input("What is the user id of employee to ipdate?: ")         
    query = """UPDATE Users
               SET ?,?,?,?,?
               WHERE user_id = ?"""

    fields = ['first_name',
              'last_name',
              'phone',
              'email',
              'password',
              ]
    values = []

    for field in fields:
        values.append(input(f"{field}: "))

    first_name =values[0]
    last_name = values[1]
    phone = values[2]
    email = values[3]
    password = values[4]
    update = Users(first_name, last_name, phone, email, password)
    update.update()
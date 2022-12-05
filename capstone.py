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


competency_tracking_tool()

# class Users:
#     def __init__(self, user_id, first_name, last_name, phone, email,
#     password, date_created, hire_date, user_type):

#         self.user_id = user_id,
#         self.first_name = first_name,
#         self.last_name = last_name,
#         self.phone = phone,
#         self.email = email,
#         self.password = password,
#         self.active = True,
#         self.date_created = date_created,
#         self.hire_date = hire_date,
#         self.user_type = user_type
#         pass


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


def view_comp_ass_data():
    #   if doesnt work change parenthesis to . on line 72
    view = """SELECT (Competencies.*, Assessment_Data.*) FROM Competencies
    JOIN Assessment_Data ON
    Assessment_Data(competency_name) = Competencies(competency_name)
    );"""
    result = cursor.execute(view).fetchall()
    headers = [
        "Comp ID",
        "Comp Name",
        "Date Created",
        "Result ID",
        "User ID",
        "Score",
        "Date Taken",
        "Manager",
    ]
    print(
        #    comp id        comp name      date created     result id       user id         score           date taken      manager
        f"{headers[0]:<11}{headers[1]:>13}{headers[2]:>14}{headers[3]:>18}{headers[4]:>14}{headers[5]:>14}{headers[6]:>14}{headers[7]:>10}"
    )
    print(
        f'{"---------":<11}{"-----------":>13}{"----------":>14}{"-------------":>18}{"-----------":>14}{"---------------":>14}{"---------------":>10}'
    )
    for row in result:
        row = [str(i) for i in row]
        print(
            f"{row[0]:<11}{row[1]:>13}{row[2]:>14}{row[3]:>18}{row[4]:>14}{row[5]:>14}{row[6]:>14}{row[7]:>10}"
        )

    return


def change_name():
    user = input("Enter user id: ")
    new_f_name = input("Enter new first name: ").title()
    new_l_name = input("Enter new last name: ").title()
    enter = f"""UPDATE Users SET (first_name, last_name) = (?,?)
    WHERE user_id = ?;"""
    cursor.execute(enter, (new_f_name, new_l_name, user))
    connection.commit()
    return


def change_password():
    # need to hash password
    user = input("Enter user id: ")
    new_pasword = input("Enter new password: ")
    check = input("Re-enter new password: ")
    if new_pasword == check:
        enter = f"""UPDATE Users SET password = ?
     WHERE user_id = ?"""
    cursor.execute(enter, (new_pasword, user))
    connection.commit()
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


def view_all_users():
    active = cursor.execute(
        """
    SELECT * FROM Users
    WHERE active = 1,0;
    """
    )

    headers = [
        "User ID",
        "First Name",
        "Last Name",
        "Phone",
        "Email",
        "Password",
        "Active",
        "Date Created",
        "Hire Date",
        "User Type",
    ]
    print(
        #    person id     first name     last name      phone          email          password       active        date created     hire date      user type
        f"{headers[0]:11}{headers[1]:13}{headers[2]:12}{headers[3]:24}{headers[4]:14}{headers[5]:14}{headers[6]:18}{headers[7]:10}{headers[8]:10}{headers[9]:13}"
    )
    print(
        f'{"---------":11}{"-----------":13}{"----------":12}{"----------------------":24}{"-------------":14}{"-----------":14}{"---------------":18}{"--------":10}{"-----------":10}{"------":13}'
    )
    # rows = cursor.execute(active)
    for row in active:
        row = [str(i) for i in row]
        print(
            f"{row[0]:<11}{row[1]:13}{row[2]:12}{row[3]:<24}{row[4]:14}{row[5]:14}{row[6]:<18}{row[7]:10}{row[8]:10}{row[9]:<13}"
        )

    return


def name_search():
    search = input("What is the first or last name of employee you are looking for?: ")
    enter = """SELECT * FROM Users WHERE first_name LIKE ? OR last_name LIKE ?"""
    results = cursor.execute(enter, (search, search))
    headers = [
        "User ID",
        "First Name",
        "Last Name",
        "Phone",
        "Email",
        "Password",
        "Active",
        "Date Created",
        "Hire Date",
        "User Type",
    ]
    print(
        #    person id     first name     last name      phone          email          password       active        date created     hire date      user type
        f"{headers[0]:11}{headers[1]:13}{headers[2]:12}{headers[3]:24}{headers[4]:14}{headers[5]:14}{headers[6]:18}{headers[7]:10}{headers[8]:10}{headers[9]:13}"
    )
    print(
        f'{"---------":11}{"-----------":13}{"----------":12}{"----------------------":24}{"-------------":14}{"-----------":14}{"---------------":18}{"--------":10}{"-----------":10}{"------":13}'
    )
    # rows = cursor.execute(active)
    for row in results:
        row = [str(i) for i in row]
        print(
            f"{row[0]:<11}{row[1]:13}{row[2]:12}{row[3]:<24}{row[4]:14}{row[5]:14}{row[6]:<18}{row[7]:10}{row[8]:10}{row[9]:<13}"
        )

    return


def view_all_competencies():
    results = cursor.execute("""SELECT * FROM Competencies""")

    headers = [
        "User ID",
        "Competency Name" "Date Created",
    ]
    print(
        #    person id     first name     last name
        f"{headers[0]:11}{headers[1]:13}{headers[2]:12}"
    )
    print(f'{"---------":11}{"-----------":13}{"----------":12}')
    for row in results:
        row = [str(i) for i in row]
        print(f"{row[0]:<11}{row[1]:13}{row[2]:12}")

    return


def view_report_users_comp_lvl():
    view_all_competencies()
    competency = input("What comp_id are you checking?: ")
    results = cursor.execute(
        f"""SELECT (user_id, first_name, last_name, score) FROM Users, Assessment_Results
    WHERE User.user_id = Assessment_Results.user_id and comp_id = ?;""",
        (competency,),
    )
    headers = [
        "User ID",
        "First Name",
        "Last Name",
        "Score",
    ]
    print(
        #    user id     first name     last name        score
        f"{headers[0]:11}{headers[1]:13}{headers[2]:12}{headers[3]:10}"
    )
    print(f'{"---------":11}{"-----------":13}{"----------":12}{"---------":10}')

    for row in results:
        row = [str(i) for i in row]
        print(f"{row[0]:<11}{row[1]:13}{row[2]:12}{row[3]:<10}")

    return


def view_user_comps():
    view_all_users()
    competency = input("What is the user_id of employee you are checking?: ")
    results = cursor.execute(
        f"""SELECT (user_id, first_name, last_name, score) FROM Users, Assessment_Results
    WHERE User.user_id = Assessment_Results.user_id and comp_id = ?;""",
        (competency,),
    )
    headers = [
        "User ID",
        "First Name",
        "Last Name",
        "Score",
    ]
    print(
        #    user id     first name     last name        score
        f"{headers[0]:11}{headers[1]:13}{headers[2]:12}{headers[3]:10}"
    )
    print(f'{"---------":11}{"-----------":13}{"----------":12}{"---------":10}')

    for row in results:
        row = [str(i) for i in row]
        print(f"{row[0]:<11}{row[1]:13}{row[2]:12}{row[3]:<10}")

    return


def view_list_of_ass_user():
    view_all_users()
    user = input("What is the user_id of employee you are checking?: ")
    # this needs work, need to use user
    results = cursor.execute(
        f"""SELECT (Users.user_id, Users.first_name, Users.last_name, Assessment_Data.competency_name,
            Assessment_Results.date_taken, Assessment_Results.score) FROM Users
            WHERE Users.user_id = ?
    LEFT JOIN Assessment_Results
    ON Users.user_id = Assessment_Results.user_id
    LEFT JOIN  Assessment_Data
    ON Assessment_Results.assessment_id = Assessment_Data.assessment_id;       
    """
    )
    connection.commit()

    headers = [
        "User ID",
        "First Name",
        "Last Name",
        "Competency",
        "Date Taken" "Score",
    ]
    print(
        #    user id     first name     last name        competency       score
        f"{headers[0]:11}{headers[1]:13}{headers[2]:12}{headers[3]:10}{headers[4]:10}{headers[5]:10}"
    )
    print(
        f'{"---------":11}{"-----------":13}{"----------":12}{"---------":10}{"----------":1}{"---------":10}'
    )

    for row in results:
        row = [str(i) for i in row]
        print(f"{row[0]:<11}{row[1]:13}{row[2]:12}{row[3]:<10}{row[4]:12}{row[5]:<10}")

    return


def add_user():
    f_name = print(input("First Name: "))
    l_name = print(input("Last Name: "))
    phone = print(input("Phone: "))
    email = print(input("Email: "))
    # password = print(input("password: ")) <--DEFAULT INSERT (make them change on first login)
    hire_date = print(input("Hire Date: "))
    type = print(input("User Type: "))
    cursor.execute(
        f"""INSERT INTO Users (first_name, last_name, phone, email, hire_date, user_type )
    VALUES (?,?,?,?,?,?);""",
        (f_name, l_name, phone, email, hire_date, type),
    )
    connection.commit()


def add_competency():
    name = input("What is the name of the new competency?: ")
    #  this should work
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    add = """INSERT INTO Competencies (comp_name, date_created)
    VALUES (?,?);"""
    cursor.execute(add, (name, date))
    connection.commit()


def add_ass_to_comp():
    view_all_competencies()
    comp = input("What is the comp_id of the competency you are adding?: ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    add = """INSERT INTO Assessment_Data (comp_id,date_created)
    VALUES (?,?);"""
    cursor.execute(add, (comp, date))
    connection.commit()


def add_assr_for_user_for_ass():
    view_all_users()
    user = input("What is the user id of emplyee?: ")
    score = input("Assessment score: ")
    date = input("Date taken: ")
    assessment = input("Assessment ID: ")
    manager = input("Manager: ")
    add = """INSERT INTO Assessment_Results (user_id, score, date_taken, assessment_id,  manager)
    VALUES (?,?,?,?,?);"""
    cursor.execute(add, (user, score, date, assessment, manager))
    connection.commit()


def edit_1():
    view_all_users()
    edit = input("What is the user id of employee to update?: ")
    f_name = input("First Name: ")
    query = f"""UPDATE Users 
    SET first_name = ?
    WHERE user_id = ?;"""
    cursor.execute(query, (f_name, edit))
    connection.commit()
    return


def edit_2():
    view_all_users()
    edit = print(input("What is the user id of employee to update?: "))
    l_name = print(input("Last Name: "))
    query = f"""UPDATE Users 
    SET last_name = ?
    WHERE user_id = ?;"""
    cursor.execute(query, (l_name, edit))
    connection.commit()
    return


def edit_3():
    view_all_users()
    edit = print(input("What is the user id of employee to update?: "))
    phone = print(input("Phone: "))
    query = f"""UPDATE Users (phone)
    SET phone = ?
    WHERE user_id = ?;"""
    cursor.execute(query, (phone, edit))
    connection.commit()
    return


def edit_4():
    view_all_users()
    edit = print(input("What is the user id of employee to update?: "))
    email = print(input("Email: "))
    query = f"""UPDATE Users (email)
    SET email = ?
    WHERE user_id = ?;"""
    cursor.execute(query, (email, edit))
    connection.commit()
    return


def edit_5():
    view_all_users()
    edit = print(input("What is the user id of employee to update?: "))
    password = print(input("Password: "))
    query = f"""UPDATE Users 
    SET password = ? 
    WHERE user_id = ?;"""
    cursor.execute(query, (password, edit))
    connection.commit()
    return


def edit_6():
    view_all_users()
    edit = print(input("What is the user id of employee to update?: "))
    type = print(input("User Type: "))
    query = f"""UPDATE Users 
    SET user_typ = ?
    WHERE user_id = ?;"""
    cursor.execute(query, (type, edit))
    connection.commit()
    return


def edit_7():
    view_all_users()
    edit = print(input("What is the user id of employee to update?: "))
    active = print(input("Active: "))
    query = f"""UPDATE Users 
    SET active = ?
    WHERE user_id = ?;"""
    cursor.execute(query, (active, edit))
    connection.commit()
    return


def edit_user_info():
    print(
        """
    User Info To Edit
    -----------------
    1. First Name
    2. Last Name
    3. Phone
    4. Email
    5. Password
    6. User Type
    7. Active
    8. Back To Manager Menu"""
    )

    edit = print(input("Choose from menu: "))
    if edit == "1":
        edit_1()
    elif edit == "2":
        edit_2()
    elif edit == "3":
        edit_3()
    elif edit == "4":
        edit_4()
    elif edit == "5":
        edit_5()
    elif edit == "6":
        edit_6()
    elif edit == "7":
        edit_7()
    elif edit == "8":
        manager_menu()
    else:
        print("Choose from menu.")
    return


def edit_competency():
    view_all_competencies()
    edit = print(input("What is the comp id of the competency to edit?: "))
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update = """UPDATE Competencies 
    SET competency_name = ?;"""
    cursor.execute(update, (edit, date))
    connection.commit()
    return


def edit_assessment_result():
    view_comp_ass_data()
    edit = input("What is the result id of assessment to edit?: ")

    # what is the assessment id to edit


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


def add():
    print(
        """
    Add Menu
    --------
    1. User Info
    2. Competency
    3. Assessment to a competency
    4. Assessment result for a user for an assessment
    5. Back to Manager Menu
    6. Log Out"""
    )
    return


def edit():
    print(
        """
    Edit Menu
    ---------
    1. User Info
    2. Competency
    3. Assessment 
    4. Assessment Result
    5. Back to Manager Menu
    6. Log Out"""
    )
    return


def export_to_csv():
    print(
        """
    Export Menu
    ---------
    1. competency report by competency and users
    2. competency report for a single user
    3. Back to Manager Menu
    4. Log Out"""
    )
    return


def import_to_csv():
    ("contains columns- user_id, assessment_id, score, date_taken")
    return

import sqlite3
import bcrypt
import csv
from datetime import datetime
from pprint import pprint

connection = sqlite3.connect("capstone.db")
cursor = connection.cursor()


def competency_tracking_tool():
    with open("capstone.sql") as db:
        data = db.read()

    cursor.executescript(data)
    connection.commit()


def login_menu():
    while True:
        print(
            """
Competency Tracking Tool
************************
Log In
------"""
        )

        email = input("Enter Email: ")
        password = input("Enter Password: ").encode()
        # hashed_pass = bcrypt.hashpw(password, salt=bcrypt.gensalt())

        email_check = "SELECT user_id, password, user_type FROM Users WHERE email = ?;"
        result = cursor.execute(email_check, (email,)).fetchone()

        user_id = result[0]
        hashed_pass = result[1]
        user_type = result[2]

        if bcrypt.checkpw(password, hashed_pass):
            if user_type == 0:
                while True:
                    user_menu(user_id)

            elif user_type == 1:
                while True:
                    manager_menu(user_id)
        else:
            print("Incorrect Information")
        return user_id


def get_user(user_id):
    user = cursor.execute(
        "SELECT * FROM Users WHERE user_id = ?;", (user_id,)
    ).fetchone()
    # user_id = user[0]
    # first_name = user[1]
    current_user = Users(
        # first   last     phone    email     pass    hiredate   type      id
        user[1],
        user[2],
        user[3],
        user[4],
        user[5],
        user[8],
        user[9],
        user[0],
    )
    return current_user


def user_menu(user_id):
    while True:
        current_user = get_user(user_id)
        print(
            """
Competency Tracking Tool
************************

User Menu
---------
1. View competency and assessment data
2. Change Info
3. Change password
4. Log Out
"""
        )
        option = input("Enter Option: ")
        if option == "1":
            view_comp_and_ass_data()

        elif option == "2":
            new_first_name = input("First Name: ")
            new_last_name = input("Last Name: ")
            new_phone = input("Phone: ")
            new_email = input("Email: ")

            current_user.first_name = new_first_name
            current_user.last_name = new_last_name
            current_user.phone = new_phone
            current_user.email = new_email
            current_user.update_db()

        elif option == "3":
            new_password = input("Password: ")
            current_user.password = new_password
            current_user.update_db()

        elif option == "4":
            print("You have been logged out.")
            break

        else:
            print("Choose from Menu.")
        return


def manager_menu(manager_id):
    while True:
        # manager_user = get_user(manager_id)
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
8. Export competency report to CSV  
9. Export report for single user to CSV
10. Import assessment results from CSV (contains columns- user_id, assessment_id, score, date_taken)
11. Log Out
"""
        )
        option = input("Choose Option: ")
        if option == "1":
            view_all_users()
        elif option == "2":
            search_users()
        elif option == "3":
            competency_results_summary_all_users()
        elif option == "4":
            user_comp_summary()
        elif option == "5":
            view_all_users()
            user_id = input("What is the id of employee?: ")
            view_comp_and_ass_data(user_id)
        elif option == "6":
            add_menu(manager_id)
        elif option == "7":
            edit_menu(manager_id)
        elif option == "8":
            comp_report_to_csv()
        elif option == "9":
            comp_report_single_to_csv()
        elif option == "10":
            import_csv()
        elif option == "11":
            print("You have been logged out.")
            login_menu()
        else:
            print("Choose from menu.")


# user_menu()
# manager_menu()


def edit_menu(manager_id):
    while True:
        print(
            """
Edit Menu
---------
1. User Info
2. Competency        
3. Assessment Result
4. Delete Assessment Result
5. Back to Manager Menu
6. Log Out"""
        )
        option = input("What info do you need to edit?: ")
        if option == "1":
            view_all_users()
            user_id = input("user id of employee to edit: ")
            user = query_user_object(user_id)
            new_first_name = input("First Name: ")
            new_last_name = input("Last Name: ")
            new_phone = input("Phone: ")
            new_email = input("Email: ")
            new_password = input("Password: ")
            active = input("Active: ")
            user_type = input("User Type: ")

            user.first_name = new_first_name
            user.last_name = new_last_name
            user.phone = new_phone
            user.email = new_email
            user.password = new_password
            user.active = active
            user.user_type = user_type
            user.update_db()

        elif option == "2":
            view_all_comps()
            comp_id = input("What is the ID of competency to edit?: ")
            comp = query_comp_object(comp_id)
            new_comp_name = input("New Competency Name: ")
            new_date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            comp.comp_name = new_comp_name
            comp.date_created = new_date_created
            comp.update_db()

        # elif option == "3":
        #     view_all_ass()
        # #    not sure what to edit

        elif option == "3":
            view_comp_and_ass_data(manager_id)
            result_id = input("Result ID of assessment to edit: ")
            assr = query_assr_object(result_id)
            new_score = input("Score: ")
            new_date_taken = input("Date Taken: ")
            new_manager_id = input("Manager ID: ")

            assr.score = new_score
            assr.date_taken = new_date_taken
            assr.manager_id = new_manager_id

            assr.update_db()
        elif option == "4":
            del_assr()
            # del_assr.update_db()

        elif option == "5":
            manager_menu(manager_id)
        elif option == "6":
            print("You have been logged out.")
            login_menu()
        else:
            print("Choose from menu.")
            return


def add_menu(manager_id):
    while True:
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
        option = input("Choose from menu: ")

        if option == "1":
            # create_user_object()
            # user = create_user_object()
            add_user()
        elif option == "2":
            add_new_comp()
        elif option == "3":
            add_new_ass()
        elif option == "4":
            add_new_assr()
        elif option == "5":
            manager_menu(manager_id)
        elif option == "6":
            print("You have been logged out")
            login_menu()
        else:
            print("Choose from menu.")
        return

        # Menu 6, Add user:

        # new_user = create_user_object()
        # id = input()
        # edit_user = get_user(id)
        # add(new_user)
        # return


class Users:
    def __init__(
        user,
        first_name,
        last_name,
        phone,
        email,
        hire_date,
        password="password1",
        user_type=0,
        date_created=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        active=True,
        user_id=None,
    ):

        user.user_id = ((user_id),)
        user.first_name = ((first_name),)
        user.last_name = ((last_name),)
        user.phone = ((phone),)
        user.email = ((email),)
        user.hire_date = ((hire_date),)
        user.password = password
        user.user_type = user_type
        user.date_created = ((date_created),)
        user.active = ((active),)

    def update_db(user):
        query = """UPDATE Users SET first_name = ?, last_name = ?, phone = ?, email = ?, password = ?, 
            active = ?, date_created = ?, hire_date = ?, user_type = ? WHERE user_id = ?"""
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
                user.user_type,
                user.user_id,
            ),
        )
        connection.commit()


class Competencies:
    def __init__(
        comp,
        comp_name,
        comp_id=None,
        date_created=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ):
        comp.comp_name = (comp_name,)
        comp.comp_id = (comp_id,)
        comp.date_created = date_created
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


def view_comp_and_ass_data(user_id):
    view = cursor.execute(
        """SELECT Competencies.comp_name, Assessment_Results.ass_id, Assessment_Results.user_id, Assessment_Results.score, Assessment_Results.date_taken,
           Assessment_Results.manager_id, Assessment_Results.result_id FROM Competencies
           LEFT OUTER JOIN Assessment_Data
           ON Competencies.comp_id = Assessment_Data.comp_id
           LEFT OUTER JOIN Assessment_results
           ON Assessment_Data.ass_id = Assessment_Results.ass_id
           WHERE user_id = ?;""",
        (user_id,),
    )

    # result = cursor.execute(view, (user_id,)).fetchall()
    headers = [
        "Comp Name",
        "Assessment ID",
        "User ID",
        "Score",
        "Date Taken",
        "Manager ID",
        "Result ID",
    ]
    print(
        #    comp name      assessment id     user id         score       date taken      manager id       result id
        f"{headers[0]:<15}{headers[1]:<15}{headers[2]:<9}{headers[3]:<7}{headers[4]:<21}{headers[5]:<12}{headers[6]:<7}"
    )
    print(
        f'{"---------":<15}{"-------------":<15}{"-------":<9}{"-----":<7}{"-------------------":<21}{"----------":<12}{"---------":<7}'
    )
    for row in view:
        row = [str(i) for i in row]
        print(
            f"{row[0]:<15}{row[1]:<15}{row[2]:<9}{row[3]:<7}{row[4]:<21}{row[5]:<12}{row[6]:<7}"
        )

    return

    # change name/edit password
    # def change_own_info(user_id): not needed, done in user menu

    fields = [
        "First Name",
        "Last Name",
        "Phone",
        "Email",
        "Password",
    ]

    values = []

    for field in fields:
        values.append(input(f"{field}: "))

    first_name = values[0]
    last_name = values[1]
    phone = values[2]
    email = values[3]
    password = values[4]
    update = Users(first_name, last_name, phone, email, password)
    update.update_db()
    return


def create_user_object():
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    password = "password1"
    active = 1
    date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hire_date = input("Hire Date(format yyyy/mm/dd): ")
    user_type = 0
    password = bcrypt.hashpw(password.encode(), salt=bcrypt.gensalt()).decode()

    user_object = Users(
        first_name,
        last_name,
        phone,
        email,
        hire_date,
        password,
        user_type,
        date_created,
        active,
    )

    return user_object


def create_comp_object():
    comp_id = input("Comp ID: ")
    comp_name = input("COmp Name: ")
    date_created = input("Date Created: ")

    comp_object = Competencies(comp_id, comp_name, date_created)
    return comp_object


def create_assr_object():
    result_id = input("Result ID: ")
    user_id = input("User ID: ")
    score = input("Score: ")
    date_taken = input("Date Taken: ")
    manager_id = input("Manager ID: ")
    ass_id = input("Assessment ID: ")

    assr_object = Assessment_Results(
        result_id, user_id, score, date_taken, manager_id, ass_id
    )
    return assr_object


def query_user_object(user_id):
    query = "SELECT * FROM Users WHERE user_id = ?"
    user_tuple = cursor.execute(query, (user_id,))

    first_name = user_tuple[0]
    last_name = user_tuple[1]
    phone = user_tuple[2]
    email = user_tuple[3]
    hire_date = user_tuple[4]
    password = user_tuple[5]
    user_type = user_tuple[6]
    date_created = user_tuple[7]
    active = user_tuple[8]
    user_id = user_tuple[9]

    user_object = Users(
        user_id,
        first_name,
        last_name,
        phone,
        email,
        hire_date,
        password,
        user_type,
        active,
        date_created,
    )
    return user_object


def query_comp_object(comp_id):

    query = "SELECT * FROM Competencies WHERE comp_id = ?"
    comp_tuple = cursor.execute(query, (comp_id,))

    comp_id = comp_tuple[0]
    comp_name = comp_tuple[1]
    date_created = comp_tuple[2]

    comp_object = Competencies(
        comp_id,
        comp_name,
        date_created,
    )
    return comp_object


def query_assr_object(ass_id):

    query = "SELECT * FROM Assessment_Results WHERE ass_id = ?"
    assr_tuple = cursor.execute(query, (ass_id,))

    result_id = assr_tuple[0]
    user_id = assr_tuple[1]
    score = assr_tuple[2]
    date_taken = assr_tuple[3]
    manager_id = assr_tuple[4]
    ass_id = assr_tuple[5]

    assr_object = Assessment_Results(
        result_id, user_id, score, date_taken, manager_id, ass_id
    )
    return assr_object


def view_all_users():
    active = cursor.execute(
        """
    SELECT user_id,first_name,last_name,phone,email,active,date_created,hire_date,user_type FROM Users;
    """
    )

    headers = [
        "User ID",
        "First Name",
        "Last Name",
        "Phone",
        "Email",
        "Active",
        "Date Created",
        "Hire Date",
        "User Type",
    ]
    print(
        #    person id     first name     last name      phone          email          active        date created     hire date      user type
        f"{headers[0]:8}{headers[1]:13}{headers[2]:14}{headers[3]:12}{headers[4]:20}{headers[5]:8}{headers[6]:14}{headers[7]:14}{headers[8]:8}"
    )
    print(
        f'{"-------":8}{"-----------":13}{"----------":14}{"------------":12}{"--------------------":20}{"---------------":8}{"--------":14}{"-----------":14}{"------":8}'
    )

    for row in active:
        row = [str(i) for i in row]
        print(
            f"{row[0]:<8}{row[1]:<13}{row[2]:<14}{row[3]:<12}{row[4]:<20}{row[5]:<8}{row[6]:<14}{row[7]:<14}{row[8]:<8}"
        )

    return


def search_users():
    search = input("What is the first or last name of employee to search?: ")
    search = f"%{search}%"
    active = """
    SELECT user_id,first_name,last_name,phone,email,active,date_created,hire_date,user_type
    FROM Users WHERE first_name LIKE ? OR last_name LIKE ?;
    """
    rows = cursor.execute(active, (search, search))

    headers = [
        "User ID",
        "First Name",
        "Last Name",
        "Phone",
        "Email",
        "Active",
        "Date Created",
        "Hire Date",
        "User Type",
    ]
    print(
        #    user id      first name     last name      phone          email          active        date created     hire date      user type
        f"{headers[0]:11}{headers[1]:13}{headers[2]:13}{headers[3]:12}{headers[4]:20}{headers[5]:8}{headers[6]:21}{headers[7]:12}{headers[8]:9}"
    )
    print(
        f'{"-------":11}{"-----------":13}{"----------":13}{"----------":12}{"------------------":20}{"------":8}{"-------------------":21}{"-----------":12}{"---------":9}'
    )
    # rows = cursor.execute(active)
    for row in rows:
        row = [str(i) for i in row]
        print(
            f"{row[0]:<11}{row[1]:<13}{row[2]:<13}{row[3]:<12}{row[4]:<20}{row[5]:<8}{row[6]:<21}{row[7]:<12}{row[8]:<9}"
        )

    return


def competency_results_summary_all_users():
    view_all_comps()
    # comp name, average score for all users for searched comp,
    # list of users with info- name, comp score, most recent assessment, most recent date taken
    search = input("What is the competency name you are searching for?: ")
    report = """SELECT Competencies.comp_name, Users.user_id, Users.first_name, Users.last_name,
                        Assessment_Results.ass_id, Assessment_Results.score, 
                        Assessment_Results.date_taken
                FROM Competencies
                LEFT JOIN Assessment_Data 
                ON  Competencies.comp_id = Assessment_Data.comp_id
                LEFT JOIN Assessment_Results
                ON Assessment_Results.ass_id = Assessment_Data.ass_id
                LEFT JOIN Users 
                ON Assessment_Results.user_id = Users.user_id
                WHERE comp_name LIKE ?;"""

    rows = cursor.execute(report, (search,))

    headers = [
        "Comp Name",
        "User ID",
        "First Name",
        "Last Name",
        "Assessment ID",
        "Score",
        "Date Taken",
    ]

    print(
        #    comp name     user id          first name     last name         ass id          score          date taken
        f"{headers[0]:<11}{headers[1]:<11}{headers[2]:<13}{headers[3]:<12}{headers[4]:<16}{headers[5]:<8}{headers[6]:<14}"
    )
    print(
        f'{"---------":<11}{"---------":<11}{"-----------":<13}{"----------":<12}{"---------------":<16}{"------":<8}{"-----------":<14}'
    )

    for row in rows:
        row = [str(i) for i in row]
        print(
            f"{row[0]:<11}{row[1]:<11}{row[2]:<13}{row[3]:<12}{row[4]:<16}{row[5]:<8}{row[6]:<14}"
        )

    return report


def view_all_comps():
    active = cursor.execute(
        """
    SELECT comp_id, comp_name, date_created FROM Competencies;
    """
    )

    headers = ["Comp ID", "Comp Name", "Date Created"]
    print(
        #    comp id        comp name       date created
        f"{headers[0]:<11}{headers[1]:<13}{headers[2]:<13}"
    )
    print(f'{"---------":11}{"-----------":14}{"-----------":14}')
    for row in active:
        row = [str(i) for i in row]
        print(f"{row[0]:<11}{row[1]:<13}{row[2]:<13}")

    return


def user_comp_summary():

    view_all_users()
    search = input("What is the user id of user to check?: ")
    view = """SELECT Users.user_id, Users.first_name, Users.last_name, Competencies.comp_name, Assessment_Results.score, 
              Assessment_Results.ass_id, Assessment_Results.date_taken, AVG(Assessment_Results.score)
              FROM Users
              LEFT JOIN Assessment_Results
              ON Users.user_id = Assessment_Results.user_id
              LEFT JOIN Assessment_Data
              ON Assessment_Data.ass_id = Assessment_Results.ass_id
              LEFT JOIN Competencies
              ON Assessment_Data.comp_id = Competencies.comp_id
              WHERE Users.user_id = ? and Users.active = 1
              ORDER BY Assessment_Results.date_taken DESC
              LIMIT 1;"""

    rows = cursor.execute(view, (search,))
    headers = [
        "User ID",
        "First Name",
        "Last Name",
        "comp_name",
        "Score",
        "Assessment ID",
        "Date Taken",
        "Average Score",
    ]

    print(
        #   user id        first name      last name        comp name          score         ass id         date taken      avg score
        f"{headers[0]:<11}{headers[1]:<11}{headers[2]:<13}{headers[3]:<12}{headers[4]:<7}{headers[5]:<14}{headers[6]:<22}{headers[7]:<14}"
    )
    print(
        f'{"-------":<11}{"----------":<11}{"---------":<13}{"----------":<12}{"------":<7}{"-----------":<14}{"------------------":<22}{"-----------":<13}'
    )

    for row in rows:
        row = [str(i) for i in row]
        print(
            f"{row[0]:<11}{row[1]:<11}{row[2]:<13}{row[3]:<12}{row[4]:<7}{row[5]:<14}{row[6]:<22}{row[7]:<13}"
        )


def add_user():
    f_name = print(input("First Name: "))
    l_name = print(input("Last Name: "))
    phone = print(input("Phone: "))
    email = print(input("Email: "))
    # password = print(input("password: ")) <--DEFAULT INSERT (make them change on first login)
    hire_date = print(input("Hire Date: "))
    type = print(input("User Type: "))
    add = """INSERT INTO Users (first_name, last_name, phone, email, hire_date, user_type )
             VALUES (?,?,?,?,?,?);"""
    # val = f_name, l_name, phone, email, hire_date, type
    cursor.execute(add, (f_name, l_name, phone, email, hire_date, type))
    connection.commit()


# def add_user(user):
#     query = """INSERT INTO Users (first_name, last_name, phone, email, password, active, date_created, hire_date, user_type)
#             VALUES (?,?,?,?,?,?,?,?,?);"""
#     print(user.first_name)
#     cursor.execute(
#         query,
#         (
#             user.first_name,
#             user.last_name,
#             user.phone,
#             user.email,
#             user.password,
#             user.active,
#             user.date_created,
#             user.hire_date,
#             user.user_type,
#         ),
#     )

#     connection.commit()


# def add_user() need to call function that is inside class
def add_new_comp():
    name = input("What is the name of the new competency?: ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    add = """INSERT INTO Competencies (comp_name, date_created)
             VALUES (?,?);"""

    cursor.execute(add, (name, date))
    connection.commit()


def add_new_ass():
    view_all_comps()
    id = input("What is the id of the competency for this assessment?: ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    add = """INSERT INTO Assessment_Data (comp_id, date_created)
             VALUES (?,?)"""
    cursor.execute(add, (id, date))
    connection.commit()


def add_new_assr():
    user_id = input("User ID: ")
    score = input("Score: ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    manager = input("Manager ID: ")
    ass_id = input("Assessment ID: ")
    add = """INSERT INTO Assessment_Results (user_id, score, date_taken, manager_id, ass_id)
             VALUES (?,?,?,?,?)"""
    cursor.execute(add, (user_id, score, date, manager, ass_id))
    connection.commit()


# def update_user_info():
#     view_all_users()
#     user = input("What is the user id of employee to update?: ")

# pass


def del_assr():
    view_all_users()
    user_id = input("What is the ID of employee?: ")
    view_comp_and_ass_data(user_id)
    res_id = input("What is the Result ID to delete?: ")
    query = """DELETE FROM Assessment_Results 
               WHERE result_id = ?;"""
    cursor.execute(query, (res_id,))
    connection.commit()


def comp_report_to_csv():
    with open("capstone.csv", "wt") as results_csv:
        writer = csv.writer(results_csv)

    results = competency_results_summary_all_users()
    headers = [
        "First Name",
        "Last Name",
        "Comp Name",
        "Score",
        "Assessment ID",
        "Date Taken",
    ]
    print(
        #  user id     first name  last name   comp name   score       ass id      date taken
        f"{headers[0]}{headers[1]}{headers[2]}{headers[3]}{headers[4]}{headers[5]}{headers[6]}"
    )
    writer.writerows(results)


def comp_report_single_to_csv():
    with open("capstone.csv", "wt") as results_csv:
        writer = csv.writer(results_csv)

    results = user_comp_summary()
    headers = [
        "First Name",
        "Last Name",
        "Comp Name",
        "Score",
        "Assessment ID",
        "Date Taken",
    ]
    print(
        #  user id     first name  last name   comp name   score       ass id      date taken
        f"{headers[0]}{headers[1]}{headers[2]}{headers[3]}{headers[4]}{headers[5]}{headers[6]}"
    )
    writer.writerows(results)


#  8. Export report to CSV (competency report by competency and users, competency report for a single user)
#         9. Import assessment results from CSV (contains columns- user_id, assessment_id, score, date_taken)
def import_csv():
    with open("capstone.csv", "rt") as results:
        for line in results:
            read = line.strip().split(",")
        print("User ID", "First Name", "Last Name", "Comp Name", "Score", "Date Taken")
        print(read)


login_menu()
# def temp():
#     password = "password1"
#     password = password.encode()
#     hashed_pass = bcrypt.hashpw(password, salt=bcrypt.gensalt())
#     query = """INSERT INTO Users (first_name,last_name,phone,email,password,date_created,hire_date)
#                VALUES ('first 1','last 1','1111111111','1@1.com',?,'1111/11/11','1111/11/11');
#                     """
#     cursor.execute(query, (hashed_pass,))
#     connection.commit()


# temp()

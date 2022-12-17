from datetime import datetime
import sqlite3

connection = sqlite3.connect("capstone.db")
cursor = connection.cursor()


def table1():
    cursor.executescript(
        f"""CREATE TABLE IF NOT EXISTS Users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT DEFAULT 'password1', 
        active DEFAULT 1,
        date_created TEXT,
        hire_date TEXT,
        user_type INTEGER DEFAULT 0

    );"""
    )

    connection.commit()


table1()


def table2():
    cursor.executescript(
        """CREATE TABLE IF NOT EXISTS Competencies(
        comp_id INTEGER PRIMARY KEY AUTOINCREMENT,
        comp_name TEXT,
        date_created TEXT);"""
    )
    connection.commit()


table2()


def table3():
    cursor.executescript(
        """CREATE TABLE IF NOT EXISTS Assessment_Results(
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        score INTEGER DEFAULT 0,
        date_taken TEXT,
        manager_id INTEGER,
        ass_id INTEGER, 
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
        FOREIGN KEY (manager_id) REFERENCES Users(user_id));"""
    )
    connection.commit()


table3()


def table4():
    cursor.executescript(
        """CREATE TABLE IF NOT EXISTS Assessment_Data(
        ass_id INTEGER PRIMARY KEY AUTOINCREMENT,
        comp_id TEXT,
        date_created TEXT,
        FOREIGN KEY (comp_id) REFERENCES Competencies(comp_id)
        );"""
    )
    connection.commit()


table4()

CREATE TABLE IF NOT EXISTS Users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT DEFAULT 'password1', 
    active DEFAULT 1,
    date_created NOT NULL,
    hire_date TEXT,
    user_type INTEGER);

CREATE TABLE IF NOT EXISTS Competencies(
    comp_id PRIMARY KEY INTEGER AUTOINCREMENT,
    comp_name TEXT,
    date_created TEXT

);

CREATE TABLE IF NOT EXISTS Assessment_Results(
    result_id PRIMARY KEY INTEGER AUTOINCREMENT
    user_id INTEGER,
    score TEXT,
    date_taken TEXT,
    manager_id INTEGER,
    ass_id INTEGER, 
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
    FOREIGN KEY (manager_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Assessment_Data(
    ass_id INTEGER AUTOINCREMENT PRIMARY KEY
    comp_id TEXT,
    date_created TEXT,
    FOREIGN KEY (comp_id) REFERENCES Competencies(comp_id)
    );
import sqlite3


# Connect to SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# Define the SQL schema
sql_schema = """
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin','teacher','parent'))
);

CREATE TABLE Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    parent_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,

    FOREIGN KEY (parent_id) REFERENCES Users(id),
    FOREIGN KEY (teacher_id) REFERENCES Users(id)
);

CREATE TABLE Homework(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    chapter_start INTEGER,
    chapter_end INTEGER,
    verse_start INTEGER,
    verse_end INTEGER,
    due_date DATE DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL CHECK(status IN ('completed', 'pending')),
    FOREIGN KEY (student_id) REFERENCES Students(id)
);

CREATE TABLE Task(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    status TEXT NOT NULL CHECK(status IN ('completed', 'incomplete')),
    FOREIGN KEY (student_id) REFERENCES Students(id)
);
"""

# Execute the schema
cursor.executescript(sql_schema)

print("Database schema created successfully!")

# Commit changes and close the connection
connection.commit()
connection.close()

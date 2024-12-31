import sqlite3

"""Below is the database schema/design"""
# # Connect to SQLite database (or create it if it doesn't exist)
# connection = sqlite3.connect("database.db")
# cursor = connection.cursor()
#
# # Define the updated SQL schema
# sql_schema = """
# CREATE TABLE Users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     email TEXT UNIQUE NOT NULL,
#     password TEXT NOT NULL,
#     role TEXT NOT NULL CHECK(role IN ('admin','teacher','parent'))
# );
#
# CREATE TABLE Students (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     email TEXT NOT NULL,
#     parent_id INTEGER NOT NULL,
#     teacher_id INTEGER NOT NULL,
#     classroom TEXT,
#
#     FOREIGN KEY (parent_id) REFERENCES Users(id),
#     FOREIGN KEY (teacher_id) REFERENCES Users(id)
# );
#
# CREATE TABLE Homeworks (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title TEXT NOT NULL,
#     description TEXT NOT NULL,
#     chapter_start INTEGER,
#     chapter_end INTEGER,
#     verse_start INTEGER,
#     verse_end INTEGER,
#     due_date DATE DEFAULT CURRENT_TIMESTAMP,
#     status TEXT NOT NULL CHECK(status IN ('completed', 'pending'))
# );
#
# CREATE TABLE Assignments (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     student_id INTEGER NOT NULL,
#     homework_id INTEGER,
#     task_id INTEGER,
#
#     FOREIGN KEY (student_id) REFERENCES Students(id),
#     FOREIGN KEY (homework_id) REFERENCES Homeworks(id),
#     FOREIGN KEY (task_id) REFERENCES Tasks(id)
# );
#
# CREATE TABLE Tasks (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title TEXT NOT NULL,
#     description TEXT NOT NULL,
#     start_date DATE,
#     end_date DATE,
#     status TEXT NOT NULL CHECK(status IN ('completed', 'incomplete'))
# );
# """
#
# # Execute the schema
# cursor.executescript(sql_schema)
#
# print("Updated database schema created successfully!")
#
# # Commit changes and close the connection
# connection.commit()
# connection.close()

"""Use the following code to add new column(s) to a specific table"""
# Connect to SQLite database (or create it if it doesn't exist)
# connection = sqlite3.connect("database.db")
# cursor = connection.cursor()
#
# # Alter the Students table to add the classroom column
# try:
#     cursor.execute("ALTER TABLE Homework ADD COLUMN title TEXT;")
#     print("Added 'title' column to the Homework table.")
# except sqlite3.OperationalError as e:
#     if "duplicate column name" in str(e).lower():
#         print("'title' column already exists in the Homework table.")
#     else:
#         raise e
#
# # Commit changes and close the connection
# connection.commit()
# connection.close()


"""Use the follwoing code to check table structure"""
# def check_table_structure():
#     connection = sqlite3.connect("database.db")
#     cursor = connection.cursor()
#     cursor.execute("PRAGMA table_info(Homework);")
#     columns = cursor.fetchall()
#     connection.close()
#     for column in columns:
#         print(column)
#
# check_table_structure()


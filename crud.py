import sqlite3
from typing import List, Dict, Any

from sqlalchemy.orm import contains_eager

#from dataBase import connection, cursor

DB_PATH = "database.db"

# Helper function to connect to the database
def get_db_connection():
    return sqlite3.connect(DB_PATH)

# CRUD operations for Users
def create_user(name: str, email: str, password: str, role: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Users (name, email, password, role)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, password, role),
        )
        connection.commit()
        return {"message": "User created successfully!"}
    except sqlite3.IntegrityError as e:
        return {"error": str(e)}
    finally:
        connection.close()

def get_user_by_id(user_id: int) -> Dict[str, Any]:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id))
    user = cursor.fetchone()
    connection.close()
    if user:
        return {"id": user[0], "name": user[1], "email": user[2], "role": user[4]}
    return {"error": "User not found"}

def get_all_users() -> List[Dict[str, Any]]:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    connection.close()
    return [{"id": user[0], "name": user[1], "email": user[2], "role": user[4]} for user in users]

def update_user(user_id: int, name: str = None, email: str = None, role: str = None):
    connection = get_db_connection()
    cursor = connection.cursor()
    updates = []
    params = []
    if name:
        updates.append("name = ?")
        params.append(name)
    if email:
        updates.append("email = ?")
        params.append(email)
    if role:
        updates.append("role = ?")
        params.append(role)
    params.append(user_id)
    sql = f"UPDATE Users SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(sql, tuple(params))
    connection.commit()
    connection.close()
    return {"message": "User updated successfully!"}

def delete_user(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    deleted_user = cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))
    if cursor.rowcount == 0:  # Check if no rows were affected
        connection.close()
        return {"error": "User not found or could not be deleted"}
    connection.commit()
    connection.close()
    return {"message": "User deleted successfully!"}

def create_student(name: str, email: str, password: str, parent_id: int, teacher_id: int, classroom: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # validate parent and tacher IDs
        cursor.execute("SELECT id FROM Users WHERE id = ? AND role = 'parent'", (parent_id,))
        if not cursor.fetchone():
            return {"error": "Invalid parent ID"}

        cursor.execute("SELECT id FROM Users WHERE id = ? AND role = 'teacher'", (teacher_id,))
        if not cursor.fetchone():
            return {"error": "Invalid teacher ID"}

        # Insert the new student
        cursor.execute(
            """INSERT INTO Students (name, email, parent_id, teacher_id, classroom)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, email, parent_id, teacher_id, classroom),
        )
        connection.commit()
        return {"message": "Student created successfully!"}
    except sqlite3.IntegrityError as e:
        return {"error": str(e)}
    finally:
        connection.close()


def get_student_by_id(student_id: int) -> Dict[str, Any]:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    connection.close()
    if student:
        return {"id": student[0], "name": student[1], "email": student[2], "parent id": student[3], "teacher id": student[4], "classroom": student[5]}
    return {"error": "Student not found"}

def get_students_by_teacher(teacher_id) -> List[Dict[str, Any]]:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Students WHERE teacher_id = ?", (teacher_id,))
    students = cursor.fetchall()
    connection.close()
    return [
        {"student id": student[0], "name": student[1], "email": student[2], "parent id": student[3],
         "teacher id": student[4], "classroom": student[5]}
        for student in students
    ]

def get_students_by_parent(parent_id) -> List[Dict[str, Any]]:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Students WHERE parent_id = ?", (parent_id,))
    students = cursor.fetchall()
    connection.close()
    return [
        {"student id": student[0], "name": student[1], "email": student[2], "parent id": student[3],
         "teacher id": student[4], "classroom": student[5]}
        for student in students
    ]

def get_all_students() -> List[Dict[str, Any]]:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    connection.close()
    return [{"student id": students[0], "name": students[1], "email": students[2], "parent id": students[3], "teacher id": students[4], "classroom": students[5]}]

def update_student(student_id: int, **kwargs):
    connection = get_db_connection()
    cursor = connection.cursor()
    updates = []
    params = []

    for key, value in kwargs.items():
        if key in ("name", "email", "classroom") and value:
            updates.append(f"{key} = ?")
            params.append(value)
        elif key == "parent_id":
            cursor.execute("SELECT id FROM Users WHERE id = ? AND role = 'parent'", (value,))
            if not cursor.fetchone():
                return {"error": f"Invalid parent ID: {value}"}
            updates.append("parent_id = ?")
            params.append(value)
        elif key == "teacher_id":
            cursor.execute("SELECT id FROM Users WHERE id = ? AND role = 'teacher'", (value,))
            if not cursor.fetchone():
                return {"error": f"Invalid teacher ID: {value}"}
            updates.append("teacher_id = ?")
            params.append(value)

    if not updates:
        return {"error": "No fields to update"}

    params.append(student_id)
    sql = f"UPDATE Students SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(sql, params)
    connection.commit()
    connection.close()
    return {"message": "Student updated successfully!"}

def delete_student(student_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Students WHERE id = ?", (student_id,))
    if cursor.rowcount == 0:
        connection.close()
        return {"error": "Student not found or could not be deleted"}
    connection.commit()
    connection.close()
    return {"message": "Student deleted successfully!"}

def create_homework(title: str, description: str, chapter_start: int, chapter_end: int, verse_start: int,
                    verse_end: int, due_date: int, status: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """INSERT INTO Homework (description, chapter_start, chapter_end, verse_start, verse_end, due_date, status, title)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (description, chapter_start, chapter_end, verse_start, verse_end, due_date, status, title),
        )
        connection.commit()
        return {"message": "Homework created successfully!"}
    except sqlite3.IntegrityError as e:
        return {"error": str(e)}
    finally:
        connection.close()

def get_homework_by_id(homework_id) -> Dict[str, Any]:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Homework WHERE id = ?""",(homework_id,))
    homework = cursor.fetchone()
    connection.close()
    if homework:
        return {"homework_id": homework[0], "title": homework[9], "description": homework[2], "chapter start": homework[3],
                "chapter end": homework[4], "verse start": homework[5], "verse end": homework[6], "due date": homework[7],
                "status": homework[8]}
    return {"error": "Homework not found"}

#def get_homework_by_student
#def get_homework_by_class

def update_homework(homework_id: int, **kwargs):
    connection = get_db_connection()
    cursor = connection.cursor()
    updates = []
    params = []

    for key, value in kwargs.items():
        if key in ("title", "description", "chapter_start", "chapter_end", "verse_start", "verse_end", "due_date", "status") and value is not None:
            updates.append(f"{key} = ?")
            params.append(value)

    if not updates:
        return {"error": "No fields to update"}

    params.append(homework_id)
    sql = f"UPDATE Homework SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(sql, params)
    connection.commit()
    connection.close()
    return {"message": "Homework updated successfully!"}

def delete_homework(homework_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM Homework WHERE id = ?""", (homework_id,))
    if cursor.rowcount == 0:
        connection.close()
        return {"error": "Student not found or could not be deleted"}
    connection.commit()
    connection.close()
    return {"message": "Homework deleted successfully!"}
import sqlite3
from typing import List, Dict, Any

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

def create_student(name: str, email: str, password: str, parent_id = int, teacher_id = int, classroom = str):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """INSERT INTO Students (name, email, password, parent_id, teacher_id, classroom)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, email, password, parent_id, teacher_id, classroom),
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
    return [{"student id": students[0], "name": students[1], "email": students[2], "parent id": students[3], "teacher id": students[4], "classroom": students[5]}]

def get_all_students() -> List[Dict[str, Any]]:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    connection.close()
    return [{"student id": students[0], "name": students[1], "email": students[2], "parent id": students[3], "teacher id": students[4], "classroom": students[5]}]

def update_student(student_id: int, teacher_id: int, parent_id: int, name: str = None, email: str = None, classroom: str = None):
    connection = get_db_connection()
    cursor = connection.cursor()
    updates = []
    params = []
    params.append(student_id)
    if name:
        updates.append("name = ?")
        params.append(name)
    if email:
        updates.append("email = ?")
        params.append(email)
    if classroom:
        updates.append("classroom = ?")
        params.append(classroom)
    if parent_id is not None:
        cursor.execute("SELECT id FROM Users WHERE id = ? AND role = 'parent'", (parent_id,))
        if not cursor.fetchone():
            return {"error": "Invalid parent_id: no such parent exists"}
        updates.append("parent_id = ?")
        params.append(parent_id)
    if teacher_id is not None:
        cursor.execute("SELECT id FROM Users WHERE id = ? AND role = 'teacher'", (teacher_id,))
        if not cursor.fetchone():
            return {"error": "Invalid teacher_id: no such teacher exists"}
        updates.append("teacher_id = ?")
        params.append(teacher_id)

    if not updates:
        return {"error": "No fields to update"}

    # Add the student_id for the WHERE clause
    params.append(student_id)
    sql = f"UPDATE Students SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(sql, tuple(params))
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


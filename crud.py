import sqlite3
from typing import List, Dict, Any

from anyio import connect_tcp

DB_PATH = "database.db"

# Helper function to connect to the database
def get_db_connection():
    return sqlite3.connect(DB_PATH)

# Helper function to validate ids
def validate_ids(**kwargs) -> List[bool]:
    """
    validate_ids checks whether the given ids exist within their respective
    tables. Returns a list of bools in the order of the ids given.
    :param kwargs: used_id, student_id, homework_id, task_id, teacher_id,
    parent_id, assignments_id
    :return: List[bool]
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    tables = {"user_id": "Users", "parent_id": "Users", "teacher_id": "Users",
             "student_id": "Students", "homework_id": "Homeworks",
             "task_id": "Tasks", "assignment_id": "Assignments"}
    res = []
    for key, value in kwargs.items():
        table = tables[key]
        if value is None:
            res.append(False)
        else:
            if key in ["user_id", "teacher_id", "parent_id"]:
                role = ""
                if key == "user_id":
                    role = "admin"
                else:
                    end = key.find('_')
                    role = key[:end]
                cursor.execute(f"SELECT FROM {table} WHERE id = {value} AND "
                               f"role = {role}")
            else:
                cursor.execute(f"SELECT FROM {table} WHERE id = {value}")
            if cursor.fetchone():
                res.append(True)
            else:
                res.append(False)
    connection.close()
    return res


def create_user(name: str, email: str, password: str, role: str)\
        -> Dict[str, Any]:
    """
    Creates a new user in the Users table.
    Args:
        name (str): User's name.
        email (str): User's email.
        password (str): User's password.
        role (str): User's role (e.g., 'teacher', 'parent').
    Returns:
        Dict[str, Any]: Message or error details.
    """
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
    """
    Retrieves a user's details by their ID.
    Args:
        user_id (int): User ID to retrieve.
    Returns:
        Dict[str, Any]: User details or an error message.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    connection.close()

    if user:
        return {"id": user[0], "name": user[1], "email": user[2],
                "role": user[4]}
    return {"error": "User not found"}

def get_all_users() -> List[Dict[str, Any]]:
    """
    Retrieves all users from the Users table.
    Returns:
        List[Dict[str, Any]]: List of user details.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    connection.close()

    return [
        {"id": user[0], "name": user[1], "email": user[2], "role": user[4]}
        for user in users
    ]

def update_user(user_id: int, name: str = None, email: str = None,
                role: str = None) -> Dict[str, Any]:
    """
    Updates user details in the Users table.
    Args:
        user_id (int): User ID to update.
        name (str, optional): New name for the user.
        email (str, optional): New email for the user.
        role (str, optional): New role for the user.
    Returns:
        Dict[str, Any]: Message or error details.
    """
    is_valid = validate_ids(user_id = user_id)
    if not is_valid[0]:
        return {"error": "Invalid user_id or user_id not found"}
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

    if not updates:
        connection.close()
        return {"error": "No fields to update"}

    params.append(user_id)
    sql = f"UPDATE Users SET {', '.join(updates)} WHERE id = ?"

    cursor.execute(sql, tuple(params))
    connection.commit()
    connection.close()
    return {"message": "User updated successfully!"}

def delete_user(user_id: int) -> Dict[str, Any]:
    """
    Deletes a user by their ID from the Users table.
    Args:
        user_id (int): User ID to delete.
    Returns:
        Dict[str, Any]: Message or error details.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))
    if cursor.rowcount == 0:
        connection.close()
        return {"error": "User not found or could not be deleted"}

    connection.commit()
    connection.close()
    return {"message": "User deleted successfully!"}

def create_student(name: str, email: str, password: str, parent_id: int,
                   teacher_id: int, classroom: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # validate parent and teacher IDs
        is_valid = validate_ids(parent_id = parent_id, teacher_id = teacher_id)
        if not is_valid[0]:
            return {"error": "Invalid parent ID"}
        if not is_valid[1]:
            return {"error": "Invalid teacher ID"}

        # Insert the new student
        cursor.execute(
            """INSERT INTO Students (name, email, parent_id, teacher_id, 
            classroom)
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
        return {"id": student[0], "name": student[1], "email": student[2],
                "parent id": student[3], "teacher id": student[4],
                "classroom": student[5]}
    return {"error": "Student not found"}

def get_students_by_teacher(teacher_id) -> List[Dict[str, Any]]:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Students WHERE teacher_id = ?", (teacher_id,))
    students = cursor.fetchall()
    connection.close()
    return [
        {"student id": student[0], "name": student[1], "email": student[2],
         "parent id": student[3], "teacher id": student[4],
         "classroom": student[5]}
        for student in students
    ]

def get_students_by_parent(parent_id) -> List[Dict[str, Any]]:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Students WHERE parent_id = ?", (parent_id,))
    students = cursor.fetchall()
    connection.close()
    return [
        {"student id": student[0], "name": student[1], "email": student[2],
         "parent id": student[3], "teacher id": student[4],
         "classroom": student[5]}
        for student in students
    ]

def get_all_students() -> List[Dict[str, Any]]:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    connection.close()
    return [
        {"student id": student[0], "name": student[1], "email": student[2],
         "parent id": student[3], "teacher id": student[4],
         "classroom": student[5]}
        for student in students
    ]

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
            is_valid = validate_ids(parent_id = key)
            if not is_valid[0]:
                connection.close()
                return {"error": f"Invalid parent ID: {value}"}
            updates.append("parent_id = ?")
            params.append(value)
        elif key == "teacher_id":
            is_valid = validate_ids(teacher_id = key)
            if not is_valid[0]:
                connection.close()
                return {"error": f"Invalid teacher ID: {value}"}
            updates.append("teacher_id = ?")
            params.append(value)

    if not updates:
        return {"error": "No fields to update"}

    if not validate_ids(student_id = student_id)[0]:
        connection.close()
        return {"error": "Incorrect student_id or student_id does not exist"}
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

def create_homework(title: str, description: str, chapter_start: int,
                    chapter_end: int, verse_start: int, verse_end: int,
                    due_date: int, status = "pending"):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """INSERT INTO Homework (description, chapter_start, 
            chapter_end, verse_start, verse_end, due_date, status, title)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (description, chapter_start, chapter_end, verse_start,
             verse_end, due_date, status, title),
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
        return {"homework_id": homework[0], "title": homework[9],
                "description": homework[2], "chapter start": homework[3],
                "chapter end": homework[4], "verse start": homework[5],
                "verse end": homework[6], "due date": homework[7],
                "status": homework[8]}
    return {"error": "Homework not found"}

def update_homework(homework_id: int, **kwargs):
    connection = get_db_connection()
    cursor = connection.cursor()
    updates = []
    params = []

    for key, value in kwargs.items():
        if (key in ("title", "description", "chapter_start", "chapter_end",
                   "verse_start", "verse_end", "due_date", "status")
                and value is not None):
            updates.append(f"{key} = ?")
            params.append(value)

    if not updates:
        connection.close()
        return {"error": "No fields to update"}

    if not validate_ids(homework_id = homework_id)[0]:
        connection.close()
        return {"error": "Incorrect student_id or student_id does not exist"}

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

def create_assignment(student_id: int, homework_id = None, task_id = None):

    # Validate ids
    if homework_id is not None:
        is_valid = validate_ids(student_id = student_id, homework_id =
        homework_id)
        if is_valid[0] == False or is_valid[1] == False:
            return {"error": "Invalid ids"}
    else:
        is_valid = validate_ids(student_id = student_id, task_id = task_id)
        if is_valid[0] == False or is_valid[1] == False:
            return {"error": "Invalid ids"}

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""INSERT INTO Assignments (student_id, homework_id, task_id)
        VALUES (?, ?, ?)""", (student_id, homework_id, task_id))
        connection.commit()
    except sqlite3.IntegrityError as e:
        return {"error": "Could not assign homework to student because of\n" +
                         str(e)}
    finally:
        connection.close()

# def get_student_homework(student_id) -> List[Dict[str, Any]]:
#     # Validate student_id
#     if not validate_student_id(student_id):
#         return [{"error": "Incorrect student_id or student_id does not exist"}]
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     cursor.execute("""SELECT * FROM Assignments WHERE student_id = ?""", (student_id,))
#     homeworks = cursor.fetchall()
#     connection.close()
#     homework_ids = [homeworks[1] for homework in homeworks]
#     res = []
#     for homework_id in homework_ids:
#         res.append(get_homework_by_id(homework_id))
#     return res
#
# def get_assigned_students(homework_id) -> List[Dict[str, Any]] or Dict:
#     # Validate homework_id
#     if not validate_homework_id(homework_id):
#         return {"error": "Incorrect student_id or student_id does not exist"}
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     cursor.execute("""SELECT * FROM Assignments WHERE homework_id = ?""", (homework_id,))
#     student_rows = cursor.fetchall()
#     student_ids = [student_id[2] for student_id in student_rows]
#     res = []
#     for student_id in student_ids:
#         res.append(get_student_by_id(student_id))
#     return res

def get_assignment(assignment_id: int) -> Dict[str, Any]:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Assignments WHERE id = ?", (assignment_id,))
    assignment = cursor.fetchone()
    if not assignment:
        return {"error":
                    "Invalid assignment_id or assignment_id does not exist"}
    return {"id": assignment[0], "student_id": assignment[1],
            "homework_id": assignment[2], "task_id": assignment[3]}

def update_assignment(assignment_id: int, student_id: int = None,
                      homework_id: int = None, task_id: int = None):
    connection = get_db_connection()
    cursor = connection.cursor()
    updates = []
    params = []
    if student_id is not None:
        if not validate_ids(student_id = student_id)[0]:
            connection.close()
            return {"error": "Invalid student_id or student_id does not exist"}
        updates.append("student_id = ?")
        params.append(student_id)
    if homework_id is not None:
        if not validate_ids(homework_id = homework_id)[0]:
            connection.close()
            return {"error":
                        "Invalid homework_id or homework_id does not exist"}
        updates.append("student_id = ?")
        params.append(student_id)
    if task_id is not None:
        if not validate_ids(task_id = task_id):
            connection.close()
            return {"error": "Invalid task_id or task_id does not exist"}
    params.append(assignment_id)
    sql = f"UPDATE Assignments SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(sql, tuple(params))
    connection.commit()
    connection.close()
    return {"message": "Assignment updated successfully!"}

def delete_assignment(assignment_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM Assignments WHERE id = ?""",
                   (assignment_id,))
    if cursor.rowcount == 0:
        connection.close()
        return {"error": "Assignment not found or could not be deleted"}
    connection.commit()
    connection.close()
    return {"message": "Homework Assignment deleted successfully!"}

def create_task(title: str, description: str, start_date: int = None,
                end_date: int = None, status: str = 'incomplete'):
    # Validate and dates and status:
    if start_date > end_date:
        return {"error": "The start date must be less than end date"}
    if status not in ['completed', 'incomplete']:
        return {"error":
                    "Invalid status. Status must be 'completed' or "
                    "'incomplete'."}

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""INSERT INTO Tasks (title, description, 
        start_date, end_date, status)
        VALUES (?, ?, ?, ?, ?)""", (title, description, start_date,
                                    end_date, status))
        connection.commit()
        return {"message": "Task created successfully!"}
    except sqlite3.IntegrityError as e:
        return {"error": str(e)}
    finally:
        connection.close()

def get_task_by_id(task_id: int) -> Dict[str, Any]:
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT * FROM Tasks WHERE id = ?""", (task_id,))
        task = cursor.fetchone()
        return {"task_id": task[0], "title": task[1], "description": task[2],
                "start_date": task[3], "end_date": task[4], "status": task[5]}
    except sqlite3.IntegrityError as e:
        return {"error": str(e) + "\nOr Invalid task_id or task_id does not "
                                  "exist"}
    finally:
        connection.close()

def update_task(task_id: int, title: str = None, description: str = None,
                start_date: int = None, end_date: int = None,
                status: str = None):
    is_valid = validate_ids(task_id = task_id)
    if not is_valid[0]:
        return {"error": "Invalid task_id or task_id does not exist"}
    connection = get_db_connection()
    cursor = connection.cursor()
    updates = []
    params = []

    if title is not None:
        updates.append("title = ?")
        params.append(title)
    if description is not None:
        updates.append("description = ?")
        params.append(description)
    if start_date is not None:
        updates.append("start_date = ?")
        params.append(start_date)
    if end_date is not None:
        updates.append("end_date = ?")
        params.append(end_date)
    if status is not None:
        updates.append("status = ?")
        params.append(start_date)
    sql = f"UPDATE Tasks SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(sql, tuple(params))
    connection.commit()
    connection.close()
    return {"message": "Updated tasks successfully!"}

def delete_task(task_id: int):
    is_valid = validate_ids(task_id = task_id)
    if not is_valid[0]:
        return {"error": "Invalid task_id or task_id does not exist"}
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Tasks WHERE id = ?", (task_id,))
    if cursor.rowcount == 0:
        connection.close()
        return {"error": "Task could not be deleted"}
    connection.commit()
    connection.close()
    return {"message": "Task was deleted successfully!"}

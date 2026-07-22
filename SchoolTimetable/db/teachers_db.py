from database import get_connection


def add_teacher(
    employee_id,
    teacher_code,
    teacher_name,
    qualification,
    phone,
    email,
    max_periods
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO teachers(
        employee_id,
        teacher_code,
        teacher_name,
        qualification,
        phone,
        email,
        max_periods
    )
    VALUES(?,?,?,?,?,?,?)
    """, (
        employee_id,
        teacher_code,
        teacher_name,
        qualification,
        phone,
        email,
        max_periods
    ))

    conn.commit()
    conn.close()


def get_teachers():

    conn = get_connection()

    teachers = conn.execute("""
    SELECT

        teacher_id,
        employee_id,
        teacher_code,
        teacher_name,
        qualification,
        phone,
        email,
        max_periods

    FROM teachers

    ORDER BY teacher_name
    """).fetchall()

    conn.close()

    return teachers


def get_teacher(teacher_id):

    conn = get_connection()

    teacher = conn.execute("""
    SELECT *

    FROM teachers

    WHERE teacher_id=?
    """, (teacher_id,)).fetchone()

    conn.close()

    return teacher


def delete_teacher(teacher_id):

    conn = get_connection()

    conn.execute("""
    DELETE FROM teacher_subjects
    WHERE teacher_id=?
    """, (teacher_id,))

    conn.execute("""
    DELETE FROM teacher_classes
    WHERE teacher_id=?
    """, (teacher_id,))

    conn.execute("""
    DELETE FROM teacher_availability
    WHERE teacher_id=?
    """, (teacher_id,))

    conn.execute("""
    DELETE FROM teachers
    WHERE teacher_id=?
    """, (teacher_id,))

    conn.commit()
    conn.close()


def teacher_exists(employee_id):

    conn = get_connection()

    teacher = conn.execute("""
    SELECT teacher_id

    FROM teachers

    WHERE employee_id=?
    """, (employee_id,)).fetchone()

    conn.close()

    return teacher is not None
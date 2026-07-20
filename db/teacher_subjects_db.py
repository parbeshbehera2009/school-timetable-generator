from database import get_connection


# ======================================================
# ASSIGN SUBJECT TO TEACHER
# ======================================================

def assign_subject(teacher_id, subject_id):

    conn = get_connection()

    # Prevent duplicate assignment
    exists = conn.execute("""
    SELECT id
    FROM teacher_subjects
    WHERE teacher_id=?
    AND subject_id=?
    """, (
        teacher_id,
        subject_id
    )).fetchone()

    if exists is None:

        conn.execute("""
        INSERT INTO teacher_subjects(
            teacher_id,
            subject_id
        )
        VALUES(?,?)
        """, (
            teacher_id,
            subject_id
        ))

    conn.commit()
    conn.close()


# ======================================================
# GET ALL ASSIGNMENTS
# ======================================================

def get_teacher_subjects():

    conn = get_connection()

    rows = conn.execute("""

    SELECT

        teacher_subjects.id,

        teachers.teacher_id,

        teachers.teacher_code,

        teachers.teacher_name,

        subjects.subject_id,

        subjects.subject_name

    FROM teacher_subjects

    JOIN teachers
    ON teachers.teacher_id = teacher_subjects.teacher_id

    JOIN subjects
    ON subjects.subject_id = teacher_subjects.subject_id

    ORDER BY

        teachers.teacher_name,
        subjects.subject_name

    """).fetchall()

    conn.close()

    return rows


# ======================================================
# DELETE
# ======================================================

def delete_teacher_subject(id):

    conn = get_connection()

    conn.execute("""
    DELETE FROM teacher_subjects
    WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()


# ======================================================
# FIND TEACHER FOR CLASS + SUBJECT
# ======================================================

def get_teacher_for_class_subject(class_id, subject_id):

    conn = get_connection()

    teacher = conn.execute("""

    SELECT

        teachers.teacher_id,
        teachers.teacher_name

    FROM teachers

    JOIN teacher_subjects
        ON teachers.teacher_id = teacher_subjects.teacher_id

    JOIN teacher_classes
        ON teachers.teacher_id = teacher_classes.teacher_id

    WHERE

        teacher_classes.class_id=?

    AND

        teacher_subjects.subject_id=?

    LIMIT 1

    """, (
        class_id,
        subject_id
    )).fetchone()

    conn.close()

    return teacher
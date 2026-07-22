from database import get_connection


# =====================================================
# ADD SUBJECT
# =====================================================

def add_subject(subject_name):

    conn = get_connection()

    conn.execute("""
    INSERT INTO subjects(
        subject_name
    )
    VALUES(?)
    """, (subject_name,))

    conn.commit()
    conn.close()


# =====================================================
# GET ALL SUBJECTS
# =====================================================

def get_subjects():

    conn = get_connection()

    rows = conn.execute("""

    SELECT

        subject_id,
        subject_name

    FROM subjects

    ORDER BY subject_name

    """).fetchall()

    conn.close()

    return rows


# =====================================================
# GET ONE SUBJECT
# =====================================================

def get_subject(subject_id):

    conn = get_connection()

    row = conn.execute("""

    SELECT *

    FROM subjects

    WHERE subject_id=?

    """, (subject_id,)).fetchone()

    conn.close()

    return row


# =====================================================
# DELETE SUBJECT
# =====================================================

def delete_subject(subject_id):

    conn = get_connection()

    conn.execute("""
    DELETE FROM teacher_subjects
    WHERE subject_id=?
    """, (subject_id,))

    conn.execute("""
    DELETE FROM class_subjects
    WHERE subject_id=?
    """, (subject_id,))

    conn.execute("""
    DELETE FROM timetable
    WHERE subject_id=?
    """, (subject_id,))

    conn.execute("""
    DELETE FROM subjects
    WHERE subject_id=?
    """, (subject_id,))

    conn.commit()
    conn.close()


# =====================================================
# SUBJECT EXISTS
# =====================================================

def subject_exists(subject_name):

    conn = get_connection()

    row = conn.execute("""

    SELECT subject_id

    FROM subjects

    WHERE subject_name=?

    """, (subject_name,)).fetchone()

    conn.close()

    return row is not None
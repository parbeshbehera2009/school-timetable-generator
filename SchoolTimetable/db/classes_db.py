from database import get_connection


# =====================================================
# ADD CLASS
# =====================================================

def add_class(class_name, section, level, working_days, periods_per_day):

    conn = get_connection()

    conn.execute("""
    INSERT INTO classes(

        class_name,
        section,
        level,
        working_days,
        periods_per_day

    )
    VALUES(?,?,?,?,?)
    """, (

        class_name,
        section,
        level,
        working_days,
        periods_per_day

    ))

    conn.commit()
    conn.close()


# =====================================================
# GET ALL CLASSES
# =====================================================

def get_classes():

    conn = get_connection()

    rows = conn.execute("""

    SELECT

        class_id,
        class_name,
        section,
        level,
        working_days,
        periods_per_day

    FROM classes

    ORDER BY

        level,
        class_name,
        section

    """).fetchall()

    conn.close()

    return rows


# =====================================================
# GET SINGLE CLASS
# =====================================================

def get_class(class_id):

    conn = get_connection()

    row = conn.execute("""

    SELECT *

    FROM classes

    WHERE class_id=?

    """, (class_id,)).fetchone()

    conn.close()

    return row


# =====================================================
# DELETE CLASS
# =====================================================

def delete_class(class_id):

    conn = get_connection()

    conn.execute("""
    DELETE FROM class_subjects
    WHERE class_id=?
    """, (class_id,))

    conn.execute("""
    DELETE FROM teacher_classes
    WHERE class_id=?
    """, (class_id,))

    conn.execute("""
    DELETE FROM timetable
    WHERE class_id=?
    """, (class_id,))

    conn.execute("""
    DELETE FROM classes
    WHERE class_id=?
    """, (class_id,))

    conn.commit()
    conn.close()


# =====================================================
# CLASS EXISTS
# =====================================================

def class_exists(class_name, section):

    conn = get_connection()

    row = conn.execute("""

    SELECT class_id

    FROM classes

    WHERE

        class_name=?

    AND

        section=?

    """, (

        class_name,
        section

    )).fetchone()

    conn.close()

    return row is not None
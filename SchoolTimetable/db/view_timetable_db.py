from database import get_connection


# =====================================================
# GET TIMETABLE OF ONE CLASS
# =====================================================

def get_class_timetable(class_id):

    conn = get_connection()

    rows = conn.execute("""

    SELECT

    timetable.day,
    timetable.period,

    subjects.subject_name,

    teachers.teacher_name,
    teachers.teacher_code

FROM timetable

LEFT JOIN subjects
ON subjects.subject_id = timetable.subject_id

LEFT JOIN teachers
ON teachers.teacher_id = timetable.teacher_id

WHERE timetable.class_id=?

ORDER BY day, period

    """, (class_id,)).fetchall()

    conn.close()

    return rows


# =====================================================
# GET ALL CLASSES
# (Used by View Timetable page)
# =====================================================

def get_all_classes():

    conn = get_connection()

    rows = conn.execute("""

    SELECT

        class_id,
        class_name,
        section

    FROM classes

    ORDER BY

        class_name,
        section

    """).fetchall()

    conn.close()

    return rows
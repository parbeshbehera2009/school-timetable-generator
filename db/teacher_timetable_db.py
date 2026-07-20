from database import get_connection

def get_teacher_timetable(teacher_id):

    conn = get_connection()

    rows = conn.execute("""

    SELECT

        timetable.day,
        timetable.period,

        classes.class_name,
        classes.section,

        subjects.subject_name

    FROM timetable

    LEFT JOIN classes
        ON classes.class_id = timetable.class_id

    LEFT JOIN subjects
        ON subjects.subject_id = timetable.subject_id

    WHERE timetable.teacher_id=?

    ORDER BY
        timetable.day,
        timetable.period

    """, (teacher_id,)).fetchall()

    conn.close()

    return rows
from database import get_connection

def get_teacher_timetable(teacher_id):

    conn = get_connection()

    # Count how many subjects this teacher teaches
    subject_count = conn.execute("""

    SELECT COUNT(*)

    FROM teacher_subjects

    WHERE teacher_id=?

    """, (teacher_id,)).fetchone()[0]

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

    return rows, subject_count
from random import shuffle

from database import get_connection
from db.teacher_subjects_db import get_teacher_for_class_subject


# =====================================================
# CLEAR TIMETABLE
# =====================================================

def clear_timetable():

    conn = get_connection()

    conn.execute("DELETE FROM timetable")

    conn.commit()
    conn.close()


# =====================================================
# GENERATE EMPTY TIMETABLE
# =====================================================

def generate_empty_timetable():

    clear_timetable()

    conn = get_connection()
    cursor = conn.cursor()

    classes = cursor.execute("""

    SELECT
        class_id,
        working_days,
        periods_per_day

    FROM classes

    """).fetchall()

    for cls in classes:

        for day in range(1, cls["working_days"] + 1):

            for period in range(1, cls["periods_per_day"] + 1):

                cursor.execute("""

                INSERT INTO timetable(

                    class_id,
                    teacher_id,
                    subject_id,
                    day,
                    period

                )

                VALUES(?,?,?,?,?)

                """, (

                    cls["class_id"],
                    None,
                    None,
                    day,
                    period

                ))

    conn.commit()
    conn.close()


# =====================================================
# GET EMPTY SLOTS OF A CLASS
# =====================================================

def get_empty_slots(class_id):

    conn = get_connection()

    rows = conn.execute("""

    SELECT

        id,
        day,
        period

    FROM timetable

    WHERE

        class_id=?

    AND

        subject_id IS NULL

    ORDER BY day,period

    """, (class_id,)).fetchall()

    conn.close()

    return rows


# =====================================================
# CHECK WHETHER TEACHER IS FREE
# =====================================================

def is_teacher_free(teacher_id, day, period):

    conn = get_connection()

    row = conn.execute("""

    SELECT id

    FROM timetable

    WHERE

        teacher_id=?

    AND

        day=?

    AND

        period=?

    """, (

        teacher_id,
        day,
        period

    )).fetchone()

    conn.close()

    return row is None


# =====================================================
# ASSIGN SUBJECT TO SLOT
# =====================================================

def assign_slot(slot_id, teacher_id, subject_id):

    conn = get_connection()

    conn.execute("""

    UPDATE timetable

    SET

        teacher_id=?,
        subject_id=?

    WHERE id=?

    """, (

        teacher_id,
        subject_id,
        slot_id

    ))

    conn.commit()
    conn.close()


# =====================================================
# GENERATE BASIC TIMETABLE
# =====================================================

def generate_basic_timetable():

    conn = get_connection()
    cursor = conn.cursor()

    classes = cursor.execute("""

    SELECT class_id

    FROM classes

    ORDER BY class_name,section

    """).fetchall()

    for cls in classes:

        class_id = cls["class_id"]

        curriculum = cursor.execute("""

        SELECT

            subject_id,
            weekly_periods

        FROM class_subjects

        WHERE class_id=?

        """, (class_id,)).fetchall()

        for subject in curriculum:

            subject_id = subject["subject_id"]

            periods_needed = subject["weekly_periods"]

            teacher = get_teacher_for_class_subject(

                class_id,
                subject_id

            )

            if teacher is None:
                continue

            teacher_id = teacher["teacher_id"]

            slots = get_empty_slots(class_id)

            shuffle(slots)

            filled = 0

            for slot in slots:

                if filled >= periods_needed:
                    break

                if is_teacher_free(

                    teacher_id,
                    slot["day"],
                    slot["period"]

                ):

                    assign_slot(

                        slot["id"],
                        teacher_id,
                        subject_id

                    )

                    filled += 1

    conn.close()
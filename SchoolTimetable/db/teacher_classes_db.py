from database import get_connection


# =====================================================
# ASSIGN CLASS TO TEACHER
# =====================================================

def assign_class(teacher_id, class_id):

    conn = get_connection()

    # Prevent duplicate assignment
    exists = conn.execute("""
    SELECT id
    FROM teacher_classes
    WHERE teacher_id=?
    AND class_id=?
    """, (
        teacher_id,
        class_id
    )).fetchone()

    if exists is None:

        conn.execute("""
        INSERT INTO teacher_classes(
            teacher_id,
            class_id
        )
        VALUES(?,?)
        """, (
            teacher_id,
            class_id
        ))

    conn.commit()
    conn.close()


# =====================================================
# GET ALL CLASS ASSIGNMENTS
# =====================================================

def get_teacher_classes():

    conn = get_connection()

    rows = conn.execute("""

    SELECT

        teacher_classes.id,

        teachers.teacher_id,
        teachers.teacher_code,
        teachers.teacher_name,

        classes.class_id,
        classes.class_name,
        classes.section

    FROM teacher_classes

    JOIN teachers
    ON teachers.teacher_id = teacher_classes.teacher_id

    JOIN classes
    ON classes.class_id = teacher_classes.class_id

    ORDER BY

        teachers.teacher_name,
        classes.class_name,
        classes.section

    """).fetchall()

    conn.close()

    return rows


# =====================================================
# DELETE CLASS ASSIGNMENT
# =====================================================

def delete_teacher_class(id):

    conn = get_connection()

    conn.execute("""
    DELETE FROM teacher_classes
    WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()


# =====================================================
# GET CLASSES OF ONE TEACHER
# =====================================================

def get_classes_of_teacher(teacher_id):

    conn = get_connection()

    rows = conn.execute("""

    SELECT

        classes.class_id,
        classes.class_name,
        classes.section

    FROM teacher_classes

    JOIN classes
    ON classes.class_id = teacher_classes.class_id

    WHERE teacher_classes.teacher_id=?

    ORDER BY
        classes.class_name,
        classes.section

    """, (teacher_id,)).fetchall()

    conn.close()

    return rows
from database import get_connection

def get_subject_id(cursor, subject_name):

    row = cursor.execute("""
    SELECT subject_id
    FROM subjects
    WHERE subject_name=?
    """, (subject_name,)).fetchone()

    return row["subject_id"]


def add_class_subject(cursor, class_id, subject_name, weekly_periods):

    subject_id = get_subject_id(cursor, subject_name)

    cursor.execute("""
    INSERT INTO class_subjects
    (class_id, subject_id, weekly_periods)
    VALUES(?,?,?)
    """, (class_id, subject_id, weekly_periods))
#
def initialize_school(section_counts, delete_old):

    conn = get_connection()
    cursor = conn.cursor()
    print("1")
    # ----------------------------------
    # DELETE OLD DATA
    # ----------------------------------
    if delete_old:

        cursor.execute("DELETE FROM timetable")
        cursor.execute("DELETE FROM teacher_subjects")
        cursor.execute("DELETE FROM teacher_classes")
        cursor.execute("DELETE FROM class_subjects")
        cursor.execute("DELETE FROM classes")
        cursor.execute("DELETE FROM subjects")
        cursor.execute("DELETE FROM cbse_defaults")

    # ----------------------------------
    # SCHOOL STRUCTURE
    # ----------------------------------

    school_structure = [

    ("LKG", "Kindergarten", section_counts["LKG"]),
    ("UKG", "Kindergarten", section_counts["UKG"]),

    ("1", "Primary", section_counts["1"]),
    ("2", "Primary", section_counts["2"]),

    ("3", "Upper Primary", section_counts["3"]),
    ("4", "Upper Primary", section_counts["4"]),
    ("5", "Upper Primary", section_counts["5"]),

    ("6", "Middle", section_counts["6"]),
    ("7", "Middle", section_counts["7"]),
    ("8", "Middle", section_counts["8"]),

    ("9", "Secondary", section_counts["9"]),
    ("10", "Secondary", section_counts["10"]),

    ("11 Science", "Science", 1),
    ("11 Commerce", "Commerce", 1),

    ("12 Science", "Science", 1),
    ("12 Commerce", "Commerce", 1)]

    # ----------------------------------
    # CREATE CLASSES
    # ----------------------------------
    print("2")
    for class_name, level, sections in school_structure:

        if sections == 1:

            cursor.execute("""
            INSERT INTO classes
            (class_name, section, level, working_days, periods_per_day)
            VALUES(?,?,?,?,?)
            """,
            (
                class_name,
                "A",
                level,
                6,
                6 if level == "Kindergarten" or class_name in ["1","2"] else 8
            ))

        else:

            for i in range(sections):

                section = chr(65+i)
                print()
                cursor.execute("""
                INSERT INTO classes
                (class_name, section, level, working_days, periods_per_day)
                VALUES(?,?,?,?,?)
                """,
                (
                    class_name,
                    section,
                    level,
                    6,
                    6 if level == "Kindergarten" or class_name in ["1","2"] else 8
                ))
    print("3")
    # ----------------------------------
    # CREATE SUBJECTS
    # ----------------------------------

    subjects = [

        "English",
        "Mathematics",
        "EVS",
        "Science",
        "Social Science",
        "Hindi",
        "Sanskrit",
        "Computer Science",
        "Physics",
        "Chemistry",
        "Biology",
        "Accountancy",
        "Business Studies",
        "Economics",
        "Physical Education",
        "Art",
        "Games",
        "GK"

    ]
    print("4")
    for subject in subjects:

        cursor.execute("""
        INSERT INTO subjects(subject_name)
        VALUES(?)
        """, (subject,))
    print("5") 
    #
    classes = cursor.execute("""
    SELECT class_id, class_name, level
    FROM classes
    """).fetchall()
    #
    CURRICULUM = {

        "Kindergarten": {
            "English": 8,
            "Mathematics": 8,
            "GK": 4,
            "Art": 5,
            "Games": 5
        },

        "Primary": {
            "English": 8,
            "Mathematics": 8,
            "EVS": 6,
            "Hindi": 6,
            "Computer Science": 2
        },

        "Upper Primary": {
            "English": 6,
            "Mathematics": 7,
            "Science": 6,
            "Social Science": 6,
            "Hindi": 5,
            "Computer Science": 2,
            "Art": 1,
            "Games": 3
        },

        "Middle": {
            "English": 6,
            "Mathematics": 7,
            "Science": 6,
            "Social Science": 6,
            "Hindi": 5,
            "Sanskrit": 3,
            "Computer Science": 2,
            "Games": 3
        },

        "Secondary": {
            "English": 6,
            "Mathematics": 7,
            "Science": 7,
            "Social Science": 6,
            "Hindi": 5,
            "Computer Science": 2,
            "Games": 3
        },

        "Science": {
            "English": 5,
            "Physics": 7,
            "Chemistry": 7,
            "Biology": 7,
            "Mathematics": 7,
            "Computer Science": 6,
            "Physical Education": 3
        },

        "Commerce": {
            "English": 5,
            "Accountancy": 8,
            "Business Studies": 7,
            "Economics": 7,
            "Mathematics": 5,
            "Computer Science": 5,
            "Physical Education": 3
        }

    }
    # ----------------------------------
    # KINDERGARTEN SUBJECTS
    # ----------------------------------
    for cls in classes:

        level = cls["level"]

        if level not in CURRICULUM:
            continue

        for subject_name, periods in CURRICULUM[level].items():

            add_class_subject(
                cursor,
                cls["class_id"],
                subject_name,
                periods
            )
    conn.commit()
    conn.close()
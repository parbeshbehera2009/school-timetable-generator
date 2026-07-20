import sqlite3

DATABASE = "school.db"


def get_connection():
    conn = sqlite3.connect(DATABASE,timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():

    print("Creating database...")

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------
    # Admin Table
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # --------------------------
    # Teachers Table
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers(
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT UNIQUE,
        teacher_code TEXT,
        teacher_name TEXT NOT NULL,
        qualification TEXT,
        phone TEXT,
        email TEXT,
        max_periods INTEGER
    )
    """)

    # --------------------------
    # Subjects Table
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects(
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_name TEXT NOT NULL
    )
    """)
    # --------------------------
    # CURRICULUM MASTER
    # --------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS curriculum(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        class_level TEXT NOT NULL,

        subject_name TEXT NOT NULL,

        weekly_periods INTEGER NOT NULL,

        subject_type TEXT NOT NULL,

        option_group TEXT

    )
    """)
    # --------------------------
    # CBSE DEFAULT SUBJECTS
    # --------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cbse_defaults(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        class_level TEXT,

        subject_name TEXT,

        weekly_periods INTEGER

    )
    """)
    # --------------------------
    # Classes Table
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classes(
        class_id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_name TEXT NOT NULL,
        section TEXT,
        level TEXT,
        working_days INTEGER,
        periods_per_day INTEGER
    )
    """)
    # --------------------------
    # CLASS SUBJECTS
    # --------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS class_subjects(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        class_id INTEGER,

        subject_id INTEGER,

        weekly_periods INTEGER,

        FOREIGN KEY(class_id) REFERENCES classes(class_id),
        FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)

    )
    """)

    # --------------------------
    # Teacher Subject Mapping
    # --------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teacher_subjects(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        teacher_id INTEGER NOT NULL,

        subject_id INTEGER NOT NULL,

        FOREIGN KEY(teacher_id) REFERENCES teachers(teacher_id),

        FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)

    )
    """)

    # --------------------------
    # Teacher Availability
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teacher_availability(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        day TEXT,
        period INTEGER,
        available INTEGER,
        FOREIGN KEY(teacher_id) REFERENCES teachers(teacher_id)
    )
    """)

    # --------------------------
    # Timetable Table
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timetable(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        teacher_id INTEGER,
        subject_id INTEGER,
        day TEXT,
        period INTEGER,
        FOREIGN KEY(class_id) REFERENCES classes(class_id),
        FOREIGN KEY(teacher_id) REFERENCES teachers(teacher_id),
        FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
    )
    """)
    # --------------------------
    # School Settings
    # --------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS school_settings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        school_name TEXT,
        working_days INTEGER,
        primary_periods INTEGER,
        senior_periods INTEGER,
        long_break_after INTEGER,
        short_break_after INTEGER
    )
    """)
    # ======================================================
    #               TEACHER FUNCTIONS
    # ======================================================
    # --------------------------
    # TEACHER CLASS ASSIGNMENT
    # --------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teacher_classes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        teacher_id INTEGER,

        class_id INTEGER,

        FOREIGN KEY(teacher_id) REFERENCES teachers(teacher_id),
        FOREIGN KEY(class_id) REFERENCES classes(class_id)

    )
    """)
    # --------------------------
    # Default Admin
    # --------------------------
    cursor.execute("""
    INSERT OR IGNORE INTO admin(username,password)
    VALUES('admin','admin123')
    """)

    conn.commit()
    print("All tables created successfully!")
    conn.close()

    print("Database created successfully!")



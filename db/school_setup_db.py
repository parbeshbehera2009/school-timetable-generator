from database import get_connection, create_tables


# =====================================================
# SAVE SCHOOL SETTINGS
# =====================================================

def save_school_settings(
    school_name,
    working_days,
    primary_periods,
    senior_periods,
    long_break_after,
    short_break_after
):

    create_tables()

    conn = get_connection()

    conn.execute("DELETE FROM school_settings")

    conn.execute("""

    INSERT INTO school_settings(

        school_name,
        working_days,
        primary_periods,
        senior_periods,
        long_break_after,
        short_break_after

    )

    VALUES(?,?,?,?,?,?)

    """, (

        school_name,
        int(working_days),
        int(primary_periods),
        int(senior_periods),
        int(long_break_after),
        int(short_break_after)

    ))

    conn.commit()
    conn.close()


# =====================================================
# GET SCHOOL SETTINGS
# =====================================================

def get_school_settings():

    conn = get_connection()

    row = conn.execute("""

    SELECT *

    FROM school_settings

    LIMIT 1

    """).fetchone()

    conn.close()

    return row
from database import get_connection


def get_defaults(class_level):

    conn = get_connection()

    data = conn.execute("""

    SELECT *

    FROM cbse_defaults

    WHERE class_level=?

    ORDER BY subject_name

    """,(class_level,)).fetchall()

    conn.close()

    return data
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    PageBreak,
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from database import get_connection

styles = getSampleStyleSheet()


# =====================================================
# GET TIMETABLE OF ONE CLASS
# =====================================================

def get_class_data(cursor, class_id):

    return cursor.execute("""

    SELECT

        timetable.day,
        timetable.period,

        subjects.subject_name,

        teachers.teacher_code

    FROM timetable

    LEFT JOIN subjects
        ON timetable.subject_id = subjects.subject_id

    LEFT JOIN teachers
        ON timetable.teacher_id = teachers.teacher_id

    WHERE timetable.class_id=?

    ORDER BY day, period

    """, (class_id,)).fetchall()
# =====================================================
# GET TIMETABLE OF ONE TEACHER
# =====================================================

def get_teacher_data(cursor, teacher_id):

    return cursor.execute("""

    SELECT

        timetable.day,
        timetable.period,

        classes.class_name,
        classes.section

    FROM timetable

    LEFT JOIN classes
        ON timetable.class_id = classes.class_id

    WHERE timetable.teacher_id=?

    ORDER BY day, period

    """, (teacher_id,)).fetchall()

# =====================================================
# CREATE CLASS PDF
# =====================================================

def create_class_pdf(filename):

    conn = get_connection()
    cursor = conn.cursor()

    pdf = SimpleDocTemplate(
        filename,
        pagesize=landscape(A4)
    )

    elements = []

    classes = cursor.execute("""

    SELECT
        class_id,
        class_name,
        section

    FROM classes

    ORDER BY class_name, section

    """).fetchall()

    for cls in classes:

        timetable = get_class_data(cursor, cls["class_id"])

        title = Paragraph(

            f"<b>{cls['class_name']} - {cls['section']}</b>",

            styles["Heading1"]

        )

        elements.append(title)
        # -----------------------------
        # Build Timetable Matrix
        # -----------------------------

        header = [
            "Day",
            "1",
            "2",
            "3",
            "Short\nBreak",
            "4",
            "5",
            "Long\nBreak",
            "6",
            "7",
            "8"
        ]

        table_data = [header]

        days = {
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday"
        }

        for day in range(1, 7):

            row = [days[day]]

            day_rows = {}

            for item in timetable:

                if int(item["day"]) == day:

                    text = ""

                    if item["subject_name"]:
                        text += item["subject_name"]

                    if item["teacher_code"]:
                        text += "\n" + item["teacher_code"]

                    day_rows[int(item["period"])] = text

            for period in range(1, 9):

                row.append(day_rows.get(period, ""))

                if period == 3:
                    row.append("")

                if period == 5:
                    row.append("")

            table_data.append(row)
            #
        table = Table(table_data)

        table.setStyle(TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565C0")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("BACKGROUND", (4, 1), (4, -1), colors.lightgrey),
            ("BACKGROUND", (7, 1), (7, -1), colors.lightgrey),

            ("BACKGROUND", (4, 0), (4, 0), colors.grey),
            ("BACKGROUND", (7, 0), (7, 0), colors.grey),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

        ]))

        elements.append(table)
            #
        elements.append(PageBreak())

    pdf.build(elements)

    conn.close()
# =====================================================
# CREATE TEACHER PDF
# =====================================================

def create_teacher_pdf(filename):

    conn = get_connection()
    cursor = conn.cursor()

    pdf = SimpleDocTemplate(
        filename,
        pagesize=landscape(A4)
    )

    elements = []

    teachers = cursor.execute("""

    SELECT

        teacher_id,
        teacher_name,
        teacher_code

    FROM teachers

    ORDER BY teacher_name

    """).fetchall()

    days = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday"
    }

    for teacher in teachers:

        timetable = get_teacher_data(
            cursor,
            teacher["teacher_id"]
        )

        elements.append(

            Paragraph(

                f"<b>{teacher['teacher_name']} ({teacher['teacher_code']})</b>",

                styles["Heading1"]

            )

        )

        header = [

            "Day",
            "1",
            "2",
            "3",
            "Short\nBreak",
            "4",
            "5",
            "Long\nBreak",
            "6",
            "7",
            "8"

        ]

        table_data = [header]

        for day in range(1,7):

            row = [days[day]]

            day_rows = {}

            for item in timetable:

                if int(item["day"]) == day:

                    day_rows[int(item["period"])] = \
                        f"{item['class_name']}-{item['section']}"

            for period in range(1,9):

                row.append(day_rows.get(period,""))

                if period == 3:
                    row.append("")

                if period == 5:
                    row.append("")

            table_data.append(row)

        table = Table(table_data)

        table.setStyle(TableStyle([

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1565C0")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("BACKGROUND",(4,1),(4,-1),colors.lightgrey),
            ("BACKGROUND",(7,1),(7,-1),colors.lightgrey),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("FONTSIZE",(0,0),(-1,-1),9)

        ]))

        elements.append(table)

        elements.append(PageBreak())

    pdf.build(elements)

    conn.close()
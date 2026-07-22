from flask import Flask, render_template, request, redirect, send_file
from database import create_tables
from db.teachers_db import *
from db.classes_db import *
from db.subjects_db import *
from db.school_setup_db import *
from db.initialize_school import initialize_school as generate_school
from db.teacher_subjects_db import *
from db.teacher_classes_db import *
from db.timetable_generator import *
from db.view_timetable_db import *
from db.teacher_timetable_db import get_teacher_timetable
from db.pdf_generator import create_class_pdf, create_teacher_pdf
#from db.teacher_timetable_db import *
app = Flask(__name__)

# Create the database and tables when the application starts
# already doing this at the end of this file
print("Creating 1...")
# --------------------------
# LOGIN
# --------------------------


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "admin123":
        return redirect("/dashboard")

    return "Invalid Username or Password"

@app.route("/logout")
def logout():
    return redirect("/")

print("Creating 2...")
# --------------------------
# DASHBOARD
# --------------------------


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# --------------------------
# TEACHERS
# --------------------------


@app.route("/teachers")
def teachers():
    teacher_list = get_teachers()

    return render_template("teachers.html", teachers=teacher_list)


@app.route("/add_teacher", methods=["POST"])
def add_new_teacher():
    add_teacher(
        request.form["employee_id"],
        request.form["teacher_code"],
        request.form["teacher_name"],
        request.form["qualification"],
        request.form["phone"],
        request.form["email"],
        request.form["max_periods"],
    )

    return redirect("/teachers")


@app.route("/delete_teacher/<int:teacher_id>")
def remove_teacher(teacher_id):
    delete_teacher(teacher_id)

    return redirect("/teachers")


# teacher_subjects-------------
@app.route("/teacher_subjects")
def teacher_subjects():
    teachers = get_teachers()

    subjects = get_subjects()

    classes = get_classes()

    subject_assignments = get_teacher_subjects()

    class_assignments = get_teacher_classes()

    return render_template(
        "teacher_subjects.html",
        teachers=teachers,
        subjects=subjects,
        classes=classes,
        subject_assignments=subject_assignments,
        class_assignments=class_assignments,
    )


# --------------------------
# CLASSES
# --------------------------
print("Creating 3...")


@app.route("/classes")
def classes():
    class_list = get_classes()

    return render_template("classes.html", classes=class_list)


@app.route("/add_class", methods=["POST"])
def add_new_class():
    add_class(
        request.form["class_name"],
        request.form["section"],
        request.form["level"],
        request.form["working_days"],
        request.form["periods_per_day"],
    )

    return redirect("/classes")


@app.route("/delete_class/<int:class_id>")
def remove_class(class_id):
    delete_class(class_id)

    return redirect("/classes")


# --------------------------
# SUBJECTS
# --------------------------
print("Creating 4...")


@app.route("/subjects")
def subjects():
    subject_list = get_subjects()

    return render_template("subjects.html", subjects=subject_list)


@app.route("/add_subject", methods=["POST"])
def add_new_subject():
    add_subject(request.form["subject_name"])

    return redirect("/subjects")


@app.route("/delete_subject/<int:subject_id>")
def remove_subject(subject_id):
    delete_subject(subject_id)

    return redirect("/subjects")


# assign subjects-----------------
@app.route("/assign_subject", methods=["POST"])
def assign_subject_route():

    teacher_id = request.form["teacher_id"]

    subject_ids = request.form.getlist("subject_ids")

    for subject_id in subject_ids:
        assign_subject(teacher_id, subject_id)

    return redirect("/teacher_subjects")


# assign classes-----------------
@app.route("/assign_class", methods=["POST"])
def assign_class_route():

    teacher_id = request.form["teacher_id"]

    class_ids = request.form.getlist("class_ids")

    for class_id in class_ids:

        assign_class(
            teacher_id,
            class_id
        )

    return redirect("/teacher_subjects")

# delete teacher subject-----------------
@app.route("/delete_teacher_subject/<int:id>")
def delete_teacher_subject_route(id):
    delete_teacher_subject(id)

    return redirect("/teacher_subjects")


# delete teacher class-----------------
@app.route("/delete_teacher_class/<int:id>")
def delete_teacher_class_route(id):
    delete_teacher_class(id)

    return redirect("/teacher_subjects")


# --------------------------
# SCHOOL SETUP
# --------------------------
@app.route("/school_setup")
def school_setup():
    return render_template("school_setup.html")


# --------------------------
# GENERATE TIMETABLE
# --------------------------
@app.route("/generate_timetable")
def generate_timetable():
    generate_empty_timetable()
    generate_basic_timetable()

    return "Timetable Generated Successfully!"
#generate again
@app.route("/generate_again")
def generate_again():

    generate_empty_timetable()
    generate_basic_timetable()

    return redirect("/view_timetable")

# view timetable
@app.route("/view_timetable")
def view_timetable():

    classes = get_classes()
    teachers = get_teachers()

    return render_template(
        "view_timetable.html",
        classes=classes,
        teachers=teachers,
        timetable=None
    )
#teacher_timetable

# show timetable
@app.route("/show_timetable", methods=["POST"])
def show_timetable():

    view_type = request.form["view_type"]

    classes = get_classes()
    teachers = get_teachers()

    if view_type == "class":

        class_id = request.form["class_id"]
        timetable = get_class_timetable(class_id)

    else:

        teacher_id = request.form["teacher_id"]
        timetable, subject_count = get_teacher_timetable(teacher_id)

    return render_template(
        "view_timetable.html",
        classes=classes,
        teachers=teachers,
        timetable=timetable,
        view_type=view_type,
        subject_count=subject_count if view_type == "teacher" else 0
    )

# ---------------------------
# INITIALIZE SCHOOL
# ---------------------------
@app.route("/initialize_school", methods=["POST"])
def initialize_school_route():

    save_school_settings(
        request.form["school_name"],
        request.form["working_days"],
        request.form["primary_periods"],
        request.form["senior_periods"],
        request.form["long_break_after"],
        request.form["short_break_after"],
    )

    section_counts = {
        "LKG": int(request.form["lkg_sections"]),
        "UKG": int(request.form["ukg_sections"]),
        "1": int(request.form["class1_sections"]),
        "2": int(request.form["class2_sections"]),
        "3": int(request.form["class3_sections"]),
        "4": int(request.form["class4_sections"]),
        "5": int(request.form["class5_sections"]),
        "6": int(request.form["class6_sections"]),
        "7": int(request.form["class7_sections"]),
        "8": int(request.form["class8_sections"]),
        "9": int(request.form["class9_sections"]),
        "10": int(request.form["class10_sections"]),
    }

    delete_old = "delete_old" in request.form

    generate_school(section_counts, delete_old)

    return "School Initialized Successfully!"


# reset original(teachers and subjects assigned will be reversed)
@app.route("/reset_teacher_assignments")
def reset_teacher_assignments():
    conn = get_connection()

    conn.execute("DELETE FROM teacher_subjects")
    conn.execute("DELETE FROM teacher_classes")

    conn.commit()
    conn.close()

    return redirect("/teacher_subjects")
#download_class_pdf
@app.route("/download_class_pdf")
def download_class_pdf():

    create_class_pdf("Class_Timetables.pdf")

    return send_file(
        "Class_Timetables.pdf",
        as_attachment=True
    )
#download_teahers_pdf
@app.route("/download_teacher_pdf")
def download_teacher_pdf():

    create_teacher_pdf("Teacher_Timetables.pdf")

    return send_file(
        "Teacher_Timetables.pdf",
        as_attachment=True
    )
# --------------------------
# START APPLICATION
# --------------------------
print(app.url_map)
if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", port=81, debug=True)

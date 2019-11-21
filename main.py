from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import datetime
import psycopg2

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        database="dfpqqefj777q4p",
        user="kktimoofiemaue",
        password="cdabbc31fb60189e193c2f1a75bf5c78244fc2879950c0adb81a3269d6362b15",
        host="ec2-54-221-215-228.compute-1.amazonaws.com",
        port="5432",
    )
    return conn


@app.route("/admin")
@login_required
def main_page():
    cursor = conn.cursor()
    n_faculty_q = "SELECT count(*) from faculty"
    cursor.execute(n_faculty_q)
    n_faculty = cursor.fetchone()[0]

    n_dept_q = "SELECT count(*) from department"
    cursor.execute(n_dept_q)
    n_dept = cursor.fetchone()[0]

    n_proctor_q = "SELECT count(faculty_id) from Faculty where faculty_id in (select distinct proctor_id from ProctorCredentials)"
    cursor.execute(n_proctor_q)
    n_proctor = cursor.fetchone()[0]

    n_student_q = "SELECT count(*) from Student"
    cursor.execute(n_student_q)
    n_student = cursor.fetchone()[0]

    return render_template(
        "admin_main_page.html", dc=n_dept, fc=n_faculty, pc=n_proctor, sc=n_student
    )


@app.route("/")
def hello():
    return "Index page"


@app.route("/admin/department/remove", methods=["POST"])
@login_required
def remove_department():
    cursor = conn.cursor()
    dept_id = request.form.get("dept_id")
    remove_query = "DELETE FROM Department where department_id=%(department_id)s"
    cursor.execute(remove_query, {"department_id": dept_id})
    print(cursor.rowcount)
    conn.commit()
    return {"error": False}


def replace_last_occurence(s, s1, s2):
    s = s[::-1].replace(s1[::-1], s2[::-1])[::-1]
    return s


@app.route("/admin/faculty/remove", methods=["POST"])
@login_required
def remove_faculty():

    cursor = conn.cursor()
    fid = request.form.get("fid")
    fid = replace_last_occurence(fid, "__at__", "@")
    fid = replace_last_occurence(fid, "__dot__", ".")

    remove_query = "DELETE FROM Faculty where faculty_id=%(fid)s"
    cursor.execute(remove_query, {"fid": fid})
    print(cursor.rowcount)
    conn.commit()
    return {"error": False}


@app.route("/admin/faculty/add", methods=["POST"])
@login_required
def add_faculty():
    cursor = conn.cursor()
    fid = request.form.get("fid")
    fname = request.form.get("fname")
    dept_id = request.form.get("dept_id")
    dname_q = "SELECT department_name FROM Department WHERE department_id=%(dept_id)s"
    cursor.execute(dname_q, {"dept_id": dept_id})
    dname = cursor.fetchone()[0]
    add_query = "INSERT INTO Faculty VALUES(%(fid)s, %(fname)s, %(dept_id)s)"
    try:
        cursor.execute(add_query, {"fid": fid, "fname": fname, "dept_id": dept_id})
        conn.commit()
        return jsonify({"error": False, "dept_name": dname})
    except:
        return jsonify({"error": True})


@app.route("/admin/department/add", methods=["POST"])
@login_required
def add_department():
    cursor = conn.cursor()
    dept_id = request.form.get("dept_id")
    dept_name = request.form.get("dept_name")
    add_query = "INSERT INTO Department VALUES(%(dept_id)s, %(dept_name)s)"
    try:
        cursor.execute(add_query, {"dept_id": dept_id, "dept_name": dept_name})
        conn.commit()
        return jsonify({"error": False})
    except:
        return jsonify({"error": True})


@app.route("/admin/department")
@login_required
def manage_department():

    cursor = conn.cursor()
    depts_q = "SELECT department_name,department_id from department"
    cursor.execute(depts_q)
    departments = cursor.fetchall()

    return render_template("manage_department.html", depts=departments)


@app.route("/admin/add_proctor_cred", methods=["POST"])
@login_required
def add_proctor_cred():
    email = request.form.get("email")
    password = request.form.get("password")
    q_add_cred = "INSERT INTO ProctorCredentials VALUES(%(proctor_id)s, %(password)s) ON CONFLICT(proctor_id) DO UPDATE SET password=%(password)s"
    cursor = conn.cursor()
    try:
        cursor.execute(q_add_cred, {"proctor_id": email, "password": password})
        conn.commit()
        return jsonify({"error": False})
    except Exception as e:
        print(e)
        conn.commit()
        return jsonify({"error": True})


@app.route("/admin/student/remove", methods=["POST"])
@login_required
def remove_student():
    usn = request.form.get("usn")
    delete_q = "DELETE FROM Student WHERE student_usn=%(usn)s"
    cursor = conn.cursor()
    cursor.execute(delete_q, {"usn": usn})
    conn.commit()
    return jsonify({"error": False})


@app.route("/admin/student/add", methods=["POST"])
@login_required
def add_student():

    fname = request.form.get("fname")
    mname = request.form.get("mname")
    lname = request.form.get("lname")
    usn = request.form.get("usn")
    dob = request.form.get("dob")
    stud_email = request.form.get("stud_email")
    stud_phone = request.form.get("stud_phone")
    join_year = int(request.form.get("join_year"))
    grad_year = int(request.form.get("grad_year"))
    dept_id = request.form.get("dept_id")
    quota = request.form.get("quota").upper()
    parent_email = request.form.get("parent_email")
    parent_phone = request.form.get("parent_phone")
    parent_name = request.form.get("parent_name")
    dob = datetime.datetime.strptime(dob, "%d/%m/%Y")

    cursor = conn.cursor()
    try:
        add_student = """INSERT INTO Student VALUES(%(usn)s, %(fname)s, %(mname)s, %(lname)s,
                                                    %(join_year)s, %(grad_year)s, %(quota)s, 
                                                    %(stud_email)s, %(stud_phone)s,
                                                    %(dept_id)s, %(dob)s)"""
        cursor.execute(
            add_student,
            {
                "usn": usn,
                "fname": fname,
                "mname": mname,
                "lname": lname,
                "join_year": join_year,
                "grad_year": grad_year,
                "quota": quota,
                "stud_email": stud_email,
                "stud_phone": stud_phone,
                "dept_id": dept_id,
                "dob": dob,
            },
        )
        conn.commit()

        add_parent = "INSERT INTO Parent VALUES(%(stud_usn)s, %(parent_name)s, %(parent_phone)s, %(parent_email)s) ON CONFLICT DO NOTHING"
        cursor.execute(
            add_parent,
            {
                "parent_name": parent_name,
                "stud_usn": usn,
                "parent_phone": parent_phone,
                "parent_email": parent_email,
            },
        )
        conn.commit()
        return jsonify({"error": False})
    except Exception as e:
        print(e)
        return jsonify({"error": True})


@app.route("/admin/student")
@login_required
def manage_student():
    stud_data_q = "SELECT student_usn, CONCAT(first_name, ' ', middle_name,' ', last_name), department_id from Student"
    cursor = conn.cursor()
    cursor.execute(stud_data_q)
    stud_data = cursor.fetchall()
    get_deptids_q = "SELECT department_id FROM Department"
    cursor.execute(get_deptids_q)
    deptid_list = cursor.fetchall()
    deptid_list = [d[0] for d in deptid_list]
    print(deptid_list)
    return render_template(
        "manage_student.html", stud_data=stud_data, deptid_list=deptid_list
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        for _ in range(15):
            print("YO")

        return render_template("admin_login_page.html")

    entered_password = request.form.get("password")
    print(entered_password)
    if entered_password == users["admin"]["password"]:
        user = User()
        user.id = "admin"
        login_user(user)
        return jsonify({"error": False})

    return jsonify({"error": True})


@app.route("/auth/proctor", methods=["POST"])
@login_required
def auth_proctor():
    email_entered = request.form.get("email")
    pass_entered = request.form.get("passward")

    q_chk_pass = (
        "SELECT password for ProctorCredentials where proctor_id=%(proctor_id)s"
    )
    cursor = conn.cursor()
    cursor.execute(q_chk_pass, {"proctor_id": email_entered})
    password = cursor.fetchone()[0]
    if pass_entered == password:
        return jsonify({"error": False})
    else:
        return jsonify({"error": True})


@app.route("/admin/faculty")
@login_required
def manage_faculty():
    cursor = conn.cursor()
    fact_details_q = "SELECT name,faculty_id,department_name,REPLACE(REPLACE(faculty_id, '@', '__at__'), '.', '__dot__') from Faculty f,Department d where f.department_id=d.department_id"
    cursor.execute(fact_details_q)
    faculties = cursor.fetchall()
    print(faculties)
    dept_abbr_q = "SELECT distinct department_id from Department"
    cursor.execute(dept_abbr_q)
    dept_abbr = cursor.fetchall()
    dept_abbr = [d[0] for d in dept_abbr]
    print(dept_abbr)

    return render_template(
        "manage_faculty.html", faculties=faculties, dept_abbr=dept_abbr
    )


@app.route("/admin/logout")
def logout():
    logout_user()
    return redirect("/admin/login")


@app.route("/admin/proctor", methods=["GET"])
@login_required
def admin():
    q_faculty_details = "SELECT name, faculty_id from Faculty"
    q_proctor_ids = "SELECT distinct proctor_id from ProctorCredentials"
    cursor = conn.cursor()
    cursor.execute(q_faculty_details)
    fne = cursor.fetchall()
    cursor.execute(q_proctor_ids)
    proctor_ids = cursor.fetchall()
    proctor_ids = [a[0] for a in proctor_ids]
    print(fne)
    faculty_data = [(fname, fid, fid in proctor_ids) for fname, fid in fne]
    print(faculty_data)
    print(proctor_ids)

    return render_template("admin_page.html", faculty_data=faculty_data)


@app.route("/app/get_students", methods=["POST"])
def get_students():
    faculty_id = request.form.get("faculty_id")
    fetch_students_q = "SELECT student_usn, CONCAT(first_name,' ',middle_name,' ',lname),department_id FROM Student WHERE student_usn IN (SELECT student_usn from Proctor where proctor_id=%(proctor_id)s)"
    cursor = conn.cursor()
    cursor.execute(fetch_students_q, {"proctor_id": faculty_id})
    student_data = cursor.fetchall()
    student_data = [{"usn": usn, "name": name} for usn, name in student_data]
    return student_data


@app.route("/app/get_all_students", methods=["POST"])
def get_all_students():
    fetch_all_usns = "SELECT student_usn from Student"
    cursor = conn.cursor()
    cursor.execute(fetch_all_usns)
    usn_list = cursor.fetchall()
    usn_list = [usn[0] for usn in usn_list]
    return usn_list


@app.route("/app/add_student_proctor", methods=["POST"])
def add_student_proctor():
    proctor_id = request.form.get("faculty_id")
    student_usn = request.form.get("student_usn")
    cursor = conn.cursor()
    add_stud_query = "INSERT INTO Proctor VALUES(%(proctor_id)s, %(student_usn)s)"
    try:
        cursor.execute(
            add_stud_query, {"proctor_id": proctor_id, "student_usn": student_usn}
        )
        return jsonify({"error": False})
    except:
        return jsonify({"error": True})


@app.route("/app/check_proctor_cred", methods=["POST"])
def check_proctor_cred():
    proctor_id = request.form.get("proctor_id")
    password = request.form.get("password")
    cursor = conn.cursor()
    fetch_creds = (
        "SELECT password from ProctorCredentials where proctor_id=%(proctor_id)s"
    )
    cursor.execute(fetch_creds, {"proctor_id": proctor_id})
    if len(cursor.fetchall()) == 0:
        print('Fail..., cursors.fetchall()={}, len={}'.format(cursor.fetchall(), len(cursor.fetchall())))
        return jsonify({"error": True})
    else:
        print('Pass..., cursors.fetchall()={}, pass={}'.format(cursor.fetchall(), len(cursor.fetchone()[0])))

        password_in_db = cursor.fetchone()[0]
        if password_in_db == password:
            return jsonify({"error": False})
        return jsonify({"error": True})


@app.route("/app/check_student_cred", methods=["POST"])
def check_student_cred():
    student_usn = request.form.get("student_usn")
    dob = request.form.get("dob")
    fetch_dob = "SELECT dob from Student where student_usn=%(student_usn)s"
    cursor = conn.cursor()
    cursor.execute(fetch_dob, {"student_usn": student_usn})
    if len(cursor.fetchall()) == 0:
        return jsonify({"error": True})
    else:
        dob_in_db = cursor.fetchone()[0]
        if dob_in_db == dob:
            return jsonify({"error": False})
        return jsonify({"error": True})


app.config[
    "SECRET_KEY"
] = '\x94\x94d"\xf0/\xa4j\xa7\xc7\xa2;\x1aOEp\xb3\xf1\xc3%v+W\xdd'
login_manager = LoginManager()
login_manager.init_app(app)

conn = get_db_connection()
cursor = conn.cursor()
with open("queries/create_query.sql") as query_file:
    q = query_file.read()
    cursor.execute(q)
conn.commit()

admin_pass_q = "SELECT admin_password FROM ADMIN"
cursor.execute(admin_pass_q)
admin_password = cursor.fetchone()[0]

users = {"admin": {"password": admin_password}}


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(user_id):
    if user_id not in users:
        return

    user = User()
    user.id = user_id
    return user


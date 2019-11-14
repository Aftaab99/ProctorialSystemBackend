from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="aftaab",
        host="localhost",
        port="5432",
    )
    return conn


@app.route("/admin/main_page")
def main_page():
    conn = get_db_connection()
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
    conn.close()

    return render_template(
        "admin_main_page.html", dc=n_dept, fc=n_faculty, pc=n_proctor, sc=n_student
    )


@app.route("/")
def hello():
    return "Index page"


@app.route("/admin/department/remove", methods=["POST"])
def remove_department():
    conn = get_db_connection()
    cursor = conn.cursor()
    dept_id = request.form.get("dept_id")
    remove_query = "DELETE FROM Department where department_id=%(department_id)s"
    cursor.execute(remove_query, {"department_id": dept_id})
    print(cursor.rowcount)
    conn.commit()
    conn.close()
    return {"error": False}


def replace_last_occurence(s, s1, s2):
    s = s[::-1].replace(s1[::-1], s2[::-1])[::-1]
    return s


@app.route("/admin/faculty/remove", methods=["POST"])
def remove_faculty():

    conn = get_db_connection()
    cursor = conn.cursor()
    fid = request.form.get("fid")
    fid = replace_last_occurence(fid, "__at__", "@")
    fid = replace_last_occurence(fid, "__dot__", ".")

    remove_query = "DELETE FROM Faculty where faculty_id=%(fid)s"
    cursor.execute(remove_query, {"fid": fid})
    print(cursor.rowcount)
    conn.commit()
    conn.close()
    return {"error": False}


@app.route("/admin/faculty/add", methods=["POST"])
def add_faculty():
    conn = get_db_connection()
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
        conn.close()
        return jsonify({"error": False, "dept_name": dname})
    except:
        conn.close()
        return jsonify({"error": True})


@app.route("/admin/department/add", methods=["POST"])
def add_department():
    conn = get_db_connection()
    cursor = conn.cursor()
    dept_id = request.form.get("dept_id")
    dept_name = request.form.get("dept_name")
    add_query = "INSERT INTO Department VALUES(%(dept_id)s, %(dept_name)s)"
    try:
        cursor.execute(add_query, {"dept_id": dept_id, "dept_name": dept_name})
        conn.commit()
        conn.close()
        return jsonify({"error": False})
    except:
        conn.close()
        return jsonify({"error": True})


@app.route("/admin/department")
def manage_department():

    conn = get_db_connection()
    cursor = conn.cursor()
    depts_q = "SELECT department_name,department_id from department"
    cursor.execute(depts_q)
    departments = cursor.fetchall()

    conn.close()

    return render_template("manage_department.html", depts=departments)


@app.route("/admin/student")
def manage_student():
    return render_template("add_department.html", depts=["ISE", "CSE"])


@app.route("/admin/add_proctor_cred", methods=["POST"])
def add_proctor_cred():
    email = request.form.get("email")
    password = request.form.get("password")
    conn = get_db_connection()
    q_add_cred = "INSERT INTO ProctorCredentials VALUES(%(proctor_id)s, %(password)s) ON CONFLICT(proctor_id) DO UPDATE SET password=%(password)s"
    cursor = conn.cursor()
    try:
        cursor.execute(q_add_cred, {"proctor_id": email, "password": password})
        conn.commit()
        conn.close()
        return jsonify({"error": False})
    except Exception as e:
        print(e)
        conn.commit()
        conn.close()
        return jsonify({"error": True})


@app.route("/admin/login")
def admin_login():
    return render_template("admin_login_page.html")


@app.route("/auth/proctor", methods=["POST"])
def auth_proctor():
    email_entered = request.form.get("email")
    pass_entered = request.form.get("passward")

    q_chk_pass = (
        "SELECT password for ProctorCredentials where proctor_id=%(proctor_id)s"
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(q_chk_pass, {"proctor_id": email_entered})
    password = cursor.fetchone()[0]
    if pass_entered == password:
        return jsonify({"error": False})
    else:
        return jsonify({"error": True})


@app.route("/admin/faculty")
def manage_faculty():
    conn = get_db_connection()
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
    conn.close()

    return render_template(
        "manage_faculty.html", faculties=faculties, dept_abbr=dept_abbr
    )


@app.route("/admin", methods=["GET"])
def admin():
    q_faculty_details = "SELECT name, faculty_id from Faculty"
    q_proctor_ids = "SELECT distinct proctor_id from ProctorCredentials"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(q_faculty_details)
    fne = cursor.fetchall()
    cursor.execute(q_proctor_ids)
    proctor_ids = cursor.fetchall()
    proctor_ids = [a[0] for a in proctor_ids]
    conn.close()
    print(fne)
    faculty_data = [(fname, fid, fid in proctor_ids) for fname, fid in fne]
    print(faculty_data)
    print(proctor_ids)

    return render_template("admin_page.html", faculty_data=faculty_data)


@app.route("/admin/checkpassword", methods=["POST"])
def checkpassword():
    entered_password = request.form.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT admin_password from Admin")
    hashed_password = cursor.fetchone()[0]
    print(entered_password)
    print(hashed_password)
    if entered_password == hashed_password:
        return jsonify({"error": False})
    else:
        return jsonify({"error": True})


if __name__ == "__main__":
    conn = get_db_connection()
    cursor = conn.cursor()
    assert (
        replace_last_occurence("shivshankar__at__dayanandasagar.com", "__at__", "@")
        == "shivshankar@dayanandasagar.com"
    )
    print("Database opened successfully")
    with open("queries/create_query.sql") as query_file:
        q = query_file.read()
        cursor.execute(q)
    with open("queries/add_department_data.sql") as query_file:
        q = query_file.read()
        cursor.execute(q)
    with open("queries/add_faculty_data.sql") as query_file:
        q = query_file.read()
        cursor.execute(q)
    conn.commit()
    conn.close()
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(database="postgres", user="postgres",
                            password="aftaab", host="127.0.0.1", port="5432")
    return conn

@app.route('/')
def hello():
    return "Index page"

@app.route('/admin/add_proctor_cred', methods=['POST'])
def add_proctor_cred():
    email = request.form.get('email')
    password = request.form.get('password')
    conn = get_db_connection()
    q_add_cred = "INSERT INTO ProctorCredentials VALUES(%(proctor_id)s, %(password)s) ON CONFLICT(proctor_id) DO UPDATE SET password=%(password)s"
    cursor = conn.cursor()
    try:
        cursor.execute(q_add_cred, {'proctor_id': email, 'password': password})
        conn.commit()
        conn.close()
        return jsonify({'error': False})
    except Exception as e:
        print(e)
        conn.commit()
        conn.close()
        return jsonify({'error': True})

@app.route('/admin/login')
def admin_login():
    return render_template('admin_login_page.html')


@app.route('/admin', methods=['GET'])
def admin():
    q_faculty_details = "SELECT name, faculty_id from Faculty"
    q_proctor_ids = "SELECT distinct proctor_id from ProctorCredentials"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(q_faculty_details)
    fne = cursor.fetchall()
    cursor.execute(q_proctor_ids)
    proctor_ids =cursor.fetchall()
    proctor_ids = [a[0] for a in proctor_ids]
    conn.close()
    print(fne)
    faculty_data = [(fname,fid,fid in proctor_ids) for fname, fid in fne]
    print(faculty_data)
    print(proctor_ids)
    
    return render_template('admin_page.html', faculty_data=faculty_data)




@app.route('/admin/checkpassword', methods=['POST'])
def checkpassword():
    entered_password = request.form.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT admin_password from Admin")
    hashed_password = cursor.fetchone()[0]
    print(entered_password)
    print(hashed_password)
    if entered_password == hashed_password:
        return jsonify({'error': False})
    else:
        return jsonify({'error': True})

if __name__ == '__main__':

    conn = get_db_connection()
    cursor = conn.cursor()
    print("Database opened successfully")
    with open('queries/create_query.sql') as query_file:
        q = query_file.read()
        cursor.execute(q)
    with open('queries/add_department_data.sql') as query_file:
        q = query_file.read()
        cursor.execute(q)
    with open('queries/add_faculty_data.sql') as query_file:
        q = query_file.read()
        cursor.execute(q)
    conn.commit()
    conn.close()
    app.run(debug=True)

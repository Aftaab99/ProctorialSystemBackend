from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2

app = Flask(__name__)


@app.route('/')
def hello():
    return "Index page"


@app.route('/admin/login')
def admin_login():
    return render_template('admin_login_page.html')


@app.route('/admin', methods=['GET'])
def admin():
    return "This is the admin page"


@app.route('/admin/checkpassword', methods=['POST'])
def checkpassword():
    entered_password = request.form.get('password')

    conn = psycopg2.connect(database="postgres", user="postgres",
                            password="aftaab", host="127.0.0.1", port="5432")
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

    conn = psycopg2.connect(database="postgres", user="postgres",
                            password="aftaab", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    print("Database opened successfully")
    with open('queries/create_query.sql') as query_file:
        q = query_file.read()
        cursor.execute(q)
    conn.commit()
    conn.close()
    app.run(debug=True)

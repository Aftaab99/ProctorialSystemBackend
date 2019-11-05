from flask import Flask
import psycopg2

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':

    conn = psycopg2.connect(database="postgres", user="postgres", password="aftaab", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    print("Database opened successfully")
    with open('queries/create_query.sql') as query_file:
        q = query_file.read()
        cursor.execute(q)
    conn.commit()
    app.run(debug=True)

from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# Set up connection to your Postgres database
db_config = {
    'dbname': 'my_database',
    'user': 'postgres',
    'password': 'Sunita',
    'host': 'localhost',
    'port': '5433',
}

def connect_to_database():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route('/')
def show_table():
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM my_table")
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('table.html', data=data)
        except psycopg2.Error as e:
            return f"Error executing query: {e}"
    else:
        return "Unable to connect to the database"

@app.route('/search_by_diarrhea_no', methods=['POST'])
def search_by_diarrhea_no():
    diarrhea_no = request.form.get('diarrhea_no')
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM my_table WHERE "Diarrhea_no" = %s', (diarrhea_no,))
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('table.html', data=data)
        except psycopg2.Error as e:
            return f"Error executing query: {e}"
    else:
        return "Unable to connect to the database"

if __name__ == '__main__':
    app.run(port=4000)

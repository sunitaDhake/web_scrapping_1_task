from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
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
            return render_template('table.html')
        except psycopg2.Error as e:
            return f"Error executing query: {e}"
    else:
        return "Unable to connect to the database"

@app.route('/search_form')
def search_form():
    return render_template('search_form.html')

@app.route('/search', methods=['POST'])
def search():
    column = request.form.get('column')
    search_value = request.form.get('search_value')


    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            
            base_query = "SELECT * FROM my_table WHERE"
            
            # According to input column selection query going execute because data type for  every column is different
            if column == 'Diarrhea_no':
                query = f'{base_query} "{column}" = %s'
                search_value = int(search_value) 
            elif column in ['Buyer', 'Seller', 'Other_information']:                                 
                search_value = f"%{search_value}%" 
                query = f'{base_query} "{column}" LIKE %s'  
            else:
                query = f'{base_query} "{column}" LIKE %s' 

            cursor.execute(query, (search_value,))

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

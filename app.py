from flask import Flask, request, render_template, redirect
import mysql.connector
import time

app = Flask(__name__,template_folder='./templates')

# Database Configuration
db_config = {
    'user': 'root',        # Your MySQL username
    'password': 'pouet',        # Your MySQL password
    'host': 'localhost',
    'database': 'testdb'   # Your database name
}
'''
@app.route('/')
def index():
    return render_template('index.html')
'''
# Route for handling the landing page
@app.route('/')
def index():
    return render_template('index.html')

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Hash the password for security
        #hashed_password = generate_password_hash(password, method='sha256')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (firstName, lastName, email, username, password) VALUES (%s,%s, %s, %s, %s)", (firstName, lastName, email, username, password))
        conn.commit()

        cursor.close()
        conn.close()

        return render_template('login.html')

    return render_template('signup.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username= '"+username+"' AND password= '"+password+"' ;")
        user = cursor.fetchall()

        cursor.close()
        conn.close()

        if user:
            # User is authenticated
            return redirect('/')

            time.sleep(3)

        else:
            # Invalid credentials
            return 'Login Failed'

    return render_template('login.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    users = []
    if request.method == 'POST':
        username_search = request.form['username']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE username LIKE '%"+username_search+"%';"
        cursor.execute(query)

        users = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template('search.html', users=users)

@app.route('/user')
def user_page():
    # This page can be accessed by standard users
    return render_template('user.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():

    return render_template('admin.html')


@app.route('/admin/add', methods=['POST'])
def admin_add():
    msg_add = ''
    msg_del = ''
    msg = ''
    print(request.form)
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Hash the password for security
        #hashed_password = generate_password_hash(password, method='sha256')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (firstName, lastName, email, username, password) VALUES (%s,%s, %s, %s, %s)", (firstName, lastName, email, username, password))
        conn.commit()

        cursor.close()
        conn.close()
        msg = 'User added successfully!'
        return render_template('admin.html', msg_add=msg)

@app.route('/admin/del', methods=['POST'])
def admin_del():
    msg_add = ''
    msg_del = ''
    msg = ''
    if request.method == 'POST':
        # Logic for deleting a user
        user_id = request.form['user_id']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        msg = 'User deleted successfully!'
        return render_template('admin.html', msg_del=msg)

@app.route('/admin/search', methods=['POST'])
def admin_search():
    msg_add = ''
    msg_del = ''
    msg = ''
    users=[]
    print(request.form)
    if request.method == 'POST':
        username_search = request.form['username']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username LIKE '%"+username_search+"%';"
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('admin.html', users=users, msg=msg)


if __name__ == '__main__':
    app.run(debug=True)

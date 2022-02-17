# flask imports
from pickle import FALSE
from flask import Flask, request, render_template, flash,redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import uuid # for public id

# creates Flask object
app = Flask(__name__)
# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = 'your secret key'
# database name
# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'perpustakaan1'
# Intialize MySQL
mysql = MySQL(app)

def checking_login():          
    if not session.get("id_user"):
        return False        
    else:        
        return True

@app.route('/', methods=['GET'])
def home():
    check = checking_login()
    if not check:
        return render_template('base/login.html')

    return redirect(url_for('get_buku_all'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST':
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result        
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id_user'] = account['id_user']
            session['username'] = account['username']
            session['role'] = account['role']
            # Redirect to home page
            return redirect(url_for('get_buku_all'))
        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username/password!", "danger")            

    return render_template('base/login.html')

    
# signup route
@app.route('/daftar', methods =['POST','GET'])
def daftar():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #take data
        id_user = str(uuid.uuid4())
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        nama_lengkap = request.form['nama_lengkap']        
        alamat = request.form['alamat']
        role_user = "user"

        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            flash("Account already exists!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash("Username must contain only characters and numbers!", "danger")
        elif not username or not password or not email:
            flash("Incorrect username/password!", "danger")
        else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
            sql="INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s,%s)"
            cursor.execute(sql, (id_user,username,email,password,nama_lengkap,alamat, role_user))
            mysql.connection.commit()
            flash("You have successfully registered!", "success")  
            return redirect(url_for('get_anggota_all'))      

    check = checking_login()
    if not check:
        return redirect(url_for('login'))

    return render_template('anggota/input_anggota.html')

# Anggota Route
@app.route('/anggota/get_all', methods =['GET'])
def get_anggota_all():
    role_user = ''
    check = checking_login()
    if not check:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql="SELECT * FROM users"
    cursor.execute(sql)
    anggota_all = cursor.fetchall()    
    
    if not session.get("id_user"):
        role_user = ''     
    else:        
        role_user = session['role']

    return render_template('anggota/index.html', data=anggota_all, role = role_user)

@app.route('/anggota/edit/<string:id_user>', methods=['GET'])
def edit_anggota(id_user):
    check = checking_login()
    if not check:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql="SELECT * FROM users WHERE id_user = %s"
    cursor.execute(sql,(id_user, ))
    anggota_one = cursor.fetchone()
    return render_template('anggota/edit_anggota.html', data=anggota_one)

@app.route('/proses_edit_anggota', methods=['POST', 'GET'])
def proses_edit_anggota():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    id_user = request.form['id_user']

    if request.method == 'POST':       
        #take data
        username = request.form['username']
        email = request.form['email']
        nama_lengkap = request.form['nama_lengkap']        
        alamat = request.form['alamat']
        #process
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!", "danger")

        sql="UPDATE users SET username= %s, email= %s, nama_lengkap= %s, alamat= %s WHERE id_user = %s"
        print(id_user)
        cursor.execute(sql, (username,email,nama_lengkap,alamat, id_user))
        mysql.connection.commit()
        flash("You have successfully edited", "success")  
        return redirect(url_for('get_anggota_all'))

    sql="SELECT * FROM users WHERE id_user = %s"
    cursor.execute(sql,(id_user, ))
    anggota_one = cursor.fetchone()
    return render_template('anggota/edit_anggota.html', data=anggota_one)
    
@app.route('/anggota/<string:id_user>', methods =['GET'])
def get_anggota_one(id_user):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql="SELECT * FROM users WHERE id_user = %s"
    cursor.execute(sql,(id_user, ))
    anggota_one = cursor.fetchone()
    return render_template('anggota/edit_anggota.html', data=anggota_one)

@app.route('/anggota/delete/<string:id_user>', methods =['GET', 'DELETE'])
def delete_anggota(id_user):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if id_user:        
        sql="DELETE FROM users WHERE `id_user` = %s"
        cursor.execute(sql,(id_user, )) 
        mysql.connection.commit()
        flash("You have successfully Delete it!", "success") 
        return redirect(url_for('get_anggota_all'))

    return redirect(url_for('get_anggota_all'))    

# book Route
@app.route('/buku/input_buku', methods =['POST','GET'])
def input_buku():
    if request.method == 'POST':
        #take data
        id_buku = str(uuid.uuid4())
        judul_buku = request.form['judul_buku']
        pengarang = request.form['pengarang']
        penerbit = request.form['penerbit']
        tahun_terbit = request.form['tahun_terbit']
        #process
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql="INSERT INTO buku VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (id_buku, judul_buku,pengarang,penerbit,tahun_terbit))
        mysql.connection.commit()

        flash("You have successfully registered!", "success")  
        return redirect(url_for('get_buku_all'))      

    check = checking_login()
    if not check:
        return redirect(url_for('login'))

    return render_template('buku/input_buku.html')

@app.route('/buku/get_all', methods =['GET'])
def get_buku_all():
    role_user = ''
    check = checking_login()
    if not check:
        return render_template('base/login.html')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql="SELECT * FROM buku"
    cursor.execute(sql)
    buku_all = cursor.fetchall()    
    if not session.get("id_user"):
        role_user = ''     
    else:        
        role_user = session['role']

    return render_template('buku/index.html', data=buku_all, role = role_user)

@app.route('/buku/edit/<string:id_buku>', methods=['GET'])
def edit_buku(id_buku):
    check = checking_login()
    if not check:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql="SELECT * FROM buku WHERE id_buku = %s"
    cursor.execute(sql,(id_buku, ))
    buku_one = cursor.fetchone()
    return render_template('buku/edit_buku.html', data=buku_one)

@app.route('/proses_edit_buku', methods=['POST', 'GET'])
def proses_edit_buku():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    id_buku = request.form['id_buku']

    if request.method == 'POST':       
        #take data
        id_buku = request.form['id_buku']
        judul_buku = request.form['judul_buku']
        pengarang = request.form['pengarang']
        penerbit = request.form['penerbit']
        tahun_terbit = request.form['tahun_terbit']
        #process
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql="UPDATE buku SET judul_buku= %s, pengarang= %s, penerbit= %s, tahun_terbit= %s WHERE id_buku = %s"
        cursor.execute(sql, (judul_buku,pengarang,penerbit,tahun_terbit, id_buku))
        mysql.connection.commit()
        flash("You have successfully edited", "success")  
        return redirect(url_for('get_buku_all'))

    sql="SELECT * FROM buku WHERE id_buku = %s"
    cursor.execute(sql,(id_buku, ))
    buku_one = cursor.fetchone()
    return render_template('buku/edit_buku.html', data=buku_one)

@app.route('/buku/<string:id_user>', methods =['GET'])
def get_buku_one(id_buku):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql="SELECT * FROM buku WHERE id_buku = %s"
    cursor.execute(sql,(id_buku, ))
    buku_one = cursor.fetchone()
    return render_template('buku/edit_buku.html', data=buku_one)

@app.route('/buku/delete/<string:id_buku>', methods =['GET', 'DELETE'])
def delete_buku(id_buku):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if id_buku:        
        sql="DELETE FROM buku WHERE `id_buku` = %s"
        cursor.execute(sql,(id_buku, )) 
        mysql.connection.commit()
        flash("You have successfully Delete it!", "success") 
        return redirect(url_for('get_buku_all'))

    return redirect(url_for('get_buku_all'))    

@app.route('/logout', methods=['GET'])
def logout():
    session['loggedin'] = False
    session['id_user'] = None
    session['username'] = None
    session['role'] = None
    # Redirect to home page
    return redirect(url_for('login'))
    
if __name__ =='__main__':
	app.run(Debug=True)

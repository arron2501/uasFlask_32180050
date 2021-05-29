import MySQLdb
import os
import hashlib
import pdfkit
import jinja2
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SECRET_KEY'] = 'u!a@s#f$l%a^s&k*_(32180050)'

# Koneksi ke database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'uasflask_32180050'
mysql = MySQL(app)

# Mengatur lamanya session akan tersimpan
app.permanent_session_lifetime = timedelta(days=1)

# Mengatur ekstensi yang diperbolehkan untuk diupload
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Mengatur lokasi folder untuk menempatkan file yang akan diupload
app.config['AGENTS_UPLOAD_FOLDER'] = '\\'.join(
    './static/images/uploads/agents'.split("/"))
app.config['ABILITIES_UPLOAD_FOLDER'] = '\\'.join(
    './static/images/uploads/agents/abilities'.split("/"))
app.config['WEAPONS_UPLOAD_FOLDER'] = '\\'.join(
    './static/images/uploads/weapons'.split("/"))
app.config['MAPS_UPLOAD_FOLDER'] = '\\'.join(
    './static/images/uploads/maps'.split("/"))

# Setting flask-mail untuk gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'ravencase.testflaskmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'testflaskmail'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = True

# Konfigurasi pdfkit
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
app.config['PDF_FOLDER'] = os.path.realpath('.') + \
    '/static/pdf'


# --- Autentikasi ---
@app.route('/login', methods=['get', 'post'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Apabila requestnya POST, maka sistem akan mengambil value dari inputan dan mengirim ke database
        email = request.form['email']
        # Mengubah password yang diketik dari tipe teks ke md5 agar lebih aman
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        # Proses komunikasi dengan database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM users WHERE email = %s AND password = %s', (email, password,))
        auth_result = cursor.fetchone()
        # Apabila inputan sama dengan atau cocok dengan data pada database, maka statemen berikut akan diset
        if auth_result:
            # Session user
            # Menyalakan timer session
            session.permanent = True
            # Fungsi loggedin ini sebagai statemen untuk menampilkan membuktikan bahwa user telah login
            session['loggedin'] = True
            # Mengambil data user dari database untuk disimpan sementara kedalam session
            session['id'] = auth_result['id']
            session['role_id'] = auth_result['role_id']
            session['name'] = auth_result['name']
            session['email'] = auth_result['email']
            session['created_at'] = auth_result['created_at']
            # Jika role_id nya 1 (member), maka otomatis akan redirect ke halaman khusus member
            if session.get('role_id') == 1:
                return redirect(url_for('index'))
            # Jika role_id nya 0 (admin), maka otomatis akan redirect ke halaman khusus admin
            if session.get('role_id') == 0:
                return redirect(url_for('admin'))
        # Apabila tidak cocok atau proses autentikasi gagal, maka akan tampil pesan flash berikut
        else:
            flash('Incorrect username/password!')
    else:
        # User dan admin akan diredirect ke page indexnya masing-masing apabila, mengakses halaman login pada saat user/admin tsb sudah login
        if "name" in session:
            # Jika role_id nya 1 (member), maka otomatis akan redirect ke halaman khusus member
            if session.get('role_id') == 1:
                return redirect(url_for('index'))
            # Jika role_id nya 0 (admin), maka otomatis akan redirect ke halaman khusus admin
            if session.get('role_id') == 0:
                return redirect(url_for('admin'))
    return render_template('/auth/login.html', title="Sign In", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")


@app.route('/register', methods=['get', 'post'])
def register():
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'confirmpassword' in request.form:
        # Apabila requestnya POST, maka sistem akan mengambil value dari inputan dan mengirim ke database
        id = None
        # Set role_id ke 1 (member), untuk membedakan antara member dengan admin
        role_id = 1
        name = request.form['name']
        email = request.form['email']
        # Mengubah password yang diinput dari tipe string ke md5 agar lebih aman
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        # Menambahkan timestamp untuk merekam tanggal register
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Proses komunikasi dengan database
        register_user = (id, role_id, name, email,
                         password, created_at, updated_at)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        users = cursor.fetchone()
        # Jika email yang diinput sudah terdaftar, maka proses input ke database dibatalkan
        if users:
            flash('Email already registered! Please use another email!')
            return redirect(url_for('register'))
        # Jika data yang diinput unik, maka data akan dikirim ke database
        else:
            cursor.execute(
                """INSERT INTO users VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % register_user)
            mysql.connection.commit()
            cursor.close()
            flash('Successfully registered! You can login now!')
            # Mengirim email greetings new user
            msg = Message("Registration Success! 🎉", sender=("VALORANT Guides Team", app.config.get("MAIL_USERNAME")),
                          recipients=[(name, email)])
            msg.html = render_template('email/welcome_user.html', name=name)
            try:
                mail = Mail(app)
                mail.connect()
                mail.send(msg)
                print('Greetings email sent!')
                return redirect(url_for('login'))
            except:
                return print('Failed to send greetings email!')
    else:
        # User dan admin akan diredirect ke page indexnya masing-masing apabila, mengakses halaman register pada saat user/admin tsb sudah login
        if "name" in session:
            # Jika role_id nya 1 (member), maka otomatis akan redirect ke halaman khusus member
            if session.get('role_id') == 1:
                return redirect(url_for('index'))
            # Jika role_id nya 0 (admin), maka otomatis akan redirect ke halaman khusus admin
            if session.get('role_id') == 0:
                return redirect(url_for('admin'))
    # Apabila requestnya GET, maka sistem akan menampilkan form register
    return render_template('/auth/register.html', title="Register", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")


@app.route('/register_admin', methods=['get', 'post'])
def register_admin():
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'confirmpassword' in request.form:
        # Apabila requestnya POST, maka sistem akan mengambil value dari inputan dan mengirim ke database
        id = None
        # Set role_id ke 0 (admin), untuk membedakan antara member dengan admin
        role_id = 0
        name = request.form['name']
        email = request.form['email']
        # Mengubah password yang diinput dari tipe string ke md5 agar lebih aman
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        # Menambahkan timestamp untuk merekam tanggal register
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Proses komunikasi dengan database
        register_user = (id, role_id, name, email,
                         password, created_at, updated_at)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        users = cursor.fetchone()
        # Jika email yang diinput sudah terdaftar, maka proses input ke database dibatalkan
        if users:
            flash('Email already registered! Please use another email!')
            return redirect(url_for('register'))
        # Jika data yang diinput unik, maka data akan dikirim ke database
        else:
            cursor.execute(
                """INSERT INTO users VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % register_user)
            mysql.connection.commit()
            cursor.close()
            flash('Successfully registered! You can login now!')
            # Mengirim email greetings new user
            msg = Message("Registration Success! 🎉", sender=("VALORANT Guides Team", app.config.get("MAIL_USERNAME")),
                          recipients=[(name, email)])
            msg.html = render_template('email/welcome_user.html', name=name)
            try:
                mail = Mail(app)
                mail.connect()
                mail.send(msg)
                print('Greetings email sent!')
                return redirect(url_for('login'))
            except:
                return print('Failed to send greetings email!')
    else:
        # User dan admin akan diredirect ke page indexnya masing-masing apabila, mengakses halaman register_admin pada saat user/admin tsb sudah login
        if "name" in session:
            # Jika role_id nya 1 (member), maka otomatis akan redirect ke halaman khusus member
            if session.get('role_id') == 1:
                return redirect(url_for('index'))
            # Jika role_id nya 0 (admin), maka otomatis akan redirect ke halaman khusus admin
            if session.get('role_id') == 0:
                return redirect(url_for('admin'))
    # Apabila requestnya GET, maka sistem akan menampilkan form register admin
    return render_template('/auth/register_admin.html', title="Register Admin", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")


@app.route('/logout')
def logout():
    # Menghapus semua data session
    session['loggedin'] = False
    session.pop('id', None)
    session.pop('role_id', None)
    session.pop('name', None)
    session.pop('email', None)
    session.pop('created_at', None)
    # Kemudian kembali ke halaman login
    return redirect(url_for('login'))


# --- For Admin ---
@app.route('/admin')
def admin():
    # Menghalangi member agar tidak bisa masuk ke halaman admin
    if session['loggedin'] == True and session.get('role_id') != 0:
        print('Member not allowed to access admin page!')
        return redirect(url_for('index'))
    return render_template('/admin/index.html', title="Admin Page", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")


# --- Manage ---
@app.route('/manage_agents', methods=['get', 'post'])
def manage_agents():
    # Proses komunikasi dengan database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM agents")
    agent_data = cursor.fetchall()
    # Memastikan apakah yang membuka halaman adalah admin
    if session['loggedin'] == True and session.get('role_id') == 0:
        return render_template('/admin/agents/index.html', title="Manage Agents", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden", agent_data=agent_data)
    else:
        flash('Masuk dulu sebagai admin!')
        return redirect(url_for('admin'))


@app.route('/manage_weapons', methods=['get', 'post'])
def manage_weapons():
    # Proses komunikasi dengan database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM weapons")
    weapon_data = cursor.fetchall()
    # Memastikan apakah yang membuka halaman adalah admin
    if session['loggedin'] == True and session.get('role_id') == 0:
        return render_template('/admin/weapons/index.html', title="Manage Weapons", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden", weapon_data=weapon_data)
    else:
        flash('Masuk dulu sebagai admin!')
        return redirect(url_for('admin'))


@app.route('/manage_maps', methods=['get', 'post'])
def manage_maps():
    # Proses komunikasi dengan database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM maps")
    map_data = cursor.fetchall()
    # Memastikan apakah yang membuka halaman adalah admin
    if session['loggedin'] == True and session.get('role_id') == 0:
        return render_template('/admin/maps/index.html', title="Manage Maps", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden", map_data=map_data)
    else:
        flash('Masuk dulu sebagai admin!')
        return redirect(url_for('admin'))


# --- Add ---
def allowed_file(filename):
    # Fungsi untuk mengecek filename dari data yang diinput
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add_agent', methods=['get', 'post'])
def add_agent():
    if request.method == 'POST':
        # Apabila requestnya POST, maka sistem akan mengambil value dari inputan dan mengirim ke database
        id = None
        # Jika form kosong, maka akan muncul pesan berikut
        if 'agentimage' not in request.files:
            flash('Please upload agent image!')
            return redirect(url_for('add_agent'))
        agentimage = request.files['agentimage']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if agentimage and allowed_file(agentimage.filename):
            filename = secure_filename(agentimage.filename)
            agentimage.save(os.path.join(
                app.config['AGENTS_UPLOAD_FOLDER'], filename))
        agentimage = "uploads/agents/" + \
            (agentimage.filename).replace(" ", "_")
        agentname = request.form['agentname']
        if 'agentrole' not in request.form:
            flash('Please select agent role!')
            return redirect(url_for('add_agent'))
        agentrole = request.form['agentrole']
        agentbio = request.form['agentbio']
        a1 = request.form['a1']
        a2 = request.form['a2']
        a3 = request.form['a3']
        a4 = request.form['a4']
        # Jika form kosong, maka akan muncul pesan berikut
        if 'ai1' not in request.files:
            flash('Please upload ability 1 image!')
            return redirect(url_for('add_agent'))
        ai1 = request.files['ai1']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if ai1 and allowed_file(ai1.filename):
            filename = secure_filename(ai1.filename)
            ai1.save(os.path.join(
                app.config['ABILITIES_UPLOAD_FOLDER'], filename))
        ai1 = "uploads/agents/abilities/" + \
            (ai1.filename).replace(" ", "_")
        # Jika form kosong, maka akan muncul pesan berikut
        if 'ai2' not in request.files:
            flash('Please upload ability 2 image!')
            return redirect(url_for('add_agent'))
        ai2 = request.files['ai2']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if ai2 and allowed_file(ai2.filename):
            filename = secure_filename(ai2.filename)
            ai2.save(os.path.join(
                app.config['ABILITIES_UPLOAD_FOLDER'], filename))
        ai2 = "uploads/agents/abilities/" + \
            (ai2.filename).replace(" ", "_")
        # Jika form kosong, maka akan muncul pesan berikut
        if 'ai3' not in request.files:
            flash('Please upload ability 3 image!')
            return redirect(url_for('add_agent'))
        ai3 = request.files['ai3']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if ai3 and allowed_file(ai3.filename):
            filename = secure_filename(ai3.filename)
            ai3.save(os.path.join(
                app.config['ABILITIES_UPLOAD_FOLDER'], filename))
        ai3 = "uploads/agents/abilities/" + \
            (ai3.filename).replace(" ", "_")
        # Jika form kosong, maka akan muncul pesan berikut
        if 'ai4' not in request.files:
            flash('Please upload ability 4 image!')
            return redirect(url_for('add_agent'))
        ai4 = request.files['ai4']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if ai4 and allowed_file(ai4.filename):
            filename = secure_filename(ai4.filename)
            ai4.save(os.path.join(
                app.config['ABILITIES_UPLOAD_FOLDER'], filename))
        ai4 = "uploads/agents/abilities/" + \
            (ai4.filename).replace(" ", "_")
        ad1 = request.form['ad1']
        ad2 = request.form['ad2']
        ad3 = request.form['ad3']
        ad4 = request.form['ad4']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        agent_data = (id, agentimage, agentname, agentrole, agentbio, a1,
                      ai1, ad1, a2, ai2, ad2, a3, ai3, ad3, a4, ai4, ad4, created_at, updated_at)
        # Proses komunikasi dengan database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            '''INSERT INTO agents VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s","%s", "%s", "%s", "%s", "%s")''' % agent_data)
        mysql.connection.commit()
        cursor.close()

        # Inisialisasi direktori file pdf
        pdffile = app.config['PDF_FOLDER'] + '/updates.pdf'
        # Proses render html dengan jinja template agar bisa dikonversi menjadi file pdf
        venv = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
        template = venv.get_template('templates/pdf/updates.html')
        html_out = template.render(
            updates="New Agent", image=agentimage, name=agentname)
        css = 'static/css/pdf_styles.css'

        options = {
            "enable-local-file-access": None
        }
        # Proses konversi menjadi file pdf
        pdfkit.from_string(html_out, pdffile,
                           configuration=config, css=css, options=options)
        # Mengirim email new updates ke semua user
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        user_data = cursor.fetchall()
        for row in user_data:
            with app.open_resource(pdffile) as fp:
                name = row['name']
                email = row['email']
                # Custom file name attachment pdf
                filename = "VALORANT_UPDATES_" + created_at
                msg = Message("New Updates! 🎉", sender=("VALORANT Guides Team", app.config.get(
                    "MAIL_USERNAME")), recipients=[(name, email)])
                msg.html = render_template(
                    'email/new_updates.html', name=name, date=created_at)
                msg.attach(filename, "application/pdf",
                           fp.read())
                try:
                    mail = Mail(app)
                    mail.connect()
                    mail.send(msg)
                    print('New updates email sent!')
                except:
                    return print('Failed to send new updates email!')
        flash('Success add agent!')
        return redirect(url_for('manage_agents'))
    # Apabila requestnya GET, maka sistem akan menampilkan form tambah agent
    else:
        if session['loggedin'] == True and session.get('role_id') == 0:
            return render_template('/admin/agents/add.html', title="Add Agent", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")
        else:
            flash('Masuk dulu sebagai admin!')
            return redirect(url_for('admin'))


@app.route('/add_weapon', methods=['get', 'post'])
def add_weapon():
    if request.method == 'POST':
        # Apabila requestnya POST, maka sistem akan mengambil value dari inputan dan mengirim ke database
        id = None
        # Jika form kosong, maka akan muncul pesan berikut
        if 'weaponimage' not in request.files:
            flash('Please upload weapon image!')
            return redirect(url_for('add_weapon'))
        weaponimage = request.files['weaponimage']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if weaponimage and allowed_file(weaponimage.filename):
            filename = secure_filename(weaponimage.filename)
            weaponimage.save(os.path.join(
                app.config['WEAPONS_UPLOAD_FOLDER'], filename))
        weaponimage = "uploads/weapons/" + \
            (weaponimage.filename).replace(" ", "_")
        weaponname = request.form['weaponname']
        weaponcategory = request.form['weaponcategory']
        pfr = request.form['pfr']
        afr = request.form['afr']
        bodydmg = request.form['bodydmg']
        headdmg = request.form['headdmg']
        legdmg = request.form['legdmg']
        mag = request.form['mag']
        wp = request.form['wp']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        weapon_data = (id, weaponimage, weaponname, weaponcategory, pfr,
                       afr, bodydmg, headdmg, legdmg, mag, wp, created_at, updated_at)
        # Proses komunikasi dengan database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            '''INSERT INTO weapons VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")''' % weapon_data)
        mysql.connection.commit()
        cursor.close()
        # Inisialisasi direktori file pdf
        pdffile = app.config['PDF_FOLDER'] + '/updates.pdf'
        # Proses render html dengan jinja template agar bisa dikonversi menjadi file pdf
        venv = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
        template = venv.get_template('templates/pdf/updates.html')
        html_out = template.render(
            updates="New Weapon", image=weaponimage, name=weaponname)
        css = 'static/css/pdf_styles.css'

        options = {
            "enable-local-file-access": None
        }
        # Proses konversi menjadi file pdf
        pdfkit.from_string(html_out, pdffile,
                           configuration=config, css=css, options=options)
        # Mengirim email new updates ke semua user
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        user_data = cursor.fetchall()
        for row in user_data:
            with app.open_resource(pdffile) as fp:
                name = row['name']
                email = row['email']
                # Custom file name attachment pdf
                filename = "VALORANT_UPDATES_" + created_at
                msg = Message("New Updates! 🎉", sender=("VALORANT Guides Team", app.config.get(
                    "MAIL_USERNAME")), recipients=[(name, email)])
                msg.html = render_template(
                    'email/new_updates.html', name=name, date=created_at)
                msg.attach(filename, "application/pdf",
                           fp.read())
                try:
                    mail = Mail(app)
                    mail.connect()
                    mail.send(msg)
                    print('New updates email sent!')
                except:
                    return print('Failed to send new updates email!')
        flash('Success add weapon!')
        return redirect(url_for('manage_weapons'))
    # Apabila requestnya GET, maka sistem akan menampilkan form tambah weapon
    else:
        if session['loggedin'] == True and session.get('role_id') == 0:
            return render_template('/admin/weapons/add.html', title="Add Weapon", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")
        else:
            flash('Masuk dulu sebagai admin!')
            return redirect(url_for('admin'))


@app.route('/add_map', methods=['get', 'post'])
def add_map():
    if request.method == 'POST':
        # Apabila requestnya POST, maka sistem akan mengambil value dari inputan dan mengirim ke database
        id = None
        # Jika form kosong, maka akan muncul pesan berikut
        if 'mapsplash' not in request.files:
            flash('Please upload map splash image!')
            return redirect(url_for('add_map'))
        mapsplash = request.files['mapsplash']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if mapsplash and allowed_file(mapsplash.filename):
            filename = secure_filename(mapsplash.filename)
            mapsplash.save(os.path.join(
                app.config['MAPS_UPLOAD_FOLDER'], filename))
        mapsplash = "uploads/maps/" + \
            (mapsplash.filename).replace(" ", "_")
        # Jika form kosong, maka akan muncul pesan berikut
        if 'mapdisplay' not in request.files:
            flash('Please upload map display image!')
            return redirect(url_for('add_map'))
        mapdisplay = request.files['mapdisplay']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if mapdisplay and allowed_file(mapdisplay.filename):
            filename = secure_filename(mapdisplay.filename)
            mapdisplay.save(os.path.join(
                app.config['MAPS_UPLOAD_FOLDER'], filename))
        mapdisplay = "uploads/maps/" + \
            (mapdisplay.filename).replace(" ", "_")
        mapname = request.form['mapname']
        mapcoordinate = request.form['mapcoordinate']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        map_data = (id, mapsplash, mapdisplay, mapname,
                    mapcoordinate, created_at, updated_at)
        # Proses komunikasi dengan database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            '''INSERT INTO maps VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s")''' % map_data)
        mysql.connection.commit()
        cursor.close()
        # Inisialisasi direktori file pdf
        pdffile = app.config['PDF_FOLDER'] + '/updates.pdf'
        # Proses render html dengan jinja template agar bisa dikonversi menjadi file pdf
        venv = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
        template = venv.get_template('templates/pdf/updates.html')
        html_out = template.render(
            updates="New Map", image=mapsplash, name=mapname)
        css = 'static/css/pdf_styles.css'

        options = {
            "enable-local-file-access": None
        }
        # Proses konversi menjadi file pdf
        pdfkit.from_string(html_out, pdffile,
                           configuration=config, css=css, options=options)
        # Mengirim email new updates ke semua user
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        user_data = cursor.fetchall()
        for row in user_data:
            with app.open_resource(pdffile) as fp:
                name = row['name']
                email = row['email']
                # Custom file name attachment pdf
                filename = "VALORANT_UPDATES_" + created_at
                msg = Message("New Updates! 🎉", sender=("VALORANT Guides Team", app.config.get(
                    "MAIL_USERNAME")), recipients=[(name, email)])
                msg.html = render_template(
                    'email/new_updates.html', name=name, date=created_at)
                msg.attach(filename, "application/pdf",
                           fp.read())
                try:
                    mail = Mail(app)
                    mail.connect()
                    mail.send(msg)
                    print('New updates email sent!')
                except:
                    return print('Failed to send new updates email!')

        flash('Success add map!')
        return redirect(url_for('manage_maps'))
    # Apabila requestnya GET, maka sistem akan menampilkan form tambah map
    else:
        if session['loggedin'] == True and session.get('role_id') == 0:
            return render_template('/admin/maps/add.html', title="Add Map", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")
        else:
            flash('Masuk dulu sebagai admin!')
            return redirect(url_for('admin'))


# --- Edit ---
@app.route('/edit_agent/<id>', methods=['get', 'post'])
def edit_agent(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM agents WHERE id='%s'" % id)
    agent_data = cursor.fetchone()
    if request.method == 'POST':
        # Apabila requestnya POST, maka sistem akan mengambil value dari inputan dan mengirim ke database
        # Jika form kosong, maka akan muncul pesan berikut
        if 'agentimage' not in request.files:
            flash('Please upload agent image!')
            return redirect(url_for('add_agent'))
        agentimage = request.files['agentimage']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if agentimage and allowed_file(agentimage.filename):
            filename = secure_filename(agentimage.filename)
            agentimage.save(os.path.join(
                app.config['AGENTS_UPLOAD_FOLDER'], filename))
        agentimage = "uploads/agents/" + \
            (agentimage.filename).replace(" ", "_")
        agentname = request.form['agentname']
        if 'agentrole' not in request.form:
            flash('Please select agent role!')
            return redirect(url_for('add_agent'))
        agentrole = request.form['agentrole']
        agentbio = request.form['agentbio']
        a1 = request.form['a1']
        a2 = request.form['a2']
        a3 = request.form['a3']
        a4 = request.form['a4']
        # Jika form kosong, maka akan muncul pesan berikut
        if 'ai1' not in request.files:
            flash('Please upload ability 1 image!')
            return redirect(url_for('add_agent'))
        ai1 = request.files['ai1']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if ai1 and allowed_file(ai1.filename):
            filename = secure_filename(ai1.filename)
            ai1.save(os.path.join(
                app.config['ABILITIES_UPLOAD_FOLDER'], filename))
        ai1 = "uploads/agents/abilities/" + \
            (ai1.filename).replace(" ", "_")
        # Jika form kosong, maka akan muncul pesan berikut
        if 'ai2' not in request.files:
            flash('Please upload ability 2 image!')
            return redirect(url_for('add_agent'))
        ai2 = request.files['ai2']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if ai2 and allowed_file(ai2.filename):
            filename = secure_filename(ai2.filename)
            ai2.save(os.path.join(
                app.config['ABILITIES_UPLOAD_FOLDER'], filename))
        ai2 = "uploads/agents/abilities/" + \
            (ai2.filename).replace(" ", "_")
        # Jika form kosong, maka akan muncul pesan berikut
        if 'ai3' not in request.files:
            flash('Please upload ability 3 image!')
            return redirect(url_for('add_agent'))
        ai3 = request.files['ai3']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if ai3 and allowed_file(ai3.filename):
            filename = secure_filename(ai3.filename)
            ai3.save(os.path.join(
                app.config['ABILITIES_UPLOAD_FOLDER'], filename))
        ai3 = "uploads/agents/abilities/" + \
            (ai3.filename).replace(" ", "_")
        # Jika form kosong, maka akan muncul pesan berikut
        if 'ai4' not in request.files:
            flash('Please upload ability 4 image!')
            return redirect(url_for('add_agent'))
        ai4 = request.files['ai4']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if ai4 and allowed_file(ai4.filename):
            filename = secure_filename(ai4.filename)
            ai4.save(os.path.join(
                app.config['ABILITIES_UPLOAD_FOLDER'], filename))
        ai4 = "uploads/agents/abilities/" + \
            (ai4.filename).replace(" ", "_")
        ad1 = request.form['ad1']
        ad2 = request.form['ad2']
        ad3 = request.form['ad3']
        ad4 = request.form['ad4']
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Proses komunikasi dengan database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            '''UPDATE agents SET img="%s", name="%s", role="%s", bio="%s", a1="%s", ai1="%s", ad1="%s", a2="%s", ai2="%s", ad2="%s", a3="%s", ai3="%s", ad3="%s", a4="%s", ai4="%s", ad4="%s", updated_at="%s"
            WHERE id="%s" ''' % (agentimage, agentname, agentrole, agentbio, a1,
                                 ai1, ad1, a2, ai2, ad2, a3, ai3, ad3, a4, ai4, ad4, updated_at, id))
        mysql.connection.commit()
        cursor.close()
        # Inisialisasi direktori file pdf
        pdffile = app.config['PDF_FOLDER'] + '/updates.pdf'
        # Proses render html dengan jinja template agar bisa dikonversi menjadi file pdf
        venv = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
        template = venv.get_template('templates/pdf/updates.html')
        html_out = template.render(
            updates="Agent Updates", image=agentimage, name=agentname)
        css = 'static/css/pdf_styles.css'

        options = {
            "enable-local-file-access": None
        }
        # Proses konversi menjadi file pdf
        pdfkit.from_string(html_out, pdffile,
                           configuration=config, css=css, options=options)
        # Mengirim email new updates ke semua user
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        user_data = cursor.fetchall()
        for row in user_data:
            with app.open_resource(pdffile) as fp:
                name = row['name']
                email = row['email']
                # Custom file name attachment pdf
                filename = "VALORANT_UPDATES_" + updated_at
                msg = Message("New Updates! 🎉", sender=("VALORANT Guides Team", app.config.get(
                    "MAIL_USERNAME")), recipients=[(name, email)])
                msg.html = render_template(
                    'email/new_updates.html', name=name, date=updated_at)
                msg.attach(filename, "application/pdf",
                           fp.read())
                try:
                    mail = Mail(app)
                    mail.connect()
                    mail.send(msg)
                    print('New updates email sent!')
                except:
                    return print('Failed to send new updates email!')
        flash('Success update agent!')
        return redirect(url_for('manage_agents'))
    # Apabila requestnya GET, maka sistem akan menampilkan form edit agent
    else:
        cursor.close()
        if session['loggedin'] == True and session.get('role_id') == 0:
            return render_template('/admin/agents/edit.html', title="Edit Agent", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden", agent_data=agent_data)
        else:
            flash('Masuk dulu sebagai admin!')
            return redirect(url_for('admin'))


@app.route('/edit_weapon/<id>', methods=['get', 'post'])
def edit_weapon(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM weapons WHERE id='%s'" % id)
    weapon_data = cursor.fetchone()
    if request.method == 'POST':
        # Apabila requestnya POST, maka sistem akan mengambil value dari inputan dan mengirim ke database
        # Jika form kosong, maka akan muncul pesan berikut
        if 'weaponimage' not in request.files:
            flash('Please upload weapon image!')
            return redirect(url_for('add_weapon'))
        weaponimage = request.files['weaponimage']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if weaponimage and allowed_file(weaponimage.filename):
            filename = secure_filename(weaponimage.filename)
            weaponimage.save(os.path.join(
                app.config['WEAPONS_UPLOAD_FOLDER'], filename))
        weaponimage = "uploads/weapons/" + \
            (weaponimage.filename).replace(" ", "_")
        weaponname = request.form['weaponname']
        weaponcategory = request.form['weaponcategory']
        pfr = request.form['pfr']
        afr = request.form['afr']
        bodydmg = request.form['bodydmg']
        headdmg = request.form['headdmg']
        legdmg = request.form['legdmg']
        mag = request.form['mag']
        wp = request.form['wp']
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Proses komunikasi dengan database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
        UPDATE weapons SET img="%s", name="%s", category="%s", pfr="%s", afr="%s", body_dmg="%s", head_dmg="%s", leg_dmg="%s", mag="%s", wp="%s", updated_at="%s"
        WHERE id="%s" ''' % (weaponimage, weaponname, weaponcategory, pfr, afr, bodydmg, headdmg, legdmg, mag, wp, updated_at, id))
        mysql.connection.commit()
        cursor.close()
        # Inisialisasi direktori file pdf
        pdffile = app.config['PDF_FOLDER'] + '/updates.pdf'
        # Proses render html dengan jinja template agar bisa dikonversi menjadi file pdf
        venv = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
        template = venv.get_template('templates/pdf/updates.html')
        html_out = template.render(
            updates="Weapon Updates", image=weaponimage, name=weaponname)
        css = 'static/css/pdf_styles.css'

        options = {
            "enable-local-file-access": None
        }
        # Proses konversi menjadi file pdf
        pdfkit.from_string(html_out, pdffile,
                           configuration=config, css=css, options=options)
        # Mengirim email new updates ke semua user
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        user_data = cursor.fetchall()
        for row in user_data:
            with app.open_resource(pdffile) as fp:
                name = row['name']
                email = row['email']
                # Custom file name attachment pdf
                filename = "VALORANT_UPDATES_" + updated_at
                msg = Message("New Updates! 🎉", sender=("VALORANT Guides Team", app.config.get(
                    "MAIL_USERNAME")), recipients=[(name, email)])
                msg.html = render_template(
                    'email/new_updates.html', name=name, date=updated_at)
                msg.attach(filename, "application/pdf",
                           fp.read())
                try:
                    mail = Mail(app)
                    mail.connect()
                    mail.send(msg)
                    print('New updates email sent!')
                except:
                    return print('Failed to send new updates email!')
        flash('Success update weapon!')
        return redirect(url_for('manage_weapons'))
    # Apabila requestnya GET, maka sistem akan menampilkan form edit weapon
    else:
        cursor.close()
        if session['loggedin'] == True and session.get('role_id') == 0:
            return render_template('/admin/weapons/edit.html', title="Edit Weapon", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden", weapon_data=weapon_data)
        else:
            flash('Masuk dulu sebagai admin!')
            return redirect(url_for('admin'))


@app.route('/edit_map/<id>', methods=['get', 'post'])
def edit_map(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM maps WHERE id='%s'" % id)
    map_data = cursor.fetchone()
    if request.method == 'POST':
        # Apabila requestnya POST, maka sistem akan mengambil value dari inputan dan mengirim ke database
        # Jika form kosong, maka akan muncul pesan berikut
        if 'mapsplash' not in request.files:
            flash('Please upload map splash image!')
            return redirect(url_for('add_map'))
        mapsplash = request.files['mapsplash']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if mapsplash and allowed_file(mapsplash.filename):
            filename = secure_filename(mapsplash.filename)
            mapsplash.save(os.path.join(
                app.config['MAPS_UPLOAD_FOLDER'], filename))
        mapsplash = "uploads/maps/" + \
            (mapsplash.filename).replace(" ", "_")
        # Jika form kosong, maka akan muncul pesan berikut
        if 'mapdisplay' not in request.files:
            flash('Please upload map display image!')
            return redirect(url_for('add_map'))
        mapdisplay = request.files['mapdisplay']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if mapdisplay and allowed_file(mapdisplay.filename):
            filename = secure_filename(mapdisplay.filename)
            mapdisplay.save(os.path.join(
                app.config['MAPS_UPLOAD_FOLDER'], filename))
        mapdisplay = "uploads/maps/" + \
            (mapdisplay.filename).replace(" ", "_")
        mapname = request.form['mapname']
        mapcoordinate = request.form['mapcoordinate']
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Proses komunikasi dengan database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
        UPDATE maps SET splash="%s", display="%s", name="%s", coordinate="%s", updated_at="%s"
        WHERE id="%s" ''' % (mapsplash, mapdisplay, mapname, mapcoordinate, updated_at, id))
        mysql.connection.commit()
        cursor.close()
        # Inisialisasi direktori file pdf
        pdffile = app.config['PDF_FOLDER'] + '/updates.pdf'
        # Proses render html dengan jinja template agar bisa dikonversi menjadi file pdf
        venv = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
        template = venv.get_template('templates/pdf/updates.html')
        html_out = template.render(
            updates="Map Updates", image=mapsplash, name=mapname)
        css = 'static/css/pdf_styles.css'

        options = {
            "enable-local-file-access": None
        }
        # Proses konversi menjadi file pdf
        pdfkit.from_string(html_out, pdffile,
                           configuration=config, css=css, options=options)
        # Mengirim email new updates ke semua user
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        user_data = cursor.fetchall()
        for row in user_data:
            with app.open_resource(pdffile) as fp:
                name = row['name']
                email = row['email']
                # Custom file name attachment pdf
                filename = "VALORANT_UPDATES_" + updated_at
                msg = Message("New Updates! 🎉", sender=("VALORANT Guides Team", app.config.get(
                    "MAIL_USERNAME")), recipients=[(name, email)])
                msg.html = render_template(
                    'email/new_updates.html', name=name, date=updated_at)
                msg.attach(filename, "application/pdf",
                           fp.read())
                try:
                    mail = Mail(app)
                    mail.connect()
                    mail.send(msg)
                    print('New updates email sent!')
                except:
                    return print('Failed to send new updates email!')
        flash('Success update map!')
        return redirect(url_for('manage_maps'))
    # Apabila requestnya GET, maka sistem akan menampilkan form edit map
    else:
        cursor.close()
        if session['loggedin'] == True and session.get('role_id') == 0:
            return render_template('/admin/maps/edit.html', title="Edit Map", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden", map_data=map_data)
        else:
            flash('Masuk dulu sebagai admin!')
            return redirect(url_for('admin'))


# --- Delete ---
@app.route('/delete_agent/<id>', methods=['get', 'post'])
def delete_agent(id):
    # Proses hapus agent
    # Wajib login sbg admin, jika belum login maka akan redirect ke halaman login
    if session['loggedin'] == True and session.get('role_id') == 0:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM agents WHERE id='%s'" % id)
        mysql.connection.commit()
        cursor.close()
        flash('Agent successfully deleted!')
        return redirect(url_for('manage_agents'))
    else:
        flash('Masuk dulu sebagai admin!')
        return redirect(url_for('admin'))


@app.route('/delete_weapon/<id>', methods=['get', 'post'])
def delete_weapon(id):
    # Proses hapus weapon
    # Wajib login sbg admin, jika belum login maka akan redirect ke halaman login
    if session['loggedin'] == True and session.get('role_id') == 0:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM weapons WHERE id='%s'" % id)
        mysql.connection.commit()
        cursor.close()
        flash('Weapon successfully deleted!')
        return redirect(url_for('manage_weapons'))
    else:
        flash('Masuk dulu sebagai admin!')
        return redirect(url_for('admin'))


@app.route('/delete_map/<id>', methods=['get', 'post'])
def delete_map(id):
    # Proses hapus map
    # Wajib login sbg admin, jika belum login maka akan redirect ke halaman login
    if session['loggedin'] == True and session.get('role_id') == 0:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM maps WHERE id='%s'" % id)
        mysql.connection.commit()
        cursor.close()
        flash('Map successfully deleted!')
        return redirect(url_for('manage_maps'))
    else:
        flash('Masuk dulu sebagai admin!')
        return redirect(url_for('admin'))


# --- For Member ---
# START Home Page
@app.route('/')
def index():
    if session['loggedin'] == True:
        return render_template('/home/index.html', title="Home", home_active="text-red-500", homemenu_active="text-white")
    else:
        return redirect(url_for('login'))
# END Home Page


# START Agents Page
@app.route('/agents', methods=['get', 'post'])
def agents():
    # Proses komunikasi dengan database utk menampilkan data dari database ke website
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM agents")
    agent_data = cursor.fetchall()
    if session['loggedin'] == True:
        return render_template('/home/agents/index.html', title="Agents", home_active="text-red-500", agents_active="text-white", agent_data=agent_data)
    # Apabila belum login akan redirect kehalaman login
    else:
        flash('You must logged in!')
        return redirect(url_for('login'))


@app.route('/agent_details/<id>', methods=['get', 'post'])
def agent_details(id):
    # Proses komunikasi dengan database utk menampilkan data dari database ke website
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM agents WHERE id = %s", (id,))
    agent_data = cursor.fetchall()
    if session['loggedin'] == True:
        return render_template('/home/agents/details.html', title="Agent Details", home_active="text-red-500", agents_active="text-white", agent_data=agent_data)
    # Apabila belum login akan redirect kehalaman login
    else:
        flash('You must logged in!')
        return redirect(url_for('login'))
# END Agents Page


# START Weapons Page
@app.route('/weapons', methods=['get', 'post'])
def weapons():
    # Proses komunikasi dengan database utk menampilkan data dari database ke website
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM weapons")
    weapon_data = cursor.fetchall()
    if session['loggedin'] == True:
        return render_template('/home/weapons/index.html', title="Weapons", home_active="text-red-500", weapons_active="text-white", weapon_data=weapon_data)
    # Apabila belum login akan redirect kehalaman login
    else:
        flash('You must logged in!')
        return redirect(url_for('login'))


@app.route('/weapon_details/<id>', methods=['get', 'post'])
def weapon_details(id):
    # Proses komunikasi dengan database utk menampilkan data dari database ke website
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM weapons WHERE id = %s", (id,))
    weapon_data = cursor.fetchall()
    if session['loggedin'] == True:
        return render_template('/home/weapons/details.html', title="Weapon Details", home_active="text-red-500", weapons_active="text-white", weapon_data=weapon_data)
    # Apabila belum login akan redirect kehalaman login
    else:
        flash('You must logged in!')
        return redirect(url_for('login'))
# END Weapons Page


# START Maps Page
@app.route('/maps', methods=['get', 'post'])
def maps():
    # Proses komunikasi dengan database utk menampilkan data dari database ke website
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM maps")
    map_data = cursor.fetchall()
    if session['loggedin'] == True:
        return render_template('/home/maps/index.html', title="Maps", home_active="text-red-500", maps_active="text-white", map_data=map_data)
    # Apabila belum login akan redirect kehalaman login
    else:
        flash('You must logged in!')
        return redirect(url_for('login'))


@app.route('/map_details/<id>', methods=['get', 'post'])
def map_details(id):
    # Proses komunikasi dengan database utk menampilkan data dari database ke website
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM maps WHERE id = %s", (id,))
    map_data = cursor.fetchall()
    if session['loggedin'] == True:
        return render_template('/home/maps/details.html', title="Map Details", home_active="text-red-500", maps_active="text-white", map_data=map_data)
    # Apabila belum login akan redirect kehalaman login
    else:
        flash('You must logged in!')
        return redirect(url_for('login'))
# END Maps Page


# START Account Page
@app.route('/accounts')
def accounts():
    if session['loggedin'] == True:
        return render_template('/accounts/index.html', title="Accounts", accounts_active="text-red-500", home_menu="hidden")
    # Apabila belum login akan redirect kehalaman login
    else:
        flash('You must logged in!')
        return redirect(url_for('login'))


@app.route('/change_password/<id>', methods=['get', 'post'])
def change_password(id):
    # Proses komunikasi dengan database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE id='%s'" % id)
    user_data = cursor.fetchone()
    if request.method == 'POST':
        # Apabila requestnya POST, maka sistem akan mengambil value dari inputan dan mengirim ke database
        oldpassword = hashlib.md5(
            request.form['oldpassword'].encode()).hexdigest()
        if oldpassword != user_data['password']:
            flash('Wrong old password!')
            return redirect(url_for('change_password', id=id))
        newpassword = hashlib.md5(
            request.form['newpassword'].encode()).hexdigest()
        confirmpassword = hashlib.md5(
            request.form['confirmpassword'].encode()).hexdigest()
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if newpassword == confirmpassword and oldpassword == user_data['password']:
            # Proses komunikasi dengan database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('''
            UPDATE users SET password="%s", updated_at="%s"
            WHERE id="%s" ''' % (newpassword, updated_at, id))
            mysql.connection.commit()
            cursor.close()
            flash('Success change password!')
            return redirect(url_for('change_password', id=id))
        else:
            flash('New password doesnt match!')
            return redirect(url_for('change_password', id=id))
    # Apabila requestnya GET, maka sistem akan menampilkan form change password
    else:
        cursor.close()
        if session['loggedin'] == True:
            return render_template('/accounts/change_password.html', title="Change Password", accounts_active="text-red-500", home_menu="hidden")
        else:
            flash('Login dulu!')
            return redirect(url_for('login'))


@app.route('/contact_us', methods=['get', 'post'])
def contact_us():
    # Harus login terlebih dahulu
    if session["loggedin"] == True:
        if request.method == 'POST':
            # Mengambil data dari form
            subject = request.form['subject']
            message = request.form['message']
            # Proses mengirim email
            msg = Message(subject, sender=(session.get('name'), app.config.get("MAIL_USERNAME")),
                          recipients=[("VALORANT Guides Team", "ravencase.testflaskmail@gmail.com")])
            msg.body = message
            try:
                mail = Mail(app)
                mail.connect()
                mail.send(msg)
                print('Email sent!')
                flash(
                    'Your email has been sent to our customer service, and will be responded soonly!')
                return redirect(url_for('contact_us'))
            except:
                flash('Failed to send ticket email!')
                return render_template('/accounts/contact_us.html', title="Contact Us", accounts_active="text-red-500", home_menu="hidden")
        else:
            return render_template('/accounts/contact_us.html', title="Contact Us", accounts_active="text-red-500", home_menu="hidden")
    # Apabila belum login akan redirect kehalaman login
    else:
        flash('You must logged in!')
        return redirect(url_for('login'))
# END Account Page


# For downloading pdf
@app.route('/download_pdf', methods=['GET', 'POST'])
def download_pdf():
    # User akan diredirect ke link download file pdf
    return redirect("http://localhost:5000/static/pdf/updates.pdf", code=302)


if __name__ == '__main__':
    app.run()

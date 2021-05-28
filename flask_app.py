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
@app.route('/manage_agents')
def manage_agents():
    return render_template('/admin/agents/index.html', title="Manage Agents", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")


@app.route('/manage_weapons')
def manage_weapons():
    return render_template('/admin/weapons/index.html', title="Manage Weapons", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")


@app.route('/manage_maps')
def manage_maps():
    return render_template('/admin/maps/index.html', title="Manage Maps", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")


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
        if 'ia1' not in request.files:
            flash('Please upload ability 1 image!')
            return redirect(url_for('add_agent'))
        ia1 = request.files['ia1']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if ia1 and allowed_file(ia1.filename):
            filename = secure_filename(ia1.filename)
            ia1.save(os.path.join(
                app.config['ABILITIES_UPLOAD_FOLDER'], filename))
        ia1 = "uploads/agents/abilities/" + \
            (ia1.filename).replace(" ", "_")
        # Jika form kosong, maka akan muncul pesan berikut
        if 'ia2' not in request.files:
            flash('Please upload ability 2 image!')
            return redirect(url_for('add_agent'))
        ia2 = request.files['ia2']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if ia2 and allowed_file(ia2.filename):
            filename = secure_filename(ia2.filename)
            ia2.save(os.path.join(
                app.config['ABILITIES_UPLOAD_FOLDER'], filename))
        ia2 = "uploads/agents/abilities/" + \
            (ia2.filename).replace(" ", "_")
        # Jika form kosong, maka akan muncul pesan berikut
        if 'ia3' not in request.files:
            flash('Please upload ability 3 image!')
            return redirect(url_for('add_agent'))
        ia3 = request.files['ia3']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if ia3 and allowed_file(ia3.filename):
            filename = secure_filename(ia3.filename)
            ia3.save(os.path.join(
                app.config['ABILITIES_UPLOAD_FOLDER'], filename))
        ia3 = "uploads/agents/abilities/" + \
            (ia3.filename).replace(" ", "_")
        # Jika form kosong, maka akan muncul pesan berikut
        if 'ia4' not in request.files:
            flash('Please upload ability 4 image!')
            return redirect(url_for('add_agent'))
        ia4 = request.files['ia4']
        # Jika form image diisi, maka filename image akan diubah menjadi format berikut
        if ia4 and allowed_file(ia4.filename):
            filename = secure_filename(ia4.filename)
            ia4.save(os.path.join(
                app.config['ABILITIES_UPLOAD_FOLDER'], filename))
        ia4 = "uploads/agents/abilities/" + \
            (ia4.filename).replace(" ", "_")
        da1 = request.form['da1']
        da2 = request.form['da2']
        da3 = request.form['da3']
        da4 = request.form['da4']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        agent_data = (id, agentimage, agentname, agentrole, agentbio, a1,
                      ia1, da1, a2, ia2, da2, a3, ia3, da3, a4, ia4, da4, created_at, updated_at)
        # Proses komunikasi dengan database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            '''INSERT INTO agents VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s","%s", "%s", "%s", "%s", "%s")''' % agent_data)
        mysql.connection.commit()
        cursor.close()
        flash('Success add agent!')
        return redirect(url_for('add_agent'))
    # Apabila requestnya GET, maka sistem akan menampilkan form tambah agent
    else:
        if session['loggedin'] == True and session.get('role_id') == 0:
            return render_template('/admin/agents/add.html', title="Add Agent", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")
        else:
            print('Masuk dulu sebagai admin!')
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
        pfm = request.form['pfm']
        pfr = request.form['pfr']
        afr = request.form['afr']
        bodydmg = request.form['bodydmg']
        headdmg = request.form['headdmg']
        legdmg = request.form['legdmg']
        mag = request.form['mag']
        wp = request.form['wp']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        weapon_data = (id, weaponimage, weaponname, weaponcategory, pfm, pfr,
                       afr, bodydmg, headdmg, legdmg, mag, wp, created_at, updated_at)
        # Proses komunikasi dengan database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            '''INSERT INTO weapons VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")''' % weapon_data)
        mysql.connection.commit()
        cursor.close()
        flash('Success add weapon!')
        return redirect(url_for('add_weapon'))
    # Apabila requestnya GET, maka sistem akan menampilkan form tambah weapon
    else:
        if session['loggedin'] == True and session.get('role_id') == 0:
            return render_template('/admin/weapons/add.html', title="Add Weapon", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")
        else:
            print('Masuk dulu sebagai admin!')
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
        flash('Success add map!')
        return redirect(url_for('add_map'))
    # Apabila requestnya GET, maka sistem akan menampilkan form tambah map
    else:
        if session['loggedin'] == True and session.get('role_id') == 0:
            return render_template('/admin/maps/add.html', title="Add Map", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")
        else:
            print('Masuk dulu sebagai admin!')
            return redirect(url_for('admin'))


# --- Edit ---
@app.route('/edit_agent')
def edit_agents():
    return render_template('/admin/agents/edit.html', title="Edit Agent", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")


@app.route('/edit_weapon')
def edit_weapon():
    return render_template('/admin/weapons/edit.html', title="Edit Weapon", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")


@app.route('/edit_map')
def edit_map():
    return render_template('/admin/maps/edit.html', title="Edit Map", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")


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
@app.route('/agents')
def agents():
    return render_template('/home/agents/index.html', title="Agents", home_active="text-red-500", agents_active="text-white")


@app.route('/agent_details')
def agent_details():
    return render_template('/home/agents/details.html', title="Agent Details", home_active="text-red-500", agents_active="text-white")
# END Agents Page


# START Weapons Page
@app.route('/weapons')
def weapons():
    return render_template('/home/weapons/index.html', title="Weapons", home_active="text-red-500", weapons_active="text-white")


@app.route('/weapon_details')
def weapon_details():
    return render_template('/home/weapons/details.html', title="Weapon Details", home_active="text-red-500", weapons_active="text-white")
# END Weapons Page


# START Maps Page
@app.route('/maps')
def maps():
    return render_template('/home/maps/index.html', title="Maps", home_active="text-red-500", maps_active="text-white")


@app.route('/map_details')
def map_details():
    return render_template('/home/maps/details.html', title="Map Details", home_active="text-red-500", maps_active="text-white")
# END Maps Page


# START Account Page
@app.route('/accounts')
def accounts():
    return render_template('/accounts/index.html', title="Accounts", accounts_active="text-red-500", home_menu="hidden")


@app.route('/change_password')
def change_password():
    return render_template('/accounts/change_password.html', title="Change Password", accounts_active="text-red-500", home_menu="hidden")


@app.route('/contact_us')
def contact_us():
    return render_template('/accounts/contact_us.html', title="Contact Us", accounts_active="text-red-500", home_menu="hidden")
# END Account Page


if __name__ == '__main__':
    app.run()

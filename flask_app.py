from flask import Flask, render_template
app = Flask(__name__)


# Auth
@app.route('/login')
def login():
   return render_template('/auth/login.html', title="Sign In", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")

@app.route('/register')
def register():
   return render_template('/auth/register.html', title="Register", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")

@app.route('/register_admin')
def register_admin():
   return render_template('/auth/register_admin.html', title="Register Admin", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")



# Admin
@app.route('/admin')
def admin():
   return render_template('/admin/index.html', title="Admin Page", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")

# Manage
@app.route('/manage_agents')
def manage_agents():
   return render_template('/admin/agents/index.html', title="Manage Agents", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")

@app.route('/manage_weapons')
def manage_weapons():
   return render_template('/admin/weapons/index.html', title="Manage Weapons", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")

@app.route('/manage_maps')
def manage_maps():
   return render_template('/admin/maps/index.html', title="Manage Maps", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")

# Add
@app.route('/add_agent')
def add_agents():
   return render_template('/admin/agents/add.html', title="Add Agent", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")

@app.route('/add_weapon')
def add_weapon():
   return render_template('/admin/weapons/add.html', title="Add Weapon", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")

@app.route('/add_map')
def add_map():
   return render_template('/admin/maps/add.html', title="Add Map", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")

# Edit
@app.route('/edit_agent')
def edit_agents():
   return render_template('/admin/agents/edit.html', title="Edit Agent", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")

@app.route('/edit_weapon')
def edit_weapon():
   return render_template('/admin/weapons/edit.html', title="Edit Weapon", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")

@app.route('/edit_map')
def edit_map():
   return render_template('/admin/maps/edit.html', title="Edit Map", home_menu="hidden", sidenav="hidden", mobile_sidenav="hidden")



# Home
@app.route('/')
def index():
    return render_template('/home/index.html', title="Home", home_active="text-red-500", homemenu_active="text-white")

@app.route('/agents')
def agents():
    return render_template('/home/agents/index.html', title="Agents", home_active="text-red-500", agents_active="text-white")

@app.route('/agent_details')
def agent_details():
    return render_template('/home/agents/details.html', title="Agent Details", home_active="text-red-500", agents_active="text-white")

@app.route('/weapons')
def weapons():
   return render_template('/home/weapons/index.html', title="Weapons", home_active="text-red-500", weapons_active="text-white")

@app.route('/weapon_details')
def weapon_details():
   return render_template('/home/weapons/details.html', title="Weapon Details", home_active="text-red-500", weapons_active="text-white")

@app.route('/maps')
def maps():
   return render_template('/home/maps/index.html', title="Maps", home_active="text-red-500", maps_active="text-white")

@app.route('/map_details')
def map_details():
   return render_template('/home/maps/details.html', title="Map Details", home_active="text-red-500", maps_active="text-white")



# Accounts
@app.route('/accounts')
def accounts():
   return render_template('/accounts/index.html', title="Accounts", accounts_active="text-red-500", home_menu="hidden")

@app.route('/change_password')
def change_password():
   return render_template('/accounts/change_password.html', title="Change Password", accounts_active="text-red-500", home_menu="hidden")

@app.route('/contact_us')
def contact_us():
   return render_template('/accounts/contact_us.html', title="Contact Us", accounts_active="text-red-500", home_menu="hidden")


if __name__ == '__main__':
    app.run()
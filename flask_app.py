from flask import Flask, render_template
app = Flask(__name__)





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
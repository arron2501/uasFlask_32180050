from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="Home", home_active="text-red-500", homemenu_active="text-white")

@app.route('/agents')
def agents():
    return render_template('/agents/index.html', title="Agents", home_active="text-red-500", agents_active="text-white")

@app.route('/agent_details')
def agent_details():
    return render_template('/agents/details.html', title="Agent Details", home_active="text-red-500", agents_active="text-white")

@app.route('/weapons')
def weapons():
   return render_template('/weapons/index.html', title="Weapons", home_active="text-red-500", weapons_active="text-white")

@app.route('/weapon_details')
def weapon_details():
   return render_template('/weapons/details.html', title="Weapon Details", home_active="text-red-500", weapons_active="text-white")

@app.route('/maps')
def maps():
   return render_template('/maps/index.html', title="Maps", home_active="text-red-500", maps_active="text-white")

@app.route('/map_details')
def map_details():
   return render_template('/maps/details.html', title="Map Details", home_active="text-red-500", maps_active="text-white")

if __name__ == '__main__':
    app.run()
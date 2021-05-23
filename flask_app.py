from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="Home", home_active="text-red-500", homemenu_active="text-white")

@app.route('/agents')
def agents():
    return render_template('/agents/index.html', title="Agents", home_active="text-red-500", agents_active="text-white")

if __name__ == '__main__':
    app.run()
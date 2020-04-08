from flask import Flask,render_template

from registration_validate import user_reg
from list_user_conn import user_reg1
from login import login_reg


app = Flask(__name__)
app.register_blueprint(user_reg)
app.register_blueprint(user_reg1)
app.register_blueprint(login_reg)
@app.route('/')
def index():
    return render_template('home.html')


app.run(debug=True)
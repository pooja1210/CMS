from flask import Flask, Blueprint, render_template


admin1_reg = Blueprint('admin1_reg',__name__)

@admin1_reg.route('/admin_dashboard' )
def admin():
    return render_template('index.html')


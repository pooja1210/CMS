from flask import Flask,render_template, request
from login import login_reg
from fun import result_front, cat_img
from admin_login import admin_login_reg
from list_user_conn import user_reg1
from registration_validate import user_reg
from add_category import  cat_manager
from article_manager import article_manager_reg
from slider_manager import sld_manager
from page_manager import page_manager
from contact_us import contact_manager
from user_article import user_article_reg

import country_database
app = Flask(__name__)

app.register_blueprint(login_reg)
app.register_blueprint(user_reg)
app.register_blueprint(cat_manager)
app.register_blueprint(article_manager_reg)
app.register_blueprint( admin_login_reg)
app.register_blueprint(user_reg1)
app.register_blueprint(sld_manager)
app.register_blueprint(page_manager)
app.register_blueprint(contact_manager)
app.register_blueprint(user_article_reg)


'''app.secret_key = os.urandom(12)'''
app.secret_key = "b'\x95\x12Y\x97\xcd\x07>\x00J\xcc\x91\x17'"

@app.route('/home')
def home():
    art_result = result_front(' article_manager')
    return render_template('home.html',  art_result =  art_result )
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')
@app.route('/')
def foo():
    result=""
    myresult=""
    art_result=""
    result = result_front('slider_manager')
    myresult = cat_img('category_manager')
    art_result= result_front(' article_manager')


    print(result)


    return render_template('foo.html',result=result_front('slider_manager'),  my_result= myresult, art_result=art_result)
@app.route('/about')
def about():
    art_result = result_front(' article_manager')
    return render_template('about.html', art_result=art_result)

@app.route('/contact_food')
def contact_food():
    art_result = result_front(' article_manager')
    return render_template('contact.html', art_result=art_result)






app.run(debug=True)


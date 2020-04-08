from flask import Flask, Blueprint, render_template, flash, redirect, url_for, send_from_directory
from datetime import  datetime
import country_database


import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = ('upload_img/cat_img')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cat_manager1 = Blueprint('cat_manager1',__name__)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS





@cat_manager1.route('/add_cat',  methods=['GET', 'POST'])
def add_category():
    error = {}
    val = {}
    if request.method== 'POST':


        title = request.form['title']

        if title=='':
            error['t_er']="no title"
        val['title']= title

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("================")
            print(filename)
            print("===============")
            return redirect(url_for('uploaded_file', filename=filename))

        else:
            error['file_upload_error'] = "Image is not selected"





        if len(error) !=0:
            return render_template('add_category.html', error=error)
        else:
            try:
                print("hellooo this coming")
                country_database.connects()
                sql = "INSERT INTO category_manager(title, image, created_date, modified_date) VALUES (%s, %s, %s, %s)"
                print("hellooo this coming")
                print("i am after sql")
                value = (title,  str(datetime.now()), str(datetime.now()))


                print(title)
                country_database.cur.execute(sql,value)
                country_database.conn.commit()

            except:
                country_database.conn.rollback()
            finally:
                country_database.conn.close()
    else:
        return render_template('add_category.html', error=error , val = val)
    return  render_template('login.html')



@cat_manager1.route('/cat_list',  methods=['GET', 'POST'])
def cat_list():
    result_cat_list=""
    try:
        country_database.connects()
        sql="SELECT * from category_manager"
        country_database.cur.execute(sql)
        result_cat_list = country_database.cur.fetchall()
        country_database.conn.commit()
        print(result_cat_list)
    except:
        country_database.conn.rollback()
    finally:
        country_database.conn.close()
    return render_template('category_list.html', result_cat_list = result_cat_list)





@cat_manager1.route('/upload_img/cat_img/<filename>')
def upload_img(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


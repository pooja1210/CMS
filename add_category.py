import os
from datetime import datetime
from math import ceil

import country_database
from flask import Flask, Blueprint, render_template, flash, redirect, url_for, send_from_directory, json, request
from fun import delete, allowed_file, slugify,allowed_file
from werkzeug.utils import secure_filename


cat_manager = Blueprint('cat_manager',__name__)
cat = Flask(__name__)
UPLOAD_FOLDER = os.path.expandvars('./upload_img/cat_img')
cat.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@cat_manager.route('/add_cat',  methods=['GET', 'POST'])
def add_category():
    error = {}
    val = {}
    if request.method== 'POST':


        title = request.form['title']
        t=slugify(title)

        if title=='':
            error['t_er']="no title"
        val['title']= title

        file_upload=""
        img_upload=""
        if request.files:
            # file_upload = request.files['image']


            fileupload = request.files['image']
            if fileupload and allowed_file(fileupload.filename):
                    filename = secure_filename(fileupload.filename)

                    fileupload.save(os.path.join(cat.config['UPLOAD_FOLDER'], filename))
                    image=fileupload.filename
        else:
            error['as']="image not selected"






        if request.files:
            file_upload = request.files['image']

        else:
            error['file_upload_error'] = "Image is not selected"
        if file_upload:
            new_file = file_upload.filename.split('.')
            file_upload.filename = "image"+str(datetime.now())+"."+ new_file[-1]

            img_upload= file_upload.filename

            f= os.path.join(cat.config['UPLOAD_FOLDER'], file_upload.filename)
            file_upload.save(f)

            print(f)

        if len(error) !=0:
            return render_template('add_category.html', error=error)
        else:
            try:
                print("hellooo this coming")
                country_database.connects()
                t=slugify(title)
                sql = "INSERT INTO category_manager(title, image, created_date, modified_date) VALUES (%s, %s, %s, %s)"
                print("hellooo this coming")
                print("i am after sql")
                value = (t, img_upload, str(datetime.now()), str(datetime.now()))
                if 'ch' in request.form and request.form['ch'] =='on':
                    delete(cat.config['UPLOAD_FOLDER'], img_upload)


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



@cat_manager.route('/cat_list',  methods=['GET', 'POST'])
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





@cat_manager.route('/upload_img/cat_img/<filename>')
def upload_img(filename):
    return send_from_directory(cat.config['UPLOAD_FOLDER'], filename)




cat_manager = Blueprint('cat_manager',__name__)
cat = Flask(__name__)
UPLOAD_FOLDER = os.path.expandvars('upload_img/cat_img')
cat.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@cat_manager.route('/add_cat',  methods=['GET', 'POST'])
def add_category():
    error = {}
    val = {}
    if request.method== 'POST':


        title = request.form['title']
        print("here $$$$", title)
        t=slugify(title)

        if title=='':
            error['t_er']="no title"
        val['title']= title

        file_upload=""
        img_upload=""
        if request.files:
            file_upload = request.files['image']

        else:
            error['file_upload_error'] = "Image is not selected"
        if file_upload:
            new_file = file_upload.filename.split('.')
            file_upload.filename = "image"+str(datetime.now())+"."+ new_file[-1]

            img_upload= file_upload.filename

            f= os.path.join(cat.config['UPLOAD_FOLDER'], file_upload.filename)
            file_upload.save(f)

            print(f)

        if len(error) !=0:
            return render_template('add_category.html', error=error)
        else:
            try:
                print("hellooo this coming")
                country_database.connects()
                sql = "INSERT INTO category_manager(title, image, created_date, modified_date) VALUES (%s, %s, %s, %s)"
                print("hellooo this coming")
                print("i am after sql")
                value = (t, img_upload, str(datetime.now()), str(datetime.now()))


                print(title)
                country_database.cur.execute(sql,value)
                country_database.conn.commit()
                return redirect(url_for('cat_manager.cat_list'))
            except:
                country_database.conn.rollback()
            finally:
                country_database.conn.close()
    else:
        return render_template('add_category.html', error=error , val = val)
    return redirect(url_for('cat_manager.cat_list'))



@cat_manager.route('/cat_list',  methods=['GET', 'POST'])
def cat_list():
    result_cat_list=""
    result_ordering=""
    try:


        page = request.args.get('page')
        print("page",page)

        country_database.connects()

        sql="SELECT count(id) from category_manager"
        country_database.cur.execute(sql)
        total_row = country_database.cur.fetchall()
        print("total row")
        print(total_row)
        no_of_row = total_row[0]['count(id)']
        page_size = 3
        total_page = ceil(no_of_row / page_size)
        starting_row = page_size * int(page)
        country_database.cur.execute("SELECT * FROM category_manager LIMIT " + str(page_size) + " OFFSET " + str(starting_row))



        result_cat_list = country_database.cur.fetchall()
        country_database.conn.commit()
        print(result_cat_list)
    except:
        country_database.conn.rollback()
    finally:
        country_database.conn.close()
    return render_template('category_list.html', result_cat_list = result_cat_list,total_page=total_page)





@cat_manager.route('/upload_img/cat_img/<filename>')
def upload_img(filename):
    return send_from_directory(cat.config['UPLOAD_FOLDER'], filename)


# @cat_manager.route('/upload_img/cat_img/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(cat.config['UPLOAD_FOLDER '], filename)





@cat_manager.route('/delete_cat')
def cat_list_delete():
    print("here")
    try:
        id=request.args.get('idi')
        print("here")
        print(id)
        country_database.connects()
        sql= "delete from category_manager where id = %s"
       
        print("sqlllllllll")

        val=(id,)
        print(val)
        country_database.cur.execute(sql,val)

        country_database.conn.commit()
    except Exception as err:
        print(err)
        country_database.conn.rollback()
    finally:
        country_database.conn.close()
    flash('Data deleted successfully!')
    return json.dumps({"type": "success"})





@cat_manager.route('/edit', methods=['GET', 'POST'])
def edit():
    error={}
    result1= ""
    fo=""
    try:
        result1 = None
        country_database.connects()
        id=request.args.get('id')
        sql1 ="SELECT * from category_manager where id=%s"
        val=(id,)
        country_database.cur.execute(sql1,val)
        result1=country_database.cur.fetchone()

        fo=result1['image']

        country_database.commit()
    except:
        country_database.conn.rollback()
    finally:
        country_database.conn.close()

    if request.method == 'POST':

        flag=0
        file=''
        val=""
        id = request.args.get('id')

        title = request.form['title']

        if request.files:
            file=request.files['image']
            if file and allowed_file(file.filename):

                filename = secure_filename(file.filename)


                file.save(os.path.join(cat.config['UPLOAD_FOLDER'], filename))

                flag = 1

        if len(error)==0:

            try:
                if flag==0:
                    print("here flag 0")
                    country_database.connects()
                    t=slugify(title)
                    if 'ch' in request.form and request.form['ch'] == 'on':
                        print("dsfguydfgjsdgf")
                        os.remove(cat.config['UPLOAD_FOLDER']+ "/" + fo)
                    id= request.args.get('id')
                    sql="UPDATE category_manager SET title=%s, modified_date=%s WHERE id=%s"
                    val=(t,str(datetime.now()), id)
                    country_database.cur.execute(sql,val)
                    country_database.conn.commit()
                    return redirect(url_for('cat_manager.cat_list'))
                if flag==1:
                    print("here flag 1")
                    country_database.connects()
                    t = slugify(title)
                    t=slugify(t)
                    if 'ch' in request.form and request.form['ch']== 'on':
                        print("dsfguydfgjsdgf")
                        os.remove(fo + "/" + filename)
                    sql = "UPDATE category_manager SET title=%s,image=%s, modified_date=%s WHERE id=%s"
                    val = (t, file.filename, str(datetime.now()), id)
                    print(title)

                    print(val)
                    country_database.cur.execute(sql, val)
                    country_database.conn.commit()
                    return redirect(url_for('cat_manager.cat_list'))


            except Exception as err:
                print(err)
                country_database.conn.rollback()
            finally:
                print("ufgdui")
                country_database.conn.close()
    return render_template('cat_list_edit.html', result1=result1)




















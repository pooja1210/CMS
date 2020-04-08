from flask import Flask, Blueprint, render_template,request, send_from_directory, json, session, redirect, url_for,flash
import country_database
# from fun import allowed_file
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from fun import *
# from fun import result_front, cat_img
user_article_reg = Blueprint('user_article_reg',__name__)
art = Flask(__name__)
UPLOAD_FOLDER = os.path.expandvars('./upload_img/art_img')
art.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@user_article_reg.route('/user_add_article', methods=['GET', 'POST'])
def add_article():
    print("hello")
    error = {}
    val={}
    myresult = ""
    file_upload = ""
    user_id = session['user']['id']
    print("user_id", user_id)
    UnPublish="UnPublish"
    img_upload=""
    try:
        country_database.connects()
        sql = "SELECT * FROM category_manager "
        country_database.cur.execute(sql)
        myresult = country_database.cur.fetchall()

    except:
        country_database.conn.rollback()
    finally:
        country_database.conn.close()
    if request.method == "POST":

        title = request.form['title']

        slug = request.form['title']
        s = slugify(slug)

        description = request.form['summernote']
        status = UnPublish
        print("status",status)

        cat_id = request.form['cat_id']
        val['title'] = title
        val['desc']= description
        val['cat_id']= cat_id
        print(val['title'])
        print(val['desc'])
        print(val['cat_id'])

        if title == "":
            error['tt'] = "Title is required"
        if cat_id == " ":
            error['b'] = "Select Category"
        if description == "":
            error['c'] = "Enter some description"



        if request.files:
            # file_upload = request.files['image']
            print("hello")
            file_upload = request.files['image']
            print(file_upload)
        else:
            error['as'] = "image not selected"
        if file_upload:
            new_file = file_upload.filename.split('.')
            file_upload.filename = "image" + str(datetime.now()) + "." + new_file[-1]

            img_upload = file_upload.filename

            f = os.path.join(art.config['UPLOAD_FOLDER'], file_upload.filename)
            file_upload.save(f)
        if len(error)==0:

            try:


                country_database.connects()
                t = datetime.now()

                y = t.strftime("%y") + "-" + t.strftime("%b") + "-" + t.strftime("%d")

                s = slugify(slug)
                sql = "insert into article_manager(title,slug,description,file,category_id ," \
                      "status ,created_date,modified_date,user_id)" \
                      " value(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (title, s, description, img_upload, cat_id, status, t, t,user_id)
                print(val)

                country_database.cur.execute(sql, val)
                country_database.conn.commit()
                flash('Article has been added successfully!')
                return redirect(url_for('user_article_reg.user_list_article'))





            except Exception as err:
                print(err)
                country_database.conn.rollback()
            finally:
                country_database.conn.close()

    return render_template('/frontend/article/user_add_article.html', myresult=myresult, error=error, val=val)


@user_article_reg.route('/get_title', methods=['POST', 'GET'])
def check_title():
    record =''
    title = request.args.get('eml')

    val = (title, )
    print(val)
    try:
       country_database.connects()
       sql ="SELECT * FROM article_manager where title=%s"
       country_database.cur.execute(sql, val)
       record = country_database.cur.fetchone()
       print("sql value is", sql)
       print("val value is", val)
       print(record)
    except:
        country_database.conn.rolback()
    finally:
        country_database.conn.close()
    return json.dumps({"type": "check_title", "record": record})

@user_article_reg.route('/user_list_article')
def user_list_article():
    result = result_front('slider_manager')

    try:
        id=request.args.get('id')
        country_database.connects()
        sql = "select * from article_manager where user_id = %s"
        val = (session['user']['id'],)
        print("val value is", val)
        country_database.cur.execute(sql, val)
        record = country_database.cur.fetchall()
        print("ghdfs", result)
        country_database.conn.commit()


    except Exception as err:
        print(err)
        country_database.conn.rollback()
    finally:
        country_database.conn.close()


    return render_template('/frontend/article/user_list_article.html', result=result, record=record)

@user_article_reg.route('/user_edit_article', methods=['GET', 'POST'])
def user_edit_article():

    myresult=""
    val={}
    file=""
    error={}
    record=""
    oldimage=""
    user_id = session['user']['id']
    print("user_id", user_id)
    UnPublish = "UnPublish"
    id = request.args.get('id')

    record=''
    try:
        country_database.connects()
        sql = "SELECT * FROM category_manager "
        country_database.cur.execute(sql)
        myresult = country_database.cur.fetchall()
        country_database.conn.commit()
        print(myresult)


        sql="SELECT * from article_manager WHERE  id = %s"
        val=(id,)
        country_database.cur.execute(sql,val)

        record=country_database.cur.fetchone()
        print("record is",record)
        print("cat_title",record['category_id'])
        oldimage=record['file']
        country_database.conn.commit()
    except:
        country_database.conn.rollback()
    finally:
        country_database.conn.close()
    if request.method=='POST':
        flag=0

        title = request.form['title']
        slug = request.form['title']
        s = slugify(slug)
        print(s)
        description = request.form['summernote']
        status = UnPublish

        cat_id = request.form['cat_id']

        if title=="":
            error['ti']="title is required"

        if description=='':
            error['de_er']="description is required"
        print("erro is",error)
        if request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                file.save(os.path.join(art.config['UPLOAD_FOLDER'], filename))


                flag = 1
        if len(error)==0:

            if flag==1:
                try:
                    print("here is flag 1")
                    country_database.connects()



                    sql="UPDATE article_manager SET title=%s,slug=%s, description=%s, file=%s, category_id=%s,"\
                         "status=%s, modified_date=%s, user_id=%s where id=%s"
                    val=(title,s,description,file.filename, cat_id, status, str(datetime.now()),user_id,id)
                    print("val value is",val)
                    country_database.cur.execute(sql,val)
                    country_database.conn.commit()
                    flash('Article has been updated successfully!')
                    return redirect(url_for('user_article_reg.user_list_article'))
                except Exception as err:
                    print(err)
                    country_database.conn.rollback()
                finally:
                    country_database.conn.close()
                flash('Article has been updated successfully!')

            else:
                try:
                    country_database.connects()

                    if 'pt' in request.form and request.form['pt'] == 'on':
                        print("file%%%",oldimage)
                        os.remove(art.config['UPLOAD_FOLDER'] + "/" + oldimage)


                    sql = "UPDATE article_manager SET title=%s, slug=%s, description=%s, category_id=%s," \
                          " status=%s, modified_date=%s,user_id=%s where id=%s"
                    val = (title,s,description, cat_id, status,str(datetime.now()),user_id, id,)
                    print("val is in flag o side", val)


                    country_database.cur.execute(sql, val)
                    country_database.conn.commit()
                    flash('Article has been updated successfully!')
                    return redirect(url_for('user_article_reg.user_list_article'))


                except Exception as err:
                    print(err)
                    country_database.conn.rollback()
                finally:
                    country_database.conn.close()






    return render_template('/frontend/article/user_list_edit_article.html',val=val, record=record, myresult=myresult, error=error)

@user_article_reg.route('/user_delete_article', methods=['GET', 'POST'])
def user_delete_article():

    print("in delete article")
    id=request.args.get('idi')
    print("here is your id", id)
    try:

        country_database.connects()
        sql = "DELETE FROM article_manager WHERE id=%s"
        val=(id,)
        country_database.cur.execute(sql,val)
        country_database.conn.commit()
    except Exception as err:
        print(err)
        country_database.conn.rollback()
    finally:
        country_database.conn.close()
    flash('Article has been deleted successfully!')
    return json.dumps({"type": "success"})






@user_article_reg.route('/upload_img/art_img/<filename>')
def get_article__image_path(filename):
    return send_from_directory(art.config['UPLOAD_FOLDER'], filename)





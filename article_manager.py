from flask import Flask, Blueprint, render_template,request, send_from_directory, json, session, redirect, url_for,flash
from fun import allowed_file
import country_database
from werkzeug.utils import secure_filename
from datetime import datetime
from fun import slugify, deleted, allowed_file

import os
from fun import result_front, cat_img

article_manager_reg = Blueprint('article_manager_reg',__name__)


art = Flask(__name__)
UPLOAD_FOLDER = os.path.expandvars('./upload_img/art_img')
art.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print("start")


@article_manager_reg.route('/article_manager', methods=['GET', 'POST'])
def add_article():
    error={}
    myresult=""
    fileupload=""
    user_id = session['user']['id']
    print(user_id)
    try:
        country_database.connects()
        sql = "SELECT * FROM category_manager "
        country_database.cur.execute(sql)
        myresult = country_database.cur.fetchall()

    except:
        country_database.conn.rollback()
    finally:
        country_database.conn.close()


    if request.method=="POST":

        title = request.form['title']

        slug=request.form['title']
        s = slugify(slug)
        print(s)
        description = request.form['summernote']
        status = request.form['ck']

        cat_id = request.form['cat_id']

        if title=="":
            error['tt']="title is required"
        if slug=="":
             error['b']="slug is required"
        if description=="":
            error['c'] = "please enter some description"

        if cat_id=='':
            error['e']="select category id"

        print(request.files)
        if request.files:
            # file_upload = request.files['image']


            fileupload = request.files['image']
            if fileupload and allowed_file(fileupload.filename):
                    filename = secure_filename(fileupload.filename)

                    fileupload.save(os.path.join(art.config['UPLOAD_FOLDER'], filename))
                    image=fileupload.filename
        else:
            error['as']="image not selected"
        



        try:
            country_database.connects()
            t = str(datetime.now())

            # y = t.strftime("%y") + "-" + t.strftime("%b") + "-" + t.strftime("%d")
            print("here is date time format")

            print(user_id)
            s=slugify(slug)
            sql = "insert into article_manager(title,slug,description,file,category_id ," \
                  "status ,created_date,modified_date,user_id)" \
                  " value(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val=(title, s, description,image,cat_id,status, t,t,user_id,)
            print(val)
            # user_id=session['user'['id']]

            country_database.cur.execute(sql,val)
            country_database.conn.commit()
            return redirect(url_for('article_manager_reg.list_article'))



        except Exception as err:
            print(err)
            country_database.conn.rollback()
        finally:
            country_database.conn.close()

    return render_template("article_manager.html", error=error,myresult=myresult)
@article_manager_reg.route('/article_manager/article_manager_list', methods=['GET', 'POST'])
def list_article():

    record=""
    try:

        country_database.connects()

        sql="SELECT * from article_manager"
        country_database.cur.execute(sql)
        record=country_database.cur.fetchall()
        print(record)


        for i in record:
             t=(i['modified_date'])
             x=(i['description'])
             u=x.split()
             v=u[0:10]
             s = ' '.join(v)
             y = t.strftime("%y") + "-" + t.strftime("%b") + "-" + t.strftime("%d")
             print(y)
             print(s)




        print(record.modified_date())

        country_database.conn.commit()
    except:
        country_database.conn.rollback()
    finally:
        country_database.conn.close()
    return render_template('article_manager_list.html', record=record, y=y, s=s)


@article_manager_reg.route('/delete_article', methods=['GET', 'POST'])
def delete_article():

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

@article_manager_reg.route('/edit_article', methods=['GET', 'POST'])
def edit_article():

    myresult=""
    files=""
    error={}
    record=""
    oldimage=""
    id = request.args.get('id')

    record=''
    try:
        print("fsdijdfsjidfsj")
        country_database.connects()
        sql = "SELECT * FROM category_manager "
        country_database.cur.execute(sql)
        myresult = country_database.cur.fetchall()
        country_database.conn.commit()


        sql="SELECT * from article_manager WHERE  id =%s"
        val=(id,)
        country_database.cur.execute(sql,val)

        record=country_database.cur.fetchone()
        print("record ffff", record)
        print("$$$$$$$",record['category_id'], record['id'])
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
        description = request.form['decs']
        status = request.form['ck']

        cat_id = request.form['cat_id']
        if title=="":
            error['ti']="title is required"

        if description=='':
            error['de_er']="description is required"
        if request.files:
            files = request.files['image']
            if files and allowed_file(files.filename):
                filename = secure_filename(files.filename)

                files.save(os.path.join(art.config['UPLOAD_FOLDER'], filename))


                flag = 1
        if len(error)==0:

            if flag==1:
                try:
                    print("here is flag 1")
                    country_database.connects()

                    # os.remove(art.config['UPLOAD_FOLDER'] + "/" + oldimage)
                    print("here is flag 2")
                    sql="UPDATE article_manager SET title=%s,slug=%s, description=%s, file=%s, category_id=%s,"\
                         "status=%s, modified_date=%s where id=%s"
                    val=(title,s,description,files.filename, cat_id, status, str(datetime.now()),id,)
                    print("val is",val)
                    country_database.cur.execute(sql,val)
                    country_database.conn.commit()
                    flash('Article has been updated successfully!')
                    return redirect(url_for('article_manager_reg.list_article'))
                except Exception as err:
                    print(err)
                    country_database.conn.rollback()
                finally:
                    country_database.conn.close()
                flash('Article has been updated successfully!')
                return render_template('article_manager_list_edit.html', record=record, myresult=myresult, error=error)
            else:
                try:
                    country_database.connects()

                    if 'pt' in request.form and request.form['pt'] == 'on':
                        print("file%%%",oldimage)
                        os.remove(art.config['UPLOAD_FOLDER'] + "/" + oldimage)


                    sql = "UPDATE article_manager SET title=%s, slug=%s, description=%s, category_id=%s," \
                          " status=%s, modified_date=%s where id=%s"
                    val = (title,s,description, cat_id, status,str(datetime.now()), id,)
                    print("val is in flag o side", val)


                    country_database.cur.execute(sql, val)
                    country_database.conn.commit()
                    flash('Article has been updated successfully!')
                    return redirect(url_for('article_manager_reg.list_article'))


                except Exception as err:
                    print(err)
                    country_database.conn.rollback()
                finally:
                    country_database.conn.close()






    return render_template('article_manager_list_edit.html', record=record, myresult=myresult, error=error)












@article_manager_reg.route('/upload_img/art_img/<filename>')
def get_article__image_path(filename):
    return send_from_directory(art.config['UPLOAD_FOLDER'], filename)





@article_manager_reg.route('/get_title', methods=['POST', 'GET'])
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





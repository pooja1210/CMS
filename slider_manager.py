from flask import Flask, flash, request, redirect, url_for, Blueprint,render_template, send_from_directory, json
import country_database
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from fun import delete, allowed_file, slugify
sld_manager = Blueprint('sld_manager', __name__)
UPLOAD_FOLDER = os.path.expandvars('./upload_img/slider_img')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
sld = Flask(__name__)

sld.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@sld_manager.route('/slider_manager', methods=['POST', 'GET'])
def add_slider():
    val=""
    error=""
    fileupload=""
    if request.method=='POST':

            title=request.form['title']
            ck = request.form['ck']


            if title=="":
               error['a']="title is required"
            if request.files:
                fileupload = request.files['image']
                if fileupload and allowed_file(fileupload.filename):
                    filename = secure_filename(fileupload.filename)

                    fileupload.save(os.path.join(sld.config['UPLOAD_FOLDER'], filename))
                    image=fileupload.filename

            else:
                error['im'] = "Images is empty"
            if len(error)==0:
                try:
                    country_database.connects()
                    sql="insert into slider_manager(title,image,status," \
                              "created_date,modified_date)" \
                              " value(%s,%s,%s,%s,%s)"
                    val=(title,image,ck,str(datetime.now()),str(datetime.now()))
                    print(val)
                    country_database.cur.execute(sql,val)
                    country_database.conn.commit()
                    update_query()
                    return redirect(url_for('sld_manager.sld_list'))


                except Exception as err:
                    print(err)
                    country_database.conn.rollback()
                finally:
                    country_database.conn.close()
            return render_template('slider_manager.html', error=error, val=val)
    return render_template('slider_manager.html')
@sld_manager.route('/slider_manager_list')
def sld_list():
    try:
        country_database.connects()
        sql="SELECT * FROM slider_manager  ORDER BY order_id ASC"
        country_database.cur.execute(sql)
        record=country_database.cur.fetchall()

        country_database.conn.commit()
    except:
        country_database.conn.rollback()
    finally:
        country_database.conn.close()
    return render_template("slider_manager_list.html", record=record)
@sld_manager.route('/delete_slider')
def sld_delete():
    print("here")
    try:
        id=request.args.get('idi')
        print(id)
        country_database.connects()
        sql= "delete from slider_manager where id = %s"
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
    flash('Slider has been deleted successfully!')
    return json.dumps({"type": "success"})


@sld_manager.route('/edit_slider', methods=['POST', 'GET'])
def slider_edit():
    record={}
    old_image = ''
    error=""
    try:
        print("in edit")
        id = request.args.get('id')

        print(id)
        country_database.connects()
        flag=0
        sql="SELECT * FROM  slider_manager where id=%s"
        val=(id,)
        print(val)
        country_database.cur.execute(sql,val)
        record=country_database.cur.fetchone()
        old_image=record['image']
        print(record)

        country_database.conn.commit()
    except Exception as err:
        print(err)
        country_database.conn.rollback()
    finally:
        country_database.conn.close()
    if request.method=="POST":
        title=request.form['title']
        ck=request.form['ck']
        if title=="":
            error['a']="title required"
        if request.files:
            fileupload=request.files['image']
            filename = secure_filename(fileupload.filename)

            fileupload.save(os.path.join(sld.config['UPLOAD_FOLDER'], filename))
            image = fileupload.filename
            flag=1

        if  flag==0:
            print("in flag 0")
            try:
                country_database.connects()
                sql="UPDATE slider_manager set title=%s, status=%s," \
                     "modified_date=%s where id=%s"
                val = (title, ck, str(datetime.now()), id,)
                if 'pt' in request.form and request.form['pt'] == 'on':
                    os.remove(sld.config['UPLOAD_FOLDER'] + "/" + old_image)
                    print("pt is on")
                    print(sld.config['UPLOAD_FOLDER'])
                    print(old_image)


                country_database.cur.execute(sql,val)
                country_database.conn.commit()
            except Exception as err:
                print(err)
                country_database.conn.rollback()
            finally:
                country_database.conn.close()
            flash('Slider has been updated successfully!')
            return redirect(url_for('sld_manager.sld_list'))
        else:
            try:
                print("in flag 1")
                country_database.connects()
                sql =  "update slider_manager set title=%s ,image=%s, status=%s, " \
                            "modified_date=%s where id=%s"
                val = (title,image, ck, str(datetime.now()), id,)
                print(val)

                country_database.cur.execute(sql, val)
                country_database.conn.commit()
            except Exception as err:
                print(err)
                country_database.conn.rollback()
            finally:
                country_database.conn.close()
            flash('Slider has been updated successfully!')
            return redirect(url_for('sld_manager.sld_list'))








    return render_template('slider_manager_list_edit.html', record=record)









def update_query():
    result=""
    count=0
    try:
        country_database.connects()
        sql = "SELECT * FROM slider_manager ORDER BY order_id ASC"
        country_database.cur.execute(sql)
        result =country_database.cur.fetchall()
        for row in result:
            count= count+1
            sql = "UPDATE slider_manager SET order_id=%s WHERE id=%s"
            val=(str(count),row['id'],)
            country_database.cur.execute(sql, val)
            country_database.conn.commit()
    except Exception as err:
        print(err)
        country_database.conn.rollback()

    finally:
        country_database.conn.close()
    return True


@sld_manager.route('/slider_order', methods=['POST', 'GET'])
def ordering_list():
    id = request.args.get('id')
    action = request.args.get('action')
    order = request.args.get('order')
    oder_step = ""
    print(id,order,action)
    try:
        country_database.connects()
        if action == 'up':
            oder_step = str(float(order) - 1.5)

        else:
            oder_step = str(float(order) + 1.5)

        sql = "UPDATE slider_manager SET order_id=%s WHERE id=%s"
        val = (oder_step, id,)
        country_database.cur.execute(sql, val)
        country_database.conn.commit()
        update_query()

    except Exception as err:
        print(err)
        country_database.conn.rollback()
    finally:
        country_database.conn.close()

    return json.dumps({"type": "error"})













@sld_manager.route('/upload_img/slider_img/<filename>')
def get_article__image_path(filename):
    print("get image");
    print(filename);
    return send_from_directory(sld.config['UPLOAD_FOLDER'], filename)













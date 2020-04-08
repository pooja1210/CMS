from flask import Flask, flash, request, redirect, url_for, Blueprint,render_template, send_from_directory, json
import country_database
from datetime import datetime
from fun import result_front, cat_img
from fun import  slugify
page_manager = Blueprint('page_manager', __name__)

@page_manager.route('/add_page', methods=['POST', 'GET'])
def add_page():

error={}
if request.method=='POST':
title=request.form['title']

slug=request.form['slug']
s=slugify(slug)

decs=request.form['decs']
if title=="":
error['a']="title is required"
if decs=="":
error['b']="description is required"

if len(error)==0:

try:
country_database.connects()

sql="INSERT INTO page_manager (title, slug, description) VALUES(%s, %s, %s)"
val=(title,s, decs,)

country_database.cur.execute(sql,val)
country_database.conn.commit()
return redirect(url_for('page_manager.list_page'))
except Exception as err:
print(err)
country_database.conn.rollback()
finally:
country_database.conn.close()


return render_template('page_manager.html')

@page_manager.route('/list_page')
def list_page():
record=""
try:
country_database.connects()
sql="Select * from page_manager"
country_database.cur.execute(sql)
record=country_database.cur.fetchall()

country_database.conn.commit()
except Exception as err:
country_database.conn.rollback()
finally:
country_database.conn.close()
return render_template('page_manager_list.html', record=record)
@page_manager.route('/delete_page')
def delete_page():
try:
id=request.args.get('idi')
print(id)
country_database.connects()
sql = "delete from page_manager where id = %s"
# sql = "delete from page_manager where id = %s"
val=(id,)
country_database.cur.execute(sql,val)
country_database.conn.commit()
except Exception as err:
print(err)
country_database.conn.rollback()
finally:
country_database.conn.close()
flash('Content deleted successfully')
return json.dumps({"type": "success"})

@page_manager.route('/edit_page', methods=['POST', 'GET'])
def edit_page():

myresult = ''
id = request.args.get('id')
print("before")
print(id)
try:
country_database.connects()
sql = "SELECT * FROM page_manager  WHERE  id =%s"
val = (id, )
country_database.cur.execute(sql,val)
record = country_database.cur.fetchone()

except Exception as err:
print(err)
country_database.conn.rollback()
finally:
country_database.conn.close()
print("end select")

error = {}
if request.method == 'POST':
print('entry post')
title = request.form['title']
decs = request.form['decs']
slug = request.form['slug']
s = slugify(slug)
print("here is slug",s)


if title == "":
error['h'] = "Title is empty"

if decs == "":
error['decs'] = "Description is empty"

if slug== "":
error['slug'] = "Slug is empty"

if len(error) == 0:
print('entry without error')

try:

country_database.connects()
print('try')
print(id)
sql = "update page_manager set title=%s , slug=%s, description=%s where id = %s"

val = (title, s, decs,  id)
print("val is",val)

country_database.cur.execute(sql, val)
country_database.conn.commit()

flash('Page has been Updated successfully!')
return redirect(url_for('page_manager.list_page'))
except Exception as err:
print(err)
country_database.conn.rollback()
finally:
country_database.conn.close()

return render_template('page_manager_list.html'
, error=error, record=record)
return render_template('page_manager_edit.html'
, error=error, record=record)

@page_manager.route('/')
def logout_page():
result = ""
myresult = ""
art_result = ""
result = result_front('slider_manager')
myresult = cat_img('category_manager')
art_result = result_front(' article_manager')
return render_template('foo.html',result=result_front('slider_manager'),  my_result= myresult, art_result=art_result)






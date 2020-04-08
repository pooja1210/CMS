import mysql.connector
from flask import Flask, render_template,request,json,Blueprint, request, redirect,flash,url_for
import country_database

from fun import *
import hashlib
user_reg1 = Blueprint('user_reg1',__name__)
from math import ceil


@user_reg1.route('/first')
def first():
    val={}
    record1 = ""
    record2=""
    try:
        print("hello")
        country_database.connects()
        country_database.cur.execute("SELECT * FROM form")
        record1 = country_database.cur.fetchall()
        print("jdfk")

        country_database.conn.commit()

    except Exception as err:
        print(err)
        country_database.conn.rollback()
    finally:
        country_database.conn.close()
    return render_template('list_user.html', record1 = record1)


@user_reg1.route('/delete', methods=['GET','POST'])
def delete():
    try:
        user = request.args.get('em')
        country_database.connects()
        sql = "DELETE FROM form WHERE email=%s"
        val=(user,)
        country_database.cur.execute(sql,val)
        country_database.conn.commit()
    except Exception as err:
        print('err',err)
        country_database.conn.rollback()
    finally:
        country_database.conn.close()
    return json.dumps({'type': 'success'})

@user_reg1.route('/edit_list', methods=['GET', 'POST'])
def edit_list():
    error={}
    result = ""
    result1= ""
    if request.method=='GET':
        try:
            result1 = None

            country_database.connects()
            sql="SELECT *  from countries "
            country_database.cur.execute(sql)
            result=country_database.cur.fetchall()
            print(result)
            country_database.conn.commit()
            id=request.args.get('id')

            sql1 ="SELECT * from form where id=%s"
            val=(id,)
            country_database.cur.execute(sql1,val)
            result1=country_database.cur.fetchone()
            print(result1)
            country_database.commit()

        except:
            country_database.conn.rollback()
        finally:
            country_database.conn.close()


    if request.method == 'POST':
        flag = 0
        print('pooja')
        first = request.form['fname']
        last = request.form['lname']
        user = request.form['user']
        email = request.form['email']
        number = request.form['number']
        password = request.form['pwd']
        con_password = request.form['conpwd']
        country = request.form['cnm']
        city = request.form['cinm']
        state = request.form['snm']
        zip = request.form['znm']


        print(first)
        if first == "":
            error['f'] = "first name is required"
            print("vfdiugviv")
        if last == "":
            error['l'] = "last name is required"
        if user == "":
            error['us'] = "username required"

        if number == "":
            error['n'] = "phone number is required"
        if password is not "":
            if len(password) < 6:
                error['psw'] = "Password must be at least 6 characters"
            else:


                if lower_error(password) is None:
                    error['lowp'] = "Password should have lower case letter"
                if uppercase_error(password) is None:
                    error['upp'] = "Password should have upper case"
                if symbol_error(password) is None:
                    error['srr'] = "Password should have one special character"
                if digit_error(password) is None:
                    error['dp'] = "Password should have at least one digit"
                flag=1
        if country == "":
            error['cou'] = "country is required"
        if city == "":
            error['cit'] = "cit is required"
        if state == "":
            error['sta'] = "state is required"
        if zip == "":
            error['sta'] = "zip is required"
        print(len(error))
        if len(error)==0:
            try:
                print(first)
                country_database.connects()
                if flag==1:

                    print("loist nusers file")
                    id=request.args.get('id')
                    print(id)
                    p = password
                    h = hashlib.md5(p.encode())
                    h1 = h.hexdigest()
                    print("srmcem lko")
                    print(h1)
                    sql = "UPDATE form set first=%s, last=%s, number=%s, password=%s ,country=%s," \
                          " city=%s, state=%s,  zip=%s where id=%s"
                    val = (first, last,number,h1,country, city, state, zip, id,)
                    print(val)
                    country_database.cur.execute(sql, val)

                    print(val)
                    country_database.conn.commit()
                    #flash('Updated ')
                    return redirect(url_for('user_reg1.first'))
                else:
                    id = request.args.get('id')
                    print(id)
                    p = password
                    h = hashlib.md5(p.encode())
                    h1 = h.hexdigest()
                    print("srmcem lko")
                    print(h1)
                    sql = "UPDATE form set first=%s, last=%s, number=%s,country=%s," \
                          " city=%s, state=%s,  zip=%s where id=%s"
                    val = (first, last, number, country, city, state, zip, id,)
                    print(val)
                    country_database.cur.execute(sql, val)

                    print(val)
                    country_database.conn.commit()
                    # flash('Updated ')
                    return redirect(url_for('user_reg1.first'))


            except Exception as err:
                print(err)
                country_database.conn.rollback()
            finally:
                country_database.conn.close()


    return render_template('list_user_edit.html', result1= result1 , result= result, error=error)


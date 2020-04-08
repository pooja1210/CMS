from flask import Flask, render_template,request,json,Blueprint, url_for, redirect, flash
from fun import *
import country_database
import mysql.connector
import random
import string
from string import ascii_lowercase
import re
import hashlib

#user_reg=Flask(__name__)
user_reg = Blueprint('user_reg',__name__)



@user_reg.route('/list')
def list():
    return render_template('list_user.html')


@user_reg.route('/form',methods=['POST','GET'])
def frm():
    error = {}
    val = {}
    record=""
    try:
        country_database.connects()
        sql="select * from countries"
        country_database.cur.execute(sql)
        record=country_database.cur.fetchall()
        country_database.conn.commit()
    except:
        country_database.conn.rollback()
    finally:
        country_database.conn.close()


    if request.method=='POST':
        first= request.form['fname']
        last= request.form['lname']
        user=request.form['user']
        email= request.form['email']


        number=request.form['number']
        password= request.form['pwd']
        con_password= request.form['conpwd']
        country=request.form['cnm']
        city=request.form['cinm']
        state=request.form['snm']
        zip=request.form['znm']
        print("hello")
        print(first)
        print(email)


        print("vfdiugviv")
        val['a']=first
        val['b']=last
        val['c']=user
        val['d']=email
        val['e']=number
        val['f']=password
        val['g']=con_password
        val['h']=country
        val['i']=city
        val['g']=state
        val['h']=zip

        if first== "":
            error['f'] ="first name is required"
            print("vfdiugviv")
        if last== "":
            error['l'] ="last name is required"
        if user=="":
            error['us']="username required"

        if email=='':
            error['e'] ="email address required"
        else:
            if re.match("^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$",email) is None:
                error['ie'] = "Invalid EmailId"
        if number=="":
            error['n'] ="phone number is required"
        if password == '':
            error['pa'] ="password required"
        if con_password == '':
            error['cp'] ="Confirm Password required"
        else:
            if len(password)<6:
                error['lp'] ="Password cant be greater than 6"
            if lower_error(password) is None:
                error['lowp']="Password should have lower case letter"
            if uppercase_error(password) is None:
                error['upp']="Password should have upper case"
            if symbol_error(password) is None:
                error['srr']="Password should have one special character"
            if digit_error(password)is None:
                error['dp']="Password should have at least one digit"
        if country=="":
            error['cou']="country is required"
        if city == "":
            error['cit'] = "cit is required"
        if state == "":
            error['sta'] = "state is required"
        if zip == "":
            error['sta'] = "zip is required"


        if len(error)==0:
            conn = ""
            try:

                p = password
                h = hashlib.md5(p.encode())
                h1 = h.hexdigest()
                print("srmcem")
                print(h1)


                conn = mysql.connector.connect(host="localhost", user="root", passwd="", database="template_adduser")

                cursor = conn.cursor()
                print("pooja")



                sql="INSERT INTO form(first,last,user,email,number,password,country,city,state,zip)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                values=(first,last,user,email,number,h1,country,city,state,zip)
                cursor.execute(sql,values)
                conn.commit()
                print(values)
                return redirect(url_for('user_reg1.first'))
                # return "successful1"
            except Exception as err:
                print(err)
                conn.rollback()
            finally:
                conn.close()
            return "hello "


    return render_template('registration.html',error=error, val=val, record=record)

@user_reg.route('/get_state', methods=['POST', 'GET'])
def state():
    recordcity =''
    country = request.args.get('cnm')

    val = (country, )
    print(val)
    try:
       country_database.connects()
       state ="SELECT * FROM states WHERE country_id=%s"
       country_database.cur.execute(state, val)
       recordcity = country_database.cur.fetchall()
       print(recordcity)
    except:
        country_database.conn.rolback()
    finally:
        country_database.conn.close()
    return json.dumps({"type": "get_state1", "result":recordcity})


@user_reg.route('/get_city', methods=['POST', 'GET'])

def city():
    recordcity = ''
    country = request.args.get('snm')

    val = (country,)
    print(val)
    try:
        country_database.connects()
        state = "SELECT * FROM cities  WHERE state_id=%s"
        country_database.cur.execute(state, val)
        recordcity = country_database.cur.fetchall()
        print(recordcity)
    except:
        country_database.conn.rollback()
    print(recordcity)
    return json.dumps({"type": "get_city", "result": recordcity})

@user_reg.route('/get_email', methods=['POST', 'GET'])
def myemail():
    recordemail =''
    email = request.args.get('eml')

    val = (email, )
    print(val)
    try:
       country_database.connects()
       sql ="SELECT * FROM form where email=%s"
       country_database.cur.execute(sql, val)
       recordemail = country_database.cur.fetchone()
       print("sql value is", sql)
       print("val value is", val)
       print(recordemail)
    except:
        country_database.conn.rolback()
    finally:
        country_database.conn.close()
    return json.dumps({"type": "get_email1", "recordemail": recordemail})


@user_reg.route('/registration', methods=['POST', 'GET'])

def reg():
    error = {}
    val = {}
    record = ""
    try:
        country_database.connects()
        sql = "SELECT id FROM form ORDER BY id DESC LIMIT 1"
        country_database.cur.execute(sql)
        current_id = country_database.cur.fetchone()
        print("last_id",current_id)
        i_d=current_id['id']
        print(i_d)
        print(type(current_id))
        str_id=str(current_id)
        country_database.conn.commit()
        sql = "select * from countries"
        country_database.cur.execute(sql)
        record = country_database.cur.fetchall()
        country_database.conn.commit()
    except:
        country_database.conn.rollback()
    finally:
        country_database.conn.close()

    if request.method=='POST':
        first= request.form['fname']
        last= request.form['lname']
        user=request.form['user']
        email= request.form['email']
        number=request.form['number']
        password= request.form['pwd']
        con_password= request.form['conpwd']
        country=request.form['cnm']
        city=request.form['cinm']
        state=request.form['snm']
        zip=request.form['znm']

        print("hello")
        print(first)
        print(email)
        print("vfdiugviv")
        val['a'] = first
        val['b'] = last
        val['c'] = user
        val['d'] = email
        val['e'] = number
        val['f'] = password
        val['g'] = con_password
        val['h'] = country
        val['i'] = city
        val['g'] = state
        val['h'] = zip

        if first == "":
            error['f'] = "first name is required"
            print("vfdiugviv")
        if last == "":
            error['l'] = "last name is required"
        if user == "":
            error['us'] = "username required"

        if email == '':
            error['e'] = "email address required"
        else:

            if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$)", email) is None:
                error['ie'] = "Invalid EmailId"
        if number == "":
            error['n'] = "phone number is required"
        if password == '':
            error['pa'] = "password required"
        if con_password == '':
            error['cp'] = "Confirm Password required"
        else:
            if len(password) < 6:
                error['lp'] = "Password cant be greater than 6"
            if lower_error(password) is None:
                error['lowp'] = "Password should have lower case letter"
            if uppercase_error(password) is None:
                error['upp'] = "Password should have upper case"
            if symbol_error(password) is None:
                error['srr'] = "Password should have one special character"
            if digit_error(password) is None:
                error['dp'] = "Password should have at least one digit"
        if country == "":
            error['cou'] = "country is required"
        if city == "":
            error['cit'] = "cit is required"
        if state == "":
            error['sta'] = "state is required"
        if zip == "":
            error['sta'] = "zip is required"
        if len(error) == 0:
            conn = ""
            try:




                p = password
                h = hashlib.md5(p.encode())
                h1 = h.hexdigest()

                country_database.connects()


                print("shubham1")
                status="false"
                link="true"
                sql = "INSERT INTO form(first,last,user,email,number,password,country,city,state,zip,status,linked)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                values = (first, last, user, email, number, h1, country, city, state, zip,status,link)
                country_database.cur.execute(sql, values)
                country_database.conn.commit()
                print("pooja m")
                sql="SELECT id FROM form where email = %s"
                val=(email,)
                country_database.cur.execute(sql,val)
                record1 = country_database.cur.fetchone()
                print("recorad",record1)
                id=record1['id']
                print(id)
                a=encr(id)
                print("a",a)
                sql = "UPDATE form set OTP =%s  where id=%s"
                values = (a,id,)
                country_database.cur.execute(sql, values)
                country_database.conn.commit()
                # send_email('Food Blog Activation Link ',
                #            'We thank you for registerting with Foodblog'
                #            '\n Hello ' + user +
                #             '\n You are successfully registered with us\nYour activation link is http://127.0.0.1:5000/activation_link/'+a+
                #              '\nThanks & Regards\nFood blog Team',email)

                flash("You  are now registered with us")

                return redirect(url_for('user_reg.reg'))
                # return "successful1"
            except Exception as err:
                print(err)
                country_database.conn.rollback()
            finally:
                country_database.conn.close()





    return render_template('frontend/user_reg.html',error=error, val=val, record=record)

@user_reg.route('/check-email', methods=['POST', 'GET'])

def check():
    send_email('Food Blog Activation Link ',
               'We thank you for registerting with Foodblog'
               '\n Hello '
               '\n You are successfully registered with us\nYour activation link is http://127.0.0.1:5000/activation_link/'
               '\nThanks & Regards\nFood blog Team', 'kartik.joshi@dotsquares.com')
    return 'xyz'



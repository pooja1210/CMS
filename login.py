from flask import Flask,render_template, request, Blueprint, redirect, url_for,session,flash

import country_database
from fun import result_front, cat_img,  send_email
import hashlib


login_reg = Blueprint('login_reg',__name__)



@login_reg.route('/login', methods=['GET','POST'] )
def login():

    error={}
    result=""



    results = result_front('slider_manager')
    status=request.args.get('status')
    if request.method=='POST':
        print("poojaaaaaa pandey")

        user=request.form['username']
        print(user)
        password=request.form['password']
        print(password)
        if user=='':

            error['a']="username required"
        if password=="":

            error['b']="password required"
        results = result_front('slider_manager')

        print("error",error)
        if len(error)==0:




            try:

                p = password
                h = hashlib.md5(p.encode())
                h1 = h.hexdigest()

                country_database.connects()
                val = (user, h1,)
                country_database.cur.execute("SELECT * FROM form WHERE email=%s and password=%s", val)
                result = country_database.cur.fetchone()
                session['user'] = result
                print(result)




                print("total",session['user'])
                print("status", session['user']['status'])
                print("OTP", session['user']['OTP'])
                country_database.conn.commit()




            except Exception as err:
                print(err)
                country_database.conn.rollback()
            finally:
                country_database.conn.close()
            print("next")
            
            if result is not None:
                if session['user']['OTP'] is None:
                    print("user user")
                    error['link expire']='link expire'
                    return render_template('login.html', error=error)



                if session['user']['status'] == 'true':
                    print("zero status")

                    error['activation'] = "Sorry You can't login, First activate your account just by clicking the activation link sent to your registered email_id"
                    return render_template('login.html' ,error=error, result=results)
                else:
                    return redirect(url_for('login_reg.login_view'))

            if result is None:
                error['em']="User And Password not match "
                return render_template('login.html' ,error=error, result=results)
            return redirect(url_for('login_reg.login_view'))



    return render_template('login.html', error=error)

@login_reg.route('/login_view', methods=['GET','POST'] )
def login_view():
    record=""
    result=""
    result = result_front('slider_manager')
    # print("#@#@#@",result)
    if 'user' in session:

        try:

            country_database.connects()
            print("session_user",session['user'])
            sql="select * from article_manager where user_id = %s"
            val=(session['user']['id'],)
            print("val value is",val)
            country_database.cur.execute(sql,val)
            record=country_database.cur.fetchall()
            print("ghdfs",record)
            country_database.conn.commit()
        except  Exception as err:
            print(err)
            country_database.conn.rollback()
        finally:
            country_database.conn.close()
    return render_template('login_view.html', result=result, record=record )

@login_reg.route('/login_home_view', methods=['GET','POST'] )
def login_home_view():
    results = result_front('slider_manager')
    sql="select * from "

    return render_template('login_home_view.html',  result=results)
@login_reg.route('/article_view')
def article_view():
    art_result = result_front(' article_manager')
    print("art%%", art_result)
    country_database.connects()

    return render_template('login_article.html',art_result=art_result)
@login_reg.route('/category_view')
def category_view():
    myresult = cat_img('category_manager')
    art_result = result_front(' article_manager')
    result = result_front('slider_manager')
    print("art", art_result)
    print("cat", myresult)
    return render_template('login_category.html',result=result,   myresult=myresult )

@login_reg.route('/', methods=['GET','POST'] )
def login_logout_view():
    result = ""
    myresult = ""
    art_result = ""
    result = result_front('slider_manager')
    myresult = cat_img('category_manager')
    art_result = result_front(' article_manager')
    return render_template('foo.html',result=result_front('slider_manager'),  my_result= myresult, art_result=art_result)


@login_reg.route('/article/detail/<slug>')
def login_image_link_view(slug):
    result=""
    record=""

    try:
        print("in edit")
        slug = slug
        print(slug)

        result = result_front('slider_manager')

        country_database.connects()
        flag = 0
        sql = "SELECT * FROM  article_manager where slug=%s"
        val = (slug,)

        country_database.cur.execute(sql, val)
        record= country_database.cur.fetchone()

        record_file =record['file']
        print("$$$$4",record_file)

        a=record['category_id']
        x=record['id']

        country_database.conn.commit()


        sql= "Select category_id FROM article_manager where slug=%s"
        val=(slug,)
        country_database.cur.execute(sql,val)
        result_s=country_database.cur.fetchone()

        c_ti=result_s['category_id']
        print(c_ti)
        country_database.conn.commit()

        sql="Select * FROM article_manager where category_id IN (%s) AND id NOT IN (%s)"
        val=(c_ti,x,)

        country_database.cur.execute(sql,val)
        result_final=country_database.cur.fetchall()
        print("$$$$", result_final)

        country_database.conn.commit()





        country_database.conn.commit()

    except Exception as err:
        print(err)
        country_database.conn.rollback()
    finally:
        country_database.conn.close()

    return render_template('login_image_link.html', record=record, result=result, record_final=result_final)




@login_reg.route('/activation_link/<slug>', methods=['GET','POST'] )
def login_activate(slug):

    error={}
    result=""
    print("above")
    results = result_front('slider_manager')

    status = "true"

    try:
        country_database.connects()
        sql= "select * from form where OTP=%s"
        val=(slug,)
        country_database.cur.execute(sql, val, )
        result_final = country_database.cur.fetchone()
        country_database.conn.commit()
    except Exception as err:
        print(err)
        country_database.conn.rollback()
    finally:
        country_database.conn.close()

    if result_final is not None:
        try:
            print("slug is not none")
            country_database.connects()

            sql = "UPDATE form set status =%s, OTP=%s  where OTP=%s"
            status="true"
            empty=" "
            val = (status,empty, slug,)
            print("val is", val)
            country_database.cur.execute(sql, val, )
            country_database.conn.commit()

            return redirect(url_for('login_reg.login'))
        except Exception as err:
            print(err)
            country_database.conn.rollback()
        finally:
            country_database.conn.close()
    else:
        print("OTP is blank")
        error['cccc']='link expired!'

        print("erro is", error)

        return  render_template('login.html', error=error)













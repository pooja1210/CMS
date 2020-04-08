from flask import Flask, Blueprint, render_template, request,session

import country_database

admin_login_reg = Blueprint('admin_login_reg', __name__)

@admin_login_reg.route('/admin', methods=['GET','POST'])
def admin_login():
    error ={}
    result=""
    if request.method=='POST':
        user=request.form['email']
        password=request.form['password']
        if user=='':
            error['a']="email required"
        if password=='':
            error['b']="password required"
        if len(error)==0:
            try:
                country_database.connects()
                val=(user,password)
                country_database.cur.execute("SELECT id FROM form WHERE email=%s and password=%s", val)
                result= country_database.cur.fetchone()
                session['user']=result
                print(result)
                print(session['user'])
                print(session['user']['id'])
                country_database.conn.commit()
            except:
                country_database.conn.rollback()
            finally:
                country_database.conn.close()
            if result is not None:
                print("result is not none")
                if session['user']['id'] is not 1:
                    print("user and password not match")
                    error['em']='USER AND PASSWORD NOT MATCH'
                    print('desfetgrt')
                    return render_template('admin_login.html', error=error)
                return render_template('index.html')
        return render_template('admin_login.html', error=error)



    return render_template('admin_login.html')










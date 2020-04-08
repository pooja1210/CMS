from flask import Flask, Blueprint, render_template, flash, redirect, url_for, send_from_directory, json, request
import  re
import country_database
contact_manager = Blueprint('contact_manager',__name__)


@contact_manager .route('/contact_us',  methods=['GET', 'POST'])
def contact_us():
    error = {}
    val = {}
    if request.method== 'POST':


        name = request.form['name']
        subject= request.form['subject']
        email=request.form['email']
        message=request.form['message']
        print(name)
        print(email)
        if name=="":
            error['a']="Your name is required"
        if subject == "":
            error['b'] = "subject is required"
        if email == "":
            error['c'] = "Email is required"
        else:
            if re.match("^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$", email) is None:
                error['ie'] = "Invalid EmailId"

        if message == "":
            error['d'] = "Please write your message"
        if len(error)==0:
            try:
                country_database.connects()
                sql = "INSERT INTO contact_us(name,subject ,email , message) VALUES (%s, %s, %s, %s)"
                val=(name, subject, email, message,)
                country_database.cur.execute(sql, val)
                country_database.conn.commit()
                flash('We will contact you soon!')
                return render_template('contact.html', error=error)
            except Exception as err:
                print(err)
                country_database.conn.rollback()
            finally:
                country_database.conn.close()
            return render_template('contact.html', error=error)
    return render_template('contact.html', error=error)





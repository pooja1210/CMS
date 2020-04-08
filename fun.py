import re
import hashlib

import os
import smtplib
from flask import  Flask, request
import smtplib
from werkzeug.utils import secure_filename
import country_database
import math, random
import string

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
from unicodedata import normalize
app =Flask(__name__)



def digit_error(password):
    return re.search(r"\d", password)

def symbol_error(password):
    return re.search(r"[!@&$]", password)

def lower_error(password):
    return re.search(r"[a-z]", password)

def uppercase_error(password):
    return re.search("[A-Z]", password)

def delete(fo, filename):
    print("fgdiugfuyr")
    os.remove(fo + "/" + filename)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend((word).split())
    return (delim.join(result))


def upload_file():

      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

def deleted(file, filename):
    print("fgdiugfuyr")
    os.remove(file + "/" + filename)




def result_front(tables):
    result = ""
    try:
        country_database.connects()
        sql = ''
        if tables is 'page_tbl' or tables is 'category_tbl':
            sql = "select * from " + tables
            country_database.excute(sql)
        else:
            print(tables)
            status = ('Publish',)
            sql = "select * from " + tables + " WHERE status = %s"
            country_database.cur.execute(sql, status)

        result = country_database.cur.fetchall()

    except Exception as err:
        print(err)
        country_database.conn.rollback()
    finally:
        country_database.conn.close()
    return result
def cat_img(tables):
    try:
        country_database.connects()
        sql = "select * from " + tables
        country_database.cur.execute(sql)
        myresult = country_database.cur.fetchall()
    except Exception as err:
        print(err)
        country_database.conn.rollback()
    finally:
        country_database.conn.close()
    return myresult

# def send_email(subject,meassage, recipients):
#     app.config['MAIL_SERVER'] = 'mail.24livehost.com'
#     app.config['MAIL_PORT'] = 587
#     app.config['MAIL_USERNAME'] = 'wwwsmtp@24livehost.com'
#     app.config['MAIL_PASSWORD'] = 'dsmtp909#'
#     app.config['MAIL_USE_TLS'] = True
#     app.config['MAIL_USE_SSL'] = False
#     mail = Mail(app)
#
#
#     msg = Message(subject, sender='wwwsmtp@24livehost.com', recipients=[recipients])
#     msg.body = meassage
#     mail.send(msg)
#     return "Sent"

def send_email(subject, msg, email_reciver):

  try:

    server = smtplib.SMTP('smtp.gmail.com:587',)
    server.ehlo()
    server.starttls()
    server.login('poojapandey12oct@gmail.com', 'up@12345A')
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % ('poojapandey12oct@gmail.com', ", ".join([email_reciver]), subject, msg)

    # message = 'subject : {} \r\n\n {}'.format(subject, msg)
    print("mesage is here",message)
    server.sendmail('poojapandey12oct@gmail.com', email_reciver, message)
    server.quit()
  except Exception as err:
    print(err)
  return message

def generateOTP(a):
    # Declare a digits variable
    # which stores all digits

    OTP = ""

    # length of password can be chaged
    # by changing value in range
    for i in range(4):
        OTP += a[math.floor(random.random() * 10)]

    return OTP
def generatestring(x):
    # Declare a string variable
    # which stores all string


    string = x+'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print(string)
    OTP = ""
    length = len(string)
    for i in range(4):
        OTP += string[math.floor(random.random() * length)]

    return OTP



def encr(id):
    a = str(id)
    print(type(a),a)
    h = hashlib.md5(a.encode())
    h1 = h.hexdigest()
    # id1 = ''.join(random.choice(string.ascii_letters) for x in range(a))
    # print(id1)
    print(h1)
    return h1










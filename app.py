from flask_mail import *
from flask import request, Flask, render_template, session, redirect, url_for
import pymysql
import random
from Crypto.Random import get_random_bytes
from random import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from math import *
import pandas as pd
import os
import random
from Crypto.Random import get_random_bytes
from audio import encrypt_audio, decrypt_audio
from video import encrypt_video, decrypt_video
from image import encrypt_image, decrypt_image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b0b4fbefdc48be27a6123605f02b6b86'
db = pymysql.connect(host='localhost', user='root',
                     port=3306, password='', db='Cloud')
cursor = db.cursor()

mail = Mail(app)
otp = randint(000000, 999999)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("home.html")

# CLOUD SERVICE PROVIDER


@app.route("/homes")
def homes():
    return render_template("homes.html")




# DATAOWNER PAGES
@app.route("/DataOwners", methods=['POST', 'GET'])
def DataOwners():

    if request.method == 'POST':
        Name = request.form['Name']
        Email = request.form["Email"]
        Number = request.form["Number"]
        Gender = request.form["Gender"]
        Address = request.form["Address"]
        otp = randint(000000, 999999)
        msg="Your account is activated use secret key to login :"
        mail_content = msg + ' ' + str(otp)
        sender_address = 'charan.nallanagula1@gmail.com'
        sender_pass = 'xtvjmelpfjttmzaw'
        receiver_address = Email
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Data Encryption And Sharing'
        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        sql = "insert into Dataowners (Name,Email,Number,Gender,Address,Otp) values (%s,%s,%s,%s,%s,%s)"
        val = (Name, Email, Number, Gender, Address, otp)
        cursor.execute(sql, val)
        db.commit()
        return render_template("Data Owners.html", message="register", name=Name)
    return render_template("Data Owners.html")


@app.route("/DataOwnerslogin", methods=['POST', 'GET'])
def DataOwnerslogin():
    if request.method == 'POST':
        Email = request.form["Email"]
        OTP = request.form["OTP"]
        sql = "select * from Dataowners where Email=%s and Otp=%s"
        val = (Email, OTP)

        cursor.execute(sql,val)
        Results = cursor.fetchall()
        print(Results)
        print("skdjvnsdjbcjsdbcskckc")

        if Results != ():
            session["useremail"] = Results[0][2]
            print(session.get('useremail'))
            return render_template("Data Owners Home.html", msg="sucess")
        else:
            return render_template("Data Owners.html", mfg="not found")
    return render_template("DataOwnerslogin.html")


@app.route("/DataOwnersUploadFiles", methods=['POST', 'GET'])
def DataOwnersUploadFiles():
    sql = "select * from dataowners"
    cursor.execute(sql)
    all_dataowners = cursor.fetchall()
    if request.method == 'POST':
        sender = session.get('useremail')
        print(session.get('useremail'))
        receiver = request.form['dataowner']
        Files = request.files["Files"]
        filename = Files.filename
        if filename.endswith(".wav") or filename.endswith(".mp3"):
            randomkey = str(random.randint(00000000, 99999999))

            # Example usage
            input_audio_file = "static/audiofiles/audio/" + filename

            path = os.path.join("static/audiofiles/audio/", filename)
            Files.save(path)

            encrypted_audio_file = "static/audiofiles/encryptedaudio/" + \
                f'{filename}'

            decrypted_audio_file = "static/audiofiles/decryptedaudio/" + \
                f'{filename}'

            # Generate a random 256-bit key (32 bytes)
            encryption_key = get_random_bytes(32)

            # Encrypt the audio file
            encrypt_audio(input_audio_file,
                          encrypted_audio_file, encryption_key)

            # Decrypt the encrypted audio file
            decrypt_audio(encrypted_audio_file,
                          decrypted_audio_file, encryption_key)
            data = decrypted_audio_file
            sql = "insert into filesupload (owneremail,FileName,receiver,Files,path,randomkey) values (%s,%s,%s,AES_ENCRYPT(%s,'rupesh'),%s,%s)"
            values = (sender, filename, receiver, data, data, randomkey)
            cursor.execute(sql, values)
            db.commit()
        elif filename.endswith('.mp4') or filename.endswith('.ogg'):
            randomkey = str(random.randint(00000000, 99999999))

            input_video = "static/videofiles/video/" + filename
            path = os.path.join("static/videofiles/video/", filename)
            Files.save(path)

            encrypted_video = "static/videofiles/encryptedvideo/" + \
                f'{filename}'
            decrypted_video = "static/videofiles/decryptedvideo/" + \
                f'{filename}'
            # 256-bit key for AES-256
            key = get_random_bytes(32)

            encrypt_video(input_video, encrypted_video, key)
            print(f'Video encrypted with key: {key.hex()}')

            decrypt_video(encrypted_video, decrypted_video, key)
            print(f'Video decrypted successfully')
            data = decrypted_video
            sql = "insert into filesupload (owneremail,FileName,receiver,Files,path,randomkey) values (%s,%s,%s,AES_ENCRYPT(%s,'rupesh'),%s,%s)"
            values = (sender, filename, receiver, data, data, randomkey)
            cursor.execute(sql, values)
            db.commit()
        elif filename.endswith(".txt"):
            randomkey = str(random.randint(00000000, 99999999))
            path = os.path.join("static/uploadFiles/", filename)
            newpath = f"static/uploadfiles/{filename}"
            Files.save(path)
            f = open(newpath, "r")
            data = f.read()
            data = data[0][0]

            sql = "insert into filesupload (owneremail,FileName,receiver,Files,path,randomkey) values (%s,%s,%s,AES_ENCRYPT(%s,'rupesh'),%s,%s)"
            values = (sender, filename, receiver, data, newpath, randomkey)
            cursor.execute(sql, values)
            db.commit()
        else:
            randomkey = str(random.randint(0, 99999999)).zfill(8)

            path = os.path.join("static/images/image/", filename)
            newpath = f"static/images/image/{filename}"

            # Assuming `Files` is the uploaded file, save it to the specified path
            Files.save(path)

            input_image = path
            key = get_random_bytes(32)  # 256-bit key for AES-256
            encrypted_image = f"static/images/encryptedimage/{filename}"
            decrypted_image = f"static/images/decryptedimage/"

            encrypt_image(input_image, encrypted_image, key)
            decrypt_image(encrypted_image, filename,decrypted_image, key)

            sql = "insert into filesupload (owneremail,FileName,receiver,Files,path,randomkey) values (%s,%s,%s,AES_ENCRYPT(%s,'rupesh'),%s,%s)"
            values = (sender, filename, receiver,
                      encrypted_image, newpath, randomkey)
            cursor.execute(sql, values)
            db.commit()
        msg = "Decryption Key for your File : "
        mail_content = msg + ' ' + str(randomkey)
        sender_address = 'charan.nallanagula1@gmail.com'
        sender_pass = 'xtvjmelpfjttmzaw'
        receiver_address = receiver
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Data Encryption And Sharing'
        message.attach(MIMEText(mail_content, 'plain'))
        session_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        session_smtp.starttls()
        session_smtp.login(sender_address, sender_pass)
        text = message.as_string()
        session_smtp.sendmail(sender_address, receiver_address, text)
        session_smtp.quit()

        return render_template("DataOwnersUploadFiles.html", all_dataowners=all_dataowners, msg="success")

    return render_template("DataOwnersUploadFiles.html", all_dataowners=all_dataowners)


@app.route("/DataOwnersViewFiles")
def DataOwnersViewFiles():
    print(session["useremail"])
    sql = "select SL_NO,owneremail,FileName,receiver from filesupload where owneremail='%s'" % (
        session["useremail"])
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    result = pd.read_sql_query(sql, db)
    return render_template("DataOwnersViewFiles.html", col_name=result.columns.values, row_val=result.values.tolist())


@app.route("/DataOwnersViewAllFiles", methods=["POST", "GET"])
def DataOwnersViewAllFiles():
    if request.method == "POST":
        filekey = request.form['filekey']
        receiveremail = session["useremail"]
        sql = "select * from filesupload where receiver='%s' and randomkey='%s'" % (
            receiveremail, filekey)
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        if data != []:
            filename = data[0][2]
            print(filename)
            if filename.endswith(".wav") or filename.endswith(".mp3"):

                filepath = data[0][5]
                print(filepath)
                return render_template("ViewFiles.html", filepath=filepath, type="audio")
            elif filename.endswith('.mp4') or filename.endswith('.ogg'):
                filepath = data[0][5]
                return render_template("ViewFiles.html", filepath=filepath, type="video")

            elif filename.endswith('.txt'):
                sql = "select AES_DECRYPT(Files,'rupesh') from filesupload where randomkey=%s and receiver=%s"
                val = (filekey, receiveremail)
                cursor.execute(sql, val)
                data = cursor.fetchall()
                f = open(f"static/uploadFiles/{filename}","r")
                data = f.read()
                
                return render_template("ViewFiles.html", type="text",filename=filename,data=data)
            else:
                sql = "select AES_DECRYPT(Files,'rupesh') from filesupload where randomkey=%s and receiver=%s"
                val = (filekey, receiveremail)
                cursor.execute(sql, val) 
                data = cursor.fetchall()
                print(data)
                return render_template("ViewFiles.html", type="new",filename=filename, data=data)

        return render_template("DataOwnersViewAllFiles.html")
    return render_template("DataOwnersViewAllFiles.html")


if (__name__) == ("__main__"):
    app.run(debug=True)

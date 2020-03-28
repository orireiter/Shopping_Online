# flask imports
from flask import Flask, redirect, render_template, request
# homemade imports
import db_for_home, db_search, shopping_processor, barcode_maker, db_for_auth
# general use imports
import datetime, os, json, email, smtplib, ssl
# email related
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)


@app.route("/sender/<username>", methods=['POST'])
def order_page(username):
    
    doc, ran = shopping_processor.order_sender(username)
    try: 
        collection = db_for_auth.db_info()
        db_obj = collection.find_one({"name": str(username)})
        if db_obj == None:
            return "error", 404
        else:
            email = db_obj['email']
            print(email)
    except:
        return "error", 404    
    
    # email
    gmail_user = 'basket4yotvata@gmail.com'
    gmail_password = 'Yt6357510'
    receivers = str(email)
    subject = f'{datetime.date.today()} הזמנה של: {username}'
    #-------------------#


    #-------------------#
    # formatting a mail #

    raw_mail = MIMEMultipart()
    raw_mail["From"] = gmail_user
    raw_mail["To"] = receivers
    raw_mail["Subject"] = f'{subject}'

    
    # Open docx file in binary mode
    with open(doc, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {ran}{datetime.date.today()}.docx",
    )

    # Add attachment to message and convert message to string
    raw_mail.attach(part)
    ready_mail = raw_mail.as_string()
    
    
    try: 
        mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mail_server.ehlo()
        mail_server.login(user=gmail_user, password=gmail_password)
        mail_server.sendmail(from_addr=gmail_user, to_addrs=receivers, msg=ready_mail)
        mail_server.close()
        print('mail sent')
    except:
        print("didnt work")

    clean_json = open('.\orders\\'+str(username)+str(datetime.date.today())+'.json', 'w')
    clean_json.write(r"{}")
    clean_json.close()

    backk = request.referrer
    #return redirect(backk)
    return render_template("done.html")
    
if __name__ == "__main__":
    app.run(debug=True,host='172.16.0.17', port=5002)
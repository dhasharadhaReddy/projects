import time
from flask import Flask, request, render_template
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route("/motor")
def get_info():
    global df
    filename = 'datafile.csv'
    df = pd.read_csv(filename)
    
    timestamp = request.args.get("timestamp")
    temp = request.args.get("temp")
    hum = request.args.get("hum")
    moist = request.args.get("moisture")
    print("\nvalues\n")
    print(timestamp,'\n',temp,'\n',hum,'\n',moist)
    new_row = pd.DataFrame({'Timestamp':[timestamp],'Temperature': [temp], 'Humidity': [hum], 'Moisture': [moist]})
    
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(filename, index=False)
    time.sleep(1)
    send_mail_alert()
    if (moist==1):
        if (temp>=32):
            if (hum>=50):
                
                while (moist!=1):
                    return "motor running"
                print("Sufficient water added")
    return "motor not running"
    
    
@app.route('/dashboard', methods=['GET', 'POST'])
def db():
    return render_template('plots.html')

@app.route('/chartdata', methods=['GET', 'POST'])
def chart_data():
    data = pd.read_csv("datafile.csv")
    data = data.tail(10)
    return data.to_json()

def send_mail_alert():
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Motor is on"
    msg['From'] = 'bommana2011042@ssn.edu.in'
    msg['To'] = 'dasarath.reddy22@gmail.com'

    html_table = df.to_html()
    html_body = MIMEText(html_table, 'html')
    msg.attach(html_body)

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "bommana2011042@ssn.edu.in"
    smtp_password = "app_password"

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail('bommana2011042@ssn.edu.in', 'dasarath.reddy22@gmail.com', msg.as_string())

if __name__=="__main__":
    app.run("0.0.0.0",debug=True)
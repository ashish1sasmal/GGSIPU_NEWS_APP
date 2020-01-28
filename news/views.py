from django.shortcuts import render
import schedule
import os
import time
import smtplib
from bs4 import BeautifulSoup
import requests

EMAIL_ID = os.environ.get('EMAIL_ID')
EMAIL_PASS = os.environ.get('EMAIL_PASS')

def send_email(subject,msg,email_id):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ID,EMAIL_PASS)
        print("here")
        message = f'Subject:{subject}\n\n{msg}'
        server.sendmail(EMAIL_ID,email_id,message)
        server.quit()
        print("success!")
    except:
        print("email failed!")

def job():
    subject = "HELlo"
    msg="come tommorrow"
    send_email(subject,msg,"ashishsasmal1@gmail.com")

schedule.every(60*30).seconds.do(job)

def home(request):
    while True:
        schedule.run_pending()
        time.sleep(1)
    return render(request,'news/home.html')

def test(request):

    return render(request,'news/test.html')


############$$$$$$$$$$$$$$ W E B - S C R A P I N G $$$$$$$$$$$$$$#########################

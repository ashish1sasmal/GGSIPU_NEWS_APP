from django.shortcuts import render
import schedule
import os
import time
import smtplib
from bs4 import BeautifulSoup
import requests
from .models import LastNotice
from datetime import date

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

schedule.every(10).seconds.do(job)

def test(request):
    while True:
        schedule.run_pending()
        time.sleep(1)
    return render(request,'news/home.html')

def home(request):

    return render(request,'news/test.html')


############$$$$$$$$$$$$$$ W E B - S C R A P I N G $$$$$$$$$$$$$$#########################

source  = requests.get('http://www.ipu.ac.in/notices.php').text
soup = BeautifulSoup(source,'lxml')
notices = soup.find_all('tr')

day=date.today().strftime("%d-%m-%Y")

for notice in notices:
    l=notice('td')
    if len(l)>1:
        if (l[-1].get_text()==day):
            print(l[0].a.get_text())
            print("http://www.ipu.ac.in"+(l[0].a)['href'])
            print()

from django.shortcuts import render
import schedule
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import time
import smtplib
from bs4 import BeautifulSoup
import requests
from .models import LastNotice
from datetime import date

EMAIL_ID = os.environ.get('EMAIL_ID')
EMAIL_PASS = os.environ.get('EMAIL_PASS')
day=date.today().strftime("%d-%m-%Y")

def send_email(subject,msg,email_id):
        print("inside login!")

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ID,EMAIL_PASS)
        print("after login")
        notice=""
        for i in msg:
            notice+="\nTITLE : "+str(i[0])+"\nURL : "+str(i[1])+"\n"
        print(notice)
        server.sendmail(EMAIL_ID,email_id,notice)
        server.quit()
        print("success! after sent!")


def job():
    latest=scrap_notices()
    print(latest)

    if latest!=[]:
        form = LastNotice(title=latest[0][0],url=latest[0][1])
        form.save()
        print('success after scrap')
        send_email("ggsipu notice",latest,"ashishsasmal1@gmail.com")
    else:
        print('no new notice')

schedule.every(10).seconds.do(job)


def home(request):
    return render(request,'news/home.html')

def test(request):

    while True:
        schedule.run_pending()
        time.sleep(1)

    return render(request,'news/test.html')


############$$$$$$$$$$$$$$ W E B - S C R A P I N G $$$$$$$$$$$$$$#########################



def scrap_notices():
    print('here')
    source  = requests.get('http://www.ipu.ac.in/notices.php').text
    soup = BeautifulSoup(source,'lxml')
    notices = soup.find_all('tr')

    latest=[]
    index=0
    for notice in notices:
        l=notice('td')
        if len(l)>1:
            text=l[0].a.get_text()
            if (l[-1].get_text()==day) and LastNotice.objects.last().title!=text:
                latest.append([text,("http://www.ipu.ac.in"+(l[0].a)['href'])])
                index+=1

            else:
                break

    return latest

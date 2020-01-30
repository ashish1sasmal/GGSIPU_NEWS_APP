from django.shortcuts import render
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib import messages
import time
import smtplib
from bs4 import BeautifulSoup
import requests

from apscheduler.schedulers.background import BackgroundScheduler

from .models import LastNotice,Profile
from datetime import date

EMAIL_ID = os.environ.get('EMAIL_ID')
EMAIL_PASS = os.environ.get('EMAIL_PASS')
day=date.today().strftime("%d-%m-%Y")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', minutes=5)
    scheduler.start()

def send_email(subject,msg):
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
        email_ids=list(Profile.objects.values_list('email',flat=True))
        for id in email_ids:
            server.sendmail(EMAIL_ID,id,notice)
        server.quit()
        print("success! after sent!")


def job():
    print("job running")
    latest=scrap_notices()
    print("after scrap")
    if latest!=[]:
        form = LastNotice(title=latest[0][0],url=latest[0][1])
        form.save()
        print('success after scrap')
        send_email("ggsipu notice",latest)
    else:
        print('no new notice')
    print(LastNotice.objects.all())

# schedule.every(120).seconds.do(job)


def home(request):
    if request.method=="POST":
        email=request.POST.get('email')
        check=Profile.objects.filter(email=email).exists()
        if not check:
            form=Profile(email=email)
            form.save()
            messages.success(request,'You are subscribed!')
        else:
            messages.warning(request,'You are already subscribed!')
    return render(request,'news/home.html')



############$$$$$$$$$$$$$$ W E B - S C R A P I N G $$$$$$$$$$$$#########################



def scrap_notices():
    print('inside scrap notice')
    source  = requests.get('http://www.ipu.ac.in/notices.php').text
    soup = BeautifulSoup(source,'lxml')
    notices = soup.find_all('tr')

    latest=[]
    index=0
    print(day)
    print(LastNotice.objects.last().title)
    for notice in notices:
        l=notice('td')
        if len(l)>1:
            text=l[0].a.get_text()
            print(text)
            if (l[-1].get_text()==day) and LastNotice.objects.last().title!=text:
                latest.append([text,("http://www.ipu.ac.in"+(l[0].a)['href'])])
                index+=1

            else:
                break
    print(latest)
    return latest

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
day=date.today().strftime("%d-%m-%Y")

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
    latest=scrap_notices()
    print(latest)

    if latest!=[]:
        form = LastNotice(title=latest[0][0],url=latest[0][1])
        form.save()
        print('success')
        send_email("ggsipu notice",str(latest),"ashishsasmal1@gmail.com")
    else:
        print('no new notice')
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
        print('y')
        l=notice('td')
        if len(l)>1:
            text=l[0].a.get_text()
            print(LastNotice.objects.last().title)
            if (l[-1].get_text()==day) and LastNotice.objects.last().title!=text:
                latest.append([text,("http://www.ipu.ac.in"+(l[0].a)['href'])])
                index+=1

            else:
                break

    return latest

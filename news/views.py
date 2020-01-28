from django.shortcuts import render
import schedule
# Create your views here.
import time

def job():
    print("I'm working...")

schedule.every(5).seconds.do(job)

def home(request):
    while True:
        schedule.run_pending()
        time.sleep(1)
    return render(request,'news/home.html')

from django.db import models
import datetime
# Create your models here.

class LastNotice(models.Model):
    title=models.CharField(max_length=200)
    url=models.URLField()
    notice_date=models.DateField(_("Date"), default=datetime.date.today)
    date=models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f'{self.title}'

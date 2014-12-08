from __future__ import absolute_import
import os
from celery import Celery, task, current_task
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TweetMap.settings')

app = Celery('TweetMap', backend='', broker='"sqs://%s:%s@" % (AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)',
            include=['twitter_service.tasks'])

if __name__ == '__main__':
  app.start()    

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
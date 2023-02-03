from django.db import models

# Create your models here.
from django.utils import timezone

from json_auth_project import settings


class Tag(models.Model):
    title = models.CharField(max_length=31, unique=True)

    def __str__(self):
        return self.title


TYPE_EVENT = ['TypeA', 'TypeB', 'TypeC']
TYPE_EVENT_CHOICES = sorted([(item, item) for item in TYPE_EVENT])
CATEGORY_EVENT = ['info', 'attention', 'alarm']
CATEGORY_EVENT_CHOICES = sorted([(item, item) for item in CATEGORY_EVENT])


class Event(models.Model):
    title = models.CharField(max_length=63)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    #timezone = models.CharField(default=timezone.get_current_timezone(), max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='events', on_delete=models.CASCADE)
    type_event = models.CharField(choices=TYPE_EVENT_CHOICES, default='TypeA', max_length=100)
    category_event = models.CharField(choices=CATEGORY_EVENT_CHOICES, default='info', max_length=100)
    tags = models.ManyToManyField(Tag, related_name='events')

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        if self.category_event != 'alarm':
            super(Event, self).delete()


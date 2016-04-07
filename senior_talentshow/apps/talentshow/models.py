import datetime
import pytz
import random
import string

from django.db import models
from django.utils import timezone
from django.conf import settings

from localflavor.us.models import PhoneNumberField


tz = pytz.timezone(settings.TIME_ZONE)


def _generate_secret():
    while True:
        secret = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(30))
        try:
            existing = Auditioner.objects.get(secret=secret)
        except Auditioner.DoesNotExist:
            return secret


class Auditioner(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    phone = PhoneNumberField(null=True, blank=True)
    description = models.CharField(max_length=500)
    props_info = models.CharField(max_length=500, null=True, blank=True)
    time_registered = models.DateTimeField(auto_now_add=True, blank=True)
    reminder_email = models.BooleanField(default=True)
    reminder_text = models.BooleanField(default=False)
    #in_show = models.BooleanField(default=False)

    secret = models.CharField(default=_generate_secret, max_length=40, unique=True)

    sent_reminder_email = models.BooleanField(default=False)
    sent_reminder_text = models.BooleanField(default=False)
    sent_slot_reminder_email = models.BooleanField(default=False)

    def full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    def __unicode__(self):
        return self.full_name()


class AuditionSession(models.Model):
    location = models.CharField(max_length=200)

    @property
    def start_time(self):
        start = self.auditionslot_set.order_by('start_time').first()
        return start.get_start_time() if start else None

    @property
    def last_time(self):
        end = self.auditionslot_set.order_by('start_time').last()
        return end.get_end_time() if end else None

    def remaining_slots_exist(self):
        six_hours_ahead = timezone.now() + datetime.timedelta(hours=6)
        return self.auditionslot_set.filter(start_time__gte=six_hours_ahead, auditioner=None).exists()

    def __unicode__(self):
        if not self.start_time or not self.last_time:
            return self.location

        start_time = timezone.localtime(self.start_time)
        last_time = timezone.localtime(self.last_time)

        return '{}, {} - {}'.format(self.location, start_time.strftime('%m/%d/%y %X'), last_time.strftime('%X') if last_time.date() == start_time.date() else last_time.strftime('%m/%d/%y %X'))


class AuditionSlot(models.Model):
    auditioner = models.OneToOneField('talentshow.Auditioner', null=True, blank=True, on_delete=models.SET_NULL)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    session = models.ForeignKey('talentshow.AuditionSession')

    @property
    def duration(self):
        return '{} minutes'.format((self.end_time - self.start_time).seconds / 60)

    @property
    def location(self):
        return self.session.location

    @property
    def auditioner_full_name(self):
        if self.auditioner:
            return self.auditioner.full_name
        else:
            return None

    def get_start_time(self):
        return self.start_time.astimezone(tz)

    def get_end_time(self):
        return self.end_time.astimezone(tz)

    def as_csv_dict(self):
        if self.auditioner:
            return {
                'Slot Time': timezone.localtime(self.start_time).strftime('%I:%M %p'),
                'First Name': self.auditioner.first_name,
                'Last Name': self.auditioner.last_name,
                'Email': self.auditioner.email,
                'Phone': self.auditioner.phone,
                'Act Description': self.auditioner.description,
                'Prop A/V Needs': self.auditioner.props_info,
            }
        else:
            return {
                'Slot Time': timezone.localtime(self.start_time).strftime('%I:%M %p'),
                'First Name': '',
                'Last Name': '',
                'Email': '',
                'Phone': '',
                'Act Description': '',
                'Prop A/V Needs': '',
            }


    def __unicode__(self):
        start_time = timezone.localtime(self.get_start_time())
        end_time = timezone.localtime(self.get_end_time())
        return '{} - {} at {}'.format(start_time.strftime('%m/%d/%y %X'), end_time.strftime('%X') if end_time.date() == start_time.date() else end_time.strftime('%m/%d/%y %X'), self.session.location)        


class AuditionSignUpReminder(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


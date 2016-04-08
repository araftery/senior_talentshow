import datetime, logging

import pytz

from django.conf import settings
from django.utils import timezone

from celery.task import task

from talentshow.utils.general import generate_audition_session_csv
from core.utils.general import send_html_email
from core.utils.general import send_text as send_text_utility
from core.utils.general import audition_signup_open
from talentshow.models import Auditioner, AuditionSignUpReminder, AuditionSession
from celery.task.schedules import crontab
from celery.decorators import periodic_task

logger = logging.getLogger(__name__)


@task
def send_email(template_name, subject, from_email, recipients, context, bcc=None, attachments=None):
    logger.info('Sending {} email to {}'.format(template_name, from_email))
    return send_html_email(template_name, subject, from_email, recipients, context, bcc, attachments)

@task
def send_text(template_name, recipient, context):
    logger.info('Sending {} text to {}'.format(template_name, recipient))
    return send_text_utility(template_name, recipient, context)

#@periodic_task(run_every=crontab(hour="*/2", minute=0))
def send_reminder_chooseslot_emails():
    if not audition_signup_open():
        return

    one_hour_ago = timezone.now() - datetime.timedelta(hours=1)
    auditioners = Auditioner.objects.filter(
        time_registered__lte=one_hour_ago,
        auditionslot=None,
        sent_slot_reminder_email=False
    )
    for auditioner in auditioners:
        send_email.delay(
            template_name='auditionslot_signup_reminder',
            subject='Reminder: Choose an audition slot',
            from_email=settings.HARVARD_TALENT_EMAIL,
            recipients=[auditioner.email],
            context={'auditioner': auditioner},
        )
        auditioner.sent_slot_reminder_email = True
        auditioner.save()

#@periodic_task(run_every=crontab(hour=19, minute=0))
def send_reminder_emails():
    tomorrow = timezone.now().date() + datetime.timedelta(1)
    next_day = tomorrow + datetime.timedelta(1)
    tomorrow_start = datetime.datetime.combine(tomorrow, datetime.time())
    tomorrow_end = datetime.datetime.combine(next_day, datetime.time())

    # get all of tomorrow's auditioners who asked for email
    # reminders
    auditioners = Auditioner.objects.filter(
        reminder_email=True,
        sent_reminder_email=False,
        auditionslot__start_time__gte=tomorrow_start,
        auditionslot__start_time__lte=tomorrow_end,
    )
    for auditioner in auditioners:
        send_email.delay(
            template_name='audition_reminder',
            subject='Reminder: Talent show audition tomorrow',
            from_email=settings.HARVARD_TALENT_EMAIL,
            recipients=[auditioner.email],
            context={'auditioner': auditioner},
        )
        auditioner.sent_reminder_email = True
        auditioner.save()


@periodic_task(run_every=crontab(hour="*/2", minute=0))
def send_reminder_texts():
    now = timezone.now()
    four_hours_ahead = now + datetime.timedelta(hours=4)

    # get all auditioners who want a reminder text, haven't yet been
    # sent one, and are auditioning within the next 4 hours
    auditioners = Auditioner.objects.filter(
        reminder_text=True,
        sent_reminder_text=False,
        auditionslot__start_time__gte=now,
        auditionslot__start_time__lte=four_hours_ahead,
    ).exclude(
        phone=None,
    )
    for auditioner in auditioners:
        send_text.delay(
            template_name='audition_reminder',
            recipient=auditioner.phone,
            context={'auditioner': auditioner},
        )
        auditioner.sent_reminder_text = True
        auditioner.save()


def send_signup_open_emails():
    people = AuditionSignUpReminder.objects.all()
    for person in people:
        send_email.delay(
            template_name='audition_signup_open',
            subject='Senior Talent Show Sign-Ups are Open!',
            from_email=settings.HARVARD_TALENT_EMAIL,
            recipients=[person.email],
            context={'person': person},
        )

@periodic_task(run_every=crontab(hour=7, minute=0))
def send_auditionsession_csv():
    sessions = AuditionSession.objects.all()
    now = timezone.now().astimezone(pytz.timezone('America/New_York'))
    attachments = []
    sessions_today = []
    for session in sessions:
        if session.start_time.date() != now.date():
            continue

        csvfile = generate_audition_session_csv(session)
        attachments.append(['audition_session_{}.csv'.format(session.start_time.strftime('%m-%d')), csvfile.getvalue(), 'text/csv'])
        sessions_today.append(session)

    if len(attachments) == 0:
        return 0
    elif len(attachments) > 1:
        for i, attachment in enumerate(attachments):
            attachment[0] = '{}-{}.csv'.format(attachment[0].replace('.csv', ''), i+1)

    send_email.delay(
        template_name='audition_csv',
        subject="Today's Talent Show Auditioners: {}".format(now.strftime('%m/%d')),
        from_email=settings.HARVARD_TALENT_EMAIL,
        recipients=[settings.HARVARD_TALENT_EMAIL],
        context={'sessions': sessions_today},
        bcc=[i[1] for i in settings.ADMINS],
        attachments=attachments,
    )

import textwrap

import pytz
from twilio.rest import TwilioRestClient
try:
    from premailer import transform
except:
    transform = lambda x: x

from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.conf import settings
from django.template.loader import get_template
from django.template import Context

from talentshow.models import AuditionSession


tz = pytz.timezone(settings.TIME_ZONE)
site = Site.objects.get_current()


def audition_signup_open():
    return any(i.remaining_slots_exist() for i in AuditionSession.objects.all())


def send_html_email(template_name, subject, from_email, recipients, context, bcc=None, attachments=None):
    if attachments is None:
        attachments = []
    plaintext = get_template('common/emails/{}.txt'.format(template_name))
    htmly = get_template('common/emails/{}.html'.format(template_name))
    context.update({'title': subject, 'SITE_URL': u'http://{}'.format(site.domain)})
    d = Context(context)

    reply_to_email = from_email

    text_content = plaintext.render(d)
    html_content = transform(htmly.render(d))
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipients, bcc=bcc, headers={'Reply-To': reply_to_email })
    msg.attach_alternative(html_content, "text/html")

    for attachment in attachments:
        msg.attach(*attachment)

    return msg.send()


def send_text(template_name, recipient, context):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token  = settings.TWILIO_AUTH_TOKEN
    client = TwilioRestClient(account_sid, auth_token)
    plaintext = get_template(u'common/texts/{}.txt'.format(template_name))
    d = Context(context)
    body = plaintext.render(d)
    bodies = textwrap.wrap(body, 160)
    for body in bodies:
        message = client.sms.messages.create(
        body=body,
        to=u"+1{0}".format(recipient),
        from_=settings.TWILIO_PHONE_NUMBER)

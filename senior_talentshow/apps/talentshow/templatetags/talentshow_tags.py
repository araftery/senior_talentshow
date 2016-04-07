from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def talentshow_email():
    email = settings.HARVARD_TALENT_EMAIL_ADDRESS
    cutoff = len(email)/3
    part1 = email[:cutoff]
    part2 = email[cutoff:]
    return '<span class="email">{}<span class="nospam">no_spam</span>{}</span>'.format(part1, part2)

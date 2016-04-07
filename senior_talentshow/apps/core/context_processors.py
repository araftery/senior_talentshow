from django.conf import settings
from django.contrib.sites.models import Site


site = Site.objects.get_current()


def debug(request):
    "Returns context variables helpful for debugging."
    context_extras = {}
    if settings.DEBUG:
        context_extras['debug'] = True
    return context_extras


def site_url(request):
    """
    Returns the current site url to the context
    """
    return {'SITE_URL': u'http://{}'.format(site.domain)}

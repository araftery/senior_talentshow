from django import template
from django.core.urlresolvers import resolve

import markdown

register = template.Library()

# usage: {% navactive request 'comma-separated-list,of-url-pattern-names,to-match'}
@register.simple_tag
def navactive(request, urls):
    if resolve(request.path).url_name in [url.strip() for url in urls.split(',')]:
        return "active"
    return ''

@register.filter(name='markdown')
def markdown_filter(value):
    return markdown.markdown(value)
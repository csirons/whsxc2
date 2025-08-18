from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_format(value):
    """
    Convert markdown text to HTML.
    Usage: {{ content|markdown }}
    """
    if value:
        # Configure markdown with common extensions
        md = markdown.Markdown(extensions=['extra', 'codehilite', 'tables'])
        html = md.convert(value)
        return mark_safe(html)
    return ''
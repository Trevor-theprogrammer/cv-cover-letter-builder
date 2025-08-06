from django import template

register = template.Library()

@register.filter
def scoreclass(score):
    """Return CSS class based on score value"""
    try:
        score = int(score)
        if score >= 80:
            return 'excellent'
        elif score >= 60:
            return 'good'
        else:
            return 'needs-improvement'
    except (ValueError, TypeError):
        return 'needs-improvement'

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    return dictionary.get(key, '')

@register.filter
def split_newlines(text):
    """Split text by newlines and return as list"""
    return text.split('\n') if text else []

from django import template
import datetime

register = template.Library()

@register.filter(name='duration_string')
def duration_string(duration):
    """

    """
    seconds = duration.seconds
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)

    hour = round(hour)
    min = round(min)
    sec = round(sec)

    if hour > 0:
        duration_string = f"{hour}h {min}m"
    else:
        duration_string = f"{min}m {sec}s"

    return duration_string

    return 'test'
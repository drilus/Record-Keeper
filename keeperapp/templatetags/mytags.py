import json
import os

from django import template

register = template.Library()


@register.filter
def loadjson(data):
    return json.loads(data)


@register.filter
def getfilename(value):
    return os.path.basename(value)

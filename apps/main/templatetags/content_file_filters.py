from django import template

register = template.Library()

@register.filter
def print_file_content(f):
    try:
        contents = ""
        for line in f:
            contents += line
            contents += "<br />"
        return contents
    except IOError:
        return ''

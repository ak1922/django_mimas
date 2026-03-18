from django import template
register = template.Library()


# Mask last four for ss
@register.filter(name='mask_ssn')
def mask_ssn(value):

    clean_ssn = str(value).replace('-', '')
    if len(clean_ssn) == 9:
        return f'***-**-{clean_ssn[-4:]}'
    return '****'

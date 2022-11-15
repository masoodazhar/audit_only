from django import template

register = template.Library()


@register.simple_tag(name='stringToArray')
def stringToArray(value):
    try:
        return value.split(',')
    except:
        return ['No data found']
register.filter('stringToArray', stringToArray)


@register.simple_tag(name='get_value_from')
def get_value_from(value,index):
    return str(value[index])
register.filter('get_value_from', get_value_from)

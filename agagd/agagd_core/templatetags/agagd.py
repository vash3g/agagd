from django import template
from django.core.urlresolvers import reverse
from django.template import TemplateSyntaxError
import json

register = template.Library()

@register.simple_tag(takes_context=True)
def async_table(context, table_id, url_name=None, remote_url=None, **kwargs):
    if '_async_table' not in context:
        context['_async_table'] = set()

    if table_id in context['_async_table']:
        raise TemplateSyntaxError('Duplicated async_table id: %s' % table_id)
    else:
        context['_async_table'].add(table_id)

    if all([url_name, remote_url]) or not any([url_name, remote_url]):
        raise TemplateSyntaxError('You must set url_name or remote_url - not both or none.')

    remote_url = remote_url or reverse(url_name)
    if kwargs:
        extra_parameters = 'extra_parameters: %s,' % json.dumps(kwargs)
    else:
        extra_parameters = ''
    return '''
        <script>
            $.async_table.init({{
                id: "{table_id}",
                {extra_parameters}
                remote_url: "{remote_url}"
            }});
        </script>
        <div id="{table_id}"></div>
    '''.format(table_id=table_id, remote_url=remote_url, extra_parameters=extra_parameters)

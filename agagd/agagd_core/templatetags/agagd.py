from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def async_table(table_id, remote_view):
    remote_url = reverse(remote_view)
    return '''
        <script>
            $.async_table.init({{
                id: "{table_id}",
                remote_url: "{remote_url}"
            }});
        </script>
        <div id="{table_id}"></div>
    '''.format(table_id=table_id, remote_url=remote_url)

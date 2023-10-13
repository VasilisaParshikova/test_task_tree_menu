from urllib import request

from django import template
from app.models import MenuItem
from django.utils.html import format_html

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    menu_items = MenuItem.objects.filter(name=menu_name).get_descendants(include_self=True)
    request = context['request']
    if request.GET:
        flag = False
        name_list = request.GET.getlist('name')
        level_list = request.GET.getlist('level')
        item_id_list = request.GET.getlist('id')
        if name_list is None:
            name_list = [menu_name]
            item_id_list = [0]
            level_list = [0]
            index = 0
        elif menu_name not in name_list:
            index = len(name_list)
            item_id_list.append(0)
            level_list.append(0)
            name_list.append(menu_name)
        else:
            index = name_list.index(menu_name)
    else:
        name_list = [menu_name]
        item_id_list = [0]
        level_list = [0]
        index = 0
        flag = True
    item_id = item_id_list[index]
    level = level_list[index]
    printed_id = []
    def render_menu_items(items):
        nonlocal flag
        nonlocal item_id
        nonlocal level
        html = ""
        for point in items:
            if point.id not in printed_id:
                printed_id.append(point.id)
                if point.children.count():
                    html += '<li> <details '
                    if point.level < int(level) or (point.id == int(item_id)):
                        html += 'open'
                    html += '>'
                    if flag:
                        html += f'<summary> <a href="?name={menu_name}&id={point.id}&level={point.level}">{point.name}</a></summary>'
                    else:
                        nonlocal level_list
                        nonlocal name_list
                        nonlocal item_id_list
                        nonlocal index
                        level_list[index] = point.level
                        item_id_list[index] = point.id
                        ref_str = ''
                        for i in range(len(name_list)):
                            ref_str += f'name={name_list[i]}&'
                        for i in range(len(name_list)):
                            ref_str += f'id={item_id_list[i]}&'
                        for i in range(len(name_list)):
                            ref_str += f'level={level_list[i]}&'
                        ref_str = ref_str[:-1]
                        html += f'<summary><a href="?{ref_str}">{point.name}</a></summary>'

                    html += '<ul>'
                    html += render_menu_items(point.children.all())
                    html += '</ul>'
                else:
                    if flag:
                        html += f'<li> <a href="?name={menu_name}&id={point.id}&level={point.level}">{point.name}</a>'
                    else:
                        level_list[index] = point.level
                        item_id_list[index] = point.id
                        ref_str = ''
                        for i in range(len(name_list)):
                            ref_str += f'name={name_list[i]}&'
                        for i in range(len(name_list)):
                            ref_str += f'id={item_id_list[i]}&'
                        for i in range(len(name_list)):
                            ref_str += f'level={level_list[i]}&'
                        ref_str = ref_str[:-1]
                        html += f'<li> <a href="?{ref_str}">{point.name}</a>'
                html += '</li>'
        return html
    html_str = f'<ul>{render_menu_items(menu_items)}</ul>'
    return format_html(html_str)

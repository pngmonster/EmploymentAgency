from django import template

register = template.Library()

@register.inclusion_tag('partials/file_field.html')
def file_field(field, icon='📎', preview_type='none', current_url=''):
    """
    Рендерит красивый кастомный file input.
    preview_type: 'none' | 'avatar' | 'logo' | 'pdf'
    current_url: URL текущего файла если уже загружен
    """
    return {
        'field': field,
        'icon': icon,
        'preview_type': preview_type,
        'current_url': current_url,
    }

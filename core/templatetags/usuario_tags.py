from django import template

register = template.Library()


@register.simple_tag
def perfil_usuario(user):
    if user.is_superuser:
        return "Administrador"

    grupo = user.groups.first()

    if grupo:
        return grupo.name

    return "Sem perfil"
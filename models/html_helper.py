# -*- coding: utf-8 -*-

# for ide
if False:
    from gluon import I, SPAN, BR, DIV, A, TABLE, URL, H4, CENTER
    from gluon import request, redirect
    from gluon import SQLFORM
    from log import log


def icon_title(icon, title):
    return I(f' {str(title)}', _class=f'fa {str(icon)} fa-1x')


# iconos en https://fontawesome.com/v4.7.0/icon/list
def grand_button(nombre, link, icono, **kwargs):
    """ nombre: 1 a 3 palabras"""
    lista = nombre.split()
    spanlist = []
    for i in lista:
        spanlist.append(SPAN(i.title()))
        spanlist.append(BR())
    result = DIV(spanlist)
    if 'vars' in kwargs:
        url = URL(link, vars=kwargs['vars'])
    else:
        url = URL(link)
    boton = A(TABLE(I(_class='fa ' + str(icono) + ' fa-3x'), result),
              _class="btn-square-blue",
              _href=url)
    return boton


def opt_tabla(tabla):
    if tabla == 'cliente':
        fields = ('db.cliente.id, db.cliente.nombre,' +
                  'db.cliente.razon_social,' + 'db.cliente.lista,' +
                  'db.cliente.saldo, db.cliente.tipocuenta, db.cliente.cuit')
    else:
        fields = 'None'
    return {'fields': fields}


def admin_tabla():
    if 'tabla' in request.vars:
        tabla = request.vars['tabla']
        titulo = DIV(
            A(icon_title('fa-arrow-left', 'Volver'), _id='boton_r',
              _class="btn-grid", _href=URL('admin')),
            CENTER(H4('Admin ' + (str(tabla).title()))))
        log('acceso grid ' + str(tabla))
        grid = SQLFORM.smartgrid(eval('db.' + str(tabla)),
                                 maxtextlength=20,
                                 linked_tables=['child'],
                                 fields=eval(opt_tabla(tabla)['fields']))
        return dict(grid=grid, titulo=titulo)
    else:
        redirect(URL('index'))

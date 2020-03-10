# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# for ide
if False:
    from db import db
    from gluon import response, request, auth, cache
    from gluon import HTTP, CENTER, FORM, DIV, I
    from gluon import SQLFORM
    from log import log
    from html_helper import grand_button

# ---- example index page ----

def index():
    log('acceso')
    # menu favoritos
    form = CENTER(FORM(
        DIV(I(' Personal', _class='fa fa-ticket fa-2x',
            _id='tit_minigrid'),
            DIV(grand_button('empleados',
                             'admin_tabla',
                             'fa-cart-plus'),
                grand_button('ver marcadas',
                             'admin_tabla',
                             'fa-th-large'),
                grand_button('informe mes empleado',
                             'informe_mes_empleado',
                             'fa-truck'),
                _id='mini_grid'),
            _id='indexdiv'),
        DIV(I(' Produccion', _class='fa fa-industry fa-2x',
              _id='tit_minigrid'),
            DIV(grand_button('ingreso productos terminados',
                             'ingreso_produccion',
                             'fa-database'),
                grand_button('consulta productos',
                             'consulta_ingreso_stock',
                             'fa-list'),
                grand_button('Ingreso materias primas',
                             'admin_tabla',
                             'fa-qrcode',
                             vars={'tabla': 'mat_primas'}),
                _id='mini_grid'),
            _id='indexdiv'),
        DIV(I(' Compras', _class='fa fa-shopping-bag fa-2x',
              _id='tit_minigrid'),
            DIV(grand_button('ingreso productos terminados',
                             'ingreso_produccion',
                             'fa-database'),
                grand_button('consulta productosNN',
                             'consulta_ingreso_stock',
                             'fa-list'),
                grand_button('Ingreso materias primasNN',
                             'admin_tabla',
                             'fa-qrcode',
                             vars={'tabla': 'mat_primas'}),
                _id='mini_grid'),
            _id='indexdiv'),
        DIV(I(' Contabilidad', _class='fa fa-calculator fa-2x',
              _id='tit_minigrid'),
            DIV(grand_button('IngresosNN',
                             'ingresos',
                             'fa-download'),
                grand_button('EgresosNN',
                             'consulta_ingreso_stock',
                             'fa-upload'),
                grand_button('ConsultaNN',
                             'admin_tabla',
                             'fa-university',
                             vars={'tabla': 'mat_primas'}),
                _id='mini_grid'),
            _id='indexdiv'),
        _id='panel_grid'))
    return dict(form=form)

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

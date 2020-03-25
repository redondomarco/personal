# -*- coding: utf-8 -*-

import csv
import string
import random
from babel.dates import format_date, format_datetime, format_time

# for ide
if False:
    from db import configuration
    from log import log
    from empleados import datetime
    from gluon import MARKMIN, A, URL, DIV, XML
    from gluon import session


valid_chars1 = (string.ascii_uppercase + string.digits +
                string.ascii_lowercase)


files_dir = 'applications/' + str(configuration.get('app.name')) + '/files/'


def idtemp_generator(size=50, chars=valid_chars1):
    """genero id random con marca de tiempo"""
    dia = (str(datetime.datetime.now().year) + '-' +
           str(datetime.datetime.now().month) + '-' +
           str(datetime.datetime.now().day) + '_')
    return dia + ''.join(random.choice(chars) for _ in range(size))


def list_of_dict_to_csv(nombre, lista, **kwargs):
    """recibe nombre y una lista de dicts y lo graba en disco
    devuelve string nombre+hash python2"""
    nombre_archivo = (str(nombre) + '_' + str(idtemp_generator(10)) +
                      '.csv')
    try:
        if ('orden' in kwargs):
            keys = kwargs['orden']
        else:
            keys = lista[0].keys()
        # log(keys)
    except Exception as e:
        log('error con lista longitud ' + str(len(lista)) + ' ' + str(e))
        return ['error', e.args]
    try:
        path_completo = files_dir + 'csv/' + nombre_archivo
        with open(path_completo, 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(lista)
            log('generado ' + path_completo)
            return ['ok', nombre_archivo]
    except Exception as e:
        log('error lod_tocsv ' + str(e))
        return ['error', e.args]


def list_dict_to_table_sortable(lista, nombre_archivo):
    '''recibe una lista de diccionarios(clave-valor iguales)
    y devuelve una tabla html'''
    if type(lista) == list:
        if type(lista[0]) == dict:
            claves = lista[0].keys()
            orden = ['dni', 'usuario', 'apellido y nombre', 'apellido',
                     'nombre', 'nombre map', 'baja map', 'reparticion',
                     'Unif', 'Unif_creado', 'Unif_modificado']
            for i in reversed(orden):
                try:
                    claves.insert(0, claves.pop(claves.index(i)))
                except Exception:
                    pass
                    # log(e)
            # cabecera tabla
            tabla = '<table data-toggle="table"> <thead> <tr>'
            for i in claves:
                fila = """<th data-field="%s" data-sortable="true">
                       %s</th>""" % (i, i)
                tabla = tabla + fila
            tabla = tabla + '</tr> </thead> <tbody>'
            # contenido tabla
            for i in lista:
                tabla = tabla + '<tr>'
                for j in claves:
                    tabla = tabla + '<td>%s</td>' % (i[j])
                tabla = tabla + '</tr>'
            tabla = tabla + '</tbody> </table>'
            cantidad = len(lista)
            leyenda_cantidad = (MARKMIN("Cantidad de dias registrados: " +
                                str(cantidad)))
            session.nombre_archivo = list_of_dict_to_csv(
                nombre_archivo, lista)[1]
            # open_archivo = open(dir_files + session.nombre_archivo, "r")
            boton_csv = A('Descarga tabla como CSV...',
                          _href=URL('descarga_csv'),
                          _class='btn btn-default')
            # return CENTER(TABLE(boton_csv,XML(tabla)))
            return DIV(boton_csv, leyenda_cantidad, XML(tabla))


def fecha_sp(datetime):
    fecha = datetime.date()
    return format_date(fecha, locale='es')


def datetime_sp(datetime):
    return format_datetime(datetime, locale='es')


def time_sp(datetime):
    time = datetime.time()
    return format_time(time, locale='es')


def s_horario(horario):
    return f'{time_sp(horario[0])} a {time_sp(horario[1])}'

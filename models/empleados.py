# -*- coding: utf-8 -*-

# for ide
if False:
    from gluon import Field, auth
    from gluon.validators import IS_IN_SET
    from db import db
    from fuente_datos import marcadas_tunel_latix

dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves',
               'Viernes', 'Sabado']

db.define_table(
    'marcadas',
    Field('id_reg'),
    Field('user_code'),
    Field('datetime'),
    Field('bkp_type'),
    Field('type_code'),
    Field('huella', unique=True, length=40)
)

db.define_table(
    'empleado',
    Field('Nombre', length=255),
    Field('Apellido', length=255),
    Field('user_code', 'integer', unique=True, length=4),
    Field('dias'),
    Field('entrada', 'time'),
    Field('salida', 'time'),
    Field('descanso', 'time'),
    auth.signature,
    format='%(Nombre)s %(Apellido)',
)
db.empleado.dias.requires = IS_IN_SET(dias_semana, multiple=True)


def huella(id_reg, user_code, datetime, bkp_type, type_code):
    salida = (str(id_reg) +
              str(user_code) +
              str(datetime.isoformat()) +
              str(bkp_type) +
              str(type_code))
    return salida


# actualizo marcadas
def actualizo_marcadas():
    marcadas = marcadas_tunel_latix()
    for registro in marcadas:
        huellagen = huella(registro[0], registro[1], registro[2],
                           registro[3], registro[4])
        marcada = {'id_reg': registro[0],
                   'user_code': registro[1],
                   'datetime': registro[2],
                   'bkp_type': registro[3],
                   'type_code': registro[4],
                   'huella': huellagen}
        if db(db.marcadas.huella == huellagen).select().first():
            pass
        else:
            db['marcadas'].insert(**marcada)
    db.commit()

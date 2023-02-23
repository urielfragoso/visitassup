from odoo import fields, api, models, _
from odoo.exceptions import UserError, ValidationError


class planvisita(models.Model):
    _name = 'visitas.cd.visitadores'
    _description = 'Tabla que guarda el listado de visitadores'
    _rec_name = 'refidusuario'


    refidusuario = fields.Many2one(comodel_name='res.users', string='Asesor Asignado', domain=[("direccionuser_id", '=', 4)])
    estatus = fields.Boolean()
    no_visitador = fields.Char()
    no_notificador = fields.Char()




class fraccionesvisita(models.Model):
    _name='visitas.cd.fracciones'
    _description = 'Tabla que contiene las fracciones del plan de visita'

    fraccion = fields.Char()
    estatus = fields.Boolean(default=True)


class atencionfinalinm(models.Model):
    _name='visitas.cd.atencionfinal'
    _description ='Catalogo de atencion final para asociarlos al inmueble'

    nombre_atencion = fields.Char()
    estatus = fields.Boolean(default=True)

class cuotasrecuperacion(models.Model):
    _name = 'visitas.cuotas.recuperacion'
    _description = 'Se almacenran los proyectos por isntitución'

    rev_id_plan = fields.Many2one('visitas.plan.visita')
    proyecto = fields.Char()
    estuio_cuotas = fields.Char()
    tabulador = fields.Char()
    montos  = fields.Char()
    exentos = fields.Char()
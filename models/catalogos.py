from odoo import fields, api, models, _
from odoo.exceptions import UserError, ValidationError


class planvisita(models.Model):
    _name = 'visitas.cd.visitadores'
    _description = 'Tabla que guarda el listado de visitadores'
    _rec_name = 'refidusuario'


    refidusuario = fields.Many2one(comodel_name='res.users', string='Asesor Asignado', domain=[("direccionuser_id", '=', 4)])
    estatus = fields.Boolean()
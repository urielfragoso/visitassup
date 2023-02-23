from odoo import fields,api,models,_
from odoo.exceptions import UserError, ValidationError



class inmueblesvisitas(models.Model):
    _name='visitas.inmuebles'
    _rec_name = 'establecimiento'

    idiap = fields.Many2one(comodel_name='res.partner',
                            domain=[('is_IAP', '=', True), ('estatus_id', 'in', [1, 2, 4, 5])])

    establecimiento = fields.Char()
    noiap = fields.Char(related="idiap.no_iap")
    atencion_final = fields.Char(string="Especialidad")
    id_visitasinmueble = fields.Char()









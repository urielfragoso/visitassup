from odoo import fields,api,models,_
from odoo.exceptions import UserError, ValidationError



class planvisita(models.Model):
    _name='visitas.plan.visita'
    _description = 'Tabla que guarda datas del plan de visita de registrada'
    _rec_name = 'idiap'



    refid_visita = fields.Many2one(comodel_name='visitas.programacion')
    idiap = fields.Many2one(related="refid_visita.idiap", store=True)
    fecha_elaboracion = fields.Date()



    def btn_documento1(self):
        for record in self:
            record.id
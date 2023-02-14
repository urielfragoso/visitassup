from odoo import fields,api,models,_
from odoo.exceptions import UserError, ValidationError



class planvisita(models.Model):
    _name='visitas.orden.comision.visita'
    _description = 'Tabla que guarda datos del documento de orden de visit ay comision'
    _rec_name = 'idiap'



    refid_visita = fields.Many2one(comodel_name='visitas.programacion')
    idiap = fields.Many2one(related="refid_visita.idiap", store=True)
    fecha_elaboracion = fields.Date()
    nooficio = fields.Char()
    novisitasiap = fields.Integer()




    def btn_documento2(self):
        for record in self:
            record.id
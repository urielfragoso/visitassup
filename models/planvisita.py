from odoo import fields,api,models,_
from odoo.exceptions import UserError, ValidationError



class planvisita(models.Model):
    _name='visitas.plan.visita'
    _description = 'Tabla que guarda datas del plan de visita de registrada'
    _rec_name = 'idiap'



    refid_visita = fields.Many2one(comodel_name='visitas.programacion')
    idiap = fields.Many2one(related="refid_visita.idiap", store=True)
    refid_domicilios =  fields.Many2one(comodel_name='cd.domicilios')
    fecha_elaboracion = fields.Date()
    articulo_servasis = fields.Char()
    articulo_perfilpob = fields.Char()
    tipo_domicilio = fields.Selection([('1','OPERATIVO'),
                                       ('2','FISCAL'),
                                       ('3','OTRO')])

    refid_visitador = fields.Many2many(comodel_name='visitas.cd.visitadores', domain=[("estatus", '=', True)])
    refid_fracciones = fields.Many2many(comodel_name='visitas.cd.fracciones', domain=[("estatus", '=', True)])


    def btn_documento1(self):
        for record in self:
            record.id
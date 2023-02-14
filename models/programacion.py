from odoo import fields,api,models,_
from odoo.exceptions import UserError, ValidationError

class programacionvisita(models.Model):
    _name='visitas.programacion'
    _description = 'visitas programadas por institucion'
    _rec_name = 'idiap'

    idiap = fields.Many2one(comodel_name='res.partner', domain=[('is_IAP','=',True),('estatus_id','in',[1,2,4,5])])
    fecha_programacion = fields.Date("Fecha de visita")
    noiap = fields.Char()
    estatus = fields.Selection([('pendiente','Pendiente'),
                                ('programada','Visita Programada')])



    @api.model
    def create(self, vals):
        vidiap = vals['idiap']
        filtro = [('id','=',vidiap)]
        vnoiap_obj = self.env['res.partner'].sudo().search(filtro)

        vals['noiap'] = vnoiap_obj.no_iap
        vals['estatus'] = 'pendiente'

        return super(programacionvisita, self).create(vals)

    #FUNCION QUE GENERA LA PANTALL DE CAPTURA DEL PLAN DE VISITA
    def btn_planvisita(self):
        for record in self:
            filtro_visita = [('refid_visita','=',self.id),
                             ('idiap','=',self.idiap.id)]

            plan_visita_obj = self.env['visitas.plan.visita'].sudo().search(filtro_visita)

            return {"view_mode": "[form]",
                    "res_model": "visitas.plan.visita",
                    "type": "ir.actions.act_window",
                    "target": "new",
                    "name": ('Generar documento de Plan de visita'),
                    'res_id': plan_visita_obj.id if plan_visita_obj else False,
                    "views": [(self.env.ref('visitassup.visitas_plan_visita_form_view').id, "form")],
                    "context": {'default_refid_visita': self.id,
                                'default_idiap': self.idiap.id},

                    "domain": [('refid_visita', '=', self.id),
                               ('idiap', '=', self.idiap.id)]}


    def btn_ordenvisita(self):
        for record in self:

            filtro_visita = [('refid_visita', '=', self.id),
                             ('idiap', '=', self.idiap.id)]

            orden_visita_obj = self.env['visitas.orden.comision.visita'].sudo().search(filtro_visita)

            return {"view_mode": "[form]",
                    "res_model": "visitas.orden.comision.visita",
                    "type": "ir.actions.act_window",
                    "target": "new",
                    "name": ('Generar documento de Orden de visita y comisión'),
                    'res_id': orden_visita_obj.id if orden_visita_obj else False,
                    "views": [(self.env.ref('visitassup.visitas_orden_comision_visita_form_view').id, "form")],
                    "context": {'default_refid_visita': self.id,
                                'default_idiap': self.idiap.id},

                    "domain": [('refid_visita', '=', self.id),
                               ('idiap', '=', self.idiap.id)]}


    def btn_documento3(self):
        for record in self:
            record.id

    def btn_documento4(self):
        for record in self:
            record.id
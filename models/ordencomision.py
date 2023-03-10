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
    reviso = fields.Many2one(comodel_name='res.users', string="Revisó")
    coordinator = fields.Many2one(comodel_name="res.users", string="Coordinador")

    fechanow=fields.Char(compute="_get_fecha_formato")
    fechaformatvisita = fields.Char(compute="_get_fecha_formato_visita")
    visitadores = fields.Char(compute="_get_visitadores")
    folio_noti = fields.Char(compute="_get_folio_noti")
    coordinaodor = fields.Char(compute="_get_nombre_coordinador")
    c_email  = fields.Char(compute="_get_nombre_coordinador_email")
    usu_creo = fields.Char(compute="_get_nombre_usuario")
    usu_email  = fields.Char(compute="_get_nombre_usuario_email")
    domicilio = fields.Char(compute="_direccion")
    fechaformatvigencia = fields.Char(compute="_get_fecha_formato_vigencia")



    def btn_oordencomision(self):
        return self.env.ref('visitassup.orden_visitas_report').report_action(self)

    def _get_fecha_formato(self):
        for record in self:
            format_fecha = record.fecha_elaboracion.strftime("%d de %B del %Y")
        record.fechanow = format_fecha

    def _get_fecha_formato_visita(self):
        for record in self:
            format_fecha_v = record.refid_visita.fecha_programacion.strftime("%d de %B del %Y")
        record.fechaformatvisita = format_fecha_v

    def _get_visitadores(self):
        for record_v in self:
            usuarios = self.env['visitas.plan.visita'].sudo().search([('id', '=', self.refid_visita.id)])
            record_v.visitadores = usuarios.vistador

    def _get_folio_noti(self):
        vuelta_folio = 0
        almecena_folio_1 = ''
        for record_v in self:
            folio_vi = self.env['visitas.plan.visita'].sudo().search([('id', '=', self.refid_visita.id)])
            for recordvisitador in folio_vi.refid_visitador.ids:
                usuario = self.env['visitas.cd.visitadores'].sudo().search([('id', '=', recordvisitador)])
                almecena_folio = usuario.no_visitador
                if vuelta_folio == 0:
                    almecena_folio_1 = almecena_folio
                    vuelta_folio = 1
                else:
                    almecena_folio_1 = almecena_folio_1 + ', ' + almecena_folio + '\n'

            record_v.folio_noti = almecena_folio_1

    def _get_nombre_coordinador(self):
        for record in self :
            record.coordinaodor =self.coordinator.display_name

    def _get_nombre_coordinador_email(self):
        for record in self :
            record.c_email =self.coordinator.email

    def _get_nombre_usuario(self):
        for record in self :
            record.usu_creo =self.create_uid.display_name

    def _get_nombre_usuario_email(self):
        for record in self :
            record.usu_email =self.create_uid.email

    def _direccion(self):
        for record_v in self:
            domicilio = self.env['visitas.plan.visita'].sudo().search([('id', '=', self.refid_visita.id)])
            record_v.domicilio = domicilio.refid_domicilio.establecimiento

    def _get_fecha_formato_vigencia(self):
        for record in self:
            format_fecha_vigencia = record.refid_visita.fecha_vigencia.strftime("%d de %B del %Y")
        record.fechaformatvigencia = format_fecha_vigencia

    def get_fraccion1(self):
        result = []
        f1 = 0
        folio_vi = self.env['visitas.plan.visita'].sudo().search([('id', '=', self.refid_visita.id)])
        for record_fraccionid in folio_vi.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 1:
                f1 = 1

        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f1):
                if record_id_plan.id == 1:
                    if f1 == 1:
                        fraccion = 'I,'
                        f1 = 0
                result.append(fraccion)
        return result

    def get_fraccion2(self):
        result = []
        f2 = 0
        folio_vi = self.env['visitas.plan.visita'].sudo().search([('id', '=', self.refid_visita.id)])
        for record_fraccionid in folio_vi.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 2:
                f2 = 2

        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f2):
                if record_id_plan.id == 2:
                    if f2 == 2:
                        fraccion2 = 'II,'
                        f2 = 0
                result.append(fraccion2)
        return result

    def get_fraccion3(self):
        result = []
        f3 = 0
        folio_vi = self.env['visitas.plan.visita'].sudo().search([('id', '=', self.refid_visita.id)])
        for record_fraccionid in folio_vi.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 3:
                f3 = 3

        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f3):
                if record_id_plan.id == 3:
                    if f3 == 3:
                        fraccion3 = 'III,'
                        f3 = 0
                result.append(fraccion3)
        return result

    def get_fraccion4(self):
        result = []
        f4 = 0
        folio_vi = self.env['visitas.plan.visita'].sudo().search([('id', '=', self.refid_visita.id)])
        for record_fraccionid in folio_vi.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 4:
                f4 = 4

        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f4):
                if record_id_plan.id == 4:
                    if f4 == 4:
                        fraccion4 = 'IV,'
                        f4 = 0
                result.append(fraccion4)
        return result

    def get_fraccion5(self):
        result = []
        f5 = 0
        folio_vi = self.env['visitas.plan.visita'].sudo().search([('id', '=', self.refid_visita.id)])
        for record_fraccionid in folio_vi.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 5:
                f5 = 5

        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f5):
                if record_id_plan.id == 5:
                    if f5 == 5:
                        fraccion5 = 'V,'
                        f5 = 0
                result.append(fraccion5)
        return result

    def get_fraccion6(self):
        result = []
        f6 = 0
        folio_vi = self.env['visitas.plan.visita'].sudo().search([('id', '=', self.refid_visita.id)])
        for record_fraccionid in folio_vi.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 6:
                f6 = 6
        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f6):
                if record_id_plan.id == 6:
                    if f6 == 6:
                        fraccion6 = 'VI,'
                        f6 = 0
                result.append(fraccion6)
        return result

    def get_fraccion7(self):
        result = []
        f7 = 0
        folio_vi = self.env['visitas.plan.visita'].sudo().search([('id', '=', self.refid_visita.id)])
        for record_fraccionid in folio_vi.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 7:
                f7 = 7

        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f7):
                if record_id_plan.id == 7:
                    if f7 == 7:
                        fraccion7 = 'VII,'
                        f7 = 0
                result.append(fraccion7)
        return result

    def get_fraccion8(self):
        result = []
        f8 = 0
        folio_vi = self.env['visitas.plan.visita'].sudo().search([('id', '=', self.refid_visita.id)])
        for record_fraccionid in folio_vi.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 8:
                f8 = 8

        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f8):
                if record_id_plan.id == 8:
                    if f8 == 8:
                        fraccion8 = 'VIII'
                        f8 = 0
                result.append(fraccion8)
        return result
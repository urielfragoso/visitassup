from odoo import fields,api,models,_
from odoo.exceptions import UserError, ValidationError
from PIL import Image
import requests


class planvisita(models.Model):
    _name='visitas.plan.visita'
    _description = 'Tabla que guarda datas del plan de visita de registrada'
    _rec_name = 'idiap'



    refid_visita = fields.Many2one(comodel_name='visitas.programacion')
    idiap = fields.Many2one(related="refid_visita.idiap", store=True)
    noiap = fields.Char(related="refid_visita.noiap", store=True)


    refid_domicilio =  fields.Many2one(comodel_name='visitas.inmuebles')



    fecha_elaboracion = fields.Date()
    articulo_servasis = fields.Char()
    articulo_perfilpob = fields.Char()
    tipo_domicilio = fields.Selection([('1','LEGAL'),
                                       ('2','OPERATIVO'),
                                       ('3','LEGAL / OPERATIVO'),
                                       ('4','OTRO')])

    refid_visitador = fields.Many2many(comodel_name='visitas.cd.visitadores', domain=[("estatus", '=', True)])
    refid_fracciones = fields.Many2many(comodel_name='visitas.cd.fracciones', domain=[("estatus", '=', True)])

    ref_cuotas = fields.One2many('visitas.cuotas.recuperacion','rev_id_plan')

    tipo_visita = fields.Selection([('1', 'VISITA DE SUPERVISIÓN'),
                                    ('2', 'VISITA DE INSPECCIÓN')],default="1")

    director_representante = fields.Char()
    objeto_social = fields.Text()
    estatuto_asistencial = fields.Char()
    vista_asistencial = fields.Char()
    estatuto_poblacion = fields.Char()
    vista_poblacion = fields.Char()

    sueldos  = fields.Char()
    asimilados  = fields.Char()
    honoraios  = fields.Char()
    voluntarios  = fields.Char()
    social  = fields.Char()
    otros  = fields.Char()
    resultado = fields.Text()
    vistador = fields.Char(compute="_get_nombres_visitadores")
    establecimiento = fields.Char(compute="_get_tipo_establecimiento")
    tipovisita_su = fields.Char(compute="_get_tipo_visita_super")
    tipovisita_ins = fields.Char(compute="_get_tipo_visita_inspe")
    fechaformatela = fields.Char(compute="_get_fecha_formato")
    fechaformavisi = fields.Char(compute="_get_fecha_formato_visita")
    directores = fields.Char(compute="_get_directores")
    objetoasiste = fields.Char(compute="_get_objeto_asistencial")
    actasistencial  = fields.Char(compute="_get_asistencial")

    def doc_planvisita(self):
        return self.env.ref('visitassup.plan_visitas_report').report_action(self)

    def _get_nombres_visitadores(self):
        almecena = ''
        vuelta = 0
        for record in self:
            id_visitador = record.refid_visitador.ids
            for recordvisitador in id_visitador:
                usuario = self.env['visitas.cd.visitadores'].sudo().search([('id', '=', recordvisitador)])
                almecena = usuario.refidusuario.name
                if vuelta == 0:
                    almancen_1 = almecena + '(inip)'
                    vuelta = 1
                else:
                    almancen_1 = almancen_1 + ', ' + almecena+ '(inip)'

            record.vistador = almancen_1

    def _get_tipo_establecimiento(self):
        for record in self:
            if self.tipo_domicilio == '1':
                record.establecimiento = 'LEGAL'
            elif self.tipo_domicilio == '2':
                record.establecimiento = 'OPERATIVO'
            elif self.tipo_domicilio == '3':
                record.establecimiento = 'LEGAL / OPERATIVO'
            elif self.tipo_domicilio == '4':
                record.establecimiento = 'OTRO'

    def _get_tipo_visita_super(self):
        for record in self:
            if self.tipo_visita == "1":
                record.tipovisita_su = "X"
            elif self.tipo_visita == "2":
                record.tipovisita_su = ""

    def _get_tipo_visita_inspe(self):
        for record in self:
            if self.tipo_visita == "1":
                record.tipovisita_ins = ""
            elif self.tipo_visita == "2":
                record.tipovisita_ins = "X"

    def _get_fecha_formato(self):
        for record in self:
            format_fecha = record.fecha_elaboracion.strftime("%d de %B del %Y")
        record.fechaformatela = format_fecha

    def _get_fecha_formato_visita(self):
        for record in self:
            fromat_fecha = self.refid_visita.fecha_programacion.strftime("%d de %B del %Y")
        record.fechaformavisi = fromat_fecha

    def _get_directores(self):
        for record in self:
            filtro = self.idiap.id
            usuario = self.env['directores'].sudo().search([('partner_id', '=', filtro)])
            if bool(usuario.primernombre):
                v_primernombre = usuario.primernombre
            else:
                v_primernombre = ''

            if bool(usuario.segundonombre):
                v_segundonombre = usuario.segundonombre
            else:
                v_segundonombre = ''
            if bool(usuario.primerapellido):
                v_primerapellido = usuario.primerapellido
            else:
                v_primerapellido = ''

            if bool(usuario.segundoapellido):
                v_segundoapellido = usuario.segundoapellido
            else:
                v_segundoapellido = ''

            directores_ = v_primernombre + ' ' + v_segundonombre + ' ' + v_primerapellido + ' ' + v_segundoapellido
        record.directores = directores_

    def _get_objeto_asistencial(self):
        for record in self:
            filtro = self.idiap.id
            objeto = self.env['objetoasistencial'].sudo().search([('partner_id', '=', filtro)])
            objasistencial = objeto.objetoiap
        record.objetoasiste = objasistencial

    def _get_asistencial(self):
        for record in self:
            filtro = self.idiap.id
            objeto = self.env['actividad.asistencial.estatutos'].sudo().search([('partner_id', '=', filtro)])
            objasistencial = objeto.actividad
        record.actasistencial = objasistencial

    def get_patronatoword(self):
        filtro_patronato = [('partner_id', '=', self.idiap.id),
                            ('estatus_patrono', '=', 'AC')]
        patronato_iap = self.env['patronosiap'].sudo().search(filtro_patronato)
        result = []
        for record in patronato_iap:
            if record.segundonombre:
                vsegundonombre = record.segundonombre
            else:
                vsegundonombre = ""
            if record.apellidopaterno:
                vprimerapellido = record.apellidopaterno
            else:
                vprimerapellido = ""
            if record.apellidomaterno:
                vsegundoapellido = record.apellidomaterno
            else:
                vsegundoapellido = ""
            result.append(
                record.refidpuesto.descripcion + "-      " + record.primernombre + " " + vsegundonombre + " " + vprimerapellido + " " + vsegundoapellido + '(inip)')
        return result

    def get_fraccion1(self):
        result = []
        f1 = 0
        for record_fraccionid in self.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 1:
                f1 = 1

        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f1):
                if record_id_plan.id == 1:
                    if f1 == 1:
                        fraccion = 'X'
                        f1 = 0
                result.append(fraccion)
        return result

    def get_fraccion2(self):
        result = []
        f2 = 0
        for record_fraccionid in self.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 2:
                f2 = 2

        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f2):
                if record_id_plan.id == 2:
                    if f2 == 2:
                        fraccion2 = 'X'
                        f2 = 0
                result.append(fraccion2)
        return result

    def get_fraccion3(self):
        result = []
        f3 = 0
        for record_fraccionid in self.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 3:
                f3 = 3

        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f3):
                if record_id_plan.id == 3:
                    if f3 == 3:
                        fraccion3 = 'X'
                        f3 = 0
                result.append(fraccion3)
        return result

    def get_fraccion4(self):
        result = []
        f4 = 0
        for record_fraccionid in self.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 4:
                f4 = 4

        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f4):
                if record_id_plan.id == 4:
                    if f4 == 4:
                        fraccion4 = 'X'
                        f4 = 0
                result.append(fraccion4)
        return result

    def get_fraccion5(self):
        result = []
        f5 = 0
        for record_fraccionid in self.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 5:
                f5 = 5

        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f5):
                if record_id_plan.id == 5:
                    if f5 == 5:
                        fraccion5 = 'X'
                        f5 = 0
                result.append(fraccion5)
        return result

    def get_fraccion6(self):
        result = []
        f6 = 0
        for record_fraccionid in self.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 6:
                f6 = 6
        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f6):
                if record_id_plan.id == 6:
                    if f6 == 6:
                        fraccion6 = 'X'
                        f6 = 0
                result.append(fraccion6)
        return result

    def get_fraccion7(self):
        result = []
        f7 = 0
        for record_fraccionid in self.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 7:
                f7 = 7

        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f7):
                if record_id_plan.id == 7:
                    if f7 == 7:
                        fraccion7 = 'X'
                        f7 = 0
                result.append(fraccion7)
        return result

    def get_fraccion8(self):
        result = []
        f8 = 0
        for record_fraccionid in self.refid_fracciones.ids:
            numf = record_fraccionid
            if numf == 8:
                f8 = 8

        filtros = [('estatus', '=', True)]
        frccion_id = self.env['visitas.cd.fracciones'].sudo().search(filtros)
        for record_id_plan in frccion_id:
            if record_id_plan.id == (f8):
                if record_id_plan.id == 8:
                    if f8 == 8:
                        fraccion8 = 'X'
                        f8 = 0
                result.append(fraccion8)
        return result

    def get_cuotas(self):
        filtro_cuotas = [('rev_id_plan', '=', self.id)]
        cuotas_id = self.env['visitas.cuotas.recuperacion'].sudo().search(filtro_cuotas)
        result = []
        for record in cuotas_id.ids:
            fltro2 =[('id', '=', record)]
            cuotas_pr = self.env['visitas.cuotas.recuperacion'].sudo().search(fltro2)
            result.append(
                cuotas_pr.proyecto + "&" + cuotas_pr.estuio_cuotas + "&" + cuotas_pr.tabulador +'&'+ cuotas_pr.montos + '&' + cuotas_pr.exentos +'(inip)')
        return result

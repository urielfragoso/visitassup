{
    'name': 'VISITAS SUPERVISION',
    'version': '1.0',
    'category': 'VISITAS DE SUPERVISION - JAPCDMX',
    'sequence': 15,
    'author': 'DTIC JAPCDMX',
    'summary': 'VISITAS DE SUPERVISION ',
    'description': 'GENERACION DE DOCUMENTOS DE LAS VISITAS DE SUPERVISION POR PARTE DE LA DAS - JAPCDMX',
    'depends': ['base', 'mail', 'registroiap', 'web', 'report_py3o'],

    'data': [
        'security/visitas_security.xml',
        'security/ir.model.access.csv',
        'views/visitas_programacion_view.xml',
        'views/visitas_plan_visita_view.xml',
        'views/visitas_menu_view.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
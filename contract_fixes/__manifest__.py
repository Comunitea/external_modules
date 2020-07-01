# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Contract fixes',
    'summary': "Link Sales Contract & Projects",
    'version': '12.0.0.0.0',
    'category': 'Project',
    'author': 'Comunitea, '
              'Javier Colmenero (javier@comunitea.com), ',
    'license': 'AGPL-3',
    'depends': [
        'contract', 
        'contract_variable_qty_timesheet'],
    'data': [
            'views/contract_line.xml'
        ],
    'development_status': 'Beta',
    'maintainers': [
        'Javier Colmenero',
    ],
    'installable': True,
}

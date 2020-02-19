import odoorpc
import os

IP_DB_SERVER = os.environ.get('ODOO_HOST', 'fencri.altabpo.com')
PORT_DB_SERVER = os.environ.get('ODOO_PORT', '8069')
USER_DB_SERVER = os.environ.get('ODOO_USER', 'admin')
PASSWORD_DB_SERVER = os.environ.get('ODOO_PASSWORD', 'admin')
DB_NAME = os.environ.get('ODOO_DB', 'casinodev')


class Fencri:
    odoo = None

    def __init__(self):
        self.initial_odoo()
        self.login_db()

    def initial_odoo(self):
        self.odoo = odoorpc.ODOO(IP_DB_SERVER, 'jsonrpc', PORT_DB_SERVER)

    # listar las base de datos
    def listar_dbs(self):
        print(self.odoo.db.list())

    # iniciar sesión en una base de datos dada
    def login_db(self):
        self.odoo.login(DB_NAME, USER_DB_SERVER, PASSWORD_DB_SERVER)

    def get_ludopata(self, dni):
        model = self.odoo.env['res.partner']
        partner_id = model.search([('is_ludopath', '=', True), ('vat', '=', dni)], limit=1)
        if partner_id:
            partner = self.odoo.execute('res.partner', 'read', partner_id, ['id', 'name'])
            return partner
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

db.define_table('company',
                Field('name', 'string', label='Namn'),
                Field('address', 'string', label='Adress'),
                Field('zip_code', 'string', label='Postnummer'),
                Field('city', 'string', label='Stad'),
                Field('phone_number', 'string', label='Telefonnummer'),
                Field('email', 'string', label='Epost'),
                Field('vat', 'string', label='Org. nummer'),
                Field('account', 'string', label='Konto nummer'),
                Field('payment_terms', 'integer', label='Betalingsvillkor i dagar'),
                Field('expiration_fee', 'integer', label='Dröjsmålsränta %'),
                Field('ftax', 'boolean', label='Godkänd för f-skatt'))

db.define_table('customer',
                Field('name', 'string', label='Namn'),
                Field('address', 'string', label='Adress'),
                Field('zip_code', 'string', label='Postnummer'),
                Field('city', 'string', label='Stad'))

db.define_table('invoice',
    Field('company_id', 'reference company', label='Leverantör', requires=IS_IN_DB(db, db.company.id, '%(name)s')),
    Field('customer_id', 'reference customer', label='Kund', requires=IS_IN_DB(db, db.customer.id, '%(name)s')),
    Field('created_on', 'date', label='Leveransdatum'),
    Field('expires_on', 'date', label='Förfallodatum'),
    Field('tax_percentage', 'integer', label='Moms (%)'),
    Field('paid', 'boolean', label='Betalad'),
    Field('deleted', 'boolean', label='Mackulerad'),
    Field('extra_info', 'string', label='Extra fotnot'))

db.define_table('service',
    Field('name', 'string', label='Produkt'),
    Field('cost_per', 'integer', label='á pris', requires=IS_MATCH('^\d+$', error_message='Du måste sätta ett pris')),
    Field('tax_free', 'boolean', label='Momsfri'))


db.define_table('invoice_service_mapping',
    Field('invoice_id', 'reference invoice', label='Fakturanummer'),
    Field('service_id', 'reference service', label='Produkt', requires=IS_IN_DB(db, db.service.id, '%(name)s - %(cost_per)s')),
    Field('quantity', 'integer', label='Antal', requires=IS_MATCH('^\d+$', error_message='Du måste sätta antal')))

# add price of invoice
# db.invoice.total_price = Field.Virtual('total_price', lambda row: db((db.invoice_service_mapping.invoice_id==row.id)).count())

# class MyVirtualFields(object):
#     def total_price(self):
#         return lambda self=self: self.invoice.tax_percentage*2
#
# db.invoice.virtualfields.append(MyVirtualFields())

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Hem'), False, URL('default', 'index'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        (T('Skapa/Ändra'), False, '#', [
            (T('Företag'), False, URL('company', 'create')),
            (T('Kund'), False, URL('client', 'create')),
            (T('Produkt'), False, URL('service', 'create')),
            (T('Faktura'), False, URL('invoice', 'create')),
        ]),
         (T('System administration'), False, '#', [
             (T('Säkerhetskopiera databasen'), False, URL('admin', 'export_db_to_csv')),
          #   (T('Återställ från säkerhetskopia'), False, URL('admin', 'import_and_sync')),
          #   (T('Töm databasen'), False, URL('admin', 'reset_database'))
          ])
    ]


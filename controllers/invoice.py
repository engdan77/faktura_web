def create():
    # This part used when removing items
    if 'remove_id' in request.vars.keys():
        remove_ids = request.vars['remove_id']
        remove_ids = remove_ids if type(remove_ids) is list else [remove_ids,]
        print(remove_ids)
        for row in db(db.invoice.id.belongs(remove_ids)).select():
            row.update_record(deleted=True)
        response.flash = '{} faktur(or) tagits bort'.format(len(remove_ids))
    if 'paid_id' in request.vars.keys():
        paid_ids = request.vars['paid_id']
        paid_ids = paid_ids if type(paid_ids) is list else [paid_ids,]
        for row in db(db.invoice.id.belongs(paid_ids)).select():
            row.update_record(paid=True)
        response.flash = '{} faktur(or) markerats betald'.format(len(paid_ids))

    form = SQLFORM.factory(db.invoice, formstyle='table3cols', submit_button='Lägg till')
    if form.accepts(request, session):
        db.invoice.insert(**db.invoice._filter_fields(form.vars))
        response.flash = 'Faktura skapad'

    def disable_field(obj_attrs_dict):
        for o, attrs in obj_attrs_dict.items():
            for a in attrs:
                _ = getattr(o, a)
                _.writable = False
                _.readable = False

    disable_field({db.company: ['id', 'address', 'zip_code', 'city', 'phone_number', 'email', 'vat',
                                'account', 'payment_terms', 'expiration_fee', 'ftax'],
                   db.invoice: ['company_id', 'customer_id'],
                   db.customer: ['id', 'address', 'zip_code', 'city', 'address']})

    grid_invoice = SQLFORM.grid(db.invoice.deleted==False,
                                left=(db.customer.on(db.invoice.customer_id == db.customer.id),
                                      db.company.on(db.invoice.company_id == db.company.id)),
                                headers={'invoice.id': 'Fakturanr',
                                         'customer.name': 'Kund',
                                         'company.name': 'Eget företag'},
                                selectable=[('Ta bort', lambda ids: redirect(URL('invoice',
                                                                                 'create',
                                                                                 vars=dict(remove_id=ids)))),
                                            ('Markera betald', lambda ids: redirect(URL('invoice',
                                                                                 'create',
                                                                                 vars=dict(paid_id=ids))))],
                                editable=False,
                                deletable=False,
                                searchable=False,
                                create=False,
                                details=False,
                                csv=False,
                                links=[dict(header='Summa (kr exkl. moms)', body=lambda row: sum(
                                            [list(r['_extra'].values())[0] for r in db(row.invoice.id == db.invoice_service_mapping.invoice_id)
                                            .select(db.service.cost_per * db.invoice_service_mapping.quantity)])),
                                       dict(header='Moms (kr)', body=lambda row: int(sum(
                                            [list(r['_extra'].values())[0] for r in db(row.invoice.id == db.invoice_service_mapping.invoice_id)
                                            .select(db.service.cost_per * db.invoice_service_mapping.quantity)]) * (row.invoice.tax_percentage / 100))),
                                       lambda row: A('Produkter', _href=URL("invoice", "service_to_invoice",
                                                                            vars={'invoice_id': row.invoice.id})),
                                       lambda row: A('Skriv ut faktura', _href=URL("invoice", "print_invoice",
                                                                            vars={'invoice_id': row.invoice.id}))
                                       ]
                                )
    [button.__setitem__(0, 'Titta') for button in grid_invoice.elements('span[title=%s]' % T('View'))]
    [button.__setitem__(0, 'Ta bort') for button in grid_invoice.elements('span[title=%s]' % T('Delete'))]
    [button.__setitem__(0, 'Tillbaka') for button in grid_invoice.elements('span[title=%s]' % T('Back'))]
    return dict(form=form, grid_invoice=grid_invoice)


def service_to_invoice():
    # This part used when removing items
    if 'remove_id' in request.vars.keys():
        remove_ids = request.vars['remove_id']
        remove_ids = remove_ids if type(remove_ids) is list else [remove_ids,]
        for row in db(db.invoice_service_mapping.id.belongs(remove_ids)).select():
            row.delete_record()
        response.flash = '{} produkt(er) tagits bort'.format(len(remove_ids))

    # this part for display the SQLform
    invoice_id = request.vars['invoice_id']
    # db.invoice_service_mapping.invoice_id.default = invoice_id
    # db.invoice_service_mapping.invoice_id.writable = False
    form = SQLFORM.factory(db.invoice_service_mapping,
                           formstyle='table3cols',
                           submit_button='Lägg till',
                            )

    if form.accepts(request, session):
        db.invoice_service_mapping.insert(**db.invoice_service_mapping._filter_fields(form.vars))
        response.flash = 'Lagt till produkt'

    # This part for displaying the grid
    db.service.id.writable = False
    db.service.id.readable = False
    db.invoice_service_mapping.id.writable = False
    db.invoice_service_mapping.id.readable = False
    db.invoice_service_mapping.invoice_id.writable = False
    db.invoice_service_mapping.invoice_id.readable = False
    db.invoice_service_mapping.service_id.writable = False
    db.invoice_service_mapping.service_id.readable = False
    grid_services = SQLFORM.grid(db((db.invoice_service_mapping.invoice_id == invoice_id) & (db.invoice_service_mapping.service_id == db.service.id)),
                                editable=True,
                                deletable=False,
                                searchable=False,
                                create=False,
                                csv=False,
                                selectable=[('Ta bort',
                                              lambda ids: redirect(URL('invoice', 'service_to_invoice',
                                                                       vars=dict(remove_id=ids))))]
                                )
    [button.__setitem__(0, 'Titta') for button in grid_services.elements('span[title=%s]' % T('View'))]
    [button.__setitem__(0, 'Ändra') for button in grid_services.elements('span[title=%s]' % T('Edit'))]
    [button.__setitem__(0, 'Ta bort') for button in grid_services.elements('span[title=%s]' % T('Delete'))]
    [button.__setitem__(0, 'Tillbaka') for button in grid_services.elements('span[title=%s]' % T('Back'))]
    return dict(form=form, grid_services=grid_services)


def print_invoice():
    from invoice_writer import create_pdf
    import os
    from io import BytesIO

    invoice_file = os.path.join(request.folder, 'static', 'faktura.pdf')

    invoice_id = request.vars['invoice_id']
    response.flash = 'Skriv ut faktura {}'.format(invoice_id)
    r = db((db.invoice.id == invoice_id) & (db.invoice.company_id == db.company.id) & (db.invoice.customer_id == db.customer.id)).select().first()

    purchased_services_query = db((db.invoice_service_mapping.service_id == db.service.id) & (db.invoice_service_mapping.invoice_id == invoice_id)).select()
    purchased_service = []
    for row in purchased_services_query:
        purchased_service.append({'name': row.service.name,
                                  'quantity': row.invoice_service_mapping.quantity,
                                  'cost_per': row.service.cost_per})

    d = {'invoice_id': r.invoice.id,
         'created_on': r.invoice.created_on,
         'expires_on': r.invoice.expires_on,
         'paid': r.invoice.paid,
         'tax_percantage': r.invoice.tax_percentage,
         'company_name': r.company.name,
         'company_address': r.company.address,
         'company_zip_code': r.company.zip_code,
         'company_city': r.company.city,
         'company_phone_number': r.company.phone_number,
         'company_vat': r.company.vat,
         'company_account': r.company.account,
         'company_payment_terms': r.company.payment_terms,
         'company_expiration_fee': r.company.expiration_fee,
         'company_ftax': r.company.ftax,
         'company_email': r.company.email,
         'customer_id': r.customer.id,
         'customer_name': r.customer.name,
         'customer_address': r.customer.address,
         'customer_zip_code': r.customer.zip_code,
         'customer_city': r.customer.city,
         'item_list': purchased_service}
    create_pdf(invoice_file, d)
    data = open(invoice_file, "rb").read()
    response.headers['Content-Type'] = 'application/pdf'
    #return dict(vars=locals())
    return response.stream(BytesIO(data))
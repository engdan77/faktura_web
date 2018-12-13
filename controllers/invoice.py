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
                                                                            vars={'invoice_id': row.invoice.id}))]
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
    db.invoice_service_mapping.invoice_id.default = invoice_id
    db.invoice_service_mapping.invoice_id.writable = False
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
    grid_services = SQLFORM.grid(db.invoice_service_mapping,
                                editable=True,
                                deletable=False,
                                searchable=False,
                                create=False,
                                csv=False,
                                left=(db.service.on(db.invoice_service_mapping.service_id == db.service.id)),
                                selectable=[('Ta bort',
                                              lambda ids: redirect(URL('invoice', 'service_to_invoice',
                                                                       vars=dict(remove_id=ids))))]
                                )
    [button.__setitem__(0, 'Titta') for button in grid_services.elements('span[title=%s]' % T('View'))]
    [button.__setitem__(0, 'Ändra') for button in grid_services.elements('span[title=%s]' % T('Edit'))]
    [button.__setitem__(0, 'Ta bort') for button in grid_services.elements('span[title=%s]' % T('Delete'))]
    [button.__setitem__(0, 'Tillbaka') for button in grid_services.elements('span[title=%s]' % T('Back'))]
    return dict(form=form, grid_services=grid_services)

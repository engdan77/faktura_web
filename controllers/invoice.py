def create():
    form = SQLFORM.factory(db.invoice, formstyle='table3cols', submit_button='Lägg till')
    if form.accepts(request, session):
        db.invoice.insert(**db.invoice._filter_fields(form.vars))
        response.flash = 'Faktura skapad'
    grid_invoice = SQLFORM.grid(db.invoice,
                                editable=True,
                                deletable=False,
                                searchable=False,
                                create=False,
                                csv=False,
                                links=[lambda row: A('Produkter',_href=URL("invoice", "service_to_invoice", vars={'invoice_id': row.id}))]
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
        print(remove_ids)
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
    [button.__setitem__(0, 'Ta bort') for button in grid_services.elements('span[title=%s]' % T('Delete'))]
    [button.__setitem__(0, 'Tillbaka') for button in grid_services.elements('span[title=%s]' % T('Back'))]
    return dict(form=form, grid_services=grid_services)

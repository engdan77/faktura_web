def create():
    form = SQLFORM.factory(db.invoice, formstyle='table3cols', submit_button='Lägg till')
    if form.accepts(request, session):
        result_id = db.invoice.insert(**db.invoice._filter_fields(form.vars))
        response.flash = 'Faktura skapad'
    grid_invoice = SQLFORM.grid(db.invoice,
                                editable=True,
                                deletable=False,
                                searchable=False,
                                create=False,
                                csv=False,
                                links=[lambda row: A('Produkter',_href=URL("default","show",args=[row.id]))]
                                )
    [button.__setitem__(0, 'Titta') for button in grid_invoice.elements('span[title=%s]' % T('View'))]
    [button.__setitem__(0, 'Ta bort') for button in grid_invoice.elements('span[title=%s]' % T('Delete'))]
    [button.__setitem__(0, 'Tillbaka') for button in grid_invoice.elements('span[title=%s]' % T('Back'))]
    return dict(form=form, grid_invoice=grid_invoice)

def map_service_to_invoice():
    form = SQLFORM.factory(db.invoice_service_mapping, formstyle='table3cols', submit_button='Lägg till').process()
    if form.accepted:
        response.flash = 'Produkt tillagd'
    return dict(form=form)

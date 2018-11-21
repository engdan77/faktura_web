def create():
    form = SQLFORM.factory(db.invoice, formstyle='table3cols').process()
    if form.accepted:
        response.flash = 'Faktura skapad'
    return dict(form=form, grid=SQLFORM.grid(db.invoice, editable=False, searchable=False, create=False))
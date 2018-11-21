def create():
    form = SQLFORM(db.customer, formstyle='table3cols').process()
    if form.accepted:
        response.flash = 'Kund skapad'
    return dict(form=form, grid=SQLFORM.grid(db.customer, editable=False, searchable=False, create=False))
def create():
    form = SQLFORM(db.service, formstyle='table3cols', submit_button='Lägg till').process()
    if form.accepted:
        response.flash = 'Service skapad'
    grid = SQLFORM.grid(db.service, editable=False, searchable=False, create=False)
    [button.__setitem__(0, 'Titta') for button in grid.elements('span[title=%s]' % T('View'))]
    [button.__setitem__(0, 'Ta bort') for button in grid.elements('span[title=%s]' % T('Delete'))]
    return dict(form=form, grid=grid)
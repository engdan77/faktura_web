def create():
    """
    create controller for client
    :return:
    """
    form = SQLFORM(db.customer, formstyle='table3cols', submit_button='Lägg till').process()
    if form.accepted:
        response.flash = 'Kund skapad'
    grid = SQLFORM.grid(db.customer, editable=True, deletable=False, searchable=False, create=False, csv=False)
    [button.__setitem__(0, 'Titta') for button in grid.elements('span[title=%s]' % T('View'))]
    [button.__setitem__(0, 'Ändra') for button in grid.elements('span[title=%s]' % T('Edit'))]
    [button.__setitem__(0, 'Ta bort') for button in grid.elements('span[title=%s]' % T('Delete'))]
    [button.__setitem__(0, 'Tillbaka') for button in grid.elements('span[title=%s]' % T('Back'))]
    return dict(form=form, grid=grid)

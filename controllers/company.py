def create():
    '''
    create controller for company
    :return:
    '''
    form = SQLFORM(db.company, formstyle='table3cols', submit_button='Lägg till').process()
    if form.accepted:
        response.flash = 'Företag skapad'
    grid = SQLFORM.grid(db.company, editable=True, deletable=False, searchable=False, create=False, csv=False)
    [button.__setitem__(0, 'Titta') for button in grid.elements('span[title=%s]' % T('View'))]
    [button.__setitem__(0, 'Ändra') for button in grid.elements('span[title=%s]' % T('Edit'))]
    [button.__setitem__(0, 'Ta bort') for button in grid.elements('span[title=%s]' % T('Delete'))]
    [button.__setitem__(0, 'Tillbaka') for button in grid.elements('span[title=%s]' % T('Back'))]
    return dict(form=form, grid=grid)
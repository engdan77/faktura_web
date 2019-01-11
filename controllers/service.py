def create():
    """
    create controller for services
    :return:
    """
    form = SQLFORM.factory(db.service, formstyle='table3cols', submit_button='Lägg till').process()
    if form.accepted:
        if not form.vars['name'] == '' and not form.vars['cost_per'] is type(int):
            db.service.insert(**db.service._filter_fields(form.vars))
            response.flash = 'Produkt skapad'
        else:
            response.flash = 'Du har angett fel information'
    grid = SQLFORM.grid(db.service, editable=True, deletable=False, searchable=False, create=False, csv=False)
    [button.__setitem__(0, 'Titta') for button in grid.elements('span[title=%s]' % T('View'))]
    [button.__setitem__(0, 'Ändra') for button in grid.elements('span[title=%s]' % T('Edit'))]
    [button.__setitem__(0, 'Ta bort') for button in grid.elements('span[title=%s]' % T('Delete'))]
    [button.__setitem__(0, 'Tillbaka') for button in grid.elements('span[title=%s]' % T('Back'))]
    return dict(form=form, grid=grid)

def export_db_to_csv():
    """
    export database
    :return:
    """
    import os
    from io import BytesIO, StringIO
    import shutil

    s = StringIO()
    db.export_to_csv_file(s)
    response.headers['Content-Type'] = 'text/csv'
    backup_file = os.path.join(request.folder, 'static', 'backup.csv')
    with open(backup_file, 'w') as f:
        s.seek(0)
        shutil.copyfileobj(s, f)
    response.headers['Content-Type'] = 'application/csv'
    data = open(backup_file, "rb").read()
    return response.stream(BytesIO(data))

def import_and_sync():
    '''
    import csv to database
    :return:
    '''
    form = FORM(INPUT(_type='file', _name='data'), INPUT(_type='submit'))
    if form.process().accepted:
        db.import_from_csv_file(form.vars.data.file, unique=False)
        # for every table
        for table in db.tables:
            # for every uuid, delete all but the latest
            items = db(db[table]).select(db[table].id,
                                         db[table].uuid,
                                         orderby=db[table].modified_on,
                                         groupby=db[table].uuid)
            for item in items:
                db((db[table].uuid == item.uuid) &
                   (db[table].id != item.id)).delete()
    return dict(form=form)


def reset_database():
    '''
    simple function for resetting database without auth tables
    :return:
    '''
    if 'reset' in request.vars.keys():
        exclude = []
        import os
        import sys
        import glob
        for tablename in db.tables[:]:
            if tablename in exclude or tablename[0:4] == 'auth':
                print(f"keep {tablename}")
            else:
                table = db[tablename]
                print(f'table found {table}')
                try:
                    print(f'delete {tablename}')
                    t = getattr(db, tablename)
                    t.drop()
                    filelist = os.path.join(request.folder, 'databases', f'*{tablename}.table')
                    print(filelist)
                    filelist = glob.glob(filelist)
                    print(filelist)
                    if len(filelist) > 0:
                        os.remove(filelist[0])
                except Exception as e:
                    print(f'failed to delete {tablename}')
                    print(e)
                    print(sys.exc_info())
        db.commit()
        form = redirect(URL('default', 'index'))
    else:
        form = SQLFORM.factory(Field('reset', 'boolean', label='Rensa databas?'))
        btn = form.element("input", _type="submit")
        btn['_value'] = T("Fortsätt")
        btn['_onclick'] = "return confirm('Är du säker på att radera och börja om?');"
    return dict(form=form)

def export_db_to_csv():
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
                db((db[table].uuid==item.uuid) &
                   (db[table].id!=item.id)).delete()
    return dict(form=form)


def reset_database():
    exclude = []
    import os
    import sys
    import glob
    for tablename in db.tables[:]:
        if tablename in exclude or tablename[0:4]=="auth":
            print("keep "+tablename)
        else:
            table = db[tablename]
            try:
                print("delete "+tablename)
                filelist = os.path.join(request.folder, 'databases', f'*{tablename}.table')
                print(filelist)
                filelist = glob.glob(filelist)
                print(filelist)
                if len(filelist) > 0:
                    os.remove(filelist[0])
                table.drop()
            except Exception as e:
                print("failed to delete "+tablename)
                print(e)
                print(sys.exc_info())
    db.commit()
    return 'Database reset'

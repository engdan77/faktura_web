def create_pdf(invoice_file, input_dict):
    from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item
    from pyinvoice.templates import SimpleInvoice

    # purchased_service = []
    # purchased_service.append({'name': 'jobb',
    #                           'quantity': 3,
    #                           'cost_per': 500})
    #
    # d = {'invoice_id': 1,
    #      'created_on': datetime.now(),
    #      'expires_on': datetime.now(),
    #      'tax_percantage': 25,
    #      'paid': True,
    #      'company_name': 'Bannes',
    #      'company_address': 'Holländaregatn 3',
    #      'company_zip_code': '561 39',
    #      'company_city': 'Huskvarna',
    #      'company_phone_number': '0701111122222',
    #      'company_vat': '555-666',
    #      'company_account': '9150-77777',
    #      'company_payment_terms': 30,
    #      'company_expiration_fee': 10,
    #      'company_ftax': True,
    #      'company_email': 'banne@banne.com',
    #      'customer_id': 55,
    #      'customer_name': 'Snabel AB',
    #      'customer_address': 'Snabelgatan 2',
    #      'customer_zip_code': '171 57',
    #      'customer_city': 'Solna',
    #      'item_list': purchased_service}


    d = input_dict
    print('generating pdf')
    doc = SimpleInvoice(invoice_file)
    doc.is_paid = d['paid']

    doc.invoice_info = InvoiceInfo(d['invoice_id'],
                                   d['created_on'],
                                   d['expires_on'],
                                   f"{d['company_expiration_fee']} %")

    # Service Provider Info, optional
    doc.service_provider_info = ServiceProviderInfo(
        name=d['company_name'],
        street=d['company_address'],
        city=d['company_city'],
        post_code=d['company_zip_code'],
        vat_tax_number=d['company_vat']
    )

    doc.client_info = ClientInfo(name=d['customer_name'],
                                 client_id=d['customer_id'],
                                 street=d['customer_address'],
                                 city=d['customer_city'],
                                 post_code=d['customer_zip_code']
                                 )

    for item in d['item_list']:
        doc.add_item(Item(item['name'], '', item['quantity'], item['cost_per']))

    # Tax rate, optional
    doc.set_item_tax_rate(d['tax_percantage'])  # 20%

    # Transactions detail, optional
    # doc.add_transaction(Transaction('Paypal', 111, datetime.now(), 1))
    # doc.add_transaction(Transaction('Stripe', 222, date.today(), 2))

    # Optional
    doc.set_bottom_tip(
        f"Email: {d['company_email']}<br />Kontonummer: {d['company_account']}<br />Vid frågor kontakt på {d['company_phone_number']}.")
    doc.finish()
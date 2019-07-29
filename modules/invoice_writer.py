def create_pdf(invoice_file, input_dict):
    """
    function for creating pdf
    :param invoice_file:
    :param input_dict:
    :return:
    """
    from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item
    from pyinvoice.templates import SimpleInvoice

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
        # if item['tax_free']:
        #     item['name'] += ' (omvänd skatteskyldighet)'
        doc.add_item(Item(item['name'], '', item['quantity'], item['cost_per']))

    # Tax rate, optional
    doc.set_item_tax_rate(d['tax_percantage'])  # 25%

    # Optional
    doc.set_bottom_tip(
        f"Email: {d['company_email']}<br />Kontonummer: {d['company_account']}<br />Godkänd för F-skatt<br />Vid frågor kontakt på {d['company_phone_number']}.<br />{d['extra_info']}")
    doc.finish()

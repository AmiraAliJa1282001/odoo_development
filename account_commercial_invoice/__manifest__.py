{
    'name': 'Commercial Invoice Report',
    'summary': 'Printable Commercial Invoice for customer invoices',
    'description': "",
    'version': '1.0',
    'category': 'Customizations',
    'sequence': 15,
    
    'website': '',
    'depends': [
        'account'
    ],
    'data': [
        'report/commercial_invoice_template.xml',
        'report/commercial_reports.xml',

    ],
    'assets': {
        "web.report_assets_pdf": [
            "account_commercial_invoice/static/src/css/ci_style.css",
        ]
    },
    'demo': [
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}


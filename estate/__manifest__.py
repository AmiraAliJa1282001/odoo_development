{
    'name': 'estate',
    'summary': 'Real Estate Module',
    'description': "",
    'version': '1.0',
    'category': 'Customizations',
    'sequence': 15,
    
    'website': '',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'data/master_property_type_data.xml',
        'report/estate_property_offer_template.xml',
        'report/estate_property_templates.xml',
        'report/res_user_property_template.xml',
        'report/estate_property_reports.xml',
    ],
    'demo': [
        'demo/tag.csv',
        'demo/real_estate_demo_data.csv',
        'demo/estate_demo_data.xml',
        'demo/property_offers_data.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}


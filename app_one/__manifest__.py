{
    'name':"App One",
    'author':"Rashed Jardaneh",
    'category':'',
    'version':'19.0.1.0.0',
    'depends': ['base', 'sale_management', 'mail', 'account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',  # Define menus first
        'views/owner_view.xml',  # Now these can safely reference base_menu items
        'views/property_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/building_view.xml',
        'views/property_history_view.xml',
        'views/account_move_view.xml',
        'wizard/change_state_wizard_view.xml',
        'reports/property_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'app_one/static/src/css/property.css',
            'app_one/static/src/components/listView/listView.css', # Added comma
            'app_one/static/src/components/listView/listView.js',  # Added comma
            'app_one/static/src/components/listView/listView.xml',
        ],
        'web.report_assets_common': ['app_one/static/src/css/font.css'],
    },
    'application':True,
'license': 'LGPL-3',

}
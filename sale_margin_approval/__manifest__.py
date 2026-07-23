{
    'name':"Sale Margin Approval",
    'author':"Rashed Jardaneh",
    'category':'',
    'version':'19.0.1.0.0',
    'depends': ['base', 'sale_management', 'mail', 'account', 'stock','product'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu_view.xml',
        'views/sale_order_views.xml', # Contains your action that links to the menu
        'wizard/approval_wizard_view.xml',

    ],

    'application':True,
'license': 'LGPL-3',

}
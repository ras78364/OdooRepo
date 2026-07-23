{
    'name':"Odoo Tasks",
    'author':"Rashed Jardaneh",
    'category':'',
    'version':'19.0.1.0.0',
    'depends': ['base', 'sale_management', 'mail', 'account', 'stock','product'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/sale_order_view.xml', # ضع ملف المعالج/الإجراء هنا أولاً
        'views/base_menu.xml',       # ثم ملف القوائم ثانياً
        'views/Inventory_view.xml',
        'views/res_partner_view.xml',
        'views/res_users_view.xml',
        'views/account_move_view.xml',
        'reports/report_by_salesman.xml',
        'reports/report_by_unpaid_invoice.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'odoo_tasks/static/src/css/report_by_salesman.css',
        ],
    },

    'application':True,
'license': 'LGPL-3',

}
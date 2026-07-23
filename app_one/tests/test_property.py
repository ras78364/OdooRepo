# from odoo import fields
# from odoo.tests.common import TransactionCase
#
# class TestProperty(TransactionCase):
#
#     def setUp(self):
#         # Simply call super().setUp() without any arguments
#         super(TestProperty,self).setUp()
#
#         self.property_01_record = self.env['property'].create({
#             'ref': 'PRT1000',
#             'name': 'Property 1000',
#             'description': 'Property 1000 description',
#             'date_availability': fields.Date.today(),
#             'bedrooms': '10',
#             'expected_price': 1000,
#             'postcode': '12345',
#         })
#
#     def test_01_property_values(self):
#         property_id = self.property_01_record
#         self.assertRecordValues(property_id, [{
#             'ref': 'PRT1000',
#             'name': 'Property 1000',
#             'description': 'Property 1000 description',
#             'date_availability': fields.Date.today(),
#             'bedrooms': '10',
#             'expected_price': 1000,
#         }])
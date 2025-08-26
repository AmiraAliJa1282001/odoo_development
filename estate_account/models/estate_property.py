from odoo import models, fields
from odoo import Command
class InheritedEstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        selling_price = self.selling_price
        admin_fee = 100.00

        invoice= self.env['account.move'].create({
            "name": self.name,
            'partner_id': self.salesperson_id.id,
            'move_type': 'out_invoice',  # Corresponds to 'Customer Invoice'
             "line_ids": [
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,  
                    'price_unit': admin_fee,
                    
                    
                }),
                Command.create({
                    'name': '6% of Selling Price',
                    'quantity': 1,  
                    'price_unit': selling_price * 0.06,
                    
                }),
                 
            ],
        })
        self.invoice_property_id= invoice.id
        return super().action_sold()
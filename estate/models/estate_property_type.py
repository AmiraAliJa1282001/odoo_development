from odoo import models, fields,api

class RealEstateType (models.Model):
    _name = 'estate.property.type'
    _order = "name"
    
    name = fields.Char('Property Type', required=True )
    property_ids = fields.One2many("estate.property", "type_id", string="Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. most used is better.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="offers")
    offer_count= fields.Integer(string="Offer Count", compute='_compute_offer_count')


    _sql_constraints = [
        ('check_type_name', 'UNIQUE(name)','Property type name must be unique.')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count= len(record.offer_ids)
    

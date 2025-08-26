from odoo import models, fields

class RealEstateTag (models.Model):
    _name = 'estate.property.tag'
    _order = "name"
    
    name = fields.Char('Tag Name', required=True )
    color = fields.Integer('Color')
    _sql_constraints = [
        ('check_tag_name', 'UNIQUE(name)','Tag name must be unique.')
    ]

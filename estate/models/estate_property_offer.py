from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError,ValidationError

class RealEstateOffer(models.Model):
    _name = 'estate.property.offer'
    _order = "price desc"    
    price = fields.Float(string='Price')
    status = fields.Selection(
        [('refused', 'Refused'), ('accepted', 'Accepted')],
        string='Status', copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(
        string="Date Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )
    property_type_id = fields.Many2one("estate.property.type" ,string= "Property type" , related="property_id.type_id")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.validity:
                offer.date_deadline = offer.create_date.date() + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
                create_date = offer.create_date.date()
                delta = offer.date_deadline - create_date
                offer.validity = delta.days

    def action_accept(self):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError("This offer has already been accepted.")
            # Check if there are other accepted offers for the same property
            accepted_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', offer.property_id.id),
                ('status', '=', 'accepted')
            ])
            
            if accepted_offers:
                raise UserError("Another offer has already been accepted for this property.")
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state= 'offer_accepted'

    def action_refused(self):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError("An accepted offer cannot be refused.")
            offer.status = 'refused'

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)','Offer price must be strictly positive.')
    ]

    @api.model
    def create(self, vals):
        price = vals.get('price')
        property_offer = self.env['estate.property'].browse(vals.get('property_id'))

        # Check if there are any offers for the property
        if property_offer.offer_ids:
            # Find the maximum offer price
            max_offer_price = max(property_offer.offer_ids.mapped('price'))

            # Check if the new offer price is lower than the maximum offer price
            if price < max_offer_price:
                raise ValidationError("A lower offer price cannot be created.")

        # Set the property state to 'Offer Received'
        property_offer.state = 'offer_received'

        # Create the offer
        return super(RealEstateOffer, self).create(vals)

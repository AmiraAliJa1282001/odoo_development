from odoo import fields,models, api
from odoo.exceptions import UserError,ValidationError
from datetime import datetime, date, timedelta
from odoo.tools.float_utils import float_compare

class EstateProperty(models.Model):
	_name = "estate.property"
	_description = "Estate Property Model"
	_order = "id desc"


	name = fields.Char()
	name = fields.Char('Estate Name', required=True)
	description = fields.Text(string='Description')
	postcode = fields.Char(string='Postcode')
	date_availability = fields.Date(string='Availability Date', copy=False, default=lambda self: datetime.today() + timedelta(days=90) )
	expected_price = fields.Float(string='Expected Price', required=True)
	selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
	bedrooms = fields.Integer(string='Number of Bedrooms', default=2)
	living_area = fields.Integer(string='Living Area (sq. ft)')
	facades = fields.Integer(string='Number of Facades')
	garage = fields.Boolean(string='Garage')
	garden = fields.Boolean(string='Garden')
	garden_area = fields.Integer(string='Garden Area (sq. ft)')
	garden_orientation = fields.Selection(
        	[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')],
        	string='Garden Orientation',
	)
	active = fields.Boolean(string='Active', default=True, help='Set to inactive to hide this record')
	state = fields.Selection(
        [('new', 'New'),('offer_received', 'Offer Received'),('offer_accepted', 'Offer Accepted'),('sold', 'Sold'),('canceled', 'Canceled')],
        string='State', required=True, default='new', copy=False,)
	type_id = fields.Many2one("estate.property.type", string="Type")
	buyer_id = fields.Many2one("res.partner", string="Buyer" )

	salesperson_id = fields.Many2one("res.users", string="Salesman" ,default=lambda self: self.env.user)
	tag_ids= fields.Many2many("estate.property.tag", string="Tags")
	offer_ids = fields.One2many("estate.property.offer", "property_id", string="offers")
	total_area= fields.Float(string="Total Area", compute="_compute_total_area")
	invoice_property_id = fields.Many2one("account.move", string="Invoices")

	@api.depends('garden_area', 'living_area')
	def _compute_total_area(self):
		for record in self:
			record.total_area = record.living_area + record.garden_area

	best_price = fields.Float(string="Best Price", compute = "_compute_best_price", )

	@api.depends('offer_ids.price')
	def _compute_best_price(self):
		for record in self:
			if record.offer_ids:
				record.best_price = max(record.offer_ids.mapped('price'))
			else:
				record.best_price = 0.0
	@api.onchange('garden')
	def _onchange_garden(self):
		if not self.garden:
			self.garden_area = 0
			self.garden_orientation = False
		else:
			self.garden_area = 10
			self.garden_orientation = 'North'

	def action_sold(self):
		for record in self:
			if record.state == 'canceled':
				raise UserError("A canceled property cannot be set as sold.")
			record.state = 'sold'

	def action_cancel(self):
		for record in self:
			if record.state == 'sold':
				raise UserError("A sold property cannot be canceled.")
			record.state = 'canceled'

	_sql_constraints = [
		('check_positive_expected_price', 'CHECK(expected_price >= 0)', 'The expected price must be strictly positive.'),
		('check_positive_selling_price', 'CHECK(selling_price >= 0)', 'The Selling Price must be strictly positive'),
	]

	@api.constrains('selling_price','expected_price')
	def _check_selling_price(self):
		for record in self:
			if float_compare(record.selling_price,0.0, precision_digits=2) == 0:
				continue
			ninety_percent_expected_price = record.expected_price * 0.9
			if float_compare(record.selling_price, ninety_percent_expected_price, precision_digits=2) == -1:
				 raise ValidationError("Selling price cannot be lower than 90 % of the expected price.")


	@api.ondelete(at_uninstall=False) 
	def _check_property_deletion(self):
		for record in self:
			if record.state not in ['new','canceled']:
				raise ValidationError("You cannot delete properties that are not in 'New' or 'Canceled' state.")


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from random import randint

# -------------
# `res.partner` To add new Fields industry_id & tone_id 
# For the Suggested Trends and Enhancing Trends Visibility to related Tags
# -------------
class Partner(models.Model):
    _inherit = "res.partner"

    def _default_industry(self):
        return self.env['res.partner.industry_category'].browse(self._context.get('industry_id'))
    
    def _default_tone(self):
        return self.env['res.partner.tone'].browse(self._context.get('tone_id'))

    industry_id = fields.Many2many('res.partner.industry_category', column1='partner_id', column2='industry_id', string='Industry/Category', default=_default_industry)
    tone_id = fields.Many2many('res.partner.tone', column1='partner_id', column2='tone_id', string='Tone Type', default=_default_tone)
    
# ---------------------------------
# res.partner.industry_category 
# To Manage the Partner Industry/Category
# ---------------------------------
class PartnerIndustry(models.Model):
    _description = 'Partner Industry/Category'
    _name = 'res.partner.industry_category'
    _order = 'name'
    _parent_store = True

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Industry/Category Name', required=True, translate=True)
    color = fields.Integer(string='Color', default=_get_default_color)
    parent_id = fields.Many2one('res.partner.industry_category', string='Parent Industry/Category', index=True, ondelete='cascade')
    child_ids = fields.One2many('res.partner.industry_category', 'parent_id', string='Child Tags')
    active = fields.Boolean(default=True, help="The active field allows you to hide the industry without removing it.")
    parent_path = fields.Char(index=True, unaccent=False)
    partner_ids = fields.Many2many('res.partner', column1='industry_id', column2='partner_id', string='Partners', copy=False)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You can not create recursive tags.'))

    def name_get(self):
        """ Return the categories' display name, including their direct
            parent by default.

            If ``context['partner_industry_display']`` is ``'short'``, the short
            version of the industry name (without the direct parent) is used.
            The default is the long version.
        """
        if self._context.get('partner_industry_display') == 'short':
            return super(PartnerIndustry, self).name_get()

        res = []
        for industry in self:
            names = []
            current = industry
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((industry.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

# ---------------------------------
# res.partner.tone 
# To Manage the Partner Tone Type
# ---------------------------------
class PartnerToneType(models.Model):
    _description = 'Partner Tone Type'
    _name = 'res.partner.tone'
    _order = 'name'
    _parent_store = True

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Tone Type', required=True, translate=True)
    color = fields.Integer(string='Color', default=_get_default_color)
    parent_id = fields.Many2one('res.partner.tone', string='Parent Tone Type', index=True, ondelete='cascade')
    child_ids = fields.One2many('res.partner.tone', 'parent_id', string='Child Tags')
    active = fields.Boolean(default=True, help="The active field allows you to hide the tone without removing it.")
    parent_path = fields.Char(index=True, unaccent=False)
    partner_ids = fields.Many2many('res.partner', column1='tone_id', column2='partner_id', string='Partners', copy=False)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You can not create recursive tags.'))

    def name_get(self):
        """ Return the categories' display name, including their direct
            parent by default.

            If ``context['partner_tone_display']`` is ``'short'``, the short
            version of the tone name (without the direct parent) is used.
            The default is the long version.
        """
        if self._context.get('partner_tone_display') == 'short':
            return super(PartnerToneType, self).name_get()

        res = []
        for tone in self:
            names = []
            current = tone
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((tone.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

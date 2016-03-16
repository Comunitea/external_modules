## -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2013 QUIVAL, S.A. All Rights Reserved
#    $Pedro Gómez Campos$ <pegomez@elnogal.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields
from openerp.tools.translate import _
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from csv import writer as csvwriter
from base64 import b64encode
from datetime import datetime

import logging
log = logging.getLogger('l10n_es_intrastat')

from openerp import models, fields as fields2
import openerp.addons.decimal_precision as dp

def get_start_date(*args, **kwargs):
    # Don't like dateutil, not in the python battery pack
    now = datetime.today()
    try:
        now = now.replace(day=1, month=now.month-1) # Rewind the month and set first of month
    except ValueError:
        # Means we have to rewind to last year
        log.debug("had to rewind start_dat to last year, had exception", exc_info=True)
        now = now.replace(
            day=1,
            month=now.month+11,
            year=now.year-1
        )
    return now.strftime('%Y-%m-%d')

class l10n_es_intrastat(models.Model):
    _name = 'l10n.es.intrastat'
    _inherit = 'report.intrastat.common'
    _rec_name = 'start_date'
    _order = 'start_date desc, ttype'

    end_date = fields2.Date(
        compute='_compute_dates', string='End date', readonly=True, store=True,
        help="End date for the declaration. Must be the last day of the "
        "month of the start date.")
    num_lines = fields2.Integer(
        compute='_compute_numbers', string='Number of lines', store=True,
        track_visibility='always',
        help="Number of lines in this declaration.")
    total_amount = fields2.Float(
        compute='_compute_numbers', digits=dp.get_precision('Account'),
        string='Total amount', store=True, track_visibility='always',
        help="Total amount in company currency of the declaration.")

    # def _compute_numbers(self, cr, uid, ids, name, arg, context=None):
    #     return self.pool.get('report.intrastat.common')._compute_numbers(cr, uid, ids, self, context=context)

    def _compute_total_fiscal_amount(self, cr, uid, ids, name, arg, context=None):
        result = {}
        for intrastat in self.browse(cr, uid, ids, context=context):
            total_fiscal_amount = 0.0
            for line in intrastat.intrastat_line_ids:
                total_fiscal_amount += line.amount_company_currency * line.intrastat_type_id.fiscal_value_multiplier
            result[intrastat.id] = total_fiscal_amount
        return result

    def _compute_end_date(self, cr, uid, ids, name, arg, context=None):
        return
        # no funciona lo de abajo
        obj = self.browse(cr, uid, ids[0], context)
        return self.pool.get('report.intrastat.common')._compute_dates(cr, uid, ids, obj, context=context)

    def _get_intrastat_from_line(self, cr, uid, ids, context=None):
        return self.pool.get('l10n.es.intrastat').search(cr, uid, [('intrastat_line_ids', 'in', ids)], context=context)

    def _compute_total_weight(self, cr, uid, ids, name, arg, context=None):
        result = {}

        for intrastat in self.browse(cr, uid, ids, context=context):
            total_weight = 0.0
            for line in intrastat.intrastat_line_ids:
                total_weight += line.weight
            result[intrastat.id] = total_weight
        return result

    _columns = {
        'company_id': fields.many2one('res.company', 'Company', required=True, readonly=True, help="Related company."),
        'country_id': fields.related('company_id', 'country_id', readonly=True, type='integer', string='Country'),
        'start_date': fields.date('Start date', required=True, states={'done':[('readonly',True)]}, help="Start date of the declaration. Must be the first day of a month."),
        # 'end_date': fields.function(_compute_dates, method=True, type='date', string='End date', store={
        #     'l10n.es.intrastat': (lambda self, cr, uid, ids, c={}: ids, ['start_date'], 10),
                # }, help="End date for the declaration. Is the last day of the month of the start date."),
        'date_done' : fields.datetime('Date done', readonly=True, help="Last date when the intrastat declaration was converted to 'Done' state."),
        'data_source': fields.selection([
            ('move', 'Generate report from Stock Moves'),
            ('invoice', 'Generate report from Invoices'),
            ], string='Report Data Source', required=True),
        'state' : fields.selection([
            ('draft','Draft'),
            ('done','Done'),
        ], 'State', select=True, readonly=True, help="State of the declaration. When the state is set to 'Done', the parameters become read-only."),
                
        'ttype': fields.selection([
            ('I', 'I-Introduction'),
            ('E', 'E-Expedition')
            ], 'Type', required=True, states={'done':[('readonly',True)]}, help="Select the type of report."),
        'revision': fields.integer('Revision', readonly=True, help="Used to keep track of unique changes"),

        'intrastat_line_ids': fields.one2many('l10n.es.intrastat.line', 'parent_id', 'Intrastat product lines', states={'done':[('readonly',True)]}),
        # 'num_lines': fields.function(_compute_numbers, method=True, type='integer', multi='numbers', string='Number of lines', store={
        #     'l10n.es.intrastat.line': (_get_intrastat_from_line, ['parent_id'], 20),
        # }, help="Number of lines in this declaration."),
        'total_weight': fields.function(_compute_total_weight, method=True, digits=(16,3), string='Total weight', store={
            'l10n.es.intrastat.line': (_get_intrastat_from_line, ['weight'], 20),
            }, help="Total weight."),
        # 'total_amount': fields.function(_compute_numbers, method=True, digits=(16,2), multi='numbers', string='Total amount', store={
        #     'l10n.es.intrastat.line': (_get_intrastat_from_line, ['amount_company_currency', 'parent_id'], 20),
        #     }, help="Total amount in Company currency of the declaration."),
        'currency_id': fields.related('company_id', 'currency_id', readonly=True, type='many2one', relation='res.currency', string='Currency'),
        'notes' : fields.text('Notes', help="You can add some comments here if you want."),
        'merge_lines': fields.boolean('Merge lines', states={'done':[('readonly',True)]}, help="Check to combine the lines with the same intrastat code, country of origin/destination, type of transport, nature of transaction, etc."),
}

    _defaults = {
        'data_source': 'invoice',
        'state': 'draft',
        'ttype': 'E',
        'revision': 1,
        'start_date': get_start_date,
        'company_id': lambda self, cr, uid, ct: self.pool.get('res.users')._get_company(cr, uid, ct),
        'merge_lines': lambda *a: False,
    }

    _sql_constraints = [
        ('date_uniq', 'unique(start_date, company_id, ttype)', 'A declaration of the same type already exists for this month!'),
    ]

    def copy(self, cr, uid, ids, default=None, context=None):
        if 'intrastat_line_ids' not in default:
            default['intrastat_line_ids'] = []
        if 'start_date' not in default:
            default['start_date'] = False
        if 'revision' not in default:
            default['revision'] = False
        return super(l10n_es_intrastat, self).copy(cr, uid, ids, default, context)

    def write(self, cr, uid, ids, vals, context=None):
        res = super(l10n_es_intrastat, self).write(cr, uid, ids, vals, context)
        if 'skip_revision' not in context:
            cr.execute("UPDATE l10n_es_intrastat SET revision=revision+1 WHERE id in (%s)", [tuple(ids)] )
        return res

    def unlink(self, cr, uid, ids, context=None):
        for t in self.read(cr, uid, ids, ['state'], context=context):
            if t['state'] not in ('draft'):
                raise osv.except_osv(_('Invalid action !'), _('Cannot delete declaration(s) which are in state done!'))
        return super(l10n_es_intrastat, self).unlink(cr, uid, ids, context=context)

    def _find_stock_links(self, cr, uid, invoice_line, context=None):
        sm_obj = self.pool.get('stock.move')
        sale_line = self.pool.get('sale.order.line')
        purchase_line = self.pool.get('purchase.order.line')
        if sale_line:
            cr.execute("""
            SELECT sm.id
            FROM sale_order_line_invoice_rel solir
            INNER JOIN stock_move sm ON (sm.sale_line_id = solir.order_line_id)
            WHERE solir.invoice_id = %s
            """, (invoice_line.invoice_id.id,))
            stock_ids = [x[0] for x in cr.fetchall()]
            log.debug("found stock moves: %s", stock_ids)
            return sm_obj.browse(cr, uid, stock_ids, context=context)
        return []

    def _find_invoice_links(self, cr, uid, stock_line, context=None):
        res_invoices = []
        res_lines = []
        if hasattr(stock_line, 'sale_line_id'):
            if stock_line.sale_line_id:
                res_lines.extend( stock_line.sale_line_id.invoice_lines )
                res_invoices.extend( stock_line.sale_line_id.order_id.invoice_ids )
        if hasattr(stock_line, 'purchase_line_id'):
            if stock_line.purchase_line_id:
                res_lines.extend( stock_line.purchase_line_id.invoice_lines )
                res_invoices.extend( stock_line.purchase_line_id.order_id.invoice_ids )
        res_invoices = list(set(res_invoices))
        res_lines = list(set(res_lines))
        return res_invoices, res_lines

    def _gather_invoices(self, cr, uid, declaration, context=None):
        """ Search invoices between start_date and end_date of declaration """
        decl_lines = []
        cur_obj = self.pool.get('res.currency')
        inv_obj = self.pool.get('account.invoice')
        product_uom_obj = self.pool.get('product.uom')

        inv_ids = inv_obj.search(cr, uid, [
            ('date_invoice','>=',declaration.start_date),
            ('date_invoice','<=',declaration.end_date),
            ('state','not in',['draft','cancel']),
            ('company_id','=',declaration.company_id.id),
        ], context=context)
        log.debug("found %d invoices: %s", len(inv_ids), inv_ids)
        for invoice in inv_obj.browse(cr, uid, inv_ids, context=context):
            if invoice.fiscal_position and not invoice.fiscal_position.intracommunity_operations:
                # La posición fiscal de la factura indica que no está sujeta a operaciones intracomunitarias
                log.debug("invoice %s had fiscal position with intracommunity oparations = False", invoice.number)
                continue
            if not invoice.partner_id.commercial_partner_id.country_id:
                log.debug("invoice %s partner had no country, assuming same country as company and skipping", invoice.number)
                continue
            if not invoice.partner_id.commercial_partner_id.country_id.intrastat:
                log.debug("invoice %s partner was in country that doesnt require intrastat reporting", invoice.number)
                continue
            if invoice.partner_id.commercial_partner_id.country_id.id == declaration.company_id.partner_id.country_id.id:
                log.debug("invoice %s had same country of origin as Company", invoice.number)
                continue

            if declaration.ttype == 'I' and invoice.type in ['out_invoice','in_refund']:
                # Wrong declaration type for this sort of invoices
                continue
            elif declaration.ttype == 'E' and invoice.type in ['in_invoice','out_refund']:
                # Wrong declaration type for this sort of invoices
                continue

            trans_type = {
                'out_invoice': 1,
                'in_invoice': 1,
                'out_refund': 2,
                'in_refund': 2,
            }.get(invoice.type)
            
            for inv_line in invoice.invoice_line:
                if not inv_line.product_id:
                    log.debug("invoice line did not have a product")
                    continue
                if inv_line.product_id.type not in ['product','consu']:
                    log.debug("invoice line product was a service")
                    continue
                if inv_line.product_id.exclude_from_intrastat:
                    log.debug("product on invoice line was explicitly banned from intrastat")
                    continue

                intrastat = inv_line.product_id.intrastat_id or inv_line.product_id.categ_id.intrastat_id
                if not intrastat:
                    raise osv.except_osv(_('Configuration Error !'), 
                        _("Product without 'Intrastat code' defined." \
                          "\nPlease review the Intrastat settings for Product '[%s] %s'.") %(inv_line.product_id.default_code, inv_line.product_id.name))
                intrastat_code = intrastat.intrastat_code

                stock_moves = self._find_stock_links(cr, uid, inv_line, context)

                line_value = inv_line.price_subtotal
                
                #if not line_value: # Si la línea tiene precio cero, lo calculamos con el precio de venta del producto
                #    line_value = (inv_line.product_id.list_price * inv_line.quantity) or 0.0 # hay qye convertir la quantity a la unidad o usar qty_in_product_uom que esta mas abajo
                    
                if invoice.currency_id.id != declaration.company_id.currency_id.id:
                    # Convert the value to the company currency
                    line_value = cur_obj.compute(cr, uid, invoice.currency_id.id, declaration.company_id.currency_id.id, line_value, context=context)
                    
                # Nettogewicht is optioneel voor producten waarvoor 'aanvullende eenheden' verplicht zijn 
                # Cf. NBB document Gecombineerde Nomenclatuur, kolom "Bijzondere maatstaf" 
                if intrastat.intrastat_uom_id:
                    quantity = inv_line.quantity #creo que habria que convertir entre unidades TODO
                    weight = None
                else:
                    quantity = None
                    if not inv_line.product_id.weight_net:
                        p_name = inv_line.product_id.name + (inv_line.product_id.default_code and (' (ref: ' + inv_line.product_id.default_code + ')') or '')
                        raise osv.except_osv(_('Configuration Error !'), 
                            _("No 'Net Weight' defined for a product without Intrastat UOM." \
                              "\nPlease review the Intrastat settings for Product '%s' (Intrastat code '%s'.") %(p_name, intrastat.intrastat_code))
                    qty_in_product_uom = product_uom_obj._compute_qty(cr, uid, from_uom_id=inv_line.uos_id.id, qty=inv_line.quantity, to_uom_id=inv_line.product_id.uom_id.id)
                    weight = inv_line.product_id.weight_net * qty_in_product_uom

                incoterm_model, default_incoterm =  self.pool.get('ir.model.data').get_object_reference(cr, uid, 'stock', "incoterm_CIP")

                decl_lines.append( (0,0,{
                    'parent_id': declaration.id,
                    'invoice_id': invoice.id,
                    'invoice_line_id': inv_line.id,
                    'picking_id': False,
                    'move_id': False,
                    'country_id': invoice.partner_id.commercial_partner_id.country_id.id,
                    'state_id': invoice.company_id.state_id.id,
                    'incoterm_id': invoice.sale_order_ids and invoice.sale_order_ids[0].incoterm and invoice.sale_order_ids[0].incoterm.id or default_incoterm,
                    'product_id': inv_line.product_id.id,
                    'intrastat_id': intrastat.id,
                    'intrastat_code': intrastat_code,
                    'country_origin_id': False,
                    'statistical_procedure': 1,
                    'weight': weight or 0.0,
                    'supplementary_quantity': quantity or 0.0,
                    'amount_company_currency': line_value or 0.0,
                    'amount_statistic_company_currency': line_value or 0.0,
                    'transaction': 11,
                    'transport': 3,
                    'port_loading_unloading': False,
                    'extnr': invoice.number[-13:],
                }) )
            log.debug("invoice %s gave us following intrastat lines: %s", invoice.number, decl_lines)
        return decl_lines

    def _gather_stock(self, cr, uid, declaration, context=None):
        """
            Search stock moves between date (not invoiced on invoices processed before)
            To find the link requires that 'sale' or 'purchase' module is installed ?
        """
        decl_lines = []
        sm_obj = self.pool.get('stock.move')
        product_uom_obj = self.pool.get('product.uom')

        # Perhaps search on pickings where intrastat_declare
        # is False so we can use this as extra filter?

        stock_ids = sm_obj.search(cr, uid, [
            ('date','>=',declaration.start_date),
            ('date','<=',declaration.end_date),
            ('state','not in',['draft','cancel']),
            ('company_id','=',declaration.company_id.id),
        ], context=context)

        for move in sm_obj.browse(cr, uid, stock_ids, context=context):
            address = (move.partner_id and move.partner_id.commercial_partner_id) or (move.picking_id and move.picking_id.partner_id.commercial_partner_id)
            if not address:
                # Think of inventory/production/internal movements
                log.debug("stock move didnt seem to have an address")
                continue
            country = address.country_id or False
            if not country:
                log.debug("assuming no country means same as company country, so skipped")
                continue
            if country and not country.intrastat:
                log.debug("stock move was from/to country that doesnt require intrastat reporting")
                continue
            if country and country.id == declaration.company_id.partner_id.country_id.id:
                log.debug("stock move was from/to same country as company")
                continue
            if move.product_id.exclude_from_intrastat:
                log.debug("product %d explicitly banned from intrastat", move.product_id.id)
                continue

            value = move.price_unit or move.product_id.list_price
            ref = move.picking_id and move.picking_id.name or '%d [%s] %s' % (move.id, move.product_id.default_code, move.product_id.name)

            intrastat = move.product_id.intrastat_id or move.product_id.categ_id.intrastat_id
            if not intrastat:
                raise osv.except_osv(_('Configuration Error !'), 
                    _("Product without 'Intrastat code' defined." \
                      "\nPlease review the Intrastat settings for Product '[%s] %s'.") %(move.product_id.default_code, move.product_id.name))
            intrastat_code = intrastat.intrastat_code

            invoices, inv_lines = self._find_invoice_links(cr, uid, move, context)
            if invoices and invoices[0].fiscal_position and not invoices[0].fiscal_position.intracommunity_operations:
                # La posición fiscal de la factura indica que no está sujeta a operaciones intracomunitarias
                log.debug("the invoice realeted with move has fiscal position with intracommunity oparations = False")
                continue

            trans_type = False
            if move.location_id.usage == 'internal' and move.location_dest_id.usage in ['supplier','customer']:
                log.debug("stock move deemed to be a expedition")
                if declaration.ttype == 'E':
                    # TODO: handle the special case when company doesnt do
                    # delivery declarations but does do the arrival
                    trans_type = 1
                else:
                    # Skip line wrong type of declaration
                    continue
            elif move.location_dest_id.usage == 'internal' and move.location_id.usage in ['supplier','customer']:
                log.debug("stock move deemed to be introduction")
                if declaration.ttype == 'I':
                    # TODO: handle the special case when company doesnt do
                    # arrival declarations but does do the departure
                    trans_type = 1
                else:
                    # Skip line wrong type of declaration
                    continue
            else:
                # Doesn't seem to be arriving or leaving, ignore the line
                log.warn("stock move %d from %s to %s ignored", move.id, move.location_id.name, move.location_dest_id.name)
                continue

            # Nettogewicht is optioneel voor producten waarvoor 'aanvullende eenheden' verplicht zijn 
            # Cf. NBB document Gecombineerde Nomenclatuur, kolom "Bijzondere maatstaf" 
            if intrastat.intrastat_uom_id:
                quantity = move.product_qty
                weight = None
            else:
                quantity = None
                if not move.product_id.weight_net:
                    p_name = move.product_id.name + (move.product_id.default_code and (' (ref: ' + move.product_id.default_code + ')') or '')
                    raise osv.except_osv(_('Configuration Error !'), 
                        _("No 'Net Weight' defined for a product without Intrastat UOM." \
                          "\nPlease review the Intrastat settings for Product '%s' (Intrastat code '%s'.") %(p_name, intrastat.intrastat_code))
                qty_in_product_uom = product_uom_obj._compute_qty(cr, uid, from_uom_id=move.product_uom.id, qty=move.product_qty, to_uom_id=move.product_id.uom_id.id)
                weight = move.product_id.weight_net * qty_in_product_uom

            incoterm_model, default_incoterm =  self.pool.get('ir.model.data').get_object_reference(cr, uid, 'stock', "incoterm_CIP")

            decl_lines.append( (0,0,{
                'parent_id': declaration.id,
                'invoice_id': invoices and invoices[0].id,
                'invoice_line_id': inv_lines and inv_lines[0].id,
                'picking_id': move.picking_id and move.picking_id.id or False,
                'move_id': move.id,
                'country_id': country.id,
                'state_id': move.company_id.state_id.id,
                'incoterm_id': move.picking_id and move.picking_id.sale_id and move.picking_id.sale_id.incoterm and move.picking_id.sale_id.incoterm.id or default_incoterm,
                'product_id': move.product_id.id,
                'intrastat_id': intrastat and intrastat.id,
                'intrastat_code': intrastat_code,
                'country_origin_id': False,
                'statistical_procedure': 1,
                'weight': weight or 0.0,
                'supplementary_quantity': quantity or 0.0,
                'amount_company_currency': (value * move.product_qty) or 0.0,
                'amount_statistic_company_currency': (value * move.product_qty) or 0.0,
                'transaction': 11,
                'transport': 3,
                'port_loading_unloading': False,
                'extnr': ref[:13],
            }) )
        return decl_lines

    def action_gather(self, cr, uid, ids, context=None):
        context = context or {}
        log.debug("gathering lines for declarations: %s", ids)

        cur_obj = self.pool.get('res.currency')
        inv_obj = self.pool.get('account.invoice')
        sm_obj = self.pool.get('stock.move')
        intr_line_obj = self.pool.get('l10n.es.intrastat.line')

        # Call function which will update the lines, preferably in one write
        # operation so the revision number does not go up much (or even nothing)
        for declaration in self.browse(cr, uid, ids, context=context):
            # Should we clear [(6,0,[])] previous lines ?
            #decl_lines = [(6,0,[])]
            decl_lines = []
            
            if declaration.data_source == 'move':
                decl_lines += self._gather_stock(cr, uid, declaration, context)
            elif declaration.data_source == 'invoice':
                decl_lines += self._gather_invoices(cr, uid, declaration, context)
            else:
                raise osv.except_osv(_('Programming Error !'), 
                    _('Please report this issue via your OpenERP support channel.'))
            
            # Drop existing lines
            line_ids = ids and intr_line_obj.search(cr, uid, [('parent_id', '=', declaration.id)]) or False
            if line_ids:
                intr_line_obj.unlink(cr, uid, line_ids)
                
            if declaration.merge_lines:
                # Combine similar records
                lines_combined = [] 
                for i in range(len(decl_lines)):
                    similar = False
                    for j in range(len(lines_combined)):
                        if decl_lines[i][2]['country_id'] == lines_combined[j][2]['country_id'] and \
                            decl_lines[i][2]['state_id'] == lines_combined[j][2]['state_id'] and \
                            decl_lines[i][2]['incoterm_id'] == lines_combined[j][2]['incoterm_id'] and \
                            decl_lines[i][2]['transaction'] == lines_combined[j][2]['transaction'] and \
                            decl_lines[i][2]['transport'] == lines_combined[j][2]['transport'] and \
                            decl_lines[i][2]['port_loading_unloading'] == lines_combined[j][2]['port_loading_unloading'] and \
                            decl_lines[i][2]['intrastat_code'] == lines_combined[j][2]['intrastat_code'] and \
                            decl_lines[i][2]['country_origin_id'] == lines_combined[j][2]['country_origin_id'] and \
                            decl_lines[i][2]['statistical_procedure'] == lines_combined[j][2]['statistical_procedure']:
                            
                            similar = True
                            
                            lines_combined[j][2]['invoice_id'] = False
                            lines_combined[j][2]['invoice_line_id'] = False
                            lines_combined[j][2]['picking_id'] = False
                            lines_combined[j][2]['move_id'] = False
                            lines_combined[j][2]['extnr'] = False
    
                            lines_combined[j][2]['weight'] += decl_lines[i][2]['weight'] or 0.0
                            lines_combined[j][2]['supplementary_quantity'] += decl_lines[i][2]['supplementary_quantity'] or 0.0
                            lines_combined[j][2]['amount_company_currency'] += decl_lines[i][2]['amount_company_currency'] or 0.0
                            lines_combined[j][2]['amount_statistic_company_currency'] += decl_lines[i][2]['amount_statistic_company_currency'] or 0.0
                    if not similar:
                        lines_combined.append(decl_lines[i])
                decl_lines = lines_combined

            # Store intrastat lines
            declaration.write({'intrastat_line_ids': decl_lines,}, context=context)

        return True

    def action_send(self, cr, uid, ids, context=None):
        context = context or {}
        # Create itx file + send (maybe ask email to send from ?)

        itx_buffer = StringIO()
        itx_file = csvwriter(itx_buffer, delimiter=';')

        today = datetime.today()
        for declaration in self.browse(cr, uid, ids, context=context):
            decl_date = datetime.strptime( declaration.start_date, "%Y-%m-%d" )
            vat_no = declaration.company_id.partner_id.vat
            if not vat_no:
                raise osv.except_osv(_('Data Insufficient'), _('No VAT Number Associated with Main Company!'))
            vat_no = vat_no.replace(' ','').upper()
            vat = vat_no[2:]
            itx_head = [
                # Field 1: Identification declarant (10 digit company number or 9 digit VAT number)
                vat_no[2:],
                # Field 2, Field 3: Third party VAT number + zip code
                '', '',
                # Field 4 : Declaration id
                '%s%s' % (str(declaration.id).zfill(4)[-4:], str(declaration.revision).zfill(4)[-4:]),
            ]

            lines_all = []
            for intrastat_line in declaration.intrastat_line_ids:
                
                if not intrastat_line.country_code:
                    raise osv.except_osv(_("Missing code of country origin/destination"), 
                                         _("The line with source reference %s has no code of country origin/destination selected") % intrastat_line.extnr)
                if not intrastat_line.state_code:
                    raise osv.except_osv(_("Missing state of origin/destination"), 
                                         _("The line with source reference %s has no State of origin/destination selected") % intrastat_line.extnr)
                if not intrastat_line.incoterm:
                    raise osv.except_osv(_("Missing incoterm"), 
                                         _("The line with source reference %s has no incoterm selected") % intrastat_line.extnr)
                if not intrastat_line.transaction:
                    raise osv.except_osv(_("Missing nature of transaction"), 
                                         _("The line with source reference %s has no nature of transaction selected") % intrastat_line.extnr)
                if not intrastat_line.transport:
                    raise osv.except_osv(_("Missing transport"), 
                                         _("The line with source reference %s has no transport selected") % intrastat_line.extnr)
                if not intrastat_line.intrastat_code:
                    raise osv.except_osv(_("Missing intrastat code"), 
                                         _("The line with source reference %s has no intrastat code selected") % intrastat_line.extnr)
                if not intrastat_line.statistical_procedure:
                    raise osv.except_osv(_("Missing statistical procedure"), 
                                         _("The line with source reference %s has no statistical procedure selected") % intrastat_line.extnr)

                lines_all.append({ 
                    'match': [ 
                        intrastat_line.country_code or '', # Field 1
                        intrastat_line.state_code or '', # Field 2
                        intrastat_line.incoterm or '', # Field 3
                        intrastat_line.transaction or '', # Field 4
                        intrastat_line.transport or '', # Field 5
                        intrastat_line.port_loading_unloading or '', # Field 6
                        intrastat_line.intrastat_code.replace(' ', ''), # Field 7
                        intrastat_line.country_origin or '', # Field 8
                        intrastat_line.statistical_procedure or '', # Field 9
                        declaration.currency_id.name, # No se exporta
                        ],
                    'vals': [ 
                        round(intrastat_line.weight,3), # Field 10
                        round(intrastat_line.supplementary_quantity,3), # Field 11
                        round(intrastat_line.amount_company_currency,2), # Field 12
                        round(intrastat_line.amount_statistic_company_currency,2), # Field 13
                        ],
                    })
                    
            # combine similar records
            lines_combined = [] 
            for i in range(len(lines_all)):
                similar = False
                for j in range(len(lines_combined)):
                    if lines_all[i]['match'] == lines_combined[j]['match']:
                        similar = True
                        lines_combined[j]={
                            'match': lines_combined[j]['match'],
                            'vals': map(lambda x,y: x+y, lines_all[i]['vals'], lines_combined[j]['vals']),
                            }
                if not similar:
                    lines_combined.append(lines_all[i])
            
            #itx_lines = map(lambda x: x['match'][:9] + x['vals'][:4], lines_combined)
            itx_lines = map(lambda x: 
                            x['match'][:9] + 
                            ['{0:.3f}'.format(x['vals'][0]).replace('.', ',')] + #Utilizamos como separador decimal la coma 
                            ['{0:.3f}'.format(x['vals'][1]).replace('.', ',')] + #Utilizamos como separador decimal la coma
                            ['{0:.2f}'.format(x['vals'][2]).replace('.', ',')] + #Utilizamos como separador decimal la coma
                            ['{0:.2f}'.format(x['vals'][3]).replace('.', ',')],  #Utilizamos como separador decimal la coma
                            lines_combined)
            for line in itx_lines:
                if line[9] == '0,000' and line[10] == '0,000': #Utilizamos como separador decimal la coma
                    raise osv.except_osv(_("Missing weight or supplementary quantity"), 
                                         _("The line with intrastat code %s may not have weight or supplementary quantity equal to zero") % line[6])
                if line[11] == '0,00' or line[12] == '0,00': #Utilizamos como separador decimal la coma
                    raise osv.except_osv(_("Missing declared value and/or statistic declared value"), 
                                         _("The line with intrastat code %s may not have declared value and/or statistic declared value equal to zero") % line[6])
                itx_line = line                
                itx_file.writerow(itx_line)

            filename = '%s%02d%02d%s%s.itx' % (
                declaration.ttype,
                decl_date.year,
                decl_date.month,
                str(declaration.id).zfill(2)[-2:],
                str(declaration.revision).zfill(2)[-2:],
            )

            att_id = self.pool.get('ir.attachment').create(cr, uid, {
                'res_id': declaration.id,
                'res_model': self._name,
                'name': filename,
                'datas': b64encode(itx_buffer.getvalue()),
            }, context=context)
            
        context.update({'skip_revision': True})
        return self.write(cr, uid, ids, {'state': 'done', 'date_done': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}, context=context)

    def action_reset(self, cr, uid, ids, context=None):
        context = context or {}
        context.update({'skip_revision': True})
        return self.write(cr, uid, ids, {'state': 'draft', 'date_done': False}, context=context)

    def action_done(self, cr, uid, ids, context=None):
        context = context or {}
        context.update({'skip_revision': True})
        return self.write(cr, uid, ids, {'state': 'done', 'date_done': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}, context=context)
    
l10n_es_intrastat()

class l10n_es_intrastat_line(osv.osv):
    _name = 'l10n.es.intrastat.line'

    _columns = {
        'parent_id': fields.many2one('l10n.es.intrastat', 'Intrastat product ref', ondelete='cascade', readonly=True),

        'invoice_id': fields.many2one('account.invoice', 'Invoice ref', readonly=True),
        'invoice_line_id': fields.many2one('account.invoice.line', 'Invoice line', readonly=True),
        'picking_id': fields.many2one('stock.picking', 'Picking ref', readonly=True),
        'move_id': fields.many2one('stock.move', 'Stock move', readonly=True),

        'country_id' : fields.many2one('res.country', 'Country of origin/destination'),
        'country_origin_id' : fields.many2one('res.country', 'Country origin of product', help='Country origin of product manufactured'),
        'state_id' : fields.many2one('res.country.state', 'State of origin/destination'),
        'incoterm_id': fields.many2one('stock.incoterms', 'Incoterm'),
        'product_id': fields.many2one('product.product', 'Product'),
        'intrastat_id': fields.many2one('report.intrastat.code', 'Intrastat Code'),

        # Campo 1: Estado miembro de procedencia/destino(A2) - Código ISO del Estado Miembro de Procedencia/Destino de la mercancía, en formato alfanumérico de dos posiciones.
        'country_code' : fields.related('country_id', 'code', type='char', size=2, string='Code of country origin/destination', readonly=True),
        # Campo 2: Provincia de destino/origen(N2) - Código de provincia española de origen/destino de la mercancía, en formato numérico de dos posiciones.
        'state_code' : fields.related('state_id', 'code', type='char', size=2, string='Code of spanish state origin/destination', readonly=True),
        # Campo 3: Condiciones de entrega(A3) - Código de las condiciones de entrega, en formato alfanumérico de tres posiciones.
        'incoterm': fields.related('incoterm_id', 'code', type='char', size=3, string='Incoterm Code', readonly=True),
        # Campo 4: Naturaleza de la Transacción(N2) - Código de la Naturaleza de la transacción, en formato numérico de dos posiciones.
        'transaction' : fields.selection([
            (11, '11-Compraventa en firme'),
            (12, '12-Entrega para venta a la vista o de prueba, para consignación o con la mediación de un agente comisionista'),
            (13, '13-Trueque (compensación en especies)'),
            (14, '14-Arrendamiento financiero (alquiler-venta)'),
            (15, '15-Compras personales de viajeros'),
            (19, '19-Otras'),
            (21, '21-Devolución de mercancías'),
            (22, '22-Sustitución de mercancías devueltas'),
            (23, '23-Sustitución (por ejemplo bajo garantía) de mercancías no devueltas'),
            (29, '29-Otras'),
            (31, '31-Mercancías suministradas en el marco de programas de ayuda promovidos o financiados parcial o totalmente por la Comunidad Europea'),
            (32, '32-Otras ayudas gubernamentales'),
            (33, '33-Otras'),
            (41, '41-Mercancías destinadas a regresar al país de exportación inicial'),
            (42, '42-Mercancías no destinadas a regresar al país de exportación inicial'),
            (44, '44-Operaciones con vistas a una transformación o una reparación: Reparación o mantenimiento a título gratuitos'),
            (45, '45-Operaciones con vistas a una transformación o una reparación: Reparación o mantenimiento a título oneroso'),
            (51, '51-Mercancías que regresan al país de exportación inicial'),
            (52, '52-Mercancías que no regresan al país de exportación inicial'),
            (54, '54-Operaciones consiguientes a una transformación: Reparación o mantenimiento a título gratuitos'),
            (55, '55-Operaciones consiguientes a una transformación: Reparación o mantenimiento a título oneroso'),
            (61, '61-Alquiler, préstamo arrendamiento operativo'),
            (62, '62-Otros usos temporales'),
            (70, '70-Operaciones en el marco de programas comunes de defensa u otros programas intergubernamentales de fabricación conjunta (ejemplo Airbus)'),
            (80, '80-Suministro de materiales y maquinaria en el marco de un contrato general de construcción o de ingeniería civil para el que no sea necesaria una facturación sepa'),
            (91, '91-Alquiler, préstamo y arrendamiento operativo superior a 24 meses'),
            (99, '99-Otras'),
            ], 'Nature of transaction'),
        # Campo 5: Modalidad de Transporte(N1) - Código del modo de transporte, en formato numérico de una posición.
        'transport' : fields.selection([
            (1, '1-Transport by sea'),
            (2, '2-Transport by rail'),
            (3, '3-Transport by road'),
            (4, '4-Transport by air'),
            (5, '5-Consignments by post'),
            (7, '7-Fixed transport installations'),
            (8, '8-Transport by inland waterway'),
            (9, '9-Own propulsion'),
            ], 'Type of transport'),
        # Campo 6: Puerto/Aeropuerto de Carga o Descarga(N4) - Código del puerto/aeropuerto español de carga/descarga de la mercancía en formato numérico de cuatro posiciones.
        'port_loading_unloading': fields.integer('Spanish port of loading/unloading', size=4),
        # Campo 7: Código de las mercancias(N8)(*) - Código de nomenclatura combinada correspondiente a la mercancía en formato alfanumérico de ocho posiciones. 
        #          Si la mercancía cumplimentada requiere código adicional, el formato del campo será (N8) + (A4)
        'intrastat_code': fields.char('Intrastat Code', size=10, required=True, readonly=True),
        # Campo 8: País de Origen(A2) - Código ISO del país de origen, en formato alfanumérico de dos posiciones.
        'country_origin' : fields.related('country_origin_id', 'code', type='char', size=2, string='Country origin of product', help='ISO Code of country origin of product manufactured', readonly=True),
        # Campo 9: Régimen estadístico(N1) - Código del Régimen Estadístico, en formato numérico de una posición.
        'statistical_procedure' : fields.selection([
            (1, '1-Mercancías destino final estado miembro'),
            (2, '2-Mercancías destino final estado miembro'),
            (3, '3-Mercancias reexpedidas después de transformar'),
            (4, '4-Mercancías devueltas sin transformar'),
            (5, '5-Mercancías devueltas, transformadas o reexpedidas previamente expedidas'),
            ], 'Statistical procedure'),
        # Campo 10: Masa Neta en Kg.(N12 ó N12,3) - Masa Neta de la mercancía, expresada en kilogramos. Formato numérico, máximo doce enteros y tres decimales separados por coma.
        'weight': fields.float('Weight', digits=(12,3), required=True),
        # Campo 11: Unidades Suplementarias(N12 ó N12,3) - Cantidad de unidades suplementarias. Formato numérico, máximo doce enteros y tres decimales separados por coma.
        'supplementary_quantity': fields.float('Supplem. qty', digits=(12,3), help='Supplementary quantity'),
        # Campo 12: Importe Facturado(N13,2) - Importe de factura de la mercancía, expresado en euros con dos decimales. Formato numérico, máximo trece enteros y dos decimales separados por coma.
        'amount_company_currency': fields.float('Invoice amount', digits=(13,2), required=True),
        # Campo 13: Valor Estadístico(N13,2) - Valor estadístico de la mercancía, expresado en euros con dos decimales. Formato numérico, máximo trece enteros y dos decimales separados por coma.
        'amount_statistic_company_currency': fields.float('Statistical value', digits=(13,2), required=True),
        # Field 17: Externe informatie (13 variable XX)
        'extnr': fields.char('Source reference', size=13, required=False),
        #'company_id': fields.related('parent_id', 'company_id', type='many2one', relation='res.company', string='Company', store=True, readonly=True),
    }
    
    _order = 'country_id, incoterm_id, transaction, transport, intrastat_code, statistical_procedure'

    def onchange_country(self, cr, uid, ids, country_id, context=None):
        res = {'value': {}}
        if country_id:
            country = self.pool.get('res.country').browse(cr, uid, country_id, context=context)
            res['value'].update({
                'country_id': country.id,
                'country_code': country.code,
            })
        return res

    def onchange_state(self, cr, uid, ids, state_id, context=None):
        res = {'value': {}}
        if state_id:
            state = self.pool.get('res.country.state').browse(cr, uid, state_id, context=context)
            res['value'].update({
                'state_id': state.id,
                'state_code': state.code,
            })
        return res

    def onchange_product(self, cr, uid, ids, product_id, qty, context=None):
        res = {'value': {}}
        if product_id:
            product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            res['value'].update({
                'intrastat_id': product.intrastat_id.id,
                'intrastat_code': product.intrastat_id.intrastat_code,
            })
            if qty:
                res['value'].update({
                    'weight': str(int(round(int(qty) * product.weight_net))),
                })
        return res

    def onchange_qty(self, cr, uid, ids, product_id, qty, context=None):
        res = {'value': {}}
        if product_id and qty:
            product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            res['value'].update({
                'weight': str(int(round(int(qty) * product.weight_net))),
            })
        return res
    
l10n_es_intrastat_line()

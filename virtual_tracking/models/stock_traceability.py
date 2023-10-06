from odoo import _, api, models


class MrpStockReport(models.TransientModel):
    _inherit = "stock.traceability.report"

    """
    @api.model
    def _get_linked_move_lines(self, move_line):

        #import ipdb; ipdb.set_trace()
        res = super()._get_linked_move_lines(move_line)
        return res
        move_lines, is_used = super(MrpStockReport, self)._get_linked_move_lines(move_line)
        if not move_lines:
            move_lines = move_line.move_id.repair_id and move_line.consume_line_ids
        if not is_used:
            is_used = move_line.move_id.repair_id and move_line.produce_line_ids
        return move_lines, is_used
    """

    @api.model
    def get_lines(self, line_id=None, **kw):
        context = dict(self.env.context)
        if not context and kw.get("active_lot_name", False):
            context.update(active_lot_name=kw["active_lot_name"])
        rec_id = kw and kw["model_id"] or context.get("active_id")
        model = kw and kw["model_name"] or context.get("model")
        ## instancio el lote para ver como es
        level = kw and kw["level"] or 1
        if rec_id and model == "stock.lot":
            move = self.env["stock.move"]
            spl = self.env["stock.lot"]
            lot_id = spl.browse(rec_id)
            if lot_id and lot_id.product_id.virtual_tracking:
                context.update({"tracking_lot_id": lot_id})
                lines = self.env["stock.move.line"]
                for move in lot_id.move_ids:
                    lines |= move.move_line_ids[0]
                move_line_vals = self.with_context(context)._lines(
                    line_id, model_id=rec_id, model=model, level=level, move_lines=lines
                )
                final_vals = sorted(
                    move_line_vals, key=lambda v: v["date"], reverse=True
                )
                lines = self.with_context(context)._final_vals_to_lines(
                    final_vals, level
                )
                return lines
        elif rec_id and model in ("stock.picking", "mrp.production"):
            record = self.env[model].browse(rec_id)
            if model == "stock.picking":
                lines = record.move_lines.mapped("move_line_ids").filtered(
                    lambda m: (m.serial_ids or m.lot_id) and m.state == "done"
                )
                move_line_vals = self.with_context(context)._lines(
                    line_id, model_id=rec_id, model=model, level=level, move_lines=lines
                )
                final_vals = sorted(
                    move_line_vals, key=lambda v: v["date"], reverse=True
                )
                lines = self.with_context(context)._final_vals_to_lines(
                    final_vals, level
                )
                return lines
        return super().get_lines(line_id=line_id, **kw)

    """
    @api.model
    def _lines(self, line_id=None, model_id=False, model=False, level=0, move_lines=[], **kw):
        return super()._lines(line_id, model_id, model, level, move_lines, **kw)
    """

    def _make_dict_move(self, level, parent_id, move_line, unfoldable=False):
        def update_vals():
            res = {
                "lot_name": lot_id.name,
                "lot_id": lot_id.id,
                "product_qty_uom": "%s %s"
                % (
                    self._quantity_to_str(
                        move_line.product_uom_id, move_line.product_id.uom_id, 1
                    ),
                    move_line.product_id.uom_id.name,
                ),

                "location_source": move_line.location_id.name,
                "location_destination": move_line.location_dest_id.name,
                ## "location_source": move_line.move_id.location_id.name,
                ## "location_destination": move_line.move_id.location_dest_id.name,
            }
            return res

        data = super()._make_dict_move(
            level=level, parent_id=parent_id, move_line=move_line, unfoldable=unfoldable
        )
        if not move_line.product_id.template_tracking == 'virtual':
            return data
        model = self._context.get("model", False)
        active_id = self._context.get("active_id", False)
        if (
            move_line._name == "stock.move.line"
            and move_line.serial_ids
            and not move_line.lot_id
        ):
            if model == "stock.lot" and active_id:
                lot_id = move_line.serial_ids.filtered(lambda x: x.id == active_id)
                data[0].update(update_vals())
                return data
            else:
                new_data = []
                for lot_id in move_line.serial_ids:
                    template = data[0].copy()
                    template.update(update_vals())
                    new_data.append(template)
                return new_data
        context_lot_name = self._context.get("lot_name", False) or self._context.get(
            "active_lot_name", False
        )
        lot_id = data[0].get("lot_id", False)
        if lot_id:
            return data

        if self._context.get("tracking_lot_id", False):
            lot_id = self._context["tracking_lot_id"]
            if lot_id:
                data[0].update(update_vals())
        elif data[0].get("res_model") == "mrp.production":
            if move_line.production_id:
                lot_id = self.env["stock.lot"].search(
                    [
                        ("product_id", "=", move_line.product_id.id),
                        ("name", "=", context_lot_name),
                    ]
                )
            elif move_line.move_id.production_id:
                # Salida de una producción.
                lot_id = self.env["stock.lot"].search(
                    [
                        ("product_id", "=", move_line.product_id.id),
                        ("name", "=", context_lot_name),
                    ]
                )
            if lot_id:
                data[0].update(update_vals())
        # if not data[0]['lot_id']:
        # import ipdb; ipdb.set_trace()
        return data

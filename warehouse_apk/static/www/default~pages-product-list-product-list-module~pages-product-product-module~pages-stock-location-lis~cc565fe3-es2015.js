(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~pages-product-list-product-list-module~pages-product-product-module~pages-stock-location-lis~cc565fe3"],{

/***/ "./src/app/services/stock.service.ts":
/*!*******************************************!*\
  !*** ./src/app/services/stock.service.ts ***!
  \*******************************************/
/*! exports provided: StockService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockService", function() { return StockService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/fesm2015/ionic-storage.js");
/* harmony import */ var _odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./odoo.service */ "./src/app/services/odoo.service.ts");





let StockService = class StockService {
    constructor(odooCon, alertCtrl, storage) {
        this.odooCon = odooCon;
        this.alertCtrl = alertCtrl;
        this.storage = storage;
        this.STOCK_FIELDS = {
            'stock.picking': {
                'tree': ['id', 'name', 'location_id', 'location_dest_id', 'scheduled_date', 'state', 'picking_fields'],
                'form': ['id', 'name', 'location_id', 'location_dest_id', 'scheduled_date', 'state', 'group_code',
                    'picking_type_id', 'priority', 'note', 'move_lines', 'move_line_ids', 'quantity_done', 'picking_fields',
                    'reserved_availability', 'product_uom_qty', 'show_check_availability',
                    'show_validate']
            },
            'stock.move': {
                'tree': ['id', 'product_id', 'product_uom_qty', 'reserved_availability', 'quantity_done', 'tracking'],
                'form': ['id', 'product_id', 'product_uom_qty', 'reserved_availability', 'quantity_done', 'state', 'tracking']
            },
            'stock.move.line': {
                'tree': ['id', 'product_id', 'product_uom_qty', 'qty_available', 'qty_done', 'location_id', 'location_dest_id', 'lot_id',
                    'package_id', 'result_package_id', 'tracking'],
                'form': ['id', 'product_id', 'product_uom_qty', 'qty_available', 'qty_done', 'location_id', 'location_dest_id', 'lot_id',
                    'package_id', 'result_package_id', 'state', 'picking_id', 'tracking']
            },
            'product.product': {
                'tree': ['id', 'name', 'default_code', 'list_price', 'qty_available', 'virtual_available'],
                'form': ['id', 'name', 'default_code', 'list_price', 'standard_price', 'qty_available', 'virtual_available', 'categ_id', 'tracking',
                    'barcode', 'description_short', 'image_medium'],
                'location-tree': ['id', 'name', 'default_code', 'list_price', 'last_purchase_price', 'qty_available', 'virtual_available', 'tracking',
                    'barcode', 'uom_id']
            },
            'stock.location': {
                'tree': ['id', 'display_name', 'usage', 'company_id'],
                'form': ['id', 'display_name', 'usage', 'company_id', 'picking_type_id']
            },
            'stock.quant': {
                'tree': ['id', 'product_id', 'reserved_quantity', 'quantity'],
                'form': ['id', 'product_id', 'reserved_quantity', 'quantity']
            },
            'stock.picking.type': {
                'tree': ['id', 'name', 'color', 'warehouse_id', 'code'],
                'form': ['id', 'name', 'color', 'warehouse_id', 'code', 'count_picking_ready', 'count_picking_waiting', 'count_picking_late', 'group_code',
                    'count_picking_backorders', 'rate_picking_late', 'rate_picking_backorders']
            }
        };
        console.log('Hello StockProvider Provider');
    }
    // Pickings
    get_picking_list(view_domain, type_id, offset = 0, limit = 0, search) {
        let self = this;
        let domain = [];
        if (view_domain) {
            view_domain.forEach(lit_domain => {
                domain.push(lit_domain);
            });
        }
        if (type_id) {
            domain.push(['picking_type_id', '=', Number(type_id)]);
        }
        if (search) {
            domain.push(['name', 'ilike', '%' + search + '%']);
        }
        let model = 'stock.picking';
        let fields = this.STOCK_FIELDS[model]['tree'];
        let promise = new Promise((resolve, reject) => {
            self.odooCon.search_read(model, domain, fields, offset, limit).then((data) => {
                for (let sm_id in data) {
                    data[sm_id]['model'] = model;
                }
                resolve(data);
            })
                .catch((err) => {
                reject(err);
            });
        });
        return promise;
    }
    get_picking_info(picking_id) {
        let self = this;
        let domain = [['id', '=', picking_id]];
        let model = 'stock.picking';
        let fields = this.STOCK_FIELDS[model]['form'];
        let promise = new Promise((resolve, reject) => {
            self.odooCon.search_read(model, domain, fields, 0, 0).then((data) => {
                for (let sm_id in data) {
                    data[sm_id]['model'] = model;
                }
                resolve(data);
            })
                .catch((err) => {
                reject(err);
            });
        });
        return promise;
    }
    get_picking_types(picking_codes, offset = 0, limit = 0, search) {
        let self = this;
        let domain = [];
        domain = [['code', 'in', picking_codes], ['active', '=', true], ['app_integrated', '=', true]];
        if (search) {
            domain.push(['name', 'ilike', search]);
        }
        let model = 'stock.picking.type';
        let fields = this.STOCK_FIELDS[model]['form'];
        let promise = new Promise((resolve, reject) => {
            self.odooCon.search_read(model, domain, fields, offset, limit).then((data) => {
                for (let sm_id in data) {
                    data[sm_id]['model'] = model;
                }
                resolve(data);
            })
                .catch((err) => {
                reject(err);
            });
        });
        return promise;
    }
    action_assign(pick_id) {
        let self = this;
        let model;
        let values = {
            'id': pick_id
        };
        model = 'stock.picking';
        let promise = new Promise((resolve, reject) => {
            self.odooCon.execute(model, 'action_assign_pick', values).then((done) => {
                resolve(done);
            })
                .catch((err) => {
                reject(false);
                console.log("Error al validar");
            });
        });
        return promise;
    }
    button_validate(pick_id) {
        let self = this;
        let model;
        let values = {
            'id': pick_id
        };
        model = 'stock.picking';
        let promise = new Promise((resolve, reject) => {
            console.log("button validate pick");
            console.log(pick_id);
            self.odooCon.execute(model, 'button_validate_pick', values).then((done) => {
                resolve(done);
            })
                .catch((err) => {
                reject(err['msg']['error_msg']);
                console.log("Error al validar");
            });
        });
        return promise;
    }
    // Move_lines
    get_move_lines_list_search(line_ids) {
        let self = this;
        let domain = [['id', 'in', line_ids]];
        let model = 'stock.move';
        let fields = this.STOCK_FIELDS[model]['tree'];
        let promise = new Promise((resolve, reject) => {
            self.odooCon.search_read(model, domain, fields, 0, 0).then((data) => {
                for (let sm_id in data) {
                    data[sm_id]['model'] = model;
                }
                resolve(data);
            })
                .catch((err) => {
                reject(err);
            });
        });
        return promise;
    }
    get_move_lines_list(line_ids) {
        let self = this;
        let domain = [['id', 'in', line_ids]];
        let model = 'stock.move';
        let fields = this.STOCK_FIELDS[model]['tree'];
        let values = { 'domain': domain, 'fields': fields, 'model': model };
        let promise = new Promise((resolve, reject) => {
            self.odooCon.execute(model, 'get_apk_object', values).then((data) => {
                for (let sm_id in data) {
                    data[sm_id]['model'] = model;
                }
                resolve(data);
            })
                .catch((err) => {
                reject(err);
            });
        });
        return promise;
    }
    get_move_lines_details_list(line_ids) {
        let self = this;
        let domain = [['id', 'in', line_ids]];
        let model = 'stock.move.line';
        let fields = this.STOCK_FIELDS[model]['tree'];
        let promise = new Promise((resolve, reject) => {
            self.odooCon.search_read(model, domain, fields, 0, 0).then((data) => {
                for (let sm_id in data) {
                    data[sm_id]['model'] = model;
                }
                resolve(data);
            })
                .catch((err) => {
                reject(err);
            });
        });
        return promise;
    }
    force_set_assigned_qty_done(move_id, model = 'stock.move') {
        let self = this;
        let values = {
            'id': move_id
        };
        let promise = new Promise((resolve, reject) => {
            self.odooCon.execute(model, 'force_set_assigned_qty_done_apk', values).then((done) => {
                resolve(done);
            })
                .catch((err) => {
                reject(false);
                console.log("Error al validar");
            });
        });
        return promise;
    }
    force_set_reserved_qty_done(move_id, model = 'stock.move') {
        let self = this;
        let values = {
            'id': move_id
        };
        let promise = new Promise((resolve, reject) => {
            self.odooCon.execute(model, 'force_set_reserved_qty_done_apk', values).then((done) => {
                resolve(done);
            })
                .catch((err) => {
                reject(false);
                console.log("Error al validar");
            });
        });
        return promise;
    }
    force_set_qty_done(move_id, field, model = 'stock.move.line') {
        let self = this;
        let values = {
            'id': move_id,
            'field': field
        };
        let promise = new Promise((resolve, reject) => {
            self.odooCon.execute(model, 'force_set_qty_done_apk', values).then((done) => {
                console.log(done);
                resolve(done);
            })
                .catch((err) => {
                reject(false);
                console.log("Error al validar");
            });
        });
        return promise;
    }
    force_set_qty_done_by_product_code_apk(product_code, field, model = 'stock.move.line', picking) {
        let self = this;
        let values = {
            'default_code': product_code,
            'field': field,
            'picking': picking
        };
        let promise = new Promise((resolve, reject) => {
            self.odooCon.execute(model, 'force_set_qty_done_by_product_code_apk', values).then((done) => {
                console.log(done);
                resolve(done);
            })
                .catch((err) => {
                reject(false);
                console.log("Error al validar");
            });
        });
        return promise;
    }
    force_reset_qties(pick_id, model = 'stock.picking') {
        let self = this;
        let values = {
            'id': pick_id
        };
        let promise = new Promise((resolve, reject) => {
            self.odooCon.execute(model, 'force_reset_qties_apk', values).then((done) => {
                resolve(done);
            })
                .catch((err) => {
                reject(false);
                console.log("Error al validar");
            });
        });
        return promise;
    }
    // Products
    get_product_list(offset = 0, limit = 0, search) {
        let self = this;
        let domain = [];
        if (search) {
            domain.push('|', ['name', 'ilike', search], ['default_code', 'ilike', search]);
        }
        let model = 'product.product';
        let fields = this.STOCK_FIELDS[model]['tree'];
        let promise = new Promise((resolve, reject) => {
            self.odooCon.search_read(model, domain, fields, offset, limit).then((data) => {
                for (let sm_id in data) {
                    data[sm_id]['model'] = model;
                }
                resolve(data);
            })
                .catch((err) => {
                reject(err);
            });
        });
        return promise;
    }
    get_product_info(product_id) {
        let self = this;
        let domain = [['id', '=', product_id]];
        let model = 'product.product';
        let fields = this.STOCK_FIELDS[model]['form'];
        let promise = new Promise((resolve, reject) => {
            self.odooCon.search_read(model, domain, fields, 0, 0).then((data) => {
                for (let sm_id in data) {
                    data[sm_id]['model'] = model;
                }
                resolve(data);
            })
                .catch((err) => {
                reject(err);
            });
        });
        return promise;
    }
    get_location_products(location, offset = 0, limit = 0, search) {
        let self = this;
        let domain = [];
        if (location) {
            domain.push(['product_tmpl_id.location_id', 'child_of', Number(location)]);
        }
        if (search) {
            domain.push(['default_code', 'ilike', search]);
        }
        let model = 'product.product';
        let fields = this.STOCK_FIELDS[model]['location-tree'];
        let promise = new Promise((resolve, reject) => {
            self.odooCon.search_read(model, domain, fields, offset, limit).then((data) => {
                for (let sm_id in data) {
                    data[sm_id]['model'] = model;
                }
                resolve(data);
            })
                .catch((err) => {
                reject(err);
            });
        });
        return promise;
    }
    // Location
    get_location_list(location_state, offset = 0, limit = 0, search) {
        let self = this;
        let domain = [];
        if (location_state != 'all') {
            domain = [['usage', '=', location_state]];
        }
        if (search) {
            domain.push(['name', 'ilike', search]);
        }
        let model = 'stock.location';
        let fields = this.STOCK_FIELDS[model]['tree'];
        let promise = new Promise((resolve, reject) => {
            self.odooCon.search_read(model, domain, fields, offset, limit).then((data) => {
                for (let sm_id in data) {
                    data[sm_id]['model'] = model;
                }
                resolve(data);
            })
                .catch((err) => {
                reject(err);
            });
        });
        return promise;
    }
    get_location_info(location_id) {
        let self = this;
        let domain = [['id', '=', location_id]];
        let model = 'stock.location';
        let fields = this.STOCK_FIELDS[model]['form'];
        let promise = new Promise((resolve, reject) => {
            self.odooCon.search_read(model, domain, fields, 0, 0).then((data) => {
                for (let sm_id in data) {
                    data[sm_id]['model'] = model;
                }
                resolve(data);
            })
                .catch((err) => {
                reject(err);
            });
        });
        return promise;
    }
    // Quants
    get_location_quants(location, offset = 0, limit = 0, search) {
        let self = this;
        let domain = [];
        if (location) {
            domain.push(['location_id', 'child_of', Number(location)]);
        }
        if (search) {
            domain.push(['product_id.default_code', 'ilike', search]);
        }
        let model = 'stock.quant';
        let fields = this.STOCK_FIELDS[model]['tree'];
        let promise = new Promise((resolve, reject) => {
            self.odooCon.search_read(model, domain, fields, offset, limit).then((data) => {
                for (let sm_id in data) {
                    data[sm_id]['model'] = model;
                }
                resolve(data);
            })
                .catch((err) => {
                reject(err);
            });
        });
        return promise;
    }
    // Move location
    create_new_move_location(location_barcode) {
        let self = this;
        let model;
        let values = {
            'location_barcode': location_barcode
        };
        model = 'wiz.stock.move.location';
        let promise = new Promise((resolve, reject) => {
            self.odooCon.execute(model, 'create_wiz_from_apk', values).then((done) => {
                if (done['err'] == true) {
                    reject(done['error']);
                }
                resolve(done);
            })
                .catch((err) => {
                reject(false);
                console.log("Error al validar:" + err);
            });
        });
        return promise;
    }
    create_new_move_location_line(location_move_id, location_id, location_dest_id, product_barcode) {
        let self = this;
        let model;
        let values = {
            'origin_location_id': location_id,
            'product_barcode': product_barcode,
            'move_location_wizard_id': location_move_id,
            'destination_location_id': location_dest_id
        };
        model = 'wiz.stock.move.location.line';
        let promise = new Promise((resolve, reject) => {
            self.odooCon.execute(model, 'create_wiz_line_from_apk', values).then((done) => {
                if (done['err'] == true) {
                    reject(done['error']);
                }
                resolve(done);
            })
                .catch((err) => {
                reject(false);
                console.log("Error al validar:" + err);
            });
        });
        return promise;
    }
    change_qty(line_id, qty) {
        let self = this;
        let model;
        let values = {
            'id': line_id,
            'move_quantity': qty
        };
        model = 'wiz.stock.move.location.line';
        let promise = new Promise((resolve, reject) => {
            self.odooCon.execute(model, 'edit_wiz_line_qty_from_apk', values).then((done) => {
                if (done['err'] == true) {
                    reject(done['error']);
                }
                resolve(done);
            })
                .catch((err) => {
                reject(false);
                console.log("Error al validar:" + err);
            });
        });
        return promise;
    }
    change_move_location(location_move_id, type, location_id) {
        let self = this;
        let model;
        let values;
        if (type == "origin") {
            values = {
                'id': location_move_id,
                'origin_location_id': location_id
            };
        }
        else if (type == "destination") {
            values = {
                'id': location_move_id,
                'destination_location_id': location_id
            };
        }
        model = 'wiz.stock.move.location';
        let promise = new Promise((resolve, reject) => {
            self.odooCon.execute(model, 'edit_wiz_location_from_apk', values).then((done) => {
                if (done['err'] == true) {
                    reject(done['error']);
                }
                resolve(done);
            })
                .catch((err) => {
                reject(false);
                console.log("Error al validar:" + err);
            });
        });
        return promise;
    }
    set_multiple_move_location(location_move_id, type) {
        let self = this;
        let model;
        let values;
        values = {
            'id': location_move_id,
            'action': type
        };
        model = 'wiz.stock.move.location';
        let promise = new Promise((resolve, reject) => {
            self.odooCon.execute(model, 'set_multiple_move_location', values).then((done) => {
                if (done['err'] == true) {
                    reject(done['error']);
                }
                resolve(done);
            })
                .catch((err) => {
                reject(false);
                console.log("Error al validar:" + err);
            });
        });
        return promise;
    }
    action_move_location(location_move_id) {
        let self = this;
        let model;
        let values;
        values = {
            'id': location_move_id
        };
        model = 'wiz.stock.move.location';
        let promise = new Promise((resolve, reject) => {
            self.odooCon.execute(model, 'action_move_location_apk', values).then((done) => {
                if (done['err'] == true) {
                    reject(done['error']);
                }
                resolve(done);
            })
                .catch((err) => {
                reject(false);
                console.log("Error al validar:" + err);
            });
        });
        return promise;
    }
};
StockService.ctorParameters = () => [
    { type: _odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"] },
    { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_2__["AlertController"] },
    { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_3__["Storage"] }
];
StockService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
        _ionic_angular__WEBPACK_IMPORTED_MODULE_2__["AlertController"],
        _ionic_storage__WEBPACK_IMPORTED_MODULE_3__["Storage"]])
], StockService);



/***/ })

}]);
//# sourceMappingURL=default~pages-product-list-product-list-module~pages-product-product-module~pages-stock-location-lis~cc565fe3-es2015.js.map
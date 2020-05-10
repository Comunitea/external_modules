(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~pages-move-form-move-form-module~pages-move-line-form-move-line-form-module~pages-product-li~23c37453"],{

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/__ivy_ngcc__/fesm5/ionic-storage.js");
/* harmony import */ var _odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./odoo.service */ "./src/app/services/odoo.service.ts");





var StockService = /** @class */ (function () {
    function StockService(odooCon, alertCtrl, storage) {
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
                'form': ['id', 'product_id', 'reserved_quantity', 'quantity', 'location_id']
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
    StockService.prototype.get_picking_list = function (view_domain, type_id, offset, limit, search) {
        if (view_domain === void 0) { view_domain = null; }
        if (type_id === void 0) { type_id = null; }
        if (offset === void 0) { offset = 0; }
        if (limit === void 0) { limit = 0; }
        if (search === void 0) { search = null; }
        var self = this;
        var domain = [];
        if (view_domain) {
            view_domain.forEach(function (lit_domain) {
                domain.push(lit_domain);
            });
        }
        if (type_id) {
            domain.push(['picking_type_id', '=', Number(type_id)]);
        }
        if (search) {
            domain.push(['name', 'ilike', '%' + search + '%']);
        }
        var values = {
            'domain': domain,
            'model': 'stock.picking',
            'offset': offset,
            'limit': limit
        };
        console.log(values);
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute('info.apk', 'get_apk_object', values).then(function (done) {
                console.log(done);
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al realizar la consulta:" + err['msg']['error_msg']);
            });
        });
        return promise;
    };
    StockService.prototype.get_picking_info = function (picking_id) {
        var self = this;
        var domain = [['id', '=', picking_id]];
        var values = {
            'domain': domain,
            'model': 'stock.picking',
            'offset': 0,
            'limit': 0,
            'fields': ['id', 'display_name', 'location_id', 'location_dest_id', 'scheduled_date', 'state', 'group_code',
                'picking_type_id', 'priority', 'note', 'move_lines', 'move_line_ids', 'quantity_done', 'picking_fields',
                'reserved_availability', 'product_uom_qty', 'show_check_availability', 'move_fields', 'move_line_fields',
                'show_validate']
        };
        console.log(values);
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute('info.apk', 'get_apk_object', values).then(function (done) {
                console.log(done);
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al realizar la consulta:" + err['msg']['error_msg']);
            });
        });
        return promise;
    };
    StockService.prototype.get_picking_types = function (picking_codes, offset, limit, search) {
        if (offset === void 0) { offset = 0; }
        if (limit === void 0) { limit = 0; }
        if (search === void 0) { search = null; }
        var self = this;
        var domain = [];
        domain = [['code', 'in', picking_codes], ['active', '=', true], ['app_integrated', '=', true]];
        if (search) {
            domain.push(['name', 'ilike', '%' + search + '%']);
        }
        var values = {
            'domain': domain,
            'model': 'stock.picking.type',
            'offset': offset,
            'limit': limit,
            'fields': ['id', 'name', 'color', 'warehouse_id', 'code', 'count_picking_ready', 'count_picking_waiting', 'count_picking_late', 'group_code',
                'count_picking_backorders', 'rate_picking_late', 'rate_picking_backorders']
        };
        console.log(values);
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute('info.apk', 'get_apk_object', values).then(function (done) {
                console.log(done);
                resolve(done);
            })
                .catch(function (err) {
                console.log(err);
                reject(false);
                console.log("Error al realizar la consulta:" + err['msg']['error_msg']);
            });
        });
        return promise;
    };
    StockService.prototype.action_assign = function (pick_id) {
        var self = this;
        var model;
        var values = {
            'id': pick_id
        };
        model = 'stock.picking';
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'action_assign_pick', values).then(function (done) {
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar");
            });
        });
        return promise;
    };
    StockService.prototype.button_validate = function (pick_id) {
        var self = this;
        var model;
        var values = {
            'id': pick_id
        };
        model = 'stock.picking';
        var promise = new Promise(function (resolve, reject) {
            console.log("button validate pick");
            console.log(pick_id);
            self.odooCon.execute(model, 'button_validate_pick', values).then(function (done) {
                resolve(done);
            })
                .catch(function (err) {
                reject(err['msg']['error_msg']);
                console.log("Error al validar");
            });
        });
        return promise;
    };
    // Move
    StockService.prototype.get_move_info = function (move_id, index) {
        if (index === void 0) { index = 0; }
        var self = this;
        var values = { 'id': move_id, 'index': index };
        var model = 'stock.move';
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'get_move_info_apk', values).then(function (data) {
                resolve(data);
            })
                .catch(function (err) {
                reject(err);
            });
        });
        return promise;
    };
    StockService.prototype.set_lot_ids_apk = function (move_id, reading) {
        var self = this;
        var values = { 'id': move_id, 'reading': reading };
        var model = 'stock.move';
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'set_lot_ids_apk', values).then(function (data) {
                resolve(data);
            })
                .catch(function (err) {
                reject(err);
            });
        });
        return promise;
    };
    StockService.prototype.set_move_qty_done_from_apk = function (move_id, qty_done) {
        var self = this;
        var values = {
            'id': move_id,
            'quantity_done': qty_done
        };
        var model = 'stock.move';
        console.log(values);
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'set_qty_done_from_apk', values).then(function (done) {
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar");
            });
        });
        return promise;
    };
    // Move_lines
    StockService.prototype.find_move_line_id = function (code, picking_id) {
        var self = this;
        var values = { 'code': code, 'picking_id': picking_id };
        var model = 'stock.move.line';
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'find_move_line_id', values).then(function (data) {
                resolve(data);
            })
                .catch(function (err) {
                reject(err);
            });
        });
        return promise;
    };
    StockService.prototype.get_move_line_info = function (move_id, index) {
        if (index === void 0) { index = 0; }
        var self = this;
        var values = { 'id': move_id, 'index': index };
        var model = 'stock.move.line';
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'get_move_line_info_apk', values).then(function (data) {
                resolve(data);
            })
                .catch(function (err) {
                reject(err);
            });
        });
        return promise;
    };
    StockService.prototype.get_move_lines_list_search = function (line_ids) {
        var self = this;
        var domain = [['id', 'in', line_ids]];
        var model = 'stock.move';
        var fields = this.STOCK_FIELDS[model]['tree'];
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.search_read(model, domain, fields, 0, 0).then(function (data) {
                for (var sm_id in data) {
                    data[sm_id]['model'] = model;
                }
                resolve(data);
            })
                .catch(function (err) {
                reject(err);
            });
        });
        return promise;
    };
    StockService.prototype.get_move_lines_list = function (picking_id) {
        var self = this;
        var domain = [['picking_id', '=', parseInt(picking_id)]];
        var values = {
            'domain': domain,
            'model': 'stock.move',
            'offset': 0,
            'limit': 0
        };
        console.log(values);
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute('info.apk', 'get_apk_object', values).then(function (done) {
                console.log(done);
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al realizar la consulta:" + err['msg']['error_msg']);
            });
        });
        return promise;
    };
    StockService.prototype.get_move_lines_details_list = function (picking_id) {
        var self = this;
        var domain = [['picking_id', '=', parseInt(picking_id)]];
        var values = {
            'domain': domain,
            'model': 'stock.move.line',
            'offset': 0,
            'limit': 0
        };
        console.log(values);
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute('info.apk', 'get_apk_object', values).then(function (done) {
                console.log(done);
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al realizar la consulta:" + err['msg']['error_msg']);
            });
        });
        return promise;
    };
    StockService.prototype.force_set_assigned_qty_done = function (move_id, model) {
        if (model === void 0) { model = 'stock.move'; }
        var self = this;
        var values = {
            'id': move_id
        };
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'force_set_qty_done_apk', values).then(function (done) {
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar");
            });
        });
        return promise;
    };
    StockService.prototype.set_qty_done_from_apk = function (move_id, qty_done) {
        var self = this;
        var values = {
            'id': move_id,
            'qty_done': qty_done
        };
        var model = 'stock.move.line';
        console.log(values);
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'set_qty_done_from_apk', values).then(function (done) {
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar");
            });
        });
        return promise;
    };
    StockService.prototype.force_set_reserved_qty_done = function (move_id, model) {
        if (model === void 0) { model = 'stock.move'; }
        var self = this;
        var values = {
            'id': move_id
        };
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'force_set_reserved_qty_done_apk', values).then(function (done) {
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar");
            });
        });
        return promise;
    };
    StockService.prototype.force_set_qty_done = function (move_id, field, model) {
        if (model === void 0) { model = 'stock.move.line'; }
        var self = this;
        var values = {
            'id': move_id,
            'field': field
        };
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'force_set_qty_done_apk', values).then(function (done) {
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar");
            });
        });
        return promise;
    };
    StockService.prototype.force_set_qty_done_by_product_code_apk = function (product_code, field, model, picking) {
        if (model === void 0) { model = 'stock.move.line'; }
        var self = this;
        var values = {
            'default_code': product_code,
            'field': field,
            'picking': picking
        };
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'force_set_qty_done_by_product_code_apk', values).then(function (done) {
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar");
            });
        });
        return promise;
    };
    StockService.prototype.force_reset_qties = function (pick_id, model) {
        if (model === void 0) { model = 'stock.picking'; }
        var self = this;
        var values = {
            'id': pick_id
        };
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'force_reset_qties_apk', values).then(function (done) {
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar");
            });
        });
        return promise;
    };
    // Products
    StockService.prototype.get_product_list = function (offset, limit, search) {
        if (offset === void 0) { offset = 0; }
        if (limit === void 0) { limit = 0; }
        if (search === void 0) { search = null; }
        var self = this;
        var domain = [];
        if (search) {
            domain.push('|', ['name', 'ilike', '%' + search + '%'], ['default_code', 'ilike', '%' + search + '%']);
        }
        var values = {
            'domain': domain,
            'model': 'product.product',
            'offset': offset,
            'limit': limit
        };
        console.log(values);
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute('info.apk', 'get_apk_object', values).then(function (done) {
                console.log(done);
                resolve(done);
            })
                .catch(function (err) {
                console.log(err);
                reject(false);
                console.log("Error al realizar la consulta:" + err['msg']['error_msg']);
            });
        });
        return promise;
    };
    StockService.prototype.get_product_info = function (product_id) {
        var self = this;
        var domain = [['id', '=', product_id]];
        var values = {
            'domain': domain,
            'model': 'product.product',
            'offset': 0,
            'limit': 0,
            'fields': ['id', 'name', 'default_code', 'list_price', 'standard_price', 'qty_available', 'virtual_available', 'categ_id', 'tracking',
                'barcode', 'description_short', 'image_medium', 'stock_quant_ids']
        };
        console.log(values);
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute('info.apk', 'get_apk_object', values).then(function (done) {
                console.log(done);
                resolve(done);
            })
                .catch(function (err) {
                console.log(err);
                reject(false);
                console.log("Error al realizar la consulta:" + err['msg']['error_msg']);
            });
        });
        return promise;
    };
    StockService.prototype.get_location_products = function (location, offset, limit, search) {
        if (offset === void 0) { offset = 0; }
        if (limit === void 0) { limit = 0; }
        var self = this;
        var domain = [];
        if (location) {
            domain.push(['product_tmpl_id.location_id', 'child_of', Number(location)]);
        }
        if (search) {
            domain.push(['default_code', 'ilike', search]);
        }
        var values = {
            'domain': domain,
            'model': 'product.product',
            'offset': offset,
            'limit': limit,
            'fields': ['id', 'display_name', 'default_code', 'qty_available', 'tracking', 'barcode', 'uom_id']
        };
        console.log(values);
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute('info.apk', 'get_apk_object', values).then(function (done) {
                console.log(done);
                resolve(done);
            })
                .catch(function (err) {
                console.log(err);
                reject(false);
                console.log("Error al realizar la consulta:" + err['msg']['error_msg']);
            });
        });
        return promise;
    };
    // Location
    StockService.prototype.get_location_list = function (location_state, offset, limit, search) {
        if (offset === void 0) { offset = 0; }
        if (limit === void 0) { limit = 0; }
        if (search === void 0) { search = null; }
        var self = this;
        var domain = [];
        if (location_state != 'all') {
            domain = [['usage', '=', location_state]];
        }
        if (search) {
            domain.push(['name', 'ilike', search]);
        }
        var values = {
            'domain': domain,
            'model': 'stock.location',
            'offset': offset,
            'limit': limit
        };
        console.log(values);
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute('info.apk', 'get_apk_object', values).then(function (done) {
                console.log(done);
                resolve(done);
            })
                .catch(function (err) {
                console.log(err);
                reject(false);
                console.log("Error al realizar la consulta:" + err['msg']['error_msg']);
            });
        });
        return promise;
    };
    StockService.prototype.get_location_info = function (location_id) {
        var self = this;
        var domain = [['id', '=', location_id]];
        var values = {
            'domain': domain,
            'model': 'stock.location',
            'offset': 0,
            'limit': 0,
            'fields': ['id', 'display_name', 'usage', 'company_id']
        };
        console.log(values);
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute('info.apk', 'get_apk_object', values).then(function (done) {
                console.log(done);
                resolve(done);
            })
                .catch(function (err) {
                console.log(err);
                reject(false);
                console.log("Error al realizar la consulta:" + err['msg']['error_msg']);
            });
        });
        return promise;
    };
    // Quants
    StockService.prototype.get_location_quants = function (location, offset, limit, search, ftype) {
        if (offset === void 0) { offset = 0; }
        if (limit === void 0) { limit = 0; }
        if (ftype === void 0) { ftype = null; }
        var self = this;
        var domain = [];
        if (location) {
            domain.push(['location_id', 'child_of', Number(location)]);
        }
        if (search) {
            domain.push(['product_id.default_code', 'ilike', search]);
        }
        var values = {
            'domain': domain,
            'model': 'stock.quant',
            'offset': offset,
            'limit': limit
        };
        if (ftype != null) {
            values['fields'] = ['id', 'product_id', 'reserved_quantity', 'quantity', 'location_id'];
        }
        console.log(values);
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute('info.apk', 'get_apk_object', values).then(function (done) {
                console.log(done);
                resolve(done);
            })
                .catch(function (err) {
                console.log(err);
                reject(false);
                console.log("Error al realizar la consulta:" + err['msg']['error_msg']);
            });
        });
        return promise;
    };
    // Move location
    StockService.prototype.create_new_move_location = function (location_barcode) {
        var self = this;
        var model;
        var values = {
            'location_barcode': location_barcode
        };
        model = 'wiz.stock.move.location';
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'create_wiz_from_apk', values).then(function (done) {
                if (done['err'] == true) {
                    reject(done['error']);
                }
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar:" + err);
            });
        });
        return promise;
    };
    StockService.prototype.create_new_move_location_line = function (location_move_id, location_id, location_dest_id, product_barcode) {
        var self = this;
        var model;
        var values = {
            'origin_location_id': location_id,
            'product_barcode': product_barcode,
            'move_location_wizard_id': location_move_id,
            'destination_location_id': location_dest_id
        };
        model = 'wiz.stock.move.location.line';
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'create_wiz_line_from_apk', values).then(function (done) {
                if (done['err'] == true) {
                    reject(done['error']);
                }
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar:" + err);
            });
        });
        return promise;
    };
    StockService.prototype.change_qty = function (line_id, qty) {
        var self = this;
        var model;
        var values = {
            'id': line_id,
            'move_quantity': qty
        };
        model = 'wiz.stock.move.location.line';
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'edit_wiz_line_qty_from_apk', values).then(function (done) {
                if (done['err'] == true) {
                    reject(done['error']);
                }
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar:" + err);
            });
        });
        return promise;
    };
    StockService.prototype.change_move_location = function (location_move_id, type, location_id) {
        var self = this;
        var model;
        var values;
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
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'edit_wiz_location_from_apk', values).then(function (done) {
                if (done['err'] == true) {
                    reject(done['error']);
                }
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar:" + err);
            });
        });
        return promise;
    };
    StockService.prototype.set_multiple_move_location = function (location_move_id, type) {
        var self = this;
        var model;
        var values;
        values = {
            'id': location_move_id,
            'action': type
        };
        model = 'wiz.stock.move.location';
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'set_multiple_move_location', values).then(function (done) {
                if (done['err'] == true) {
                    reject(done['error']);
                }
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar:" + err);
            });
        });
        return promise;
    };
    StockService.prototype.action_move_location = function (location_move_id) {
        var self = this;
        var model;
        var values;
        values = {
            'id': location_move_id
        };
        model = 'wiz.stock.move.location';
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'action_move_location_apk', values).then(function (done) {
                if (done['err'] == true) {
                    reject(done['error']);
                }
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar:" + err);
            });
        });
        return promise;
    };
    // QR 
    StockService.prototype.process_qr_lines = function (qr_codes) {
        var self = this;
        var model;
        var values;
        values = {
            'qr_codes': qr_codes
        };
        model = 'stock.picking';
        var promise = new Promise(function (resolve, reject) {
            self.odooCon.execute(model, 'process_qr_lines', values).then(function (done) {
                if (done['err'] == true) {
                    reject(done['error']);
                }
                resolve(done);
            })
                .catch(function (err) {
                reject(false);
                console.log("Error al validar:" + err);
            });
        });
        return promise;
    };
    StockService.ctorParameters = function () { return [
        { type: _odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_2__["AlertController"] },
        { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_3__["Storage"] }
    ]; };
    StockService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_2__["AlertController"],
            _ionic_storage__WEBPACK_IMPORTED_MODULE_3__["Storage"]])
    ], StockService);
    return StockService;
}());



/***/ })

}]);
//# sourceMappingURL=default~pages-move-form-move-form-module~pages-move-line-form-move-line-form-module~pages-product-li~23c37453.js.map
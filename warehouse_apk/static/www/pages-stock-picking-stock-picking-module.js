(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-stock-picking-stock-picking-module"],{

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/move-line-details-list/move-line-details-list.component.html":
/*!*******************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/components/move-line-details-list/move-line-details-list.component.html ***!
  \*******************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-grid *ngIf=\"not_allowed_fields && move_line_ids\">\n  <ion-row class=\"ion-align-items-center\">  \n\n    <ion-col size=\"3\" *ngIf=\"not_allowed_fields.indexOf('product_id') == -1\">\n      <div><strong>Pro.</strong></div>\n    </ion-col>\n\n    <ion-col size=\"2\" *ngIf=\"not_allowed_fields.indexOf('location_id') == -1\">\n      <div><strong>De</strong></div>\n    </ion-col>\n  \n    <ion-col size=\"2\" *ngIf=\"not_allowed_fields.indexOf('location_dest_id') == -1\">\n      <div><strong>A</strong></div>\n    </ion-col>\n  \n    <ion-col size=\"1\" *ngIf=\"not_allowed_fields.indexOf('package_id') == -1\">\n      <div><strong>Pqt. O.</strong></div>\n    </ion-col>\n  \n    <ion-col size=\"1\" *ngIf=\"not_allowed_fields.indexOf('result_package_id') == -1\">\n      <div><strong>Pqt. D.</strong></div>\n    </ion-col>\n    \n    <ion-col size=\"1\" *ngIf=\"not_allowed_fields.indexOf('qty_available') == -1\">\n      <div><strong>Dis.</strong></div>\n    </ion-col>\n  \n    <ion-col size=\"1\" *ngIf=\"not_allowed_fields.indexOf('product_uom_qty') == -1\">\n      <div><strong>Res.</strong></div>\n    </ion-col>\n    \n    <ion-col size=\"1\" *ngIf=\"not_allowed_fields.indexOf('qty_done') == -1\">\n      <div><strong>Hecha</strong></div>\n    </ion-col>\n  </ion-row>\n\n  <ion-row *ngFor=\"let line of move_line_ids_info\" [ngClass]=\"{'success': line.qty_done == line.product_uom_qty}\">\n    <ion-col size-xs=\"12\" size-sm=\"3\" size-md=\"3\" *ngIf=\"not_allowed_fields.indexOf('product_id') == -1\">\n      <div class=\"link\" (click)=\"open_link(line.id)\">{{line.product_id[1]}}</div>\n    </ion-col>\n  \n    <ion-col size-xs=\"6\" size-sm=\"2\" size-md=\"2\" *ngIf=\"not_allowed_fields.indexOf('location_id') == -1\">\n      <div>\n        <strong class=\"ion-hide-sm-up\">De: </strong>{{line.location_id[1]}}\n      </div>\n    </ion-col>\n  \n    <ion-col size-xs=\"6\" size-sm=\"2\" size-md=\"2\" *ngIf=\"not_allowed_fields.indexOf('location_dest_id') == -1\">\n      <div>\n        <strong class=\"ion-hide-sm-up\">A: </strong>{{line.location_dest_id[1]}}\n      </div>\n    </ion-col>\n  \n    <ion-col size-xs=\"6\" size-sm=\"1\" size-md=\"1\" *ngIf=\"not_allowed_fields.indexOf('package_id') == -1\">\n      <div>\n        <strong class=\"ion-hide-sm-up\">Pqt. O: </strong>{{line.package_id[1]}}\n      </div>\n    </ion-col>\n  \n    <ion-col size-xs=\"6\" size-sm=\"1\"size-md=\"1\" *ngIf=\"not_allowed_fields.indexOf('result_package_id') == -1\">\n      <div><strong class=\"ion-hide-sm-up\">Pqt D: </strong>{{line.result_package_id[1]}}</div>\n    </ion-col>\n    \n    <ion-col size-xs=\"6\" size-sm=\"1\"size-md=\"1\" *ngIf=\"not_allowed_fields.indexOf('qty_available') == -1\">\n      <div class=\"link\" *ngIf=\"(line.state == 'confirmed' || line.state == 'assigned') && line.qty_done == 0; else noLinkAvailable\" (click)=\"force_set_qty_done(line.id, 'qty_available')\">\n        <strong class=\"ion-hide-sm-up\">Dis: </strong>{{line.qty_available}}\n      </div>\n    </ion-col>\n\n    <ng-template #noLinkAvailable>\n        <div><strong class=\"ion-hide-sm-up\">Dis: </strong>{{line.qty_available}}</div>\n    </ng-template>\n  \n    <ion-col size-xs=\"6\" size-sm=\"1\"size-md=\"1\" *ngIf=\"not_allowed_fields.indexOf('product_uom_qty') == -1\">\n      <div class=\"link\" *ngIf=\"(line.state != 'done' || line.state == 'cancel') && line.qty_done == 0; else noLinkUom\" (click)=\"force_set_qty_done(line.id, 'product_uom_qty')\">\n        <strong class=\"ion-hide-sm-up\">Res: </strong>{{line.product_uom_qty}}\n      </div>\n    </ion-col>\n    \n    <ng-template #noLinkUom>\n        <div><strong class=\"ion-hide-sm-up\">Res: </strong>{{line.product_uom_qty}}</div>\n    </ng-template>\n\n    <ion-col size-xs=\"6\" size-sm=\"1\"size-md=\"1\" *ngIf=\"not_allowed_fields.indexOf('qty_done') == -1\">\n\n      <div><strong class=\"ion-hide-sm-up\">Hecha: </strong>{{line.qty_done}}</div>\n    </ion-col>\n  </ion-row>\n\n</ion-grid>");

/***/ }),

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/move-line-list/move-line-list.component.html":
/*!***************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/components/move-line-list/move-line-list.component.html ***!
  \***************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-grid *ngIf=\"not_allowed_fields && move_lines\">\n  <ion-row>\n    <ion-col size=\"10\" *ngIf=\"not_allowed_fields.indexOf('product_id') == -1\">\n      <div style=\"font-size: small\"><strong>Producto</strong></div>\n    </ion-col>  \n\n    <ion-col size=\"2\" *ngIf=\"not_allowed_fields.indexOf('reserved_availability') == -1\">\n      <div style=\"font-size: small\"><strong>Qty</strong></div>\n    </ion-col>\n\n    <!--ion-col size=\"2\">\n      <div><strong>Reservada</strong></div>\n    </ion-col>\n    \n    <ion-col size=\"2\">\n      <div><strong>Hecha</strong></div>\n    </ion-col-->\n  </ion-row>\n\n  <ion-row class=\"product_link\" *ngFor=\"let line of move_lines_info\" [ngClass]=\"{'success': line.quantity_done == line.product_uom_qty}\">\n    <ion-col size=\"10\" *ngIf=\"not_allowed_fields.indexOf('product_id') == -1\">\n      <div (click)=\"open_link(line.id)\" style=\"font-size: small\">{{line.product_id[1]}}</div>\n    </ion-col>\n    \n    <!--ion-col size=\"2\">\n      <div *ngIf=\"(line.quantity_done != 0 || (line.state != 'confirmed' && line.state != 'partially_available' && line.state != 'assigned')); else link_product_uom_qty\">\n        <strong class=\"ion-hide-sm-up\">Pedida: </strong>{{line.product_uom_qty}}\n      </div>\n    </ion-col>\n\n    <ng-template #link_product_uom_qty>\n      <div (click)=\"force_set_qty_done(line.id, 'product_uom_qty', 'stock.move')\" >{{line.product_uom_qty}}</div>\n    </ng-template-->\n    \n    <ion-col size=\"2\" *ngIf=\"not_allowed_fields.indexOf('product_uom_qty') == -1 && not_allowed_fields.indexOf('quantity_done') == -1\">\n      <div *ngIf=\"(line.quantity_done != 0 || line.reserved_availability == 0 || code == 'incoming' || (line.state == 'done' || line.state == 'assigned')); else link_qty_done\" \n        style=\"font-size: small\">\n        {{line.quantity_done}} // {{line.product_uom_qty}}\n      </div>\n    </ion-col>\n\n    <ng-template #link_qty_done>\n      <div (click)=\"force_set_assigned_qty_done(line.id)\" \n        style=\"font-size: small\">\n        {{line.quantity_done}} // {{line.product_uom_qty}}\n      </div>\n    </ng-template>\n    \n    <!--ion-col size=\"2\">\n      <div>{{line.quantity_done}}</div>\n    </ion-col-->\n     \n  </ion-row>\n</ion-grid>");

/***/ }),

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-picking/stock-picking.page.html":
/*!***************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-picking/stock-picking.page.html ***!
  \***************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"start\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n    <app-scanner-header slot=\"end\"></app-scanner-header>\n    <ion-title>Detalles de la operación</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <ion-card *ngIf=\"picking_data && not_allowed_fields\">\n\n    <ion-card-header>\n      <ion-row>\n        <ion-col>\n          <ion-card-title *ngIf=\"not_allowed_fields.indexOf('display_name') == -1\">{{picking_data.display_name}}</ion-card-title>\n          <ion-card-subtitle *ngIf=\"not_allowed_fields.indexOf('picking_type_id') == -1\">{{picking_data.picking_type_id[1]}}</ion-card-subtitle>\n        </ion-col>\n        <ion-col>\n          <ion-button size=\"small\" class=\"button-text\" (click)=\"presentActionSheet()\">Opciones</ion-button>\n        </ion-col>\n      </ion-row>\n    </ion-card-header>\n\n    <ion-card-content>\n      <div *ngIf=\"not_allowed_fields.indexOf('scheduled_date') == -1\">{{picking_data.scheduled_date}}</div>\n      <div *ngIf=\"not_allowed_fields.indexOf('location_id') == -1\"><span class=\"location\" (click)=\"open_link(picking_data.location_id[0])\">{{picking_data.location_id[1]}}</span></div>\n      <div *ngIf=\"not_allowed_fields.indexOf('location_dest_id') == -1\"><span class=\"location\" (click)=\"open_link(picking_data.location_dest_id[0])\">{{picking_data.location_dest_id[1]}}</span></div>\n      <div *ngIf=\"not_allowed_fields.indexOf('priority') == -1\" [ngSwitch]=\"picking_data.priority\">\n        <ion-text *ngSwitchCase=\"0\">No Urgente</ion-text>\n        <ion-text *ngSwitchCase=\"1\">Normal</ion-text>\n        <ion-text *ngSwitchCase=\"2\">Urgente</ion-text>\n        <ion-text *ngSwitchCase=\"3\">Muy Urgente</ion-text>\n      </div>\n      <div *ngIf=\"picking_data.note && not_allowed_fields.indexOf('scheduled_date') == -1\">{{picking_data.note}}</div>\n    </ion-card-content>\n\n  </ion-card>\n\n  <div>\n\n    <ion-card *ngIf=\"move_lines && move_line_ids\">\n      <ion-card-header>\n        <ion-row>\n          <ion-col>\n            <ion-card-title *ngIf=\"!active_operation; else detailed_title\">Operaciones</ion-card-title>\n          </ion-col>\n          <!-- <ion-col class=\"ion-text-right\">\n            <ion-item>\n              <ion-label>Detalles:</ion-label>\n              <ion-toggle [(ngModel)]=\"active_operation\" color=\"primary\"></ion-toggle>\n            </ion-item>\n          </ion-col> -->\n        </ion-row>\n      </ion-card-header>\n\n      <ng-template #detailed_title>\n        <ion-card-title>Operaciones detalladas</ion-card-title>\n      </ng-template>\n\n      <ion-card-content *ngIf=\"move_lines || move_line_ids\">\n        <app-move-line-list *ngIf=\"!active_operation && move_lines; else detailed_grid\" [not_allowed_fields]=\"not_allowed_ml_fields\" [scanner_reading]=\"scanner_reading\" [code]=\"picking_code\" [move_lines]=\"move_lines\"></app-move-line-list>\n\n        <ion-grid *ngIf=\"!active_operation\">          \n          <ion-row>\n            <ion-col>\n              \n            </ion-col>\n            \n            <ion-col size=\"2\">\n                <strong>Total:</strong>\n            </ion-col>\n          \n            <ion-col size=\"4\">\n              <div>{{picking_data.quantity_done}} // {{picking_data.product_uom_qty}}</div>\n            </ion-col>\n          </ion-row>\n        </ion-grid>\n\n        <ng-template #detailed_grid>\n          <app-move-line-details-list *ngIf=\"move_line_ids\" [not_allowed_fields]=\"not_allowed_m_fields\" [code]=\"picking_code\" [scanner_reading]=\"scanner_reading\"  [move_line_ids]=\"move_line_ids\"></app-move-line-details-list>\n        </ng-template>\n\n      </ion-card-content>\n    </ion-card>\n\n  </div>\n</ion-content>\n\n<app-scanner-footer (scanner_reading_changed)=\"onReadingEmitted($event)\" [scanner_reading]=\"scanner_reading\"></app-scanner-footer>");

/***/ }),

/***/ "./src/app/components/move-line-details-list/move-line-details-list.component.scss":
/*!*****************************************************************************************!*\
  !*** ./src/app/components/move-line-details-list/move-line-details-list.component.scss ***!
  \*****************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("ion-row.success {\n  color: var(--ion-color-success);\n}\n\ndiv.link {\n  color: blue;\n  text-decoration: underline;\n  -webkit-text-decoration-color: blue;\n          text-decoration-color: blue;\n  cursor: pointer;\n}\n\n/* Medias */\n\n@media screen and (max-width: 576px) {\n  ion-grid > ion-row:first-child {\n    display: none;\n  }\n\n  ion-grid > ion-row {\n    border: 1px black solid;\n  }\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL2NvbXBvbmVudHMvbW92ZS1saW5lLWRldGFpbHMtbGlzdC9tb3ZlLWxpbmUtZGV0YWlscy1saXN0LmNvbXBvbmVudC5zY3NzIiwic3JjL2FwcC9jb21wb25lbnRzL21vdmUtbGluZS1kZXRhaWxzLWxpc3QvbW92ZS1saW5lLWRldGFpbHMtbGlzdC5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFDSTtFQUNJLCtCQUFBO0FDQVI7O0FER0E7RUFDSSxXQUFBO0VBQ0EsMEJBQUE7RUFDQSxtQ0FBQTtVQUFBLDJCQUFBO0VBQ0EsZUFBQTtBQ0FKOztBRElBLFdBQUE7O0FBQ0E7RUFDSTtJQUNJLGFBQUE7RUNETjs7RURHRTtJQUNJLHVCQUFBO0VDQU47QUFDRiIsImZpbGUiOiJzcmMvYXBwL2NvbXBvbmVudHMvbW92ZS1saW5lLWRldGFpbHMtbGlzdC9tb3ZlLWxpbmUtZGV0YWlscy1saXN0LmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiaW9uLXJvdyB7XG4gICAgJi5zdWNjZXNzIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zdWNjZXNzKTtcbiAgICB9XG59XG5kaXYubGluayB7XG4gICAgY29sb3I6IGJsdWU7XG4gICAgdGV4dC1kZWNvcmF0aW9uOiB1bmRlcmxpbmU7XG4gICAgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBibHVlO1xuICAgIGN1cnNvcjogcG9pbnRlcjtcbn1cblxuXG4vKiBNZWRpYXMgKi9cbkBtZWRpYSBzY3JlZW4gYW5kIChtYXgtd2lkdGg6IDU3NnB4KSB7XG4gICAgaW9uLWdyaWQgPiBpb24tcm93OmZpcnN0LWNoaWxkIHtcbiAgICAgICAgZGlzcGxheTogbm9uZTtcbiAgICB9XG4gICAgaW9uLWdyaWQgPiBpb24tcm93IHtcbiAgICAgICAgYm9yZGVyOiAxcHggYmxhY2sgc29saWQ7XG4gICAgfVxufSIsImlvbi1yb3cuc3VjY2VzcyB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc3VjY2Vzcyk7XG59XG5cbmRpdi5saW5rIHtcbiAgY29sb3I6IGJsdWU7XG4gIHRleHQtZGVjb3JhdGlvbjogdW5kZXJsaW5lO1xuICB0ZXh0LWRlY29yYXRpb24tY29sb3I6IGJsdWU7XG4gIGN1cnNvcjogcG9pbnRlcjtcbn1cblxuLyogTWVkaWFzICovXG5AbWVkaWEgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiA1NzZweCkge1xuICBpb24tZ3JpZCA+IGlvbi1yb3c6Zmlyc3QtY2hpbGQge1xuICAgIGRpc3BsYXk6IG5vbmU7XG4gIH1cblxuICBpb24tZ3JpZCA+IGlvbi1yb3cge1xuICAgIGJvcmRlcjogMXB4IGJsYWNrIHNvbGlkO1xuICB9XG59Il19 */");

/***/ }),

/***/ "./src/app/components/move-line-details-list/move-line-details-list.component.ts":
/*!***************************************************************************************!*\
  !*** ./src/app/components/move-line-details-list/move-line-details-list.component.ts ***!
  \***************************************************************************************/
/*! exports provided: MoveLineDetailsListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MoveLineDetailsListComponent", function() { return MoveLineDetailsListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");





var MoveLineDetailsListComponent = /** @class */ (function () {
    function MoveLineDetailsListComponent(router, stock, alertCtrl, route) {
        this.router = router;
        this.stock = stock;
        this.alertCtrl = alertCtrl;
        this.route = route;
    }
    MoveLineDetailsListComponent.prototype.ngOnInit = function () {
        if (this.move_line_ids) {
            this.picking = this.route.snapshot.paramMap.get('id');
            console.log(this.move_line_ids);
            this.move_line_ids_info = this.move_line_ids;
        }
        else {
            this.get_move_lines_details_list();
        }
    };
    MoveLineDetailsListComponent.prototype.ngOnChanges = function (changeRecord) {
        var _this = this;
        if (changeRecord['scanner_reading'] && changeRecord['scanner_reading']['currentValue']) {
            var code_1 = changeRecord['scanner_reading']['currentValue'];
            var picking = +this.picking;
            this.stock.find_move_line_id(code_1, picking).then(function (move_id) {
                console.log(move_id);
                _this.router.navigateByUrl('/move-line-form/' + move_id);
            })
                .catch(function (error) {
                _this.presentAlert('Error al recuperar un movieminto para:', code_1);
            });
        }
    };
    MoveLineDetailsListComponent.prototype.get_move_lines_details_list = function () {
        var _this = this;
        this.stock.get_move_lines_details_list(this.picking).then(function (lines_data) {
            _this.move_line_ids_info = lines_data;
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperar los movimientos:', error);
        });
    };
    MoveLineDetailsListComponent.prototype.force_set_qty_done = function (move_id, field) {
        var _this = this;
        console.log(field);
        this.stock.force_set_qty_done(Number(move_id), field, 'stock.move.line').then(function (lines_data) {
            console.log(lines_data == true);
            if (lines_data == true) {
                _this.get_move_lines_details_list();
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al forzar la cantidad:', error);
        });
    };
    MoveLineDetailsListComponent.prototype.force_set_qty_done_by_product_code_apk = function (product_code, field) {
        var _this = this;
        this.stock.force_set_qty_done_by_product_code_apk(product_code, field, 'stock.move.line', this.picking).then(function (lines_data) {
            if (lines_data == true) {
                _this.get_move_lines_details_list();
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al forzar la cantidad:', error);
        });
    };
    MoveLineDetailsListComponent.prototype.open_link_product = function (pick_id) {
        this.router.navigateByUrl('/product/' + pick_id);
    };
    MoveLineDetailsListComponent.prototype.open_link = function (pick_id) {
        this.router.navigateByUrl('/move-line-form/' + pick_id);
    };
    MoveLineDetailsListComponent.prototype.presentAlert = function (titulo, texto) {
        return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"])(this, void 0, void 0, function () {
            var alert;
            return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"])(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.alertCtrl.create({
                            header: titulo,
                            subHeader: texto,
                            buttons: ['Ok']
                        })];
                    case 1:
                        alert = _a.sent();
                        return [4 /*yield*/, alert.present()];
                    case 2:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    MoveLineDetailsListComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_3__["StockService"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", String)
    ], MoveLineDetailsListComponent.prototype, "scanner_reading", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)
    ], MoveLineDetailsListComponent.prototype, "move_line_ids", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", String)
    ], MoveLineDetailsListComponent.prototype, "code", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", String)
    ], MoveLineDetailsListComponent.prototype, "picking_fields", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Boolean)
    ], MoveLineDetailsListComponent.prototype, "hide_product", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)
    ], MoveLineDetailsListComponent.prototype, "not_allowed_fields", void 0);
    MoveLineDetailsListComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-move-line-details-list',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./move-line-details-list.component.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/move-line-details-list/move-line-details-list.component.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./move-line-details-list.component.scss */ "./src/app/components/move-line-details-list/move-line-details-list.component.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_3__["StockService"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"]])
    ], MoveLineDetailsListComponent);
    return MoveLineDetailsListComponent;
}());



/***/ }),

/***/ "./src/app/components/move-line-list/move-line-list.component.scss":
/*!*************************************************************************!*\
  !*** ./src/app/components/move-line-list/move-line-list.component.scss ***!
  \*************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("ion-row.success {\n  color: var(--ion-color-success);\n}\nion-row.product_link {\n  cursor: pointer;\n}\ndiv.product_link {\n  color: blue;\n  text-decoration: underline;\n  -webkit-text-decoration-color: blue;\n          text-decoration-color: blue;\n  cursor: pointer;\n}\n/* Medias */\n@media screen and (max-width: 576px) {\n  ion-grid > ion-row:first-child {\n    display: none;\n  }\n\n  ion-grid > ion-row {\n    border: 1px black solid;\n  }\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL2NvbXBvbmVudHMvbW92ZS1saW5lLWxpc3QvbW92ZS1saW5lLWxpc3QuY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL2NvbXBvbmVudHMvbW92ZS1saW5lLWxpc3QvbW92ZS1saW5lLWxpc3QuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQ0k7RUFDSSwrQkFBQTtBQ0FSO0FERUk7RUFDSSxlQUFBO0FDQVI7QURHQTtFQUNJLFdBQUE7RUFDQSwwQkFBQTtFQUNBLG1DQUFBO1VBQUEsMkJBQUE7RUFDQSxlQUFBO0FDQUo7QURHQSxXQUFBO0FBQ0E7RUFDSTtJQUNJLGFBQUE7RUNBTjs7RURFRTtJQUNJLHVCQUFBO0VDQ047QUFDRiIsImZpbGUiOiJzcmMvYXBwL2NvbXBvbmVudHMvbW92ZS1saW5lLWxpc3QvbW92ZS1saW5lLWxpc3QuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJpb24tcm93IHtcbiAgICAmLnN1Y2Nlc3Mge1xuICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXN1Y2Nlc3MpO1xuICAgIH1cbiAgICAmLnByb2R1Y3RfbGluayB7XG4gICAgICAgIGN1cnNvcjogcG9pbnRlcjtcbiAgICB9XG59XG5kaXYucHJvZHVjdF9saW5rIHtcbiAgICBjb2xvcjogYmx1ZTtcbiAgICB0ZXh0LWRlY29yYXRpb246IHVuZGVybGluZTtcbiAgICB0ZXh0LWRlY29yYXRpb24tY29sb3I6IGJsdWU7XG4gICAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG4vKiBNZWRpYXMgKi9cbkBtZWRpYSBzY3JlZW4gYW5kIChtYXgtd2lkdGg6IDU3NnB4KSB7XG4gICAgaW9uLWdyaWQgPiBpb24tcm93OmZpcnN0LWNoaWxkIHtcbiAgICAgICAgZGlzcGxheTogbm9uZTtcbiAgICB9XG4gICAgaW9uLWdyaWQgPiBpb24tcm93IHtcbiAgICAgICAgYm9yZGVyOiAxcHggYmxhY2sgc29saWQ7XG4gICAgfVxufSIsImlvbi1yb3cuc3VjY2VzcyB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc3VjY2Vzcyk7XG59XG5pb24tcm93LnByb2R1Y3RfbGluayB7XG4gIGN1cnNvcjogcG9pbnRlcjtcbn1cblxuZGl2LnByb2R1Y3RfbGluayB7XG4gIGNvbG9yOiBibHVlO1xuICB0ZXh0LWRlY29yYXRpb246IHVuZGVybGluZTtcbiAgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBibHVlO1xuICBjdXJzb3I6IHBvaW50ZXI7XG59XG5cbi8qIE1lZGlhcyAqL1xuQG1lZGlhIHNjcmVlbiBhbmQgKG1heC13aWR0aDogNTc2cHgpIHtcbiAgaW9uLWdyaWQgPiBpb24tcm93OmZpcnN0LWNoaWxkIHtcbiAgICBkaXNwbGF5OiBub25lO1xuICB9XG5cbiAgaW9uLWdyaWQgPiBpb24tcm93IHtcbiAgICBib3JkZXI6IDFweCBibGFjayBzb2xpZDtcbiAgfVxufSJdfQ== */");

/***/ }),

/***/ "./src/app/components/move-line-list/move-line-list.component.ts":
/*!***********************************************************************!*\
  !*** ./src/app/components/move-line-list/move-line-list.component.ts ***!
  \***********************************************************************/
/*! exports provided: MoveLineListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MoveLineListComponent", function() { return MoveLineListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");





var MoveLineListComponent = /** @class */ (function () {
    function MoveLineListComponent(router, alertCtrl, 
    /* private audio: AudioService, */
    route, stock) {
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.route = route;
        this.stock = stock;
    }
    MoveLineListComponent.prototype.ngOnInit = function () {
        if (this.move_lines) {
            this.move_lines_info = this.move_lines;
            this.picking = this.route.snapshot.paramMap.get('id');
        }
        else {
            this.get_move_lines_list();
        }
    };
    MoveLineListComponent.prototype.open_link = function (move) {
        this.router.navigateByUrl('/move-form/' + move);
    };
    MoveLineListComponent.prototype.get_move_lines_list = function () {
        var _this = this;
        this.stock.get_move_lines_list(Number(this.picking)).then(function (lines_data) {
            _this.move_lines_info = lines_data;
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperar los movimientos:', error);
        });
    };
    MoveLineListComponent.prototype.force_set_qty_done = function (move_id) {
        var _this = this;
        this.stock.force_set_qty_done(Number(move_id), 'stock.move').then(function (lines_data) {
            console.log(lines_data);
            if (lines_data == true) {
                _this.get_move_lines_list();
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al forzar la cantidad:', error);
        });
    };
    MoveLineListComponent.prototype.force_set_assigned_qty_done = function (move_id) {
        var _this = this;
        this.stock.force_set_assigned_qty_done(Number(move_id), 'stock.move').then(function (lines_data) {
            console.log(lines_data);
            if (lines_data == true) {
                _this.get_move_lines_list();
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al forzar la cantidad:', error);
        });
    };
    MoveLineListComponent.prototype.presentAlert = function (titulo, texto) {
        return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"])(this, void 0, void 0, function () {
            var alert;
            return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"])(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.alertCtrl.create({
                            header: titulo,
                            subHeader: texto,
                            buttons: ['Ok']
                        })];
                    case 1:
                        alert = _a.sent();
                        return [4 /*yield*/, alert.present()];
                    case 2:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    MoveLineListComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_4__["StockService"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", String)
    ], MoveLineListComponent.prototype, "scanner_reading", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)
    ], MoveLineListComponent.prototype, "move_lines", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", String)
    ], MoveLineListComponent.prototype, "code", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", String)
    ], MoveLineListComponent.prototype, "picking_fields", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)
    ], MoveLineListComponent.prototype, "not_allowed_fields", void 0);
    MoveLineListComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-move-line-list',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./move-line-list.component.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/move-line-list/move-line-list.component.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./move-line-list.component.scss */ "./src/app/components/move-line-list/move-line-list.component.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_4__["StockService"]])
    ], MoveLineListComponent);
    return MoveLineListComponent;
}());



/***/ }),

/***/ "./src/app/pages/stock-picking/stock-picking.module.ts":
/*!*************************************************************!*\
  !*** ./src/app/pages/stock-picking/stock-picking.module.ts ***!
  \*************************************************************/
/*! exports provided: StockPickingPageModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockPickingPageModule", function() { return StockPickingPageModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _stock_picking_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./stock-picking.page */ "./src/app/pages/stock-picking/stock-picking.page.ts");
/* harmony import */ var _components_move_line_list_move_line_list_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../components/move-line-list/move-line-list.component */ "./src/app/components/move-line-list/move-line-list.component.ts");
/* harmony import */ var _components_move_line_details_list_move_line_details_list_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../components/move-line-details-list/move-line-details-list.component */ "./src/app/components/move-line-details-list/move-line-details-list.component.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../shared/shared.module */ "./src/app/shared/shared.module.ts");










var routes = [
    {
        path: '',
        component: _stock_picking_page__WEBPACK_IMPORTED_MODULE_6__["StockPickingPage"]
    }
];
var StockPickingPageModule = /** @class */ (function () {
    function StockPickingPageModule() {
    }
    StockPickingPageModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes),
                _shared_shared_module__WEBPACK_IMPORTED_MODULE_9__["SharedModule"]
            ],
            entryComponents: [_components_move_line_list_move_line_list_component__WEBPACK_IMPORTED_MODULE_7__["MoveLineListComponent"], _components_move_line_details_list_move_line_details_list_component__WEBPACK_IMPORTED_MODULE_8__["MoveLineDetailsListComponent"]],
            declarations: [_stock_picking_page__WEBPACK_IMPORTED_MODULE_6__["StockPickingPage"], _components_move_line_list_move_line_list_component__WEBPACK_IMPORTED_MODULE_7__["MoveLineListComponent"], _components_move_line_details_list_move_line_details_list_component__WEBPACK_IMPORTED_MODULE_8__["MoveLineDetailsListComponent"]]
        })
    ], StockPickingPageModule);
    return StockPickingPageModule;
}());



/***/ }),

/***/ "./src/app/pages/stock-picking/stock-picking.page.scss":
/*!*************************************************************!*\
  !*** ./src/app/pages/stock-picking/stock-picking.page.scss ***!
  \*************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3BhZ2VzL3N0b2NrLXBpY2tpbmcvc3RvY2stcGlja2luZy5wYWdlLnNjc3MifQ== */");

/***/ }),

/***/ "./src/app/pages/stock-picking/stock-picking.page.ts":
/*!***********************************************************!*\
  !*** ./src/app/pages/stock-picking/stock-picking.page.ts ***!
  \***********************************************************/
/*! exports provided: StockPickingPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockPickingPage", function() { return StockPickingPage; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_voice_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../services/voice.service */ "./src/app/services/voice.service.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");











var StockPickingPage = /** @class */ (function () {
    function StockPickingPage(odoo, router, alertCtrl, audio, voice, stock, route, location, loadingController, actionSheetController) {
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.audio = audio;
        this.voice = voice;
        this.stock = stock;
        this.route = route;
        this.location = location;
        this.loadingController = loadingController;
        this.actionSheetController = actionSheetController;
        this.moves = ['up', 'down', 'left', 'right'];
    }
    StockPickingPage.prototype.ngOnInit = function () {
        var _this = this;
        this.odoo.isLoggedIn().then(function (data) {
            if (data == false) {
                _this.router.navigateByUrl('/login');
            }
            _this.active_operation = false;
            _this.picking = _this.route.snapshot.paramMap.get('id');
            _this.get_picking_info(_this.picking);
            _this.voice.voice_command_refresh$.subscribe(function (data) {
                _this.voice_command_check();
            });
            _this.audio.play('click');
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    StockPickingPage.prototype.onReadingEmitted = function (val) {
        if (this.moves.includes(val)) {
            this.page_controller(val);
        }
        else {
            this.scanner_reading = val;
        }
    };
    StockPickingPage.prototype.presentAlert = function (titulo, texto) {
        return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"])(this, void 0, void 0, function () {
            var alert;
            return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"])(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.audio.play('error');
                        return [4 /*yield*/, this.alertCtrl.create({
                                header: titulo,
                                subHeader: texto,
                                buttons: ['Ok']
                            })];
                    case 1:
                        alert = _a.sent();
                        return [4 /*yield*/, alert.present()];
                    case 2:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    // Navigation 
    StockPickingPage.prototype.page_controller = function (direction) {
        if (direction == 'up') {
            console.log("up");
        }
        else if (direction == 'down') {
            console.log("down");
        }
        else if (direction == 'left') {
            console.log("left");
        }
        else if (direction == 'right') {
            console.log("right");
        }
    };
    StockPickingPage.prototype.open_link = function (location_id) {
        this.router.navigateByUrl('/stock-location/' + location_id);
    };
    StockPickingPage.prototype.action_assign = function () {
        var _this = this;
        this.stock.action_assign(this.picking).then(function (lines_data) {
            if (lines_data == true) {
                console.log("Reloading");
                _this.get_picking_info(_this.picking);
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al asignar cantidades:', error);
        });
    };
    StockPickingPage.prototype.button_validate = function () {
        var _this = this;
        this.presentLoading();
        this.stock.button_validate(Number(this.picking)).then(function (lines_data) {
            if (lines_data && lines_data['err'] == false) {
                console.log("Reloading");
                _this.loading.dismiss();
                _this.location.back();
            }
            else if (lines_data['err'] != false) {
                _this.loading.dismiss();
                _this.presentAlert('Error al validar el albarán:', lines_data['err']);
            }
        })
            .catch(function (error) {
            _this.loading.dismiss();
            _this.presentAlert('Error al validar el albarán:', error);
        });
    };
    StockPickingPage.prototype.force_set_qty_done = function (move_id, field, model) {
        if (model === void 0) { model = 'stock.picking'; }
        return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"])(this, void 0, void 0, function () {
            var _this = this;
            return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"])(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.stock.force_set_qty_done(Number(move_id), field, model).then(function (lines_data) {
                            if (lines_data == true) {
                                console.log("Reloading");
                                _this.move_lines = false;
                                _this.move_line_ids = false;
                                _this.get_picking_info(_this.picking);
                            }
                        })
                            .catch(function (error) {
                            _this.presentAlert('Error al forzar la cantidad:', error);
                        })];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    StockPickingPage.prototype.force_reset_qties = function (pick_id) {
        return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"])(this, void 0, void 0, function () {
            var _this = this;
            return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"])(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.stock.force_reset_qties(Number(pick_id), 'stock.picking').then(function (lines_data) {
                            console.log(lines_data);
                            if (lines_data == true) {
                                console.log("Reloading");
                                _this.move_lines = false;
                                _this.move_line_ids = false;
                                _this.get_picking_info(_this.picking);
                            }
                        })
                            .catch(function (error) {
                            _this.presentAlert('Error al forzar la cantidad:', error);
                        })];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    StockPickingPage.prototype.presentLoading = function () {
        return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"])(this, void 0, void 0, function () {
            var _a;
            return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"])(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this;
                        return [4 /*yield*/, this.loadingController.create({
                                message: 'Validando...',
                                translucent: true,
                                cssClass: 'custom-class custom-loading'
                            })];
                    case 1:
                        _a.loading = _b.sent();
                        return [4 /*yield*/, this.loading.present()];
                    case 2:
                        _b.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    StockPickingPage.prototype.get_picking_info = function (picking) {
        var _this = this;
        this.stock.get_picking_info(picking).then(function (data) {
            _this.picking_data = data[0];
            _this.picking_code = data[0].group_code[0];
            if (_this.picking_data && _this.picking_data['picking_fields']) {
                _this.not_allowed_fields = _this.picking_data['picking_fields'].split(',');
                console.log(_this.not_allowed_fields);
            }
            if (_this.picking_data && _this.picking_data['move_fields']) {
                _this.not_allowed_m_fields = _this.picking_data['move_fields'].split(',');
                console.log(_this.not_allowed_m_fields);
            }
            if (_this.picking_data && _this.picking_data['move_line_fields']) {
                _this.not_allowed_ml_fields = _this.picking_data['move_line_fields'].split(',');
                console.log(_this.not_allowed_ml_fields);
            }
            _this.move_lines = _this.picking_data['move_lines'];
            _this.move_line_ids = _this.picking_data['move_line_ids'];
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperar el picking:', error);
        });
    };
    // Voice command
    StockPickingPage.prototype.voice_command_check = function () {
        console.log("voice_command_check");
        console.log(this.voice.voice_command);
        if (this.voice.voice_command) {
            var voice_command_register = this.voice.voice_command;
            console.log("Recibida orden de voz: " + voice_command_register);
            if (this.check_if_value_in_responses("validar", voice_command_register) && this.picking_data['show_validate']) {
                console.log("entra al validate");
                this.button_validate();
            }
            else if (this.picking_data && (this.picking_data['state'] == 'confirmed' || this.picking_data['state'] == 'assigned') && this.check_if_value_in_responses("hecho", voice_command_register)) {
                console.log("entra al hecho");
                this.force_set_qty_done(this.picking_data['id'], 'product_qty', 'stock.picking');
            }
            else if (this.picking_data && (this.picking_data['state'] == 'confirmed' || this.picking_data['state'] == 'assigned') && this.check_if_value_in_responses("reiniciar", voice_command_register)) {
                console.log("entra al reset");
                this.force_reset_qties(this.picking_data['id']);
            }
        }
    };
    StockPickingPage.prototype.check_if_value_in_responses = function (value, dict) {
        if (value == dict[0] || value == dict[1] || value == dict[2]) {
            return true;
        }
        else {
            return false;
        }
    };
    StockPickingPage.prototype.create_buttons = function () {
        var _this = this;
        var buttons = [{
                text: 'Cancel',
                icon: 'close',
                role: 'cancel',
                handler: function () {
                    console.log('Cancel clicked');
                }
            }];
        if (this.picking_data['show_validate']) {
            var button = {
                text: 'Validar',
                icon: '',
                role: '',
                handler: function () {
                    _this.button_validate();
                }
            };
            buttons.push(button);
        }
        if (this.picking_data && (this.picking_data['state'] == 'confirmed' || this.picking_data['state'] == 'assigned')) {
            var button = {
                text: 'Reservas a hecho',
                icon: '',
                role: '',
                handler: function () {
                    _this.force_set_qty_done(_this.picking_data['id'], 'product_qty', 'stock.picking');
                }
            };
            var buttonReset = {
                text: 'Reset',
                icon: '',
                role: '',
                handler: function () {
                    _this.force_reset_qties(_this.picking_data['id']);
                }
            };
            buttons.push(button);
            buttons.push(buttonReset);
        }
        /* if (this.picking_data['show_check_availability']) {
          actionSheet.buttons.push({
            text: 'Asignar',
              handler: () => {
                this.action_assign();
              }
          })
        } */
        return buttons;
    };
    StockPickingPage.prototype.presentActionSheet = function () {
        return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"])(this, void 0, void 0, function () {
            var actionSheet;
            return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"])(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.actionSheetController.create({
                            header: 'Opciones',
                            buttons: this.create_buttons()
                        })];
                    case 1:
                        actionSheet = _a.sent();
                        return [4 /*yield*/, actionSheet.present()];
                    case 2:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    StockPickingPage.ctorParameters = function () { return [
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_1__["OdooService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_6__["AudioService"] },
        { type: _services_voice_service__WEBPACK_IMPORTED_MODULE_7__["VoiceService"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_5__["StockService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _angular_common__WEBPACK_IMPORTED_MODULE_8__["Location"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["LoadingController"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["ActionSheetController"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", String)
    ], StockPickingPage.prototype, "scanner_reading", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Boolean)
    ], StockPickingPage.prototype, "voice_command", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)
    ], StockPickingPage.prototype, "pick", void 0);
    StockPickingPage = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Component"])({
            selector: 'app-stock-picking',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./stock-picking.page.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-picking/stock-picking.page.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./stock-picking.page.scss */ "./src/app/pages/stock-picking/stock-picking.page.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_1__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_6__["AudioService"],
            _services_voice_service__WEBPACK_IMPORTED_MODULE_7__["VoiceService"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_5__["StockService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"],
            _angular_common__WEBPACK_IMPORTED_MODULE_8__["Location"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["LoadingController"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["ActionSheetController"]])
    ], StockPickingPage);
    return StockPickingPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-stock-picking-stock-picking-module.js.map
(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-stock-picking-stock-picking-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/components/move-line-details-list/move-line-details-list.component.html":
/*!*******************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/components/move-line-details-list/move-line-details-list.component.html ***!
  \*******************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-grid>\n  <ion-row>  \n    <ion-col size=\"6\">\n      <div><strong>Producto</strong></div>\n    </ion-col>\n\n    <ion-col *ngIf=\"picking_fields.indexOf('location_id')<0\">\n      <div><strong>De</strong></div>\n    </ion-col>\n  \n    <ion-col *ngIf=\"picking_fields.indexOf('location_dest_id')<0\">\n      <div><strong>A</strong></div>\n    </ion-col>\n  \n    <!--ion-col *ngIf=\"picking_fields.indexOf('package_id')<0\">\n      <div><strong>Pqt. O.</strong></div>\n    </ion-col>\n  \n    <ion-col  *ngIf=\"picking_fields.indexOf('package_dest_id')<0\">\n      <div><strong>Pqt. D.</strong></div>\n    </ion-col-->\n    \n    <ion-col size=\"1\" *ngIf=\"picking_fields.indexOf('qty_available')<0\">\n      <div><strong>Dis.</strong></div>\n    </ion-col>\n  \n    <ion-col size=\"1\">\n      <div><strong>Res.</strong></div>\n    </ion-col>\n    \n    <ion-col size=\"1\">\n      <div><strong>Hecha</strong></div>\n    </ion-col>\n  </ion-row>\n\n  <ion-row *ngFor=\"let line of move_line_ids_info\" [ngClass]=\"{'success': line.qty_done == line.product_uom_qty}\">\n    <ion-col size=\"6\" >\n      <div class=\"link\" (click)=\"open_link(line.product_id[0])\">{{line.product_id[1]}} <strong *ngIf=\"line.lot_id\"> = > {{line.lot_id[1]}}</strong></div>\n    </ion-col>\n  \n    <ion-col *ngIf=\"picking_fields.indexOf('location_id')<0\">\n      <div>{{line.location_id[1]}}</div>\n      <div *ngIf=\"line.package_id\" >{{line.package_id[1]}}</div>\n    </ion-col>\n  \n    <ion-col *ngIf=\"picking_fields.indexOf('location_dest_id')<0\">\n      <div>{{line.location_dest_id[1]}}</div>\n      <div *ngIf=\"line.result_package_id\" >{{line.result_package_id[1]}}</div>\n    </ion-col>\n  \n    <!--ion-col  *ngIf=\"picking_fields.indexOf('result_package_id')<0\">\n      <div>{{line.package_id[1]}}</div>\n    </ion-col>\n  \n    <ion-col  *ngIf=\"picking_fields.indexOf('package_dest_id')<0\">\n      <div>{{line.result_package_id[1]}}</div>\n    </ion-col-->\n    \n    <ion-col size=\"1\" *ngIf=\"picking_fields.indexOf('qty_available')<0\">\n      <div class=\"link\" *ngIf=\"code != 'incoming' && (line.state == 'confirmed' || line.state == 'assigned') && line.qty_done == 0; else noLinkAvailable\" \n        (click)=\"force_set_qty_done(line.id, 'qty_available')\">{{line.qty_available}}</div>\n    </ion-col>\n\n    <ng-template #noLinkAvailable >\n        <div>{{line.qty_available}}</div>\n    </ng-template>\n  \n    <ion-col size=\"1\">\n      <div class=\"link\" *ngIf=\"(line.state != 'done' || line.state == 'cancel') && line.qty_done == 0; else noLinkUom\" \n      (click)=\"force_set_qty_done(line.id, 'product_uom_qty')\">{{line.product_uom_qty}}</div>\n    </ion-col>\n    \n    <ng-template #noLinkUom>\n        <div>{{line.product_uom_qty}}</div>\n    </ng-template>\n\n    <ion-col size=\"1\">\n\n      <div>{{line.qty_done}}</div>\n    </ion-col>\n  </ion-row>\n\n</ion-grid>"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/components/move-line-list/move-line-list.component.html":
/*!***************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/components/move-line-list/move-line-list.component.html ***!
  \***************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-grid>\n  <ion-row>\n    <ion-col>\n      <div><strong>Producto</strong></div>\n    </ion-col>  \n\n    <ion-col size=\"2\">\n      <div><strong>Pedida</strong></div>\n    </ion-col>\n\n    <ion-col size=\"2\">\n      <div><strong>Reservada</strong></div>\n    </ion-col>\n    \n    <ion-col size=\"2\">\n      <div><strong>Hecha</strong></div>\n    </ion-col>\n  </ion-row>\n\n  <ion-row *ngFor=\"let line of move_lines_info\" [ngClass]=\"{'success': line.quantity_done == line.product_uom_qty}\">\n    <ion-col>\n      <div class=\"product_link\" (click)=\"open_link(line.product_id[0])\">{{line.product_id[1]}}</div>\n    </ion-col>\n    \n    <ion-col size=\"2\">\n      <div *ngIf=\"(line.quantity_done != 0 || (line.state != 'confirmed' && line.state != 'partially_available' && line.state != 'assigned')); else link_product_uom_qty\">\n        {{line.product_uom_qty}}\n      </div>\n    </ion-col>\n\n    <ng-template #link_product_uom_qty>\n      <div (click)=\"force_set_qty_done(line.id, 'product_uom_qty', 'stock.move')\" >{{line.product_uom_qty}}</div>\n    </ng-template>\n    \n    <ion-col size=\"2\">\n      <div *ngIf=\"(line.quantity_done != 0 || line.reserved_availability == 0 || code == 'incoming' || (line.state == 'done' || line.state == 'assigned')); else link_qty_done\">{{line.reserved_availability}}</div>\n    </ion-col>\n\n    <ng-template #link_qty_done>\n      <div (click)=\"force_set_assigned_qty_done(line.id)\">{{line.reserved_availability}}</div>\n    </ng-template>\n    \n    <ion-col size=\"2\">\n      <div>{{line.quantity_done}}</div>\n    </ion-col>\n  </ion-row>\n</ion-grid>"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/components/picking-info/picking-info.component.html":
/*!***********************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/components/picking-info/picking-info.component.html ***!
  \***********************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-card *ngIf=\"picking_data\">\n\n  <ion-card-header>\n    <ion-row>\n      <ion-col>\n        <ion-card-title>{{picking_data.name}}</ion-card-title>\n        <ion-card-subtitle>{{picking_data.picking_type_id[1]}}</ion-card-subtitle>\n      </ion-col>\n      <ion-col>\n        <!-- <ion-button *ngIf=\"picking_data.show_check_availability\" size=\"small\" class=\"button-text\" (click)=\"action_assign()\">Asignar</ion-button> -->\n        <ion-button *ngIf=\"picking_data.show_validate\" size=\"small\" class=\"button-text\" (click)=\"button_validate()\">Validar</ion-button>\n        <ion-button size=\"small\" *ngIf=\"picking_data && (picking_data.state == 'confirmed' || picking_data.state == 'assigned')\" class=\"button-text\" (click)=\"force_set_qty_done(picking_data.id, 'product_qty', 'stock.picking')\">Reservas a hecho</ion-button>\n        <ion-button size=\"small\" *ngIf=\"picking_data && (picking_data.state == 'confirmed' || picking_data.state == 'assigned')\" class=\"button-text\" (click)=\"force_reset_qties(picking_data.id, 'stock.picking')\">Reset</ion-button>\n      </ion-col>\n    </ion-row>\n  </ion-card-header>\n\n  <ion-card-content>\n    <div><strong>Previsto: </strong>{{picking_data.scheduled_date}}</div>\n    <div><strong>Origen: </strong><span class=\"location\" (click)=\"open_link(picking_data.location_id[0])\">{{picking_data.location_id[1]}}</span></div>\n    <div><strong>Destino: </strong><span class=\"location\" (click)=\"open_link(picking_data.location_dest_id[0])\">{{picking_data.location_dest_id[1]}}</span></div>\n    <div [ngSwitch]=\"picking_data.priority\">\n      <strong>Prioridad: </strong>\n      <ion-text *ngSwitchCase=\"0\">No Urgente</ion-text>\n      <ion-text *ngSwitchCase=\"1\">Normal</ion-text>\n      <ion-text *ngSwitchCase=\"2\">Urgente</ion-text>\n      <ion-text *ngSwitchCase=\"3\">Muy Urgente</ion-text>\n    </div>\n    \n    <div *ngIf=\"picking_data.note\"><strong>Nota: </strong>{{picking_data.note}}</div>\n\n  </ion-card-content>\n\n</ion-card>\n\n<div>\n\n  <ion-card *ngIf=\"move_lines\">\n    <ion-card-header>\n      <ion-row>\n        <ion-col>\n          <ion-card-title *ngIf=\"!active_operation; else detailed_title\">Operaciones</ion-card-title>\n        </ion-col>\n        <!-- <ion-col class=\"ion-text-right\">\n          <ion-item>\n            <ion-label>Detalles:</ion-label>\n            <ion-toggle [(ngModel)]=\"active_operation\" color=\"primary\"></ion-toggle>\n          </ion-item>\n        </ion-col> -->\n      </ion-row>\n    </ion-card-header>\n\n    <ng-template #detailed_title>\n      <ion-card-title>Operaciones detalladas</ion-card-title>\n    </ng-template>\n\n    <ion-card-content *ngIf=\"move_lines\">\n      <app-move-line-list *ngIf=\"!active_operation && move_lines; else detailed_grid\" \n          [scanner_reading]=\"scanner_reading\" \n          [code]=\"picking_code\" \n          [picking_fields] = \"picking_data.picking_fields\"\n          [move_lines]=\"move_lines\">\n      </app-move-line-list>\n\n\n      <!-- <ion-grid>          \n        <ion-row>\n          <ion-col>\n            \n          </ion-col>\n          \n          <ion-col size=\"2\">\n              <strong>Totales:</strong>\n          </ion-col>\n        \n          <ion-col size=\"2\">\n            <div *ngIf=\"!active_operation; else reserved_lines\">{{picking_data.reserved_availability}}</div>\n          </ion-col>\n      \n          <ion-col size=\"2\">\n            <div *ngIf=\"!active_operation; else done_lines\">{{picking_data.quantity_done}}</div>\n          </ion-col>\n        </ion-row>\n      </ion-grid> -->\n      <ng-template #detailed_grid>\n        <app-move-line-details-list *ngIf=\"move_line_ids\" \n        [code]=\"picking_code\" \n        [picking_fields] = \"picking_data.picking_fields\"\n        [scanner_reading]=\"scanner_reading\"  \n        [move_line_ids]=\"move_line_ids\"></app-move-line-details-list>\n      </ng-template>\n      <!-- <ng-template #reserved_lines>\n        <div>{{picking_data.reserved_availability_lines}}</div>\n      </ng-template>\n\n      <ng-template #done_lines>\n        <div>{{picking_data.quantity_done_lines}}</div>\n      </ng-template> -->\n\n    </ion-card-content>\n  </ion-card>\n  \n   <ion-card *ngIf=\"move_line_ids\">\n    <ion-card-header>\n      <ion-row>\n        <ion-col>\n          <ion-card-title>Operaciones detalladas</ion-card-title>\n        </ion-col>\n      </ion-row>\n    </ion-card-header>\n\n    \n\n    <ion-card-content *ngIf=\"move_line_ids\">\n       <app-move-line-details-list *ngIf=\"move_line_ids\" \n        [code]=\"picking_code\" \n        [picking_fields] = \"picking_data.picking_fields\"\n        [scanner_reading]=\"scanner_reading\"  \n        [move_line_ids]=\"move_line_ids\"></app-move-line-details-list>\n\n    </ion-card-content>\n  </ion-card>\n\n</div>"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/pages/stock-picking/stock-picking.page.html":
/*!***************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/pages/stock-picking/stock-picking.page.html ***!
  \***************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"start\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n    <app-scanner-header slot=\"end\" (show_scan_form_changed)=\"onShowEmitted($event)\" [show_scan_form]=show_scan_form></app-scanner-header>\n    <ion-title>Detalles de la operación</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <app-picking-info [scanner_reading]=\"scanner_reading\"></app-picking-info>\n</ion-content>\n\n<app-scanner-footer (scanner_reading_changed)=\"onReadingEmitted($event)\" [show_scan_form]=show_scan_form [scanner_reading]=\"scanner_reading\"></app-scanner-footer>"

/***/ }),

/***/ "./src/app/components/move-line-details-list/move-line-details-list.component.scss":
/*!*****************************************************************************************!*\
  !*** ./src/app/components/move-line-details-list/move-line-details-list.component.scss ***!
  \*****************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "ion-row.success {\n  color: var(--ion-color-success);\n}\n\ndiv.link {\n  color: blue;\n  text-decoration: underline;\n  -webkit-text-decoration-color: blue;\n          text-decoration-color: blue;\n  cursor: pointer;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9jb21wb25lbnRzL21vdmUtbGluZS1kZXRhaWxzLWxpc3QvbW92ZS1saW5lLWRldGFpbHMtbGlzdC5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvY29tcG9uZW50cy9tb3ZlLWxpbmUtZGV0YWlscy1saXN0L21vdmUtbGluZS1kZXRhaWxzLWxpc3QuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQ0k7RUFDSSwrQkFBQTtBQ0FSOztBREdBO0VBQ0ksV0FBQTtFQUNBLDBCQUFBO0VBQ0EsbUNBQUE7VUFBQSwyQkFBQTtFQUNBLGVBQUE7QUNBSiIsImZpbGUiOiJzcmMvYXBwL2NvbXBvbmVudHMvbW92ZS1saW5lLWRldGFpbHMtbGlzdC9tb3ZlLWxpbmUtZGV0YWlscy1saXN0LmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiaW9uLXJvdyB7XG4gICAgJi5zdWNjZXNzIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zdWNjZXNzKTtcbiAgICB9XG59XG5kaXYubGluayB7XG4gICAgY29sb3I6IGJsdWU7XG4gICAgdGV4dC1kZWNvcmF0aW9uOiB1bmRlcmxpbmU7XG4gICAgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBibHVlO1xuICAgIGN1cnNvcjogcG9pbnRlcjtcbn0iLCJpb24tcm93LnN1Y2Nlc3Mge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXN1Y2Nlc3MpO1xufVxuXG5kaXYubGluayB7XG4gIGNvbG9yOiBibHVlO1xuICB0ZXh0LWRlY29yYXRpb246IHVuZGVybGluZTtcbiAgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBibHVlO1xuICBjdXJzb3I6IHBvaW50ZXI7XG59Il19 */"

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");





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
            this.get_move_lines_details_list();
        }
    };
    MoveLineDetailsListComponent.prototype.ngOnChanges = function (changeRecord) {
        if (changeRecord['scanner_reading'] && changeRecord['scanner_reading']['currentValue']) {
            var default_code = changeRecord['scanner_reading']['currentValue'];
            console.log("Confirmamos cantidad reservada para el producto con default code:" + default_code);
            this.force_set_qty_done_by_product_code_apk(default_code, 'product_uom_qty');
        }
    };
    MoveLineDetailsListComponent.prototype.get_move_lines_details_list = function () {
        var _this = this;
        this.stock.get_move_lines_details_list(this.move_line_ids).then(function (lines_data) {
            _this.move_line_ids_info = lines_data;
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperar los movimientos:', error);
        });
    };
    MoveLineDetailsListComponent.prototype.force_set_qty_done = function (move_id, field) {
        var _this = this;
        this.stock.force_set_qty_done(Number(move_id), field, 'stock.move.line').then(function (lines_data) {
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
    MoveLineDetailsListComponent.prototype.open_link = function (pick_id) {
        this.router.navigateByUrl('/product/' + pick_id);
    };
    MoveLineDetailsListComponent.prototype.presentAlert = function (titulo, texto) {
        return tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"](this, void 0, void 0, function () {
            var alert;
            return tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"](this, function (_a) {
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
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", String)
    ], MoveLineDetailsListComponent.prototype, "scanner_reading", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], MoveLineDetailsListComponent.prototype, "move_line_ids", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", String)
    ], MoveLineDetailsListComponent.prototype, "code", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", String)
    ], MoveLineDetailsListComponent.prototype, "picking_fields", void 0);
    MoveLineDetailsListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-move-line-details-list',
            template: __webpack_require__(/*! raw-loader!./move-line-details-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/components/move-line-details-list/move-line-details-list.component.html"),
            styles: [__webpack_require__(/*! ./move-line-details-list.component.scss */ "./src/app/components/move-line-details-list/move-line-details-list.component.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
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
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "ion-row.success {\n  color: var(--ion-color-success);\n}\n\ndiv.product_link {\n  color: blue;\n  text-decoration: underline;\n  -webkit-text-decoration-color: blue;\n          text-decoration-color: blue;\n  cursor: pointer;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9jb21wb25lbnRzL21vdmUtbGluZS1saXN0L21vdmUtbGluZS1saXN0LmNvbXBvbmVudC5zY3NzIiwic3JjL2FwcC9jb21wb25lbnRzL21vdmUtbGluZS1saXN0L21vdmUtbGluZS1saXN0LmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUNJO0VBQ0ksK0JBQUE7QUNBUjs7QURHQTtFQUNJLFdBQUE7RUFDQSwwQkFBQTtFQUNBLG1DQUFBO1VBQUEsMkJBQUE7RUFDQSxlQUFBO0FDQUoiLCJmaWxlIjoic3JjL2FwcC9jb21wb25lbnRzL21vdmUtbGluZS1saXN0L21vdmUtbGluZS1saXN0LmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiaW9uLXJvdyB7XG4gICAgJi5zdWNjZXNzIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zdWNjZXNzKTtcbiAgICB9XG59XG5kaXYucHJvZHVjdF9saW5rIHtcbiAgICBjb2xvcjogYmx1ZTtcbiAgICB0ZXh0LWRlY29yYXRpb246IHVuZGVybGluZTtcbiAgICB0ZXh0LWRlY29yYXRpb24tY29sb3I6IGJsdWU7XG4gICAgY3Vyc29yOiBwb2ludGVyO1xufSIsImlvbi1yb3cuc3VjY2VzcyB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc3VjY2Vzcyk7XG59XG5cbmRpdi5wcm9kdWN0X2xpbmsge1xuICBjb2xvcjogYmx1ZTtcbiAgdGV4dC1kZWNvcmF0aW9uOiB1bmRlcmxpbmU7XG4gIHRleHQtZGVjb3JhdGlvbi1jb2xvcjogYmx1ZTtcbiAgY3Vyc29yOiBwb2ludGVyO1xufSJdfQ== */"

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");





var MoveLineListComponent = /** @class */ (function () {
    function MoveLineListComponent(router, alertCtrl, 
    /* private audio: AudioService, */
    stock) {
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.stock = stock;
    }
    MoveLineListComponent.prototype.ngOnInit = function () {
        if (this.move_lines) {
            console.log(this.move_lines);
            this.get_move_lines_list();
        }
    };
    MoveLineListComponent.prototype.open_link = function (product_id) {
        this.router.navigateByUrl('/product/' + product_id);
    };
    MoveLineListComponent.prototype.get_move_lines_list = function () {
        var _this = this;
        this.stock.get_move_lines_list(this.move_lines).then(function (lines_data) {
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
        return tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"](this, void 0, void 0, function () {
            var alert;
            return tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"](this, function (_a) {
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
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_4__["StockService"] }
    ]; };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", String)
    ], MoveLineListComponent.prototype, "scanner_reading", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], MoveLineListComponent.prototype, "move_lines", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", String)
    ], MoveLineListComponent.prototype, "code", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", String)
    ], MoveLineListComponent.prototype, "picking_fields", void 0);
    MoveLineListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-move-line-list',
            template: __webpack_require__(/*! raw-loader!./move-line-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/components/move-line-list/move-line-list.component.html"),
            styles: [__webpack_require__(/*! ./move-line-list.component.scss */ "./src/app/components/move-line-list/move-line-list.component.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_4__["StockService"]])
    ], MoveLineListComponent);
    return MoveLineListComponent;
}());



/***/ }),

/***/ "./src/app/components/picking-info/picking-info.component.scss":
/*!*********************************************************************!*\
  !*** ./src/app/components/picking-info/picking-info.component.scss ***!
  \*********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "span.location {\n  color: blue;\n  text-decoration: underline;\n  -webkit-text-decoration-color: blue;\n          text-decoration-color: blue;\n  cursor: pointer;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9jb21wb25lbnRzL3BpY2tpbmctaW5mby9waWNraW5nLWluZm8uY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL2NvbXBvbmVudHMvcGlja2luZy1pbmZvL3BpY2tpbmctaW5mby5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNJLFdBQUE7RUFDQSwwQkFBQTtFQUNBLG1DQUFBO1VBQUEsMkJBQUE7RUFDQSxlQUFBO0FDQ0oiLCJmaWxlIjoic3JjL2FwcC9jb21wb25lbnRzL3BpY2tpbmctaW5mby9waWNraW5nLWluZm8uY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJzcGFuLmxvY2F0aW9uIHtcbiAgICBjb2xvcjogYmx1ZTtcbiAgICB0ZXh0LWRlY29yYXRpb246IHVuZGVybGluZTtcbiAgICB0ZXh0LWRlY29yYXRpb24tY29sb3I6IGJsdWU7XG4gICAgY3Vyc29yOiBwb2ludGVyO1xufSIsInNwYW4ubG9jYXRpb24ge1xuICBjb2xvcjogYmx1ZTtcbiAgdGV4dC1kZWNvcmF0aW9uOiB1bmRlcmxpbmU7XG4gIHRleHQtZGVjb3JhdGlvbi1jb2xvcjogYmx1ZTtcbiAgY3Vyc29yOiBwb2ludGVyO1xufSJdfQ== */"

/***/ }),

/***/ "./src/app/components/picking-info/picking-info.component.ts":
/*!*******************************************************************!*\
  !*** ./src/app/components/picking-info/picking-info.component.ts ***!
  \*******************************************************************/
/*! exports provided: PickingInfoComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PickingInfoComponent", function() { return PickingInfoComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");








var PickingInfoComponent = /** @class */ (function () {
    function PickingInfoComponent(router, alertCtrl, stock, route, audio, location, loadingController) {
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.stock = stock;
        this.route = route;
        this.audio = audio;
        this.location = location;
        this.loadingController = loadingController;
    }
    PickingInfoComponent.prototype.ngOnInit = function () {
        this.active_operation = false;
        this.picking = this.route.snapshot.paramMap.get('id');
        this.get_picking_info(this.picking);
    };
    PickingInfoComponent.prototype.open_link = function (location_id) {
        this.router.navigateByUrl('/stock-location/' + location_id);
    };
    PickingInfoComponent.prototype.action_assign = function () {
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
    PickingInfoComponent.prototype.button_validate = function () {
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
    PickingInfoComponent.prototype.force_set_qty_done = function (move_id, field, model) {
        if (model === void 0) { model = 'stock.picking'; }
        return tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"](this, void 0, void 0, function () {
            var _this = this;
            return tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"](this, function (_a) {
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
    PickingInfoComponent.prototype.force_reset_qties = function (pick_id) {
        return tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"](this, void 0, void 0, function () {
            var _this = this;
            return tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"](this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.stock.force_reset_qties(Number(pick_id), 'stock.picking').then(function (lines_data) {
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
    PickingInfoComponent.prototype.presentAlert = function (titulo, texto) {
        return tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"](this, void 0, void 0, function () {
            var alert;
            return tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"](this, function (_a) {
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
    PickingInfoComponent.prototype.presentLoading = function () {
        return tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"](this, void 0, void 0, function () {
            var _a;
            return tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"](this, function (_b) {
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
    PickingInfoComponent.prototype.get_picking_info = function (picking) {
        var _this = this;
        this.stock.get_picking_info(picking).then(function (data) {
            _this.picking_data = data[0];
            _this.picking_code = data[0].code;
            _this.move_lines = _this.picking_data['move_lines'];
            _this.move_line_ids = _this.picking_data['move_line_ids'];
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperar el picking:', error);
        });
    };
    PickingInfoComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_4__["StockService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"] },
        { type: _angular_common__WEBPACK_IMPORTED_MODULE_6__["Location"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["LoadingController"] }
    ]; };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", String)
    ], PickingInfoComponent.prototype, "scanner_reading", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], PickingInfoComponent.prototype, "pick", void 0);
    PickingInfoComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-picking-info',
            template: __webpack_require__(/*! raw-loader!./picking-info.component.html */ "./node_modules/raw-loader/index.js!./src/app/components/picking-info/picking-info.component.html"),
            styles: [__webpack_require__(/*! ./picking-info.component.scss */ "./src/app/components/picking-info/picking-info.component.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_4__["StockService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"],
            _angular_common__WEBPACK_IMPORTED_MODULE_6__["Location"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["LoadingController"]])
    ], PickingInfoComponent);
    return PickingInfoComponent;
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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _stock_picking_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./stock-picking.page */ "./src/app/pages/stock-picking/stock-picking.page.ts");
/* harmony import */ var _components_picking_info_picking_info_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../components/picking-info/picking-info.component */ "./src/app/components/picking-info/picking-info.component.ts");
/* harmony import */ var _components_move_line_list_move_line_list_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../components/move-line-list/move-line-list.component */ "./src/app/components/move-line-list/move-line-list.component.ts");
/* harmony import */ var _components_move_line_details_list_move_line_details_list_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../components/move-line-details-list/move-line-details-list.component */ "./src/app/components/move-line-details-list/move-line-details-list.component.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../shared/shared.module */ "./src/app/shared/shared.module.ts");











var routes = [
    {
        path: '',
        component: _stock_picking_page__WEBPACK_IMPORTED_MODULE_6__["StockPickingPage"]
    }
];
var StockPickingPageModule = /** @class */ (function () {
    function StockPickingPageModule() {
    }
    StockPickingPageModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes),
                _shared_shared_module__WEBPACK_IMPORTED_MODULE_10__["SharedModule"]
            ],
            entryComponents: [_components_picking_info_picking_info_component__WEBPACK_IMPORTED_MODULE_7__["PickingInfoComponent"], _components_move_line_list_move_line_list_component__WEBPACK_IMPORTED_MODULE_8__["MoveLineListComponent"], _components_move_line_details_list_move_line_details_list_component__WEBPACK_IMPORTED_MODULE_9__["MoveLineDetailsListComponent"]],
            declarations: [_stock_picking_page__WEBPACK_IMPORTED_MODULE_6__["StockPickingPage"], _components_picking_info_picking_info_component__WEBPACK_IMPORTED_MODULE_7__["PickingInfoComponent"], _components_move_line_list_move_line_list_component__WEBPACK_IMPORTED_MODULE_8__["MoveLineListComponent"], _components_move_line_details_list_move_line_details_list_component__WEBPACK_IMPORTED_MODULE_9__["MoveLineDetailsListComponent"]]
        })
    ], StockPickingPageModule);
    return StockPickingPageModule;
}());



/***/ }),

/***/ "./src/app/pages/stock-picking/stock-picking.page.scss":
/*!*************************************************************!*\
  !*** ./src/app/pages/stock-picking/stock-picking.page.scss ***!
  \*************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3BhZ2VzL3N0b2NrLXBpY2tpbmcvc3RvY2stcGlja2luZy5wYWdlLnNjc3MifQ== */"

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/fesm5/ionic-storage.js");







var StockPickingPage = /** @class */ (function () {
    function StockPickingPage(odoo, router, alertCtrl, audio, storage) {
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.audio = audio;
        this.storage = storage;
        this.scanner_options = { reader: true, microphone: false, sound: false };
        this.check_scanner_values();
        this.moves = ['up', 'down', 'left', 'right'];
    }
    StockPickingPage.prototype.ngOnInit = function () {
        var _this = this;
        this.odoo.isLoggedIn().then(function (data) {
            if (data == false) {
                _this.router.navigateByUrl('/login');
            }
            _this.show_scan_form = _this.scanner_options['reader'];
            _this.audio.play('click');
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    StockPickingPage.prototype.check_scanner_values = function () {
        var _this = this;
        this.storage.get('SCANNER').then(function (val) {
            if (val) {
                _this.scanner_options = val;
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al acceder a las opciones del scanner:', error);
        });
    };
    StockPickingPage.prototype.onReadingEmitted = function (val) {
        if (this.moves.includes(val)) {
            this.page_controller(val);
        }
        else {
            console.log(this.scanner_reading);
            this.scanner_reading = val;
        }
    };
    StockPickingPage.prototype.onShowEmitted = function (val) {
        this.show_scan_form = val;
    };
    StockPickingPage.prototype.presentAlert = function (titulo, texto) {
        return tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"](this, void 0, void 0, function () {
            var alert;
            return tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"](this, function (_a) {
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
    StockPickingPage.ctorParameters = function () { return [
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"] },
        { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_6__["Storage"] }
    ]; };
    StockPickingPage = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-stock-picking',
            template: __webpack_require__(/*! raw-loader!./stock-picking.page.html */ "./node_modules/raw-loader/index.js!./src/app/pages/stock-picking/stock-picking.page.html"),
            styles: [__webpack_require__(/*! ./stock-picking.page.scss */ "./src/app/pages/stock-picking/stock-picking.page.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"],
            _ionic_storage__WEBPACK_IMPORTED_MODULE_6__["Storage"]])
    ], StockPickingPage);
    return StockPickingPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-stock-picking-stock-picking-module-es5.js.map
(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-move-form-move-form-module"],{

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/move-form/move-form.page.html":
/*!*******************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/pages/move-form/move-form.page.html ***!
  \*******************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"start\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n    <app-scanner-header slot=\"end\"></app-scanner-header>\n    <ion-title>Movimiento</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n<ion-card *ngIf=\"data\">\n\n    <ion-card-header>\n      <ion-card-title class=\"ion-text-center\">{{data.display_name}}</ion-card-title>\n    </ion-card-header>\n  \n    <ion-card-content class=\"ion-text-center\">\n      <div class=\"product_img\" class=\"ion-text-center\">\n        <ion-img *ngIf=\"data.base64\" src=\"data:image/jpeg;base64,{{ data['image'] }}\" ></ion-img>\n        <ion-img *ngIf=\"!data.base64\" src=\"{{ data['image'] }}\"></ion-img>\n      </div>\n      <div><strong>Pick: </strong>{{data.picking_id['id'] && data.picking_id['display_name']}}</div>\n      <div><strong>Referencia: </strong>{{data.default_code}}</div>\n      <div><strong>{{data.location_id['display_name']}} >> {{data.location_dest_id['display_name']}}</strong></div>\n      <!-- <div [ngSwitch]=\"data.tracking\">\n        <strong *ngSwitchCase=\"'none'\">Sin tracking</strong>\n        <strong *ngSwitchCase=\"'lot'\">Por lotes</strong>\n        <strong *ngSwitchCase=\"'serial'\">Por serie</strong>\n      </div> -->\n      <ion-row *ngIf=\"data.state != 'cancel' && data.state != 'done' && data.tracking=='none'\">\n        <ion-col>\n           <ion-badge class=\"link\" (click)=\"changeqty(-1)\"> - </ion-badge>\n        </ion-col>\n        <ion-col class=\"link\" (click)=\"changeqty(0)\"><strong>Cantidad: </strong><br/>\n          <ion-badge class=\"primary\"> {{data.quantity_done}} de {{data.product_uom_qty}} </ion-badge> \n        </ion-col>\n        <ion-col>\n          <ion-badge class=\"link\" (click)=\"changeqty(+1)\"> + </ion-badge>\n        </ion-col>\n      </ion-row>\n\n      <div *ngIf=\"data.state != 'cancel' && data.state != 'done' && data.tracking !='none'\">\n        <div>\n          <ion-badge class=\"primary\"> {{data.quantity_done}} de {{data.product_uom_qty}} </ion-badge> \n        </div>\n        <strong>Lotes/Serie:</strong>\n        <div *ngFor=\"let lot of data.lot_ids\">\n          {{lot.name}}\n        </div>\n      </div>\n\n      <div *ngIf=\"new_lots\">\n        <strong>Añadiendo:</strong>\n        <div *ngFor=\"let lot of new_lots\">\n          {{lot[0]}}\n        </div>\n      </div>\n\n      <ion-row>\n        <ion-col class=\"link\" (click)=\"get_move_info(data.id, -1)\">Anterior\n        </ion-col>\n        <!-- <ion-col *ngIf=\"data.ready_to_validate\" class=\"link\" (click)=\"button_validate(data.picking_id.id)\">Validar\n        </ion-col> -->\n        <ion-col class=\"link\" (click)=\"action_confirm()\">Confirmar\n        </ion-col>\n        <ion-col class=\"link\" (click)=\"get_move_info(data.id, +1)\">Siguiente\n        </ion-col>\n      </ion-row>\n    </ion-card-content>\n  \n  </ion-card>\n</ion-content>\n\n<app-scanner-footer (scanner_reading_changed)=\"onReadingEmitted($event)\" [scanner_reading]=\"scanner_reading\"></app-scanner-footer>\n\n<ng-template #lineDoneTemplate>\n  <ion-col><strong>Cantidad: </strong><br/>\n    <ion-badge class=\"secondary\"> {{data.quantity_done}} de {{data.product_uom_qty}} </ion-badge>\n  </ion-col>\n</ng-template>");

/***/ }),

/***/ "./src/app/pages/move-form/move-form.module.ts":
/*!*****************************************************!*\
  !*** ./src/app/pages/move-form/move-form.module.ts ***!
  \*****************************************************/
/*! exports provided: MoveFormPageModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MoveFormPageModule", function() { return MoveFormPageModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _move_form_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./move-form.page */ "./src/app/pages/move-form/move-form.page.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../shared/shared.module */ "./src/app/shared/shared.module.ts");








var routes = [
    {
        path: '',
        component: _move_form_page__WEBPACK_IMPORTED_MODULE_6__["MoveFormPage"]
    }
];
var MoveFormPageModule = /** @class */ (function () {
    function MoveFormPageModule() {
    }
    MoveFormPageModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes),
                _shared_shared_module__WEBPACK_IMPORTED_MODULE_7__["SharedModule"]
            ],
            declarations: [_move_form_page__WEBPACK_IMPORTED_MODULE_6__["MoveFormPage"]]
        })
    ], MoveFormPageModule);
    return MoveFormPageModule;
}());



/***/ }),

/***/ "./src/app/pages/move-form/move-form.page.scss":
/*!*****************************************************!*\
  !*** ./src/app/pages/move-form/move-form.page.scss ***!
  \*****************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("ion-img {\n  max-width: 100px;\n  max-height: 100px;\n  margin-left: auto;\n  margin-right: auto;\n  width: 100px;\n}\n\n.link {\n  cursor: pointer;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL3BhZ2VzL21vdmUtZm9ybS9tb3ZlLWZvcm0ucGFnZS5zY3NzIiwic3JjL2FwcC9wYWdlcy9tb3ZlLWZvcm0vbW92ZS1mb3JtLnBhZ2Uuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNJLGdCQUFBO0VBQ0EsaUJBQUE7RUFDQSxpQkFBQTtFQUNBLGtCQUFBO0VBQ0EsWUFBQTtBQ0NKOztBREVBO0VBQ0ksZUFBQTtBQ0NKIiwiZmlsZSI6InNyYy9hcHAvcGFnZXMvbW92ZS1mb3JtL21vdmUtZm9ybS5wYWdlLnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJpb24taW1nIHtcbiAgICBtYXgtd2lkdGg6IDEwMHB4O1xuICAgIG1heC1oZWlnaHQ6IDEwMHB4O1xuICAgIG1hcmdpbi1sZWZ0OiBhdXRvO1xuICAgIG1hcmdpbi1yaWdodDogYXV0bztcbiAgICB3aWR0aDogMTAwcHg7XG59XG5cbi5saW5re1xuICAgIGN1cnNvcjogcG9pbnRlcjtcbn0iLCJpb24taW1nIHtcbiAgbWF4LXdpZHRoOiAxMDBweDtcbiAgbWF4LWhlaWdodDogMTAwcHg7XG4gIG1hcmdpbi1sZWZ0OiBhdXRvO1xuICBtYXJnaW4tcmlnaHQ6IGF1dG87XG4gIHdpZHRoOiAxMDBweDtcbn1cblxuLmxpbmsge1xuICBjdXJzb3I6IHBvaW50ZXI7XG59Il19 */");

/***/ }),

/***/ "./src/app/pages/move-form/move-form.page.ts":
/*!***************************************************!*\
  !*** ./src/app/pages/move-form/move-form.page.ts ***!
  \***************************************************/
/*! exports provided: MoveFormPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MoveFormPage", function() { return MoveFormPage; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/__ivy_ngcc__/fesm5/ionic-storage.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");










var MoveFormPage = /** @class */ (function () {
    function MoveFormPage(odoo, router, alertCtrl, route, audio, stock, storage, location, loadingController) {
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.route = route;
        this.audio = audio;
        this.stock = stock;
        this.storage = storage;
        this.location = location;
        this.loadingController = loadingController;
        this.moves = ['up', 'down', 'left', 'right'];
    }
    MoveFormPage.prototype.ngOnInit = function () {
        var _this = this;
        this.odoo.isLoggedIn().then(function (data) {
            if (data === false) {
                _this.router.navigateByUrl('/login');
            }
            else {
                _this.storage.get('CONEXION').then(function (con) {
                    _this.placeholder = con.url + '/web/static/src/img/placeholder.png';
                })
                    .catch(function (error) {
                    _this.presentAlert('Error al comprobar tu sesión:', error);
                });
                var move = +_this.route.snapshot.paramMap.get('id');
                _this.get_move_info(move);
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    MoveFormPage.prototype.onReadingEmitted = function (val) {
        if (this.moves.includes(val)) {
            this.page_controller(val);
        }
        else {
            this.scanner_reading = val;
            this.process_reading();
        }
    };
    // Navigation 
    MoveFormPage.prototype.page_controller = function (direction) {
        if (direction == 'up') {
            console.log("up");
            this.router.navigateByUrl('/stock-picking/' + this.data['picking_id']['id'] + '/' + this.data['picking_id']['code']);
        }
        else if (direction == 'down') {
            console.log("down");
            if (this.data['ready_to_validate']) {
                this.button_validate(this.data['picking_id']['id']);
            }
            else {
                this.action_confirm();
            }
        }
        else if (direction == 'left') {
            console.log("left");
            this.get_move_info(this.data['id'], -1);
        }
        else if (direction == 'right') {
            console.log("right");
            this.get_move_info(this.data['id'], +1);
        }
    };
    MoveFormPage.prototype.presentAlert = function (titulo, texto) {
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
    MoveFormPage.prototype.changeqty = function (qty) {
        if (qty == 0) {
            this.data['quantity_done'] = this.data['product_uom_qty'];
        }
        else {
            this.data['quantity_done'] += qty;
        }
    };
    MoveFormPage.prototype.get_move_info = function (move, index) {
        var _this = this;
        if (index === void 0) { index = 0; }
        this.stock.get_move_info(move, index).then(function (data) {
            _this.new_lots = false;
            console.log(data);
            if (data['image'] == false) {
                data['base64'] = false;
                data['image'] = _this.placeholder;
            }
            else {
                data['base64'] = true;
            }
            _this.data = data;
            console.log(_this.data);
            _this.audio.play('click');
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperar el movimiento:', error);
        });
    };
    MoveFormPage.prototype.action_confirm = function () {
        var _this = this;
        if (this.data['tracking'] == 'none') {
            this.stock.set_move_qty_done_from_apk(this.data['id'], this.data['quantity_done']).then(function (lines_data) {
                console.log(lines_data);
                _this.get_move_info(_this.data['id'], +1);
            })
                .catch(function (error) {
                _this.presentAlert('Error al validar el albarán:', error);
            });
        }
        else if (this.data['tracking'] != 'none' && this.new_lots) {
            this.update_lots();
        }
    };
    MoveFormPage.prototype.button_validate = function (picking_id) {
        var _this = this;
        this.presentLoading();
        this.stock.button_validate(Number(picking_id)).then(function (lines_data) {
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
    MoveFormPage.prototype.presentLoading = function () {
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
    MoveFormPage.prototype.update_lots = function () {
        var _this = this;
        this.stock.set_lot_ids_apk(this.data['id'], this.new_lots).then(function (lines_data) {
            _this.get_move_info(_this.data['id']);
        })
            .catch(function (error) {
            _this.presentAlert('Error al validar el albarán:', error);
        });
    };
    MoveFormPage.prototype.process_reading = function () {
        if (this.data['tracking'] == 'none' && Number(this.scanner_reading)) {
            this.data['quantity_done'] = Number(this.scanner_reading);
        }
        else if (this.data['tracking'] != 'none') {
            if (!this.new_lots) {
                this.new_lots = new Array();
            }
            this.new_lots.push([this.scanner_reading, 1]); /* Editar más adelante, serial cantidad = 1, lot cantidad = a introducir */
            /* Provisional, cuando estén preparada la función para gestionar cantidades en lot_ids editar */
            /* if (this.data['tracking'] == 'serial') { */
            if (this.data['tracking'] == 'serial' || this.data['tracking'] == 'lot') {
                this.data['quantity_done']++;
            }
        }
    };
    MoveFormPage.ctorParameters = function () { return [
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_5__["OdooService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_6__["AudioService"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_7__["StockService"] },
        { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_3__["Storage"] },
        { type: _angular_common__WEBPACK_IMPORTED_MODULE_8__["Location"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["LoadingController"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", String)
    ], MoveFormPage.prototype, "scanner_reading", void 0);
    MoveFormPage = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-move-form',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./move-form.page.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/move-form/move-form.page.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./move-form.page.scss */ "./src/app/pages/move-form/move-form.page.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_5__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_6__["AudioService"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_7__["StockService"],
            _ionic_storage__WEBPACK_IMPORTED_MODULE_3__["Storage"],
            _angular_common__WEBPACK_IMPORTED_MODULE_8__["Location"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["LoadingController"]])
    ], MoveFormPage);
    return MoveFormPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-move-form-move-form-module.js.map
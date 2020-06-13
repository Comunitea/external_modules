(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-stock-location-stock-location-module"],{

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-location/stock-location.page.html":
/*!*****************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-location/stock-location.page.html ***!
  \*****************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"start\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n    <app-scanner-header [disabled_reader]=\"true\" slot=\"end\"></app-scanner-header>\n    <ion-title>Detalles de la ubicación</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <ion-card *ngIf=\"location_data\">\n\n    <ion-card-header>\n      <ion-card-title>{{location_data.display_name}}</ion-card-title>\n    </ion-card-header>\n  \n    <ion-card-content>\n      <div *ngIf=\"location_data.company_id[1]\"><strong>Compañía: </strong>{{location_data.company_id[1]}}</div>\n      <div [ngSwitch]=\"location_data.usage\">\n        <strong>Tipo: </strong>\n        <!-- <ion-text *ngSwitchCase=\"'supplier'\">Ubicación de proveedor</ion-text> -->\n        <ion-text *ngSwitchCase=\"'view'\">Ver</ion-text>\n        <ion-text *ngSwitchCase=\"'internal'\">Ubicación interna</ion-text>\n        <!-- <ion-text *ngSwitchCase=\"'customer'\">Ubicación de cliente</ion-text>\n        <ion-text *ngSwitchCase=\"'inventory'\">Ubicación de inventario</ion-text>\n        <ion-text *ngSwitchCase=\"'procurement'\">Abastecimiento</ion-text> -->\n        <ion-text *ngSwitchCase=\"'production'\">Producción</ion-text>\n        <ion-text *ngSwitchCase=\"'transit'\">Ubicación de tránsito</ion-text>\n      </div>\n      <ion-row>\n        <ion-col>\n          <ion-button (click)=\"open_link('stock', location_data.id)\" expand=\"block\">Stock actual</ion-button>\n        </ion-col>\n        <ion-col>\n          <ion-button (click)=\"open_link('product', location_data.id)\" expand=\"block\">Productos</ion-button>\n          </ion-col>\n      </ion-row>\n    </ion-card-content>\n  \n  </ion-card>\n</ion-content>");

/***/ }),

/***/ "./src/app/pages/stock-location/stock-location.module.ts":
/*!***************************************************************!*\
  !*** ./src/app/pages/stock-location/stock-location.module.ts ***!
  \***************************************************************/
/*! exports provided: StockLocationPageModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockLocationPageModule", function() { return StockLocationPageModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _stock_location_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./stock-location.page */ "./src/app/pages/stock-location/stock-location.page.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../shared/shared.module */ "./src/app/shared/shared.module.ts");








var routes = [
    {
        path: '',
        component: _stock_location_page__WEBPACK_IMPORTED_MODULE_6__["StockLocationPage"]
    }
];
var StockLocationPageModule = /** @class */ (function () {
    function StockLocationPageModule() {
    }
    StockLocationPageModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes),
                _shared_shared_module__WEBPACK_IMPORTED_MODULE_7__["SharedModule"]
            ],
            entryComponents: [],
            declarations: [_stock_location_page__WEBPACK_IMPORTED_MODULE_6__["StockLocationPage"]]
        })
    ], StockLocationPageModule);
    return StockLocationPageModule;
}());



/***/ }),

/***/ "./src/app/pages/stock-location/stock-location.page.scss":
/*!***************************************************************!*\
  !*** ./src/app/pages/stock-location/stock-location.page.scss ***!
  \***************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("ion-col {\n  cursor: pointer;\n}\nion-col.success {\n  color: var(--ion-color-success);\n}\nion-col.danger {\n  color: var(--ion-color-danger);\n}\nion-col.primary {\n  color: var(--ion-color-primary);\n}\nion-col.secondary {\n  color: var(--ion-color-secondary);\n}\nion-col.tertiary {\n  color: var(--ion-color-tertiary);\n}\nion-col.medium {\n  color: var(--ion-color-medium);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL3BhZ2VzL3N0b2NrLWxvY2F0aW9uL3N0b2NrLWxvY2F0aW9uLnBhZ2Uuc2NzcyIsInNyYy9hcHAvcGFnZXMvc3RvY2stbG9jYXRpb24vc3RvY2stbG9jYXRpb24ucGFnZS5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBbUJJLGVBQUE7QUNqQko7QURESTtFQUNJLCtCQUFBO0FDR1I7QURESTtFQUNJLDhCQUFBO0FDR1I7QURESTtFQUNJLCtCQUFBO0FDR1I7QURESTtFQUNJLGlDQUFBO0FDR1I7QURESTtFQUNJLGdDQUFBO0FDR1I7QURESTtFQUNJLDhCQUFBO0FDR1IiLCJmaWxlIjoic3JjL2FwcC9wYWdlcy9zdG9jay1sb2NhdGlvbi9zdG9jay1sb2NhdGlvbi5wYWdlLnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJpb24tY29sIHtcbiAgICAmLnN1Y2Nlc3Mge1xuICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXN1Y2Nlc3MpO1xuICAgIH1cbiAgICAmLmRhbmdlciB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItZGFuZ2VyKTtcbiAgICB9XG4gICAgJi5wcmltYXJ5IHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1wcmltYXJ5KTtcbiAgICB9XG4gICAgJi5zZWNvbmRhcnkge1xuICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXNlY29uZGFyeSk7XG4gICAgfVxuICAgICYudGVydGlhcnkge1xuICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXRlcnRpYXJ5KTtcbiAgICB9XG4gICAgJi5tZWRpdW0ge1xuICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLW1lZGl1bSk7XG4gICAgfVxuICAgIGN1cnNvcjogcG9pbnRlcjtcbn0iLCJpb24tY29sIHtcbiAgY3Vyc29yOiBwb2ludGVyO1xufVxuaW9uLWNvbC5zdWNjZXNzIHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zdWNjZXNzKTtcbn1cbmlvbi1jb2wuZGFuZ2VyIHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1kYW5nZXIpO1xufVxuaW9uLWNvbC5wcmltYXJ5IHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1wcmltYXJ5KTtcbn1cbmlvbi1jb2wuc2Vjb25kYXJ5IHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zZWNvbmRhcnkpO1xufVxuaW9uLWNvbC50ZXJ0aWFyeSB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItdGVydGlhcnkpO1xufVxuaW9uLWNvbC5tZWRpdW0ge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLW1lZGl1bSk7XG59Il19 */");

/***/ }),

/***/ "./src/app/pages/stock-location/stock-location.page.ts":
/*!*************************************************************!*\
  !*** ./src/app/pages/stock-location/stock-location.page.ts ***!
  \*************************************************************/
/*! exports provided: StockLocationPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockLocationPage", function() { return StockLocationPage; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");
/* harmony import */ var _services_voice_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../services/voice.service */ "./src/app/services/voice.service.ts");








var StockLocationPage = /** @class */ (function () {
    function StockLocationPage(odoo, router, alertCtrl, route, audio, stock, voice) {
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.route = route;
        this.audio = audio;
        this.stock = stock;
        this.voice = voice;
    }
    StockLocationPage.prototype.ngOnInit = function () {
        var _this = this;
        this.odoo.isLoggedIn().then(function (data) {
            if (data == false) {
                _this.router.navigateByUrl('/login');
            }
            else {
                var location = _this.route.snapshot.paramMap.get('id');
                _this.voice.voice_command_refresh$.subscribe(function (data) {
                    _this.voice_command_check();
                });
                _this.get_location_info(location);
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    StockLocationPage.prototype.presentAlert = function (titulo, texto) {
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
    StockLocationPage.prototype.get_location_info = function (location) {
        var _this = this;
        this.stock.get_location_info(location).then(function (data) {
            _this.location_data = data[0];
            _this.audio.play('click');
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperar el location:', error);
        });
    };
    StockLocationPage.prototype.open_link = function (type, location_id) {
        if (type == 'stock') {
            this.router.navigateByUrl('/stock-quant-list/' + location_id);
        }
        else {
            this.router.navigateByUrl('/stock-location-product-list/' + location_id);
        }
    };
    // Voice command
    StockLocationPage.prototype.voice_command_check = function () {
        console.log("voice_command_check");
        console.log(this.voice.voice_command);
        if (this.voice.voice_command) {
            var voice_command_register = this.voice.voice_command;
            console.log("Recibida orden de voz: " + voice_command_register);
            if (this.check_if_value_in_responses("stock", voice_command_register)) {
                console.log("Stock");
                this.router.navigateByUrl('/stock-quant-list/' + this.location['id']);
            }
            else if (this.check_if_value_in_responses("productos", voice_command_register)) {
                console.log("Productos");
                this.router.navigateByUrl('/stock-location-product-list/' + this.location['id']);
            }
        }
    };
    StockLocationPage.prototype.check_if_value_in_responses = function (value, dict) {
        if (value == dict[0] || value == dict[1] || value == dict[2]) {
            return true;
        }
        else {
            return false;
        }
    };
    StockLocationPage.ctorParameters = function () { return [
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"] },
        { type: _services_voice_service__WEBPACK_IMPORTED_MODULE_7__["VoiceService"] }
    ]; };
    StockLocationPage = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-stock-location',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./stock-location.page.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-location/stock-location.page.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./stock-location.page.scss */ "./src/app/pages/stock-location/stock-location.page.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"],
            _services_voice_service__WEBPACK_IMPORTED_MODULE_7__["VoiceService"]])
    ], StockLocationPage);
    return StockLocationPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-stock-location-stock-location-module.js.map
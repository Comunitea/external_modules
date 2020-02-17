(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-stock-location-product-list-stock-location-product-list-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/components/location-product-list/location-product-list.component.html":
/*!*****************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/components/location-product-list/location-product-list.component.html ***!
  \*****************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-grid>\n  \n  <ion-row>\n    <ion-col size=\"3\">\n        <div><strong>Referencia</strong></div>\n    </ion-col>\n    \n    <ion-col size=\"7\">\n        <div><strong>Nombre</strong></div>\n    </ion-col>\n\n    <!--ion-col size=\"1\">\n      <div><strong>Precio de venta</strong></div>\n    </ion-col>\n\n    <ion-col size=\"1\">\n      <div><strong>Último precio de compra</strong></div>\n    </ion-col-->\n\n    <ion-col size=\"2\">\n      <div><strong>Stock</strong></div>\n    </ion-col>\n\n    <!--ion-col size=\"1\">\n      <div><strong>Pronóstico</strong></div>\n    </ion-col>\n\n    <ion-col size=\"1\">\n      <div><strong>Unidad</strong></div>\n    </ion-col>\n\n    <ion-col size=\"2\">\n      <div><strong>Código</strong></div>\n    </ion-col-->\n  </ion-row>\n\n  <ion-row *ngFor=\"let product of products\" (click)=\"open_link(product.id)\" >\n    <ion-col size=\"3\">\n      <div style='font-size: xx-small'>{{product.default_code}}</div>\n    </ion-col>\n      <ion-col size=\"7\">\n      <div style='font-size: xx-small'>{{product.name}}</div>\n    </ion-col>\n  \n    <!--ion-col size=\"1\">\n      <div>{{product.lst_price}}</div>\n    </ion-col>\n  \n    <ion-col size=\"1\">\n      <div>{{product.last_purchase_price}}</div>\n    </ion-col-->\n  \n    <ion-col size=\"2\">\n      <div [ngClass]=\"{'danger': product.qty_available &lt;= 0}\" style='font-size: x-small' >{{product.qty_available}}</div>\n    </ion-col>\n  \n    <!--ion-col size=\"1\">\n      <div [ngClass]=\"{'danger': product.virtual_available &lt;= 0}\">{{product.virtual_available}}</div>\n    </ion-col>\n  \n    <ion-col size=\"1\">\n      <div>{{product.uom_id[1]}}</div>\n    </ion-col>\n  \n    <ion-col size=\"2\">\n      <div>{{product.barcode}}</div>\n    </ion-col-->\n  </ion-row>\n</ion-grid>"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/pages/stock-location-product-list/stock-location-product-list.page.html":
/*!*******************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/pages/stock-location-product-list/stock-location-product-list.page.html ***!
  \*******************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"start\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n    <app-scanner-header slot=\"end\" (show_scan_form_changed)=\"onShowEmitted($event)\" [show_scan_form]=show_scan_form></app-scanner-header>\n    <ion-title>Productos</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <ion-card>\n    <ion-card-content>\n      <ion-row>\n        <ion-toolbar>\n          <ion-searchbar type=\"text\" (ionInput)=\"get_search_results($event)\" autocomplete=\"on\" showCancelButton=\"always\"></ion-searchbar>\n        </ion-toolbar>\n      </ion-row>\n\n      <app-location-product-list [products]=\"products\"></app-location-product-list>\n\n      <ion-infinite-scroll threshold=\"100px\" (ionInfinite)=\"loadData($event)\">\n        <ion-infinite-scroll-content\n          loadingSpinner=\"bubbles\"\n          loadingText=\"Cargando más productos...\">\n        </ion-infinite-scroll-content>\n      </ion-infinite-scroll>\n    </ion-card-content>\n  </ion-card>\n</ion-content>\n\n<app-scanner-footer (scanner_reading_changed)=\"onReadingEmitted($event)\" [show_scan_form]=show_scan_form [scanner_reading]=\"scanner_reading\"></app-scanner-footer>"

/***/ }),

/***/ "./src/app/components/location-product-list/location-product-list.component.scss":
/*!***************************************************************************************!*\
  !*** ./src/app/components/location-product-list/location-product-list.component.scss ***!
  \***************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "div.danger {\n  color: var(--ion-color-danger);\n}\ndiv.product_link {\n  color: blue;\n  text-decoration: underline;\n  -webkit-text-decoration-color: blue;\n          text-decoration-color: blue;\n  cursor: pointer;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9jb21wb25lbnRzL2xvY2F0aW9uLXByb2R1Y3QtbGlzdC9sb2NhdGlvbi1wcm9kdWN0LWxpc3QuY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL2NvbXBvbmVudHMvbG9jYXRpb24tcHJvZHVjdC1saXN0L2xvY2F0aW9uLXByb2R1Y3QtbGlzdC5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFDSTtFQUNJLDhCQUFBO0FDQVI7QURFSTtFQUNJLFdBQUE7RUFDQSwwQkFBQTtFQUNBLG1DQUFBO1VBQUEsMkJBQUE7RUFDQSxlQUFBO0FDQVIiLCJmaWxlIjoic3JjL2FwcC9jb21wb25lbnRzL2xvY2F0aW9uLXByb2R1Y3QtbGlzdC9sb2NhdGlvbi1wcm9kdWN0LWxpc3QuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJkaXYge1xuICAgICYuZGFuZ2VyIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1kYW5nZXIpO1xuICAgIH1cbiAgICAmLnByb2R1Y3RfbGluayB7XG4gICAgICAgIGNvbG9yOiBibHVlO1xuICAgICAgICB0ZXh0LWRlY29yYXRpb246IHVuZGVybGluZTtcbiAgICAgICAgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBibHVlO1xuICAgICAgICBjdXJzb3I6IHBvaW50ZXI7XG4gICAgfVxufSIsImRpdi5kYW5nZXIge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLWRhbmdlcik7XG59XG5kaXYucHJvZHVjdF9saW5rIHtcbiAgY29sb3I6IGJsdWU7XG4gIHRleHQtZGVjb3JhdGlvbjogdW5kZXJsaW5lO1xuICB0ZXh0LWRlY29yYXRpb24tY29sb3I6IGJsdWU7XG4gIGN1cnNvcjogcG9pbnRlcjtcbn0iXX0= */"

/***/ }),

/***/ "./src/app/components/location-product-list/location-product-list.component.ts":
/*!*************************************************************************************!*\
  !*** ./src/app/components/location-product-list/location-product-list.component.ts ***!
  \*************************************************************************************/
/*! exports provided: LocationProductListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LocationProductListComponent", function() { return LocationProductListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");



var LocationProductListComponent = /** @class */ (function () {
    function LocationProductListComponent(router) {
        this.router = router;
    }
    LocationProductListComponent.prototype.ngOnInit = function () { };
    LocationProductListComponent.prototype.open_link = function (product_id) {
        this.router.navigateByUrl('/product/' + product_id);
    };
    LocationProductListComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] }
    ]; };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], LocationProductListComponent.prototype, "products", void 0);
    LocationProductListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-location-product-list',
            template: __webpack_require__(/*! raw-loader!./location-product-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/components/location-product-list/location-product-list.component.html"),
            styles: [__webpack_require__(/*! ./location-product-list.component.scss */ "./src/app/components/location-product-list/location-product-list.component.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]])
    ], LocationProductListComponent);
    return LocationProductListComponent;
}());



/***/ }),

/***/ "./src/app/pages/stock-location-product-list/stock-location-product-list.module.ts":
/*!*****************************************************************************************!*\
  !*** ./src/app/pages/stock-location-product-list/stock-location-product-list.module.ts ***!
  \*****************************************************************************************/
/*! exports provided: StockLocationProductListPageModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockLocationProductListPageModule", function() { return StockLocationProductListPageModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _stock_location_product_list_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./stock-location-product-list.page */ "./src/app/pages/stock-location-product-list/stock-location-product-list.page.ts");
/* harmony import */ var _components_location_product_list_location_product_list_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../components/location-product-list/location-product-list.component */ "./src/app/components/location-product-list/location-product-list.component.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../shared/shared.module */ "./src/app/shared/shared.module.ts");









var routes = [
    {
        path: '',
        component: _stock_location_product_list_page__WEBPACK_IMPORTED_MODULE_6__["StockLocationProductListPage"]
    }
];
var StockLocationProductListPageModule = /** @class */ (function () {
    function StockLocationProductListPageModule() {
    }
    StockLocationProductListPageModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes),
                _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__["SharedModule"]
            ],
            entryComponents: [_components_location_product_list_location_product_list_component__WEBPACK_IMPORTED_MODULE_7__["LocationProductListComponent"]],
            declarations: [_stock_location_product_list_page__WEBPACK_IMPORTED_MODULE_6__["StockLocationProductListPage"], _components_location_product_list_location_product_list_component__WEBPACK_IMPORTED_MODULE_7__["LocationProductListComponent"]]
        })
    ], StockLocationProductListPageModule);
    return StockLocationProductListPageModule;
}());



/***/ }),

/***/ "./src/app/pages/stock-location-product-list/stock-location-product-list.page.scss":
/*!*****************************************************************************************!*\
  !*** ./src/app/pages/stock-location-product-list/stock-location-product-list.page.scss ***!
  \*****************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3BhZ2VzL3N0b2NrLWxvY2F0aW9uLXByb2R1Y3QtbGlzdC9zdG9jay1sb2NhdGlvbi1wcm9kdWN0LWxpc3QucGFnZS5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/pages/stock-location-product-list/stock-location-product-list.page.ts":
/*!***************************************************************************************!*\
  !*** ./src/app/pages/stock-location-product-list/stock-location-product-list.page.ts ***!
  \***************************************************************************************/
/*! exports provided: StockLocationProductListPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockLocationProductListPage", function() { return StockLocationProductListPage; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/fesm5/ionic-storage.js");








var StockLocationProductListPage = /** @class */ (function () {
    function StockLocationProductListPage(odoo, router, alertCtrl, route, audio, stock, storage) {
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.route = route;
        this.audio = audio;
        this.stock = stock;
        this.storage = storage;
        this.scanner_options = { reader: true, microphone: false, sound: false };
        this.check_scanner_values();
        this.offset = 0;
        this.limit = 25;
        this.limit_reached = false;
    }
    StockLocationProductListPage.prototype.ngOnInit = function () {
        var _this = this;
        this.odoo.isLoggedIn().then(function (data) {
            if (data == false) {
                _this.router.navigateByUrl('/login');
            }
            else {
                _this.location = _this.route.snapshot.paramMap.get('id');
                _this.get_location_products();
                _this.show_scan_form = _this.scanner_options['reader'];
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    StockLocationProductListPage.prototype.check_scanner_values = function () {
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
    StockLocationProductListPage.prototype.onReadingEmitted = function (val) {
        this.scanner_reading = val;
        this.search = val;
        this.get_location_products(this.search);
    };
    StockLocationProductListPage.prototype.onShowEmitted = function (val) {
        this.show_scan_form = val;
    };
    StockLocationProductListPage.prototype.presentAlert = function (titulo, texto) {
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
    StockLocationProductListPage.prototype.get_location_products = function (search) {
        var _this = this;
        if (search === void 0) { search = null; }
        this.offset = 0;
        this.limit_reached = false;
        this.stock.get_location_products(this.location, this.offset, this.limit, search).then(function (products_lists) {
            _this.products = products_lists;
            if (Object.keys(products_lists).length < 25) {
                _this.limit_reached = true;
            }
            if (Object.keys(_this.products).length == 1) {
                _this.router.navigateByUrl('/product/' + _this.products[0]['id']);
            }
            _this.audio.play('click');
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperador el listado de productos:', error);
        });
    };
    StockLocationProductListPage.prototype.get_search_results = function (ev) {
        this.search = ev.target.value;
        this.get_location_products(this.search);
    };
    // Infinitescroll
    StockLocationProductListPage.prototype.loadData = function (event) {
        var _this = this;
        setTimeout(function () {
            console.log('Loading more locations');
            event.target.complete();
            _this.product_list_infinite_scroll_add();
            // App logic to determine if all data is loaded
            // and disable the infinite scroll
            if (_this.limit_reached) {
                event.target.disabled = true;
            }
        }, 500);
    };
    StockLocationProductListPage.prototype.product_list_infinite_scroll_add = function () {
        var _this = this;
        this.offset += this.limit;
        this.stock.get_location_products(this.location, this.offset, this.limit, this.search).then(function (data) {
            var current_length = Object.keys(_this.products).length;
            if (Object.keys(data).length < 25) {
                _this.limit_reached = true;
            }
            for (var k in data)
                _this.products[current_length + Number(k)] = data[k];
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperador el listado de productos:', error);
        });
    };
    StockLocationProductListPage.prototype.toggleInfiniteScroll = function () {
        this.infiniteScroll.disabled = !this.infiniteScroll.disabled;
    };
    StockLocationProductListPage.ctorParameters = function () { return [
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"] },
        { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_7__["Storage"] }
    ]; };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])(_ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"], { static: false }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"])
    ], StockLocationProductListPage.prototype, "infiniteScroll", void 0);
    StockLocationProductListPage = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-stock-location-product-list',
            template: __webpack_require__(/*! raw-loader!./stock-location-product-list.page.html */ "./node_modules/raw-loader/index.js!./src/app/pages/stock-location-product-list/stock-location-product-list.page.html"),
            styles: [__webpack_require__(/*! ./stock-location-product-list.page.scss */ "./src/app/pages/stock-location-product-list/stock-location-product-list.page.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"],
            _ionic_storage__WEBPACK_IMPORTED_MODULE_7__["Storage"]])
    ], StockLocationProductListPage);
    return StockLocationProductListPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-stock-location-product-list-stock-location-product-list-module-es5.js.map
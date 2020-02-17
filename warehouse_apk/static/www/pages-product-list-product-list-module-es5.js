(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-product-list-product-list-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/components/product-list-info/product-list-info.component.html":
/*!*********************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/components/product-list-info/product-list-info.component.html ***!
  \*********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-grid>\n  <ion-row>\n    <ion-col size=\"7\">\n        <div><strong>Nombre</strong></div>\n    </ion-col>\n    \n    <ion-col size=\"2\">\n        <div><strong>Código</strong></div>\n    </ion-col>\n\n    <ion-col size=\"1\">\n      <div><strong>Disponible</strong></div>\n    </ion-col>\n    \n    <ion-col size=\"1\">\n      <div><strong>Previsto</strong></div>\n    </ion-col>\n    <ion-col size=\"1\">\n      <div><strong>Precio de venta</strong></div>\n    </ion-col>\n  </ion-row>\n\n  <ion-row *ngFor=\"let product of products\">\n      <ion-col size=\"7\">\n          <div class=\"product_link\" (click)=\"open_link(product.id)\">{{product.name}}</div>\n      </ion-col>\n      \n      <ion-col size=\"2\">\n          <div>{{product.default_code}}</div>\n      </ion-col>\n    \n      <ion-col size=\"1\">\n        <div [ngClass]=\"{'danger': product.qty_available &lt;= 0}\" >{{product.qty_available}}</div>\n      </ion-col>\n      \n      <ion-col size=\"1\">\n        <div [ngClass]=\"{'danger': product.virtual_available &lt;= 0}\">{{product.virtual_available}}</div>\n      </ion-col>\n    \n      <ion-col size=\"1\">\n          <div>{{product.list_price}}€</div>\n      </ion-col>\n    </ion-row>\n</ion-grid>"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/pages/product-list/product-list.page.html":
/*!*************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/pages/product-list/product-list.page.html ***!
  \*************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"start\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n    <app-scanner-header slot=\"end\" (show_scan_form_changed)=\"onShowEmitted($event)\" [show_scan_form]=show_scan_form></app-scanner-header>\n    <ion-title>Listado de productos</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <ion-card-content>\n    <ion-row>\n      <ion-toolbar>\n        <ion-searchbar type=\"text\" (ionInput)=\"get_search_results($event)\" autocomplete=\"on\" showCancelButton=\"always\"></ion-searchbar>\n      </ion-toolbar>\n    </ion-row>\n\n    <app-product-list-info [products]=\"product_list\"></app-product-list-info>\n    \n    <ion-infinite-scroll threshold=\"100px\" (ionInfinite)=\"loadData($event)\">\n      <ion-infinite-scroll-content\n        loadingSpinner=\"bubbles\"\n        loadingText=\"Cargando más productos...\">\n      </ion-infinite-scroll-content>\n    </ion-infinite-scroll>\n  </ion-card-content>\n</ion-content>\n\n<app-scanner-footer (scanner_reading_changed)=\"onReadingEmitted($event)\" [show_scan_form]=show_scan_form [scanner_reading]=\"scanner_reading\"></app-scanner-footer>"

/***/ }),

/***/ "./src/app/components/product-list-info/product-list-info.component.scss":
/*!*******************************************************************************!*\
  !*** ./src/app/components/product-list-info/product-list-info.component.scss ***!
  \*******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "div.danger {\n  color: var(--ion-color-danger);\n}\ndiv.product_link {\n  color: blue;\n  text-decoration: underline;\n  -webkit-text-decoration-color: blue;\n          text-decoration-color: blue;\n  cursor: pointer;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9jb21wb25lbnRzL3Byb2R1Y3QtbGlzdC1pbmZvL3Byb2R1Y3QtbGlzdC1pbmZvLmNvbXBvbmVudC5zY3NzIiwic3JjL2FwcC9jb21wb25lbnRzL3Byb2R1Y3QtbGlzdC1pbmZvL3Byb2R1Y3QtbGlzdC1pbmZvLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUNJO0VBQ0ksOEJBQUE7QUNBUjtBREVJO0VBQ0ksV0FBQTtFQUNBLDBCQUFBO0VBQ0EsbUNBQUE7VUFBQSwyQkFBQTtFQUNBLGVBQUE7QUNBUiIsImZpbGUiOiJzcmMvYXBwL2NvbXBvbmVudHMvcHJvZHVjdC1saXN0LWluZm8vcHJvZHVjdC1saXN0LWluZm8uY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJkaXYge1xuICAgICYuZGFuZ2VyIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1kYW5nZXIpO1xuICAgIH1cbiAgICAmLnByb2R1Y3RfbGluayB7XG4gICAgICAgIGNvbG9yOiBibHVlO1xuICAgICAgICB0ZXh0LWRlY29yYXRpb246IHVuZGVybGluZTtcbiAgICAgICAgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBibHVlO1xuICAgICAgICBjdXJzb3I6IHBvaW50ZXI7XG4gICAgfVxufSIsImRpdi5kYW5nZXIge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLWRhbmdlcik7XG59XG5kaXYucHJvZHVjdF9saW5rIHtcbiAgY29sb3I6IGJsdWU7XG4gIHRleHQtZGVjb3JhdGlvbjogdW5kZXJsaW5lO1xuICB0ZXh0LWRlY29yYXRpb24tY29sb3I6IGJsdWU7XG4gIGN1cnNvcjogcG9pbnRlcjtcbn0iXX0= */"

/***/ }),

/***/ "./src/app/components/product-list-info/product-list-info.component.ts":
/*!*****************************************************************************!*\
  !*** ./src/app/components/product-list-info/product-list-info.component.ts ***!
  \*****************************************************************************/
/*! exports provided: ProductListInfoComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProductListInfoComponent", function() { return ProductListInfoComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");



var ProductListInfoComponent = /** @class */ (function () {
    function ProductListInfoComponent(router) {
        this.router = router;
    }
    ProductListInfoComponent.prototype.ngOnInit = function () { };
    ProductListInfoComponent.prototype.open_link = function (product_id) {
        this.router.navigateByUrl('/product/' + product_id);
    };
    ProductListInfoComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] }
    ]; };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], ProductListInfoComponent.prototype, "products", void 0);
    ProductListInfoComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-product-list-info',
            template: __webpack_require__(/*! raw-loader!./product-list-info.component.html */ "./node_modules/raw-loader/index.js!./src/app/components/product-list-info/product-list-info.component.html"),
            styles: [__webpack_require__(/*! ./product-list-info.component.scss */ "./src/app/components/product-list-info/product-list-info.component.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]])
    ], ProductListInfoComponent);
    return ProductListInfoComponent;
}());



/***/ }),

/***/ "./src/app/pages/product-list/product-list.module.ts":
/*!***********************************************************!*\
  !*** ./src/app/pages/product-list/product-list.module.ts ***!
  \***********************************************************/
/*! exports provided: ProductListPageModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProductListPageModule", function() { return ProductListPageModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _product_list_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./product-list.page */ "./src/app/pages/product-list/product-list.page.ts");
/* harmony import */ var _components_product_list_info_product_list_info_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../components/product-list-info/product-list-info.component */ "./src/app/components/product-list-info/product-list-info.component.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../shared/shared.module */ "./src/app/shared/shared.module.ts");









var routes = [
    {
        path: '',
        component: _product_list_page__WEBPACK_IMPORTED_MODULE_6__["ProductListPage"],
    }
];
var ProductListPageModule = /** @class */ (function () {
    function ProductListPageModule() {
    }
    ProductListPageModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__["SharedModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes)
            ],
            entryComponents: [_components_product_list_info_product_list_info_component__WEBPACK_IMPORTED_MODULE_7__["ProductListInfoComponent"]],
            declarations: [_product_list_page__WEBPACK_IMPORTED_MODULE_6__["ProductListPage"], _components_product_list_info_product_list_info_component__WEBPACK_IMPORTED_MODULE_7__["ProductListInfoComponent"]],
        })
    ], ProductListPageModule);
    return ProductListPageModule;
}());



/***/ }),

/***/ "./src/app/pages/product-list/product-list.page.scss":
/*!***********************************************************!*\
  !*** ./src/app/pages/product-list/product-list.page.scss ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3BhZ2VzL3Byb2R1Y3QtbGlzdC9wcm9kdWN0LWxpc3QucGFnZS5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/pages/product-list/product-list.page.ts":
/*!*********************************************************!*\
  !*** ./src/app/pages/product-list/product-list.page.ts ***!
  \*********************************************************/
/*! exports provided: ProductListPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProductListPage", function() { return ProductListPage; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/fesm5/ionic-storage.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");








var ProductListPage = /** @class */ (function () {
    function ProductListPage(odoo, router, storage, alertCtrl, audio, stock) {
        this.odoo = odoo;
        this.router = router;
        this.storage = storage;
        this.alertCtrl = alertCtrl;
        this.audio = audio;
        this.stock = stock;
        this.scanner_options = { reader: true, microphone: false, sound: false };
        this.check_scanner_values();
        this.offset = 0;
        this.limit = 25;
        this.limit_reached = false;
    }
    ProductListPage.prototype.ngOnInit = function () {
        var _this = this;
        this.odoo.isLoggedIn().then(function (data) {
            if (data == false) {
                _this.router.navigateByUrl('/login');
            }
            else {
                _this.get_product_list();
                _this.show_scan_form = _this.scanner_options['reader'];
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    ProductListPage.prototype.check_scanner_values = function () {
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
    ProductListPage.prototype.presentAlert = function (titulo, texto) {
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
    ProductListPage.prototype.onReadingEmitted = function (val) {
        this.scanner_reading = val;
        this.search = val;
        this.get_product_list(this.search);
    };
    ProductListPage.prototype.onShowEmitted = function (val) {
        this.show_scan_form = val;
    };
    ProductListPage.prototype.get_product_list = function (search) {
        var _this = this;
        if (search === void 0) { search = null; }
        this.offset = 0;
        this.limit_reached = false;
        this.stock.get_product_list(this.offset, this.limit, search).then(function (data) {
            _this.product_list = data;
            if (Object.keys(data).length < 25) {
                _this.limit_reached = true;
            }
            if (Object.keys(_this.product_list).length == 1) {
                _this.router.navigateByUrl('/product/' + _this.product_list[0]['id']);
            }
            _this.audio.play('click');
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperador el listado de operaciones:', error);
        });
    };
    ProductListPage.prototype.get_search_results = function (ev) {
        this.search = ev.target.value;
        this.get_product_list(this.search);
    };
    // Infinitescroll
    ProductListPage.prototype.loadData = function (event) {
        var _this = this;
        setTimeout(function () {
            console.log('Loading more products');
            event.target.complete();
            _this.product_list_infinite_scroll_add();
            // App logic to determine if all data is loaded
            // and disable the infinite scroll
            if (_this.limit_reached) {
                event.target.disabled = true;
            }
        }, 500);
    };
    ProductListPage.prototype.product_list_infinite_scroll_add = function () {
        var _this = this;
        this.offset += this.limit;
        this.stock.get_product_list(this.offset, this.limit, this.search).then(function (data) {
            var current_length = Object.keys(_this.product_list).length;
            if (Object.keys(data).length < 25) {
                _this.limit_reached = true;
            }
            for (var k in data)
                _this.product_list[current_length + Number(k)] = data[k];
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperador el listado de operaciones:', error);
        });
    };
    ProductListPage.prototype.toggleInfiniteScroll = function () {
        this.infiniteScroll.disabled = !this.infiniteScroll.disabled;
    };
    ProductListPage.ctorParameters = function () { return [
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_5__["OdooService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] },
        { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_2__["Storage"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_6__["AudioService"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_7__["StockService"] }
    ]; };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])(_ionic_angular__WEBPACK_IMPORTED_MODULE_4__["IonInfiniteScroll"], { static: false }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["IonInfiniteScroll"])
    ], ProductListPage.prototype, "infiniteScroll", void 0);
    ProductListPage = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-product-list',
            template: __webpack_require__(/*! raw-loader!./product-list.page.html */ "./node_modules/raw-loader/index.js!./src/app/pages/product-list/product-list.page.html"),
            styles: [__webpack_require__(/*! ./product-list.page.scss */ "./src/app/pages/product-list/product-list.page.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_5__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"],
            _ionic_storage__WEBPACK_IMPORTED_MODULE_2__["Storage"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_6__["AudioService"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_7__["StockService"]])
    ], ProductListPage);
    return ProductListPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-product-list-product-list-module-es5.js.map
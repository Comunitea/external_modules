(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-product-list-product-list-module"],{

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/product-list-info/product-list-info.component.html":
/*!*********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/components/product-list-info/product-list-info.component.html ***!
  \*********************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-grid>\n  <ion-row class=\"ion-align-items-center\">\n    <ion-col size=\"7\">\n        <div><strong>Nombre</strong></div>\n    </ion-col>\n    \n    <ion-col size=\"2\">\n        <div><strong>Código</strong></div>\n    </ion-col>\n\n    <ion-col size=\"1\">\n      <div><strong>Disponible</strong></div>\n    </ion-col>\n    \n    <ion-col size=\"1\">\n      <div><strong>Previsto</strong></div>\n    </ion-col>\n    <ion-col size=\"1\">\n      <div><strong>Precio de venta</strong></div>\n    </ion-col>\n  </ion-row>\n\n  <ion-row *ngFor=\"let product of products\">\n      <ion-col size-xs=\"12\" size-sm=\"7\" size-md=\"7\">\n          <div class=\"product_link\" (click)=\"open_link(product.id)\">{{product.display_name}}</div>\n      </ion-col>\n      \n      <ion-col size-xs=\"6\" size-sm=\"2\" size-md=\"2\">\n          <div><strong class=\"ion-hide-sm-up\">Código: </strong>{{product.default_code}}</div>\n      </ion-col>\n    \n      <ion-col size-xs=\"6\" size-sm=\"1\" size-md=\"1\">\n        <div [ngClass]=\"{'danger': product.qty_available &lt;= 0}\">\n          <strong class=\"ion-hide-sm-up\">Disponible: </strong>{{product.qty_available}}\n        </div>\n      </ion-col>\n      \n      <ion-col size-xs=\"6\" size-sm=\"1\" size-md=\"1\">\n        <div [ngClass]=\"{'danger': product.virtual_available &lt;= 0}\">\n          <strong class=\"ion-hide-sm-up\">Previsto: </strong>{{product.virtual_available}}\n        </div>\n      </ion-col>\n    \n      <ion-col size-xs=\"6\" size-sm=\"1\" size-md=\"1\">\n          <div>\n            <strong class=\"ion-hide-sm-up\">Precio de venta</strong>{{product.list_price}}€\n          </div>\n      </ion-col>\n    </ion-row>\n</ion-grid>");

/***/ }),

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/product-list/product-list.page.html":
/*!*************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/pages/product-list/product-list.page.html ***!
  \*************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"start\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n    <app-scanner-header slot=\"end\"></app-scanner-header>\n    <ion-title>Listado de productos</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <ion-card-content>\n    <ion-row>\n      <ion-toolbar>\n        <ion-searchbar type=\"text\" (ionInput)=\"get_search_results($event)\" autocomplete=\"on\" showCancelButton=\"always\"></ion-searchbar>\n      </ion-toolbar>\n    </ion-row>\n\n    <app-product-list-info [products]=\"product_list\"></app-product-list-info>\n    \n    <ion-infinite-scroll threshold=\"100px\" (ionInfinite)=\"loadData($event)\">\n      <ion-infinite-scroll-content\n        loadingSpinner=\"bubbles\"\n        loadingText=\"Cargando más productos...\">\n      </ion-infinite-scroll-content>\n    </ion-infinite-scroll>\n  </ion-card-content>\n</ion-content>\n\n<app-scanner-footer (scanner_reading_changed)=\"onReadingEmitted($event)\" [scanner_reading]=\"scanner_reading\"></app-scanner-footer>");

/***/ }),

/***/ "./src/app/components/product-list-info/product-list-info.component.scss":
/*!*******************************************************************************!*\
  !*** ./src/app/components/product-list-info/product-list-info.component.scss ***!
  \*******************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("div.danger {\n  color: var(--ion-color-danger);\n}\ndiv.product_link {\n  color: blue;\n  text-decoration: underline;\n  -webkit-text-decoration-color: blue;\n          text-decoration-color: blue;\n  cursor: pointer;\n}\n/* Medias */\n@media screen and (max-width: 576px) {\n  ion-grid > ion-row:first-child {\n    display: none;\n  }\n\n  ion-grid > ion-row {\n    border: 1px black solid;\n  }\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL2NvbXBvbmVudHMvcHJvZHVjdC1saXN0LWluZm8vcHJvZHVjdC1saXN0LWluZm8uY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL2NvbXBvbmVudHMvcHJvZHVjdC1saXN0LWluZm8vcHJvZHVjdC1saXN0LWluZm8uY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQ0k7RUFDSSw4QkFBQTtBQ0FSO0FERUk7RUFDSSxXQUFBO0VBQ0EsMEJBQUE7RUFDQSxtQ0FBQTtVQUFBLDJCQUFBO0VBQ0EsZUFBQTtBQ0FSO0FESUEsV0FBQTtBQUNBO0VBQ0k7SUFDSSxhQUFBO0VDRE47O0VER0U7SUFDSSx1QkFBQTtFQ0FOO0FBQ0YiLCJmaWxlIjoic3JjL2FwcC9jb21wb25lbnRzL3Byb2R1Y3QtbGlzdC1pbmZvL3Byb2R1Y3QtbGlzdC1pbmZvLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiZGl2IHtcbiAgICAmLmRhbmdlciB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItZGFuZ2VyKTtcbiAgICB9XG4gICAgJi5wcm9kdWN0X2xpbmsge1xuICAgICAgICBjb2xvcjogYmx1ZTtcbiAgICAgICAgdGV4dC1kZWNvcmF0aW9uOiB1bmRlcmxpbmU7XG4gICAgICAgIHRleHQtZGVjb3JhdGlvbi1jb2xvcjogYmx1ZTtcbiAgICAgICAgY3Vyc29yOiBwb2ludGVyO1xuICAgIH1cbn1cblxuLyogTWVkaWFzICovXG5AbWVkaWEgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiA1NzZweCkge1xuICAgIGlvbi1ncmlkID4gaW9uLXJvdzpmaXJzdC1jaGlsZCB7XG4gICAgICAgIGRpc3BsYXk6IG5vbmU7XG4gICAgfVxuICAgIGlvbi1ncmlkID4gaW9uLXJvdyB7XG4gICAgICAgIGJvcmRlcjogMXB4IGJsYWNrIHNvbGlkO1xuICAgIH1cbn0iLCJkaXYuZGFuZ2VyIHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1kYW5nZXIpO1xufVxuZGl2LnByb2R1Y3RfbGluayB7XG4gIGNvbG9yOiBibHVlO1xuICB0ZXh0LWRlY29yYXRpb246IHVuZGVybGluZTtcbiAgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBibHVlO1xuICBjdXJzb3I6IHBvaW50ZXI7XG59XG5cbi8qIE1lZGlhcyAqL1xuQG1lZGlhIHNjcmVlbiBhbmQgKG1heC13aWR0aDogNTc2cHgpIHtcbiAgaW9uLWdyaWQgPiBpb24tcm93OmZpcnN0LWNoaWxkIHtcbiAgICBkaXNwbGF5OiBub25lO1xuICB9XG5cbiAgaW9uLWdyaWQgPiBpb24tcm93IHtcbiAgICBib3JkZXI6IDFweCBibGFjayBzb2xpZDtcbiAgfVxufSJdfQ== */");

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");



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
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)
    ], ProductListInfoComponent.prototype, "products", void 0);
    ProductListInfoComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-product-list-info',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./product-list-info.component.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/product-list-info/product-list-info.component.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./product-list-info.component.scss */ "./src/app/components/product-list-info/product-list-info.component.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]])
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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
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
    ProductListPageModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
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
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3BhZ2VzL3Byb2R1Y3QtbGlzdC9wcm9kdWN0LWxpc3QucGFnZS5zY3NzIn0= */");

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");







var ProductListPage = /** @class */ (function () {
    function ProductListPage(odoo, router, alertCtrl, audio, stock) {
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.audio = audio;
        this.stock = stock;
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
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    ProductListPage.prototype.presentAlert = function (titulo, texto) {
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
    ProductListPage.prototype.onReadingEmitted = function (val) {
        this.scanner_reading = val;
        this.search = val;
        this.get_product_list(this.search);
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
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])(_ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"], { static: false }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"])
    ], ProductListPage.prototype, "infiniteScroll", void 0);
    ProductListPage = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-product-list',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./product-list.page.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/product-list/product-list.page.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./product-list.page.scss */ "./src/app/pages/product-list/product-list.page.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"]])
    ], ProductListPage);
    return ProductListPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-product-list-product-list-module.js.map
(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-product-product-module"],{

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/product-quant-list/product-quant-list.component.html":
/*!***********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/components/product-quant-list/product-quant-list.component.html ***!
  \***********************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-grid>\n  <ion-row>\n    <ion-col size=\"8\">\n        <div><strong>Ubicación</strong></div>\n    </ion-col>\n    \n    <ion-col size=\"2\">\n        <div><strong>Reservado</strong></div>\n    </ion-col>\n\n    <ion-col size=\"2\">\n      <div><strong>A mano</strong></div>\n    </ion-col>\n  </ion-row>\n  <ion-row *ngFor=\"let quant of quants\">\n      <ion-col size-xs=\"12\" size-sm=\"8\" size=\"8\">\n      <div class=\"product_link\" (click)=\"open_link(quant.location_id[0])\">{{quant.location_id[1]}}</div>\n    </ion-col>\n    \n    <ion-col size-xs=\"6\" size-sm=\"2\" size=\"2\">\n      <div><strong class=\"ion-hide-sm-up\">Reservado: </strong>{{quant.reserved_quantity}}</div>\n    </ion-col>\n    \n    <ion-col size-xs=\"6\" size-sm=\"2\" size=\"2\">\n      <div [ngClass]=\"{'danger': quant.quantity &lt;= 0}\"><strong class=\"ion-hide-sm-up\">A mano: </strong>{{quant.quantity}}</div>\n    </ion-col>\n  </ion-row>\n</ion-grid>");

/***/ }),

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/product/product.page.html":
/*!***************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/pages/product/product.page.html ***!
  \***************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"start\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n    <app-scanner-header [disabled_reader]=\"true\" slot=\"end\"></app-scanner-header>\n    <ion-title>Detalles del producto</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <ion-card *ngIf=\"product_data\">\n    <ion-card-header>\n      <ion-card-title>{{product_data.display_name}}</ion-card-title>\n    </ion-card-header>\n\n    <ion-card-content>\n      <div class=\"product_img\">\n      <ion-img *ngIf=\"product_data.base64\" src=\"data:image/jpeg;base64,{{ product_data['image_medium'] }}\"></ion-img>\n      <ion-img *ngIf=\"!product_data.base64\" src=\"{{ product_data['image_medium'] }}\"></ion-img>\n      <ion-label *ngIf=\"product_data.description_short\">{{product_data.description_short}}</ion-label>\n      </div>\n      <div><strong>Categoría: </strong>{{product_data.categ_id[1]}}</div>\n      <div><strong>Referencia: </strong>{{product_data.default_code}}</div>\n      <div *ngIf=\"product_data.barcode\"><strong>Codigo de barras: </strong>{{product_data.barcode}}</div>\n      <div><strong>Precio de venta: </strong>{{product_data.list_price}}€</div>\n      <div><strong>Precio de compra: </strong>{{product_data.standard_price}}€</div>\n      <div [ngClass]=\"{'danger': product_data.qty_available &lt;= 0}\"><strong>A mano: </strong>{{product_data.qty_available}}</div>\n      <div [ngClass]=\"{'danger': product_data.virtual_available &lt;= 0}\"><strong>Previsto: </strong>{{product_data.virtual_available}}</div>\n    </ion-card-content>\n  </ion-card>\n\n  <app-product-quant-list [quants]=\"quants\"></app-product-quant-list>\n  \n  <ion-infinite-scroll threshold=\"100px\" (ionInfinite)=\"loadData($event)\">\n    <ion-infinite-scroll-content\n      loadingSpinner=\"bubbles\"\n      loadingText=\"Cargando más localizaciones...\">\n    </ion-infinite-scroll-content>\n  </ion-infinite-scroll>\n</ion-content>");

/***/ }),

/***/ "./src/app/components/product-quant-list/product-quant-list.component.scss":
/*!*********************************************************************************!*\
  !*** ./src/app/components/product-quant-list/product-quant-list.component.scss ***!
  \*********************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("div.danger {\n  color: var(--ion-color-danger);\n}\ndiv.product_link {\n  color: blue;\n  text-decoration: underline;\n  -webkit-text-decoration-color: blue;\n          text-decoration-color: blue;\n  cursor: pointer;\n}\n/* Medias */\n@media screen and (max-width: 576px) {\n  ion-grid > ion-row:first-child {\n    display: none;\n  }\n\n  ion-grid > ion-row {\n    border: 1px black solid;\n  }\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL2NvbXBvbmVudHMvcHJvZHVjdC1xdWFudC1saXN0L3Byb2R1Y3QtcXVhbnQtbGlzdC5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvY29tcG9uZW50cy9wcm9kdWN0LXF1YW50LWxpc3QvcHJvZHVjdC1xdWFudC1saXN0LmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUNJO0VBQ0ksOEJBQUE7QUNBUjtBREVJO0VBQ0ksV0FBQTtFQUNBLDBCQUFBO0VBQ0EsbUNBQUE7VUFBQSwyQkFBQTtFQUNBLGVBQUE7QUNBUjtBRElBLFdBQUE7QUFDQTtFQUNJO0lBQ0ksYUFBQTtFQ0ROOztFREdFO0lBQ0ksdUJBQUE7RUNBTjtBQUNGIiwiZmlsZSI6InNyYy9hcHAvY29tcG9uZW50cy9wcm9kdWN0LXF1YW50LWxpc3QvcHJvZHVjdC1xdWFudC1saXN0LmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiZGl2IHtcbiAgICAmLmRhbmdlciB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItZGFuZ2VyKTtcbiAgICB9XG4gICAgJi5wcm9kdWN0X2xpbmsge1xuICAgICAgICBjb2xvcjogYmx1ZTtcbiAgICAgICAgdGV4dC1kZWNvcmF0aW9uOiB1bmRlcmxpbmU7XG4gICAgICAgIHRleHQtZGVjb3JhdGlvbi1jb2xvcjogYmx1ZTtcbiAgICAgICAgY3Vyc29yOiBwb2ludGVyO1xuICAgIH1cbn1cblxuLyogTWVkaWFzICovXG5AbWVkaWEgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiA1NzZweCkge1xuICAgIGlvbi1ncmlkID4gaW9uLXJvdzpmaXJzdC1jaGlsZCB7XG4gICAgICAgIGRpc3BsYXk6IG5vbmU7XG4gICAgfVxuICAgIGlvbi1ncmlkID4gaW9uLXJvdyB7XG4gICAgICAgIGJvcmRlcjogMXB4IGJsYWNrIHNvbGlkO1xuICAgIH1cbn0iLCJkaXYuZGFuZ2VyIHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1kYW5nZXIpO1xufVxuZGl2LnByb2R1Y3RfbGluayB7XG4gIGNvbG9yOiBibHVlO1xuICB0ZXh0LWRlY29yYXRpb246IHVuZGVybGluZTtcbiAgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBibHVlO1xuICBjdXJzb3I6IHBvaW50ZXI7XG59XG5cbi8qIE1lZGlhcyAqL1xuQG1lZGlhIHNjcmVlbiBhbmQgKG1heC13aWR0aDogNTc2cHgpIHtcbiAgaW9uLWdyaWQgPiBpb24tcm93OmZpcnN0LWNoaWxkIHtcbiAgICBkaXNwbGF5OiBub25lO1xuICB9XG5cbiAgaW9uLWdyaWQgPiBpb24tcm93IHtcbiAgICBib3JkZXI6IDFweCBibGFjayBzb2xpZDtcbiAgfVxufSJdfQ== */");

/***/ }),

/***/ "./src/app/components/product-quant-list/product-quant-list.component.ts":
/*!*******************************************************************************!*\
  !*** ./src/app/components/product-quant-list/product-quant-list.component.ts ***!
  \*******************************************************************************/
/*! exports provided: ProductQuantListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProductQuantListComponent", function() { return ProductQuantListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");



var ProductQuantListComponent = /** @class */ (function () {
    function ProductQuantListComponent(router) {
        this.router = router;
    }
    ProductQuantListComponent.prototype.ngOnInit = function () { };
    ProductQuantListComponent.prototype.open_link = function (location_id) {
        this.router.navigateByUrl('/stock-location/' + location_id);
    };
    ProductQuantListComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)
    ], ProductQuantListComponent.prototype, "quants", void 0);
    ProductQuantListComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-product-quant-list',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./product-quant-list.component.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/product-quant-list/product-quant-list.component.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./product-quant-list.component.scss */ "./src/app/components/product-quant-list/product-quant-list.component.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]])
    ], ProductQuantListComponent);
    return ProductQuantListComponent;
}());



/***/ }),

/***/ "./src/app/pages/product/product.module.ts":
/*!*************************************************!*\
  !*** ./src/app/pages/product/product.module.ts ***!
  \*************************************************/
/*! exports provided: ProductPageModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProductPageModule", function() { return ProductPageModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _product_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./product.page */ "./src/app/pages/product/product.page.ts");
/* harmony import */ var _components_product_quant_list_product_quant_list_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../components/product-quant-list/product-quant-list.component */ "./src/app/components/product-quant-list/product-quant-list.component.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../shared/shared.module */ "./src/app/shared/shared.module.ts");









var routes = [
    {
        path: '',
        component: _product_page__WEBPACK_IMPORTED_MODULE_6__["ProductPage"]
    }
];
var ProductPageModule = /** @class */ (function () {
    function ProductPageModule() {
    }
    ProductPageModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes),
                _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__["SharedModule"]
            ],
            entryComponents: [],
            declarations: [_product_page__WEBPACK_IMPORTED_MODULE_6__["ProductPage"], _components_product_quant_list_product_quant_list_component__WEBPACK_IMPORTED_MODULE_7__["ProductQuantListComponent"]]
        })
    ], ProductPageModule);
    return ProductPageModule;
}());



/***/ }),

/***/ "./src/app/pages/product/product.page.scss":
/*!*************************************************!*\
  !*** ./src/app/pages/product/product.page.scss ***!
  \*************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("div.danger {\n  color: var(--ion-color-danger);\n}\ndiv.product_img ion-img {\n  max-width: 100px;\n  max-height: 100px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL3BhZ2VzL3Byb2R1Y3QvcHJvZHVjdC5wYWdlLnNjc3MiLCJzcmMvYXBwL3BhZ2VzL3Byb2R1Y3QvcHJvZHVjdC5wYWdlLnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQ0k7RUFDSSw4QkFBQTtBQ0FSO0FER1E7RUFDSSxnQkFBQTtFQUNBLGlCQUFBO0FDRFoiLCJmaWxlIjoic3JjL2FwcC9wYWdlcy9wcm9kdWN0L3Byb2R1Y3QucGFnZS5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiZGl2IHtcbiAgICAmLmRhbmdlciB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItZGFuZ2VyKTtcbiAgICB9XG4gICAgJi5wcm9kdWN0X2ltZyB7XG4gICAgICAgIGlvbi1pbWcge1xuICAgICAgICAgICAgbWF4LXdpZHRoOiAxMDBweDtcbiAgICAgICAgICAgIG1heC1oZWlnaHQ6IDEwMHB4O1xuICAgICAgICB9XG4gICAgfVxufSIsImRpdi5kYW5nZXIge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLWRhbmdlcik7XG59XG5kaXYucHJvZHVjdF9pbWcgaW9uLWltZyB7XG4gIG1heC13aWR0aDogMTAwcHg7XG4gIG1heC1oZWlnaHQ6IDEwMHB4O1xufSJdfQ== */");

/***/ }),

/***/ "./src/app/pages/product/product.page.ts":
/*!***********************************************!*\
  !*** ./src/app/pages/product/product.page.ts ***!
  \***********************************************/
/*! exports provided: ProductPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProductPage", function() { return ProductPage; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/__ivy_ngcc__/fesm5/ionic-storage.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");








var ProductPage = /** @class */ (function () {
    function ProductPage(odoo, router, alertCtrl, route, audio, stock, storage) {
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.route = route;
        this.audio = audio;
        this.stock = stock;
        this.storage = storage;
        this.offset = 0;
        this.limit = 25;
        this.limit_reached = false;
    }
    ProductPage.prototype.ngOnInit = function () {
        var _this = this;
        this.odoo.isLoggedIn().then(function (data) {
            if (data == false) {
                _this.router.navigateByUrl('/login');
            }
            else {
                _this.storage.get('CONEXION').then(function (con) {
                    _this.placeholder = con.url + "/web/static/src/img/placeholder.png";
                })
                    .catch(function (error) {
                    _this.presentAlert('Error al comprobar tu sesión:', error);
                });
                var product = _this.route.snapshot.paramMap.get('id');
                _this.get_product_info(product);
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    ProductPage.prototype.presentAlert = function (titulo, texto) {
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
    ProductPage.prototype.get_product_info = function (product) {
        var _this = this;
        console.log(product);
        this.stock.get_product_info(product).then(function (data) {
            if (data[0]['image_medium'] == false) {
                data[0]['base64'] = false;
                data[0]['image_medium'] = _this.placeholder;
            }
            else {
                data[0]['base64'] = true;
            }
            _this.product_data = data[0];
            _this.audio.play('click');
            console.log("QUANTS");
            console.log(_this.product_data);
            console.log(_this.product_data['stock_quant_ids']);
            _this.quants = _this.product_data['stock_quant_ids'];
            /* this.get_location_quants(this.product_data['default_code']); */
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperar el picking:', error);
        });
    };
    ProductPage.prototype.get_location_quants = function (search) {
        var _this = this;
        if (search === void 0) { search = null; }
        this.offset = 0;
        this.limit_reached = false;
        this.stock.get_location_quants(null, this.offset, this.limit, search, 'form').then(function (quants_list) {
            _this.quants = quants_list;
            console.log(_this.quants);
            if (Object.keys(quants_list).length < 25) {
                _this.limit_reached = true;
            }
            _this.audio.play('click');
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperador el listado de stock:', error);
        });
    };
    // Infinitescroll
    ProductPage.prototype.loadData = function (event) {
        var _this = this;
        setTimeout(function () {
            console.log('Loading more locations');
            event.target.complete();
            _this.quant_list_infinite_scroll_add();
            // App logic to determine if all data is loaded
            // and disable the infinite scroll
            if (_this.limit_reached) {
                event.target.disabled = true;
            }
        }, 500);
    };
    ProductPage.prototype.quant_list_infinite_scroll_add = function () {
        var _this = this;
        this.offset += this.limit;
        this.stock.get_location_quants(null, this.offset, this.limit, this.product_data['default_code'], 'form').then(function (data) {
            var current_length = Object.keys(_this.quants).length;
            if (Object.keys(data).length < 25) {
                _this.limit_reached = true;
            }
            for (var k in data)
                _this.quants[current_length + Number(k)] = data[k];
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperador el listado de stock:', error);
        });
    };
    ProductPage.prototype.toggleInfiniteScroll = function () {
        this.infiniteScroll.disabled = !this.infiniteScroll.disabled;
    };
    ProductPage.ctorParameters = function () { return [
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_5__["OdooService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_6__["AudioService"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_7__["StockService"] },
        { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_3__["Storage"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])(_ionic_angular__WEBPACK_IMPORTED_MODULE_4__["IonInfiniteScroll"], { static: false }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["IonInfiniteScroll"])
    ], ProductPage.prototype, "infiniteScroll", void 0);
    ProductPage = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-product',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./product.page.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/product/product.page.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./product.page.scss */ "./src/app/pages/product/product.page.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_5__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_6__["AudioService"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_7__["StockService"],
            _ionic_storage__WEBPACK_IMPORTED_MODULE_3__["Storage"]])
    ], ProductPage);
    return ProductPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-product-product-module.js.map
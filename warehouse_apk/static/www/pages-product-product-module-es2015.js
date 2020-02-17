(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-product-product-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/components/product-info/product-info.component.html":
/*!***********************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/components/product-info/product-info.component.html ***!
  \***********************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-card *ngIf=\"product\">\n\n    <ion-card-header>\n      <ion-card-title>{{product.name}}</ion-card-title>\n    </ion-card-header>\n  \n    <ion-card-content>\n      <div class=\"product_img\">\n        <ion-img *ngIf=\"product.base64\" src=\"data:image/jpeg;base64,{{ product['image_medium'] }}\"></ion-img>\n        <ion-img *ngIf=\"!product.base64\" src=\"{{ product['image_medium'] }}\"></ion-img>\n        <ion-label>{{product.description_short}}</ion-label>\n      </div>\n      <div><strong>Categoría: </strong>{{product.categ_id[1]}}</div>\n      <div><strong>Referencia: </strong>{{product.default_code}}</div>\n      <div><strong>Codigo de barras: </strong>{{product.barcode}}</div>\n      <div><strong>Precio de venta: </strong>{{product.list_price}}€</div>\n      <div><strong>Precio de compra: </strong>{{product.standard_price}}€</div>\n      <div [ngClass]=\"{'danger': product.qty_available &lt;= 0}\"><strong>A mano: </strong>{{product.qty_available}}</div>\n      <div [ngClass]=\"{'danger': product.qty_available &lt;= 0}\"><strong>Previsto: </strong>{{product.virtual_available}}</div>\n    </ion-card-content>\n  \n  </ion-card>"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/pages/product/product.page.html":
/*!***************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/pages/product/product.page.html ***!
  \***************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"Productos\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n\n    <ion-title>Detalles del producto</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <app-product-info [product]=\"product_data\"></app-product-info>\n</ion-content>"

/***/ }),

/***/ "./src/app/components/product-info/product-info.component.scss":
/*!*********************************************************************!*\
  !*** ./src/app/components/product-info/product-info.component.scss ***!
  \*********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "div.danger {\n  color: var(--ion-color-danger);\n}\ndiv.product_img ion-img {\n  max-width: 100px;\n  max-height: 100px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9jb21wb25lbnRzL3Byb2R1Y3QtaW5mby9wcm9kdWN0LWluZm8uY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL2NvbXBvbmVudHMvcHJvZHVjdC1pbmZvL3Byb2R1Y3QtaW5mby5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFDSTtFQUNJLDhCQUFBO0FDQVI7QURHUTtFQUNJLGdCQUFBO0VBQ0EsaUJBQUE7QUNEWiIsImZpbGUiOiJzcmMvYXBwL2NvbXBvbmVudHMvcHJvZHVjdC1pbmZvL3Byb2R1Y3QtaW5mby5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbImRpdiB7XG4gICAgJi5kYW5nZXIge1xuICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLWRhbmdlcik7XG4gICAgfVxuICAgICYucHJvZHVjdF9pbWcge1xuICAgICAgICBpb24taW1nIHtcbiAgICAgICAgICAgIG1heC13aWR0aDogMTAwcHg7XG4gICAgICAgICAgICBtYXgtaGVpZ2h0OiAxMDBweDtcbiAgICAgICAgfVxuICAgIH1cbn0iLCJkaXYuZGFuZ2VyIHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1kYW5nZXIpO1xufVxuZGl2LnByb2R1Y3RfaW1nIGlvbi1pbWcge1xuICBtYXgtd2lkdGg6IDEwMHB4O1xuICBtYXgtaGVpZ2h0OiAxMDBweDtcbn0iXX0= */"

/***/ }),

/***/ "./src/app/components/product-info/product-info.component.ts":
/*!*******************************************************************!*\
  !*** ./src/app/components/product-info/product-info.component.ts ***!
  \*******************************************************************/
/*! exports provided: ProductInfoComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProductInfoComponent", function() { return ProductInfoComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");


let ProductInfoComponent = class ProductInfoComponent {
    constructor() { }
    ngOnInit() { }
};
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
], ProductInfoComponent.prototype, "product", void 0);
ProductInfoComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-product-info',
        template: __webpack_require__(/*! raw-loader!./product-info.component.html */ "./node_modules/raw-loader/index.js!./src/app/components/product-info/product-info.component.html"),
        styles: [__webpack_require__(/*! ./product-info.component.scss */ "./src/app/components/product-info/product-info.component.scss")]
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [])
], ProductInfoComponent);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _product_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./product.page */ "./src/app/pages/product/product.page.ts");
/* harmony import */ var _components_product_info_product_info_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../components/product-info/product-info.component */ "./src/app/components/product-info/product-info.component.ts");








const routes = [
    {
        path: '',
        component: _product_page__WEBPACK_IMPORTED_MODULE_6__["ProductPage"]
    }
];
let ProductPageModule = class ProductPageModule {
};
ProductPageModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes)
        ],
        entryComponents: [_components_product_info_product_info_component__WEBPACK_IMPORTED_MODULE_7__["ProductInfoComponent"]],
        declarations: [_product_page__WEBPACK_IMPORTED_MODULE_6__["ProductPage"], _components_product_info_product_info_component__WEBPACK_IMPORTED_MODULE_7__["ProductInfoComponent"]]
    })
], ProductPageModule);



/***/ }),

/***/ "./src/app/pages/product/product.page.scss":
/*!*************************************************!*\
  !*** ./src/app/pages/product/product.page.scss ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3BhZ2VzL3Byb2R1Y3QvcHJvZHVjdC5wYWdlLnNjc3MifQ== */"

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/fesm2015/ionic-storage.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");








let ProductPage = class ProductPage {
    constructor(odoo, router, alertCtrl, route, audio, stock, storage) {
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.route = route;
        this.audio = audio;
        this.stock = stock;
        this.storage = storage;
    }
    ngOnInit() {
        this.odoo.isLoggedIn().then((data) => {
            if (data == false) {
                this.router.navigateByUrl('/login');
            }
            else {
                this.storage.get('CONEXION').then((con) => {
                    this.placeholder = con.url + "/web/static/src/img/placeholder.png";
                })
                    .catch((error) => {
                    this.presentAlert('Error al comprobar tu sesión:', error);
                });
                var product = this.route.snapshot.paramMap.get('id');
                this.get_product_info(product);
            }
        })
            .catch((error) => {
            this.presentAlert('Error al comprobar tu sesión:', error);
        });
    }
    presentAlert(titulo, texto) {
        return tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"](this, void 0, void 0, function* () {
            this.audio.play('error');
            const alert = yield this.alertCtrl.create({
                header: titulo,
                subHeader: texto,
                buttons: ['Ok']
            });
            yield alert.present();
        });
    }
    get_product_info(product) {
        console.log(product);
        this.stock.get_product_info(product).then((data) => {
            if (data[0]['image_medium'] == false) {
                data[0]['base64'] = false;
                data[0]['image_medium'] = this.placeholder;
            }
            else {
                data[0]['base64'] = true;
            }
            this.product_data = data[0];
            this.audio.play('click');
        })
            .catch((error) => {
            this.presentAlert('Error al recuperar el picking:', error);
        });
    }
};
ProductPage.ctorParameters = () => [
    { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_5__["OdooService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
    { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_6__["AudioService"] },
    { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_7__["StockService"] },
    { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_3__["Storage"] }
];
ProductPage = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-product',
        template: __webpack_require__(/*! raw-loader!./product.page.html */ "./node_modules/raw-loader/index.js!./src/app/pages/product/product.page.html"),
        styles: [__webpack_require__(/*! ./product.page.scss */ "./src/app/pages/product/product.page.scss")]
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_5__["OdooService"],
        _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
        _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"],
        _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"],
        _services_audio_service__WEBPACK_IMPORTED_MODULE_6__["AudioService"],
        _services_stock_service__WEBPACK_IMPORTED_MODULE_7__["StockService"],
        _ionic_storage__WEBPACK_IMPORTED_MODULE_3__["Storage"]])
], ProductPage);



/***/ })

}]);
//# sourceMappingURL=pages-product-product-module-es2015.js.map
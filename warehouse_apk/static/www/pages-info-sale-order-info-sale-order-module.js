(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-info-sale-order-info-sale-order-module"],{

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/info-sale-order/info-sale-order.page.html":
/*!*******************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/pages/info-sale-order/info-sale-order.page.html ***!
  \*******************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-header>\n  <ion-toolbar class=\"cmnt-front\">\n    <button class=\"cmnt-button\" slot=\"end\" ion-button icon-only item-end (click)=\"goBack()\">\n      <ion-icon style=\"font-size: 2em;\" name=\"arrow-undo-outline\" class=\"cmnt-front\"></ion-icon>\n    </button> \n  <ion-title>{{SaleOrder && SaleOrder['name']}}</ion-title>\n  </ion-toolbar> \n  \n</ion-header>\n\n<ion-content *ngIf=\"SaleOrder\">\n<ion-list >  \n<ion-item>\n      <ion-label>\n        <h2>{{SaleOrder['partner_id']['name']}}</h2>\n      </ion-label>\n  </ion-item>\n  <ion-item>\n      <ion-label>\n        <h2>Fecha de pedido</h2>\n        <p>{{SaleOrder['date_order']}}</p>\n      </ion-label>\n  </ion-item>\n  <ion-item>\n      <ion-label>\n        <h2>Importe</h2>\n        <p>{{SaleOrder['amount_untaxed']}} €</p>\n      </ion-label>\n  </ion-item>\n  </ion-list>\n  \n</ion-content>\n");

/***/ }),

/***/ "./src/app/pages/info-sale-order/info-sale-order.module.ts":
/*!*****************************************************************!*\
  !*** ./src/app/pages/info-sale-order/info-sale-order.module.ts ***!
  \*****************************************************************/
/*! exports provided: InfoSaleOrderPageModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InfoSaleOrderPageModule", function() { return InfoSaleOrderPageModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _info_sale_order_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./info-sale-order.page */ "./src/app/pages/info-sale-order/info-sale-order.page.ts");







var routes = [
    {
        path: '',
        component: _info_sale_order_page__WEBPACK_IMPORTED_MODULE_6__["InfoSaleOrderPage"]
    }
];
var InfoSaleOrderPageModule = /** @class */ (function () {
    function InfoSaleOrderPageModule() {
    }
    InfoSaleOrderPageModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes)
            ],
            declarations: [_info_sale_order_page__WEBPACK_IMPORTED_MODULE_6__["InfoSaleOrderPage"]]
        })
    ], InfoSaleOrderPageModule);
    return InfoSaleOrderPageModule;
}());



/***/ }),

/***/ "./src/app/pages/info-sale-order/info-sale-order.page.scss":
/*!*****************************************************************!*\
  !*** ./src/app/pages/info-sale-order/info-sale-order.page.scss ***!
  \*****************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".ion-page {\n  height: 80%;\n  width: 80%;\n  top: 10%;\n  position: absolute;\n  display: block;\n}\n\nion-toolbar {\n  --min-height: 50px !important ;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL3BhZ2VzL2luZm8tc2FsZS1vcmRlci9pbmZvLXNhbGUtb3JkZXIucGFnZS5zY3NzIiwic3JjL2FwcC9wYWdlcy9pbmZvLXNhbGUtb3JkZXIvaW5mby1zYWxlLW9yZGVyLnBhZ2Uuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNJLFdBQUE7RUFDQSxVQUFBO0VBQ0EsUUFBQTtFQUNBLGtCQUFBO0VBQ0EsY0FBQTtBQ0NKOztBRENBO0VBQ0ksOEJBQUE7QUNFSiIsImZpbGUiOiJzcmMvYXBwL3BhZ2VzL2luZm8tc2FsZS1vcmRlci9pbmZvLXNhbGUtb3JkZXIucGFnZS5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLmlvbi1wYWdlIHtcbiAgICBoZWlnaHQ6IDgwJTtcbiAgICB3aWR0aDogODAlO1xuICAgIHRvcDogMTAlO1xuICAgIHBvc2l0aW9uOiBhYnNvbHV0ZTsgXG4gICAgZGlzcGxheTogYmxvY2s7ICB9IFxuXG5pb24tdG9vbGJhcntcbiAgICAtLW1pbi1oZWlnaHQ6IDUwcHggIWltcG9ydGFudFxuXG59IiwiLmlvbi1wYWdlIHtcbiAgaGVpZ2h0OiA4MCU7XG4gIHdpZHRoOiA4MCU7XG4gIHRvcDogMTAlO1xuICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gIGRpc3BsYXk6IGJsb2NrO1xufVxuXG5pb24tdG9vbGJhciB7XG4gIC0tbWluLWhlaWdodDogNTBweCAhaW1wb3J0YW50IDtcbn0iXX0= */");

/***/ }),

/***/ "./src/app/pages/info-sale-order/info-sale-order.page.ts":
/*!***************************************************************!*\
  !*** ./src/app/pages/info-sale-order/info-sale-order.page.ts ***!
  \***************************************************************/
/*! exports provided: InfoSaleOrderPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InfoSaleOrderPage", function() { return InfoSaleOrderPage; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");





var InfoSaleOrderPage = /** @class */ (function () {
    function InfoSaleOrderPage(odoo, navCtrl, route) {
        this.odoo = odoo;
        this.navCtrl = navCtrl;
        this.route = route;
    }
    InfoSaleOrderPage.prototype.ngOnInit = function () {
    };
    InfoSaleOrderPage.prototype.goBack = function () {
        this.navCtrl.back();
    };
    InfoSaleOrderPage.prototype.ionViewWillEnter = function () {
        var Id = +this.route.snapshot.paramMap.get('id');
        var self = this;
        // this.Data = this.navParams.get('data');
        this.odoo.execute('sale.order', 'get_modal_info', { id: Id }).then(function (data) {
            self.SaleOrder = data;
        }).catch(function (error) {
        });
    };
    InfoSaleOrderPage.ctorParameters = function () { return [
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_2__["OdooService"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["NavController"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] }
    ]; };
    InfoSaleOrderPage = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-info-sale-order',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./info-sale-order.page.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/info-sale-order/info-sale-order.page.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./info-sale-order.page.scss */ "./src/app/pages/info-sale-order/info-sale-order.page.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_2__["OdooService"], _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["NavController"], _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"]])
    ], InfoSaleOrderPage);
    return InfoSaleOrderPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-info-sale-order-info-sale-order-module.js.map
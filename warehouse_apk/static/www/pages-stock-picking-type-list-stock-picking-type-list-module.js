(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-stock-picking-type-list-stock-picking-type-list-module"],{

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/picking-type-info/picking-type-info.component.html":
/*!*********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/components/picking-type-info/picking-type-info.component.html ***!
  \*********************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-grid>\n  <ion-row>\n    <ion-col size-xs=\"12\" size-sm=\"6\" size-lg=\"4\" *ngFor=\"let picking_type of picking_types\">\n      <ion-card>\n        <ion-card-header>\n          <ion-card-title>{{picking_type.name}}</ion-card-title>\n          <ion-card-subtitle [ngClass]=\"{ \n            'primary': picking_type.color == 0, \n            'secondary': picking_type.color == 1, \n            'tertiary': picking_type.color == 2, \n            'medium': picking_type.color == 3,\n            'success': picking_type.color == 4,\n            'warning': picking_type.color == 5}\">{{picking_type.warehouse_id[1]}}</ion-card-subtitle>\n        </ion-card-header>\n\n        <ion-card-content>\n          <ion-row>\n            <ion-col [ngSwitch]=\"picking_type.code\">\n              <ion-button size=\"small\" class=\"button-text\" (click)=\"open_link(picking_type.id, 'ready', picking_type.code)\" *ngSwitchCase=\"'incoming'\">{{picking_type.count_picking_ready}} por recibir</ion-button>\n              <ion-button size=\"small\" class=\"button-text\" (click)=\"open_link(picking_type.id, 'ready', picking_type.code)\" *ngSwitchCase=\"'outgoing'\">{{picking_type.count_picking_ready}} por hacer</ion-button>\n              <ion-button size=\"small\" class=\"button-text\" (click)=\"open_link(picking_type.id, 'ready', picking_type.code)\" *ngSwitchCase=\"'internal'\">{{picking_type.count_picking_ready}} traspasos</ion-button>\n            </ion-col>\n            <ion-col>\n              <div class=\"link\" (click)=\"open_link(picking_type.id, 'waiting', picking_type.code)\">{{picking_type.count_picking_waiting}} en espera</div>\n              <div class=\"link\" (click)=\"open_link(picking_type.id, 'late', picking_type.code)\" *ngIf=\"picking_type.count_picking_late\">{{picking_type.count_picking_late}} retrasados</div>\n              <ion-progress-bar *ngIf=\"picking_type.count_picking_late\" color=\"primary\" type=\"determinate\" [value]=\"picking_type.rate_picking_late/100\"></ion-progress-bar>\n              <div class=\"link\" (click)=\"open_link(picking_type.id, 'backorders', picking_type.code)\" *ngIf=\"picking_type.count_picking_backorders\">{{picking_type.count_picking_backorders}} pendientes</div>\n              <ion-progress-bar *ngIf=\"picking_type.count_picking_backorders\" color=\"primary\" type=\"determinate\" [value]=\"picking_type.rate_picking_backorders/100\"></ion-progress-bar>\n            </ion-col>\n          </ion-row>\n        </ion-card-content>\n      </ion-card>\n    </ion-col>\n  </ion-row>\n</ion-grid> ");

/***/ }),

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.html":
/*!***********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.html ***!
  \***********************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-header>\n    <ion-toolbar>\n      <ion-buttons slot=\"start\">\n        <ion-menu-button></ion-menu-button>\n      </ion-buttons>\n      <ion-title>Inventario</ion-title>\n    </ion-toolbar>\n  </ion-header>\n  \n  <ion-content>\n    <ion-card>\n      <ion-row *ngIf=\"picking_menu\">\n        <ion-col col-2 class=\"ion-align-self-center ion-text-center\" \n          [ngClass]=\"{'selected': current_selected_type == option.value}\" \n          *ngFor=\"let option of picking_menu\" \n          (click)=\"get_picking_types(option.value, search)\">\n          <ion-icon class=\"icon\" [name]=\"option.icon\"></ion-icon\n          >\n          <br/>\n          {{option.name}}\n        </ion-col>\n      </ion-row>\n\n      <ion-row>\n        <ion-toolbar>\n          <ion-searchbar type=\"text\" (ionInput)=\"get_search_results($event)\" autocomplete=\"on\" showCancelButton=\"always\"></ion-searchbar>\n        </ion-toolbar>\n      </ion-row>\n    </ion-card>\n    <ion-card>\n      <app-picking-type-info [picking_types]=\"picking_types\"></app-picking-type-info>\n    </ion-card>\n\n    <ion-infinite-scroll threshold=\"100px\" (ionInfinite)=\"loadData($event)\">\n      <ion-infinite-scroll-content\n        loadingSpinner=\"bubbles\"\n        loadingText=\"Cargando más productos...\">\n      </ion-infinite-scroll-content>\n    </ion-infinite-scroll>\n  </ion-content>\n  ");

/***/ }),

/***/ "./src/app/components/picking-type-info/picking-type-info.component.scss":
/*!*******************************************************************************!*\
  !*** ./src/app/components/picking-type-info/picking-type-info.component.scss ***!
  \*******************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("ion-card ion-card-header {\n  min-height: 81px;\n}\nion-card ion-card-header ion-card-subtitle.success {\n  color: var(--ion-color-success);\n}\nion-card ion-card-header ion-card-subtitle.warning {\n  color: var(--ion-color-warning);\n}\nion-card ion-card-header ion-card-subtitle.primary {\n  color: var(--ion-color-primary);\n}\nion-card ion-card-header ion-card-subtitle.secondary {\n  color: var(--ion-color-secondary);\n}\nion-card ion-card-header ion-card-subtitle.tertiary {\n  color: var(--ion-color-tertiary);\n}\nion-card ion-card-header ion-card-subtitle.medium {\n  color: var(--ion-color-medium);\n}\nion-card ion-card-content {\n  min-height: 94px;\n}\nion-card .link {\n  color: blue;\n  cursor: pointer;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL2NvbXBvbmVudHMvcGlja2luZy10eXBlLWluZm8vcGlja2luZy10eXBlLWluZm8uY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL2NvbXBvbmVudHMvcGlja2luZy10eXBlLWluZm8vcGlja2luZy10eXBlLWluZm8uY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQ0k7RUFDSSxnQkFBQTtBQ0FSO0FERVk7RUFDSSwrQkFBQTtBQ0FoQjtBREVZO0VBQ0ksK0JBQUE7QUNBaEI7QURFWTtFQUNJLCtCQUFBO0FDQWhCO0FERVk7RUFDSSxpQ0FBQTtBQ0FoQjtBREVZO0VBQ0ksZ0NBQUE7QUNBaEI7QURFWTtFQUNJLDhCQUFBO0FDQWhCO0FESUk7RUFDSSxnQkFBQTtBQ0ZSO0FESUk7RUFDSSxXQUFBO0VBQ0EsZUFBQTtBQ0ZSIiwiZmlsZSI6InNyYy9hcHAvY29tcG9uZW50cy9waWNraW5nLXR5cGUtaW5mby9waWNraW5nLXR5cGUtaW5mby5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbImlvbi1jYXJkIHtcbiAgICBpb24tY2FyZC1oZWFkZXIge1xuICAgICAgICBtaW4taGVpZ2h0OiA4MXB4O1xuICAgICAgICBpb24tY2FyZC1zdWJ0aXRsZSB7XG4gICAgICAgICAgICAmLnN1Y2Nlc3Mge1xuICAgICAgICAgICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc3VjY2Vzcyk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICAmLndhcm5pbmcge1xuICAgICAgICAgICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itd2FybmluZyk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICAmLnByaW1hcnkge1xuICAgICAgICAgICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICAmLnNlY29uZGFyeSB7XG4gICAgICAgICAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zZWNvbmRhcnkpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgJi50ZXJ0aWFyeSB7XG4gICAgICAgICAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci10ZXJ0aWFyeSk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICAmLm1lZGl1bSB7XG4gICAgICAgICAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1tZWRpdW0pO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuICAgIGlvbi1jYXJkLWNvbnRlbnQge1xuICAgICAgICBtaW4taGVpZ2h0OiA5NHB4O1xuICAgIH1cbiAgICAubGluayB7XG4gICAgICAgIGNvbG9yOiBibHVlO1xuICAgICAgICBjdXJzb3I6IHBvaW50ZXI7IFxuICAgIH1cbn0iLCJpb24tY2FyZCBpb24tY2FyZC1oZWFkZXIge1xuICBtaW4taGVpZ2h0OiA4MXB4O1xufVxuaW9uLWNhcmQgaW9uLWNhcmQtaGVhZGVyIGlvbi1jYXJkLXN1YnRpdGxlLnN1Y2Nlc3Mge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXN1Y2Nlc3MpO1xufVxuaW9uLWNhcmQgaW9uLWNhcmQtaGVhZGVyIGlvbi1jYXJkLXN1YnRpdGxlLndhcm5pbmcge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXdhcm5pbmcpO1xufVxuaW9uLWNhcmQgaW9uLWNhcmQtaGVhZGVyIGlvbi1jYXJkLXN1YnRpdGxlLnByaW1hcnkge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXByaW1hcnkpO1xufVxuaW9uLWNhcmQgaW9uLWNhcmQtaGVhZGVyIGlvbi1jYXJkLXN1YnRpdGxlLnNlY29uZGFyeSB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc2Vjb25kYXJ5KTtcbn1cbmlvbi1jYXJkIGlvbi1jYXJkLWhlYWRlciBpb24tY2FyZC1zdWJ0aXRsZS50ZXJ0aWFyeSB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItdGVydGlhcnkpO1xufVxuaW9uLWNhcmQgaW9uLWNhcmQtaGVhZGVyIGlvbi1jYXJkLXN1YnRpdGxlLm1lZGl1bSB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItbWVkaXVtKTtcbn1cbmlvbi1jYXJkIGlvbi1jYXJkLWNvbnRlbnQge1xuICBtaW4taGVpZ2h0OiA5NHB4O1xufVxuaW9uLWNhcmQgLmxpbmsge1xuICBjb2xvcjogYmx1ZTtcbiAgY3Vyc29yOiBwb2ludGVyO1xufSJdfQ== */");

/***/ }),

/***/ "./src/app/components/picking-type-info/picking-type-info.component.ts":
/*!*****************************************************************************!*\
  !*** ./src/app/components/picking-type-info/picking-type-info.component.ts ***!
  \*****************************************************************************/
/*! exports provided: PickingTypeInfoComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PickingTypeInfoComponent", function() { return PickingTypeInfoComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");



var PickingTypeInfoComponent = /** @class */ (function () {
    function PickingTypeInfoComponent(router) {
        this.router = router;
    }
    PickingTypeInfoComponent.prototype.ngOnInit = function () { };
    PickingTypeInfoComponent.prototype.open_link = function (pick_type, view, code) {
        this.router.navigateByUrl('/stock-picking-list/' + pick_type + '/' + view + '/' + code);
    };
    PickingTypeInfoComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)
    ], PickingTypeInfoComponent.prototype, "picking_types", void 0);
    PickingTypeInfoComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-picking-type-info',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./picking-type-info.component.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/picking-type-info/picking-type-info.component.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./picking-type-info.component.scss */ "./src/app/components/picking-type-info/picking-type-info.component.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]])
    ], PickingTypeInfoComponent);
    return PickingTypeInfoComponent;
}());



/***/ }),

/***/ "./src/app/pages/stock-picking-type-list/stock-picking-type-list.module.ts":
/*!*********************************************************************************!*\
  !*** ./src/app/pages/stock-picking-type-list/stock-picking-type-list.module.ts ***!
  \*********************************************************************************/
/*! exports provided: StockPickingTypeListPageModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockPickingTypeListPageModule", function() { return StockPickingTypeListPageModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _stock_picking_type_list_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./stock-picking-type-list.page */ "./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.ts");
/* harmony import */ var _components_picking_type_info_picking_type_info_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../components/picking-type-info/picking-type-info.component */ "./src/app/components/picking-type-info/picking-type-info.component.ts");








var routes = [
    {
        path: '',
        component: _stock_picking_type_list_page__WEBPACK_IMPORTED_MODULE_6__["StockPickingTypeListPage"]
    }
];
var StockPickingTypeListPageModule = /** @class */ (function () {
    function StockPickingTypeListPageModule() {
    }
    StockPickingTypeListPageModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes)
            ],
            entryComponents: [_components_picking_type_info_picking_type_info_component__WEBPACK_IMPORTED_MODULE_7__["PickingTypeInfoComponent"]],
            declarations: [_stock_picking_type_list_page__WEBPACK_IMPORTED_MODULE_6__["StockPickingTypeListPage"], _components_picking_type_info_picking_type_info_component__WEBPACK_IMPORTED_MODULE_7__["PickingTypeInfoComponent"]]
        })
    ], StockPickingTypeListPageModule);
    return StockPickingTypeListPageModule;
}());



/***/ }),

/***/ "./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.scss":
/*!*********************************************************************************!*\
  !*** ./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.scss ***!
  \*********************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("ion-icon.icon {\n  font-size: 45px;\n  color: var(--ion-color-secondary);\n  cursor: pointer;\n}\n\nion-col.selected ion-icon.icon {\n  color: var(--ion-color-primary);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL3BhZ2VzL3N0b2NrLXBpY2tpbmctdHlwZS1saXN0L3N0b2NrLXBpY2tpbmctdHlwZS1saXN0LnBhZ2Uuc2NzcyIsInNyYy9hcHAvcGFnZXMvc3RvY2stcGlja2luZy10eXBlLWxpc3Qvc3RvY2stcGlja2luZy10eXBlLWxpc3QucGFnZS5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0ksZUFBQTtFQUNBLGlDQUFBO0VBQ0EsZUFBQTtBQ0NKOztBREdJO0VBQ0ksK0JBQUE7QUNBUiIsImZpbGUiOiJzcmMvYXBwL3BhZ2VzL3N0b2NrLXBpY2tpbmctdHlwZS1saXN0L3N0b2NrLXBpY2tpbmctdHlwZS1saXN0LnBhZ2Uuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbImlvbi1pY29uLmljb24ge1xuICAgIGZvbnQtc2l6ZTogNDVweDtcbiAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXNlY29uZGFyeSk7XG4gICAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG5pb24tY29sLnNlbGVjdGVkIHtcbiAgICBpb24taWNvbi5pY29uIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1wcmltYXJ5KTtcbiAgICB9XG59IiwiaW9uLWljb24uaWNvbiB7XG4gIGZvbnQtc2l6ZTogNDVweDtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zZWNvbmRhcnkpO1xuICBjdXJzb3I6IHBvaW50ZXI7XG59XG5cbmlvbi1jb2wuc2VsZWN0ZWQgaW9uLWljb24uaWNvbiB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG59Il19 */");

/***/ }),

/***/ "./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.ts":
/*!*******************************************************************************!*\
  !*** ./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.ts ***!
  \*******************************************************************************/
/*! exports provided: StockPickingTypeListPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockPickingTypeListPage", function() { return StockPickingTypeListPage; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");







var StockPickingTypeListPage = /** @class */ (function () {
    function StockPickingTypeListPage(odoo, router, alertCtrl, audio, stock) {
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.audio = audio;
        this.stock = stock;
        this.picking_menu = [
            {
                'value': 'all',
                'name': 'Todos',
                'icon': 'book',
                'size': 3
            },
            {
                'value': 'incoming',
                'name': 'Por recibir',
                'icon': 'log-in',
                'size': 3
            },
            {
                'value': 'internal',
                'name': 'Traspasos',
                'icon': 'sync',
                'size': 3
            },
            {
                'value': 'outgoing',
                'name': 'Por hacer',
                'icon': 'log-out',
                'size': 3
            }
        ];
        this.offset = 0;
        this.limit = 25;
        this.limit_reached = false;
        this.picking_codes = [
            'incoming',
            'outgoing',
            'internal'
        ];
    }
    StockPickingTypeListPage.prototype.ngOnInit = function () {
        var _this = this;
        this.odoo.isLoggedIn().then(function (data) {
            if (data == false) {
                _this.router.navigateByUrl('/login');
            }
            else {
                _this.get_picking_types();
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    StockPickingTypeListPage.prototype.presentAlert = function (titulo, texto) {
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
    StockPickingTypeListPage.prototype.get_picking_types = function (picking_state, search) {
        var _this = this;
        if (picking_state === void 0) { picking_state = null; }
        if (search === void 0) { search = null; }
        if (picking_state && picking_state != 'all') {
            this.current_selected_type = picking_state;
            picking_state = [picking_state];
        }
        else {
            this.current_selected_type = 'all';
            picking_state = this.picking_codes;
        }
        this.offset = 0;
        this.limit_reached = false;
        this.stock.get_picking_types(picking_state, this.offset, this.limit, search).then(function (picking_type_list) {
            _this.picking_types = picking_type_list;
            if (Object.keys(picking_type_list).length < 25) {
                _this.limit_reached = true;
            }
            _this.audio.play('click');
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperador el listado de operaciones:', error);
        });
    };
    StockPickingTypeListPage.prototype.get_search_results = function (ev) {
        this.search = ev.target.value;
        this.get_picking_types(this.current_selected_type, this.search);
    };
    // Infinitescroll
    StockPickingTypeListPage.prototype.loadData = function (event) {
        var _this = this;
        setTimeout(function () {
            console.log('Loading more locations');
            event.target.complete();
            _this.picking_list_infinite_scroll_add();
            // App logic to determine if all data is loaded
            // and disable the infinite scroll
            if (_this.limit_reached) {
                event.target.disabled = true;
            }
        }, 500);
    };
    StockPickingTypeListPage.prototype.picking_list_infinite_scroll_add = function () {
        var _this = this;
        this.offset += this.limit;
        var picking_state;
        if (this.current_selected_type == 'all') {
            picking_state = this.picking_codes;
        }
        else {
            picking_state = [this.current_selected_type];
        }
        this.stock.get_picking_types(picking_state, this.offset, this.limit, this.search).then(function (picking_type_list) {
            var current_length = Object.keys(_this.picking_types).length;
            if (Object.keys(picking_type_list).length < 25) {
                _this.limit_reached = true;
            }
            for (var k in picking_type_list)
                _this.picking_types[current_length + Number(k)] = picking_type_list[k];
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperador el listado de operaciones:', error);
        });
    };
    StockPickingTypeListPage.prototype.toggleInfiniteScroll = function () {
        this.infiniteScroll.disabled = !this.infiniteScroll.disabled;
    };
    StockPickingTypeListPage.ctorParameters = function () { return [
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])(_ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"], { static: false }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"])
    ], StockPickingTypeListPage.prototype, "infiniteScroll", void 0);
    StockPickingTypeListPage = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-stock-picking-type-list',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./stock-picking-type-list.page.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./stock-picking-type-list.page.scss */ "./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"]])
    ], StockPickingTypeListPage);
    return StockPickingTypeListPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-stock-picking-type-list-stock-picking-type-list-module.js.map
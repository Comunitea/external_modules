(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-stock-picking-type-list-stock-picking-type-list-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/components/picking-type-info/picking-type-info.component.html":
/*!*********************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/components/picking-type-info/picking-type-info.component.html ***!
  \*********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-grid>\n  <ion-row>\n    <ion-col size-xs=\"12\" size-sm=\"6\" size-lg=\"4\" *ngFor=\"let picking_type of picking_types\">\n      <ion-card>\n        <ion-card-header>\n          <ion-card-title>{{picking_type.name}}</ion-card-title>\n          <ion-card-subtitle [ngClass]=\"{ \n            'primary': picking_type.color == 0, \n            'secondary': picking_type.color == 1, \n            'tertiary': picking_type.color == 2, \n            'medium': picking_type.color == 3,\n            'success': picking_type.color == 4,\n            'warning': picking_type.color == 5}\">{{picking_type.warehouse_id[1]}}</ion-card-subtitle>\n        </ion-card-header>\n    \n        <ion-card-content>\n          <ion-row>\n            <ion-col [ngSwitch]=\"picking_type.code\">\n              <ion-button size=\"small\" class=\"button-text\" (click)=\"open_link(picking_type.id, 'ready', picking_type.group_code)\" *ngSwitchCase=\"'incoming'\">{{picking_type.count_picking_ready}} por recibir</ion-button>\n              <ion-button size=\"small\" class=\"button-text\" (click)=\"open_link(picking_type.id, 'ready', picking_type.group_code)\" *ngSwitchCase=\"'outgoing'\">{{picking_type.count_picking_ready}} por hacer</ion-button>\n              <ion-button size=\"small\" class=\"button-text\" (click)=\"open_link(picking_type.id, 'ready', picking_type.group_code)\" *ngSwitchCase=\"'internal'\">{{picking_type.count_picking_ready}} traspasos</ion-button>\n            </ion-col>\n            <ion-col>\n              <div class=\"link\" (click)=\"open_link(picking_type.id, 'waiting', picking_type.group_code)\">{{picking_type.count_picking_waiting}} en espera</div>\n              <div class=\"link\" (click)=\"open_link(picking_type.id, 'late', picking_type.group_code)\" *ngIf=\"picking_type.count_picking_late\">{{picking_type.count_picking_late}} retrasados</div>\n              <ion-progress-bar *ngIf=\"picking_type.count_picking_late\" color=\"primary\" type=\"determinate\" [value]=\"picking_type.rate_picking_late/100\"></ion-progress-bar>\n              <div class=\"link\" (click)=\"open_link(picking_type.id, 'backorders', picking_type.group_code)\" *ngIf=\"picking_type.count_picking_backorders\">{{picking_type.count_picking_backorders}} pendientes</div>\n              <ion-progress-bar *ngIf=\"picking_type.count_picking_backorders\" color=\"primary\" type=\"determinate\" [value]=\"picking_type.rate_picking_backorders/100\"></ion-progress-bar>\n            </ion-col>\n          </ion-row>\n        </ion-card-content>\n      </ion-card>\n    </ion-col>\n  </ion-row>\n</ion-grid>"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.html":
/*!***********************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.html ***!
  \***********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-header>\n    <ion-toolbar>\n      <ion-buttons slot=\"start\">\n        <ion-menu-button></ion-menu-button>\n      </ion-buttons>\n      <ion-title>Inventario</ion-title>\n    </ion-toolbar>\n  </ion-header>\n  \n  <ion-content>\n    <ion-card>\n      <ion-row *ngIf=\"picking_menu\">\n        <ion-col col-2 class=\"ion-align-self-center ion-text-center\" \n          [ngClass]=\"{'selected': current_selected_type == option.value}\" \n          *ngFor=\"let option of picking_menu\" \n          (click)=\"get_picking_types(option.value, search)\">\n          <ion-icon class=\"icon\" [name]=\"option.icon\"></ion-icon\n          >\n          <br/>\n          {{option.name}}\n        </ion-col>\n      </ion-row>\n\n      <ion-row>\n        <ion-toolbar>\n          <ion-searchbar type=\"text\" (ionInput)=\"get_search_results($event)\" autocomplete=\"on\" showCancelButton=\"always\"></ion-searchbar>\n        </ion-toolbar>\n      </ion-row>\n    </ion-card>\n    <ion-card>\n      <app-picking-type-info [picking_types]=\"picking_types\"></app-picking-type-info>\n    </ion-card>\n\n    <ion-infinite-scroll threshold=\"100px\" (ionInfinite)=\"loadData($event)\">\n      <ion-infinite-scroll-content\n        loadingSpinner=\"bubbles\"\n        loadingText=\"Cargando más productos...\">\n      </ion-infinite-scroll-content>\n    </ion-infinite-scroll>\n  </ion-content>\n  "

/***/ }),

/***/ "./src/app/components/picking-type-info/picking-type-info.component.scss":
/*!*******************************************************************************!*\
  !*** ./src/app/components/picking-type-info/picking-type-info.component.scss ***!
  \*******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "ion-card ion-card-header {\n  min-height: 81px;\n}\nion-card ion-card-header ion-card-subtitle.success {\n  color: var(--ion-color-success);\n}\nion-card ion-card-header ion-card-subtitle.warning {\n  color: var(--ion-color-warning);\n}\nion-card ion-card-header ion-card-subtitle.primary {\n  color: var(--ion-color-primary);\n}\nion-card ion-card-header ion-card-subtitle.secondary {\n  color: var(--ion-color-secondary);\n}\nion-card ion-card-header ion-card-subtitle.tertiary {\n  color: var(--ion-color-tertiary);\n}\nion-card ion-card-header ion-card-subtitle.medium {\n  color: var(--ion-color-medium);\n}\nion-card ion-card-content {\n  min-height: 94px;\n}\nion-card .link {\n  color: blue;\n  cursor: pointer;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9jb21wb25lbnRzL3BpY2tpbmctdHlwZS1pbmZvL3BpY2tpbmctdHlwZS1pbmZvLmNvbXBvbmVudC5zY3NzIiwic3JjL2FwcC9jb21wb25lbnRzL3BpY2tpbmctdHlwZS1pbmZvL3BpY2tpbmctdHlwZS1pbmZvLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUNJO0VBQ0ksZ0JBQUE7QUNBUjtBREVZO0VBQ0ksK0JBQUE7QUNBaEI7QURFWTtFQUNJLCtCQUFBO0FDQWhCO0FERVk7RUFDSSwrQkFBQTtBQ0FoQjtBREVZO0VBQ0ksaUNBQUE7QUNBaEI7QURFWTtFQUNJLGdDQUFBO0FDQWhCO0FERVk7RUFDSSw4QkFBQTtBQ0FoQjtBRElJO0VBQ0ksZ0JBQUE7QUNGUjtBRElJO0VBQ0ksV0FBQTtFQUNBLGVBQUE7QUNGUiIsImZpbGUiOiJzcmMvYXBwL2NvbXBvbmVudHMvcGlja2luZy10eXBlLWluZm8vcGlja2luZy10eXBlLWluZm8uY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJpb24tY2FyZCB7XG4gICAgaW9uLWNhcmQtaGVhZGVyIHtcbiAgICAgICAgbWluLWhlaWdodDogODFweDtcbiAgICAgICAgaW9uLWNhcmQtc3VidGl0bGUge1xuICAgICAgICAgICAgJi5zdWNjZXNzIHtcbiAgICAgICAgICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXN1Y2Nlc3MpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgJi53YXJuaW5nIHtcbiAgICAgICAgICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXdhcm5pbmcpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgJi5wcmltYXJ5IHtcbiAgICAgICAgICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXByaW1hcnkpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgJi5zZWNvbmRhcnkge1xuICAgICAgICAgICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc2Vjb25kYXJ5KTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgICYudGVydGlhcnkge1xuICAgICAgICAgICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItdGVydGlhcnkpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgJi5tZWRpdW0ge1xuICAgICAgICAgICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItbWVkaXVtKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH1cbiAgICBpb24tY2FyZC1jb250ZW50IHtcbiAgICAgICAgbWluLWhlaWdodDogOTRweDtcbiAgICB9XG4gICAgLmxpbmsge1xuICAgICAgICBjb2xvcjogYmx1ZTtcbiAgICAgICAgY3Vyc29yOiBwb2ludGVyOyBcbiAgICB9XG59IiwiaW9uLWNhcmQgaW9uLWNhcmQtaGVhZGVyIHtcbiAgbWluLWhlaWdodDogODFweDtcbn1cbmlvbi1jYXJkIGlvbi1jYXJkLWhlYWRlciBpb24tY2FyZC1zdWJ0aXRsZS5zdWNjZXNzIHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zdWNjZXNzKTtcbn1cbmlvbi1jYXJkIGlvbi1jYXJkLWhlYWRlciBpb24tY2FyZC1zdWJ0aXRsZS53YXJuaW5nIHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci13YXJuaW5nKTtcbn1cbmlvbi1jYXJkIGlvbi1jYXJkLWhlYWRlciBpb24tY2FyZC1zdWJ0aXRsZS5wcmltYXJ5IHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1wcmltYXJ5KTtcbn1cbmlvbi1jYXJkIGlvbi1jYXJkLWhlYWRlciBpb24tY2FyZC1zdWJ0aXRsZS5zZWNvbmRhcnkge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXNlY29uZGFyeSk7XG59XG5pb24tY2FyZCBpb24tY2FyZC1oZWFkZXIgaW9uLWNhcmQtc3VidGl0bGUudGVydGlhcnkge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXRlcnRpYXJ5KTtcbn1cbmlvbi1jYXJkIGlvbi1jYXJkLWhlYWRlciBpb24tY2FyZC1zdWJ0aXRsZS5tZWRpdW0ge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLW1lZGl1bSk7XG59XG5pb24tY2FyZCBpb24tY2FyZC1jb250ZW50IHtcbiAgbWluLWhlaWdodDogOTRweDtcbn1cbmlvbi1jYXJkIC5saW5rIHtcbiAgY29sb3I6IGJsdWU7XG4gIGN1cnNvcjogcG9pbnRlcjtcbn0iXX0= */"

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");



let PickingTypeInfoComponent = class PickingTypeInfoComponent {
    constructor(router) {
        this.router = router;
    }
    ngOnInit() { }
    open_link(pick_type, view, code) {
        this.router.navigateByUrl('/stock-picking-list/' + pick_type + '/' + view + '/' + code);
    }
};
PickingTypeInfoComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] }
];
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
], PickingTypeInfoComponent.prototype, "picking_types", void 0);
PickingTypeInfoComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-picking-type-info',
        template: __webpack_require__(/*! raw-loader!./picking-type-info.component.html */ "./node_modules/raw-loader/index.js!./src/app/components/picking-type-info/picking-type-info.component.html"),
        styles: [__webpack_require__(/*! ./picking-type-info.component.scss */ "./src/app/components/picking-type-info/picking-type-info.component.scss")]
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]])
], PickingTypeInfoComponent);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _stock_picking_type_list_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./stock-picking-type-list.page */ "./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.ts");
/* harmony import */ var _components_picking_type_info_picking_type_info_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../components/picking-type-info/picking-type-info.component */ "./src/app/components/picking-type-info/picking-type-info.component.ts");








const routes = [
    {
        path: '',
        component: _stock_picking_type_list_page__WEBPACK_IMPORTED_MODULE_6__["StockPickingTypeListPage"]
    }
];
let StockPickingTypeListPageModule = class StockPickingTypeListPageModule {
};
StockPickingTypeListPageModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
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



/***/ }),

/***/ "./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.scss":
/*!*********************************************************************************!*\
  !*** ./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.scss ***!
  \*********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "ion-icon.icon {\n  font-size: 45px;\n  color: var(--ion-color-secondary);\n  cursor: pointer;\n}\n\nion-col.selected ion-icon.icon {\n  color: var(--ion-color-primary);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9wYWdlcy9zdG9jay1waWNraW5nLXR5cGUtbGlzdC9zdG9jay1waWNraW5nLXR5cGUtbGlzdC5wYWdlLnNjc3MiLCJzcmMvYXBwL3BhZ2VzL3N0b2NrLXBpY2tpbmctdHlwZS1saXN0L3N0b2NrLXBpY2tpbmctdHlwZS1saXN0LnBhZ2Uuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNJLGVBQUE7RUFDQSxpQ0FBQTtFQUNBLGVBQUE7QUNDSjs7QURHSTtFQUNJLCtCQUFBO0FDQVIiLCJmaWxlIjoic3JjL2FwcC9wYWdlcy9zdG9jay1waWNraW5nLXR5cGUtbGlzdC9zdG9jay1waWNraW5nLXR5cGUtbGlzdC5wYWdlLnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJpb24taWNvbi5pY29uIHtcbiAgICBmb250LXNpemU6IDQ1cHg7XG4gICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zZWNvbmRhcnkpO1xuICAgIGN1cnNvcjogcG9pbnRlcjtcbn1cblxuaW9uLWNvbC5zZWxlY3RlZCB7XG4gICAgaW9uLWljb24uaWNvbiB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG4gICAgfVxufSIsImlvbi1pY29uLmljb24ge1xuICBmb250LXNpemU6IDQ1cHg7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc2Vjb25kYXJ5KTtcbiAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG5pb24tY29sLnNlbGVjdGVkIGlvbi1pY29uLmljb24ge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXByaW1hcnkpO1xufSJdfQ== */"

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");







let StockPickingTypeListPage = class StockPickingTypeListPage {
    constructor(odoo, router, alertCtrl, audio, stock) {
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
    ngOnInit() {
        this.odoo.isLoggedIn().then((data) => {
            if (data == false) {
                this.router.navigateByUrl('/login');
            }
            else {
                this.get_picking_types();
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
    get_picking_types(picking_state = null, search = null) {
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
        this.stock.get_picking_types(picking_state, this.offset, this.limit, search).then((picking_type_list) => {
            this.picking_types = picking_type_list;
            if (Object.keys(picking_type_list).length < 25) {
                this.limit_reached = true;
            }
            this.audio.play('click');
        })
            .catch((error) => {
            this.presentAlert('Error al recuperador el listado de operaciones:', error);
        });
    }
    get_search_results(ev) {
        this.search = ev.target.value;
        this.get_picking_types(this.current_selected_type, this.search);
    }
    // Infinitescroll
    loadData(event) {
        setTimeout(() => {
            console.log('Loading more locations');
            event.target.complete();
            this.picking_list_infinite_scroll_add();
            // App logic to determine if all data is loaded
            // and disable the infinite scroll
            if (this.limit_reached) {
                event.target.disabled = true;
            }
        }, 500);
    }
    picking_list_infinite_scroll_add() {
        this.offset += this.limit;
        let picking_state;
        if (this.current_selected_type == 'all') {
            picking_state = this.picking_codes;
        }
        else {
            picking_state = [this.current_selected_type];
        }
        this.stock.get_picking_types(picking_state, this.offset, this.limit, this.search).then((picking_type_list) => {
            let current_length = Object.keys(this.picking_types).length;
            if (Object.keys(picking_type_list).length < 25) {
                this.limit_reached = true;
            }
            for (var k in picking_type_list)
                this.picking_types[current_length + Number(k)] = picking_type_list[k];
        })
            .catch((error) => {
            this.presentAlert('Error al recuperador el listado de operaciones:', error);
        });
    }
    toggleInfiniteScroll() {
        this.infiniteScroll.disabled = !this.infiniteScroll.disabled;
    }
};
StockPickingTypeListPage.ctorParameters = () => [
    { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"] },
    { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"] },
    { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"] }
];
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])(_ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"], { static: false }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"])
], StockPickingTypeListPage.prototype, "infiniteScroll", void 0);
StockPickingTypeListPage = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-stock-picking-type-list',
        template: __webpack_require__(/*! raw-loader!./stock-picking-type-list.page.html */ "./node_modules/raw-loader/index.js!./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.html"),
        styles: [__webpack_require__(/*! ./stock-picking-type-list.page.scss */ "./src/app/pages/stock-picking-type-list/stock-picking-type-list.page.scss")]
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
        _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
        _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
        _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"],
        _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"]])
], StockPickingTypeListPage);



/***/ })

}]);
//# sourceMappingURL=pages-stock-picking-type-list-stock-picking-type-list-module-es2015.js.map
(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-stock-location-list-stock-location-list-module"],{

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/location-list/location-list.component.html":
/*!*************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/components/location-list/location-list.component.html ***!
  \*************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-grid>\n  <ion-row>\n    <ion-col size=\"12\">\n        <div><strong>Nombre</strong></div>\n    </ion-col>\n    \n    <!--ion-col size=\"4\">\n        <div><strong>Tipo de ubicación</strong></div>\n    </ion-col>\n  \n    <ion-col size=\"4\">\n      <div><strong>Compañía</strong></div>\n    </ion-col-->\n  </ion-row>\n  \n  <ion-row *ngFor=\"let location of locations\" (click)=\"open_link(location.id)\">\n    <ion-col size-xs=\"12\" size-sm=\"4\" size-md=\"4\">\n      <div>{{location.display_name}}</div>\n    </ion-col>\n  \n    <ion-col size-xs=\"6\" size-sm=\"4\" size-md=\"4\" [ngSwitch]=\"location.usage\" class=\"ion-align-self-center ion-text-center\">\n      <div *ngSwitchCase=\"'supplier'\"><strong class=\"ion-hide-sm-up\">Tipo: </strong>Ubicación de proveedor</div>\n      <div *ngSwitchCase=\"'view'\"><strong class=\"ion-hide-sm-up\">Tipo: </strong>Ver</div>\n      <div *ngSwitchCase=\"'internal'\"><strong class=\"ion-hide-sm-up\">Tipo: </strong>Ubicación interna</div>\n      <div *ngSwitchCase=\"'customer'\"><strong class=\"ion-hide-sm-up\">Tipo: </strong>Ubicación de cliente</div>\n      <div *ngSwitchCase=\"'inventory'\"><strong class=\"ion-hide-sm-up\">Tipo: </strong>Ubicación de inventario</div>\n      <div *ngSwitchCase=\"'procurement'\"><strong class=\"ion-hide-sm-up\">Tipo: </strong>Abastecimiento</div>\n      <div *ngSwitchCase=\"'production'\"><strong class=\"ion-hide-sm-up\">Tipo: </strong>Producción</div>\n      <div *ngSwitchCase=\"'transit'\"><strong class=\"ion-hide-sm-up\">Tipo: </strong>Ubicación de tránsito</div>\n    </ion-col>\n    \n    <ion-col size-xs=\"6\" size-sm=\"4\" size-md=\"4\">\n      <div>\n        <strong class=\"ion-hide-sm-up\">Compañía: </strong>{{location.company_id[1]}}\n      </div>\n    </ion-col>\n  </ion-row>\n</ion-grid>");

/***/ }),

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-location-list/stock-location-list.page.html":
/*!***************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-location-list/stock-location-list.page.html ***!
  \***************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"start\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n    <app-scanner-header slot=\"end\"></app-scanner-header>\n    <ion-title>Listado de ubicaciones</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <ion-card>\n    <ion-row *ngIf=\"location_types\">\n      <ion-col col-2 class=\"ion-align-self-center ion-text-center\" [ngClass]=\"{'selected': current_selected_type == option.value}\" *ngFor=\"let option of location_types\" (click)=\"get_location_list(option.value, search)\">\n        <ion-icon class=\"icon\" [name]=\"option.icon\"></ion-icon><br/>\n        {{option.name}}\n      </ion-col>\n    </ion-row>\n  </ion-card>\n  <ion-card>\n    <ion-card-content>\n      <ion-row>\n        <ion-toolbar>\n          <ion-searchbar type=\"text\" (ionInput)=\"get_search_results($event)\" autocomplete=\"on\" showCancelButton=\"always\"></ion-searchbar>\n        </ion-toolbar>\n      </ion-row>   \n      \n      <app-location-list [locations]=\"locations\"></app-location-list>\n\n      <ion-infinite-scroll threshold=\"100px\" (ionInfinite)=\"loadData($event)\">\n        <ion-infinite-scroll-content\n          loadingSpinner=\"bubbles\"\n          loadingText=\"Cargando más productos...\">\n        </ion-infinite-scroll-content>\n      </ion-infinite-scroll>\n    </ion-card-content>\n  </ion-card>\n</ion-content>\n\n<app-scanner-footer (scanner_reading_changed)=\"onReadingEmitted($event)\" [scanner_reading]=\"scanner_reading\"></app-scanner-footer>\n");

/***/ }),

/***/ "./src/app/components/location-list/location-list.component.scss":
/*!***********************************************************************!*\
  !*** ./src/app/components/location-list/location-list.component.scss ***!
  \***********************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("ion-col {\n  cursor: pointer;\n}\nion-col.success {\n  color: var(--ion-color-success);\n}\nion-col.danger {\n  color: var(--ion-color-danger);\n}\nion-col.primary {\n  color: var(--ion-color-primary);\n}\nion-col.secondary {\n  color: var(--ion-color-secondary);\n}\nion-col.tertiary {\n  color: var(--ion-color-tertiary);\n}\nion-col.medium {\n  color: var(--ion-color-medium);\n}\n/* Medias */\n@media screen and (max-width: 576px) {\n  ion-grid > ion-row:first-child {\n    display: none;\n  }\n\n  ion-grid > ion-row {\n    border: 1px black solid;\n  }\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL2NvbXBvbmVudHMvbG9jYXRpb24tbGlzdC9sb2NhdGlvbi1saXN0LmNvbXBvbmVudC5zY3NzIiwic3JjL2FwcC9jb21wb25lbnRzL2xvY2F0aW9uLWxpc3QvbG9jYXRpb24tbGlzdC5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQW1CSSxlQUFBO0FDakJKO0FEREk7RUFDSSwrQkFBQTtBQ0dSO0FEREk7RUFDSSw4QkFBQTtBQ0dSO0FEREk7RUFDSSwrQkFBQTtBQ0dSO0FEREk7RUFDSSxpQ0FBQTtBQ0dSO0FEREk7RUFDSSxnQ0FBQTtBQ0dSO0FEREk7RUFDSSw4QkFBQTtBQ0dSO0FERUEsV0FBQTtBQUNBO0VBQ0k7SUFDSSxhQUFBO0VDQ047O0VEQ0U7SUFDSSx1QkFBQTtFQ0VOO0FBQ0YiLCJmaWxlIjoic3JjL2FwcC9jb21wb25lbnRzL2xvY2F0aW9uLWxpc3QvbG9jYXRpb24tbGlzdC5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbImlvbi1jb2wge1xuICAgICYuc3VjY2VzcyB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc3VjY2Vzcyk7XG4gICAgfVxuICAgICYuZGFuZ2VyIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1kYW5nZXIpO1xuICAgIH1cbiAgICAmLnByaW1hcnkge1xuICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXByaW1hcnkpO1xuICAgIH1cbiAgICAmLnNlY29uZGFyeSB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc2Vjb25kYXJ5KTtcbiAgICB9XG4gICAgJi50ZXJ0aWFyeSB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItdGVydGlhcnkpO1xuICAgIH1cbiAgICAmLm1lZGl1bSB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItbWVkaXVtKTtcbiAgICB9XG4gICAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG4vKiBNZWRpYXMgKi9cbkBtZWRpYSBzY3JlZW4gYW5kIChtYXgtd2lkdGg6IDU3NnB4KSB7XG4gICAgaW9uLWdyaWQgPiBpb24tcm93OmZpcnN0LWNoaWxkIHtcbiAgICAgICAgZGlzcGxheTogbm9uZTtcbiAgICB9XG4gICAgaW9uLWdyaWQgPiBpb24tcm93IHtcbiAgICAgICAgYm9yZGVyOiAxcHggYmxhY2sgc29saWQ7XG4gICAgfVxufSIsImlvbi1jb2wge1xuICBjdXJzb3I6IHBvaW50ZXI7XG59XG5pb24tY29sLnN1Y2Nlc3Mge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXN1Y2Nlc3MpO1xufVxuaW9uLWNvbC5kYW5nZXIge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLWRhbmdlcik7XG59XG5pb24tY29sLnByaW1hcnkge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXByaW1hcnkpO1xufVxuaW9uLWNvbC5zZWNvbmRhcnkge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXNlY29uZGFyeSk7XG59XG5pb24tY29sLnRlcnRpYXJ5IHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci10ZXJ0aWFyeSk7XG59XG5pb24tY29sLm1lZGl1bSB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItbWVkaXVtKTtcbn1cblxuLyogTWVkaWFzICovXG5AbWVkaWEgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiA1NzZweCkge1xuICBpb24tZ3JpZCA+IGlvbi1yb3c6Zmlyc3QtY2hpbGQge1xuICAgIGRpc3BsYXk6IG5vbmU7XG4gIH1cblxuICBpb24tZ3JpZCA+IGlvbi1yb3cge1xuICAgIGJvcmRlcjogMXB4IGJsYWNrIHNvbGlkO1xuICB9XG59Il19 */");

/***/ }),

/***/ "./src/app/components/location-list/location-list.component.ts":
/*!*********************************************************************!*\
  !*** ./src/app/components/location-list/location-list.component.ts ***!
  \*********************************************************************/
/*! exports provided: LocationListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LocationListComponent", function() { return LocationListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");



var LocationListComponent = /** @class */ (function () {
    function LocationListComponent(router) {
        this.router = router;
    }
    LocationListComponent.prototype.ngOnInit = function () { };
    LocationListComponent.prototype.open_link = function (location_id) {
        this.router.navigateByUrl('/stock-location/' + location_id);
    };
    LocationListComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)
    ], LocationListComponent.prototype, "locations", void 0);
    LocationListComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-location-list',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./location-list.component.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/location-list/location-list.component.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./location-list.component.scss */ "./src/app/components/location-list/location-list.component.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]])
    ], LocationListComponent);
    return LocationListComponent;
}());



/***/ }),

/***/ "./src/app/pages/stock-location-list/stock-location-list.module.ts":
/*!*************************************************************************!*\
  !*** ./src/app/pages/stock-location-list/stock-location-list.module.ts ***!
  \*************************************************************************/
/*! exports provided: StockLocationListPageModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockLocationListPageModule", function() { return StockLocationListPageModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _stock_location_list_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./stock-location-list.page */ "./src/app/pages/stock-location-list/stock-location-list.page.ts");
/* harmony import */ var _components_location_list_location_list_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../components/location-list/location-list.component */ "./src/app/components/location-list/location-list.component.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../shared/shared.module */ "./src/app/shared/shared.module.ts");









var routes = [
    {
        path: '',
        component: _stock_location_list_page__WEBPACK_IMPORTED_MODULE_6__["StockLocationListPage"]
    }
];
var StockLocationListPageModule = /** @class */ (function () {
    function StockLocationListPageModule() {
    }
    StockLocationListPageModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes),
                _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__["SharedModule"]
            ],
            entryComponents: [_components_location_list_location_list_component__WEBPACK_IMPORTED_MODULE_7__["LocationListComponent"]],
            declarations: [_stock_location_list_page__WEBPACK_IMPORTED_MODULE_6__["StockLocationListPage"], _components_location_list_location_list_component__WEBPACK_IMPORTED_MODULE_7__["LocationListComponent"]]
        })
    ], StockLocationListPageModule);
    return StockLocationListPageModule;
}());



/***/ }),

/***/ "./src/app/pages/stock-location-list/stock-location-list.page.scss":
/*!*************************************************************************!*\
  !*** ./src/app/pages/stock-location-list/stock-location-list.page.scss ***!
  \*************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("ion-icon.icon {\n  font-size: 45px;\n  color: var(--ion-color-secondary);\n  cursor: pointer;\n}\n\nion-col.selected ion-icon.icon {\n  color: var(--ion-color-primary);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL3BhZ2VzL3N0b2NrLWxvY2F0aW9uLWxpc3Qvc3RvY2stbG9jYXRpb24tbGlzdC5wYWdlLnNjc3MiLCJzcmMvYXBwL3BhZ2VzL3N0b2NrLWxvY2F0aW9uLWxpc3Qvc3RvY2stbG9jYXRpb24tbGlzdC5wYWdlLnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDSSxlQUFBO0VBQ0EsaUNBQUE7RUFDQSxlQUFBO0FDQ0o7O0FER0k7RUFDSSwrQkFBQTtBQ0FSIiwiZmlsZSI6InNyYy9hcHAvcGFnZXMvc3RvY2stbG9jYXRpb24tbGlzdC9zdG9jay1sb2NhdGlvbi1saXN0LnBhZ2Uuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbImlvbi1pY29uLmljb24ge1xuICAgIGZvbnQtc2l6ZTogNDVweDtcbiAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXNlY29uZGFyeSk7XG4gICAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG5pb24tY29sLnNlbGVjdGVkIHtcbiAgICBpb24taWNvbi5pY29uIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1wcmltYXJ5KTtcbiAgICB9XG59IiwiaW9uLWljb24uaWNvbiB7XG4gIGZvbnQtc2l6ZTogNDVweDtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zZWNvbmRhcnkpO1xuICBjdXJzb3I6IHBvaW50ZXI7XG59XG5cbmlvbi1jb2wuc2VsZWN0ZWQgaW9uLWljb24uaWNvbiB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG59Il19 */");

/***/ }),

/***/ "./src/app/pages/stock-location-list/stock-location-list.page.ts":
/*!***********************************************************************!*\
  !*** ./src/app/pages/stock-location-list/stock-location-list.page.ts ***!
  \***********************************************************************/
/*! exports provided: StockLocationListPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockLocationListPage", function() { return StockLocationListPage; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");







var StockLocationListPage = /** @class */ (function () {
    function StockLocationListPage(odoo, router, alertCtrl, audio, stock) {
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.audio = audio;
        this.stock = stock;
        this.scanner_options = { reader: true, microphone: false, sound: false };
        this.location_types = [
            //{
            //  'value': 'all',
            //  'name': 'Todos',
            // 'icon': 'book',
            //  'size': 2
            //}
            //{
            //  'value': 'supplier',
            //  'name': 'Proveedor',
            //  'icon': 'boat',
            //  'size': 1
            //},
            {
                'value': 'view',
                'name': 'Ver',
                'icon': 'desktop',
                'size': 1
            },
            {
                'value': 'internal',
                'name': 'Interna',
                'icon': 'cube',
                'size': 1
            },
            //{
            //  'value': 'customer',
            //  'name': 'Cliente',
            //  'icon': 'cash',
            // / 'size': 1
            //},
            //{
            //  'value': 'inventory',
            //  'name': 'Inventario',
            //  'icon': 'clipboard',
            //  'size': 1
            //},
            //{
            //  'value': 'procurement',
            //  'name': 'Abastecimiento',
            //  'icon': 'log-in',
            //  'size': 1
            //},
            {
                'value': 'production',
                'name': 'Producción',
                'icon': 'hammer',
                'size': 1
            },
            {
                'value': 'transit',
                'name': 'Tránsito',
                'icon': 'swap',
                'size': 2
            }
        ];
        this.offset = 0;
        this.limit = 25;
        this.limit_reached = false;
    }
    StockLocationListPage.prototype.ngOnInit = function () {
        var _this = this;
        this.odoo.isLoggedIn().then(function (data) {
            if (data == false) {
                _this.router.navigateByUrl('/login');
            }
            else {
                _this.get_location_list('internal');
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    StockLocationListPage.prototype.onReadingEmitted = function (val) {
        this.scanner_reading = val;
        this.search = val;
        this.get_location_list(this.current_selected_type, this.search);
    };
    StockLocationListPage.prototype.presentAlert = function (titulo, texto) {
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
    StockLocationListPage.prototype.get_location_list = function (location_state, search) {
        var _this = this;
        if (location_state === void 0) { location_state = 'internal'; }
        if (search === void 0) { search = null; }
        this.offset = 0;
        this.limit_reached = false;
        this.current_selected_type = location_state;
        this.stock.get_location_list(location_state, this.offset, this.limit, search).then(function (location_list) {
            _this.locations = location_list;
            if (Object.keys(location_list).length < 25) {
                _this.limit_reached = true;
            }
            if (Object.keys(_this.locations).length == 1) {
                _this.router.navigateByUrl('/stock-location/' + _this.locations[0]['id']);
            }
            _this.audio.play('click');
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperador el listado de operaciones:', error);
        });
    };
    StockLocationListPage.prototype.get_search_results = function (ev) {
        this.search = ev.target.value;
        this.get_location_list(this.current_selected_type, this.search);
    };
    // Infinitescroll
    StockLocationListPage.prototype.loadData = function (event) {
        var _this = this;
        setTimeout(function () {
            console.log('Loading more locations');
            event.target.complete();
            _this.location_list_infinite_scroll_add();
            // App logic to determine if all data is loaded
            // and disable the infinite scroll
            if (_this.limit_reached) {
                event.target.disabled = true;
            }
        }, 500);
    };
    StockLocationListPage.prototype.location_list_infinite_scroll_add = function () {
        var _this = this;
        this.offset += this.limit;
        this.stock.get_location_list(this.current_selected_type, this.offset, this.limit, this.search).then(function (data) {
            var current_length = Object.keys(_this.locations).length;
            if (Object.keys(data).length < 25) {
                _this.limit_reached = true;
            }
            for (var k in data)
                _this.locations[current_length + Number(k)] = data[k];
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperador el listado de operaciones:', error);
        });
    };
    StockLocationListPage.prototype.toggleInfiniteScroll = function () {
        this.infiniteScroll.disabled = !this.infiniteScroll.disabled;
    };
    StockLocationListPage.ctorParameters = function () { return [
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])(_ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"], { static: false }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"])
    ], StockLocationListPage.prototype, "infiniteScroll", void 0);
    StockLocationListPage = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-stock-location-list',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./stock-location-list.page.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-location-list/stock-location-list.page.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./stock-location-list.page.scss */ "./src/app/pages/stock-location-list/stock-location-list.page.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"]])
    ], StockLocationListPage);
    return StockLocationListPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-stock-location-list-stock-location-list-module.js.map
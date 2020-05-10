(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-stock-picking-list-stock-picking-list-module"],{

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/picking-list/picking-list.component.html":
/*!***********************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/components/picking-list/picking-list.component.html ***!
  \***********************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-grid *ngIf=\"not_allowed_fields\">\n\n  <ion-row>\n    <ion-col *ngIf=\"not_allowed_fields.indexOf('display_name') == -1\">\n        <div><strong>Nombre</strong></div>\n    </ion-col>\n    \n    <ion-col *ngIf=\"not_allowed_fields.indexOf('location_id') == -1\">\n        <div><strong>Origen</strong></div>\n    </ion-col>\n\n    <ion-col *ngIf=\"not_allowed_fields.indexOf('location_dest_id') == -1\">\n      <div><strong>Destino</strong></div>\n    </ion-col>\n    \n    <ion-col *ngIf=\"not_allowed_fields.indexOf('scheduled_date') == -1\" class=\"ion-align-self-center ion-text-center\">\n      <div><strong>Previsto</strong></div>\n    </ion-col>\n    <ion-col *ngIf=\"not_allowed_fields.indexOf('state') == -1\" class=\"ion-align-self-center ion-text-center\">\n      <div><strong>Estado</strong></div>\n    </ion-col>\n  </ion-row>\n\n  <ion-row *ngFor=\"let pick of picks\" (click)=\"open_link(pick.id, code)\">\n    <ion-col *ngIf=\"not_allowed_fields.indexOf('display_name') == -1\">\n      <div>{{pick.display_name}}</div>\n    </ion-col>\n    \n    <ion-col *ngIf=\"not_allowed_fields.indexOf('location_id') == -1\">\n      <div>{{pick.location_id[1]}}</div>\n    </ion-col>\n  \n    <ion-col *ngIf=\"not_allowed_fields.indexOf('location_dest_id') == -1\">\n      <div>{{pick.location_dest_id[1]}}</div>\n    </ion-col>\n    \n    <ion-col *ngIf=\"not_allowed_fields.indexOf('scheduled_date') == -1\" class=\"ion-align-self-center ion-text-center\">\n      <div>{{pick.scheduled_date}}h</div>\n    </ion-col>\n  \n    <ion-col *ngIf=\"not_allowed_fields.indexOf('state') == -1\"  [ngClass]=\"{'success': pick.state == 'done',\n    'danger': pick.state == 'cancel', \n    'primary': pick.state == 'assigned', \n    'secondary': pick.state == 'confirmed', \n    'tertiary': pick.state == 'waiting', \n    'medium': pick.state == 'draft'}\" [ngSwitch]=\"pick.state\" class=\"ion-align-self-center ion-text-center\">\n      <div *ngSwitchCase=\"'draft'\">Borrador</div>\n      <div *ngSwitchCase=\"'waiting'\">Faltan operaciones</div>\n      <div *ngSwitchCase=\"'confirmed'\">En espera</div>\n      <div *ngSwitchCase=\"'assigned'\">Preparado</div>\n      <div *ngSwitchCase=\"'done'\">Hecho</div>\n      <div *ngSwitchCase=\"'cancel'\">Cancel</div>\n    </ion-col>\n  </ion-row>\n</ion-grid>");

/***/ }),

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-picking-list/stock-picking-list.page.html":
/*!*************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-picking-list/stock-picking-list.page.html ***!
  \*************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"start\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n    <ion-title>Listado de operaciones</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <ion-card>\n    <ion-card-content>\n      <ion-row>\n        <ion-toolbar>\n          <ion-searchbar type=\"text\" (ionInput)=\"get_search_results($event)\" autocomplete=\"on\" showCancelButton=\"always\"></ion-searchbar>\n        </ion-toolbar>\n      </ion-row>\n\n      <app-picking-list [code]=\"current_code\" [not_allowed_fields]=\"not_allowed_fields\" [picks]=\"pickings\"></app-picking-list>\n\n      <ion-infinite-scroll threshold=\"100px\" (ionInfinite)=\"loadData($event)\">\n        <ion-infinite-scroll-content\n          loadingSpinner=\"bubbles\"\n          loadingText=\"Cargando más productos...\">\n        </ion-infinite-scroll-content>\n      </ion-infinite-scroll>\n    </ion-card-content>\n  </ion-card>\n</ion-content>");

/***/ }),

/***/ "./src/app/components/picking-list/picking-list.component.scss":
/*!*********************************************************************!*\
  !*** ./src/app/components/picking-list/picking-list.component.scss ***!
  \*********************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("ion-col {\n  cursor: pointer;\n}\nion-col.success {\n  color: var(--ion-color-success);\n}\nion-col.danger {\n  color: var(--ion-color-danger);\n}\nion-col.primary {\n  color: var(--ion-color-primary);\n}\nion-col.secondary {\n  color: var(--ion-color-secondary);\n}\nion-col.tertiary {\n  color: var(--ion-color-tertiary);\n}\nion-col.medium {\n  color: var(--ion-color-medium);\n}\n/* Medias */\n@media screen and (max-width: 576px) {\n  ion-grid > ion-row:first-child {\n    display: none;\n  }\n\n  ion-grid > ion-row {\n    border: 1px black solid;\n  }\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL2NvbXBvbmVudHMvcGlja2luZy1saXN0L3BpY2tpbmctbGlzdC5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvY29tcG9uZW50cy9waWNraW5nLWxpc3QvcGlja2luZy1saXN0LmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBbUJJLGVBQUE7QUNqQko7QURESTtFQUNJLCtCQUFBO0FDR1I7QURESTtFQUNJLDhCQUFBO0FDR1I7QURESTtFQUNJLCtCQUFBO0FDR1I7QURESTtFQUNJLGlDQUFBO0FDR1I7QURESTtFQUNJLGdDQUFBO0FDR1I7QURESTtFQUNJLDhCQUFBO0FDR1I7QURFQSxXQUFBO0FBQ0E7RUFDSTtJQUNJLGFBQUE7RUNDTjs7RURDRTtJQUNJLHVCQUFBO0VDRU47QUFDRiIsImZpbGUiOiJzcmMvYXBwL2NvbXBvbmVudHMvcGlja2luZy1saXN0L3BpY2tpbmctbGlzdC5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbImlvbi1jb2wge1xuICAgICYuc3VjY2VzcyB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc3VjY2Vzcyk7XG4gICAgfVxuICAgICYuZGFuZ2VyIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1kYW5nZXIpO1xuICAgIH1cbiAgICAmLnByaW1hcnkge1xuICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXByaW1hcnkpO1xuICAgIH1cbiAgICAmLnNlY29uZGFyeSB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc2Vjb25kYXJ5KTtcbiAgICB9XG4gICAgJi50ZXJ0aWFyeSB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItdGVydGlhcnkpO1xuICAgIH1cbiAgICAmLm1lZGl1bSB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItbWVkaXVtKTtcbiAgICB9XG4gICAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG4vKiBNZWRpYXMgKi9cbkBtZWRpYSBzY3JlZW4gYW5kIChtYXgtd2lkdGg6IDU3NnB4KSB7XG4gICAgaW9uLWdyaWQgPiBpb24tcm93OmZpcnN0LWNoaWxkIHtcbiAgICAgICAgZGlzcGxheTogbm9uZTtcbiAgICB9XG4gICAgaW9uLWdyaWQgPiBpb24tcm93IHtcbiAgICAgICAgYm9yZGVyOiAxcHggYmxhY2sgc29saWQ7XG4gICAgfVxufSIsImlvbi1jb2wge1xuICBjdXJzb3I6IHBvaW50ZXI7XG59XG5pb24tY29sLnN1Y2Nlc3Mge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXN1Y2Nlc3MpO1xufVxuaW9uLWNvbC5kYW5nZXIge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLWRhbmdlcik7XG59XG5pb24tY29sLnByaW1hcnkge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXByaW1hcnkpO1xufVxuaW9uLWNvbC5zZWNvbmRhcnkge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXNlY29uZGFyeSk7XG59XG5pb24tY29sLnRlcnRpYXJ5IHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci10ZXJ0aWFyeSk7XG59XG5pb24tY29sLm1lZGl1bSB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItbWVkaXVtKTtcbn1cblxuLyogTWVkaWFzICovXG5AbWVkaWEgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiA1NzZweCkge1xuICBpb24tZ3JpZCA+IGlvbi1yb3c6Zmlyc3QtY2hpbGQge1xuICAgIGRpc3BsYXk6IG5vbmU7XG4gIH1cblxuICBpb24tZ3JpZCA+IGlvbi1yb3cge1xuICAgIGJvcmRlcjogMXB4IGJsYWNrIHNvbGlkO1xuICB9XG59Il19 */");

/***/ }),

/***/ "./src/app/components/picking-list/picking-list.component.ts":
/*!*******************************************************************!*\
  !*** ./src/app/components/picking-list/picking-list.component.ts ***!
  \*******************************************************************/
/*! exports provided: PickingListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PickingListComponent", function() { return PickingListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");



var PickingListComponent = /** @class */ (function () {
    function PickingListComponent(router) {
        this.router = router;
    }
    PickingListComponent.prototype.ngOnInit = function () { };
    PickingListComponent.prototype.open_link = function (pick_id, code) {
        this.router.navigateByUrl('/stock-picking/' + pick_id + '/' + code);
    };
    PickingListComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)
    ], PickingListComponent.prototype, "picks", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)
    ], PickingListComponent.prototype, "code", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)
    ], PickingListComponent.prototype, "not_allowed_fields", void 0);
    PickingListComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-picking-list',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./picking-list.component.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/picking-list/picking-list.component.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./picking-list.component.scss */ "./src/app/components/picking-list/picking-list.component.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]])
    ], PickingListComponent);
    return PickingListComponent;
}());



/***/ }),

/***/ "./src/app/pages/stock-picking-list/stock-picking-list.module.ts":
/*!***********************************************************************!*\
  !*** ./src/app/pages/stock-picking-list/stock-picking-list.module.ts ***!
  \***********************************************************************/
/*! exports provided: StockPickingListPageModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockPickingListPageModule", function() { return StockPickingListPageModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _stock_picking_list_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./stock-picking-list.page */ "./src/app/pages/stock-picking-list/stock-picking-list.page.ts");
/* harmony import */ var _components_picking_list_picking_list_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../components/picking-list/picking-list.component */ "./src/app/components/picking-list/picking-list.component.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../shared/shared.module */ "./src/app/shared/shared.module.ts");









var routes = [
    {
        path: '',
        component: _stock_picking_list_page__WEBPACK_IMPORTED_MODULE_6__["StockPickingListPage"]
    }
];
var StockPickingListPageModule = /** @class */ (function () {
    function StockPickingListPageModule() {
    }
    StockPickingListPageModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__["SharedModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes)
            ],
            entryComponents: [_components_picking_list_picking_list_component__WEBPACK_IMPORTED_MODULE_7__["PickingListComponent"]],
            declarations: [_stock_picking_list_page__WEBPACK_IMPORTED_MODULE_6__["StockPickingListPage"], _components_picking_list_picking_list_component__WEBPACK_IMPORTED_MODULE_7__["PickingListComponent"]]
        })
    ], StockPickingListPageModule);
    return StockPickingListPageModule;
}());



/***/ }),

/***/ "./src/app/pages/stock-picking-list/stock-picking-list.page.scss":
/*!***********************************************************************!*\
  !*** ./src/app/pages/stock-picking-list/stock-picking-list.page.scss ***!
  \***********************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("ion-icon.icon {\n  font-size: 45px;\n  color: var(--ion-color-secondary);\n  cursor: pointer;\n}\n\nion-col.selected ion-icon.icon {\n  color: var(--ion-color-primary);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL3BhZ2VzL3N0b2NrLXBpY2tpbmctbGlzdC9zdG9jay1waWNraW5nLWxpc3QucGFnZS5zY3NzIiwic3JjL2FwcC9wYWdlcy9zdG9jay1waWNraW5nLWxpc3Qvc3RvY2stcGlja2luZy1saXN0LnBhZ2Uuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNJLGVBQUE7RUFDQSxpQ0FBQTtFQUNBLGVBQUE7QUNDSjs7QURHSTtFQUNJLCtCQUFBO0FDQVIiLCJmaWxlIjoic3JjL2FwcC9wYWdlcy9zdG9jay1waWNraW5nLWxpc3Qvc3RvY2stcGlja2luZy1saXN0LnBhZ2Uuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbImlvbi1pY29uLmljb24ge1xuICAgIGZvbnQtc2l6ZTogNDVweDtcbiAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXNlY29uZGFyeSk7XG4gICAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG5pb24tY29sLnNlbGVjdGVkIHtcbiAgICBpb24taWNvbi5pY29uIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1wcmltYXJ5KTtcbiAgICB9XG59IiwiaW9uLWljb24uaWNvbiB7XG4gIGZvbnQtc2l6ZTogNDVweDtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zZWNvbmRhcnkpO1xuICBjdXJzb3I6IHBvaW50ZXI7XG59XG5cbmlvbi1jb2wuc2VsZWN0ZWQgaW9uLWljb24uaWNvbiB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG59Il19 */");

/***/ }),

/***/ "./src/app/pages/stock-picking-list/stock-picking-list.page.ts":
/*!*********************************************************************!*\
  !*** ./src/app/pages/stock-picking-list/stock-picking-list.page.ts ***!
  \*********************************************************************/
/*! exports provided: StockPickingListPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockPickingListPage", function() { return StockPickingListPage; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");







var StockPickingListPage = /** @class */ (function () {
    function StockPickingListPage(odoo, router, route, alertCtrl, audio, stock) {
        this.odoo = odoo;
        this.router = router;
        this.route = route;
        this.alertCtrl = alertCtrl;
        this.audio = audio;
        this.stock = stock;
        var options = { day: 'numeric', month: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', hourCycle: 'h24' };
        this.view_domain = {
            'ready': [['state', '=', 'assigned']],
            'waiting': [['state', 'in', ['waiting', 'confirmed']]],
            'late': [['state', 'in', ['assigned', 'waiting', 'confirmed']], ['scheduled_date', '<', new Date().toLocaleString('es-ES', options)]],
            'backorders': [['state', 'in', ['waiting', 'confirmed', 'assigned']], ['backorder_id', '!=', false]]
        };
        this.offset = 0;
        this.limit = 25;
        this.limit_reached = false;
    }
    StockPickingListPage.prototype.ngOnInit = function () {
        var _this = this;
        this.odoo.isLoggedIn().then(function (data) {
            if (data == false) {
                _this.router.navigateByUrl('/login');
            }
            else {
                _this.current_type_id = _this.route.snapshot.paramMap.get('id');
                _this.view_selector = _this.route.snapshot.paramMap.get('view');
                _this.current_code = _this.route.snapshot.paramMap.get('code');
                _this.get_picking_list();
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    StockPickingListPage.prototype.onReadingEmitted = function (val) {
        this.scanner_reading = val;
        this.search = val;
        this.get_picking_list(this.search);
    };
    StockPickingListPage.prototype.presentAlert = function (titulo, texto) {
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
    StockPickingListPage.prototype.get_picking_list = function (search) {
        var _this = this;
        if (search === void 0) { search = null; }
        this.offset = 0;
        this.limit_reached = false;
        this.stock.get_picking_list(this.view_domain[this.view_selector], this.current_type_id, this.offset, this.limit, search).then(function (picking_list) {
            _this.pickings = picking_list;
            if (_this.pickings[0] && _this.pickings[0]['picking_fields']) {
                _this.not_allowed_fields = _this.pickings[0]['picking_fields'].split(',');
                console.log(_this.not_allowed_fields);
            }
            if (Object.keys(picking_list).length < 25) {
                _this.limit_reached = true;
            }
            if (Object.keys(_this.pickings).length == 1) {
                _this.router.navigateByUrl('/stock-picking/' + _this.pickings[0]['id'] + '/' + _this.current_code);
            }
            _this.audio.play('click');
        })
            .catch(function (error) {
            console.log(error);
            _this.presentAlert('Error al recuperador el listado de operaciones:', error);
        });
    };
    StockPickingListPage.prototype.get_search_results = function (ev) {
        this.search = ev.target.value;
        this.get_picking_list(this.search);
    };
    // Infinitescroll
    StockPickingListPage.prototype.loadData = function (event) {
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
    StockPickingListPage.prototype.picking_list_infinite_scroll_add = function () {
        var _this = this;
        this.offset += this.limit;
        this.stock.get_picking_list(this.view_domain[this.view_selector], this.current_type_id, this.offset, this.limit, this.search).then(function (data) {
            var current_length = Object.keys(_this.pickings).length;
            if (Object.keys(data).length < 25) {
                _this.limit_reached = true;
            }
            for (var k in data)
                _this.pickings[current_length + Number(k)] = data[k];
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperador el listado de operaciones:', error);
        });
    };
    StockPickingListPage.prototype.toggleInfiniteScroll = function () {
        this.infiniteScroll.disabled = !this.infiniteScroll.disabled;
    };
    StockPickingListPage.ctorParameters = function () { return [
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])(_ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"], { static: false }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"])
    ], StockPickingListPage.prototype, "infiniteScroll", void 0);
    StockPickingListPage = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-stock-picking-list',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./stock-picking-list.page.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-picking-list/stock-picking-list.page.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./stock-picking-list.page.scss */ "./src/app/pages/stock-picking-list/stock-picking-list.page.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"]])
    ], StockPickingListPage);
    return StockPickingListPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-stock-picking-list-stock-picking-list-module.js.map
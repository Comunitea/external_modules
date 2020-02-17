(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-stock-picking-list-stock-picking-list-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/components/picking-list/picking-list.component.html":
/*!***********************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/components/picking-list/picking-list.component.html ***!
  \***********************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-grid>\n  \n  <ion-row>\n    <ion-col>\n        <div><strong>Nombre</strong></div>\n    </ion-col>\n    \n    <ion-col *ngIf=\"picking_fields.indexOf('location_id')<0\">\n        <div><strong>Origen</strong></div>\n    </ion-col>\n\n    <ion-col *ngIf=\"picking_fields.indexOf('location_dest_id')<0\">\n      <div><strong>Destino</strong></div>\n    </ion-col>\n    \n    <ion-col class=\"ion-align-self-center ion-text-center\" *ngIf=\"picking_fields.indexOf('scheduled_date')<0\">\n      <div><strong>Previsto</strong></div>\n    </ion-col>\n    <ion-col class=\"ion-align-self-center ion-text-center\" *ngIf=\"picking_fields.indexOf('state')<0\">\n      <div><strong>Estado</strong></div>\n    </ion-col>\n  </ion-row>\n\n  <ion-row *ngFor=\"let pick of picks\" (click)=\"open_link(pick.id, code)\">\n    <ion-col>\n      <div>{{pick.name}}</div>\n    </ion-col>\n    \n    <ion-col *ngIf=\"picking_fields.indexOf('location_id')<0\">\n      <div>{{pick.location_id[1]}}</div>\n    </ion-col>\n  \n    <ion-col *ngIf=\"picking_fields.indexOf('location_dest_id')<0\">\n      <div>{{pick.location_dest_id[1]}}</div>\n    </ion-col>\n    \n    <ion-col class=\"ion-align-self-center ion-text-center\" *ngIf=\"picking_fields.indexOf('scheduled_date')<0\">\n      <div>{{pick.scheduled_date}}h</div>\n    </ion-col>\n  \n    <ion-col [ngClass]=\"{'success': pick.state == 'done',\n    'danger': pick.state == 'cancel', \n    'primary': pick.state == 'assigned', \n    'secondary': pick.state == 'confirmed', \n    'tertiary': pick.state == 'waiting', \n    'medium': pick.state == 'draft'}\" [ngSwitch]=\"pick.state\" class=\"ion-align-self-center ion-text-center\" *ngIf=\"picking_fields.indexOf('state')<0\">\n      <div *ngSwitchCase=\"'draft'\">Borrador</div>\n      <div *ngSwitchCase=\"'waiting'\">Faltan operaciones</div>\n      <div *ngSwitchCase=\"'confirmed'\">En espera</div>\n      <div *ngSwitchCase=\"'assigned'\">Preparado</div>\n      <div *ngSwitchCase=\"'done'\">Hecho</div>\n      <div *ngSwitchCase=\"'cancel'\">Cancel</div>\n    </ion-col>\n  </ion-row>\n</ion-grid>\n\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/pages/stock-picking-list/stock-picking-list.page.html":
/*!*************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/pages/stock-picking-list/stock-picking-list.page.html ***!
  \*************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"start\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n    <app-scanner-header slot=\"end\" (show_scan_form_changed)=\"onShowEmitted($event)\" [show_scan_form]=show_scan_form></app-scanner-header>\n    <ion-title>Listado de albaranes</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <ion-card>\n    <ion-card-content>\n      <ion-row>\n        <ion-toolbar>\n          <ion-searchbar type=\"text\" (ionInput)=\"get_search_results($event)\" autocomplete=\"on\" showCancelButton=\"always\"></ion-searchbar>\n        </ion-toolbar>\n      </ion-row>\n\n      <app-picking-list [code]=\"current_code\" [picking_fields]=\"picking_fields\" [picks]=\"pickings\"></app-picking-list>\n\n      <ion-infinite-scroll threshold=\"100px\" (ionInfinite)=\"loadData($event)\">\n        <ion-infinite-scroll-content\n          loadingSpinner=\"bubbles\"\n          loadingText=\"Cargando más productos...\">\n        </ion-infinite-scroll-content>\n      </ion-infinite-scroll>\n    </ion-card-content>\n  </ion-card>\n</ion-content>\n\n<app-scanner-footer (scanner_reading_changed)=\"onReadingEmitted($event)\" [show_scan_form]=show_scan_form [scanner_reading]=\"scanner_reading\"></app-scanner-footer>"

/***/ }),

/***/ "./src/app/components/picking-list/picking-list.component.scss":
/*!*********************************************************************!*\
  !*** ./src/app/components/picking-list/picking-list.component.scss ***!
  \*********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "ion-col {\n  cursor: pointer;\n}\nion-col.success {\n  color: var(--ion-color-success);\n}\nion-col.danger {\n  color: var(--ion-color-danger);\n}\nion-col.primary {\n  color: var(--ion-color-primary);\n}\nion-col.secondary {\n  color: var(--ion-color-secondary);\n}\nion-col.tertiary {\n  color: var(--ion-color-tertiary);\n}\nion-col.medium {\n  color: var(--ion-color-medium);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9jb21wb25lbnRzL3BpY2tpbmctbGlzdC9waWNraW5nLWxpc3QuY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL2NvbXBvbmVudHMvcGlja2luZy1saXN0L3BpY2tpbmctbGlzdC5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQW1CSSxlQUFBO0FDakJKO0FEREk7RUFDSSwrQkFBQTtBQ0dSO0FEREk7RUFDSSw4QkFBQTtBQ0dSO0FEREk7RUFDSSwrQkFBQTtBQ0dSO0FEREk7RUFDSSxpQ0FBQTtBQ0dSO0FEREk7RUFDSSxnQ0FBQTtBQ0dSO0FEREk7RUFDSSw4QkFBQTtBQ0dSIiwiZmlsZSI6InNyYy9hcHAvY29tcG9uZW50cy9waWNraW5nLWxpc3QvcGlja2luZy1saXN0LmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiaW9uLWNvbCB7XG4gICAgJi5zdWNjZXNzIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zdWNjZXNzKTtcbiAgICB9XG4gICAgJi5kYW5nZXIge1xuICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLWRhbmdlcik7XG4gICAgfVxuICAgICYucHJpbWFyeSB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG4gICAgfVxuICAgICYuc2Vjb25kYXJ5IHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zZWNvbmRhcnkpO1xuICAgIH1cbiAgICAmLnRlcnRpYXJ5IHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci10ZXJ0aWFyeSk7XG4gICAgfVxuICAgICYubWVkaXVtIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1tZWRpdW0pO1xuICAgIH1cbiAgICBjdXJzb3I6IHBvaW50ZXI7XG59IiwiaW9uLWNvbCB7XG4gIGN1cnNvcjogcG9pbnRlcjtcbn1cbmlvbi1jb2wuc3VjY2VzcyB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc3VjY2Vzcyk7XG59XG5pb24tY29sLmRhbmdlciB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItZGFuZ2VyKTtcbn1cbmlvbi1jb2wucHJpbWFyeSB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG59XG5pb24tY29sLnNlY29uZGFyeSB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc2Vjb25kYXJ5KTtcbn1cbmlvbi1jb2wudGVydGlhcnkge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXRlcnRpYXJ5KTtcbn1cbmlvbi1jb2wubWVkaXVtIHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1tZWRpdW0pO1xufSJdfQ== */"

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");



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
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], PickingListComponent.prototype, "picks", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], PickingListComponent.prototype, "code", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], PickingListComponent.prototype, "picking_fields", void 0);
    PickingListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-picking-list',
            template: __webpack_require__(/*! raw-loader!./picking-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/components/picking-list/picking-list.component.html"),
            styles: [__webpack_require__(/*! ./picking-list.component.scss */ "./src/app/components/picking-list/picking-list.component.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]])
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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
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
    StockPickingListPageModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
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
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "ion-icon.icon {\n  font-size: 45px;\n  color: var(--ion-color-secondary);\n  cursor: pointer;\n}\n\nion-col.selected ion-icon.icon {\n  color: var(--ion-color-primary);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9wYWdlcy9zdG9jay1waWNraW5nLWxpc3Qvc3RvY2stcGlja2luZy1saXN0LnBhZ2Uuc2NzcyIsInNyYy9hcHAvcGFnZXMvc3RvY2stcGlja2luZy1saXN0L3N0b2NrLXBpY2tpbmctbGlzdC5wYWdlLnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDSSxlQUFBO0VBQ0EsaUNBQUE7RUFDQSxlQUFBO0FDQ0o7O0FER0k7RUFDSSwrQkFBQTtBQ0FSIiwiZmlsZSI6InNyYy9hcHAvcGFnZXMvc3RvY2stcGlja2luZy1saXN0L3N0b2NrLXBpY2tpbmctbGlzdC5wYWdlLnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJpb24taWNvbi5pY29uIHtcbiAgICBmb250LXNpemU6IDQ1cHg7XG4gICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zZWNvbmRhcnkpO1xuICAgIGN1cnNvcjogcG9pbnRlcjtcbn1cblxuaW9uLWNvbC5zZWxlY3RlZCB7XG4gICAgaW9uLWljb24uaWNvbiB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG4gICAgfVxufSIsImlvbi1pY29uLmljb24ge1xuICBmb250LXNpemU6IDQ1cHg7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc2Vjb25kYXJ5KTtcbiAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG5pb24tY29sLnNlbGVjdGVkIGlvbi1pY29uLmljb24ge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXByaW1hcnkpO1xufSJdfQ== */"

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/fesm5/ionic-storage.js");








var StockPickingListPage = /** @class */ (function () {
    function StockPickingListPage(odoo, router, route, alertCtrl, audio, stock, storage) {
        this.odoo = odoo;
        this.router = router;
        this.route = route;
        this.alertCtrl = alertCtrl;
        this.audio = audio;
        this.stock = stock;
        this.storage = storage;
        this.scanner_options = { reader: true, microphone: false, sound: false };
        var options = { day: 'numeric', month: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', hourCycle: 'h24' };
        this.view_domain = {
            'ready': [['state', '=', 'assigned']],
            'waiting': [['state', 'in', ['waiting', 'confirmed']]],
            'late': [['state', 'in', ['assigned', 'waiting', 'confirmed']], ['scheduled_date', '<', new Date().toLocaleString('es-ES', options)]],
            'backorders': [['state', 'in', ['waiting', 'confirmed', 'assigned']], ['backorder_id', '!=', false]]
        };
        this.picking_fields = "picking_fields";
        this.check_scanner_values();
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
                _this.show_scan_form = _this.scanner_options['reader'];
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
    StockPickingListPage.prototype.check_scanner_values = function () {
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
    StockPickingListPage.prototype.onReadingEmitted = function (val) {
        this.scanner_reading = val;
        this.search = val;
        this.get_picking_list(this.search);
    };
    StockPickingListPage.prototype.onShowEmitted = function (val) {
        this.show_scan_form = val;
    };
    StockPickingListPage.prototype.presentAlert = function (titulo, texto) {
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
    StockPickingListPage.prototype.get_picking_list = function (search) {
        var _this = this;
        if (search === void 0) { search = null; }
        this.offset = 0;
        this.limit_reached = false;
        this.stock.get_picking_list(this.view_domain[this.view_selector], this.current_type_id, this.offset, this.limit, search).then(function (picking_list) {
            _this.pickings = picking_list;
            if (picking_list) {
                _this.picking_fields = picking_list[0]['picking_fields'];
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
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"] },
        { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_7__["Storage"] }
    ]; };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])(_ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"], { static: false }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"])
    ], StockPickingListPage.prototype, "infiniteScroll", void 0);
    StockPickingListPage = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-stock-picking-list',
            template: __webpack_require__(/*! raw-loader!./stock-picking-list.page.html */ "./node_modules/raw-loader/index.js!./src/app/pages/stock-picking-list/stock-picking-list.page.html"),
            styles: [__webpack_require__(/*! ./stock-picking-list.page.scss */ "./src/app/pages/stock-picking-list/stock-picking-list.page.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"],
            _ionic_storage__WEBPACK_IMPORTED_MODULE_7__["Storage"]])
    ], StockPickingListPage);
    return StockPickingListPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-stock-picking-list-stock-picking-list-module-es5.js.map
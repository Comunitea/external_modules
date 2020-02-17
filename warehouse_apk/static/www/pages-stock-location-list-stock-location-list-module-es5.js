(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-stock-location-list-stock-location-list-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/components/location-list/location-list.component.html":
/*!*************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/components/location-list/location-list.component.html ***!
  \*************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-grid>\n  <ion-row>\n    <ion-col size=\"12\">\n        <div><strong>Nombre</strong></div>\n    </ion-col>\n    \n    <!--ion-col size=\"4\">\n        <div><strong>Tipo de ubicación</strong></div>\n    </ion-col>\n  \n    <ion-col size=\"4\">\n      <div><strong>Compañía</strong></div>\n    </ion-col-->\n  </ion-row>\n  \n  <ion-row *ngFor=\"let location of locations\" (click)=\"open_link(location.id)\">\n    <ion-col size=\"12\">\n      <div>{{location.display_name}}</div>\n    </ion-col>\n  \n    <!--ion-col size=\"4\" [ngSwitch]=\"location.usage\" class=\"ion-align-self-center ion-text-center\">\n      <div *ngSwitchCase=\"'supplier'\">Ubicación de proveedor</div>\n      <div *ngSwitchCase=\"'customer'\">Ubicación de cliente</div>\n      <div *ngSwitchCase=\"'inventory'\">Ubicación de inventario</div>\n      <div *ngSwitchCase=\"'procurement'\">Abastecimiento</div>\n      <div *ngSwitchCase=\"'view'\">Ver</div>\n      <div *ngSwitchCase=\"'internal'\">Ubicación interna</div>\n      <div *ngSwitchCase=\"'production'\">Producción</div>\n      <div *ngSwitchCase=\"'transit'\">Ubicación de tránsito</div>\n    </ion-col>\n    \n    <ion-col size=\"4\">\n      <div>{{location.company_id[1]}}</div>\n    </ion-col-->\n  </ion-row>\n</ion-grid>"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/pages/stock-location-list/stock-location-list.page.html":
/*!***************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/pages/stock-location-list/stock-location-list.page.html ***!
  \***************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"start\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n    <app-scanner-header slot=\"end\" (show_scan_form_changed)=\"onShowEmitted($event)\" [show_scan_form]=show_scan_form></app-scanner-header>\n    <ion-title>Listado de ubicaciones</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <ion-card>\n    <ion-row *ngIf=\"location_types\">\n      <ion-col col-2 class=\"ion-align-self-center ion-text-center\" [ngClass]=\"{'selected': current_selected_type == option.value}\" *ngFor=\"let option of location_types\" (click)=\"get_location_list(option.value, search)\">\n        <ion-icon class=\"icon\" [name]=\"option.icon\"></ion-icon><br/>\n        {{option.name}}\n      </ion-col>\n    </ion-row>\n  </ion-card>\n  <ion-card>\n    <ion-card-content>\n      <ion-row>\n        <ion-toolbar>\n          <ion-searchbar type=\"text\" (ionInput)=\"get_search_results($event)\" autocomplete=\"on\" showCancelButton=\"always\"></ion-searchbar>\n        </ion-toolbar>\n      </ion-row>   \n      \n      <app-location-list [locations]=\"locations\"></app-location-list>\n\n      <ion-infinite-scroll threshold=\"100px\" (ionInfinite)=\"loadData($event)\">\n        <ion-infinite-scroll-content\n          loadingSpinner=\"bubbles\"\n          loadingText=\"Cargando más productos...\">\n        </ion-infinite-scroll-content>\n      </ion-infinite-scroll>\n    </ion-card-content>\n  </ion-card>\n</ion-content>\n\n<app-scanner-footer (scanner_reading_changed)=\"onReadingEmitted($event)\" [show_scan_form]=show_scan_form [scanner_reading]=\"scanner_reading\"></app-scanner-footer>\n"

/***/ }),

/***/ "./src/app/components/location-list/location-list.component.scss":
/*!***********************************************************************!*\
  !*** ./src/app/components/location-list/location-list.component.scss ***!
  \***********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "ion-col {\n  cursor: pointer;\n}\nion-col.success {\n  color: var(--ion-color-success);\n}\nion-col.danger {\n  color: var(--ion-color-danger);\n}\nion-col.primary {\n  color: var(--ion-color-primary);\n}\nion-col.secondary {\n  color: var(--ion-color-secondary);\n}\nion-col.tertiary {\n  color: var(--ion-color-tertiary);\n}\nion-col.medium {\n  color: var(--ion-color-medium);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9jb21wb25lbnRzL2xvY2F0aW9uLWxpc3QvbG9jYXRpb24tbGlzdC5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvY29tcG9uZW50cy9sb2NhdGlvbi1saXN0L2xvY2F0aW9uLWxpc3QuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFtQkksZUFBQTtBQ2pCSjtBRERJO0VBQ0ksK0JBQUE7QUNHUjtBRERJO0VBQ0ksOEJBQUE7QUNHUjtBRERJO0VBQ0ksK0JBQUE7QUNHUjtBRERJO0VBQ0ksaUNBQUE7QUNHUjtBRERJO0VBQ0ksZ0NBQUE7QUNHUjtBRERJO0VBQ0ksOEJBQUE7QUNHUiIsImZpbGUiOiJzcmMvYXBwL2NvbXBvbmVudHMvbG9jYXRpb24tbGlzdC9sb2NhdGlvbi1saXN0LmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiaW9uLWNvbCB7XG4gICAgJi5zdWNjZXNzIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zdWNjZXNzKTtcbiAgICB9XG4gICAgJi5kYW5nZXIge1xuICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLWRhbmdlcik7XG4gICAgfVxuICAgICYucHJpbWFyeSB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG4gICAgfVxuICAgICYuc2Vjb25kYXJ5IHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zZWNvbmRhcnkpO1xuICAgIH1cbiAgICAmLnRlcnRpYXJ5IHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci10ZXJ0aWFyeSk7XG4gICAgfVxuICAgICYubWVkaXVtIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1tZWRpdW0pO1xuICAgIH1cbiAgICBjdXJzb3I6IHBvaW50ZXI7XG59IiwiaW9uLWNvbCB7XG4gIGN1cnNvcjogcG9pbnRlcjtcbn1cbmlvbi1jb2wuc3VjY2VzcyB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc3VjY2Vzcyk7XG59XG5pb24tY29sLmRhbmdlciB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItZGFuZ2VyKTtcbn1cbmlvbi1jb2wucHJpbWFyeSB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG59XG5pb24tY29sLnNlY29uZGFyeSB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc2Vjb25kYXJ5KTtcbn1cbmlvbi1jb2wudGVydGlhcnkge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXRlcnRpYXJ5KTtcbn1cbmlvbi1jb2wubWVkaXVtIHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1tZWRpdW0pO1xufSJdfQ== */"

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");



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
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], LocationListComponent.prototype, "locations", void 0);
    LocationListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-location-list',
            template: __webpack_require__(/*! raw-loader!./location-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/components/location-list/location-list.component.html"),
            styles: [__webpack_require__(/*! ./location-list.component.scss */ "./src/app/components/location-list/location-list.component.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]])
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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
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
    StockLocationListPageModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
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
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "ion-icon.icon {\n  font-size: 45px;\n  color: var(--ion-color-secondary);\n  cursor: pointer;\n}\n\nion-col.selected ion-icon.icon {\n  color: var(--ion-color-primary);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9wYWdlcy9zdG9jay1sb2NhdGlvbi1saXN0L3N0b2NrLWxvY2F0aW9uLWxpc3QucGFnZS5zY3NzIiwic3JjL2FwcC9wYWdlcy9zdG9jay1sb2NhdGlvbi1saXN0L3N0b2NrLWxvY2F0aW9uLWxpc3QucGFnZS5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0ksZUFBQTtFQUNBLGlDQUFBO0VBQ0EsZUFBQTtBQ0NKOztBREdJO0VBQ0ksK0JBQUE7QUNBUiIsImZpbGUiOiJzcmMvYXBwL3BhZ2VzL3N0b2NrLWxvY2F0aW9uLWxpc3Qvc3RvY2stbG9jYXRpb24tbGlzdC5wYWdlLnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJpb24taWNvbi5pY29uIHtcbiAgICBmb250LXNpemU6IDQ1cHg7XG4gICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zZWNvbmRhcnkpO1xuICAgIGN1cnNvcjogcG9pbnRlcjtcbn1cblxuaW9uLWNvbC5zZWxlY3RlZCB7XG4gICAgaW9uLWljb24uaWNvbiB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG4gICAgfVxufSIsImlvbi1pY29uLmljb24ge1xuICBmb250LXNpemU6IDQ1cHg7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc2Vjb25kYXJ5KTtcbiAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG5pb24tY29sLnNlbGVjdGVkIGlvbi1pY29uLmljb24ge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXByaW1hcnkpO1xufSJdfQ== */"

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/fesm5/ionic-storage.js");








var StockLocationListPage = /** @class */ (function () {
    function StockLocationListPage(odoo, router, alertCtrl, audio, stock, storage) {
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.audio = audio;
        this.stock = stock;
        this.storage = storage;
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
        this.check_scanner_values();
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
                _this.show_scan_form = _this.scanner_options['reader'];
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    StockLocationListPage.prototype.check_scanner_values = function () {
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
    StockLocationListPage.prototype.onReadingEmitted = function (val) {
        this.scanner_reading = val;
        this.search = val;
        this.get_location_list(this.current_selected_type, this.search);
    };
    StockLocationListPage.prototype.onShowEmitted = function (val) {
        this.show_scan_form = val;
    };
    StockLocationListPage.prototype.presentAlert = function (titulo, texto) {
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
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"] },
        { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_7__["Storage"] }
    ]; };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])(_ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"], { static: false }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"])
    ], StockLocationListPage.prototype, "infiniteScroll", void 0);
    StockLocationListPage = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-stock-location-list',
            template: __webpack_require__(/*! raw-loader!./stock-location-list.page.html */ "./node_modules/raw-loader/index.js!./src/app/pages/stock-location-list/stock-location-list.page.html"),
            styles: [__webpack_require__(/*! ./stock-location-list.page.scss */ "./src/app/pages/stock-location-list/stock-location-list.page.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"],
            _ionic_storage__WEBPACK_IMPORTED_MODULE_7__["Storage"]])
    ], StockLocationListPage);
    return StockLocationListPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-stock-location-list-stock-location-list-module-es5.js.map
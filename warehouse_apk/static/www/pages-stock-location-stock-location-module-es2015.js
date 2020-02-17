(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-stock-location-stock-location-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/components/location-info/location-info.component.html":
/*!*************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/components/location-info/location-info.component.html ***!
  \*************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-card *ngIf=\"location\">\n\n  <ion-card-header>\n    <ion-card-title>{{location.display_name}}</ion-card-title>\n  </ion-card-header>\n\n  <ion-card-content>\n    <div *ngIf=\"location.company_id\"><strong>Compañía: </strong>{{location.company_id[1]}}</div>\n    <div *ngIf=\"location.picking_type_id\"><strong>Tipo de albarán: </strong>{{location.picking_type_id[1]}}</div>\n    <div [ngSwitch]=\"location.usage\">\n      <strong>Tipo: </strong>\n      <!--ion-text *ngSwitchCase=\"'supplier'\">Ubicación de proveedor</ion-text-->\n      <ion-text *ngSwitchCase=\"'view'\">Ver</ion-text>\n      <ion-text *ngSwitchCase=\"'internal'\">Ubicación interna</ion-text>\n      <!--ion-text *ngSwitchCase=\"'customer'\">Ubicación de cliente</ion-text-->\n      <!--ion-text *ngSwitchCase=\"'inventory'\">Ubicación de inventario</ion-text-->\n      <!--ion-text *ngSwitchCase=\"'procurement'\">Abastecimiento</ion-text-->\n      <ion-text *ngSwitchCase=\"'production'\">Producción</ion-text>\n      <ion-text *ngSwitchCase=\"'transit'\">Ubicación de tránsito</ion-text>\n    </div>\n    <ion-row>\n      <ion-col>\n        <ion-button (click)=\"open_link('stock', location.id)\" expand=\"block\">Stock actual</ion-button>\n      </ion-col>\n      <ion-col>\n        <ion-button (click)=\"open_link('product', location.id)\" expand=\"block\">Productos</ion-button>\n        </ion-col>\n    </ion-row>\n  </ion-card-content>\n\n</ion-card>"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/pages/stock-location/stock-location.page.html":
/*!*****************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/pages/stock-location/stock-location.page.html ***!
  \*****************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"start\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n    <ion-title>Detalles de la ubicación</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <app-location-info [location]=\"location_data\"></app-location-info>\n</ion-content>"

/***/ }),

/***/ "./src/app/components/location-info/location-info.component.scss":
/*!***********************************************************************!*\
  !*** ./src/app/components/location-info/location-info.component.scss ***!
  \***********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "ion-col {\n  cursor: pointer;\n}\nion-col.success {\n  color: var(--ion-color-success);\n}\nion-col.danger {\n  color: var(--ion-color-danger);\n}\nion-col.primary {\n  color: var(--ion-color-primary);\n}\nion-col.secondary {\n  color: var(--ion-color-secondary);\n}\nion-col.tertiary {\n  color: var(--ion-color-tertiary);\n}\nion-col.medium {\n  color: var(--ion-color-medium);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9jb21wb25lbnRzL2xvY2F0aW9uLWluZm8vbG9jYXRpb24taW5mby5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvY29tcG9uZW50cy9sb2NhdGlvbi1pbmZvL2xvY2F0aW9uLWluZm8uY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFtQkksZUFBQTtBQ2pCSjtBRERJO0VBQ0ksK0JBQUE7QUNHUjtBRERJO0VBQ0ksOEJBQUE7QUNHUjtBRERJO0VBQ0ksK0JBQUE7QUNHUjtBRERJO0VBQ0ksaUNBQUE7QUNHUjtBRERJO0VBQ0ksZ0NBQUE7QUNHUjtBRERJO0VBQ0ksOEJBQUE7QUNHUiIsImZpbGUiOiJzcmMvYXBwL2NvbXBvbmVudHMvbG9jYXRpb24taW5mby9sb2NhdGlvbi1pbmZvLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiaW9uLWNvbCB7XG4gICAgJi5zdWNjZXNzIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zdWNjZXNzKTtcbiAgICB9XG4gICAgJi5kYW5nZXIge1xuICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLWRhbmdlcik7XG4gICAgfVxuICAgICYucHJpbWFyeSB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG4gICAgfVxuICAgICYuc2Vjb25kYXJ5IHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1zZWNvbmRhcnkpO1xuICAgIH1cbiAgICAmLnRlcnRpYXJ5IHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci10ZXJ0aWFyeSk7XG4gICAgfVxuICAgICYubWVkaXVtIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1tZWRpdW0pO1xuICAgIH1cbiAgICBjdXJzb3I6IHBvaW50ZXI7XG59IiwiaW9uLWNvbCB7XG4gIGN1cnNvcjogcG9pbnRlcjtcbn1cbmlvbi1jb2wuc3VjY2VzcyB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc3VjY2Vzcyk7XG59XG5pb24tY29sLmRhbmdlciB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItZGFuZ2VyKTtcbn1cbmlvbi1jb2wucHJpbWFyeSB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG59XG5pb24tY29sLnNlY29uZGFyeSB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3Itc2Vjb25kYXJ5KTtcbn1cbmlvbi1jb2wudGVydGlhcnkge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXRlcnRpYXJ5KTtcbn1cbmlvbi1jb2wubWVkaXVtIHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1tZWRpdW0pO1xufSJdfQ== */"

/***/ }),

/***/ "./src/app/components/location-info/location-info.component.ts":
/*!*********************************************************************!*\
  !*** ./src/app/components/location-info/location-info.component.ts ***!
  \*********************************************************************/
/*! exports provided: LocationInfoComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LocationInfoComponent", function() { return LocationInfoComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");



let LocationInfoComponent = class LocationInfoComponent {
    constructor(router) {
        this.router = router;
    }
    ngOnInit() { }
    open_link(type, location_id) {
        if (type == 'stock') {
            this.router.navigateByUrl('/stock-quant-list/' + location_id);
        }
        else {
            this.router.navigateByUrl('/stock-location-product-list/' + location_id);
        }
    }
};
LocationInfoComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] }
];
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
], LocationInfoComponent.prototype, "location", void 0);
LocationInfoComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-location-info',
        template: __webpack_require__(/*! raw-loader!./location-info.component.html */ "./node_modules/raw-loader/index.js!./src/app/components/location-info/location-info.component.html"),
        styles: [__webpack_require__(/*! ./location-info.component.scss */ "./src/app/components/location-info/location-info.component.scss")]
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]])
], LocationInfoComponent);



/***/ }),

/***/ "./src/app/pages/stock-location/stock-location.module.ts":
/*!***************************************************************!*\
  !*** ./src/app/pages/stock-location/stock-location.module.ts ***!
  \***************************************************************/
/*! exports provided: StockLocationPageModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockLocationPageModule", function() { return StockLocationPageModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _stock_location_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./stock-location.page */ "./src/app/pages/stock-location/stock-location.page.ts");
/* harmony import */ var _components_location_info_location_info_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../components/location-info/location-info.component */ "./src/app/components/location-info/location-info.component.ts");








const routes = [
    {
        path: '',
        component: _stock_location_page__WEBPACK_IMPORTED_MODULE_6__["StockLocationPage"]
    }
];
let StockLocationPageModule = class StockLocationPageModule {
};
StockLocationPageModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes)
        ],
        entryComponents: [_components_location_info_location_info_component__WEBPACK_IMPORTED_MODULE_7__["LocationInfoComponent"]],
        declarations: [_stock_location_page__WEBPACK_IMPORTED_MODULE_6__["StockLocationPage"], _components_location_info_location_info_component__WEBPACK_IMPORTED_MODULE_7__["LocationInfoComponent"]]
    })
], StockLocationPageModule);



/***/ }),

/***/ "./src/app/pages/stock-location/stock-location.page.scss":
/*!***************************************************************!*\
  !*** ./src/app/pages/stock-location/stock-location.page.scss ***!
  \***************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3BhZ2VzL3N0b2NrLWxvY2F0aW9uL3N0b2NrLWxvY2F0aW9uLnBhZ2Uuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/pages/stock-location/stock-location.page.ts":
/*!*************************************************************!*\
  !*** ./src/app/pages/stock-location/stock-location.page.ts ***!
  \*************************************************************/
/*! exports provided: StockLocationPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockLocationPage", function() { return StockLocationPage; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");







let StockLocationPage = class StockLocationPage {
    constructor(odoo, router, alertCtrl, route, audio, stock) {
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.route = route;
        this.audio = audio;
        this.stock = stock;
    }
    ngOnInit() {
        this.odoo.isLoggedIn().then((data) => {
            if (data == false) {
                this.router.navigateByUrl('/login');
            }
            else {
                var location = this.route.snapshot.paramMap.get('id');
                this.get_location_info(location);
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
    get_location_info(location) {
        this.stock.get_location_info(location).then((data) => {
            this.location_data = data[0];
            this.audio.play('click');
        })
            .catch((error) => {
            this.presentAlert('Error al recuperar el location:', error);
        });
    }
};
StockLocationPage.ctorParameters = () => [
    { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
    { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"] },
    { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"] }
];
StockLocationPage = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-stock-location',
        template: __webpack_require__(/*! raw-loader!./stock-location.page.html */ "./node_modules/raw-loader/index.js!./src/app/pages/stock-location/stock-location.page.html"),
        styles: [__webpack_require__(/*! ./stock-location.page.scss */ "./src/app/pages/stock-location/stock-location.page.scss")]
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
        _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
        _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
        _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"],
        _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"],
        _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"]])
], StockLocationPage);



/***/ })

}]);
//# sourceMappingURL=pages-stock-location-stock-location-module-es2015.js.map
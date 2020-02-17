(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-stock-quant-list-stock-quant-list-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/components/quant-list/quant-list.component.html":
/*!*******************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/components/quant-list/quant-list.component.html ***!
  \*******************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-grid>\n  <ion-row>\n    <ion-col size=\"10\">\n        <div><strong>Producto</strong></div>\n    </ion-col>\n    \n    <!--ion-col size=\"2\">\n        <div><strong>Reservado</strong></div>\n    </ion-col-->\n\n    <ion-col size=\"2\">\n      <div><strong>Stock</strong></div>\n    </ion-col>\n  </ion-row>\n  <ion-row *ngFor=\"let quant of quants\">\n      <ion-col size=\"10\" style='font-size: xx-small'>\n      <div (click)=\"open_link(quant.product_id[0])\">{{quant.product_id[1]}}</div>\n    </ion-col>\n    \n    <ion-col size=\"2\" style='font-size: xx-small'>\n      <div>{{quant.quantity}} -- ({{quant.reserved_quantity}})</div>\n    </ion-col>\n    \n    <!--ion-col size=\"2\">\n      <div [ngClass]=\"{'danger': quant.quantity &lt;= 0}\">{{quant.quantity}}</div>\n    </ion-col-->\n  </ion-row>\n</ion-grid>"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/pages/stock-quant-list/stock-quant-list.page.html":
/*!*********************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/pages/stock-quant-list/stock-quant-list.page.html ***!
  \*********************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-header>\n    <ion-toolbar>\n      <ion-buttons slot=\"start\">\n        <ion-menu-button></ion-menu-button>\n      </ion-buttons>\n      <app-scanner-header slot=\"end\" (microphone)=\"onMicroEmitted($event)\" (volume)=\"onVolumeEmitted($event)\" (show_scan_form_changed)=\"onShowEmitted($event)\" [show_scan_form]=show_scan_form></app-scanner-header>\n      <ion-title>Stock actual</ion-title>\n    </ion-toolbar>\n  </ion-header>\n  \n  <ion-content>\n    <ion-card>\n      <ion-card-content>\n        <ion-row>\n          <ion-toolbar>\n            <ion-searchbar type=\"text\" (ionInput)=\"get_search_results($event)\" autocomplete=\"on\" showCancelButton=\"always\"></ion-searchbar>\n          </ion-toolbar>\n        </ion-row>\n  \n        <app-quant-list [quants]=\"quants\"></app-quant-list>\n  \n        <ion-infinite-scroll threshold=\"100px\" (ionInfinite)=\"loadData($event)\">\n          <ion-infinite-scroll-content\n            loadingSpinner=\"bubbles\"\n            loadingText=\"Cargando más productos...\">\n          </ion-infinite-scroll-content>\n        </ion-infinite-scroll>\n      </ion-card-content>\n    </ion-card>\n  </ion-content>\n\n  <app-scanner-footer (scanner_reading_changed)=\"onReadingEmitted($event)\" [show_scan_form]=show_scan_form [scanner_reading]=\"scanner_reading\"></app-scanner-footer>"

/***/ }),

/***/ "./src/app/components/quant-list/quant-list.component.scss":
/*!*****************************************************************!*\
  !*** ./src/app/components/quant-list/quant-list.component.scss ***!
  \*****************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "div.danger {\n  color: var(--ion-color-danger);\n}\ndiv.product_link {\n  color: blue;\n  text-decoration: underline;\n  -webkit-text-decoration-color: blue;\n          text-decoration-color: blue;\n  cursor: pointer;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9jb21wb25lbnRzL3F1YW50LWxpc3QvcXVhbnQtbGlzdC5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvY29tcG9uZW50cy9xdWFudC1saXN0L3F1YW50LWxpc3QuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQ0k7RUFDSSw4QkFBQTtBQ0FSO0FERUk7RUFDSSxXQUFBO0VBQ0EsMEJBQUE7RUFDQSxtQ0FBQTtVQUFBLDJCQUFBO0VBQ0EsZUFBQTtBQ0FSIiwiZmlsZSI6InNyYy9hcHAvY29tcG9uZW50cy9xdWFudC1saXN0L3F1YW50LWxpc3QuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJkaXYge1xuICAgICYuZGFuZ2VyIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1kYW5nZXIpO1xuICAgIH1cbiAgICAmLnByb2R1Y3RfbGluayB7XG4gICAgICAgIGNvbG9yOiBibHVlO1xuICAgICAgICB0ZXh0LWRlY29yYXRpb246IHVuZGVybGluZTtcbiAgICAgICAgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBibHVlO1xuICAgICAgICBjdXJzb3I6IHBvaW50ZXI7XG4gICAgfVxufSIsImRpdi5kYW5nZXIge1xuICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLWRhbmdlcik7XG59XG5kaXYucHJvZHVjdF9saW5rIHtcbiAgY29sb3I6IGJsdWU7XG4gIHRleHQtZGVjb3JhdGlvbjogdW5kZXJsaW5lO1xuICB0ZXh0LWRlY29yYXRpb24tY29sb3I6IGJsdWU7XG4gIGN1cnNvcjogcG9pbnRlcjtcbn0iXX0= */"

/***/ }),

/***/ "./src/app/components/quant-list/quant-list.component.ts":
/*!***************************************************************!*\
  !*** ./src/app/components/quant-list/quant-list.component.ts ***!
  \***************************************************************/
/*! exports provided: QuantListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "QuantListComponent", function() { return QuantListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");



let QuantListComponent = class QuantListComponent {
    constructor(router) {
        this.router = router;
    }
    ngOnInit() { }
    open_link(product_id) {
        this.router.navigateByUrl('/product/' + product_id);
    }
};
QuantListComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] }
];
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
], QuantListComponent.prototype, "quants", void 0);
QuantListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-quant-list',
        template: __webpack_require__(/*! raw-loader!./quant-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/components/quant-list/quant-list.component.html"),
        styles: [__webpack_require__(/*! ./quant-list.component.scss */ "./src/app/components/quant-list/quant-list.component.scss")]
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]])
], QuantListComponent);



/***/ }),

/***/ "./src/app/pages/stock-quant-list/stock-quant-list.module.ts":
/*!*******************************************************************!*\
  !*** ./src/app/pages/stock-quant-list/stock-quant-list.module.ts ***!
  \*******************************************************************/
/*! exports provided: StockQuantListPageModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockQuantListPageModule", function() { return StockQuantListPageModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _stock_quant_list_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./stock-quant-list.page */ "./src/app/pages/stock-quant-list/stock-quant-list.page.ts");
/* harmony import */ var _components_quant_list_quant_list_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../components/quant-list/quant-list.component */ "./src/app/components/quant-list/quant-list.component.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../shared/shared.module */ "./src/app/shared/shared.module.ts");









const routes = [
    {
        path: '',
        component: _stock_quant_list_page__WEBPACK_IMPORTED_MODULE_6__["StockQuantListPage"]
    }
];
let StockQuantListPageModule = class StockQuantListPageModule {
};
StockQuantListPageModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes),
            _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__["SharedModule"]
        ],
        entryComponents: [_components_quant_list_quant_list_component__WEBPACK_IMPORTED_MODULE_7__["QuantListComponent"]],
        declarations: [_stock_quant_list_page__WEBPACK_IMPORTED_MODULE_6__["StockQuantListPage"], _components_quant_list_quant_list_component__WEBPACK_IMPORTED_MODULE_7__["QuantListComponent"]]
    })
], StockQuantListPageModule);



/***/ }),

/***/ "./src/app/pages/stock-quant-list/stock-quant-list.page.scss":
/*!*******************************************************************!*\
  !*** ./src/app/pages/stock-quant-list/stock-quant-list.page.scss ***!
  \*******************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3BhZ2VzL3N0b2NrLXF1YW50LWxpc3Qvc3RvY2stcXVhbnQtbGlzdC5wYWdlLnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/pages/stock-quant-list/stock-quant-list.page.ts":
/*!*****************************************************************!*\
  !*** ./src/app/pages/stock-quant-list/stock-quant-list.page.ts ***!
  \*****************************************************************/
/*! exports provided: StockQuantListPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StockQuantListPage", function() { return StockQuantListPage; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/fesm2015/ionic-storage.js");








let StockQuantListPage = class StockQuantListPage {
    constructor(odoo, router, alertCtrl, route, audio, stock, storage) {
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.route = route;
        this.audio = audio;
        this.stock = stock;
        this.storage = storage;
        this.scanner_options = { reader: true, microphone: false, sound: false };
        this.check_scanner_values();
        this.offset = 0;
        this.limit = 25;
        this.limit_reached = false;
    }
    ngOnInit() {
        this.odoo.isLoggedIn().then((data) => {
            if (data == false) {
                this.router.navigateByUrl('/login');
            }
            else {
                this.show_scan_form = this.scanner_options['reader'];
                this.location = this.route.snapshot.paramMap.get('id');
                this.get_location_quants();
            }
        })
            .catch((error) => {
            this.presentAlert('Error al comprobar tu sesión:', error);
        });
    }
    check_scanner_values() {
        this.storage.get('SCANNER').then((val) => {
            if (val) {
                this.scanner_options = val;
            }
        })
            .catch((error) => {
            this.presentAlert('Error al acceder a las opciones del scanner:', error);
        });
    }
    onReadingEmitted(val) {
        this.scanner_reading = val;
        this.search = val;
        this.get_location_quants(this.search);
    }
    onShowEmitted(val) {
        this.show_scan_form = val;
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
    get_location_quants(search = null) {
        this.offset = 0;
        this.limit_reached = false;
        this.stock.get_location_quants(this.location, this.offset, this.limit, search).then((quants_list) => {
            this.quants = quants_list;
            if (Object.keys(quants_list).length < 25) {
                this.limit_reached = true;
            }
            if (Object.keys(this.quants).length == 1) {
                this.router.navigateByUrl('/product/' + this.quants[0]['product_id'][0]);
            }
            this.audio.play('click');
        })
            .catch((error) => {
            this.presentAlert('Error al recuperador el listado de stock:', error);
        });
    }
    get_search_results(ev) {
        this.search = ev.target.value;
        this.get_location_quants(this.search);
    }
    // Infinitescroll
    loadData(event) {
        setTimeout(() => {
            console.log('Loading more locations');
            event.target.complete();
            this.quant_list_infinite_scroll_add();
            // App logic to determine if all data is loaded
            // and disable the infinite scroll
            if (this.limit_reached) {
                event.target.disabled = true;
            }
        }, 500);
    }
    quant_list_infinite_scroll_add() {
        this.offset += this.limit;
        this.stock.get_location_quants(this.location, this.offset, this.limit, this.search).then((data) => {
            let current_length = Object.keys(this.quants).length;
            if (Object.keys(data).length < 25) {
                this.limit_reached = true;
            }
            for (var k in data)
                this.quants[current_length + Number(k)] = data[k];
        })
            .catch((error) => {
            this.presentAlert('Error al recuperador el listado de stock:', error);
        });
    }
    toggleInfiniteScroll() {
        this.infiniteScroll.disabled = !this.infiniteScroll.disabled;
    }
};
StockQuantListPage.ctorParameters = () => [
    { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
    { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"] },
    { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"] },
    { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_7__["Storage"] }
];
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])(_ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"], { static: false }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"])
], StockQuantListPage.prototype, "infiniteScroll", void 0);
StockQuantListPage = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-stock-quant-list',
        template: __webpack_require__(/*! raw-loader!./stock-quant-list.page.html */ "./node_modules/raw-loader/index.js!./src/app/pages/stock-quant-list/stock-quant-list.page.html"),
        styles: [__webpack_require__(/*! ./stock-quant-list.page.scss */ "./src/app/pages/stock-quant-list/stock-quant-list.page.scss")]
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
        _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
        _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
        _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"],
        _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"],
        _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"],
        _ionic_storage__WEBPACK_IMPORTED_MODULE_7__["Storage"]])
], StockQuantListPage);



/***/ })

}]);
//# sourceMappingURL=pages-stock-quant-list-stock-quant-list-module-es2015.js.map
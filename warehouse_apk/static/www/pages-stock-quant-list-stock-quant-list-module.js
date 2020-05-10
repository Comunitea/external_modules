(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-stock-quant-list-stock-quant-list-module"],{

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/quant-list/quant-list.component.html":
/*!*******************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/components/quant-list/quant-list.component.html ***!
  \*******************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-grid>\n  <ion-row>\n    <ion-col size=\"10\">\n        <div><strong>Producto</strong></div>\n    </ion-col>\n\n    <ion-col size=\"2\">\n      <div><strong>Stock</strong></div>\n    </ion-col>\n  </ion-row>\n  <ion-row *ngFor=\"let quant of quants\">\n      <ion-col size=\"10\" style='font-size: small'>\n      <div class=\"product_link\" (click)=\"open_link(quant.product_id[0])\">{{quant.product_id[1]}}</div>\n    </ion-col>\n    \n    <ion-col size=\"2\" style='font-size: small'>\n      <div>{{quant.quantity}} -- ({{quant.reserved_quantity}})</div>\n    </ion-col>\n    \n  </ion-row>\n</ion-grid>");

/***/ }),

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-quant-list/stock-quant-list.page.html":
/*!*********************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-quant-list/stock-quant-list.page.html ***!
  \*********************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-header>\n    <ion-toolbar>\n      <ion-buttons slot=\"start\">\n        <ion-menu-button></ion-menu-button>\n      </ion-buttons>\n      <app-scanner-header slot=\"end\"></app-scanner-header>\n      <ion-title>Stock actual</ion-title>\n    </ion-toolbar>\n  </ion-header>\n  \n  <ion-content>\n    <ion-card>\n      <ion-card-content>\n        <ion-row>\n          <ion-toolbar>\n            <ion-searchbar type=\"text\" (ionInput)=\"get_search_results($event)\" autocomplete=\"on\" showCancelButton=\"always\"></ion-searchbar>\n          </ion-toolbar>\n        </ion-row>\n  \n        <app-quant-list [quants]=\"quants\"></app-quant-list>\n  \n        <ion-infinite-scroll threshold=\"100px\" (ionInfinite)=\"loadData($event)\">\n          <ion-infinite-scroll-content\n            loadingSpinner=\"bubbles\"\n            loadingText=\"Cargando más productos...\">\n          </ion-infinite-scroll-content>\n        </ion-infinite-scroll>\n      </ion-card-content>\n    </ion-card>\n  </ion-content>\n\n  <app-scanner-footer (scanner_reading_changed)=\"onReadingEmitted($event)\" [scanner_reading]=\"scanner_reading\"></app-scanner-footer>");

/***/ }),

/***/ "./src/app/components/quant-list/quant-list.component.scss":
/*!*****************************************************************!*\
  !*** ./src/app/components/quant-list/quant-list.component.scss ***!
  \*****************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("div.danger {\n  color: var(--ion-color-danger);\n}\ndiv.product_link {\n  color: blue;\n  text-decoration: underline;\n  -webkit-text-decoration-color: blue;\n          text-decoration-color: blue;\n  cursor: pointer;\n}\n/* Medias */\n@media screen and (max-width: 576px) {\n  ion-grid > ion-row:first-child {\n    display: none;\n  }\n\n  ion-grid > ion-row {\n    border: 1px black solid;\n  }\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL2NvbXBvbmVudHMvcXVhbnQtbGlzdC9xdWFudC1saXN0LmNvbXBvbmVudC5zY3NzIiwic3JjL2FwcC9jb21wb25lbnRzL3F1YW50LWxpc3QvcXVhbnQtbGlzdC5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFDSTtFQUNJLDhCQUFBO0FDQVI7QURFSTtFQUNJLFdBQUE7RUFDQSwwQkFBQTtFQUNBLG1DQUFBO1VBQUEsMkJBQUE7RUFDQSxlQUFBO0FDQVI7QURJQSxXQUFBO0FBQ0E7RUFDSTtJQUNJLGFBQUE7RUNETjs7RURHRTtJQUNJLHVCQUFBO0VDQU47QUFDRiIsImZpbGUiOiJzcmMvYXBwL2NvbXBvbmVudHMvcXVhbnQtbGlzdC9xdWFudC1saXN0LmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiZGl2IHtcbiAgICAmLmRhbmdlciB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItZGFuZ2VyKTtcbiAgICB9XG4gICAgJi5wcm9kdWN0X2xpbmsge1xuICAgICAgICBjb2xvcjogYmx1ZTtcbiAgICAgICAgdGV4dC1kZWNvcmF0aW9uOiB1bmRlcmxpbmU7XG4gICAgICAgIHRleHQtZGVjb3JhdGlvbi1jb2xvcjogYmx1ZTtcbiAgICAgICAgY3Vyc29yOiBwb2ludGVyO1xuICAgIH1cbn1cblxuLyogTWVkaWFzICovXG5AbWVkaWEgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiA1NzZweCkge1xuICAgIGlvbi1ncmlkID4gaW9uLXJvdzpmaXJzdC1jaGlsZCB7XG4gICAgICAgIGRpc3BsYXk6IG5vbmU7XG4gICAgfVxuICAgIGlvbi1ncmlkID4gaW9uLXJvdyB7XG4gICAgICAgIGJvcmRlcjogMXB4IGJsYWNrIHNvbGlkO1xuICAgIH1cbn0iLCJkaXYuZGFuZ2VyIHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1kYW5nZXIpO1xufVxuZGl2LnByb2R1Y3RfbGluayB7XG4gIGNvbG9yOiBibHVlO1xuICB0ZXh0LWRlY29yYXRpb246IHVuZGVybGluZTtcbiAgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBibHVlO1xuICBjdXJzb3I6IHBvaW50ZXI7XG59XG5cbi8qIE1lZGlhcyAqL1xuQG1lZGlhIHNjcmVlbiBhbmQgKG1heC13aWR0aDogNTc2cHgpIHtcbiAgaW9uLWdyaWQgPiBpb24tcm93OmZpcnN0LWNoaWxkIHtcbiAgICBkaXNwbGF5OiBub25lO1xuICB9XG5cbiAgaW9uLWdyaWQgPiBpb24tcm93IHtcbiAgICBib3JkZXI6IDFweCBibGFjayBzb2xpZDtcbiAgfVxufSJdfQ== */");

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");



var QuantListComponent = /** @class */ (function () {
    function QuantListComponent(router) {
        this.router = router;
    }
    QuantListComponent.prototype.ngOnInit = function () { };
    QuantListComponent.prototype.open_link = function (product_id) {
        this.router.navigateByUrl('/product/' + product_id);
    };
    QuantListComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)
    ], QuantListComponent.prototype, "quants", void 0);
    QuantListComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-quant-list',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./quant-list.component.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/quant-list/quant-list.component.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./quant-list.component.scss */ "./src/app/components/quant-list/quant-list.component.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]])
    ], QuantListComponent);
    return QuantListComponent;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _stock_quant_list_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./stock-quant-list.page */ "./src/app/pages/stock-quant-list/stock-quant-list.page.ts");
/* harmony import */ var _components_quant_list_quant_list_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../components/quant-list/quant-list.component */ "./src/app/components/quant-list/quant-list.component.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../shared/shared.module */ "./src/app/shared/shared.module.ts");









var routes = [
    {
        path: '',
        component: _stock_quant_list_page__WEBPACK_IMPORTED_MODULE_6__["StockQuantListPage"]
    }
];
var StockQuantListPageModule = /** @class */ (function () {
    function StockQuantListPageModule() {
    }
    StockQuantListPageModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
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
    return StockQuantListPageModule;
}());



/***/ }),

/***/ "./src/app/pages/stock-quant-list/stock-quant-list.page.scss":
/*!*******************************************************************!*\
  !*** ./src/app/pages/stock-quant-list/stock-quant-list.page.scss ***!
  \*******************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3BhZ2VzL3N0b2NrLXF1YW50LWxpc3Qvc3RvY2stcXVhbnQtbGlzdC5wYWdlLnNjc3MifQ== */");

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");







var StockQuantListPage = /** @class */ (function () {
    function StockQuantListPage(odoo, router, alertCtrl, route, audio, stock) {
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.route = route;
        this.audio = audio;
        this.stock = stock;
        this.offset = 0;
        this.limit = 25;
        this.limit_reached = false;
    }
    StockQuantListPage.prototype.ngOnInit = function () {
        var _this = this;
        this.odoo.isLoggedIn().then(function (data) {
            if (data == false) {
                _this.router.navigateByUrl('/login');
            }
            else {
                _this.location = _this.route.snapshot.paramMap.get('id');
                _this.get_location_quants();
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    StockQuantListPage.prototype.onReadingEmitted = function (val) {
        this.scanner_reading = val;
        this.search = val;
        this.get_location_quants(this.search);
    };
    StockQuantListPage.prototype.presentAlert = function (titulo, texto) {
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
    StockQuantListPage.prototype.get_location_quants = function (search) {
        var _this = this;
        if (search === void 0) { search = null; }
        this.offset = 0;
        this.limit_reached = false;
        this.stock.get_location_quants(this.location, this.offset, this.limit, search).then(function (quants_list) {
            _this.quants = quants_list;
            if (Object.keys(quants_list).length < 25) {
                _this.limit_reached = true;
            }
            if (Object.keys(_this.quants).length == 1) {
                _this.router.navigateByUrl('/product/' + _this.quants[0]['product_id'][0]);
            }
            _this.audio.play('click');
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperador el listado de stock:', error);
        });
    };
    StockQuantListPage.prototype.get_search_results = function (ev) {
        this.search = ev.target.value;
        this.get_location_quants(this.search);
    };
    // Infinitescroll
    StockQuantListPage.prototype.loadData = function (event) {
        var _this = this;
        setTimeout(function () {
            console.log('Loading more locations');
            event.target.complete();
            _this.quant_list_infinite_scroll_add();
            // App logic to determine if all data is loaded
            // and disable the infinite scroll
            if (_this.limit_reached) {
                event.target.disabled = true;
            }
        }, 500);
    };
    StockQuantListPage.prototype.quant_list_infinite_scroll_add = function () {
        var _this = this;
        this.offset += this.limit;
        this.stock.get_location_quants(this.location, this.offset, this.limit, this.search).then(function (data) {
            var current_length = Object.keys(_this.quants).length;
            if (Object.keys(data).length < 25) {
                _this.limit_reached = true;
            }
            for (var k in data)
                _this.quants[current_length + Number(k)] = data[k];
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperador el listado de stock:', error);
        });
    };
    StockQuantListPage.prototype.toggleInfiniteScroll = function () {
        this.infiniteScroll.disabled = !this.infiniteScroll.disabled;
    };
    StockQuantListPage.ctorParameters = function () { return [
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])(_ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"], { static: false }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonInfiniteScroll"])
    ], StockQuantListPage.prototype, "infiniteScroll", void 0);
    StockQuantListPage = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-stock-quant-list',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./stock-quant-list.page.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-quant-list/stock-quant-list.page.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./stock-quant-list.page.scss */ "./src/app/pages/stock-quant-list/stock-quant-list.page.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_services_odoo_service__WEBPACK_IMPORTED_MODULE_4__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["AlertController"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_5__["AudioService"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_6__["StockService"]])
    ], StockQuantListPage);
    return StockQuantListPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-stock-quant-list-stock-quant-list-module.js.map
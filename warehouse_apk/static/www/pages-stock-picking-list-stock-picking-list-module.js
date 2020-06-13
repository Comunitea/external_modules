(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-stock-picking-list-stock-picking-list-module"],{

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-picking-list/stock-picking-list.page.html":
/*!*************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/pages/stock-picking-list/stock-picking-list.page.html ***!
  \*************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-header>\n  <ion-toolbar class=\"cmnt-front\">\n    <ion-buttons slot=\"start\" >\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n    <ion-title>Listado de Albaranes</ion-title>\n      <ion-buttons slot=\"end\" class=\"cmnt-front\">\n    </ion-buttons>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <ion-card>\n    <ion-card-content>\n      <ion-row>\n        <ion-toolbar>\n          <ion-searchbar type=\"text\" (ionInput)=\"get_search_results($event)\" autocomplete=\"on\" showCancelButton=\"always\"></ion-searchbar>\n        </ion-toolbar>\n\n\n      </ion-row>\n      <ion-row>\n      <ion-col class=\"action-button\"><ion-button (click)=\"Navigate('stock-picking-type-list')\"><ion-icon class=\"primary\" name=\"arrow-undo-circle-outline\" ></ion-icon></ion-button></ion-col>\n\n      <ion-col>\n          \n      </ion-col>\n      <ion-col *ngIf=\"States\" size=3>\n        <ion-select (ionChange)=\"ChangeStateFilter()\" [(ngModel)]=\"StateValue\" interface=\"popover\" okText=\"Aplicar\" cancelText=\"Cancelar\">\n          <ion-select-option *ngFor=\"let state of States\" value='{{state.value}}'>{{state.name}}</ion-select-option>\n        </ion-select>\n        \n      </ion-col>\n      </ion-row>\n      <!--app-picking-list *ngIf=\"pickings\" [code]=\"current_code\" [filter]=\"filter\" [picks]=\"pickings\"></app-picking-list-->\n\n      <ion-row *ngFor=\"let pick of pickings; let even = even; let odd =  odd\" (click)=\"OpenLink(pick.id)\" [ngClass]=\"{'row-odd': odd, 'row-even': even}\" style=\"min-height: 30px\">\n        <ion-col class=\"ion-align-self-center\">\n          <span class=\"product-link \">{{pick.apk_name}}</span>\n        </ion-col>\n        <ion-col class=\"ion-align-self-center ion-text-center\" size=\"1\">\n            <span>{{pick.move_line_count}}</span>\n        </ion-col>\n        <ion-col class=\"ion-align-self-center ion-text-left\" *ngIf=\"pick.default_location.value === 'location_id'\">\n          <div>{{pick.location_id.name}}</div>\n        </ion-col>\n        <ion-col class=\"ion-align-self-center  ion-text-left\" *ngIf=\"pick.default_location.value === 'location_dest_id'\">\n          <div>{{pick.location_dest_id.name}}</div>\n        </ion-col>\n         \n        <ion-col size=\"3\n        \" class=\"ion-align-self-center ion-text-center\">\n        {{pick.scheduled_date}}\n        <!--/ion-col>\n        <ion-col  class=\"ion-align-self-center\"-->\n        <ion-icon  size=\"normal\" class=\"{{'state_'+ pick.state.value}} \" name=\"{{StateIcon[pick.state.value]}}\"></ion-icon>\n        </ion-col>\n      </ion-row>\n\n      <ion-infinite-scroll threshold=\"100px\" (ionInfinite)=\"loadData($event)\">\n        <ion-infinite-scroll-content\n          loadingSpinner=\"bubbles\"\n          loadingText=\"Cargando más productos...\">\n        </ion-infinite-scroll-content>\n      </ion-infinite-scroll>\n    </ion-card-content>\n  </ion-card>\n</ion-content>");

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
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../shared/shared.module */ "./src/app/shared/shared.module.ts");







//import { PickingListComponent } from '../../components/picking-list/picking-list.component';

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
                _shared_shared_module__WEBPACK_IMPORTED_MODULE_7__["SharedModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes)
            ],
            // entryComponents: [ PickingListComponent ],
            // declarations: [ StockPickingListPage, PickingListComponent ]
            declarations: [_stock_picking_list_page__WEBPACK_IMPORTED_MODULE_6__["StockPickingListPage"]]
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
        // this.offset = 0;
        // this.limit = 5;
        // this.limit_reached = false;
    }
    StockPickingListPage.prototype.ionViewDidEnter = function () {
        this.offset = 0;
        this.limit = this.MaxNumber = 25;
        this.limit_reached = false;
        this.GetPickingList(null, this.offset, this.limit);
    };
    StockPickingListPage.prototype.ngOnInit = function () {
        var _this = this;
        this.odoo.isLoggedIn().then(function (data) {
            if (data === false) {
                _this.router.navigateByUrl('/login');
            }
            else {
                // Lo voy a cambiar por
                _this.StateValue = '';
                _this.StateIcon = _this.stock.getStateIcon('stock.move');
                _this.States = _this.stock.GetModelInfo('stock.picking', 'filter_state');
                var All = { name: 'Todos', value: 'all' };
                _this.States.push(All);
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    StockPickingListPage.prototype.onReadingEmitted = function (val) {
        this.scanner_reading = val;
        this.search = val;
        this.offset = 0;
        this.GetPickingList(this.search, this.offset, this.limit);
    };
    StockPickingListPage.prototype.Navigate = function (Url) {
        return this.router.navigateByUrl('/' + Url);
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
    StockPickingListPage.prototype.OpenLink = function (PickId) {
        this.router.navigateByUrl('/stock-picking/' + PickId + '/1');
    };
    StockPickingListPage.prototype.ChangeStateFilter = function () {
        var _this = this;
        if (this.StateValue === '') {
            this.State = null;
        }
        else {
            this.State = this.States.filter(function (x) { return x['value'] === _this.StateValue; })[0];
        }
        this.offset = 0;
        this.GetPickingList(this.search, this.offset, this.limit);
    };
    StockPickingListPage.prototype.GetPickingList = function (search, offset, limit) {
        var _this = this;
        if (search === void 0) { search = null; }
        this.limit_reached = false;
        this.stock.GetPickingList(search, offset, limit, this.State).then(function (data) {
            _this.pickings = data;
            if (data.length < _this.MaxNumber) {
                _this.limit_reached = true;
            }
            // if (Object.keys(this.pickings).length === 1){
            //  this.stock.SetModelInfo('stock.picking', 'ActiveId', data[0]['id']);
            //  this.router.navigateByUrl('/stock-picking/' + data[0]['id']);
            // }
        });
    };
    /*
    get_picking_list(search = null){
      this.offset = 0;
      this.limit_reached = false;
      this.stock.GetPicking(this.compute_domain(search), null, 'tree', this.offset, this.limit, search).then((picking_list: Array<{}>) => {
        this.pickings = picking_list;
        // if (this.pickings[0] && this.pickings[0]['picking_fields']) {
        //  this.not_allowed_fields = this.pickings[0]['picking_fields'].split(',');
        //  console.log(this.not_allowed_fields);
        // }
        if (Object.keys(picking_list).length < 25){
          this.limit_reached = true;
        }
        if (Object.keys(this.pickings).length == 1){
          this.router.navigateByUrl('/stock-picking/'+this.pickings[0]['id']);
        }
  
        this.audio.play('click');
      })
      .catch((error) => {
        console.log(error);
        this.presentAlert('Error al recuperador el listado de operaciones:', error);
      });
    } */
    StockPickingListPage.prototype.get_search_results = function (ev) {
        this.search = ev.target.value;
        this.offset = 0;
        this.GetPickingList(this.search, this.offset, this.limit);
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
        this.stock.GetPickingList(this.search, this.offset, this.limit, this.State).then(function (data) {
            if (data.length < _this.MaxNumber) {
                _this.limit_reached = true;
            }
            for (var _i = 0, data_1 = data; _i < data_1.length; _i++) {
                var pick = data_1[_i];
                _this.pickings.push(pick);
            }
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
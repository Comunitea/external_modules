(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-move-form-move-form-module"],{

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/move-form/move-form.page.html":
/*!*******************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/pages/move-form/move-form.page.html ***!
  \*******************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-header>\n  <ion-toolbar class=\"cmnt-front\">\n    <ion-buttons slot=\"start\">\n      <ion-menu-button class=\"cmnt-front\"></ion-menu-button>\n    </ion-buttons>\n    <app-scanner-header  class=\"cmnt-back\" slot=\"end\">Movimiento</app-scanner-header>\n    <ion-title  class=\"cmnt-button\" *ngIf=\"data\" style=\"padding-inline-end: 2px; padding-inline-start: 2px;\">\n      {{data.picking_id.name}}\n    </ion-title>\n\n          \n  </ion-toolbar>\n</ion-header>\n<ion-content *ngIf=\"data\">\n  <ion-card >\n\n    <ion-card-header>\n    <ion-row>\n        <ion-col class=\"link\" (click)=\"GetMoveInfo(data.id, -1)\">Anterior\n        </ion-col>\n        \n        <!-- <ion-col *ngIf=\"data.ready_to_validate\" class=\"link\" (click)=\"button_validate(data.picking_id.id)\">Validar\n        </ion-col> -->\n        <ion-col class=\"ion-text-center\">\n          <span *ngIf=\"data && data.active_location_id\">{{data.active_location_id.name}}</span>\n        </ion-col>\n        <ion-col class=\"link ion-text-right\" (click)=\"GetMoveInfo(data.id, +1)\">Siguiente\n        </ion-col>\n      </ion-row>\n\n\n      <ion-card-title class=\"ion-text-center\">{{data.product_id.name}}</ion-card-title>\n      <ion-card-title class=\"ion-text-right\"> \n      </ion-card-title>\n    </ion-card-header>\n  \n    <ion-card-content class=\"ion-text-center\">\n\n      <div class=\"product_img\" class=\"ion-text-center\" *ngIf=\"data.image\">\n        <ion-img *ngIf=\"data.base64\" src=\"data:image/jpeg;base64,{{ data.product_id.image}}\" ></ion-img>\n        <!--ion-img *ngIf=\"!data.base64\" src=\"{{ data.product_id.image }}\"></ion-img-->\n      </div>\n      <!--div><strong>{{data.sale_id && (data.sale_id['name'] + \": \")}}</strong>{{data.picking_id['id'] && data.picking_id['display_name']}}</div-->\n      <!--div><strong>{{data.location_id.name}} >> {{data.location_dest_id.name}}</strong></div-->\n      <!-- <div [ngSwitch]=\"data.tracking\">\n        <strong *ngSwitchCase=\"'none'\">Sin tracking</strong>\n        <strong *ngSwitchCase=\"'lot'\">Por lotes</strong>\n        <strong *ngSwitchCase=\"'serial'\">Por serie</strong>\n      </div> -->\n      <ion-row> \n        <ion-col size=\"5\"class=\"ion-text-left\"><strong>{{data.product_id.default_code || data.product_id.barcode}}</strong></ion-col>\n        <ion-col size=\"2\"class=\"ion-text-right\"><strong>Cant: </strong></ion-col>\n        <ion-col size=\"4\"class=\"ion-text-right\"><ion-badge class=\"primary\" style=\"vertical-align: bottom\">  {{data.quantity_done}} de {{data.product_uom_qty}} {{data.product_uom.name}} </ion-badge></ion-col>\n      </ion-row>\n      <ion-row *ngIf=\"data.state.value != 'cancel' && data.state.value != 'done' && data.move_line_ids.length == 1 && data.tracking.value == 'none'\">\n      </ion-row>\n\n      <!--div *ngIf=\"data.state.value != 'cancel' && data.state.value != 'done' && data.tracking.value !='none'\">\n        <div>\n          <ion-badge class=\"primary\"> {{data.quantity_done}} de {{data.product_uom_qty}} </ion-badge> \n        </div>\n        <strong>Lotes/Serie:</strong>\n        <div *ngFor=\"let lot of data.lot_ids\">\n          {{lot.name}}\n        </div>\n      </div-->\n\n      <!--div *ngIf=\"new_lots\">\n        <strong>Añadiendo:</strong>\n        <div *ngFor=\"let lot of new_lots\">\n          {{lot[0]}}\n        </div>\n      </div-->\n      <ion-row *ngIf=\"data.state.value != 'done'\">\n        <!--BOTON VOLVER-->\n        <ion-col class=\"action-button\"><ion-button (click)=\"go_back()\"><ion-icon class=\"primary\" name=\"arrow-undo-circle-outline\" ></ion-icon></ion-button></ion-col>\n        <!--BOTON OPCIONES AVANZADAS-->\n        <ion-col class=\"action-button\"><ion-button (click)=\"PresentMenuOptions()\"><ion-icon class=\"primary\" name=\"ellipsis-vertical-outline\" ></ion-icon></ion-button></ion-col>\n        <!--BOTON MOSTRASR LINEAS/LOTES-->\n        <ion-col *ngIf=\"data.tracking.value != 'none'\" class=\"action-button\"><ion-button (click)= \"AlternateShowLots()\"><ion-icon class=\"primary\" name=\"eye-outline\" ></ion-icon></ion-button></ion-col>\n        <!--BOTON VOLVER BORRAR LOTES ????-->\n        <ion-col *ngIf=\"data.move_line_count ==1 && data.tracking.value == 'none'\" class=\"action-button\">\n          <ion-button><ion-icon class=\"primary\" name=\"remove-circle-outline\" (click)=\"GetMoveInfo(data.id, -1)\"></ion-icon></ion-button>\n        </ion-col>\n        <!--BOTON VALIDAR-->\n        <ion-col>\n          <ion-button *ngIf=\"data.picking_field_status && ['partially_available', 'assigned'].indexOf(data.state.value) != -1\" (click)=\"DoMoveValidate()\">\n            <ion-icon class=\"primary {{'state_'+ data.state.value}}\" name=\"checkmark-done-circle-outline\" ></ion-icon>\n          </ion-button>\n        </ion-col>\n        <!--BOTON SIGUIENTE-->\n        <ion-col class=\"action-button\" *ngIf=\"data.move_line_count ==1 && data.tracking.value == 'none'\">\n          <ion-button><ion-icon class=\"primary\" name=\"add-circle-outline\" (click)=\"GetMoveInfo(data.id, +1)\"></ion-icon></ion-button>\n        </ion-col>\n        <ion-col class=\"action-button\" style=\"max-width: 40px; align-self: flex-end\">\n          <ion-icon size=\"large\" class=\"{{'state_'+ data.state.value}}\"  name=\"{{StateIcon[data.state.value]}}\"></ion-icon>\n        </ion-col>\n\n      </ion-row>\n    </ion-card-content>\n  </ion-card>\n  <ion-card *ngIf=\"data.state.value != 'done' && AdvanceOptions && data\">\n    <ion-card-header>\n      <ion-card-title class=\"ion-text-center\">Opciones avanzadas: </ion-card-title>\n      <ion-card-content>\n        <ion-row>\n          <ion-col>\n          <span class='product-link'> Progreso: </span>{{data.field_status && 'Preparado' || 'No preparado'}} \n          </ion-col>\n          <ion-col>\n          <span class='product-link'> Estado: </span>{{data.state.name}} \n          </ion-col>\n        </ion-row>\n        <ion-row>\n          <ion-col>\n          <span class='product-link'> Origen: </span>{{data.location_id.name}} \n          </ion-col>\n          <ion-col>\n          <span class='product-link'> Destino: </span>{{data.location_dest_id.name}} \n          </ion-col>\n        </ion-row>\n      </ion-card-content>\n    </ion-card-header>\n    <ion-card-content>\n      \n      <ion-row>\n        <!--ion-col class=\"action-button\">\n          <ion-button (click)= \"AlternateShowLots()\"><ion-icon class=\"primary\" name=\"eye-outline\" ></ion-icon></ion-button>\n        </ion-col-->\n        <!--BOTON VOLVER-->\n        <ion-col class=\"action-button\">\n          <ion-button *ngIf=\"data.state.value=='done'\"><ion-icon class=\"secondary\" name=\"checkmark-done-circle-outline\" ></ion-icon></ion-button>\n        </ion-col>\n        <!--BOTON ACTION_ASSING>\n\n        <ion-col class=\"action-button\" *ngIf=\"['partially_available', 'confirmed'].indexOf(data.state.value) != -1\">\n          <ion-button (click)=\"ActionAssign(data.id)\"><ion-icon class=\"primary\" name=\"checkmark-outline\"></ion-icon></ion-button>\n        </ion-col>\n        <BOTON DO_UNRESERVE>\n        <ion-col *ngIf=\"['partially_available', 'assigned', 'confirmed'].indexOf(data.state.value) != -1\" class=\"action-button\">\n          <ion-button (click)=\"ActionUnReserve(data.id)\"><ion-icon class=\"primary\" name=\"trash-outline\" ></ion-icon></ion-button>\n        </ion-col-->\n\n        <ion-col *ngIf=\"move_lots && 'done' != data.state.value && data.tracking.value != 'none'\" class=\"action-button\">\n          <ion-button ><ion-icon class=\"primary\" name=\"flash-off-outline\" ></ion-icon>\n          </ion-button>\n        </ion-col>\n        <!--BOTON BORRA LOS LOTES, PERO NO LOS MOVIMIENTOS>\n        <ion-col (click)=\"CleanLots(data.id)\" *ngIf=\"data.tracking.value != 'none' && 'done' != data.state.value\" class=\"action-button\">\n          <ion-button ><ion-icon class=\"primary\" name=\"reload-circle-outline\"></ion-icon></ion-button>\n        </ion-col>\n        <BOTON NUEVA LINEA>\n        <ion-col (click)=\"CreateNewSmlId(data.id)\" *ngIf=\"data.tracking.value != 'serial' && ['draft', 'done'].indexOf(data.state.value) != 0\" class=\"action-button\">\n          <ion-button ><ion-icon class=\"primary\" name=\"duplicate-outline\"></ion-icon></ion-button>\n        </ion-col-->\n\n      </ion-row>\n    </ion-card-content>\n  </ion-card>\n  <div *ngIf=\"data.state.value != 'done' && data && ShowLots\">\n    <ion-card >\n      <ion-card-header>\n        <ion-card-title *ngIf=\"ChangeLotNames && LotNames.length > 0\" class=\"ion-text-center\">\n          <ion-button (click)=\"ActionApplyLotNames()\">\n            <ion-icon class=\"primary\" name=\"checkmark-done-circle-outline\" ></ion-icon></ion-button>\n          </ion-card-title>\n      </ion-card-header>\n      <ion-card-content>\n        <ion-row>\n            <ion-col size=\"12\" *ngFor=\"let lot of LotNames\">\n              <ion-row>\n                <ion-col size=\"10\" class=\"ion-text-center\" >\n                  <span class=\"product-link\" style=\"font-size: large\"><strong>{{lot}}</strong></span>\n                </ion-col>\n                <ion-col size=\"2\" class=\"ion-text-center\" >\n                  <ion-icon (click) = \"ChangeLineLotId(data['id'], false, lot, false)\" \n                  *ngIf=\"data.state.value != done\" size=\"small\" color = \"danger\" \n                  style=\"vertical-align: bottom state_icon\" name=\"trash-outline\"></ion-icon>\n                </ion-col>\n              </ion-row>\n              <!--ion-icon  size=\"small\" style=\"vertical-align: bottom state_icon\" class=\"{{'state_'+ sml.state.value}}\" name=\"{{StateIcon[sml.state.value]}}\"></ion-icon-->\n            </ion-col>\n           </ion-row>\n        <!--ion-card-title class=\"ion-text-center\" (click) = \"ChangeLineLotId(data['id'], false, lot, false)\">{{lot}}</ion-card-title-->\n      </ion-card-content>\n    </ion-card>\n\n   \n\n    <ion-card *ngIf=\"data.state.value != 'done' && LotNames.length == 0\">\n      <ion-card-header>\n        <ion-card-title class=\"ion-text-center\">\n          Esperando Serial/Lote\n        </ion-card-title>\n      </ion-card-header>\n    </ion-card>\n  </div>\n  <div *ngIf=\"data && ShowMoves\">\n    <ion-card *ngFor=\"let sml of data.move_line_ids\">\n      <!--ion-card-header>\n        <ion-card-title class=\"ion-text-center\">{{sml.field_status_apk}} / {{data.tracking.value}} // </ion-card-title>\n      </ion-card-header-->\n      <ion-card-content class=\"sml_not_done\">\n          <ion-row [ngClass]=\"{'success': sml.state.value=='done'}\"> \n            <!-- BORRAR LINEA -->\n            <ion-col size=\"1\" class=\"ion-text-right state_icon\" *ngIf=\"AdvanceOptions && data.state.value != done\">\n              <ion-icon (click) = \"RemoveMoveLineId(sml.id)\" size=\"small\" color = \"danger\" style=\"vertical-align: bottom state_icon\" name=\"trash-outline\"></ion-icon>\n              <!--ion-icon  size=\"small\" style=\"vertical-align: bottom state_icon\" class=\"{{'state_'+ sml.state.value}}\" name=\"{{StateIcon[sml.state.value]}}\"></ion-icon-->\n            </ion-col>\n            <!-- ORIGEN --> \n            <ion-col \n            (click) =\"ChangeLineLocationId(sml)\"\n            *ngIf=\"read_status(sml.field_status_apk, 'location_id', 'view')\"\n              [ngClass]=\"{'sml_done': read_status(sml.field_status_apk, 'location_id', 'done')}\"\n              size-xs=\"3\" size-sm=\"2\" size-md=\"2\">\n              <div>{{sml.location_id.name}}</div>\n              <div *ngIf=\"read_status(sml.field_status_apk, 'package_id', 'view')\">P:{{sml.package_id && sml.package_id.name}} </div>\n            </ion-col>\n            <!-- DESTINO-->\n            <ion-col \n              (click) =\"ChangeLineLocationId(sml)\"\n              *ngIf=\"read_status(sml.field_status_apk, 'location_dest_id', 'view')\"\n              [ngClass]=\"{'sml_done': read_status(sml.field_status_apk, 'location_dest_id', 'done')}\" size-xs=\"3\" size-sm=\"2\" size-md=\"2\">\n              <div>{{sml.location_dest_id.name}}</div>\n              <div *ngIf=\"read_status(sml.field_status_apk, 'result_package_id', 'view')\">P:{{sml.result_package_id && sml.result_package_id.name}}</div>\n            </ion-col>\n            <!-- LOTE -->\n            <ion-col  style=\"text-align: center\"\n             (click) =\"ChangeLineLotId(data['id'],sml.id, sml.lot_id && sml.lot_id.name, false)\"\n             *ngIf=\"data.tracking.value != 'none' && read_status(sml.field_status_apk, 'lot_id', 'view')\" \n              [ngClass]=\"{'sml_done': read_status(sml.field_status_apk, 'lot_id', 'done')}\"\n              size-xs=\"5\" size-sm=\"4\" size-md=\"4\">\n              {{sml.lot_id && sml.lot_id.name || 'Lote' }}\n            </ion-col>\n\n            <!--CANTIDAD -->\n            <ion-col  size-xs=\"2\" size-sm=\"1\" size-md=\"1\" *ngIf=\"data.tracking.value != 'serial' && read_status(sml.field_status_apk, 'qty_done', 'view')\" class=\"ion-text-center\">\n                <ion-badge class=\"link\" (click)=\"ChangeQty(sml, -1)\" style=\"padding: 3px; margin-right: 15px\"> <ion-icon class=\"primary\" name=\"remove-circle-outline\"></ion-icon> </ion-badge>\n                <ion-badge [ngClass]=\"{'back_state_draft': QtyDirty === true}\" (click)=\"InputQty('Cantidad', sml)\" > {{sml.qty_done}} de  {{sml.product_uom_qty}}</ion-badge>\n                <ion-badge class=\"link\" (click)=\"ChangeQty(sml, +1)\" style=\"padding: 3px; margin-left: 15px\"> <ion-icon class=\"primary\" name=\"add-circle-outline\"></ion-icon> </ion-badge>\n            </ion-col>\n            <!--BOTONES-->\n          </ion-row>\n          \n      </ion-card-content>\n    </ion-card>\n  </div>\n  <!--div *ngIf=\"data && data.tracking.value=='none'\">\n    <ion-card *ngFor=\"let sml of data.move_line_ids\">\n      <ion-card-content>\n              <ion-row [ngClass]=\"{'success': sml.qty_done == sml.product_uom_qty}\">\n              <ion-col size-xs=\"6\" size-sm=\"2\" size-md=\"2\">{{sml.location_id.name}}</ion-col>\n              <ion-col size-xs=\"6\" size-sm=\"2\" size-md=\"2\">\n                <ion-badge class=\"link\" (click)=\"ChangeQty(-1)\" style=\"margin-right: 15px\"> - </ion-badge>\n                <ion-badge > {{sml.qty_done}} </ion-badge>\n                <ion-badge class=\"link\" (click)=\"ChangeQty(+1)\" style=\"margin-left: 15px\"> + </ion-badge>\n              </ion-col>\n              <ion-col>{{StateIcon[sml.state.value]}}\n                <ion-icon  size=\"small\" style=\"vertical-align: bottom\" class=\"{{'state_'+ sml.state.value}}\" name=\"{{StateIcon[sml.state.value]}}\"></ion-icon>\n              </ion-col>\n            </ion-row>      \n      </ion-card-content>\n    </ion-card>\n  </div-->\n</ion-content>\n\n<app-scanner-footer (scanner_reading_changed)=\"onReadingEmitted($event)\" [scanner_reading]=\"scanner_reading\"></app-scanner-footer>\n\n<ng-template #lineDoneTemplate>\n  <ion-col><strong>Cantidad: </strong><br/>\n    <ion-badge class=\"secondary\"> {{data.quantity_done}} de {{data.product_uom_qty}} </ion-badge>\n  </ion-col>\n</ng-template>");

/***/ }),

/***/ "./src/app/pages/move-form/move-form.module.ts":
/*!*****************************************************!*\
  !*** ./src/app/pages/move-form/move-form.module.ts ***!
  \*****************************************************/
/*! exports provided: MoveFormPageModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MoveFormPageModule", function() { return MoveFormPageModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _move_form_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./move-form.page */ "./src/app/pages/move-form/move-form.page.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../shared/shared.module */ "./src/app/shared/shared.module.ts");








var routes = [
    {
        path: '',
        component: _move_form_page__WEBPACK_IMPORTED_MODULE_6__["MoveFormPage"]
    }
];
var MoveFormPageModule = /** @class */ (function () {
    function MoveFormPageModule() {
    }
    MoveFormPageModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes),
                _shared_shared_module__WEBPACK_IMPORTED_MODULE_7__["SharedModule"]
            ],
            declarations: [_move_form_page__WEBPACK_IMPORTED_MODULE_6__["MoveFormPage"]]
        })
    ], MoveFormPageModule);
    return MoveFormPageModule;
}());



/***/ }),

/***/ "./src/app/pages/move-form/move-form.page.scss":
/*!*****************************************************!*\
  !*** ./src/app/pages/move-form/move-form.page.scss ***!
  \*****************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("ion-img {\n  max-width: 100px;\n  max-height: 100px;\n  margin-left: auto;\n  margin-right: auto;\n  width: 100px;\n}\n\n.link {\n  cursor: pointer;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL3BhZ2VzL21vdmUtZm9ybS9tb3ZlLWZvcm0ucGFnZS5zY3NzIiwic3JjL2FwcC9wYWdlcy9tb3ZlLWZvcm0vbW92ZS1mb3JtLnBhZ2Uuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNJLGdCQUFBO0VBQ0EsaUJBQUE7RUFDQSxpQkFBQTtFQUNBLGtCQUFBO0VBQ0EsWUFBQTtBQ0NKOztBREVBO0VBQ0ksZUFBQTtBQ0NKIiwiZmlsZSI6InNyYy9hcHAvcGFnZXMvbW92ZS1mb3JtL21vdmUtZm9ybS5wYWdlLnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJpb24taW1nIHtcbiAgICBtYXgtd2lkdGg6IDEwMHB4O1xuICAgIG1heC1oZWlnaHQ6IDEwMHB4O1xuICAgIG1hcmdpbi1sZWZ0OiBhdXRvO1xuICAgIG1hcmdpbi1yaWdodDogYXV0bztcbiAgICB3aWR0aDogMTAwcHg7XG59XG5cbi5saW5re1xuICAgIGN1cnNvcjogcG9pbnRlcjtcbn0iLCJpb24taW1nIHtcbiAgbWF4LXdpZHRoOiAxMDBweDtcbiAgbWF4LWhlaWdodDogMTAwcHg7XG4gIG1hcmdpbi1sZWZ0OiBhdXRvO1xuICBtYXJnaW4tcmlnaHQ6IGF1dG87XG4gIHdpZHRoOiAxMDBweDtcbn1cblxuLmxpbmsge1xuICBjdXJzb3I6IHBvaW50ZXI7XG59Il19 */");

/***/ }),

/***/ "./src/app/pages/move-form/move-form.page.ts":
/*!***************************************************!*\
  !*** ./src/app/pages/move-form/move-form.page.ts ***!
  \***************************************************/
/*! exports provided: MoveFormPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MoveFormPage", function() { return MoveFormPage; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/__ivy_ngcc__/fesm5/ionic-storage.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_stock_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../services/stock.service */ "./src/app/services/stock.service.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");
/* harmony import */ var _components_scanner_scanner_footer_scanner_footer_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../components/scanner/scanner-footer/scanner-footer.component */ "./src/app/components/scanner/scanner-footer/scanner-footer.component.ts");
/* harmony import */ var _services_scanner_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../services/scanner.service */ "./src/app/services/scanner.service.ts");











// import { setMaxListeners } from 'cluster';

var MoveFormPage = /** @class */ (function () {
    function MoveFormPage(scanner, odoo, router, alertCtrl, route, audio, stock, storage, location, loadingController, actionSheetController) {
        this.scanner = scanner;
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.route = route;
        this.audio = audio;
        this.stock = stock;
        this.storage = storage;
        this.location = location;
        this.loadingController = loadingController;
        this.actionSheetController = actionSheetController;
        this.moves = ['up', 'down', 'left', 'right'];
    }
    MoveFormPage.prototype.handleKeyboardEvent = function (event) {
        var _this = this;
        if (this.stock.GetModelInfo('App', 'ActivePage') === 'MoveFormPage') {
            this.scanner.key_press(event);
            this.scanner.timeout.then(function (val) {
                _this.onReadingEmitted(val);
            });
        }
    };
    MoveFormPage.prototype.CreateButtons = function () {
        var _this = this;
        var Id = this.data['id'];
        var State = this.data['state'].value;
        var Tracking = this.data['tracking'].value;
        // tslint:disable-next-line:prefer-const
        var buttons = [{
                text: '',
                icon: 'close',
                role: 'Cancelar',
                handler: function () {
                    console.log('Cancel clicked');
                }
            }];
        if (this.data) {
            if (['partially_available', 'confirmed'].indexOf(State) !== -1) {
                var button = {
                    text: 'Reservar',
                    icon: '',
                    role: '',
                    handler: function () {
                        _this.ActionAssign(Id);
                    }
                };
                buttons.push(button);
            }
            if (['partially_available', 'assigned', 'confirmed'].indexOf(State) !== -1) {
                var button = {
                    text: 'Quitar reserva',
                    icon: '',
                    role: '',
                    handler: function () {
                        _this.ActionUnReserve(Id);
                    }
                };
                buttons.push(button);
            }
            if (this.LotNames && 'done' !== State && Tracking !== 'none') {
                var button = {
                    text: 'Borrar lotes',
                    icon: '',
                    role: '',
                    handler: function () {
                        _this.CleanLots(Id);
                    }
                };
                buttons.push(button);
            }
            if (this.LotNames && 'done' !== State && Tracking !== 'none') {
                var button = {
                    text: 'Nuevo',
                    icon: '',
                    role: '',
                    handler: function () {
                        _this.CreateNewSmlId(Id);
                    }
                };
                buttons.push(button);
            }
            // buttons.push(button);
            // buttons.push(buttonReset);
        }
        return buttons;
    };
    MoveFormPage.prototype.PresentMenuOptions = function () {
        return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"])(this, void 0, void 0, function () {
            var actionSheet;
            return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"])(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.audio.play('click');
                        return [4 /*yield*/, this.actionSheetController.create({
                                buttons: this.CreateButtons()
                            })];
                    case 1:
                        actionSheet = _a.sent();
                        return [4 /*yield*/, actionSheet.present()];
                    case 2:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    MoveFormPage.prototype.ionViewDidEnter = function () {
        this.stock.SetModelInfo('App', 'ActivePage', 'MoveFormPage');
        this.InitVars();
        var move = this.route.snapshot.paramMap.get('id');
        this.GetMoveInfo(move);
    };
    MoveFormPage.prototype.ngOnInit = function () {
        var _this = this;
        this.odoo.isLoggedIn().then(function (data) {
            if (data === false) {
                _this.router.navigateByUrl('/login');
            }
            else {
                _this.storage.get('CONEXION').then(function (con) {
                    _this.placeholder = con.url + '/web/static/src/img/placeholder.png';
                })
                    .catch(function (error) {
                    _this.presentAlert('Error al comprobar tu sesión:', error);
                });
                _this.InitVars();
                var move = _this.route.snapshot.paramMap.get('id');
                _this.GetMoveInfo(move);
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al comprobar tu sesión:', error);
        });
    };
    MoveFormPage.prototype.InitVars = function () {
        this.StateIcon = this.stock.getStateIcon('stock.move');
        this.FirstLoad = true;
        this.QtyDirty = false;
        this.InitData();
    };
    MoveFormPage.prototype.InitData = function () {
        this.ChangeLotNames = false;
        this.LotNames = [];
    };
    MoveFormPage.prototype.read_status = function (field, campo, propiedad) {
        return this.stock.read_status(field, campo, propiedad);
    };
    MoveFormPage.prototype.AlternateShowLots = function () {
        this.audio.play('click');
        this.ShowLots = !this.ShowLots;
        this.ShowMoves = !this.ShowLots;
    };
    MoveFormPage.prototype.AlternateAdvanceOptions = function () {
        this.audio.play('click');
        this.AdvanceOptions = !this.AdvanceOptions;
    };
    MoveFormPage.prototype.go_back = function () {
        this.audio.play('click');
        this.location.back();
    };
    MoveFormPage.prototype.GetMovesDone = function (moves, value) {
        var _this = this;
        if (value === void 0) { value = true; }
        return moves.filter(function (move) { return _this.stock.read_status(move['field_status_apk'], 'qty_done', 'done') === value; });
    };
    MoveFormPage.prototype.GetMovesToChangeLoc = function (moves, confirm) {
        var _this = this;
        if (confirm === void 0) { confirm = false; }
        var loc = this.data['default_location'].value;
        // Si confirmar:
        // filtro los movimeintos que ya tienen esa ubicación y no hechos
        if (confirm) {
            return moves.filter(function (move) { return (_this.stock.read_status(move['field_status_apk'], loc, 'done') === true) &&
                (_this.stock.read_status(move['field_status_apk'], 'qty_done', 'done') === false); });
        }
        // Si no confirmo filtro los movimeintos:
        // que ya tienen ubicación y no están hechos
        // y los que no tengan ubicación
        return moves.filter(function (move) {
            return (_this.stock.read_status(move['field_status_apk'], loc, 'done') === false) ||
                (_this.stock.read_status(move['field_status_apk'], loc, 'done') === true) &&
                    (_this.stock.read_status(move['field_status_apk'], 'qty_done', 'done') === false);
        });
    };
    MoveFormPage.prototype.onReadingEmitted = function (val) {
        if (this.moves.includes(val)) {
            this.page_controller(val);
        }
        else {
            this.scanner_reading = val;
            this.process_reading();
        }
    };
    // Navigation
    MoveFormPage.prototype.page_controller = function (direction) {
        if (direction === 'up') {
            console.log('up');
            this.router.navigateByUrl('/stock-picking/' + this.data['picking_id']['id'] + '/' + this.data['picking_id']['code']);
        }
        else if (direction === 'down') {
            console.log('down');
            if (this.data['ready_to_validate']) {
                this.button_validate(this.data['picking_id']['id']);
            }
            else {
                this.action_confirm();
            }
        }
        else if (direction === 'left') {
            console.log('left');
            this.GetMoveInfo(this.data['id'], -1);
        }
        else if (direction === 'right') {
            console.log('right');
            this.GetMoveInfo(this.data['id'], +1);
        }
    };
    MoveFormPage.prototype.presentAlert = function (titulo, texto) {
        return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"])(this, void 0, void 0, function () {
            var alert;
            return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"])(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.alertCtrl.create({
                            header: titulo,
                            subHeader: texto,
                            buttons: ['Ok'],
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
    MoveFormPage.prototype.InputQty = function (titulo, SmlId) {
        return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"])(this, void 0, void 0, function () {
            var values, Qty, alert;
            var _this = this;
            return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"])(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.audio.play('click');
                        if (this.data['state'].value === 'done') {
                            return [2 /*return*/];
                        }
                        if (this.QtyDirty) {
                            values = { qty_done: SmlId['qty_done'] };
                            this.UpdateSmlIdField(SmlId['id'], values);
                            this.QtyDirty = false;
                            return [2 /*return*/];
                        }
                        Qty = SmlId['qty_done'] || SmlId['product_uom_qty'];
                        return [4 /*yield*/, this.alertCtrl.create({
                                header: 'Cantidad',
                                subHeader: '',
                                inputs: [{ name: 'qty_done',
                                        value: Qty,
                                        type: 'number',
                                        id: 'qty-id',
                                        placeholder: SmlId['qty_done'] }],
                                buttons: [{
                                        text: 'Cancelar',
                                        role: 'cancel',
                                        cssClass: 'secondary',
                                        handler: function () {
                                            console.log('Confirm Cancel');
                                        }
                                    }, {
                                        text: 'Aplicar',
                                        handler: function (data) {
                                            if (SmlId['qty_done'] !== data['qty_done']) {
                                                var values = { qty_done: data['qty_done'] };
                                                _this.UpdateSmlIdField(SmlId['id'], values);
                                            }
                                        }
                                    }],
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
    MoveFormPage.prototype.UpdateSmlIdField = function (SmlId, values) {
        var _this = this;
        if (this.data['state'].value === 'done') {
            return;
        }
        this.stock.UpdateSmlIdField(this.data['id'], SmlId, values).then(function (data) {
            if (data) {
                _this.apply_move_data(data);
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al escribor en el movimiento:', error);
        });
    };
    MoveFormPage.prototype.ChangeQty = function (SmlId, qty) {
        this.audio.play('click');
        if (this.data['state'].value === 'done') {
            return;
        }
        this.QtyDirty = true;
        if (qty === 0) {
            if (SmlId['qty_done'] === 0) {
                SmlId['qty_done'] = SmlId['product_uom_qty'];
            }
            else {
                SmlId['qty_done'] = 0;
            }
        }
        // tslint:disable-next-line:one-line
        else {
            if (!(SmlId['qty_done'] < 1 && qty === -1)) {
                SmlId['qty_done'] += qty;
            }
        }
    };
    MoveFormPage.prototype.apply_move_data = function (data) {
        this.InitData();
        console.log(data);
        if (data['image'] === false) {
            data['base64'] = false;
            // data['image'] = this.placeholder;
        }
        else {
            data['base64'] = true;
        }
        this.data = data;
        console.log(this.data);
        for (var _i = 0, _a = data['move_line_ids']; _i < _a.length; _i++) {
            var sml = _a[_i];
            if (sml.lot_id.id) {
                this.LotNames.push(sml.lot_id.name);
            }
        }
        if (this.FirstLoad) {
            if (this.data['state'].value !== 'done') {
                this.ShowLots = this.data['tracking'].value === 'serial';
                this.ShowMoves = this.data['tracking'].value !== 'serial';
                this.FirstLoad = false;
            }
            else {
                this.ShowLots = false;
                this.ShowMoves = true;
                this.FirstLoad = false;
            }
        }
        // this.audio.play('click');
        if (data['message']) {
            this.presentAlert('Odoo', data['message']);
        }
    };
    MoveFormPage.prototype.GetMoveInfo = function (move, index) {
        var _this = this;
        if (index === void 0) { index = 0; }
        this.stock.GetMoveInfo(move, index).then(function (data) {
            _this.apply_move_data(data);
        })
            .catch(function (error) {
            _this.presentAlert('Error al recuperar el movimiento:', error);
        });
    };
    MoveFormPage.prototype.DoMoveValidate = function () {
        var _this = this;
        if (this.data['state'].value === 'done') {
            return;
        }
        this.stock.DoMoveValidate(this.data['picking_id'].id, this.data['id']).then(function (data) {
            if (data) {
                _this.apply_move_data(data);
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al validar el albarán:', error);
        });
    };
    MoveFormPage.prototype.action_confirm = function () {
        var _this = this;
        if (this.data['tracking'] === 'none') {
            this.stock.set_move_qty_done_from_apk(this.data['id'], this.data['quantity_done']).then(function (LinesData) {
                console.log(LinesData);
                _this.GetMoveInfo(_this.data['id'], +1);
            })
                .catch(function (error) {
                _this.presentAlert('Error al validar el albarán:', error);
            });
        }
        // else if (this.data['tracking'] != 'none' && this.new_lots){
        // this.update_lots();
        // }
    };
    MoveFormPage.prototype.button_validate = function (PickingId) {
        var _this = this;
        this.audio.play('click');
        this.presentLoading();
        this.stock.button_validate(Number(PickingId)).then(function (LinesData) {
            if (LinesData && LinesData['err'] === false) {
                console.log('Reloading');
                _this.loading.dismiss();
                _this.location.back();
            }
            else if (LinesData['err'] !== false) {
                _this.loading.dismiss();
                _this.presentAlert('Error al validar el albarán:', LinesData['err']);
            }
        })
            .catch(function (error) {
            _this.loading.dismiss();
            _this.presentAlert('Error al validar el albarán:', error);
        });
    };
    MoveFormPage.prototype.presentLoading = function () {
        return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"])(this, void 0, void 0, function () {
            var _a;
            return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"])(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this;
                        return [4 /*yield*/, this.loadingController.create({
                                message: 'Validando...',
                                translucent: true,
                                cssClass: 'custom-class custom-loading'
                            })];
                    case 1:
                        _a.loading = _b.sent();
                        return [4 /*yield*/, this.loading.present()];
                    case 2:
                        _b.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    MoveFormPage.prototype.update_lots = function () {
        var _this = this;
        this.stock.CreateMoveLots(this.data['id'], this.new_lots, this.data['active_location_id'].id).then(function (data) {
            _this.GetMoveInfo(_this.data['id']);
        })
            .catch(function (error) {
            _this.presentAlert('Error al validar el albarán:', error);
        });
    };
    MoveFormPage.prototype.done_status = function (field) {
        this.data['field_status_apk'] = this.stock.write_status(this.data['field_status_apk'], field, 'done');
    };
    MoveFormPage.prototype.CreateNewSmlId = function (SmId) {
        var _this = this;
        if (this.data['state'].value === 'done') {
            return;
        }
        this.stock.CreateNewSmlId(SmId).then(function (data) {
            if (data) {
                _this.reset_scanner();
                _this.apply_move_data(data);
                if (data['warning']) {
                    _this.presentAlert('Odoo', data['warning']);
                }
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al borrar el movieminto:', error);
        });
    };
    MoveFormPage.prototype.RemoveMoveLineId = function (SmlId) {
        var _this = this;
        if (this.data['state'].value === 'done') {
            return;
        }
        this.stock.RemoveMoveLineId(this.data['id'], SmlId).then(function (data) {
            if (data) {
                _this.reset_scanner();
                _this.apply_move_data(data);
                if (data['warning']) {
                    _this.presentAlert('Odoo', data['warning']);
                }
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al borrar el movieminto:', error);
        });
    };
    MoveFormPage.prototype.ProcessProductId = function () {
        var _this = this;
        if (this.data['state'].value === 'done') {
            return;
        }
        this.audio.play('click');
        var SmlIds = this.data['move_line_ids'].filter(function (move) { return (_this.data['active_location_id'].id === move[_this.data['default_location'].value].id); });
        if (SmlIds) {
            // Si hay un sml_id
            // entonces
            // Escribo el producto y l aubicación con ok. y ademas le sumo una a la cantidad
            var SmlId = SmlIds[0];
            SmlId['field_status_apk'] = this.stock.write_status(SmlId['field_status_apk'], 'product_id', 'done');
            SmlId['field_status_apk'] = this.stock.write_status(SmlId['field_status_apk'], this.data['default_location'], 'done');
            this.ChangeQty(SmlId, 1);
        }
    };
    MoveFormPage.prototype.ProcessLocation = function (barcode) {
        var _this = this;
        if (this.data['state'].value === 'done') {
            return;
        }
        var field = this.data['default_location'].value;
        // Miro si coincide con algún ucbicaión delos movimientos
        var confirm = this.LastReading === this.scanner_reading;
        var MovesToUpdate = this.GetMovesToChangeLoc(this.data['move_line_ids'], confirm);
        var SmlIds = [];
        for (var _i = 0, MovesToUpdate_1 = MovesToUpdate; _i < MovesToUpdate_1.length; _i++) {
            var move = MovesToUpdate_1[_i];
            SmlIds.push(move['id']);
        }
        var values = { move_id: this.data['id'],
            field: this.data['default_location'].value,
            value: this.data['active_location_id']['id'],
            sml_ids: SmlIds };
        this.stock.AssignLocationToMoves(this.data['id'], SmlIds, this.data['default_location'].value, this.data['active_location_id']['id'], barcode, confirm)
            .then(function (data) {
            if (data) {
                _this.reset_scanner();
                _this.apply_move_data(data);
                if (data['warning']) {
                    _this.presentAlert('Odoo', data['warning']);
                }
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al asignar las ubicaciones al los movimientos pendientes:', error);
        });
    };
    MoveFormPage.prototype.AssignLocationId = function (MoveId, LocationId, LocationField) {
        var _this = this;
        if (this.data['state'].value === 'done') {
            return;
        }
        this.stock.AssignLocationId(MoveId, LocationId, LocationField).then(function (data) {
            if (data) {
                _this.reset_scanner();
                _this.apply_move_data(data);
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al asignar las ubicaciones de origen del movimiento:', error);
        });
    };
    MoveFormPage.prototype.ProcessLocationId = function (LocationId) {
        if (LocationId === void 0) { LocationId = ''; }
        if (this.data['default_location'].value === 'location_id') {
            this.AssignLocationId(this.data['id'], this.data['default_location_id']['id'], 'location_id');
        }
        // Escribo en todos los que no tengan la ubicación como hecha la que pone, y además la marco como hecha
    };
    MoveFormPage.prototype.ProcessLocationDestId = function (LocationDestId) {
        if (LocationDestId === void 0) { LocationDestId = ''; }
        if (this.data['default_location'].value === 'location_dest_id') {
            this.AssignLocationId(this.data['id'], this.data['active_location_id'].id, 'location_dest_id');
            // Escribo en todos los que no tengan la ubicación como hecha la que pone, y además la marco como hecha
            // this.data.field_status_apk = this.stock.write_status(this.data.field_status_apk, 'location_dest_id', 'done')
        }
    };
    MoveFormPage.prototype.ActionAssign = function (MoveId) {
        var _this = this;
        if (this.data['state'].value === 'done') {
            return;
        }
        this.audio.play('click');
        this.stock.ActionAssign(MoveId).then(function (data) {
            if (data) {
                _this.reset_scanner();
                _this.apply_move_data(data);
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al quitar la reserva del movimiento:', error);
        });
    };
    MoveFormPage.prototype.CleanLots = function (MoveId) {
        var _this = this;
        if (this.data['state'].value === 'done') {
            return;
        }
        this.audio.play('click');
        this.stock.CleanLots(MoveId).then(function (data) {
            if (data) {
                _this.reset_scanner();
                _this.apply_move_data(data);
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al quitar los lotes del movimiento:', error);
        });
    };
    MoveFormPage.prototype.ActionUnReserve = function (MoveId) {
        var _this = this;
        if (this.data['state'].value === 'done') {
            return;
        }
        this.audio.play('click');
        this.stock.MoveUnReserve(MoveId).then(function (data) {
            if (data) {
                _this.reset_scanner();
                _this.apply_move_data(data);
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al quitar la reserva del movimiento:', error);
        });
    };
    MoveFormPage.prototype.ChangeLineLocationId = function (SmlId) {
        return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"])(this, void 0, void 0, function () {
            var alert;
            var _this = this;
            return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"])(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (this.data['state'].value === 'done') {
                            return [2 /*return*/];
                        }
                        if (this.data['state'].value === 'done') {
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, this.alertCtrl.create({
                                header: 'Ubicación',
                                subHeader: '',
                                inputs: [{ name: 'barcode',
                                        type: 'text',
                                        id: 'read_barcode' }],
                                buttons: [{
                                        text: 'Cancelar',
                                        role: 'cancel',
                                        cssClass: 'secondary',
                                        handler: function () {
                                        }
                                    },
                                    {
                                        text: 'Aplicar',
                                        handler: function (data) {
                                            var values = { new_location_barcode: data['barcode'] };
                                            _this.UpdateSmlIdField(SmlId, values);
                                        }
                                    }],
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
    MoveFormPage.prototype.ChangeLineLotId = function (MoveId, SmlId, OldLotName, NewLotId) {
        var _this = this;
        if (MoveId === void 0) { MoveId = false; }
        if (SmlId === void 0) { SmlId = false; }
        if (OldLotName === void 0) { OldLotName = false; }
        if (NewLotId === void 0) { NewLotId = false; }
        if (this.data['state'].value === 'done') {
            return;
        }
        this.audio.play('click');
        if (!MoveId) {
            MoveId = this.data['id'];
        }
        if (this.data['state'].value !== 'done') {
            this.stock.ChangeLineLotId(MoveId, SmlId, OldLotName, NewLotId).then(function (data) {
                if (data) {
                    _this.reset_scanner();
                    _this.apply_move_data(data);
                }
            })
                .catch(function (error) {
                _this.presentAlert('Error al actualizar el lote del movimeinto:', error);
            });
        }
        return;
    };
    MoveFormPage.prototype.BacthLot = function () {
        // Booleano que indica cuando lo que se va aleer es un lote:
        if (!this.ShowLots) {
            return false;
        }
        return true;
    };
    MoveFormPage.prototype.ProcessLotId = function () {
        return this.ProcessSerialId();
        if (this.data['state'].value === 'done') {
            return;
        }
        var LotName = this.scanner_reading;
        var SmlIds = this.data['move_line_ids'].filter(function (move) { return (move['lot_id'] && move['lot_id']['name'] === LotName); });
        if (SmlIds) {
            for (var _i = 0, SmlIds_1 = SmlIds; _i < SmlIds_1.length; _i++) {
                var SmlId = SmlIds_1[_i];
                SmlId['field_status_apk'] = this.stock.write_status(SmlId['field_status_apk'], 'lot_id', 'done');
                var values = { field_status_apk: SmlId['field_status_apk'] };
                this.UpdateSmlIdField(SmlId, values);
            }
        }
    };
    MoveFormPage.prototype.ProcessSerialId = function () {
        if (this.data['state'].value === 'done') {
            return;
        }
        var LotsToAdd = this.scanner_reading.split(',');
        var LotsToCheck = [];
        for (var _i = 0, LotsToAdd_1 = LotsToAdd; _i < LotsToAdd_1.length; _i++) {
            var lot = LotsToAdd_1[_i];
            if (this.LotNames.indexOf(lot) === -1) {
                this.LotNames.push(lot);
                this.ChangeLotNames = true;
            }
            else {
                LotsToCheck.push(lot);
            }
        }
        if (LotsToCheck.length > 0) {
            this.ActionApplyLotNames(LotsToCheck);
        }
    };
    MoveFormPage.prototype.SetWaitingQty = function (SmlId) {
        this.ActiveLine = SmlId;
        this.WaitingQty = true;
    };
    MoveFormPage.prototype.ActionApplyLotNames = function (LotNames) {
        var _this = this;
        if (this.data['state'].value === 'done') {
            return;
        }
        LotNames = LotNames || this.LotNames;
        // Saco la lista de lotes que no están los movimientos
        // Las lita de lotes siempre es la original más los que añado, por lo que tengo que quitar los de los movmientos
        if (this.LotNames.length > 0) {
            this.stock.CreateMoveLots(this.data['id'], LotNames, this.data['location_dest_id'].id).then(function (data) {
                if (data) {
                    _this.reset_scanner();
                    _this.apply_move_data(data);
                }
            })
                .catch(function (error) {
                _this.presentAlert('Error al añadir los lotes el albarán:', error);
            });
        }
        return;
        /* PRUEBO enviando todo y actualizando
    
        let LotsToCheck = []
        for (const move of this.data.move_line_ids) {
          const lot = move.lot_id;
          if (lot.id) {
            if (LotsToAdd.indexOf(lot.name) !== -1) {
              LotsToAdd.pop(lot.name);
            }
          }
        }
        if (LotsToAdd.length > 0) {
          this.stock.CreateMoveLots(this.data['id'], LotsToAdd).then((data)=>{
            this.apply_move_data(data);
          })
          .catch((error)=>{
            this.presentAlert('Error al añadir los lotes el albarán:', error);
          });
        }
        */
    };
    MoveFormPage.prototype.SearchOtherMoveByScanner = function () { };
    MoveFormPage.prototype.reset_scanner = function () {
        this.WaitingQty = false;
        this.ActiveLine = {};
        this.LastReading = this.scanner_reading;
        this.ScannerFooter.ScanReader.controls.scan.setValue('');
        // this.scanner.reset_scan();
        // this.ScanReader.controls.scan.setValue =''
    };
    MoveFormPage.prototype.process_reading = function () {
        // Primero buscon en el formulario si coincide con algo y despues decido que hacer
        // Caso 1. EAN 13
        // Busco
        this.audio.play('click');
        if (this.data['state'].value === 'done') {
            this.SearchOtherMoveByScanner();
        }
        else if (eval(this.data['barcode_re']).exec(this.scanner_reading) || /[\.]\d{3}[\.]/.exec(this.scanner_reading)) {
            // Leo UBICACION
            this.ProcessLocation(this.scanner_reading);
            // if (this.data.default_location.value === 'location_id') {this.ProcessLocationId(this.scanner_reading); }
            // else if (this.data.default_location.value === 'location_dest_id') {this.ProcessLocationDestId(this.scanner_reading);}
        }
        else if (this.WaitingQty && this.ActiveLine && this.ActiveLine['id']) {
            if (typeof this.scanner_reading) {
                this.ActiveLine['qty_done'] = this.scanner_reading;
                this.reset_scanner();
                return;
            }
            this.presentAlert('Error en los datos.', 'El valor introducido ' + this.scanner_reading + 'no es válido');
            return;
        }
        else if (this.data['tracking'].value === 'none' && (this.data['product_id']['default_code'] === this.scanner_reading || this.data['product_id'].barcode === this.scanner_reading)) {
            this.ProcessProductId();
        }
        else if (this.data['tracking'].value === 'serial') {
            this.ProcessSerialId();
        }
        else if (this.data['tracking'].value === 'lot') {
            this.ProcessLotId();
        }
        else {
            this.presentAlert('Aviso', 'No se ha encontrado nada para ' + this.scanner_reading);
        }
        this.reset_scanner();
        /*
        if (this.data['tracking'] == 'none' && Number(this.scanner_reading)) {
          this.data['quantity_done'] = Number(this.scanner_reading);
        } else if (this.data['tracking'] != 'none') {
          if(!this.new_lots){
            this.new_lots = new Array();
          }
          this.new_lots.push([this.scanner_reading, 1]); /* Editar más adelante, serial cantidad = 1, lot cantidad = a introducir */
        /* Provisional, cuando estén preparada la función para gestionar cantidades en lot_ids editar */
        /* if (this.data['tracking'] == 'serial') {
        if (this.data['tracking'] == 'serial' || this.data['tracking'] == 'lot') {
          this.data['quantity_done']++;
        }
      }  */
    };
    MoveFormPage.prototype.NavigateStockPicking = function (PickingId) {
        this.router.navigateByUrl('/stock-picking/' + PickingId);
    };
    MoveFormPage.ctorParameters = function () { return [
        { type: _services_scanner_service__WEBPACK_IMPORTED_MODULE_10__["ScannerService"] },
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_5__["OdooService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_6__["AudioService"] },
        { type: _services_stock_service__WEBPACK_IMPORTED_MODULE_7__["StockService"] },
        { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_3__["Storage"] },
        { type: _angular_common__WEBPACK_IMPORTED_MODULE_8__["Location"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["LoadingController"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["ActionSheetController"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])(_components_scanner_scanner_footer_scanner_footer_component__WEBPACK_IMPORTED_MODULE_9__["ScannerFooterComponent"]),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", _components_scanner_scanner_footer_scanner_footer_component__WEBPACK_IMPORTED_MODULE_9__["ScannerFooterComponent"])
    ], MoveFormPage.prototype, "ScannerFooter", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", String)
    ], MoveFormPage.prototype, "scanner_reading", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["HostListener"])('document:keydown', ['$event']),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Function),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [KeyboardEvent]),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:returntype", void 0)
    ], MoveFormPage.prototype, "handleKeyboardEvent", null);
    MoveFormPage = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-move-form',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./move-form.page.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/pages/move-form/move-form.page.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./move-form.page.scss */ "./src/app/pages/move-form/move-form.page.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_services_scanner_service__WEBPACK_IMPORTED_MODULE_10__["ScannerService"],
            _services_odoo_service__WEBPACK_IMPORTED_MODULE_5__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_6__["AudioService"],
            _services_stock_service__WEBPACK_IMPORTED_MODULE_7__["StockService"],
            _ionic_storage__WEBPACK_IMPORTED_MODULE_3__["Storage"],
            _angular_common__WEBPACK_IMPORTED_MODULE_8__["Location"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["LoadingController"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["ActionSheetController"]])
    ], MoveFormPage);
    return MoveFormPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-move-form-move-form-module.js.map
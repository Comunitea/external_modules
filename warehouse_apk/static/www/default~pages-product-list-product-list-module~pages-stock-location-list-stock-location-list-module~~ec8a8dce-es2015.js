(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~pages-product-list-product-list-module~pages-stock-location-list-stock-location-list-module~~ec8a8dce"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/components/scanner/scanner-footer/scanner-footer.component.html":
/*!***********************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/components/scanner/scanner-footer/scanner-footer.component.html ***!
  \***********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-footer>\n  <form [formGroup]=\"ScanReader\" class =\"alignBottom\" *ngIf=\"show_scan_form\">\n    <ion-item>\n      <ion-label item-start>Scan: </ion-label>\n      <ion-input #scan type=\"text\" formControlName=\"scan\" ></ion-input>\n    \n      <button ion-button icon-only item-end clear (click)=\"submitScan()\">\n        <ion-icon name=\"barcode\"></ion-icon>\n      </button>\n    </ion-item>   \n  </form>\n</ion-footer>"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/components/scanner/scanner-header/scanner-header.component.html":
/*!***********************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/components/scanner/scanner-header/scanner-header.component.html ***!
  \***********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-buttons end>\n  <!-- Commented voice function -->\n  <button ion-button icon-only item-end (click)=\"change_volume()\">\n    <ion-icon *ngIf=\"volume\" name=\"megaphone\"></ion-icon>\n    <ion-icon *ngIf=\"!volume\" name=\"volume-off\"></ion-icon>\n  </button>\n  <button ion-button icon-only item-end (click)=\"change_escuchando()\">\n    <ion-icon *ngIf=\"escuchando\" name=\"mic\"></ion-icon>\n    <ion-icon *ngIf=\"!escuchando\" name=\"mic-off\"></ion-icon>\n  </button>\n    \n    <button ion-button icon-only item-end (click)=\"change_hide_scan_form()\">\n    <ion-icon name=\"barcode\"></ion-icon>\n  </button>\n</ion-buttons>"

/***/ }),

/***/ "./src/app/components/scanner/scanner-footer/scanner-footer.component.scss":
/*!*********************************************************************************!*\
  !*** ./src/app/components/scanner/scanner-footer/scanner-footer.component.scss ***!
  \*********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "ion-footer button {\n  color: var(--ion-color-primary);\n  background-color: white;\n  font-size: 30px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9jb21wb25lbnRzL3NjYW5uZXIvc2Nhbm5lci1mb290ZXIvc2Nhbm5lci1mb290ZXIuY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL2NvbXBvbmVudHMvc2Nhbm5lci9zY2FubmVyLWZvb3Rlci9zY2FubmVyLWZvb3Rlci5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFDSTtFQUNJLCtCQUFBO0VBQ0EsdUJBQUE7RUFDQSxlQUFBO0FDQVIiLCJmaWxlIjoic3JjL2FwcC9jb21wb25lbnRzL3NjYW5uZXIvc2Nhbm5lci1mb290ZXIvc2Nhbm5lci1mb290ZXIuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJpb24tZm9vdGVyIHtcbiAgICBidXR0b24ge1xuICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXByaW1hcnkpO1xuICAgICAgICBiYWNrZ3JvdW5kLWNvbG9yOiB3aGl0ZTtcbiAgICAgICAgZm9udC1zaXplOiAzMHB4O1xuICAgIH1cbn0iLCJpb24tZm9vdGVyIGJ1dHRvbiB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG4gIGJhY2tncm91bmQtY29sb3I6IHdoaXRlO1xuICBmb250LXNpemU6IDMwcHg7XG59Il19 */"

/***/ }),

/***/ "./src/app/components/scanner/scanner-footer/scanner-footer.component.ts":
/*!*******************************************************************************!*\
  !*** ./src/app/components/scanner/scanner-footer/scanner-footer.component.ts ***!
  \*******************************************************************************/
/*! exports provided: ScannerFooterComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ScannerFooterComponent", function() { return ScannerFooterComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _services_scanner_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../services/scanner.service */ "./src/app/services/scanner.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../services/audio.service */ "./src/app/services/audio.service.ts");





let ScannerFooterComponent = class ScannerFooterComponent {
    constructor(scanner, formBuilder, audio) {
        this.scanner = scanner;
        this.formBuilder = formBuilder;
        this.audio = audio;
        /* ScanReader: FormGroup; */
        this.ScanReader = new _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormGroup"]({
            scan: new _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormControl"]()
        });
        this.scanner_reading_changed = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
        this.scanner.on();
        this.ScanReader = new _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormGroup"]({
            scan: new _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormControl"]()
        });
    }
    handleKeyboardEvent(event) {
        this.scanner.key_press(event);
        this.scanner.timeout.then((val) => {
            this.scan_read(val);
        });
    }
    ngOnInit() { }
    scan_read(val) {
        this.audio.play('barcode_ok');
        this.scanner_reading = val;
        this.scanner_reading_changed.emit(this.scanner_reading);
    }
    submitScan() {
        if (this.ScanReader) {
            this.audio.play('barcode_ok');
            this.scanner_reading = this.ScanReader.value['scan'];
            this.scanner_reading_changed.emit(this.scanner_reading);
        }
    }
};
ScannerFooterComponent.ctorParameters = () => [
    { type: _services_scanner_service__WEBPACK_IMPORTED_MODULE_3__["ScannerService"] },
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormBuilder"] },
    { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_4__["AudioService"] }
];
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["HostListener"])('document:keydown', ['$event']),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Function),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [KeyboardEvent]),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:returntype", void 0)
], ScannerFooterComponent.prototype, "handleKeyboardEvent", null);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Boolean)
], ScannerFooterComponent.prototype, "show_scan_form", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", String)
], ScannerFooterComponent.prototype, "scanner_reading", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Output"])(),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
], ScannerFooterComponent.prototype, "scanner_reading_changed", void 0);
ScannerFooterComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-scanner-footer',
        template: __webpack_require__(/*! raw-loader!./scanner-footer.component.html */ "./node_modules/raw-loader/index.js!./src/app/components/scanner/scanner-footer/scanner-footer.component.html"),
        styles: [__webpack_require__(/*! ./scanner-footer.component.scss */ "./src/app/components/scanner/scanner-footer/scanner-footer.component.scss")]
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_services_scanner_service__WEBPACK_IMPORTED_MODULE_3__["ScannerService"],
        _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormBuilder"],
        _services_audio_service__WEBPACK_IMPORTED_MODULE_4__["AudioService"]])
], ScannerFooterComponent);



/***/ }),

/***/ "./src/app/components/scanner/scanner-header/scanner-header.component.scss":
/*!*********************************************************************************!*\
  !*** ./src/app/components/scanner/scanner-header/scanner-header.component.scss ***!
  \*********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "ion-buttons button {\n  color: var(--ion-color-primary);\n  background-color: white;\n  font-size: 30px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9jb21wb25lbnRzL3NjYW5uZXIvc2Nhbm5lci1oZWFkZXIvc2Nhbm5lci1oZWFkZXIuY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL2NvbXBvbmVudHMvc2Nhbm5lci9zY2FubmVyLWhlYWRlci9zY2FubmVyLWhlYWRlci5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFDSTtFQUNJLCtCQUFBO0VBQ0EsdUJBQUE7RUFDQSxlQUFBO0FDQVIiLCJmaWxlIjoic3JjL2FwcC9jb21wb25lbnRzL3NjYW5uZXIvc2Nhbm5lci1oZWFkZXIvc2Nhbm5lci1oZWFkZXIuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJpb24tYnV0dG9ucyB7XG4gICAgYnV0dG9uIHtcbiAgICAgICAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1wcmltYXJ5KTtcbiAgICAgICAgYmFja2dyb3VuZC1jb2xvcjogd2hpdGU7XG4gICAgICAgIGZvbnQtc2l6ZTogMzBweDtcbiAgICB9XG59IiwiaW9uLWJ1dHRvbnMgYnV0dG9uIHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1wcmltYXJ5KTtcbiAgYmFja2dyb3VuZC1jb2xvcjogd2hpdGU7XG4gIGZvbnQtc2l6ZTogMzBweDtcbn0iXX0= */"

/***/ }),

/***/ "./src/app/components/scanner/scanner-header/scanner-header.component.ts":
/*!*******************************************************************************!*\
  !*** ./src/app/components/scanner/scanner-header/scanner-header.component.ts ***!
  \*******************************************************************************/
/*! exports provided: ScannerHeaderComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ScannerHeaderComponent", function() { return ScannerHeaderComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/fesm2015/ionic-storage.js");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");





let ScannerHeaderComponent = class ScannerHeaderComponent {
    constructor(storage, audio, alertCtrl) {
        this.storage = storage;
        this.audio = audio;
        this.alertCtrl = alertCtrl;
        this.scanner_options = { reader: true, microphone: false, sound: false };
        this.show_scan_form_changed = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
        this.show_escuchando = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
        this.show_volume = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
    }
    ngOnInit() {
        this.storage.get('SCANNER').then((val) => {
            if (val) {
                this.scanner_options = val;
                this.update_show_vals();
            }
            else {
                this.save_scanner_options();
            }
        })
            .catch((error) => {
            this.presentAlert('Error al acceder a las opciones del scanner:', error);
        });
    }
    presentAlert(titulo, texto) {
        return tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"](this, void 0, void 0, function* () {
            if (this.volume == true) {
                this.audio.play('error');
            }
            const alert = yield this.alertCtrl.create({
                header: titulo,
                subHeader: texto,
                buttons: ['Ok']
            });
            yield alert.present();
        });
    }
    change_volume() {
        this.volume = !this.volume;
        this.scanner_options['sound'] = this.volume;
        this.save_scanner_options();
        this.show_volume.emit(this.volume);
    }
    change_escuchando() {
        this.escuchando = !this.escuchando;
        this.scanner_options['microphone'] = this.escuchando;
        this.save_scanner_options();
        this.show_escuchando.emit(this.escuchando);
    }
    change_hide_scan_form() {
        this.show_scan_form = !this.show_scan_form;
        this.scanner_options['reader'] = this.show_scan_form;
        this.save_scanner_options();
        this.show_scan_form_changed.emit(this.show_scan_form);
    }
    save_scanner_options() {
        this.storage.set('SCANNER', this.scanner_options).then(() => {
        });
    }
    update_show_vals() {
        this.volume = this.scanner_options['sound'];
        this.escuchando = this.scanner_options['microphone'];
        this.show_scan_form = this.scanner_options['reader'];
    }
};
ScannerHeaderComponent.ctorParameters = () => [
    { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_2__["Storage"] },
    { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_3__["AudioService"] },
    { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"] }
];
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Boolean)
], ScannerHeaderComponent.prototype, "volume", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Boolean)
], ScannerHeaderComponent.prototype, "show_scan_form", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Boolean)
], ScannerHeaderComponent.prototype, "escuchando", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Output"])(),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
], ScannerHeaderComponent.prototype, "show_scan_form_changed", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Output"])(),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
], ScannerHeaderComponent.prototype, "show_escuchando", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Output"])(),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
], ScannerHeaderComponent.prototype, "show_volume", void 0);
ScannerHeaderComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-scanner-header',
        template: __webpack_require__(/*! raw-loader!./scanner-header.component.html */ "./node_modules/raw-loader/index.js!./src/app/components/scanner/scanner-header/scanner-header.component.html"),
        styles: [__webpack_require__(/*! ./scanner-header.component.scss */ "./src/app/components/scanner/scanner-header/scanner-header.component.scss")]
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_ionic_storage__WEBPACK_IMPORTED_MODULE_2__["Storage"],
        _services_audio_service__WEBPACK_IMPORTED_MODULE_3__["AudioService"],
        _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"]])
], ScannerHeaderComponent);



/***/ }),

/***/ "./src/app/services/scanner.service.ts":
/*!*********************************************!*\
  !*** ./src/app/services/scanner.service.ts ***!
  \*********************************************/
/*! exports provided: ScannerService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ScannerService", function() { return ScannerService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");


let ScannerService = class ScannerService {
    constructor() {
        this.code = "";
        this.timeStamp = 0;
        this.timeout = null;
        this.state = false;
        this.is_order = false;
        this.reset_scan();
    }
    handleKeyboardEvent(event) {
    }
    reset_scan() {
        this.code = "";
        this.is_order = false;
        this.timeStamp = 0;
        this.timeout = null;
        this.case = "regular";
        this.fragment = '';
    }
    on() {
        this.state = true;
        this.reset_scan();
        //this.odootools.presentToast(this.code)
    }
    off() {
        this.state = false;
        this.reset_scan();
        //this.odootools.presentToast(this.code)
    }
    key_press(event) {
        //console.log(event)
        //let st = ("Me llega " + event.which + '[' + event.keyCode + ' ]' + " y tengo " + this.code)
        //console.log(st)
        //this.odootools.presentToast(st)
        //this.odootools.presentToast(e)
        if (!this.state) { //ignore returns
        }
        else {
            //este 250 es el tiempo en resetear sin pulsaciones
            if (this.timeStamp + 400 < new Date().getTime()) {
                this.code = "";
                this.is_order = false;
            }
            this.timeStamp = new Date().getTime();
            //this.odootools.presentToast(st)
            switch (event.which) {
                case 37: {
                    this.case = "left";
                    break;
                }
                case 38: {
                    this.case = "up";
                    break;
                }
                case 39: {
                    this.case = "right";
                    break;
                }
                case 40: {
                    this.case = "down";
                    break;
                }
                default: {
                    this.case = "regular";
                    break;
                }
            }
            clearTimeout(this.timeout);
            var keyCode = event.keyCode || event.which;
            if (keyCode > 111 && keyCode < 121) {
                this.code = String.fromCharCode(keyCode);
                this.is_order = true;
            }
            else if (keyCode >= 48 && keyCode < 110 || keyCode == 190) {
                if (keyCode >= 96 && keyCode <= 105) {
                    // Numpad keys
                    keyCode -= 48;
                    this.fragment = String.fromCharCode(keyCode);
                }
                else if (keyCode == 190) {
                    this.fragment = ".";
                }
                else {
                    this.fragment = String.fromCharCode(keyCode);
                }
                this.is_order = false;
                this.code += this.fragment;
            }
            this.timeout = new Promise((resolve) => {
                setTimeout(() => {
                    if (this.case != "regular") {
                        let scan = this.case;
                        this.code = '';
                        //console.log('Envío ' + scan)
                        resolve(scan);
                    }
                    else if (this.code && (this.code.length >= 4 || this.is_order)) {
                        this.is_order = false;
                        //console.log('Devuelvo ' + this.code)
                        let scan = this.code.replace('-', '/');
                        this.code = '';
                        //console.log (scan + " ----> " + this.code)
                        resolve(scan);
                    }
                    ;
                }, 500);
                // este 500 es el tiempo que suma pulsaciones
            });
        }
        return this && this.timeout;
    }
};
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["HostListener"])('document:keydown', ['$event']),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Function),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [KeyboardEvent]),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:returntype", void 0)
], ScannerService.prototype, "handleKeyboardEvent", null);
ScannerService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [])
], ScannerService);



/***/ }),

/***/ "./src/app/shared/shared.module.ts":
/*!*****************************************!*\
  !*** ./src/app/shared/shared.module.ts ***!
  \*****************************************/
/*! exports provided: SharedModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SharedModule", function() { return SharedModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _components_scanner_scanner_header_scanner_header_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../components/scanner/scanner-header/scanner-header.component */ "./src/app/components/scanner/scanner-header/scanner-header.component.ts");
/* harmony import */ var _components_scanner_scanner_footer_scanner_footer_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../components/scanner/scanner-footer/scanner-footer.component */ "./src/app/components/scanner/scanner-footer/scanner-footer.component.ts");







let SharedModule = class SharedModule {
};
SharedModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_3__["IonicModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"]
        ],
        declarations: [
            _components_scanner_scanner_header_scanner_header_component__WEBPACK_IMPORTED_MODULE_5__["ScannerHeaderComponent"],
            _components_scanner_scanner_footer_scanner_footer_component__WEBPACK_IMPORTED_MODULE_6__["ScannerFooterComponent"]
        ],
        schemas: [_angular_core__WEBPACK_IMPORTED_MODULE_1__["CUSTOM_ELEMENTS_SCHEMA"]],
        exports: [
            _components_scanner_scanner_header_scanner_header_component__WEBPACK_IMPORTED_MODULE_5__["ScannerHeaderComponent"],
            _components_scanner_scanner_footer_scanner_footer_component__WEBPACK_IMPORTED_MODULE_6__["ScannerFooterComponent"]
        ]
    })
], SharedModule);



/***/ })

}]);
//# sourceMappingURL=default~pages-product-list-product-list-module~pages-stock-location-list-stock-location-list-module~~ec8a8dce-es2015.js.map
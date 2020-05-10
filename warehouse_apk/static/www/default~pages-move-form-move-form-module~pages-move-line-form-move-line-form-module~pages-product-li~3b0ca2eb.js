(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~pages-move-form-move-form-module~pages-move-line-form-move-line-form-module~pages-product-li~3b0ca2eb"],{

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/scanner/scanner-footer/scanner-footer.component.html":
/*!***********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/components/scanner/scanner-footer/scanner-footer.component.html ***!
  \***********************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-footer>\n  <form [formGroup]=\"ScanReader\" class =\"alignBottom\" *ngIf=\"scanner.active_scanner\">\n    <ion-item>\n      <ion-label item-start>Scan: </ion-label>\n      <ion-input #scan type=\"text\" formControlName=\"scan\" ></ion-input>\n    \n      <button ion-button icon-only item-end clear (click)=\"submitScan()\">\n        <ion-icon name=\"barcode\"></ion-icon>\n      </button>\n    </ion-item>   \n  </form>\n</ion-footer>");

/***/ }),

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/scanner/scanner-header/scanner-header.component.html":
/*!***********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/components/scanner/scanner-header/scanner-header.component.html ***!
  \***********************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ion-buttons end>\n  <!-- Commented voice function -->\n  <button ion-button icon-only item-end (click)=\"change_volume()\">\n    <ion-icon *ngIf=\"audio.active_audio\" name=\"megaphone\"></ion-icon>\n    <ion-icon *ngIf=\"!audio.active_audio\" name=\"volume-off\"></ion-icon>\n  </button>\n  <button *ngIf=\"voice.available\" ion-button icon-only item-end (click)=\"change_escuchando()\">\n    <ion-icon *ngIf=\"voice.active_voice\" name=\"mic\"></ion-icon>\n    <ion-icon *ngIf=\"!voice.active_voice\" name=\"mic-off\"></ion-icon>\n  </button>\n\n  <button *ngIf=\"!voice.available\" disabled=\"disabled\" class=\"disabled\" ion-button icon-only item-end>\n    <ion-icon name=\"mic\"></ion-icon>\n  </button>\n    \n  <button *ngIf=\"!disabled_reader\" ion-button icon-only item-end (click)=\"change_hide_scan_form()\">\n    <ion-icon name=\"barcode\"></ion-icon>\n  </button>\n  <button *ngIf=\"disabled_reader\" disabled=\"disabled\" class=\"disabled\" ion-button icon-only item-end>\n    <ion-icon name=\"barcode\"></ion-icon>\n  </button>\n</ion-buttons>");

/***/ }),

/***/ "./src/app/components/scanner/scanner-footer/scanner-footer.component.scss":
/*!*********************************************************************************!*\
  !*** ./src/app/components/scanner/scanner-footer/scanner-footer.component.scss ***!
  \*********************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("ion-footer button {\n  color: var(--ion-color-primary);\n  background-color: white;\n  font-size: 30px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL2NvbXBvbmVudHMvc2Nhbm5lci9zY2FubmVyLWZvb3Rlci9zY2FubmVyLWZvb3Rlci5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvY29tcG9uZW50cy9zY2FubmVyL3NjYW5uZXItZm9vdGVyL3NjYW5uZXItZm9vdGVyLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUNJO0VBQ0ksK0JBQUE7RUFDQSx1QkFBQTtFQUNBLGVBQUE7QUNBUiIsImZpbGUiOiJzcmMvYXBwL2NvbXBvbmVudHMvc2Nhbm5lci9zY2FubmVyLWZvb3Rlci9zY2FubmVyLWZvb3Rlci5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbImlvbi1mb290ZXIge1xuICAgIGJ1dHRvbiB7XG4gICAgICAgIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItcHJpbWFyeSk7XG4gICAgICAgIGJhY2tncm91bmQtY29sb3I6IHdoaXRlO1xuICAgICAgICBmb250LXNpemU6IDMwcHg7XG4gICAgfVxufSIsImlvbi1mb290ZXIgYnV0dG9uIHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1wcmltYXJ5KTtcbiAgYmFja2dyb3VuZC1jb2xvcjogd2hpdGU7XG4gIGZvbnQtc2l6ZTogMzBweDtcbn0iXX0= */");

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _services_scanner_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../services/scanner.service */ "./src/app/services/scanner.service.ts");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../services/audio.service */ "./src/app/services/audio.service.ts");





var ScannerFooterComponent = /** @class */ (function () {
    function ScannerFooterComponent(scanner, formBuilder, audio) {
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
    ScannerFooterComponent.prototype.handleKeyboardEvent = function (event) {
        var _this = this;
        this.scanner.key_press(event);
        this.scanner.timeout.then(function (val) {
            _this.scan_read(val);
        });
    };
    ScannerFooterComponent.prototype.ngOnInit = function () { };
    ScannerFooterComponent.prototype.scan_read = function (val) {
        this.audio.play('barcode_ok');
        this.scanner_reading = val;
        this.scanner_reading_changed.emit(this.scanner_reading);
    };
    ScannerFooterComponent.prototype.submitScan = function () {
        if (this.ScanReader) {
            this.audio.play('barcode_ok');
            this.scanner_reading = this.ScanReader.value['scan'];
            this.scanner_reading_changed.emit(this.scanner_reading);
        }
    };
    ScannerFooterComponent.ctorParameters = function () { return [
        { type: _services_scanner_service__WEBPACK_IMPORTED_MODULE_3__["ScannerService"] },
        { type: _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormBuilder"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_4__["AudioService"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["HostListener"])('document:keydown', ['$event']),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Function),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [KeyboardEvent]),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:returntype", void 0)
    ], ScannerFooterComponent.prototype, "handleKeyboardEvent", null);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", String)
    ], ScannerFooterComponent.prototype, "scanner_reading", void 0);
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Output"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)
    ], ScannerFooterComponent.prototype, "scanner_reading_changed", void 0);
    ScannerFooterComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-scanner-footer',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./scanner-footer.component.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/scanner/scanner-footer/scanner-footer.component.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./scanner-footer.component.scss */ "./src/app/components/scanner/scanner-footer/scanner-footer.component.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_services_scanner_service__WEBPACK_IMPORTED_MODULE_3__["ScannerService"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormBuilder"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_4__["AudioService"]])
    ], ScannerFooterComponent);
    return ScannerFooterComponent;
}());



/***/ }),

/***/ "./src/app/components/scanner/scanner-header/scanner-header.component.scss":
/*!*********************************************************************************!*\
  !*** ./src/app/components/scanner/scanner-header/scanner-header.component.scss ***!
  \*********************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("ion-buttons button {\n  color: var(--ion-color-primary);\n  background-color: white;\n  font-size: 30px;\n}\nion-buttons button.disabled {\n  color: var(--ion-color-medium-tint);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9tYW5hZ2VyX2Fwa18xMS9zcmMvYXBwL2NvbXBvbmVudHMvc2Nhbm5lci9zY2FubmVyLWhlYWRlci9zY2FubmVyLWhlYWRlci5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvY29tcG9uZW50cy9zY2FubmVyL3NjYW5uZXItaGVhZGVyL3NjYW5uZXItaGVhZGVyLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUNJO0VBQ0ksK0JBQUE7RUFDQSx1QkFBQTtFQUNBLGVBQUE7QUNBUjtBREVJO0VBQ0ksbUNBQUE7QUNBUiIsImZpbGUiOiJzcmMvYXBwL2NvbXBvbmVudHMvc2Nhbm5lci9zY2FubmVyLWhlYWRlci9zY2FubmVyLWhlYWRlci5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbImlvbi1idXR0b25zIHtcbiAgICBidXR0b24ge1xuICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLXByaW1hcnkpO1xuICAgICAgICBiYWNrZ3JvdW5kLWNvbG9yOiB3aGl0ZTtcbiAgICAgICAgZm9udC1zaXplOiAzMHB4O1xuICAgIH1cbiAgICBidXR0b24uZGlzYWJsZWQge1xuICAgICAgICBjb2xvcjogdmFyKC0taW9uLWNvbG9yLW1lZGl1bS10aW50KTtcbiAgICB9XG59IiwiaW9uLWJ1dHRvbnMgYnV0dG9uIHtcbiAgY29sb3I6IHZhcigtLWlvbi1jb2xvci1wcmltYXJ5KTtcbiAgYmFja2dyb3VuZC1jb2xvcjogd2hpdGU7XG4gIGZvbnQtc2l6ZTogMzBweDtcbn1cbmlvbi1idXR0b25zIGJ1dHRvbi5kaXNhYmxlZCB7XG4gIGNvbG9yOiB2YXIoLS1pb24tY29sb3ItbWVkaXVtLXRpbnQpO1xufSJdfQ== */");

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/__ivy_ngcc__/fesm5/ionic-storage.js");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../services/audio.service */ "./src/app/services/audio.service.ts");
/* harmony import */ var _services_voice_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../services/voice.service */ "./src/app/services/voice.service.ts");
/* harmony import */ var _services_scanner_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../services/scanner.service */ "./src/app/services/scanner.service.ts");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");







var ScannerHeaderComponent = /** @class */ (function () {
    function ScannerHeaderComponent(storage, audio, voice, alertCtrl, scanner) {
        this.storage = storage;
        this.audio = audio;
        this.voice = voice;
        this.alertCtrl = alertCtrl;
        this.scanner = scanner;
        this.scanner_options = { reader: true, microphone: false, sound: false };
    }
    ScannerHeaderComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.storage.get('SCANNER').then(function (val) {
            if (val) {
                _this.scanner_options = val;
                _this.update_show_vals();
            }
            else {
                _this.save_scanner_options();
            }
            if (_this.voice.available == null) {
                _this.voice.isAvailable();
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al acceder a las opciones del scanner:', error);
        });
        if (this.voice.available) {
            this.check_escuchando();
        }
    };
    ScannerHeaderComponent.prototype.presentAlert = function (titulo, texto) {
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
    ScannerHeaderComponent.prototype.change_volume = function () {
        this.audio.active_audio = !this.audio.active_audio;
        this.scanner_options['sound'] = this.audio.active_audio;
        this.save_scanner_options();
    };
    ScannerHeaderComponent.prototype.change_escuchando = function () {
        this.voice.active_voice = !this.voice.active_voice;
        this.scanner_options['microphone'] = this.voice.active_voice;
        this.save_scanner_options();
        this.check_escuchando();
    };
    ScannerHeaderComponent.prototype.check_escuchando = function () {
        if (this.voice.active_voice) {
            this.voice.startListening();
        }
        else {
            this.voice.stopListening();
        }
    };
    ScannerHeaderComponent.prototype.change_hide_scan_form = function () {
        this.scanner.active_scanner = !this.scanner.active_scanner;
        this.scanner_options['reader'] = this.scanner.active_scanner;
        this.save_scanner_options();
    };
    ScannerHeaderComponent.prototype.save_scanner_options = function () {
        this.storage.set('SCANNER', this.scanner_options).then(function () {
        });
    };
    ScannerHeaderComponent.prototype.update_show_vals = function () {
        this.audio.active_audio = this.scanner_options['sound'];
        this.voice.active_voice = this.scanner_options['microphone'];
        this.scanner.active_scanner = this.scanner_options['reader'];
    };
    ScannerHeaderComponent.ctorParameters = function () { return [
        { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_2__["Storage"] },
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_3__["AudioService"] },
        { type: _services_voice_service__WEBPACK_IMPORTED_MODULE_4__["VoiceService"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_6__["AlertController"] },
        { type: _services_scanner_service__WEBPACK_IMPORTED_MODULE_5__["ScannerService"] }
    ]; };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Boolean)
    ], ScannerHeaderComponent.prototype, "disabled_reader", void 0);
    ScannerHeaderComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-scanner-header',
            template: Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! raw-loader!./scanner-header.component.html */ "./node_modules/raw-loader/dist/cjs.js!./src/app/components/scanner/scanner-header/scanner-header.component.html")).default,
            styles: [Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__importDefault"])(__webpack_require__(/*! ./scanner-header.component.scss */ "./src/app/components/scanner/scanner-header/scanner-header.component.scss")).default]
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_ionic_storage__WEBPACK_IMPORTED_MODULE_2__["Storage"],
            _services_audio_service__WEBPACK_IMPORTED_MODULE_3__["AudioService"],
            _services_voice_service__WEBPACK_IMPORTED_MODULE_4__["VoiceService"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_6__["AlertController"],
            _services_scanner_service__WEBPACK_IMPORTED_MODULE_5__["ScannerService"]])
    ], ScannerHeaderComponent);
    return ScannerHeaderComponent;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");


var ScannerService = /** @class */ (function () {
    function ScannerService() {
        this.code = "";
        this.timeStamp = 0;
        this.timeout = null;
        this.state = false;
        this.is_order = false;
        this.reset_scan();
    }
    ScannerService.prototype.handleKeyboardEvent = function (event) {
    };
    ScannerService.prototype.reset_scan = function () {
        this.code = "";
        this.is_order = false;
        this.timeStamp = 0;
        this.timeout = null;
        this.case = "regular";
        this.fragment = '';
    };
    ScannerService.prototype.on = function () {
        this.state = true;
        this.reset_scan();
        //this.odootools.presentToast(this.code)
    };
    ScannerService.prototype.off = function () {
        this.state = false;
        this.reset_scan();
        //this.odootools.presentToast(this.code)
    };
    ScannerService.prototype.key_press = function (event) {
        //console.log(event)
        //let st = ("Me llega " + event.which + '[' + event.keyCode + ' ]' + " y tengo " + this.code)
        //console.log(st)
        //this.odootools.presentToast(st)
        var _this = this;
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
            this.timeout = new Promise(function (resolve) {
                setTimeout(function () {
                    if (_this.case != "regular") {
                        var scan = _this.case;
                        _this.code = '';
                        //console.log('Envío ' + scan)
                        resolve(scan);
                    }
                    else if (_this.code && (_this.code.length >= 4 || _this.is_order)) {
                        _this.is_order = false;
                        //console.log('Devuelvo ' + this.code)
                        var scan = _this.code.replace('-', '/');
                        _this.code = '';
                        //console.log (scan + " ----> " + this.code)
                        resolve(scan);
                    }
                    ;
                }, 500);
                // este 500 es el tiempo que suma pulsaciones
            });
        }
        return this && this.timeout;
    };
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["HostListener"])('document:keydown', ['$event']),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Function),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [KeyboardEvent]),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:returntype", void 0)
    ], ScannerService.prototype, "handleKeyboardEvent", null);
    ScannerService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [])
    ], ScannerService);
    return ScannerService;
}());



/***/ }),

/***/ "./src/app/services/voice.service.ts":
/*!*******************************************!*\
  !*** ./src/app/services/voice.service.ts ***!
  \*******************************************/
/*! exports provided: VoiceService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VoiceService", function() { return VoiceService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _ionic_native_speech_recognition_ngx__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @ionic-native/speech-recognition/ngx */ "./node_modules/@ionic-native/speech-recognition/__ivy_ngcc__/ngx/index.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");




var VoiceService = /** @class */ (function () {
    function VoiceService(voice) {
        this.voice = voice;
        this.voice_command_refresh = new rxjs__WEBPACK_IMPORTED_MODULE_3__["Subject"]();
        this.voice_command_refresh$ = this.voice_command_refresh.asObservable();
    }
    VoiceService.prototype.isAvailable = function () {
        var _this = this;
        this.voice.isRecognitionAvailable().then(function (available) {
            _this.available = available;
            console.log(available);
        }).catch(function (error) {
            _this.available = false;
            console.log("Voz no disponible: " + error);
        });
    };
    VoiceService.prototype.publishVoiceRefresh = function () {
        this.voice_command_refresh.next();
    };
    VoiceService.prototype.getSupportedLanguages = function () {
        // Get the list of supported languages
        this.voice
            .getSupportedLanguages()
            .then(function (languages) { return console.log(languages); }, function (error) { return console.log(error); });
    };
    VoiceService.prototype.stopListening = function () {
        this.voice.stopListening();
    };
    VoiceService.prototype.getPermission = function () {
        var _this = this;
        this.voice.hasPermission()
            .then(function (hasPermission) {
            console.log(hasPermission);
            if (!hasPermission) {
                _this.voice.requestPermission();
            }
        })
            .catch(function (error) {
            console.log("Sin permisos.");
            _this.voice.requestPermission();
        });
    };
    VoiceService.prototype.startListening = function () {
        var _this = this;
        this.voice_command = [];
        this.getPermission();
        this.getSupportedLanguages();
        console.log("Escucha");
        var options = {
            language: 'es-ES',
            matches: 1000,
            prompt: "Te escucho",
            showPopup: true,
            showPartial: false
        };
        this.voice.startListening(options).subscribe((function (matches) {
            _this.voice_command = matches;
            _this.publishVoiceRefresh();
            _this.voice.stopListening().then(function () {
                _this.active_voice = false;
                console.log("Dejo de escuchar");
            });
        }), function (onerror) {
            _this.active_voice = false;
            _this.voice.stopListening();
            console.log('error:', onerror);
        });
    };
    VoiceService.ctorParameters = function () { return [
        { type: _ionic_native_speech_recognition_ngx__WEBPACK_IMPORTED_MODULE_2__["SpeechRecognition"] }
    ]; };
    VoiceService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        }),
        Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_ionic_native_speech_recognition_ngx__WEBPACK_IMPORTED_MODULE_2__["SpeechRecognition"]])
    ], VoiceService);
    return VoiceService;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/__ivy_ngcc__/fesm5/ionic-angular.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _components_scanner_scanner_header_scanner_header_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../components/scanner/scanner-header/scanner-header.component */ "./src/app/components/scanner/scanner-header/scanner-header.component.ts");
/* harmony import */ var _components_scanner_scanner_footer_scanner_footer_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../components/scanner/scanner-footer/scanner-footer.component */ "./src/app/components/scanner/scanner-footer/scanner-footer.component.ts");







var SharedModule = /** @class */ (function () {
    function SharedModule() {
    }
    SharedModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
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
    return SharedModule;
}());



/***/ })

}]);
//# sourceMappingURL=default~pages-move-form-move-form-module~pages-move-line-form-move-line-form-module~pages-product-li~3b0ca2eb.js.map
(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pages-login-login-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/pages/login/login.page.html":
/*!***********************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/pages/login/login.page.html ***!
  \***********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ion-header>\n  <ion-toolbar>\n    <ion-buttons slot=\"start\">\n      <ion-menu-button></ion-menu-button>\n    </ion-buttons>\n\n    <ion-title>Iniciar Sesión</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <div class=\"login-logo\">\n    <img src=\"assets/imgs/logo.png\" alt=\"Company logo\">\n  </div>\n\n  <form #loginForm=\"ngForm\" novalidate>\n    <ion-list>\n      <ion-item>\n        <ion-label position=\"stacked\" color=\"primary\">Usuario</ion-label>\n        <ion-input [(ngModel)]=\"CONEXION.username\" name=\"username\" type=\"text\" #username=\"ngModel\" spellcheck=\"false\" autocapitalize=\"off\"\n          required>\n        </ion-input>\n      </ion-item>\n\n      <ion-text color=\"danger\">\n        <p [hidden]=\"username.valid || submitted == false\" class=\"ion-padding-start\">\n          Usuario es un campo obligatorio.\n        </p>\n      </ion-text>\n\n      <ion-item>\n        <ion-label position=\"stacked\" color=\"primary\">Contraseña</ion-label>\n        <ion-input [(ngModel)]=\"CONEXION.password\" name=\"password\" type=\"password\" #password=\"ngModel\" required>\n        </ion-input>\n      </ion-item>\n\n      <ion-text color=\"danger\">\n        <p [hidden]=\"password.valid || submitted == false\" class=\"ion-padding-start\">\n          Contraseña es un campo obligatorio.\n        </p>\n      </ion-text>\n      \n\n      <ion-item>\n          <ion-label color=\"dark\">Servidor</ion-label>\n          <ion-toggle [(ngModel)]=\"login_server\" [ngModelOptions] = {standalone:true} ></ion-toggle>\n      </ion-item>\n    \n    </ion-list>\n\n    <ion-list *ngIf=\"!cargar && login_server\">\n\n      <ion-item>\n        <ion-label position=\"stacked\" color=\"primary\">URL</ion-label>\n        <ion-input [(ngModel)]=\"CONEXION.url\" #url=\"ngModel\" name=\"url\" placeholder=\"Ingresa url\" required>\n        </ion-input>\n      </ion-item>\n\n      <ion-text color=\"danger\">\n        <p [hidden]=\"url.valid || submitted == false\" class=\"ion-padding-start\">\n          URL es un campo obligatorio.\n        </p>\n      </ion-text>\n\n      <ion-item>\n        <ion-label position=\"stacked\" color=\"primary\">Port</ion-label>\n        <ion-input [(ngModel)]=\"CONEXION.port\" #port=\"ngModel\" name=\"port\" placeholder=\"Ingresa puerto\" required>\n        </ion-input>\n      </ion-item>\n\n      <ion-text color=\"danger\">\n        <p [hidden]=\"port.valid || submitted == false\" class=\"ion-padding-start\">\n          Puerto es un campo obligatorio.\n        </p>\n      </ion-text>\n\n      <ion-item>\n          <ion-label position=\"stacked\" color=\"primary\">Base de datos</ion-label>\n          <ion-input [(ngModel)]=\"CONEXION.db\" #db=\"ngModel\" name=\"db\" placeholder=\"Ingresa base de datos\" required>\n          </ion-input>\n        </ion-item>\n  \n        <ion-text color=\"danger\">\n          <p [hidden]=\"db.valid || submitted == false\" class=\"ion-padding-start\">\n            Base de datos es un campo obligatorio.\n          </p>\n        </ion-text>\n\n    </ion-list>\n\n    <ion-row>\n      <ion-col>\n        <ion-button (click)=\"onLogin(loginForm)\" type=\"submit\" expand=\"block\">Login</ion-button>\n      </ion-col>\n    </ion-row>\n  </form>\n\n</ion-content>"

/***/ }),

/***/ "./src/app/pages/login/login.module.ts":
/*!*********************************************!*\
  !*** ./src/app/pages/login/login.module.ts ***!
  \*********************************************/
/*! exports provided: LoginPageModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LoginPageModule", function() { return LoginPageModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _login_page__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./login.page */ "./src/app/pages/login/login.page.ts");







var routes = [
    {
        path: '',
        component: _login_page__WEBPACK_IMPORTED_MODULE_6__["LoginPage"]
    }
];
var LoginPageModule = /** @class */ (function () {
    function LoginPageModule() {
    }
    LoginPageModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _ionic_angular__WEBPACK_IMPORTED_MODULE_5__["IonicModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(routes)
            ],
            declarations: [_login_page__WEBPACK_IMPORTED_MODULE_6__["LoginPage"]]
        })
    ], LoginPageModule);
    return LoginPageModule;
}());



/***/ }),

/***/ "./src/app/pages/login/login.page.scss":
/*!*********************************************!*\
  !*** ./src/app/pages/login/login.page.scss ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".login-logo {\n  padding: 20px 0;\n  min-height: 200px;\n  text-align: center;\n}\n\n.login-logo img {\n  max-width: 150px;\n}\n\n.list {\n  margin-bottom: 0;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2tpa28vaW9uaWM0L3dhcmVob3VzZV9hcGsvc3JjL2FwcC9wYWdlcy9sb2dpbi9sb2dpbi5wYWdlLnNjc3MiLCJzcmMvYXBwL3BhZ2VzL2xvZ2luL2xvZ2luLnBhZ2Uuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNJLGVBQUE7RUFDQSxpQkFBQTtFQUNBLGtCQUFBO0FDQ0o7O0FERUU7RUFDRSxnQkFBQTtBQ0NKOztBREVFO0VBQ0UsZ0JBQUE7QUNDSiIsImZpbGUiOiJzcmMvYXBwL3BhZ2VzL2xvZ2luL2xvZ2luLnBhZ2Uuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi5sb2dpbi1sb2dvIHtcbiAgICBwYWRkaW5nOiAyMHB4IDA7XG4gICAgbWluLWhlaWdodDogMjAwcHg7XG4gICAgdGV4dC1hbGlnbjogY2VudGVyO1xuICB9XG4gIFxuICAubG9naW4tbG9nbyBpbWcge1xuICAgIG1heC13aWR0aDogMTUwcHg7XG4gIH1cbiAgXG4gIC5saXN0IHtcbiAgICBtYXJnaW4tYm90dG9tOiAwO1xuICB9XG4gICIsIi5sb2dpbi1sb2dvIHtcbiAgcGFkZGluZzogMjBweCAwO1xuICBtaW4taGVpZ2h0OiAyMDBweDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xufVxuXG4ubG9naW4tbG9nbyBpbWcge1xuICBtYXgtd2lkdGg6IDE1MHB4O1xufVxuXG4ubGlzdCB7XG4gIG1hcmdpbi1ib3R0b206IDA7XG59Il19 */"

/***/ }),

/***/ "./src/app/pages/login/login.page.ts":
/*!*******************************************!*\
  !*** ./src/app/pages/login/login.page.ts ***!
  \*******************************************/
/*! exports provided: LoginPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LoginPage", function() { return LoginPage; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _services_odoo_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../services/odoo.service */ "./src/app/services/odoo.service.ts");
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ionic/angular */ "./node_modules/@ionic/angular/dist/fesm5.js");
/* harmony import */ var _ionic_storage__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/storage */ "./node_modules/@ionic/storage/fesm5/ionic-storage.js");
/* harmony import */ var _services_audio_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/audio.service */ "./src/app/services/audio.service.ts");







var LoginPage = /** @class */ (function () {
    function LoginPage(audio, odoo, router, alertCtrl, storage, route) {
        this.audio = audio;
        this.odoo = odoo;
        this.router = router;
        this.alertCtrl = alertCtrl;
        this.storage = storage;
        this.route = route;
        this.CONEXION = { username: '', password: '', url: 'http://localhost', port: 8069, db: '', uid: 0, context: {}, user: {}, logged_in: false };
        this.CONEXION_local = { username: '', password: '', url: '', port: null, db: '', uid: 0, context: {}, user: {}, logged_in: false };
        if (this.route.snapshot.paramMap.get('login')) {
            this.CONEXION.username = this.route.snapshot.paramMap.get('login');
        }
        ;
        this.check_storage_conexion(this.route.snapshot.paramMap.get('borrar'));
        if (this.route.snapshot.paramMap.get('borrar')) {
            this.cargar = false;
        }
        else {
            // Autologin al cargar app
            this.cargar = false;
            this.conectarApp(false);
        }
    }
    LoginPage.prototype.check_storage_conexion = function (borrar) {
        var _this = this;
        // Fijamos siempre a false el parámetro borrar para no tener que teclear usuario y contraseña siempre
        borrar = false;
        if (borrar) {
            this.CONEXION = this.CONEXION_local;
        }
        else {
            this.storage.get('CONEXION').then(function (val) {
                if (val && val['username']) {
                    _this.CONEXION = val;
                }
                else {
                    _this.CONEXION = _this.CONEXION_local;
                    _this.storage.set('CONEXION', _this.CONEXION).then(function () {
                    });
                }
            });
        }
    };
    LoginPage.prototype.conectarApp = function (verificar) {
        var _this = this;
        this.cargar = true;
        if (verificar) {
            this.storage.set('CONEXION', this.CONEXION).then(function () {
                _this.log_in();
            });
        }
        else {
            this.storage.get('CONEXION').then(function (val) {
                var con;
                if (val == null) { //no existe datos         
                    _this.cargar = false;
                    con = _this.CONEXION;
                    if (con.username.length < 3 || con.password.length < 3) {
                        if (verificar) {
                            _this.presentAlert('Alerta!', 'Por favor ingrese usuario y contraseña');
                        }
                        return;
                    }
                }
                else {
                    //si los trae directamente ya fueron verificados
                    con = val;
                    if (con.username.length < 3 || con.password.length < 3) {
                        _this.cargar = false;
                        return;
                    }
                }
                if (con) {
                    _this.storage.set('CONEXION', con).then(function () {
                        _this.log_in();
                        _this.cargar = false;
                    });
                }
            });
        }
    };
    LoginPage.prototype.log_in = function () {
        var _this = this;
        this.odoo.login(this.CONEXION.username, this.CONEXION.password).then(function (data) {
            _this.router.navigateByUrl('/stock-picking-type-list');
        }).catch(function (error) {
            _this.presentAlert('Error al hacer login:', error);
        });
    };
    LoginPage.prototype.ngOnInit = function () {
        var _this = this;
        this.odoo.isLoggedIn().then(function (data) {
            if (data == true) {
                _this.router.navigateByUrl('/stock-picking-type-list');
            }
        })
            .catch(function (error) {
            _this.presentAlert('Error al hacer login:', error);
        });
    };
    LoginPage.prototype.onLogin = function (form) {
        var _this = this;
        this.submitted = true;
        if (form.valid) {
            this.CONEXION = {
                username: form.form.value.username,
                password: form.form.value.password,
                port: form.form.value.port || this.CONEXION.port,
                url: form.form.value.url || this.CONEXION.url,
                db: form.form.value.db || this.CONEXION.db,
                uid: 0,
                context: {},
                user: {},
                logged_in: false
            };
            this.storage.set('CONEXION', this.CONEXION).then(function () {
                _this.log_in();
            });
        }
    };
    LoginPage.prototype.presentAlert = function (titulo, texto) {
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
    LoginPage.ctorParameters = function () { return [
        { type: _services_audio_service__WEBPACK_IMPORTED_MODULE_6__["AudioService"] },
        { type: _services_odoo_service__WEBPACK_IMPORTED_MODULE_3__["OdooService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"] },
        { type: _ionic_storage__WEBPACK_IMPORTED_MODULE_5__["Storage"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] }
    ]; };
    LoginPage = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-login',
            template: __webpack_require__(/*! raw-loader!./login.page.html */ "./node_modules/raw-loader/index.js!./src/app/pages/login/login.page.html"),
            styles: [__webpack_require__(/*! ./login.page.scss */ "./src/app/pages/login/login.page.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_services_audio_service__WEBPACK_IMPORTED_MODULE_6__["AudioService"],
            _services_odoo_service__WEBPACK_IMPORTED_MODULE_3__["OdooService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"],
            _ionic_angular__WEBPACK_IMPORTED_MODULE_4__["AlertController"],
            _ionic_storage__WEBPACK_IMPORTED_MODULE_5__["Storage"],
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"]])
    ], LoginPage);
    return LoginPage;
}());



/***/ })

}]);
//# sourceMappingURL=pages-login-login-module-es5.js.map
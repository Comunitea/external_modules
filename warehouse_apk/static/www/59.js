(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[59],{

/***/ "./node_modules/@ionic/core/dist/esm-es5/ion-segment_2-ios.entry.js":
/*!**************************************************************************!*\
  !*** ./node_modules/@ionic/core/dist/esm-es5/ion-segment_2-ios.entry.js ***!
  \**************************************************************************/
/*! exports provided: ion_segment, ion_segment_button */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ion_segment", function() { return Segment; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ion_segment_button", function() { return SegmentButton; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./core-80bde1aa.js */ "./node_modules/@ionic/core/dist/esm-es5/core-80bde1aa.js");
/* harmony import */ var _config_3c7f3790_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./config-3c7f3790.js */ "./node_modules/@ionic/core/dist/esm-es5/config-3c7f3790.js");
/* harmony import */ var _helpers_46f4a262_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./helpers-46f4a262.js */ "./node_modules/@ionic/core/dist/esm-es5/helpers-46f4a262.js");
/* harmony import */ var _theme_18cbe2cc_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./theme-18cbe2cc.js */ "./node_modules/@ionic/core/dist/esm-es5/theme-18cbe2cc.js");





var Segment = /** @class */ (function () {
    function class_1(hostRef) {
        var _this = this;
        Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["r"])(this, hostRef);
        this.didInit = false;
        this.activated = false;
        /**
         * If `true`, the user cannot interact with the segment.
         */
        this.disabled = false;
        /**
         * If `true`, the segment buttons will overflow and the user can swipe to see them.
         * In addition, this will disable the gesture to drag the indicator between the buttons
         * in order to swipe to see hidden buttons.
         */
        this.scrollable = false;
        this.onClick = function (ev) {
            var current = ev.target;
            var previous = _this.checked;
            _this.value = current.value;
            if (previous && _this.scrollable) {
                _this.checkButton(previous, current);
            }
            _this.checked = current;
        };
        this.ionChange = Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["d"])(this, "ionChange", 7);
        this.ionSelect = Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["d"])(this, "ionSelect", 7);
        this.ionStyle = Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["d"])(this, "ionStyle", 7);
    }
    class_1.prototype.valueChanged = function (value, oldValue) {
        this.ionSelect.emit({ value: value });
        if (oldValue !== '' || this.didInit) {
            if (!this.activated) {
                this.ionChange.emit({ value: value });
            }
            else {
                this.valueAfterGesture = value;
            }
        }
    };
    class_1.prototype.disabledChanged = function () {
        this.gestureChanged();
        var buttons = this.getButtons();
        for (var _i = 0, buttons_1 = buttons; _i < buttons_1.length; _i++) {
            var button = buttons_1[_i];
            button.disabled = this.disabled;
        }
    };
    class_1.prototype.gestureChanged = function () {
        if (this.gesture && !this.scrollable) {
            this.gesture.enable(!this.disabled);
        }
    };
    class_1.prototype.connectedCallback = function () {
        this.emitStyle();
    };
    class_1.prototype.componentWillLoad = function () {
        this.emitStyle();
    };
    class_1.prototype.componentDidLoad = function () {
        return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"])(this, void 0, void 0, function () {
            var _a;
            var _this = this;
            return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"])(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.setCheckedClasses();
                        _a = this;
                        return [4 /*yield*/, Promise.resolve(/*! import() */).then(__webpack_require__.bind(null, /*! ./index-c38df685.js */ "./node_modules/@ionic/core/dist/esm-es5/index-c38df685.js"))];
                    case 1:
                        _a.gesture = (_b.sent()).createGesture({
                            el: this.el,
                            gestureName: 'segment',
                            gesturePriority: 100,
                            threshold: 0,
                            passive: false,
                            onStart: function (ev) { return _this.onStart(ev); },
                            onMove: function (ev) { return _this.onMove(ev); },
                            onEnd: function (ev) { return _this.onEnd(ev); },
                        });
                        this.gesture.enable(!this.scrollable);
                        this.gestureChanged();
                        if (this.disabled) {
                            this.disabledChanged();
                        }
                        this.didInit = true;
                        return [2 /*return*/];
                }
            });
        });
    };
    class_1.prototype.onStart = function (detail) {
        this.activate(detail);
    };
    class_1.prototype.onMove = function (detail) {
        this.setNextIndex(detail);
    };
    class_1.prototype.onEnd = function (detail) {
        this.setActivated(false);
        var checkedValidButton = this.setNextIndex(detail, true);
        detail.event.preventDefault();
        detail.event.stopImmediatePropagation();
        if (checkedValidButton) {
            this.addRipple(detail);
        }
        var value = this.valueAfterGesture;
        if (value !== undefined) {
            this.ionChange.emit({ value: value });
            this.valueAfterGesture = undefined;
        }
    };
    class_1.prototype.getButtons = function () {
        return Array.from(this.el.querySelectorAll('ion-segment-button'));
    };
    /**
     * The gesture blocks the segment button ripple. This
     * function adds the ripple based on the checked segment
     * and where the cursor ended.
     */
    class_1.prototype.addRipple = function (detail) {
        var _this = this;
        var useRippleEffect = _config_3c7f3790_js__WEBPACK_IMPORTED_MODULE_2__["b"].getBoolean('animated', true) && _config_3c7f3790_js__WEBPACK_IMPORTED_MODULE_2__["b"].getBoolean('rippleEffect', true);
        if (!useRippleEffect) {
            return;
        }
        var buttons = this.getButtons();
        var checked = buttons.find(function (button) { return button.value === _this.value; });
        var root = checked.shadowRoot || checked;
        var ripple = root.querySelector('ion-ripple-effect');
        if (!ripple) {
            return;
        }
        var _a = Object(_helpers_46f4a262_js__WEBPACK_IMPORTED_MODULE_3__["p"])(detail.event), x = _a.x, y = _a.y;
        ripple.addRipple(x, y).then(function (remove) { return remove(); });
    };
    /*
     * Activate both the segment and the buttons
     * due to a bug with ::slotted in Safari
     */
    class_1.prototype.setActivated = function (activated) {
        var buttons = this.getButtons();
        buttons.forEach(function (button) {
            if (activated) {
                button.classList.add('segment-button-activated');
            }
            else {
                button.classList.remove('segment-button-activated');
            }
        });
        this.activated = activated;
    };
    class_1.prototype.activate = function (detail) {
        var _this = this;
        var clicked = detail.event.target;
        var buttons = this.getButtons();
        var checked = buttons.find(function (button) { return button.value === _this.value; });
        // Make sure we are only checking for activation on a segment button
        // since disabled buttons will get the click on the segment
        if (clicked.tagName !== 'ION-SEGMENT-BUTTON') {
            return;
        }
        // If there are no checked buttons, set the current button to checked
        if (!checked) {
            this.value = clicked.value;
        }
        // If the gesture began on the clicked button with the indicator
        // then we should activate the indicator
        if (this.value === clicked.value) {
            this.setActivated(true);
        }
    };
    class_1.prototype.getIndicator = function (button) {
        var root = button.shadowRoot || button;
        return root.querySelector('.segment-button-indicator');
    };
    class_1.prototype.checkButton = function (previous, current) {
        var previousIndicator = this.getIndicator(previous);
        var currentIndicator = this.getIndicator(current);
        if (previousIndicator === null || currentIndicator === null) {
            return;
        }
        var previousClientRect = previousIndicator.getBoundingClientRect();
        var currentClientRect = currentIndicator.getBoundingClientRect();
        var widthDelta = previousClientRect.width / currentClientRect.width;
        var xPosition = previousClientRect.left - currentClientRect.left;
        // Scale the indicator width to match the previous indicator width
        // and translate it on top of the previous indicator
        var transform = "translate3d(" + xPosition + "px, 0, 0) scaleX(" + widthDelta + ")";
        Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["w"])(function () {
            // Remove the transition before positioning on top of the previous indicator
            currentIndicator.classList.remove('segment-button-indicator-animated');
            currentIndicator.style.setProperty('transform', transform);
            // Force a repaint to ensure the transform happens
            currentIndicator.getBoundingClientRect();
            // Add the transition to move the indicator into place
            currentIndicator.classList.add('segment-button-indicator-animated');
            // Remove the transform to slide the indicator back to the button clicked
            currentIndicator.style.setProperty('transform', '');
        });
        this.value = current.value;
        this.setCheckedClasses();
    };
    class_1.prototype.setCheckedClasses = function () {
        var _this = this;
        var buttons = this.getButtons();
        var index = buttons.findIndex(function (button) { return button.value === _this.value; });
        var next = index + 1;
        // Keep track of the currently checked button
        this.checked = buttons.find(function (button) { return button.value === _this.value; });
        for (var _i = 0, buttons_2 = buttons; _i < buttons_2.length; _i++) {
            var button = buttons_2[_i];
            button.classList.remove('segment-button-after-checked');
        }
        if (next < buttons.length) {
            buttons[next].classList.add('segment-button-after-checked');
        }
    };
    class_1.prototype.setNextIndex = function (detail, isEnd) {
        var _this = this;
        if (isEnd === void 0) { isEnd = false; }
        var isRTL = document.dir === 'rtl';
        var activated = this.activated;
        var buttons = this.getButtons();
        var index = buttons.findIndex(function (button) { return button.value === _this.value; });
        var previous = buttons[index];
        var current;
        var nextIndex;
        if (index === -1) {
            return;
        }
        // Get the element that the touch event started on in case
        // it was the checked button, then we will move the indicator
        var rect = previous.getBoundingClientRect();
        var left = rect.left;
        var width = rect.width;
        // Get the element that the gesture is on top of based on the currentX of the
        // gesture event and the Y coordinate of the starting element, since the gesture
        // can move up and down off of the segment
        var currentX = detail.currentX;
        var previousY = rect.top + (rect.height / 2);
        var nextEl = document.elementFromPoint(currentX, previousY);
        var decreaseIndex = isRTL ? currentX > (left + width) : currentX < left;
        var increaseIndex = isRTL ? currentX < left : currentX > (left + width);
        // If the indicator is currently activated then we have started the gesture
        // on top of the checked button so we need to slide the indicator
        // by checking the button next to it as we move
        if (activated && !isEnd) {
            // Decrease index, move left in LTR & right in RTL
            if (decreaseIndex) {
                var newIndex = index - 1;
                if (newIndex >= 0) {
                    nextIndex = newIndex;
                }
                // Increase index, moves right in LTR & left in RTL
            }
            else if (increaseIndex) {
                if (activated && !isEnd) {
                    var newIndex = index + 1;
                    if (newIndex < buttons.length) {
                        nextIndex = newIndex;
                    }
                }
            }
            if (nextIndex !== undefined && !buttons[nextIndex].disabled) {
                current = buttons[nextIndex];
            }
        }
        // If the indicator is not activated then we will just set the indicator
        // to the element where the gesture ended
        if (!activated && isEnd) {
            current = nextEl;
        }
        /* tslint:disable-next-line */
        if (current != null) {
            /**
             * If current element is ion-segment then that means
             * user tried to select a disabled ion-segment-button,
             * and we should not update the ripple.
             */
            if (current.tagName === 'ION-SEGMENT') {
                return false;
            }
            if (previous !== current) {
                this.checkButton(previous, current);
            }
        }
        return true;
    };
    class_1.prototype.emitStyle = function () {
        this.ionStyle.emit({
            'segment': true
        });
    };
    class_1.prototype.render = function () {
        var _a;
        var mode = Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["c"])(this);
        return (Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["h"])(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["H"], { onClick: this.onClick, class: Object.assign(Object.assign({}, Object(_theme_18cbe2cc_js__WEBPACK_IMPORTED_MODULE_4__["c"])(this.color)), (_a = {}, _a[mode] = true, _a['in-toolbar'] = Object(_theme_18cbe2cc_js__WEBPACK_IMPORTED_MODULE_4__["h"])('ion-toolbar', this.el), _a['in-toolbar-color'] = Object(_theme_18cbe2cc_js__WEBPACK_IMPORTED_MODULE_4__["h"])('ion-toolbar[color]', this.el), _a['segment-activated'] = this.activated, _a['segment-disabled'] = this.disabled, _a['segment-scrollable'] = this.scrollable, _a)) }, Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["h"])("slot", null)));
    };
    Object.defineProperty(class_1.prototype, "el", {
        get: function () { return Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["e"])(this); },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(class_1, "watchers", {
        get: function () {
            return {
                "value": ["valueChanged"],
                "disabled": ["disabledChanged"]
            };
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(class_1, "style", {
        get: function () { return ":host{--ripple-color:currentColor;-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;display:-ms-flexbox;display:flex;position:relative;-ms-flex-align:stretch;align-items:stretch;-ms-flex-pack:center;justify-content:center;width:100%;background:var(--background);font-family:var(--ion-font-family,inherit);text-align:center;contain:paint}:host(.segment-scrollable){-ms-flex-pack:start;justify-content:start;width:auto;overflow-x:scroll}:host(.segment-scrollable::-webkit-scrollbar){display:none}:host{--background:rgba(var(--ion-text-color-rgb,0,0,0),0.065);border-radius:8px;overflow:hidden;z-index:0}:host(.ion-color){background:rgba(var(--ion-color-base-rgb),.065)}:host(.in-toolbar){margin-left:auto;margin-right:auto;margin-top:0;margin-bottom:0;width:auto}\@supports ((-webkit-margin-start:0) or (margin-inline-start:0)) or (-webkit-margin-start:0){:host(.in-toolbar){margin-left:unset;margin-right:unset;-webkit-margin-start:auto;margin-inline-start:auto;-webkit-margin-end:auto;margin-inline-end:auto}}:host(.in-toolbar:not(.ion-color)){background:var(--ion-toolbar-segment-background,var(--background))}:host(.in-toolbar-color:not(.ion-color)){background:rgba(var(--ion-color-contrast-rgb),.11)}"; },
        enumerable: true,
        configurable: true
    });
    return class_1;
}());
var ids = 0;
var SegmentButton = /** @class */ (function () {
    function SegmentButton(hostRef) {
        var _this = this;
        Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["r"])(this, hostRef);
        this.segmentEl = null;
        this.checked = false;
        /**
         * If `true`, the user cannot interact with the segment button.
         */
        this.disabled = false;
        /**
         * Set the layout of the text and icon in the segment.
         */
        this.layout = 'icon-top';
        /**
         * The type of the button.
         */
        this.type = 'button';
        /**
         * The value of the segment button.
         */
        this.value = 'ion-sb-' + (ids++);
        this.updateState = function () {
            if (_this.segmentEl) {
                _this.checked = _this.segmentEl.value === _this.value;
            }
        };
    }
    SegmentButton.prototype.connectedCallback = function () {
        var segmentEl = this.segmentEl = this.el.closest('ion-segment');
        if (segmentEl) {
            this.updateState();
            segmentEl.addEventListener('ionSelect', this.updateState);
        }
    };
    SegmentButton.prototype.disconnectedCallback = function () {
        var segmentEl = this.segmentEl;
        if (segmentEl) {
            segmentEl.removeEventListener('ionSelect', this.updateState);
            this.segmentEl = null;
        }
    };
    Object.defineProperty(SegmentButton.prototype, "hasLabel", {
        get: function () {
            return !!this.el.querySelector('ion-label');
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(SegmentButton.prototype, "hasIcon", {
        get: function () {
            return !!this.el.querySelector('ion-icon');
        },
        enumerable: true,
        configurable: true
    });
    SegmentButton.prototype.render = function () {
        var _a;
        var _b = this, checked = _b.checked, type = _b.type, disabled = _b.disabled, hasIcon = _b.hasIcon, hasLabel = _b.hasLabel, layout = _b.layout;
        var mode = Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["c"])(this);
        return (Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["h"])(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["H"], { "aria-disabled": disabled ? 'true' : null, class: (_a = {},
                _a[mode] = true,
                _a['in-toolbar'] = Object(_theme_18cbe2cc_js__WEBPACK_IMPORTED_MODULE_4__["h"])('ion-toolbar', this.el),
                _a['in-toolbar-color'] = Object(_theme_18cbe2cc_js__WEBPACK_IMPORTED_MODULE_4__["h"])('ion-toolbar[color]', this.el),
                _a['in-segment'] = Object(_theme_18cbe2cc_js__WEBPACK_IMPORTED_MODULE_4__["h"])('ion-segment', this.el),
                _a['in-segment-color'] = Object(_theme_18cbe2cc_js__WEBPACK_IMPORTED_MODULE_4__["h"])('ion-segment[color]', this.el),
                _a['segment-button-has-label'] = hasLabel,
                _a['segment-button-has-icon'] = hasIcon,
                _a['segment-button-has-label-only'] = hasLabel && !hasIcon,
                _a['segment-button-has-icon-only'] = hasIcon && !hasLabel,
                _a['segment-button-disabled'] = disabled,
                _a['segment-button-checked'] = checked,
                _a["segment-button-layout-" + layout] = true,
                _a['ion-activatable'] = true,
                _a['ion-activatable-instant'] = true,
                _a['ion-focusable'] = true,
                _a) }, Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["h"])("button", { type: type, "aria-pressed": checked ? 'true' : null, class: "button-native", disabled: disabled }, Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["h"])("span", { class: "button-inner" }, Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["h"])("slot", null)), mode === 'md' && Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["h"])("ion-ripple-effect", null)), Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["h"])("div", { part: "indicator", class: {
                'segment-button-indicator': true,
                'segment-button-indicator-animated': true
            } }, Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["h"])("div", { part: "indicator-background", class: "segment-button-indicator-background" }))));
    };
    Object.defineProperty(SegmentButton.prototype, "el", {
        get: function () { return Object(_core_80bde1aa_js__WEBPACK_IMPORTED_MODULE_1__["e"])(this); },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(SegmentButton, "style", {
        get: function () { return ":host{--color:initial;--color-hover:var(--color);--color-checked:var(--color);--color-disabled:var(--color);--padding-start:0;--padding-end:0;border-radius:var(--border-radius);-ms-flex:1 1 auto;flex:1 1 auto;-ms-flex-direction:column;flex-direction:column;background:var(--background);color:var(--color);text-decoration:none;text-overflow:ellipsis;white-space:nowrap;-webkit-font-kerning:none;font-kerning:none;cursor:pointer}.button-native,:host{display:-ms-flexbox;display:flex;height:auto}.button-native{border-radius:0;font-family:inherit;font-size:inherit;font-style:inherit;font-weight:inherit;letter-spacing:inherit;text-decoration:inherit;text-indent:inherit;text-overflow:inherit;text-transform:inherit;text-align:inherit;white-space:inherit;color:inherit;margin-left:var(--margin-start);margin-right:var(--margin-end);margin-top:var(--margin-top);margin-bottom:var(--margin-bottom);padding-left:var(--padding-start);padding-right:var(--padding-end);padding-top:var(--padding-top);padding-bottom:var(--padding-bottom);-webkit-transform:translateZ(0);transform:translateZ(0);position:relative;-ms-flex-direction:inherit;flex-direction:inherit;-ms-flex-positive:1;flex-grow:1;-ms-flex-align:center;align-items:center;-ms-flex-pack:center;justify-content:center;width:100%;min-width:inherit;max-width:inherit;min-height:inherit;max-height:inherit;-webkit-transition:var(--transition);transition:var(--transition);border:none;outline:none;background:transparent;contain:content;pointer-events:none;overflow:hidden;z-index:2}\@supports ((-webkit-margin-start:0) or (margin-inline-start:0)) or (-webkit-margin-start:0){.button-native{margin-left:unset;margin-right:unset;-webkit-margin-start:var(--margin-start);margin-inline-start:var(--margin-start);-webkit-margin-end:var(--margin-end);margin-inline-end:var(--margin-end);padding-left:unset;padding-right:unset;-webkit-padding-start:var(--padding-start);padding-inline-start:var(--padding-start);-webkit-padding-end:var(--padding-end);padding-inline-end:var(--padding-end)}}.button-native:after{left:0;right:0;top:0;bottom:0;position:absolute;content:\"\";opacity:0}.button-inner{display:-ms-flexbox;display:flex;position:relative;-ms-flex-flow:inherit;flex-flow:inherit;-ms-flex-align:center;align-items:center;-ms-flex-pack:center;justify-content:center;width:100%;height:100%;z-index:1}:host(.segment-button-checked){background:var(--background-checked);color:var(--color-checked)}:host(.segment-button-disabled){cursor:default;pointer-events:none}:host(.ion-focused) .button-native{color:var(--color-focused)}:host(.ion-focused) .button-native:after{background:var(--background-focused);opacity:var(--background-focused-opacity)}\@media (any-hover:hover){:host(:hover) .button-native{color:var(--color-hover)}:host(:hover) .button-native:after{background:var(--background-hover);opacity:var(--background-hover-opacity)}:host(.segment-button-checked:hover) .button-native{color:var(--color-checked)}}::slotted(ion-icon){-ms-flex-negative:0;flex-shrink:0;-ms-flex-order:-1;order:-1;pointer-events:none}::slotted(ion-label){display:block;-ms-flex-item-align:center;align-self:center;line-height:22px;text-overflow:ellipsis;white-space:nowrap;-webkit-box-sizing:border-box;box-sizing:border-box;pointer-events:none}:host(.segment-button-layout-icon-top) .button-native{-ms-flex-direction:column;flex-direction:column}:host(.segment-button-layout-icon-start) .button-native{-ms-flex-direction:row;flex-direction:row}:host(.segment-button-layout-icon-end) .button-native{-ms-flex-direction:row-reverse;flex-direction:row-reverse}:host(.segment-button-layout-icon-bottom) .button-native{-ms-flex-direction:column-reverse;flex-direction:column-reverse}:host(.segment-button-layout-icon-hide) ::slotted(ion-icon),:host(.segment-button-layout-label-hide) ::slotted(ion-label){display:none}ion-ripple-effect{color:var(--ripple-color,var(--color-checked))}.segment-button-indicator{-webkit-transform-origin:left;transform-origin:left;position:absolute;opacity:0;-webkit-box-sizing:border-box;box-sizing:border-box;will-change:transform,opacity}.segment-button-indicator-background{width:100%;height:var(--indicator-height);-webkit-transform:var(--indicator-transform);transform:var(--indicator-transform);-webkit-box-shadow:var(--indicator-box-shadow);box-shadow:var(--indicator-box-shadow)}.segment-button-indicator-animated{-webkit-transition:var(--indicator-transition);transition:var(--indicator-transition)}:host(.segment-button-checked) .segment-button-indicator{opacity:1}\@media (prefers-reduced-motion:reduce){.segment-button-indicator-background{-webkit-transform:none;transform:none}.segment-button-indicator-animated{-webkit-transition:none;transition:none}}:host{--background:none;--background-checked:none;--background-hover:none;--background-hover-opacity:0;--background-focused:none;--background-focused-opacity:0;--border-radius:7px;--border-width:1px;--border-color:rgba(var(--ion-text-color-rgb,0,0,0),0.12);--border-style:solid;--indicator-box-shadow:0 0 5px rgba(0,0,0,0.16);--indicator-color:var(--ion-color-step-350,var(--ion-background-color,#fff));--indicator-height:100%;--indicator-transition:transform 260ms cubic-bezier(0.4,0,0.2,1);--indicator-transform:none;--transition:100ms all linear;--padding-top:0;--padding-end:13px;--padding-bottom:0;--padding-start:13px;margin-top:2px;margin-bottom:2px;position:relative;-ms-flex-preferred-size:0;flex-basis:0;-ms-flex-direction:row;flex-direction:row;min-width:70px;min-height:28px;-webkit-transform:translateZ(0);transform:translateZ(0);font-size:13px;font-weight:450;line-height:37px}:host:before{margin-left:0;margin-right:0;margin-top:5px;margin-bottom:5px;-webkit-transition:opacity .16s ease-in-out;transition:opacity .16s ease-in-out;-webkit-transition-delay:.1s;transition-delay:.1s;border-left:var(--border-width) var(--border-style) var(--border-color);content:\"\";opacity:1;will-change:opacity}:host(:first-of-type):before{border-left-color:transparent}:host(.segment-button-disabled){opacity:.3}::slotted(ion-icon){font-size:24px}:host(.segment-button-layout-icon-start) ::slotted(ion-label){margin-left:2px;margin-right:0}\@supports ((-webkit-margin-start:0) or (margin-inline-start:0)) or (-webkit-margin-start:0){:host(.segment-button-layout-icon-start) ::slotted(ion-label){margin-left:unset;margin-right:unset;-webkit-margin-start:2px;margin-inline-start:2px;-webkit-margin-end:0;margin-inline-end:0}}:host(.segment-button-layout-icon-end) ::slotted(ion-label){margin-left:0;margin-right:2px}\@supports ((-webkit-margin-start:0) or (margin-inline-start:0)) or (-webkit-margin-start:0){:host(.segment-button-layout-icon-end) ::slotted(ion-label){margin-left:unset;margin-right:unset;-webkit-margin-start:0;margin-inline-start:0;-webkit-margin-end:2px;margin-inline-end:2px}}.segment-button-indicator{padding-left:2px;padding-right:2px;left:0;right:0;top:0;bottom:0}\@supports ((-webkit-margin-start:0) or (margin-inline-start:0)) or (-webkit-margin-start:0){.segment-button-indicator{padding-left:unset;padding-right:unset;-webkit-padding-start:2px;padding-inline-start:2px;-webkit-padding-end:2px;padding-inline-end:2px}}.segment-button-indicator-background{border-radius:var(--border-radius);background:var(--indicator-color);-webkit-transition:var(--indicator-transition);transition:var(--indicator-transition)}:host(.segment-button-after-checked):before,:host(.segment-button-checked):before{opacity:0}:host(.segment-button-checked){z-index:-1}:host(.segment-button-activated){--indicator-transform:scale(0.95)}:host(.ion-focused) .button-native{opacity:.7}\@media (any-hover:hover){:host(:hover) .button-native{opacity:.5}:host(.segment-button-checked:hover) .button-native{opacity:1}}:host(.in-segment-color){background:none;color:var(--ion-text-color,#000)}:host(.in-segment-color) .segment-button-indicator-background{background:var(--ion-color-step-350,var(--ion-background-color,#fff))}\@media (any-hover:hover){:host(.in-segment-color.segment-button-checked:hover) .button-native,:host(.in-segment-color:hover) .button-native{color:var(--ion-text-color,#000)}}:host(.in-toolbar:not(.in-segment-color)){--background-checked:var(--ion-toolbar-segment-background-checked,none);--color:var(--ion-toolbar-segment-color,var(--ion-toolbar-color),initial);--color-checked:var(--ion-toolbar-segment-color-checked,var(--ion-toolbar-color),initial);--indicator-color:var(--ion-toolbar-segment-indicator-color,var(--ion-color-step-350,var(--ion-background-color,#fff)))}:host(.in-toolbar-color) .segment-button-indicator-background{background:#fff}:host(.in-toolbar-color:not(.in-segment-color)) .button-native{color:var(--ion-color-contrast)}:host(.in-toolbar-color.segment-button-checked:not(.in-segment-color)) .button-native{color:var(--ion-color-base)}\@media (any-hover:hover){:host(.in-toolbar-color:not(.in-segment-color):hover) .button-native{color:var(--ion-color-contrast)}:host(.in-toolbar-color.segment-button-checked:not(.in-segment-color):hover) .button-native{color:var(--ion-color-base)}}"; },
        enumerable: true,
        configurable: true
    });
    return SegmentButton;
}());



/***/ })

}]);
//# sourceMappingURL=59.js.map
/**
* Patching an existing class for modify start method. It is necessary for convert default checkout in OSC.
* thus, only add a ajax call to reload page when an acquirer is changed if is necessary.
* Includes a load gif image when reload is required.
*/

odoo.define("website_sale_one_step_checkout_charge_payment_fee.osc", function (require) {
    "use strict";

    var inherit = require('website_sale_one_step_checkout.osc');
    var ajax = require('web.ajax');

    var OneStepCheckoutChargePayment = inherit.include({
        start: function () {
            var self = this;

            // activate event listener
            self.changeShipping();
            self.hideShow();

            // Editing Billing Address
            $('.js-billing-address .js_edit_address').on('click',
                function (e) {
                    self.editBilling(null, self, e)
                });

            // Editing shipping address
            $('.js-shipping-address .js_edit_address').on('click', function (e) {
                self.editShipping(self, e)
            });

            // Add new shipping address
            $("#add-shipping-address").on('click', 'a, input', function (e) {
                self.addShipping(self, e)
            });

            $('#address-modal').on('click', '#js_confirm_address', function (ev) {
                ev.preventDefault();
                ev.stopPropagation();
                // Upon confirmation, validate data.
                self.validateModalAddress();
                return false;
            });

            // when choosing an acquirer, display its order now button
            var $payment = $('#payment_method');
            $payment.on('click', 'input[name="acquirer"]', function (ev) {
                var payment_id = $(ev.currentTarget).val();
                $('div.oe_sale_acquirer_button[data-id]').addClass('hidden');
                $('div.oe_sale_acquirer_button[data-id="' + payment_id + '"]').removeClass('hidden');

                // Get acquirer to check for fee payment, when true then reload page
                // It is necessary for simulate default checkout in one step checkout
                var acquirer = $('input[name="acquirer"]:checked'),
                data = {};
                data = self.getPostFields(acquirer, data);
                data['payment_fee_id'] = payment_id

                return ajax.jsonRpc('/shop/checkout/charge_payment/', 'call', data).then(function (result) {

                    // Load spinner gif image
                    var $spn_div = $('#col-3');
                    var spinner = '<div class="wp-load-spinner"/>';
                    $spn_div.append(spinner);

                    if (result['reload_page'] === true) {
                        window.location.reload(true);
                    } else {
                        $spn_div.find('.wp-load-spinner').fadeOut(300);
                        $spn_div.find('.wp-load-spinner').detach();
                    }
                });
            });

            // when clicking checkout submit button validate address data first
            // if all is fine trigger payment transaction
            $('#col-3 .js_payment').on('click', 'form button[type=submit]', function (ev) {
                ev.preventDefault();
                ev.stopPropagation();

                self.checkData().then(function (result) {
                    if (result.success) {
                        // proceed to payment transaction
                        self.proceedPayment(ev);
                    } else {
                        return false;
                        // do nothing, address modal in edit mode
                        // will get automatically opened at this point
                    }
                });
                return false;
            });
        }
    });
});
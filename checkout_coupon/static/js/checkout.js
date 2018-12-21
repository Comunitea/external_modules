odoo.define('checkout_coupon.couponcheck', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    $('.wp-checkout-coupon form#to_checkout').on('submit', function(e){
        e.preventDefault();

        var coupon_code = $('input[name="coupon_code"]').val();

        if(coupon_code.length < 4){
            $('.coupon-message').html('<div class="red">Coupon code is too short</div>');
        }else{
            $('.wp-checkout-loader').toggle();
            ajax.jsonRpc('/shop/checkout/couponcheck', 'call', {
                'coupon_code': coupon_code
            }).then(function (data) {
                data = $.parseJSON(data);
//                console.log(data)
                setTimeout(function(){
                    if(data['success'] == true){
                        window.location.replace(window.location.href);
                    }else{
                        $('.coupon-message').html('<div class="'+data['flags']+'">'+data['message']+'</div>');
                        $('.wp-checkout-loader').toggle();
                    }
                }, 500);
            });
        }
    });

    $('.wp-checkout-coupon form#to_remove').on('submit', function(e){
        e.preventDefault();
        $('.wp-checkout-loader').toggle();

        var coupon_code = $('input[name="coupon_code"]').val();

        ajax.jsonRpc('/shop/checkout/couponremove', 'call', {
            'coupon_code': coupon_code
        }).then(function (data) {
            data = $.parseJSON(data);
//            console.log(data)
            setTimeout(function(){
                if(data['success'] == true){
                    window.location.replace(window.location.href);
                }else{
                    $('.coupon-message').html('<div class="'+data['flags']+'">'+data['message']+'</div>');
                    $('.wp-checkout-loader').toggle();
                }
            }, 500);
        });
    });

});
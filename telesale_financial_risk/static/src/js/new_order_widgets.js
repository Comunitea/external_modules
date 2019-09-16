odoo.define('telesale_financial_risk.new_order_widgets2', function (require) {
"use strict";
var NewOrderWidgets = require('telesale.new_order_widgets');
var core = require('web.core');
var _t = core._t;
var rpc = require('web.rpc');



// var DataOrderWidget = NewOrderWidgets.DataOrderWidget.include({
//     // FULL OVERWRITED TO MANAGE RISK EXCEPTION OR THE WARNING
//     perform_onchange: function(key, value) {
//         var self=this;
//         if (!value) {return;}
//         if (key == "partner"){
//             var partner_id = self.ts_model.db.partner_name_id[value];

//             // Not partner found in backbone model
//             if (value && !partner_id){
//                 var alert_msg = _t("Customer name '" + value + "' does not exist");
//                 alert(alert_msg);
//                 self.order_model.set('partner', "");
//                 self.refresh();
//                 self.$('#partner').focus();
//             }
//             else {
//                 var partner_obj = self.ts_model.db.get_partner_by_id(partner_id);
//                 var model = new Model("sale.order");
//                 model.call("ts_onchange_partner_id", [partner_id])
//                 .then(function(result){
//                     var cus_name = self.ts_model.getComplexName(partner_obj);
//                     self.order_model.set('partner', cus_name);
//                     self.order_model.set('partner_code', partner_obj.ref ? partner_obj.ref : "");

//                     self.order_model.set('customer_comment', partner_obj.comment);

//                     self.order_model.set('comercial', partner_obj.user_id ? partner_obj.user_id[1] : "");
//                     var partner_shipp_obj = self.ts_model.db.get_partner_by_id(result.partner_shipping_id);
//                     var shipp_addr =self.ts_model.getComplexName(partner_shipp_obj);
//                     self.order_model.set('shipp_addr', shipp_addr);
//                     var pricelist_obj = self.ts_model.db.pricelist_by_id[result.pricelist_id];
//                     if (pricelist_obj){
//                         self.order_model.set('pricelist', pricelist_obj.name);
//                     }
//                     self.order_model.set('epd', result.early_payment_discount);
//                     // Get alert if warning is not false
//                     if (result.warning){
//                         alert(result.warning);
//                         if (result.mode == 'block'){
//                             self.order_model.set('partner', "");
//                         }
//                     }
//                     self.refresh();
//                     // New line and VUA button when chang
//                     // Only do it when partner is setted
//                     // if (self.order_model.get('partner')){
//                     //     $('#vua-button').click();
//                     // }
//                     if(self.order_model.get('orderLines').length == 0 && self.order_model.get('partner')){
//                         $('.add-line-button').click()
//                     }
//                     else{
//                         self.$('#date_order').focus();
//                     }

//                 });
//             }
//         }
//         else if (key == "pricelist"){
//             var pricelist_id = self.ts_model.db.pricelist_name_id[value];

//             // Not partner found in backbone model
//             if (!pricelist_id){
//                 var alert_msg = _t("Pricelist name '" + value + "' does not exist");
//                 alert(alert_msg);
//                 self.order_model.set('pricelist', "");
//                 self.refresh();
//                 self.$('#pricelist').focus();
//             }
//         }
//     },
// });

var TotalsOrderWidget = NewOrderWidgets.TotalsOrderWidget.include({

    // Checks risk before puting into lqdr state or pending
    // OVERWRITED
    confirmCurrentOrder: function() {
        var self = this;
        var currentOrder = this.order_model;
        currentOrder.set('action_button', 'save')
        if ( (currentOrder.get('erp_state')) && (currentOrder.get('erp_state') != 'draft') ){
            alert(_t('You cant confirm an order which state is diferent than draft.'));
            self.enable_more_clicks();
            return;
        }
        self.saveCurrentOrder(true)
        $.when( self.ts_model.ready2 )
        .done(function(){
            if (self.ts_model.last_sale_id){
                var domain = [['id', '=', self.ts_model.last_sale_id]]
            }
            else{
                var domain = [['chanel', '=', 'telesale'], ['user_id', '=', self.ts_model.get('user').id]]
            }
            var loaded = self.ts_model.fetch('sale.order', ['id', 'name'], domain)
                .then(function(orders){
                    if (orders[0]) {
                        // MIG11: Quizá con notación then.
                        rpc.query({model: 'sale.order', method: 'get_risk_msg', args:[orders[0].id]})
                        .fail(function(unused, event){
                            //don't show error popup if it fails
                            self.ts_model.last_sale_id = false
                        })
                        .done(function(msg){
                            
                            var skip = true;
                            if (msg){
                                var skip = confirm(msg)
                            }
                            // IF NO MSG OR SKIP MSG WE CONFIRM THE ORDER
                            if (skip){
                                // MIG11: Quizá con notación then
                                rpc({model: 'sale.order', method: 'confirm_order_from_ui', args:[orders[0].id], context:{bypass_risk: true}})
                                .fail(function(unused, event){
                                  //don't show error popup if it fails
                                   self.ts_model.last_sale_id = false
                                })
                                .done(function(res){
                                    // LOAD THE ORDER
                                    var my_id = orders[0].id
                                    $.when( self.ts_widget.new_order_screen.order_widget.load_order_from_server(my_id) )
                                        .done(function(){
                                            self.ts_model.last_sale_id = false
                                        })
                                        .fail(function(){
                                            self.ts_model.last_sale_id = false
                                    });
                                });

                            }
                            // IF RISK AND NOT SKIPPED, NO CONFIRM, BUT LOAD THE ORDER AGAIN
                            else {
                                var my_id = orders[0].id
                                $.when( self.ts_widget.new_order_screen.order_widget.load_order_from_server(my_id) )
                                    .done(function(){
                                        self.ts_model.last_sale_id = false
                                    })
                                    .fail(function(){
                                        self.ts_model.last_sale_id = false
                                });
                            }

                        });

                    }
                });
         });
    },

});


});

odoo.define('Web_Printscreen.Pager', function (require) {
"use strict";

var Pager = require('web.Pager');
var core = require('web.core');
var session = require('web.session');

var _t = core._t;

return Pager.include({
  start: function() {
    this._super();
    var self = this;
    this.$el.find("a#button_export_excel").click(function(event){
      self.export_to_excel("excel");
    });

    this.$el.find("a#button_export_pdf").click(function(event){
      self.export_to_excel("pdf");
    });
  },

  export_to_excel: function(export_type) {
    var self = this
    var export_type = export_type
    var view = this.getParent()

    // Find Header Element
    var header_eles = self.getParent().$el.find('.o_list_view > thead')
    var header_name_list = []
    $.each(header_eles,function(){
      var $header_ele = $(this)
      var header_td_elements = $header_ele.find('th')
      var i = 0;
      $.each(header_td_elements,function(){
        var $header_td = $(this)
        var data_id = ''
        var text = $header_td.text().trim() || ""
        if($header_td.attr("class") != 'o_list_record_selector') {
          data_id = self.getParent().renderer.columns[i].attrs.name;
          i += 1;
        }
        header_name_list.push({'header_name': text.trim(), 'header_data_id': data_id})
      });
    });

    //Find Data Element
    var data_eles = self.getParent().$el.find('.o_list_view > tbody > tr')
    var export_data = []
    $.each(data_eles,function(){
      var data = []
      var $data_ele = $(this)
      var is_analysis = false
      if ($data_ele.text().trim()){
      //Find group name
        var group_th_eles = $data_ele.find('th')
        $.each(group_th_eles,function(){
          var $group_th_ele = $(this)
          var text = $group_th_ele.text().trim() || ""
          var is_analysis = true
          data.push({'data': text, 'bold': true})
        });
        var data_td_eles = $data_ele.find('td')
        $.each(data_td_eles,function(){
          var $data_td_ele = $(this)
          var text = $data_td_ele.text().trim() || ""
          if ($data_td_ele && $data_td_ele[0].classList.contains('oe_number') && !$data_td_ele[0].classList.contains('oe_list_field_float_time')){
            var text = text.replace('%', '')
            data.push({'data': text || "", 'number': true})
          }
          else{
            data.push({'data': text})
          }
        });
        export_data.push(data)
      }
    });

    //Find Footer Element

    var parse_float = function(value) {
      //copy of old odoo/addons/web/static/src/js/framework/formats.js
      var tmp2 = value;
      do {
        tmp = tmp2;
        tmp2 = tmp.replace(_t.database.parameters.thousands_sep, "");
      } while(tmp !== tmp2);
      var reformatted_value = tmp.replace(_t.database.parameters.decimal_point, ".");
      var parsed = Number(reformatted_value);
      if (isNaN(parsed))
        throw new Error(_.str.sprintf(_t("'%s' is not a correct float"), value));
      return parsed;
    }

    var footer_eles = self.getParent().$el.find('.o_list_view > tfoot> tr')
    $.each(footer_eles,function(){
      var data = []
      var $footer_ele = $(this)
      var footer_td_eles = $footer_ele.find('td')
      $.each(footer_td_eles,function(){
        var $footer_td_ele = $(this)
        var text = $footer_td_ele.text().trim() || ""
        if ($footer_td_ele && $footer_td_ele[0].classList.contains('oe_number')){
          var text = parse_float(text);
          data.push({'data': text || "", 'bold': true, 'number': true})
        }
        else{
          data.push({'data': text, 'bold': true})
        }
      });
      export_data.push(data)
    });

    //Export to excel
    $.blockUI();
    if (export_type === 'excel'){
      session.get_file({
        url: '/web/export/mw_excel_export',
        data: {data: JSON.stringify({
              model : self.getParent().modelName,
              headers : header_name_list,
              rows : export_data,
        })},
        complete: $.unblockUI
      });
    } else {
      self._rpc({
        model: 'res.users',
        method: 'read',
        args: [session.uid, ["company_id"]]
      }).then(function(res) {
        self._rpc({
          model: 'res.company',
          method: 'read',
          args: [res[0]['company_id'][0], ["name"]]
        }).then(function(result) {
          session.get_file({
            url: '/web/export/mw_pdf_export',
            data: {data: JSON.stringify({
                  uid: session.uid,
                  model : self.getParent().modelName,
                  headers : header_name_list,
                  rows : export_data,
                  company_name: result[0].name
            })},
            complete: $.unblockUI
          });
        });
      });
    }
  }
});

});
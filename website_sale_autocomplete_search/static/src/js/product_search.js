odoo.define('website_sale_autocomplete_search.product_search', function (require) {
"use strict";

$(function() {

    $(".oe_search_box").autocomplete({
        source: function(request, response) {
            $.ajax({
            url: "/shop/search",
            method: "GET",
            dataType: "json",
            data: { keywords: request.term, category: false },
            success: function( data ) {               
                response( $.map( data, function( item ) {
                    return {
                        label: ((item.type === 'c'? 'Categoría: ': '') + item.name),
                        value: item.name,
                        id: item.id,
                    }
                }));
            },
            error: function (error) {
                console.error(error);               
            }
            });
        },
        select:function(suggestion, term, item){
            console.log('suggestion', suggestion, term, item);
            if (term.item.label.indexOf('Categoría:') === 0) {
                window.location.href='/shop/category/' + term.item.id;
            }
            else {
                window.location.href= "/shop/product/"+ term.item.id;
            }
        },
        minLength: 1
    });
});
});
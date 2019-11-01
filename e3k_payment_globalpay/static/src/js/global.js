
odoo.define('e3k_payment_globalpay.global', function(require) {
    "use strict";


    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;
    var qweb = core.qweb;
    ajax.loadXML('/e3k_payment_globalpay/static/src/xml/global_templates.xml', qweb);


    function display_global_form(provider_form) {

         var $modal = $(qweb.render('test.modal'));
         $modal.appendTo($('body')).modal({'keyboard': true});
    }

    $.getScript("https://api.sandbox.realexpayments.com/epage-remote.cgi", function() {

            display_global_form($('form[provider="globalpayment"]'));

    });




});

odoo.define('payment_checkout.checkout', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;
    var qweb = core.qweb;
    ajax.loadXML('/payment_checkout/static/src/xml/checkout_templates.xml', qweb);

    // The following currencies are integer only, see
    var int_currencies = [
        'BIF', 'XAF', 'XPF', 'CLP', 'KMF', 'DJF', 'GNF', 'JPY', 'MGA', 'PYG',
        'RWF', 'KRW', 'VUV', 'VND', 'XOF'
    ];

    if ($.blockUI) {
        // our message needs to appear above the modal dialog
        $.blockUI.defaults.baseZ = 2147483647; //same z-index as StripeCheckout
        $.blockUI.defaults.css.border = '0';
        $.blockUI.defaults.css["background-color"] = '';
        $.blockUI.defaults.overlayCSS["opacity"] = '0.9';
    }
    function getCheckoutHandler()
    {
        
    	console.log('######getCheckoutHandler : checkout_key #######', $("input[name='checkout_key']").val())
    	// Checkout.configure
    	var handler = Checkout.configure({
        	publicKey: $("input[name='checkout_key']").val(),
        	paymentToken: function(paymentToken, args) {
                handler.isTokenGenerate = true;
                
                ajax.jsonRpc("/payment/checkout/create_charge", 'call', {
                    tokenid: paymentToken.id,
                    email: token.email,
                    amount: $("input[name='amount']").val(),
                    acquirer_id: $("#acquirer_checkout").val(),
                    currency: $("input[name='currency']").val(),
                    invoice_num: $("input[name='invoice_num']").val(),
                    tx_ref: $("input[name='invoice_num']").val(),
                    return_url: $("input[name='return_url']").val()
                }).always(function(){
                    if ($.blockUI) {
                        $.unblockUI();
                    }
                }).done(function(data){
                    handler.isTokenGenerate = false;
                    window.location.href = data;
                }).fail(function(){
                    var msg = arguments && arguments[1] && arguments[1].data && arguments[1].data.arguments && arguments[1].data.arguments[0];
                    var wizard = $(qweb.render('checkout.error', {'msg': msg || _t('Payment error')}));
                    wizard.appendTo($('body')).modal({'keyboard': true});
                });
                console.log('######token #######',token)
            },
        });
    	
    	console.log('######handler #######',handler)
        return handler;
    }

    require('web.dom_ready');
    if (!$('.o_payment_form').length) {
        return $.Deferred().reject("DOM doesn't contain '.o_payment_form'");
    }

    var observer = new MutationObserver(function(mutations, observer) {
        for(var i=0; i<mutations.length; ++i) {
            for(var j=0; j<mutations[i].addedNodes.length; ++j) {
                if(mutations[i].addedNodes[j].tagName.toLowerCase() === "form" && mutations[i].addedNodes[j].getAttribute('provider') == 'checkout') {
                    display_checkout_form($(mutations[i].addedNodes[j]));
                }
            }
        }
    });


    function display_checkout_form(provider_form) {
        // Open Checkout with further options
    	
    	console.log('#######display_checkout_form########')
        var payment_form = $('.o_payment_form');
    	console.log('#######payment_form########',payment_form)
        if(!payment_form.find('i').length)
            payment_form.append('<i class="fa fa-spinner fa-spin"/>');
            payment_form.attr('disabled','disabled');

        var acquirer_id = payment_form.find('input[type="radio"][data-provider="checkout"]:checked').data('acquirer-id');
        if (! acquirer_id) {
            return false;
        }
    	console.log('#######acquirer_id########',acquirer_id)
        var access_token = $("input[name='access_token']").val() || $("input[name='token']").val();
        var so_id = $("input[name='return_url']").val().match(/quote\/([0-9]+)/) || undefined;
        console.log('#######so_id########',so_id)
        if (so_id) {
            so_id = parseInt(so_id[1]);
        }


        var currency = $("input[name='currency']").val();
        console.log('#######currency########',currency)
        var currency_id = $("input[name='currency_id']").val();
        console.log('#######currency_id########',currency_id)
        var amount = parseFloat($("input[name='amount']").val() || '0.0');
        
        console.log('#######amount########',amount)


        if ($('.o_website_payment').length !== 0) {
        	console.log('#######/website_payment/transaction#######')
            var create_tx = ajax.jsonRpc('/website_payment/transaction', 'call', {
                    reference: $("input[name='invoice_num']").val(),
                    value: amount,
                    currency_id: currency_id,
                    acquirer_id: acquirer_id
            });
        }
        else if ($('.o_website_quote').length !== 0) {
        	 console.log('#######/quote/%s/transaction//#######')
            var url = _.str.sprintf("/quote/%s/transaction/", so_id);
            console.log('#######url########',url)
            var create_tx = ajax.jsonRpc(url, 'call', {
                access_token: access_token,
                acquirer_id: acquirer_id
            }).then(function (data) {
                try { provider_form[0].innerHTML = data; } catch (e) {};
            });
        }
        else {
        	
            console.log('#######/shop/payment/transaction/#######')
            var create_tx = ajax.jsonRpc('/shop/payment/transaction/' + acquirer_id, 'call', {
                    so_id: so_id,
                    access_token: access_token,
                    acquirer_id: acquirer_id
            }).then(function (data) {
                try { provider_form.innerHTML = data; } catch (e) {};
            });
            
            console.log('#######create_tx#######',create_tx)
        }
        create_tx.done(function () {
            if (!_.contains(int_currencies, currency)) {
                amount = amount*100;
            }
            console.log('######create_tx done#######')
            getCheckoutHandler().open();
            
            console.log('#######create_tx 2 #######')
            
        });
    }
	// https://cdn.checkout.com/sandbox/js/checkout.js
    $.getScript("https://cdn.checkout.com/sandbox/js/checkout.js", function(data, textStatus, jqxhr) {
        observer.observe(document.body, {childList: true});
        display_checkout_form($('form[provider="checkout"]'));
    });
});

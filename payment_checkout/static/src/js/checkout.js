odoo.define('payment_checkout.checkout', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;
    var qweb = core.qweb;
    ajax.loadXML('/payment_checkout/static/src/xml/checkout_templates.xml', qweb);

    if ($.blockUI) {
        // our message needs to appear above the modal dialog
    	console.log("blockUI",$.blockUI)
        $.blockUI.defaults.css.border = '0';
        $.blockUI.defaults.css["background-color"] = '';
        $.blockUI.defaults.overlayCSS["opacity"] = '0.9';
    }
    function getCheckoutHandler()
    {   
    	
    	 // Charge with Card Token
    	 // Send card details through Checkout.js.
    	Checkout.configure({
            publicKey: $("input[name='checkout_key']").val(),// Your public key obtained from The Hub.
            customerEmail:$("input[name='email']").val(), // Customer e-mail address.
            value: $("input[name='amount']").val(),// Value of the charge. Must be a non-zero positive integer (i.e. decimal figures not allowed). 
            currency: $("input[name='currency']").val(), //Transaction currency.
            customerName:  $("input[name='customerName']").val(),
	        paymentMode: 'cards',
	        cardFormMode: 'cardTokenisation', // Set to Checkout.CardFormModes.CARD_TOKENISATION to charge with card token.
	        appMode:'lightbox',
	        renderMode: 5,
	        title :$("input[name='name']").val(),
	        subtitle : $("input[name='invoice_num']").val(),
	        billingDetails: {
                'addressLine1': $("input[name='address_line1']").val(),
                'postcode': $("input[name='address_zip']").val(),
                'city': $("input[name='address_city']").val(),
                'phone': {'number': $("input[name='phone']").val()}
                },
            cardTokenised: function(event) {
                console.log(event.data.cardToken); // Return single-use card token.
                console.log(event.data);
                if ($.blockUI) {
                    var msg = _t("Just one more second, confirming your payment...");
                    $.blockUI({
                        'message': '<h2 class="text-white"><img src="/web/static/src/img/spin.png" class="fa-pulse"/>' +
                                '    <br />' + msg +
                                '</h2>'
                    });
                }
                // Send card token to merchant backend server
                ajax.jsonRpc("/payment/checkout/create_charge", 'call', {
                	cardToken:event.data.cardToken,
                	value : $("input[name='amount']").val(),
                	email:$("input[name='email']").val(),
                	currency:$("input[name='currency']").val(),
                    acquirer_id: $("#acquirer_checkout").val(),
                    currency: $("input[name='currency']").val(),
                    invoice_num: $("input[name='invoice_num']").val(),
                    tx_ref: $("input[name='invoice_num']").val(),
                    return_url: $("input[name='return_url']").val(),
                   
                }).always(function(){
                    if ($.blockUI) {
                        $.unblockUI();
                    }
                }).done(function(data){
                	window.location.href = data;
                }).fail(function(){
                    var msg = arguments && arguments[1] && arguments[1].data && arguments[1].data.arguments && arguments[1].data.arguments[0];
                    var wizard = $(qweb.render('checkout.error', {'msg': msg || _t('Payment error')}));
                    wizard.appendTo($('body')).modal({'keyboard': true});
                });

            },
        });
    	
    	Checkout.open();// to trigger the payment lightbox to open.
    
    }


    require('web.dom_ready');
    if (!$('.o_payment_form').length) {
        return $.Deferred().reject("DOM doesn't contain '.o_payment_form'");
    	console.log('#####o_payment_form#######')
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
    	
        var payment_form = $('.o_payment_form');
        if(!payment_form.find('i').length)
            payment_form.append('<i class="fa fa-spinner fa-spin"/>');
            payment_form.attr('disabled','disabled');

        var acquirer_id = payment_form.find('input[type="radio"][data-provider="checkout"]:checked').data('acquirer-id');
        if (! acquirer_id) {
            return false;
        }
        
        // access_token
        var access_token = $("input[name='access_token']").val() || $("input[name='token']").val();
       
        var so_id = $("input[name='return_url']").val().match(/quote\/([0-9]+)/) || undefined;
        if (so_id) {
            so_id = parseInt(so_id[1]);
        }
        
        //
        var currency = $("input[name='currency']").val();
        var currency_id = $("input[name='currency_id']").val();
        var amount = parseFloat($("input[name='amount']").val() || '0.0');
        
        if ($('.o_website_payment').length !== 0) {
        	
            var create_tx = ajax.jsonRpc('/website_payment/transaction', 'call', {
                    reference: $("input[name='invoice_num']").val(),
                    amount: amount, // exact amount, not stripe cents
                    currency_id: currency_id,
                    acquirer_id: acquirer_id
            });
        }
        else if ($('.o_website_quote').length !== 0) {
            var url = _.str.sprintf("/quote/%s/transaction/", so_id);
            var create_tx = ajax.jsonRpc(url, 'call', {
                access_token: access_token,
                acquirer_id: acquirer_id
            }).then(function (data) {
                try { provider_form[0].innerHTML = data; } catch (e) {};
            });
        }
        else {
            var create_tx = ajax.jsonRpc('/shop/payment/transaction/' + acquirer_id, 'call', {
                    so_id: so_id,
                    access_token: access_token,
                    acquirer_id: acquirer_id
            }).then(function (data) {
                try { provider_form.innerHTML = data; } catch (e) {};
            });
        }
        create_tx.done(function () {
        	
        	 getCheckoutHandler(); // call method 
        });
    }
    
    $.getScript("https://cdn.checkout.com/sandbox/js/checkout.js", function(data, textStatus, jqxhr) {
        observer.observe(document.body, {childList: true});
        display_checkout_form($('form[provider="checkout"]'));
    });
});

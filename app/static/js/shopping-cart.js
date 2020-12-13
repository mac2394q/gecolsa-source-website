/*jshint strict:true, browser:true, jquery:true */

function calculate_cart_total_price() {
    'use strict';

    var cart_total_price = 0;

    $('.js-product-price').each(function() {
        cart_total_price += parseInt($(this).data('value'), 10);
    });

    $('#id_cart_subtotal_price').text(formatNumber(cart_total_price, '',',','','$ ',' COP','-',''));
    $('#id_cart_subtotal_price').data('value', cart_total_price);
}


$(function() {
    'use strict';

    // Validate form fields.
    $('.js-confirm-purchase').validate({
        rules: {
            shipping_name: 'required',
            shipping_address: 'required',
            shipping_mobile_number: 'required',
            customer_email: 'required',
            customer_doc_type: 'required',
            customer_docid: {
                required: true,
                digits: true,
                minlength: 3,
                maxlength: 15
            },
            accept_terms: 'required'
        }
    });

    // Different billing address.
    var differentBillingAddress = false;

    // Is rate calculated?
    var rateCalculated = false;
    var citySelected = false;
    $(document).on('rate.calculated', function() {
        rateCalculated = true;
    });

    // Listen for choice removal.
    $(document).on('click', '.hilight .remove', function() {

        // Deactivate button
        $('.shipping-data .js-rate-shipping').attr('disabled', 'disabled');
        $('.js-pay-purchase').attr('disabled', 'disabled');
        if (typeof $('#id_city-shipping_city-deck').find('span').data('value') === 'undefined') {
            rateCalculated = false;
        }
        if (typeof $('#id_customer_city-deck').find('span').data('value') === 'undefined') {
            citySelected = false;
            customerCitySelected = false;
        }
        $('#id_cart_tax_price').html('--');
        $('#id_cart_shipping_price').html('--');
        $('#id_cart_total_price').html('--');
        if ($('#id_accept_terms').prop('checked')) {
            $('.js-pay-purchase').attr('disabled', 'disabled');
        }
    });

    // Make sure user picks a city when they select another billing address.
    var customerCitySelected = false;
    $('.customer_city').bind('selectChoice', function(e, choice, autocomplete) {
        customerCitySelected = true;
        if ($('#id_accept_terms').is(':checked') && rateCalculated && ((!differentBillingAddress) || (differentBillingAddress && customerCitySelected)) ) {
            $('.js-pay-purchase').removeAttr('disabled');
        } else {
            $('.js-pay-purchase').attr('disabled', 'disabled');
        }
    });

    // Diferent invoice address.
    $('#id_different_data').change(function() {
        if ( $(this).is(':checked') ) {
            differentBillingAddress = true;
            $('#id_customer_docid').val("");
        } else {
            differentBillingAddress = false;
        }

    });

    // Enable `Comprar` button when user accepts terms.
    $('#id_accept_terms').on("change", function() {
        if ($(this).is(':checked') && rateCalculated && ((!differentBillingAddress) || (differentBillingAddress && customerCitySelected)) ) {
            $('.js-pay-purchase').removeAttr('disabled');
        } else {
            $('.js-pay-purchase').attr('disabled', 'disabled');
        }
    });

    if($('.shopping-cart, .sell-confirmation, .shipping-data').length === 0) {
        return;
    }

    $.cookie.json = true;

    if ($('.shopping-cart').length > 0) {
        calculate_cart_total_price();
    }

    $('.js-cart-item-delete').on('click', function() {
        var cart_item = $(this).closest('.js-cart-item');

        Swal({
            title: '¿Está seguro que quiere borrar el producto?',
            type: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí',
            cancelButtonText: 'No',
            closeOnConfirm: false
        }, function() {
            var reference = $(cart_item).data('reference');
            var size_to_delete = $(cart_item).data('size-id');
            var j = 0;
            var products = $.cookie('products');
            for(var i = products.length - 1; i >= 0 ; i--) {
                if(products[i].reference === reference) {
                    for (j = 0; j < products[i].product_stock.length; j++) {
                        if (products[i].product_stock[j].size_id === size_to_delete){
                            products[i].product_stock.splice(j, 1);
                        }
                    }
                    if (products[i].product_stock.length === 0 || products[i].product_stock[0].size_id === null)
                        products.splice(i, 1);
                }
            }
            $.cookie('products', products, { path: '/' });
            $(cart_item).remove();

            calculate_cart_total_price();
            if ($('.js-cart-item').length === 0 ) {
                $('.js-hide-shipping-button').hide();
                $('.section-title').parent().append('<p class="no-items-in-cart text-center">No hay artículos en tu carrito de compras</p>');
            }

            Swal('El producto ha sido borrado exitosamente.', '', 'success');
        });
    });

    $('.shipping-data').on('change', '#id_different_data', function() {
        if( $(this).is(':checked')) {
            $('#other_information').show();
            $('#div_id_customer_doc_type').appendTo('#other_information');
            $('#div_id_customer_docid').appendTo('#other_information');
        } else {
            $('#div_id_customer_doc_type').appendTo('#shipping_information');
            $('#div_id_customer_docid').appendTo('#shipping_information');
            $('#other_information').hide();
        }
    });

    var citySearch = new Bloodhound({
      datumTokenizer: Bloodhound.tokenizers.obj.whitespace('full_name'),
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      prefetch: '../../city-search/',
      remote: {
        url: '../../city-search/',
        wildcard: '%QUERY'
      }
    });
    $('#id_city-autocomplete').typeahead({
        hint: true,
        highlight: true,
        minLength: 2
    }, {
      name: 'full_name',
      display: 'full_name',
      source: citySearch
    }).on('keypress', function (event) {
        if (event.which === 13) {
            return false;
        }
    }).on('typeahead:autocompleted typeahead:selected', function (event, object) {
        $('#id_city-shipping_city').val(object.id);
        $('.shipping-data .js-rate-shipping').removeAttr('disabled');
        citySelected = true;
    });

    $('#id_autocomplete').typeahead({
        hint: true,
        highlight: true,
        minLength: 2
    }, {
      name: 'full_name',
      display: 'full_name',
      source: citySearch
    }).on('keypress', function (event) {
        if (event.which === 13) {
            return false;
        }
    }).on('typeahead:autocompleted typeahead:selected', function (event, object) {
        $('#id_city-autocomplete').val(object.full_name);
        $('#id_city-shipping_city').val(object.id);
        $('.shipping-data .js-rate-shipping').removeAttr('disabled');
        citySelected = true;
    });

    $('.shipping-data').on('submit', '.rate-request', function() {
        if ($('#id_city-shipping_city').val() === null) {
            Swal('Por favor elija la ciudad');
            return false;
        }
        // Show loading animation.
        Swal({
            title: 'Un momento!',
            text: 'Estamos procesando tu solicitud.',
            imageUrl: '/static/img/spinner.gif',
            showConfirmButton: false,
            allowOutsideClick: true
        });

        $.post($(this).attr('action'), $(this).serialize(), function(result) {
            Swal.close();
            var total = parseInt($('#id_cart_subtotal_price').data('value'), 10);
            if (result.error !== '') {
                Swal(result.error);
            } else {
                $('#id_cart_shipping_price').html(formatNumber(result.shipping, '',',','','$ ',' COP','-',''));
                $('#id_cart_shipping_price').data('value', result.shipping);
                $('#id_cart_tax_price').html(formatNumber(result.taxes, '',',','','$ ',' COP','-',''));
                $('#id_cart_tax_price').data('value', result.taxes);
                total += result.shipping + result.taxes ;
                $('#id_cart_total_price').html(formatNumber(total, '',',','','$ ',' COP','-',''));
                $('#id_cart_total_price').data('value', total);

                // Trigger a global event so that we can tell
                // that the rate was caclculated.
                $(document).trigger('rate.calculated');
                if ($('#id_accept_terms').prop('checked')) {
                    $('.js-pay-purchase').removeAttr('disabled');
                }
            }
        });
        return false;

    });

    $('.shipping-data').on('submit', '.confirm-buy', function() {
        Swal({
            title: 'Un momento!',
            text: 'Estamos procesando tu solicitud.',
            imageUrl: '/static/img/spinner.gif',
            showConfirmButton: false,
            allowOutsideClick: true
        });
        $.post($(this).attr('action'), $(this).serialize(), function(result) {
            if (result.error !== '') {
                Swal(result.error);
            } else {
                // Fill the required fields
                $('#usuarioId').val(result.usuarioId);
                $('#descripcion').val(result.descripcion);
                $('#refVenta').val(result.refVenta);
                $('#valor').val(result.valor);
                $('#iva').val(result.iva);
                $('#baseDevolucionIva').val(result.baseDevolucionIva);
                $('#moneda').val(result.moneda);
                $('#firma').val(result.firma);
                $('#emailComprador').val(result.emailComprador);
                $('#extra1').val(result.extra1);
                $('#extra2').val(result.extra2);
                $('#prueba').val(result.prueba);
                $('#lng').val(result.lng);
                $('#nombreComprador').val(result.nombreComprador);
                $('#url_respuesta').val(result.url_respuesta);
                $('#url_confirmacion').val(result.url_confirmacion);
                $('#telefonoMovil').val(result.telefonoMovil);
                $('#documentoIdentificacion').val(result.documentoIdentificacion);

                $('.payu-form').attr('action', result.payu_url);

                $('.payu-form').submit();
            }
        });
        return false;
    });

    // Confirmation print button.
    $('.js-confirmation-print').click(function(e) {
        e.preventDefault();
        window.print();
    });

    // Add items count.
    $.cookie.json = true;
    var products = $.cookie('products');
    var products_count = 0;
    if (products) {
        products_count = products.length;
    }

    $('#shopping_cart_count').text(products_count);
});


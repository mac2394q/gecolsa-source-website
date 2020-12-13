/*jshint strict:true, browser:true, jquery:true */

$(function() {
    'use strict';

    if($('.js-carousel').length) {
        $('.js-carousel').slick({
            infinite: true,
            slidesToShow: 1,
            arrows: true,
            cssEase:'linear',
            autoplay: true,
            autoplaySpeed: 4000,
            dots: true,
            prevArrow: '<div class="banner-prev carousel-control left"><svg class="icon"><use xlink:href="/static/svg/icons.svg#arrow"></use></svg></div>',
            nextArrow: '<div class="banner-next carousel-control right"><svg class="icon"><use xlink:href="/static/svg/icons.svg#arrow"></use></svg></div>'
        });
    }


    if($('.product-detail').length === 0) {
        return;
    }

    var has_quantity_without_size = $('.js-size-quantities[data-size-id=""]').length;
    if (has_quantity_without_size) {
        var quantity = Math.min(parseInt($('.js-size-quantities[data-size-id=""]').data('quantity'), 10), 50);
        for (var z = 1; z <= quantity; z++) {
            $('#id_quantity').append($('<option></option>').attr('value', z).text(z));
        }
    }
    if (has_quantity_without_size !== undefined && has_quantity_without_size > 0 && $('#product_reference').length > 0){
        var ref = $('#product_reference').data('reference');
        $.cookie.json = true;
        var products = $.cookie('products');
        if (products !== undefined){
            $.each(products, function(k, product) {
                if (product.reference == ref) {
                    $('.product-detail select').val(product.product_stock[0].quantity).selectpicker('refresh');
                }
            });
        }
    }

    //
    // Get quantity by reference and size.
    //
    // Usage:
    //
    //      getQuantityByRefAndSize('five', 1);
    //      => number of products in cart of ref `five` and size id `1`.
    //
    var getQuantityByRefAndSize = function(ref, sizeId) {
        $.cookie.json = true;
        var products, quantity;
        products = $.cookie('products');
        quantity = null;
        if (products === undefined){
            return quantity;
        }
        // Cicle through products.
        $.each(products, function(k, product) {

            if (product.reference == ref) {
                $.each(product.product_stock, function(k, stock) {
                    if (stock.size_id == sizeId) {
                        quantity = stock.quantity;
                        return false;
                    }
                });
            }
        });

        // Return found quantity.
        return quantity;
    };

    // When the product has no sizes, if we have it in cart,
    // make sure to autoselect the quantity.
    var productInfo = $('.product-info');
    if ( productInfo.data('has-sizes') === false ) {
        var the_ref = productInfo.data('reference');
        var number = getQuantityByRefAndSize(the_ref, null);
        $('#id_quantity').val(number);
    }

    // Size change.
    $('#id_size').on('change', function() {
        var selected_size = $(this).val();
        var selected_quantity = $('#id_quantity option[value!=""]:selected').val();
        var reference = $('#product_reference').data('reference');
        var quantity;
        $('#id_quantity option[value!=""]').remove();
        if (selected_size || has_quantity_without_size) {
            selected_size = Math.min(parseInt($('.js-size-quantities[data-size-id="' + selected_size + '"]').data('quantity'), 10), 50);
            for (var i = 1; i <= selected_size; i++)
                $('#id_quantity').append($('<option></option>').attr('value', i).text(i));

            quantity = getQuantityByRefAndSize(reference, $(this).val());
            // When I select a size, the item I have in card should be the one.
            if (selected_quantity && selected_size && quantity)
                $("#id_quantity").val(Math.min(selected_size, selected_quantity));

            // Get count by id and size.

            // Select quantity.
            if (quantity !== null) {
                $("#id_quantity").val(quantity);
                var newPrice = $('#product_total_price').data('item-price');
                var newPriceWithDiscount = $('#product_total_price').data('item-price-with-discount');

                if ($('#id_quantity').val()) {
                    newPrice = newPrice * $('#id_quantity').val();
                    newPriceWithDiscount = newPriceWithDiscount * $('#id_quantity').val();
                }

                $('#product_total_price').text(formatNumber(newPrice, '', ',', '', '$ ',' COP', '-', ''));
                $('.discounted-price span').text(formatNumber(newPriceWithDiscount, '', ',', '', '$ ',' COP', '-', ''));
            }
        }

        // Update bootstrap select.
        $('.product-detail select').selectpicker('refresh');
    });

    $('#id_quantity').on('change', function() {
        var newPrice;
        var newPriceWithDiscount;
        newPrice = $('#product_total_price').data('item-price');
        newPriceWithDiscount = $('#product_total_price').data('item-price-with-discount');
        if ($('#id_quantity').val()) {
            newPrice = newPrice * $('#id_quantity').val();
            newPriceWithDiscount = newPriceWithDiscount * $('#id_quantity').val();
        }

        $('#product_total_price').text(formatNumber(newPrice, '', ',', '', '$ ',' COP', '-', ''));
        $('.discounted-price span').text(formatNumber(newPriceWithDiscount, '', ',', '', '$ ',' COP', '-', ''));

        // Update bootstrap select.
        $('.product-detail select').selectpicker('refresh');
    });

    $('#id_buy_product_form').on('submit', function(e) {
        e.preventDefault();

        $.cookie.json = true;

        var products = $.cookie('products');
        if (!products) {
            products = [];
        }
        var selected_size = $('#id_size').val();
        if (selected_size) {
            selected_size = parseInt(selected_size, 10);
        } else {
            selected_size = null;
        }
        var reference = $('#product_reference').data('reference');
        var quantity = parseInt($('#id_quantity').val(), 10);
        var products_count = 0;

        if (isNaN(quantity) || quantity === 0) {
            return Swal('Debes seleccionar una cantidad.', '', 'error');
        }

        var product_in_cart = false;
        for (var i = 0; i < products.length; i++) {
            if (products[i].reference == reference) {
                var product = products[i];
                var product_stock = product.product_stock;
                var in_stock = false;
                for(var j = 0; j < product_stock.length; j++) {
                    if (product_stock[j].size_id == selected_size) {
                        in_stock = true;
                        product_stock[j].quantity = quantity;
                        break;
                    }
                }
                if (!in_stock) {
                    product_stock.push({
                        'quantity': quantity,
                        'size_id': selected_size
                    });
                }
                product.product_stock = product_stock;
                products[i] = product;
                product_in_cart = true;
            }
        }
        if (!product_in_cart) {
            products.push({
                'reference': reference,
                'product_stock': [{
                    'quantity': quantity,
                    'size_id': selected_size
                }]
            });
        }
        $.cookie('products', products, { path: '/' });

        if (products.length >= 0) {
            products_count = products.length;
        } else {
            products_count = 0;
        }

        $('#shopping_cart_count').text(products_count);

        $('#id_size').val('');
        $('#id_quantity').val('');
        $('.product-detail select').selectpicker('refresh');

        Swal('El producto ha sido agregado exitosamente.', '', 'success');
    }).validate({
        rules: {
            'quantity': {
                required: true
            }
        },
        messages: {
            quantity: {
                required: 'Por favor, elija la cantidad.'
            }
        }
    });

    // Trigger click on add tu cart button.
    $('.js-add-to-cart-trigger').click(function(e) {
        e.preventDefault();
        $('.buy-product-form').submit();
    });

    if ($('#id_size option').length === 1)
        $('#id_size').trigger('change');

});

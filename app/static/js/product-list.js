/*jshint strict:true, browser:true, jquery:true */

$(function() {
    'use strict';

    // Submit form on change.
    $('.js-product-list-filter').change(function() {
        $(this).submit();
    });

    // Zoom.
    $('.js-equipment-zoom').click(function(e) {
        var currentSlide = $('.js-carousel').slick('slickCurrentSlide');
        e.preventDefault();
        $('.full-size-image').eq(currentSlide).click();
    });

    $('.js-equipment-used-zoom').click(function(e) {
        var equipment = $(this).data('equipment');
        e.preventDefault();
        $('.equipment-'+equipment).eq(0).click();
    });
});

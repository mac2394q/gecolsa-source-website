(function($) {
    'use strict';

    $('.js-carousel').slick({
        infinite: true,
        arrows: true,
        cssEase:'linear',
        slidesToShow: 1,
        slidesToScroll: 1,
        dots: true,
        prevArrow: '<div class="banner-prev carousel-control left"><svg class="icon"><use xlink:href="/static/svg/icons.svg#arrow"></use></svg></div>',
        nextArrow: '<div class="banner-next carousel-control right"><svg class="icon"><use xlink:href="/static/svg/icons.svg#arrow"></use></svg></div>'
    });

    $('.js-zoom').click(function(e) {
        e.preventDefault();
        var currentSlide = $('.js-carousel').slick('slickCurrentSlide');
        $('.full-size-image').eq(currentSlide).click();
    });

    if ($('div.lazy').length > 0 ) {
        $('div.lazy').lazyload({effect : 'fadeIn'});
    }
})(jQuery);

(function($) {
    'use strict';

    $('.slider').slick({
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

})(jQuery);

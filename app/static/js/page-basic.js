(function($) {
    'use strict';

    $('.js-carousel').slick({
        infinite: true,
        slidesToShow: 1,
        arrows:true,
        cssEase:'linear',
        dots: true,
        prevArrow: '<div class="banner-prev carousel-control left"><svg class="icon"><use xlink:href="/static/svg/icons.svg#arrow"></use></svg></div>',
        nextArrow: '<div class="banner-next carousel-control right"><svg class="icon"><use xlink:href="/static/svg/icons.svg#arrow"></use></svg></div>'
    });

    // Zoom.
    $('.js-zoom').click(function(e) {
        e.preventDefault();
        var currentSlide = $('.js-carousel').slick('slickCurrentSlide');
        $('.full-size-image').eq(currentSlide).click();
    });

    $('.gp-page-detail a').on('click', function() {
        if ($(this).attr('href') === 'https://gecolsa.cat.com/DSFUnbundled/instantAccess.do') {
            ga('send', 'event', 'partstore', 'click');
        }
    });

    if ($('img.lazy').length > 0 ) {
        $('img.lazy').lazyload({effect : 'fadeIn'});
    }
})(jQuery);

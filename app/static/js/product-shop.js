(function($) {
    'use strict';
    if($('.js-shop-carousel').length > 0) {
        var item = 5;
        if ($('.product-carousel').width() < 368) {
            item = 3;
        }

        var slider = create_carrousel(item);

        $(window).on('resize', function () {
            var new_item = 5;
            if ($('.product-carousel').width() < 368) {
                new_item = 3;
            }
            if (item != new_item) {
                item = new_item;
                slider.destroy();
                slider = create_carrousel(item);
            }
        });
    }
})(jQuery);

function create_carrousel(item) {
    return $('.js-shop-carousel').lightSlider({
        gallery:true,
        item:1,
        loop:false,
        thumbItem:item,
        slideMargin:0,
        enableDrag: true,
        currentPagerPosition:'middle',
        prevHtml: '<div class="banner-prev carousel-control left"><svg class="icon"><use xlink:href="/static/svg/icons.svg#arrow"></use></svg></div>',
        nextHtml: '<div class="banner-next carousel-control right"><svg class="icon"><use xlink:href="/static/svg/icons.svg#arrow"></use></svg></div>',
        onSliderLoad: function(el) {
            el.lightGallery({
                selector: '.js-shop-carousel .lslide',
                download: false
            });
        }
    });
}

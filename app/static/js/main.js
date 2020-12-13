/*jshint strict:true, browser:true, jquery:true */

// Check whether we're in a mobile browser.
var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

// Django CSRF Handling
function csrfSafeMethod(method) {
    'use strict';
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Calculate padding of second and third level menu
function paddingMenu() {
    'use strict';
    var paddingDis = ($(window).width()-1200)/2;
    if(paddingDis>0) {
        $('.navbar-nav .dropdown-menu').css('padding', '0px '+paddingDis+'px');
    } else {
        $('.navbar-nav .dropdown-menu').css('padding', '0px');
    }
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        'use strict';
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});

$(function() {
    'use strict';
    var match = false;

    // First level equal
    $('.nav > li > a').each(function () {
        var href = $(this).attr('href');
        if ( href && document.location.pathname === (href)) {
            $(this).parents('li').addClass('active');
            match = true;
            return false;
        }
    });

    // First level
    $('.nav > li > a').each(function () {
        if (match) { return false; }
        var href = $(this).attr('href');
        if ( href && document.location.pathname.indexOf(href) === 0) {
            $(this).parents('li').addClass('active');
            match = true;
            return false;
        }
    });

    // Second level
    $('.nav > .dropdown > .dropdown-menu > li > a').each(function () {
        if (match) { return false; }
        var href = $(this).attr('href');
        if ( href && document.location.pathname.indexOf(href) === 0) {
            $(this).parents('.dropdown-menu').parents('.dropdown').addClass('active');
            match = true;
            return false;
        }
    });

    // Third level.
    $('.nav > .dropdown > .dropdown-menu .dropdown li a').each(function () {
        var href = $(this).attr('href');
        if (href && document.location.pathname.indexOf(href) === 0) {
            $(this).closest('.dropdown').find('> .dropdown-toggle').closest('.dropdown-menu').parent().addClass('active').find('> .dropdown-toggle');

            return false;
        }
    });

    $('.js-back-btn').on('click', function() {
        window.history.back();
    });

    paddingMenu();
    $(window).resize(function() {
        paddingMenu();
    });

    // Greather than 992px.
    if (! isMobile) {
        // Change menu background image
        $('.navbar-nav >li.dropdown').on('mouseenter', function() {
            $(this).addClass('open');
        });

        $('.navbar-nav >li.dropdown').on('mouseleave', function() {
            $(this).removeClass('open');
        });

        // Bootstrap 3 Triple Nested Sub-Menus
        $('ul.dropdown-menu .dropdown').on('mouseenter mouseleave', function() {
            $(this).toggleClass('open');
        });

        $('.navbar-nav >li.dropdown .dropdown-toggle').on('click', function(e) {
            var href = $(this).attr('href');
            e.preventDefault();
            e.stopPropagation();

            if ( $.inArray(href, ['#', '']) < 0 ) {
                return window.location.href = href;
            }
            return false;
        });

        // Prevent Bootstrap to keep buttons active.
        $('.navbar-nav >li.dropdown .dropdown-toggle').on('mouseup', function(e) {
            $(this).blur();
        });

    } else {

        // Bootstrap 3 Triple Nested Sub-Menus
        $('ul.dropdown-menu [data-toggle=dropdown]').unbind('mouseenter').unbind('mouseleave').on('click', function(event) {
            event.preventDefault();
            event.stopPropagation();

            // Close other open menus
            if (!$(this).parent().hasClass('open')) {
                $(this).closest('ul').find('.open').removeClass('open');
            }

            // Re-add .open to parent sub-menu item
            $(this).parent().toggleClass('open');
            $(this).parent().find('ul').parent().find('li.dropdown').toggleClass('open');
        });
    }

    // Toggle search input.
    $('.js-toggle-search').click(function() {
        $('.search-form').slideToggle(200).find('input').focus();
    });

    $('.search-form .hide-search').click(function() {
        $('.search-form').slideUp(200);
    });

    // History page custom markup.
    if ($('.page-detail').length > 0) {
        $('.year-box').parents('.gp-page-item').addClass('with-year');
    }

    if ($('.js-current-slug').length > 0) {
        $('.js-current-slug').each(function () {
            var element = $('[data-active-slug="' + $(this).data('current-slug') + '"]');
            $(element).addClass('active').closest('ul').show().closest('li').addClass('active');
            $(element).find('ul').show();
        });
    }

    // Go to top.
    $('.js-go-to-top').click(function(e) {
        e.preventDefault();

        $('html,body').animate({
          scrollTop: 0
        }, 1000);

    });

    // Notification  messages.
    if ($('.messages-list').length > 0) {
        var message = $('.messages-list .message').html();
        Swal(message);
    }

    // City selector on sidebar.
    $('.sidebar-box #id_city').on('change', function() {
        $(this).closest('form').submit();
    });

    // Offices list selectpicker.
    if ($('.office-list .city-selector select').length > 0) {
        $('.office-list .city-selector select').selectpicker();
    }

    // Contact form selectpicker.
    if ($('.contact-form select').length > 0) {
        $('.contact-form select').selectpicker();
    }

    if ($('.used-category').length > 0) {
        $('.used-category form select').selectpicker();

        // Handle z-index issue.
        $('.bootstrap-select').click(function(e) {
            if ( $(this).hasClass('open') ) {
                $(this).parent('.controls').css('z-index', 1);
            } else {
                $(this).parent('.controls').css('z-index', 2);
            }
        });

    }

    // Equipment detail selectpicker.
    if ($('.equipment-detail select').length > 0) {
        $('.equipment-detail select').selectpicker();
    }

    // Shipping-data data selectpicker.
    if ($('.shipping-data select').length > 0) {
        $('.shipping-data select').selectpicker();
    }

    // Responsive table
    $('.table-responsive table').addClass('table');

    // Zoom.
    $('.js-equipment-zoom').click(function(e) {
        e.preventDefault();
        $('.full-size-image').eq(0).click();
    });
    if ($('#lightbox').length > 0) {
        $('.lb-outerContainer').insertAfter('.lb-dataContainer');
    }

    $('.js-chat-popup').on('click', function () {
        window.open($(this).attr('href'), "chatrequest", "width=425,height=455,left=0,resizable=yes,scrollbars=no,location=no");
        return false;
    });

    // Sweet alert configuration.
    Swal.mixin({
        confirmButtonColor: '#FDBF00'
    });

    svg4everybody({
        polyfill: true
    });
});


// Window load.
$(function() {
    'use strict';

    // Product detail selectpicker.
    if ($('.product-detail select').length > 0) {
        $('.product-detail select').selectpicker();
    }

    // Product detail selectpicker.
    if ($('.product-list .js-product-list-filter select').length > 0) {
        $('.product-list .js-product-list-filter select').selectpicker();
    }

});


$('.js-contact-form input#id_full_path').val(document.URL);

var contact_by = [];

$('.breadcrumb li').each(function() {
    contact_by += $(this).text() + ' - ';
});

contact_by += $('.js-product-detail h4').text();

$('.js-contact-form input#id_contact_by').val(contact_by);

$('.js-contact-form').on('submit', function(event) {
    $.each($('.form-error'), function() {
        $(this).remove();
    });
    $('.send_yellow_button').attr('disabled', true);

    var that = this;
    $.post(
        $(that).attr('action'),
        $(that).serialize(),
        function(response) {
            if (response.ok) {
                Swal(response.message);
                that.reset();
                $('.send_yellow_button').attr('disabled', false);
            } else {
                $.each(response.message, function( key, value ) {
                    let hash = '.'+ key;
                    $(that).find(hash).after('<p class="form-error">'+ value +'</p>');
                });
            }
            $('.send_yellow_button').attr('disabled', false);
        }, 'json')
        .fail(function() {
            $('.send_yellow_button').attr('disabled', false);
            Swal('Hubo un error en el envío del formulario');
        })
    return false;

});
//
// Utilities
//
(function(window) {
    'use strict';

    // Utility function.
    //
    // Taken from http://javascript.about.com/library/blnumfmt.htm
    // Formats a number to be shown with separators.
    //
    // Usage:
    //
    //      formatNumber(18555848, '', ',', '', '$ ',' COP', '-', '');
    //      => $ 18,555,848 COP
    //
    window.formatNumber = function(num, dec, thou, pnt, curr1, curr2, n1, n2) {
        var x = Math.round(num * Math.pow(10,dec));
        if (x >= 0) { n1=n2=''; }
        var y = (''+Math.abs(x)).split('');
        var z = y.length - dec;
        if (z<0) { z--; }
        for(var i = z; i < 0; i++) { y.unshift('0'); }
        if (z<0) { z = 1; }
        y.splice(z, 0, pnt);
        if(y[0] == pnt) { y.unshift('0'); }
        while (z > 3) { z-=3; y.splice(z,0,thou); }
        var r = curr1+n1+y.join('')+n2+curr2;
        return r;
    };

})(this);

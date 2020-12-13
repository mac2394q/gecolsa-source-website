function toggleElement(element, value1, value2) {
    if (value1 == value2) {
        element.slideDown(300);
    } else {
        element.slideUp(300);
    }
}

$(function () {
    if ($('.js-type-complaint:checked').val()) {
        toggleElement($('.js-not-anonymous'), $('.js-type-complaint:checked').val(), window.not_anonymous_option);
    }

    $('.js-type-complaint').on('change', function () {
        toggleElement($('.js-not-anonymous'), $(this).val(), window.not_anonymous_option);
        if($(this).val() != window.not_anonymous_option) {
            $('.js-not-anonymous').find('input').val('')
        }
    });

    $('.js-company-relation').on('change', function () {
        toggleElement($('.js-other-option'), $(this).val(), window.other_choice);
    });

    $('input[type=file]').on('change', function (event) {
        var fileName = 'Subir archivo...';
        var labelInput = $('label[for="' + $(this).attr('id') + '"].js-input-file-text');
        if (event.target.value) {
            fileName = event.target.value.split('\\').pop();
        }
        labelInput.html(fileName);
        $(this).blur();
    });

    $.validator.addMethod('filesize', function (value, element, param) {
        return this.optional(element) || (element.files[0].size <= param);
    }, 'El tamaño del archivo debe ser menor que 2 mb');

    $('.js-request-complaint-form').validate({
        rules: {
            type_complaint: {
                required: true,
            },
            full_name: {
                required: {
                    depends: function () {
                        return $('.js-type-complaint:checked').val() == window.not_anonymous_option
                    }
                }
            },
            email: {
                required: {
                    depends: function () {
                        return $('.js-type-complaint:checked').val() == window.not_anonymous_option
                    }
                }
            },
            phone_number: {
                required: {
                    depends: function () {
                        return $('.js-type-complaint:checked').val() == window.not_anonymous_option
                    }
                }
            },
            company_relation: {
                required: true,
            },
            other_relation: {
                required: {
                    depends: function () {
                        return $('.js-company-relation').children('option:selected').val() == window.other_choice
                    }
                }
            },
            purpose: {
                required: true,
                maxlength: 100,
            },
            date: {
                required: true,
            },
            place: {
                required: true,
                maxlength: 100,
            },
            acts: {
                required: true,
            },
            document: {
                extension: 'png,jpg,jpeg,pdf,doc,docx,xlsx,xls,ppt',
                filesize: 2097152,
            }
        },
        submitHandler(form) {
            $('.js-send-button').prop('disabled', true);
            form.submit();
        },
        errorPlacement(error, element) {
            error.insertAfter(element);
            $('.js-send-button').prop('disabled', false);
        }
    });

    $('.js-people-complaint-btn-add').on('click', function () {
        let that = $(this);
        let template = Handlebars.compile($('#item-people-complaint').html());
        $('.js-people-complaint').append(template({ id: that.data('target') }));
        that.data('target', (that.data('target') + 1));
    });

    $(document).on('click', '.js-people-complaint-item-btn-remove', function () {
        $(this).closest('.js-people-complaint-item').remove();
    });
});

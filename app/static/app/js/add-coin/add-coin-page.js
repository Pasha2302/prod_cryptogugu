
var j2 = setInterval(function () {

    if (typeof $ == 'function') {
        clearInterval(j2);
        $(document).ready(function () {

            $('[name="meta[tba]"]').change(function () {
                if ($(this).prop('checked')) {
                    $('[name="meta[launch_date]"]').prop('readonly', !0).val('')
                } else {
                    $('[name="meta[launch_date]"]').prop('readonly', !1)
                }
            });

            $('body').on('click', '.js-next-step', function (e) {
                e.preventDefault();
                var step = $(this).closest('.form-step');
                // if (valide(step)) {
                if (step.find('.error').length == 0) {
                    step.fadeOut();
                    step.next().fadeIn(function () {
                        $('body,html').animate({
                            scrollTop: step.next().offset().top
                        }, 400)
                    });
                    $('.add-coin__steps-item').eq(step.index()).removeClass('active').addClass('done');
                    $('.add-coin__steps-item').eq(step.next().index()).addClass('active');
                    $('.add-coin__steps-item').eq(step.index()).next().addClass('active')
                } else {
                    // Этот код вычисляет позицию прокрутки так, чтобы элемент с классом error оказался по середине экрана.
                    $('body,html').animate({
                        scrollTop: step.find('.error').offset().top - ($(window)
                            .height() / 2) + ($('.form-step:last-child')
                                .find('.error').outerHeight() / 2)
                    }, 400);
                }
            });

            $('body').on('click', '.js-prev-step', function (e) {
                e.preventDefault();
                var step = $(this).closest('.form-step');
                step.fadeOut();
                step.prev().fadeIn();
                $('.add-coin__steps-item').eq(step.prev().index()).addClass('active').removeClass('done');
                $('.add-coin__steps-item').eq(step.index()).removeClass('active');
                $('.add-coin__steps-item').eq(step.prev().index()).next().removeClass('active')
            });

            $('body').on('change', '[name="meta[presale]"]', function () {
                if ($(this).val() == 1) {
                    $('.js-presale').removeClass('hide')
                } else {
                    $('.js-presale').addClass('hide')
                }
            });

            document.querySelector('#presale-yes')?.click();

            $("#file").change(function (e) {
                $('.file-name').remove();
                $('.js-add-coin').after('<div class="file-name">' + e.target.files[0].name + '</div>')
            });

            $('.js-add-coin-address').click(function () {
                var b = $(this).closest('.add-coin__grid');
                var c = parseInt(b.attr('data-count'));
                var b1 = b.find('.add-coin__field').eq(0).clone();
                b1.find('select').attr('name', 'meta[contract_addresses_chain][' + c + ']').val("");
                b1.find('label').append('<div class="js-coin-remove">Remove</div>');
                var b2 = b.find('.add-coin__field').eq(1).clone();
                b2.find('input').attr('name', 'meta[contract_addresses][' + c + ']').val("");
                $(this).before(b1).before(b2);
                c++;
                b.attr('data-count', c)
            });

            $('body').on('click', '.js-coin-remove', function () {
                $(this).closest('.add-coin__field').next().remove();
                $(this).closest('.add-coin__field').remove()
            })

            $('body').on('click', '.coin-success .banner-block__overlay, .coin-success .banner-block__item-close', function (e) {
                location.reload()
            });

            $('body').on('submit', '.js-form', function (e) {
                e.preventDefault();
                var form = $(this);
                // if (valide(form)) {
                if (form.find('.error').length == 0) {
                    var btn = $(form).find('[type="submit"]');

                    btn.prop('disabled', 1);
                    const formData = new FormData(form[0]);
                    $.ajax({
                        url: '/add-coin/',
                        type: "POST",
                        processData: false,
                        contentType: false,
                        cache: false,
                        headers: {
                            "X-CSRFToken": csrf_token  // Добавляем CSRF-токен
                        },
                        data: formData,
                        dataType: "json",
                        success: function (json) {
                            btn.prop('disabled', 0);
                            if (json.errors) {
                                for (var k in json.errors) {
                                    $this.find('[name="' + k + '"]').addClass('error')
                                }
                            } else {
                                if (json.redirect) {
                                    location = json.redirect
                                } else {
                                    $('.coin-success').addClass('open')
                                }
                            }
                        },
                    })
                } else {
                    // Этот код вычисляет позицию прокрутки так, чтобы элемент с классом error оказался по середине экрана.
                    $('body,html').animate({
                        scrollTop: form.find('.error').offset().top - ($(window)
                            .height() / 2) + ($('.form-step:last-child')
                                .find('.error').outerHeight() / 2)
                    }, 400);
                }
            })

            // Может быть выбрано только одно поле для файла изображения монеты:
            const fileInput = document.querySelector('input[name="file"]');
            const fileUrlInput = document.querySelector('input[name="file_url"]');

            fileInput.addEventListener("change", function () {
                if (fileInput.files.length > 0) {
                    fileUrlInput.value = ""; // Очистить поле URL, если выбран файл
                }
            });

            fileUrlInput.addEventListener("input", function () {
                if (fileUrlInput.value.trim() !== "") {
                    fileInput.value = ""; // Очистить поле файла, если введён URL
                    document.querySelector('.file-name')?.remove();
                }
            });

        })
    }
});


var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
function isValidHttpUrl(string) {
    let url;
    try {
        url = new URL(string)
    } catch (_) {
        return !1
    }
    return url.protocol === "http:" || url.protocol === "https:"
}


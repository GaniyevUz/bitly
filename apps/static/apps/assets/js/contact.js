(function ($) {
    "use strict";

    jQuery(document).ready(function ($) {
        $(document).on('submit', '#contact_form_submit', function (e) {
            e.preventDefault();
            let name = $('#name').val();
            let email = $('#email').val();
            // let lastname = $('#lastname').val();
            let message = $('#message').val();
            // let phone = $('#phone').val();
            let csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val()

            if (name && email && message) {
                $.ajax({
                    type: "POST",
                    url: 'send-mail',
                    data: {
                        'name': name,
                        'email': email,
                        // 'lastname': lastname,
                        'message': message,
                        // 'phone': phone,
                        'csrfmiddlewaretoken': csrfmiddlewaretoken
                    },
                    success: function (data) {
                        $('#contact_form_submit').children('.email-success').remove();
                        $('#contact_form_submit').prepend('<span class="alert alert-success email-success">' + data + '</span>');
                        $('#name').val('');
                        $('#email').val('');
                        $('#message').val('');
                        // $('#lastname').val('');
                        // $('#phone').val('');
                        // $('#map').height('576px');
                        $('.email-success').fadeOut(3000);
                    },
                    error: function (res) {

                    }
                });
            } else {
                $('#contact_form_submit').children('.email-success').remove();
                $('#contact_form_submit').prepend('<span class="alert alert-danger email-success">All Fields are Required.</span>');
                // $('#map').height('576px');
                $('.email-success').fadeOut(3000);
            }

        });
    })

}(jQuery));
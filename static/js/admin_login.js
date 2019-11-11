$(document).ready(() => {

    console.log('ready');
    $('#form-error').hide()

    console.log('Ready')
    $('#submit_btn').click((event) => {

        event.preventDefault();
        let password = $('#password').val();
        let hashed_password = md5(password);
        $.ajax({
            type: 'POST',
            url: '/admin/checkpassword',
            data: { 'password': hashed_password },
            dataType: 'json',
        }).done((res) => {
            if (res.error == true) {
                $('#form-error').show();
            }
            else if (res.error == false) {
                window.location = '/admin';
            }
        });





    });



});
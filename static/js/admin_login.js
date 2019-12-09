$(document).ready(() => {

    console.log('ready');
    $('#form-error').hide()

    console.log('Ready')
    $('#submit_btn').click((event) => {
        console.log('CLicked')
        event.preventDefault();
        let password = $('#password').val();
        let hashed_password = md5(password);
        $.ajax({
            type: 'POST',
            url: '/admin/login',
            data: { 'password': hashed_password },
            dataType: 'json',
        }).done((res) => {
            console.log('Sent')
            if (res.error == true) {
                $('#form-error').show();
            }else{
                window.location.href='/admin';
            }

        });
    });
});
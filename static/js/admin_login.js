$(document).ready(() => {

    console.log('ready');
    $('#form-error').hide()

    console.log('Ready')
    $('#submit_btn').click((event) => {
        console.log($('#password').val())

        event.preventDefault();
        console.log('entered')
        let password = $('#password').val();
        console.log(password);
        let hashed_password = md5(password);
        console.log(hashed_password)
        $.ajax({
            type: 'POST',
            url: '/admin/checkpassword',
            data: { 'password': hashed_password },
            dataType: 'json',
        }).done((res) => {
            console.log("res=" + res)
            if (res.error == true) {
                $('#form-error').show();
            }
            else if (res.error == false) {
                window.location = '/admin';
            }
        });





    });



});
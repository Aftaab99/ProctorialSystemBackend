$(document).ready(()=>{

    $('#form-error').hide();
    $('#form-success').hide();
    console.log('Hidden')

    $('#submit_btn').click((event)=>{
        event.preventDefault();

        let pid = $('#proc_email').val()
        let pass = $('#proc_pass').val()
        let cpass = $('#cproc_pass').val()
        console.log(pid)
        console.log(pass)
        console.log(cpass)
        if(!pid=="" && pass==cpass && !pass==""){
            $.ajax({
                type: 'POST',
                url: '/admin/add_proctor_cred',
                data: {'email': pid, 'password': md5(pass)},
                dataType: 'json'
            }).done((res)=>{
                if(res.error==true){
                    $('#form-error').show();
                    $('#form-success').hide();
                }
                else if(res.error==false){
                    $('#form-error').hide();
                    $('#form-success').show();
                }
            })
        }
        else{
            $('#form-error').show();
            $('#form-success').hide();

        }




    });

});
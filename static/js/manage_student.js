$(document).ready(() => {
    console.log('Ready')
    remove_btn_clicked = (i) => {
        console.log(i);
        $.ajax({
            url: '/admin/student/remove',
            type: 'POST',
            data: { usn: i },
            success: (res) => {
                $("#" + i).remove();

            },
            dataType: 'json'
        })
    }

    $('#dob').datepicker({
        format: 'dd/mm/yyyy'
    });



    $("#add_new_student").click((e) => {
        let fname = $('#fname').val();
        let mname = $('#mname').val();
        let lname = $('#lname').val();
        let usn = $('#student_usn').val();
        let dob = $('#dob').val();
        let student_email = $('#student_email').val().toLowerCase();
        let student_phone = $('#student_phone').val();
        let join_year = $('#join_year').val();
        let grad_year = $('#grad_year').val();
        let quota = $('#quota').val();
        let dept_id = $('#dept_id').val();
        let parent_name = $('#parent_name').val();
        let parent_email = $('#parent_email').val();
        console.log('Parent_email=' + parent_email)
        let parent_phone = $('#parent_phone').val();
        var email_regex = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
        console.log(email_regex.test(student_email));

        console.log(student_phone)
        let result = $('#add-result')
        if (!/^[0-9][A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{3}/.test(usn)) {
            result.text("USN empty or invalid");
            result.removeAttr('class')
            result.attr('class', 'col-12 text-danger');
        }
        else if (fname == "") {
            result.text("First name required");
            result.removeAttr('class')
            result.attr('class', 'col-12 text-danger');
        }
        else if (dob == "") {
            result.text("Date of birth invalid");
            result.removeAttr('class')
            result.attr('class', 'col-12 text-danger');
        }
        else if (!email_regex.test(student_email)) {
            result.text("Student email not valid");
            result.removeAttr('class')
            result.attr('class', 'col-12 text-danger');
        }
        else if (!/^\d{10}$/.test(student_phone)) {
            result.text("Student phone not valid");
            result.removeAttr('class')
            result.attr('class', 'col-12 text-danger');
        }

        else if (!/\d{4}/.test(join_year)) {
            result.text("Invalid joining year");
            result.removeAttr('class')
            result.attr('class', 'col-12 text-danger');
        }
        else if (!/\d{4}/.test(grad_year)) {
            result.text("Invalid graduation year");
            result.removeAttr('class')
            result.attr('class', 'col-12 text-danger');
        }
        else if (!email_regex.test(parent_email)) {
            result.text("Parent email not valid");
            result.removeAttr('class')
            result.attr('class', 'col-12 text-danger');
        }
        else if (!/^\d{10}$/.test(parent_phone)) {
            result.text("Parent phone not valid");
            result.removeAttr('class')
            result.attr('class', 'col-12 text-danger');
        }
        else if (parent_name == "") {
            result.text("Parent name empty");
            result.removeAttr('class')
            result.attr('class', 'col-12 text-danger');
        }

        else {
            console.log('Cool!')
            result.text("");

            // let dept_id=$('#add-fact-dept').val()
            // let fact_id_esc = replace_last_occurence(fact_id, '@', '__at__')
            // fact_id_esc = replace_last_occurence(fact_id_esc, '.', '__dot__')

            $.ajax({
                url: '/admin/student/add',
                type: 'POST',
                data: { fname: fname, lname: lname, mname: mname, dept_id: dept_id, usn: usn, dob: dob, join_year: join_year, grad_year: grad_year, student_email: student_email, student_phone: student_phone, quota: quota, parent_name: parent_name, parent_email: parent_email, parent_phone: parent_phone },
                dataType: 'json',
                success: (res) => {
                    if (!res.error) {
                        result.text("Student added successfully");
                        result.removeAttr('class')
                        result.attr('class', 'col-12 text-success');
                        $('#studlist').append(`
                        <li class="list-group-item" id="${usn}">
                        <div class="row">
                            <div class="col-4">${fname + " " + mname + " " + lname}</div>
                            <div class="col-4">${usn}</div>
                            <div class="col-2">${dept_id}</div>
                            <div class="col-2">
                                <button class="btn btn-primary" value="${usn}"
                                    onclick="remove_btn_clicked(this.value)"><i
                                        class="fa fa-trash-o text-white"></i></button>
                            </div>

                        </div>
                    </li>
                        `);
                    }
                    else {
                        result.text("Add failed. Student already exists");
                        result.removeAttr('class')
                        result.attr('class', 'col-12 text-danger');
                    }
                }

            })
        }


    })
})

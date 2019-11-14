$(document).ready(() => {

    remove_btn_clicked = (i) => {
        $.ajax({
            url: '/admin/department/remove',
            type: 'POST',
            data: { dept_id: i },
            success: (res) => {
                $("#" + i).remove();
            },
            dataType: 'json'
        })
    }


    $("#add-dept-btn").click((e) => {
        let dept_name = $('#add-dept-name').val();
        let dept_id = $('#add-dept-id').val();
        dept_id = dept_id.toUpperCase();
        let result = $('#add-result')
        if (dept_name == "") {
            result.text("Department name empty");
            result.removeAttr('class')
            result.attr('class', 'col-12 text-danger');
        }
        else if (dept_id == "") {
            result.text("Department abbreviation empty");
            result.removeAttr('class')
            result.attr('class', 'col-12 text-danger');
        }
        else {
            $.ajax({
                url: '/admin/department/add',
                type: 'POST',
                data: { dept_name: dept_name, dept_id: dept_id },
                dataType: 'json',
                success: (res) => {
                    if (!res.error) {
                        result.text("Department added successfully");
                        result.removeAttr('class')
                        result.attr('class', 'col-12 text-success');
                        $('#deptlist').append(`
                        <li class="list-group-item" id="${dept_id}">
                            <div class="row">

                                <div class="col-sm-11 mt-sm-2">${dept_name}</div>
                                
                                <div class="col-md-1 col-sm-1 mt-sm-2 text-center"><button class="btn btn-primary"
                                        value="${dept_id}" onclick="remove_btn_clicked(this.value)"><i
                                            class="fa fa-trash-o text-white"></i></button></div>
                            </div>
                        </li>
                        `);
                    }
                    else {
                        result.text("Add failed. Department already exists");
                        result.removeAttr('class')
                        result.attr('class', 'col-12 text-danger');
                    }
                }

            })
        }


    })

})
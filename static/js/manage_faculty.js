$(document).ready(() => {

    remove_btn_clicked = (i) => {
        $.ajax({
            url: '/admin/faculty/remove',
            type: 'POST',
            data: { fid: i },
            success: (res) => {
                $("#" + i).remove();

            },
            dataType: 'json'
        })
    }

    replace_last_occurence = (s, s1, s2)=>{
        let index = s.lastIndexOf(s1);
        return s.slice(0, index)+s2+s.slice(index+1);
        
    }

    $("#add-fact-btn").click((e) => {
        let fact_name = $('#add-fact-name').val();
        let fact_id = $('#add-fact-id').val();
        
        let result = $('#add-result')
        if (fact_name == "") {
            result.text("Faculty name empty");
            result.removeAttr('class')
            result.attr('class', 'col-12 text-danger');
        }
        else if (fact_id == "") {
            result.text("Faculty email not valid");
            result.removeAttr('class')
            result.attr('class', 'col-12 text-danger');
        }
        else {
            let dept_id=$('#add-fact-dept').val()
            let fact_id_esc = replace_last_occurence(fact_id, '@', '__at__')
            fact_id_esc = replace_last_occurence(fact_id_esc, '.', '__dot__')

            $.ajax({
                url: '/admin/faculty/add',
                type: 'POST',
                data: { fid: fact_id, fname: fact_name, dept_id:dept_id },
                dataType: 'json',
                success: (res) => {
                    if (!res.error) {
                        result.text("Faculty added successfully");
                        result.removeAttr('class')
                        result.attr('class', 'col-12 text-success');
                        $('#factlist').append(`
                        <li class="list-group-item" id="${fact_id_esc}">
                            <div class="row">

                                <div class="col-4 mt-sm-2">${fact_name}</div>
                                <div class="col-4 mt-sm-2">${fact_id}</div>
                                <div class="col-3 mt-sm-2">${res.dept_name}</div>
                                <div class="col-1 mt-sm-2">
                                    <button class="btn btn-primary" value="${fact_id_esc}" onclick="remove_btn_clicked(this.value)"><i
                                            class="fa fa-trash-o text-white"></i></button>
                                </div>
                            </div>
                        </li>
                        `);
                    }
                    else {
                        result.text("Add failed. Faculty already exists");
                        result.removeAttr('class')
                        result.attr('class', 'col-12 text-danger');
                    }
                }

            })
        }


    })
})

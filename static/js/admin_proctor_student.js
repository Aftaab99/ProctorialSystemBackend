$(document).ready(()=>{
    $('.col-12.students').hide();
    hide_or_show=(id, button_id)=>{
        if($("#"+id).is(':visible')){
            $("#"+id).hide();
            $("#"+button_id).text("View");
        }
        else{
            $("#"+id).show();
            $("#"+button_id).text("Hide")

        }
    }
})
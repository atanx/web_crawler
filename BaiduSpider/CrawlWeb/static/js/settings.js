/**
 * Created by youxiang on 2017/3/10.
 */


$(document).ready(function() {
    $("#groups").change(function () {
        var selected = $("#groups option:selected").text();
        if (selected != "--请选择--") {
            $.ajax({
                type: 'post',
                url: '/query_site_list',
                data: {'name': selected},
                success: function (data) {
                    $("#site_list").val(data);
                }
            });
        }
        else {
            $("#site_list").val("");
        }
        console.log(selected)
    });

    $("#AddSiteFormClick").click(function () {
        $("#addSiteFormModel").modal();
    })
})
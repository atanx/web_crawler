/**
 * Created by youxiang on 2017/03/06.
 */
$(function() {
    function get_result() {
        $.ajax({
            type: 'get',
            url: '/get_result',
            success: function (data) {
                $("#result_table").html(data);
            }
        })
    };
    get_result();
    setInterval(get_result, 3000);
})




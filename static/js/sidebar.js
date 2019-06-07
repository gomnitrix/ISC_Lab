
function get_data() {
    $.ajax({
        type: "GET",
        url: "./proto", //后台处理函数的url


        success: function (result) { //获取后台处理后传过来的result
            data = result.data;

        },

    });
}
function start() {
    $.ajax({
        type: "GET",
        url: "./start", //后台处理函数的url

        success: function (result) { //获取后台处理后传过来的result
            data = result.info;
        },
    });
    setInterval(function () { get_data() }, 3000);
}
function stop() {


    $.ajax({
        type: "GET",
        url: "./stop", //后台处理函数的url

        success: function (result) { //获取后台处理后传过来的result
            data = result.info;
        },
    });
}
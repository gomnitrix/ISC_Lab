
function get_data() {
    $.ajax({
        type: "GET",
        url: "./proto", //后台处理函数的url


        success: function (result) { //获取后台处理后传过来的result
            data = result.data;

        },

    });
}

function get_total() {
    $.ajax({
        type: "GET",
        url: "./pkt_sum", //后台处理函数的url


        success: function (result) { //获取后台处理后传过来的result
            total = result.num;

        },

    });
}
function get_rst() {
    $.ajax({
        type: "GET",
        url: "./get_rst_num", //后台处理函数的url


        success: function (result) { //获取后台处理后传过来的result
            reset = result.num;

        },

    });
}
function get_riskflow() {
    $.ajax({
        type: "GET",
        url: "./riskflow", //后台处理函数的url


        success: function (result) { //获取后台处理后传过来的result
            rf = result.num;

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
    setInterval(function () { get_data() }, 1000);
    setInterval(function () { get_total() }, 1000);
    setInterval(function () { get_riskflow() }, 1000);
    setInterval(function () { get_rst() }, 1000);

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

function counterNum(obj, start, end, step, duration) {
    $(obj).html(start);
    setInterval(function () {
        var val = Number($(obj).html());
        if (val < end) {
            $(obj).html(val + step);
        } else {
            $(obj).html(end);
            clearInterval();
        }
    }, duration);
}
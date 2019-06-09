
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
function get_app() {
    $.ajax({
        type: "GET",
        url: "./app", //后台处理函数的url


        success: function (result) { //获取后台处理后传过来的result
            app_num = result.num;
            app_num2 = app_num.slice(0,5);

        },

    });
}

function change()
{

   qq[0] = qq[1]
   qq[1] = qq[2]
   qq[2] = qq[3]
   qq[3] = qq[4]
   qq[4] = qq[5]
   qq[5] = app_num2[0]
     wc[0] = wc[1]
   wc[1] = wc[2]
   wc[2] = wc[3]
   wc[3] = wc[4]
   wc[4] = wc[5]
   wc[5] = app_num2[1]

     iqy[0] = iqy[1]
   iqy[1] = iqy[2]
   iqy[2] = iqy[3]
   iqy[3] = iqy[4]
   iqy[4] = iqy[5]
   iqy[5] = app_num2[2]

   tdr[0] = tdr[1]
   tdr[1] = tdr[2]
   tdr[2] = tdr[3]
   tdr[3] = tdr[4]
   tdr[4] = tdr[5]
   tdr[5] = app_num2[3]

    we[0] = we[1]
  we[1] = we[2]
   we[2] = we[3]
   we[3] = we[4]
   we[4] = we[5]
   we[5] = app_num2[4]



}
function start() {
    $.ajax({
        type: "GET",
        url: "./start", //后台处理函数的url

        success: function (result) { //获取后台处理后传过来的result
            data = result.info;
        },
    });
    t1 = setInterval(function () { get_data() }, 1000);
    t2 = setInterval(function () { get_total() }, 1000);
    t3 = setInterval(function () { get_riskflow() }, 1000);
    t4 = setInterval(function () { get_rst() }, 1000);
    t5 = setInterval(function () { get_app() }, 1000);
    t6 = setInterval(function () { change() }, 1000);

}


function stop() {

    t1.clearInterval
    t2.clearInterval
    t3.clearInterval
    t4.clearInterval
    t5.clearInterval
    t6.clearInterval
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
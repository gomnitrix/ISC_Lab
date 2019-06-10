var t1;
function get_data() {
    $.ajax({
        type: "GET",
        url: "./proto", //后台处理函数的url


        success: function (result) { //获取后台处理后传过来的result
            data = result.data;
            show()
        },

    });
}

function show() {

    var barChartData = {
        animation: false,
        labels: ["SSL", "SSH", "HTTP", "DNS", "FTP", "MYSQL"],/*这里传变量（如果协议种类变化的话）*/
        datasets: [
            {

                data: data,/*这里传变量*/
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)']
            }

        ]
    };
    // var options = {
    //     animation: false
    // }
    new Chart(document.getElementById("bar1").getContext("2d")).Bar(barChartData);

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
            app_num2 = app_num.slice(0, 5);

        },

    });
}
function AddTableRow(proto, src_ip, dst_ip, sport, dport) {

    var tab = document.getElementById('tab1')
    var len = tab.rows.length;//获取表格的行数
    var x = tab.insertRow(len);
    var y = x.insertCell(0);
    var z = x.insertCell(1);
    var a = x.insertCell(2);
    var b = x.insertCell(3);
    var c = x.insertCell(4);
    y.innerHTML = proto;
    z.innerHTML = src_ip;
    a.innerHTML = dst_ip;
    b.innerHTML = sport;
    c.innerHTML = dport;
}
function dtl() {
    $.ajax({
        type: "GET",
        url: "./dtl", //后台处理函数的url


        success: function (result) { //获取后台处理后传过来的result
            var values = result.data

            if (values == 0) {
                rkf_dtl = []
            }
            else {
                var len = values.length
                for (i = 0; i < len; i++) {
                    var proto = ""
                    if (values[i].proto == "6") {
                        proto = "TCP"
                    }
                    else {
                        proto = "UDP"
                    }
                    AddTableRow(proto, values[i].src_ip, values[i].dst_ip, values[i].sport, values[i].dport)

                }
            }
            console.log(rkf_dtl)

        },

    });



}

function change() {

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

    var time = new Date();
    var h = time.getHours();
    var m = time.getMinutes();
    var s = time.getSeconds();
    var T = h + ":" + m + ":" + s;
    times[0] = times[1]
    times[1] = times[2]
    times[2] = times[3]
    times[3] = times[4]
    times[4] = times[5]
    times[5] = T


}
function start() {
    window.alert("start running");
    $.ajax({
        type: "GET",
        url: "./start", //后台处理函数的url

        success: function (result) { //获取后台处理后传过来的result
            data = result.info;
            flag = 1;
        },
    });

    t1 = setInterval(function () {
        get_data();
        get_total();
        counterTotal();
        get_riskflow();
        // counterRf();
        get_rst();
        // counterReset();
        get_app();
        change();
        dtl();
    }, interval);
}


function stop() {
    window.alert("stop running");
    clearInterval(t1)
    flag = 2;
    $.ajax({
        type: "GET",
        url: "./stop", //后台处理函数的url

        success: function (result) { //获取后台处理后传过来的result
            data = result.info;
        },
    });
}


function counterTotal() {
    var element = document.getElementById("total");
    step = Math.round((total - element.value) / 20)
    var element2 = document.getElementById("rf");
    step2 = Math.round((rf - element2.value) / 20)
    var element3 = document.getElementById("rst");
    step3 = Math.round((reset - element3.value) / 20)
    setInterval(function () {
        val = element.value;
        val = val + step
        if (val < total) {
            element.innerHTML = val;
        } else {
            element.innerHTML = total;
            val2 = element2.value;
            val2 = val2 + step2
            if (val2 < rf) {
                element2.innerHTML = val2;
            } else {
                element2.innerHTML = rf;
                val3 = element3.value;
                val3 = val3 + step3
                if (val3 < reset) {
                    element3.innerHTML = val3;
                } else {
                    element3.innerHTML = reset;
                    clearInterval();
                }
            }
        }
    }, 15);
}

function counterRf() {
    var element = document.getElementById("rf");
    step = Math.round((rf - element.value) / 20)
    setInterval(function () {
        val = element.value;
        val = val + step
        if (val < rf) {
            element.innerHTML = val;
        } else {
            element.innerHTML = rf;

            clearInterval();
        }
    }, 30);
}

function counterReset() {
    var element = document.getElementById("rst");
    step = Math.round((reset - element.value) / 20)
    setInterval(function () {
        val = element.value;
        val = val + step
        if (val < reset) {
            element.innerHTML = val;
        } else {
            element.innerHTML = reset;
            clearInterval();
        }
    }, 30);
}
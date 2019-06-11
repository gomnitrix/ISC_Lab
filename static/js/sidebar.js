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
            var element = document.getElementById("total");
            element.innerHTML=total;
        },

    });
}

function get_block()
{
$.ajax({
        type: "GET",
        url: "./block", //后台处理函数的url


        success: function (result) { //获取后台处理后传过来的result
            block = result.num;
            var element = document.getElementById("block");
            element.innerHTML=block;
        },

    });
}
function get_rst() {
    $.ajax({
        type: "GET",
        url: "./get_rst_num", //后台处理函数的url


        success: function (result) { //获取后台处理后传过来的result
            reset = result.num;
            var element = document.getElementById("rst");
            element.innerHTML=reset;
        },

    });
}
function get_riskflow() {
    $.ajax({
        type: "GET",
        url: "./riskflow", //后台处理函数的url


        success: function (result) { //获取后台处理后传过来的result
            rf = result.num;
            var element = document.getElementById("rf");
            element.innerHTML=rf;
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
function AddTable2Row(id,str,data) {

    var tab = document.getElementById('tab2')
    var len = tab.rows.length;//获取表格的行数
    var x = tab.insertRow(len);
    var y = x.insertCell(0);
    var z = x.insertCell(1);
    var a = x.insertCell(2);

    y.innerHTML = id;
    z.innerHTML = str;
    a.innerHTML = data;

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
        },

    });



}

function change() {
    qq = qq.slice(1)
    qq.push(app_num2[0])
    wc = wc.slice(1)
    wc.push(app_num2[1])
    iqy = iqy.slice(1)
    iqy.push(app_num2[2])
    tdr = tdr.slice(1)
    tdr.push(app_num2[3])
    we = we.slice(1)
    we.push(app_num2[4])

    var time = new Date();
    var h = time.getHours();
    var m = time.getMinutes();
    var s = time.getSeconds();
    var T = h + ":" + m + ":" + s;
    times = times.slice(1)
    times.push(T)

}

function store(){
    var storage = window.sessionStorage;
    storage['flag'] = flag;
    window.location.href = window.setting_host;
}

function store2(){
    var storage = window.sessionStorage;
    storage['flag'] = flag;
    storage['home'] = 1;
    window.location.href = window.home_host;
}

function tostop() {
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

function start() {
    if (flag == 0 || flag == 2) {
        window.alert("start running");
    }
    
    flag = 1;
    $.ajax({
        type: "GET",
        url: "./start", //后台处理函数的url

        success: function (result) { //获取后台处理后传过来的result
            data = result.info;
        },
    });

    t1 = setInterval(function () {
        get_data();
        get_total();
        get_riskflow();
        get_block();
        get_rst();
        get_app();
        change();
        dtl();
    }, interval);
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

function submit()
  {

  var filter = document.getElementById("ipt").value
       $.ajax({
        type: "GET",
        url: "./submit/?ft="+filter, //后台处理函数的url

        success: function (result) { //获取后台处理后传过来的result
            data = result.data;
                var tab = document.getElementById('tab2')
                var l = tab.rows.length;//获取表格的行数
                var x = tab.insertRow(l);
                var y = x.insertCell(0);
                var z = x.insertCell(1);
                var a = x.insertCell(2);
                var time = new Date();
                var yr = time.getFullYear();
                var mth = time.getMonth()+1;
                var dy = time.getDate();
                var T = 'June' + " " + dy + "," +yr;
                y.innerHTML = l;
                z.innerHTML = filter;
                a.innerHTML = T;

        },
    });
 }

 function dlt()
 {
    var filter = document.getElementById("ipt").value
    $.ajax({
        type: "GET",
        url: "./delete/?ft="+filter, //后台处理函数的url

        success: function (result) { //获取后台处理后传过来的result
        values = result.data
          location.reload()
        },
    });
 }
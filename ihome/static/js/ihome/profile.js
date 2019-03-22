function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(document).ready(function(){
    $("#form-avatar").submit(function (e){
        //阻止表单的默认行为
        e.preventDefault();
        // 利用jquery.form.min.js提供的ajaxSubmit对表单进行异步提交
        $(this).ajaxSubmit({
            url:"/api/v1.0/users/avatar",
            type:"post",
            dataType:"json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success:function(resp){
                if(resp.errno == "0"){
                    //上传成功
                    var avatarUrl=resp.data.file_name;
                    $("#user-avatar").attr("src",avatarUrl);
                }else{
                    alert(resp.errmsg);
                }
            }
        })
    });

     // 在页面加载是向后端查询用户的信息
    $.get("/api/v1.0/user", function(resp){
        // 用户未登录
        if ("4101" == resp.errno) {
            location.href = "/login.html";
        }
        // 查询到了用户的信息
        else if ("0" == resp.errno) {
            $("#user-name").val(resp.data.name);
            if (resp.data.avatar) {
                $("#user-avatar").attr("src", resp.data.avatar);
            }
        }
    }, "json");

     $("#form-name").submit(function(e){
        e.preventDefault();
        // 获取参数
        var name = $("#user-name").val();

        if (!name) {
            alert("请填写用户名！");
            return;
        }
        $.ajax({
            url:"/api/v1.0/users/name",
            type:"PUT",
            data: JSON.stringify({name: name}),
            contentType: "application/json",
            dataType: "json",
            headers:{
                "X-CSRFTOKEN":getCookie("csrf_token")
            },
            success: function (data) {
                if ("0" == data.errno) {
                    $(".error-msg").hide();
                    showSuccessMsg();
                } else if ("4001" == data.errno) {
                    $(".error-msg").show();
                } else if ("4101" == data.errno) {
                    location.href = "/login.html";
                }
            }
        });
    })
});





function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    var alipayData = document.location.search.substr(1);
    $.ajax({
        url: "/api/v1.0/order/payment",
        type: "PUT",
        data: alipayData,
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        }
    })
});


/*!
 */

if (typeof jQuery === 'undefined') {
  throw new Error('UtilsLib\'s JavaScript requires jQuery')
}

function UtilsLib(){}

UtilsLib.LastOpenedPopupParam = null;

UtilsLib.TogglePopup = function(id, param){    
    UtilsLib.LastOpenedPopupParam = param;
    $(id).modal("toggle");
}

UtilsLib.ShowSuccess = function(msg){
    if ($("#msgBody").length)
        $("#msgBody").text(msg);    
    else
        $("body").prepend('<div id="msgBody" class="alert alert-success">'+msg+'</div>');
    $("#msgBody").visible = true;
}

UtilsLib.getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function ShowError(str)
{
    alert(str);
}

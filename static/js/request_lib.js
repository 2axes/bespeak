/*!
 */

if (typeof jQuery === 'undefined') {
  throw new Error('RequestLib\'s JavaScript requires jQuery')
}

function RequestLib(){}

RequestLib.Request = function(action, parentNode, templateNode, title,nick,email,type,message){
    $.ajax({
        type: "POST",
        url: action,
        data: {inTitle: title, inNick: nick, inEmail: email, inType: type, inMessage: message}
    }).fail(function (resp, data, status) {
        ShowError("Request failed. Last result: " + resp.responseText);
    }).done(function(data, text, obj){
        if (templateNode.length){
            clone = templateNode.clone();
            clone.find("div[id^='divIssueTitle']").html(title);
            clone.find("#divIssueDate").html('Now');
            clone.find("#divIssueType").html(type);
            clone.find("#divIssueNick").html(nick);
            clone.find("div[id^='divIssueDescription']").html(message);
            clone.find("#divIssueComments").remove();
            clone.find("#btnVote").attr("disabled","disabled");
            clone.find("#btnComment").attr("disabled","disabled");
            clone.attr("id","divIssueCloned");
            clone.find("#barIssueTriage").remove();
            clone.prependTo(parentNode);
        }
    });
}

RequestLib.Comment = function(action, issueId, parentNode, templateNode, nick, email,message){
    $.ajax({
        type: "POST",
        url: action,
        data: {inIssueId: issueId, inNick: nick, inEmail: email, inMessage: message}
    }).fail(function (resp, data, status) {
        ShowError("Comment failed. Last result: " + resp.responseText);
    }).done(function(data, text, obj){
        if (templateNode.length){
            clone = templateNode.clone();
            clone.find("#divCommentDate").html('Now');
            clone.find("#divCommentNick").html(nick);
            clone.find("div[id^='divCommentMessage']").html(message);
            clone.attr("id", "divCommentCloned");
            clone.find("#barCommentTriage").remove();
            clone.appendTo(parentNode);
        }
    });
}

RequestLib.Vote = function(action, issueId, nick,email){
    $.ajax({
        type: "POST",
        url: action,
        data: {inIssueId: issueId, inNick: nick, inEmail: email}
    }).fail(function (data, status) {
        ShowError("Comment failed. Last result: " + status);
    });    
}

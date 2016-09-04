/*!
 */

if (typeof jQuery === 'undefined') {
  throw new Error('triage_op\'s JavaScript requires jQuery')
}


function TriageOp(){}

TriageOp.IssueVisibility = function(objId, issueId, v){
    $.ajax({
        type: "POST",
        url: 'forms/UpdateIssueCommand/',
        data: {inIssueId: issueId, 
               inVisibility: v}
    }).fail(function(data, status){
        ShowError("Visibility Post failed. Last result: " + status);
    });
    $('#'+objId).html('Visibility: '+v+' <span class="caret"></span>')
}

TriageOp.CommentVisibility = function(objId, commentId, v){
    if (v == 'public'){
        toggle = false;
        v = 'private'
    }
    else{
        toggle = true;
        v = 'public'
    }

    if (confirm('Change visibility to ' + v + '?') == false)
        return;

    $.ajax({
        type: "POST",
        url: 'forms/UpdateCommentCommand/',
        data: {inCommentId: commentId, 
               inPublic: toggle}
    }).fail(function(data, status){
        ShowError("Comment Visibility Post failed. Last result: " + status);
    });
    $('#'+objId).text('visibility: '+v);
    $('#'+objId).attr('href', "javascript:TriageOp.CommentVisibility('aVisibility"+commentId+"',"+commentId+", '" + v + "')");
}

TriageOp.IssueDelete = function(objId, issueId){
    if (confirm('Delete Issue?') ==  false)
        return;

    $.ajax({
        type: "POST",
        url: 'forms/DeleteIssueCommand/',
        data: {inIssueId: issueId}
    }).fail(function(data, status){
        ShowError("Delete Post failed. Last result: " + status);
    });
    $('#'+objId).remove();
}

TriageOp.CommentDelete = function(objId, commentId){
    if (confirm('Delete Comment?') == false)
        return;
    $.ajax({
        type: "POST",
        url: 'forms/DeleteCommentCommand/',
        data: {inCommentId: commentId}
    }).fail(function(data, status){
        ShowError("Delete Post failed. Last result: " + status);
    });
    $('#'+objId).remove();
}

TriageOp.IssueEditPopup = function(objId, issueId, currentTitle, currentMessage){
    document.getElementById('inUpdateMessage').value = currentMessage;
    $('#inUpdateTitle').attr('value', currentTitle);
    $('#inUpdateIssueId').attr('value', issueId);
    $('#inUpdateIssueObjId').attr('value', objId);
    UtilsLib.TogglePopup('#updateIssuePopup');
}

TriageOp.IssueEdit = function(objId, issueId, newTitle, newMessage){
    $.ajax({
        type: "POST",
        url: 'forms/UpdateIssueCommand/',
        data: {inIssueId: issueId,
               inTitle: newTitle,
               inMessage: newMessage }
    }).fail(function(data, status){
        ShowError("IssueEdit Post failed. Last result: " + status);
    });

    $('#divIssueDescription_'+issueId).html(newMessage);
    $('#divIssueTitle_'+issueId).html(newTitle);
    UtilsLib.TogglePopup('#updateIssuePopup');
}

TriageOp.CommentEditPopup = function(objId, commentId, currentMessage){
    document.getElementById('inUpdateComment').value = currentMessage;
    $('#inUpdateCommentId').attr('value', commentId);
    $('#inUpdateCommentObjId').attr('value', objId);
    UtilsLib.TogglePopup('#updateCommentPopup');
}

TriageOp.CommentEdit = function(objId, commentId, newMessage){
    $.ajax({
        type: "POST",
        url: 'forms/UpdateCommentCommand/',
        data: {inCommentId: commentId,
               inMessage: newMessage }
    }).fail(function(resp, data, status){
        ShowError("CommentEdit Post failed. Last result: " + resp.responseText);
    }).done(function(data, text, obj){
        $('#'+objId).html(newMessage);
    });

    UtilsLib.TogglePopup('#updateCommentPopup');
}

TriageOp.IssueStatus = function(objId, issueId, s){
    $.ajax({
        type: "POST",
        url: 'forms/UpdateIssueCommand/',
        data: {inIssueId: issueId,
               inStatus: s}
    }).fail(function(data, status){
        ShowError("IssueStatus Post failed. Last result: " + status);
    });
    $('#'+objId).html('Status: '+s+' <span class="caret"></span>');
}


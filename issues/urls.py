from django.conf.urls import patterns, include, url
from . import views
from . import forms

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^forms/IssueRequestCommand/$', forms.Commands.IssueRequestCommand, name='IssueRequestCommand'),
    url(r'^forms/UpdateIssueCommand/$', forms.Commands.UpdateIssueCommand, name='UpdateIssueCommand'),
    url(r'^forms/DeleteIssueCommand/$', forms.Commands.DeleteIssueCommand, name='DeleteCommand'),
    url(r'^forms/CommentCommand/$', forms.Commands.CommentCommand, name='CommentCommand'),
    url(r'^forms/UpdateCommentCommand/$', forms.Commands.UpdateCommentCommand, name='UpdateCommentCommand'),
    url(r'^forms/DeleteCommentCommand/$', forms.Commands.DeleteCommentCommand, name='DeleteCommentCommand'),
    url(r'^forms/VoteCommand/$', forms.Commands.VoteCommand, name='VoteCommand'),
    url(r'^load/$', views.LoadView.as_view(), name='Load'),
    url(r'^confirm/$', views.ConfirmView.as_view(), name='Confirm'),
    url(r'^vote/$', views.VoteConfirmView.as_view(), name='VoteConfirm'),
]

from django.shortcuts import render_to_response, redirect
from django import template
from ..models import IssueStatus

register = template.Library()


@register.inclusion_tag('triage_comment_controls.html')
def show_comment_controls(user,comment):
    visible = 'private'
    if comment.public:
        visible = 'public'
    return { 
        'user': user,
        'commentId': comment.id,
        'commentVisibility': visible
    }


@register.inclusion_tag('triage_controls.html')
def show_issue_controls(user,issue):
    issueVisibility = 'Private'
    if issue.public:
        issueVisibility = 'Public'
    
    return { 
        'user': user,
        'issueId': issue.id,
        'issueDivObjId': 'divIssue_{0}'.format(issue.id),
        'issueVisibility': issueVisibility,
        'issueStatus': issue.status,
        'iStatusList': IssueStatus.objects.all(),
        'issueTitle': issue.title,
        'issueDescription': issue.description
    }

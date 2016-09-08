from django.shortcuts import render_to_response, redirect
from django import template
from django.core.paginator import Paginator
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

@register.inclusion_tag('paginator.html')
def show_paginator(paginator, current_page, order):
    if current_page > 1:
        previous = current_page -1
    else:
        previous = current_page

    if current_page < paginator.num_pages:
        next = current_page +1
    else:
        next = paginator.num_pages

    return {
        'current_page': current_page,
        'previous_link': '?order={0}&page={1}'.format(order, previous),
        'next_link': '?order={0}&page={1}'.format(order, next),
        'first_link': '?order={0}&page=1'.format(order),
        'last_link': '?order={0}&page={1}'.format(order, paginator.num_pages)
    }

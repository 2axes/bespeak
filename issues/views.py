import urllib
from urllib import parse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from .models import Issue
from .models import Settings
from .models import Nickname
from .models import IssueStatus
from .models import IssueType
from .models import VoteHistory
from .loader import Defs
from .loader import Loader
from .forms import IssueRequestForm
from .forms import EmailQueueUtils
from .tokenbuilder import NewUserToken
from .tokenbuilder import VoteConfirmToken

# Create your views here.
from django.views.generic.base import TemplateView

class IssuesListView(generic.TemplateView):
    model = Issue
    template_name = 'issues/index.html'


class IndexView(generic.ListView):
    model = Issue
    paginate_by = 100
    template_name = 'issues/index.html'
    context_object_name = 'issues'

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['iTypeList'] = IssueType.objects.all()
        return context


class ConfirmView(generic.TemplateView):
    template_name = 'issues/confirm.html'

    def get_context_data(self, **kwargs):
        print('!x1')
        context = super(ConfirmView,self).get_context_data(**kwargs)
        secret = Settings.objects.get(id=Defs.TOKEN_CRYPT_SECRET_id).value
        tkstr = urllib.parse.unquote(self.request.GET.get('token'))
        tkobj = NewUserToken()
        context['confirmed'] = False
        try:
            context['confirmed'] = tkobj.validate(secret,tkstr)
            context['confirmation_for'] = tkobj.tokenfor
            if (context['confirmed'] == True):
                user = Nickname.objects.get(id=tkobj.userid)
                context['user'] = user
                user.confirmed = True
                user.save()
            EmailQueueUtils.process_queue()
        except Exception as err:
            print('ConfirmView Exception {0}'.format(err))
        return context


class VoteConfirmView(generic.TemplateView):
    template_name = 'issues/confirm.html'

    def get_context_data(self, **kwargs):
        print('!x2')
        context = super(VoteConfirmView,self).get_context_data(**kwargs)
        secret = Settings.objects.get(id=Defs.TOKEN_CRYPT_SECRET_id).value
        tkstr = urllib.parse.unquote(self.request.GET.get('token'))
        tkobj = VoteConfirmToken()
        context['confirmed'] = False
        try:
            context['confirmed'] = tkobj.validate(secret,tkstr)
            context['confirmation_for'] = tkobj.tokenfor
            if (context['confirmed'] == True):
                issue = Issue.objects.get(id=tkobj.issueId)
                context['confirmation_issue'] = issue.title
                user = Nickname.objects.get(id=tkobj.userid)
                context['user'] = user
                user.confirmed = True
                user.save()
                try:
                    VoteHistory.objects.get(email=tkobj.email,issueObj=issue)
                except VoteHistory.DoesNotExist:
                    issue.votesCount = issue.votesCount + 1
                    issue.save()
                    vote = VoteHistory()
                    vote.issueObj = issue
                    vote.email = tkobj.email
                    vote.save()
        except Exception as err:
            print('ConfirmView Exception {0}'.format(err))
        return context


class LoadView(generic.ListView):
    model = Settings
    template_name = 'issues/loaded.html'
    context_object_name = 'settings'

    def dispatch(self, request, *args, **kwargs):
        loader = Loader()
        loader.loadAll()
        return super(LoadView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoadView,self).get_context_data(**kwargs)
        context['iTypeList'] = IssueType.objects.all()
        context['iStatusList'] = IssueStatus.objects.all()
        return context

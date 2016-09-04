import datetime
import threading
import urllib
from urllib import parse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .loader import Defs
from .models import Issue
from .models import Comment
from .models import Nickname
from .models import Settings
from .models import EmailQueue
from .models import VoteHistory
from .tokenbuilder import NewUserToken
from .tokenbuilder import VoteConfirmToken
from .notification import Notification

#@csrf_exempt

# notification_type: string as 'NewRequest', 'Comment', 'Vote'

def send_confirmation_mail(user, subject, notification_type):
    secret = Settings.objects.get(id=Defs.TOKEN_CRYPT_SECRET_id).value
    newUserToken = NewUserToken().tokenize(secret, notification_type, user.email, user.id)
    newUserToken = urllib.parse.quote(newUserToken)
    forumUri = Settings.objects.get(id=Defs.BASE_URI_id).value
    forumName = Settings.objects.get(id=Defs.FORUM_NAME_id).value
    newUserConfirmationUri = '{0}/confirm/?token={1}'.format(forumUri,newUserToken)
    varCollection = [['#Nickname#', user.nick],
                    ['#RequestForumUri#',forumUri],
                    ['#LinkConfirmation#',newUserConfirmationUri],
                    ['#RequestForumName#', forumName],
                    ['#UserEmail#', user.email]]
    notification = Notification()
    if (notification_type == 'NewRequest'):
        notification.send(user.email, subject, 'notif_newuser', varCollection)
    elif (notification_type == 'Comment'):
        notification.send(user.email, subject, 'notif_newuser', varCollection)


_locker = threading.Lock()
class EmailQueueUtils:
    @staticmethod
    def send_mail(item):
        user = item.to
        if not user.confirmed:
            return
        forumUri = Settings.objects.get(id=Defs.BASE_URI_id).value
        forumName = Settings.objects.get(id=Defs.FORUM_NAME_id).value
        varCollection = [['#Nickname#', user.nick],
                        ['#RequestForumUri#',forumUri],
                        ['#RequestForumName#',forumName],
                        ['#Header#', item.header],
                        ['#Description#', item.description]]
        notification = Notification()
        if (item.etype == EmailQueue.TP_NEWREQUEST):
            notification.send(user.email, 'New Request Posted', 'notif_newrequest', varCollection)
        elif (item.etype == EmailQueue.TP_NEWCOMMENT):
            notification.send(user.email, 'New Comment Posted', 'notif_newcomment', varCollection)

    @staticmethod
    def remove_old_items_from_queue():
        return

    @staticmethod
    def process_queue():
        if not hasattr(EmailQueueUtils.process_queue, 'running_count'):
            EmailQueueUtils.process_queue.running_count = 0
        if EmailQueueUtils.process_queue.running_count > 0:
            return

        can_run = False
        with _locker:
            EmailQueueUtils.process_queue.running_count += 1
            if EmailQueueUtils.process_queue.running_count == 1:
                can_run = True

        if can_run:
            EmailQueueUtils.remove_old_items_from_queue()
            exception_count = 0
            while True:
                try:
                    item = EmailQueue.objects.filter(to__confirmed=True).order_by('id')[:1].get()
                    EmailQueueUtils.send_mail(item)
                    item.delete()
                except EmailQueue.DoesNotExist:
                    break
                except Exception as ex:
                    print('Exception {0}', ex)
                    exception_count += 1
                    if exception_count > 10:
                        break
                    pass
        with _locker:
            EmailQueueUtils.process_queue.running_count -= 1

    # enqueue_type: must follow consts in EmailQueue
    # header: issue title
    # description: issue or comment message
    @staticmethod
    def enqueue_mail(user, enqueue_type, header, description):
        enqueue = EmailQueue()
        enqueue.to = user
        enqueue.etype = enqueue_type
        enqueue.header = header
        enqueue.description = description
        enqueue.date = datetime.datetime.utcnow()
        enqueue.save()
        EmailQueueUtils.process_queue()

class Commands():
    def IssueRequestCommand(request):
        if request.method == 'POST':
            form = IssueRequestForm(request.POST)
            if form.is_valid():
                try:
                    form.new(request)
                except Exception as ex:
                    print('Error {0}'.format(ex))
                    return HttpResponse('Value Error')
            else:
                print(form.errors)
                return HttpResponse(form.errors.items(), status=500)
        return HttpResponse('ok')


    def VoteCommand(request):
        if request.method == 'POST':
            form = VoteConfirmationForm(request.POST)
            if form.is_valid():
                try:
                    form.new()
                except Exception as ex:
                    print('Error {0}'.format(ex))
                    return HttpResponse('Value Error')
            else:
                print('VoteConfirmationForm not valid')
        return HttpResponse('ok')


    def CommentCommand(request):
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                try:
                    form.new(request)
                except Exception as ex:
                    print('Error {0}'.format(ex))
                    return HttpResponse('Value Error')
            else:
                print('CommentForm not valid')
        return HttpResponse('ok')


    def UpdateIssueCommand(request):
        if request.method == 'POST' and request.user.is_authenticated():
            form = IssueRequestForm(request.POST)
            if form.is_valid():
               try:
                   form.update()
               except Exception as ex:
                   print('Error {0}'.format(ex))
                   return HttpResponse('Value Error')
            else:
               print('UpdateIssue not valid')
               return HttpResponse(form.errors.items(),status=500)
        return HttpResponse('ok')

    def DeleteIssueCommand(request):
        if request.method == 'POST' and request.user.is_authenticated():
            form = IssueRequestForm(request.POST)
            if form.is_valid():
               try:
                   form.delete()
               except Exception as ex:
                   print('Error {0}'.format(ex))
                   return HttpResponse('Value Error')
            else:
               print('DeleteIssue not valid')
        return HttpResponse('ok')

    def UpdateCommentCommand(request):
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                try:
                    form.update()
                except Exception as ex:
                    print('Error {0}'.format(ex))
                    return HttpResponse('Value Error')
            else:
                print('UpdateCommentForm not valid')
                return HttpResponse(form.errors.items(),status=500)
        return HttpResponse('ok')

    def DeleteCommentCommand(request):
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                try:
                    form.delete()
                except Exception as ex:
                    print('Error {0}'.format(ex))
                    return HttpResponse('Value Error')
            else:
                print('DeleteCommentForm not valid')
        return HttpResponse('ok')



class IssueRequestForm(forms.Form):
    inIssueId = forms.IntegerField(required=False)
    inStatus = forms.CharField(max_length=32, required=False)
    inVisibility = forms.CharField(max_length=32, required=False)
    inType = forms.CharField(max_length=32,required=False)
    inEmail = forms.CharField(max_length=128,required=False)
    inNick = forms.CharField(max_length=64,required=False)
    inTitle = forms.CharField(max_length=256, required=False)
    inMessage = forms.CharField(max_length=4096, required=False)

    def clean_inVisibility(self):
        v = self.cleaned_data['inVisibility']
        if len(v) > 0 and  v.lower() != 'public' and v.lower() != 'private':
            raise forms.ValidationError('Invalid inVisibility')
        return v

    def clean_inNick(self):
        _email = self.cleaned_data['inEmail']
        try:
            nickname = Nickname.objects.get(nick=self.cleaned_data['inNick'])
            if nickname.email != _email:
                raise forms.ValidationError('This email doesn''t owns the nickname have choosen. Try another one.')
        except Nickname.DoesNotExist:
            return self.cleaned_data['inNick']
        return nickname.nick

    def send_confirmation_mail(self, user):
        send_confirmation_mail(user, 'New User Confirmation', 'NewRequest')

    def delete(self):
        _id = self.cleaned_data['inIssueId']
        issue = Issue.objects.get(id=_id)
        issue.delete()

    def update(self):
        _id = self.cleaned_data['inIssueId']
        _status = self.cleaned_data['inStatus']
        _visibility = self.cleaned_data['inVisibility']
        _title = self.cleaned_data['inTitle']
        _description = self.cleaned_data['inMessage']

        try:
            issue = Issue.objects.get(id=_id)
        except:
            raise ValidationError('Unable to find Issue')

        if len(_status) > 0:
            issue.status = _status
        if len(_visibility) > 0:
            if _visibility.lower() == 'public':
                issue.public = True
            else:
                issue.public = False
        if len(_title) > 0:
            issue.title = _title
        if len(_description) > 0:
            issue.description = _description

        issue.save()

    def new(self, request):
        _type = self.cleaned_data['inType']
        _nick = self.cleaned_data['inNick']
        _email = self.cleaned_data['inEmail']
        _title = self.cleaned_data['inTitle']
        _description = self.cleaned_data['inMessage']

        issue = Issue()
        issue.nick = _nick
        issue.issueType = _type
        issue.email = _email
        issue.title = _title
        issue.description = _description
        issue.date = datetime.datetime.utcnow()
        issue.status = 'New'
        issue.votesCount = 1
        if request.user.is_authenticated():
            issue.public = True
        else:
            issue.public = Settings.objects.get(id=Defs.DEFAULT_VISIBILITY)

        try:
            nickname = Nickname.objects.get(nick=_nick)
            if nickname.email != _email:
                raise ValidationError('This email doesn''t owns the nickname have choosen. Try another one.')

            if nickname.confirmed == False:
                self.send_confirmation_mail(nickname)
        except Nickname.DoesNotExist:
            nickname = Nickname()
            nickname.nick = _nick
            nickname.email = _email
            nickname.confirmed = False
            nickname.save()

        nickname = Nickname.objects.get(nick=_nick)
        issue.nickObj = nickname
        issue.save()

        self.send_confirmation_mail(nickname)
        EmailQueueUtils.enqueue_mail(nickname, EmailQueue.TP_NEWREQUEST, _title, _description)


class VoteConfirmationForm(forms.Form):
    inNick = forms.CharField(max_length=64)
    inEmail = forms.CharField(max_length=128)
    inIssueId = forms.IntegerField()

    def clean_nick(self):
        inNick = self.cleaned_data['inNick']
        return inNick

    def clean_email(self):
        inEmail = self.cleaned_data['inEmail']
        return inEmail

    def send_confirmation_mail(self, user, issueId):
        secret = Settings.objects.get(id=Defs.TOKEN_CRYPT_SECRET_id).value
        voteToken = VoteConfirmToken().tokenize(secret, user.email, user.id, issueId)
        voteToken = urllib.parse.quote(voteToken)
        forumUri = Settings.objects.get(id=Defs.BASE_URI_id).value
        forumName = Settings.objects.get(id=Defs.FORUM_NAME_id).value
        voteConfirmationUri = '{0}/vote/?token={1}'.format(forumUri,voteToken)
        issueName = Issue.objects.get(id=issueId).title
        varCollection = [['#Nickname#', user.nick],
                        ['#RequestForumUri#',forumUri],
                        ['#LinkConfirmation#',voteConfirmationUri],
                        ['#RequestForumName#',forumName],
                        ['#UserEmail#', user.email],
                        ['#IssueName#', issueName]]
        notification = Notification()
        notification.send(user.email, 'Vote Confirmation', 'notif_vote', varCollection)

    def new(self):
        _nick = self.cleaned_data['inNick']
        _email = self.cleaned_data['inEmail']
        inIssueId = self.cleaned_data['inIssueId']

        issue = Issue.objects.get(id=inIssueId)

        try:
            nickname = Nickname.objects.get(nick=_nick,email=_email)
            self.send_confirmation_mail(nickname, issue.id)
            return True
        except Nickname.DoesNotExist:
            pass

        nickname = Nickname()
        nickname.nick = _nick
        nickname.email = _email
        nickname.confirmed = False
        nickname.save()
        nickname = Nickname.objects.get(nick=_nick)
        self.send_confirmation_mail(nickname, issue.id)
        return False


class CommentForm(forms.Form):
    inCommentId = forms.IntegerField(required=False)
    inEmail = forms.CharField(max_length=128, required=False)
    inNick = forms.CharField(max_length=64, required=False)
    inMessage = forms.CharField(max_length=4096, required=False)
    inPublic = forms.BooleanField(required=False)
    inIssueId = forms.IntegerField(required=False)

    def clean_inNick(self):
        _email = self.cleaned_data['inEmail']
        try:
            nickname = Nickname.objects.get(nick=self.cleaned_data['inNick'])
            if nickname.email != _email:
                raise forms.ValidationError('This email doesn''t owns the nickname have choosen. Try another one.')
        except Nickname.DoesNotExist:
            return self.cleaned_data['inNick']
        return nickname.nick


    def send_confirmation_mail(self, user):
        send_confirmation_mail(user, 'New User Confirmation', 'Comment')

    def new(self, request):
        _nick = self.cleaned_data['inNick']
        _email = self.cleaned_data['inEmail']
        _message = self.cleaned_data['inMessage']
        inIssueId = self.cleaned_data['inIssueId']

        issue = Issue.objects.get(id=inIssueId)
        try:
            nickname = Nickname.objects.get(nick=_nick)
            if nickname.email != _email:
                raise ValidationError('This email doesn''t owns the nickname have choosen. Try another one.')

            if nickname.confirmed == False:
                self.send_confirmation_mail(nickname)

        except Nickname.DoesNotExist:
            print('Comment Nick DoesNotExist')
            nickname = Nickname()
            nickname.nick = _nick
            nickname.email = _email
            nickname.confirmed = False
            nickname.save()
            nickname = Nickname.objects.get(nick=_nick)
            self.send_confirmation_mail(nickname)

        comment = Comment()
        comment.nickObj = nickname
        comment.issueObj = issue
        comment.nick = nickname.nick
        comment.text = _message
        if request.user.is_authenticated():
            comment.public = True
        else:
            comment.public = Settings.objects.get(id=Defs.DEFAULT_VISIBILITY)

        comment.date = datetime.datetime.utcnow()
        comment.save()
        EmailQueueUtils.enqueue_mail(nickname, EmailQueue.TP_NEWCOMMENT, issue.title, _message)

    def update(self):
        _id = self.cleaned_data['inCommentId']
        _text = self.cleaned_data['inMessage']
        _public = self.cleaned_data['inPublic']

        comment = Comment.objects.get(id=_id)
        if len(_text) > 0:
            comment.text = _text
        if _public != None:
            comment.public = _public

        comment.save()

    def delete(self):
        _id = self.cleaned_data['inCommentId']

        comment = Comment.objects.get(id=_id)
        comment.delete()

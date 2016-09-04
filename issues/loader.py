import random
from .models import Issue
from .models import IssueType
from .models import IssueStatus
from .models import Settings

class Defs(object):
    IS_LOADED_id = 1
    SMTP_SERVER_id = 2
    SMTP_PORT_id = 3
    SMTP_SSL_id = 4
    SMTP_USER_id = 5
    SMTP_PWD_id = 6
    SMTP_SENDER_id = 7
    BASE_URI_id = 8
    NEWUSER_CONFIRM_URI_id = 9
    TOKEN_CRYPT_SECRET_id = 10
    FORUM_NAME_id = 11
    ROOT_PATH_id = 12
    DEFAULT_VISIBILITY = 13


class Loader(object):
    def flagAsLoaded(self):
        loaded = Settings()
        loaded.setup(Defs.IS_LOADED_id, 'IsLoaded', 'true')
        loaded.save()

    def loadTypes(self):
        types = ['Issue','Doubt','Question','Suggestion','Other']
        for t in types:
            itype = IssueType()
            itype.name = t
            itype.save()

    def loadStatuses(self):
        status = ['New','Done','Duplicated','In progress','Testing','Canceled','Closed']
        for s in status:
            istatus = IssueStatus()
            istatus.name = s
            istatus.save()

    def loadSMTPSettings(self):
        s = Settings()
        s.setup(Defs.SMTP_SERVER_id,'SMTP Server','')
        s.save()
        s = Settings()
        s.setup(Defs.SMTP_PORT_id,'Port','25')
        s.save()
        s = Settings()
        s.setup(Defs.SMTP_SSL_id,'SSL Enabled','')
        s.save()
        s = Settings()
        s.setup(Defs.SMTP_USER_id,'User','')
        s.save()
        s = Settings()
        s.setup(Defs.SMTP_PWD_id,'Password(*)','')
        s.save()
        s = Settings()
        s.setup(Defs.SMTP_SENDER_id,'Sender','')
        s.save()

    def loadAll(self):
        try:
            isLoaded = Settings.objects.get(id=1)
        except:
            self.flagAsLoaded()
            self.loadTypes()
            self.loadStatuses()
            self.loadSMTPSettings()
            s = Settings()
            s.setup(Defs.BASE_URI_id,'BaseUri','http://localhost/issues/')
            s.save()
            s = Settings()
            s.setup(Defs.NEWUSER_CONFIRM_URI_id,'New User Confirmation Uri','http://localhost/issues/confirmed/?token={0}')
            s.save()
            s = Settings()
            s.setup(Defs.TOKEN_CRYPT_SECRET_id,'Token Crypto Key(*)',random.randint(1000000,2000000))
            s.save()
            s = Settings()
            s.setup(Defs.FORUM_NAME_id,'Forum Name','Request Forum')
            s.save()
            s = Settings()
            s.setup(Defs.ROOT_PATH_id,'Installed Path','./issues/')
            s.save()
            s.setup(Defs.DEFAULT_VISIBILITY, 'Default Visibilty', 'True')
            s.save()

from django.test import TestCase
from .notification import Notification
from .models import Settings
from .loader import Defs
from .tokenbuilder import NewUserToken

# Create your tests here


class NotificationTestCase(TestCase):
    varCollection = [['#Nickname#','Iam Nick'],
                     ['#RequestForumUri#','http://localhost/xpto'],
                     ['#LinkConfirmation#','http://localhost/confirmation/xpto'],
                     ['#RequestForumName#','Whoa Who Forum'],
                     ['#UserEmail#','mymail@whoawho.forum']]
    def setUp(self):
        print('testing...')
        s = Settings()
        s.setup(Defs.SMTP_SERVER_id,'SMTP Server','192.168.0.47')
        s.save()
        s = Settings()
        s.setup(Defs.SMTP_PORT_id,'Port','25')
        s.save()
        s = Settings()
        s.setup(Defs.SMTP_SSL_id,'SSL Enabled','false')
        s.save()
        s = Settings()
        s.setup(Defs.SMTP_USER_id,'User','')
        s.save()
        s = Settings()
        s.setup(Defs.SMTP_PWD_id,'Password','')
        s.save()
        s = Settings()
        s.setup(Defs.SMTP_SENDER_id,'Sender','sxavier@somesendersample.com')
        s.save()
        s = Settings()
        s.setup(Defs.ROOT_PATH_id,'Root Path','./issues')
        s.save()

    def test_variables_must_be_converted(self):
        n = Notification()
        n.process_template('notif_newuser', self.varCollection)
        txtHasVar = n.text.find('#')
        htmlHasVar = n.html.find('#')
        self.assertEqual(txtHasVar, -1)
        self.assertEqual(htmlHasVar, -1)

    def test_notification_must_send_email_for_new_users(self):
        n = Notification()
        n.send('sxavier@somemail.com',
               'Notification Test',
               'notif_newuser',
               self.varCollection)

class NewUserTokenTestCase(TestCase):
    def test_token_must_be_encoded_and_decoded(self):
        token = NewUserToken()
        encoded_str = token.tokenize('1234567890', 'NewRequest', 'email@testemail.test', 1)
        token.read_token('1234567890', encoded_str)
        self.assertEqual('email@testemail.test', token.email)
        self.assertEqual(1, token.userid)

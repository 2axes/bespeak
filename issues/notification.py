import smtplib
import urllib

from urllib import parse

from .loader import Defs
from .models import Settings

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Notification(object):
    text = ''
    html = ''

    def process_template(self, templateName, varCollection):
        rootPath = Settings.objects.get(id=Defs.ROOT_PATH_id).value
        templatePath = '{0}/templates/issues/{1}.txt'.format(rootPath,templateName)
        with open(templatePath, 'r') as templatefile:
            self.text = templatefile.read()

        templatePath = '{0}/templates/issues/{1}.html'.format(rootPath,templateName)
        with open(templatePath, 'r') as templatefile:
            self.html = templatefile.read()

        for var in varCollection:
            self.text = self.text.replace(var[0], var[1])
            self.html = self.html.replace(var[0], var[1])

    def send(self, to, subject, templateName, varCollection):
        self.process_template(templateName, varCollection)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = Settings.objects.get(id=Defs.SMTP_SENDER_id).value
        msg['To'] = to
        part1 = MIMEText(self.text, 'plain')
        part2 = MIMEText(self.html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        smtpserver = Settings.objects.get(id=Defs.SMTP_SERVER_id).value
        sender = Settings.objects.get(id=Defs.SMTP_SENDER_id).value
        user = Settings.objects.get(id=Defs.SMTP_USER_id).value
        pwd = Settings.objects.get(id=Defs.SMTP_PWD_id).value
        ssl = Settings.objects.get(id=Defs.SMTP_SSL_id).value
        port = Settings.objects.get(id=Defs.SMTP_PORT_id).value
        server = '{0}:{1}'.format(smtpserver,port)

        if (ssl == 'true'):
            s = smtplib.SMTP_SSL(server)
        else:
            s = smtplib.SMTP(server)
        if (user != '') or (pwd != ''):
            s.login(user, pwd)
        s.sendmail(sender, to, msg.as_string())
        s.quit()

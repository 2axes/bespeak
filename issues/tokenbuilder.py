from .models import Nickname
from Crypto.Cipher import AES
import base64
import os

class NewUserToken(object):
    BLOCK_SIZE = 32
    PADDING = '{'
    email = ''
    tokenfor = ''
    userid = 0

    def tokenize(self, secret, tokenfor, email, userid):
        pad = lambda s: s + ((self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * self.PADDING)
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        secret = secret.rjust(self.BLOCK_SIZE, self.PADDING)
        cipher = AES.new(secret)
        text = '{0}|{1}|{2}|'.format(email, userid, tokenfor)
        encoded = EncodeAES(cipher, text)
        return encoded

    def read_token(self, secret, stuff):
        secret = secret.rjust(self.BLOCK_SIZE, self.PADDING)
        cipher = AES.new(secret)
        decoded = cipher.decrypt(base64.b64decode(stuff)).decode('utf-8').rstrip(self.PADDING)
        parts = decoded.split('|')
        self.email = parts[0]
        self.userid = int(parts[1])
        self.tokenfor = parts[2]
        return self.userid

    # Validate the token for NewUser confirmation
    # After validation the fields email, userid and tokenfor are filled out
    #   and can be used to get user's information
    def validate(self, secret, stuff):
        self.read_token(secret, stuff)
        try:
            nick = Nickname.objects.get(id=self.userid)
            if (nick.email.lower() == self.email.lower()):
                return True
        except Exception as err:
            print('User not Found: {0}'.format(err))
            return False
        return False

class VoteConfirmToken(object):
    BLOCK_SIZE = 32
    PADDING = '{'
    email = ''
    tokenfor = 'Vote'
    userid = 0
    issueId = 0

    def tokenize(self, secret, email, userid, issueId):
        pad = lambda s: s + ((self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * self.PADDING)
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        secret = secret.rjust(self.BLOCK_SIZE, self.PADDING)
        cipher = AES.new(secret)
        text = '{0}|{1}|{2}|{3}'.format(email, userid, 'Vote', issueId)
        encoded = EncodeAES(cipher, text)
        return encoded

    def read_token(self, secret, stuff):
        secret = secret.rjust(self.BLOCK_SIZE, self.PADDING)
        cipher = AES.new(secret)
        decoded = cipher.decrypt(base64.b64decode(stuff)).decode('utf-8').rstrip(self.PADDING)
        parts = decoded.split('|')
        self.email = parts[0]
        self.userid = int(parts[1])
        self.tokenfor = parts[2]
        self.issueId = parts[3]
        return self.userid

    # Validate the token for Vote confirmation
    # After validation the fields email, userid, tokenfor and issueId are filled out
    #   and can be used to get vote's information
    def validate(self, secret, stuff):
        self.read_token(secret, stuff)
        try:
            nick = Nickname.objects.get(id=self.userid)
            if (nick.email.lower() == self.email.lower()):
                return True
        except Exception as err:
            print('User not Found: {0}'.format(err))
            return False
        return False

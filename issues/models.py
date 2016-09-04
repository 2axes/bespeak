from django.db import models

# Create your models here


class Nickname(models.Model):
    id = models.AutoField(primary_key=True)
    nick = models.CharField(max_length=64)
    email = models.CharField(max_length=128)
    confirmed = models.BooleanField()

class Issue(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    issueType = models.CharField(max_length=32)
    nick = models.CharField(max_length=64)
    nickObj = models.ForeignKey(Nickname)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=4096)
    votesCount = models.IntegerField()
    status = models.CharField(max_length=32)
    public = models.BooleanField()

    class Meta:
        ordering = ('-date',)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    issueObj = models.ForeignKey(Issue, related_name='comments', on_delete=models.CASCADE)
    date = models.DateTimeField()
    text = models.CharField(max_length=4096)
    nick = models.CharField(max_length=64)
    nickObj = models.ForeignKey(Nickname)
    public = models.BooleanField()

    class Meta:
        ordering = ('date',)


class Settings(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    value = models.CharField(max_length=1024)

    def setup(self, id, name, value):
        self.id = id
        self.name = name
        self.value = value

    def __str__(self):
        if self.name.find('(*)') != -1:
            return '%s: %s' % (self.name, '******')
        return '%s: %s' % (self.name, self.value)

    class Meta:
        verbose_name_plural = 'Settings'


class VoteHistory(models.Model):
    issueObj = models.ForeignKey(Issue, related_name='issues', on_delete=models.CASCADE)
    email = models.CharField(max_length=128)


class IssueStatus(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name = "Issue Status"
        verbose_name_plural = "Issue Statuses"

        def __str__(self):
            return self.name


class IssueType(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name = "Issue Type"
        verbose_name_plural = "Issue Types"

        def __str__(self):
            return self.name


class EmailQueue(models.Model):
    TP_NEWCOMMENT = 1
    TP_NEWREQUEST = 2

    to = models.ForeignKey(Nickname, related_name='nickname', on_delete=models.CASCADE)
    etype = models.IntegerField()
    header = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    date = models.DateTimeField()

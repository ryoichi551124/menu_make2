from django.db import models
from django.contrib.auth import get_user_model

class Test(models.Model):
    name = models.CharField(max_length=50, null=True)
    mail = models.EmailField(max_length=100)
    sub_list = models.CharField(max_length=1000, null=True)
    soup_list = models.CharField(max_length=1000, null=True)
    mainNum = models.IntegerField(null=True)
    subNum = models.IntegerField(null=True)
    soupNum = models.IntegerField(null=True)
    judge = models.BooleanField(null=True)

    def __str__(self):
        return 'id: ' + str(self.id) + '、name: ' + str(self.name) + '、主菜: ' + str(self.mainNum) + '、副菜: ' + str(self.subNum) + '、汁物: ' + str(self.soupNum) + '、判定: ' + str(self.judge)


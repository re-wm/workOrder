from django.db import models

from django.contrib.auth.models import AbstractUser

import django.utils.timezone as timezone

class Group(models.Model):
    """
    分组信息
    """
    id = models.AutoField(primary_key=True)
    groupname = models.CharField(verbose_name='组名',max_length=10,unique=True)
    status = models.BooleanField(default=1)
    def __str__(self):
        return self.groupname

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name='登录名',max_length=20,null=False,unique=True)
    nickname = models.CharField(verbose_name='昵称',max_length=20)
    mailbox = models.CharField(verbose_name='邮箱',max_length=32)
    password = models.CharField(verbose_name='密码',null=False,max_length=20)
    status = models.BooleanField(default=1)
    group = models.ForeignKey(verbose_name='所属分组',to='Group',to_field='id',on_delete=models.CASCADE)
    def __str__(self):
        return self.username

class Operator(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='运维名',max_length=20,null=False,unique=True)
    passwd = models.CharField(verbose_name='运维密码',null=False,default='123456',max_length=20)
    is_admin = models.BooleanField(default=1)
    status = models.BooleanField(default=1)
    # onduty = models.IntegerField(default=0)

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    c_name = models.CharField(verbose_name='公司名',unique=True,max_length=20)
    c_code = models.CharField(verbose_name='公司代码',unique=True,max_length=20)
    status = models.BooleanField(default=1)
    def __str__(self):
        return self.c_name

class Workorder(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标题',unique=True,null=False,default='默认标题',max_length=32)
    release_addr = models.CharField(verbose_name='发版地址(SVN/GIT)',max_length=128)
    release_content = models.CharField(verbose_name='发版更新内容',max_length=64)
    release_attention = models.CharField(verbose_name='发版注意事项',max_length=128)
    remark = models.CharField(verbose_name='备注',null=True,max_length=64)
    status = models.BooleanField()
    is_update_db = models.BooleanField()
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    end_time = models.DateTimeField(verbose_name='结束时间',auto_now_add=True)
    order_user = models.ForeignKey(verbose_name='提工单人',to='User',to_field='id',on_delete=models.CASCADE)
    ops = models.ForeignKey(verbose_name='处理工单人',to='Operator',to_field='id',on_delete=models.CASCADE)
    company = models.ManyToManyField(to='Company')
    def __str__(self):
        return self.id


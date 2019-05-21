from django.db import models


# Create your models here.

class User(models.Model):
    gender = (('male', '男'), ('female', '女'),)
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class FormTypes(models.Model):
    types = (('1', '1.调账说明'), ('2', '2.未达账项'), ('3', '3.表单3'), ('4', '表单4'), ('5', '表单5'),)
    months = (('1', '1月',), ('2', '2月',), ('3', '3月',), ('4', '4月',), ('5', '5月',), ('6', '6月',), ('7', '7月',), ('8', '8月',), ('9', '9月',), ('10', '10月',), ('11', '11月',), ('12', '12月',),)
    type = models.CharField(max_length=128, choices=types, default='1')
    month = models.CharField(max_length=128, choices=months, default='1')
    user = models.CharField(max_length=256, default='admin')
    c_time2 = models.DateTimeField(auto_now_add=True)
    n_time = models.CharField(max_length=256, default='upload_time')

    def __str__(self):
        return '-'.join(self.type, self.month)

    class Meta:
        ordering = ['c_time2']
        verbose_name = '文件'
        verbose_name_plural = '文件'

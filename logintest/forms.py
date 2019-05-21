from django import forms
from captcha.fields import CaptchaField
import datetime

class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length= 128, widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='密码', max_length= 256, widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

class RegisterForm(forms.Form):
    gender = (('male','男'), ('female','女'),)
    username = forms.CharField(label='用户名', max_length= 128, widget = forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='邮箱地址', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')

month = datetime.datetime.now().month
class TypeForm(forms.Form):
    types = (('1', '1.调账说明'), ('2', '2.银行未达账项'), ('3', '3.组织架构及共享分工明细'), ('4', '4.融资费用缺失发票'), ('5', '5.金蝶报表制作问题'),('6', '6.2018年报调整账套'),)
    months = (('1', '1月',), ('2', '2月',), ('3', '3月',), ('4', '4月',), ('5', '5月',), ('6', '6月',), ('7', '7月',), ('8', '8月',), ('9', '9月',), ('10', '10月',), ('11', '11月',), ('12', '12月',),)
    type = forms.ChoiceField(label='种类', choices=types)
    month = forms.ChoiceField(label='月份', choices=months, initial=month)

class ChPswdForm(forms.Form):
    username = forms.CharField(label='用户名', max_length= 128, widget = forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='旧密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='新密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password3 = forms.CharField(label='确认新密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
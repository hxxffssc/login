from django.shortcuts import render, redirect, HttpResponse
import os
from . import models
from .forms import UserForm, RegisterForm, TypeForm, ChPswdForm
import hashlib
import datetime
import pandas as pd
from django.http import FileResponse
from pandas import Series, DataFrame
import xlrd
import xlwt
import openpyxl

# Create your views here.
def index(request):
    pass
    return render(request, 'login/index.html', locals())

def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        message = '请检查填写内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name = username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = '密码不正确！'
            except:
                message = '用户不存在！'
        return render(request,'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')

def verify_file(uploaded_file_path, model_file_path):
    try:
        u_file = pd.ExcelFile(uploaded_file_path)
        u_df = u_file.parse(u_file.sheet_names[0])
    except:
        return 3  #'上传表格类型有误'
    try:
        m_file = pd.ExcelFile(model_file_path)
        m_df = m_file.parse(u_file.sheet_names[0])
    except:
        return 0   #'表格类型或月份选错'

    if len(u_file.sheet_names) >1:
        return 4   #超过1个工作表

    if set(u_df.columns) == set(m_df.columns):
        return 1  #'正确'
    else:
        return 2  #'上传表格与模板不同'

def upload(request):

    if request.method == 'GET':
        type_form = TypeForm()
        return render(request, 'login/upload.html', locals())

    if request.method == 'POST':
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        type_form = TypeForm(request.POST)
        if type_form.is_valid():  # 获取数据
            type = type_form.cleaned_data['type']
            month = type_form.cleaned_data['month']

        new_file = models.FormTypes.objects.create()
        new_file.type = type
        new_file.month = month
        new_file.user = request.session['user_name']
        new_file.n_time = timestamp
        new_file.save()
        folder = 'C:\\Users\\Administrator\\PycharmProjects\\login\\logintest\\uploadedfiles'
        obj = request.FILES.get('tiaozhang')
        f = open(os.path.join(folder, timestamp + obj.name), 'wb')
        for line in obj.chunks():
            f.write(line)
        f.close()
        model_dir = 'C:\\Users\\Administrator\\PycharmProjects\\login\\logintest\\uploadedfiles\\model_file'
        model_name = '%s_%s.xlsx'%(type, month)
        if verify_file(os.path.join(folder, timestamp + obj.name), os.path.join(model_dir, model_name)) == 1:
            message = '上传成功！'
        else:
            if verify_file(os.path.join(folder, timestamp + obj.name), os.path.join(model_dir, model_name)) == 0:
                message = '上传不成功！类型或月份选错；'
            elif verify_file(os.path.join(folder, timestamp + obj.name), os.path.join(model_dir, model_name)) == 2:
                message = '上传不成功！上传表格与模板表头不同；'
            elif verify_file(os.path.join(folder, timestamp + obj.name), os.path.join(model_dir, model_name)) == 3:
                message = '上传不成功！不是Excel文件；'
            elif verify_file(os.path.join(folder, timestamp + obj.name), os.path.join(model_dir, model_name)) == 4:
                message = '上传不成功！Excel文件多于1个表格，只需上传1个表格的Excel文件；'

            os.remove(os.path.join(folder, timestamp + obj.name))

        return render(request, 'login/upload.html', locals())

    type_form = TypeForm()
    return render(request, 'login/upload.html', locals())

def register(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())

def hash_code(s, salt = 'salty'):
    h = hashlib.sha256()
    s = str(s) + salt
    h.update(s.encode('utf-8'))
    return h.hexdigest()


def merger_file(files_starters , root_dir, to_down, type, month):
    files = os.listdir(root_dir)
    path_list = []
    ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    for file in files:
        for starters in files_starters:
            if file.startswith(starters[0]):
                path = os.path.join(root_dir, file)
                path_list += [(path, starters[1])]

    if len(path_list) != 0:
        for i, single_path in enumerate(path_list):
            tb = pd.ExcelFile(single_path[0])
            name = tb.sheet_names[0]
            df = tb.parse(name)
            df['上传人'] = single_path[1]
            joined = pd.concat([joined, df]) if i else df
        filename = '%s-%s-%s.xls'%(str(type),str(month), ts )
        joined.to_excel(os.path.join(to_down, filename))
        return filename

    else:
        return 0

def get_max_id(files_starters):
    df = pd.DataFrame(files_starters, columns=['time','user','id'])
    df_g = df[['user','id']].groupby(by = 'user', as_index= False).max()
    df_m = pd.merge(df_g, df, on = ['user','id'],how='left')
    return [(df_m.loc[i, 'time'], df_m.loc[i, 'user'],df_m.loc[i, 'id']) for i in df_m.index]

def integrate(request):
    root_dir = 'C:\\Users\\Administrator\\PycharmProjects\\login\\logintest\\uploadedfiles'
    to_down = 'C:\\Users\\Administrator\\PycharmProjects\\login\\logintest\\to_down'
    if request.method == 'GET':
        type_form = TypeForm()
        return render(request, 'login/integrate.html', locals())

    if request.method == 'POST':
        type_form = TypeForm(request.POST)
        if type_form.is_valid():
            type = type_form.cleaned_data['type']
            month = type_form.cleaned_data['month']

        files_starters_sets = models.FormTypes.objects.filter(type = type, month = month)
        files_starters = [(f.n_time, f.user, f.pk) for f in files_starters_sets]
        files_starters = get_max_id(files_starters)
        try:
            f_name = merger_file(files_starters, root_dir, to_down, type, month)
        except:
            message = '合并文件时出错，请联系管理员！'
            return render(request, 'login/integrate.html', locals())

        if f_name != 0:
            fileopen = open(to_down + '\\' + f_name, 'rb')
            response = FileResponse(fileopen)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="%s"' % f_name
            return response

        else:
            message = '没有可以合并的文件！'
            return render(request, 'login/integrate.html', locals())

    type_form = TypeForm()
    return render(request, 'login/integrate.html', locals())

def chpswd(request):
    if request.method == "GET":
        c_form = ChPswdForm()
        return render(request, 'login/chpswd.html', locals())
    if request.method == "POST":
        c_form = ChPswdForm(request.POST)
        message = "请检查填写的内容！"
        if c_form.is_valid():  # 获取数据
            username = c_form.cleaned_data['username']
            password1 = c_form.cleaned_data['password1']
            password2 = c_form.cleaned_data['password2']
            password3 = c_form.cleaned_data['password3']
            #判断旧密码
            user = models.User.objects.get(name = username)
            if user.password != hash_code(password1):
                message = "旧密码有误！"
                return render(request, 'login/chpswd.html', locals())

            else:
                if password2 != password3:  # 判断两次密码是否相同
                    message = "两次输入的密码不同！"
                    return render(request, 'login/chpswd.html', locals())

                else:
                    models.User.objects.filter(name=username).update(password = hash_code(password2))
                    message = "密码修改成功，下次登录时请使用新密码！"
                    return render(request, 'login/login.html', locals())

def check(request):
    if request.method == 'GET':
        type_form = TypeForm()
        return render(request, 'login/check.html', locals())

    if request.method == 'POST':
        type_form = TypeForm(request.POST)
        if type_form.is_valid():
            type = type_form.cleaned_data['type']
            month = type_form.cleaned_data['month']

        files_users = models.FormTypes.objects.filter(type = type, month = month)
        dup_users = [f.user for f in files_users]
        users = set(dup_users)
        all_users_info = models.User.objects.all()
        all_users = [a.name for a in all_users_info]
        left_user = [u for u in all_users if u not in users]

        return render(request, 'login/check.html', locals())
    type_form = TypeForm()
    return render(request, 'login/check.html', locals())


from django.shortcuts import render, redirect
from django.contrib import auth
# from django.contrib.auth.decorators import login_required

import jpush
from jpush import common

and_app_key = 'Android11111'
and_master_secret = 'Android11111'

ios_app_key = 'ios11111'
ios_master_secret = 'ios11111'

app_key = 'all11111'
master_secret = 'all11111'


# Create your views here.
def login(request):
    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('/index/')
        else:
            error_msg = '用户名或密码错误'

    return render(request, 'login.html', {"error_msg": error_msg})


FLAG = False


def login_req(func):
    def inner(request, *args, **kwargs):
        global FLAG
        error_msg = ''
        '''登录程序'''
        if FLAG:
            ret = func(request, *args, **kwargs)
            return ret
        else:
            if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                if username == 'admin' and password == 'asdf@123':
                    FLAG = True
                    ret = func(request, *args, **kwargs)
                    return ret
                else:
                    error_msg = '用户名或密码错误'
        return render(request, 'login.html', {"error_msg": error_msg})

    return inner


# 用户名： admin@cmcc.com
# 密码： password123

def log_out(request):
    # del request.session['username']
    global FLAG
    FLAG = False
    return redirect('/index/')


@login_req
def index(request):
    return render(request, 'index.html')


@login_req
def pushAllIos(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        print(title, content)
        print(type(title), type(content))
        ios_jpush = jpush.JPush(ios_app_key, ios_master_secret)
        push = ios_jpush.create_push()
        ios_jpush.set_logging("DEBUG")
        push.audience = jpush.all_
        raw = {
            "body": content,
            "title": title
        }
        ios_msg = jpush.ios(alert=raw, badge="+1", sound="beep.wav")
        push.notification = jpush.notification(alert=content, ios=ios_msg)
        push.platform = jpush.all_
        push.options = {"apns_production": False}
        try:
            response = push.send()
            print(response, type(response))
            return render(request, 'success.html')
        except common.Unauthorized:
            return render(request, 'failed.html', {"err_msg": "验证失败!"})
            # raise common.Unauthorized("Unauthorized")  # AppKey，Master Secret 错误，验证失败必须改正。
        except common.APIConnectionException:
            return render(request, 'failed.html', {"err_msg": "请求超时!"})
            # raise common.APIConnectionException("conn error")  # 包含错误的信息：比如超时，无网络等情况。
        except common.JPushFailure:
            return render(request, 'failed.html', {"err_msg": "请求出错!"})
            # print("JPushFailure")  # 请求出错，参考业务返回码。
        except:
            return render(request, 'failed.html', {"err_msg": "其他异常!"})
            # print("Exception")
    return render(request, 'iospush.html')


@login_req
def pushAllAndroid(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        print(title, content)
        print(type(title), type(content))
        and_jpush = jpush.JPush(and_app_key, and_master_secret)
        push = and_jpush.create_push()
        and_jpush.set_logging("DEBUG")
        push.audience = jpush.all_
        android_msg = jpush.android(alert=content, title=title)
        push.notification = jpush.notification(alert=content, android=android_msg)
        push.platform = jpush.all_
        try:
            response = push.send()
            print(response, type(response))
            return render(request, 'success.html')
        except common.Unauthorized:
            return render(request, 'failed.html', {"err_msg": "验证失败!"})
            # raise common.Unauthorized("Unauthorized")  # AppKey，Master Secret 错误，验证失败必须改正。
        except common.APIConnectionException:
            return render(request, 'failed.html', {"err_msg": "请求超时!"})
            # raise common.APIConnectionException("conn error")  # 包含错误的信息：比如超时，无网络等情况。
        except common.JPushFailure:
            return render(request, 'failed.html', {"err_msg": "请求出错!"})
            # print("JPushFailure")  # 请求出错，参考业务返回码。
        except:
            return render(request, 'failed.html', {"err_msg": "其他异常!"})
            # print("Exception")
    return render(request, 'androidpush.html')


@login_req
def pushAll(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        print(title, content)
        print(type(title), type(content))
        ios_jpush = jpush.JPush(ios_app_key, ios_master_secret)
        and_jpush = jpush.JPush(and_app_key, and_master_secret)
        ios_push = ios_jpush.create_push()
        and_push = and_jpush.create_push()
        raw = {
            "body": content,
            "title": title
        }
        ios = jpush.ios(alert=raw, badge="+1", sound="beep.wav")
        android = jpush.android(alert=content, title=title)
        ios_push.notification = jpush.notification(alert=content, ios=ios)
        ios_push.options = {"apns_production": False}
        and_push.notification = jpush.notification(alert=content, android=android)
        ios_push.audience = jpush.all_
        and_push.audience = jpush.all_
        ios_push.platform = jpush.all_
        and_push.platform = jpush.all_
        try:
            response = ios_push.send()
            response1 = and_push.send()
            print(response, response1, type(response), type(response1))
            return render(request, 'success.html')
        except common.Unauthorized:
            return render(request, 'failed.html', {"err_msg": "验证失败!"})
            # raise common.Unauthorized("Unauthorized")  # AppKey，Master Secret 错误，验证失败必须改正。
        except common.APIConnectionException:
            return render(request, 'failed.html', {"err_msg": "请求超时!"})
            # raise common.APIConnectionException("conn error")  # 包含错误的信息：比如超时，无网络等情况。
        except common.JPushFailure:
            return render(request, 'failed.html', {"err_msg": "请求出错!"})
            # print("JPushFailure")  # 请求出错，参考业务返回码。
        except:
            return render(request, 'failed.html', {"err_msg": "其他异常!"})
            # print("Exception")
    return render(request, 'allpush.html')

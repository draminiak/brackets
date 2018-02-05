from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .lib.registration import Registration

def test(request):
    return HttpResponse('Hello from Python!') #noqa

def index(request):
    return render(request, 'index.html')

def register(request):
    reg = Registration(request)
    success = reg.process()
    if success:
        return HttpResponseRedirect('/account')
    return render(request, 'registration/index.html', {'form' : reg.form})

@login_required(login_url='/login/')
def account(request):
    return render(request, 'account.html')

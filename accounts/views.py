from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm, PasswordForm
from django.contrib.auth import get_user_model
from django.views.generic import ListView,CreateView, UpdateView,DetailView
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def signin(request):
    if request.user.is_authenticated and get_user_model().objects.get(pk=request.user.id).is_superuser:
        return redirect("/list")
    if request.user.is_authenticated:
        return redirect('theory/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(request, username=username, password=password, backend='accounts.backends.UserBackend')
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = SignInForm(request.POST)
            return render(request, 'login.html', {'form': form})
    else:
        form = SignInForm()
        return render(request, 'login.html', {'form': form})

@login_required
def signup(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password, backend='accounts.backends.UserBackend')
                print(user)
                
                if user is not None:
                    print("NOT")
                    return render(request,'signup.html',{'form':form,'isCreated':1,'message':"User Not Created"})
                else:
                    return render(request,'signup.html',{'form':form,'isCreated':1,'message':"User Created"})
            else:
                return render(request, 'signup.html', {'form': form,'isCreated':1,'message':'Invalid Information'})
        else:
            form = SignUpForm()
            return render(request, 'signup.html', {'form': form,'isCreated':0})
    return redirect('/')

def signout(request):
    logout(request)
    return redirect('/')

class UserListView(ListView):
    queryset=get_user_model().objects.filter(is_superuser=False)
    template_name='user_list.html'
    model=User
    def get(self,request, *args, **kwargs):
        if not get_user_model().objects.get(pk=request.user.id).is_superuser:
            return render(request,"theoryTag/401.html")
        return super().get(request, *args, **kwargs)

@login_required
def change_password(request,pk):
    if not request.user.is_superuser:
        return redirect('/')
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get('user').id
            user = get_user_model().objects.get(pk=id)
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            message = "Password Changed Successfully"
            form = PasswordForm()
            return render(request, 'password_change.html', {'form':form ,'message':message})
        else:
            form = PasswordForm()
            message = "Password Didnt Match"
            return render(request, 'password_change.html', {'form':form ,'message':message})
    else:
        form = PasswordForm()
        return render(request, 'password_change.html', {'form': form})
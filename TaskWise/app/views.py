from django.shortcuts import render
from django.http import HttpResponse
from django import views
from django.contrib.auth import authenticate,login as loginUser,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import redirect
from django.views.generic import TemplateView
from app.forms import TASKForm
from app.models import TASKS
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')

def home(request):
 form = TASKForm()
 tasks = TASKS.objects.all()


 return render(request, 'home.html', context = {'form': form, 'tasks' : tasks})

def login(request):
 if request.method=='GET':
   form = AuthenticationForm()
   context = {
    "form": form
    }

   return render(request, 'login.html', context=context)
 else:
     form = AuthenticationForm(data=request.POST)
     print(form.is_valid())
     if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            loginUser(request, user)
            return redirect('home')
     else:
      context = {
       "form": form
      }

      return render(request, 'login.html', context=context)

def signup(request):
 if request.method == 'GET':
  form = UserCreationForm()
  context = {
   "form": form
  }
  return render(request, 'signup.html', context=context)
 else:
  print(request.POST)
  form = UserCreationForm(request.POST)
  context = {
   "form": form
  }
  if form.is_valid():
   user = form.save()
   print(user)
   if user is not None:
    return redirect('/login')
  else:
   return render(request, 'signup.html', context=context)


@login_required(login_url='login')

def add_tasks(request):
        if request.user.is_authenticated:
         user = request.user
         print(user)
        form=TASKForm(request.POST)
        if form.is_valid():
           print(form.cleaned_data)
           task = form.save(commit=False)
           task.user=user
           task.save()
           print(task)
           return redirect("home")
        else:
              return render(request, 'home.html', context={'form': form})

def delete_tasks(request , id ):
    print(id)
    TASKS.objects.get(pk = id).delete()
    return redirect('home')

def change_status(request ,id ,status):
    task = TASKS.objects.get(pk = id)
    task.status = status
    task.save()
    return redirect('home')

def signout(request):
            logout(request)
            return redirect('login')


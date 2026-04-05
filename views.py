from django.shortcuts import render,redirect
from django.views import View
from .models import List
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
class RegisterToDo(View):
    def get(self,request):
        return render(request,'todolist/register.html')
    def post(self,request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            return render(request, 'todolist/register.html', {
                'error': 'Passwords do not match'
            })
        if User.objects.filter(username=username).exists():
            return render(request, 'todolist/register.html', {
                'error': 'Username already exists'
            })
        if User.objects.filter(email=email).exists():
            return render(request, 'todolist/register.html', {
                'error': 'Email already registered'
            })
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return redirect('login')
class LoginToDo(View):
    def get(self,request):
        return render(request,'todolist/login.html')
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request,username = user_obj.username,password=password)
        except User.DoesNotExist:
            user = None
        if user is not None:
            login(request,user)
            return redirect('inserturl')
        else:
            return render(request,'todolist/login.html', {'error': 'Invalid credentials'})
class InsertToDo(LoginRequiredMixin,View):
    def get(self,request):
        print(request.user)
        print(request.user.is_authenticated)
        return render(request,'todolist/insert.html')
    def post(self,request):
        it = request.POST.get("t")
        l_obj = List.objects.create(user=request.user,item=it)
        return redirect('selecturl')
class SelectToDo(LoginRequiredMixin,View):
    def get(self,request):
        l_obj = l_obj = List.objects.filter(user=request.user)
        return render(request, 'todolist/select.html', {'lists': l_obj})
class UpdateToDo(LoginRequiredMixin,View):
    def get(self,request,pk):
        l = List.objects.get(id=pk, user=request.user)
        return render(request,'todolist/update.html',{'lists':l})
    def post(self,request,pk):
        tname = request.POST.get('uname')
        l_obj = List.objects.get(id=pk, user=request.user)
        l_obj.item = tname
        l_obj.save()
        return redirect('selecturl')
class DeleteToDo(LoginRequiredMixin,View):
    def get(self,request,pk):
        l = List.objects.get(id=pk, user=request.user)
        return render(request,'todolist/delete.html',{'lists':l})
    def post(self,request,pk):
        action = request.POST.get('action')
        if action == 'Yes':
            lists = List.objects.get(id=pk, user=request.user)
            lists.delete()
        return redirect('selecturl')
class LogoutToDo(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')


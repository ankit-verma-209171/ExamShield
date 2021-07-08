from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.urls import reverse
from django.views import View
from mysite.decorators import allowed_users
from .models import Administrator, User
from .forms import (
    UserForm,
    InstituteForm,
    AdministratorForm
)
from utils.random_password import generate_random_password


class Register(View):
    def get(self, request):
        context = {
            'user_form': UserForm(),
            'institute_form': InstituteForm(),
            'administrator_form': AdministratorForm()
        }
        return render(request, 'administrator/register.html', context=context)

    def post(self, request):
        user_form = UserForm(data=request.POST)
        institute_form = InstituteForm(data=request.POST)
        administrator_form = AdministratorForm(data=request.POST)

        # all valid data send by request
        if user_form.is_valid() and institute_form.is_valid() and administrator_form.is_valid():
            # saving user
            user = user_form.save()
            user.set_password(user.password)
            user.is_active = True
            user.is_staff = True
            user.save()

            # saving institute
            institute = institute_form.save()

            # saving administrator
            administrator = administrator_form.save(commit=False)
            administrator.user = user
            administrator.institute = institute
            administrator.save()

            # adding to administrator group
            administrator_group = Group.objects.get(name='administrator')
            administrator_group.user_set.add(administrator.user)

            # redirecting to login page
            return HttpResponseRedirect(reverse('administrator:login'))

        # invalid data sent via request
        context = {
            'user_form': user_form,
            'institute_form': institute_form,
            'administrator_form': administrator_form,
        }
        return render(request, 'administrator/register.html', context=context)


class Login(View):
    def get(self, request):
        return render(request, 'administrator/login.html')

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                return redirect('administrator:dashboard')
            else:
                return render(request, 'administrator/login.html')

        return render(request, 'administrator/login.html')


@allowed_users(allowed_groups=['administrator'])
def create_faculty(request):
    if request.method == 'GET':
        password = generate_random_password()
        print(password)
        context = {
            'user_form': UserForm(initial={'password': password}),
            'password': password,
        }
        return render(request, 'administrator/create-faculty.html', context=context)

    elif request.method == 'POST':
        # getting data to create user
        faculty_username = request.POST.get('username', '')
        faculty_password = request.POST.get('password', '')
        if faculty_username and faculty_password:
            try:
                new_user = User.objects.create_user(username=faculty_username, password=faculty_password)
                messages.success(request, 'User Created Successfully!')
            except IntegrityError as ie:
                # i.e if user exists in database
                messages.error(request, f'User can\'t be created! User with {faculty_username} already exists!')

        return render(request, 'administrator/create-faculty.html')

    # tried requesting page using any other methods
    return HttpResponse('BAD REQUEST')


@allowed_users(allowed_groups=['administrator'])
def create_student(request):
    return render(request, 'administrator/create-student.html')


@allowed_users(allowed_groups=['administrator'])
def edit_institute_profile(request):
    # TODO: update institute profile
    return render(request, 'administrator/edit-institute-profile.html')


@allowed_users(allowed_groups=['administrator'])
def dashboard(request):
    user = request.user

    context = {
        'user': user,
        'total_faculties': Administrator.objects.all().count(),
        'total_subjects': Administrator.objects.all().count(),
        'total_students': Administrator.objects.all().count(),
        'institute': user.administrator.institute,
    }
    return render(request, 'administrator/dashboard.html', context=context)


@login_required(login_url='administrator:login')
def logout(request):
    auth.logout(request)
    return redirect('administrator:login')

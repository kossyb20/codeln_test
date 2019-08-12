from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Person
import re

# Create your views here.

def login(request):
    visitor_ip = request.environ['REMOTE_ADDR']


    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        person = Person.objects.get(ip_address=visitor_ip)
        saved_pass = person.password
        saved_ip = person.ip_address
        failed_attempts = person.fail_login_attempts
        if password != saved_pass:
            if failed_attempts <= 3:
                failed_attempts += 1
                person.fail_login_attempts = failed_attempts
                print('Incorrect Login, Try again. You have {} attempts left' .format(3 - failed_attempts))
            else:
                print('Incorrect Login, Try again in 5 minutes')
                person.fail_login_attempts = 0
                person.save()

        if password == saved_pass and email == person.email:
            person.fail_login_attempts = 0
            person.save()
            print('Success')
            return HttpResponseRedirect('/home')

    return render(request, 'login.html', {})

def signup(request):
    visitor_ip = request.environ['REMOTE_ADDR']
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nums = re.findall(r'[0-9]+', password)
        low_case = re.findall(r'[a-z]+', password)
        char = re.findall(r'[@#$%&]+', password)
        first_two = re.findall(r'^.{0,2}', password)
        try:
            if len(nums[0]) >= 3 and len(low_case[0]) >= 1 and len(char[0]) >= 2 and first_two[0].isupper() == True:
                person = Person()
                person.email = email
                person.password = password
                person.ip_address = visitor_ip
                person.fail_login_attempts = 0
                person.save()
                return HttpResponseRedirect('/home')

            else:
                print(len(nums[0]) > 3, len(low_case[0]) >= 1, len(char[0]) >= 2, first_two[0].isupper() == True)
                print('error. Password must contain at least 3 numbers, 2 symbols, a lowercase letter and two preceeding uppercase letters')
                HttpResponseRedirect('/signup')
        except Exception as e:
            print(e, '. Password must contain at least 3 numbers, 2 symbols, a lowercase letter and two preceeding uppercase letters')
            return HttpResponseRedirect('/login')

        

        

    return render(request, 'signup.html', {})

def home(request):
    return render(request, 'home.html')
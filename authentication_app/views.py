from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required


class LoginView(View):
    """
    This class contain all methods related to login functionality
    """
    def get(self, request):
        """
        - This function simply render the login page to user
        - This function also checked that user is already logged in or not in system
        """
        try:
            return redirect("dashboard") if request.session.get('_auth_user_id') else render(request, 'login.html')
        except Exception as e:
            raise Http404("Does not Exist")

    def post(self, request):
        """
        - This function check authenticate the users.
        - Here we use inbuilt User model
        - authenticate() : 
            -   Use authenticate() to verify a set of credentials.
            -   It takes credentials as keyword arguments, 
                username and password for the default case, checks them against each authentication backend, 
                and returns a User object if the credentials are valid for a backend. 
        - request parameters :
            - username - > username inputed value from user
            - password - > password inputed value from user
        - returns : 
            - render the html page
        """
        try:
            username = request.POST.get('username').strip()
            password = request.POST.get('password')
            if user := auth.authenticate(username=username, password=password):
                try:
                    auth.login(request, user)
                    return redirect('dashboard')
                except:
                    messages.error(request, "something went wrong ... ")
                    return render(request, 'login.html')
            else:
                messages.error(request, "invalid credentials ... ")
                return render(request, 'login.html')
        except:
            raise Http404("Template does not exist")


class LogoutView(View):
    """
    - This class contain all logout related functionality
    """
    def get(self, request):
        """
        - This function logout the current logged in user
        - auth.logout() delete the session object of logged in user
        """
        try:
            auth.logout(request)
            return redirect('login')
        except:
            raise Http404("Does not Exist")


class RegisterView(View):
    """ 
    -  This class contain user registration related functionality
    """
    def get(self,request):
        """  
        - This function render the register page and form
        """
        return render(request,'register.html')

    def post(self,request):
        """ 
        - This function create new user entry in table 
        """
        try:
            fname = request.POST['fname']
            lname = request.POST['lname']
            username = request.POST['username']
            pass1 = request.POST['password1']
            pass2 = request.POST['password2']
            if User.objects.filter(username = username).exists():
                messages.error(request,"Username is already Used ... ")
                return redirect('register')
            if pass1 == pass2:
                user = User.objects.create_user(
                    first_name = fname,
                    last_name = lname,
                    username = username,
                    password = pass1
                )
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request,"Both password are not matching ... ")
                return redirect('register')
        except Exception as e:
            return Http404("Not found")


@login_required(login_url = '/')
def dashboard(request):
    return render(request,'dashboard.html')




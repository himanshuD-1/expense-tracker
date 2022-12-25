from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from .utils import token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading

# Create your views here.
class EmailThread(threading.Thread):
    def __init__(self, email):
       self.email = email
       threading.Thread.__init__(self)
    
    def run(self):
        self.email.send(fail_silently= False)

class EmailValidateView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if email == '':
            return JsonResponse({'email_error': 'Email field cannot be empty!'})

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry Email in use, try another Email '}, status=400)
        return JsonResponse({'email_valid': True})


class UsernameValidateView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characteres'})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use, try another username '})
        return JsonResponse({'username_valid': True})


class RegisterationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):

        # Get User Data
        # Validate user data
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldvalues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                # path to view
                # - getting domain we are on
                # - relatives url to verification
                # - encode uid
                # - token

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': token_generator.make_token(user)})
                
                activate_url = 'http://'+domain+link

                email_subject = 'Activate your account'
                email_body = 'Hi '+user.username+ 'Please use this link to verify your accounts\n' + activate_url
                

                email1 = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [email]
                )

                EmailThread(email1).start()

                messages.success(
                    request, 'Account created successfully...Please Login')

        return render(request, 'authentication/register.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, 'Welcome, ' +
                                 user.username+' you are logged in')
                return redirect('expenses')

            messages.error(request, 'Invalid Credentials, try again')

        messages.error(request, 'Please fill all the fields')

        return render(request, 'authentication/login.html')


class LogOutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = urlsafe_base64_decode(force_str(uidb64))
            user = User.objects.get(pk=id)
            
            if not token_generator.check_token(user,token):
                return redirect('login'+'?message'+'User already exists')
            
            if user.is_active:
                messages.success("Account Activated Successfully")
                return redirect('login')
        
            user.is_active = True
            user.save()
            messages.success("Account Activated Successfully")
            return redirect('login')
            
        
        except Exception as ex:
            pass
        return redirect('login')

class ResetPasswordResetEmail(View):
    def get(self, request):
        return render(request,'authentication/reset-password.html')
    
    def post(self, request):
        email = request.POST['email']
        
        if not validate_email(email):
            messages.error(request, "Please supply a valid email")
            return render(request, 'authentication/reset-password.html')
        
        
        user = User.objects.filter(email=email)
        domain = get_current_site(request).domain
        
            
        if user.exists():
            email_contents ={
                'user': user[0],
                'uidb64':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'domain':get_current_site(request).domain,
                'token' : PasswordResetTokenGenerator().make_token(user[0])
            }
            
            link = reverse('reset-user-password', kwargs={
                                'uidb64': email_contents['uidb64'], 'token':email_contents['token']})
                    
            reset_url = 'http://'+domain+link

            email_subject = 'Password reset Instructions'
            email_body = 'Hi there,Please check this link below to reset your password \n' +reset_url
                    

            email1 = EmailMessage(
            email_subject,
            email_body,
            'noreply@semycolon.com',
            [email]
            )

            EmailThread(email1).start()

            messages.success(
                        request, 'We have sent you an email to reset your password')
        
        return render(request,'authentication/reset-password.html')
    

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context={
            'uidb64':uidb64,
            'token': token
        }
        return render(request, 'authentication/set-newpassword.html',context)

    def post(self,request,uidb64, token):
        context={
            'uidb64':uidb64,
            'token': token
        }
        
        password = request.POST['password1']
        password2 = request.POST['password2']
        
        if password != password2:
            messages.error(request, "Password does not match")
            return render(request, 'authentication/set-newpassword.html',context)
        
        if len(password) < 6:
            messages.error(request, "Password should contains atleast 6 characters")
            return render(request, 'authentication/set-newpassword.html',context)
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            
            messages.success(request, "Password Reseted Successfully..!!")
            return redirect('login')
        
        except Exception as identifier:
            messages.info(request,"Something went wrong")
            return render(request, 'authentication/set-newpassword.html',context)

